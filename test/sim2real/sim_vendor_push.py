"""VALIDATION_SIM: vendor stand controller identified from the 19:27 push captures, replayed in MuJoCo.

Identification is least squares on the 500 Hz ROS joint_states/IMU of ``stand_<height>_push``, with the quiet
``stand_<height>`` capture held out. Torques are firmware-reported N m. Wheel position/speed is the encoder
rolling distance ``R*(q_wheel + pitch + q_thigh + q_knee)``, the same definition as the training observation.

- wheels (mean): pitch, pitch rate, rolling position, rolling speed, thigh angle, thigh rate;
- thighs (mean): pitch, pitch rate, rolling position, rolling speed, thigh angle, thigh rate;
- knees and hips: stiff hold at the measured posture with the measured feed-forward. Not identifiable:
  the knee std is ~1e-5 rad;
- heading and left/right differences: stabilising PD, not identified.

The simulation starts in the measured posture. Torque-unit hypotheses scale the controller output per joint
group. The run is compared with the real quiet stand (pitch, thigh, drift) and with a base push.
"""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_sit_transitions as vst  # noqa: E402

REPO = vst.REPO
DATA = REPO / 'docs/exp/2026-10-18/vendor_lqr_reproduction/capture_1927'
BUNDLE = REPO / 'sim2real/tita_ws/src/tita_controller/policies/flashsac_80000'
R, DT = 0.0925, vst.DT
FEATURES = ['phi', 'dphi', 'x', 'v', 'th', 'dth']


def load(tag: str) -> dict:
    z = np.load(glob.glob(str(DATA / f'ros_vendor_{tag}_1*.npz'))[0])
    imu, joints = z['imu'], z['joints']
    t = joints[:, 0]
    q, dq, e = joints[:, 1:9].copy(), joints[:, 9:17], joints[:, 17:25]
    for j in (3, 7):
        q[:, j] = np.unwrap(q[:, j])
    i = np.array([np.interp(t, imu[:, 0], imu[:, k]) for k in range(1, 8)]).T
    w, x, y, zq = i[:, :4].T
    phi = np.arcsin(np.clip(2 * (w * y - zq * x), -1, 1))
    th, kn = (q[:, 1] + q[:, 5]) / 2, (q[:, 2] + q[:, 6]) / 2
    dth, dkn = (dq[:, 1] + dq[:, 5]) / 2, (dq[:, 2] + dq[:, 6]) / 2
    s = R * ((q[:, 3] + q[:, 7]) / 2 + phi + th + kn)
    return dict(t=t - t[0], phi=phi, dphi=i[:, 5], x=s - s[0], v=R * ((dq[:, 3] + dq[:, 7]) / 2 + i[:, 5] + dth + dkn),
                th=th, dth=dth, q=q, e=e, tw=(e[:, 3] + e[:, 7]) / 2, tt=(e[:, 1] + e[:, 5]) / 2)


def identify(height: str) -> dict:
    push, quiet = load(f'stand_{height}_push'), load(f'stand_{height}')
    law = {}
    for target in ('tw', 'tt'):
        a = np.c_[tuple(push[k] for k in FEATURES) + (np.ones(len(push['t'])),)]
        c, *_ = np.linalg.lstsq(a, push[target], rcond=None)
        aq = np.c_[tuple(quiet[k] for k in FEATURES) + (np.ones(len(quiet['t'])),)]
        law[target] = dict(coef=c.tolist(), r2_push=float(1 - np.var(push[target] - a @ c) / np.var(push[target])),
                           r2_quiet=float(1 - np.var(quiet[target] - aq @ c) / np.var(quiet[target])))
    q = quiet['q']
    law['posture'] = q.mean(0).tolist()
    law['effort'] = quiet['e'].mean(0).tolist()
    law['real_quiet'] = dict(pitch_deg=float(np.degrees(quiet['phi']).mean()), pitch_std_deg=float(np.degrees(quiet['phi']).std()),
                             thigh=float(quiet['th'].mean()), drift_cm=float(quiet['x'][-1] * 100), seconds=float(quiet['t'][-1]))
    return law


