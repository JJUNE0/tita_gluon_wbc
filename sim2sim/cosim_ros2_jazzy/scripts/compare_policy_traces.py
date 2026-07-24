#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


TERM_SLICES = {
    "base_ang_vel": slice(0, 3),
    "projected_gravity": slice(3, 6),
    "command": slice(6, 9),
    "joint_pos_error": slice(9, 17),
    "joint_vel": slice(17, 25),
    "last_action": slice(25, 33),
}


def _load_npz(path: str) -> dict[str, np.ndarray]:
    with np.load(Path(path).expanduser(), allow_pickle=False) as data:
        return {k: np.asarray(data[k]) for k in data.files}


def _max_abs_diff(a: np.ndarray, b: np.ndarray) -> float:
    if a.shape != b.shape:
        return float("inf")
    diff = a.astype(np.float64) - b.astype(np.float64)
    valid = ~np.isnan(diff)
    if not np.any(valid):
        return 0.0
    return float(np.max(np.abs(diff[valid])))


def _shape(value: np.ndarray | None) -> str:
    return "missing" if value is None else str(tuple(value.shape))


def _onnx_action(policy_path: str, obs: np.ndarray, hist: np.ndarray) -> np.ndarray:
    import onnxruntime as ort

    session = ort.InferenceSession(str(Path(policy_path).expanduser()), providers=["CPUExecutionProvider"])
    inputs = session.get_inputs()
    outputs = session.get_outputs()
    result = session.run(
        [outputs[0].name],
        {
            inputs[0].name: obs.astype(np.float32).reshape(1, 33),
            inputs[1].name: hist.astype(np.float32).reshape(1, 10, 33),
        },
    )[0]
    return np.asarray(result, dtype=np.float32).reshape(8)


