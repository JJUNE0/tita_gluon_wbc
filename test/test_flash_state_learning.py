"""DESKTOP_DRY_RUN: augmented-state causality and recursive prediction checks."""

import unittest
import numpy as np

from analyze_flash_state_learning import fit, predict, MODELS
from eval_flash_state_learning import make_inputs, prefix_inputs


class StateLearningTests(unittest.TestCase):
    def test_augmented_matrices_and_action_input_causality(self):
        rng = np.random.default_rng(77)
        full_x = rng.normal(0., 1., (1200, 24))
        u = rng.normal(0., .1, 1200)
        for name, indices in MODELS.items():
            n = len(indices)
            A = np.eye(n)*.7+rng.normal(0., .03, (n, n))
            A[:, 0] = 0.; A[0, 0] = 1.
            B = rng.normal(0., .01, n)
            action_rows = [i for i, original in enumerate(indices) if 4 <= original < 12]
            B[action_rows] = 0.
            full_y = np.zeros_like(full_x)
            full_y[:, indices] = full_x[:, indices]@A.T+u[:, None]*B
            model = fit(full_x, full_y, u, name)
            np.testing.assert_allclose(model['A'], A, atol=1e-12)
            np.testing.assert_allclose(model['B'], B, atol=1e-12)
            np.testing.assert_array_equal(np.asarray(model['B'])[action_rows], np.zeros(len(action_rows)))

    def test_full_hidden_states_follow_independent_matrix_power_solution(self):
        rng = np.random.default_rng(78)
        for n in [2, 4, 12, 16, 24]:
            A = np.eye(n)*.8+rng.normal(0., .01, (n, n))
            B = rng.normal(0., .02, n)
            initial = rng.normal(0., .1, (3, n)); u = rng.normal(0., .02, (3, 100))
            output = predict(A, B, initial, u)
            self.assertEqual(output.shape, (3, 101, n))
            for h in [1, 5, 25, 50, 100]:
                expected = initial@np.linalg.matrix_power(A, h).T
                expected += sum(u[:, k, None]*(np.linalg.matrix_power(A, h-1-k)@B) for k in range(h))
                np.testing.assert_allclose(output[:, h], expected, atol=1e-12)

    def test_micro_probes_and_prefix_end_before_snapshots(self):
        for amplitude in [.01, .02, .04]:
            values = make_inputs('micro_prbs', amplitude, 79, 200)
            self.assertLessEqual(max(abs(values)), amplitude)
            self.assertLessEqual(max(abs(np.diff(np.r_[0., values]))), .04+1e-12)
            if amplitude == .02:
                self.assertGreater(np.mean(np.diff(values) != 0), .3)
        for seed in [100, 107, 110, 113]:
            values = prefix_inputs(dict(cohort='expanded', seed=seed, pitch_index=1), 650)
            self.assertGreater(max(abs(values)), .01)
            self.assertLessEqual(max(abs(values)), .2)
            np.testing.assert_array_equal(values[200:], np.zeros(450))


if __name__ == '__main__':
    unittest.main(verbosity=2)
