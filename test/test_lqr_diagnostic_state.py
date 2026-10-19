"""DESKTOP_DRY_RUN: oracle frame, derivative and non-mutation checks."""

import json
from pathlib import Path
import sys
import unittest
import numpy as np

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'test'))
from debug_lqr_d4_diagnostics import Plant,policy_config,ARCHIVE,Description,read_yaml


class OracleTests(unittest.TestCase):
    def setUp(self):
        cfg=json.loads((ARCHIVE/'config.json').read_text())
        manifest=json.loads((ARCHIVE/'manifest.json').read_text())
        policy=policy_config()
        source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
        description=Description(source['scene']['robot']['spawn']['asset_path'])
        self.plant=Plant(policy,cfg,description,manifest['nominal_parameters'],{'name':'nominal'},42,0.)

    def tearDown(self):
        self.plant.env.close()

    def test_clone_does_not_change_runtime_state(self):
        env=self.plant.env
        fields=['qpos','qvel','qacc','qacc_warmstart','ctrl','sensordata']
        before={k:getattr(env.data,k).copy() for k in fields}
        self.plant.observe()
        for k in fields:
            np.testing.assert_array_equal(getattr(env.data,k),before[k])

    def test_pitch_rate_and_axle_velocity_match_finite_difference(self):
        env=self.plant.env
        env.data.qvel[:6]=[.1,-.2,.05,.2,.3,.4]
        env.data.qvel[env.qvel_addr]=np.arange(8)*.1
        data=self.plant.truth()
        _,vel,rpy,omega,_=self.plant.instant(data)
        gyro=data.sensor('trunk_gyro').data
        self.assertAlmostEqual(omega,gyro[1]*np.cos(rpy[0])-gyro[2]*np.sin(rpy[0]),places=10)
        outcomes=[]
        eps=1e-6
        for sign in (-1,1):
            clone=env.mujoco.MjData(env.model)
            env.mujoco.mj_copyData(clone,env.model,data)
            env.mujoco.mj_integratePos(env.model,clone.qpos,clone.qvel,sign*eps)
            env.mujoco.mj_forward(env.model,clone)
            pos,_,angles,_,_=self.plant.instant(clone)
            outcomes.append((pos,angles[1]))
        np.testing.assert_allclose((outcomes[1][0]-outcomes[0][0])/(2*eps),vel,atol=1e-8)
        self.assertAlmostEqual((outcomes[1][1]-outcomes[0][1])/(2*eps),omega,places=8)


if __name__=='__main__':
    unittest.main(verbosity=2)
