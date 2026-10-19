"""DESKTOP_DRY_RUN: sim2real C++ adapter/state machine == sim2sim Python on the same inputs.

usage: python test/sim2real/test_sim2real_parity.py <policy_dir with config.json>
"""

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import ActionAdapter, ObservationBuilder, ObsState  # noqa: E402
from sim2sim_ros2_jazzy.state_machine import StateMachine  # noqa: E402

spec = importlib.util.spec_from_file_location(
    'tita_launch', REPO / 'sim2real/tita_ws/src/tita_controller/launch/tita.launch.py')
launch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launch)

policy_dir = Path(sys.argv[1])
cfg = __import__('json').loads((policy_dir / 'config.json').read_text())
params = launch.policy_parameters(policy_dir)
rng = np.random.default_rng(0)
N, STEPS, DT = 50, 6000, 0.002

q = np.asarray(cfg['robot']['default_joint_angles']) + rng.normal(0, .3, (N, 8))
dq = rng.normal(0, 2., (N, 8))
quat = rng.normal(0, 1., (N, 4))
quat /= np.linalg.norm(quat, axis=1, keepdims=True)
gyro, cmd = rng.normal(0, 1., (N, 3)), rng.normal(0, .5, (N, 3))
last, action = rng.normal(0, 1., (N, 8)), rng.normal(0, 2., (N, 8))
sm_start = q[0]
sm_q = np.asarray(cfg['robot']['default_joint_angles']) + rng.normal(0, .5, (STEPS, 8))
sm_dq = rng.normal(0, 2., (STEPS, 8))

fixture = {**params, 'q': q, 'dq': dq, 'quat': quat, 'gyro': gyro, 'cmd': cmd, 'last': last, 'action': action,
           'sm_start': sm_start, 'sm_q': sm_q, 'sm_dq': sm_dq, 'sm_dt': [DT]}
with tempfile.TemporaryDirectory(dir=REPO / 'test/sim2real', prefix='parity_') as tmp:
    path = Path(tmp) / 'fixture.txt'
    path.write_text(''.join(f'{k} ' + ' '.join(repr(float(v)) for v in np.ravel(np.asarray(val, dtype=float))) + '\n'
                            for k, val in fixture.items() if not isinstance(val, str)))
    binary = Path(tmp) / 'parity'
    subprocess.run(['g++', '-std=c++17', '-O2', '-I', str(REPO / 'sim2real/tita_ws/src/tita_controller/include'),
                    str(REPO / 'test/sim2real/parity.cpp'), '-o', str(binary)], check=True)
    lines = subprocess.run([str(binary), str(path)], check=True, capture_output=True, text=True).stdout.splitlines()
cpp = {}
for line in lines:
    key, *values = line.split()
    cpp.setdefault(key, []).append([float(v) for v in values])

obs_builder, adapter = ObservationBuilder(cfg), ActionAdapter(cfg)
obs_err = max(np.max(np.abs(obs_builder.build(ObsState(q[n], dq[n], quat[n], gyro[n], cmd[n], last[n]))
                            - cpp['obs'][n])) for n in range(N))
torque_err = max(np.max(np.abs(adapter.compute(action[n], q[n], dq[n]) - cpp['torque'][n])) for n in range(N))

sm = StateMachine(cfg['robot']['torque_limit'])
sm.request('transform_up', sm_start)
sm_err, state_mismatch = 0., 0
for n in range(STEPS):
    sm.update(DT)
    sm_err = max(sm_err, np.max(np.abs(sm.torque(sm_q[n], sm_dq[n]) - cpp['sm_torque'][n])))
    state_mismatch += (sm.state == 'sit') != bool(cpp['sm_state'][n][0])
print(f'obs max err {obs_err:.2e} ({N} samples, {len(cpp["obs"][0])} dims)')
print(f'rl torque max err {torque_err:.2e}')
print(f'state machine torque max err {sm_err:.2e}, state mismatches {state_mismatch}/{STEPS}, final {sm.state}')
ok = obs_err < 1e-5 and torque_err < 1e-4 and sm_err < 1e-3 and state_mismatch <= 1 and sm.state == 'sit'
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
