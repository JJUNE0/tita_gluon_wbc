"""DESKTOP_DRY_RUN: audit the paired stop benchmark and plot saved evidence."""
import argparse
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    groups = ['nominal_matrix_t3', 'nominal_matrix_t8', 'nominal_matrix_t12', 'final_mismatch']
    trials = []
    for group in groups:
        rows = json.loads((args.root/group/'results.json').read_text())
        pairs = {}
        for row in rows:
            key = row['domain'], row['seed'], row['prefix_s'], row['motion']
            pairs.setdefault(key, []).append(row)
            signals = np.load(args.root/group/(row['id']+'.npz'))['rows']
            post = signals[:, 0] >= 0
            assert np.isfinite(signals).all()
            np.testing.assert_allclose(max(0, -signals[post, 7].min()), row['max_downward_speed_m_s'], atol=1e-12)
            np.testing.assert_allclose(signals[post, -1].max(), row['peak_floor_normal_n'], atol=1e-12)
            assert (abs(signals[:, 30:38]) <= np.array([60, 60, 60, 12, 60, 60, 60, 12])+1e-9).all()
            trials.append(dict(group=group, **row))
        for pair in pairs.values():
            assert len(pair) == 4
            assert len({r['initial_state_sha256'] for r in pair}) == 1
            assert len({r['physics_sha256'] for r in pair}) == 1
    reference = args.root/'nominal_matrix_t8'
    repeated = args.root/'repeat_nominal'
    max_repeat_error = 0.
    for path in repeated.glob('*.npz'):
        original = np.load(reference/path.name)
        repeat = np.load(path)
        for name in ['rows', 'qpos', 'qvel', 'sample_times']:
            assert original[name].shape == repeat[name].shape
            max_repeat_error = max(max_repeat_error, float(abs(original[name]-repeat[name]).max()))
    assert max_repeat_error == 0.
    summary = dict(execution_domain='DESKTOP_DRY_RUN', source_domain='VALIDATION_SIM',
                   evidence_status='PASS', paired_trials=len(trials),
                   matched_initial_states=True, finite_and_torque_bounds=True,
                   repeated_trace_max_error=max_repeat_error, groups={})
    for domain in ['nominal', 'fitted_A', 'fitted_B', 'fitted_C']:
        for family in ['baseline', 'candidate']:
            selected = [r for r in trials if r['domain'] == domain and r['mode'].startswith(family)]
            summary['groups'][domain+'_'+family] = dict(
                count=len(selected), acceptance_pass=sum(r['acceptance_status'] == 'PASS' for r in selected),
                downward_speed_range_m_s=[min(r['max_downward_speed_m_s'] for r in selected), max(r['max_downward_speed_m_s'] for r in selected)],
                peak_contact_range_n=[min(r['peak_floor_normal_n'] for r in selected), max(r['peak_floor_normal_n'] for r in selected)],
                peak_tilt_range_deg=[min(r['peak_tilt_deg'] for r in selected), max(r['peak_tilt_deg'] for r in selected)])
    (args.root/'benchmark_summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    fields = ['group', 'id', 'domain', 'mode', 'seed', 'prefix_s', 'acceptance_status',
              'max_downward_speed_m_s', 'peak_floor_normal_n', 'peak_tilt_deg',
              'tail_horizontal_speed_m_s', 'max_horizontal_displacement_m']
    with (args.root/'benchmark.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader(); writer.writerows(trials)
    modes = ['baseline_estop', 'baseline_return', 'candidate_com_estop', 'candidate_com_return']
    labels = ['Current damping stop', 'Current return', 'Candidate controlled stop', 'Candidate return']
    fig, axes = plt.subplots(4, 1, figsize=(12, 11), sharex=True, constrained_layout=True)
    for mode, label in zip(modes, labels):
        a = np.load(reference/f'nominal_neutral_s42_t8_{mode}.npz')['rows']
        axes[0].plot(a[:, 0], a[:, 4], label=label)
        axes[1].plot(a[:, 0], a[:, 7], label=label)
        axes[2].plot(a[:, 0], np.degrees(a[:, 9]), label=label)
        axes[3].plot(a[:, 0], a[:, -1], label=label)
    axes[0].set_ylabel('Body height (m)')
    axes[1].set_ylabel('Vertical velocity (m/s)')
    axes[2].set_ylabel('Pitch (degrees)')
    axes[3].set_ylabel('Floor normal sum (N)')
    axes[3].set_xlabel('Seconds from stop request')
    for axis in axes:
        axis.axvline(0, color='black', ls=':'); axis.grid(alpha=.2)
        axis.set_xlim(-.3, 6.)
        axis.legend(fontsize=8)
    fig.suptitle('VALIDATION_SIM: matched native baseline and simulation-only candidate')
    fig.savefig(args.root/'paired_nominal_metrics.png', dpi=160)
    plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
