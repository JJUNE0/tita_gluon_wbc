"""DESKTOP_DRY_RUN: posture transitions ignore unbounded wheel encoder angles."""

from pathlib import Path
import sys
import unittest

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.state_machine import SPLAY_POSE, SIT_POSE, StateMachine


class WalkStateMachineTest(unittest.TestCase):
    def test_policy_entry_preserves_prepared_target(self):
        sm = StateMachine([60., 60., 60., 12.] * 2)
        sm.request('transform_up', SPLAY_POSE)
        for _ in range(120):
            sm.update(.02)
        self.assertEqual(sm.state, 'sit')
        np.testing.assert_allclose(sm.target, SIT_POSE, atol=1e-6)
        before = sm.target.copy()
        self.assertTrue(sm.request('rl', SIT_POSE))
        np.testing.assert_array_equal(sm.target, before)

    def test_damp_has_only_bounded_velocity_damping_and_rejects_direct_rl(self):
        sm = StateMachine([60., 60., 60., 12.] * 2, auto_rl=True)
        sm.request('damp', SPLAY_POSE)
        velocity = np.array([100., -100., 0., 100., 0., 0., 0., -100.])
        np.testing.assert_allclose(sm.torque(SPLAY_POSE, velocity), [-60., 60., 0., -12., 0., 0., 0., 12.])
        self.assertFalse(sm.request('rl', SPLAY_POSE))
        sm.update(100.)
        self.assertEqual(sm.state, 'damp')

    def test_wheel_encoder_turns_do_not_delay_manual_or_automatic_posture_setup(self):
        for automatic in (False, True):
            with self.subTest(automatic=automatic):
                normal = StateMachine([60., 60., 60., 12.] * 2, auto_rl=automatic)
                rolled = StateMachine([60., 60., 60., 12.] * 2, auto_rl=automatic)
                start = SPLAY_POSE.copy()
                start[[3, 7]] = [200., -500.]
                self.assertFalse(normal.request('rl', SPLAY_POSE))
                normal.request('transform_up', SPLAY_POSE)
                rolled.request('transform_up', start)
                for _ in range(120):
                    normal.update(.02)
                    rolled.update(.02)
                    self.assertEqual(normal.state, rolled.state)
                    velocity = np.array([0., 0., 0., 2., 0., 0., 0., -2.])
                    np.testing.assert_allclose(normal.torque(SPLAY_POSE, velocity), rolled.torque(start, velocity))
                self.assertEqual(rolled.state, 'rl' if automatic else 'sit')


if __name__ == '__main__':
    unittest.main(verbosity=2)
