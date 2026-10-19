"""VALIDATION_SIM: sim2sim evaluation and checkpoint selection for the A/B retraining arms.

Stage 1 (selection): reference R0 (115632/model_60000) and arm A/B checkpoints 40k-100k run the
separated acceptance scenarios of ``flashsac_acceptance_suite`` under the CoM physics set (nominal,
base CoM -2/-3.5/-5 cm, C). Per arm the checkpoint with the most passed gates is selected; ties go
to the lower mean |zero-command speed| over the four mismatch physics, then to the later step.
The rule is written to ``evaluation_protocol.json`` before any rollout.

Stage 2 (selected checkpoints + R0): the A/B/C physics set and a replay of the recorded 17:44:21
joystick command sequence (nominal, CoM -3.5 cm, C) as a realistic command profile. Replay metrics
compare policies inside the same sim physics; they are not a comparison with the real trajectory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

import flashsac_acceptance_suite as acc
import real2sim_leg_wheel_grid as grid

REPO = grid.REPO
EXPORTS = REPO / 'docs/exp/2026-10-18/flashsac_ab_sim2sim/exports'
REFERENCE = dict(label='R0_60000', config=str(REPO / 'docs/exp/2026-10-16/velocity_bias_overnight/exports/'
                                               'tita_flash_sac_115632_883848_model_60000/config.json'))
ARMS = {'A': 'tita_flash_sac_201940_278440', 'B': 'tita_flash_sac_201942_248862'}
STEPS = [40000, 50000, 60000, 70000, 80000, 90000, 100000]
MISMATCH = ['com_-2.0cm', 'com_-3.5cm', 'com_-5.0cm', 'C_com2']
REPLAY = dict(command_npz='docs/exp/2026-10-17/flashsac_60000_174421_torque_review/signals.npz', frames=1611,
              physics=['nominal', 'com_-3.5cm', 'C_com2'], windows=dict(W1=[7.71, 9.25], W2=[31.67, 32.19]))


def policies() -> list[dict]:
    rows = [dict(REFERENCE, arm='R0', step=60000)]
    for arm, run in ARMS.items():
        for step in STEPS:
            rows.append(dict(label=f'{arm}_{step // 1000}k', arm=arm, step=step,
                             config=str(EXPORTS / f'{run}_model_{step}' / 'config.json')))
    return rows


def protocol() -> dict:
    return dict(
        execution_domain='VALIDATION_SIM', policies=policies(),
        stage1=dict(physics=acc.PHYSICS_SETS['com'], scenarios=acc.SCENARIOS, criteria=acc.CRITERIA,
                    seeds=[104, 270], extra_seed_scenarios=['zero'],
                    selection='per arm: max total passed gates (a failed rollout fails all of its gates); '
                              'tie 1: min mean |zero-command v| (seed 104) over ' + ','.join(MISMATCH) +
                              '; tie 2: later step'),
        stage2=dict(physics=acc.PHYSICS_SETS['abc'], replay=REPLAY,
                    replay_metrics='W1/W2 mean speed; post-3 s mean |v - cmd_x| and |wz - cmd_wz| (sim GT/gyro)'),
        note='Sim-only screening; passing is not evidence of real-robot success.')


def jobs_for(policy: dict, physics_set: dict, out: Path, seeds=(104, 270)) -> list[dict]:
    jobs = []
    for pname, (phys, imu) in physics_set.items():
        for sname, spec in acc.SCENARIOS.items():
            for seed in seeds:
                if seed != seeds[0] and sname != 'zero':
                    continue
                job = dict(id=f"{policy['label']}__{pname}__{sname}__s{seed}", checkpoint=policy['label'],
                           config_path=policy['config'], physics=phys, sensor=dict(imu_pitch_deg=imu), seed=seed,
                           duration_s=spec['duration_s'], save_signals=True, output=str(out))
                if spec['command']:
                    job['command'] = spec['command']
                jobs.append(job)
    return jobs


def scenario_rows(results: list[dict], signals: Path) -> dict:
    report = {}
    for r in results:
        label, pname, sname, seed = r['job']['id'].split('__')
        entry = dict(evidence_status=r['evidence_status'], failure=r.get('failure', []))
        if r['evidence_status'] == 'PASS':
            s = dict(np.load(signals / f"{r['job']['id']}.npz"))
            metrics = acc.scenario_metrics(sname, s)
            spec = acc.SCENARIOS[sname]['command']
            entry.update(metrics=metrics, gates=acc.evaluate_gates(sname, metrics, spec['value'] if spec else None))
        report.setdefault(label, {}).setdefault(pname, {})[f'{sname}__{seed}'] = entry
    return report


def gate_total(entry: dict, sname: str) -> tuple[int, int]:
    """(passed, possible) for one scenario; a failed rollout fails every gate of its scenario."""
    possible = {'zero': 5}.get(sname, 3)
    if entry['evidence_status'] != 'PASS':
        return 0, possible
    return sum(entry['gates'].values()), len(entry['gates'])


def summarize(report: dict) -> dict:
    summary = {}
    for label, by_physics in report.items():
        passed = possible = 0
        zero = []
        failures = []
        for pname, rows in by_physics.items():
            for key, entry in rows.items():
                sname = key.split('__')[0]
                p, n = gate_total(entry, sname)
                passed, possible = passed + p, possible + n
                if entry['evidence_status'] != 'PASS':
                    failures.append(f'{pname}/{key}')
                if sname == 'zero' and key.endswith('s104') and pname in MISMATCH:
                    zero.append(abs(entry['metrics']['main']['mean_speed']) if entry['evidence_status'] == 'PASS' else 9.9)
        summary[label] = dict(gates_passed=passed, gates_possible=possible, failures=failures,
                              mean_abs_zero_speed_mismatch=float(np.mean(zero)) if zero else None)
    return summary


def select(summary: dict, protocol_policies: list[dict]) -> dict:
    chosen = {}
    for arm in ARMS:
        candidates = [p for p in protocol_policies if p['arm'] == arm]
        best = max(candidates, key=lambda p: (summary[p['label']]['gates_passed'],
                                              -summary[p['label']]['mean_abs_zero_speed_mismatch'], p['step']))
        chosen[arm] = best
    return chosen


def replay_metrics(signals: dict) -> dict:
    t = np.arange(len(signals['speed'])) * grid.DT
    cmd = signals['command']
    out = {}
    for name, (a, b) in REPLAY['windows'].items():
        m = (t >= a - 1e-6) & (t <= b + 1e-6)
        out[f'{name}_mean_speed'] = float(signals['speed'][m].mean())
    post3 = t >= 3.0
    out['post3_mean_abs_v_err'] = float(np.mean(np.abs(signals['speed'][post3] - cmd[post3, 0])))
    out['post3_mean_abs_wz_err'] = float(np.mean(np.abs(signals['gyro'][post3, 2] - cmd[post3, 2])))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, default=REPO / 'docs/exp/2026-10-18/flashsac_ab_sim2sim')
    parser.add_argument('--stage1-signals', type=Path, required=True, help='large stage-1 rollouts (scratch dir)')
    parser.add_argument('--workers', type=int, default=12)
    args = parser.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    fixed = protocol()
    path = out / 'evaluation_protocol.json'
    if path.exists() and json.loads(path.read_text()) != json.loads(json.dumps(fixed)):
        raise SystemExit('evaluation_protocol.json differs; refusing to overwrite a fixed protocol')
    path.write_text(json.dumps(fixed, indent=2) + '\n')

    # Stage 1: selection under the CoM physics set.
    jobs = [j for p in fixed['policies'] for j in jobs_for(p, acc.PHYSICS_SETS['com'], args.stage1_signals)]
    stage1 = scenario_rows(grid.run_jobs(jobs, args.workers, 'stage1_rollouts', out), args.stage1_signals)
    summary = summarize(stage1)
    chosen = select(summary, fixed['policies'])
    (out / 'stage1_metrics.json').write_text(json.dumps(stage1, indent=2) + '\n')
    (out / 'stage1_summary.json').write_text(json.dumps(dict(summary=summary, selected=chosen), indent=2) + '\n')
    print(f"{'policy':10s} {'gates':>9s} {'mean|v0| mismatch':>18s} failures")
    for p in fixed['policies']:
        s = summary[p['label']]
        print(f"{p['label']:10s} {s['gates_passed']:4d}/{s['gates_possible']:<4d} {s['mean_abs_zero_speed_mismatch']:18.3f} "
              f"{','.join(s['failures']) or '-'}")
    print('selected:', {arm: p['label'] for arm, p in chosen.items()})

    # Stage 2: A/B/C physics and the recorded-command replay for R0 and the selected checkpoints.
    finalists = [fixed['policies'][0]] + [chosen[arm] for arm in ARMS]
    stage2_dir = out / 'stage2_signals'
    jobs = [j for p in finalists for j in jobs_for(p, acc.PHYSICS_SETS['abc'], stage2_dir)]
    for p in finalists:
        for pname in REPLAY['physics']:
            phys, imu = acc.PHYSICS_SETS['com'][pname]
            jobs.append(dict(id=f"{p['label']}__{pname}__replay174421__s104", checkpoint=p['label'], config_path=p['config'],
                             physics=phys, sensor=dict(imu_pitch_deg=imu), seed=104,
                             duration_s=REPLAY['frames'] * grid.DT, command_npz=REPLAY['command_npz'],
                             save_signals=True, output=str(stage2_dir)))
    results = grid.run_jobs(jobs, args.workers, 'stage2_rollouts', out)
    abc = scenario_rows([r for r in results if 'replay174421' not in r['job']['id']], stage2_dir)
    replay = {}
    for r in results:
        if 'replay174421' not in r['job']['id']:
            continue
        label, pname, _, _ = r['job']['id'].split('__')
        entry = dict(evidence_status=r['evidence_status'], failure=r.get('failure', []))
        if r['evidence_status'] == 'PASS':
            entry.update(replay_metrics(dict(np.load(stage2_dir / f"{r['job']['id']}.npz"))))
        replay.setdefault(label, {})[pname] = entry
    (out / 'stage2_metrics.json').write_text(json.dumps(dict(abc=abc, abc_summary=summarize(abc), replay=replay),
                                                        indent=2) + '\n')
    for label, rows in replay.items():
        for pname, e in rows.items():
            print(f'replay {label:10s} {pname:12s}', {k: round(v, 3) if isinstance(v, float) else v for k, v in e.items()})


if __name__ == '__main__':
    main()
