"""DESKTOP_DRY_RUN: paired physical drift plots, with explicit incomplete-batch labels."""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--stage', default='physics02')
    parser.add_argument('--mode', default='v02')
    args = parser.parse_args()
    root = args.root.resolve()
    rows = json.loads((root / f'{args.stage}_results.json').read_text())
    by_id = {row['job']['id']: row for row in rows}
    pairs = []
    for row in rows:
        if f'_nominal_{args.mode}_' not in row['job']['id']:
            continue
        baseline = by_id.get(row['job']['id'].replace(f'_{args.mode}_', '_baseline_'))
        if baseline and row.get('complete') and baseline.get('complete'):
            pairs.append((baseline, row))
    pairs.sort(key=lambda pair: (pair[1]['job']['checkpoint_id'].rsplit('_model_', 1)[0],
                                int(pair[1]['job']['checkpoint_id'].rsplit('_model_', 1)[1])))
    if not pairs:
        raise RuntimeError('No completed nominal pairs')
    labels = [f'{"A" if "115632" in c["job"]["checkpoint_id"] else "B"}/{c["job"]["checkpoint_id"].rsplit("_", 1)[1]}'
              for _, c in pairs]
    fig, axes = plt.subplots(2, 1, figsize=(16, 9), constrained_layout=True)
    x = np.arange(len(pairs))
    axes[0].bar(x - .18, [b['tail_speed_mean_m_s'] * 1000 for b, _ in pairs], .36, label='FlashSAC')
    axes[0].bar(x + .18, [c['tail_speed_mean_m_s'] * 1000 for _, c in pairs], .36, label='FlashSAC + velocity bias')
    axes[0].axhline(0., color='black', linewidth=.6)
    axes[0].set_ylabel('Last-20-s mean chassis speed [mm/s]')
    axes[0].legend()
    axes[1].bar(x - .18, [b['max_drift_m'] for b, _ in pairs], .36, label='FlashSAC')
    axes[1].bar(x + .18, [c['max_drift_m'] for _, c in pairs], .36, label='FlashSAC + velocity bias')
    axes[1].set_yscale('log')
    axes[1].axhline(.25, color='black', linestyle='--', linewidth=.8, label='60 s gate: 0.25 m')
    axes[1].set_ylabel('Maximum distance from initial position [m]')
    axes[1].legend()
    for axis in axes:
        axis.set_xticks(x, labels, rotation=70, fontsize=8)
        axis.grid(axis='y', alpha=.25)
    state = 'COMPLETE' if len(pairs) == 40 else f'PARTIAL: {len(pairs)}/40 nominal pairs'
    seed = pairs[0][1]['job']['seed']
    fig.suptitle(f'{state} | 60 s, zero command, flat floor, seed {seed} | physical MuJoCo chassis metrics')
    suffix = '' if args.stage == 'physics02' and args.mode == 'v02' else '_' + args.mode
    fig.savefig(root / ('nominal_paired_overview' + suffix + '.png'), dpi=160)
    plt.close(fig)

    cases = [('tita_flash_sac_115632_883848_model_10000_mass130', 'Changed mass: +30%, checkpoint A/10000'),
             ('tita_flash_sac_115632_883848_model_25000_friction02', 'Low friction: 0.2, checkpoint A/25000')]
    for key, title in cases:
        row = next((r for r in rows if r['job']['id'].startswith(key + '_' + args.mode + '_')), None)
        baseline = by_id.get(row['job']['id'].replace('_' + args.mode + '_', '_baseline_')) if row else None
        if not row or not baseline or not row.get('complete') or not baseline.get('complete'):
            continue
        fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True, constrained_layout=True)
        for result, label in [(baseline, 'FlashSAC'), (row, 'FlashSAC + velocity bias')]:
            with np.load(root / args.stage / result['job']['id'] / 'trace.npz') as trace:
                state, inputs = trace['state'], trace['input']
                time = np.arange(len(state)) * .02
                distance = np.linalg.norm(state[:, :2] - trace['origin'][:2], axis=1)
                axes[0].plot(time, distance, label=label)
                axes[1].plot(time, state[:, 3], label=label + ': chassis')
                if result is row:
                    axes[1].plot(time, state[:, 10], alpha=.6, label='Encoder/IMU finite-difference FK estimate')
                    axes[2].plot(time[:-1], inputs[:, 0], label='Velocity target bias')
        axes[0].set_ylabel('Radial displacement [m]')
        axes[1].set_ylabel('Forward speed [m/s]')
        axes[2].set_ylabel('Bias [m/s]')
        axes[2].set_xlabel('Time after common 1.2 s RL acquisition [s]')
        for axis in axes:
            axis.legend(loc='upper right')
            axis.grid(alpha=.25)
        fig.suptitle(title + '\nFinite completion is separate from vibration/observation quality gates')
        fig.savefig(root / (key + '_diagnostic' + suffix + '.png'), dpi=150)
        plt.close(fig)
    print('[DESKTOP_DRY_RUN] Saved paired plot and available failure diagnostics. Nominal pairs:', len(pairs))


if __name__ == '__main__':
    main()
