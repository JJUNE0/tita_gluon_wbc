"""DESKTOP_DRY_RUN: audit completion separately from physical control and observation gates."""

import argparse
import json
from pathlib import Path

import numpy as np


def pair_key(job):
    return json.dumps([job['checkpoint_id'], job.get('physics', {}), job.get('kick', 0.), job.get('seed'),
                       job.get('pitch', 0.), job.get('warmup', 8.), job['duration']], sort_keys=True)


def analyze(root, stage, baseline_stage=None):
    rows = json.loads((root / f'{stage}_results.json').read_text())
    planned = json.loads((root / f'{stage}_jobs.json').read_text())
    items = []
    for row in rows:
        item = dict(id=row['job']['id'], checkpoint_sha256=row.get('checkpoint_sha256'),
                    job=row['job'], completion_status=row['evidence_status'], complete=row.get('complete', False),
                    failure=row.get('failure', []), error=row.get('error'))
        for key in ['max_drift_m', 'final_drift_m', 'tail_speed_mean_m_s', 'tail_speed_rms_m_s',
                    'radial_IAE_m_s', 'initial_physics_sha256', 'peak_tilt_rad']:
            item[key] = row.get(key)
        path = root / stage / item['id'] / 'trace.npz'
        if path.exists():
            with np.load(path) as trace:
                state = trace['state']
                tail = np.arange(len(state)) * .02 >= max(0., row['job']['duration'] - 20.)
                discrepancy = state[:, 10] - state[:, 3]
                item['max_yaw_excursion_deg'] = float(np.max(abs(np.unwrap(state[:, 6]) - state[0, 6])) * 180. / np.pi)
                item['sensor_tail_rms_error_m_s'] = float(np.sqrt(np.mean(discrepancy[tail]**2))) if tail.any() else None
                item['observation_gate'] = bool(tail.any() and item['sensor_tail_rms_error_m_s'] <= .05)
                item['net_longitudinal_path_m'] = float(np.trapz(state[:, 3], dx=.02))
                item['absolute_longitudinal_path_m'] = float(np.trapz(abs(state[:, 3]), dx=.02))
        item['speed_gate'] = bool(item['complete'] and abs(item['tail_speed_mean_m_s']) <= .005
                                  and item['tail_speed_rms_m_s'] <= .02)
        position_limit = .25 if row['job']['duration'] <= 60. else .5
        item['position_gate'] = bool(item['complete'] and item['max_drift_m'] <= position_limit)
        item['control_gate'] = bool(item['speed_gate'] and item['position_gate'] and item.get('observation_gate'))
        items.append(item)
    baselines = {}
    baseline_items = items
    if baseline_stage:
        external = json.loads((root / f'{baseline_stage}_results.json').read_text())
        baseline_items = items + [dict(row, id=row['job']['id'], complete=row.get('complete', False)) for row in external]
    for item in baseline_items:
        job = item['job']
        key = pair_key(job)
        if job['law'].get('mode') == 'constant' and job['law'].get('bias', 0.) == 0.:
            baselines[key] = item
    for item in items:
        job = item['job']
        key = pair_key(job)
        if job['law'].get('mode') == 'constant':
            continue
        baseline = baselines.get(key)
        if baseline:
            item['baseline_id'] = baseline['id']
            item['baseline_stage'] = baseline_stage or stage
            item['new_failure_vs_baseline'] = baseline['complete'] and not item['complete']
            item['identical_initial_physics'] = (item['initial_physics_sha256'] is not None
                                                and item['initial_physics_sha256'] == baseline['initial_physics_sha256'])
            if baseline['complete'] and item['complete']:
                item['max_drift_improvement_fraction'] = 1. - item['max_drift_m'] / max(baseline['max_drift_m'], 1e-12)
                item['IAE_improvement_fraction'] = 1. - item['radial_IAE_m_s'] / max(baseline['radial_IAE_m_s'], 1e-12)
    controls = [i for i in items if i['job']['law'].get('mode') != 'constant']
    audit = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='SUSPICIOUS', stage=stage,
                 baseline_stage=baseline_stage,
                 planned_trials=len(planned), batch_complete=len(rows) == len(planned),
                 trials=len(items), controls=len(controls), completed=sum(i['complete'] for i in controls),
                 speed_pass=sum(i['speed_gate'] for i in controls), position_pass=sum(i['position_gate'] for i in controls),
                 control_pass=sum(i['control_gate'] for i in controls),
                 initial_state_mismatches=sum(i.get('baseline_id') is not None
                    and i.get('initial_physics_sha256') is not None and not i.get('identical_initial_physics') for i in controls),
                 new_failures_vs_baseline=sum(i.get('new_failure_vs_baseline', False) for i in controls),
                 rows=items)
    if not audit['batch_complete']:
        audit['evidence_status'] = 'NOT_TESTED'
    elif (controls and audit['control_pass'] == len(controls) and not audit['new_failures_vs_baseline']
          and not audit['initial_state_mismatches']):
        audit['evidence_status'] = 'PASS'
    (root / f'{stage}_audit.json').write_text(json.dumps(audit, indent=2, allow_nan=False) + '\n')
    print('[DESKTOP_DRY_RUN]', stage, {k: v for k, v in audit.items() if k != 'rows'})
    return audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--stages', nargs='+', required=True)
    parser.add_argument('--baseline-stage')
    args = parser.parse_args()
    for stage in args.stages:
        analyze(args.root, stage, args.baseline_stage)


if __name__ == '__main__':
    main()
