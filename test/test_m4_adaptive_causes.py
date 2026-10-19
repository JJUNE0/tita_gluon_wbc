"""DESKTOP_DRY_RUN: affine forcing, gain timing and independent response scores."""
import unittest
import numpy as np

from diagnose_m4_adaptive_causes import defect,steady_error,applied_gains,limit_sequence,validate_models,BIAS


class Diagnostics(unittest.TestCase):
    def test_affine_forcing_and_reference_coordinates(self):
        A=np.array([[1.,.02],[0.,.9]]);B=np.array([0.,.02]);reference=np.array([3.,-.7])
        target=np.array([.2,0.]);wanted=np.array([0.,.001])
        c=wanted-(A-np.eye(2))@(target-reference)
        model=dict(A=A.tolist(),B=B.tolist(),state_reference=reference.tolist(),c_center=c.tolist())
        np.testing.assert_allclose(defect(model,target),wanted,atol=1e-15)
        for K in [np.array([2.,1.]),np.array([4.,1.])]:
            solution=steady_error(model,K,target);e=np.zeros(2)
            for _ in range(5000):e=(A-np.outer(B,K))@e+wanted
            np.testing.assert_allclose(solution['error'],e,atol=1e-12)
            self.assertAlmostEqual(solution['input'],BIAS-.05,places=12)
        self.assertAlmostEqual(steady_error(model,[2.,1.],target)['error'][0],.025,places=12)
        self.assertAlmostEqual(steady_error(model,[4.,1.],target)['error'][0],.0125,places=12)

    def test_after_step_gain_is_shifted_and_saturation_can_hide_gain_change(self):
        after=np.array([[1.,2.],[3.,4.],[5.,6.]])
        np.testing.assert_array_equal(applied_gains(after,[0.,0.]),[[0.,0.],[1.,2.],[3.,4.]])
        np.testing.assert_array_equal(limit_sequence(np.full(150,.2)),limit_sequence(np.full(150,.35)))
        self.assertEqual(limit_sequence(np.full(150,.2))[-1],.05)

    def test_known_full_state_free_response_and_wrong_input_effect(self):
        A=np.eye(24)*.8;A[0,0]=1.;A[0,1]=.02
        B=np.zeros(24);B[:2]=[.0003,.02]
        rng=np.random.default_rng(189);u=rng.choice([-.01,.01],size=(8,200))
        values=np.zeros((8,201,24))
        for t in range(200):values[:,t+1]=values[:,t]@A.T+u[:,t,None]*B
        good=dict(A=A.tolist(),B=B.tolist());bad=dict(good,B=(-B).tolist())
        result=validate_models({'known':good,'wrong':bad},values,u,B)
        self.assertTrue(result['known']['gate']);self.assertFalse(result['wrong']['gate'])


if __name__=='__main__':unittest.main()
