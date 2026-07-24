#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


def _load(path: str) -> dict[str, np.ndarray]:
    with np.load(Path(path).expanduser(), allow_pickle=False) as data:
        return {k: np.asarray(data[k]) for k in data.files}


def _diff(a: np.ndarray, b: np.ndarray) -> float:
    if a.shape != b.shape:
        return float("inf")
    d = a.astype(np.float64) - b.astype(np.float64)
    valid = ~np.isnan(d)
    if not np.any(valid):
        return 0.0
    return float(np.max(np.abs(d[valid])))


def _optional_steps(data: dict[str, np.ndarray], *names: str) -> np.ndarray | None:
    for name in names:
        if name in data:
            return data[name]
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--isaac", required=True)
    parser.add_argument("--mujoco", required=True)
    parser.add_argument(
        "--output-prefix",
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/actuator_response_comparison",
    )
    args = parser.parse_args()

    isaac = _load(args.isaac)
    mujoco = _load(args.mujoco)
    n = min(len(isaac["steps_sim_time"]), len(mujoco["steps_sim_time"]))

    isaac_command_torque = _optional_steps(isaac, "steps_computed_torque")
    mujoco_command_torque = _optional_steps(mujoco, "steps_torque_cmd")
    isaac_applied_torque = _optional_steps(isaac, "steps_applied_torque")
    mujoco_applied_torque = _optional_steps(mujoco, "steps_qfrc_actuator")
    rows: list[dict[str, float | int]] = []
    for i in range(n):
        row = {
            "substep": i,
            "isaac_time": float(isaac["steps_sim_time"][i]),
            "mujoco_time": float(mujoco["steps_sim_time"][i]),
            "joint_pos_diff": _diff(isaac["steps_joint_pos"][i], mujoco["steps_joint_pos"][i]),
            "joint_vel_diff": _diff(isaac["steps_joint_vel"][i], mujoco["steps_joint_vel"][i]),
            "joint_pos_error_diff": _diff(isaac["steps_joint_pos_error"][i], mujoco["steps_joint_pos_error"][i]),
            "base_rpy_diff": _diff(isaac["steps_base_rpy"][i], mujoco["steps_base_rpy"][i]),
            "base_ang_vel_diff": _diff(isaac["steps_base_ang_vel"][i], mujoco["steps_base_ang_vel"][i]),
            "projected_gravity_diff": _diff(isaac["steps_projected_gravity"][i], mujoco["steps_projected_gravity"][i]),
            "target_leg_pos_diff": _diff(isaac["steps_target_leg_pos"][i], mujoco["steps_target_leg_pos"][i]),
            "target_wheel_vel_diff": _diff(isaac["steps_target_wheel_vel"][i], mujoco["steps_target_wheel_vel"][i]),
            "command_torque_diff": _diff(isaac_command_torque[i], mujoco_command_torque[i])
            if isaac_command_torque is not None and mujoco_command_torque is not None
            else float("nan"),
            "applied_torque_diff": _diff(isaac_applied_torque[i], mujoco_applied_torque[i])
            if isaac_applied_torque is not None and mujoco_applied_torque is not None
            else float("nan"),
        }
        rows.append(row)

    header = (
        "time | max joint_pos diff | max joint_vel diff | max command torque diff | "
        "max applied torque diff | "
        "max base_rpy diff | max base_ang_vel diff"
    )
    print(header)
    for row in rows:
        print(
            f"{row['isaac_time']:.3f}/{row['mujoco_time']:.3f} | "
            f"{row['joint_pos_diff']:.9g} | {row['joint_vel_diff']:.9g} | "
            f"{row['command_torque_diff']:.9g} | {row['applied_torque_diff']:.9g} | "
            f"{row['base_rpy_diff']:.9g} | {row['base_ang_vel_diff']:.9g}"
        )

    print("target_leg_pos_step0_diff:", f"{rows[0]['target_leg_pos_diff']:.9g}")
    print("target_wheel_vel_step0_diff:", f"{rows[0]['target_wheel_vel_diff']:.9g}")
    print("joint_pos_error_step4_diff:", f"{rows[-1]['joint_pos_error_diff']:.9g}")
    print("joint_vel_step4_diff:", f"{rows[-1]['joint_vel_diff']:.9g}")

    prefix = Path(args.output_prefix).expanduser()
    prefix.parent.mkdir(parents=True, exist_ok=True)
    with open(prefix.with_suffix(".json"), "w", encoding="utf-8") as f:
        json.dump(
            {
                "isaac": str(Path(args.isaac).expanduser()),
                "mujoco": str(Path(args.mujoco).expanduser()),
                "rows": rows,
            },
            f,
            indent=2,
        )
    with open(prefix.with_suffix(".csv"), "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print("saved_summary_json:", prefix.with_suffix(".json"))
    print("saved_summary_csv:", prefix.with_suffix(".csv"))


if __name__ == "__main__":
    main()
