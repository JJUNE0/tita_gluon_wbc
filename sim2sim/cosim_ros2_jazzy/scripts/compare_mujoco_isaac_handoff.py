#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import onnxruntime as ort


TERM_SLICES = {
    "ang_vel": slice(0, 3),
    "projected_gravity": slice(3, 6),
    "command": slice(6, 9),
    "joint_pos_error": slice(9, 17),
    "joint_vel": slice(17, 25),
    "last_action": slice(25, 33),
}


def _to_jsonable(value):
    if isinstance(value, np.ndarray):
        if np.issubdtype(value.dtype, np.number):
            return value.astype(float).tolist()
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


def _run_onnx(onnx_path: str, obs_current: np.ndarray, obs_history: np.ndarray) -> np.ndarray:
    sess = ort.InferenceSession(str(Path(onnx_path).expanduser()), providers=["CPUExecutionProvider"])
    out = sess.run(
        [sess.get_outputs()[0].name],
        {
            sess.get_inputs()[0].name: obs_current.reshape(1, 33).astype(np.float32),
            sess.get_inputs()[1].name: obs_history.reshape(1, 10, 33).astype(np.float32),
        },
    )[0]
    return out.reshape(-1).astype(np.float32)


def _term_table(mujoco_obs: np.ndarray, isaac_obs: np.ndarray) -> list[dict[str, object]]:
    table = []
    for name, sl in TERM_SLICES.items():
        m = mujoco_obs[sl]
        i = isaac_obs[sl]
        table.append(
            {
                "term": name,
                "max_abs_diff": float(np.max(np.abs(m - i))),
                "mujoco_value": m.astype(float).tolist(),
                "isaac_value": i.astype(float).tolist(),
            }
        )
    return table


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mujoco", required=True)
    parser.add_argument("--isaac", required=True)
    parser.add_argument("--onnx", default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/policy.onnx")
    parser.add_argument(
        "--output-prefix",
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/mujoco_isaac_handoff_compare",
    )
    args = parser.parse_args()

    mujoco = np.load(Path(args.mujoco).expanduser(), allow_pickle=True)
    isaac = np.load(Path(args.isaac).expanduser(), allow_pickle=True)

    mujoco_obs_current = np.asarray(mujoco["obs_current"], dtype=np.float32)
    mujoco_obs_history = np.asarray(mujoco["obs_history"], dtype=np.float32)
    isaac_obs_current = np.asarray(isaac["obs_current"], dtype=np.float32)
    isaac_obs_history = np.asarray(isaac["obs_history"], dtype=np.float32)

    action_a = np.asarray(mujoco["policy_action_raw"], dtype=np.float32)
    action_b = _run_onnx(args.onnx, mujoco_obs_current, mujoco_obs_history)
    action_c = _run_onnx(args.onnx, isaac_obs_current, isaac_obs_history)

    summary = {
        "mujoco_state_path": str(Path(args.mujoco).resolve()),
        "isaac_state_path": str(Path(args.isaac).resolve()),
        "onnx_path": str(Path(args.onnx).resolve()),
        "action_raw_A_mujoco_shadow": action_a,
        "action_raw_B_onnx_same_obs": action_b,
        "action_raw_C_onnx_isaac_injected_obs": action_c,
        "max_abs_diff_A_B": np.asarray(float(np.max(np.abs(action_a - action_b))), dtype=np.float32),
        "max_abs_diff_A_C": np.asarray(float(np.max(np.abs(action_a - action_c))), dtype=np.float32),
        "obs_current_max_abs_diff": np.asarray(float(np.max(np.abs(mujoco_obs_current - isaac_obs_current))), dtype=np.float32),
        "obs_history_max_abs_diff": np.asarray(float(np.max(np.abs(mujoco_obs_history - isaac_obs_history))), dtype=np.float32),
        "history_first_row_diff": np.asarray(
            float(np.max(np.abs(mujoco_obs_history[0] - isaac_obs_history[0]))), dtype=np.float32
        ),
        "history_last_row_diff": np.asarray(
            float(np.max(np.abs(mujoco_obs_history[-1] - isaac_obs_history[-1]))), dtype=np.float32
        ),
        "term_table": np.asarray(_term_table(mujoco_obs_current, isaac_obs_current), dtype=object),
    }

    prefix = Path(args.output_prefix).expanduser()
    prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = prefix.with_suffix(".json")
    csv_path = prefix.with_suffix(".csv")
    json_path.write_text(json.dumps({k: _to_jsonable(v) for k, v in summary.items()}, indent=2), encoding="utf-8")

    lines = ["term,max_abs_diff"]
    for row in summary["term_table"]:
        lines.append(f"{row['term']},{row['max_abs_diff']}")
    csv_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("action_raw_A_mujoco_shadow:", action_a.tolist())
    print("action_raw_B_onnx_same_obs:", action_b.tolist())
    print("action_raw_C_onnx_isaac_injected_obs:", action_c.tolist())
    print("max_abs_diff_A_B:", float(summary["max_abs_diff_A_B"]))
    print("max_abs_diff_A_C:", float(summary["max_abs_diff_A_C"]))
    print("obs_current_max_abs_diff:", float(summary["obs_current_max_abs_diff"]))
    print("obs_history_max_abs_diff:", float(summary["obs_history_max_abs_diff"]))
    print("history_first_row_diff:", float(summary["history_first_row_diff"]))
    print("history_last_row_diff:", float(summary["history_last_row_diff"]))
    for row in summary["term_table"]:
        print(f"{row['term']}: diff={row['max_abs_diff']:.6f}")
    print("saved_json:", json_path)
    print("saved_csv:", csv_path)


if __name__ == "__main__":
    main()
