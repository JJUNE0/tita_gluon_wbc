"""VALIDATION_SIM: post-hoc safety screen for a sim2real trial candidate among the A/B checkpoints.

Unlike the pre-registered gate-count selection (``evaluate_ab_policies.py``), this screen ranks
safety first. It was defined after seeing the stage-1 results and is written to
``screen_protocol.json`` before the extra stage-2 rollouts run:

1. no harness failure in any physics/scenario (stage 1 CoM set + stage 2 A/B/C set + replay);
2. no sustained standstill oscillation: zero-command pitch std <= 1 deg in nominal and the CoM-only
   physics (nominal leg strength);
3. startup pitch peak <= 10 deg in every physics;
4. among those, mean |zero-command speed| over the mismatch physics below R0's, lowest first.

Sim-only; a pass is a reason to consider a supervised trial, not evidence of real success.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import evaluate_ab_policies as ev
import flashsac_acceptance_suite as acc
import real2sim_leg_wheel_grid as grid

REPO = grid.REPO
ROOT = REPO / 'docs/exp/2026-10-18/flashsac_ab_sim2sim'
CANDIDATES = ['R0_60000', 'A_40k', 'A_70k', 'A_80k', 'B_40k', 'B_80k']
NOMINAL_LEG_PHYSICS = ['nominal', 'com_-2.0cm', 'com_-3.5cm', 'com_-5.0cm']
MISMATCH = ['com_-2.0cm', 'com_-3.5cm', 'com_-5.0cm', 'C_com2', 'A_imu2', 'B_com1_imu1']


def screen(label: str, stage1: dict, stage2: dict, replay: dict) -> dict:
    rows = {**stage1[label], **{k: v for k, v in stage2[label].items() if k not in stage1[label]}}
    failures = [f'{p}/{k}' for p, r in rows.items() for k, e in r.items() if e['evidence_status'] != 'PASS']
    failures += [f'replay/{p}' for p, e in replay[label].items() if e['evidence_status'] != 'PASS']
    oscillation = {p: rows[p]['zero__s104']['metrics']['main']['pitch_std'] for p in NOMINAL_LEG_PHYSICS
                   if rows[p]['zero__s104']['evidence_status'] == 'PASS'}
    startup = {p: r['zero__s104']['metrics']['startup']['peak_pitch_deg'] for p, r in rows.items()
               if r['zero__s104']['evidence_status'] == 'PASS'}
    zero = {p: rows[p]['zero__s104']['metrics']['main']['mean_speed'] for p in MISMATCH
            if rows[p]['zero__s104']['evidence_status'] == 'PASS'}
    return dict(failures=failures, max_standstill_pitch_std=max(oscillation.values()) if oscillation else None,
                max_startup_pitch_peak=max(startup.values()) if startup else None,
                zero_speed_mismatch=zero, mean_abs_zero_mismatch=float(np.mean(np.abs(list(zero.values())))),
                checks=dict(no_failure=not failures, no_oscillation=max(oscillation.values()) <= 1.0,
                            startup_pitch=max(startup.values()) <= 10.0))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--workers', type=int, default=6)
    args = parser.parse_args()
    out = ROOT / 'sim2real_screen'
    out.mkdir(parents=True, exist_ok=True)
    fixed = dict(execution_domain='VALIDATION_SIM', kind='post-hoc safety screen (defined after stage-1 results)',
                 candidates=CANDIDATES, rules=__doc__.split('\n\n')[1], nominal_leg_physics=NOMINAL_LEG_PHYSICS,
                 mismatch_physics=MISMATCH)
    path = out / 'screen_protocol.json'
    if path.exists() and json.loads(path.read_text()) != fixed:
        raise SystemExit('screen_protocol.json differs; refusing to overwrite')
    path.write_text(json.dumps(fixed, indent=2) + '\n')

    stage1 = json.loads((ROOT / 'stage1_metrics.json').read_text())
    stage2 = json.loads((ROOT / 'stage2_metrics.json').read_text())
    abc, replay = dict(stage2['abc']), dict(stage2['replay'])
    policies = {p['label']: p for p in ev.protocol()['policies']}
    missing = [c for c in CANDIDATES if c not in abc]
    jobs = [j for c in missing for j in ev.jobs_for(policies[c], acc.PHYSICS_SETS['abc'], out / 'signals')]
    for c in missing:
        for pname in ev.REPLAY['physics']:
            phys, imu = acc.PHYSICS_SETS['com'][pname]
            jobs.append(dict(id=f'{c}__{pname}__replay174421__s104', checkpoint=c, config_path=policies[c]['config'],
                             physics=phys, sensor=dict(imu_pitch_deg=imu), seed=104,
                             duration_s=ev.REPLAY['frames'] * grid.DT, command_npz=ev.REPLAY['command_npz'],
                             save_signals=True, output=str(out / 'signals')))
    if jobs:
        results = grid.run_jobs(jobs, args.workers, 'extra_stage2_rollouts', out)
        abc.update(ev.scenario_rows([r for r in results if 'replay174421' not in r['job']['id']], out / 'signals'))
        for r in results:
            if 'replay174421' in r['job']['id']:
                label, pname, _, _ = r['job']['id'].split('__')
                entry = dict(evidence_status=r['evidence_status'], failure=r.get('failure', []))
                if r['evidence_status'] == 'PASS':
                    entry.update(ev.replay_metrics(dict(np.load(out / 'signals' / f"{r['job']['id']}.npz"))))
                replay.setdefault(label, {})[pname] = entry
    report = {c: screen(c, stage1, abc, replay) for c in CANDIDATES}
    r0 = report['R0_60000']['mean_abs_zero_mismatch']
    for c, r in report.items():
        r['checks']['less_drift_than_R0'] = c != 'R0_60000' and r['mean_abs_zero_mismatch'] < r0
        r['passes_screen'] = all(r['checks'].values())
        r['replay'] = replay[c]
    passing = sorted((c for c, r in report.items() if r['passes_screen']), key=lambda c: report[c]['mean_abs_zero_mismatch'])
    (out / 'screen_results.json').write_text(json.dumps(dict(report=report, ranking=passing), indent=2) + '\n')
    print(f"{'candidate':10s} {'fail':>4s} {'osc std':>7s} {'startup':>7s} {'mean|v0|':>8s} checks")
    for c, r in report.items():
        print(f"{c:10s} {len(r['failures']):4d} {r['max_standstill_pitch_std']:7.2f} {r['max_startup_pitch_peak']:7.1f} "
              f"{r['mean_abs_zero_mismatch']:8.3f} {r['checks']} {'PASS' if r['passes_screen'] else ''}")
        if r['failures']:
            print('           failures:', ', '.join(r['failures']))
    print('ranking (screen pass, lowest drift first):', passing)


if __name__ == '__main__':
    main()
