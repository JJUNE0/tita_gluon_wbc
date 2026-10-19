"""DESKTOP_DRY_RUN: inspect finalized legacy bags for return/stop handoff.

No robot SDK, ROS node or actuator interface is instantiated.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message


def nearest(source, target):
    right = np.clip(np.searchsorted(source, target), 0, len(source)-1)
    left = np.maximum(right-1, 0)
    return np.where(abs(source[left]-target) <= abs(source[right]-target), left, right)


def analyze(root, run, output):
    db = next((root/f'{run}_bag').glob('*.db3'))
    required = ['/sim2real/debug/state', '/sim2real/debug/torque', '/tita4252763/joint_states',
                '/tita4252763/imu_sensor_broadcaster/imu']
    rows = {name: [] for name in required}
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as connection:
        assert connection.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        topics = {i: (name, get_message(kind)) for i, name, kind in connection.execute(
            'SELECT id,name,type FROM topics') if name in rows}
        for topic, stamp, raw in connection.execute('SELECT topic_id,timestamp,data FROM messages ORDER BY timestamp'):
            if topic in topics:
                name, cls = topics[topic]
                rows[name].append((stamp*1e-9, deserialize_message(raw, cls)))
    reference = np.array([s for s, _ in rows[required[0]]])
    states = np.array([m.data for _, m in rows[required[0]]])
    messages, errors = {}, {}
    valid = np.ones(len(reference), dtype=bool)
    for name in required[1:]:
        stamps = np.array([s for s, _ in rows[name]])
        index = nearest(stamps, reference)
        errors[name] = abs(stamps[index]-reference)
        valid &= (errors[name] <= .008) & np.r_[True, np.diff(index) > 0]
        messages[name] = [rows[name][i][1] for i in index]
    assert valid.mean() > .98
    reference, states = reference[valid], states[valid]
    messages = {k: [m for m, keep in zip(v, valid) if keep] for k, v in messages.items()}
    q = np.array([m.position for m in messages[required[2]]])
    dq = np.array([m.velocity for m in messages[required[2]]])
    torque = np.array([m.data for m in messages[required[1]]])
    quat = np.array([[m.orientation.w, m.orientation.x, m.orientation.y, m.orientation.z]
                     for m in messages[required[3]]])
    assert all(np.isfinite(a).all() for a in (q, dq, torque, quat))
    tilt = np.degrees(np.arccos(np.clip(1-2*(quat[:, 1]**2+quat[:, 2]**2), -1, 1)))
    changes = np.r_[0, np.flatnonzero(states[1:] != states[:-1])+1]
    result = dict(run=run, database_sha256=hashlib.sha256(db.read_bytes()).hexdigest(),
                  aligned_samples=int(valid.sum()), excluded_samples=int((~valid).sum()),
                  max_alignment_s={k: float(v[valid].max()) for k, v in errors.items()},
                  state_changes=[{'state': str(states[i]), 'time_s': float(reference[i]-reference[0]),
                                  'tilt_deg': float(tilt[i])} for i in changes], events=[])
    for index in changes:
        if states[index] not in ('return_to_sit', 'estop'):
            continue
        event = str(states[index])
        t = reference-reference[index]
        following = changes[changes > index]
        end = int(following[0]) if len(following) else len(states)
        mask = (np.arange(len(states)) >= index) & (np.arange(len(states)) < end)
        summary = dict(state=event, duration_s=float(t[end-1]), entry_q=q[index].tolist(),
                       entry_dq=dq[index].tolist(), entry_torque=torque[index].tolist(),
                       preceding_torque=torque[max(index-1, 0)].tolist(),
                       peak_tilt_deg=float(tilt[mask].max()),
                       following_state=str(states[end]) if end < len(states) else None,
                       following_time_s=float(t[end]) if end < len(states) else None,
                       following_tilt_deg=float(tilt[end]) if end < len(states) else None,
                       snapshots=[])
        for pivot in (0., .1, .2, .5, .9, 1., 2., 2.2):
            j = int(np.argmin(abs(t-pivot)))
            if abs(t[j]-pivot) < .025:
                summary['snapshots'].append(dict(t=float(t[j]), state=str(states[j]),
                                                tilt_deg=float(tilt[j]), q=q[j].tolist(),
                                                dq=dq[j].tolist(), torque=torque[j].tolist()))
        if event == 'estop':
            kd = np.array([8., 8., 8., .5, 8., 8., 8., .5])
            limits = np.array([60., 60., 60., 12., 60., 60., 60., 12.])
            error = float(abs(torque[mask]-np.clip(-dq[mask]*kd, -limits, limits)).max())
            summary['damping_reconstruction_max_error_nm'] = error
            assert error < 1e-4
        sit = np.array([-.05, .9, -2.6, 0., .05, .9, -2.6, 0.])
        alpha = np.clip((t+.002)/2., 0, 1)
        alpha = alpha*alpha*(3-2*alpha)
        target = q[index]+alpha[:, None]*(sit-q[index])
        fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True, constrained_layout=True)
        axes[0].plot(t, tilt, label='measured tilt')
        axes[0].axhline(np.degrees(.65), color='red', ls='--', label='damp threshold')
        axes[0].set_ylabel('degrees')
        for j in (0, 1, 2):
            axes[1].plot(t, q[:, j], label=f'left joint {j+1}')
            if event == 'return_to_sit':
                axes[1].plot(t, np.where(mask, target[:, j], np.nan), ls='--', alpha=.7,
                             label=f'joint {j+1} return reference')
            axes[2].plot(t, torque[:, j], label=f'left joint {j+1}')
        axes[1].set_ylabel('rad')
        axes[2].set_ylabel('computed Nm')
        axes[2].set_xlabel('Seconds from mode change')
        for ax in axes:
            ax.axvline(0, color='black', ls=':')
            if end < len(states):
                ax.axvline(t[end], color='red', ls=':', label=str(states[end]))
            ax.set_xlim(-.5, 3.)
            ax.grid(alpha=.25)
            ax.legend(fontsize=8, loc='best')
        fig.suptitle(f'DESKTOP_DRY_RUN: {run}\n{event}; reference reconstructed from first aligned entry frame')
        fig.savefig(output/f'{run}_{event}.png', dpi=150)
        plt.close(fig)
        result['events'].append(summary)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('runs', nargs='+')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    result = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='SUSPICIOUS',
                  runs=[analyze(args.root, run, args.output) for run in args.runs])
    (args.output/'recorded_transitions.json').write_text(json.dumps(result, indent=2)+'\n')
    for run in result['runs']:
        print(run['run'], 'samples', run['aligned_samples'], 'excluded', run['excluded_samples'])
        for event in run['events']:
            print(event['state'], 'next', event['following_state'], 'after', event['following_time_s'],
                  'tilt', event['following_tilt_deg'], 'peak', event['peak_tilt_deg'])
            for x in event['snapshots'][:5]:
                print('t',round(x['t'],3),x['state'],'tilt',round(x['tilt_deg'],2),
                      'q_L',np.round(x['q'][:3],3),'tau_L',np.round(x['torque'][:3],3))


if __name__ == '__main__':
    main()
