"""DESKTOP_DRY_RUN + VALIDATION_SIM: does a CoM / IMU pitch offset (gap.md G6) reproduce the real fore-aft hunting?

Real references: ``yaw_drift.npz`` of the copied headw0 runs (50k 142158, 65k 153755). Sim: signals of
``screen_sphere_wheel_runs.py --evaluate --g6`` (plant A + base CoM x shift or IMU pitch offset). Same measures for both:
- holds (zero command, from 1 s after entry): IMU pitch, x_err observation mean and clip fraction, forward speed std,
  hunting period (first autocorrelation peak of v at 1.5-8 s lag, reported when the peak correlation >= 0.3),
  net position change from entry;
- in-place turns (|wz cmd| > 0.5, |vx cmd| < 0.05): mean forward speed, thigh and pitch change against the 2 s before.
No robot command.
usage: python analyze_g6_reproduction.py --sim DIR --real NAME=DIR [--real ...] --out JSON
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

DT = .02


def intervals(mask):
    e = np.flatnonzero(np.diff(np.r_[0, mask.astype(int), 0]))
    return list(zip(e[::2], e[1::2]))


def period(v):
    v = v - np.polyval(np.polyfit(np.arange(len(v)), v, 1), np.arange(len(v)))
    if len(v) < 400 or v.std() < 1e-4:
        return float('nan'), 0.
    ac = np.correlate(v, v, 'full')[len(v) - 1:] / (v.var() * len(v))
    lo, hi = int(1.5 / DT), min(int(8. / DT), len(v) // 2)
    k = lo + int(np.argmax(ac[lo:hi]))
    return (float(k * DT), float(ac[k])) if ac[k] >= .3 else (float('nan'), float(ac[k]))


def measures(t, cmd, v, x_obs, pitch, thigh, x_pos):
    """t [s], cmd (n,3), v forward speed, x_obs [m], pitch [deg] (IMU), thigh mean [deg], x_pos forward position [m]."""
    zero = np.all(np.abs(cmd) <= [.02, .02, .03], axis=1)
    holds = []
    for a, b in intervals(zero):
        a1 = a + 50
        if b - a1 < 150:
            continue
        per, corr = period(v[a1:b])
        holds.append(dict(t0=float(t[a]), seconds=float((b - a1) * DT), pitch_deg=float(pitch[a1:b].mean()),
                          x_obs_mean_m=float(x_obs[a1:b].mean()),
                          x_obs_sat=float((np.abs(x_obs[a1:b]) >= .3 - 1e-4).mean()),
                          v_std=float(v[a1:b].std()), period_s=per, period_corr=corr,
                          net_m=float(x_pos[b - 1] - x_pos[a])))
    turns = []
    turning = (np.abs(cmd[:, 2]) > .5) & (np.abs(cmd[:, 0]) < .05)
    for a, b in intervals(turning):
        if b - a < 50:
            continue
        pre = slice(max(0, a - 100), a)
        turns.append(dict(t0=float(t[a]), v_mean=float(v[a:b].mean()),
                          thigh_change_deg=float(thigh[a:b].mean() - thigh[pre].mean()),
                          pitch_change_deg=float(pitch[a:b].mean() - pitch[pre].mean())))
    return holds, turns


def pool(holds, turns):
    w = np.array([h['seconds'] for h in holds]) if holds else np.zeros(0)
    avg = lambda k: float(np.average([h[k] for h in holds], weights=w)) if holds else float('nan')
    per = [h['period_s'] for h in holds if np.isfinite(h['period_s'])]
    return dict(hold_s=float(w.sum()), pitch_deg=avg('pitch_deg'), x_obs_mean_m=avg('x_obs_mean_m'),
                x_obs_sat=avg('x_obs_sat'), v_std=avg('v_std'),
                periodic_holds=f"{len(per)}/{len(holds)}", period_s=float(np.median(per)) if per else float('nan'),
                net_m=float(np.mean([h['net_m'] for h in holds])) if holds else float('nan'),
                turn_v=float(np.mean([x['v_mean'] for x in turns])) if turns else float('nan'),
                turn_thigh=float(np.mean([x['thigh_change_deg'] for x in turns])) if turns else float('nan'),
                turn_pitch=float(np.mean([x['pitch_change_deg'] for x in turns])) if turns else float('nan'))


def real(folder):
    z = np.load(Path(folder) / 'yaw_drift.npz')
    rl = z['rl'].astype(bool)
    v = np.gradient(z['s'], DT)
    pick = lambda x: x[rl]
    return measures(pick(z['t']), pick(z['cmd']), pick(v), pick(z['x_obs']), pick(np.degrees(z['pitch'])),
                    pick(np.degrees(z['q'][:, [1, 5]].mean(1))), pick(z['s']))


def sim(path):
    z = np.load(path)
    v = z['velocity_body'][:, 0].astype(float)
    x_pos = np.cumsum(v) * DT          # forward odometry, comparable to the real wheel-arc s
    return measures(z['t'].astype(float), z['command'].astype(float), v, z['x_err'].astype(float),
                    z['imu_rpy_deg'][:, 1].astype(float), np.degrees(z['q'][:, [1, 5]].astype(float).mean(1)), x_pos)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--sim', type=Path, required=True)
    ap.add_argument('--real', action='append', default=[])
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    rows = []
    for item in a.real:
        name, folder = item.split('=', 1)
        h, tr = real(folder)
        rows.append(dict(source=f'real {name}', stand=None, drive=pool(h, tr), holds=h, turns=tr))
    results = json.loads((a.sim / 'results.json').read_text())
    by = {}
    for r in results:
        j = r['job']
        by.setdefault((j['step'], j['plant']), {})[j['scenario']] = r
    for (step, plant), d in sorted(by.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        row = dict(source=f'sim {step // 1000}k {plant}', failures=[k for k, r in d.items() if r['evidence_status'] != 'PASS'])
        got = {}
        for scenario in ('stand', 'drive', 'turn'):
            r = d.get(scenario)
            if r is not None and r['evidence_status'] == 'PASS':
                j = r['job']
                got[scenario] = sim(a.sim / 'signals' / f"{j['tag']}_{j['step']}_{j['plant']}_{scenario}_g{j['g']:g}.npz")
        if 'stand' in got:
            row['stand'] = pool(got['stand'][0], [])
        if 'drive' in got:
            row['drive'] = pool(got['drive'][0], got['turn'][1] if 'turn' in got else [])
        rows.append(row)
    a.out.write_text(json.dumps(dict(execution_domain='DESKTOP_DRY_RUN+VALIDATION_SIM', rows=rows), indent=1) + '\n')
    cols = ['pitch_deg', 'x_obs_mean_m', 'x_obs_sat', 'v_std', 'periodic_holds', 'period_s', 'net_m', 'turn_v',
            'turn_thigh', 'turn_pitch']
    fmt = lambda v: v if isinstance(v, str) else ('—' if not np.isfinite(v) else f'{v:+.3f}' if abs(v) < 1 else f'{v:+.2f}')
    print('source | stand: pitch x_obs | holds after motion: ' + ' '.join(cols))
    for r in rows:
        st = r.get('stand')
        dr = r.get('drive') or {}
        print(f"{r['source']:18s} | " + (f"{st['pitch_deg']:+.2f} {st['x_obs_mean_m']:+.3f} v{st['v_std']:.3f}" if st else '  —            ')
              + ' | ' + ' '.join(fmt(dr.get(c, float('nan'))) for c in cols) + (f"  FAIL {r['failures']}" if r.get('failures') else ''))


if __name__ == '__main__':
    main()
