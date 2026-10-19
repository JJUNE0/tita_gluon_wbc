"""VALIDATION_SIM: holdout replay of the real 17:44:21 joystick run against real-to-sim candidates.

The real-to-sim candidates were fitted only on the 14:11:13 free-drift run
(``docs/exp/2026-10-17/real2sim_leg_wheel_grid.md``). This script replays the *recorded*
command sequence of ``flashsac_60000_174421_440893411_output_true`` (RL frame k -> sim policy
tick k, 50 Hz) through the same frozen model_60000 ONNX and sim2sim startup, for nominal physics
and each candidate, and scores them with metrics fixed in ``holdout_protocol.json`` *before* the
rollouts run. The whole run is the holdout; no frames are split or refitted.

Real speed is the encoder/IMU/FK estimate (no external ground truth); sim speed is MuJoCo GT.
Torques compared are commanded PD torques on both sides.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import real2sim_leg_wheel_grid as grid

REPO = grid.REPO
RUN = 'docs/exp/2026-10-17/flashsac_60000_174421_torque_review'
SIGNALS = f'{RUN}/signals.npz'
METRICS = f'{RUN}/metrics.json'
BASE_PHYSICS = dict(leg_gain=0.6, leg_frictionloss=2.0, wheel_frictionloss=0.3)
CANDIDATE_SETS = {}
CANDIDATES = {
    'nominal': (dict(), 0.0),
    'A_imu2': (dict(BASE_PHYSICS), 2.0),
    'B_com1_imu1': (dict(BASE_PHYSICS, com=-0.01), 1.0),
    'C_com2': (dict(BASE_PHYSICS, com=-0.02), 0.0),
    'D_imu2_only': (dict(), 2.0),
    'E_gain_friction_only': (dict(BASE_PHYSICS), 0.0),
}
CANDIDATE_SETS['abc'] = CANDIDATES
# Operator decision 2026-10-17: IMU considered fine, CoM the main issue, no actuator/friction model.
# Base CoM x shifts with nominal legs; -3.5/-4 cm bracket the real pitch in the CoM-only sweep.
CANDIDATE_SETS['com_only'] = {
    'nominal': (dict(), 0.0),
    'com_only_-3.0cm': (dict(com=-0.03), 0.0),
    'com_only_-3.5cm': (dict(com=-0.035), 0.0),
    'com_only_-4.0cm': (dict(com=-0.04), 0.0),
    'C_com2': (dict(BASE_PHYSICS, com=-0.02), 0.0),
}
def make_protocol(candidates: dict) -> dict:
    return dict(PROTOCOL, candidates={k: dict(physics=v[0], imu_pitch_deg=v[1]) for k, v in candidates.items()})


PROTOCOL = dict(
    execution_domain='VALIDATION_SIM',
    fitted_on='flashsac_60000_141113_460666182_output_true (RL+5-10 s, zero command)',
    holdout='flashsac_60000_174421_440893411_output_true (whole RL span, recorded commands replayed)',
    checkpoint='tita_flash_sac_115632_883848/model_60000',
    alignment='real RL frame k <-> sim policy tick k (50 Hz); sim starts from the sim2sim startup sequence',
    candidates={k: dict(physics=v[0], imu_pitch_deg=v[1]) for k, v in CANDIDATES.items()},
    metrics=dict(
        segment_speed_mae='sample-weighted |mean speed sim - mean FK speed real| over report segments with >= 20 samples',
        post3_rmse='RMSE over real t >= 3 s of speed, gyro z, pitch [deg], mean knee q, mean knee commanded torque',
        neutral_settled='RL+7.71-9.25 s (neutral >= 1 s): mean speed, pitch, knee q, knee torque, wheel torque',
        startup='0-1 s and 1-3 s: peak |wheel commanded torque|, peak |pitch|, mean speed (reported separately)'),
    pass_rule=dict(segment_speed_mae_max=0.08, neutral_speed_abs_err_max=0.08, neutral_knee_q_abs_err_max=0.10,
                   neutral_knee_tau_abs_err_max=4.0, neutral_pitch_abs_err_max_deg=1.5),
    note='Thresholds fixed before running. Passing means consistency with this one holdout, not a physical identification.')


def pitch_of(quat):
    return grid.pitch_deg(quat)


def stats_in(mask, series):
    return float(np.mean(series[mask])) if mask.any() else float('nan')


def evaluate(real: dict, sim: dict, segments: list) -> dict:
    n = min(len(real['t']), len(sim['speed']))
    t = real['t'][:n]
    r_speed, s_speed = real['velocity'][:n], sim['speed'][:n]
    r_pitch, s_pitch = real['pitch'][:n], pitch_of(sim['quat'][:n])
    r_knee, s_knee = real['q'][:n][:, [2, 6]].mean(1), sim['q'][:n][:, [2, 6]].mean(1)
    r_ktau, s_ktau = real['torque'][:n][:, [2, 6]].mean(1), sim['tau_cmd'][:n][:, [2, 6]].mean(1)
    r_wtau, s_wtau = real['torque'][:n][:, [3, 7]].mean(1), sim['tau_cmd'][:n][:, [3, 7]].mean(1)
    r_yaw, s_yaw = real['gyro'][:n, 2], sim['gyro'][:n, 2]
    command_error = float(np.max(np.abs(real['command'][:n] - sim['command'][:n])))

    rows, weight, err = [], 0, 0.0
    for seg in segments:
        if seg['samples'] < 20:
            continue
        m = (t >= seg['start_s'] - 1e-6) & (t <= seg['end_s'] + 1e-6)
        e = abs(stats_in(m, s_speed) - stats_in(m, r_speed))
        rows.append(dict(label=seg['label'], start_s=seg['start_s'], end_s=seg['end_s'], samples=int(m.sum()),
                         command=seg['command_mean'], real_speed=stats_in(m, r_speed), sim_speed=stats_in(m, s_speed),
                         real_pitch=stats_in(m, r_pitch), sim_pitch=stats_in(m, s_pitch), abs_err=e))
        weight += m.sum()
        err += e * m.sum()
    post3 = t >= 3.0
    rmse = lambda a, b: float(np.sqrt(np.mean((a[post3] - b[post3]) ** 2)))
    w1 = (t >= 7.71 - 1e-6) & (t <= 9.25 + 1e-6)
    neutral = dict(real=dict(speed=stats_in(w1, r_speed), pitch=stats_in(w1, r_pitch), knee_q=stats_in(w1, r_knee),
                             knee_tau=stats_in(w1, r_ktau), wheel_tau=stats_in(w1, r_wtau)),
                   sim=dict(speed=stats_in(w1, s_speed), pitch=stats_in(w1, s_pitch), knee_q=stats_in(w1, s_knee),
                            knee_tau=stats_in(w1, s_ktau), wheel_tau=stats_in(w1, s_wtau)))
    startup = {}
    for name, (a, b) in dict(s0to1=(0., 1.), s1to3=(1., 3.)).items():
        m = (t >= a) & (t < b)
        startup[name] = dict(
            real_peak_wheel_tau=float(np.max(np.abs(real['torque'][:n][m][:, [3, 7]]))),
            sim_peak_wheel_tau=float(np.max(np.abs(sim['tau_cmd'][:n][m][:, [3, 7]]))),
            real_peak_pitch=float(np.max(np.abs(r_pitch[m]))), sim_peak_pitch=float(np.max(np.abs(s_pitch[m]))),
            real_speed=stats_in(m, r_speed), sim_speed=stats_in(m, s_speed))
    rule = PROTOCOL['pass_rule']
    seg_mae = err / max(weight, 1)
    checks = {k: bool(v) for k, v in dict(
        segment_speed_mae=seg_mae <= rule['segment_speed_mae_max'],
        neutral_speed=abs(neutral['sim']['speed'] - neutral['real']['speed']) <= rule['neutral_speed_abs_err_max'],
        neutral_knee_q=abs(neutral['sim']['knee_q'] - neutral['real']['knee_q']) <= rule['neutral_knee_q_abs_err_max'],
        neutral_knee_tau=abs(neutral['sim']['knee_tau'] - neutral['real']['knee_tau']) <= rule['neutral_knee_tau_abs_err_max'],
        neutral_pitch=abs(neutral['sim']['pitch'] - neutral['real']['pitch']) <= rule['neutral_pitch_abs_err_max_deg']).items()}
    return dict(frames=int(n), command_replay_max_abs_err=command_error, segment_speed_mae=float(seg_mae), segments=rows,
                post3_rmse=dict(speed=rmse(s_speed, r_speed), yaw_rate=rmse(s_yaw, r_yaw), pitch_deg=rmse(s_pitch, r_pitch),
                                knee_q=rmse(s_knee, r_knee), knee_tau=rmse(s_ktau, r_ktau)),
                neutral_settled=neutral, startup=startup, checks=checks, holdout_consistent=all(checks.values()))


def plot(real, sims, out: Path, names=('nominal', 'A_imu2', 'C_com2')) -> None:
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return
    fig, axes = plt.subplots(5, 1, figsize=(13, 13), sharex=True)
    n = len(real['t'])
    t = real['t']
    series = [('command x [m/s]', lambda d, r: d['command'][:, 0]),
              ('speed [m/s] (real FK / sim GT)', lambda d, r: d['velocity'] if r else d['speed']),
              ('pitch [deg]', lambda d, r: d['pitch'] if r else pitch_of(d['quat'])),
              ('mean knee q [rad]', lambda d, r: d['q'][:, [2, 6]].mean(1)),
              ('mean knee cmd torque [N m]', lambda d, r: (d['torque'] if r else d['tau_cmd'])[:, [2, 6]].mean(1))]
    for ax, (label, fn) in zip(axes, series):
        ax.plot(t, fn(real, True)[:n], 'k', lw=1.4, label='real 17:44:21')
        for name, d in sims.items():
            if name in names:
                m = min(n, len(d['speed']))
                ax.plot(t[:m], fn(d, False)[:m], lw=1.0, label=f'sim {name}')
        ax.set_ylabel(label)
        ax.grid(alpha=.3)
    axes[0].legend(loc='upper right', ncol=4, fontsize=8)
    axes[-1].set_xlabel('time since RL entry [s]')
    fig.tight_layout()
    fig.savefig(out, dpi=110)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, default=REPO / 'docs/exp/2026-10-17/flashsac_retrain_prep/holdout_174421')
    parser.add_argument('--workers', type=int, default=6)
    parser.add_argument('--set', choices=sorted(CANDIDATE_SETS), default='abc')
    args = parser.parse_args()
    candidates = CANDIDATE_SETS[args.set]
    protocol = make_protocol(candidates)
    out = args.output if args.set == 'abc' else args.output.with_name(f'{args.output.name}_{args.set}')
    out.mkdir(parents=True, exist_ok=True)
    protocol_path = out / 'holdout_protocol.json'
    if protocol_path.exists():
        if json.loads(protocol_path.read_text()) != protocol:
            raise SystemExit('holdout_protocol.json differs from the script protocol; refusing to overwrite')
    else:
        protocol_path.write_text(json.dumps(protocol, indent=2) + '\n')

    d = np.load(REPO / SIGNALS)
    rl = d['rl'].astype(bool)
    real = {k: d[k][rl] for k in ('t', 'velocity', 'pitch', 'q', 'torque', 'gyro', 'command')}
    duration = len(real['t']) * grid.DT
    jobs = [dict(id=f'holdout_{name}', checkpoint='model_60000', physics=phys, sensor=dict(imu_pitch_deg=imu),
                 seed=104, duration_s=duration, command_npz=SIGNALS, save_signals=True, output=str(out / 'signals'))
            for name, (phys, imu) in candidates.items()]
    results = grid.run_jobs(jobs, args.workers, 'holdout_rollouts', out)
    segments = json.loads((REPO / METRICS).read_text())['segments']
    sims, report = {}, {}
    for r in results:
        name = r['job']['id'].removeprefix('holdout_')
        if r['evidence_status'] != 'PASS':
            report[name] = dict(evidence_status=r['evidence_status'], failure=r.get('failure'))
            continue
        sim = dict(np.load(out / 'signals' / f"{r['job']['id']}.npz"))
        sims[name] = sim
        report[name] = dict(evidence_status='PASS', **evaluate(real, sim, segments))
    (out / 'holdout_metrics.json').write_text(json.dumps(report, indent=2) + '\n')
    plot(real, sims, out / 'holdout_timeseries.png',
         names=('nominal', 'A_imu2', 'C_com2') if args.set == 'abc' else ('nominal', 'com_only_-3.5cm', 'C_com2'))

    print(f"{'candidate':22s} {'segMAE':>7s} {'rmse_v':>7s} {'rmse_yaw':>8s} {'rmse_pitch':>10s} {'rmse_knee':>9s} "
          f"{'rmse_ktau':>9s} | W1 v sim/real | W1 knee q | W1 knee tau | W1 pitch | consistent")
    for name, m in report.items():
        if m['evidence_status'] != 'PASS':
            print(f'{name:22s} FAIL {m.get("failure")}')
            continue
        p, w = m['post3_rmse'], m['neutral_settled']
        print(f"{name:22s} {m['segment_speed_mae']:7.3f} {p['speed']:7.3f} {p['yaw_rate']:8.3f} {p['pitch_deg']:10.2f} "
              f"{p['knee_q']:9.3f} {p['knee_tau']:9.2f} | {w['sim']['speed']:+.3f}/{w['real']['speed']:+.3f} | "
              f"{w['sim']['knee_q']:+.3f}/{w['real']['knee_q']:+.3f} | {w['sim']['knee_tau']:5.1f}/{w['real']['knee_tau']:5.1f} | "
              f"{w['sim']['pitch']:4.2f}/{w['real']['pitch']:4.2f} | {m['holdout_consistent']}")
        print(f"{'':22s} command replay max err {m['command_replay_max_abs_err']:.2e}; startup 0-1 s peak wheel tau "
              f"sim/real {m['startup']['s0to1']['sim_peak_wheel_tau']:.2f}/{m['startup']['s0to1']['real_peak_wheel_tau']:.2f} N m")


if __name__ == '__main__':
    main()
