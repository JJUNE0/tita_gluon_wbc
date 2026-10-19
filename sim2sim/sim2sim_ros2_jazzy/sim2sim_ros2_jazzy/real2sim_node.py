"""ROBOT_READ_ONLY: mirror incoming ROS state in MuJoCo, without control publishers."""

from pathlib import Path

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, JointState
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool, Float32MultiArray
import yaml

from .adapter import NATIVE_JOINTS, quat_wxyz_to_rpy, quat_wxyz_to_rotmat
from .mujoco_env import TitaMujocoEnv


class Real2SimNode(Node):
    def __init__(self):
        super().__init__('real2sim')
        for name, default in [('config', ''), ('viewer', True), ('real_tita_ns', 'tita4252763'),
                              ('mirror_base_orientation', True), ('mirror_base_position', False)]:
            self.declare_parameter(name, default)
        path = self.get_parameter('config').value or Path(__file__).resolve().parents[1] / 'config/tita.yaml'
        self.cfg = yaml.safe_load(Path(path).expanduser().read_text())
        self.env = TitaMujocoEnv(self.cfg, viewer_enabled=self.get_parameter('viewer').value)
        namespace = '/' + self.get_parameter('real_tita_ns').value.strip('/')
        self.latest_joints = self.latest_imu = self.latest_odom = None
        self.mapping_ok = False
        self.create_subscription(JointState, namespace + '/joint_states', self._joints, 10)
        self.create_subscription(Imu, namespace + '/imu_sensor_broadcaster/imu', self._imu, 10)
        self.create_subscription(Odometry, namespace + '/chassis/odometry', self._odom, 10)
        self.mapping_pub = self.create_publisher(Bool, '/real2sim/mapping_ok', 10)
        self.position_pub = self.create_publisher(Float32MultiArray, '/real2sim/joint_pos_native', 10)
        self.velocity_pub = self.create_publisher(Float32MultiArray, '/real2sim/joint_vel_native', 10)
        self.rpy_pub = self.create_publisher(Float32MultiArray, '/real2sim/base_rpy', 10)
        self.gravity_pub = self.create_publisher(Float32MultiArray, '/real2sim/projected_gravity', 10)
        self.timer = self.create_timer(.02, self._step)
        self.get_logger().info(f'[ROBOT_READ_ONLY] Mirroring {namespace}; no robot command publisher')

    def _joints(self, message):
        self.latest_joints = message

    def _imu(self, message):
        self.latest_imu = message

    def _odom(self, message):
        self.latest_odom = message

    def _update(self):
        joints = self.latest_joints
        names = {name: index for index, name in enumerate(joints.name)} if joints else {}
        if any(name not in names or names[name] >= len(joints.position) for name in NATIVE_JOINTS):
            self.mapping_ok = False
            return
        positions = np.asarray([joints.position[names[name]] for name in NATIVE_JOINTS])
        velocities = np.asarray([joints.velocity[names[name]] if names[name] < len(joints.velocity) else 0.
                                 for name in NATIVE_JOINTS])
        if not np.isfinite(positions).all() or not np.isfinite(velocities).all():
            self.mapping_ok = False
            return
        quaternion = self.env.data.qpos[3:7].copy()
        if self.latest_imu and self.get_parameter('mirror_base_orientation').value:
            q = self.latest_imu.orientation
            candidate = np.asarray([q.w, q.x, q.y, q.z])
            norm = np.linalg.norm(candidate)
            if self.latest_imu.orientation_covariance[0] != -1 and np.isfinite(norm) and norm > 1e-6:
                quaternion = candidate / norm
        self.env.data.qpos[3:7] = quaternion
        if self.latest_odom and self.get_parameter('mirror_base_position').value:
            position = self.latest_odom.pose.pose.position
            candidate = np.asarray([position.x, position.y, position.z])
            if np.isfinite(candidate).all():
                self.env.data.qpos[:3] = candidate
        self.env.data.qpos[self.env.qpos_addr] = positions
        self.env.data.qvel[:] = 0.
        self.env.data.qvel[self.env.qvel_addr] = velocities
        self.env.mujoco.mj_forward(self.env.model, self.env.data)
        self.mapping_ok = True

    def _step(self):
        if not self.env.is_running():
            rclpy.try_shutdown()
            return
        self._update()
        self.mapping_pub.publish(Bool(data=self.mapping_ok))
        if self.mapping_ok:
            quaternion = self.env.base_quat()
            for publisher, values in [(self.position_pub, self.env.joint_pos()), (self.velocity_pub, self.env.joint_vel()),
                                      (self.rpy_pub, quat_wxyz_to_rpy(quaternion)),
                                      (self.gravity_pub, quat_wxyz_to_rotmat(quaternion).T @ np.array([0., 0., -1.]))]:
                publisher.publish(Float32MultiArray(data=values.astype(float).tolist()))
        if self.env.viewer:
            self.env.viewer.sync()

def main(args=None):
    rclpy.init(args=args)
    node = Real2SimNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.env.close()
        node.destroy_node()
        rclpy.try_shutdown()
