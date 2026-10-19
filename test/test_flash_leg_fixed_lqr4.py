"""DESKTOP_DRY_RUN: unchanged actor/history semantics and wheel-only replacement."""

import sys
from pathlib import Path
import unittest
import numpy as np

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'test'))
from eval_flash_leg_fixed_lqr4 import hybrid_torque,action_history_slice,policy_config,LEGS,WHEELS
from sim2sim.lqr.runtime import Playback
from sim2sim_ros2_jazzy.adapter import ObservationBuilder,ActionAdapter,ObsState,quat_wxyz_to_rotmat


class HybridTests(unittest.TestCase):
    def test_only_wheel_torque_changes(self):
        original=np.array([1,2,3,4,5,6,7,8],dtype=np.float32)
        mixed=hybrid_torque(original,6.,np.array([1.,-1.]))
        np.testing.assert_array_equal(mixed[LEGS],original[LEGS])
        np.testing.assert_array_equal(mixed[WHEELS],[3.,-3.])
        np.testing.assert_array_equal(original,[1,2,3,4,5,6,7,8])

    def test_full_actor_and_last_action_match_a_path(self):
        cfg=policy_config()
        playback=Playback(cfg)
        try:
            previous=np.array([.2,-.3,.4,5.,-.1,.6,-.5,-4.],dtype=np.float32)
            playback.last_action=previous.copy()
            env=playback.env
            quaternion=env.base_quat_sensor()
            original_state=ObsState(env.joint_pos(),env.joint_vel(),quaternion,env.base_ang_vel(),
                np.zeros(3,dtype=np.float32),previous,quat_wxyz_to_rotmat(quaternion).T @ env.base_lin_vel())
            expected=ObservationBuilder(cfg).build(original_state)
            obs,action=playback.infer()
            np.testing.assert_array_equal(obs,expected)
            history,scale,clip=action_history_slice(cfg)
            np.testing.assert_array_equal(obs[history],np.clip(previous,*clip)*scale)
            reference_action=playback.policy.run(['nn_output'],{'nn_input0':expected.reshape(1,-1)})[0].reshape(8)
            np.testing.assert_array_equal(action,reference_action)
            original=ActionAdapter(cfg).compute(action,env.joint_pos(),env.joint_vel())
            mixed=hybrid_torque(original,0.,np.ones(2))
            np.testing.assert_array_equal(mixed[LEGS],original[LEGS])
            playback.step(action,lambda q,dq,tau:hybrid_torque(tau,0.,np.ones(2)))
            np.testing.assert_array_equal(playback.last_action,action)
        finally:
            playback.env.close()


if __name__=='__main__':
    unittest.main(verbosity=2)
