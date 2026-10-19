"""DESKTOP_DRY_RUN: independent affine arithmetic and absolute-error checks."""

import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
from scipy.linalg import solve_discrete_are

from analyze_flash_stop_local import fit_local, predict
from analyze_flash_operating_affine import evaluate_affine
from eval_flash_fixed_residual_lqr import design, lqr_gain, limited


class AffineTests(unittest.TestCase):
    def test_scaled_lqr_matches_independent_physical_DARE(self):
        A = np.array([[1.,.02],[0.,.95]])
        B = np.array([.0002,.02])
        Q = np.diag([250000.,250000.])
        R = 400.
        K,diagnostics = lqr_gain(A,B,[.0003,.001],Q,R)
        P = solve_discrete_are(A,B[:,None],Q,np.array([[R]]))
        expected = np.linalg.solve(np.array([[R]])+B[None]@P@B[:,None],B[None]@P@A)[0]
        np.testing.assert_allclose(K,expected,rtol=1e-10,atol=1e-10)
        self.assertLess(diagnostics['closed_model_spectral_radius'],1.)

    def test_correction_bounds_and_failed_affine_gate(self):
        previous = 0.
        for i in range(200):
            value = limited(100. if i<100 else -100.,previous,i*.02)
            self.assertLessEqual(abs(value),.05+1e-12)
            self.assertLessEqual(abs(value-previous),.04+1e-12)
            previous = value
        self.assertEqual(limited(100.,0.,0.),0.)
        self.assertAlmostEqual(limited(100.,0.,.75),.025)
        with TemporaryDirectory(dir=Path(__file__).parent) as temp:
            root = Path(temp)
            (root/'calibrated').mkdir()
            (root/'calibrated/fresh_confirmation.json').write_text(json.dumps({'gate':False}))
            with self.assertRaises(AssertionError):design(root)
            self.assertFalse((root/'fixed_gain_frozen.json').exists())

    def test_affine_coefficients_with_nonzero_internal_reference(self):
        rng = np.random.default_rng(21931)
        n = 24
        A = np.eye(n)*.9 + rng.normal(0,.01,(n,n))
        A[:,0] = 0
        A[0,0] = 1
        B = rng.normal(0,.01,n)
        B[4:12] = 0
        ref = np.linspace(-1.8, .9, n)
        ref[0] = 0
        c = ref-A@ref-B*.4828 + rng.normal(0,1e-6,n)
        rows = []
        for _ in range(1200):
            x = ref+rng.normal(0,.002,n)
            u = .4828+rng.normal(0,.02)
            y = A@x+B*u+c
            rows.append(dict(mode='frozen',absolute=np.stack([x,y]),u=np.array([u])))
        fitted = fit_local(rows,'M4',affine=True)
        zref = np.asarray(fitted['state_reference'])
        physical_c = zref-np.asarray(fitted['A'])@zref-np.asarray(fitted['B'])*fitted['input_reference']+fitted['c_center']
        np.testing.assert_allclose(fitted['A'],A,atol=2e-12)
        np.testing.assert_allclose(fitted['B'],B,atol=2e-12)
        np.testing.assert_allclose(physical_c,c,atol=2e-12)

    def test_affine_free_prediction_against_augmented_matrix_powers(self):
        n,N = 24,400
        A = np.diag(np.linspace(.85,.96,n))
        A[:,0] = 0
        A[0,0] = 1
        A[0,1] = .02
        A[1,4] = .03
        B = np.zeros(n)
        B[1] = .022
        ref = np.linspace(-1.,1.,n)
        ref[0] = 100.
        c = ref-A@ref-B*.4828
        model = dict(A=A.tolist(),B=B.tolist(),state_reference=ref.tolist(),
                     input_reference=.4828,c_center=np.zeros(n).tolist(),indices=list(range(n)))
        M = np.eye(n+1)
        M[:n,:n] = A
        M[:n,n] = c
        G = np.r_[B,0.]
        powers = np.asarray([np.linalg.matrix_power(M,k) for k in range(N+1)])
        u = np.full((1,N),.4828)
        u[0,5:25] += .02
        expected = []
        for t in range(N+1):
            z = powers[t]@np.r_[ref,1.]
            if t:z += u[0,:t]@np.einsum('tij,j->ti',powers[:t][::-1],G)
            expected.append(z[:n])
        expected = np.asarray(expected)
        got = predict(model,ref[None],u)[0]
        np.testing.assert_allclose(got,expected,atol=1e-11)
        row = dict(absolute=expected,delta=expected-ref,u=u[0])
        metrics,_ = evaluate_affine(model,[row])
        self.assertLess(np.max(metrics['full8s']['rmse']),1e-11)
        bad = dict(model,c_center=np.r_[1e-5,np.zeros(23)].tolist())
        bad_metrics,_ = evaluate_affine(bad,[row])
        self.assertGreater(bad_metrics['full8s']['rmse'][0,0],.002)
        self.assertGreater(bad_metrics['full8s']['nrmse'][0,0],.3)


if __name__=='__main__':
    unittest.main(verbosity=2)
