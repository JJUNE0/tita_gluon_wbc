"""DESKTOP_DRY_RUN: independent checks of fitting and long-response metrics."""

import unittest

import numpy as np

from analyze_flash_operating_local import evaluate_extended, crossing_time, pulse_diagnostics
from analyze_flash_state_learning import fit
from eval_flash_operating_local import cases, COUNT
from eval_flash_stop_release import inputs_for


class OperatingLocalTests(unittest.TestCase):
    def test_known_models_and_causal_action_rows(self):
        rng = np.random.default_rng(7201)
        for name, n in [('M2', 12), ('M4', 24)]:
            A = rng.normal(0, .03, (n, n))
            A[:, 0] = 0
            A[0, 0] = 1
            B = rng.normal(0, .02, n)
            B[4:12] = 0
            x = rng.normal(size=(3000, 24))
            u = rng.normal(size=3000)
            y = np.zeros_like(x)
            y[:, :n] = x[:, :n] @ A.T + u[:, None] * B
            model = fit(x, y, u, name)
            np.testing.assert_allclose(model['A'], A, atol=2e-14)
            np.testing.assert_allclose(model['B'], B, atol=2e-14)

    def test_extended_prediction_against_matrix_power_convolution(self):
        n, count = 12, COUNT
        A = np.diag(np.linspace(.86, .97, n))
        A[0, 0] = 1
        A[0, 1] = .02
        A[1, 4] = .025
        A[4, 2] = -.04
        B = np.zeros(n)
        B[1:4] = [.022, -.00015, -.01]
        inputs = np.zeros((2, count))
        inputs[0, 5:25] = .02
        inputs[1, 9:39] = -.03
        initial = np.zeros((2, n))
        initial[:, 4] = [.002, -.001]
        powers = np.asarray([np.linalg.matrix_power(A, k) for k in range(count + 1)])
        expected = np.zeros((2, count + 1, n))
        for t in range(count + 1):
            expected[:, t] = initial @ powers[t].T
            if t:
                kernel = np.einsum('tij,j->ti', powers[:t][::-1], B)
                expected[:, t] += inputs[:, :t] @ kernel
        data = np.zeros((2, count + 1, 24))
        data[:, :, :n] = expected
        model = dict(A=A.tolist(), B=B.tolist(), indices=list(range(n)))
        metrics, predicted = evaluate_extended(model, data, inputs)
        np.testing.assert_allclose(predicted, expected, atol=1e-16)
        for key in ['full2s', 'full4s', 'full8s', 'tail4_8s']:
            self.assertLess(np.max(metrics[key]['rmse']), 1e-16)
        for metric in metrics['horizons'].values():
            self.assertLess(np.max(metric['rmse']), 1e-16)
        self.assertAlmostEqual(predicted[0, 6, 1] - (predicted[0, 5] @ A.T)[1], .02 * B[1])

    def test_inverse_response_reversal_and_decay(self):
        inputs = np.zeros(COUNT)
        inputs[5:25] = .02
        actual = np.zeros((COUNT + 1, 24))
        actual[6:16, 1] = .001
        actual[16:60, 1] = -.0004
        predicted = actual.copy()
        predicted[16:18, 1] = .0001
        self.assertAlmostEqual(crossing_time(actual[:, 1], inputs), .2)
        row = dict(family='pulse_pos', context='synthetic', amplitude=.02,
                   start_rl_s=908., z=actual, u=inputs)
        result = pulse_diagnostics([row], predicted[None])['summary']
        self.assertEqual(result['first_velocity_sign_matches'], 1)
        self.assertAlmostEqual(result['median_reversal_time_error_s'], .04)
        self.assertEqual(result['median_tail_velocity_rmse'], 0)
        self.assertAlmostEqual(crossing_time(-actual[:, 1], -inputs), .2)

    def test_probe_families_and_limits(self):
        self.assertEqual(len(cases('train')), 13)
        self.assertEqual(len(cases('test')), 17)
        self.assertFalse(any('bipulse' in f for f, _ in cases('train')))
        for family, amplitude in cases('train') + cases('test'):
            values = inputs_for(family, amplitude, 14231, COUNT)
            self.assertEqual(values.shape, (COUNT,))
            self.assertLessEqual(np.max(abs(values)), amplitude + 1e-12)
            self.assertLessEqual(np.max(abs(np.diff(np.r_[0., values]))), .04 + 1e-12)


if __name__ == '__main__':
    unittest.main(verbosity=2)
