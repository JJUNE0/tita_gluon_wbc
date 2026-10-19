"""DESKTOP_DRY_RUN: same-checkpoint, same-initial-state Flash/M4/velocity-PI comparison."""

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
    parser.add_argument('--velocity-mode', choices=['v02', 'v03', 'v04'], default='v02')
    args = parser.parse_args()
    root = args.root.resolve()
    stages = ['primary_m4_comparison', 'primary_m4_comparison02', 'long_physics01', 'seeded_primary01', 'rate3_primary01']
    available = {}
    for stage in stages:
        path = root / f'{stage}_results.json'
        if path.exists():
            for row in json.loads(path.read_text()):
                if row.get('complete'):
                    available[row['job']['id']] = stage, row
    checkpoint = 'tita_flash_sac_115632_883848_model_60000'
    conditions = [('nominal', 'Nominal'), ('mass115', 'Mass +15%'), ('mass130', 'Mass +30%')]
    selected = []
    for key, title in conditions:
        group = []
        velocity_label = 'FlashSAC + seeded velocity bias' if args.velocity_mode != 'v02' else 'FlashSAC + velocity PI'
        for mode, label in [('baseline', 'FlashSAC'), ('m4', 'FlashSAC + Fixed M4'), (args.velocity_mode, velocity_label)]:
            identity = f'{checkpoint}_{key}_{mode}_s913_300s'
            if identity not in available:
                print('[DESKTOP_DRY_RUN] NOT_TESTED: waiting for', identity)
                return
            stage, row = available[identity]
            group.append((stage, row, label))
        assert len({row['initial_physics_sha256'] for _, row, _ in group}) == 1, key
        selected.append((title, group))
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True, constrained_layout=True)
    metrics = []
    for col, (title, group) in enumerate(selected):
        for stage, row, label in group:
            with np.load(root / stage / row['job']['id'] / 'trace.npz') as trace:
                state = trace['state']
                time = np.arange(len(state)) * .02
                distance = np.linalg.norm(state[:, :2] - trace['origin'][:2], axis=1)
                axes[0, col].semilogy(time, np.maximum(distance, 1e-5), label=label)
                axes[1, col].plot(time, state[:, 3] * 1000, label=label, linewidth=.8)
            metrics.append(dict(condition=title, controller=label, stage=stage, checkpoint_sha256=row['checkpoint_sha256'],
                onnx_sha256=row['onnx_sha256'], initial_physics_sha256=row['initial_physics_sha256'],
                final_drift_m=row['final_drift_m'], max_drift_m=row['max_drift_m'],
                radial_IAE_m_s=row['radial_IAE_m_s'], tail_mean_speed_m_s=row['tail_speed_mean_m_s'],
                tail_speed_rms_m_s=row['tail_speed_rms_m_s'],
                max_yaw_excursion_deg=float(np.max(abs(np.unwrap(state[:, 6]) - state[0, 6])) * 180. / np.pi)))
        axes[0, col].set_title(title)
        axes[0, col].set_ylim(1e-4, 100.)
        axes[0, col].grid(alpha=.25)
        axes[1, col].axhline(0., color='black', linewidth=.5)
        axes[1, col].grid(alpha=.25)
        axes[1, col].set_xlabel('Time after common acquisition [s]')
    axes[0, 0].set_ylabel('Distance from initial position [m], log scale')
    axes[1, 0].set_ylabel('Physical chassis forward speed [mm/s]')
    axes[0, 0].legend(loc='upper left', fontsize=8)
    fig.suptitle('Same FlashSAC model_60000 | 300 s zero command | seed 913 | fixed physics before startup')
    filename = {'v02': 'primary_three_way_300s', 'v03': 'primary_three_way_seeded_300s',
                'v04': 'primary_three_way_rate3_300s'}[args.velocity_mode]
    fig.savefig(root / (filename + '.png'), dpi=170)
    plt.close(fig)
    result = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
                  detail='Paired comparison audit, not a claim that every controller passes station-keeping gates', rows=metrics)
    (root / (filename + '.json')).write_text(json.dumps(result, indent=2) + '\n')
    print('[DESKTOP_DRY_RUN] PASS: nine completed matched-initial-state runs; saved primary three-way comparison.')


if __name__ == '__main__':
    main()
