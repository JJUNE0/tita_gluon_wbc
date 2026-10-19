"""DESKTOP_DRY_RUN: copied bags only; no ROS node/SDK/CAN. Compare four sphere candidates."""
import argparse
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
from scipy.integrate import trapezoid
from scipy.signal import butter, coherence, sosfiltfilt, welch
from tita_controller.msg import ActionFilterSample, MotorFeedback, TrainingSample

ROOT = Path(__file__).resolve().parents[2]
NAMES = ['L_hip', 'L_thigh', 'L_knee', 'L_wheel', 'R_hip', 'R_thigh', 'R_knee', 'R_wheel']
LEGS = [0, 1, 2, 4, 5, 6]
ZERO = np.array([.02, .02, .03], dtype=np.float32)
RADIUS = .0925


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runs(mask):
    edges = np.flatnonzero(np.diff(np.r_[0, np.asarray(mask, int), 0]))
    return list(zip(edges[::2], edges[1::2]))


def rms(x, axis=0):
    return np.sqrt(np.mean(np.asarray(x)**2, axis=axis))


def spectrum(x, mask, fs=50.):
    x = np.asarray(x)
    if x.ndim == 1:
        x = x[:, None]
    accum, weight, freq = None, 0, None
    for a, b in runs(mask):
        if b-a < 128:
            continue
        n = min(512, b-a)
        freq, power = welch(x[a:b], fs=fs, nperseg=n, nfft=512, noverlap=n//2, detrend='linear', axis=0)
        accum = power*(b-a) if accum is None else accum+power*(b-a)
        weight += b-a
    if weight == 0:
        return {}, None, None
    power = accum/weight
    out = {}
    for lo, hi in ((.3, 3), (3, 8), (8, 15), (15, 25)):
        band = (freq >= lo) & (freq <= hi)
        out[f'{lo:g}-{hi:g}_rms'] = np.sqrt(trapezoid(power[band], freq[band], axis=0)).tolist()
    band = (freq >= 1) & (freq <= 24.9)
    out['peak_hz_1to24p9'] = freq[band][np.argmax(power[band], axis=0)].tolist()
    for lo, hi, key in ((.3, 24.9, 'peak_hz_0p3to24p9'), (.3, 3., 'peak_hz_0p3to3'), (3., 24.9, 'peak_hz_3to24p9')):
        band = (freq >= lo) & (freq <= hi)
        out[key] = freq[band][np.argmax(power[band], axis=0)].tolist()
    return out, freq, power


def highpass_rms(x, mask, fs=50.):
    chunks = []
    sos = butter(4, 3., btype='highpass', fs=fs, output='sos')
    for a, b in runs(mask):
        if b-a >= 128:
            chunks.append(sosfiltfilt(sos, x[a:b], axis=0)[25:-25])
    return rms(np.concatenate(chunks)) if chunks else np.full(x.shape[1], np.nan)


def load(bag, cfg):
    db = next(bag.glob('*.db3'))
    with sqlite3.connect(f'file:{db.resolve()}?mode=ro', uri=True) as conn:
        assert conn.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        ids = dict(conn.execute('select name,id from topics'))
        counts = dict(conn.execute('select topics.name,count(*) from messages join topics '
            'on messages.topic_id=topics.id group by topics.id'))
        def rows(topic, cls):
            return [deserialize_message(data, cls) for data, in conn.execute(
                'select data from messages where topic_id=? order by timestamp', (ids[topic],))]
        samples = rows('/sim2real/training_sample', TrainingSample)
        feedback = rows('/sim2real/motor_feedback', MotorFeedback)
        filters = rows('/sim2real/action_filter_sample', ActionFilterSample)
    get = lambda key: np.array([getattr(s, key) for s in samples])
    d = {k: get(v) for k, v in dict(mono='monotonic_ns', seq='sequence_id', tick='control_tick',
        state='state', cmd='command', q='joint_position', dq='joint_velocity', quat='quaternion_wxyz',
        gyro='angular_velocity', raw='action_raw', tau='computed_torque', obs='observation',
        teacher='teacher_action', bias='wheel_velocity_bias').items()}
    d['mono'] = d['mono'].astype(np.int64)
    assert np.all(np.diff(d['mono']) > 0)
    assert np.all(np.diff(d['seq'].astype(np.int64)) == 1)
    assert d['obs'].shape[1] == 34
    d['rl'] = d['state'] == 'rl'
    d['t'] = (d['mono']-d['mono'][d['rl']][0])*1e-9
    d['dt'] = np.r_[.02, np.diff(d['t'])]
    d['zero'] = (abs(d['cmd'].astype(np.float32)) <= ZERO).all(1)
    d['flags'] = {k: int(np.count_nonzero(~get(k)[d['rl']])) for k in (
        'sensors_valid', 'policy_valid', 'output_enabled', 'torque_sent', 'teacher_action_valid')}
    assert all(v == 0 for v in d['flags'].values())
    assert np.isfinite(np.c_[d['q'], d['dq'], d['quat'], d['gyro'], d['obs'], d['raw'], d['tau']]).all()
    assert not d['bias'][d['rl']].any()
    table = {(x.sequence_id, x.monotonic_ns): x for x in filters}
    fb = {(x.sequence_id, x.monotonic_ns): x for x in feedback}
    assert len(table) == len(filters) and len(fb) == len(feedback)
    d['applied'] = np.full_like(d['raw'], np.nan)
    d['reported'] = np.full_like(d['tau'], np.nan)
    d['previous'] = np.full_like(d['tau'], np.nan)
    d['feedback_age'] = np.full(len(samples), np.nan)
    missing = 0
    for i, sample in enumerate(samples):
        key = (sample.sequence_id, sample.monotonic_ns)
        f = table.get(key)
        if f is not None:
            assert f.control_tick == sample.control_tick
            assert f.leg_action_filter == cfg['policy_interface']['leg_action_filter']
            d['applied'][i] = f.action_applied
        else:
            assert not d['rl'][i]
            missing += 1
        feedback_sample = fb.get(key)
        if feedback_sample is not None and feedback_sample.valid and feedback_sample.previous_torque_sent:
            assert feedback_sample.control_tick == sample.control_tick
            assert feedback_sample.previous_command_monotonic_ns < sample.monotonic_ns
            d['reported'][i] = feedback_sample.reported_torque
            d['previous'][i] = feedback_sample.previous_computed_torque
            d['feedback_age'][i] = (sample.monotonic_ns-feedback_sample.previous_command_monotonic_ns)*1e-6
    expected = d['raw'].copy()
    last = None
    for i in range(len(samples)):
        if not d['rl'][i]:
            last = None
            continue
        if cfg['policy_interface']['leg_action_filter'] == 'ma2_legs' and last is not None:
            expected[i, LEGS] = .5*d['raw'][i, LEGS]+.5*last[LEGS]
        last = d['raw'][i].copy()
    d['filter_error'] = float(abs(expected[d['rl']]-d['applied'][d['rl']]).max())
    d['teacher_error'] = float(abs(d['teacher'][d['rl']]-d['applied'][d['rl']]).max())
    assert d['filter_error'] == 0 and d['teacher_error'] < 1e-6
    terms = cfg['policy_interface']['actions']
    assert [x['joint'] for x in terms] == [f'joint_{side}_leg_{j}' for side in ('left', 'right') for j in range(1, 5)]
    target = np.zeros_like(d['tau'])
    for i, term in enumerate(terms):
        target[:, i] = np.clip(d['applied'][:, i].astype(float)*term['scale']+term['offset'], *term['clip'])
    kp, kd, cap = (np.array(cfg['robot'][k]) for k in ('joint_kp', 'joint_kd', 'torque_limit'))
    reconstructed = kp*(target-d['q'])-kd*d['dq']
    reconstructed[:, [3, 7]] = kd[[3, 7]]*(target[:, [3, 7]]-d['dq'][:, [3, 7]])
    d['torque_error'] = float(abs(np.clip(reconstructed, -cap, cap)[d['rl']]-d['tau'][d['rl']]).max())
    assert d['torque_error'] < 1e-8, d['torque_error']
    d['target'] = target
    w, x, y, z = d['quat'].T
    d['yaw'] = np.unwrap(np.arctan2(2*(w*z+x*y), 1-2*(y*y+z*z)))
    d['pitch'] = np.arcsin(np.clip(2*(w*y-z*x), -1, 1))
    d['roll'] = np.arctan2(2*(w*x+y*z), 1-2*(x*x+y*y))
    d['yaw_rate'] = (d['gyro'][:, 1]*np.sin(d['roll'])+d['gyro'][:, 2]*np.cos(d['roll']))/np.cos(d['pitch'])
    qw = np.unwrap(d['q'][:, [3, 7]], axis=0)
    d['q_unwrapped'] = d['q'].copy()
    d['q_unwrapped'][:, [3, 7]] = qw
    d['s'] = RADIUS*.5*(qw.sum(1)+2*d['pitch']+d['q'][:, [1, 2, 5, 6]].sum(1))
    d['v_proxy'] = np.gradient(d['s'], d['t'])
    d['wheel_diff_rate'] = RADIUS*(d['dq'][:, 7]+d['dq'][:, 5]+d['dq'][:, 6]
        -d['dq'][:, 3]-d['dq'][:, 1]-d['dq'][:, 2])
    rebuilt = np.zeros(len(samples))
    d['x_unclipped'] = np.full(len(samples), np.nan)
    reference = d['s'][0]
    for i in range(len(samples)):
        if not d['rl'][i] or not d['zero'][i] or (i and not d['rl'][i-1]):
            reference = d['s'][i]
        rebuilt[i] = np.clip(d['s'][i]-reference, -.3, .3) if d['rl'][i] and d['zero'][i] else 0.
        if d['rl'][i] and d['zero'][i]:
            d['x_unclipped'][i] = d['s'][i]-reference
    d['x_error'] = d['obs'][:, 33]/5.
    d['x_parity'] = float(abs(rebuilt[d['rl']]-d['x_error'][d['rl']]).max())
    assert d['x_parity'] < 1e-6
    d['pair'] = np.r_[False, d['rl'][1:] & d['rl'][:-1] & (np.diff(d['tick'].astype(np.int64)) == 10)]
    d['settled'] = np.zeros(len(samples), bool)
    d['late_zero'] = np.zeros(len(samples), bool)
    for a, b in runs(d['rl'] & d['zero']):
        d['settled'][a:b] = (d['t'][a:b]-d['t'][a] >= 1.) & (d['t'][a:b] >= 3.)
        if d['t'][b-1]-d['t'][a] >= 15.:
            d['late_zero'][a:b] = d['t'][a:b] >= d['t'][b-1]-10.
    d['common'] = np.zeros(len(samples), bool)
    for a, b in runs(d['rl'] & d['zero']):
        if d['t'][b-1]-d['t'][a] >= 13.:
            d['common'][a:b] = (d['t'][a:b]-d['t'][a] >= 3.) & (d['t'][a:b]-d['t'][a] < 13.)
            break
    d['quality'] = dict(db_sha256=digest(db), topic_counts=counts, false_rl_flags=d['flags'],
        missing_filter_nonrl=missing, missing_feedback_rl=int((d['rl'] & ~np.isfinite(d['reported']).all(1)).sum()),
        sequence_contiguous=True, max_filter_error=d['filter_error'], max_teacher_error=d['teacher_error'],
        max_torque_replay_error_nm=d['torque_error'], max_x_observation_replay_error_m=d['x_parity'],
        dt_rl_ms_percentiles=(1000*np.percentile(d['dt'][d['rl']], [0, 50, 95, 99, 100])).tolist())
    idle = (d['state'] == 'idle') & (abs(d['dq'][:, LEGS]).max(1) < .03) & (abs(d['dq'][:, [3, 7]]).max(1) < .05)
    d['quality']['stationary_idle_samples'] = int(idle.sum())
    d['quality']['stationary_idle_gz_median_dps'] = float(np.degrees(np.median(d['gyro'][idle, 2]))) if idle.any() else None
    return d


def phase_metrics(d, mask, cfg):
    if not mask.any():
        return dict(samples=0)
    pair = mask & d['pair']
    feedback = mask & np.isfinite(d['reported']).all(1)
    delta_target = np.r_[np.zeros((1, 8)), np.diff(d['target'], axis=0)]
    kp, kd, cap = (np.array(cfg['robot'][k]) for k in ('joint_kp', 'joint_kd', 'torque_limit'))
    injected = delta_target*np.where(kp > 0, kp, kd)
    step = d['tau']-d['previous']
    good = pair & np.isfinite(step).all(1)
    raw_delta = np.r_[np.zeros((1, 8)), np.diff(d['raw'], axis=0)]
    applied_delta = np.r_[np.zeros((1, 8)), np.diff(d['applied'], axis=0)]
    consecutive = pair[1:] & pair[:-1]
    raw_lag1 = [float(np.corrcoef(raw_delta[1:, j][consecutive], raw_delta[:-1, j][consecutive])[0, 1])
        if consecutive.sum() > 10 and np.std(raw_delta[1:, j][consecutive]) > 1e-9 else None for j in range(8)]
    yaw_change, span = 0., 0.
    for a, b in runs(mask):
        if b-a > 1:
            yaw_change += d['yaw'][b-1]-d['yaw'][a]
            span += d['t'][b-1]-d['t'][a]
    spec, _, _ = spectrum(np.degrees(d['gyro'][:, 1]), mask)
    joint_spec, _, _ = spectrum(d['dq'], mask)
    return dict(samples=int(mask.sum()), sample_seconds=float(d['dt'][mask].sum()),
        intervals=[[float(d['t'][a]), float(d['t'][b-1])] for a, b in runs(mask)],
        pitch_mean_deg=float(np.degrees(d['pitch'][mask]).mean()), pitch_std_deg=float(np.degrees(d['pitch'][mask]).std()),
        roll_mean_deg=float(np.degrees(d['roll'][mask]).mean()), yaw_rate_mean_dps=float(np.degrees(d['yaw_rate'][mask]).mean()),
        yaw_quat_rate_dps=float(np.degrees(yaw_change)/span) if span else None,
        yaw_rate_rms_dps=float(rms(np.degrees(d['yaw_rate'][mask]))),
        x_error_mean_m=float(d['x_error'][mask].mean()), x_clip_fraction=float((abs(d['x_error'][mask]) >= .3-1e-6).mean()),
        q_mean_deg=np.degrees(d['q'][mask]).mean(0).tolist(), dq_std_rads=d['dq'][mask].std(0).tolist(),
        q_hp3_rms_deg=np.degrees(highpass_rms(d['q_unwrapped'], mask)).tolist(), dq_hp3_rms_rads=highpass_rms(d['dq'], mask).tolist(),
        tau_mean_nm=d['tau'][mask].mean(0).tolist(), tau_std_nm=d['tau'][mask].std(0).tolist(),
        tau_hp3_rms_nm=highpass_rms(d['tau'], mask).tolist(), tau_maxabs_nm=abs(d['tau'][mask]).max(0).tolist(),
        torque_clip_fraction=(abs(d['tau'][mask]) >= cap-1e-6).mean(0).tolist(),
        target_injected_step_rms_nm=rms(injected[pair]).tolist(),
        raw_action_delta_rms=rms(raw_delta[pair]).tolist(), applied_action_delta_rms=rms(applied_delta[pair]).tolist(),
        raw_action_delta_lag1=raw_lag1,
        actual_update_step_rms_nm=rms(step[good]).tolist(),
        sdk_reported_mean_nm=d['reported'][feedback].mean(0).tolist(),
        sdk_minus_previous_rms_nm=rms(d['reported'][feedback]-d['previous'][feedback]).tolist(),
        wheel_target_mean_rads=d['target'][mask][:, [3, 7]].mean(0).tolist(),
        wheel_velocity_mean_rads=d['dq'][mask][:, [3, 7]].mean(0).tolist(),
        wheel_torque_diff_mean_nm=float((d['tau'][mask, 7]-d['tau'][mask, 3]).mean()),
        pitch_rate_spectrum=spec, joint_velocity_spectrum=joint_spec)


def hold_metrics(d):
    out = []
    for a, b in runs(d['rl'] & d['zero']):
        duration = d['t'][b-1]-d['t'][a]
        if duration < 2.:
            continue
        start = a+np.searchsorted(d['t'][a:b]-d['t'][a], 1.)
        if d['t'][b-1]-d['t'][start] < .5:
            continue
        tail = max(start, int(np.searchsorted(d['t'], d['t'][b-1]-5.)))
        span = d['t'][b-1]-d['t'][start]
        yaw = np.degrees(d['yaw'][b-1]-d['yaw'][start])
        last_span = d['t'][b-1]-d['t'][tail]
        post = a+np.searchsorted(d['t'][a:b]-d['t'][a], 3.)
        trend = {}
        if b-post >= 50:
            tt = d['t'][post:b]-d['t'][post]
            xx = d['s'][post:b]-d['s'][post]
            slope, intercept = np.polyfit(tt, xx, 1)
            residual = xx-(slope*tt+intercept)
            trend = dict(x_post3s_trend_mps=float(slope),
                x_post3s_oscillation_std_m=float(residual.std()),
                x_post3s_oscillation_p98_span_m=float(np.percentile(residual, 99)-np.percentile(residual, 1)))
        if duration >= 15.:
            j = int(np.searchsorted(d['t'], d['t'][b-1]-10.))
            tt = d['t'][j:b]-d['t'][j]
            xx = d['s'][j:b]-d['s'][j]
            slope, intercept = np.polyfit(tt, xx, 1)
            residual = xx-(slope*tt+intercept)
            trend.update(x_last10s_trend_mps=float(slope),
                x_last10s_oscillation_p98_span_m=float(np.percentile(residual, 99)-np.percentile(residual, 1)))
        out.append(dict(t0=float(d['t'][a]), t1=float(d['t'][b-1]), seconds=float(duration),
            settled_start=float(d['t'][start]), settled_seconds=float(span),
            x_from_hold_start_m=float(d['s'][b-1]-d['s'][a]),
            x_after_first_second_m=float(d['s'][b-1]-d['s'][start]),
            x_tail_5s_rate_mps=float((d['s'][b-1]-d['s'][tail])/last_span),
            x_error_start_end_m=[float(d['x_error'][a]), float(d['x_error'][b-1])],
            x_error_range_m=[float(d['x_error'][a:b].min()), float(d['x_error'][a:b].max())],
            yaw_settled_deg=float(yaw), yaw_settled_rate_dps=float(yaw/span),
            yaw_gyro_integral_deg=float(np.degrees(trapezoid(d['yaw_rate'][start:b], d['t'][start:b]))),
            yaw_tail_5s_rate_dps=float(np.degrees(d['yaw'][b-1]-d['yaw'][tail])/last_span), **trend))
    return out


def figures(signals, rows, output):
    fig, axes = plt.subplots(6, 4, figsize=(19, 15), sharex='col', constrained_layout=True)
    for col, (name, d) in enumerate(signals.items()):
        m = d['rl']; t = d['t'][m]
        axes[0, col].set_title(rows[name]['label']+' / '+name)
        axes[0, col].plot(t, d['cmd'][m, 0], label='vx cmd')
        axes[0, col].plot(t, d['cmd'][m, 2], label='yaw cmd')
        axes[1, col].plot(t, 100*d['x_error'][m], label='latched x error')
        axes[1, col].plot(t, 100*d['x_unclipped'][m], label='unclipped neutral travel', alpha=.7)
        axes[1, col].axhline(-30, ls=':', color='grey')
        axes[1, col].set_ylim(-50, 5)
        axes[2, col].plot(t, np.degrees(d['yaw'][m]-d['yaw'][m][0]), label='quaternion yaw')
        rate = d['yaw_rate'][m]
        gyro_yaw = np.r_[0., np.cumsum(.5*(rate[1:]+rate[:-1])*np.diff(t))]
        axes[2, col].plot(t, np.degrees(gyro_yaw), label='gyro integral', alpha=.7)
        axes[3, col].plot(t, np.degrees(d['pitch'][m]), label='pitch')
        for j, label in [(2, 'L knee'), (6, 'R knee')]:
            axes[4, col].plot(t, d['tau'][m, j], label=label, lw=.6)
            axes[5, col].plot(t, d['dq'][m, j], label=label, lw=.6)
        for ax in axes[:, col]:
            for a, b in runs(d['settled']):
                ax.axvspan(d['t'][a], d['t'][b-1], color='green', alpha=.07)
            ax.grid(alpha=.2)
        axes[-1, col].set_xlabel('Seconds since RL entry')
    for row, ylabel in enumerate(('Command [m/s, rad/s]', 'Encoder proxy [cm]', 'Yaw [deg]',
        'Pitch [deg]', 'Command knee torque [Nm]', 'Knee speed [rad/s]')):
        axes[row, 0].set_ylabel(ylabel)
        axes[row, 0].legend(fontsize=7, loc='best')
    fig.suptitle('Four hardware runs; green = settled zero command; command profiles differ')
    fig.savefig(output/'overview.png', dpi=150)
    fig.savefig(output/'overview.pdf')
    plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4), constrained_layout=True)
    for name, d in signals.items():
        for ax, x, scale in [(axes[0], d['dq'][:, [2, 6]], 1),
                (axes[1], d['tau'][:, [2, 6]], 1), (axes[2], np.degrees(d['gyro'][:, 1]), 1)]:
            _, freq, power = spectrum(x, d['settled'])
            if power is not None:
                ax.semilogy(freq, power.mean(1)*scale, label=rows[name]['label'])
    for ax, title in zip(axes, ('Knee speed PSD [(rad/s)^2/Hz]', 'Command knee torque PSD [Nm^2/Hz]', 'Pitch-rate PSD [(deg/s)^2/Hz]')):
        ax.set_title(title); ax.set_xlim(.3, 25); ax.set_xlabel('Frequency [Hz]'); ax.grid(alpha=.2); ax.legend()
    fig.savefig(output/'neutral_psd.png', dpi=160)
    fig.savefig(output/'neutral_psd.pdf')
    plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(16, 3.8), constrained_layout=True)
    for ax, key, title in zip(axes, ('q_hp3_rms_deg', 'tau_hp3_rms_nm', 'tau_mean_nm'),
        ('Joint vibration >3 Hz [deg RMS]', 'Command torque >3 Hz [Nm RMS]', 'Mean command torque [Nm]')):
        values = np.array([rows[n]['phases']['settled_zero'][key] for n in signals])[:, LEGS]
        im = ax.imshow(values, aspect='auto', cmap='viridis' if key != 'tau_mean_nm' else 'coolwarm')
        ax.set_xticks(range(6), [NAMES[j] for j in LEGS], rotation=35, ha='right')
        ax.set_yticks(range(4), [rows[n]['label'] for n in signals]); ax.set_title(title)
        for i in range(4):
            for j in range(6): ax.text(j, i, f'{values[i,j]:.2f}', ha='center', va='center', fontsize=8, color='white')
        fig.colorbar(im, ax=ax, shrink=.7)
    fig.savefig(output/'joint_metrics.png', dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT/'docs/exp/2026-10-19/sphere_hardware_review')
    args = parser.parse_args(); output = args.root.resolve()
    specs = json.loads((ROOT/'test/sim2real/sphere_candidates/specs.json').read_text())
    cases, signals = {}, {}
    for spec in specs:
        name = spec['bundle']; bundle = ROOT/'sim2real/tita_ws/src/tita_controller/policies'/name
        cfg = json.loads((bundle/'config.json').read_text())
        assert digest(bundle/'policy.onnx') == spec['onnx_sha256']
        assert cfg['policy_interface']['checkpoint_sha256'] == spec['checkpoint_sha256']
        bag, = (output/'raw').glob(name+'_*_bag')
        summary = bag.with_name(bag.name[:-4]+'_summary.md').read_text()
        assert spec['checkpoint_sha256'] in summary and spec['onnx_sha256'] in summary and digest(bundle/'config.json') in summary
        d = load(bag, cfg)
        opts = ort.SessionOptions(); opts.intra_op_num_threads = opts.inter_op_num_threads = 1
        actor = ort.InferenceSession(str(bundle/'policy.onnx'), sess_options=opts, providers=['CPUExecutionProvider'])
        predictions = np.array([actor.run(None, {actor.get_inputs()[0].name: obs[None].astype(np.float32)})[0][0] for obs in d['obs'][d['rl']]])
        error = float(abs(predictions-d['raw'][d['rl']]).max()); assert error < 1e-5
        d['quality']['max_recorded_onnx_replay_error'] = error
        phases = {phase: phase_metrics(d, mask, cfg) for phase, mask in dict(rl=d['rl'],
            startup=d['rl'] & (d['t'] < 3), settled_zero=d['settled'], common_neutral_3to13=d['common'],
            late_neutral_10s=d['late_zero']).items()}
        cases[name] = {**spec, 'config_sha256': digest(bundle/'config.json'), 'bag': str(bag), 'quality': d['quality'],
            'rl_seconds': float(d['t'][d['rl']][-1]), 'zero_fraction': float(d['zero'][d['rl']].mean()),
            'command_min': d['cmd'][d['rl']].min(0).tolist(), 'command_max': d['cmd'][d['rl']].max(0).tolist(),
            'holds': hold_metrics(d), 'phases': phases,
            'states': [dict(t=float(d['t'][i]), state=str(d['state'][i]))
                for i in np.flatnonzero(np.r_[True, d['state'][1:] != d['state'][:-1]])]}
        np.savez_compressed(output/(name+'_signals.npz'), **{k: v for k, v in d.items() if isinstance(v, np.ndarray)})
        signals[name] = d
        print(name, json.dumps(dict(seconds=cases[name]['rl_seconds'], zero_fraction=cases[name]['zero_fraction'],
            yaw_rate_dps=phases['settled_zero']['yaw_rate_mean_dps'], pitch_mean=phases['settled_zero']['pitch_mean_deg'],
            pitch_std=phases['settled_zero']['pitch_std_deg'], holds=cases[name]['holds']), ensure_ascii=False), flush=True)
    result = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
        operator_annotation='No hand disturbances; stick command profiles differ. Not a randomized paired trial.', cases=cases,
        limitations=['Encoder/IMU wheel travel is a rolling proxy, not externally measured world x.',
            'Quaternion yaw and gyro agree only to the degree shown; no external heading ground truth.',
            '50 Hz logged snapshots alias motion above 25 Hz; injected update steps are not full 500 Hz torque RMS.',
            'SDK-reported Nm is not calibrated force; transport success is not motor actuation acknowledgement.',
            'Different initial states and command histories prevent a causal isolated filter/checkpoint comparison.'])
    (output/'metrics.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    with (output/'joint_metrics.csv').open('w') as f:
        writer = csv.writer(f); writer.writerow(['bundle', 'phase', 'joint', 'mean_q_deg', 'hp3_q_deg_rms', 'dq_std_rads',
            'mean_command_nm', 'command_std_nm', 'hp3_command_nm_rms', 'sdk_mean_nm', 'update_step_nm_rms'])
        for name, case in cases.items():
            for phase, m in case['phases'].items():
                for j, joint in enumerate(NAMES):
                    writer.writerow([name, phase, joint, *[m[k][j] for k in ('q_mean_deg', 'q_hp3_rms_deg', 'dq_std_rads',
                        'tau_mean_nm', 'tau_std_nm', 'tau_hp3_rms_nm', 'sdk_reported_mean_nm', 'actual_update_step_rms_nm')]])
    figures(signals, cases, output)
    associations = []
    for name, d in signals.items():
        a, b = max(runs(d['settled']), key=lambda interval: interval[1]-interval[0])
        freq, value = coherence(d['tau'][a:b][:, [3, 7]].mean(1), d['gyro'][a:b, 1],
            fs=50, nperseg=min(512, b-a))
        peak = cases[name]['phases']['settled_zero']['pitch_rate_spectrum']['peak_hz_0p3to24p9'][0]
        index = abs(freq-peak).argmin()
        associations.append(dict(bundle=name, interval=[float(d['t'][a]), float(d['t'][b-1])],
            freq_hz=float(freq[index]), wheel_common_torque_vs_pitch_rate_coherence=float(value[index])))
    (output/'coherence_check.json').write_text(json.dumps(dict(execution_domain='DESKTOP_DRY_RUN',
        evidence_status='PASS', method='Welch coherence, fs50, nperseg512 on longest settled neutral segment; association only',
        cases=associations), indent=2)+'\n')
    (output/'analysis_source.sha256').write_text(digest(Path(__file__))+'  test/sim2real/analyze_sphere_hardware_runs.py\n')


if __name__ == '__main__':
    main()
