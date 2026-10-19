"""DESKTOP_DRY_RUN: numerical equivalence, causality and sensor prediction tests."""
import unittest
import numpy as np

from online_local_m4 import (features,objective,theta_difference,ConstrainedRLS,LocalRLS,
    nominal,BIAS,training_allowed,validate_candidate)


class LocalIdentificationTests(unittest.TestCase):
    def test_weighted_prior_batch_and_recursive_are_same_objective(self):
        rng=np.random.default_rng(992);prior=nominal();ref=np.asarray(prior['state_reference']);scale=ConstrainedRLS(prior).scale
        z=ref+rng.normal(size=(301,24))*scale;u=BIAS+rng.normal(0.,.02,300);streams=[(z,u,np.ones(300,dtype=bool))]
        X,Y=features(streams)
        for lam,P in [(.9995,100.),(1.,100.),(1.,1e8)]:
            exact,_=objective(X,Y,lam,P);raw=ConstrainedRLS(prior,forgetting=lam,prior_covariance=P)
            for i in range(300):raw.update(z[i],u[i],z[i+1])
            self.assertLess(theta_difference(raw,exact),1e-5)

    def test_local_downdate_matches_exact_recent_time_window(self):
        rng=np.random.default_rng(545);prior=nominal();ref=np.asarray(prior['state_reference']);scale=ConstrainedRLS(prior).scale
        z=ref+rng.normal(size=(101,24))*scale;u=BIAS+rng.normal(0.,.02,100)
        setting=dict(window=1.,forgetting=1.,P=100.);local=LocalRLS(setting)
        for i in range(100):local.observe((i+1)*.02,z[i],u[i],z[i+1])
        frozen=local.freeze(2.);self.assertEqual(frozen['information']['samples'],50)
        self.assertGreater(frozen['first_training_time'],1.);self.assertLess(frozen['recursion_vs_exact'],1e-7)
        local.expire(4.);self.assertEqual(len(local.buffer),0)

    def test_validation_windows_never_become_training_later(self):
        self.assertTrue(training_allowed(9.98));self.assertFalse(training_allowed(10.))
        self.assertFalse(training_allowed(13.98));self.assertTrue(training_allowed(14.))
        local=LocalRLS(dict(window=20.,forgetting=1.,P=100.));ref=np.asarray(nominal()['state_reference'])
        for i in range(1700):
            t=i*.02;local.observe(t+.02,ref,BIAS,ref,training_allowed(t))
        self.assertTrue(all(not (10.<t<=14.)and not(30.<t<=34.)for t,_,_ in local.buffer))

    def test_conditional_B_and_free_prediction_reject_wrong_dynamics(self):
        # Controlled full-state excitation, including the eight causal action rows.
        rng=np.random.default_rng(492);prior=nominal();ref=np.asarray(prior['state_reference']);A=np.eye(24)*.7;A[:,0]=0.;A[0,0]=1.;A[0,1]=.02
        B=np.zeros(24);B[1]=.02;c=np.zeros(24);model=dict(prior,A=A.tolist(),B=B.tolist(),c_center=c.tolist())
        u=BIAS+rng.normal(0.,.01,200);x=np.empty((201,24));x[0]=ref
        for i in range(200):x[i+1]=ref+A@(x[i]-ref)+B*(u[i]-BIAS)
        bad=dict(model,c_center=(np.eye(24)[0]*.001).tolist())
        score=validate_candidate(bad,x,u);self.assertFalse(score['prediction_gate'])
        # No excitation in hidden states means the complete model gate must fail.
        self.assertFalse(validate_candidate(model,x,u)['conditional_B']['gate'])

    def test_position_symmetry_and_action_causality_survive_refinement(self):
        local=LocalRLS(dict(window=None,forgetting=1.,P=100.));rng=np.random.default_rng(982);ref=np.asarray(nominal()['state_reference'])
        for i in range(30):local.observe((i+1)*.02,ref+rng.normal(0.,.01,24),BIAS+.01,ref+rng.normal(0.,.01,24))
        m=local.freeze(.6)['model'];expected=np.zeros(24);expected[0]=1.
        np.testing.assert_array_equal(np.asarray(m['A'])[:,0],expected);np.testing.assert_array_equal(np.asarray(m['B'])[4:12],np.zeros(8))


if __name__=='__main__':unittest.main()
