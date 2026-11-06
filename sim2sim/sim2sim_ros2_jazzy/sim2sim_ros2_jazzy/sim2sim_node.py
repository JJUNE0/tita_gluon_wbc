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
from geometry_msgs.msg import Twist, Vector3
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String

from .adapter import ActionAdapter, LegActionFilter, ObservationBuilder, ObsState, quat_wxyz_to_rotmat, quat_wxyz_to_rpy
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
        self.declare_parameter('support_mode', -1)
        fixed_lqr = self.get_parameter('fixed_residual_lqr').value
        residual_pd = self.get_parameter('residual_wheel_pd').value
        velocity_bias = self.get_parameter('velocity_bias').value
        if sum([fixed_lqr, residual_pd, velocity_bias]) > 1:
            raise ValueError('Choose one residual controller')
        self.cfg = json.loads(Path(self.get_parameter('config').value).read_text())
        self.pose_cfg = self.cfg.get('pose_command')
        self.pose_target = self.pose_command = None
        if self.pose_cfg is not None:
            self.nominal_pose = np.array([0., 0., self.pose_cfg['nominal_height']], dtype=np.float32)
            self.pose_command = self.nominal_pose.copy()
            self.pose_target = self.nominal_pose.copy()
            self.pose_ranges = np.asarray([self.pose_cfg[name] for name in
                                           ('roll_range', 'pitch_range', 'height_range')], dtype=np.float32)
            self.pose_rates = np.asarray(self.pose_cfg['ramp_rates'], dtype=np.float32)
        requested_support = self.get_parameter('support_mode').value
        if requested_support not in (-1, 0, 1, 2):
            raise ValueError('Support mode must be 0, 1 or 2')
        if requested_support != -1 and 'support_command' not in self.cfg:
            raise ValueError('This checkpoint has no support-mode command')
        self.support_mode = self.cfg.get('support_command', {}).get('default_mode', 2)
        if requested_support != -1:
            self.support_mode = requested_support
        self.support_fall_tilt = None
        if 'support_command' in self.cfg:
            tilt = self.cfg['control'].get('support_fall_tilt_deg', 55.0)
            if isinstance(tilt, bool) or not isinstance(tilt, (int, float)) or not np.isfinite(tilt) or not 0 < tilt < 90:
                raise ValueError('control.support_fall_tilt_deg must be finite and between 0 and 90 degrees')
            self.support_fall_tilt = np.radians(tilt)
        self.tilt_faults = 0
        self.walking = 'gait_command' in self.cfg
        if (self.walking or 'support_command' in self.cfg or self.pose_cfg is not None) and any((fixed_lqr, residual_pd, velocity_bias)):
            raise ValueError('Wheel residual controllers require a driving checkpoint without gait/support/pose commands')
        # Old exported configs retain their original caps until prepared again.
        caps = self.cfg['command']
        self.command_ranges = self.cfg.get('sim_command_ranges', {
            'lin_vel_x': [-caps['max_lin_x'], caps['max_lin_x']],
            'lin_vel_y': [0., 0.],
            'ang_vel_z': [-caps['max_ang_z'], caps['max_ang_z']],
        })
        # Training command ramp [units/s]; None = step change. Configs exported before this key keep 0.5/s.
        self.command_ramp = self.cfg.get('sim_command_ramp', .5)
        self.env = TitaMujocoEnv(self.cfg, viewer_enabled=self.get_parameter('viewer').value)
        if self.cfg['model'].get('ground_friction') is not None:
            self.get_logger().info(f"Terrain sliding friction: {self.cfg['model']['ground_friction']:g}")
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
        self.command_target = np.zeros(3, dtype=np.float32)
        self.last_action = np.zeros(8, dtype=np.float32)
        self.steps = 0
        self.was_rl = False
        # Headless runs have no keyboard, so they stand up and enter RL automatically.
        self.sm = StateMachine(self.cfg['robot']['torque_limit'], auto_rl=not self.get_parameter('viewer').value)
        if self.support_fall_tilt is not None:
            self.get_logger().info(f'Support RL total-tilt cutoff: {np.degrees(self.support_fall_tilt):g} deg')
        self.env.reset(SPLAY_POSE)
        if self.sm.auto_rl:
            self.sm.request('transform_up', self.env.joint_pos())
        self.create_subscription(String, '/tita/command/manager/cmd_key', self._cmd_key_cb, 10)
        self.create_subscription(Twist, '/tita/command/manager/cmd_twist', self._cmd_twist_cb, 10)
        if self.pose_cfg is not None:
            self.create_subscription(Vector3, '/tita/command/manager/cmd_pose', self._cmd_pose_cb, 10)
        self.obs_pub = self.create_publisher(Float32MultiArray, '/sim2sim/debug/obs', 10)
        self.action_pub = self.create_publisher(Float32MultiArray, '/sim2sim/debug/action', 10)
        self.applied_pub = self.create_publisher(Float32MultiArray, '/sim2sim/debug/action_applied', 10)
        self.timer = self.create_timer(self.env.control_dt, self._step)
        self.get_logger().info(self.cfg['policy_interface']['checkpoint'])

    def _cmd_key_cb(self, message):
        if message.data in ('support_left', 'support_right', 'support_both'):
            if 'support_command' not in self.cfg:
                self.get_logger().warn('This checkpoint has no support-mode command')
                return
            self.support_mode = ('support_left', 'support_right', 'support_both').index(message.data)
            self.get_logger().info(f'support mode: {self.support_mode}')
        elif message.data in ('pose_stand', 'reset'):
            self.env.reset(SPLAY_POSE)
            self.command[:] = self.command_target[:] = 0.
            self.last_action[:] = 0.
            if self.pose_cfg is not None:
                self.pose_command[:] = self.pose_target[:] = self.nominal_pose
            self.obs_builder.reset()
            self.leg_filter.reset()
            self.was_rl = False
            self.sm.request('idle', self.env.joint_pos())
        elif message.data in ('balance', 'rl_0'):
            if not self.sm.request('rl', self.env.joint_pos()):
                self.get_logger().warn('RL rejected: press 1 (transform_up) and wait for sit first')
        elif message.data in ('idle', 'transform_up'):
            self.sm.request(message.data, self.env.joint_pos())
        self.get_logger().info(f'state: {self.sm.state}')

    def _cmd_twist_cb(self, message):
        for index, (value, name) in enumerate(zip(
            (message.linear.x, message.linear.y, message.angular.z), ('lin_vel_x', 'lin_vel_y', 'ang_vel_z')
        )):
            self.command_target[index] = np.clip(value, *self.command_ranges.get(name, [0., 0.]))
        if not self.walking:
            self.command[:] = self.command_target

    def _cmd_pose_cb(self, message):
        if self.pose_cfg is None:
            self.get_logger().warn('This checkpoint has no roll/pitch/height command')
            return
        target = np.asarray([message.x, message.y, message.z], dtype=np.float32)
        if not np.isfinite(target).all():
            self.get_logger().warn('Ignoring non-finite pose command')
            return
        self.pose_target[:] = np.clip(target, self.pose_ranges[:, 0], self.pose_ranges[:, 1])

    def _step(self):
        if not self.env.is_running():
            rclpy.try_shutdown()
            return
        self.sm.update(self.env.control_dt)
        is_rl = self.sm.state == 'rl'
        if is_rl and self.support_fall_tilt is not None:
            rotation = quat_wxyz_to_rotmat(self.env.base_quat_sensor())
            tilt = np.arccos(np.clip(rotation[2, 2], -1., 1.))
            if tilt > self.support_fall_tilt:
                self.sm.request('damp', self.env.joint_pos())
                self.command[:] = self.command_target[:] = 0.
                self.tilt_faults += 1
                is_rl = False
                self.get_logger().warn(f'Total tilt {np.degrees(tilt):.1f} deg exceeded support cutoff; entering damp')
        if not is_rl or not self.was_rl:
            self.obs_builder.reset()
            if self.pose_cfg is not None:
                self.pose_command[:] = self.nominal_pose
            if self.walking:
                self.command[:] = 0.
        self.was_rl = is_rl
        motion_range = self.pose_cfg.get('height_motion_range') if self.pose_cfg is not None else None
        if motion_range is not None:
            lo, hi = motion_range
            motion = np.clip((self.pose_command[2] - lo) / (hi - lo), 0., 1.)
            self.command[:] = self.command_target * motion
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
            quat_wxyz_to_rotmat(quaternion).T @ self.env.base_lin_vel(), support_mode=self.support_mode,
            pose_command=self.pose_command)
        obs = self.obs_builder.build(state)
        action = np.zeros(8, dtype=np.float32)
        applied = action.copy()
        if self.sm.state == 'rl':
            action = self.policy.run(['nn_output'], {'nn_input0': obs.reshape(1, -1)})[0].reshape(8)
            applied = self.leg_filter.update(action)
            # Freeze the same mode that was present in this policy observation
            # for every physics substep. The next gait state is computed later.
            gait_enabled = self.obs_builder.gait_enabled
            def torque(positions, velocities):
                if isinstance(self.residual, WheelVelocityBias):
                    return self.residual.compute(self.action_adapter, applied, positions, velocities)
                result = self.action_adapter.compute(applied, positions, velocities, gait_enabled=gait_enabled)
                return self.residual.apply(result) if self.residual else result

            self.env.step_with_torque_callback(torque)
            if self.pose_cfg is not None:
                delta = self.pose_rates * np.float32(self.env.control_dt)
                desired = self.pose_target.copy()
                if motion_range is not None:
                    height = self.pose_command[2] + np.clip(desired[2] - self.pose_command[2], -delta[2], delta[2])
                    motion = np.clip((height - lo) / (hi - lo), 0., 1.)
                    desired[:2] *= motion
                    self.command[:] = self.command_target * motion
                self.pose_command += np.clip(desired - self.pose_command, -delta, delta)
            if self.walking:
                elapsed = self.obs_builder.next_gait_elapsed
                settle = self.cfg['sim_command_initial_phase_time']
                settling = elapsed <= settle
                if self.cfg['gait_command'].get('clock') == 'episode_steps':
                    settling = elapsed < settle  # mjlab emits its first ramp sample at t >= settle.
                if settling:
                    self.command[:] = 0.
                else:
                    step = np.inf if self.command_ramp is None else self.command_ramp * self.env.control_dt
                    self.command += np.clip(self.command_target - self.command, -step, step)
                self.obs_builder.advance_gait(self.command)
                if self.env.viewer is not None:
                    rotation = quat_wxyz_to_rotmat(self.env.base_quat_sensor())
                    velocity = rotation.T @ self.env.base_lin_vel()
                    wheel_policy = self.action_adapter.gait_gate.any() and not self.obs_builder.gait_enabled
                    wheel_policy |= any(term.get('gate') == 'always' for term in self.cfg['policy_interface']['actions'])
                    self.env.viewer.set_texts((None, None, 'MuJoCo walk | body m/s\nCMD vx / vy\nACT vx / vy\nGait phase\nWheel policy',
                        f'\n{self.command[0]:+.3f} / {self.command[1]:+.3f}\n'
                        f'{velocity[0]:+.3f} / {velocity[1]:+.3f}\n{self.obs_builder.gait_phase:.3f}\n'
                        f'{"ON" if wheel_policy else "OFF"}'))
        else:
            self.env.step_with_torque_callback(self.sm.torque)
        if self.pose_cfg is not None and self.env.viewer is not None:
            actual = quat_wxyz_to_rpy(self.env.base_quat())
            self.env.viewer.set_texts((None, None, 'Pose | roll deg / pitch deg / height m\nTARGET\nCMD\nACT\nState',
                f'\n{np.degrees(self.pose_target[0]):+.1f} / {np.degrees(self.pose_target[1]):+.1f} / {self.pose_target[2]:.3f}\n'
                f'{np.degrees(self.pose_command[0]):+.1f} / {np.degrees(self.pose_command[1]):+.1f} / {self.pose_command[2]:.3f}\n'
                f'{np.degrees(actual[0]):+.1f} / {np.degrees(actual[1]):+.1f} / {self.env.base_pos()[2]:.3f}\n{self.sm.state}'))
        self.last_action = action.copy()
        self.steps += 1
        self.obs_pub.publish(Float32MultiArray(data=obs.astype(float).tolist()))
        self.action_pub.publish(Float32MultiArray(data=action.astype(float).tolist()))
        self.applied_pub.publish(Float32MultiArray(data=applied.astype(float).tolist()))

    def run_interactive(self):
        """Read keys and spin the same ROS executor; physics stays on its timer."""
        saved = termios.tcgetattr(sys.stdin)
        target = np.zeros(3)
        current = np.zeros(3)
        last_key = previous = time.monotonic()
        startup = '1: splay -> sit, 0: policy (after sit), 6: idle.'
        print(f'[VALIDATION_SIM] {startup} 2: reset, w/s: forward/back, q/e: left/right, '
              'a/d: yaw, r: stop command, Ctrl-C: quit.', flush=True)
        if 'support_command' in self.cfg:
            print('[VALIDATION_SIM] Support: 7 = mode 0 left, 8 = mode 1 right, 9 = mode 2 both.', flush=True)
        pose_keys = {'j': (0, np.radians(1.)), 'l': (0, -np.radians(1.)),
                     'i': (1, np.radians(1.)), 'k': (1, -np.radians(1.)),
                     'u': (2, .01), 'o': (2, -.01)}
        if self.pose_cfg is not None:
            print('[VALIDATION_SIM] Pose: j/l roll +/-1 deg, i/k pitch +/-1 deg, u/o height +/-1 cm, p nominal pose. '
                  f'Ranges: roll {np.degrees(self.pose_ranges[0]).tolist()} deg, '
                  f'pitch {np.degrees(self.pose_ranges[1]).tolist()} deg, height {self.pose_ranges[2].tolist()} m.', flush=True)
        print(f"[VALIDATION_SIM] command limits (tita.yaml capped by trained ranges): lin_vel_x {self.command_ranges['lin_vel_x']} m/s, "
              f"lin_vel_y {self.command_ranges.get('lin_vel_y', [0., 0.])} m/s, "
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
                        target[2] = self.command_ranges['ang_vel_z'][1 if key == 'a' else 0]
                    elif key in 'qe':
                        target[1] = self.command_ranges.get('lin_vel_y', [0., 0.])[1 if key == 'q' else 0]
                    elif key == 'r':
                        target[:] = 0.
                    elif self.pose_cfg is not None and (key in pose_keys or key == 'p'):
                        pose_target = self.nominal_pose.copy() if key == 'p' else self.pose_target.copy()
                        if key in pose_keys:
                            axis, increment = pose_keys[key]
                            pose_target[axis] += increment
                        self._cmd_pose_cb(Vector3(x=float(pose_target[0]), y=float(pose_target[1]), z=float(pose_target[2])))
                    elif key in '789':
                        self._cmd_key_cb(String(data={'7': 'support_left', '8': 'support_right',
                                                      '9': 'support_both'}[key]))
                    elif key in '0126':
                        self._cmd_key_cb(String(data={'0': 'balance', '1': 'transform_up', '2': 'reset',
                                                      '6': 'idle'}[key]))
                        target[:] = current[:] = 0.
                now = time.monotonic()
                dt, previous = now - previous, now
                if now - last_key > .5:
                    target[:] = 0.
                step = np.inf if self.walking or self.command_ramp is None else self.command_ramp * dt
                current += np.clip(target - current, -step, step)
                message = Twist()
                message.linear.x, message.linear.y, message.angular.z = current.tolist()
                self._cmd_twist_cb(message)
                rclpy.spin_once(self, timeout_sec=0.)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, saved)