def _history_suspicion(isaac_hist: np.ndarray, mujoco_hist: np.ndarray) -> str:
    if isaac_hist.shape != mujoco_hist.shape:
        return "shape mismatch"
    normal = _max_abs_diff(isaac_hist, mujoco_hist)
    reversed_time = _max_abs_diff(isaac_hist, mujoco_hist[::-1])
    isaac_repeated_current = float(np.max(np.abs(isaac_hist - isaac_hist[-1]))) if isaac_hist.size else float("inf")
    mujoco_repeated_current = float(np.max(np.abs(mujoco_hist - mujoco_hist[-1]))) if mujoco_hist.size else float("inf")
    notes = [
        f"normal={normal:.6g}",
        f"mujoco_time_reversed={reversed_time:.6g}",
        f"isaac_rows_identical={isaac_repeated_current < 1e-6}",
        f"mujoco_rows_identical={mujoco_repeated_current < 1e-6}",
    ]
    if mujoco_repeated_current < 1e-6:
        notes.append("mujoco_history_rows_are_identical")
    if isaac_repeated_current < 1e-6:
        notes.append("isaac_history_rows_are_identical")
    if reversed_time + 1e-6 < normal:
        notes.append("possible_time_order_mismatch")
    return ", ".join(notes)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--isaac", required=True)
    parser.add_argument("--mujoco", required=True)
    parser.add_argument(
        "--policy",
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/policy.onnx",
        help="Exported ONNX policy used for same-input verification.",
    )
    parser.add_argument(
        "--output-prefix",
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/policy_trace_comparison",
        help="Output path prefix. Writes <prefix>.json and <prefix>.csv.",
    )
    args = parser.parse_args()

    isaac = _load_npz(args.isaac)
    mujoco = _load_npz(args.mujoco)
    rows: list[dict[str, str | float]] = []

    for key in [
        "obs_current",
        "obs_history",
        "policy_action_raw",
        "policy_action_used",
        "target_leg_pos",
        "target_wheel_vel",
    ]:
        a = isaac.get(key)
        b = mujoco.get(key)
        rows.append(
            {
                "name": key,
                "isaac_shape": _shape(a),
                "mujoco_shape": _shape(b),
                "max_abs_diff": _max_abs_diff(a, b) if a is not None and b is not None else float("inf"),
            }
        )

    isaac_obs = isaac.get("obs_current")
    mujoco_obs = mujoco.get("obs_current")
    if isaac_obs is not None and mujoco_obs is not None:
        isaac_obs = isaac_obs.reshape(33)
        mujoco_obs = mujoco_obs.reshape(33)
        for name, sl in TERM_SLICES.items():
            rows.append(
                {
                    "name": name,
                    "isaac_shape": str(tuple(isaac_obs[sl].shape)),
                    "mujoco_shape": str(tuple(mujoco_obs[sl].shape)),
                    "max_abs_diff": _max_abs_diff(isaac_obs[sl], mujoco_obs[sl]),
                }
            )

    isaac_hist = isaac.get("obs_history")
    mujoco_hist = mujoco.get("obs_history")
    history_note = "missing"
    if isaac_hist is not None and mujoco_hist is not None:
        isaac_hist = isaac_hist.reshape(10, 33)
        mujoco_hist = mujoco_hist.reshape(10, 33)
        for name, a_row, b_row in [
            ("history_first_row", isaac_hist[0], mujoco_hist[0]),
            ("history_last_row", isaac_hist[-1], mujoco_hist[-1]),
        ]:
            rows.append(
                {
                    "name": name,
                    "isaac_shape": str(tuple(a_row.shape)),
                    "mujoco_shape": str(tuple(b_row.shape)),
                    "max_abs_diff": _max_abs_diff(a_row, b_row),
                }
            )
        history_note = _history_suspicion(isaac_hist, mujoco_hist)

    for key in [
        "steps_obs_current",
        "steps_joint_pos_error",
        "steps_joint_vel",
        "steps_policy_action_raw",
        "steps_policy_action_used",
        "steps_target_leg_pos",
        "steps_target_wheel_vel",
    ]:
        a = isaac.get(key)
        b = mujoco.get(key)
        if a is None or b is None:
            continue
        max_steps = min(a.shape[0], b.shape[0], 2)
        for idx in range(max_steps):
            rows.append(
                {
                    "name": f"{key}[{idx}]",
                    "isaac_shape": str(tuple(a[idx].shape)),
                    "mujoco_shape": str(tuple(b[idx].shape)),
                    "max_abs_diff": _max_abs_diff(a[idx], b[idx]),
                }
            )

    onnx_summary = {}
    if isaac_obs is not None and mujoco_obs is not None and isaac_hist is not None and mujoco_hist is not None:
        onnx_isaac = _onnx_action(args.policy, isaac_obs, isaac_hist)
        onnx_mujoco = _onnx_action(args.policy, mujoco_obs, mujoco_hist)
        isaac_recorded = isaac.get("policy_action_raw")
        mujoco_recorded = mujoco.get("policy_action_raw")
        onnx_summary = {
            "onnx_isaac_input": onnx_isaac.tolist(),
            "onnx_mujoco_input": onnx_mujoco.tolist(),
            "onnx_input_action_diff": _max_abs_diff(onnx_isaac, onnx_mujoco),
            "onnx_vs_isaac_recorded": _max_abs_diff(onnx_isaac, isaac_recorded.reshape(8)) if isaac_recorded is not None else float("inf"),
            "onnx_vs_mujoco_recorded": _max_abs_diff(onnx_mujoco, mujoco_recorded.reshape(8)) if mujoco_recorded is not None else float("inf"),
        }
        rows.append(
            {
                "name": "ONNX(isaac_input)_vs_ONNX(mujoco_input)",
                "isaac_shape": "(8,)",
                "mujoco_shape": "(8,)",
                "max_abs_diff": onnx_summary["onnx_input_action_diff"],
            }
        )

    summary = {
        "isaac_trace": str(Path(args.isaac).expanduser()),
        "mujoco_trace": str(Path(args.mujoco).expanduser()),
        "policy": str(Path(args.policy).expanduser()),
        "rows": rows,
        "history_note": history_note,
        "onnx": onnx_summary,
    }

    for row in rows:
        print(
            f"{row['name']}: isaac={row['isaac_shape']} mujoco={row['mujoco_shape']} "
            f"max_abs_diff={float(row['max_abs_diff']):.9g}"
        )
    print("history:", history_note)
    if onnx_summary:
        print("onnx_vs_isaac_recorded:", f"{onnx_summary['onnx_vs_isaac_recorded']:.9g}")
        print("onnx_vs_mujoco_recorded:", f"{onnx_summary['onnx_vs_mujoco_recorded']:.9g}")

    prefix = Path(args.output_prefix).expanduser()
    prefix.parent.mkdir(parents=True, exist_ok=True)
    with open(prefix.with_suffix(".json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    with open(prefix.with_suffix(".csv"), "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "isaac_shape", "mujoco_shape", "max_abs_diff"])
        writer.writeheader()
        writer.writerows(rows)
    print("saved_summary_json:", prefix.with_suffix(".json"))
    print("saved_summary_csv:", prefix.with_suffix(".csv"))


if __name__ == "__main__":
    main()
