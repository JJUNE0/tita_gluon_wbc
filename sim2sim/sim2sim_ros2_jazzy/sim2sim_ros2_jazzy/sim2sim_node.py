"""VALIDATION_SIM: one ROS control loop for policy, physics and terminal input."""

import json
from pathlib import Path
import select
import sys
import termios
import time
import tty

import numpy as np
import onnxruntime as ort
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String

from .adapter import ActionAdapter, LegActionFilter, ObservationBuilder, ObsState, quat_wxyz_to_rotmat
from .mujoco_env import TitaMujocoEnv
from .residual_wheel_pd import ResidualWheelPD
from .residual_wheel_lqr import ResidualWheelLQR
from .velocity_bias import WheelVelocityBias
from .state_machine import SPLAY_POSE, StateMachine


class Sim2SimNode(Node):
    def __init__(self):
        super().__init__('sim2sim')
        self.declare_parameter('config', '')
        self.declare_parameter('viewer', True)
        self.declare_parameter('residual_wheel_pd', False)
        self.declare_parameter('fixed_residual_lqr', False)
        self.declare_parameter('velocity_bias', False)
        self.declare_parameter('leg_action_filter', 'auto')
        self.declare_parameter('leg_notch_hz', 8.3)
        self.declare_parameter('leg_notch_q', 3.)
        fixed_lqr = self.get_parameter('fixed_residual_lqr').value
        residual_pd = self.get_parameter('residual_wheel_pd').value
        velocity_bias = self.get_parameter('velocity_bias').value
        if sum([fixed_lqr, residual_pd, velocity_bias]) > 1:
            raise ValueError('Choose one residual controller')
        self.cfg = json.loads(Path(self.get_parameter('config').value).read_text())
        # Old exported configs retain their original caps until prepared again.
        caps = self.cfg['command']
        self.command_ranges = self.cfg.get('sim_command_ranges', {
            'lin_vel_x': [-caps['max_lin_x'], caps['max_lin_x']],
            'ang_vel_z': [-caps['max_ang_z'], caps['max_ang_z']],
        })
        # Training command ramp [units/s]; None = step change. Configs exported before this key keep 0.5/s.
        self.command_ramp = self.cfg.get('sim_command_ramp', .5)
        self.env = TitaMujocoEnv(self.cfg, viewer_enabled=self.get_parameter('viewer').value)
        self.residual = None
        if velocity_bias:
            self.residual = WheelVelocityBias(self.env)
        elif fixed_lqr:
            self.residual = ResidualWheelLQR(self.env)
        elif residual_pd:
            self.residual = ResidualWheelPD(self.env)
        self.obs_builder = ObservationBuilder(self.cfg)
        self.action_adapter = ActionAdapter(self.cfg)
        filter_mode = self.get_parameter('leg_action_filter').value
        if filter_mode == 'auto':
            filter_mode = self.cfg['policy_interface'].get('leg_action_filter', 'none')
        if filter_mode != 'none' and abs(self.env.control_dt - .02) > 1e-9:
            raise ValueError('leg action MA2 requires a 20 ms policy period')
        self.leg_filter = LegActionFilter(filter_mode, self.action_adapter.order,
            self.get_parameter('leg_notch_hz').value, self.get_parameter('leg_notch_q').value)
        options = ort.SessionOptions()
        options.intra_op_num_threads = 1
        self.policy = ort.InferenceSession(
            self.cfg['policy']['path'], sess_options=options, providers=['CPUExecutionProvider'])
        if (self.policy.get_inputs()[0].shape != [1, self.cfg['policy']['obs_dim']]
                or self.policy.get_outputs()[0].shape != [1, 8]):
            raise ValueError('ONNX interface does not match the checkpoint metadata')
        self.command = np.zeros(3, dtype=np.float32)
        self.last_action = np.zeros(8, dtype=np.float32)
        self.steps = 0
        self.was_rl = False
        # Headless runs have no keyboard, so they stand up and enter RL automatically.
        self.sm = StateMachine(self.cfg['robot']['torque_limit'], auto_rl=not self.get_parameter('viewer').value)
        self.env.reset(SPLAY_POSE)
        if self.sm.auto_rl:
            self.sm.request('transform_up', self.env.joint_pos())
        self.create_subscription(String, '/tita/command/manager/cmd_key', self._cmd_key_cb, 10)
        self.create_subscription(Twist, '/tita/command/manager/cmd_twist', self._cmd_twist_cb, 10)
        self.obs_pub = self.create_publisher(Float32MultiArray, '/sim2sim/debug/obs', 10)
        self.action_pub = self.create_publisher(Float32MultiArray, '/sim2sim/debug/action', 10)
        self.applied_pub = self.create_publisher(Float32MultiArray, '/sim2sim/debug/action_applied', 10)
        self.timer = self.create_timer(self.env.control_dt, self._step)
        self.get_logger().info(self.cfg['policy_interface']['checkpoint'])

    def _cmd_key_cb(self, message):
        if message.data in ('pose_stand', 'reset'):
            self.env.reset(SPLAY_POSE)
            self.command[:] = 0
            self.sm.request('idle', self.env.joint_pos())
        elif message.data in ('balance', 'rl_0'):
            if not self.sm.request('rl', self.env.joint_pos()):
                self.get_logger().warn('RL rejected: press 1 (transform_up) and wait for sit first')
        elif message.data in ('idle', 'transform_up'):
            self.sm.request(message.data, self.env.joint_pos())
        self.get_logger().info(f'state: {self.sm.state}')

    def _cmd_twist_cb(self, message):
        self.command[0] = np.clip(message.linear.x, *self.command_ranges['lin_vel_x'])
        self.command[2] = np.clip(message.angular.z, *self.command_ranges['ang_vel_z'])

    def _step(self):
        if not self.env.is_running():
            rclpy.try_shutdown()
            return
        self.sm.update(self.env.control_dt)
        is_rl = self.sm.state == 'rl'
        if not is_rl or not self.was_rl:
            self.obs_builder.reset()
        self.was_rl = is_rl
        if self.sm.state != 'rl':
            self.last_action[:] = 0  # RL starts from a fresh action history.
            self.leg_filter.reset()
        if isinstance(self.residual, ResidualWheelLQR):
            self.residual.update(self.command if self.sm.state == 'rl' else None, self.last_action)
        elif self.residual:
            self.residual.update(self.command if self.sm.state == 'rl' else None)
        sensors = self.residual.data if self.residual and self.sm.state == 'rl' else self.env.data
        quaternion = sensors.sensor('trunk_quat').data.astype(np.float32).copy()
        state = ObsState(
            self.env.joint_pos(), self.env.joint_vel(), quaternion,
            sensors.sensor('trunk_gyro').data.astype(np.float32).copy(),
            self.command, self.last_action,
            quat_wxyz_to_rotmat(quaternion).T @ self.env.base_lin_vel())
        obs = self.obs_builder.build(state)
        action = np.zeros(8, dtype=np.float32)
        applied = action.copy()
        if self.sm.state == 'rl':
            action = self.policy.run(['nn_output'], {'nn_input0': obs.reshape(1, -1)})[0].reshape(8)
            applied = self.leg_filter.update(action)
            def torque(positions, velocities):
                if isinstance(self.residual, WheelVelocityBias):
                    return self.residual.compute(self.action_adapter, applied, positions, velocities)
                result = self.action_adapter.compute(applied, positions, velocities)
                return self.residual.apply(result) if self.residual else result

            self.env.step_with_torque_callback(torque)
        else:
            self.env.step_with_torque_callback(self.sm.torque)
        self.last_action = action.copy()
        self.steps += 1
        self.obs_pub.publish(Float32MultiArray(data=obs.astype(float).tolist()))
        self.action_pub.publish(Float32MultiArray(data=action.astype(float).tolist()))
        self.applied_pub.publish(Float32MultiArray(data=applied.astype(float).tolist()))

    def run_interactive(self):
        """Read keys and spin the same ROS executor; physics stays on its timer."""
        saved = termios.tcgetattr(sys.stdin)
        target = np.zeros(2)
        current = np.zeros(2)
        last_key = previous = time.monotonic()
        print('[VALIDATION_SIM] 1: splay -> sit, 0: policy (after sit), 6: idle, 2: reset, '
              'w/s: forward/back, a/d: yaw, r: stop, Ctrl-C: quit.', flush=True)
        print(f"[VALIDATION_SIM] commands as trained: lin_vel_x {self.command_ranges['lin_vel_x']} m/s, "
              f"ang_vel_z {self.command_ranges['ang_vel_z']} rad/s, ramp "
              f"{'step' if self.command_ramp is None else f'{self.command_ramp:g}/s'}", flush=True)
        try:
            tty.setcbreak(sys.stdin.fileno())
            while rclpy.ok() and self.env.is_running():
                timeout = max(0., self.timer.time_until_next_call() / 1e9)
                if select.select([sys.stdin], [], [], timeout)[0]:
                    key = sys.stdin.read(1)
                    last_key = time.monotonic()
                    if key == '\x03':
                        raise KeyboardInterrupt
                    if key in 'ws':
                        target[0] = self.command_ranges['lin_vel_x'][1 if key == 'w' else 0]
                    elif key in 'ad':
                        target[1] = self.command_ranges['ang_vel_z'][1 if key == 'a' else 0]
                    elif key == 'r':
                        target[:] = 0.
                    elif key in '0126':
                        self._cmd_key_cb(String(data={'0': 'balance', '1': 'transform_up', '2': 'reset',
                                                      '6': 'idle'}[key]))
                        target[:] = current[:] = 0.
                now = time.monotonic()
                dt, previous = now - previous, now
                if now - last_key > .5:
                    target[:] = 0.
                step = np.inf if self.command_ramp is None else self.command_ramp * dt
                current += np.clip(target - current, -step, step)
                message = Twist()
                message.linear.x, message.angular.z = current.tolist()
                self._cmd_twist_cb(message)
                rclpy.spin_once(self, timeout_sec=0.)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, saved)
