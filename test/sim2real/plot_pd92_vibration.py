"""DESKTOP_DRY_RUN: figure for the 2026-10-18 11:53 leg PD 92/2.3 vibration review.

Inputs are the outputs of ``analyze_pd_vibration.py`` (``pd_vibration_series.npz``) and the
``sim_pd_gain_latency_chatter.py`` excitation probe (``sim_excite_probe/results.json``).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review', type=Path, required=True, help='folder with pd_vibration_series.npz')
    args = parser.parse_args()
    review = args.review.resolve()
    assert review.is_relative_to(ROOT / 'docs/exp')
    s = np.load(review / 'pd_vibration_series.npz')
    fig, ax = plt.subplots(2, 2, figsize=(12, 7.5))

    # (a) left knee action in a neutral window, both gain sets.
    for lab, color in (('A80k_pd92', 'C3'), ('A80k_pd60', 'C0')):
        t, a, hold = s[f'{lab}__t'], s[f'{lab}__action'], s[f'{lab}__neutral_hold']
        i = np.flatnonzero(hold)[200]
        w = slice(i, i + 20)
        ax[0, 0].step((t[w] - t[i]) * 1e3, a[w, 2], where='post', color=color,
                      label=f"{lab.split('_')[1]}: 92/2.3" if lab.endswith('92') else 'pd60: 60/1.5')
    ax[0, 0].set(title='(a) left knee policy action, zero-command hold', xlabel='ms', ylabel='ONNX action')
    ax[0, 0].legend()

    # (b) left knee commanded torque around policy updates (pd92): tau_prev 2 ms before, tau_new at tick.
    t, tau, prev, hold = s['A80k_pd92__t'], s['A80k_pd92__tau'], s['A80k_pd92__tau_prev'], s['A80k_pd92__neutral_hold']
    i = np.flatnonzero(hold)[200]
    times, values = [], []
    for k in range(i, i + 20):
        times += [(t[k] - t[i]) * 1e3 - 2., (t[k] - t[i]) * 1e3]
        values += [prev[k, 2], tau[k, 2]]
    ax[0, 1].plot(times, values, 'C3.-')
    ax[0, 1].set(title='(b) left knee command torque, 92/2.3 (2 ms before / at each update)',
                 xlabel='ms', ylabel='N m')

    # (c) rolling knee |d action| since RL entry.
    for lab, color in (('A80k_pd92', 'C3'), ('A80k_pd60', 'C0')):
        t, a, rl = s[f'{lab}__t'], s[f'{lab}__action'], s[f'{lab}__rl']
        i0 = np.flatnonzero(rl)[0]
        end = i0 + np.flatnonzero(~rl[i0:])[0] if (~rl[i0:]).any() else len(t)
        da = np.abs(np.diff(a[i0:end], axis=0))[:, [2, 6]].mean(1)
        ax[1, 0].plot(t[i0 + 1:end] - t[i0], np.convolve(da, np.ones(25) / 25, mode='same'), color=color,
                      label='92/2.3' if lab.endswith('92') else '60/1.5 (first RL segment)')
    ax[1, 0].set(title='(c) knee |action step|, 0.5 s mean', xlabel='s since RL entry', ylabel='|da|')
    ax[1, 0].legend()

    # (d) 25 Hz joint-velocity response to the same command alternation: real vs MuJoCo probe.
    def alternation(x):
        return np.abs(np.mean((-1.) ** np.arange(len(x))[:, None] * (x - x.mean(0)), axis=0))
    dq, hold = s['A80k_pd92__dq'], s['A80k_pd92__neutral_hold']
    edges = np.flatnonzero(np.diff(np.r_[0, hold.astype(int), 0]))
    amps, weights = [], []
    for a, b in zip(edges[::2], edges[1::2]):
        if b - a >= 50:
            amps.append(alternation(dq[a:b]))
            weights.append(b - a)
    bars = {'real 92/2.3': np.average(amps, axis=0, weights=weights)}
    probe = {r['id']: r for r in json.loads((review / 'sim_excite_probe/results.json').read_text())}
    for key, label in (('g1.533_k1.00_d0_l0_s42_excite', 'sim k=1.0'), ('g1.533_k0.65_d0_l0_s42_excite', 'sim k=0.65'),
                       ('g1.533_k0.65_d2_l0_s42_excite', 'sim k=0.65 +4 ms')):
        bars[label] = np.array(probe[key]['dq_alt_amp'])
    groups = {'hip': [0, 4], 'thigh': [1, 5], 'knee': [2, 6]}
    x = np.arange(len(groups))
    for n, (label, value) in enumerate(bars.items()):
        ax[1, 1].bar(x + (n - 1.5) * .2, [value[g].mean() for g in groups.values()], .2, label=label)
    ax[1, 1].set_xticks(x, list(groups))
    ax[1, 1].set(title='(d) 25 Hz joint speed amplitude, same command alternation', ylabel='rad/s')
    ax[1, 1].legend()
    fig.tight_layout()
    fig.savefig(review / 'pd92_vibration.png', dpi=110)
    print('[DESKTOP_DRY_RUN] wrote', review / 'pd92_vibration.png')


if __name__ == '__main__':
    main()
