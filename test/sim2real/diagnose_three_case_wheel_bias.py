"""DESKTOP_DRY_RUN: three labelled bias-OFF runs plus earlier bias-ON evidence.

No ROS node, hardware command or closed-loop counterfactual simulation is used.
Command ablations keep recorded sensors/history fixed for one policy evaluation.
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
import onnxruntime as ort
from rclpy.serialization import deserialize_message
from tita_controller.msg import TrainingSample

from analyze_free_drift_baseline import PACKAGE, REPO, digest, stats


def load(bag):
    db = next(bag.glob('*.db3'))
    before = digest(db)
    with sqlite3.connect(f'file:{db}?mode=ro', uri=True) as conn:
        assert conn.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        topic = conn.execute("SELECT id FROM topics WHERE name='/sim2real/training_sample'").fetchone()
        frames = [deserialize_message(row[0], TrainingSample) for row in conn.execute(
            'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', topic)]
    get = lambda key: np.array([getattr(f, key) for f in frames])
    mono = get('monotonic_ns').astype(np.int64)
    seq = get('sequence_id').astype(np.int64)
    assert np.all(np.diff(mono) > 0) and np.all(np.diff(seq) == 1)
    rl = get('state') == 'rl'
    assert np.count_nonzero(rl & ~np.r_[False, rl[:-1]]) == 1
    result = dict(t=(mono-mono[rl][0])*1e-9, dt=np.r_[.02, np.diff(mono)*1e-9], rl=rl)
    for name, key in dict(q='joint_position', dq='joint_velocity', quat='quaternion_wxyz',
            gyro='angular_velocity', command='command', action='action_raw', teacher='teacher_action',
            torque='computed_torque', offsets='wheel_velocity_bias', diag='velocity_bias_diagnostics').items():
        result[name] = get(key)
        assert np.isfinite(result[name]).all()
    result['obs'] = np.zeros((len(frames), 33), dtype=np.float32)
    result['obs'][rl] = np.array([f.observation for f in frames if f.state == 'rl'], dtype=np.float32)
    for key in ('sensors_valid', 'policy_valid', 'output_enabled', 'torque_sent', 'teacher_action_valid'):
        assert get(key)[rl].all(), key
    w, x, y, z = result['quat'].T
    result['pitch'] = np.degrees(np.arcsin(np.clip(2*(w*y-z*x), -1, 1)))
    result['wheel_proxy'] = .0925*result['dq'][:, [3, 7]].mean(axis=1)
    result['source_db'] = str(db.relative_to(REPO))
    result['source_db_sha256'] = before
    assert digest(db) == before
    return result


def targets(actions, cfg):
    native = [f'joint_{side}_leg_{i}' for side in ('left', 'right') for i in range(1, 5)]
    result = np.zeros_like(actions, dtype=float)
    for i, a in enumerate(cfg['policy_interface']['actions']):
        j = native.index(a['joint'])
        result[:, j] = actions[:, i]*float(a['scale'])+float(a['offset'])
        if a['clip']:
            result[:, j] = np.clip(result[:, j], *a['clip'])
    return result


def torques(target, data, cfg, corrected=False):
    target = target.copy()
    if corrected:
        target[:, [3, 7]] += data['offsets']
    kp, kd = np.array(cfg['robot']['joint_kp']), np.array(cfg['robot']['joint_kd'])
    result = kp*(target-data['q'])-kd*data['dq']
    result[:, [3, 7]] = kd[[3, 7]]*(target[:, [3, 7]]-data['dq'][:, [3, 7]])
    limit = np.array(cfg['robot']['torque_limit'])
    return np.clip(result, -limit, limit)


def common(values):
    return values[:, [3, 7]].mean(axis=1)


def summarize(d, mask):
    if mask.sum() < 2:
        return dict(samples=int(mask.sum()))
    return dict(samples=int(mask.sum()), start_s=float(d['t'][mask][0]), end_s=float(d['t'][mask][-1]),
        **{key: stats(value[mask]) for key, value in dict(command_x=d['command'][:, 0],
            command_yaw=d['command'][:, 2], fk_velocity_m_s=d['velocity'], wheel_proxy_m_s=d['wheel_proxy'],
            pitch_deg=d['pitch'], policy_wheel_target_proxy_m_s=.0925*common(d['target']),
            baseline_torque_nm=common(d['base']), final_torque_nm=common(d['torque']),
            added_torque_nm=common(d['torque']-d['base']), bias_m_s=d['diag'][:, 6]).items()})


def blocks(mask):
    ind = np.flatnonzero(mask)
    return np.split(ind, np.flatnonzero(np.diff(ind) > 1)+1) if len(ind) else []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    day = REPO/'docs/exp/2026-10-17'
    paths = dict(
        free=day/'flashsac_141113_free_drift_review/flashsac_60000_141113_460666182_output_true_bag',
        hand=day/'flashsac_141605_hand_blocked_review/flashsac_60000_141605_080644640_output_true_bag',
        joystick=out/'flashsac_60000_141821_088426888_output_true_bag',
        bias_on=day/'flashsac_bias_oscillation_review/flashsac_60000_133338_353802215_output_true_bag')
    data = {name: load(path) for name, path in paths.items()}
    cfg_path = PACKAGE/'policies/flashsac_60000/config.json'
    geo_path = PACKAGE/'config/velocity_bias_geometry.json'
    cfg, geo = [json.loads(p.read_text()) for p in (cfg_path, geo_path)]
    onnx = PACKAGE/'policies/flashsac_60000/policy.onnx'
    assert digest(onnx) == cfg['policy_interface']['onnx_sha256']
    native = [f'joint_{side}_leg_{i}' for side in ('left', 'right') for i in range(1, 5)]
    terms = []
    for a in cfg['policy_interface']['actions']:
        terms.extend([native.index(a['joint']), int(a['kind'] == 'velocity'), a['scale'], a['offset'], *(a['clip'] or [-1e9, 1e9])])
    header = [*geo['xyz'], *geo['rpy'], *geo['axis'], geo['wheel_radius'], 1.,
        *cfg['robot']['joint_kp'], *cfg['robot']['joint_kd'], *cfg['robot']['torque_limit'], *terms]
    options = ort.SessionOptions()
    options.intra_op_num_threads = options.inter_op_num_threads = 1
    session = ort.InferenceSession(str(onnx), sess_options=options, providers=['CPUExecutionProvider'])
    infer = lambda obs: session.run(None, {session.get_inputs()[0].name: obs[None].astype(np.float32)})[0][0]
    report = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='SUSPICIOUS',
        checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'], onnx_sha256=digest(onnx),
        config_sha256=digest(cfg_path), initial_exclusion_s=5., cases={})
    with tempfile.TemporaryDirectory(dir=REPO/'test/sim2real', prefix='three_case_') as temp:
        binary = Path(temp)/'runtime'
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
            '-I/usr/include/eigen3', '-I', str(PACKAGE/'include'),
            str(REPO/'test/sim2real/velocity_bias_runtime.cpp'), '-o', str(binary)], check=True)
        for name, d in data.items():
            rl, t = d['rl'], d['t']
            runtime_dt = d['dt'].copy()
            runtime_dt[np.flatnonzero(rl)[0]] = .02  # Node's first bias update uses .02, independent of last non-RL snapshot.
            # Force zero command ONLY inside a passive math replay to keep the observer running during joystick motion.
            rows = np.c_[rl, runtime_dt, np.zeros_like(d['command']), d['q'], d['dq'], d['quat'], d['gyro'], d['action']]
            stream = io.StringIO()
            np.savetxt(stream, np.array(header)[None], fmt='%.17g')
            np.savetxt(stream, rows, fmt='%.17g')
            process = subprocess.run([str(binary), 'on'], input=stream.getvalue(), capture_output=True, text=True, check=True)
            replay = np.loadtxt(io.StringIO(process.stdout), ndmin=2)
            assert replay.shape == (len(t), 25)
            d['velocity'] = replay[:, 3]
            d['target'] = targets(d['action'].astype(float), cfg)
            d['base'] = torques(d['target'], d, cfg)
            rebuilt = torques(d['target'], d, cfg, corrected=True)
            error = float(abs(rebuilt[rl]-d['torque'][rl]).max())
            assert error < 1e-4
            predictions = np.array([infer(row) for row in d['obs'][rl]])
            infer_error = float(abs(predictions-d['action'][rl]).max())
            assert infer_error < 2e-5
            obs_cmd_error = float(abs(d['obs'][rl, 6:9]-d['command'][rl]*[2., 2., .25]).max())
            assert obs_cmd_error < 1e-6
            if name != 'bias_on':
                assert abs(d['offsets'][rl]).max() == 0. and abs(d['teacher'][rl]-d['action'][rl]).max() == 0.
            summary = dict(source_db=d['source_db'], source_db_sha256=d['source_db_sha256'],
                total_frames=len(t), rl_frames=int(rl.sum()), last_rl_sample_s=float(t[rl][-1]),
                rl_dt_s=stats(d['dt'][rl]), rl_dt_over_30ms=int((d['dt'][rl] > .03).sum()),
                command_abs_max=abs(d['command'][rl]).max(axis=0).tolist(),
                bias_offset_abs_max=float(abs(d['offsets'][rl]).max()),
                torque_reconstruction_error_nm=error, onnx_replay_error=infer_error, obs_command_error=obs_cmd_error,
                common_5_10=summarize(d, rl & (t >= 5) & (t < 10)),
                post_initial=summarize(d, rl & (t >= 5) & (t < min(65, t[rl][-1]-1))),
                five_second_windows=[dict(window_start=float(lo), **summarize(d, rl & (t >= lo) & (t < lo+5)))
                                     for lo in np.arange(5., t[rl][-1]-1., 5.)])
            # Conditional one-step command effect: same sensors AND recorded raw-action history.
            if name == 'joystick':
                counter_obs = d['obs'].copy()
                counter_obs[:, 6:9] = 0.
                counter_action = d['action'].astype(float).copy()
                counter_action[rl] = np.array([infer(row) for row in counter_obs[rl]])
                counter_target = targets(counter_action, cfg)
                counter_torque = torques(counter_target, d, cfg)
                d['counter_torque'] = counter_torque
                d['counter_target'] = counter_target
                delta = d['base']-counter_torque
                d['command_torque_delta'] = common(delta)
                d['command_action_delta'] = d['action']-counter_action
                keep = rl & (t >= 5) & (t < 65)
                summary['same_state_command_ablation'] = dict(samples=int(keep.sum()),
                    mean_torque_delta_nm=delta[keep].mean(axis=0).tolist(),
                    mean_target_delta=(d['target'][keep]-counter_target[keep]).mean(axis=0).tolist(),
                    common_wheel_delta_nm=stats(common(delta)[keep]),
                    common_wheel_target_delta_m_s=stats(.0925*common(d['target']-counter_target)[keep]),
                    limitation='Single policy evaluation with recorded history held fixed; not zero-command robot trajectory.')
                windows = []
                for lo in np.arange(5., 65., 2.):
                    mask = rl & (t >= lo) & (t < lo+2)
                    if mask.sum() < 90:
                        continue
                    entry = dict(window_start=float(lo), **summarize(d, mask))
                    entry['near_zero_proxy'] = bool(abs(d['velocity'][mask]).mean() < .03)
                    entry['command_range_x'] = float(np.ptp(d['command'][mask, 0]))
                    windows.append(entry)
                summary['two_second_windows'] = windows
                summary['near_zero_window_starts'] = [w['window_start'] for w in windows if w['near_zero_proxy']]
                summary['representative_intervals'] = {}
                for label, lo, hi in [('adjusted_10_65', 10, 65), ('low_yaw_example_25_30', 25, 30),
                                     ('command_release_68_69', 68, 69)]:
                    mask = rl & (t >= lo) & (t < hi)
                    summary['representative_intervals'][label] = dict(**summarize(d, mask),
                        same_state_common_wheel_delta_nm=stats(common(delta)[mask]),
                        same_state_target_delta=(d['target'][mask]-counter_target[mask]).mean(axis=0).tolist(),
                        same_state_torque_delta_nm=delta[mask].mean(axis=0).tolist())
            if name == 'bias_on':
                active = rl & (d['diag'][:, 1] > .5)
                diag_error = float(abs(d['velocity'][active]-d['diag'][active, 3]).max())
                assert diag_error < 1e-5
                consecutive = active & np.r_[False, active[:-1]]
                predicted_i = np.r_[0., d['diag'][:-1, 5]]+4*d['diag'][:, 4]*runtime_dt
                integral_error = float(abs(predicted_i[consecutive]-d['diag'][consecutive, 5]).max())
                assert integral_error < 1e-5
                summary['observer_active_error_m_s'] = diag_error
                summary['integrator_step_error_m_s'] = integral_error
                episodes = []
                for ind in blocks(active):
                    if t[ind[-1]]-t[ind[0]] < 5:
                        continue
                    first, last = ind[0], ind[-1]
                    settled = active & (t >= t[first]+2) & (t < t[last]-1)
                    seed = 3*float(d['diag'][first, 3])
                    episodes.append(dict(onset_s=float(t[first]), end_s=float(t[last]),
                        seed_m_s=seed, initial_integral_m_s=float(d['diag'][first, 5]),
                        initial_velocity_m_s=float(d['diag'][first, 3]),
                        seed_equivalent_nm_per_wheel=.5*seed/.0925,
                        retained_integral_mean_m_s=float(d['diag'][settled, 5].mean()),
                        accumulated_after_seed_mean_m_s=float(d['diag'][settled, 5].mean()-seed),
                        seed_to_settled_abs_ratio=float(abs(seed)/abs(d['diag'][settled, 5].mean())),
                        settled=summarize(d, settled)))
                summary['episodes'] = episodes
                summary['max_abs_pitch_deg'] = float(abs(d['pitch'][rl]).max())
                summary['max_abs_bias_m_s'] = float(abs(d['diag'][rl, 6]).max())
                summary['wheel_saturation_fraction'] = (abs(d['torque'][rl][:, [3, 7]]) >= 12.-1e-5).mean(axis=0).tolist()
            report['cases'][name] = summary
            arrays = {k: v for k, v in d.items() if isinstance(v, np.ndarray)}
            np.savez_compressed(out/f'{name}_signals.npz', **arrays)
            print(name, 'frames', int(rl.sum()), 'torque error', error, 'ONNX error', infer_error, flush=True)
    report['conversion'] = dict(wheel_kd=.5, radius_m=.0925, nm_per_m_s=.5/.0925,
        bias_limit_m_s=2., equivalent_limit_nm_per_wheel=2*.5/.0925,
        seed_gain=3., integral_gain=4., slew_m_s2=3., equivalent_nm_s_per_wheel=3*.5/.0925,
        pitch_absolute_gate_deg=float(np.degrees(.3)))
    report['sources'] = {str(p.relative_to(REPO)): digest(p) for p in (cfg_path, geo_path, onnx,
        PACKAGE/'include/tita_controller/velocity_bias.hpp', PACKAGE/'include/tita_controller/adapter.hpp',
        PACKAGE/'src/tita_node.cpp', Path(__file__))}
    report['limitations'] = ['Separate operator-controlled runs; no independent chassis velocity or hand force.',
        'Near-zero windows are selected by the estimated velocity proxy, not measured physical standstill.',
        'Retained integral explains offset mathematically; exact plant cause of equilibrium change/8 Hz oscillation is not identified.',
        'No modified controller, hardware deployment or predicted closed-loop benefit.']
    (out/'metrics.json').write_text(json.dumps(report, indent=2)+'\n')
    fig, axes = plt.subplots(4, 3, figsize=(17, 12), sharex='col', constrained_layout=True)
    for col, name in enumerate(('free', 'hand', 'joystick')):
        d = data[name]
        keep = d['rl'] & (d['t'] >= 5) & (d['t'] < (10 if name == 'free' else 20 if name == 'hand' else 65))
        for row, values, label in [(0, d['command'][:, 0], 'Command x (m/s)'),
                (1, d['velocity'], 'FK speed (m/s)'), (2, d['pitch'], 'Pitch (deg)'),
                (3, common(d['torque']), 'Computed Nm / wheel')]:
            axes[row, col].plot(d['t'][keep], values[keep], lw=.8)
            axes[row, col].set_ylabel(label)
            axes[row, col].grid(alpha=.2)
        axes[0, col].set_title(name)
        axes[-1, col].set_xlabel('Seconds from RL entry; first 5 s excluded')
    fig.suptitle('FlashSAC bias OFF: three operator-labelled conditions\nSpeed is an encoder/IMU estimate; torque is a computed command')
    fig.savefig(out/'three_cases.png', dpi=150)
    plt.close(fig)
    labels, base, added, final, pitch = [], [], [], [], []
    for name, mask in [('Free\n5–10 s', data['free']['rl'] & (data['free']['t'] >= 5) & (data['free']['t'] < 10)),
                       ('Hand\n5–10 s', data['hand']['rl'] & (data['hand']['t'] >= 5) & (data['hand']['t'] < 10)),
                       ('Joystick\n25–30 s', data['joystick']['rl'] & (data['joystick']['t'] >= 25) & (data['joystick']['t'] < 30))]:
        key = 'joystick' if name.startswith('Joystick') else 'hand' if name.startswith('Hand') else 'free'
        values = summarize(data[key], mask)
        labels.append(name)
        base.append(values['baseline_torque_nm']['mean'])
        added.append(values['added_torque_nm']['mean'])
        final.append(values['final_torque_nm']['mean'])
        pitch.append(values['pitch_deg']['mean'])
    for i, episode in enumerate(report['cases']['bias_on']['episodes']):
        values = episode['settled']
        labels.append(f'Bias ON\nepisode {i+1}')
        base.append(values['baseline_torque_nm']['mean'])
        added.append(values['added_torque_nm']['mean'])
        final.append(values['final_torque_nm']['mean'])
        pitch.append(values['pitch_deg']['mean'])
    x = np.arange(len(labels))
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), constrained_layout=True)
    for offset, values, label in [(-.25, base, 'Policy/PD at recorded state'), (0, added, 'Additional wheel bias'),
                                  (.25, final, 'Final CAN torque command')]:
        axes[0].bar(x+offset, values, .25, label=label)
    axes[0].axhline(0, color='black', lw=.8)
    axes[0].set_ylabel('Mean Nm per wheel')
    axes[0].set_xticks(x, labels)
    axes[0].legend(fontsize=8)
    axes[1].bar(x, pitch, color='tab:purple', width=.55)
    axes[1].set_ylabel('Mean pitch (degrees)')
    axes[1].set_xticks(x, labels)
    for axis in axes:
        axis.grid(axis='y', alpha=.2)
    fig.suptitle('Large wheel-bias offset is cancelled by the policy/PD response\nSeparate recorded conditions; not a matched causal A/B test')
    fig.savefig(out/'torque_cancellation.png', dpi=160)
    plt.close(fig)


if __name__ == '__main__':
    main()
