"""VALIDATION_SIM: run the identified vendor (MCU AUTO_LOCOMOTION) stand controller in MuJoCo.

The stand law is identified by least squares from the 2026-10-18 vendor stand capture
(ROS joint_states/IMU at 500 Hz; ``identify`` below; firmware-reported Nm):
- wheels (mean): LQR-like feedback on body pitch, pitch rate, wheel position and wheel velocity;
- thighs (mean): mostly body-pitch feedback, i.e. the leg-pitch torque of a wheel-legged LQR;
- knees and hips: very stiff position hold with the measured feed-forward.

The plant is run under torque-unit hypotheses ``scale`` (physical N m = scale x firmware N m) per joint
group. The result is compared with the real stand:
- pitch 1.42 deg;
- thigh 1.104/1.082, knee -2.178/-2.135 rad;
- drift -1.9 cm over 60 s.

Sim-only. The firmware Nm calibration is unknown, and the yaw/differential terms are a stabilising
choice, not identified.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_sit_transitions as vst  # noqa: E402

REPO = vst.REPO
DATA = REPO / 'docs/exp/2026-10-18/vendor_lqr_reproduction'
BUNDLE = REPO / 'sim2real/tita_ws/src/tita_controller/policies/flashsac_80000'
R = 0.0925
DT = vst.DT
GROUPS = {'hip': [0, 4], 'thigh': [1, 5], 'knee': [2, 6], 'wheel': [3, 7]}


def stand_signals(path: Path) -> dict:
    z = np.load(path)
    imu, joints = z['imu'], z['joints']
    t = joints[:, 0]
    q, dq, effort = joints[:, 1:9].copy(), joints[:, 9:17], joints[:, 17:25]
    for j in (3, 7):
        q[:, j] = np.unwrap(q[:, j])
    i = np.array([np.interp(t, imu[:, 0], imu[:, k]) for k in range(1, 8)]).T
    w, x, y, zq = i[:, :4].T
    return dict(t=t - t[0], q=q, dq=dq, effort=effort, pitch=np.arcsin(np.clip(2 * (w * y - zq * x), -1, 1)),
                gyro=i[:, 4:7])


def lstsq(y: np.ndarray, cols: np.ndarray) -> tuple[np.ndarray, float]:
    a = np.c_[cols, np.ones(len(y))]
    c, *_ = np.linalg.lstsq(a, y, rcond=None)
    return c, float(1 - np.var(y - a @ c) / np.var(y))


def identify(s: dict) -> dict:
    q, dq, e, phi, g = s['q'], s['dq'], s['effort'], s['pitch'], s['gyro']
    x = R * (q[:, 3] + q[:, 7]) / 2
    x = x - x[0]
    v = R * (dq[:, 3] + dq[:, 7]) / 2
    thigh, dthigh = (q[:, 1] + q[:, 5]) / 2, (dq[:, 1] + dq[:, 5]) / 2
    wheel, r2w = lstsq((e[:, 3] + e[:, 7]) / 2, np.c_[phi, g[:, 1], x, v])
    thigh_law, r2t = lstsq((e[:, 1] + e[:, 5]) / 2, np.c_[phi, g[:, 1], x, v, thigh, dthigh])
    # Knees/hips barely move in the stand (knee std 2e-5 rad), so per-joint stiffness is only kept when
    # well identified; otherwise a stiff hold is assumed (knee 400 from the mean-knee fit, hip 800 from the left hip).
    hold = {}
    for name, j, assumed in (('knee', [2, 6], 400.), ('hip', [0, 4], 800.)):
        for k in j:
            c, r2 = lstsq(e[:, k], np.c_[q[:, k]])
            kp = float(-c[0]) if r2 > .9 and -c[0] > 0 else assumed
            hold[k] = dict(kp=kp, kp_fit=float(-c[0]), r2=r2, assumed=bool(kp == assumed),
                           q0=float(q[:, k].mean()), ff=float(e[:, k].mean()))
    return dict(wheel=wheel.tolist(), wheel_r2=r2w, thigh=thigh_law.tolist(), thigh_r2=r2t, hold=hold,
                thigh_diff_q0=float((q[:, 1] - q[:, 5]).mean() / 2),
                real=dict(pitch_deg=float(np.degrees(phi).mean()), pitch_std_deg=float(np.degrees(phi).std()),
                          q_mean=q[:, [0, 1, 2, 4, 5, 6]].mean(0).tolist(), drift_m=float(x[-1]),
                          effort_mean=e.mean(0).tolist(), duration_s=float(s['t'][-1])))


def run(law: dict, scale: dict, seconds: float, push: tuple[float, float] | None = None) -> dict:
    cfg = json.loads((BUNDLE / 'config.json').read_text())
    cfg['control'] = dict(sim_timestep=DT, decimation=10)
    env = vst.TitaMujocoEnv(cfg)
    m, d = env.model, env.data
    floor = m.geom('floor').id
    obstacles = np.flatnonzero((m.geom_bodyid == 0) & (np.arange(m.ngeom) != floor))
    m.geom_contype[obstacles] = m.geom_conaffinity[obstacles] = 0
    real_q = law['real']['q_mean']
    pose = np.array([real_q[0], real_q[1], real_q[2], 0., real_q[3], real_q[4], real_q[5], 0.])
    env.reset(pose)
    pitch0 = np.deg2rad(law['real']['pitch_deg'])
    d.qpos[3:7] = [np.cos(pitch0 / 2), 0., np.sin(pitch0 / 2), 0.]
    d.qvel[:] = 0.
    vst.mujoco.mj_forward(m, d)
    wheel_bodies = [m.jnt_bodyid[m.joint(env.joint_names[j]).id] for j in (3, 7)]
    d.qpos[2] += R - min(d.xpos[b][2] for b in wheel_bodies) + 1e-4  # wheels just touching the floor
    vst.mujoco.mj_forward(m, d)
    k = np.array([scale[n] for n in ('hip', 'thigh', 'knee', 'wheel', 'hip', 'thigh', 'knee', 'wheel')])
    limits = np.array(cfg['robot']['torque_limit'])
    wheel, thigh, hold = np.array(law['wheel']), np.array(law['thigh']), law['hold']
    x0 = None
    rows, fault = [], None
    base_body = m.body('base_link').id
    for tick in range(round(seconds / DT)):
        q, dq = env.joint_pos().copy(), env.joint_vel().copy()
        quat, gyro = d.sensor('trunk_quat').data.copy(), d.sensor('trunk_gyro').data.copy()
        w, xq, y, z = quat
        phi = np.arcsin(np.clip(2 * (w * y - z * xq), -1, 1))
        xw = R * (q[3] + q[7]) / 2
        x0 = xw if x0 is None else x0
        x, v = xw - x0, R * (dq[3] + dq[7]) / 2
        ydiff, wdiff = R * (q[3] - q[7]) / 2, R * (dq[3] - dq[7]) / 2
        tau = np.zeros(8)
        tw = wheel @ np.r_[phi, gyro[1], x, v, 1.]
        td = -4. * ydiff - 1. * wdiff - .3 * gyro[2]  # stabilising heading hold (not identified)
        tau[3], tau[7] = tw + td, tw - td
        tt = thigh @ np.r_[phi, gyro[1], x, v, (q[1] + q[5]) / 2, (dq[1] + dq[5]) / 2, 1.]
        tdiff = -60. * ((q[1] - q[5]) / 2 - law['thigh_diff_q0']) - 1. * (dq[1] - dq[5]) / 2
        tau[1], tau[5] = tt + tdiff, tt - tdiff
        for j in (0, 2, 4, 6):
            h = hold[str(j)] if str(j) in hold else hold[j]
            tau[j] = h['ff'] - h['kp'] * (q[j] - h['q0']) - 4. * dq[j]
        applied = np.clip(tau * k, -limits, limits)
        d.xfrc_applied[base_body] = 0.
        if push and push[0] <= d.time < push[0] + .1:
            d.xfrc_applied[base_body, 0] = push[1]
        d.ctrl[env.actuator_ids] = applied
        vst.mujoco.mj_step(m, d)
        if tick % 10 == 0:
            rows.append(np.r_[d.time, phi, x, v, q, tau])
        if np.arccos(np.clip(1 - 2 * (xq * xq + y * y), -1, 1)) > .65:
            fault = dict(kind='fall', t=float(d.time))
            break
    env.close()
    rows = np.array(rows)
    tail = rows[:, 0] >= rows[-1, 0] - 10.
    return dict(scale=scale, push=push, fault=fault, seconds=float(rows[-1, 0]),
                pitch_deg=float(np.degrees(rows[tail, 1]).mean()), pitch_std_deg=float(np.degrees(rows[tail, 1]).std()),
                drift_m=float(rows[-1, 2]), speed_tail=float(rows[tail, 3].mean()),
                q_mean=rows[tail][:, 4:12][:, [0, 1, 2, 4, 5, 6]].mean(0).tolist(),
                firmware_tau_mean=rows[tail][:, 12:20].mean(0).tolist(), series=rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, default=DATA)
    parser.add_argument('--seconds', type=float, default=30.)
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(REPO / 'docs/exp')
    law = identify(stand_signals(DATA / 'ros_stand.npz'))
    (out / 'vendor_stand_law.json').write_text(json.dumps(law, indent=2) + '\n')
    hypotheses = {
        'all_1.0': dict(hip=1., thigh=1., knee=1., wheel=1.),
        'legs_0.65': dict(hip=.65, thigh=.65, knee=.65, wheel=1.),
        'all_0.65': dict(hip=.65, thigh=.65, knee=.65, wheel=.65),
        'knee_0.65': dict(hip=1., thigh=1., knee=.65, wheel=1.),
    }
    real = law['real']
    print(f"[VALIDATION_SIM] identified wheel {np.round(law['wheel'], 2).tolist()} (R2 {law['wheel_r2']:.3f}), "
          f"thigh {np.round(law['thigh'], 2).tolist()} (R2 {law['thigh_r2']:.3f})")
    print(f"REAL      pitch {real['pitch_deg']:5.2f}+-{real['pitch_std_deg']:.2f} deg drift {real['drift_m'] * 100:+.1f} cm/"
          f"{real['duration_s']:.0f} s q {np.round(real['q_mean'], 3).tolist()}")
    results = {}
    for name, scale in hypotheses.items():
        r = run(law, scale, args.seconds)
        np.save(out / f'sim_stand_{name}.npy', r.pop('series'))
        results[name] = r
        print(f"{name:10s} pitch {r['pitch_deg']:5.2f}+-{r['pitch_std_deg']:.2f} deg drift {r['drift_m'] * 100:+.1f} cm/"
              f"{r['seconds']:.0f} s tail v {r['speed_tail']:+.3f} q {np.round(r['q_mean'], 3).tolist()} "
              f"fw tau thigh/knee/hip {np.round(np.array(r['firmware_tau_mean'])[[1, 5, 2, 6, 0, 4]], 1).tolist()} "
              f"fault {r['fault']}")
    (out / 'sim_stand_results.json').write_text(json.dumps(dict(law=law, results=results), indent=2) + '\n')


if __name__ == '__main__':
    main()
