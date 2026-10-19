"""VALIDATION_SIM: sim2sim screening of the C1/C2 leg-scale arms (checkpoints 40k-75k, training running).

C1 (``DDT-Velocity-Flat-Tita-My-LegScale-v0``) and C2 (``...-LegScale-Reward-v0``) train with leg Kp/Kd
x log-U[0.55, 0.78] so that the deployed 60/1.5 config matches a real leg output scale near 0.65
(``docs/exp/2026-10-18/flashsac_legscale_training.md``). They are evaluated *without* deployment-side
compensation under the ``cscale`` physics set of ``flashsac_acceptance_suite``:
- nominal (k = 1, regression);
- k 0.55 / 0.65 / 0.75 on all legs and all phases;
- k 0.65 + friction (stress, not used for selection).

References under the same physics:
- R0 (115632/model_60000), trained nominal;
- A80k (201940/model_80000), the policy currently on the robot. The 200 Hz harness cannot apply A80k's
  knee-only 92/2.3, so this is A80k at 60/1.5.

Selection per arm uses the most passed gates over nominal and k 0.55/0.65/0.75. Ties go to the lower mean
|zero-command v| over k 0.55/0.65/0.75, then to the later step. The rule and criteria are written to
``evaluation_protocol.json`` before any rollout.

Also reported: zero-command stand posture (mean hip/thigh/knee, pitch) under k 0.65, compared with the vendor
stand (hip 0, thigh 1.09, knee -2.16 rad, pitch 1.4 deg) that C2's reward targets.

Sim-only screening. Passing is not evidence of real-robot success, and the real 25 Hz chatter is not modelled.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import evaluate_ab_policies as ab
import flashsac_acceptance_suite as acc
import real2sim_leg_wheel_grid as grid

REPO = grid.REPO
EXPORTS = REPO / 'docs/exp/2026-10-18/flashsac_legscale_sim2sim/exports'
ARMS = {'C1': 'tita_flash_sac_114458_484840', 'C2': 'tita_flash_sac_114500_483968'}
STEPS = [40000, 50000, 60000, 70000, 75000]
REFERENCES = [
    dict(label='R0_60k', arm='R0', step=60000, config=ab.REFERENCE['config']),
    dict(label='A_80k', arm='A', step=80000, config=str(REPO / 'docs/exp/2026-10-18/flashsac_ab_sim2sim/exports/'
                                                          'tita_flash_sac_201940_278440_model_80000/config.json')),
]
SELECTION_PHYSICS = ['nominal', 'k0.55', 'k0.65', 'k0.75']
MISMATCH = ['k0.55', 'k0.65', 'k0.75']
VENDOR_STAND = dict(hip=0.0, thigh=1.09, knee=-2.16, pitch_deg=1.4)


def policies() -> list[dict]:
    rows = list(REFERENCES)
    for arm, run in ARMS.items():
        for step in STEPS:
            rows.append(dict(label=f'{arm}_{step // 1000}k', arm=arm, step=step,
                             config=str(EXPORTS / f'{run}_model_{step}' / 'config.json')))
    return rows


def protocol() -> dict:
    return dict(execution_domain='VALIDATION_SIM', policies=policies(), physics=acc.PHYSICS_SETS['cscale'],
                scenarios=acc.SCENARIOS, criteria=acc.CRITERIA, seeds=[104, 270], extra_seed_scenarios=['zero'],
                selection='per arm: max total passed gates over ' + ','.join(SELECTION_PHYSICS) +
                          ' (a failed rollout fails all of its gates); tie 1: min mean |zero-command v| (seed 104) '
                          'over ' + ','.join(MISMATCH) + '; tie 2: later step. k0.65_friction is reported only.',
                posture='zero-command (seed 104) mean hip/thigh/knee [5, 30] s under k0.65 vs vendor stand',
                note='Sim-only screening; C1/C2 deploy at 60/1.5 (no deployment-side compensation).')


def summarize(report: dict) -> dict:
    summary = {}
    for label, by_physics in report.items():
        passed = possible = 0
        zero, failures, stress = [], [], 0
        for pname, rows in by_physics.items():
            for key, entry in rows.items():
                sname = key.split('__')[0]
                p, n = ab.gate_total(entry, sname)
                if entry['evidence_status'] != 'PASS':
                    failures.append(f'{pname}/{key}')
                if pname not in SELECTION_PHYSICS:
                    stress += p
                    continue
                passed, possible = passed + p, possible + n
                if sname == 'zero' and key.endswith('s104') and pname in MISMATCH:
                    zero.append(abs(entry['metrics']['main']['mean_speed']) if entry['evidence_status'] == 'PASS' else 9.9)
        summary[label] = dict(gates_passed=passed, gates_possible=possible, stress_gates_passed=stress,
                              failures=failures, mean_abs_zero_speed_mismatch=float(np.mean(zero)) if zero else None)
    return summary


def posture(results: list[dict], signals: Path) -> dict:
    out = {}
    for r in results:
        label, pname, sname, seed = r['job']['id'].split('__')
        if (sname, seed, pname) != ('zero', 's104', 'k0.65') or r['evidence_status'] != 'PASS':
            continue
        s = dict(np.load(signals / f"{r['job']['id']}.npz"))
        t = np.arange(len(s['speed'])) * grid.DT
        m = (t >= 5.0) & (t < 30.0)
        q = s['q'][m]
        out[label] = dict(hip=[float(q[:, 0].mean()), float(q[:, 4].mean())],
                          thigh=[float(q[:, 1].mean()), float(q[:, 5].mean())],
                          knee=[float(q[:, 2].mean()), float(q[:, 6].mean())],
                          pitch_deg=float(grid.pitch_deg(s['quat'])[m].mean()))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, default=REPO / 'docs/exp/2026-10-18/flashsac_legscale_sim2sim')
    parser.add_argument('--signals', type=Path, required=True, help='large rollout signals (scratch dir)')
    parser.add_argument('--workers', type=int, default=10)
    args = parser.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    fixed = protocol()
    path = out / 'evaluation_protocol.json'
    if path.exists() and json.loads(path.read_text()) != json.loads(json.dumps(fixed)):
        raise SystemExit('evaluation_protocol.json differs; refusing to overwrite a fixed protocol')
    path.write_text(json.dumps(fixed, indent=2) + '\n')

    jobs = [j for p in fixed['policies'] for j in ab.jobs_for(p, acc.PHYSICS_SETS['cscale'], args.signals)]
    results = grid.run_jobs(jobs, args.workers, 'cscale_rollouts', out)
    report = ab.scenario_rows(results, args.signals)
    summary = summarize(report)
    chosen = {}
    for arm in ARMS:
        candidates = [p for p in fixed['policies'] if p['arm'] == arm]
        chosen[arm] = max(candidates, key=lambda p: (summary[p['label']]['gates_passed'],
                                                     -summary[p['label']]['mean_abs_zero_speed_mismatch'], p['step']))
    stand = posture(results, args.signals)
    (out / 'cscale_metrics.json').write_text(json.dumps(report, indent=2) + '\n')
    (out / 'cscale_summary.json').write_text(json.dumps(dict(summary=summary, selected=chosen, posture_k065=stand,
                                                             vendor_stand=VENDOR_STAND), indent=2) + '\n')
    print(f"{'policy':8s} {'gates':>9s} {'stress':>6s} {'mean|v0| k':>10s}  posture@k0.65 hip/thigh/knee (L,R) pitch  failures")
    for p in fixed['policies']:
        s, q = summary[p['label']], stand.get(p['label'])
        pose = (f"{np.round(q['hip'], 2).tolist()} {np.round(q['thigh'], 2).tolist()} {np.round(q['knee'], 2).tolist()} "
                f"{q['pitch_deg']:.1f}" if q else '-')
        print(f"{p['label']:8s} {s['gates_passed']:4d}/{s['gates_possible']:<4d} {s['stress_gates_passed']:6d} "
              f"{s['mean_abs_zero_speed_mismatch']:10.3f}  {pose}  {','.join(s['failures']) or '-'}")
    print('selected:', {arm: p['label'] for arm, p in chosen.items()})


if __name__ == '__main__':
    main()
