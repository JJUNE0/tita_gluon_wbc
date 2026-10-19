"""DESKTOP_DRY_RUN: distinguish sustainable stop from zero-average drift."""

import unittest
import numpy as np

from eval_flash_constant_hold import metrics


def trace_with_velocity(velocity):
    count=len(velocity)
    t=np.arange(count)*.02
    position=np.r_[0.,np.cumsum(velocity[:-1])*.02]
    sensor=np.column_stack([position,velocity,np.full(count,.06),np.zeros(count)])
    q=np.zeros((count,6));q[:,1]=.001*np.sin(2*np.pi*t)
    action=np.zeros((count,8));action[:,0]=.1*np.sin(2*np.pi*t)
    return dict(sensor=sensor,gt=sensor.copy(),position=np.column_stack([position,np.zeros((count,2))]),
        rpy=np.column_stack([np.zeros(count),np.full(count,.06),np.zeros(count)]),
        leg_position=q,leg_velocity=np.zeros_like(q),previous_action=action,
        motor=np.zeros((count-1,4,8)))


class ConstantHoldTests(unittest.TestCase):
    def test_bounded_periodic_operation_need_not_have_constant_hidden_states(self):
        t=np.arange(9001)*.02
        trace=trace_with_velocity(.0001*np.sin(2*np.pi*t))
        result=metrics(trace,np.tile([-1.,1.],(6,1)),True,180.)
        self.assertTrue(result['operating_gate'])
        self.assertGreater(result['action_std_last60'][0],.01)
        self.assertGreater(result['leg_position_std_last60'][1],.0001)

    def test_zero_final_mean_does_not_hide_prior_drift(self):
        t=np.arange(9001)*.02
        velocity=np.where(t<120.,-.002,0.)
        result=metrics(trace_with_velocity(velocity),np.tile([-1.,1.],(6,1)),True,180.)
        self.assertAlmostEqual(result['gt_v_mean_last60'],0.)
        self.assertFalse(result['operating_gate'])
        self.assertFalse(result['checks']['block_speed'])
        self.assertFalse(result['checks']['sagittal_span'])

    def test_lateral_motion_and_physical_failure_are_not_stop_success(self):
        trace=trace_with_velocity(np.zeros(9001))
        trace['position'][:,1]=np.arange(9001)*.02*.001
        result=metrics(trace,np.tile([-1.,1.],(6,1)),True,180.)
        self.assertFalse(result['operating_gate'])
        self.assertFalse(result['checks']['planar_radius'])
        trace['position'][:,1]=0.
        self.assertFalse(metrics(trace,np.tile([-1.,1.],(6,1)),False,180.)['operating_gate'])

    def test_terminal_window_preserves_original_failure_and_state_transition_alignment(self):
        t=np.arange(45001)*.02
        trace=trace_with_velocity(np.where(t<600.,.002,.0001*np.sin(2*np.pi*t)))
        limits=np.tile([-1.,1.],(6,1))
        self.assertFalse(metrics(trace,limits,True,900.)['operating_gate'])
        terminal={key:value[30000:] for key,value in trace.items()}
        self.assertEqual(len(terminal['motor'])+1,len(terminal['sensor']))
        self.assertTrue(metrics(terminal,limits,True,300.)['operating_gate'])


if __name__=='__main__':
    unittest.main(verbosity=2)
