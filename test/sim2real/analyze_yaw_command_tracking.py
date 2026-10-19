"""DESKTOP_DRY_RUN: yaw-command tracking in copied real FlashSAC bags (read-only), focused on in-place turns.

Per run, samples with |wz cmd| > 0.1 rad/s are split into in-place (|vx cmd| < 0.05) and moving turns. Reported:
- gyro z (minus the run's pre-RL stationary gyro median) against the command: tracking ratio (least squares through 0),
  mean error, and lag (cross-correlation over the windows);
- wheel speed difference R-L: policy target (action x 20), measured, and the kinematic need wz * W / R with W the
  geometric wheel-centre width from MuJoCo forward kinematics of the logged legs;
- wheel torque command per side and the fraction at the 12 N m limit; encoder yaw rate / gyro (slip);
- leg posture (hip, thigh, knee means per side) and pitch.
No robot command.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3
import sys

import numpy as np
from rclpy.serialization import deserialize_message
from tita_controller.msg import TrainingSample

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyze_pd_vibration as pd  # noqa: E402
from compare_heading_sources import TrackWidth  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
POL = REPO / 'sim2real/tita_ws/src/tita_controller/policies'
R = 0.0925
RUNS = {
    'headw0_50k': ('docs/exp/2026-10-19/flashsac_headw0_50000_142158_review', 'flashsac_headw0_50000'),
    'headw0_65k': ('docs/exp/2026-10-19/flashsac_headw0_65000_153755_review', 'flashsac_headw0_65000'),
    'posma2_50k': ('docs/exp/2026-10-18/flashsac_posma2_50000_202450_review', 'flashsac_posma2_50000'),
    'posma2_75k': ('docs/exp/2026-10-18/flashsac_posma2_75000_210936_review', 'flashsac_posma2_75000'),
    'sphere1_90k': ('docs/exp/2026-10-19/sphere_hardware_review/raw', 'flashsac_sphere1_90000'),
    'sphere3_70k': ('docs/exp/2026-10-19/sphere_hardware_review/raw', 'flashsac_sphere3_70000'),
}


def load(folder, bundle):
    bag = next((REPO / folder).glob(f'{bundle}_*_bag'))
    cfg = json.loads((POL / bundle / 'config.json').read_text())
    d = pd.load(bag, cfg['policy_interface']['actions'])
    with sqlite3.connect(f"file:{d['db']}?mode=ro", uri=True) as c:
        tid = dict(c.execute('SELECT name,id FROM topics'))['/sim2real/training_sample']
        quat = np.array([deserialize_message(b, TrainingSample).quaternion_wxyz for b, in c.execute(
            'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', (tid,))])
    d['quat'] = quat
    return d


def analyze(name, folder, bundle, width):
    d = load(folder, bundle)
    rl = d['state'] == 'rl'
    t = (d['mono'] - d['mono'][0]) * 1e-9
    first = int(np.flatnonzero(rl)[0])
    still = (d['state'] == 'idle') & np.all(np.abs(d['dq']) < 0.02, axis=1)
    still[first:] = False
    bias = float(np.median(d['gyro'][still, 2])) if still.sum() > 20 else 0.
    gz = d['gyro'][:, 2] - bias
    cmd = d['command']
    q = d['q'].copy()
    q[:, [3, 7]] = np.unwrap(q[:, [3, 7]], axis=0)
    w, x, y, z = d['quat'].T
    pitch = np.arcsin(np.clip(2 * (w * y - z * x), -1, 1))
    pitch_rate = np.gradient(pitch, t)
    vL = d['dq'][:, 3] + pitch_rate + d['dq'][:, 1] + d['dq'][:, 2]
    vR = d['dq'][:, 7] + pitch_rate + d['dq'][:, 5] + d['dq'][:, 6]
    W = np.interp(np.arange(len(q)), np.arange(len(q))[::5], width(d['q'][::5]))
    enc_rate = R * (vR - vL) / W
    target_diff = d['target'][:, 7] - d['target'][:, 3]          # wheel velocity targets [rad/s]
    wheel_diff = d['dq'][:, 7] - d['dq'][:, 3]
    tau = d['tau']
    out = dict(run=name, bundle=bundle, gyro_bias_dps=float(np.degrees(bias)), rl_seconds=float(rl.sum() * .02))
    turning = rl & (np.abs(cmd[:, 2]) > 0.1)
    for label, m in [('in_place', turning & (np.abs(cmd[:, 0]) < 0.05)), ('moving', turning & (np.abs(cmd[:, 0]) >= 0.05))]:
        if m.sum() < 25:
            out[label] = dict(seconds=float(m.sum() * .02))
            continue
        c = cmd[m, 2]
        ratio = float(np.dot(gz[m], c) / np.dot(c, c))
        need = c * W[m] / R                                       # wheel diff needed without slip [rad/s]
        lags = list(range(0, 26))
        corr = [np.corrcoef(cmd[:, 2][np.flatnonzero(m)], gz[np.clip(np.flatnonzero(m) + k, 0, len(gz) - 1)])[0, 1]
                for k in lags]
        out[label] = dict(
            seconds=float(m.sum() * .02), cmd_abs_mean=float(np.abs(c).mean()), cmd_abs_max=float(np.abs(c).max()),
            gyro_over_cmd=ratio, err_abs_mean_dps=float(np.degrees(np.abs(gz[m] - c).mean())),
            lag_s=float(lags[int(np.argmax(corr))] * .02),
            target_diff_over_need=float(np.dot(target_diff[m], need) / np.dot(need, need)),
            wheel_diff_over_need=float(np.dot(wheel_diff[m], need) / np.dot(need, need)),
            encoder_over_gyro=float(np.dot(enc_rate[m], gz[m]) / np.dot(gz[m], gz[m])),
            wheel_tau_abs_mean=float(np.abs(tau[m][:, [3, 7]]).mean()),
            wheel_tau_abs_p95=float(np.percentile(np.abs(tau[m][:, [3, 7]]), 95)),
            wheel_tau_sat_frac=float((np.abs(tau[m][:, [3, 7]]) >= 12 - 1e-6).mean()),
            hip_deg=np.degrees(q[m][:, [0, 4]].mean(0)).round(2).tolist(),
            thigh_deg=np.degrees(q[m][:, [1, 5]].mean(0)).round(2).tolist(),
            knee_deg=np.degrees(q[m][:, [2, 6]].mean(0)).round(2).tolist(),
            pitch_deg=float(np.degrees(pitch[m]).mean()), W_m=float(W[m].mean()))
    return out, dict(t=t, rl=rl, cmd=cmd, gz=gz, enc=enc_rate, target_diff=target_diff, wheel_diff=wheel_diff,
                     tau=tau, W=W)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    width = TrackWidth()
    rows = []
    for name, (folder, bundle) in RUNS.items():
        row, signals = analyze(name, folder, bundle, width)
        rows.append(row)
        np.savez_compressed(a.out.parent / f'yaw_tracking_{name}.npz', **signals)
    a.out.write_text(json.dumps(dict(execution_domain='DESKTOP_DRY_RUN', runs=rows), indent=1))
    f = lambda v: '—' if v is None else f'{v:.2f}'
    print('run | kind | s | |cmd| mean/max | gyro/cmd | err dps | lag s | target/need | wheel/need | enc/gyro | |tau| mean/p95 sat | hip L/R | pitch')
    for r in rows:
        for k in ('in_place', 'moving'):
            v = r[k]
            if 'gyro_over_cmd' not in v:
                print(f"{r['run']:11s} {k:8s} {v['seconds']:5.1f}s (too short)")
                continue
            print(f"{r['run']:11s} {k:8s} {v['seconds']:5.1f}s | {f(v['cmd_abs_mean'])}/{f(v['cmd_abs_max'])} | {f(v['gyro_over_cmd'])} | "
                  f"{v['err_abs_mean_dps']:.1f} | {v['lag_s']:.2f} | {f(v['target_diff_over_need'])} | {f(v['wheel_diff_over_need'])} | "
                  f"{f(v['encoder_over_gyro'])} | {f(v['wheel_tau_abs_mean'])}/{f(v['wheel_tau_abs_p95'])} {v['wheel_tau_sat_frac']:.2f} | "
                  f"{v['hip_deg']} | {v['pitch_deg']:.1f}")


if __name__ == '__main__':
    main()
