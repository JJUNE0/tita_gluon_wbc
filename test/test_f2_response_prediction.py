"""DESKTOP_DRY_RUN: verify prediction timing against a closed-form LTI response."""

from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_f2_residual_response import evaluate


class PredictionTimingTest(unittest.TestCase):
    def test_known_input_convolution_all_horizons(self):
        A = np.array([[1., .02, 0., 0.], [0., .8, .1, .02],
                      [0., 0., .95, .02], [0., -.1, .2, .6]])
        B = np.array([[.001], [.03], [-.002], [-.02]])
        inputs = np.random.default_rng(7).uniform(-.4, .4, 100)
        # Independent closed-form convolution; no step loop under test is used.
        states = np.zeros((101, 4))
        for t in range(1, 101):
            states[t] = sum((np.linalg.matrix_power(A, t - 1 - j) @ B[:, 0]) * inputs[j]
                            for j in range(t))
        results = evaluate(A, B, states, inputs)
        for key in ['one_step', 'full_from_start']:
            np.testing.assert_allclose(results[key]['rmse'], 0., atol=1e-13)
        for value in results['horizons'].values():
            np.testing.assert_allclose(value['rmse'], 0., atol=1e-13)
        self.assertGreater(results['omit_B']['rmse'][1], 1e-4)
        self.assertGreater(results['persistence']['rmse'][1], 1e-4)


if __name__ == '__main__':
    unittest.main(verbosity=2)
