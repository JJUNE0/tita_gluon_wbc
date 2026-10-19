"""DESKTOP_DRY_RUN: read-only OFF/MA2/notch telemetry comparison; no robot commands."""
import argparse
import json
from pathlib import Path
import sqlite3

import numpy as np
from scipy.signal import iirnotch, lfilter, lfilter_zi, welch
from rclpy.serialization import deserialize_message
from tita_controller.msg import ActionFilterSample, TrainingSample
import analyze_leg_filter_real as prior
import analyze_pd_vibration as pd

ROOT = Path(__file__).resolve().parents[2]


def load(path, cfg, mode):
    d = pd.load(path, cfg['policy_interface']['actions'])
    with sqlite3.connect(f"file:{d['db']}?mode=ro", uri=True) as conn:
        topics = dict(conn.execute('SELECT name,id FROM topics'))
        def rows(topic, cls):
            return [deserialize_message(b, cls) for b, in conn.execute(
                'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', (topics[topic],))]
        samples = rows('/sim2real/training_sample', TrainingSample)
        filters = rows('/sim2real/action_filter_sample', ActionFilterSample) if mode != 'none' else []
    get = lambda name: np.array([getattr(s, name) for s in samples])
    table = {(f.sequence_id, f.monotonic_ns): f for f in filters}
    assert len(table) == len(filters)
    rl = d['state'] == 'rl'
    d['rl'] = rl
    assert rl.any()
    for field in ('sensors_valid', 'policy_valid', 'output_enabled', 'torque_sent'):
        assert get(field)[rl].all(), field
    assert (np.diff(get('sequence_id').astype(np.int64)) == 1).all()
    assert not d['bias'][rl].any()
    d['applied'] = d['action'].copy()
    for i, s in enumerate(samples):
        if mode == 'none':
            continue
        f = table.get((s.sequence_id, s.monotonic_ns))
        assert f is not None, 'missing applied frame'
        assert f.control_tick == s.control_tick and f.leg_action_filter == mode
        d['applied'][i] = f.action_applied
    legs = [i for i, term in enumerate(cfg['policy_interface']['actions'])
            if pd.JOINTS.index(term['joint']) not in (3, 7)]
    raw = d['action'].astype(np.float32)
    expected = raw.copy()
    for a, b in pd.runs(rl):
        if mode == 'none':
            continue
        expected[a+1:b, legs] = .5 * raw[a+1:b, legs] + .5 * raw[a:b-1, legs]
        if mode == 'ma2_notch_legs':
            num, den = iirnotch(8.3, 3., fs=50.)
            for j in legs:
                x = expected[a:b, j].copy()
                expected[a:b, j] = lfilter(num, den, x, zi=lfilter_zi(num, den)*x[0])[0]
    d['replay_error'] = float(abs(expected[rl] - d['applied'][rl]).max())
    assert d['replay_error'] < 2e-6
    d['teacher_error'] = float(abs(get('teacher_action')[rl] - d['applied'][rl]).max())
    assert d['teacher_error'] < 1e-6
    for i, term in enumerate(cfg['policy_interface']['actions']):
        j = pd.JOINTS.index(term['joint'])
        d['target'][:, j] = np.clip(d['applied'][:, i]*term['scale']+term['offset'], *term['clip'])
    kp, kd, limits = [np.array(cfg['robot'][k]) for k in ('joint_kp', 'joint_kd', 'torque_limit')]
    rebuilt = kp*(d['target']-d['q']) - kd*d['dq']
    rebuilt[:, [3, 7]] = kd[[3, 7]]*(d['target'][:, [3, 7]]-d['dq'][:, [3, 7]])
    rebuilt = np.clip(rebuilt, -limits, limits)
    d['torque_error'] = float(abs(rebuilt[rl] - d['tau'][rl]).max())
    assert d['torque_error'] < 1e-8
    w, x, y, z = get('quaternion_wxyz').T
    d['pitch'] = np.degrees(np.arcsin(np.clip(2*(w*y-z*x), -1, 1)))
    d['roll'] = np.degrees(np.arctan2(2*(w*x+y*z), 1-2*(x*x+y*y)))
    d['t'] = (d['mono'] - d['mono'][rl][0])*1e-9
    d['dt'] = np.r_[.02, np.diff(d['mono'])*1e-9]
    d['pair'] = np.r_[False, rl[1:] & rl[:-1] & (np.diff(d['tick']) == 10)]
    d['neutral'] = np.zeros(len(rl), bool)
    neutral = (abs(d['command']) <= [.02, .02, .03]).all(1)
    for a, b in pd.runs(rl & neutral):
        d['neutral'][a:b] = (d['t'][a:b] - d['t'][a]) >= 3.
    return d


