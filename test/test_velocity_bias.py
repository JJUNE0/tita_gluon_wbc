"""DESKTOP_DRY_RUN: deployed math matches measured research traces and obeys lifecycle bounds."""

from pathlib import Path
import sys
import unittest

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.velocity_bias import VelocityBias


class VelocityBiasTests(unittest.TestCase):
    def test_same_feedback_sign_handles_drift_reversal_without_reset(self):
        law = VelocityBias(kp=0., ki=4., seed_gain=3., slew=3.)
        velocity = .3
        for disturbance in [.3, -.3, .15]:
            for _ in range(3000):
                bias = law.update(velocity, .02)
                velocity = disturbance - .3 * bias
            self.assertLess(abs(velocity), 1e-8)
            self.assertAlmostEqual(bias, disturbance / .3, delta=1e-8)
            self.assertEqual(law.response_sign, 1.)

    def test_positive_and_negative_drift_are_rejected_by_same_controller(self):
        for disturbance in [-.3, .3]:
            law = VelocityBias()
            velocity = disturbance
            for _ in range(10000):
                bias = law.update(velocity, .02)
                # Local measured FlashSAC low-frequency response has negative gain.
                velocity = disturbance - .3 * bias
            self.assertLess(abs(velocity), 1e-8)
            self.assertAlmostEqual(bias, disturbance / .3)

    def test_saturation_anti_windup_release_reentry_and_fault_samples(self):
        law = VelocityBias(limit=.2, slew=.1)
        previous = 0.
        for _ in range(300):
            value = law.update(100., .02)
            self.assertLessEqual(abs(value - previous), .002 + 1e-12)
            self.assertLessEqual(abs(value), .2)
            self.assertLessEqual(abs(law.integral), .2)
            previous = value
        for _ in range(200):
            law.update(0., .02, enabled=False)
        self.assertEqual(law.bias, 0.)
        self.assertEqual(law.integral, 0.)
        self.assertEqual(law.update(-1., .02), 0.)
        for _ in range(300):
            law.update(-1., .02)
        self.assertLess(law.bias, 0.)
        law.reset()
        self.assertEqual(law.bias, 0.)
        for velocity, dt in [(float('nan'), .02), (0., 0.), (0., float('inf'))]:
            with self.assertRaises(ValueError):
                law.update(velocity, dt)

    def test_matches_actual_simulation_candidate_outputs(self):
        root = REPO / 'docs/exp/2026-10-16/velocity_bias_overnight/coverage_v01'
        paths = sorted(root.glob('*/trace.npz'))
        self.assertEqual(len(paths), 40)
        maximum = 0.
        for path in paths:
            with np.load(path) as trace:
                law = VelocityBias(kp=2., ki=10., tau=.05, slew=2., seed_gain=0.)
                actual = np.array([law.update(float(v), .02) for v in trace['state'][:-1, 10]])
                expected = trace['input'][:, 0]
                maximum = max(maximum, float(np.max(abs(actual - expected))))
                np.testing.assert_allclose(actual, expected, atol=1e-11, rtol=1e-11,
                                           err_msg=path.parent.name)
        print('[DESKTOP_DRY_RUN] Runtime PI math / 40 measured candidate traces max error:', maximum)

    def test_velocity_seed_matches_40_guarded_nominal_research_traces(self):
        root = REPO / 'docs/exp/2026-10-16/velocity_bias_overnight/seeded_coverage01'
        paths = sorted(root.glob('*/trace.npz'))
        self.assertEqual(len(paths), 40)
        maximum = 0.
        for path in paths:
            with np.load(path) as trace:
                law = VelocityBias(kp=0., ki=4., seed_gain=3., slew=2.)
                actual = []
                for state in trace['state'][:-1]:
                    eligible = max(abs(state[4:6])) <= .3 and abs(state[10]) <= 1.
                    actual.append(law.update(float(state[10]), .02, enabled=eligible))
                expected = trace['input'][:, 0]
                maximum = max(maximum, float(np.max(abs(np.asarray(actual) - expected))))
                np.testing.assert_allclose(actual, expected, atol=1e-11, rtol=1e-11, err_msg=path.parent.name)
        print('[DESKTOP_DRY_RUN] Seeded integral math / 40 guarded candidate traces max error:', maximum)

    def test_selected_defaults_match_40_actual_runtime_traces(self):
        root = REPO / 'docs/exp/2026-10-16/velocity_bias_overnight/rate3_runtime01'
        paths = sorted(root.glob('*_v04_runtime_s920/trace.npz'))
        self.assertEqual(len(paths), 40)
        maximum = 0.
        for path in paths:
            with np.load(path) as trace:
                law = VelocityBias()
                actual = []
                for state in trace['state'][:-1]:
                    eligible = max(abs(state[4:6])) <= .3 and abs(state[10]) <= 1.
                    actual.append(law.update(float(state[10]), .02, enabled=eligible))
                expected = trace['input'][:, 0]
                maximum = max(maximum, float(np.max(abs(np.asarray(actual) - expected))))
                np.testing.assert_allclose(actual, expected, atol=1e-6, rtol=0., err_msg=path.parent.name)
        print('[DESKTOP_DRY_RUN] Selected defaults / 40 actual runtime traces max bias error:', maximum)

    def test_seed_is_cleared_on_inhibit_and_reinitialized_with_current_direction(self):
        law = VelocityBias(kp=0., ki=4., seed_gain=3.)
        self.assertEqual(law.update(-.1, .02), 0.)
        self.assertLess(law.integral, -.3)
        law.update(0., .02, enabled=False)
        self.assertFalse(law.seeded)
        self.assertEqual(law.integral, 0.)
        self.assertEqual(law.update(.1, .02), 0.)
        self.assertGreater(law.integral, .3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
