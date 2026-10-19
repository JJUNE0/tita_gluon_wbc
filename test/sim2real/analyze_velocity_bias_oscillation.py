"""DESKTOP_DRY_RUN: analyze atomic training frames without robot/ROS node creation.

Source ROS and the desktop TrainingSample message overlay before running.
All torque fields are computed commands; velocity is an encoder/IMU proxy.
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
from tita_controller.msg import TrainingSample


def stats(x):
    return dict(mean=float(np.mean(x)), std=float(np.std(x)),
                p05=float(np.percentile(x, 5)), p95=float(np.percentile(x, 95)),
                abs_max=float(np.max(np.abs(x))))


def blocks(mask):
    indices = np.flatnonzero(mask)
    return np.split(indices, np.flatnonzero(np.diff(indices) > 1) + 1) if len(indices) else []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bag', type=Path)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    db = next(args.bag.glob('*.db3'))
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as connection:
        assert connection.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        topic = connection.execute("SELECT id FROM topics WHERE name='/sim2real/training_sample'").fetchone()
        assert topic, 'No atomic training topic in this bag'
        frames = [deserialize_message(row[0], TrainingSample) for row in connection.execute(
            'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', topic)]
        topic_counts = dict(connection.execute('SELECT topics.name,count(*) FROM messages JOIN topics ON messages.topic_id=topics.id GROUP BY topics.id'))
    assert frames
    cfg = json.loads(args.config.read_text())
    sequence = np.array([f.sequence_id for f in frames], dtype=np.uint64)
    monotonic = np.array([f.monotonic_ns for f in frames], dtype=np.uint64)
    assert np.all(np.diff(monotonic.astype(np.int64)) > 0)
    t = (monotonic - monotonic[0]).astype(float) * 1e-9
    states = np.array([f.state for f in frames])
    rl = states == 'rl'
    assert rl.any()
    t -= t[rl][0]
    dt = np.diff(monotonic.astype(np.int64)) * 1e-9
    diag = np.array([f.velocity_bias_diagnostics for f in frames])
    quat = np.array([f.quaternion_wxyz for f in frames])
    q = np.array([f.joint_position for f in frames])
    dq = np.array([f.joint_velocity for f in frames])
    gyro = np.array([f.angular_velocity for f in frames])
    action = np.array([f.action_raw for f in frames])
    teacher = np.array([f.teacher_action for f in frames])
    torque = np.array([f.computed_torque for f in frames])
    offsets = np.array([f.wheel_velocity_bias for f in frames])
    command = np.array([f.command for f in frames])
    valid = np.array([f.sensors_valid and f.policy_valid for f in frames])
    neutral = rl & valid & (np.abs(command).max(axis=1) <= .02)
    active = neutral & (diag[:, 1] > .5)
    assert active.any(), 'No eligible bias frames'
    onset = t[active][0]
    w, x, y, z = quat.T
    pitch = np.rad2deg(np.arcsin(np.clip(2*(w*y-z*x), -1, 1)))
    roll = np.rad2deg(np.arctan2(2*(w*x+y*z), 1-2*(x*x+y*y)))
    base = np.zeros_like(torque)
    recomputed = np.zeros_like(torque)
    rebuilt_teacher = np.zeros_like(teacher)
    native = [f'joint_{side}_leg_{i}' for side in ('left', 'right') for i in range(1, 5)]
    limits = np.array(cfg['robot']['torque_limit'])
    for i, term in enumerate(cfg['policy_interface']['actions']):
        j = native.index(term['joint'])
        target = action[:, i]*term['scale']+term['offset']
        if term['clip']:
            target = np.clip(target, *term['clip'])
        kd, kp = cfg['robot']['joint_kd'][j], cfg['robot']['joint_kp'][j]
        corrected = target + (offsets[:, j//4] if j in (3, 7) and term['kind'] == 'velocity' else 0.)
        base[:, j] = kd*(target-dq[:, j]) if term['kind'] == 'velocity' else kp*(target-q[:, j])-kd*dq[:, j]
        recomputed[:, j] = kd*(corrected-dq[:, j]) if term['kind'] == 'velocity' else kp*(corrected-q[:, j])-kd*dq[:, j]
        rebuilt_teacher[:, i] = (corrected-term['offset'])/term['scale']
    base = np.clip(base, -limits, limits)
    recomputed = np.clip(recomputed, -limits, limits)
    delta = torque-base
    common = lambda a: a[:, [3, 7]].mean(axis=1)
    wheel_proxy = .0925*common(dq)

    def metrics(mask):
        if mask.sum() < 2:
            return {'samples': int(mask.sum())}
        result = {'samples': int(mask.sum()), 'start_s': float(t[mask][0]), 'end_s': float(t[mask][-1])}
        for name, values in dict(pitch_deg=pitch, roll_deg=roll, gyro_y_rad_s=gyro[:, 1],
                                 wheel_proxy_m_s=wheel_proxy, estimated_velocity_m_s=diag[:, 3],
                                 filtered_velocity_m_s=diag[:, 4], bias_m_s=diag[:, 6],
                                 baseline_wheel_torque_nm=common(base), added_wheel_torque_nm=common(delta),
                                 final_wheel_torque_nm=common(torque)).items():
            result[name] = stats(values[mask])
        result['eligible_fraction'] = float((diag[mask, 1] > .5).mean())
        result['wheel_saturation_fraction'] = (np.abs(torque[mask][:, [3, 7]]) >= limits[[3, 7]]-1e-5).mean(axis=0).tolist()
        a, b = common(base)[mask], common(delta)[mask]
        result['baseline_added_torque_correlation'] = float(np.corrcoef(a, b)[0, 1]) if a.std()*b.std() > 1e-9 else None
        return result

    intervals = {'before_bias': metrics(neutral & (t >= .5) & (t < onset)),
                 'bias_first_3s': metrics(neutral & (t >= onset) & (t < onset+3)),
                 'bias_after_3s': metrics(neutral & (t >= onset+3)), 'all_rl': metrics(rl & valid)}
    windows = []
    for start in np.arange(0, t[rl][-1], 2.):
        windows.append(dict(window_start=float(start), **metrics(neutral & (t >= start) & (t < start+2))))
    long_blocks = blocks(neutral & (t >= onset+1))
    longest = max(long_blocks, key=len) if long_blocks else np.array([], dtype=int)
    spectral = {}
    if len(longest) >= 150:
        step = float(np.median(dt))
        uniform = np.arange(t[longest][0], t[longest][-1], step)
        for name, a in dict(pitch=pitch, gyro_y=gyro[:, 1], bias=diag[:, 6],
                            baseline_torque=common(base), added_torque=common(delta),
                            final_torque=common(torque), velocity=diag[:, 3]).items():
            values = np.interp(uniform, t[longest], a[longest])
            power = np.abs(np.fft.rfft((values-values.mean())*np.hanning(len(values))))**2
            freq = np.fft.rfftfreq(len(values), step)
            select = np.flatnonzero((freq >= .2) & (freq <= 10.))
            peaks = select[np.argsort(power[select])[-3:][::-1]]
            spectral[name] = {'top_frequencies_hz': freq[peaks].tolist(),
                              'power_fraction_below_2hz': float(power[(freq >= .2) & (freq < 2)].sum()/max(power[select].sum(), 1e-30))}
    episodes = []
    for indices in blocks(active):
        start, end = t[indices[0]], t[indices[-1]]
        if end-start < 5.:
            continue
        mask = neutral & (t >= start+2.) & (t < end-1.)
        index = indices[0]
        episode = dict(onset_s=float(start), end_s=float(end), settled=metrics(mask),
                       initial_estimated_velocity=float(diag[index, 3]),
                       initial_integral=float(diag[index, 5]), spectra={})
        step = float(np.median(np.diff(t[mask])))
        tx = np.arange(t[mask][0], t[mask][-1], step)
        for name, values in dict(pitch=pitch, gyro_y=gyro[:, 1], bias=diag[:, 6],
                                 added_torque=common(delta), baseline_torque=common(base),
                                 final_torque=common(torque)).items():
            values = np.interp(tx, t[mask], values[mask])
            window = np.hanning(len(values))
            power = abs(np.fft.rfft((values-values.mean())*window))**2
            freq = np.fft.rfftfreq(len(values), step)
            band = (freq >= 6.) & (freq <= 10.)
            denominator = (freq >= .2) & (freq <= 12.)
            episode['spectra'][name] = dict(
                peak_6_10_hz=float(freq[band][np.argmax(power[band])]),
                fraction_6_10_hz=float(power[band].sum()/max(power[denominator].sum(), 1e-30)),
                band_rms=float(np.sqrt(2*power[band].sum()/(len(values)*np.sum(window**2)))))
        episodes.append(episode)
    flags = {key: int(sum(not getattr(f, key) for f in frames if f.state == 'rl'))
             for key in ('sensors_valid', 'policy_valid', 'output_enabled', 'torque_sent', 'teacher_action_valid')}
    report = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='SUSPICIOUS',
                  run=args.bag.name.removesuffix('_bag'), database_sha256=hashlib.sha256(db.read_bytes()).hexdigest(),
                  onnx_sha256='f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a',
                  frames=len(frames), topic_counts=topic_counts, rl_duration_s=float(t[rl][-1]), bias_eligible_onset_s=float(onset),
                  missing_sequences=int((np.diff(sequence)-1).sum()), sample_dt_s=stats(dt),
                  dt_over_30ms=int((dt > .03).sum()), dt_over_60ms=int((dt > .06).sum()),
                  rl_false_flags=flags, command_abs_max=np.abs(command[rl]).max(axis=0).tolist(),
                  torque_reconstruction_max_error_nm=float(np.abs(recomputed[rl & valid]-torque[rl & valid]).max()),
                  teacher_reconstruction_max_error=float(np.abs(rebuilt_teacher[rl & valid]-teacher[rl & valid]).max()),
                  bias_delta_log_max_error_nm=float(np.abs(delta[rl & valid][:, [3, 7]]-diag[rl & valid, 9:11]).max()),
                  intervals=intervals, two_second_windows=windows, spectra=spectral,
                  bias_episodes=episodes,
                  eligibility_transitions=int(np.abs(np.diff(diag[rl, 1])).sum()),
                  limitations=['Single closed-loop run, not an isolated causal A/B test.',
                               'Velocity and wheel rolling speed are proxies, not externally measured chassis velocity.',
                               'Torques are computed transport commands, not measured motor torques.',
                               'Spectral peaks alone cannot determine causality or physical transfer-function phase.'])
    assert report['torque_reconstruction_max_error_nm'] < 1e-4, 'Action/torque mismatch'
    assert report['teacher_reconstruction_max_error'] < 1e-5, 'Teacher-unit reconstruction mismatch'
    assert report['bias_delta_log_max_error_nm'] < 1e-4, 'Added-torque logging mismatch'
    (args.output/'metrics.json').write_text(json.dumps(report, indent=2)+'\n')
    np.savez_compressed(args.output/'signals.npz', t=t, rl=rl, valid=valid, neutral=neutral,
                        pitch=pitch, roll=roll, gyro=gyro, dq=dq, q=q, quat=quat,
                        diag=diag, command=command, torque=torque, baseline=base, delta=delta,
                        action=action, teacher=teacher, dt=dt)
    fig, axes = plt.subplots(6, 1, figsize=(14, 15), sharex=True, constrained_layout=True)
    axes[0].plot(t, command[:, 0], color='black', label='forward command')
    axes[0].plot(t, wheel_proxy, label='wheel rolling proxy', alpha=.8)
    axes[0].plot(t, diag[:, 3], label='IMU/FK velocity estimate', alpha=.8)
    axes[0].set_ylabel('m/s')
    axes[1].plot(t, pitch, label='pitch')
    axes[1].plot(t, roll, label='roll', alpha=.7)
    axes[1].set_ylabel('degrees')
    axes[2].plot(t, diag[:, 6], label='bias u')
    axes[2].plot(t, diag[:, 5], label='integral', alpha=.7)
    axes[2].set_ylabel('m/s (target bias)')
    axes[3].plot(t, common(base), label='baseline PD at recorded state', alpha=.8)
    axes[3].plot(t, common(delta), label='added wheel torque', alpha=.8)
    axes[3].plot(t, common(torque), label='final wheel torque', color='black', lw=.8)
    axes[3].set_ylabel('Nm / wheel (mean)')
    axes[4].plot(t, gyro[:, 1], label='body gyro y')
    axes[4].plot(t, diag[:, 4], label='filtered velocity', alpha=.7)
    axes[4].set_ylabel('rad/s; m/s')
    axes[5].plot(t, diag[:, 1], label='bias eligible')
    axes[5].plot(t, rl.astype(int), label='RL state', ls='--')
    axes[5].set_ylabel('flags')
    axes[5].set_xlabel('Seconds from RL entry')
    for axis in axes:
        axis.axvline(onset, color='red', ls=':', label='bias eligibility onset')
        axis.grid(alpha=.25)
        axis.legend(loc='upper right', fontsize=8, ncol=3)
        axis.set_xlim(-.5, t[rl][-1]+.5)
    fig.suptitle('DESKTOP_DRY_RUN: recorded bias activation / pitch / computed wheel torque')
    fig.savefig(args.output/'oscillation_overview.png', dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True, constrained_layout=True)
    axes[0].plot(t, pitch, label='pitch')
    axes[0].set_ylabel('degrees')
    axes[1].plot(t, common(base), label='baseline at recorded state')
    axes[1].plot(t, common(delta), label='added torque')
    axes[1].plot(t, common(torque), label='final torque', color='black')
    axes[1].set_ylabel('computed Nm / wheel')
    axes[2].plot(t, gyro[:, 1], label='body gyro y')
    axes[2].set_ylabel('rad/s')
    axes[2].set_xlabel('Seconds from RL entry')
    for axis in axes:
        axis.set_xlim(onset+4., onset+5.)
        axis.grid(alpha=.25)
        axis.legend(loc='upper right')
    axes[0].set_ylim(np.min(pitch[(t >= onset+4.) & (t <= onset+5.)])-.2,
                     np.max(pitch[(t >= onset+4.) & (t <= onset+5.)])+.2)
    fig.suptitle('DESKTOP_DRY_RUN: fast balance oscillation; added torque is nearly constant')
    fig.savefig(args.output/'oscillation_zoom.png', dpi=160)
    plt.close(fig)
    print(json.dumps({k: report[k] for k in ['frames', 'rl_duration_s', 'bias_eligible_onset_s',
                                             'missing_sequences', 'sample_dt_s', 'rl_false_flags',
                                             'torque_reconstruction_max_error_nm', 'intervals', 'spectra']}, indent=2))


if __name__ == '__main__':
    main()
