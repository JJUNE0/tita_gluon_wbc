"""VALIDATION_SIM: sign of the leg/body correction for encoder wheel odometry.

The wheel joint angle is measured relative to the shank. Ground rolling therefore needs the shank's
absolute pitch:

    s = R * mean_side(q_wheel + c * (body_pitch + q_thigh + q_knee))

This script drives the frozen A80k policy in the 500 Hz MuJoCo harness (forward/back/yaw) and compares
the displacement of each wheel centre along the robot heading with ``s`` for c in {-1, 0, +1}.
It is used only to choose ``c`` for the training observation.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sim_leg_action_filter as s  # noqa: E402

R = 0.0925


def main() -> None:
    cfg = s.load_config(s.BUNDLE)
    s._init(str(s.BUNDLE))
    captured = {}
    original_step = s.vst.mujoco.mj_step

    def step(m, d):
        original_step(m, d)
        if 'wheels' not in captured:
            captured['wheels'] = [m.jnt_bodyid[m.joint(n).id] for n in ('joint_left_leg_4', 'joint_right_leg_4')]
            captured['rows'] = []
        if int(round(d.time / s.DT)) % 10 == 0:
            yaw = s.vst.rpy(d.qpos[3:7])
            captured['rows'].append(np.r_[d.time, yaw, d.xpos[captured['wheels'][0]], d.xpos[captured['wheels'][1]]])
    s.vst.mujoco.mj_step = step
    job = dict(scenario='drive', gains='knee92', filter='none', preemphasis=0., leg_scale=(1., 1., .65),
               friction='none', delay_ticks=0, seed=42)
    rows_policy = {}
    original_summarize = s.summarize

    def keep(rows, scenario):
        rows_policy['rows'] = rows
        return original_summarize(rows, scenario)
    s.summarize = keep
    s.rollout(cfg, job)
    pol = rows_policy['rows']                      # policy ticks in RL: t_rl, ..., rpy at 39:42, q at 44:52
    sim = np.array(captured['rows'])               # every 20 ms: time, rpy, wheel xpos L, wheel xpos R
    t_rl, rpy, q = pol[:, 0], pol[:, 39:42], pol[:, 44:52]
    t0 = sim[-1, 0] - t_rl[-1]                    # RL entry in sim time (last samples coincide)
    idx = np.searchsorted(sim[:, 0], t_rl + t0 - 1e-6)
    idx = np.clip(idx, 0, len(sim) - 1)
    yaw = sim[idx, 3]
    heading = np.c_[np.cos(yaw), np.sin(yaw)]
    results = {}
    for side, (iw, ith, ikn, col) in enumerate([(3, 1, 2, 4), (7, 5, 6, 7)]):
        centre = sim[idx][:, col:col + 2]
        d_true = np.sum(np.diff(centre, axis=0) * heading[1:], axis=1)
        for c in (-1., 0., 1.):
            angle = q[:, iw] + c * (rpy[:, 1] + q[:, ith] + q[:, ikn])
            d_est = R * np.diff(angle)
            err = d_est - d_true
            results[f'side{side}_c{c:+.0f}'] = dict(rms_step_error_mm=float(np.sqrt(np.mean(err ** 2)) * 1e3),
                                                     total_true_m=float(d_true.sum()), total_est_m=float(d_est.sum()))
    print(json.dumps(results, indent=1))


if __name__ == '__main__':
    main()
