"""DESKTOP_DRY_RUN: summarize actual timing trials and draw fixed-origin comparisons."""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

MAIN = 'tita_flash_sac_115632_883848_model_60000'
REPO = Path(__file__).resolve().parents[1]
COLORS = {None: 'black', 0.: 'C0', .5: 'C1', 1.: 'C2', 1.2: 'C3', 2.: 'C4', 3.: 'C5'}


def label(delay):
    return 'FlashSAC only' if delay is None else f'RL + {delay:g} s'


def analyze(root):
    stages = {}
    policy_hashes = {}
    for stage in ['screen60', 'long300', 'finalists300']:
        folder = root / stage
        rows = json.loads((folder / 'results.json').read_text())
        executed_source = (folder / 'harness_source.py.txt').read_bytes()
        for row in rows:
            policy_hashes[row['job']['checkpoint_id']] = dict(checkpoint_sha256=row['checkpoint_sha256'],
                                                             onnx_sha256=row['onnx_sha256'])
            for path, expected in row['job']['source_hashes'].items():
                actual = executed_source if path == 'test/compare_velocity_bias_activation.py' else (REPO / path).read_bytes()
                assert hashlib.sha256(actual).hexdigest() == expected, (stage, path)
        groups = {}
        for row in rows:
            j = row['job']
            groups.setdefault((j['checkpoint_id'], j['condition'], j['seed']), {})[j['delay_s']] = row
        assert all(len({r['initial_physics_sha256'] for r in group.values()}) == 1 for group in groups.values())
        details = []
        for (checkpoint, condition, seed), group in groups.items():
            for delay, row in group.items():
                item = dict(checkpoint_id=checkpoint, condition=condition, seed=seed, delay_s=delay,
                            evidence_status=row['evidence_status'], gates=row.get('gates'), failure=row.get('failure'))
                for k in ['max_drift_from_rl_m', 'radial_IAE_from_rl_m_s', 'max_drift_from_2s_m',
                          'drift_at_2s_m', 'observed_speed_settled_rl_s', 'max_tilt_first2_rad',
                          'max_tilt_after2_rad', 'tail_speed_rms_m_s', 'first_eligible_rl_s',
                          'first_nonzero_bias_rl_s']:
                    item[k] = row.get(k)
                details.append(item)
        stages[stage] = dict(count=len(rows), complete=sum(r.get('complete', False) for r in rows),
                             quality_pass=sum(r['evidence_status'] == 'PASS' for r in rows),
                             errors=[r['job']['id'] for r in rows if r.get('error')],
                             all_initial_states_matched=True, all_source_hashes_matched=True, details=details)
        selected = [r for r in rows if r['job']['checkpoint_id'] == MAIN and r['job']['seed'] == 913]
        conditions = list(dict.fromkeys(r['job']['condition'] for r in selected))
        fig, axes = plt.subplots(len(conditions), 2, figsize=(13, 3.2 * len(conditions)), squeeze=False)
        for row in selected:
            j = row['job']
            path = folder / j['id'] / 'trace.npz'
            if not path.exists():
                continue
            trace = np.load(path)
            state = trace['state']
            t = np.arange(len(state)) * .02
            distance = np.linalg.norm(state[:, :2] - state[0, :2], axis=1) * 1000
            i, d = conditions.index(j['condition']), j['delay_s']
            axes[i, 0].plot(t, distance, color=COLORS[d], label=label(d))
            axes[i, 1].plot(t, state[:, 3] * 1000, color=COLORS[d], label=label(d))
            axes[i, 0].set_title(j['condition'] + ' / fixed RL-entry origin')
            axes[i, 1].set_title(j['condition'] + ' / first 10 seconds')
        for i in range(len(conditions)):
            for ax in axes[i]:
                ax.axvline(2., color='grey', linestyle=':', alpha=.8)
                ax.grid(alpha=.25)
                ax.set_xlabel('Time since transform_up -> RL (s)')
            axes[i, 0].set_ylabel('XY distance from RL entry (mm)')
            axes[i, 0].set_ylim(0, 150)
            axes[i, 1].set_ylabel('Actual forward velocity (mm/s)')
            axes[i, 1].set_xlim(0, 10)
            axes[i, 1].axhline(0, color='grey', linewidth=.5)
        axes[0, 0].legend(fontsize=8)
        fig.suptitle(f'VALIDATION_SIM / model_60000 / seed913 / {stage} / distance zoom 0-150 mm')
        fig.tight_layout(rect=(0., 0., 1., .96))
        fig.savefig(root / f'{stage}_comparison.png', dpi=150)
        plt.close(fig)
    (root / 'analysis.json').write_text(json.dumps(stages, indent=2, allow_nan=False) + '\n')
    (root / 'policy_hashes.json').write_text(json.dumps(policy_hashes, indent=2) + '\n')
    for stage in stages:
        print('[DESKTOP_DRY_RUN]', stage, 'completed', stages[stage]['complete'], '/', stages[stage]['count'],
              'quality PASS', stages[stage]['quality_pass'], 'errors', stages[stage]['errors'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    analyze(parser.parse_args().root)
