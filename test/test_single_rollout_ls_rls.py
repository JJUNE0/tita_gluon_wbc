"""DESKTOP_DRY_RUN: meaningful sample alignment and known-system checks."""
import unittest
import numpy as np

from compare_single_rollout_ls_rls import (select_indices, fit_batch, features,
    objective, model_difference, nominal, BIAS, ConstrainedRLS, training_allowed)
from m4_joint_adaptation import advance


class SameTransitionTests(unittest.TestCase):
    def test_exact_window_and_validation_exclusion(self):
        end=(np.arange(3000)+1)*.02
        mask=np.array([training_allowed(t-.02) for t in end])
        candidate=dict(created=60.,training_times=end[mask & (end>40.+1e-9)].tolist())
        selected=select_indices(candidate,mask,dict(window=20.))
        self.assertTrue(all(t>40. for t in end[selected]))
        bad=dict(candidate,training_times=candidate['training_times']+[60.02])
        with self.assertRaises(AssertionError):select_indices(bad,mask,dict(window=20.))

    def test_validation_sample_cannot_be_reintroduced(self):
        end=(np.arange(1500)+1)*.02;mask=np.array([training_allowed(t-.02) for t in end])
        candidate=dict(created=30.,training_times=end[mask].tolist())
        select_indices(candidate,mask,dict(window=None))
        candidate['training_times']=sorted(candidate['training_times']+[10.02])
        with self.assertRaises(AssertionError):select_indices(candidate,mask,dict(window=None))

    def test_plain_LS_recovers_excited_affine_system_and_causality(self):
        rng=np.random.default_rng(84931);prior=nominal();ref=np.asarray(prior['state_reference']);scale=ConstrainedRLS(prior).scale
        A=np.eye(24)*.5;A[:,0]=0.;A[0,0]=1.;A[0,1]=.02
        B=np.zeros(24);B[1]=.03;c=np.zeros(24);c[1]=.0002
        # Disjoint transitions in one stream mask: each predecessor independently
        # excites the regressors; every selected successor follows the known model.
        z=ref+rng.normal(size=(1601,24))*scale;u=BIAS+rng.normal(0.,.02,1600)
        model=dict(prior,A=A.tolist(),B=B.tolist(),c_center=c.tolist())
        mask=np.zeros(1600,dtype=bool);mask[::2]=True
        for i in np.flatnonzero(mask):z[i+1]=advance(model,z[i],u[i])
        fitted,_=fit_batch([(z,u,mask)])
        self.assertLess(model_difference(fitted,model),1e-7)
        np.testing.assert_array_equal(np.asarray(fitted['B'])[4:12],np.zeros(8))
        shifted=z.copy();shifted[:,0]+=.8
        other,_=fit_batch([(shifted,u,mask)])
        self.assertLess(model_difference(fitted,other),1e-7)

    def test_same_cost_batch_uses_only_selected_rows(self):
        rng=np.random.default_rng(459);prior=nominal();ref=np.asarray(prior['state_reference']);scale=ConstrainedRLS(prior).scale
        z=ref+rng.normal(size=(401,24))*scale;u=BIAS+rng.normal(0.,.02,400)
        mask=np.zeros(400,dtype=bool);mask[:100]=True
        X,Y=features([(z,u,mask)]);first,_=objective(X,Y,1.,1e8)
        z[200:]=1e9;u[200:]=-1e9
        X,Y=features([(z,u,mask)]);second,_=objective(X,Y,1.,1e8)
        self.assertEqual(model_difference(first.model(),second.model()),0.)


if __name__=='__main__':unittest.main()