def run(law: dict, scale: dict, seconds: float, push_n: float, push_at: float, com_dx: float = 0.) -> dict:
    cfg = json.loads((BUNDLE / 'config.json').read_text())
    cfg['control'] = dict(sim_timestep=DT, decimation=10)
    env = vst.TitaMujocoEnv(cfg)
    m, d = env.model, env.data
    floor = m.geom('floor').id
    obstacles = np.flatnonzero((m.geom_bodyid == 0) & (np.arange(m.ngeom) != floor))
    m.geom_contype[obstacles] = m.geom_conaffinity[obstacles] = 0
    if com_dx:
        m.body_ipos[m.body('base_link').id, 0] += com_dx  # calibration hypothesis: base CoM shift along x
        vst.mujoco.mj_setConst(m, d)
    pose = np.array(law['posture'])
    pose[[3, 7]] = 0.
    env.reset(pose)
    pitch0 = np.deg2rad(law['real_quiet']['pitch_deg'])
    d.qpos[3:7] = [np.cos(pitch0 / 2), 0., np.sin(pitch0 / 2), 0.]
    d.qvel[:] = 0.
    vst.mujoco.mj_forward(m, d)
    wheels = [m.jnt_bodyid[m.joint(env.joint_names[j]).id] for j in (3, 7)]
    d.qpos[2] += R - min(d.xpos[b][2] for b in wheels) + 1e-4
    vst.mujoco.mj_forward(m, d)
    base = m.body('base_link').id
    k = np.array([scale[n] for n in ('hip', 'thigh', 'knee', 'wheel', 'hip', 'thigh', 'knee', 'wheel')])
    limits = np.array(cfg['robot']['torque_limit'])
    cw, ct = np.array(law['tw']['coef']), np.array(law['tt']['coef'])
    hold_q, hold_ff = np.array(law['posture']), np.array(law['effort'])
    x0, rows, fault = None, [], None
    for tick in range(round(seconds / DT)):
        q, dq = env.joint_pos().copy(), env.joint_vel().copy()
        w, xq, y, z = d.sensor('trunk_quat').data
        gyro = d.sensor('trunk_gyro').data.copy()
        phi = np.arcsin(np.clip(2 * (w * y - z * xq), -1, 1))
        th, kn, dth, dkn = (q[1] + q[5]) / 2, (q[2] + q[6]) / 2, (dq[1] + dq[5]) / 2, (dq[2] + dq[6]) / 2
        s = R * ((q[3] + q[7]) / 2 + phi + th + kn)
        x0 = s if x0 is None else x0
        v = R * ((dq[3] + dq[7]) / 2 + gyro[1] + dth + dkn)
        feat = np.r_[phi, gyro[1], s - x0, v, th, dth, 1.]
        tau = np.zeros(8)
        tw, tt = cw @ feat, ct @ feat
        td = -4. * R * (q[3] - q[7]) / 2 - 1. * R * (dq[3] - dq[7]) / 2 - .3 * gyro[2]
        tau[3], tau[7] = tw + td, tw - td
        tdiff = -60. * ((q[1] - q[5]) - (hold_q[1] - hold_q[5])) / 2 - 1. * (dq[1] - dq[5]) / 2
        tau[1], tau[5] = tt + tdiff, tt - tdiff
        for j, kp in ((0, 800.), (4, 800.), (2, 400.), (6, 400.)):
            tau[j] = hold_ff[j] - kp * (q[j] - hold_q[j]) - 4. * dq[j]
        d.xfrc_applied[base] = 0.
        if push_n and push_at <= d.time < push_at + .1:
            d.xfrc_applied[base, 0] = push_n
        d.ctrl[env.actuator_ids] = np.clip(tau * k, -limits, limits)
        vst.mujoco.mj_step(m, d)
        if tick % 10 == 0:
            rows.append([d.time, phi, s - x0, v, th, kn, tw, tt])
        if np.arccos(np.clip(1 - 2 * (xq * xq + y * y), -1, 1)) > .65 or not np.isfinite(d.qpos).all():
            fault = dict(kind='fall', t=float(d.time))
            break
    env.close()
    rows = np.array(rows)
    pre = (rows[:, 0] > push_at - 4.) & (rows[:, 0] < push_at) if push_n else rows[:, 0] > rows[-1, 0] - 5.
    if pre.sum() < 2:
        return dict(scale=scale, fault=fault, seconds=float(rows[-1, 0]), pitch_deg=float('nan'), pitch_std_deg=float('nan'),
                    thigh=float('nan'), knee=float('nan'), drift_cm_per_10s=float('nan'))
    out = dict(scale=scale, com_dx=com_dx, fault=fault, seconds=float(rows[-1, 0]),
               pitch_deg=float(np.degrees(rows[pre, 1]).mean()), pitch_std_deg=float(np.degrees(rows[pre, 1]).std()),
               thigh=float(rows[pre, 4].mean()), knee=float(rows[pre, 5].mean()),
               drift_cm_per_10s=float((rows[pre, 2][-1] - rows[pre, 2][0]) * 100 / max(rows[pre, 0][-1] - rows[pre, 0][0], 1e-6) * 10))
    if push_n and fault is None:
        post = rows[:, 0] >= push_at
        settled = np.flatnonzero(np.abs(rows[post, 3]) > .05)
        out.update(push_peak_pitch_deg=float(np.degrees(np.abs(rows[post, 1] - rows[pre, 1].mean())).max()),
                   push_peak_speed=float(np.abs(rows[post, 3]).max()), push_travel_m=float(rows[-1, 2] - rows[pre, 2].mean()),
                   settle_s=float(rows[post, 0][settled[-1]] - push_at) if len(settled) else 0.)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, default=REPO / 'docs/exp/2026-10-18/vendor_lqr_reproduction/push_sim')
    parser.add_argument('--seconds', type=float, default=25.)
    parser.add_argument('--push', type=float, default=60., help='base push force [N] for 0.1 s at 10 s (0 = none)')
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(REPO / 'docs/exp')
    out.mkdir(parents=True, exist_ok=True)
    hypotheses = {'all_1.0': dict(hip=1., thigh=1., knee=1., wheel=1.),
                  'legs_0.65': dict(hip=.65, thigh=.65, knee=.65, wheel=1.),
                  'knee_0.65': dict(hip=1., thigh=1., knee=.65, wheel=1.),
                  'all_0.65': dict(hip=.65, thigh=.65, knee=.65, wheel=.65)}
    report = {}
    for height in ('high', 'mid', 'low'):
        law = identify(height)
        real = law['real_quiet']
        print(f"== {height}: wheel {np.round(law['tw']['coef'], 2).tolist()} R2 push/quiet {law['tw']['r2_push']:.2f}/"
              f"{law['tw']['r2_quiet']:.2f}; thigh {np.round(law['tt']['coef'], 2).tolist()} R2 {law['tt']['r2_push']:.2f}/"
              f"{law['tt']['r2_quiet']:.2f}")
        print(f"   REAL quiet: pitch {real['pitch_deg']:.2f}+-{real['pitch_std_deg']:.2f} deg thigh {real['thigh']:.3f} "
              f"drift {real['drift_cm']:+.1f} cm/{real['seconds']:.0f} s")
        report[height] = dict(law=law, sim={})
        for name, scale in hypotheses.items():
            r = run(law, scale, args.seconds, args.push, 10.)
            report[height]['sim'][name] = r
            extra = (f" | push {args.push:.0f} N: peak pitch {r['push_peak_pitch_deg']:.1f} deg, peak v {r['push_peak_speed']:.2f}, "
                     f"travel {r['push_travel_m']:+.2f} m, settle {r['settle_s']:.1f} s") if 'push_peak_speed' in r else ''
            print(f"   {name:10s} pitch {r['pitch_deg']:5.2f}+-{r['pitch_std_deg']:.2f} thigh {r['thigh']:.3f} knee {r['knee']:.3f} "
                  f"drift {r['drift_cm_per_10s']:+.2f} cm/10s fault {r['fault']}{extra}")
    (out / 'results.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
