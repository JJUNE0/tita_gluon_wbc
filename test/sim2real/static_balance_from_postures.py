"""DESKTOP_DRY_RUN: URDF/MuJoCo static check of measured standing postures (no simulation step).

For each measured quiet-standing configuration (joint angles + IMU roll/pitch) this places the
corrected MuJoCo TITA model on flat ground and reports:

- the horizontal offset/angle of the whole-robot CoM from the midpoint of the two wheel contacts
  along the heading. A static stand with ~zero wheel torque and speed needs the *real* CoM over the
  contacts, so a non-zero URDF value there estimates the model's CoM error for that posture;
- the joint torques that hold the posture statically if each wheel carries half the weight
  (generalized gravity minus contact Jacobian forces), to compare with firmware/commanded torque.

The sim's own quiet posture (balanced by construction) is included as a convention check.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import mujoco
import numpy as np
from scipy.spatial.transform import Rotation

ROOT = Path(__file__).resolve().parents[2]
SCENE = ROOT / 'tita_gluon_ws/src/ddt_ros2_control/urdfs/tita_description/mujoco_corrected/scene.xml'
JOINTS = ['joint_left_leg_1', 'joint_left_leg_2', 'joint_left_leg_3', 'joint_left_leg_4',
          'joint_right_leg_1', 'joint_right_leg_2', 'joint_right_leg_3', 'joint_right_leg_4']
WHEEL_RADIUS = 0.0925


def analyse(model, q, roll_deg, pitch_deg):
    data = mujoco.MjData(model)
    qadr = [model.jnt_qposadr[model.joint(n).id] for n in JOINTS]
    dadr = [model.jnt_dofadr[model.joint(n).id] for n in JOINTS]
    data.qpos[3:7] = Rotation.from_euler('xyz', [np.radians(roll_deg), np.radians(pitch_deg), 0.]).as_quat()[[3, 0, 1, 2]]
    data.qpos[qadr] = q
    data.qpos[2] = 1.0
    mujoco.mj_kinematics(model, data)
    wheels = [model.jnt_bodyid[model.joint(n).id] for n in (JOINTS[3], JOINTS[7])]
    centers = data.xpos[wheels].copy()
    data.qpos[2] -= centers[:, 2].mean() - WHEEL_RADIUS  # wheels touch z=0 on average
    mujoco.mj_forward(model, data)
    centers = data.xpos[wheels].copy()
    contacts = centers - np.array([0., 0., WHEEL_RADIUS])
    mass = model.body_mass[1:].sum()
    com = (model.body_mass[1:, None] * data.xipos[1:]).sum(0) / mass
    heading = data.xmat[model.body('base_link').id].reshape(3, 3)[:, 0]
    heading = np.array([heading[0], heading[1], 0.]) / np.linalg.norm(heading[:2])
    mid = contacts.mean(0)
    dx = float((com - mid) @ heading)
    angle = float(np.degrees(np.arctan2(dx, com[2] - mid[2])))
    # Static joint torques with half the weight on each wheel contact (vertical force).
    weight = mass * -model.opt.gravity[2]
    tau = data.qfrc_bias.copy()  # zero velocity: generalized gravity
    for body, point in zip(wheels, contacts):
        jacp = np.zeros((3, model.nv))
        mujoco.mj_jac(model, data, jacp, None, point, body)
        tau -= jacp.T @ np.array([0., 0., weight / 2])
    return dict(com_offset_along_heading_m=dx, com_angle_deg=angle, com_height_above_contact_m=float(com[2] - mid[2]),
                base_height_m=float(data.qpos[2]), static_torque_nm=tau[dadr].tolist(),
                base_residual=tau[:6].tolist(), mass_kg=float(mass))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    model = mujoco.MjModel.from_xml_path(str(SCENE))
    exp = ROOT / 'docs/exp'
    cases = {}
    # Vendor controller quiet stand (firmware STAND, neutral channel input), from Codex's extracted signals.
    vs = np.load(exp / '2026-10-18/vendor_supported_stand_review/stand_signals.npz')
    cases['vendor_LQR_stand'] = dict(q=vs['q'].mean(0), roll=float(vs['roll'].mean()), pitch=float(vs['pitch'].mean()),
                                     reported=vs['effort'].mean(0), source='vendor stand 60 s')
    # R0 (model_60000) free drift 14:11, RL+5-10 s.
    r0 = np.load(exp / '2026-10-17/flashsac_141113_free_drift_review/signals.npz')
    t = r0['t'] - r0['t'][r0['rl']][0]
    m = r0['rl'] & (t >= 5) & (t < 10)
    w, x, y, z = r0['quat'][m].T
    cases['R0_real_1411'] = dict(q=r0['q'][m].mean(0), roll=float(np.degrees(np.arctan2(2*(w*x+y*z), 1-2*(x*x+y*y))).mean()),
                                 pitch=float(r0['pitch'][m].mean()), reported=r0['torque'][m].mean(0),
                                 source='R0 commanded torque, drifting -0.20 m/s')
    # A 80k real 10:59 (bias OFF), held-neutral samples of both RL segments.
    a8 = np.load(exp / '2026-10-18/flashsac_80000_105921_claude_review/signals.npz')
    seg = json.loads((exp / '2026-10-18/flashsac_80000_105921_claude_review/segments.json').read_text())
    sel = np.zeros(len(a8['t']), bool)
    for s in seg['segments']:
        for wdw in s['neutral_windows']:
            sel |= (a8['t'] >= s['start_s'] + wdw['start_s']) & (a8['t'] <= s['start_s'] + wdw['end_s'])
    w, x, y, z = a8['quat'][sel].T
    cases['A80k_real_1059'] = dict(q=a8['q'][sel].mean(0), roll=float(np.degrees(np.arctan2(2*(w*x+y*z), 1-2*(x*x+y*y))).mean()),
                                   pitch=float(a8['pitch'][sel].mean()), reported=np.nanmean(a8['reported'][sel], 0),
                                   source='A 80k firmware-reported torque, drifting -0.06..-0.12 m/s')
    # Sim quiet postures (balanced by construction) as a convention check.
    sig = Path('/tmp/claude-1000/-home-cocel-Desktop-Research-tita-gluon-wbc/f96007eb-3f49-4a46-9644-c4413236c239/scratchpad/ab_stage1_signals')
    for label in ('R0_60000__nominal', 'A_80k__nominal', 'A_80k__C_com2'):
        path = sig / f'{label}__zero__s104.npz'
        if path.exists():
            d = np.load(path)
            tt = np.arange(len(d['speed'])) * .02
            mm = (tt >= 5) & (tt < 30)
            w, x, y, z = d['quat'][mm].T
            cases[f'sim_{label}'] = dict(q=d['q'][mm].mean(0), roll=float(np.degrees(np.arctan2(2*(w*x+y*z), 1-2*(x*x+y*y))).mean()),
                                         pitch=float(np.degrees(np.arcsin(np.clip(2*(w*y-z*x), -1, 1))).mean()),
                                         reported=d['tau_applied'][mm].mean(0), source='sim applied torque (C: after leg gain 0.6)')
    report = {}
    print(f"{'case':26s} {'pitch':>6s} {'thigh':>6s} {'knee':>7s} {'CoM dx':>8s} {'CoM ang':>8s} {'z':>6s} | "
          f"{'URDF static hip/thigh/knee (L)':>32s} | {'measured hip/thigh/knee (L)':>28s}")
    for name, c in cases.items():
        r = analyse(model, np.asarray(c['q'], float), c['roll'], c['pitch'])
        r.update(pitch_deg=c['pitch'], roll_deg=c['roll'], q=np.asarray(c['q']).tolist(),
                 measured_torque_nm=np.asarray(c['reported']).tolist(), source=c['source'])
        report[name] = r
        st, me = r['static_torque_nm'], r['measured_torque_nm']
        print(f"{name:26s} {c['pitch']:6.2f} {c['q'][1]:6.3f} {c['q'][2]:7.3f} {r['com_offset_along_heading_m']*100:+7.2f}cm "
              f"{r['com_angle_deg']:+7.2f}d {r['base_height_m']:6.3f} | {st[0]:+9.1f} {st[1]:+8.1f} {st[2]:+8.1f} (R {st[4]:+6.1f} {st[6]:+6.1f}) | "
              f"{me[0]:+8.1f} {me[1]:+7.1f} {me[2]:+7.1f} (R {me[4]:+6.1f} {me[6]:+6.1f})")
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'static_balance.json').write_text(json.dumps(dict(
        execution_domain='DESKTOP_DRY_RUN', model=str(SCENE), assumptions=[
            'flat ground, wheels touching on average; vertical contact force = weight/2 per wheel',
            'base orientation from IMU roll/pitch (IMU assumed aligned with base; yaw irrelevant)',
            'URDF/MuJoCo masses and link CoMs; total mass from the model',
            'firmware/commanded torques are not calibrated Nm'], cases=report), indent=2) + '\n')


if __name__ == '__main__':
    main()
