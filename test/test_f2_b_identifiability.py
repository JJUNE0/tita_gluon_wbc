"""DESKTOP_DRY_RUN: independent synthetic checks for the B attribution audit."""

import unittest
import numpy as np

from analyze_f2_b_identifiability import fwl


class IdentifiabilityChecks(unittest.TestCase):
    def setUp(self):
        # Orthogonal Walsh columns give analytical partial-regression answers.
        self.states = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
        self.innovation = np.ones(4) * .1
        self.u = self.states @ np.array([2., -3., 4.]) + self.innovation
        self.A = np.array([[.4, -.3], [2., .1], [-1., 4.]])
        self.B = np.array([.02, -.00015])

    def test_collinearity_alone_does_not_change_exact_B(self):
        target = self.states @ self.A + self.u[:, None] * self.B
        result, innovation = fwl(self.states, target, self.u)
        np.testing.assert_allclose(innovation, self.innovation, atol=1e-13)
        np.testing.assert_allclose(result['B'], self.B, atol=1e-13)
        self.assertAlmostEqual(result['innovation_energy_fraction'], .01 / 29.01)
        self.assertGreater(result['uncentered_input_vif'], 2000.)

    def test_unobserved_effect_correlated_with_input_innovation_biases_projection(self):
        # Known omitted contribution; its projection produces exactly this bias.
        omitted_coefficient = np.array([-.016, .000145])
        hidden = self.innovation[:, None] * omitted_coefficient
        target = self.states @ self.A + self.u[:, None] * self.B + hidden
        result, _ = fwl(self.states, target, self.u)
        np.testing.assert_allclose(result['B'], self.B + omitted_coefficient, atol=1e-13)
        self.assertLess(result['B'][0], self.B[0] / 4.)


if __name__ == '__main__':
    unittest.main(verbosity=2)
