"""DESKTOP_DRY_RUN: independent checks for centered affine local identification."""

import unittest
import numpy as np

from analyze_flash_stop_local import fit_local, predict, evaluate


class StopLocalTests(unittest.TestCase):
    def test_affine_recovery_and_feedback_position_dependence(self):
        rng = np.random.default_rng(900)
        for mode in ['frozen', 'feedback']:
            for name, n in [('M2', 12), ('M4', 24)]:
                A = .5*np.eye(n)+rng.normal(0., .025, (n, n))
                if mode == 'frozen':
                    A[:, 0] = 0.; A[0, 0] = 1.
                B = rng.normal(0., .01, n); B[4:12] = 0.
                offset = rng.normal(0., .002, n)
                rows = []
                for i in range(24):
                    u = rng.normal(.5, .2, 120)
                    x = [rng.normal(0., .1, n)]
                    for value in u:
                        x.append(A@x[-1]+B*value+offset)
                    full = np.zeros((121, 24)); full[:, :n] = x
                    rows.append(dict(mode=mode, absolute=full, u=u))
                model = fit_local(rows, name, affine=True)
                np.testing.assert_allclose(model['A'], A, atol=1e-10)
                np.testing.assert_allclose(model['B'], B, atol=1e-10)
                ref = np.asarray(model['state_reference'])
                np.testing.assert_allclose(model['c_center'], A@ref+B*model['input_reference']+offset-ref, atol=1e-11)
                output = predict(model, rows[0]['absolute'][None, 0, :n], rows[0]['u'][None])
                np.testing.assert_allclose(output[0], rows[0]['absolute'][:, :n], atol=1e-10)
                self.assertEqual(model['position_translation_symmetry'], mode=='frozen')

    def test_affine_prediction_matches_independent_matrix_power_convolution(self):
        rng = np.random.default_rng(901)
        n = 12
        A = np.eye(n)*.8+rng.normal(0., .01, (n, n))
        B, c = rng.normal(0., .1, (2, n))
        ref = rng.normal(0., .1, n); uref = .5
        initial = rng.normal(0., .1, (3, n)); u = rng.normal(.5, .1, (3, 100))
        model = dict(A=A, B=B, c_center=c, state_reference=ref, input_reference=uref)
        output = predict(model, initial, u)
        for h in [1, 5, 25, 50, 100]:
            expected = (initial-ref)@np.linalg.matrix_power(A, h).T+ref
            expected += sum((u[:, k, None]-uref)*(np.linalg.matrix_power(A, h-1-k)@B)
                +np.linalg.matrix_power(A, h-1-k)@c for k in range(h))
            np.testing.assert_allclose(output[:, h], expected, atol=1e-11)

    def test_affine_metric_does_not_hide_error_behind_absolute_position(self):
        n = 12
        model = dict(A=np.eye(n), B=np.zeros(n), c_center=np.zeros(n),
            state_reference=np.zeros(n), input_reference=0., indices=list(range(n)), kind='affine')
        base = np.zeros((201, 24)); base[:, 0] = 100.
        current = base.copy(); current[:, 0] += np.arange(201)*.00001
        rows = [dict(absolute=current, base=base, delta=current-base, u=np.zeros(200), du=np.zeros(200))]
        result, _ = evaluate(model, rows)
        np.testing.assert_allclose(result['full2s']['nrmse'][0], 1., atol=1e-10)


if __name__ == '__main__':
    unittest.main(verbosity=2)
