"""DESKTOP_DRY_RUN / VALIDATION_SIM: static deployment invariant regressions."""
import copy
import json
import unittest
import tempfile
from pathlib import Path

import numpy as np

from static_target_domain import StaticEnv, StaticRunner, CKPT, prepared_config
from static_target_learner import StaticLearner, causal_validation
from m4_joint_adaptation import Command, LOW, HIGH
from run_static_target_adaptation import safe_domains, score, collect, validate
from m4_joint_adaptation import nominal


class StaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cfg=json.loads(prepared_config(CKPT).read_text())

    def test_target_installed_before_any_physics_and_static(self):
        e=StaticEnv(self.cfg,dict(mass=1.15,com=.005,friction=.2,gain=.8,lag=.02))
        self.assertEqual(e.data.time,0.);self.assertTrue(e.metadata['configured_before_first_step'])
        self.assertEqual(e.metadata['floor_friction'],.2);e.assert_static()
        e.step_with_torque_callback(lambda q,dq:np.zeros(8));e.assert_static();e.close()

    def test_motor_lag_applies_at_physics_dt_wheel_only(self):
        e=StaticEnv(self.cfg,dict(gain=.8,lag=.02));request=np.arange(8.)*.1
        e.step_with_torque_callback(lambda q,dq:request.copy())
        for i,value in enumerate(e.physical):
            np.testing.assert_allclose(value[[3,7]],request[[3,7]]*.8*(1.-np.exp(-(i+1)*.005/.02)),atol=1e-14)
            np.testing.assert_array_equal(value[[0,1,2,4,5,6]],request[[0,1,2,4,5,6]])
        e.close()

    def test_com_inertia_positive_and_center_shift(self):
        a=StaticEnv(self.cfg,{});b=StaticEnv(self.cfg,dict(com=-.005))
        base=a.model.body('base_link').id
        self.assertAlmostEqual(b.model.body_ipos[base,0]-a.model.body_ipos[base,0],-.005)
        np.testing.assert_array_equal(a.model.body_inertia,b.model.body_inertia)
        a.close();b.close()

    def test_changed_domain_is_detected(self):
        e=StaticEnv(self.cfg,{});e.model.body_mass[1]*=1.01
        with self.assertRaises(AssertionError):e.assert_static()
        e.close()

    def test_model_and_goal_centers_never_follow_internal_reference(self):
        learner=StaticLearner((1,1,1),np.array([[-3.,3.]]*6),False)
        center=learner.regression_center.copy();learner.reference[4]+=.01
        np.testing.assert_array_equal(learner.rls.ref,center)
        np.testing.assert_array_equal(learner.reference[:2],[0.,0.]);self.assertFalse(learner.permit_K)

    def test_shared_band_and_startup_slew(self):
        command=Command(previous=0.);before=0.
        for _ in range(100):
            u,_=command.compute(np.zeros(24),np.zeros(24),HIGH,np.zeros(24))
            self.assertLessEqual(abs(u-before),.040000001);self.assertLessEqual(u,HIGH+1e-12);before=u
        self.assertGreaterEqual(u,LOW)

    def test_bias_only_request_slew_is_independent_of_delivered_clipping(self):
        r=StaticRunner(self.cfg,dict(seed=599,pitch=0.),{})
        original=r.step
        def clipped(u):
            result=original(u);result['actual_u']=0.
            return result
        r.step=clipped
        trace,stats,_,_=collect(r,'Bias',599,.5)
        np.testing.assert_allclose(trace['raw_requested'][:12],np.arange(1,13)*.04,atol=1e-12)
        self.assertLessEqual(max(abs(np.diff(np.r_[0.,trace['raw_requested']]))),.040000001)
        self.assertAlmostEqual(trace['raw_requested'][-1],.4828)
        r.env.close()

    def test_scoring_keeps_initial_error_and_incomplete_failure(self):
        n=9001;t=np.arange(n)*.02
        trace=dict(sensor=np.zeros((n,4)),base_path=np.full(n,.02),base_velocity=np.zeros((n,1)),
            base_position=np.column_stack([np.zeros(n),np.zeros(n),np.ones(n)]),
            physical_motor=np.zeros((n-1,4,8)),rpy=np.zeros((n,3)),midpoint_path=np.zeros(n))
        s=score(trace,True,[])
        self.assertAlmostEqual(s['full']['IAE'],3.6);self.assertAlmostEqual(s['post_calibration']['IAE'],2.4)
        self.assertFalse(s['absolute_hold']);self.assertIsNone(s['recovery_s'])
        self.assertFalse(score(trace,False,['guard'])['absolute_hold'])

    def test_domain_failure_does_not_block_other_domain(self):
        def trial(name,complete):return dict(job=dict(domain=name),rows=[dict(arm='Fixed',complete=complete,last5=dict(speed_RMS=0.),terminal_error=0.)])
        good,verdict=safe_domains([trial('a',True)]*3+[trial('b',False)]*3)
        self.assertEqual(good,['a']);self.assertFalse(verdict['b']['safe'])

    def test_snapshot_restores_motor_memory_and_raw_policy_history(self):
        r=StaticRunner(self.cfg,dict(seed=599,pitch=0.),dict(lag=.02))
        snapshot=r.full_snapshot();one=r.step(.48);r.full_restore(snapshot);two=r.step(.48)
        for key in ['physical_motor','motor','action','history','policy_observation']:
            np.testing.assert_array_equal(one[key],two[key])
        r.env.assert_static();r.env.close()

    def test_offline_validation_bridges_to_interior_with_bounded_slew(self):
        r=StaticRunner(self.cfg,dict(seed=599,pitch=0.),{})
        for _ in range(100):r.step(.4828)
        r.step(HIGH)
        folder=Path(tempfile.mkdtemp(prefix='bridge_',dir='docs/exp/2026-10-16/static_target_adaptation/development'))
        validate(r,r.full_snapshot(),nominal(),folder,9,HIGH)
        bridge=json.loads((folder/'bridge.json').read_text())['steps']
        self.assertEqual(len(bridge),2)
        self.assertLessEqual(max(abs(np.diff(np.r_[HIGH,[x['requested']for x in bridge]]))),.040000001)
        self.assertAlmostEqual(bridge[-1]['requested'],.4828)
        r.env.assert_static();r.env.close()

    def test_free_prediction_uses_frozen_model_not_future_state_injection(self):
        rng=np.random.default_rng(82);A=rng.normal(0.,.03,(24,24))+np.eye(24)*.5
        A[:,0]=0.;A[0,0]=1.;A[0,1]=.02;B=rng.normal(0.,.01,24);B[4:12]=0.
        model=dict(A=A.tolist(),B=B.tolist(),state_reference=np.zeros(24).tolist(),state_std=np.ones(24).tolist(),c_center=np.zeros(24).tolist())
        u=.4828+rng.normal(0.,.01,200);x=[rng.normal(0.,.01,24)]
        for value in u:x.append(A@x[-1]+B*(value-.4828))
        correct=causal_validation(model,x,u)
        wrong=copy.deepcopy(model);wrong['B']=(-B).tolist();bad=causal_validation(wrong,x,u)
        self.assertLess(max(correct['horizons']['100']['RMSE']),1e-12)
        self.assertGreater(max(bad['horizons']['100']['RMSE']),1e-6)


if __name__=='__main__':unittest.main()
