"""DESKTOP_DRY_RUN: one reset per stop command, hysteresis and bounded release."""

from pathlib import Path
import sys
import unittest
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from play_flash_velocity_hold import StopHold,Description,policy_config,read_yaml,ARCHIVE,Sensors
import json


class HoldGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        policy=policy_config()
        source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
        cls.description=Description(source['scene']['robot']['spawn']['asset_path'])
        cls.parameters=json.loads((ARCHIVE/'manifest.json').read_text())['nominal_parameters']
        cls.q=np.asarray(policy['robot']['default_joint_angles'])

    def packet(self,displacement=0.,speed=0.):
        q=self.q.copy();dq=np.zeros(8)
        q[[3,7]]+=displacement/self.description.radius
        dq[[3,7]]=speed/self.description.radius
        return Sensors(q,dq,np.array([1.,0.,0.,0.]),np.zeros(3))

    def test_reset_once_and_actual_motion_does_not_disable_hold(self):
        hold=StopHold(self.description,self.parameters['equilibrium_pitch'])
        hold.step([.2,0.,0.],self.packet(1.),.02)
        _,d=hold.step([0.,0.,0.],self.packet(1.),.02)
        self.assertEqual(d['event'],'hold_enter');self.assertEqual(d['relative_p'],0.)
        _,d=hold.step([0.,0.,0.],self.packet(1.1,.2),.02)
        self.assertTrue(hold.holding);self.assertGreater(abs(d['relative_p']),.05)
        self.assertEqual(hold.entries,1)
        hold.step([.2,0.,0.],self.packet(2.),.02)
        _,d=hold.step([0.,0.,0.],self.packet(2.),.02)
        self.assertEqual(hold.entries,2);self.assertEqual(d['relative_p'],0.)

    def test_yaw_command_and_hysteresis_release_without_torque_jump(self):
        hold=StopHold(self.description,self.parameters['equilibrium_pitch'])
        previous=0.
        for tick in range(100):
            u,_=hold.step([0.,0.,0.],self.packet(tick*.005,.1),.02)
            self.assertLessEqual(abs(u-previous),.04+1e-12);self.assertLessEqual(abs(u),1.)
            previous=u
        u,_=hold.step([.03,0.,0.],self.packet(.5),.02)
        self.assertLessEqual(abs(u-previous),.04+1e-12);previous=u
        self.assertTrue(hold.holding)
        for tick in range(30):
            u,d=hold.step([0.,0.,.3],self.packet(10.),.02)
            self.assertFalse(hold.holding)
            self.assertLessEqual(abs(u-previous),.04+1e-12)
            previous=u
        self.assertEqual(u,0.);self.assertEqual(d['mode'],'MOVE')
        self.assertEqual(hold.entries,1)


if __name__=='__main__':unittest.main(verbosity=2)
