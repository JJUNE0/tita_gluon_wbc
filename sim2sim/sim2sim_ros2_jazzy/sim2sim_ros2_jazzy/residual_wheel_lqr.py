"""VALIDATION_SIM: frozen model_60000 M4 residual; no online identification."""

import numpy as np

from .residual_wheel_pd import ResidualWheelPD

# Frozen from docs/exp/2026-10-15/flash_overnight_pipeline/run_final/gains_frozen.json.
# State: encoder p/v, IMU pitch/rate, previous raw action8, native leg q6/dq6.
K = np.array([
    -19.742442086143033, -20.696383544789906, 16.840158142230806, -7.937603936362346,
    8.103037367908843, -4.784195179102777, -4.990906972076356, 24.840508583590285,
    7.861664438569217, 15.72037581011739, -15.26560968776548, -19.81814375642627,
    13.451378691763411, 40.840298865637166, 12.983556877148244, 2.0817908743173237,
    -89.65179648030504, 38.00549200282186, 712.921104178439, 1.4790982549232279,
    7.634482158476087, -715.4968390550263, -8.951874903338297, 2.2313013812681137,
])
REFERENCE = np.array([
    0.0, 0.0, 0.05231580168830151, -4.034573919559486e-09,
    -0.8180009782976574, 0.3611045290529728, -0.13207465370289154, -0.012457838284576105,
    0.7314805508073833, 0.25010435211161774, -0.10895301156987747, -0.03608260363081677,
    0.01218336467553551, 0.8742186339944601, -1.8193678752746847, -0.03348179519435184,
    0.8523016801807616, -1.8095878709852695, -3.502021007202671e-10, 6.969365421028116e-09,
    4.114762903005322e-10, -1.1615357240912513e-09, 1.959838263389709e-09, 1.0656585109775536e-09,
])
CHECKPOINT_SHA256 = "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05"
BIAS = .4828
LEGS = [0, 1, 2, 4, 5, 6]


class ResidualWheelLQR(ResidualWheelPD):
    def __init__(self, env):
        if env.cfg['policy_interface']['checkpoint_sha256'] != CHECKPOINT_SHA256:
            raise ValueError('Fixed M4 requires the calibrated FlashSAC model_60000 checkpoint')
        if not np.isclose(env.control_dt, .02):
            raise ValueError('Fixed M4 requires a 20 ms control period')
        super().__init__(env)

    def reset(self):
        super().reset()
        self.correction = 0.

    def update(self, command, previous_action):
        self.previous_action = np.asarray(previous_action, dtype=float)
        if self.previous_action.shape != (8,) or not np.isfinite(self.previous_action).all():
            raise ValueError('Fixed M4 requires eight finite previous raw actions')
        super().update(command)

    def _target(self, rotation):
        roll, pitch, _ = rotation.as_euler('xyz')
        gyro = self.data.sensor('trunk_gyro').data
        pitch_rate = gyro[1] * np.cos(roll) - gyro[2] * np.sin(roll)
        state = np.r_[self.position, self.velocity, pitch, pitch_rate, self.previous_action,
                      self.env.joint_pos()[LEGS], self.env.joint_vel()[LEGS]]
        if not np.isfinite(state).all():
            raise ValueError('Non-finite M4 state')
        phase = min(self.age / 1.5, 1.)
        ramp = phase * phase * (3. - 2. * phase)
        if self.age == 0.:
            self.correction = 0.
        target = ramp * np.clip(-K @ (state - REFERENCE), -.05, .05)
        delta = 2. * self.env.control_dt
        self.correction = float(np.clip(target, self.correction - delta, self.correction + delta))
        return BIAS + self.correction
