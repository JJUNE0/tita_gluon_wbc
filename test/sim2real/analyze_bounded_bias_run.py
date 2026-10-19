"""DESKTOP_DRY_RUN: exact replay of the deployed bounded-bias controller.

Local SQLite/ONNX-free controller-math analysis. No ROS node or robot SDK.
"""
import argparse
import io
import json
from pathlib import Path
import subprocess
import tempfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from diagnose_three_case_wheel_bias import load, targets, torques, common, summarize, blocks
from test_velocity_bias_08nm import CFG, PACKAGE, REPO, header
from analyze_free_drift_baseline import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bag', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--support-annotation', choices=['unknown', 'sparse_possible'], default='unknown')
    args = parser.parse_args()
    args.bag, args.output = args.bag.resolve(), args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    d = load(args.bag)
    t, rl, diag = d['t'], d['rl'], d['diag']
    dt = d['dt'].copy()
    dt[np.flatnonzero(rl)[0]] = .02
    rows = np.c_[rl, dt, d['command'], d['q'], d['dq'], d['quat'], d['gyro'], d['action']]
    stream = io.StringIO()
    np.savetxt(stream, np.array(header())[None], fmt='%.17g')
    np.savetxt(stream, rows, fmt='%.17g')
    with tempfile.TemporaryDirectory(dir=REPO/'test/sim2real', prefix='bounded_review_') as temp:
        binary = Path(temp)/'runtime'
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
                        '-isystem', '/usr/include/eigen3', '-I', str(PACKAGE/'include'),
                        str(REPO/'test/sim2real/velocity_bias_runtime.cpp'), '-o', str(binary)], check=True)
        result = subprocess.run([str(binary), 'status'], input=stream.getvalue(), capture_output=True, text=True, check=True)
    replay = np.loadtxt(io.StringIO(result.stdout), ndmin=2)
    assert replay.shape == (len(t), 29)
    replay_error = abs(replay[rl, :9]-diag[rl, :9]).max(axis=0)
    np.testing.assert_allclose(replay[rl, :9], diag[rl, :9], atol=1e-5, rtol=1e-5)
    d['velocity'] = diag[:, 3]
    d['target'] = targets(d['action'].astype(float), CFG)
    d['base'] = torques(d['target'], d, CFG)
    rebuilt = torques(d['target'], d, CFG, corrected=True)
    added = d['torque']-d['base']
    torque_error = float(abs(rebuilt[rl]-d['torque'][rl]).max())
    added_log_error = float(abs(added[rl][:, [3, 7]]-diag[rl, 9:11]).max())
    assert torque_error < 1e-8 and added_log_error < 1e-6
    assert abs(added[rl]).max() <= .8+1e-8
    w, x, y, z = d['quat'].T
    roll = np.degrees(np.arctan2(2*(w*x+y*z), 1-2*(x*x+y*y)))
    ref = np.degrees(replay[:, 28])
    eligible = rl & (diag[:, 1] > .5)
    holding = rl & (diag[:, 0] > .5)
    inhibited = rl & (replay[:, 26] > .5)
    zero_command = (abs(d['command']) <= 1e-6).all(axis=1)

    def stats(mask):
        value = summarize(d, mask)
        if mask.sum() > 1:
            value['at_torque_cap_fraction'] = float((abs(common(added)[mask]) >= .7999).mean())
            value['pitch_reference_deg'] = float(ref[mask].mean())
            value['pitch_deviation_abs_max_deg'] = float(abs(d['pitch'][mask]-ref[mask]).max())
        return value

    episodes = []
    for i, ind in enumerate(blocks(holding), 1):
        onset, end = t[ind[0]], t[ind[-1]]
        mask = np.zeros(len(t), dtype=bool)
        mask[ind] = True
        active = ind[eligible[ind]]
        entry = dict(id=i, hold_start_s=float(onset), hold_end_s=float(end),
            acquired=bool(len(active)), acquisition=stats(mask & (diag[:, 2] >= 1.) & (diag[:, 2] < 3.)))
        if len(active):
            first, last = t[active[0]], t[active[-1]]
            settled = mask & eligible & zero_command & (t >= first+2.) & (t <= last)
            last3 = mask & eligible & zero_command & (t >= max(first+1., last-3.)) & (t <= last)
            entry.update(eligible_start_s=float(first), eligible_end_s=float(last),
                         acquired_drift_m_s=float(replay[active[0], 27]),
                         acquired_pitch_reference_deg=float(ref[active[0]]),
                         settled=stats(settled), last_3s=stats(last3))
        episodes.append(entry)
    guard_events = []
    for ind in blocks(inhibited):
        i = int(ind[0])
        causes = []
        if abs(roll[i]) > np.degrees(.3): causes.append('absolute_roll')
        if abs(d['pitch'][i]) > np.degrees(.3): causes.append('absolute_pitch')
        if abs(diag[i, 3]) > 1.: causes.append('estimated_speed')
        if abs(d['pitch'][i]-ref[i]) > 5.: causes.append('pitch_deviation')
        if replay[i, 25] < .5: causes.append('insufficient_acquisition')
        guard_events.append(dict(time_s=float(t[i]), end_s=float(t[ind[-1]]), causes=causes,
            pitch_deg=float(d['pitch'][i]), reference_deg=float(ref[i]), roll_deg=float(roll[i]),
            pitch_deviation_deg=float(d['pitch'][i]-ref[i]), velocity_m_s=float(diag[i, 3]),
            added_before_nm=added[i-1, [3, 7]].tolist(), added_after_nm=added[i, [3, 7]].tolist()))
    command_events = []
    for ind in blocks(rl & ~holding):
        command_events.append(dict(start_s=float(t[ind[0]]), end_s=float(t[ind[-1]]),
            command_min=d['command'][ind].min(axis=0).tolist(),
            command_max=d['command'][ind].max(axis=0).tolist()))
    # Sensitivity to brief unlabelled disturbances: this does NOT detect hands.
    excluded = t >= t[rl][-1]-1.
    for event in guard_events:
        excluded |= abs(t-event['time_s']) <= 1.
    trimmed = []
    for entry in episodes:
        if not entry['acquired']:
            continue
        mask = (eligible & zero_command & ~excluded &
                (t >= entry['eligible_start_s']+2.) & (t <= entry['eligible_end_s']))
        trimmed.append(dict(id=entry['id'], **stats(mask)))
    report = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='SUSPICIOUS',
        operator_support_annotation=args.support_annotation,
        disturbance_sensitivity=dict(excludes_guard_onset_plus_minus_s=1., excludes_last_rl_s=1.,
            note='Event-based exclusion, not identification of hand contact; brief contact times remain unknown.',
            episodes=trimmed),
        checkpoint_sha256=CFG['policy_interface']['checkpoint_sha256'], onnx_sha256=CFG['policy_interface']['onnx_sha256'],
        source_db=d['source_db'], source_db_sha256=d['source_db_sha256'], frames=len(t), rl_frames=int(rl.sum()),
        last_rl_sample_s=float(t[rl][-1]), rl_dt_max_s=float(d['dt'][rl].max()),
        diag_replay_max_errors=replay_error.tolist(), torque_reconstruction_error_nm=torque_error,
        added_log_error_nm=added_log_error, max_added_nm=float(abs(added[rl]).max()),
        command_abs_max=abs(d['command'][rl]).max(axis=0).tolist(), episodes=episodes,
        inhibited_interval_metrics=stats(inhibited & zero_command),
        guard_events=guard_events, command_exit_intervals=command_events,
        five_second_windows=[dict(window_start_s=float(lo), **stats(eligible & (t >= lo) & (t < lo+5)))
                             for lo in np.arange(5., t[rl][-1], 5.)],
        sources={str(p.relative_to(REPO)): digest(p) for p in (Path(__file__),
            PACKAGE/'include/tita_controller/velocity_bias.hpp', PACKAGE/'src/tita_node.cpp')},
        limitations=['Velocity is an encoder/IMU/FK proxy, not independently measured chassis translation.',
                     'Commands/support and initial posture vary; within-run differences are not isolated causal estimates.',
                     'Torque is computed command, not measured applied torque.',
                     'Exact replay validates software behavior, not physical feedback sign or stability margin.'])
    (args.output/'metrics.json').write_text(json.dumps(report, indent=2)+'\n')
    np.savez_compressed(args.output/'signals.npz', **{k: v for k, v in d.items() if isinstance(v, np.ndarray)},
                        replay=replay, reference=ref, added=added, roll=roll)
    fig, ax = plt.subplots(5, 1, figsize=(14, 14), sharex=True, constrained_layout=True)
    ax[0].plot(t[rl], d['command'][rl, 0], label='forward command')
    ax[0].plot(t[rl], d['command'][rl, 2], label='yaw command', alpha=.7)
    ax[1].plot(t[rl], np.where(holding, diag[:, 3], np.nan)[rl], label='FK speed while holding', lw=.9)
    ax[1].plot(t[rl], d['wheel_proxy'][rl], label='wheel rolling proxy', lw=.7, alpha=.6)
    ax[2].plot(t[rl], d['pitch'][rl], label='pitch')
    ax[2].plot(t[rl], np.where(holding & (replay[:, 25] > .5), ref, np.nan)[rl],
               label='acquired pitch reference', ls='--')
    ax[3].plot(t[rl], common(d['base'])[rl], label='policy/PD')
    ax[3].plot(t[rl], common(added)[rl], label='added correction')
    ax[3].plot(t[rl], common(d['torque'])[rl], label='final computed torque', alpha=.7)
    ax[3].axhline(-.8, color='gray', ls=':')
    ax[4].plot(t[rl], diag[rl, 1], label='eligible')
    ax[4].plot(t[rl], replay[rl, 26], label='guard inhibited')
    for axis, label in zip(ax, ['m/s; rad/s', 'm/s (estimated)', 'degrees', 'Nm / wheel', 'flags']):
        axis.set_ylabel(label)
        axis.grid(alpha=.2)
        axis.legend(fontsize=8)
        for event in guard_events:
            axis.axvline(event['time_s'], color='red', ls=':')
    ax[-1].set_xlabel('Seconds from RL entry')
    support = ('Operator reports sparse possible contact; exact timing unknown'
               if args.support_annotation == 'sparse_possible' else 'External support annotation pending')
    fig.suptitle('Real bounded wheel-bias run: computed commands and sensor estimates\n'+support)
    fig.savefig(args.output/'bounded_bias_overview.png', dpi=150)
    plt.close(fig)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
