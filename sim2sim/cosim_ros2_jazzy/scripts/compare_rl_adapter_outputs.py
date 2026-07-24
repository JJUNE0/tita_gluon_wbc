#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from cosim_ros2_jazzy.action_adapter import ActionAdapter


CONTROLLED_STEP0 = np.array(
    [-1.029673, -0.178142, 0.133714, 0.419854, 0.211553, -0.072685, -0.511154, 0.210179],
    dtype=np.float32,
)
WHEEL_STRESS = np.array([0.0, 0.0, 0.0, 18.043791, 0.0, 0.0, 0.0, 18.043791], dtype=np.float32)


def load_yaml(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_vec(text: str, size: int) -> np.ndarray:
    values = [float(x.strip()) for x in text.split(",") if x.strip()]
    if len(values) != size:
        raise ValueError(f"Expected {size} comma-separated values, got {len(values)}")
    return np.asarray(values, dtype=np.float32)


def load_trace(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    data = np.load(path, allow_pickle=True)

    def pick(name: str) -> np.ndarray:
        arr = data[name]
        arr = np.asarray(arr, dtype=np.float32)
        if arr.ndim > 1:
            arr = arr[0]
        return arr

    return pick("policy_action_raw"), pick("joint_pos"), pick("joint_vel")


def adapter_result(adapter: ActionAdapter, action: np.ndarray, joint_pos: np.ndarray, joint_vel: np.ndarray) -> dict[str, Any]:
    torque, debug = adapter.compute(action, joint_pos, joint_vel)
    return {
        "profile": adapter.summary(),
        "action_raw": debug.action_raw_by_joint.astype(float).tolist(),
        "action_used": debug.action_used_by_joint.astype(float).tolist(),
        "action_scaled": debug.action_scaled_by_joint.astype(float).tolist(),
        "target_joint_pos": debug.target_joint_pos_by_joint.astype(float).tolist(),
        "target_wheel_vel": debug.target_wheel_vel_by_joint.astype(float).tolist(),
        "torque_cmd": torque.astype(float).tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="cosim_ros2_jazzy/config/tita.yaml")
    parser.add_argument("--trace", help="Optional .npz trace file containing policy_action_raw, joint_pos, joint_vel")
    parser.add_argument("--sample", choices=["controlled_step0", "wheel_stress"], default="controlled_step0")
    parser.add_argument("--action", help="Optional 8-value comma-separated action override")
    parser.add_argument("--joint-pos", help="Optional 8-value comma-separated joint position override")
    parser.add_argument("--joint-vel", help="Optional 8-value comma-separated joint velocity override")
    parser.add_argument("--json-out", help="Optional JSON output path")
    args = parser.parse_args()

    cfg = load_yaml(Path(args.config))
    action = CONTROLLED_STEP0.copy() if args.sample == "controlled_step0" else WHEEL_STRESS.copy()
    joint_pos = np.asarray(cfg["robot"]["default_joint_angles"], dtype=np.float32).copy()
    joint_vel = np.zeros(8, dtype=np.float32)

    if args.trace:
        action, joint_pos, joint_vel = load_trace(Path(args.trace))
    if args.action:
        action = parse_vec(args.action, 8)
    if args.joint_pos:
        joint_pos = parse_vec(args.joint_pos, 8)
    if args.joint_vel:
        joint_vel = parse_vec(args.joint_vel, 8)

    cfg_current = copy.deepcopy(cfg)
    cfg_current.setdefault("rl_adapter", {})
    cfg_current["rl_adapter"]["mode"] = "current"
    cfg_ddt = copy.deepcopy(cfg)
    cfg_ddt.setdefault("rl_adapter", {})
    cfg_ddt["rl_adapter"]["mode"] = "ddt_reference"

    current = adapter_result(ActionAdapter(cfg_current), action, joint_pos, joint_vel)
    ddt = adapter_result(ActionAdapter(cfg_ddt), action, joint_pos, joint_vel)

    result = {
        "sample": args.sample,
        "action": action.astype(float).tolist(),
        "joint_pos": joint_pos.astype(float).tolist(),
        "joint_vel": joint_vel.astype(float).tolist(),
        "current": current,
        "ddt_reference": ddt,
    }

    print("sample:", args.sample)
    print("action:", result["action"])
    print("joint_pos:", result["joint_pos"])
    print("joint_vel:", result["joint_vel"])
    print()
    print("current.profile:", json.dumps(current["profile"], indent=2))
    print("ddt_reference.profile:", json.dumps(ddt["profile"], indent=2))
    print()
    for key in ["action_scaled", "target_joint_pos", "target_wheel_vel", "torque_cmd"]:
        print(f"{key}.current:", current[key])
        print(f"{key}.ddt_reference:", ddt[key])
        curr = np.asarray(current[key], dtype=np.float32)
        ref = np.asarray(ddt[key], dtype=np.float32)
        both = np.nan_to_num(curr - ref, nan=0.0)
        print(f"{key}.max_abs_diff:", float(np.max(np.abs(both))))
        print()

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"saved_json: {out_path}")


if __name__ == "__main__":
    main()
