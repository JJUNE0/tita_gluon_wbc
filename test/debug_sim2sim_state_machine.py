"""VALIDATION_SIM: trace sim2sim state machine (splay -> sit -> rl) without ROS."""

import json
import sys
from pathlib import Path

import numpy as np
import onnxruntime as ort

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import ActionAdapter, ObservationBuilder, ObsState, quat_wxyz_to_rotmat, quat_wxyz_to_rpy
from sim2sim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from sim2sim_ros2_jazzy.state_machine import SPLAY_POSE, StateMachine

cfg = json.loads(Path(sys.argv[1]).read_text())
env = TitaMujocoEnv(cfg)
policy = ort.InferenceSession(cfg['policy']['path'], providers=['CPUExecutionProvider'])
obs_builder, adapter = ObservationBuilder(cfg), ActionAdapter(cfg)
sm = StateMachine(cfg['robot']['torque_limit'])
env.reset(SPLAY_POSE)
last_action = np.zeros(8, dtype=np.float32)


def report(tag):
    rpy = np.degrees(quat_wxyz_to_rpy(env.base_quat()))
    print(f'{tag:>14} t={step * env.control_dt:5.2f}s state={sm.state:12} height={env.base_pos()[2]:.3f} '
          f'roll={rpy[0]:+6.1f} pitch={rpy[1]:+6.1f} legs={np.round(env.joint_pos()[[0, 1, 2, 4, 5, 6]], 2)}')


schedule = {50: 'transform_up', 100: 'rl_early', 300: 'rl'}  # rl_early is before sit -> must be rejected
for step in range(851):
    if step in schedule:
        request = schedule[step].removesuffix('_early')
        print(f'request {schedule[step]} -> accepted={sm.request(request, env.joint_pos())}')
    sm.update(env.control_dt)
    if sm.state != 'rl':
        last_action[:] = 0
    q = env.base_quat_sensor()
    obs = obs_builder.build(ObsState(env.joint_pos(), env.joint_vel(), q, env.base_ang_vel(), np.zeros(3),
                                     last_action, quat_wxyz_to_rotmat(q).T @ env.base_lin_vel()))
    if sm.state == 'rl':
        action = policy.run(['nn_output'], {'nn_input0': obs.reshape(1, -1)})[0].reshape(8)
        env.step_with_torque_callback(lambda p, v: adapter.compute(action, p, v))
        last_action = action.copy()
    else:
        env.step_with_torque_callback(sm.torque)
    if step % 50 == 0:
        report('')
print('final policy-pose leg error max (rad):', float(np.max(np.abs(env.joint_pos() - adapter.targets(np.zeros(8)))[[0, 1, 2, 4, 5, 6]])))
