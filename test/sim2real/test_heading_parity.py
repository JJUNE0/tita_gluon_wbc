"""DESKTOP_DRY_RUN: C++ ObservationBuilder == sim2sim Python ObservationBuilder on stateful sequences (heading error).

usage: python test/sim2real/test_heading_parity.py <policy_dir with config.json> [--write-fixture DIR]
       (--write-fixture saves the C++ stdin input and the Python expected output for an on-robot comparison)

The observation layout and heading/position parameters go through launch/tita.launch.py ``policy_parameters`` (the
robot path). Sequences switch between zero and non-zero commands (including values next to the zero-band
thresholds), vary gyro z and joints smoothly, and reset at random, with a non-zero gyro bias. No robot command.
"""

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import ObservationBuilder, ObsState  # noqa: E402

spec = importlib.util.spec_from_file_location(
    'tita_launch', REPO / 'sim2real/tita_ws/src/tita_controller/launch/tita.launch.py')
launch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launch)


def main() -> None:
    policy_dir = Path(sys.argv[1])
    cfg = json.loads((policy_dir / 'config.json').read_text())
    p = launch.policy_parameters(policy_dir)
    assert 'heading_clip_rad' in p and launch.OBS_KINDS.index('heading_error') in p['obs_kind'], 'no heading term'
    rng = np.random.default_rng(1)
    steps, bias = 4000, 0.0021
    default = np.asarray(cfg['robot']['default_joint_angles'])
    # command segments: zero, non-zero, and values just inside / outside the zero band
    edge = [[0.019, 0., 0.], [0.021, 0., 0.], [0., 0., 0.029], [0., 0., 0.031], [0., 0.019, 0.]]
    cmds, k = [], 0
    while k < steps:
        n = int(rng.integers(5, 150))
        r = rng.random()
        c = [0., 0., 0.] if r < .5 else edge[int(rng.integers(len(edge)))] if r < .65 else \
            [rng.uniform(-1, 1), 0., rng.uniform(-1.5, 1.5)]
        cmds += [c] * n
        k += n
    cmds = np.asarray(cmds[:steps])
    gz = np.cumsum(rng.normal(0, .02, steps)).clip(-1, 1)
    q = default + np.cumsum(rng.normal(0, .005, (steps, 8)), axis=0)
    q[:, [3, 7]] = np.cumsum(rng.normal(.05, .2, (steps, 2)), axis=0)        # wheels roll and wrap
    q[:, [3, 7]] = (q[:, [3, 7]] + np.pi) % (2 * np.pi) - np.pi
    dq = rng.normal(0, 1., (steps, 8))
    quat = np.c_[np.ones(steps), rng.normal(0, .02, (steps, 3))]
    quat /= np.linalg.norm(quat, axis=1, keepdims=True)
    gyro = np.c_[rng.normal(0, .2, (steps, 2)), gz]
    last = rng.normal(0, 1., (steps, 8))
    resets = rng.random(steps) < .004
    resets[0] = True

    builder = ObservationBuilder(cfg)
    builder.gyro_bias = bias
    py = []
    for i in range(steps):
        if resets[i]:
            builder.reset()
        py.append(builder.build(ObsState(q[i], dq[i], quat[i], gyro[i], cmds[i].astype(np.float32),
                                         last[i].astype(np.float32))))
    py = np.asarray(py, dtype=np.float64)

    lines = [str(len(p['obs_kind']))]
    lines += [f"{k} {i} {s!r} {lo!r} {hi!r}" for k, i, s, lo, hi in
              zip(p['obs_kind'], p['obs_index'], p['obs_scale'], p['obs_low'], p['obs_high'])]
    lines += [' '.join(repr(float(v)) for v in p['default_joint_angles']),
              ' '.join(repr(float(v)) for v in p['default_joint_velocities']),
              f"{p.get('wheel_position_radius', 0.)!r} {p.get('wheel_position_clip_m', 0.)!r} "
              + ' '.join(repr(float(v)) for v in p.get('wheel_position_zero_thresholds', [0., 0., 0.])),
              f"{p['heading_clip_rad']!r} {p['heading_warmup_s']!r} {p['policy_dt']!r} "
              + ' '.join(repr(float(v)) for v in p['heading_zero_thresholds']),
              repr(bias)]
    for i in range(steps):
        row = [int(resets[i]), *q[i], *dq[i], *quat[i], *gyro[i], *cmds[i], *last[i].astype(np.float32)]
        lines.append(' '.join(repr(float(v)) if not isinstance(v, (int, np.integer)) else str(v) for v in row))
    if '--write-fixture' in sys.argv:
        out_dir = Path(sys.argv[sys.argv.index('--write-fixture') + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / 'heading_parity_input.txt').write_text('\n'.join(lines) + '\n')
        np.savetxt(out_dir / 'heading_parity_expected.txt', py, fmt='%.9g')
    with tempfile.TemporaryDirectory(dir=REPO / 'test/sim2real', prefix='heading_parity_') as tmp:
        binary = Path(tmp) / 'heading_parity'
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-I',
                        str(REPO / 'sim2real/tita_ws/src/tita_controller/include'),
                        str(REPO / 'test/sim2real/checkpoint_heading_parity.cpp'), '-o', str(binary)], check=True)
        out = subprocess.run([str(binary)], input='\n'.join(lines) + '\n', check=True, capture_output=True,
                             text=True).stdout.splitlines()
    cpp = np.asarray([[float(v) for v in line.split()] for line in out])
    assert cpp.shape == py.shape, (cpp.shape, py.shape)
    err = np.abs(cpp - py)
    head = err[:, -1]
    active = np.count_nonzero(py[:, -1])
    clipped = np.count_nonzero(np.abs(py[:, -1]) >= 2 * p['heading_clip_rad'] - 1e-6)
    print(json.dumps(dict(policy=str(policy_dir), steps=steps, obs_dim=int(py.shape[1]), max_abs_error=float(err.max()),
                          heading_max_abs_error=float(head.max()), heading_nonzero_steps=int(active),
                          heading_clipped_steps=int(clipped), resets=int(resets.sum()),
                          warmup_s=p['heading_warmup_s'], gyro_bias=bias)))
    assert err.max() < 1e-5 and active > 100, 'parity failed'
    print('PASS')


if __name__ == '__main__':
    main()
