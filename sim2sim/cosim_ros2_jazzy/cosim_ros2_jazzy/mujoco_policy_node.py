from __future__ import annotations

import threading
from pathlib import Path
from typing import Any
import hashlib

import numpy as np
import yaml

import rclpy
from geometry_msgs.msg import PoseStamped, Twist
from rclpy.node import Node
from sensor_msgs.msg import Imu, JointState
from std_msgs.msg import Float32, Float32MultiArray, String

from cosim_ros2_jazzy.action_adapter import ActionAdapter
from cosim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from cosim_ros2_jazzy.obs_builder import (
    ObsState,
    ObservationBuilder,
    estimate_base_lin_vel_naive_wheel,
    quat_wxyz_to_rpy,
    quat_wxyz_to_rotmat,
)
from cosim_ros2_jazzy.policy_runner import PolicyRunner


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"1", "true", "yes", "on"}


class MujocoPolicyNode(Node):
    def __init__(self) -> None:
        super().__init__("cosim_ros2_jazzy")
        self.declare_parameter("config", "")
        self.declare_parameter("viewer", True)
        self.declare_parameter("plot", False)
        self.declare_parameter("tita_ns", "tita")
        config_path = self.get_parameter("config").get_parameter_value().string_value
        if not config_path:
            raise RuntimeError("Parameter 'config' is required")
        self.cfg = self._load_yaml(config_path)
        self.cfg.setdefault("tita_ns", "tita")
        viewer = _as_bool(self.get_parameter("viewer").value)
        plot = _as_bool(self.get_parameter("plot").value)
        self.cfg["viewer"]["enabled"] = viewer
        self.cfg.setdefault("plot", {})
        self.cfg["plot"]["enabled"] = plot or bool(self.cfg["plot"].get("enabled", False))
        topic_cfg = self.cfg.get("topics", {})
        self.tita_ns = str(self.get_parameter("tita_ns").value or self.cfg.get("tita_ns", "tita")).strip("/") or "tita"
        self.use_manual_topics = bool(topic_cfg.get("use_manual_topics", True))
        self.enable_legacy_command_aliases = bool(topic_cfg.get("enable_legacy_command_aliases", True))
        manual_topics = dict(topic_cfg.get("manual", {}))
        legacy_topics = dict(topic_cfg.get("legacy", {}))
        self.cmd_twist_topic = str(manual_topics.get("cmd_twist", f"/{self.tita_ns}/command/manager/cmd_twist"))
        self.cmd_pose_topic = str(manual_topics.get("cmd_pose", f"/{self.tita_ns}/command/manager/cmd_pose"))
        self.cmd_key_topic = str(manual_topics.get("cmd_key", f"/{self.tita_ns}/command/manager/cmd_key"))
        self.joy_topic = str(manual_topics.get("joy", "/joy"))
        self.legacy_cmd_twist_topic = str(legacy_topics.get("cmd_twist", "/command/cmd_twist"))
        self.legacy_cmd_key_topic = str(legacy_topics.get("cmd_key", "/command/cmd_key"))
        self._apply_timing_mode()

        self.command = np.asarray(
            [
                self.cfg["command"]["default_lin_x"],
                self.cfg["command"]["default_lin_y"],
                self.cfg["command"]["default_ang_z"],
            ],
            dtype=np.float32,
        )
        self.state = "idle"
        self.transform_up_complete = False
        self.bridge_complete = False
        self.last_action = np.zeros(8, dtype=np.float32)
        self.last_action_scaled = np.zeros(8, dtype=np.float32)
        self.last_target_joint_pos = np.full(8, np.nan, dtype=np.float32)
        self.last_target_joint_vel = np.zeros(8, dtype=np.float32)
        self.last_target_wheel_vel = np.full(8, np.nan, dtype=np.float32)
        self.last_torque_cmd = np.zeros(8, dtype=np.float32)
        self.last_joint_vel = np.zeros(8, dtype=np.float32)
        self.manual_joint_target = self._pose("standing_joint_angles")
        self.manual_wheel_vel = np.zeros(2, dtype=np.float32)
        self.last_projected_gravity = np.zeros(3, dtype=np.float32)
        self.last_base_ang_vel = np.zeros(3, dtype=np.float32)
        self.last_gyro_raw = np.zeros(3, dtype=np.float32)
        self.last_command_scaled = np.zeros(3, dtype=np.float32)
        self.last_command_pose = None
        self.last_obs_current = np.zeros(int(self.cfg["policy"]["obs_dim"]), dtype=np.float32)
        self.last_obs_history = np.zeros((int(self.cfg["policy"]["history_len"]), int(self.cfg["policy"]["obs_dim"])), dtype=np.float32)
        self.last_obs = np.zeros(int(self.cfg["policy"]["obs_dim"]), dtype=np.float32)
        self.policy_tick_seq = 0
        self.policy_forward_rate_hz = float(self.cfg.get("rl_policy", {}).get("forward_rate_hz", float(self.cfg["control"]["control_rate"])))
        self.policy_substeps_per_tick = max(1, int(round(self.policy_forward_rate_hz / float(self.cfg["control"]["control_rate"]))))
        self.action_hold_steps = int(self.cfg.get("timing", {}).get("action_hold_steps", self.cfg["control"].get("decimation", 1)))
        if int(self.cfg["control"].get("decimation", 1)) % self.policy_substeps_per_tick != 0:
            self.get_logger().warn(
                "control.decimation is not divisible by rl_policy.forward_rate_hz / control_rate; "
                "rl_0 substep split will use single chunk."
            )
            self.policy_substeps_per_tick = 1
        self.transform_up_elapsed = 0.0
        self.transform_up_progress = 0.0
        self.transform_up_start_joint_angles = self._pose("idle_joint_angles")
        self.reference_transform_up_elapsed = 0.0
        self.reference_transform_up_progress = 0.0
        self.reference_transform_up_start_joint_angles = self._pose("idle_joint_angles")
        self.handoff_bridge_elapsed = 0.0
        self.handoff_bridge_progress = 0.0
        self.handoff_bridge_start_joint_angles = self._pose(
            self.cfg.get("handoff_bridge", {}).get("source_pose", "low_stand_1")
        )
        self.pose_hold_elapsed = 0.0
        self.pose_hold_progress = 0.0
        self.last_torque_clip = np.zeros(8, dtype=np.float32)
        self._warned_legacy_cmd_twist = False
        self._warned_legacy_cmd_key = False
        self.plot_enabled = bool(self.cfg["plot"].get("enabled", False))
        self.plot_namespace = str(self.cfg["plot"].get("namespace", "/cosim_ros2_jazzy/plot")).rstrip("/")
        self.plot_period = 1.0 / max(float(self.cfg["plot"].get("publish_rate_hz", 50.0)), 1e-6)
        self.last_plot_publish_time = -np.inf
        self.plot_publishers: dict[str, Any] = {}
        self.diagnostic_enabled = bool(self.cfg.get("diagnostic", {}).get("enabled", False))
        self.diagnostic_namespace = str(self.cfg.get("diagnostic", {}).get("namespace", "/cosim_ros2_jazzy/diagnostic")).rstrip("/")
        self.diagnostic_period = 1.0 / max(float(self.cfg.get("diagnostic", {}).get("publish_rate_hz", 50.0)), 1e-6)
        self.last_diagnostic_publish_time = -np.inf
        self.diagnostic_publishers: dict[str, Any] = {}
        self._lock = threading.Lock()

        self.env = TitaMujocoEnv(self.cfg, viewer_enabled=viewer)
        self.obs_builder = ObservationBuilder(self.cfg)
        self.action_adapter = ActionAdapter(self.cfg)
        self.policy = PolicyRunner.from_config(self.cfg)

        init_obs = self._build_obs()
        self.obs_builder.reset_history(init_obs)
        self.last_obs = init_obs

        if self.use_manual_topics:
            self.create_subscription(String, self.cmd_key_topic, self._cmd_key_cb, 10)
            self.create_subscription(Twist, self.cmd_twist_topic, self._cmd_twist_cb, 10)
            self.create_subscription(PoseStamped, self.cmd_pose_topic, self._cmd_pose_cb, 10)
        if self.enable_legacy_command_aliases:
            self.create_subscription(String, self.legacy_cmd_key_topic, self._legacy_cmd_key_cb, 10)
            self.create_subscription(Twist, self.legacy_cmd_twist_topic, self._legacy_cmd_twist_cb, 10)
        self.create_subscription(Float32MultiArray, "/command/joint_targets", self._joint_targets_cb, 10)
        self.create_subscription(Float32MultiArray, "/command/wheel_vel", self._wheel_vel_cb, 10)
        self.joint_pub = self.create_publisher(JointState, "/joint_states", 10)
        self.imu_pub = self.create_publisher(Imu, "/imu", 10)
        self.obs_pub = self.create_publisher(Float32MultiArray, "/cosim_ros2_jazzy/debug/obs", 10)
        self.obs_current_pub = self.create_publisher(Float32MultiArray, "/cosim_ros2_jazzy/debug/obs_current", 10)
        self.action_raw_pub = self.create_publisher(Float32MultiArray, "/cosim_ros2_jazzy/debug/action_raw", 10)
        self.action_scaled_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/action_scaled", 10
        )
        self.joint_target_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_target", 10
        )
        self.joint_pos_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_pos", 10
        )
        self.joint_vel_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_vel", 10
        )
        self.base_lin_vel_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/base_lin_vel", 10
        )
        self.base_pos_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/base_pos", 10
        )
        self.sim_time_pub = self.create_publisher(Float32, "/cosim_ros2_jazzy/debug/sim_time", 10)
        self.joint_pos_error_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_pos_error", 10
        )
        self.target_wheel_vel_by_joint_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/target_wheel_vel_by_joint", 10
        )
        self.torque_cmd_by_joint_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/torque_cmd_by_joint", 10
        )
        self.wheel_joint_vel_pub = self.create_publisher(Float32MultiArray, "/cosim_ros2_jazzy/debug/wheel_joint_vel", 10)
        self.projected_gravity_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/projected_gravity", 10
        )
        self.base_ang_vel_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/base_ang_vel", 10
        )
        self.command_pub = self.create_publisher(Twist, "/cosim_ros2_jazzy/debug/command", 10)
        self.command_scaled_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/command_scaled", 10
        )
        self.state_pub = self.create_publisher(String, "/cosim_ros2_jazzy/debug/state", 10)
        self.base_rpy_pub = self.create_publisher(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_rpy", 10)
        self.gyro_raw_pub = self.create_publisher(Float32MultiArray, "/cosim_ros2_jazzy/debug/gyro_raw", 10)
        self.gyro_filtered_pub = self.create_publisher(Float32MultiArray, "/cosim_ros2_jazzy/debug/gyro_filtered", 10)
        self.obs_history_pub = self.create_publisher(Float32MultiArray, "/cosim_ros2_jazzy/debug/obs_history", 10)
        self.policy_tick_pub = self.create_publisher(Float32, "/cosim_ros2_jazzy/debug/policy_tick", 10)
        self.torque_clip_by_joint_pub = self.create_publisher(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/torque_clip_by_joint", 10
        )
        if self.plot_enabled:
            self._create_plot_publishers()
        if self.diagnostic_enabled:
            self._create_diagnostic_publishers()

        period = 1.0 / float(self.cfg["control"]["control_rate"])
        self.timer = self.create_timer(period, self._step)
        self.get_logger().info("cosim_ros2_jazzy started")
        self.get_logger().info(self.env.model_summary())
        self.get_logger().info(f"Policy: {self.cfg['policy']['path']}")
        self.get_logger().info(f"Policy sha256: {self._sha256(self.cfg['policy']['path'])}")
        self.get_logger().info(f"RL adapter mode: {self.cfg.get('rl_adapter', {}).get('mode', 'current')}")
        self.get_logger().info(f"Obs adapter mode: {self.cfg.get('obs_adapter', {}).get('mode', 'current')}")
        self.get_logger().info(
            f"RL policy forward rate target: {self.policy_forward_rate_hz:.1f} Hz "
            f"(control_rate={float(self.cfg['control']['control_rate']):.1f}, subcycles={self.policy_substeps_per_tick})"
        )
        policy_period = 1.0 / max(self.policy_forward_rate_hz, 1e-6)
        self.get_logger().info(
            "Timing summary: "
            f"physics_dt={float(self.cfg['control']['sim_timestep']):.4f} s, "
            f"policy_forward_rate_hz={self.policy_forward_rate_hz:.1f}, "
            f"policy_period={policy_period:.4f} s, "
            f"action_hold_steps={self.action_hold_steps}, "
            f"effective_policy_dt={float(self.cfg['control']['decimation']) * float(self.cfg['control']['sim_timestep']):.4f} s"
        )
        if self.plot_enabled:
            self.get_logger().info(
                f"Plot topics enabled at {1.0 / self.plot_period:.1f} Hz under {self.plot_namespace}"
            )
        self.get_logger().info(
            f"Manual command topics: {self.cmd_key_topic}, {self.cmd_twist_topic}, {self.cmd_pose_topic}"
        )
        if self.enable_legacy_command_aliases:
            self.get_logger().warn(
                "[DEPRECATED] /command/cmd_twist and /command/cmd_key are legacy simulator topics. "
                f"Use {self.cmd_twist_topic} and {self.cmd_key_topic} instead."
            )

    def _apply_timing_mode(self) -> None:
        timing_cfg = self.cfg.get("timing", {})
        mode = str(timing_cfg.get("mode", "current"))
        if mode == "current":
            return
        physics_dt = float(timing_cfg.get("physics_dt", 0.005))
        policy_rate_hz = float(timing_cfg.get("policy_rate_hz", 50.0))
        action_hold_steps = int(timing_cfg.get("action_hold_steps", timing_cfg.get("action_hold_ticks", 4)))
        if action_hold_steps <= 0:
            raise ValueError("timing.action_hold_steps must be positive")
        if mode == "ddt_reference_500hz":
            torque_rate_hz = float(timing_cfg.get("torque_update_rate_hz", 500.0))
            control_rate = policy_rate_hz
            decimation = max(1, int(round((1.0 / control_rate) / physics_dt)))
            expected_decimation = max(1, int(round(torque_rate_hz / policy_rate_hz)))
            if decimation != expected_decimation:
                decimation = expected_decimation
        elif mode == "isaac_reference_50hz":
            control_rate = policy_rate_hz
            decimation = action_hold_steps
        else:
            return
        self.cfg.setdefault("control", {})
        self.cfg["control"]["sim_timestep"] = physics_dt
        self.cfg["control"]["control_rate"] = control_rate
        self.cfg["control"]["decimation"] = decimation
        self.cfg.setdefault("rl_policy", {})
        self.cfg["rl_policy"]["forward_rate_hz"] = policy_rate_hz
        self.cfg.setdefault("timing", {})
        self.cfg["timing"]["action_hold_steps"] = action_hold_steps

    @staticmethod
    def _load_yaml(path: str) -> dict[str, Any]:
        with open(Path(path).expanduser(), "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def _sha256(path: str) -> str:
        h = hashlib.sha256()
        with open(Path(path).expanduser(), "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def _pose(self, name: str) -> np.ndarray:
        poses = self.cfg.get("poses", {})
        if name in poses:
            return np.asarray(poses[name], dtype=np.float32)
        robot = self.cfg["robot"]
        if name in robot:
            return np.asarray(robot[name], dtype=np.float32)
        raise KeyError(f"Unknown pose '{name}'")

    def _reset_runtime_buffers(self) -> None:
        self.obs_builder.reset_runtime()
        self.policy_tick_seq = 0
        self.last_action[:] = 0.0
        self.last_action_scaled[:] = 0.0
        self.last_target_joint_pos[:] = np.nan
        self.last_target_joint_vel[:] = 0.0
        self.last_target_wheel_vel[:] = np.nan
        self.last_torque_cmd[:] = 0.0
        self.last_torque_clip[:] = 0.0
        obs = self._build_obs()
        self.obs_builder.reset_history(obs)
        self.last_obs = obs

    def _create_plot_publishers(self) -> None:
        # PlotJuggler should stay on scalar topics only so the dashboard remains light.
        # Use canonical names only; arrays stay in /debug and temporary sign checks go to /diagnostic.
        scalar_topics = [
            "state_code",
            "cmd_vx",
            "measured_vx",
            "cmd_yaw_rate",
            "measured_yaw_rate",
            "pitch",
            "roll",
            "max_abs_action_raw",
            "max_abs_torque_clip",
            "L1_target_pos",
            "L1_joint_pos",
            "L2_target_pos",
            "L2_joint_pos",
            "L3_target_pos",
            "L3_joint_pos",
            "R1_target_pos",
            "R1_joint_pos",
            "R2_target_pos",
            "R2_joint_pos",
            "R3_target_pos",
            "R3_joint_pos",
            "L4_target_wheel_vel",
            "L4_wheel_vel",
            "R4_target_wheel_vel",
            "R4_wheel_vel",
        ]
        for name in scalar_topics:
            self.plot_publishers[name] = self.create_publisher(Float32, f"{self.plot_namespace}/{name}", 10)

    def _create_diagnostic_publishers(self) -> None:
        diagnostic_topics = [
            "measured_vx_body",
            "measured_vx_world",
            "base_x_world",
            "base_y_world",
            "base_yaw",
            "policy_obs_cmd_vx",
            "policy_obs_cmd_yaw_rate",
        ]
        for name in diagnostic_topics:
            self.diagnostic_publishers[name] = self.create_publisher(
                Float32, f"{self.diagnostic_namespace}/{name}", 10
            )

    def _publish_plot_scalar(self, name: str, value: float) -> None:
        publisher = self.plot_publishers.get(name)
        if publisher is None:
            return
        publisher.publish(Float32(data=float(value)))

    def _publish_diagnostic_scalar(self, name: str, value: float) -> None:
        publisher = self.diagnostic_publishers.get(name)
        if publisher is None:
            return
        publisher.publish(Float32(data=float(value)))

    @staticmethod
    def _state_code(state: str) -> float:
        mapping = {
            "idle": 0.0,
            "transform_up": 1.0,
            "hold_default": 2.0,
            "joint_pd": 3.0,
            "wheel_test": 4.0,
            "rl_0": 5.0,
            "shadow_rl0": 5.5,
            "bridge_to_policy_stand": 6.0,
            "pose_hold_test": 7.0,
            "reference_transform_up": 8.0,
            "reference_stand_hold": 9.0,
        }
        return mapping.get(state, -1.0)

    def _cmd_key_cb(self, msg: String) -> None:
        data = msg.data.strip()
        with self._lock:
            if data in {"idle", "standby"}:
                self.state = "idle"
                self.transform_up_complete = False
                self.bridge_complete = False
                self.handoff_bridge_progress = 0.0
                self.pose_hold_progress = 0.0
                self.reference_transform_up_progress = 0.0
            elif data in {"balance", "rl_0", "rl_flat", "shadow_rl0"}:
                if not self.transform_up_complete:
                    self.get_logger().warn("Rejecting balance/rl_0: transform_up has not completed")
                    return
                using_reference_startup = self.state == "reference_stand_hold"
                bridge_cfg = self.cfg.get("handoff_bridge", {})
                if not using_reference_startup:
                    if bool(bridge_cfg.get("enabled", False)) and bool(bridge_cfg.get("allow_rl_after_bridge", True)):
                        if not self.bridge_complete:
                            self.get_logger().warn("Rejecting balance/rl_0: handoff bridge has not completed")
                            return
                active_default = self.action_adapter.default_joint_angles
                joint_pos_error = self.env.joint_pos() - np.asarray(active_default, dtype=np.float32)
                leg_indices = [i for i in range(len(joint_pos_error)) if i not in self.cfg["robot"].get("wheel_indices", [])]
                max_leg_error = float(np.max(np.abs(joint_pos_error[leg_indices])))
                if max_leg_error > 0.3:
                    self.get_logger().warn(f"balance/rl_0 entry leg joint_pos_error is large: max_abs={max_leg_error:.3f} rad")
                self._reset_runtime_buffers()
                self.state = "rl_0"
            elif data in {"transform_up", "reference_transform_up"}:
                self.reference_transform_up_start_joint_angles = self.env.joint_pos()
                self._reset_runtime_buffers()
                self.reference_transform_up_elapsed = 0.0
                self.reference_transform_up_progress = 0.0
                self.transform_up_elapsed = 0.0
                self.transform_up_progress = 0.0
                self.handoff_bridge_elapsed = 0.0
                self.handoff_bridge_progress = 0.0
                self.pose_hold_elapsed = 0.0
                self.pose_hold_progress = 0.0
                self.state = "reference_transform_up"
                self.transform_up_complete = False
                self.bridge_complete = False
                self.get_logger().info(
                    "reference_transform_up starts from current joint_pos: "
                    f"{self.reference_transform_up_start_joint_angles.tolist()}"
                )
            elif data == "transform_down":
                self.state = "transform_down"
                self.transform_up_complete = False
                self.bridge_complete = False
                self.handoff_bridge_progress = 0.0
                self.pose_hold_progress = 0.0
                self.reference_transform_up_progress = 0.0
            elif data == "jump":
                self.get_logger().warn("Ignoring unsupported manual cmd_key 'jump' for now")
                return
            elif data == "pose_idle":
                self.env.reset_to_joint_angles(self._pose("idle_joint_angles"))
                self._reset_runtime_buffers()
                self.state = "idle"
                self.transform_up_complete = False
                self.bridge_complete = False
                self.handoff_bridge_progress = 0.0
                self.pose_hold_progress = 0.0
                self.reference_transform_up_progress = 0.0
            elif data == "pose_fold":
                self.env.reset_to_joint_angles(self._pose("fold_joint_angles"))
                self._reset_runtime_buffers()
                self.state = "idle"
                self.transform_up_complete = False
                self.bridge_complete = False
                self.handoff_bridge_progress = 0.0
                self.pose_hold_progress = 0.0
                self.reference_transform_up_progress = 0.0
            elif data == "pose_stand":
                self.env.reset_to_joint_angles(self._pose("standing_joint_angles"))
                self._reset_runtime_buffers()
                self.state = "hold_default"
                self.transform_up_complete = True
                self.bridge_complete = True
                self.handoff_bridge_progress = 1.0
                self.pose_hold_progress = 0.0
                self.reference_transform_up_progress = 0.0
            elif data == "reference_stand_hold":
                self.state = "reference_stand_hold"
                self.transform_up_complete = True
                self.bridge_complete = False
            elif data == "bridge_to_policy_stand":
                if not self.transform_up_complete:
                    self.get_logger().warn("Rejecting bridge_to_policy_stand: transform_up has not completed")
                    return
                self.handoff_bridge_start_joint_angles = self.env.joint_pos()
                self._reset_runtime_buffers()
                self.handoff_bridge_elapsed = 0.0
                self.handoff_bridge_progress = 0.0
                self.pose_hold_elapsed = 0.0
                self.pose_hold_progress = 0.0
                self.state = "bridge_to_policy_stand"
                self.bridge_complete = False
                self.get_logger().info(
                    "bridge_to_policy_stand starts from current joint_pos: "
                    f"{self.handoff_bridge_start_joint_angles.tolist()}"
                )
            elif data == "pose_hold_test":
                pose_mode = str(self.cfg.get("pose_hold_test", {}).get("pose_mode", "policy_stand"))
                self.env.reset_to_joint_angles(self._pose(pose_mode))
                self._reset_runtime_buffers()
                self.pose_hold_elapsed = 0.0
                self.pose_hold_progress = 0.0
                self.state = "pose_hold_test"
                self.transform_up_complete = False
                self.bridge_complete = False
                self.handoff_bridge_progress = 0.0
                self.reference_transform_up_progress = 0.0
                self.get_logger().info(f"pose_hold_test reset to pose: {pose_mode}")
            elif data in {"hold_default", "stand_debug"}:
                self.state = "hold_default"
            elif data == "stand_ready":
                self.state = "hold_default"
            elif data == "joint_pd":
                self.manual_joint_target = self.env.joint_pos()
                if str(self.cfg.get("manual_joint_control", {}).get("wheel_mode", "zero_velocity")) == "zero_velocity":
                    for idx in self.cfg["robot"].get("wheel_indices", []):
                        self.manual_joint_target[int(idx)] = 0.0
                self.state = "joint_pd"
            elif data == "wheel_test":
                self.manual_joint_target = self.env.joint_pos()
                self.manual_wheel_vel[:] = 0.0
                self.state = "wheel_test"
            else:
                self.get_logger().warn(f"Ignoring unknown manual cmd_key: {data!r}")
                return
        self.get_logger().info(f"FSM command accepted: {data} -> state={self.state}")

    def _legacy_cmd_key_cb(self, msg: String) -> None:
        if not self._warned_legacy_cmd_key:
            self._warned_legacy_cmd_key = True
            self.get_logger().warn(
                "[DEPRECATED] /command/cmd_key is a legacy simulator topic. "
                f"Use {self.cmd_key_topic} instead."
            )
        self._cmd_key_cb(msg)

    def _cmd_twist_cb(self, msg: Twist) -> None:
        cmd = np.asarray([msg.linear.x, 0.0, msg.angular.z], dtype=np.float32)
        cmd[0] = np.clip(cmd[0], -self.cfg["command"]["max_lin_x"], self.cfg["command"]["max_lin_x"])
        cmd[1] = 0.0
        cmd[2] = np.clip(cmd[2], -self.cfg["command"]["max_ang_z"], self.cfg["command"]["max_ang_z"])
        with self._lock:
            self.command = cmd

    def _legacy_cmd_twist_cb(self, msg: Twist) -> None:
        if not self._warned_legacy_cmd_twist:
            self._warned_legacy_cmd_twist = True
            self.get_logger().warn(
                "[DEPRECATED] /command/cmd_twist is a legacy simulator topic. "
                f"Use {self.cmd_twist_topic} instead."
            )
        self._cmd_twist_cb(msg)

    def _cmd_pose_cb(self, msg: PoseStamped) -> None:
        # Accept the manual cmd_pose topic for future posture support.
        # The current simulator does not force a posture change from pose commands.
        with self._lock:
            self.last_command_pose = msg

    def _joint_targets_cb(self, msg: Float32MultiArray) -> None:
        values = np.asarray(msg.data, dtype=np.float32)
        if values.size != 8:
            self.get_logger().warn(f"Ignoring /command/joint_targets with {values.size} values; expected 8")
            return
        manual_cfg = self.cfg.get("manual_joint_control", {})
        if not bool(manual_cfg.get("enabled", True)):
            self.get_logger().warn("Ignoring /command/joint_targets because manual_joint_control.enabled=false")
            return
        target_min = np.asarray(manual_cfg.get("joint_target_min", [-np.inf] * 8), dtype=np.float32)
        target_max = np.asarray(manual_cfg.get("joint_target_max", [np.inf] * 8), dtype=np.float32)
        max_delta = float(manual_cfg.get("max_delta_per_command", np.inf))
        with self._lock:
            limited = np.clip(values, target_min, target_max)
            if str(manual_cfg.get("wheel_mode", "zero_velocity")) == "zero_velocity":
                for idx in self.cfg["robot"].get("wheel_indices", []):
                    limited[int(idx)] = self.manual_joint_target[int(idx)]
            delta = np.clip(limited - self.manual_joint_target, -max_delta, max_delta)
            self.manual_joint_target = self.manual_joint_target + delta
        self.get_logger().info(f"manual joint target updated: {self.manual_joint_target.tolist()}")

    def _wheel_vel_cb(self, msg: Float32MultiArray) -> None:
        values = np.asarray(msg.data, dtype=np.float32)
        if values.size != 2:
            self.get_logger().warn(f"Ignoring /command/wheel_vel with {values.size} values; expected 2")
            return
        limit = float(self.cfg.get("transform_up", {}).get("wheel_vel_limit", 3.0))
        with self._lock:
            self.manual_wheel_vel = np.clip(values, -limit, limit).astype(np.float32)
        self.get_logger().info(f"manual wheel velocity target updated: {self.manual_wheel_vel.tolist()}")

    def _build_obs(self) -> np.ndarray:
        base_quat = self.env.base_quat_sensor()
        base_ang_vel = self.env.base_ang_vel()
        self.last_gyro_raw = base_ang_vel.astype(np.float32)
        self.last_projected_gravity = self.obs_builder.projected_gravity(base_quat)
        self.last_base_ang_vel = base_ang_vel.astype(np.float32)
        base_lin_vel_b = None
        if self.obs_builder.include_base_lin_vel:
            if self.obs_builder.base_lin_vel_source == "wheel_vel_estimate":
                # My18-style: real hardware-deployable naive wheel-spin
                # kinematic estimate, no ground truth involved. Mirrors
                # mdp.NaiveWheelVelBaseLinVel (Isaac Lab training side).
                joint_vel = self.env.joint_vel()
                wheel_indices = [int(i) for i in self.cfg["robot"].get("wheel_indices", [])]
                left_wheel_idx, right_wheel_idx = wheel_indices
                base_lin_vel_b = estimate_base_lin_vel_naive_wheel(
                    base_quat_wxyz=base_quat,
                    left_wheel_quat_wxyz=self.env.body_quat("left_leg_4"),
                    right_wheel_quat_wxyz=self.env.body_quat("right_leg_4"),
                    left_wheel_omega=float(joint_vel[left_wheel_idx]),
                    right_wheel_omega=float(joint_vel[right_wheel_idx]),
                )
            else:
                # "ground_truth" (default): MuJoCo knows this exactly (unlike
                # real hardware) -- used only by sim2sim-only variants like
                # My16 that were trained on ground-truth base_lin_vel. See
                # Experiments/RL_Experiments.md.
                rot = quat_wxyz_to_rotmat(base_quat)
                base_lin_vel_b = rot.T @ self.env.base_lin_vel()
        state = ObsState(
            joint_pos=self.env.joint_pos(),
            joint_vel=self.env.joint_vel(),
            base_quat_wxyz=base_quat,
            base_ang_vel=base_ang_vel,
            command=self.command,
            last_action=self.last_action,
            base_lin_vel_b=base_lin_vel_b,
        )
        obs = self.obs_builder.build(state)
        self.last_obs_current = obs.copy()
        self.last_obs_history = self.obs_builder.history.copy()
        self.last_command_scaled = (np.asarray(state.command, dtype=np.float32) * self.obs_builder.command_scale).astype(np.float32)
        return obs

    def _publish_policy_tick_debug(self, state: str) -> None:
        self.policy_tick_pub.publish(Float32(data=float(self.policy_tick_seq)))

    @staticmethod
    def _smoothstep(a: float) -> float:
        a = float(np.clip(a, 0.0, 1.0))
        return 3.0 * a * a - 2.0 * a * a * a

    def _transform_up_target(self) -> tuple[np.ndarray, bool]:
        cfg = self.cfg["transform_up"]
        duration = max(float(cfg.get("duration", 3.0)), 1e-6)
        settle_time = max(float(cfg.get("settle_time", 0.5)), 0.0)
        start = self.transform_up_start_joint_angles.astype(np.float32)
        mid = np.asarray(cfg["mid_joint_angles"], dtype=np.float32)
        final_pose_mode = str(cfg.get("final_pose_mode", "policy_stand"))
        if final_pose_mode in self.cfg.get("poses", {}):
            stand = np.asarray(self.cfg["poses"][final_pose_mode], dtype=np.float32)
        else:
            stand = np.asarray(cfg.get("standing_joint_angles", self.cfg["poses"]["policy_stand"]), dtype=np.float32)
        if self.transform_up_elapsed < duration:
            s = self._smoothstep(self.transform_up_elapsed / duration)
            if s < 0.5:
                local_s = 2.0 * s
                target = (1.0 - local_s) * start + local_s * mid
            else:
                local_s = 2.0 * (s - 0.5)
                target = (1.0 - local_s) * mid + local_s * stand
            complete = False
        else:
            target = stand
            complete = self.transform_up_elapsed >= duration + settle_time
        self.transform_up_progress = float(np.clip(self.transform_up_elapsed / (duration + settle_time), 0.0, 1.0))
        return target.astype(np.float32), complete

    def _handoff_bridge_target(self) -> tuple[np.ndarray, bool]:
        cfg = self.cfg["handoff_bridge"]
        duration = max(float(cfg.get("duration", 3.0)), 1e-6)
        settle_time = max(float(cfg.get("settle_time", 1.0)), 0.0)
        start = self.handoff_bridge_start_joint_angles.astype(np.float32)
        target_pose_name = str(cfg.get("target_pose", "policy_stand"))
        target_pose = self._pose(target_pose_name)
        if self.handoff_bridge_elapsed < duration:
            s = self._smoothstep(self.handoff_bridge_elapsed / duration)
            target = (1.0 - s) * start + s * target_pose
            complete = False
        else:
            target = target_pose
            complete = self.handoff_bridge_elapsed >= duration + settle_time
        self.handoff_bridge_progress = float(np.clip(self.handoff_bridge_elapsed / (duration + settle_time), 0.0, 1.0))
        return target.astype(np.float32), complete

    def _reference_transform_up_target(self) -> tuple[np.ndarray, bool]:
        cfg = dict(self.cfg.get("reference_transform_up", {}))
        start = self.reference_transform_up_start_joint_angles.astype(np.float32)
        fold = np.asarray(cfg.get("fold_jpos", self._pose("fold_joint_angles")), dtype=np.float32)
        stand = np.asarray(cfg.get("stand_jpos", self._pose("ddt_stand")), dtype=np.float32)
        # Optional phase 3: stand → policy_jpos using the same high-gain reference controller.
        # This avoids the gain-mismatch fall that occurs when switching to the low-gain bridge.
        policy_jpos_raw = cfg.get("policy_jpos")
        policy = np.asarray(policy_jpos_raw, dtype=np.float32) if policy_jpos_raw is not None else stand
        policy_timer = max(float(cfg.get("policy_timer", 0.0)), 0.0)
        fold_timer = max(float(cfg.get("fold_timer", 4.0)), 1e-6)
        stand_timer = max(float(cfg.get("stand_timer", 2.0)), 1e-6)
        settle_iters = max(int(cfg.get("settle_iters", 100)), 0)
        update_rate = max(float(cfg.get("update_rate", 500.0)), 1e-6)

        fold_duration = fold_timer * max(float(np.max(np.abs(start - fold))), 1e-6)
        stand_duration = stand_timer
        settle_duration = settle_iters / update_rate
        total_duration = max(fold_duration + stand_duration + policy_timer + settle_duration, 1e-6)
        t = self.reference_transform_up_elapsed

        if t < fold_duration:
            b = float(np.clip(t / fold_duration, 0.0, 1.0))
            target = (1.0 - b) * start + b * fold
            complete = False
        elif t < fold_duration + stand_duration:
            phase_t = t - fold_duration
            b = float(np.clip(phase_t / stand_duration, 0.0, 1.0))
            target = (1.0 - b) * fold + b * stand
            complete = False
        elif t < fold_duration + stand_duration + policy_timer:
            phase_t = t - fold_duration - stand_duration
            b = float(np.clip(phase_t / max(policy_timer, 1e-6), 0.0, 1.0))
            target = (1.0 - b) * stand + b * policy
            complete = False
        else:
            target = policy
            complete = t >= total_duration

        self.reference_transform_up_progress = float(np.clip(t / total_duration, 0.0, 1.0))
        return target.astype(np.float32), complete

    @staticmethod
    def _clip_torque(torque_raw: np.ndarray, limit: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        torque_raw = np.asarray(torque_raw, dtype=np.float32)
        limit = np.asarray(limit, dtype=np.float32)
        torque = np.clip(torque_raw, -limit, limit)
        clip = torque_raw - torque
        return torque.astype(np.float32), clip.astype(np.float32)

    def _reference_controller_torque(self, target: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        cfg = dict(self.cfg.get("reference_transform_up", {}))
        q = self.env.joint_pos()
        dq = self.env.joint_vel()
        target = np.asarray(target, dtype=np.float32)
        kp = np.asarray(cfg.get("joint_kp", self.cfg["robot"]["joint_kp"]), dtype=np.float32).copy()
        kd = np.asarray(cfg.get("joint_kd", self.cfg["robot"]["joint_kd"]), dtype=np.float32).copy()
        ff = np.asarray(cfg.get("ff_torque", [0.0] * len(target)), dtype=np.float32).copy()
        qd_des = np.zeros_like(target, dtype=np.float32)
        wheel_indices = [int(i) for i in self.cfg["robot"].get("wheel_indices", [])]
        wheel_kp = float(cfg.get("wheel_kp", 0.0))
        wheel_kd = float(cfg.get("wheel_kd", 0.5))
        wheel_qd_des = float(cfg.get("wheel_qd_des", 0.0))

        for idx in wheel_indices:
            kp[idx] = wheel_kp
            kd[idx] = wheel_kd
            ff[idx] = 0.0
            qd_des[idx] = wheel_qd_des

        raw = kp * (target - q) + kd * (qd_des - dq) + ff
        limit = np.asarray(self.cfg["robot"]["torque_limit"], dtype=np.float32)
        torque, clip = self._clip_torque(raw, limit)
        wheel_target = np.full(8, np.nan, dtype=np.float32)
        for idx in wheel_indices:
            wheel_target[idx] = wheel_qd_des
        return torque, clip, wheel_target

    def _apply_wheel_balance(self, torque: np.ndarray, balance_cfg: dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
        torque = np.asarray(torque, dtype=np.float32).copy()
        wheel_target = np.full(8, np.nan, dtype=np.float32)
        if not bool(balance_cfg.get("use_wheel_balance", True)):
            return torque, wheel_target

        base_rpy = quat_wxyz_to_rpy(self.env.base_quat_sensor())
        pitch = float(base_rpy[1])
        pitch_rate = float(self.env.base_ang_vel()[1])
        target_vel = float(balance_cfg.get("balance_sign", 1.0)) * (
            -float(balance_cfg.get("pitch_kp", 2.0)) * pitch - float(balance_cfg.get("pitch_kd", 0.3)) * pitch_rate
        )
        limit = float(balance_cfg.get("wheel_vel_limit", 3.0))
        target_vel = float(np.clip(target_vel, -limit, limit))
        kd = np.asarray(self.cfg["robot"]["joint_kd"], dtype=np.float32)
        gain_override = balance_cfg.get("wheel_vel_gain_override")
        wheel_gain = float(gain_override) if gain_override is not None else None
        joint_vel = self.env.joint_vel()
        for idx in self.cfg["robot"].get("wheel_indices", []):
            i = int(idx)
            wheel_target[i] = target_vel
            gain = wheel_gain if wheel_gain is not None else float(kd[i])
            torque[i] = gain * (target_vel - joint_vel[i])
        limit_arr = np.asarray(self.cfg["robot"]["torque_limit"], dtype=np.float32)
        torque = np.clip(torque, -limit_arr, limit_arr)
        return torque.astype(np.float32), wheel_target

    def _transform_up_torque(self, target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        torque = self.env.target_pd(target, wheel_mode="zero_velocity")
        self.last_torque_clip[:] = 0.0
        return self._apply_wheel_balance(torque, self.cfg["transform_up"])

    def _handoff_bridge_torque(self, target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        torque = self.env.target_pd(target, wheel_mode="zero_velocity")
        self.last_torque_clip[:] = 0.0
        bridge_cfg = dict(self.cfg["handoff_bridge"])
        bridge_cfg.setdefault("pitch_kp", self.cfg["transform_up"].get("pitch_kp", 2.0))
        bridge_cfg.setdefault("pitch_kd", self.cfg["transform_up"].get("pitch_kd", 0.3))
        return self._apply_wheel_balance(torque, bridge_cfg)

    def _pose_hold_test_torque(self, target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        pose_cfg = dict(self.cfg.get("pose_hold_test", {}))
        if str(pose_cfg.get("controller_mode", "default")) == "reference":
            torque, clip, wheel_target = self._reference_controller_torque(target)
            self.last_torque_clip = clip
            return torque, wheel_target
        wheel_mode = "zero_velocity" if bool(pose_cfg.get("wheel_zero_velocity_hold", True)) else "manual_velocity"
        torque = self.env.target_pd(target, wheel_mode=wheel_mode)
        self.last_torque_clip[:] = 0.0
        if bool(pose_cfg.get("use_wheel_balance", False)):
            pose_cfg.setdefault("pitch_kp", self.cfg["transform_up"].get("pitch_kp", 2.0))
            pose_cfg.setdefault("pitch_kd", self.cfg["transform_up"].get("pitch_kd", 0.3))
            pose_cfg.setdefault("wheel_vel_gain_override", self.cfg["transform_up"].get("wheel_vel_gain_override"))
            pose_cfg.setdefault("wheel_vel_limit", self.cfg["transform_up"].get("wheel_vel_limit", 3.0))
            pose_cfg.setdefault("balance_sign", self.cfg["transform_up"].get("balance_sign", 1.0))
            return self._apply_wheel_balance(torque, pose_cfg)
        wheel_target = np.full(8, np.nan, dtype=np.float32)
        if bool(pose_cfg.get("wheel_zero_velocity_hold", True)):
            for idx in self.cfg["robot"].get("wheel_indices", []):
                wheel_target[int(idx)] = 0.0
        return torque.astype(np.float32), wheel_target

    def _wheel_velocity_override(self, torque: np.ndarray, wheel_targets_2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        torque = np.asarray(torque, dtype=np.float32).copy()
        wheel_target = np.full(8, np.nan, dtype=np.float32)
        self.last_torque_clip[:] = 0.0
        kd = np.asarray(self.cfg["robot"]["joint_kd"], dtype=np.float32)
        joint_vel = self.env.joint_vel()
        wheel_indices = [int(i) for i in self.cfg["robot"].get("wheel_indices", [])]
        for local_idx, joint_idx in enumerate(wheel_indices[:2]):
            target_vel = float(wheel_targets_2[local_idx])
            wheel_target[joint_idx] = target_vel
            torque[joint_idx] = kd[joint_idx] * (target_vel - joint_vel[joint_idx])
        limit = np.asarray(self.cfg["robot"]["torque_limit"], dtype=np.float32)
        torque = np.clip(torque, -limit, limit)
        return torque.astype(np.float32), wheel_target

    def _step(self) -> None:
        if not self.env.is_running():
            self.get_logger().info("MuJoCo viewer closed; shutting down node")
            rclpy.shutdown()
            return

        with self._lock:
            state = self.state

        obs = self._build_obs()
        self.last_obs = obs

        if state in {"rl_0", "shadow_rl0"}:
            self.last_torque_clip[:] = 0.0
            subcycles = max(1, self.policy_substeps_per_tick)
            substeps_per_policy = max(1, int(self.env.decimation / subcycles))
            for policy_cycle in range(subcycles):
                cycle_obs = self._build_obs()
                self.last_obs = cycle_obs
                action = self.policy.act(cycle_obs, self.obs_builder.history)
                torque, action_debug = self.action_adapter.compute(action, self.env.joint_pos(), self.env.joint_vel())
                self.last_action = action_debug.action_raw_by_joint
                self.last_action_scaled = action_debug.action_scaled_by_joint
                self.last_target_joint_pos = action_debug.target_joint_pos_by_joint
                self.last_target_joint_vel = action_debug.target_joint_vel_by_joint
                self.last_target_wheel_vel = action_debug.target_wheel_vel_by_joint
                self.last_torque_clip = action_debug.torque_clip_by_joint
                self.last_torque_cmd = action_debug.torque_cmd_by_joint
                self.last_joint_vel = action_debug.joint_vel_by_joint
                self.policy_tick_seq += 1
                self._publish_policy_tick_debug(state)

                if state == "rl_0":
                    def torque_callback(joint_pos, joint_vel):
                        sub_torque, sub_debug = self.action_adapter.compute(action, joint_pos, joint_vel)
                        self.last_torque_clip = sub_debug.torque_clip_by_joint
                        self.last_torque_cmd = sub_debug.torque_cmd_by_joint
                        self.last_target_joint_vel = sub_debug.target_joint_vel_by_joint
                        self.last_joint_vel = sub_debug.joint_vel_by_joint
                        return sub_torque
                    self.env.step_with_torque_callback(
                        torque_callback,
                        num_substeps=substeps_per_policy,
                        sleep=(policy_cycle == subcycles - 1),
                    )
                else:
                    _ref_cfg = self.cfg.get("reference_transform_up", {})
                    _hold_key = "policy_jpos" if "policy_jpos" in _ref_cfg else "stand_jpos"
                    target = np.asarray(
                        _ref_cfg.get(_hold_key, self._pose("ddt_stand")),
                        dtype=np.float32,
                    )
                    def shadow_torque_callback(_q, _dq):
                        sub_torque, sub_clip, sub_wheel_target = self._reference_controller_torque(target)
                        self.last_joint_vel = self.env.joint_vel()
                        return sub_torque
                    self.env.step_with_torque_callback(
                        shadow_torque_callback,
                        num_substeps=substeps_per_policy,
                        sleep=(policy_cycle == subcycles - 1),
                    )
                self.obs_builder.push_history(cycle_obs)
        else:
            if state == "idle":
                target = self._pose("idle_joint_angles")
                wheel_mode = "zero_velocity"
            elif state == "transform_down":
                target = self._pose("idle_joint_angles")
                wheel_mode = "zero_velocity"
            elif state == "transform_up":
                target, complete = self._transform_up_target()
                wheel_mode = "imu_balance"
                if complete and not self.transform_up_complete:
                    self.transform_up_complete = True
                    self.bridge_complete = False
                    self.last_action[:] = 0.0
                    self.last_action_scaled[:] = 0.0
                    standing_obs = self._build_obs()
                    self.obs_builder.reset_history(standing_obs)
                    self.get_logger().info("transform_up complete")
            elif state == "reference_transform_up":
                target, complete = self._reference_transform_up_target()
                wheel_mode = "reference_damping"
                if complete:
                    self.transform_up_complete = True
                    self.bridge_complete = False
                    self.last_action[:] = 0.0
                    self.last_action_scaled[:] = 0.0
                    ref_obs = self._build_obs()
                    self.obs_builder.reset_history(ref_obs)
                    self.last_obs = ref_obs
                    with self._lock:
                        self.state = "reference_stand_hold"
                    state = "reference_stand_hold"
                    self.get_logger().info("reference_transform_up complete; entering reference_stand_hold")
            elif state == "bridge_to_policy_stand":
                target, complete = self._handoff_bridge_target()
                wheel_mode = "imu_balance"
                if complete and not self.bridge_complete:
                    self.bridge_complete = True
                    self.last_action[:] = 0.0
                    self.last_action_scaled[:] = 0.0
                    bridge_obs = self._build_obs()
                    self.obs_builder.reset_history(bridge_obs)
                    self.last_obs = bridge_obs
                    with self._lock:
                        self.state = "hold_default"
                    state = "hold_default"
                    self.get_logger().info("handoff bridge complete; entering hold_default")
            elif state == "reference_stand_hold":
                ref_cfg = self.cfg.get("reference_transform_up", {})
                hold_key = "policy_jpos" if "policy_jpos" in ref_cfg else "stand_jpos"
                target = np.asarray(ref_cfg.get(hold_key, self._pose("ddt_stand")), dtype=np.float32)
                wheel_mode = "reference_damping"
            elif state == "pose_hold_test":
                pose_mode = str(self.cfg.get("pose_hold_test", {}).get("pose_mode", "policy_stand"))
                target = self._pose(pose_mode)
                wheel_mode = "zero_velocity"
                duration = float(self.cfg.get("pose_hold_test", {}).get("duration", 5.0))
                self.pose_hold_progress = float(np.clip(self.pose_hold_elapsed / max(duration, 1e-6), 0.0, 1.0))
            elif state == "joint_pd":
                target = self.manual_joint_target.copy()
                wheel_mode = str(self.cfg.get("manual_joint_control", {}).get("wheel_mode", "zero_velocity"))
            elif state == "wheel_test":
                target = self.manual_joint_target.copy()
                wheel_mode = "manual_velocity"
            else:
                target = self._pose("standing_joint_angles")
                if self.bridge_complete:
                    wheel_mode = "imu_balance"
                else:
                    wheel_mode = "zero_velocity"
            if state == "transform_up":
                torque, transform_wheel_target = self._transform_up_torque(target)
            elif state == "reference_transform_up":
                torque, clip, transform_wheel_target = self._reference_controller_torque(target)
                self.last_torque_clip = clip
            elif state == "reference_stand_hold":
                torque, clip, transform_wheel_target = self._reference_controller_torque(target)
                self.last_torque_clip = clip
            elif state == "bridge_to_policy_stand":
                torque, transform_wheel_target = self._handoff_bridge_torque(target)
            elif state == "wheel_test":
                base_torque = self.env.target_pd(target, wheel_mode="zero_velocity")
                torque, transform_wheel_target = self._wheel_velocity_override(base_torque, self.manual_wheel_vel)
            elif state == "hold_default" and self.bridge_complete:
                torque, transform_wheel_target = self._handoff_bridge_torque(target)
            elif state == "pose_hold_test":
                torque, transform_wheel_target = self._pose_hold_test_torque(target)
            else:
                torque = self.env.target_pd(target, wheel_mode=wheel_mode)
                transform_wheel_target = None
            self.last_action[:] = 0.0
            self.last_action_scaled[:] = 0.0
            self.last_target_joint_pos = target.astype(np.float32)
            self.last_target_joint_vel[:] = 0.0
            self.last_target_wheel_vel[:] = np.nan
            for idx in self.cfg["robot"].get("wheel_indices", []):
                if wheel_mode == "zero_velocity":
                    self.last_target_joint_pos[int(idx)] = np.nan
                    self.last_target_wheel_vel[int(idx)] = 0.0
                    self.last_target_joint_vel[int(idx)] = 0.0
            if transform_wheel_target is not None:
                self.last_target_joint_pos[np.asarray(self.cfg["robot"].get("wheel_indices", []), dtype=np.int32)] = np.nan
                self.last_target_wheel_vel = transform_wheel_target
            self.last_torque_cmd = torque.astype(np.float32)
            self.last_joint_vel = self.env.joint_vel()
            if state == "transform_up":
                def transform_torque_callback(_q, _dq):
                    sub_torque, sub_wheel_target = self._transform_up_torque(target)
                    self.last_torque_cmd = sub_torque.astype(np.float32)
                    self.last_target_wheel_vel = sub_wheel_target.astype(np.float32)
                    self.last_target_joint_vel[[int(i) for i in self.cfg["robot"].get("wheel_indices", [])]] = 0.0
                    self.last_joint_vel = self.env.joint_vel()
                    return sub_torque
                self.env.step_with_torque_callback(transform_torque_callback)
                self.transform_up_elapsed += self.env.control_dt
            elif state == "reference_transform_up":
                def reference_transform_torque_callback(_q, _dq):
                    sub_torque, sub_clip, sub_wheel_target = self._reference_controller_torque(target)
                    self.last_torque_cmd = sub_torque.astype(np.float32)
                    self.last_torque_clip = sub_clip.astype(np.float32)
                    self.last_target_wheel_vel = sub_wheel_target.astype(np.float32)
                    self.last_target_joint_vel[[int(i) for i in self.cfg["robot"].get("wheel_indices", [])]] = 0.0
                    self.last_joint_vel = self.env.joint_vel()
                    return sub_torque
                self.env.step_with_torque_callback(reference_transform_torque_callback)
                self.reference_transform_up_elapsed += self.env.control_dt
            elif state == "bridge_to_policy_stand":
                def bridge_torque_callback(_q, _dq):
                    sub_torque, sub_wheel_target = self._handoff_bridge_torque(target)
                    self.last_torque_cmd = sub_torque.astype(np.float32)
                    self.last_target_wheel_vel = sub_wheel_target.astype(np.float32)
                    self.last_target_joint_vel[[int(i) for i in self.cfg["robot"].get("wheel_indices", [])]] = 0.0
                    self.last_joint_vel = self.env.joint_vel()
                    return sub_torque
                self.env.step_with_torque_callback(bridge_torque_callback)
                self.handoff_bridge_elapsed += self.env.control_dt
            elif state == "wheel_test":
                def wheel_test_torque_callback(_q, _dq):
                    base_torque = self.env.target_pd(target, wheel_mode="zero_velocity")
                    sub_torque, sub_wheel_target = self._wheel_velocity_override(base_torque, self.manual_wheel_vel)
                    self.last_torque_cmd = sub_torque.astype(np.float32)
                    self.last_target_wheel_vel = sub_wheel_target.astype(np.float32)
                    self.last_target_joint_vel[[int(i) for i in self.cfg["robot"].get("wheel_indices", [])]] = 0.0
                    self.last_joint_vel = self.env.joint_vel()
                    return sub_torque
                self.env.step_with_torque_callback(wheel_test_torque_callback)
            elif state == "pose_hold_test":
                def pose_hold_torque_callback(_q, _dq):
                    sub_torque, sub_wheel_target = self._pose_hold_test_torque(target)
                    self.last_torque_cmd = sub_torque.astype(np.float32)
                    self.last_target_wheel_vel = sub_wheel_target.astype(np.float32)
                    self.last_target_joint_vel[[int(i) for i in self.cfg["robot"].get("wheel_indices", [])]] = 0.0
                    self.last_joint_vel = self.env.joint_vel()
                    return sub_torque
                self.env.step_with_torque_callback(pose_hold_torque_callback)
                self.pose_hold_elapsed += self.env.control_dt
            elif state == "reference_stand_hold":
                def reference_hold_torque_callback(_q, _dq):
                    sub_torque, sub_clip, sub_wheel_target = self._reference_controller_torque(target)
                    self.last_torque_cmd = sub_torque.astype(np.float32)
                    self.last_torque_clip = sub_clip.astype(np.float32)
                    self.last_target_wheel_vel = sub_wheel_target.astype(np.float32)
                    self.last_joint_vel = self.env.joint_vel()
                    return sub_torque
                self.env.step_with_torque_callback(reference_hold_torque_callback)
            elif state == "hold_default" and self.bridge_complete:
                def hold_default_torque_callback(_q, _dq):
                    sub_torque, sub_wheel_target = self._handoff_bridge_torque(target)
                    self.last_torque_cmd = sub_torque.astype(np.float32)
                    self.last_target_wheel_vel = sub_wheel_target.astype(np.float32)
                    self.last_joint_vel = self.env.joint_vel()
                    return sub_torque
                self.env.step_with_torque_callback(hold_default_torque_callback)
            else:
                self.last_torque_clip[:] = 0.0
                self.env.step_with_torque_callback(lambda _q, _dq: self.env.target_pd(target, wheel_mode=wheel_mode))
        if state not in {"rl_0", "shadow_rl0"}:
            self.obs_builder.push_history(obs)
        self._publish_debug(state)

    def _publish_debug(self, state: str) -> None:
        now = self.get_clock().now().to_msg()
        joint_msg = JointState()
        joint_msg.header.stamp = now
        joint_msg.name = list(self.cfg["robot"]["joint_names"])
        joint_msg.position = self.env.joint_pos().astype(float).tolist()
        joint_msg.velocity = self.env.joint_vel().astype(float).tolist()
        joint_msg.effort = self.env.data.ctrl[self.env.actuator_ids].astype(float).tolist()
        self.joint_pub.publish(joint_msg)

        quat = self.env.base_quat_sensor()
        imu = Imu()
        imu.header.stamp = now
        imu.header.frame_id = self.cfg["robot"]["imu_site_name"]
        imu.orientation.w = float(quat[0])
        imu.orientation.x = float(quat[1])
        imu.orientation.y = float(quat[2])
        imu.orientation.z = float(quat[3])
        gyro = self.env.base_ang_vel()
        accel = self.env.base_accel()
        imu.angular_velocity.x = float(gyro[0])
        imu.angular_velocity.y = float(gyro[1])
        imu.angular_velocity.z = float(gyro[2])
        imu.linear_acceleration.x = float(accel[0])
        imu.linear_acceleration.y = float(accel[1])
        imu.linear_acceleration.z = float(accel[2])
        self.imu_pub.publish(imu)

        self.obs_pub.publish(Float32MultiArray(data=self.last_obs.astype(float).tolist()))
        self.obs_current_pub.publish(Float32MultiArray(data=self.last_obs_current.astype(float).tolist()))
        self.action_raw_pub.publish(Float32MultiArray(data=self.last_action.astype(float).tolist()))
        self.action_scaled_pub.publish(Float32MultiArray(data=self.last_action_scaled.astype(float).tolist()))
        self.target_wheel_vel_by_joint_pub.publish(
            Float32MultiArray(data=self.last_target_wheel_vel.astype(float).tolist())
        )
        self.torque_cmd_by_joint_pub.publish(Float32MultiArray(data=self.last_torque_cmd.astype(float).tolist()))
        self.torque_clip_by_joint_pub.publish(Float32MultiArray(data=self.last_torque_clip.astype(float).tolist()))
        wheel_indices = [int(i) for i in self.cfg["robot"].get("wheel_indices", [])]
        self.wheel_joint_vel_pub.publish(
            Float32MultiArray(data=self.env.joint_vel()[wheel_indices].astype(float).tolist())
        )
        self.joint_pos_pub.publish(Float32MultiArray(data=self.env.joint_pos().astype(float).tolist()))
        self.joint_vel_pub.publish(Float32MultiArray(data=self.env.joint_vel().astype(float).tolist()))
        self.base_lin_vel_pub.publish(Float32MultiArray(data=self.env.base_lin_vel().astype(float).tolist()))
        self.base_pos_pub.publish(Float32MultiArray(data=self.env.base_pos().astype(float).tolist()))
        self.sim_time_pub.publish(Float32(data=float(self.env.data.time)))
        joint_pos_error = self.env.joint_pos() - np.asarray(self.obs_builder.default_joint_angles, dtype=np.float32)
        self.joint_pos_error_pub.publish(Float32MultiArray(data=joint_pos_error.astype(float).tolist()))
        self.joint_target_pub.publish(Float32MultiArray(data=self.last_target_joint_pos.astype(float).tolist()))
        self.projected_gravity_pub.publish(Float32MultiArray(data=self.last_projected_gravity.astype(float).tolist()))
        self.base_ang_vel_pub.publish(Float32MultiArray(data=self.last_base_ang_vel.astype(float).tolist()))
        cmd_msg = Twist()
        cmd_msg.linear.x = float(self.command[0])
        cmd_msg.linear.y = float(self.command[1])
        cmd_msg.angular.z = float(self.command[2])
        self.command_pub.publish(cmd_msg)
        self.command_scaled_pub.publish(Float32MultiArray(data=self.last_command_scaled.astype(float).tolist()))
        self.state_pub.publish(String(data=state))
        self.base_rpy_pub.publish(Float32MultiArray(data=quat_wxyz_to_rpy(quat).astype(float).tolist()))
        self.gyro_raw_pub.publish(Float32MultiArray(data=self.last_gyro_raw.astype(float).tolist()))
        self.gyro_filtered_pub.publish(Float32MultiArray(data=self.obs_builder.filtered_ang_vel.astype(float).tolist()))
        self.obs_history_pub.publish(Float32MultiArray(data=self.last_obs_history.astype(float).reshape(-1).tolist()))
        self._publish_plot(now, state, quat)

    def _publish_plot(self, now: Any, state: str, quat: np.ndarray) -> None:
        if not self.plot_enabled:
            return
        stamp_sec = float(now.sec) + float(now.nanosec) * 1e-9
        if stamp_sec - self.last_plot_publish_time < self.plot_period:
            return
        self.last_plot_publish_time = stamp_sec

        joint_pos = self.env.joint_pos()
        joint_vel = self.env.joint_vel()
        wheel_indices = [int(i) for i in self.cfg["robot"].get("wheel_indices", [])]
        left_wheel_idx, right_wheel_idx = wheel_indices
        base_rpy = quat_wxyz_to_rpy(quat)
        # PlotJuggler uses body-frame forward speed so cmd_vx is compared against robot-forward motion.
        rot = quat_wxyz_to_rotmat(quat)
        base_lin_vel_world = self.env.base_lin_vel()
        base_lin_vel_body = rot.T @ base_lin_vel_world
        measured_vx = float(base_lin_vel_body[0])
        measured_yaw_rate = float(self.env.base_ang_vel()[2])
        pitch = float(base_rpy[1])
        roll = float(base_rpy[0])
        cmd_vx = float(self.command[0])
        cmd_yaw_rate = float(self.command[2])

        self._publish_plot_scalar("state_code", self._state_code(state))
        self._publish_plot_scalar("cmd_vx", cmd_vx)
        self._publish_plot_scalar("measured_vx", measured_vx)
        self._publish_plot_scalar("cmd_yaw_rate", cmd_yaw_rate)
        self._publish_plot_scalar("measured_yaw_rate", measured_yaw_rate)
        self._publish_plot_scalar("pitch", pitch)
        self._publish_plot_scalar("roll", roll)
        self._publish_plot_scalar("max_abs_action_raw", float(np.max(np.abs(self.last_action))))
        self._publish_plot_scalar("max_abs_torque_clip", float(np.max(np.abs(self.last_torque_clip))))
        leg_labels = ["L1", "L2", "L3", "R1", "R2", "R3"]
        leg_indices = [0, 1, 2, 4, 5, 6]
        for label, idx in zip(leg_labels, leg_indices, strict=True):
            self._publish_plot_scalar(f"{label}_target_pos", self.last_target_joint_pos[idx])
            self._publish_plot_scalar(f"{label}_joint_pos", joint_pos[idx])
        wheel_labels = ["L4", "R4"]
        wheel_indices = [left_wheel_idx, right_wheel_idx]
        for label, idx in zip(wheel_labels, wheel_indices, strict=True):
            self._publish_plot_scalar(f"{label}_target_wheel_vel", self.last_target_wheel_vel[idx])
            self._publish_plot_scalar(f"{label}_wheel_vel", joint_vel[idx])

        if self.diagnostic_enabled:
            base_pos = self.env.base_pos()
            base_yaw = float(base_rpy[2])
            policy_obs_cmd_vx = float(self.last_obs_current[6]) if self.last_obs_current.size >= 9 else 0.0
            policy_obs_cmd_yaw_rate = float(self.last_obs_current[8]) if self.last_obs_current.size >= 9 else 0.0
            self._publish_diagnostic_scalar("measured_vx_body", float(base_lin_vel_body[0]))
            self._publish_diagnostic_scalar("measured_vx_world", float(base_lin_vel_world[0]))
            self._publish_diagnostic_scalar("base_x_world", float(base_pos[0]))
            self._publish_diagnostic_scalar("base_y_world", float(base_pos[1]))
            self._publish_diagnostic_scalar("base_yaw", base_yaw)
            self._publish_diagnostic_scalar("policy_obs_cmd_vx", policy_obs_cmd_vx)
            self._publish_diagnostic_scalar("policy_obs_cmd_yaw_rate", policy_obs_cmd_yaw_rate)


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = MujocoPolicyNode()
    try:
        rclpy.spin(node)
    finally:
        node.env.close()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
