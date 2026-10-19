"""DESKTOP_DRY_RUN: known affine plant, causal constraints, and free prediction."""
import unittest
import numpy as np

from m4_shadow_stages import ConstrainedRLS


class Identification(unittest.TestCase):
    def test_unknown_affine_plant_and_full_recursive_prediction(self):
        rng=np.random.default_rng(3819);n=24
        A=np.eye(n)*.7;A[0,0]=1.;A[0,1]=.02;A[1:,0]=0.
        A[1:,1:]+=rng.normal(0,.01,(23,23))
        B=rng.normal(0,.03,n);B[4:12]=0.
        c=rng.normal(0,.002,n);ref=rng.normal(0,.05,n)
        prior=dict(A=(A+np.diag(np.r_[0.,np.full(23,.02)])).tolist(),B=(B*.7).tolist(),
            c_center=np.zeros(n).tolist(),state_reference=ref.tolist(),state_std=np.full(n,.1).tolist())
        rls=ConstrainedRLS(prior,forgetting=1.)
        # Independent initial perturbations supply information on all model states.
        for _ in range(6000):
            x=rng.normal(0,.1,n);u=rng.normal(0,.05)
            y=A@x+B*u+c
            rls.update(x+ref,u+.4828,y+ref)
        model=rls.model()
        np.testing.assert_array_equal(np.asarray(model['A'])[:,0],np.r_[1.,np.zeros(23)])
        np.testing.assert_array_equal(np.asarray(model['B'])[4:12],np.zeros(8))
        np.testing.assert_allclose(model['A'],A,atol=1e-6)
        np.testing.assert_allclose(model['B'],B,atol=2e-6)
        x=rng.normal(0,.1,n);pred=x.copy()
        for u in rng.normal(0,.05,400):
            x=A@x+B*u+c
            pred=np.asarray(model['A'])@pred+np.asarray(model['B'])*u+model['c_center']
        np.testing.assert_allclose(pred[:2],x[:2],atol=1e-5)
        self.assertTrue(rls.diagnostics()['gate'])

    def test_no_excitation_rejects_gain_eligibility_and_partial_keeps_A(self):
        model=dict(A=np.eye(24).tolist(),B=np.r_[0,.02,np.zeros(22)].tolist(),
            c_center=np.zeros(24).tolist(),state_reference=np.zeros(24).tolist(),state_std=np.ones(24).tolist())
        for partial in [False,True]:
            rls=ConstrainedRLS(model,partial=partial)
            for _ in range(300):rls.update(np.zeros(24),.4828,np.zeros(24))
            self.assertFalse(rls.diagnostics()['gate'])
            if partial:np.testing.assert_array_equal(rls.model()['A'],model['A'])


if __name__=='__main__':unittest.main()
