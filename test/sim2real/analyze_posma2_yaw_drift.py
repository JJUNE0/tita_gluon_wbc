"""DESKTOP_DRY_RUN: zero-command yaw/x drift in a copied posma2 FlashSAC bag (read-only).

Heading sources (all recorded telemetry, no robot command):
- IMU quaternion yaw (vendor attitude filter, unwrapped),
- gyro z integral (body frame, small-tilt approximation),
- encoder differential: R * (v_R - v_L) / W with v_side = dq_wheel + pitch_rate + dq_thigh + dq_knee.
  W is fitted against gyro z on yaw-commanded samples, so it is an effective track width.
x: policy observation 33 (wheel_position_error * 5) and the same encoder odometry recomputed.
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

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / 'sim2real/tita_ws/src/tita_controller/policies/flashsac_posma2_50000/config.json'
R = 0.0925
ZERO = np.array([.02, .02, .03])


def quat_ypr(q):
    w, x, y, z = q.T
    yaw = np.arctan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
    pitch = np.arcsin(np.clip(2 * (w * y - z * x), -1, 1))
    roll = np.arctan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    return np.unwrap(yaw), pitch, roll


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('bag', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--settle', type=float, default=1.0, help='s after entering zero command')
    ap.add_argument('--config', type=Path, default=CONFIG, help='같은 34-obs 인터페이스의 정책 config.json')
    a = ap.parse_args()
    cfg = json.loads(a.config.read_text())
    d = pd.load(a.bag, cfg['policy_interface']['actions'])
    with sqlite3.connect(f"file:{d['db']}?mode=ro", uri=True) as c:
        tid = dict(c.execute('SELECT name,id FROM topics'))['/sim2real/training_sample']
        samples = [deserialize_message(b, TrainingSample) for b, in c.execute(
            'SELECT data FROM messages WHERE topic_id=? ORDER BY timestamp', (tid,))]
    obs = np.array([s.observation for s in samples], dtype=float)
    quat = np.array([s.quaternion_wxyz for s in samples])
    rl = d['state'] == 'rl'
    assert obs.shape[1] in (34, 35), obs.shape        # 35: + gyro heading_error (scale 2) last
    t = (d['mono'] - d['mono'][rl][0]) * 1e-9
    dt = np.r_[.02, np.diff(t)]
    yaw, pitch, roll = quat_ypr(quat)
    gz = d['gyro'][:, 2]
    q, dq = d['q'].copy(), d['dq']
    q[:, [3, 7]] = np.unwrap(q[:, [3, 7]], axis=0)   # wheel encoders wrap at +/-pi (adapter.hpp unwraps too)
    pitch_rate = np.gradient(pitch, t)
    # Per-side ground rolling velocity and distance (sign c=+1 verified in MuJoCo).
    vL = dq[:, 3] + pitch_rate + dq[:, 1] + dq[:, 2]
    vR = dq[:, 7] + pitch_rate + dq[:, 5] + dq[:, 6]
    sL = R * (q[:, 3] + pitch + q[:, 1] + q[:, 2])
    sR = R * (q[:, 7] + pitch + q[:, 5] + q[:, 6])
    s = .5 * (sL + sR)
    cmd = d['command']
    zero = np.all(np.abs(cmd) <= ZERO, axis=1)
    x_obs = obs[:, 33] / 5.

    # Effective track width from yawing samples: gz = R (vR - vL) / W.
    yawing = rl & (np.abs(cmd[:, 2]) > .1) & (np.abs(gz) > .1)
    k_fit = float(np.linalg.lstsq((R * (vR - vL))[yawing, None], gz[yawing], rcond=None)[0][0]) \
        if yawing.sum() > 20 else float('nan')
    W = 1. / k_fit if np.isfinite(k_fit) and k_fit else float('nan')
    gz_enc = R * (vR - vL) / W if np.isfinite(W) else np.full_like(gz, np.nan)
    corr = float(np.corrcoef(gz[yawing], gz_enc[yawing])[0, 1]) if yawing.sum() > 20 else float('nan')

    segs = []
    settled = np.zeros(len(t), bool)
    for i0, i1 in pd.runs(rl & zero):
        tt = t[i0:i1]
        if tt[-1] - tt[0] < a.settle + 1.:
            continue
        j0 = i0 + int(np.searchsorted(tt - tt[0], a.settle))
        sl = slice(j0, i1)
        settled[sl] = True
        dur = float(t[i1 - 1] - t[j0])
        gyro_int = float(np.sum(gz[sl] * dt[sl]))
        enc_int = float(np.nansum(gz_enc[sl] * dt[sl]))
        yaw_d = float(yaw[i1 - 1] - yaw[j0])
        segs.append(dict(
            t0=float(t[j0]), t1=float(t[i1 - 1]), duration_s=dur,
            yaw_quat_deg=np.degrees(yaw_d), yaw_gyro_int_deg=np.degrees(gyro_int),
            yaw_encoder_int_deg=np.degrees(enc_int),
            yaw_rate_mean_dps=np.degrees(yaw_d / dur) if dur > 0 else float('nan'),
            gz_mean_dps=float(np.degrees(gz[sl].mean())),
            x_obs_m=dict(start=float(x_obs[j0]), end=float(x_obs[i1 - 1]),
                         min=float(x_obs[sl].min()), max=float(x_obs[sl].max())),
            s_disp_m=float(s[i1 - 1] - s[i0]),
            sL_minus_sR_m=float((sL[i1 - 1] - sR[i1 - 1]) - (sL[i0] - sR[i0])),
            pitch_mean_deg=float(np.degrees(pitch[sl].mean())),
            roll_mean_deg=float(np.degrees(roll[sl].mean())),
            wheel_tau_mean=d['tau'][sl][:, [3, 7]].mean(0).tolist(),
            wheel_tau_diff_mean=float((d['tau'][sl, 7] - d['tau'][sl, 3]).mean()),
            hip_q_mean=q[sl][:, [0, 4]].mean(0).tolist(),
            thigh_q_mean=q[sl][:, [1, 5]].mean(0).tolist(),
            knee_q_mean=q[sl][:, [2, 6]].mean(0).tolist(),
            wheel_target_vel_mean=d['target'][sl][:, [3, 7]].mean(0).tolist(),
            wheel_vel_mean=dq[sl][:, [3, 7]].mean(0).tolist(),
        ))
    # Parity: rebuild the latched x error from the unwrapped odometry (same latch as adapter.hpp).
    rebuilt = np.zeros(len(t))
    ref = s[0]
    for i in range(len(t)):
        if not (rl[i] and zero[i]) or (i and not rl[i - 1]):
            ref = s[i]
        rebuilt[i] = np.clip(s[i] - ref, -.3, .3) if rl[i] and zero[i] else 0.
    x_parity = dict(max_abs_err_m=float(np.abs(rebuilt - x_obs)[rl].max()),
                    rms_err_m=float(np.sqrt(np.mean((rebuilt - x_obs)[rl] ** 2))))
    # Command-time yaw tracking (moving samples).
    moving = rl & ~zero
    trk = {}
    for name, m in [('yaw_cmd_nonzero', moving & (np.abs(cmd[:, 2]) > .03)),
                    ('yaw_cmd_zero_but_moving', moving & (np.abs(cmd[:, 2]) <= .03))]:
        if m.sum():
            trk[name] = dict(samples=int(m.sum()), err_mean_dps=float(np.degrees((gz - cmd[:, 2])[m].mean())),
                             err_rms_dps=float(np.degrees(np.sqrt(((gz - cmd[:, 2])[m] ** 2).mean()))))
    rl_segs = [(int(x), int(y)) for x, y in pd.runs(rl)]
    vib = {k: pd.band_powers(v, [(x, y) for x, y in rl_segs])
           for k, v in [('pitch_rate', pitch_rate[:, None]), ('leg_dq', dq[:, [0, 1, 2, 4, 5, 6]])]}
    out = dict(
        execution_domain='DESKTOP_DRY_RUN', bag_db=d['db'], bag_db_sha256=d['db_sha256'],
        checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
        rl_duration_s=float(t[rl][-1] - t[rl][0]), rl_segments=len(rl_segs),
        zero_cmd_fraction=float((rl & zero).sum() / rl.sum()),
        x_obs_parity=x_parity, effective_track_width_m=W, encoder_vs_gyro_corr_yawing=corr, yawing_samples=int(yawing.sum()),
        zero_segments=segs, yaw_tracking=trk, vibration=vib,
        total_rl_yaw_quat_deg=float(np.degrees(yaw[rl][-1] - yaw[rl][0])),
    )
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=1))
    np.savez_compressed(a.out.with_suffix('.npz'), t=t, rl=rl, zero=zero, cmd=cmd, yaw=yaw, pitch=pitch,
                        roll=roll, gz=gz, gz_enc=gz_enc, x_obs=x_obs, s=s, sL=sL, sR=sR, tau=d['tau'], q=q,
                        dq=dq, action=d['action'], obs=obs, sel=settled)
    print(json.dumps({k: v for k, v in out.items() if k not in ('zero_segments', 'vibration')}, indent=1))
    for g in segs:
        print(f"t {g['t0']:6.1f}-{g['t1']:6.1f} ({g['duration_s']:5.1f}s) yaw quat {g['yaw_quat_deg']:+6.1f} "
              f"gyro {g['yaw_gyro_int_deg']:+6.1f} enc {g['yaw_encoder_int_deg']:+6.1f} deg | "
              f"rate {g['yaw_rate_mean_dps']:+5.2f} dps | x_obs {g['x_obs_m']['start']:+.3f}->{g['x_obs_m']['end']:+.3f} "
              f"[{g['x_obs_m']['min']:+.3f},{g['x_obs_m']['max']:+.3f}] | dsL-dsR {g['sL_minus_sR_m']:+.3f} m | "
              f"wheel tau R-L {g['wheel_tau_diff_mean']:+.3f} vt {np.round(g['wheel_target_vel_mean'],2)} v {np.round(g['wheel_vel_mean'],2)} | pitch {g['pitch_mean_deg']:+.2f} roll {g['roll_mean_deg']:+.2f}")
    for k, v in vib.items():
        print(k, {b: np.round(p, 5).tolist() for b, p in v.get('bands', {}).items()}, 'peak', v.get('peak_hz_above_1'))


if __name__ == '__main__':
    main()
