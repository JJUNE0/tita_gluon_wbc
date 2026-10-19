"""DESKTOP_DRY_RUN: independent numerical and gate tests for joint adaptation."""
import unittest
import numpy as np

from m4_joint_adaptation import (offset,advance,reference_target,predicted_bias,JointEstimator,Command,
    MASKS,REF_LIMIT,BIAS,LOW,HIGH)
from eval_m4_joint_pipeline import compare,recovery_time,metrics


class JointTests(unittest.TestCase):
    def test_effective_offset_and_nonidentifiability(self):
        K=np.array([2.,3.,4.]);z=np.array([.1,.2,.3]);ref=np.array([0.,0.,.05]);b=.48
        self.assertAlmostEqual(b-K@(z-ref),-K@z+offset(K,b,ref))
        shifted=ref+np.array([0.,0.,.01]);shifted_bias=b-K@(shifted-ref)
        self.assertAlmostEqual(offset(K,b,ref),offset(K,shifted_bias,shifted))

    def test_reference_uses_observed_hidden_mean_and_never_changes_goal(self):
        original=np.zeros(24);original[12:18]=-.5
        x=np.tile(original,(1100,1));x[:,0]=np.linspace(0.,.2,1100);x[:,2]=.01
        ref,reason=reference_target(x,original,np.array([[-2.,2.]]*6))
        self.assertEqual(reason,'observed_mean');np.testing.assert_array_equal(ref[:2],[0.,0.])
        self.assertAlmostEqual(ref[2],.01)
        fast=x.copy();fast[:,1]=.01;self.assertIsNone(reference_target(fast,original,np.array([[-2.,2.]]*6))[0])
        distant=x.copy();distant[:,4]=REF_LIMIT[2]+.1
        self.assertIsNone(reference_target(distant,original,np.array([[-2.,2.]]*6))[0])

    def test_regression_coordinates_do_not_follow_control_reference(self):
        model=dict(A=[[1.,.02],[0.,.9]],B=[0.,.02],state_reference=[3.,-.7],c_center=[.001,.002])
        z=np.array([.1,.2]);expected=np.array(model['state_reference'])+np.array(model['A'])@(z-model['state_reference'])+model['c_center']
        np.testing.assert_allclose(advance(model,z,BIAS),expected)
        learner=JointEstimator((0,0,1));center=learner.rls.ref.copy();learner.reference[2]+=.01
        np.testing.assert_array_equal(learner.rls.ref,center)

    def test_model_based_bias_uses_finite_horizon_and_absolute_budget(self):
        A=np.eye(24)*.8;A[0,0]=1.;A[0,1]=.02;B=np.zeros(24);B[1]=-.02
        model=dict(A=A.tolist(),B=B.tolist(),state_reference=np.zeros(24).tolist(),c_center=np.zeros(24).tolist())
        z=np.zeros(24);z[0]=.01;K=np.zeros(24)
        value,record=predicted_bias(model,z,K,np.zeros(24),BIAS)
        self.assertGreater(value,BIAS);self.assertTrue(record['gate']);self.assertFalse(record['static_equilibrium_solve'])
        self.assertTrue(all(LOW<=x<=HIGH for x in record['candidates']))

    def test_shared_command_budget_and_distinct_factorial_masks(self):
        self.assertEqual(len(set(MASKS.values())),8)
        command=Command();z=np.zeros(24);z[0]=1.;K=np.ones(24)*-1.;ref=np.zeros(24);previous=BIAS
        for _ in range(200):
            u,record=command.compute(z,K,.52,ref)
            self.assertTrue(LOW<=u<=HIGH);self.assertLessEqual(abs(u-previous),.040000001);previous=u
        self.assertEqual(u,HIGH);self.assertTrue(record['global_clipped'])

    def test_missing_recovery_and_post_change_window(self):
        t=np.arange(1001)*.02;p=np.zeros(1001);v=np.zeros(1001)
        self.assertAlmostEqual(recovery_time(t,p,v,10.),0.)
        p[500:900]=.01
        self.assertIsNone(recovery_time(t,p,v,10.))
        p[500:600]=.01;p[600:]=0.
        self.assertAlmostEqual(recovery_time(t,p,v,10.),2.)

    def test_outside_24_state_support_stops_parameter_and_model_updates(self):
        learner=JointEstimator();before=np.asarray(learner.reference0).copy();after=before.copy();after[5]+=2.
        K,b,r=learner.values();learner.observe(before,BIAS,after)
        self.assertEqual(learner.rls.count,0);self.assertEqual(learner.paused,1)
        np.testing.assert_array_equal(K,learner.K);np.testing.assert_array_equal(r,learner.reference);self.assertEqual(b,learner.bias)

    def test_one_arm_failure_does_not_promote_or_block_other_arms(self):
        base=dict(complete=True,metrics=dict(pitch_RMS=.001,wheel_RMS=.1,base_IAE=1.,last5_base_RMSE=.1))
        good=dict(complete=True,metrics=dict(base['metrics'],base_IAE=.8,last5_base_RMSE=.08))
        self.assertTrue(compare([good]*6,[base]*6)['performance'])
        bad=dict(good,requires_model_validation=True,model_independent_gate=False)
        self.assertFalse(compare([bad]*6,[base]*6)['admissible'])
        self.assertTrue(compare([good]*6,[base]*6)['performance'])
        self.assertFalse(compare([dict(complete=False)],[base])['admissible'])

    def test_wheel_metric_selects_axes_after_temporal_mask(self):
        n=401;trace=dict(sensor=np.zeros((n,4)),sensor_error=np.zeros((n,4)),base_path=np.zeros(n),
            axle_path=np.zeros(n),base_velocity=np.zeros((n,1)),base_position=np.zeros((n,3)),goal_base_position=np.zeros(3),
            physical_motor=np.full((n-1,4,8),100.),rpy=np.zeros((n,3)),raw_correction=np.zeros(n-1),
            pre_global_clip=np.full(n-1,BIAS),actual_u=np.full(n-1,BIAS))
        trace['physical_motor'][:,:,[3,7]]=2.
        self.assertEqual(metrics(trace,8.,True,2.)['wheel_RMS'],2.)


if __name__=='__main__':unittest.main()
