"""DESKTOP_DRY_RUN: offline review of finalized FlashSAC SQLite rosbags."""
import argparse
import json
from pathlib import Path
import sqlite3

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message


def review(directory, stem, config):
    db = next((directory / f'{stem}_bag').glob('*.db3'))
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as conn:
        topics = {i: (n, get_message(t)) for i, n, t in conn.execute('SELECT id,name,type FROM topics')}
        rows = {n: [] for n, _ in topics.values()}
        for tid, t, raw in conn.execute('SELECT topic_id,timestamp,data FROM messages ORDER BY timestamp'):
            name, cls = topics[tid]
            rows[name].append((t / 1e9, deserialize_message(raw, cls)))
    names = ['/sim2real/debug/' + n for n in ('state', 'obs', 'action', 'torque')]
    names += ['/tita4252763/joint_states', '/tita4252763/imu_sensor_broadcaster/imu']
    assert len({len(rows[n]) for n in names}) == 1, 'Cannot align cycles with dropped topic rows'
    stamps = np.array([[t for t, _ in rows[n]] for n in names])
    spread = float(np.ptp(stamps, axis=0).max())
    assert spread < .015, f'Topic cycle timestamp spread too large: {spread}'
    start = stamps[0, 0]
    times = stamps[0] - start
    states = np.array([m.data for _, m in rows[names[0]]])
    arrays = {n: np.array([m.data for _, m in rows[f'/sim2real/debug/{n}']]) for n in ('obs', 'action', 'torque')}
    joints = [m for _, m in rows['/tita4252763/joint_states']]
    q = np.array([m.position for m in joints])
    dq = np.array([m.velocity for m in joints])
    imu = [m.orientation for _, m in rows['/tita4252763/imu_sensor_broadcaster/imu']]
    tilt = np.degrees(np.arccos(np.clip([1 - 2 * (p.x ** 2 + p.y ** 2) for p in imu], -1, 1)))
    changes = np.r_[0, np.flatnonzero(states[1:] != states[:-1]) + 1]
    ends = np.r_[changes[1:], len(states) - 1]
    phases = [{'state': str(states[a]), 'start_s': float(times[a]), 'end_s': float(times[b]),
               'duration_s': float(times[b] - times[a])} for a, b in zip(changes, ends)]
    joy = rows['/tita4252763/joy']
    edges = []
    for t, m in joy:
        values = [float(m.axes[i]) for i in (4, 6)]
        if not edges or edges[-1]['left4_right6'] != values:
            edges.append({'time_s': t - start, 'left4_right6': values})
    limit = np.array(config['robot']['torque_limit'])
    metrics = {}
    for state in dict.fromkeys(states):
        mask = states == state
        metrics[str(state)] = {
            'samples': int(mask.sum()), 'tilt_max_deg': float(tilt[mask].max()),
            'joint_speed_abs_max_rad_s': np.abs(dq[mask]).max(axis=0).tolist(),
            'computed_torque_abs_max_nm': np.abs(arrays['torque'][mask]).max(axis=0).tolist(),
            'torque_limit_fraction': (np.abs(arrays['torque'][mask]) >= limit - 1e-5).mean(axis=0).tolist(),
        }
    rl = states == 'rl'
    if rl.any():
        expected = np.zeros_like(q[rl])
        native = [f'joint_{s}_leg_{j}' for s in ('left', 'right') for j in range(1, 5)]
        for i, a in enumerate(config['policy_interface']['actions']):
            j = native.index(a['joint'])
            target = arrays['action'][rl, i] * a['scale'] + a['offset']
            if a['clip']: target = np.clip(target, *a['clip'])
            kd, kp = config['robot']['joint_kd'][j], config['robot']['joint_kp'][j]
            expected[:, j] = kd * (target - dq[rl, j]) if a['kind'] == 'velocity' else kp * (target - q[rl, j]) - kd * dq[rl, j]
        expected = np.clip(expected, -limit, limit)
        metrics['rl']['adapter_max_error_nm'] = float(np.abs(expected - arrays['torque'][rl]).max())
        command = arrays['obs'][rl, 6:9] / [2., 2., .25]
        metrics['rl']['command_abs_max'] = np.abs(command).max(axis=0).tolist()
        metrics['rl']['command_nonzero_fraction'] = float((np.abs(command).max(axis=1) > .01).mean())
    stop = states == 'estop'
    if stop.any():
        expected = np.clip(-dq[stop] * [8., 8., 8., .5, 8., 8., 8., .5], -limit, limit)
        metrics['estop']['damping_max_error_nm'] = float(np.abs(expected - arrays['torque'][stop]).max())
        stop_time = times[stop][0]
        after = stop & (times >= stop_time + .5)
        metrics['estop']['joint_speed_abs_max_after_half_second'] = float(np.abs(dq[after]).max())
    sit = np.flatnonzero(states == 'sit')
    if len(sit):
        legs = [0, 1, 2, 4, 5, 6]
        target = np.array([-.05, .9, -2.6, .05, .9, -2.6])
        metrics['final_sit'] = {'joint_error_deg': np.degrees(q[sit[-1], legs] - target).tolist()}
    console = (directory / f'{stem}_console.log').read_text(errors='replace')
    summary = {
        'run': stem, 'duration_s': float(times[-1]), 'published_samples': len(states),
        'cycle_topic_timestamp_spread_max_s': spread,
        'all_finite': all(np.isfinite(a).all() for a in (*arrays.values(), q, dq, tilt)),
        'phases': phases, 'button_edges': edges,
        'joy_max_gap_s': float(np.diff([t for t, _ in joy]).max()),
        'metrics': metrics, 'can_send_errors': console.count('[CAN_TX'),
        'shutdown_sigbus': 'exit code -7' in console,
        'shutdown_forced_kill': 'sending SIGKILL' in console,
    }
    (directory / f'{stem}_review.json').write_text(json.dumps(summary, indent=2) + '\n')
    fig, ax = plt.subplots(4, 1, figsize=(11, 8), sharex=True, constrained_layout=True)
    order = ['idle', 'transform_up', 'sit', 'rl', 'return_to_sit', 'estop']
    codes = [order.index(s) for s in states]
    ax[0].step(times, codes, where='post', color='#253b53')
    ax[0].set_yticks(range(len(order)), order, fontsize=8)
    ax[0].set_ylim(-.4, 5.4)
    ax[1].plot(times, tilt, color='#335caa')
    ax[1].set_ylabel('Body tilt (deg)')
    ax[2].plot(times, dq[:, 3], label='Left wheel', color='#1c8e88')
    ax[2].plot(times, dq[:, 7], label='Right wheel', color='#d98528')
    ax[2].set_ylabel('Wheel speed\n(rad/s)')
    ax[2].legend(loc='upper right', ncol=2, fontsize=8)
    ax[3].plot(times, arrays['torque'][:, 3], color='#1c8e88')
    ax[3].plot(times, arrays['torque'][:, 7], color='#d98528')
    ax[3].axhline(12., color='grey', linestyle='--', lw=.7)
    ax[3].axhline(-12., color='grey', linestyle='--', lw=.7)
    ax[3].set_ylabel('Computed wheel\ntorque (N m)')
    ax[3].set_xlabel('Seconds from first recorded state')
    for a in ax:
        a.grid(alpha=.2)
        for phase in phases:
            if phase['state'] in ('rl', 'estop'):
                a.axvspan(phase['start_s'], phase['end_s'], alpha=.08,
                          color='#1c8e88' if phase['state'] == 'rl' else '#ba3535')
    fig.suptitle(stem.replace('flashsac_60000_', 'FlashSAC 60000 | '), fontsize=12)
    fig.savefig(directory / f'{stem}_review.png', dpi=160)
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('runs', nargs='+')
    parser.add_argument('--config', type=Path, required=True)
    args = parser.parse_args()
    cfg = json.loads(args.config.read_text())
    for run in args.runs: review(args.directory, run, cfg)
