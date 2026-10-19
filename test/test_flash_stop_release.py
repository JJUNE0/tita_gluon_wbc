"""DESKTOP_DRY_RUN: release probing and p/v response evaluation checks."""

import unittest
import numpy as np

from eval_flash_stop_release import inputs_for
from analyze_flash_stop_release import assess


class StopReleaseTests(unittest.TestCase):
    def test_held_out_bipulse_has_both_signs_and_returns_to_zero(self):
        for amplitude in [.1,.25]:
            positive=inputs_for('bipulse_pos',amplitude,1)
            negative=inputs_for('bipulse_neg',amplitude,1)
            np.testing.assert_array_equal(negative,-positive)
            self.assertEqual(len(positive),200)
            self.assertLessEqual(max(abs(positive)),amplitude)
            self.assertLessEqual(max(abs(np.diff(np.r_[0.,positive]))),.040000001)
            self.assertGreater(max(positive),0.)
            self.assertLess(min(positive),0.)
            np.testing.assert_array_equal(positive[100:],np.zeros(100))

    def test_known_dynamics_pass_and_wrong_input_direction_fails(self):
        A=np.eye(12)*.5
        A[:,0]=0.;A[0,0]=1.;A[0,1]=.02;A[1,1]=.9
        B=np.zeros(12);B[:2]=[.0002,.02]
        model=dict(name='M2',indices=list(range(12)),A=A.tolist(),B=B.tolist())
        rows=[]
        for family in ['bipulse_pos','bipulse_neg']:
            u=inputs_for(family,.25,2)
            z=np.zeros((201,24))
            for k,value in enumerate(u):
                z[k+1,0]=z[k,0]+.02*z[k,1]+.0002*value
                z[k+1,1]=.9*z[k,1]+.02*value
            rows.append(dict(z=z,u=u,gt=z[:,:4].copy(),family=family))
        direct=[dict(sensor_B=B.tolist())]
        result=assess(model,rows,direct)
        self.assertTrue(result['diagnostic_gate'])
        np.testing.assert_allclose(result['full2s']['nrmse'],[0.,0.],atol=1e-10)
        self.assertEqual(result['initial_velocity_direction_matches'],2)
        wrong=dict(model,B=(-B).tolist())
        result=assess(wrong,rows,direct)
        self.assertFalse(result['diagnostic_gate'])
        self.assertEqual(result['initial_velocity_direction_matches'],0)


if __name__=='__main__':
    unittest.main(verbosity=2)
