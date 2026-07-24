#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Compare Isaac and MuJoCo response test results.")
    parser.add_argument("--isaac", type=str, default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/isaac_response_tests.json")
    parser.add_argument("--mujoco", type=str, default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/mujoco_response_tests.json")
    parser.add_argument("--out-json", type=str, default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/isaac_mujoco_response_tests.json")
    parser.add_argument("--out-csv", type=str, default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/isaac_mujoco_response_tests.csv")
    args = parser.parse_args()

    isaac = json.loads(Path(args.isaac).expanduser().read_text(encoding="utf-8"))
    mujoco = json.loads(Path(args.mujoco).expanduser().read_text(encoding="utf-8"))
    rows = []
    for test_name in sorted(set(isaac["tests"]) & set(mujoco["tests"])):
        it = isaac["tests"][test_name]
        mt = mujoco["tests"][test_name]
        rows.append(
            {
                "test": test_name,
                "isaac_max_abs_pitch": it.get("max_abs_pitch"),
                "mujoco_max_abs_pitch": mt.get("max_abs_pitch"),
                "isaac_max_abs_wheel_vel": it.get("max_abs_wheel_vel"),
                "mujoco_max_abs_wheel_vel": mt.get("max_abs_wheel_vel"),
                "isaac_base_pitch_delta": it.get("base_pitch_delta"),
                "mujoco_base_pitch_delta": mt.get("base_pitch_delta"),
                "isaac_base_x_delta": it.get("base_x_delta"),
                "mujoco_base_x_delta": mt.get("base_x_delta"),
                "isaac_max_abs_torque_cmd": it.get("max_abs_torque_cmd"),
                "mujoco_max_abs_torque_cmd": mt.get("max_abs_torque_cmd"),
            }
        )
    out_json = Path(args.out_json).expanduser()
    out_csv = Path(args.out_csv).expanduser()
    out_json.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["test"])
        writer.writeheader()
        writer.writerows(rows)
    print(out_json)
    print(out_csv)


if __name__ == "__main__":
    main()
