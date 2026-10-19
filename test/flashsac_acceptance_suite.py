"""VALIDATION_SIM: separated sim2sim acceptance suite for FlashSAC TITA policies.

Evaluates one exported checkpoint under nominal physics and the real-to-sim mismatch candidates
A/B/C (``docs/exp/2026-10-17/real2sim_leg_wheel_grid.md``). Startup, zero-command hold,
forward/backward translation (with stop re-entry) and yaw are separate scenarios with separate
metric windows. Criteria are written to ``acceptance_protocol.json`` before any rollout and are
*proposed* gates for retrained policies; the current model_60000 run only provides reference values.
Passing in simulation is not evidence of real-robot success.

Sim speed is MuJoCo GT forward speed; yaw rate is body gyro z; torques are commanded PD torques.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import real2sim_leg_wheel_grid as grid

REPO = grid.REPO
BASE_PHYSICS = dict(leg_gain=0.6, leg_frictionloss=2.0, wheel_frictionloss=0.3)
PHYSICS_SETS = {
    'abc': {
        'nominal': (dict(), 0.0),
        'A_imu2': (dict(BASE_PHYSICS), 2.0),
        'B_com1_imu1': (dict(BASE_PHYSICS, com=-0.01), 1.0),
        'C_com2': (dict(BASE_PHYSICS, com=-0.02), 0.0),
    },
    # CoM-only family (nominal legs) for the BaseComShift arm; C kept as the leg-coefficient stress case.
    'com': {
        'nominal': (dict(), 0.0),
        'com_-2.0cm': (dict(com=-0.02), 0.0),
        'com_-3.5cm': (dict(com=-0.035), 0.0),
        'com_-5.0cm': (dict(com=-0.05), 0.0),
        'C_com2': (dict(BASE_PHYSICS, com=-0.02), 0.0),
    },
}
# Deployment-side leg torque compensation c = 1/0.65 on the RL PD output (startup PD unchanged), for a
# true leg output scale k in {0.55, 0.65, 0.75}: startup uses k, RL uses k*c. 'uncomp' is k=0.65 without c.
_C = 1 / 0.65
PHYSICS_SETS['legcomp'] = {
    'nominal': (dict(), 0.0),
    'uncomp_k0.65': (dict(leg_gain=0.65), 0.0),
    'comp_k0.55': (dict(startup_leg_gain=0.55, leg_gain=0.55 * _C), 0.0),
    'comp_k0.65': (dict(startup_leg_gain=0.65, leg_gain=0.65 * _C), 0.0),
    'comp_k0.75': (dict(startup_leg_gain=0.75, leg_gain=0.75 * _C), 0.0),
    'comp_k0.65_friction': (dict(startup_leg_gain=0.65, leg_gain=0.65 * _C, leg_frictionloss=2.0,
                                 wheel_frictionloss=0.3), 0.0),
}
# Training-side compensation arms (C1/C2) deploy at 60/1.5: uncompensated leg output scale k on all
# legs and all phases, plus the nominal regression case and a friction stress case.
PHYSICS_SETS['cscale'] = {
    'nominal': (dict(), 0.0),
    'k0.55': (dict(leg_gain=0.55), 0.0),
    'k0.65': (dict(leg_gain=0.65), 0.0),
    'k0.75': (dict(leg_gain=0.75), 0.0),
    'k0.65_friction': (dict(leg_gain=0.65, leg_frictionloss=2.0, wheel_frictionloss=0.3), 0.0),
}
PHYSICS = PHYSICS_SETS['abc']
HOLD = (6.0, 13.0)        # command fully ramped (start 3 s + 1 s ramp) .. ramp-down start
STOP = (18.0, 23.0)       # 5 s after the command returned to zero
SCENARIOS = {
    'zero': dict(duration_s=30.0, command=None),
    'fwd_0.3': dict(duration_s=23.0, command=dict(start_s=3.0, ramp_s=1.0, end_s=13.0, value=[0.3, 0.0, 0.0])),
    'bwd_0.3': dict(duration_s=23.0, command=dict(start_s=3.0, ramp_s=1.0, end_s=13.0, value=[-0.3, 0.0, 0.0])),
    'fwd_0.6': dict(duration_s=23.0, command=dict(start_s=3.0, ramp_s=1.0, end_s=13.0, value=[0.6, 0.0, 0.0])),
    'bwd_0.6': dict(duration_s=23.0, command=dict(start_s=3.0, ramp_s=1.0, end_s=13.0, value=[-0.6, 0.0, 0.0])),
    'yaw_+0.5': dict(duration_s=23.0, command=dict(start_s=3.0, ramp_s=1.0, end_s=13.0, value=[0.0, 0.0, 0.5])),
    'yaw_-0.5': dict(duration_s=23.0, command=dict(start_s=3.0, ramp_s=1.0, end_s=13.0, value=[0.0, 0.0, -0.5])),
}
CRITERIA = dict(
    startup=dict(window_s=[0.0, 3.0], no_failure=True, peak_pitch_deg_max=10.0,
                 report=['peak |wheel tau|', 'peak |leg tau|', 'displacement at 3 s', 'knee settle time']),
    zero_command=dict(window_s=[5.0, 30.0], mean_speed_abs_max=0.03, displacement_abs_max_m=0.75,
                      pitch_std_deg_max=1.0, all_physics=True),
    translation=dict(hold_window_s=list(HOLD), stop_window_s=list(STOP), tracking_err_abs_max={'0.3': 0.05, '0.6': 0.10},
                     stop_speed_abs_max=0.05, all_physics=True),
    yaw=dict(hold_window_s=list(HOLD), yaw_err_abs_max=0.05, translation_during_yaw_abs_max=0.05, all_physics=True),
    regression_guard=dict(torque_rms_ratio_max_vs_reference=1.2, pitch_std_ratio_max_vs_reference=1.2,
                          wheel_clip_fraction_max=0.01, reference='tita_flash_sac_115632_883848/model_60000'),
)


def window(t, span):
    return (t >= span[0] - 1e-9) & (t < span[1] - 1e-9)


def scenario_metrics(name: str, s: dict) -> dict:
    t = np.arange(len(s['speed'])) * grid.DT
    speed, yaw = s['speed'], s['gyro'][:, 2]
    pitch = grid.pitch_deg(s['quat'])
    tau = s['tau_cmd']
    wheel, legs = tau[:, [3, 7]], tau[:, [0, 1, 2, 4, 5, 6]]
    displacement = np.concatenate([[0.], np.cumsum(speed[:-1]) * grid.DT])
    knee = s['q'][:, [2, 6]].mean(1)

    def block(span):
        m = window(t, span)
        return dict(mean_speed=float(speed[m].mean()), mean_yaw_rate=float(yaw[m].mean()),
                    pitch_mean=float(pitch[m].mean()), pitch_std=float(pitch[m].std()),
                    wheel_tau_rms=float(np.sqrt(np.mean(wheel[m] ** 2))), wheel_tau_peak=float(np.abs(wheel[m]).max()),
                    leg_tau_rms=float(np.sqrt(np.mean(legs[m] ** 2))), leg_tau_peak=float(np.abs(legs[m]).max()),
                    wheel_clip_fraction=float(np.mean(np.abs(wheel[m]) >= 12.0 - 1e-6)),
                    displacement_m=float(displacement[m][-1] - displacement[m][0]))

    out = dict(startup=None, main=None, stop=None)
    m0 = window(t, (0.0, 3.0))
    final_knee = knee[window(t, (5.0, 10.0))].mean() if t[-1] >= 10.0 else knee[-1]
    settled = np.flatnonzero(np.abs(knee - final_knee) > 0.05)
    out['startup'] = dict(peak_wheel_tau=float(np.abs(wheel[m0]).max()), peak_leg_tau=float(np.abs(legs[m0]).max()),
                          peak_pitch_deg=float(np.abs(pitch[m0]).max()), displacement_3s_m=float(displacement[m0][-1]),
                          knee_settle_s=float(t[settled[-1]] + grid.DT) if len(settled) and settled[-1] < len(t) - 1 else 0.0)
    if name == 'zero':
        out['main'] = block((5.0, 30.0))
    else:
        out['main'] = block(HOLD)
        out['stop'] = block(STOP)
    return out


def evaluate_gates(name: str, m: dict, command: list | None) -> dict:
    c = CRITERIA
    gates = {}
    if name == 'zero':
        z = m['main']
        gates.update(zero_mean_speed=abs(z['mean_speed']) <= c['zero_command']['mean_speed_abs_max'],
                     zero_displacement=abs(z['displacement_m']) <= c['zero_command']['displacement_abs_max_m'],
                     zero_pitch_std=z['pitch_std'] <= c['zero_command']['pitch_std_deg_max'],
                     startup_peak_pitch=m['startup']['peak_pitch_deg'] <= c['startup']['peak_pitch_deg_max'])
    elif name.startswith(('fwd', 'bwd')):
        level = name.split('_')[1]
        gates.update(tracking=abs(m['main']['mean_speed'] - command[0]) <= c['translation']['tracking_err_abs_max'][level],
                     stop_reentry=abs(m['stop']['mean_speed']) <= c['translation']['stop_speed_abs_max'])
    else:
        gates.update(yaw_tracking=abs(m['main']['mean_yaw_rate'] - command[2]) <= c['yaw']['yaw_err_abs_max'],
                     yaw_translation=abs(m['main']['mean_speed']) <= c['yaw']['translation_during_yaw_abs_max'])
    gates['wheel_clip'] = m['main']['wheel_clip_fraction'] <= c['regression_guard']['wheel_clip_fraction_max']
    return {k: bool(v) for k, v in gates.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--checkpoint', default='model_60000', help='export under velocity_bias_overnight/exports')
    parser.add_argument('--output', type=Path, default=REPO / 'docs/exp/2026-10-17/flashsac_retrain_prep/acceptance_model_60000')
    parser.add_argument('--seeds', type=int, nargs='+', default=[104, 270])
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--physics-set', choices=sorted(PHYSICS_SETS), default='abc')
    args = parser.parse_args()
    physics_set = PHYSICS_SETS[args.physics_set]
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    protocol = dict(execution_domain='VALIDATION_SIM', physics={k: dict(physics=v[0], imu_pitch_deg=v[1])
                    for k, v in physics_set.items()}, scenarios=SCENARIOS, criteria=CRITERIA, seeds=args.seeds,
                    startup='sim2sim splay -> transform_up -> sit -> RL (same as real state machine), seed-dependent '
                            'initial base/leg velocity noise', note='criteria fixed before rollouts')
    path = out / 'acceptance_protocol.json'
    if path.exists() and json.loads(path.read_text()) != protocol:
        raise SystemExit('acceptance_protocol.json differs; refusing to overwrite a fixed protocol')
    path.write_text(json.dumps(protocol, indent=2) + '\n')

    jobs = []
    for (pname, (phys, imu)), (sname, spec), seed in [(p, s, seed) for p in physics_set.items() for s in SCENARIOS.items()
                                                     for seed in args.seeds]:
        if seed != args.seeds[0] and sname != 'zero':
            continue  # extra seeds only for the zero-command/startup scenario
        job = dict(id=f'{pname}__{sname}__s{seed}', checkpoint=args.checkpoint, physics=phys,
                   sensor=dict(imu_pitch_deg=imu), seed=seed, duration_s=spec['duration_s'],
                   save_signals=True, output=str(out / 'signals'))
        if spec['command']:
            job['command'] = spec['command']
        jobs.append(job)
    results = grid.run_jobs(jobs, args.workers, 'acceptance_rollouts', out)
    report = {}
    for r in results:
        pname, sname, seed = r['job']['id'].split('__')
        entry = dict(evidence_status=r['evidence_status'], failure=r.get('failure', []))
        if r['evidence_status'] == 'PASS':
            s = dict(np.load(out / 'signals' / f"{r['job']['id']}.npz"))
            metrics = scenario_metrics(sname, s)
            spec = SCENARIOS[sname]['command']
            entry.update(metrics=metrics, gates=evaluate_gates(sname, metrics, spec['value'] if spec else None))
        report.setdefault(pname, {})[f'{sname}__{seed}'] = entry
    (out / 'acceptance_metrics.json').write_text(json.dumps(report, indent=2) + '\n')

    for pname, rows in report.items():
        print(f'== {pname}')
        for key, e in rows.items():
            if e['evidence_status'] != 'PASS':
                print(f'  {key:18s} FAIL {e["failure"]}')
                continue
            m, g = e['metrics'], e['gates']
            main_ = m['main']
            extra = (f"stop v={m['stop']['mean_speed']:+.3f}" if m['stop'] else
                     f"disp={main_['displacement_m']:+.2f} m pitch_std={main_['pitch_std']:.2f}")
            print(f"  {key:18s} v={main_['mean_speed']:+.3f} wz={main_['mean_yaw_rate']:+.3f} pitch={main_['pitch_mean']:+.2f} "
                  f"wheelRMS/peak={main_['wheel_tau_rms']:.2f}/{main_['wheel_tau_peak']:.2f} legRMS/peak={main_['leg_tau_rms']:.1f}/"
                  f"{main_['leg_tau_peak']:.1f} {extra} | startup wheel/leg peak={m['startup']['peak_wheel_tau']:.2f}/"
                  f"{m['startup']['peak_leg_tau']:.1f} pitch peak={m['startup']['peak_pitch_deg']:.1f} | gates "
                  + ','.join(f"{k}={'P' if v else 'F'}" for k, v in g.items()))


if __name__ == '__main__':
    main()
