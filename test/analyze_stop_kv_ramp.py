"""DESKTOP_DRY_RUN: rank completed paired kv/ramp simulation ablations."""

import argparse
from collections import defaultdict
import json
from pathlib import Path

import numpy as np


def condition(row):
    return row['scenario'], row['seed'], row['pitch'], row['duration_s']


def rank(rows):
    baseline = {condition(r): r for r in rows if r['kv'] == .5 and r['ramp_s'] == 1.}
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row['kv'], row['ramp_s'])].append(row)
    output = []
    for (kv, ramp), values in grouped.items():
        problems = []
        if len({condition(r) for r in values}) != len(values):
            raise ValueError('Duplicate experiment condition')
        for row in values:
            label = str(condition(row))
            ref = baseline.get(condition(row))
            if ref is None:
                problems.append(label + ':missing_baseline')
                continue
            if row['initial_hash'] != ref['initial_hash']:
                raise ValueError('Mismatched initial state')
            if row['failure'] or row['completed_s'] != row['duration_s']:
                problems.append(label + ':incomplete')
                continue
            for key, ratio in [('pitch_error_rms_rad', 1.1), ('pitch_rate_rms_rad_s', 1.25),
                               ('wheel_torque_rms_nm', 1.25)]:
                if row['metrics'][key] > ref['metrics'][key] * ratio:
                    problems.append(label + ':' + key)
        metric_keys = sorted(set.intersection(*(set(v['metrics']) for v in values)))
        means = {key: float(np.mean([v['metrics'][key] for v in values]))
                 for key in metric_keys if all(v['metrics'][key] is not None for v in values)}
        output.append(dict(kv=kv, ramp_s=ramp, trials=len(values), eligible=not problems,
            problems=problems, means=means))
    output.sort(key=lambda r: (not r['eligible'], r['means'].get('score', float('inf'))))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', nargs='+', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for directory in args.results:
        rows.extend(json.loads(l) for l in (directory / 'results.jsonl').read_text().splitlines())
    ranking = rank(rows)
    args.output.write_text(json.dumps(dict(execution_domain='DESKTOP_DRY_RUN',
        evidence_status='PASS', ranking=ranking), indent=2, allow_nan=False) + '\n')
    for r in ranking[:12]:
        print(r['kv'], r['ramp_s'], 'eligible', r['eligible'], 'n', r['trials'],
              'score', round(r['means'].get('score', -1), 5),
              'peak', round(r['means'].get('stop_planar_max_m', -1), 5),
              'reverse', round(r['means'].get('reverse_excursion_m', -1), 5))


if __name__ == '__main__':
    main()
