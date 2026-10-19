"""DESKTOP_DRY_RUN / VALIDATION_SIM: physical metric gates and wheel motor path."""

import copy
import json
import unittest

import numpy as np

from flash_overnight_control_stages import summarize_control,EffectRunner
from flash_overnight_model_stages import Runner,prepared_config,CKPT


def synthetic_rows():
    rows=[]
    for family in ['zero','position','kick']:
        for group in ['bias_only','M4','M5']:
            good=group!='bias_only'
            rows.append(dict(context='independent',start_hold_s=1000.,group=group,family=family,amplitude=0.,
                complete=True,pitch_RMS=.001,wheel_torque_RMS=.1,last5_base_speed_mean=0.,
                base=dict(IAE=.0001 if good else .001,last5_RMSE=.00001 if good else .0001),
                wheel_midpoint=dict(IAE=9. if good else 0.,last5_RMSE=9. if good else 0.)))
    return rows


class ControlChecks(unittest.TestCase):
    def test_only_predeclared_base_point_determines_gate(self):
        result=summarize_control(synthetic_rows())
        self.assertTrue(result['gate'])
        rows=synthetic_rows()
        for r in rows:
            if r['group']=='M5' and r['family']=='position':r['base']['IAE']=.002
        self.assertFalse(summarize_control(rows)['models']['M5']['gate'])

    def test_incomplete_episode_is_not_a_small_drift_success(self):
        rows=synthetic_rows()
        for r in rows:
            if r['group']=='M5' and r['family']=='kick':
                r['complete']=False;r['base']['last5_RMSE']=None;r['base']['IAE']=0.
        result=summarize_control(rows)
        self.assertFalse(result['gate'])
        self.assertIn('incomplete',result['models']['M5']['families']['kick']['reason'])

    def test_nominal_motor_wrapper_is_identity_with_raw_history_preserved(self):
        cfg=json.loads(prepared_config(CKPT).read_text())
        job=dict(seed=299,pitch=0.,pitch_index=1)
        a=Runner(cfg,job);b=EffectRunner(cfg,job)
        try:
            snapshot=a.snapshot();b.restore(snapshot);b.enable_effect(dict(gain=1.,lag=0.))
            for u in [.1,.2,0.,-.1]:
                left=a.step(u);right=b.step(u)
                for k in left:np.testing.assert_array_equal(left[k],right[k])
                np.testing.assert_array_equal(right['physical_motor'],right['motor'])
                np.testing.assert_array_equal(a.env.data.qpos,b.env.data.qpos)
                np.testing.assert_array_equal(a.playback.last_action,b.playback.last_action)
        finally:a.env.close();b.env.close()

    def test_lag_is_applied_at_physics_dt_only_to_wheels(self):
        cfg=json.loads(prepared_config(CKPT).read_text());r=EffectRunner(cfg,dict(seed=299,pitch=0.,pitch_index=1))
        try:
            r.enable_effect(dict(gain=.8,lag=.02));previous=r.motor_state.copy()
            trace=r.step(.1);dt=r.env.model.opt.timestep
            expected=[]
            for command in trace['motor']:
                previous=previous+(1.-np.exp(-dt/.02))*(.8*command[[3,7]]-previous)
                result=command.copy();result[[3,7]]=np.clip(previous,-12.,12.);expected.append(result)
            np.testing.assert_allclose(trace['physical_motor'],expected,atol=1e-7,rtol=1e-7)
            np.testing.assert_array_equal(trace['physical_motor'][:,[0,1,2,4,5,6]],trace['motor'][:,[0,1,2,4,5,6]])
        finally:r.env.close()


if __name__=='__main__':unittest.main(verbosity=2)
