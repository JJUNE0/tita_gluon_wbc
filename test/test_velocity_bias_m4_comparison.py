"""VALIDATION_SIM: hybrid removes only nominal M4 bias and keeps the torque path."""

import unittest

import numpy as np

from compare_velocity_bias_m4 import Comparison, M4WithoutFixedBias
from sim2sim_ros2_jazzy.residual_wheel_lqr import ResidualWheelLQR


class HybridComparisonTests(unittest.TestCase):
    def test_frozen_correction_without_fixed_bias_on_same_sensor_stream(self):
        experiment = Comparison(dict(seed=913, warmup=1.2, mode='baseline', physics={}))
        self.addCleanup(experiment.env.close)
        fixed = ResidualWheelLQR(experiment.env)
        hybrid = M4WithoutFixedBias(experiment.env)
        peak = 0.
        for _ in range(200):
            action = experiment.runner.playback.last_action
            fixed.update(np.zeros(3), action)
            hybrid.update(np.zeros(3), action)
            self.assertAlmostEqual(hybrid.correction, fixed.correction, places=12)
            self.assertAlmostEqual(hybrid.u, fixed.correction, places=12)
            self.assertLessEqual(abs(hybrid.u), .050000001)
            peak = max(peak, abs(hybrid.u))
            experiment.step()
        self.assertGreater(peak, .001)
        print('[VALIDATION_SIM] same sensor stream: frozen correction matches, fixed bias removed')

    def test_hybrid_warmup_history_legs_and_torque_order(self):
        experiment = Comparison(dict(seed=913, warmup=1.2, mode='hybrid', physics={}))
        self.addCleanup(experiment.env.close)
        for _ in range(260):
            step = experiment.step()  # Includes per-substep torque, leg and raw-history assertions.
            self.assertLessEqual(abs(step['m4_torque']), .050000001)
        self.assertGreater(abs(experiment.velocity.u), .001)
        self.assertGreater(abs(experiment.m4.u), .001)
        print('[VALIDATION_SIM] hybrid: common acquisition, native velocity PD, then bounded LQR PASS')


if __name__ == '__main__':
    unittest.main()
