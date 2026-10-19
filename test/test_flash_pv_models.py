"""DESKTOP_DRY_RUN: synthetic identification and independent prediction checks."""

import unittest
import numpy as np

from analyze_flash_pv_models import fit_model, free_run
from eval_flash_pv_models import waveform


class ModelComparisonTests(unittest.TestCase):
    def test_known_two_and_four_state_models_recovered(self):
        rng = np.random.default_rng(15)
        for n in [2, 4]:
            A = rng.normal(0., .1, (n, n)) + np.eye(n)*.7
            A[:, 0] = 0.; A[0, 0] = 1.
            B = rng.normal(0., .01, n)
            x = rng.normal(0., 1., (600, n)); u = rng.normal(0., .2, 600)
            y = x@A.T + u[:, None]*B
            fitted = fit_model(x, y, u, n)
            np.testing.assert_allclose(fitted['A'], A, atol=1e-12)
            np.testing.assert_allclose(fitted['B'], B, atol=1e-12)

    def test_free_prediction_matches_independent_matrix_power_convolution(self):
        rng = np.random.default_rng(18)
        for n in [2, 4]:
            A = np.eye(n)*.8 + rng.normal(0., .03, (n, n))
            B = rng.normal(0., .1, n); initial = rng.normal(0., 1., n)
            u = rng.normal(0., .2, 100)
            prediction = free_run(A, B, initial, u)
            for h in [1, 5, 25, 50, 100]:
                expected = np.linalg.matrix_power(A, h)@initial
                expected += sum(np.linalg.matrix_power(A, h-1-k)@B*u[k] for k in range(h))
                np.testing.assert_allclose(prediction[h], expected, atol=1e-12)

    def test_probes_bounded_and_phase_randomization_effective(self):
        families = ['train_sine', 'train_prbs', 'validation_sine', 'validation_prbs',
                    'pulse_pos', 'pulse_neg', 'step_pos', 'step_neg']
        for family in families:
            for amplitude in [.1, .25, .5]:
                u = waveform(family, amplitude, 72)
                self.assertEqual(u.shape, (100,))
                self.assertLessEqual(max(abs(u)), amplitude+1e-12)
                self.assertLessEqual(max(abs(np.diff(np.r_[0., u]))), .04+1e-12)
        for family in families[:4]:
            self.assertGreater(np.linalg.norm(waveform(family, .25, 72)-waveform(family, .25, 73)), .01)


if __name__ == '__main__':
    unittest.main(verbosity=2)
