"""DESKTOP_DRY_RUN: inspect recorded buttons, early RL exit and motor feedback.

No ROS nodes, SDK instances or hardware commands. Source ROS and message overlay.
"""
import csv
import hashlib
import json
from pathlib import Path
import sqlite3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import onnxruntime as ort
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

from diagnose_three_case_wheel_bias import targets, torques


def main():
    root = Path(__file__).resolve().parents[2]
    out = root / 'docs/exp/2026-10-17/flashsac_60000_173848_fall_review'
    db = next(out.rglob('*.db3'))
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    before = digest(db)
    required = ('/sim2real/training_sample', '/sim2real/motor_feedback', '/tita4252763/joy')
    rows = {name: [] for name in required}
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as connection:
        assert connection.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        types = {i: (name, get_message(kind)) for i, name, kind in connection.execute(
            'SELECT id,name,type FROM topics') if name in rows}
        for i, stamp, data in connection.execute('SELECT topic_id,timestamp,data FROM messages ORDER BY timestamp'):
            if i in types:
                name, cls = types[i]
                rows[name].append((stamp, deserialize_message(data, cls)))
    samples = [m for _, m in rows[required[0]]]
    feedback = {m.sequence_id: m for _, m in rows[required[1]]}
    stamp = lambda m: m.header.stamp.sec * 10**9 + m.header.stamp.nanosec
    rl_first = next(m for m in samples if m.state == 'rl')
    t0 = stamp(rl_first)
    t = np.array([(stamp(m)-t0)*1e-9 for m in samples])
    mono = np.array([m.monotonic_ns for m in samples], dtype=np.int64)
    seq = np.array([m.sequence_id for m in samples], dtype=np.int64)
    assert np.all(np.diff(seq) == 1) and np.all(np.diff(mono) > 0)
    state = np.array([m.state for m in samples])
    q = np.array([m.joint_position for m in samples])
    dq = np.array([m.joint_velocity for m in samples])
    gyro = np.array([m.angular_velocity for m in samples])
    torque = np.array([m.computed_torque for m in samples])
    w, x, y, z = np.array([m.quaternion_wxyz for m in samples]).T
    pitch = np.degrees(np.arcsin(np.clip(2*(w*y-z*x), -1, 1)))
    tilt = np.degrees(np.arccos(np.clip(1-2*(x*x+y*y), -1, 1)))
    changes = np.r_[0, np.flatnonzero(state[1:] != state[:-1])+1]
    events = [dict(time_s=float(t[i]), state=str(state[i]), pitch_deg=float(pitch[i]),
                   tilt_deg=float(tilt[i]), sensors_valid=samples[i].sensors_valid,
                   gyro_rad_s=gyro[i].tolist(), joint_position=q[i].tolist(),
                   joint_velocity=dq[i].tolist(), command_torque_nm=torque[i].tolist()) for i in changes]
    edges = []
    previous = None
    for received, message in rows[required[2]]:
        buttons = (float(message.axes[4]), float(message.axes[6]))
        if buttons != previous:
            edges.append(dict(source_time_s=(stamp(message)-t0)*1e-9,
                              received_time_s=(received-t0)*1e-9,
                              left_axis_4=buttons[0], right_axis_6=buttons[1]))
            previous = buttons
    rl = state == 'rl'
    bundle = root / 'sim2real/tita_ws/src/tita_controller/policies/flashsac_60000'
    cfg = json.loads((bundle / 'config.json').read_text())
    options = ort.SessionOptions()
    options.intra_op_num_threads = options.inter_op_num_threads = 1
    session = ort.InferenceSession(str(bundle / 'policy.onnx'), sess_options=options)
    actual = np.array([m.action_raw for m in samples if m.state == 'rl'])
    predicted = np.array([session.run(None, {session.get_inputs()[0].name:
        np.array(m.observation, dtype=np.float32)[None]})[0][0] for m in samples if m.state == 'rl'])
    rebuilt = torques(targets(actual, cfg), dict(q=q[rl], dq=dq[rl]), cfg)
    infer_error = float(abs(predicted-actual).max())
    pd_error = float(abs(rebuilt-torque[rl]).max())
    assert infer_error < 2e-5 and pd_error < 1e-4
    assert all(np.max(np.abs(m.wheel_velocity_bias)) == 0 for m in samples)
    reported = np.full_like(torque, np.nan)
    read_delay = []
    for i, sample in enumerate(samples):
        if sample.sequence_id not in feedback:
            continue
        f = feedback[sample.sequence_id]
        assert (f.header == sample.header and f.control_tick == sample.control_tick and
                f.monotonic_ns == sample.monotonic_ns)
        if f.valid:
            assert np.isfinite(f.reported_torque).all()
            reported[i] = f.reported_torque
        if -.2 <= t[i] <= 1.:
            read_delay.append((f.feedback_read_monotonic_ns-f.monotonic_ns)*1e-6)
    near = (t >= -.2) & (t <= 1.)
    early_dt = np.diff(mono)[near[1:] & near[:-1]] * 1e-6
    missing = sorted(set(seq.tolist())-set(feedback))
    result = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='SUSPICIOUS',
        checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
        onnx_sha256=digest(bundle / 'policy.onnx'), database_sha256=before,
        samples=len(samples), feedback_samples=len(feedback), feedback_missing_sequences=missing,
        feedback_invalid_count=sum(not f.valid for f in feedback.values()), rl_samples=int(rl.sum()),
        rl_max_action_error=infer_error, rl_max_pd_torque_error_nm=pd_error,
        state_transitions=events, button_edges=edges,
        early_sample_dt_ms=dict(median=float(np.median(early_dt)), max=float(early_dt.max())),
        early_sample_to_feedback_read_ms=dict(median=float(np.median(read_delay)), max=float(max(read_delay))),
        early_sensor_invalid=sum(not m.sensors_valid for m, keep in zip(samples, near) if keep),
        early_torque_transport_failed=sum(not m.torque_sent for m, keep in zip(samples, near) if keep),
        limitations=['Button telemetry does not identify intentional release, switch/contact issue or receiver behavior.',
                     'Physical collapse onset is not established by body tilt alone.',
                     'Read completion delay is not isolated SDK call time or CAN acquisition age.',
                     'Firmware-reported torques are not independent calibrated physical torque.'])
    (out / 'analysis.json').write_text(json.dumps(result, indent=2)+'\n')
    with (out / 'early_frames.csv').open('w') as stream:
        writer = csv.writer(stream)
        writer.writerow(['rl_time_s', 'state', 'tilt_deg', 'pitch_deg']+
            [f'{name}_{j}' for name in ('q', 'dq', 'command_nm', 'reported_nm') for j in range(8)])
        for i in np.flatnonzero(near):
            writer.writerow([t[i], state[i], tilt[i], pitch[i], *q[i], *dq[i], *torque[i], *reported[i]])
    fig, axes = plt.subplots(4, 1, figsize=(11, 9), sharex=True, constrained_layout=True)
    axes[0].plot(t[near], pitch[near], label='pitch')
    axes[0].plot(t[near], tilt[near], label='tilt')
    axes[0].axhline(np.degrees(.65), color='red', ls=':', label='damp threshold')
    axes[0].set_ylabel('degrees')
    for j in (2, 6):
        axes[1].plot(t[near], q[near, j], label=f'knee {j}')
        axes[2].plot(t[near], torque[near, j], label=f'command {j}')
        axes[2].plot(t[near], reported[near, j], ls='--', label=f'reported {j}')
    axes[1].set_ylabel('joint radians')
    axes[2].set_ylabel('knee Nm')
    for j in (3, 7):
        axes[3].plot(t[near], torque[near, j], label=f'wheel command {j}')
    axes[3].set_ylabel('wheel Nm')
    axes[3].set_xlabel('seconds from RL entry')
    for ax in axes:
        for event in events:
            if 0 <= event['time_s'] <= 1.:
                ax.axvline(event['time_s'], color='gray', alpha=.6)
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(alpha=.25)
    fig.suptitle('RL entry -> left release / return_to_sit -> tilt cutoff')
    fig.savefig(out / 'early_transition.png', dpi=160)
    plt.close(fig)
    assert digest(db) == before
    print(json.dumps({k: v for k, v in result.items() if k not in ('button_edges', 'state_transitions')}, indent=2))
    print('STATE TRANSITIONS', [(e['time_s'], e['state'], round(e['tilt_deg'], 3)) for e in events])
    print('NEARBY BUTTON EDGES', [e for e in edges if -.5 <= e['source_time_s'] <= 1.])


if __name__ == '__main__':
    main()
