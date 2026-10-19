"""VALIDATION_SIM: saved observation layout and native joint PD targets."""

from dataclasses import dataclass

import numpy as np

NATIVE_JOINTS = [f'joint_{side}_leg_{index}' for side in ('left', 'right') for index in range(1, 5)]
ISAAC_JOINTS = [f'joint_{side}_leg_{index}' for index in range(1, 5) for side in ('left', 'right')]


def quat_wxyz_to_rotmat(quaternion):
    w, x, y, z = np.asarray(quaternion, dtype=np.float32)
    return np.array([
        [1 - 2*(y*y + z*z), 2*(x*y - z*w), 2*(x*z + y*w)],
        [2*(x*y + z*w), 1 - 2*(x*x + z*z), 2*(y*z - x*w)],
        [2*(x*z - y*w), 2*(y*z + x*w), 1 - 2*(x*x + y*y)],
    ], dtype=np.float32)


def quat_wxyz_to_rpy(quaternion):
    w, x, y, z = np.asarray(quaternion, dtype=np.float32)
    return np.array([
        np.arctan2(2*(w*x + y*z), 1 - 2*(x*x + y*y)),
        np.arcsin(np.clip(2*(w*y - z*x), -1, 1)),
        np.arctan2(2*(w*z + x*y), 1 - 2*(y*y + z*z)),
    ], dtype=np.float32)


@dataclass
class ObsState:
    joint_pos: np.ndarray
    joint_vel: np.ndarray
    base_quat_wxyz: np.ndarray
    base_ang_vel: np.ndarray
    command: np.ndarray
    last_action: np.ndarray
    base_lin_vel_b: np.ndarray | None = None


class ObservationBuilder:
    def __init__(self, cfg):
        self.layout = cfg['policy_interface']['observations']
        self.size = cfg['policy']['obs_dim']
        self.defaults = np.asarray(cfg['robot']['default_joint_angles'], dtype=np.float32)
        self.vel_defaults = np.asarray(cfg['robot']['default_joint_velocities'], dtype=np.float32)
        self.position_term = next((term for term in self.layout if term['kind'] == 'wheel_position_error'), None)
        self.heading_term = next((term for term in self.layout if term['kind'] == 'heading_error'), None)
        if self.heading_term is not None:
            self.dt = cfg['control']['sim_timestep'] * cfg['control']['decimation']
            self.heading_warmup = max(1, round(self.heading_term['params']['warmup_s'] / self.dt))
        # Gyro z bias [rad/s] subtracted before integration; the robot uses its pre-RL stationary estimate.
        self.gyro_bias = 0.
        self.reset()

    def reset(self):
        self.previous_wheels = None
        self.unwrapped_wheels = None
        self.reference = None
        self.heading_hold = 0
        self.heading = 0.

    def wheel_position_error(self, state):
        params = self.position_term['params']
        q = np.asarray(state.joint_pos, dtype=np.float64)
        if not all(np.isfinite(value).all() for value in (q, state.base_quat_wxyz, state.command)):
            raise ValueError('non-finite wheel position inputs')
        wheels = q[[3, 7]]
        if self.previous_wheels is None:
            self.unwrapped_wheels = wheels.copy()
        else:
            # Same encoder unwrap as C++; valid when travel per policy tick is < pi.
            delta = wheels - self.previous_wheels
            self.unwrapped_wheels += np.arctan2(np.sin(delta), np.cos(delta))
        self.previous_wheels = wheels.copy()
        pitch = float(quat_wxyz_to_rpy(state.base_quat_wxyz)[1])
        distance = params['radius'] * np.mean(self.unwrapped_wheels + pitch + q[[1, 5]] + q[[2, 6]])
        zero = (np.abs(np.asarray(state.command, dtype=np.float32))
                <= np.asarray(params['zero_thresholds'], dtype=np.float32)).all()
        if self.reference is None or not zero:
            self.reference = distance
        error = distance - self.reference if zero else 0.
        return np.array([np.clip(error, -params['clip_m'], params['clip_m'])], dtype=np.float32)

    def heading_error(self, state):
        # Same rule as the training GyroHeadingError: integrate after warmup inside the zero band, clip output only.
        params = self.heading_term['params']
        gyro_z = float(np.asarray(state.base_ang_vel, dtype=np.float64)[2])
        if not (np.isfinite(gyro_z) and np.isfinite(state.command).all()):
            raise ValueError('non-finite heading inputs')
        zero = (np.abs(np.asarray(state.command, dtype=np.float32))
                <= np.asarray(params['zero_thresholds'], dtype=np.float32)).all()
        self.heading_hold = self.heading_hold + 1 if zero else 0
        if zero and self.heading_hold > self.heading_warmup:
            self.heading += (gyro_z - self.gyro_bias) * self.dt
        else:
            self.heading = 0.
        return np.array([np.clip(self.heading, -params['clip_rad'], params['clip_rad'])], dtype=np.float32)

    def build(self, state):
        values = {
            'ang_vel': state.base_ang_vel,
            'gravity': quat_wxyz_to_rotmat(state.base_quat_wxyz).T @ np.array([0., 0., -1.]),
            'commands': state.command,
            'last_action': state.last_action,  # Keep policy order, before joint mapping.
            'lin_vel': state.base_lin_vel_b,
            'joint_pos': np.asarray(state.joint_pos, dtype=np.float32) - self.defaults,
            'joint_vel': np.asarray(state.joint_vel, dtype=np.float32) - self.vel_defaults,
        }
        if self.position_term is not None:
            values['wheel_position_error'] = self.wheel_position_error(state)
        if self.heading_term is not None:
            values['heading_error'] = self.heading_error(state)
        parts = []
        for term in self.layout:
            value = np.asarray(values[term['kind']], dtype=np.float32).copy()
            if term.get('zero_wheel_pos'):
                value[[3, 7]] = 0.
            if 'joints' in term:
                value = value[[NATIVE_JOINTS.index(name) for name in term['joints']]]
            if term['clip'] is not None:
                value = np.clip(value, *term['clip'])
            parts.append(value * np.asarray(term['scale'], dtype=np.float32))
        observation = np.concatenate(parts).astype(np.float32)
        if observation.shape != (self.size,) or not np.isfinite(observation).all():
            raise ValueError(f'Observation layout mismatch or non-finite values: {observation.shape}')
        return observation