def spectrum(x, segments, nperseg):
    psd, count, freq = 0., 0, None
    for a, b in segments:
        if b-a < nperseg:
            continue
        freq, p = welch(x[a:b], fs=50., nperseg=nperseg, axis=0)
        psd += p*(b-a)
        count += b-a
    if not count:
        return {}
    psd /= count
    df = freq[1]-freq[0]
    return {'nperseg': nperseg, 'resolution_hz': df, 'frequency_hz': freq.tolist(), 'psd': psd.tolist(),
            'peak_hz': freq[freq >= 1][np.argmax(psd[freq >= 1], axis=0)].tolist(),
            'band_rms': {f'{lo}-{hi}': np.sqrt(psd[(freq >= lo) & (freq < hi)].sum(0)*df).tolist()
                         for lo, hi in ((1, 5), (5, 7), (7, 10), (10, 15), (15, 25))}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    cfg_path = pd.INTERFACE
    cfg = json.loads(cfg_path.read_text())
    assert pd.digest(cfg_path) == 'a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719'
    base = ROOT/'docs/exp/2026-10-18'
    paths = {
        'off': ('none', base/'flashsac_knee92_bias_pair/flashsac_80000_125618_839843723_output_true_bag'),
        'ma2': ('ma2_legs', base/'leg_action_filter_real_review/flashsac_80000_135923_560039455_output_true_bag'),
        'notch': ('ma2_notch_legs', base/'flashsac_80000_150320_869838811_output_true_bag')}
    signals = {key: load(path, cfg, mode) for key, (mode, path) in paths.items()}
    # Restrict to the common initial neutral interval before any stick command.
    ends = []
    for d in signals.values():
        moving = d['rl'] & (abs(d['command']) > [.02, .02, .03]).any(1)
        ends.append(float(d['t'][moving][0]) if moving.any() else float(d['t'][d['rl']][-1]))
    end = min(ends)
    assert end > 3.
    cases = {}
    for key, d in signals.items():
        masks = {'initial_common': d['neutral'] & (d['t'] < end), 'neutral_all': d['neutral']}
        windows = {}
        for name, mask in masks.items():
            assert mask.any(), name
            result = prior.metrics(d, mask, cfg)
            segments = pd.runs(mask)
            result['pitch_rate_std_rad_s'] = float(d['gyro'][mask, 1].std())
            result['joint_velocity_std_rad_s'] = d['dq'][mask].std(0).tolist()
            result['spectra'] = {signal_name: spectrum(value, segments, 64 if name == 'initial_common' else 128)
                                for signal_name, value in
                                 (('pitch', d['pitch'][:, None]), ('gyro', d['gyro']),
                                  ('dq', d['dq']), ('tau', d['tau']), ('raw', d['action']),
                                  ('applied', d['applied']))}
            windows[name] = result
        cases[key] = {'source_db': d['db'], 'source_db_sha256': d['db_sha256'],
                      'rl_samples': int(d['rl'].sum()), 'rl_max_dt_s': float(d['dt'][d['rl']].max()),
                      'replay_error': d['replay_error'], 'teacher_error': d['teacher_error'],
                      'torque_error': d['torque_error'], 'fitted_gains': pd.fit_gains(d, d['rl']),
                      'neutral_blocks_s': [[float(d['t'][a]), float(d['t'][b-1])]
                                           for a, b in pd.runs(d['neutral'])], 'windows': windows}
    report = {'execution_domain': 'DESKTOP_DRY_RUN', 'evidence_status': 'SUSPICIOUS',
              'checkpoint_sha256': cfg['policy_interface']['checkpoint_sha256'],
              'onnx_sha256': cfg['policy_interface']['onnx_sha256'], 'config_sha256': pd.digest(cfg_path),
              'initial_common_end_s': end, 'cases': cases,
              'limitations': ['Separate operator trials; command histories/initial state differ.',
                              '50 Hz telemetry aliases above 25 Hz; wheel speed is not ground truth body speed.',
                              'Computed command is not measured force. Spectral attenuation does not identify root cause.'],
              'sources': {str(p.relative_to(ROOT)): pd.digest(p) for p in
                          (Path(__file__), Path(prior.__file__), Path(pd.__file__), cfg_path)}}
    (out/'metrics.json').write_text(json.dumps(report, indent=2)+'\n')
    fig, axes = prior.plt.subplots(4, 3, figsize=(15, 10), constrained_layout=True)
    for col, (key, d) in enumerate(signals.items()):
        mask = d['rl']
        t = d['t'][mask]
        axes[0, col].plot(t, d['command'][mask, 0], label='vx')
        axes[0, col].plot(t, d['command'][mask, 2], label='yaw')
        axes[1, col].plot(t, d['pitch'][mask], label='pitch deg')
        for j in (1, 2):
            axes[2, col].plot(t, d['dq'][mask, j], lw=.5, label=f'dq {j} rad/s')
        spec = cases[key]['windows']['initial_common']['spectra']['pitch']
        axes[3, col].semilogy(spec['frequency_hz'], np.maximum(np.array(spec['psd'])[:, 0], 1e-12))
        axes[3, col].axvline(8.3, color='r', ls=':', label='notch center')
        axes[3, col].set(xlabel='Hz', ylabel='pitch PSD deg²/Hz', xlim=(0, 25))
        axes[3, col].set_ylim(1e-7, .2)
        axes[1, col].set_ylim(-1, 12)
        axes[2, col].set_ylim(-2, 6)
        axes[0, col].set_title(key)
        for ax in axes[:, col]:
            ax.grid(alpha=.2)
            ax.legend(fontsize=7)
    fig.suptitle(f'Separate real trials; PSD common neutral 3–{end:.2f} s after RL entry')
    fig.savefig(out/'comparison.png', dpi=160)
    prior.plt.close(fig)
    fig, axes = prior.plt.subplots(3, 3, figsize=(14, 8), sharex=True, sharey='row', constrained_layout=True)
    for col, (key, d) in enumerate(signals.items()):
        mask = d['rl'] & (d['t'] >= 3.8) & (d['t'] < 4.8)
        t = d['t'][mask]
        axes[0, col].plot(t, d['pitch'][mask]-d['pitch'][mask].mean(), marker='.', ms=3)
        axes[1, col].plot(t, d['gyro'][mask, 1], marker='.', ms=3)
        axes[2, col].plot(t, d['dq'][mask, 1], marker='.', ms=3)
        axes[0, col].set_title(key)
        for row, label in enumerate(('pitch minus mean [deg]', 'pitch rate [rad/s]', 'left shoulder dq [rad/s]')):
            axes[row, col].set_ylabel(label)
            axes[row, col].grid(alpha=.2)
        axes[2, col].set_xlabel('Seconds from RL entry')
    fig.suptitle('Matched initial neutral second; shared scales; recorded 50 Hz telemetry')
    fig.savefig(out/'neutral_zoom.png', dpi=160)
    prior.plt.close(fig)
    for key, case in cases.items():
        for name, m in case['windows'].items():
            print(key, name, 'seconds', round(m['seconds'], 3), 'pitch std', round(m['pitch_std_deg'], 4),
                  'gyro std', round(m['pitch_rate_std_rad_s'], 4), 'pitch peak Hz', m['spectra']['pitch'].get('peak_hz'),
                  'knee step', np.round(np.array(m['actual_update_step_rms_nm'])[[2, 6]], 3),
                  'shoulder dq std', np.round(np.array(m['joint_velocity_std_rad_s'])[[1, 5]], 3))
    print('PASS DESKTOP_DRY_RUN: bags/joins/flags, independent filter replay, teacher, applied PD reconstruction')


if __name__ == '__main__':
    main()
