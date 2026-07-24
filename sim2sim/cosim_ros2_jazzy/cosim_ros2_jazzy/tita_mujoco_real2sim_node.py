from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

import numpy as np
import yaml

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import Imu, JointState
from std_msgs.msg import Bool, Float32, Float32MultiArray

from cosim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from cosim_ros2_jazzy.obs_builder import ObservationBuilder, quat_wxyz_to_rpy


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"1", "true", "yes", "on"}


MUJOCO_NATIVE_JOINTS = [
    "joint_left_leg_1",
    "joint_left_leg_2",
    "joint_left_leg_3",
    "joint_left_leg_4",
    "joint_right_leg_1",
    "joint_right_leg_2",
    "joint_right_leg_3",
    "joint_right_leg_4",
]

REAL_TO_NATIVE = {
    "joint_left_leg_1": 0,
    "joint_left_leg_2": 1,
    "joint_left_leg_3": 2,
    "joint_left_leg_4": 3,
    "joint_right_leg_1": 4,
    "joint_right_leg_2": 5,
    "joint_right_leg_3": 6,
    "joint_right_leg_4": 7,
}


class TitaMujocoReal2SimNode(Node):
    """Read-only real-to-sim mirror for validating observation mapping."""

    def __init__(self) -> None:
        super().__init__("tita_mujoco_real2sim")
        self.declare_parameter("config", "")
        self.declare_parameter("viewer", True)
        self.declare_parameter("real_tita_ns", "tita4252763")
        self.declare_parameter("mirror_base_orientation", True)
        self.declare_parameter("mirror_base_position", False)
        self.declare_parameter("publish_debug", True)
        self.declare_parameter("use_state_relay", False)
        self.declare_parameter("relay_ns", "tita_relay")

        config_path = str(self.get_parameter("config").value or "").strip()
        if not config_path:
            raise RuntimeError("Parameter 'config' is required")
        self.cfg = self._load_yaml(config_path)

        self.viewer_enabled = _as_bool(self.get_parameter("viewer").value)
        self.real_tita_ns = str(self.get_parameter("real_tita_ns").value).strip("/") or "tita4252763"
        self.mirror_base_orientation = _as_bool(self.get_parameter("mirror_base_orientation").value)
        self.mirror_base_position = _as_bool(self.get_parameter("mirror_base_position").value)
        self.publish_debug = _as_bool(self.get_parameter("publish_debug").value)
        self.use_state_relay = _as_bool(self.get_parameter("use_state_relay").value)
        self.relay_ns = str(self.get_parameter("relay_ns").value).strip("/") or "tita_relay"
        self.real_ns_prefix = f"/{self.real_tita_ns}"
        self.state_source_ns = self.relay_ns if self.use_state_relay else self.real_tita_ns
        self.state_source_ns_prefix = f"/{self.state_source_ns}"
        self.state_joint_topic = f"{self.state_source_ns_prefix}/joint_states"
        self.state_imu_topic = f"{self.state_source_ns_prefix}/imu_sensor_broadcaster/imu"
        self.state_odom_topic = f"{self.state_source_ns_prefix}/chassis/odometry"
        self.plot_namespace = "/cosim_ros2_jazzy/real2sim/plot"

        self.env = TitaMujocoEnv(self.cfg, viewer_enabled=self.viewer_enabled)
        self.obs_builder = ObservationBuilder(self.cfg)

        self.latest_joint_state: JointState | None = None
        self.latest_imu: Imu | None = None
        self.latest_odom: Odometry | None = None
        self.mapping_ok = False
        self.missing_joint_names: list[str] = []
        self.last_native_joint_pos = np.full(8, np.nan, dtype=np.float32)
        self.last_native_joint_vel = np.full(8, np.nan, dtype=np.float32)
        self.last_base_quat_wxyz = self.env.base_quat().astype(np.float32)
        self.last_base_pos = self.env.base_pos().astype(np.float32)
        self.last_base_rpy = quat_wxyz_to_rpy(self.last_base_quat_wxyz)
        self.last_projected_gravity = self.obs_builder.projected_gravity(self.last_base_quat_wxyz)
        self._lock = threading.Lock()
        self._warned_missing_joints = False

        self.create_subscription(JointState, self.state_joint_topic, self._joint_state_cb, 10)
        self.create_subscription(Imu, self.state_imu_topic, self._imu_cb, 10)
        self.create_subscription(Odometry, self.state_odom_topic, self._odom_cb, 10)

        self.mapping_ok_pub = self.create_publisher(Bool, "/cosim_ros2_jazzy/real2sim/mapping_ok", 10)
        self.joint_pos_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/real2sim/joint_pos_native", 10
        )
        self.joint_vel_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/real2sim/joint_vel_native", 10
        )
        self.base_rpy_pub = self.create_publisher(Float32MultiArray, "/cosim_ros2_jazzy/real2sim/base_rpy", 10)
        self.projected_gravity_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/real2sim/projected_gravity", 10
        )

        self.plot_pubs: dict[str, Any] = {}
        if self.publish_debug:
            self._create_plot_publishers()

        self.timer = self.create_timer(0.02, self._step)
        self.get_logger().info("tita_mujoco_real2sim started")
        self.get_logger().info(f"Real robot namespace: {self.real_ns_prefix}")
        self.get_logger().info(f"State source namespace: {self.state_source_ns_prefix}")
        self.get_logger().info(f"Joint topic: {self.state_joint_topic}")
        self.get_logger().info(f"IMU topic: {self.state_imu_topic}")
        self.get_logger().info(f"Odom topic: {self.state_odom_topic}")
        self.get_logger().info(f"MuJoCo scene: {self.cfg['model']['scene_xml']}")

    def _load_yaml(self, path: str) -> dict[str, Any]:
        with Path(path).expanduser().open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _create_plot_publishers(self) -> None:
        topic_names = [
            "L1_joint_pos",
            "L2_joint_pos",
            "L3_joint_pos",
            "L4_joint_pos",
            "R1_joint_pos",
            "R2_joint_pos",
            "R3_joint_pos",
            "R4_joint_pos",
            "roll",
            "pitch",
            "yaw",
            "mapping_ok",
        ]
        for name in topic_names:
            self.plot_pubs[name] = self.create_publisher(Float32, f"{self.plot_namespace}/{name}", 10)

    def _publish_plot_scalar(self, name: str, value: float) -> None:
        publisher = self.plot_pubs.get(name)
        if publisher is not None:
            publisher.publish(Float32(data=float(value)))

    def _joint_state_cb(self, msg: JointState) -> None:
        with self._lock:
            self.latest_joint_state = msg

    def _imu_cb(self, msg: Imu) -> None:
        with self._lock:
            self.latest_imu = msg

    def _odom_cb(self, msg: Odometry) -> None:
        with self._lock:
            self.latest_odom = msg

    @staticmethod
    def _quat_msg_to_wxyz(q: Any) -> np.ndarray:
        return np.asarray([float(q.w), float(q.x), float(q.y), float(q.z)], dtype=np.float32)

    def _update_mujoco_state(self) -> None:
        joint_msg = self.latest_joint_state
        if joint_msg is None:
            self.mapping_ok = False
            return

        name_to_index = {str(name): i for i, name in enumerate(joint_msg.name)}
        missing = [name for name in MUJOCO_NATIVE_JOINTS if name not in name_to_index]
        if missing:
            self.mapping_ok = False
            self.missing_joint_names = missing
            if not self._warned_missing_joints:
                self._warned_missing_joints = True
                self.get_logger().warn(
                    f"Missing source joint names in {self.state_joint_topic}: {missing}"
                )
            return

        native_pos = np.zeros(8, dtype=np.float32)
        native_vel = np.zeros(8, dtype=np.float32)
        for name, native_idx in REAL_TO_NATIVE.items():
            src_idx = name_to_index[name]
            native_pos[native_idx] = float(joint_msg.position[src_idx]) if src_idx < len(joint_msg.position) else 0.0
            if src_idx < len(joint_msg.velocity):
                native_vel[native_idx] = float(joint_msg.velocity[src_idx])

        with self._lock:
            imu_msg = self.latest_imu
            odom_msg = self.latest_odom

        if self.mirror_base_orientation:
            if imu_msg is not None:
                base_quat_wxyz = self._quat_msg_to_wxyz(imu_msg.orientation)
            elif odom_msg is not None:
                base_quat_wxyz = self._quat_msg_to_wxyz(odom_msg.pose.pose.orientation)
            else:
                base_quat_wxyz = self.last_base_quat_wxyz
        else:
            base_quat_wxyz = self.last_base_quat_wxyz

        base_pos = self.last_base_pos.copy()
        if self.mirror_base_position and odom_msg is not None:
            base_pos = np.asarray(
                [
                    float(odom_msg.pose.pose.position.x),
                    float(odom_msg.pose.pose.position.y),
                    float(odom_msg.pose.pose.position.z),
                ],
                dtype=np.float32,
            )

        self.env.data.qpos[0:3] = base_pos.astype(np.float64)
        self.env.data.qpos[3:7] = base_quat_wxyz.astype(np.float64)
        self.env.data.qpos[self.env.qpos_addr] = native_pos.astype(np.float64)
        self.env.data.qvel[0:6] = 0.0
        self.env.data.qvel[self.env.qvel_addr] = native_vel.astype(np.float64)
        self.env.mujoco.mj_forward(self.env.model, self.env.data)

        self.last_native_joint_pos = native_pos
        self.last_native_joint_vel = native_vel
        self.last_base_quat_wxyz = base_quat_wxyz
        self.last_base_pos = base_pos
        self.last_base_rpy = quat_wxyz_to_rpy(base_quat_wxyz)
        self.last_projected_gravity = self.obs_builder.projected_gravity(base_quat_wxyz)
        self.mapping_ok = True
        self.missing_joint_names = []
        self._warned_missing_joints = False

    def _publish_outputs(self) -> None:
        self.mapping_ok_pub.publish(Bool(data=bool(self.mapping_ok)))
        self.joint_pos_pub.publish(Float32MultiArray(data=self.last_native_joint_pos.astype(float).tolist()))
        self.joint_vel_pub.publish(Float32MultiArray(data=self.last_native_joint_vel.astype(float).tolist()))
        self.base_rpy_pub.publish(Float32MultiArray(data=self.last_base_rpy.astype(float).tolist()))
        self.projected_gravity_pub.publish(Float32MultiArray(data=self.last_projected_gravity.astype(float).tolist()))

        if not self.publish_debug:
            return
        labels = ["L1", "L2", "L3", "L4", "R1", "R2", "R3", "R4"]
        for idx, label in enumerate(labels):
            self._publish_plot_scalar(f"{label}_joint_pos", float(self.last_native_joint_pos[idx]))
        self._publish_plot_scalar("roll", float(self.last_base_rpy[0]))
        self._publish_plot_scalar("pitch", float(self.last_base_rpy[1]))
        self._publish_plot_scalar("yaw", float(self.last_base_rpy[2]))
        self._publish_plot_scalar("mapping_ok", 1.0 if self.mapping_ok else 0.0)

    def _step(self) -> None:
        self._update_mujoco_state()
        self._publish_outputs()
        if self.env.viewer is not None:
            self.env.viewer.sync()


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = TitaMujocoReal2SimNode()
    try:
        rclpy.spin(node)
    finally:
        node.env.close()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
