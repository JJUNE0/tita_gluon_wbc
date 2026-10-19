"""DESKTOP_DRY_RUN: join motor feedback, replay policy/PD, export retraining evidence.

Uses recorded states only. No ROS node, SDK instance or hardware command.
"""
import argparse
import csv
import hashlib
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
import onnxruntime as ort
from rclpy.serialization import deserialize_message
from scipy.spatial.transform import Rotation
from tita_controller.msg import MotorFeedback, TrainingSample

from diagnose_three_case_wheel_bias import targets, torques, blocks

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'sim2real/tita_ws/src/tita_controller'
LEGS = [0, 1, 2, 4, 5, 6]
NAMES = [f'{side}_leg_{j}' for side in ('left', 'right') for j in range(1, 5)]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary(values):
    v = np.asarray(values)
    v = v[np.isfinite(v)]
    return None if not len(v) else dict(mean=float(v.mean()), std=float(v.std()),
        min=float(v.min()), max=float(v.max()), rms=float(np.sqrt(np.mean(v*v))))


def comparison(x, y):
    if not len(x):
        return dict(samples=0)
    error = y-x
    energy = float(x@x)
    return dict(samples=len(x), command_mean_nm=float(x.mean()), reported_mean_nm=float(y.mean()),
        command_rms_nm=float(np.sqrt(np.mean(x*x))), command_std_nm=float(x.std()),
        reported_std_nm=float(y.std()), gain_origin=float(x@y/energy) if energy else None,
        error_mean_nm=float(error.mean()), error_rms_nm=float(np.sqrt(np.mean(error*error))),
        error_abs_p95_nm=float(np.quantile(abs(error), .95)),
        model_06_error_rms_nm=float(np.sqrt(np.mean((y-.6*x)**2))))


