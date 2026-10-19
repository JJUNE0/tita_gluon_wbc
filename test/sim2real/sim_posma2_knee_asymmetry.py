"""VALIDATION_SIM: 좌우 무릎 출력 비대칭 / 무릎 엔코더 오프셋이 정지 yaw 회전을 만드는지 MuJoCo로 확인한다.

Codex 체크포인트 스크린(`test/evaluate_posknee_checkpoints.py`)의 rollout을 그대로 쓰고 두 가지만 바꾼다.
- 무릎 Kp/Kd를 좌(2)·우(6) 따로 곱한다(학습 knee_output_scale 이벤트와 같은 의미: clip 전 PD 배율).
- 무릎 엔코더 오프셋: 정책 관측과 PD 계산에 쓰는 측정 각도에만 더한다(물리 관절은 그대로).
- 휠 접촉(plant): cyl = 공개 XML 원통(폭 3.4 cm, 다점 접촉, mu=max(0.4,1.0)=1.0),
  sphere = 같은 반경의 구(점 접촉, 제자리 회전 scrub 저항 없음), cyl_mu04 = 원통 + 바닥 마찰 0.4.
로봇 명령 없음. 출력은 docs/exp/2026-10-18/posma2_knee_asymmetry_sim/.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
import copy
import dataclasses
import json
from pathlib import Path
import sys

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'test'))
import evaluate_posknee_checkpoints as E  # noqa: E402

OUT = REPO / 'docs/exp/2026-10-18/posma2_knee_asymmetry_sim'
POLICIES = {p['step']: p for p in json.loads((REPO / 'docs/exp/2026-10-18/posknee_checkpoint_screen/policies.json').read_text())}
# (좌 무릎 배율, 우 무릎 배율, 좌 무릎 엔코더 오프셋 [deg], 우 무릎 오프셋 [deg], 휠 접촉)
CASES = {
    'sym068': (.68, .68, 0., 0., 'cyl'),
    'weakL_060_075': (.60, .75, 0., 0., 'cyl'),
    'weakR_075_060': (.75, .60, 0., 0., 'cyl'),
    'encL_m3deg': (.68, .68, -3., 0., 'cyl'),
    'sym068_sphere': (.68, .68, 0., 0., 'sphere'),
    'weakL_060_075_sphere': (.60, .75, 0., 0., 'sphere'),
    'weakL_060_075_cylmu04': (.60, .75, 0., 0., 'cyl_mu04'),
}
JOBS = ([(c, 50000) for c in CASES] + [(c, s) for s in (45000, 75000)
        for c in ('sym068', 'weakL_060_075', 'sym068_sphere', 'weakL_060_075_sphere')])
CASE = {}


class Adapter(E.ActionAdapter):
    def __init__(self, cfg):
        cfg = copy.deepcopy(cfg)
        for key in ('joint_kp', 'joint_kd'):
            cfg['robot'][key][2] *= CASE['sL']
            cfg['robot'][key][6] *= CASE['sR']
        super().__init__(cfg)

    def compute(self, action, joint_pos, joint_vel):
        return super().compute(action, np.asarray(joint_pos) + CASE['offset'], joint_vel)


class Builder(E.ObservationBuilder):
    def build(self, state):
        return super().build(dataclasses.replace(state, joint_pos=np.asarray(state.joint_pos) + CASE['offset']))


class Env(E.TitaMujocoEnv):
    def __init__(self, cfg):
        super().__init__(cfg)
        m = self.model
        wheels = [g for g in range(m.ngeom) if m.geom_bodyid[g] in
                  (m.body('left_leg_4').id, m.body('right_leg_4').id) and (m.geom_contype[g] or m.geom_conaffinity[g])]
        assert len(wheels) == 2 and all(m.geom_type[g] == E_mj.mjtGeom.mjGEOM_CYLINDER for g in wheels)
        if CASE['plant'] == 'sphere':
            for g in wheels:
                r = m.geom_size[g][0]
                m.geom_type[g] = E_mj.mjtGeom.mjGEOM_SPHERE
                m.geom_size[g] = [r, 0., 0.]
                m.geom_rbound[g] = r
                m.geom_aabb[g] = [0., 0., 0., r, r, r]
        elif CASE['plant'] == 'cyl_mu04':
            m.geom_friction[m.geom('floor').id][0] = .4


import mujoco as E_mj  # noqa: E402
E.ActionAdapter, E.ObservationBuilder, E.TitaMujocoEnv = Adapter, Builder, Env


def run(job):
    name, step, scenario = job
    sL, sR, oL, oR, plant = CASES[name]
    CASE.update(sL=sL, sR=sR, offset=np.radians([0, 0, oL, 0, 0, 0, oR, 0]), plant=plant)
    out = OUT / f'{name}_{step}'
    (out / 'signals').mkdir(parents=True, exist_ok=True)
    r = E.rollout(dict(step=step, config=POLICIES[step]['config'], output=str(out), seed=42, scale=1., scenario=scenario))
    row = dict(case=name, step=step, scenario=scenario, knee_scale_LR=[sL, sR], knee_offset_deg_LR=[oL, oR], plant=plant,
               status=r['evidence_status'], failure=r['failure'], checkpoint_sha256=r['checkpoint_sha256'])
    if r['evidence_status'] != 'PASS':
        return row
    z = np.load(REPO / r['signal_file'])
    t, cmd = z['t'], z['command']
    yaw = np.unwrap(np.radians(z['rpy_deg'][:, 2]))
    tgt = z['applied_action'] * .25 + np.array([0, .8, -1.5, 0, 0, .8, -1.5, 0])
    meas = z['q'] + CASE['offset']                                     # 정책이 보는 각도
    zero = np.max(np.abs(cmd), axis=1) < 1e-7
    if scenario == 'stand':
        m = t >= 8.
        row['yaw_rate_dps'] = float(np.degrees((yaw[m][-1] - yaw[m][0]) / (t[m][-1] - t[m][0])))
    else:
        rates = []
        for block in E.intervals(zero):
            if t[block[0]] < 8.:
                continue
            b = block[t[block] >= t[block[0]] + 1.]
            if len(b) > 50:
                rates.append(float(np.degrees((yaw[b[-1]] - yaw[b[0]]) / (t[b[-1]] - t[b[0]]))))
        row['stop_yaw_rates_dps'] = rates
        row['yaw_rate_dps'] = float(np.mean(rates))
        m = np.zeros(len(t), bool)
        for block in E.intervals(zero):
            if t[block[0]] >= 8.:
                m[block[t[block] >= t[block[0]] + 1.]] = True
    row.update(
        knee_meas_LR_deg=np.degrees(meas[m][:, [2, 6]].mean(0)).round(2).tolist(),
        knee_true_LR_deg=np.degrees(z['q'][m][:, [2, 6]].mean(0)).round(2).tolist(),
        knee_meas_L_minus_R_deg=float(np.degrees((meas[m, 2] - meas[m, 6]).mean())),
        thigh_L_minus_R_deg=float(np.degrees((meas[m, 1] - meas[m, 5]).mean())),
        knee_sag_LR_deg=np.degrees((tgt - meas)[m][:, [2, 6]].mean(0)).round(2).tolist(),
        wheel_target_diff_RL_rad_s=float(((z['applied_action'][m, 7] - z['applied_action'][m, 3]) * 20).mean()),
        wheel_tau_diff_RL_nm=float((z['torque'][m].mean(1)[:, 7] - z['torque'][m].mean(1)[:, 3]).mean()),
        roll_deg=float(z['rpy_deg'][m, 0].mean()), pitch_deg=float(z['rpy_deg'][m, 1].mean()),
        x_disp_m=float(z['position'][m][-1, 0] - z['position'][m][0, 0]) if scenario == 'stand' else None)
    return row


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [(c, s, sc) for c, s in JOBS for sc in ('stand', 'drive')]
    with ProcessPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(run, jobs))
    (OUT / 'results.json').write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    for r in rows:
        if r['status'] != 'PASS':
            print(r['case'], r['step'], r['scenario'], 'FAIL', r['failure'])
            continue
        print(f"{r['case']:22s} {r['step']} {r['scenario']:5s} yaw {r['yaw_rate_dps']:+6.2f} dps | knee meas L-R "
              f"{r['knee_meas_L_minus_R_deg']:+5.2f} | sag L/R {r['knee_sag_LR_deg']} | thigh L-R {r['thigh_L_minus_R_deg']:+5.2f} | "
              f"wheel D {r['wheel_target_diff_RL_rad_s']:+5.2f} tau {r['wheel_tau_diff_RL_nm']:+5.2f} | roll {r['roll_deg']:+5.2f} pitch {r['pitch_deg']:+5.2f}"
              + (f" | stops {np.round(r['stop_yaw_rates_dps'], 2).tolist()}" if r['scenario'] == 'drive' else ''))


if __name__ == '__main__':
    main()
