"""DESKTOP_DRY_RUN: review bias-OFF and optional ON bags for a selected policy.

Contact times are unknown. Neutral commands do not establish absence of support.
Pure C++ observer replay on recorded states is not a closed-loop counterfactual.
"""
import argparse
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import onnxruntime as ort

from diagnose_three_case_wheel_bias import load, targets, torques, common, summarize, blocks
from analyze_free_drift_baseline import PACKAGE, REPO, digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--policy-dir', type=Path, required=True)
    parser.add_argument('--off-bag', type=Path, required=True)
    parser.add_argument('--on-bag', type=Path)
    parser.add_argument('--support-annotation', choices=['unknown', 'intermittent'], default='unknown')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(REPO / 'docs/exp')
    out.mkdir(parents=True, exist_ok=True)
    bundle = args.policy_dir.resolve()
    cfg = json.loads((bundle / 'config.json').read_text())
    geo = json.loads((PACKAGE / 'config/velocity_bias_geometry.json').read_text())
    onnx_hash = digest(bundle / 'policy.onnx')
    assert onnx_hash == cfg['policy_interface']['onnx_sha256']
    native = [f'joint_{side}_leg_{i}' for side in ('left', 'right') for i in range(1, 5)]
    terms = []
    for a in cfg['policy_interface']['actions']:
        terms.extend([native.index(a['joint']), int(a['kind'] == 'velocity'),
                      a['scale'], a['offset'], *(a['clip'] or [-1e9, 1e9])])
    header = [*geo['xyz'], *geo['rpy'], *geo['axis'], geo['wheel_radius'], 1.,
              *cfg['robot']['joint_kp'], *cfg['robot']['joint_kd'], *cfg['robot']['torque_limit'], *terms]
    options = ort.SessionOptions()
    options.intra_op_num_threads = options.inter_op_num_threads = 1
    session = ort.InferenceSession(str(bundle / 'policy.onnx'), sess_options=options,
                                  providers=['CPUExecutionProvider'])
    sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
    from sim2sim_ros2_jazzy.adapter import ObservationBuilder, ObsState
    builder = ObservationBuilder(cfg)
    report = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='SUSPICIOUS',
                  checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
                  onnx_sha256=onnx_hash, config_sha256=digest(bundle / 'config.json'),
                  operator_support=('Intermittent hand contact reported; exact times unknown.'
                                    if args.support_annotation == 'intermittent'
                                    else 'Hand contact/support not yet confirmed.'),
                  limitations=['Neutral command does not establish free motion.',
                               'Velocity is an encoder/IMU/FK estimate; no external ground-truth translation.',
                               'Computed torques are not measured motor torques.',
                               'Different runs and support prevent causal improvement percentages.'], cases={})
    data = {}
    with tempfile.TemporaryDirectory(dir=REPO / 'test/sim2real', prefix='policy_drift_') as temp:
        binary = Path(temp) / 'runtime'
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
                        '-isystem', '/usr/include/eigen3', '-I', str(PACKAGE / 'include'),
                        str(REPO / 'test/sim2real/velocity_bias_runtime.cpp'), '-o', str(binary)], check=True)

        def replay(d, command):
            dt = d['dt'].copy()
            dt[np.flatnonzero(d['rl'])[0]] = .02
            rows = np.c_[d['rl'], dt, command, d['q'], d['dq'], d['quat'], d['gyro'], d['action']]
            stream = io.StringIO()
            np.savetxt(stream, np.asarray(header)[None], fmt='%.17g')
            np.savetxt(stream, rows, fmt='%.17g')
            result = subprocess.run([str(binary), 'status'], input=stream.getvalue(),
                                    capture_output=True, text=True, check=True)
            return np.loadtxt(io.StringIO(result.stdout), ndmin=2)

        cases = [('off', args.off_bag)]
        if args.on_bag is not None:
            cases.append(('on', args.on_bag))
        for name, bag in cases:
            d = load(bag.resolve())
            t, rl = d['t'], d['rl']
            summary = bag.resolve().parent / (bag.name.removesuffix('_bag') + '_summary.md')
            text = summary.read_text()
            assert cfg['policy_interface']['checkpoint_sha256'] in text and onnx_hash in text
            assert digest(bundle / 'config.json') in text
            assert f'Velocity bias enabled: {str(name == "on").lower()}' in text
            observer = replay(d, np.zeros_like(d['command']))
            # The observer is computed continuously through commands, only for evaluation.
            d['velocity'] = observer[:, 3]
            d['target'] = targets(d['action'].astype(float), cfg)
            d['base'] = torques(d['target'], d, cfg)
            rebuilt = torques(d['target'], d, cfg, corrected=True)
            torque_error = float(abs(rebuilt[rl] - d['torque'][rl]).max())
            assert torque_error < 1e-8
            added = d['torque'] - d['base']
            action_error = obs_error = 0.
            previous = np.zeros(8, dtype=np.float32)
            for i in np.flatnonzero(rl):
                actual = session.run(None, {session.get_inputs()[0].name: d['obs'][i:i+1]})[0][0]
                action_error = max(action_error, float(abs(actual - d['action'][i]).max()))
                obs = builder.build(ObsState(d['q'][i], d['dq'][i], d['quat'][i],
                                              d['gyro'][i], d['command'][i], previous))
                obs_error = max(obs_error, float(abs(obs - d['obs'][i]).max()))
                previous = d['action'][i].copy()
            assert action_error < 2e-5 and obs_error < 1e-5
            diag_error = None
            guard_events, acquisitions = [], []
            if name == 'on':
                actual = replay(d, d['command'])
                assert actual.shape == (len(t), 29)
                diag_error = abs(actual[rl, :9] - d['diag'][rl, :9]).max(axis=0).tolist()
                np.testing.assert_allclose(actual[rl, :9], d['diag'][rl, :9], atol=1e-5, rtol=1e-5)
                np.testing.assert_allclose(added[rl][:, [3, 7]], d['diag'][rl, 9:11], atol=1e-6)
                assert abs(added[rl]).max() <= .8 + 1e-8
                for ind in blocks(rl & (actual[:, 26] > .5)):
                    i = ind[0]
                    guard_events.append(dict(time_s=float(t[i]), end_s=float(t[ind[-1]]),
                                             pitch_deg=float(d['pitch'][i]),
                                             reference_deg=float(np.degrees(actual[i, 28]))))
                for ind in blocks(rl & (d['diag'][:, 1] > .5)):
                    i = ind[0]
                    acquisitions.append(dict(time_s=float(t[i]), end_s=float(t[ind[-1]]),
                                             drift_m_s=float(actual[i, 27]),
                                             reference_deg=float(np.degrees(actual[i, 28]))))
            else:
                assert abs(d['offsets'][rl]).max() == 0 and abs(d['diag'][rl]).max() == 0
            neutral = rl & (abs(d['command']) <= 1e-6).all(axis=1)
            # Exclude command entry/exit transients without claiming contact detection.
            settled_neutral = np.zeros(len(t), dtype=bool)
            for ind in blocks(neutral):
                settled_neutral[ind] = t[ind] >= t[ind[0]] + 2.

            def metrics(mask):
                value = summarize(d, mask)
                if mask.sum() >= 2:
                    value['cap_fraction'] = float((abs(common(added)[mask]) >= .7999).mean())
                    value['negative_speed_fraction'] = float((d['velocity'][mask] < 0).mean())
                return value

            windows = []
            for lo, hi in [(1., 3.), (3., 5.), (5., 10.), (10., 15.), (15., 20.), (20., 25.)]:
                mask = settled_neutral & (t >= lo) & (t < hi)
                windows.append(dict(window=[lo, hi], **metrics(mask)))
            report['cases'][name] = dict(run=bag.name, frames=len(t), rl_frames=int(rl.sum()),
                last_rl_s=float(t[rl][-1]), source_db_sha256=d['source_db_sha256'],
                action_replay_error=action_error, observation_reconstruction_error=obs_error,
                torque_reconstruction_error_nm=torque_error, diag_replay_errors=diag_error,
                max_added_nm=float(abs(added[rl]).max()), acquisitions=acquisitions,
                guard_events=guard_events, neutral_after_5s=metrics(settled_neutral & (t >= 5.)),
                neutral_after_5s_trimmed=metrics(settled_neutral & (t >= 5.) & (t < t[rl][-1]-1.)),
                neutral_command_windows=windows,
                two_second_neutral_windows=[dict(window=[float(lo), float(lo+2.)],
                    **metrics(settled_neutral & (t >= lo) & (t < lo+2.)))
                    for lo in np.arange(2., t[rl][-1], 2.)],
                command_intervals=[dict(start_s=float(t[ind[0]]), end_s=float(t[ind[-1]]),
                    min=d['command'][ind].min(axis=0).tolist(), max=d['command'][ind].max(axis=0).tolist())
                    for ind in blocks(rl & ~neutral)])
            np.savez_compressed(out / f'{name}_signals.npz',
                **{k: v for k, v in d.items() if isinstance(v, np.ndarray)}, added=added)
            data[name] = d
    (out / 'metrics.json').write_text(json.dumps(report, indent=2) + '\n')
    fig, axes = plt.subplots(4, len(data), figsize=(6.5*len(data), 10),
                             sharex='col', constrained_layout=True, squeeze=False)
    for col, (name, d) in enumerate(data.items()):
        m, t = d['rl'], d['t'][d['rl']]
        axes[0, col].plot(t, d['command'][m, 0], label='forward command')
        axes[0, col].plot(t, d['command'][m, 2], label='yaw command')
        axes[1, col].plot(t, d['velocity'][m], label='encoder/IMU/FK estimate')
        axes[1, col].plot(t, d['wheel_proxy'][m], alpha=.5, label='wheel rolling proxy')
        axes[2, col].plot(t, d['pitch'][m], label='pitch')
        axes[3, col].plot(t, common(d['base'])[m], label='policy/PD')
        axes[3, col].plot(t, common(d['torque'] - d['base'])[m], label='additional bias')
        axes[3, col].plot(t, common(d['torque'])[m], label='final computed torque', alpha=.6)
        axes[0, col].set_title(bundle.name.replace('flashsac_', 'model_') + ': bias ' + name.upper())
        axes[3, col].set_xlabel('Seconds from RL entry')
    for row, unit in enumerate(['m/s; rad/s', 'm/s', 'degrees', 'Nm/wheel']):
        axes[row, 0].set_ylabel(unit)
    for axis in axes.flat:
        axis.grid(alpha=.2)
        axis.legend(fontsize=7)
    fig.suptitle('Recorded runs; ' + report['operator_support'])
    fig.savefig(out / 'comparison.png', dpi=150)
    plt.close(fig)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
