"""DESKTOP_DRY_RUN: compare operator-labelled hand-blocked and free-drift bags.

Only deserialize recorded frames and execute the existing pure-math C++ fixture.
Operator excludes the first few seconds from hand blocking. Primary comparisons
omit the first 5 s; 3/7 s exclusions are sensitivity checks, not contact detection.
"""
import argparse
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import tempfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from rclpy.serialization import deserialize_message
from tita_controller.msg import TrainingSample

from analyze_free_drift_baseline import PACKAGE, REPO, digest, stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bag', type=Path)
    parser.add_argument('--free-signals', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.bag, args.free_signals, args.output = [p.resolve() for p in (args.bag, args.free_signals, args.output)]
    args.output.mkdir(parents=True, exist_ok=True)
    db = next(args.bag.glob('*.db3'))
    before = digest(db)
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as conn:
        assert conn.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        topic = conn.execute("SELECT id FROM topics WHERE name='/sim2real/training_sample'").fetchone()
        assert topic
        frames = [deserialize_message(r[0], TrainingSample) for r in conn.execute(
            'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', topic)]
        counts = dict(conn.execute('SELECT topics.name,count(*) FROM messages JOIN topics ON messages.topic_id=topics.id GROUP BY topics.id'))
    field = lambda key: np.array([getattr(f, key) for f in frames])
    mono = field('monotonic_ns').astype(np.int64)
    sequence = field('sequence_id').astype(np.int64)
    assert np.all(np.diff(mono) > 0) and np.all(np.diff(sequence) > 0)
    rl = field('state') == 'rl'
    assert np.count_nonzero(rl & ~np.r_[False, rl[:-1]]) == 1
    t = (mono-mono[rl][0])*1e-9
    dt = np.r_[.02, np.diff(mono)*1e-9]
    q, dq, quat, gyro, command, action, teacher, torque, offsets, diag = [field(k) for k in (
        'joint_position', 'joint_velocity', 'quaternion_wxyz', 'angular_velocity', 'command',
        'action_raw', 'teacher_action', 'computed_torque', 'wheel_velocity_bias', 'velocity_bias_diagnostics')]
    rows = np.c_[rl, dt, command, q, dq, quat, gyro, action]
    assert np.isfinite(rows).all() and np.isfinite(torque).all()
    assert abs(offsets[rl]).max() == 0. and abs(teacher[rl]-action[rl]).max() < 1e-6
    cfg_path = PACKAGE/'policies/flashsac_60000/config.json'
    geometry_path = PACKAGE/'config/velocity_bias_geometry.json'
    cfg, geo = [json.loads(p.read_text()) for p in (cfg_path, geometry_path)]
    native = [f'joint_{side}_leg_{i}' for side in ('left', 'right') for i in range(1, 5)]
    terms = []
    for a in cfg['policy_interface']['actions']:
        terms.extend([native.index(a['joint']), int(a['kind'] == 'velocity'), a['scale'], a['offset'], *(a['clip'] or [-1e9, 1e9])])
    header = [*geo['xyz'], *geo['rpy'], *geo['axis'], geo['wheel_radius'], 1.,
              *cfg['robot']['joint_kp'], *cfg['robot']['joint_kd'], *cfg['robot']['torque_limit'], *terms]
    stream = io.StringIO()
    np.savetxt(stream, np.array(header)[None], fmt='%.17g')
    np.savetxt(stream, rows, fmt='%.17g')
    with tempfile.TemporaryDirectory(dir=REPO/'test/sim2real', prefix='hand_drift_') as temp:
        binary = Path(temp)/'runtime'
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
            '-I/usr/include/eigen3', '-I', str(PACKAGE/'include'),
            str(REPO/'test/sim2real/velocity_bias_runtime.cpp'), '-o', str(binary)], check=True)
        run = subprocess.run([str(binary), 'on'], input=stream.getvalue(), text=True, capture_output=True, check=True)
    shadow = np.loadtxt(io.StringIO(run.stdout), ndmin=2)
    assert shadow.shape == (len(frames), 25)
    error = float(abs(shadow[rl, 17:25]-torque[rl]).max())
    assert error < 1e-4
    w, x, y, z = quat.T
    pitch = np.degrees(np.arcsin(np.clip(2*(w*y-z*x), -1, 1)))
    velocity = shadow[:, 3]
    wheel_proxy = geo['wheel_radius']*dq[:, [3, 7]].mean(axis=1)
    target = np.zeros_like(dq)
    for a, term in enumerate(cfg['policy_interface']['actions']):
        j = native.index(term['joint'])
        target[:, j] = action[:, a]*term['scale']+term['offset']
        if term['clip']:
            target[:, j] = np.clip(target[:, j], *term['clip'])
    target_proxy = geo['wheel_radius']*target[:, [3, 7]].mean(axis=1)
    neutral = rl & (abs(command) <= [.02, .02, .03]).all(axis=1)
    windows = []
    for lo, hi in [(5, 10), (10, 15), (15, 20), (5, 20), (3, 20), (7, 20)]:
        mask = neutral & (t >= lo) & (t < hi)
        if mask.sum() < 2:
            continue
        windows.append(dict(start_s=lo, end_s=hi, samples=int(mask.sum()),
            **{key: stats(value[mask]) for key, value in dict(fk_velocity_m_s=velocity,
                wheel_proxy_m_s=wheel_proxy, pitch_deg=pitch, gyro_y_rad_s=gyro[:, 1],
                policy_wheel_target_proxy_m_s=target_proxy, wheel_torque_nm=torque[:, [3, 7]].mean(axis=1)).items()}))
    flags = {k: int(np.count_nonzero(~field(k)[rl])) for k in (
        'sensors_valid', 'policy_valid', 'output_enabled', 'torque_sent', 'teacher_action_valid')}
    transitions = np.flatnonzero(np.r_[True, field('state')[1:] != field('state')[:-1]])
    result = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='SUSPICIOUS',
        operator_annotation='Operator clarifies hand blocking started after the first few seconds; exact onset, force and ground velocity are unmeasured.',
        primary_analysis_window_s=[5., 20.], exclusion_sensitivity_s=[3., 5., 7.],
        run=args.bag.name.removesuffix('_bag'), checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
        onnx_sha256=cfg['policy_interface']['onnx_sha256'], frames=len(frames), topic_counts=counts,
        rl_samples=int(rl.sum()), rl_last_sample_s=float(t[rl][-1]), command_abs_max=abs(command[rl]).max(axis=0).tolist(),
        neutral_rl_samples=int(neutral.sum()), bias_offset_abs_max=float(abs(offsets[rl]).max()),
        logged_diag_abs_max=float(abs(diag[rl]).max()), rl_false_flags=flags,
        missing_sequences=int(np.maximum(np.diff(sequence)-1, 0).sum()), rl_dt_s=stats(dt[rl]),
        rl_dt_over_30ms=int((dt[rl] > .03).sum()), baseline_torque_error_nm=error,
        state_transitions=[dict(state=frames[i].state, time_from_rl_s=float(t[i])) for i in transitions],
        windows=windows, source_sha256={str(p.relative_to(REPO)): digest(p) for p in (db, cfg_path, geometry_path,
            args.free_signals, PACKAGE/'include/tita_controller/velocity_bias.hpp', REPO/'test/sim2real/velocity_bias_runtime.cpp', Path(__file__))},
        limitations=['External hand force changes the plant; this is not autonomous stop performance.',
            'Wheel/FK speed is not independently measured chassis ground speed; contact, slip and sensor-frame errors remain unresolved.',
            'Shadow outputs follow recorded states only; no corrected hardware trajectory is inferred.',
            'Computed torque and transport flags are not measured torque or motor acknowledgement.'])
    assert not any(flags.values()) and digest(db) == before
    np.savez_compressed(args.output/'signals.npz', t=t, rl=rl, neutral=neutral, command=command,
        q=q, dq=dq, quat=quat, gyro=gyro, action=action, teacher=teacher, torque=torque,
        pitch=pitch, velocity=velocity, wheel_proxy=wheel_proxy, target_proxy=target_proxy, shadow=shadow)
    (args.output/'metrics.json').write_text(json.dumps(result, indent=2)+'\n')
    free = np.load(args.free_signals)
    fig, ax = plt.subplots(4, 1, figsize=(13, 11), sharex=True, constrained_layout=True)
    for axis, key, held, label in zip(ax, ['velocity', 'pitch', 'torque', 'dq'],
            [velocity, pitch, torque[:, [3, 7]].mean(axis=1), wheel_proxy],
            ['FK/IMU speed (m/s)', 'Pitch (deg)', 'Mean computed wheel torque (Nm)', 'Wheel rolling proxy (m/s)']):
        source = free[key]
        if key == 'torque':
            source = source[:, [3, 7]].mean(axis=1)
        elif key == 'dq':
            source = source[:, [3, 7]].mean(axis=1)*geo['wheel_radius']
        axis.plot(free['t'][free['rl']], source[free['rl']], label='Free drift (previous run)', alpha=.8)
        axis.plot(t[rl], held[rl], label='Hand-blocked run (initial seconds excluded)', alpha=.8)
        axis.axvspan(0, 5, color='gray', alpha=.15, label='Excluded: first 5 s')
        axis.axvline(5, color='gray', ls=':')
        axis.set_ylabel(label)
        axis.grid(alpha=.2)
        axis.legend(fontsize=8)
    ax[-1].set_xlabel('Seconds from each RL entry')
    fig.suptitle('FlashSAC bias OFF: free drift vs operator-labelled hand-blocked run\nNo measured hand force or chassis ground-truth velocity')
    fig.savefig(args.output/'hand_vs_free.png', dpi=150)
    plt.close(fig)
    print(json.dumps({k: v for k, v in result.items() if k not in ('source_sha256', 'topic_counts')}, indent=2))


if __name__ == '__main__':
    main()