def fk_velocity(q, dq, quat, gyro, dt, rl, geometry):
    origins = Rotation.from_euler('xyz', np.array(geometry['rpy']).reshape(8, 3)).as_matrix()
    xyz = np.array(geometry['xyz']).reshape(8, 3)
    axes = np.array(geometry['axis']).reshape(8, 3)
    result = np.full(len(q), np.nan)
    previous = None
    for i in range(len(q)):
        if not rl[i] or not 0 < dt[i] <= .06:
            previous = None
            continue
        rot = Rotation.from_quat(quat[i, [1, 2, 3, 0]]).as_matrix()
        yaw = np.arctan2(rot[1, 0], rot[0, 0])
        lateral, forward = np.array([-np.sin(yaw), np.cos(yaw), 0]), np.array([np.cos(yaw), np.sin(yaw), 0])
        rate, offset = 2*lateral@(rot@gyro[i]), np.zeros(3)
        for side in range(2):
            rotation, position = rot.copy(), np.zeros(3)
            for j in range(4*side, 4*side+4):
                position += rotation@xyz[j]
                rotation = rotation@origins[j]
                rate += lateral@(rotation@axes[j])*dq[i, j]
                rotation = rotation@Rotation.from_rotvec(axes[j]*q[i, j]).as_matrix()
            offset += position/2
        result[i] = geometry['wheel_radius']*rate/2
        if previous is not None:
            result[i] -= (offset-previous)@forward/dt[i]
        previous = offset
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bag', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--contact', choices=['none', 'unknown', 'intermittent'], default='unknown')
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(ROOT / 'docs/exp')
    out.mkdir(parents=True, exist_ok=True)
    db = next(args.bag.resolve().glob('*.db3'))
    db_hash = digest(db)
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as conn:
        assert conn.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        ids = dict(conn.execute('SELECT name,id FROM topics'))
        topic_counts = dict(conn.execute('SELECT topics.name,count(*) FROM messages JOIN topics '
            'ON messages.topic_id=topics.id GROUP BY topics.id'))
        samples = [deserialize_message(b, TrainingSample) for b, in conn.execute(
            'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', (ids['/sim2real/training_sample'],))]
        feedback_list = [deserialize_message(b, MotorFeedback) for b, in conn.execute(
            'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', (ids['/sim2real/motor_feedback'],))]
    feedback = {f.sequence_id: f for f in feedback_list}
    assert len(feedback) == len(feedback_list)
    get = lambda name: np.array([getattr(s, name) for s in samples])
    sequence = get('sequence_id').astype(np.uint64)
    mono = get('monotonic_ns').astype(np.int64)
    ticks = get('control_tick').astype(np.uint64)
    state = get('state')
    rl = state == 'rl'
    assert np.count_nonzero(rl & ~np.r_[False, rl[:-1]]) == 1
    assert np.all(np.diff(mono) > 0) and np.all(np.diff(sequence.astype(np.int64)) == 1)
    t = (mono-mono[rl][0])*1e-9
    dt = np.r_[.02, np.diff(mono)*1e-9]
    q, dq, quat, gyro, command, action, torque, offsets = [get(name) for name in (
        'joint_position', 'joint_velocity', 'quaternion_wxyz', 'angular_velocity', 'command',
        'action_raw', 'computed_torque', 'wheel_velocity_bias')]
    assert np.isfinite(np.c_[q, dq, quat, gyro, command, action, torque, offsets]).all()
    assert np.max(abs(offsets[rl])) == 0
    flags = {name: get(name) for name in ('sensors_valid', 'policy_valid', 'output_enabled', 'torque_sent', 'teacher_action_valid')}
    assert all(flags[name][rl].all() for name in ('sensors_valid', 'policy_valid', 'output_enabled', 'torque_sent'))
    teacher = get('teacher_action')
    assert np.max(abs(teacher[rl]-action[rl])) < 1e-6
    ros_ns = np.array([s.header.stamp.sec*10**9+s.header.stamp.nanosec for s in samples], dtype=np.int64)
    obs = np.full((len(samples), 33), np.nan, dtype=np.float32)
    obs[rl] = np.array([s.observation for s in samples if s.state == 'rl'], dtype=np.float32)
    reported, preceding = np.full_like(torque, np.nan), np.full_like(torque, np.nan)
    feedback_valid, previous_sent = np.zeros(len(t), bool), np.zeros(len(t), bool)
    read_ns, command_ns = np.zeros(len(t), np.uint64), np.zeros(len(t), np.uint64)
    for i, sample in enumerate(samples):
        if sample.sequence_id not in feedback:
            continue
        f = feedback[sample.sequence_id]
        assert f.header == sample.header and f.monotonic_ns == sample.monotonic_ns and f.control_tick == sample.control_tick
        reported[i], preceding[i] = f.reported_torque, f.previous_computed_torque
        feedback_valid[i], previous_sent[i] = f.valid, f.previous_torque_sent
        read_ns[i], command_ns[i] = f.feedback_read_monotonic_ns, f.previous_command_monotonic_ns
        if f.valid:
            assert np.isfinite(f.reported_torque).all()
    joined = feedback_valid & previous_sent & np.isfinite(preceding).all(axis=1)
    assert np.all(command_ns[joined].astype(np.int64) < mono[joined])
    assert np.all(read_ns[joined].astype(np.int64) >= mono[joined])
    post = rl & (t >= 3) & joined
    neutral = rl & np.all(abs(command) <= [.02, .02, .03], axis=1)
    neutral_age = np.zeros(len(t))
    for i in range(1, len(t)):
        if neutral[i] and neutral[i-1]:
            neutral_age[i] = neutral_age[i-1]+dt[i]
    settled = post & neutral & (neutral_age >= 1.)
    bundle = PACKAGE / 'policies/flashsac_60000'
    cfg_path, geo_path = bundle / 'config.json', PACKAGE / 'config/velocity_bias_geometry.json'
    cfg, geo = json.loads(cfg_path.read_text()), json.loads(geo_path.read_text())
    assert digest(bundle / 'policy.onnx') == cfg['policy_interface']['onnx_sha256']
    opts = ort.SessionOptions()
    opts.intra_op_num_threads = opts.inter_op_num_threads = 1
    session = ort.InferenceSession(str(bundle / 'policy.onnx'), sess_options=opts)
    predictions = np.array([session.run(None, {session.get_inputs()[0].name: row[None]})[0][0] for row in obs[rl]])
    actor_error = float(abs(predictions-action[rl]).max())
    rebuilt = torques(targets(action[rl], cfg), dict(q=q[rl], dq=dq[rl]), cfg)
    torque_error = float(abs(rebuilt-torque[rl]).max())
    assert actor_error < 2e-5 and torque_error < 1e-4
    observer_dt = dt.copy()
    observer_dt[np.flatnonzero(rl)[0]] = .02
    velocity = fk_velocity(q, dq, quat, gyro, observer_dt, rl, geo)
    # Cross-check FK with existing pure C++ math on the recorded states. Zero
    # shadow commands keep the observer active; no resulting correction is applied.
    native = ['joint_'+name for name in NAMES]
    terms = []
    for term in cfg['policy_interface']['actions']:
        terms.extend([native.index(term['joint']), int(term['kind'] == 'velocity'),
            term['scale'], term['offset'], *(term['clip'] or [-1e9, 1e9])])
    header = [*geo['xyz'], *geo['rpy'], *geo['axis'], geo['wheel_radius'], 1.,
        *cfg['robot']['joint_kp'], *cfg['robot']['joint_kd'], *cfg['robot']['torque_limit'], *terms]
    with tempfile.TemporaryDirectory(dir=ROOT / 'test/sim2real', prefix='motor_feedback_math_') as tmp:
        binary = Path(tmp) / 'runtime'
        subprocess.run(['g++', '-std=c++17', '-O2', '-I/usr/include/eigen3', '-I', str(PACKAGE / 'include'),
            str(ROOT / 'test/sim2real/velocity_bias_runtime.cpp'), '-o', str(binary)], check=True)
        stream = io.StringIO()
        np.savetxt(stream, np.array(header)[None], fmt='%.17g')
        np.savetxt(stream, np.c_[rl, observer_dt, np.zeros_like(command), q, dq, quat, gyro, action], fmt='%.17g')
        result = subprocess.run([str(binary), 'on'], input=stream.getvalue(), text=True, capture_output=True, check=True)
        shadow = np.loadtxt(io.StringIO(result.stdout), ndmin=2)
    observer_error = float(abs(shadow[rl, 3]-velocity[rl]).max())
    assert observer_error < 1e-5
    w, x, y, z = quat.T
    pitch = np.degrees(np.arcsin(np.clip(2*(w*y-z*x), -1, 1)))
    tilt = np.degrees(np.arccos(np.clip(1-2*(x*x+y*y), -1, 1)))
    wheel_proxy = geo['wheel_radius']*dq[:, [3, 7]].mean(axis=1)
    windows = {}
    def window(mask):
        return dict(samples=int(mask.sum()), start_s=float(t[mask][0]) if mask.any() else None,
            end_s=float(t[mask][-1]) if mask.any() else None,
            command_mean=command[mask].mean(axis=0).tolist() if mask.any() else [],
            velocity_fk_m_s=summary(velocity[mask]), wheel_proxy_m_s=summary(wheel_proxy[mask]),
            pitch_deg=summary(pitch[mask]), tilt_deg=summary(tilt[mask]),
            q_mean=q[mask].mean(axis=0).tolist() if mask.any() else [],
            command_torque_mean_nm=torque[mask].mean(axis=0).tolist() if mask.any() else [],
            reported_torque_mean_nm=reported[mask].mean(axis=0).tolist() if mask.any() else [])
    for name, mask in dict(rl_all=rl, rl_after3s=post, neutral_after3s_settled1s=settled,
            translation_command=post & (abs(command[:, 0]) > .02) & (abs(command[:, 2]) <= .03),
            rotation_command=post & (abs(command[:, 2]) > .03), initial_0to1=rl & (t < 1),
            initial_1to3=rl & (t >= 1) & (t < 3), old_grid_window_5to10=rl & (t >= 5) & (t < 10)).items():
        windows[name] = window(mask)
    segments = []
    for label, mask in [('neutral_raw', neutral), ('neutral_settled1s_after3s', settled),
            ('translation_command', post & (abs(command[:, 0]) > .02) & (abs(command[:, 2]) <= .03)),
            ('rotation_command', post & (abs(command[:, 2]) > .03))]:
        for indices in blocks(mask):
            m = np.zeros(len(t), bool)
            m[indices] = True
            segments.append(dict(label=label, span_s=float(t[indices[-1]]-t[indices[0]]), **window(m)))
    metrics = []
    stable_masks = {}
    for j, name in enumerate(NAMES):
        for label, base in [('rl_all', rl & joined), ('rl_after3s', post), ('neutral_settled1s', settled)]:
            metrics.append(dict(joint=j, name=name, selection=label, **comparison(preceding[base, j], reported[base, j])))
        for width, span in [(3, .5), (5, 1.), (5, 2.), (11, .5)]:
            stable = np.zeros(len(t), bool)
            half = width//2
            for i in range(half, len(t)-half):
                sl = slice(i-half, i+half+1)
                stable[i] = post[sl].all() and np.ptp(preceding[sl, j]) <= span and abs(preceding[i, j]) > 3.
            selection = f'quasistatic_{width}frames_range{span:g}Nm_abs3Nm'
            stable_masks[(j, selection)] = stable
            metrics.append(dict(joint=j, name=name, selection=selection,
                **comparison(preceding[stable, j], reported[stable, j])))
    lag = []
    for j, name in enumerate(NAMES):
        for label, shift in [('current_computed', -1), ('preceding_500Hz', 0),
                ('preceding_older1logged', 1), ('preceding_older2logged', 2), ('preceding_older3logged', 3)]:
            index = np.flatnonzero(post)
            if shift > 0:
                index = index[(index >= shift) & post[np.maximum(index-shift, 0)]]
            source = torque[index, j] if shift == -1 else preceding[index-max(shift, 0), j]
            lag.append(dict(joint=j, name=name, reference=label, **comparison(source, reported[index, j])))
    transitions = np.r_[0, np.flatnonzero(state[1:] != state[:-1])+1]
    saturation = [dict(joint=j, limit_nm=float(limit), command_abs_peak_nm=float(abs(torque[rl, j]).max()),
        preceding_command_abs_peak_nm=float(abs(preceding[rl & joined, j]).max()),
        reported_abs_peak_nm=float(abs(reported[rl & feedback_valid, j]).max()),
        command_near_limit_samples=int(np.count_nonzero(abs(torque[rl, j]) >= .99*limit)),
        preceding_command_near_limit_samples=int(np.count_nonzero(abs(preceding[rl & joined, j]) >= .99*limit)))
        for j, limit in enumerate(cfg['robot']['torque_limit'])]
    report = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
        physical_calibration_status='NOT_TESTED', operator_contact=args.contact,
        operator_annotation='No hand contact; joystick commands used to maintain near standstill.' if args.contact == 'none' else args.contact,
        checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'], onnx_sha256=digest(bundle / 'policy.onnx'),
        config_sha256=digest(cfg_path), database_sha256=db_hash, topic_counts=topic_counts,
        samples=len(samples), rl_samples=int(rl.sum()), feedback_samples=len(feedback_list),
        feedback_invalid_count=int(sum(not f.valid for f in feedback_list)),
        missing_feedback_sequences=sorted(set(sequence.tolist())-set(feedback)),
        rl_missing_feedback=int((rl & ~feedback_valid).sum()), rl_false_flags={k: int((rl & ~v).sum()) for k, v in flags.items()},
        rl_actor_max_abs_error=actor_error, rl_pd_max_abs_error_nm=torque_error,
        fk_python_cpp_max_abs_error_m_s=observer_error,
        rl_sample_dt_ms=summary(dt[rl]*1000), rl_sample_dt_over30ms=int((rl & (dt > .03)).sum()),
        sample_to_feedback_read_ms=summary((read_ns[joined].astype(np.int64)-mono[joined])*1e-6),
        previous_command_to_read_ms=summary((read_ns[joined].astype(np.int64)-command_ns[joined].astype(np.int64))*1e-6),
        command_abs_max=np.max(abs(command[rl]), axis=0).tolist(),
        state_transitions=[dict(state=str(state[i]), time_s=float(t[i]), tilt_deg=float(tilt[i])) for i in transitions],
        windows=windows, segments=segments, saturation=saturation, torque_metrics=metrics,
        neutral_settle_sensitivity=[dict(settle_s=age, **window(post & neutral & (neutral_age >= age))) for age in (.5, 1., 2.)],
        limitations=['Firmware-reported Nm is not independent physical calibration.',
            '50 Hz snapshots and SDK cache timestamps do not identify motor/CAN latency or all 500 Hz deadlines.',
            'Velocity is an IMU/encoder/FK estimate, not externally measured chassis motion; slip can bias it.',
            'Short neutral segments follow commands; no long steady free-drift baseline in this run.',
            'Quasistatic samples are correlated, not independent statistical replicates.',
            'No current, voltage, temperature or external force measurement is recorded.'])
    (out / 'metrics.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    for filename, records in [('joint_torque_metrics.csv', metrics), ('lag_sensitivity.csv', lag)]:
        fields = list(dict.fromkeys(key for row in records for key in row))
        with (out / filename).open('w') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(records)
    np.savez_compressed(out / 'signals.npz', t=t, ros_timestamp_ns=ros_ns, monotonic_ns=mono, sequence_id=sequence, control_tick=ticks,
        state=state, rl=rl, post3=post, neutral=neutral, neutral_age=neutral_age, neutral_settled1=settled,
        q=q, dq=dq, quat=quat, gyro=gyro, command=command, action=action, teacher_action=teacher,
        wheel_velocity_bias=offsets, velocity_bias_diagnostics=get('velocity_bias_diagnostics'), observation=obs,
        torque=torque, reported_torque=reported, previous_computed_torque=preceding,
        feedback_valid=feedback_valid, previous_torque_sent=previous_sent, feedback_read_ns=read_ns,
        previous_command_ns=command_ns, velocity=velocity, wheel_proxy=wheel_proxy, pitch=pitch, tilt=tilt, **flags)
    with (out / 'joined_frames.csv').open('w') as stream:
        writer = csv.writer(stream)
        writer.writerow(['rl_time_s', 'sequence_id', 'monotonic_ns', 'control_tick', 'state',
            'feedback_valid', 'previous_torque_sent', 'feedback_read_ns', 'previous_command_ns',
            'neutral_age_s', 'velocity_fk_m_s', 'pitch_deg']+
            [f'command_{j}' for j in range(3)]+
            [f'{name}_{j}' for name in ('q', 'dq', 'current_command_nm', 'previous_command_nm', 'reported_nm') for j in range(8)])
        for i in range(len(t)):
            writer.writerow([t[i], int(sequence[i]), int(mono[i]), int(ticks[i]), state[i],
                int(feedback_valid[i]), int(previous_sent[i]), int(read_ns[i]), int(command_ns[i]),
                neutral_age[i], velocity[i], pitch[i], *command[i], *q[i], *dq[i], *torque[i], *preceding[i], *reported[i]])
    # Main trajectory and paired torque traces retain the joystick context.
    m = rl
    fig, axes = plt.subplots(5, 1, figsize=(13, 12), sharex=True, constrained_layout=True)
    axes[0].plot(t[m], command[m, 0], label='command x (m/s)')
    axes[0].plot(t[m], command[m, 2], label='command yaw (rad/s)', alpha=.7)
    axes[0].plot(t[m], velocity[m], label='FK velocity estimate (m/s)')
    axes[0].set_ylabel('command / estimate')
    axes[1].plot(t[m], pitch[m], label='pitch (deg)')
    axes[1].plot(t[m], q[m, 2], label='left knee (rad)')
    axes[1].plot(t[m], q[m, 6], label='right knee (rad)')
    axes[1].set_ylabel('posture')
    for ax, joints in zip(axes[2:], ([0, 4], [2, 6], [3, 7])):
        for j in joints:
            line, = ax.plot(t[m], preceding[m, j], label=f'{NAMES[j]} preceding cmd', lw=1)
            ax.plot(t[m], reported[m, j], color=line.get_color(), ls='--', alpha=.75, label=f'{NAMES[j]} reported', lw=1)
        ax.set_ylabel('Nm')
    for ax in axes:
        for indices in blocks(settled):
            ax.axvspan(t[indices[0]], t[indices[-1]], color='green', alpha=.10)
        ax.axvline(3, color='gray', ls=':')
        ax.legend(loc='upper right', fontsize=8, ncol=2)
        ax.grid(alpha=.2)
    axes[-1].set_xlabel('seconds from RL entry; green = neutral held >=1s, RL >=3s')
    fig.suptitle('60000: no hand contact; joystick-compensated run; bias OFF')
    fig.savefig(out / 'torque_overview.png', dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(2, 4, figsize=(15, 8), constrained_layout=True)
    for j, ax in enumerate(axes.flat):
        xx, yy = preceding[post, j], reported[post, j]
        ax.scatter(xx, yy, s=4, alpha=.35)
        low, high = min(xx.min(), yy.min()), max(xx.max(), yy.max())
        ax.plot([low, high], [low, high], color='black', label='1.0 x command')
        ax.plot([low, high], [.6*low, .6*high], color='red', ls='--', label='0.6 x command')
        row = next(r for r in metrics if r['joint'] == j and r['selection'] == 'rl_after3s')
        ax.set_title(f'{NAMES[j]}: gain {row["gain_origin"]:.4f}\nRMS error {row["error_rms_nm"]:.3f} Nm')
        ax.set_xlabel('preceding computed torque (Nm)')
        ax.set_ylabel('firmware-reported torque (Nm)')
        ax.grid(alpha=.2)
    axes.flat[0].legend(fontsize=8)
    fig.suptitle('Telemetry tracking only; firmware units do not certify physical torque calibration')
    fig.savefig(out / 'command_vs_reported.png', dpi=160)
    plt.close(fig)
    inputs = [db, cfg_path, geo_path, bundle / 'policy.onnx', Path(__file__),
        PACKAGE / 'include/tita_controller/velocity_bias.hpp', ROOT / 'test/sim2real/velocity_bias_runtime.cpp',
        ROOT / 'test/sim2real/diagnose_three_case_wheel_bias.py']
    (out / 'inputs.sha256').write_text(''.join(f'{digest(p)}  {p.relative_to(ROOT)}\n' for p in inputs))
    assert digest(db) == db_hash
    print('DESKTOP_DRY_RUN PASS: SQLite integrity, exact integer joins, flags, actor/PD/FK replays; original bag unchanged')
    print('COUNTS', len(samples), int(rl.sum()), len(feedback_list))
    print('ERRORS actor / PD Nm / FK m/s', actor_error, torque_error, observer_error)
    for row in metrics:
        if row['selection'] == 'rl_after3s':
            print('TORQUE', row)
    print('NEUTRAL SEGMENTS', [(s['start_s'], s['end_s'], s['samples'], s['velocity_fk_m_s']) for s in segments if s['label']=='neutral_settled1s_after3s'])


if __name__ == '__main__':
    main()