class LegActionFilter:
    """Call once per 50 Hz inference; keep raw action for the observation history."""

    def __init__(self, mode, joint_order, notch_hz=8.3, notch_q=3.):
        if mode not in ('none', 'ma2_legs', 'ma2_notch_legs'):
            raise ValueError('unknown leg_action_filter')
        if sorted(joint_order) != list(range(8)):
            raise ValueError('invalid filter joint mapping')
        self.mode = mode
        self.legs = np.array([j not in (3, 7) for j in joint_order])
        self.previous = None
        self.z1 = self.z2 = None
        if mode == 'ma2_notch_legs':
            if (not np.isfinite([notch_hz, notch_q]).all() or
                    not 0 < notch_hz < 25 or notch_q <= 0 or notch_hz / notch_q >= 25):
                raise ValueError('notch requires 0 < frequency < 25 Hz, Q > 0, bandwidth < 25 Hz')
            omega = 2 * np.pi * notch_hz / 50
            gain = 1 / (1 + np.tan(omega / (2 * notch_q)))
            self.b = np.array([gain, -2 * gain * np.cos(omega), gain])
            self.a = np.array([1., self.b[1], 2 * gain - 1])

    def reset(self):
        self.previous = None
        self.z1 = self.z2 = None

    def update(self, raw):
        raw = np.asarray(raw, dtype=np.float32)
        if raw.shape != (8,) or not np.isfinite(raw).all():
            raise ValueError('invalid leg filter action')
        applied = raw.copy()
        if self.mode != 'none' and self.previous is not None:
            applied[self.legs] = .5 * raw[self.legs] + .5 * self.previous[self.legs]
        if self.mode == 'ma2_notch_legs':
            x = applied[self.legs].astype(np.float64)
            if self.z1 is None:
                # Steady-state initialization gives exact first/DC pass-through.
                self.z1 = (1 - self.b[0]) * x
                self.z2 = (self.b[2] - self.a[2]) * x
            else:
                y = self.b[0] * x + self.z1
                self.z1 = self.b[1] * x - self.a[1] * y + self.z2
                self.z2 = self.b[2] * x - self.a[2] * y
                applied[self.legs] = y
        if not np.isfinite(applied).all():
            raise ValueError('non-finite leg filter output')
        self.previous = raw.copy()
        return applied


class ActionAdapter:
    """Map policy order to MuJoCo order, then apply position/velocity PD."""

    def __init__(self, cfg):
        terms = cfg['policy_interface']['actions']
        self.order = [NATIVE_JOINTS.index(term['joint']) for term in terms]
        self.scale = np.asarray([term['scale'] for term in terms], dtype=np.float32)
        self.offset = np.asarray([term['offset'] for term in terms], dtype=np.float32)
        self.clip = np.asarray([term['clip'] or [-np.inf, np.inf] for term in terms])
        self.velocity = np.zeros(8, dtype=bool)
        self.velocity[self.order] = [term['kind'] == 'velocity' for term in terms]
        self.kp = np.asarray(cfg['robot']['joint_kp'], dtype=np.float32)
        self.kd = np.asarray(cfg['robot']['joint_kd'], dtype=np.float32)
        self.limit = np.asarray(cfg['robot']['torque_limit'], dtype=np.float32)

    def targets(self, action):
        action = np.asarray(action, dtype=np.float32)
        if action.shape != (8,) or not np.isfinite(action).all():
            raise ValueError('Invalid or non-finite policy action')
        processed = np.clip(action * self.scale + self.offset, self.clip[:, 0], self.clip[:, 1])
        targets = np.empty(8, dtype=np.float32)
        targets[self.order] = processed
        return targets

    def compute(self, action, joint_pos, joint_vel):
        targets = self.targets(action)
        position_error = np.where(self.velocity, 0., targets - joint_pos)
        velocity_target = np.where(self.velocity, targets, 0.)
        torque = self.kp * position_error + self.kd * (velocity_target - joint_vel)
        return np.clip(torque, -self.limit, self.limit)
