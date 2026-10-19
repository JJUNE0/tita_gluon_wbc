#!/usr/bin/env python3
"""DESKTOP_DRY_RUN: compare zero-command stance, PD torque and drift between
existing real FlashSAC bags (already exported to signals NPZ) and the saved
MuJoCo nominal / mass+CoM rollouts of the same policy family.

Read-only: it only loads NPZ files under docs/exp and prints a summary.
Joint order of both sources is the action order
L1, L2, L3, L4(wheel), R1, R2, R3, R4(wheel).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

KP_LEG = 60.0
ACTION_SCALE_LEG = 0.25
DEFAULT_Q = np.array([0.0, 0.8, -1.5, 0.0, 0.0, 0.8, -1.5, 0.0])
WHEEL_RADIUS = 0.0925

REAL_RUNS = {
    "real_60k_free": "2026-10-17/flashsac_141113_free_drift_review/signals.npz",
    "real_60k_hand": "2026-10-17/flashsac_three_case_bias_diagnosis/hand_signals.npz",
    "real_60k_joy": "2026-10-17/flashsac_three_case_bias_diagnosis/joystick_signals.npz",
    "real_50k_off": "2026-10-17/flashsac_50000_real_review/off_signals.npz",
    "real_75k_off": "2026-10-17/flashsac_75000_real_review/off_signals.npz",
}
SIM_RUNS = {
    "sim_60k_nominal": "2026-10-17/velocity_bias_grid_video/nominal/group_0.npz",
    "sim_60k_low_friction": "2026-10-17/velocity_bias_grid_video/low_friction/group_0.npz",
    "sim_60k_com_fwd_mass115": "2026-10-17/velocity_bias_grid_video/com_forward_mass115/group_0.npz",
    "sim_60k_com_back_mass115": "2026-10-17/velocity_bias_grid_video/com_backward_mass115/group_0.npz",
}


def real_summary(path: Path) -> dict[str, np.ndarray | float | int]:
    d = np.load(path, allow_pickle=True)
    rl = d["rl"].astype(bool)
    t = d["t"] - d["t"][rl][0]
    zero_cmd = np.all(np.abs(d["command"]) < 1e-9, axis=1)
    mask = rl & (t >= 5.0) & zero_cmd
    if mask.sum() < 20:  # joystick run: fall back to all RL samples after 5 s
        mask = rl & (t >= 5.0)
    return {
        "n": int(mask.sum()),
        "q": d["q"][mask].mean(0),
        "action": d["action"][mask].mean(0),
        "torque": d["torque"][mask].mean(0),
        "dq_wheel_std": d["dq"][mask][:, [3, 7]].std(0),
        "speed": float(d["velocity"][mask].mean()),
    }


def sim_summary(path: Path) -> dict[str, np.ndarray | float | int]:
    d = np.load(path, allow_pickle=True)
    state, qpos, prev_action = d["state"], d["qpos"], d["previous_action"]
    # state rows are 50 Hz (dt=0.02 s); qpos is sampled every 5th state row.
    s0, s1 = int(5.0 / 0.02), int(10.0 / 0.02)
    q = qpos[s0 // 5 : s1 // 5, 7:].mean(0)
    action = prev_action[s0:s1].mean(0)
    target = DEFAULT_Q + ACTION_SCALE_LEG * action
    torque = KP_LEG * (target - q)
    torque[[3, 7]] = np.nan  # wheel PD needs velocity targets; not reconstructed here
    return {
        "n": s1 - s0,
        "q": q,
        "action": action,
        "torque": torque,
        "speed": float(state[s0:s1, 3].mean()),
        "pitch_deg": float(np.degrees(state[s0:s1, 5]).mean()),
    }


def fmt_pair(v: np.ndarray, i: int, j: int, spec: str = "+.3f") -> str:
    return f"{v[i]:{spec}}/{v[j]:{spec}}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exp-root", type=Path, default=Path("docs/exp"))
    args = parser.parse_args()

    print("window: RL+5 s onward, exact zero command (real); 5-10 s (sim). Torques are computed PD commands.")
    header = f"{'run':26s} {'n':>5s} {'speed m/s':>9s} {'hip q L/R':>15s} {'leg2 q L/R':>15s} {'leg3 q L/R':>15s} " \
             f"{'hip tau L/R':>13s} {'leg3 tau L/R':>13s} {'wheel tau L/R':>13s}"
    print(header)
    for name, rel in {**REAL_RUNS, **SIM_RUNS}.items():
        path = args.exp_root / rel
        s = real_summary(path) if name.startswith("real") else sim_summary(path)
        q, tau = s["q"], s["torque"]
        print(
            f"{name:26s} {s['n']:5d} {s['speed']:+9.3f} {fmt_pair(q, 0, 4):>15s} {fmt_pair(q, 1, 5):>15s} "
            f"{fmt_pair(q, 2, 6):>15s} {fmt_pair(tau, 0, 4, '+.1f'):>13s} {fmt_pair(tau, 2, 6, '+.1f'):>13s} "
            f"{fmt_pair(tau, 3, 7, '+.2f'):>13s}"
            + (f"  pitch={s['pitch_deg']:.2f}deg" if "pitch_deg" in s else f"  wheel_dq_std={fmt_pair(s['dq_wheel_std'], 0, 1)}")
        )

    # Static upper bound of knee (leg_3) load from the URDF: per-wheel axle load times shank length.
    total_mass, wheel_mass, shank = 25.691, 1.509, 0.2
    axle_load = (total_mass - 2 * wheel_mass) / 2 * 9.81
    print(f"\nURDF static bound: per-wheel axle load {axle_load:.1f} N x shank {shank} m "
          f"=> knee load <= {axle_load * shank:.1f} N m (+ shank weight ~0.6 N m)")
    print(f"training joint_vel noise U(-1.5, 1.5) rad/s => std {1.5 / np.sqrt(3):.3f} rad/s "
          f"= {1.5 * WHEEL_RADIUS:.3f} m/s wheel-equivalent bound")


if __name__ == "__main__":
    main()
