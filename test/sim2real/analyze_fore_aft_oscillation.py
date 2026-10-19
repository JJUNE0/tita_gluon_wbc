"""DESKTOP_DRY_RUN: back-and-forth (fore-aft / yaw) oscillation in copied real FlashSAC runs (read-only, no robot command).

Input: ``yaw_drift.npz`` written by analyze_posma2_yaw_drift.py for each run (s = mean wheel arc [m], pitch, gyro z,
x_err observation, command, actions at 50 Hz). Per run and segment kind
- hold: zero command, 1 s after entry;
- turn: in-place turn (|wz cmd| > 0.1, |vx cmd| < 0.05);
- drive: |vx cmd| >= 0.05;
report the fore-aft position oscillation (s high-passed at 0.2 Hz: RMS, p2p), forward speed RMS around the commanded
speed, dominant frequency of v in 0.2-5 Hz, pitch and yaw-rate oscillation (0.3-3 Hz RMS), thigh target oscillation and
the x_err observation range. Also prints a per-hold table and 2 s windows with the largest fore-aft motion.
usage: python analyze_fore_aft_oscillation.py --run NAME=DIR [--run ...] --out JSON
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy import signal

DT = .02
FS = 1 / DT


def band(x, lo, hi):
    b, a = signal.butter(2, [lo, hi] if hi else lo, btype='bandpass' if hi else 'highpass', fs=FS)
    return signal.filtfilt(b, a, x) if len(x) > 30 else x - x.mean()


def intervals(mask):
    edges = np.flatnonzero(np.diff(np.r_[0, mask.astype(int), 0]))
    return list(zip(edges[::2], edges[1::2]))


def peak_hz(x, lo=.2, hi=5.):
    if len(x) < 128:
        return float('nan')
    f, p = signal.welch(x - x.mean(), fs=FS, nperseg=min(256, len(x)))
    m = (f >= lo) & (f <= hi)
    return float(f[m][np.argmax(p[m])])


def segment_stats(z, idx):
    s, pitch, gz = z['s'], np.degrees(z['pitch']), np.degrees(z['gz'])
    v = np.gradient(s, DT)
    thigh_target = z['action'][:, [1, 5]].mean(1) * .25          # native action order, legs position x 0.25
    out = []
    for a, b in idx:
        if b - a < 50:
            continue
        sl = slice(a, b)
        s_hp = band(s[sl], .2, None)
        out.append(dict(
            t0=float(z['t'][a]), seconds=float((b - a) * DT), cmd_vx=float(z['cmd'][sl, 0].mean()),
            cmd_wz=float(z['cmd'][sl, 2].mean()),
            pos_osc_rms_m=float(np.sqrt(np.mean(s_hp ** 2))), pos_osc_p2p_m=float(np.ptp(s_hp)),
            net_disp_m=float(s[b - 1] - s[a]),
            v_rms_m_s=float(np.sqrt(np.mean((v[sl] - z['cmd'][sl, 0]) ** 2))), v_peak_hz=peak_hz(v[sl]),
            pitch_osc_rms_deg=float(np.sqrt(np.mean(band(pitch[sl], .3, 3.) ** 2))), pitch_peak_hz=peak_hz(pitch[sl]),
            yaw_osc_rms_dps=float(np.sqrt(np.mean(band(gz[sl], .3, 3.) ** 2))), yaw_peak_hz=peak_hz(gz[sl]),
            thigh_target_osc_rms_deg=float(np.degrees(np.sqrt(np.mean(band(thigh_target[sl], .3, 3.) ** 2)))),
            x_obs_min_m=float(z['x_obs'][sl].min()), x_obs_max_m=float(z['x_obs'][sl].max()),
            x_obs_sat_frac=float((np.abs(z['x_obs'][sl]) >= .3 - 1e-4).mean())))
    return out


def summarize(rows):
    if not rows:
        return dict(seconds=0.)
    w = np.array([r['seconds'] for r in rows])
    avg = lambda k: float(np.nansum([r[k] * x for r, x in zip(rows, w)]) / w.sum())
    return dict(seconds=float(w.sum()), segments=len(rows), **{k: avg(k) for k in (
        'pos_osc_rms_m', 'pos_osc_p2p_m', 'v_rms_m_s', 'v_peak_hz', 'pitch_osc_rms_deg', 'pitch_peak_hz',
        'yaw_osc_rms_dps', 'yaw_peak_hz', 'thigh_target_osc_rms_deg', 'x_obs_sat_frac')})


def analyze(folder):
    z = dict(np.load(folder / 'yaw_drift.npz'))
    rl, cmd = z['rl'].astype(bool), z['cmd']
    zero = rl & np.all(np.abs(cmd) <= [.02, .02, .03], axis=1)
    hold = np.zeros_like(zero)
    for a, b in intervals(zero):
        hold[a + 50:b] = True                                        # skip 1 s after entering zero command
    turn = rl & (np.abs(cmd[:, 2]) > .1) & (np.abs(cmd[:, 0]) < .05)
    drive = rl & (np.abs(cmd[:, 0]) >= .05)
    per = {k: segment_stats(z, intervals(m)) for k, m in (('hold', hold), ('turn', turn), ('drive', drive))}
    # 2 s windows (1 s hop) over RL with the largest fore-aft p2p
    s, t = z['s'], z['t']
    wins = []
    for a, b in intervals(rl):
        for k in range(a, b - 100, 50):
            hp = band(s[k:k + 100], .3, None)
            wins.append(dict(t0=float(t[k]), p2p_m=float(np.ptp(hp)), cmd=np.round(cmd[k:k + 100].mean(0), 2).tolist(),
                             v_peak_hz=peak_hz(np.gradient(s[k:k + 100], DT), .3, 5.)))
    wins.sort(key=lambda w: -w['p2p_m'])
    return dict(rl_seconds=float(rl.sum() * DT), summary={k: summarize(v) for k, v in per.items()}, segments=per,
                top_windows=wins[:8])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--run', action='append', required=True, help='NAME=DIR containing yaw_drift.npz')
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    result = dict(execution_domain='DESKTOP_DRY_RUN', runs={})
    for item in a.run:
        name, folder = item.split('=', 1)
        result['runs'][name] = analyze(Path(folder))
    a.out.write_text(json.dumps(result, indent=1) + '\n')
    keys = ['seconds', 'pos_osc_rms_m', 'pos_osc_p2p_m', 'v_rms_m_s', 'v_peak_hz', 'pitch_osc_rms_deg', 'pitch_peak_hz',
            'yaw_osc_rms_dps', 'yaw_peak_hz', 'thigh_target_osc_rms_deg', 'x_obs_sat_frac']
    print('run kind ' + ' '.join(keys))
    for name, r in result['runs'].items():
        for kind, v in r['summary'].items():
            print(name, kind, ' '.join('—' if k not in v else f'{v[k]:.3g}' for k in keys))
    for name, r in result['runs'].items():
        print(f'--- {name} holds: t0 s | pos rms/p2p m | net m | v pk Hz | pitch rms | yaw rms | x_obs min/max sat')
        for h in r['segments']['hold']:
            print(f"{h['t0']:6.1f} {h['seconds']:5.1f} | {h['pos_osc_rms_m']:.3f}/{h['pos_osc_p2p_m']:.3f} | "
                  f"{h['net_disp_m']:+.3f} | {h['v_peak_hz']:.2f} | {h['pitch_osc_rms_deg']:.2f} | "
                  f"{h['yaw_osc_rms_dps']:.2f} | {h['x_obs_min_m']:+.2f}/{h['x_obs_max_m']:+.2f} {h['x_obs_sat_frac']:.2f}")
        print(f'--- {name} top 2 s windows (fore-aft p2p, hp 0.3 Hz)')
        for w in r['top_windows']:
            print(f"  t={w['t0']:6.1f} p2p {w['p2p_m']:.3f} m  peak {w['v_peak_hz']:.2f} Hz  cmd {w['cmd']}")


if __name__ == '__main__':
    main()
