"""DESKTOP_DRY_RUN: how strongly each policy reacts to the x_err (wheel position error) observation, on real hold states.

Hold samples (zero command, >= 1 s after entry, every 5th tick, excluding the 65k run's 64-67 s and 100-104 s events)
are taken from the copied headw0 50k and 65k runs (``yaw_drift.npz``: reconstructed 35-d policy observations). For each
policy (bundle ONNX) the x_err entry (index 33, scale 5) is swept over -0.30 ... +0.10 m while the rest of the
observation is kept; reported per x_err: mean wheel velocity target (action x 20 -> m/s with R 0.0925, native wheel
indices 3/7) and mean thigh target (native 1/5, x 0.25 + offset). The slope between -0.25 and -0.05 m is the policy's
static position gain. No robot command.
usage: python compare_xerr_response.py --out JSON
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import onnxruntime as ort

REPO = Path(__file__).resolve().parents[2]
POL = REPO / 'sim2real/tita_ws/src/tita_controller/policies'
RUNS = {'run50k': 'docs/exp/2026-10-19/flashsac_headw0_50000_142158_review',
        'run65k': 'docs/exp/2026-10-19/flashsac_headw0_65000_153755_review'}
POLICIES = {'50k': 'flashsac_headw0_50000', '65k': 'flashsac_headw0_65000'}
EXCLUDE = {'run65k': [(64., 67.), (100., 104.)]}
R, X_INDEX, X_SCALE = .0925, 33, 5.
SWEEP = np.round(np.arange(-.30, .101, .05), 3)


def intervals(mask):
    e = np.flatnonzero(np.diff(np.r_[0, mask.astype(int), 0]))
    return list(zip(e[::2], e[1::2]))


def hold_obs(folder, run):
    z = np.load(REPO / folder / 'yaw_drift.npz')
    rl = z['rl'].astype(bool)
    zero = rl & np.all(np.abs(z['cmd']) <= [.02, .02, .03], axis=1)
    keep = np.zeros_like(zero)
    for a, b in intervals(zero):
        keep[a + 50:b] = True
    for lo, hi in EXCLUDE.get(run, []):
        keep &= ~((z['t'] >= lo) & (z['t'] < hi))
    idx = np.flatnonzero(keep)[::5]
    return z['obs'][idx].astype(np.float32)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    out = dict(execution_domain='DESKTOP_DRY_RUN', sweep_m=SWEEP.tolist(), results={})
    print('policy  states  | x_err: ' + ' '.join(f'{x:+.2f}' for x in SWEEP) + ' | gain')
    for pname, bundle in POLICIES.items():
        cfg = json.loads((POL / bundle / 'config.json').read_text())
        offsets = [t['offset'] for t in cfg['policy_interface']['actions']]
        session = ort.InferenceSession(str(POL / bundle / 'policy.onnx'), providers=['CPUExecutionProvider'])
        for run, folder in RUNS.items():
            obs = hold_obs(folder, run)
            wheel, thigh = [], []
            for x in SWEEP:
                o = obs.copy()
                o[:, X_INDEX] = x * X_SCALE
                act = np.array([session.run(['nn_output'], {'nn_input0': row[None]})[0].reshape(8) for row in o])
                wheel.append(float((act[:, [3, 7]].mean(1) * 20 * R).mean()))
                thigh.append(float(np.degrees((act[:, [1, 5]] * .25 + np.array(offsets)[[1, 5]]).mean())))
            sel = (SWEEP >= -.25 - 1e-9) & (SWEEP <= -.05 + 1e-9)
            gain = float(np.polyfit(SWEEP[sel], np.array(wheel)[sel], 1)[0])
            thigh_gain = float(np.polyfit(SWEEP[sel], np.array(thigh)[sel], 1)[0])
            out['results'][f'{pname}@{run}'] = dict(samples=int(len(obs)), wheel_target_m_s=wheel, thigh_target_deg=thigh,
                                                    wheel_gain_m_s_per_m=gain, thigh_gain_deg_per_m=thigh_gain)
            print(f'{pname:5s} {run}:{len(obs):4d} | wheel m/s ' + ' '.join(f'{w:+.3f}' for w in wheel)
                  + f' | {gain:+.2f} (m/s)/m')
            print(f'{"":5s} {"":11s}| thigh deg ' + ' '.join(f'{v:5.1f}' for v in thigh) + f' | {thigh_gain:+.1f} deg/m')
    a.out.write_text(json.dumps(out, indent=1) + '\n')


if __name__ == '__main__':
    main()
