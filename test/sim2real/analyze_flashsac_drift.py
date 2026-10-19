"""DESKTOP_DRY_RUN: timestamp-aligned analysis of finalized FlashSAC bags.

Wheel-equivalent velocity is a rolling proxy, not measured chassis velocity.
No ROS node, robot API, network connection or actuator command is constructed.
"""

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


def nearest(source, reference):
    right = np.clip(np.searchsorted(source, reference), 0, len(source) - 1)
    left = np.maximum(right - 1, 0)
    return np.where(abs(source[left] - reference) <= abs(source[right] - reference), left, right)


def spans(mask, times):
    indices = np.flatnonzero(mask)
    if not len(indices):
        return []
    split = np.flatnonzero((np.diff(indices) > 1) | (np.diff(times[indices]) > .045)) + 1
    return np.split(indices, split)


def analyze(directory, run, cfg):
    database = next((directory / f'{run}_bag').glob('*.db3'))
    with sqlite3.connect(f'file:{database}?mode=ro', uri=True) as conn:
        assert conn.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        topics = {i: (name, get_message(kind)) for i, name, kind in
                  conn.execute('SELECT id,name,type FROM topics')}
        rows = {name: [] for name, _ in topics.values()}
        for tid, stamp, raw in conn.execute('SELECT topic_id,timestamp,data FROM messages ORDER BY timestamp'):
            name, cls = topics[tid]
            rows[name].append((stamp / 1e9, deserialize_message(raw, cls)))
    reference = '/sim2real/debug/obs'
    aliases = {key: f'/sim2real/debug/{key}' for key in ('state', 'action', 'torque')}
    aliases.update(joints='/tita4252763/joint_states', imu='/tita4252763/imu_sensor_broadcaster/imu')
    absolute = np.array([stamp for stamp, _ in rows[reference]])
    aligned, offsets, counts = {}, {}, {}
    valid = np.ones(len(absolute), dtype=bool)
    for key, topic in aliases.items():
        stamps = np.array([stamp for stamp, _ in rows[topic]])
        index = nearest(stamps, absolute)
        delta = abs(stamps[index] - absolute)
        valid &= (delta <= .008) & np.r_[True, np.diff(index) > 0]
        aligned[key] = [rows[topic][i][1] for i in index]
        offsets[key] = delta
        counts[key] = len(stamps)
    assert valid.mean() > .98, f'Too many unaligned cycles: {valid.mean()}'
    original_start = absolute[0]
    absolute = absolute[valid]
    times = absolute - original_start
    aligned = {key: [m for m, keep in zip(msgs, valid) if keep] for key, msgs in aligned.items()}
    obs = np.array([m.data for (_, m), keep in zip(rows[reference], valid) if keep])
    states = np.array([m.data for m in aligned['state']])
    action = np.array([m.data for m in aligned['action']])
    torque = np.array([m.data for m in aligned['torque']])
    q = np.array([m.position for m in aligned['joints']])
    dq = np.array([m.velocity for m in aligned['joints']])
    quat = np.array([[m.orientation.w, m.orientation.x, m.orientation.y, m.orientation.z]
                     for m in aligned['imu']])
    assert all(np.isfinite(a).all() for a in (obs, action, torque, q, dq, quat))
    w, x, y, z = quat.T
    pitch = np.degrees(np.arcsin(np.clip(2 * (w * y - z * x), -1, 1)))
    roll = np.degrees(np.arctan2(2 * (w * x + y * z), 1 - 2 * (x*x + y*y)))
    tilt = np.degrees(np.arccos(np.clip(1 - 2 * (x*x + y*y), -1, 1)))
    command = obs[:, 6:9] / [2., 2., .25]
    gyro_z = obs[:, 2] / .25
    wheels = dq[:, [3, 7]]
    wheel_targets = action[:, [3, 7]] * 20.
    equivalent = wheels.mean(axis=1) * .0925
    rl = states == 'rl'
    assert rl.any()
    rl_start = times[rl][0]
    elapsed = times - rl_start
    joy_stamps = np.array([stamp for stamp, _ in rows['/tita4252763/joy']])
    joy_index = nearest(joy_stamps, absolute)
    sticks = np.array([[rows['/tita4252763/joy'][i][1].axes[j] for j in (2, 3)] for i in joy_index])

    def metrics(mask):
        if not mask.any():
            return {'samples': 0}
        return {
            'samples': int(mask.sum()),
            'command_mean': command[mask].mean(axis=0).tolist(),
            'wheel_speed_mean_rad_s': wheels[mask].mean(axis=0).tolist(),
            'wheel_target_mean_rad_s': wheel_targets[mask].mean(axis=0).tolist(),
            'wheel_equivalent_mean_m_s': float(equivalent[mask].mean()),
            'wheel_equivalent_median_m_s': float(np.median(equivalent[mask])),
            'wheel_equivalent_p10_p90_m_s': np.percentile(equivalent[mask], [10, 90]).tolist(),
            'negative_common_speed_fraction': float((equivalent[mask] < 0).mean()),
            'computed_wheel_torque_mean_nm': torque[mask][:, [3, 7]].mean(axis=0).tolist(),
            'pitch_mean_deg': float(pitch[mask].mean()),
            'pitch_std_deg': float(pitch[mask].std()),
            'roll_mean_deg': float(roll[mask].mean()),
            'tilt_peak_deg': float(tilt[mask].max()),
            'body_gyro_z_mean_rad_s': float(gyro_z[mask].mean()),
            'raw_stick_abs_max': abs(sticks[mask]).max(axis=0).tolist(),
        }

    neutral = rl & (abs(command).max(axis=1) < .01) & (abs(sticks).max(axis=1) < .013)
    settled = np.zeros_like(neutral)
    windows = []
    for indices in spans(neutral, times):
        start, end = indices[0], indices[-1]
        duration = times[end] - times[start]
        if duration < 3.:
            continue
        mask = np.zeros_like(neutral)
        mask[indices] = (times[indices] >= times[start] + 2.) & (elapsed[indices] >= 2.)
        settled |= mask
        windows.append({
            'start_from_rl_s': float(elapsed[start]), 'end_from_rl_s': float(elapsed[end]),
            'duration_s': float(duration), 'settled_after_2s': metrics(mask),
        })

    expected = np.zeros_like(torque)
    native = [f'joint_{side}_leg_{j}' for side in ('left', 'right') for j in range(1, 5)]
    for i, term in enumerate(cfg['policy_interface']['actions']):
        j = native.index(term['joint'])
        target = action[:, i] * term['scale'] + term['offset']
        if term['clip']:
            target = np.clip(target, *term['clip'])
        kd, kp = cfg['robot']['joint_kd'][j], cfg['robot']['joint_kp'][j]
        expected[:, j] = kd * (target - dq[:, j]) if term['kind'] == 'velocity' else kp * (target - q[:, j]) - kd * dq[:, j]
    limit = np.array(cfg['robot']['torque_limit'])
    expected = np.clip(expected, -limit, limit)
    changes = np.r_[0, np.flatnonzero(states[1:] != states[:-1]) + 1]
    phases = [{'state': str(states[i]), 'time_from_rl_s': float(elapsed[i]),
               'tilt_deg': float(tilt[i])} for i in changes]
    console = (directory / f'{run}_console.log').read_text(errors='replace')
    summary_text = (directory / f'{run}_summary.md').read_text()
    entry = np.flatnonzero(rl)[0]
    yaw_mask = rl & (elapsed >= 2.) & (abs(command[:, 2]) >= .1)
    yaw_error = gyro_z[yaw_mask] - command[yaw_mask, 2]
    neutral_blocks = []
    for window in windows:
        start = window['start_from_rl_s'] + 2.
        for block_start in np.arange(start, window['end_from_rl_s'] - 1., 1.):
            mask = settled & (elapsed >= block_start) & (elapsed < block_start + 1.)
            neutral_blocks.append({'start_from_rl_s': float(block_start), **metrics(mask)})
    report = {
        'execution_domain': 'DESKTOP_DRY_RUN', 'run': run,
        'evidence_status': 'SUSPICIOUS',
        'onnx_sha256': 'f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a',
        'new_speed_config': 'd429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d' in summary_text,
        'alignment': {'reference_samples': len(valid), 'kept': int(valid.sum()),
                      'excluded': int((~valid).sum()), 'topic_counts': counts,
                      'max_kept_offset_s': {k: float(v[valid].max()) for k, v in offsets.items()}},
        'phases': phases, 'rl_duration_s': float(elapsed[rl][-1]),
        'command_abs_max': abs(command[rl]).max(axis=0).tolist(),
        'all_rl': metrics(rl), 'first_second': metrics(rl & (elapsed < 1.)),
        'all_neutral': metrics(neutral), 'settled_neutral': metrics(settled),
        'neutral_windows': windows,
        'neutral_1s_blocks': neutral_blocks,
        'forward_straight': metrics(rl & (elapsed >= 2.) & (command[:, 0] >= .15) & (abs(command[:, 2]) < .03)),
        'reverse_straight': metrics(rl & (elapsed >= 2.) & (command[:, 0] <= -.15) & (abs(command[:, 2]) < .03)),
        'yaw_command': metrics(yaw_mask),
        'yaw_tracking': {
            'body_gyro_z_rmse_rad_s': float(np.sqrt(np.mean(yaw_error**2))) if len(yaw_error) else None,
            'body_gyro_z_command_correlation': float(np.corrcoef(command[yaw_mask, 2], gyro_z[yaw_mask])[0, 1]) if len(yaw_error) > 1 else None,
        },
        'adapter_max_error_nm': float(abs(expected[rl] - torque[rl]).max()),
        'rl_torque_limit_fraction': (abs(torque[rl]) >= limit - 1e-5).mean(axis=0).tolist(),
        'first_rl_wheel_targets_rad_s': wheel_targets[entry].tolist(),
        'can_errors': console.count('[CAN_TX'),
        'shutdown_forced_kill': 'sending SIGKILL' in console,
        'limitations': ['No chassis translation or external force measurement.',
                        'Neutral windows discard their first 2 s; push/recovery events are not excluded without operator labels.',
                        'Wheel-equivalent speed assumes 0.0925 m radius and no slip, ignoring leg/body rotation.',
                        'Nearest receipt timestamps within 8 ms, unique per topic; this is not hardware time synchronization.',
                        'Computed torque topic is not applied motor torque.'],
    }
    output = directory / f'{run}_drift_analysis'
    output.with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
    fig, axes = plt.subplots(5, 1, figsize=(12, 11), sharex=True, constrained_layout=True)
    axes[0].plot(elapsed, command[:, 0], label='Forward command', color='black', lw=1.1)
    axes[0].plot(elapsed, equivalent, label='Wheel rolling proxy', color='#197d93', lw=.8)
    axes[0].set_ylabel('m/s (proxy)')
    axes[1].plot(elapsed, command[:, 2], label='Yaw command', color='black', lw=1.1)
    axes[1].plot(elapsed, gyro_z, label='Measured body gyro z', color='#936bb0', lw=.8)
    axes[1].set_ylabel('rad/s')
    axes[2].plot(elapsed, pitch, label='Pitch', color='#b16c27')
    axes[2].plot(elapsed, roll, label='Roll', color='#527b4f')
    axes[2].set_ylabel('deg')
    axes[3].plot(elapsed, wheels[:, 0], label='Left measured', color='#197d93')
    axes[3].plot(elapsed, wheels[:, 1], label='Right measured', color='#b16c27')
    axes[3].set_ylabel('Wheel rad/s')
    axes[4].plot(elapsed, torque[:, 3], label='Left computed', color='#197d93')
    axes[4].plot(elapsed, torque[:, 7], label='Right computed', color='#b16c27')
    axes[4].set_ylabel('Wheel N m')
    axes[4].set_xlabel('Seconds from RL entry; blue spans = neutral, red line = state transition')
    for ax in axes:
        for window in windows:
            ax.axvspan(window['start_from_rl_s'], window['end_from_rl_s'], color='#197d93', alpha=.08)
        for phase in phases:
            if phase['time_from_rl_s'] > 0:
                ax.axvline(phase['time_from_rl_s'], color='red', lw=.8, alpha=.5)
        ax.axhline(0, color='grey', lw=.6)
        ax.grid(alpha=.2)
        ax.legend(loc='upper right', fontsize=8, ncol=2)
        ax.set_xlim(-1., elapsed[rl][-1] + 3.)
    fig.suptitle(run + '\nWheel rolling proxy is not measured chassis speed', fontsize=11)
    fig.savefig(output.with_suffix('.png'), dpi=150)
    plt.close(fig)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('runs', nargs='+')
    parser.add_argument('--config', type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    for name in args.runs:
        analyze(args.directory, name, config)
