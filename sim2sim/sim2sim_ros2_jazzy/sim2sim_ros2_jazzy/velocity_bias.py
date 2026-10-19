"""DESKTOP_DRY_RUN / VALIDATION_SIM: bounded signed velocity feedback, no nominal torque bias."""

import math

import numpy as np

from .residual_wheel_pd import ResidualWheelPD


class VelocityBias:
    """Velocity bias in m/s: initial velocity seed, then bounded PI feedback.

    Positive response_sign is calibrated for the measured low-frequency
    FlashSAC closed-loop response in MuJoCo, not a hardware motor sign claim.
    """

    def __init__(self, kp=0., ki=4., tau=.1, limit=2., slew=3., ramp=.25, response_sign=1., seed_gain=3.):
        values = (kp, ki, tau, limit, slew, ramp, response_sign, seed_gain)
        if (not all(math.isfinite(v) for v in values) or min(tau, limit, slew, ramp) <= 0
                or seed_gain < 0):
            raise ValueError('Invalid velocity-bias parameters')
        if response_sign not in (-1., 1.):
            raise ValueError('Velocity response sign must be -1 or +1')
        self.kp, self.ki, self.tau = kp, ki, tau
        self.limit, self.slew, self.ramp = limit, slew, ramp
        self.response_sign = response_sign
        self.seed_gain = seed_gain
        self.reset()

    def reset(self):
        self.filtered = self.integral = self.bias = self.age = 0.
        self.seeded = False

    def update(self, velocity, dt, enabled=True):
        if not math.isfinite(velocity) or not math.isfinite(dt) or dt <= 0:
            raise ValueError('Invalid velocity-bias sample')
        if enabled:
            if not self.seeded:
                self.integral = min(max(self.response_sign * self.seed_gain * velocity, -self.limit), self.limit)
                self.seeded = True
            self.filtered += (1. - math.exp(-dt / max(self.tau, dt))) * (velocity - self.filtered)
            change = self.response_sign * self.ki * self.filtered * dt
            proposed = min(max(self.integral + change, -self.limit), self.limit)
            desired = proposed + self.response_sign * self.kp * self.filtered
            if abs(desired) <= self.limit or desired * change < 0:
                self.integral = proposed
            desired = min(max(self.integral + self.response_sign * self.kp * self.filtered,
                              -self.limit), self.limit)
            phase = min(self.age / self.ramp, 1.)
            desired *= phase * phase * (3. - 2. * phase)
            self.age += dt
        else:
            self.filtered = self.integral = self.age = 0.
            self.seeded = False
            desired = 0.
        delta = self.slew * dt
        self.bias = min(max(desired, self.bias - delta), self.bias + delta)
        return self.bias


class WheelVelocityBias(ResidualWheelPD):
    """VALIDATION_SIM: zero-command velocity targets before native wheel PD clipping.

    The observer uses the current IMU, encoders and relative wheel/base FK.
    Severe wheel slip is not observable as chassis speed with these sensors.
    The fixed M4 torque bias and gain are deliberately a separate selectable mode.
    """

    ACQUISITION_SECONDS = 2.

    def __init__(self, env):
        if env.cfg['policy_interface'].get('algorithm') != 'FlashSAC':
            raise ValueError('Velocity bias is calibrated for FlashSAC checkpoints')
        if not np.isclose(env.control_dt, .02):
            raise ValueError('Velocity bias requires the validated 20 ms control period')
        self.law = VelocityBias()
        self.base_body = env.model.body('base_link').id
        super().__init__(env)
        self.wheel_bodies = env.model.jnt_bodyid[self.joints[[3, 7]]]

    def reset(self):
        super().reset()
        self.law.reset()
        self.previous_offset = None
        self.eligible = False

    @property
    def slew_rate(self):
        return self.law.slew  # Velocity target bias, m/s².

    def update(self, command):
        super().update(command)
        if not self.holding:
            self.law.reset()
            self.previous_offset = None
            self.eligible = False

    def _target(self, rotation):
        if self.age == 0.:
            self.law.reset()
            self.previous_offset = None
        offset = self.data.xpos[self.wheel_bodies].mean(0) - self.data.xpos[self.base_body]
        roll, pitch, yaw = rotation.as_euler('xyz')
        forward = np.array([np.cos(yaw), np.sin(yaw), 0.])
        if self.previous_offset is not None:
            self.velocity -= (offset - self.previous_offset) @ forward / self.env.control_dt
        self.previous_offset = offset.copy()
        # Acquire after stand-up; reject gross wheelspin/tilt rather than integrate it.
        self.eligible = (self.age + 1e-9 >= self.ACQUISITION_SECONDS and max(abs(roll), abs(pitch)) <= .3
                         and abs(self.velocity) <= 1.)
        return self.law.update(float(self.velocity), self.env.control_dt, enabled=self.eligible)

    def compute(self, adapter, action, positions, velocities):
        if not adapter.velocity[[3, 7]].all():
            raise ValueError('Velocity bias requires native wheel velocity targets')
        torque = adapter.compute(action, positions, velocities)
        targets = adapter.targets(action)[[3, 7]]
        # Float32 target addition matches the checkpoint adapter and research runner.
        targets += self.signs * self.u / self.radius
        torque[[3, 7]] = np.clip(adapter.kd[[3, 7]] * (targets - velocities[[3, 7]]),
                                -adapter.limit[[3, 7]], adapter.limit[[3, 7]])
        return torque
