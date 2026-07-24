#!/usr/bin/env python3
"""Reproduce the real My26@1700 zero-command backward-wheel behavior in headless
MuJoCo by initializing the sim in the real robot's exact logged posture (joint
positions/velocities, base orientation, base angular velocity) instead of the
default trained standing pose, then running zero-command policy inference.

Domain: DESKTOP_DRY_RUN. Offline, no ROS2, no hardware, no live viewer node
touched.

Motivation: the real zero-command log
(analysis_runs/my26_zero_command_estimator_real_20260722) shows that at the
first RL_RUNNING row, both leg_3 knee joints were still at approximately
-2.64 / -2.65 rad -- near reference_transform_up.stand_jpos (-2.6), not the
trained default_joint_angles knee value of -1.5 rad used for pos_rel/PD
targets. That is an obs pos_rel error of about -1.14 rad on that single
dimension, well outside anything seen in training. This script tests, purely
in simulation (so no real-hardware friction/COM/actuator confound is
possible), whether reproducing that exact posture is by itself sufficient to
trigger the same persistent negative wheel action / estimator output, as an
A/B against starting from the trained standing pose with the same policy.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
import yaml

from cosim_ros2_jazzy.action_adapter import ActionAdapter
from cosim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from cosim_ros2_jazzy.obs_builder import ObsState, ObservationBuilder

WHEEL_RADIUS_M = 0.0925


def load_real_first_rl_state(csv_path: Path) -> dict:
    with open(csv_path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    idx = {name: i for i, name in enumerate(header)}
    first_rl = next(row for row in rows if row[idx["controller_state"]] == "4.0")

    def col(prefix: str, n: int) -> np.ndarray:
        return np.array([float(first_rl[idx[f"{prefix}_{i}"]]) for i in range(n)], dtype=np.float64)

    quat_xyzw = col("imu_quat_xyzw", 4)
    quat_wxyz = np.array([quat_xyzw[3], quat_xyzw[0], quat_xyzw[1], quat_xyzw[2]], dtype=np.float64)
    return {
        "joint_pos": col("joint_pos", 8),
        "joint_vel": col("joint_vel", 8),
        "quat_wxyz": quat_wxyz,
        "gyro": col("imu_ang_vel", 3),
    }


def run_condition(cfg: dict, real_state: dict, use_real_pose: bool, duration_s: float, out_csv: Path) -> list[dict]:
    import onnxruntime as ort

    env = TitaMujocoEnv(cfg, viewer_enabled=False)
    env.reset()
    if use_real_pose:
        env.data.qpos[3:7] = real_state["quat_wxyz"]
        env.data.qpos[env.qpos_addr] = real_state["joint_pos"]
        env.data.qvel[3:6] = real_state["gyro"]
        env.data.qvel[env.qvel_addr] = real_state["joint_vel"]
        env.mujoco.mj_forward(env.model, env.data)

    obs_builder = ObservationBuilder(cfg)
    adapter = ActionAdapter(cfg)

    session = ort.InferenceSession(cfg["policy"]["path"], providers=["CPUExecutionProvider"])
    input_name = cfg["policy"]["input_obs_name"]
    obs_dim = int(cfg["policy"]["obs_dim"])
    action_dim = int(cfg["policy"]["action_dim"])
    est_scale = float(cfg["observation"].get("base_lin_vel_scale", 2.0))
    wheel_indices = list(cfg["robot"]["wheel_indices"])

    out_names = [o.name for o in session.get_outputs()]
    est_name = next(n for n in out_names if n != "nn_output")

    last_action = np.zeros(action_dim, dtype=np.float32)

    def build_obs() -> np.ndarray:
        state = ObsState(
            joint_pos=env.joint_pos(),
            joint_vel=env.joint_vel(),
            base_quat_wxyz=env.base_quat_sensor(),
            base_ang_vel=env.base_ang_vel(),
            command=np.zeros(3, dtype=np.float32),
            last_action=last_action,
        )
        return obs_builder.build(state)

    init_obs = build_obs()
    obs_builder.reset_history(init_obs)

    policy_dt = env.model.opt.timestep * env.decimation
    n_steps = max(1, round(duration_s / policy_dt))

    rows: list[dict] = []
    est_integral = 0.0
    wheel_integral = 0.0
    for step in range(n_steps):
        obs = build_obs()
        outputs = session.run(None, {input_name: obs.reshape(1, obs_dim).astype(np.float32)})
        action = np.asarray(outputs[out_names.index("nn_output")], dtype=np.float32).reshape(action_dim)
        est_scaled = np.asarray(outputs[out_names.index(est_name)], dtype=np.float32).reshape(3)
        est_mps = est_scaled / est_scale

        def torque_callback(jp, jv, _action=action):
            t, _ = adapter.compute(_action, jp, jv)
            return t

        env.step_with_torque_callback(torque_callback, sleep=False)
        obs_builder.push_history(obs)
        _, debug = adapter.compute(action, env.joint_pos(), env.joint_vel())
        last_action = debug.action_raw_by_joint.astype(np.float32)

        jv = env.joint_vel()
        jp = env.joint_pos()
        wheel_common = 0.5 * (float(jv[wheel_indices[0]]) + float(jv[wheel_indices[1]]))
        wheel_no_slip = wheel_common * WHEEL_RADIUS_M
        est_integral += float(est_mps[0]) * policy_dt
        wheel_integral += float(wheel_no_slip) * policy_dt

        rows.append(
            {
                "t": step * policy_dt,
                "est_vx": float(est_mps[0]),
                "wheel_L_rad_s": float(jv[wheel_indices[0]]),
                "wheel_R_rad_s": float(jv[wheel_indices[1]]),
                "wheel_no_slip_mps": float(wheel_no_slip),
                "est_integral_m": est_integral,
                "wheel_integral_m": wheel_integral,
                "action_wheel_L": float(action[wheel_indices[0]]),
                "action_wheel_R": float(action[wheel_indices[1]]),
                "leg3_L_rad": float(jp[2]),
                "leg3_R_rad": float(jp[6]),
                "base_z_m": float(env.base_pos()[2]),
            }
        )

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    env.close()
    return rows


def summarize(rows: list[dict], window_s: float, policy_dt: float) -> dict:
    n = max(1, round(window_s / policy_dt))
    n = min(n, len(rows))
    sub = rows[:n]
    est = np.array([r["est_vx"] for r in sub])
    wheel_no_slip = np.array([r["wheel_no_slip_mps"] for r in sub])
    wl = np.array([r["wheel_L_rad_s"] for r in sub])
    wr = np.array([r["wheel_R_rad_s"] for r in sub])
    return {
        "n_steps": n,
        "est_vx_mean": float(est.mean()),
        "est_vx_std": float(est.std()),
        "wheel_no_slip_mean": float(wheel_no_slip.mean()),
        "wheel_L_mean": float(wl.mean()),
        "wheel_R_mean": float(wr.mean()),
        "est_integral_m": sub[-1]["est_integral_m"],
        "wheel_integral_m": sub[-1]["wheel_integral_m"],
        "leg3_L_final": sub[-1]["leg3_L_rad"],
        "leg3_R_final": sub[-1]["leg3_R_rad"],
        "base_z_final": sub[-1]["base_z_m"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="cosim_ros2_jazzy/config/tita_my26_1700.yaml")
    parser.add_argument(
        "--real_log",
        default="analysis_runs/my26_zero_command_estimator_real_20260722/estimator/estimator_step_log.csv",
    )
    parser.add_argument("--duration_s", type=float, default=10.0)
    parser.add_argument("--out_dir", default="analysis_runs/my26_real_pose_mujoco_replay_20260722")
    args = parser.parse_args()

    with open(Path(args.config), "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    real_state = load_real_first_rl_state(Path(args.real_log))

    out_dir = Path(args.out_dir)
    policy_dt = 0.005 * int(cfg["control"]["decimation"])

    print("=" * 70)
    print("Condition A: MuJoCo default trained standing pose (control)")
    rows_a = run_condition(cfg, real_state, use_real_pose=False, duration_s=args.duration_s, out_csv=out_dir / "condition_a_default_pose.csv")
    summary_a = summarize(rows_a, window_s=args.duration_s, policy_dt=policy_dt)
    for k, v in summary_a.items():
        print(f"  {k}: {v}")

    print("-" * 70)
    print("Condition B: MuJoCo initialized to real robot's logged RL-entry posture")
    rows_b = run_condition(cfg, real_state, use_real_pose=True, duration_s=args.duration_s, out_csv=out_dir / "condition_b_real_pose.csv")
    summary_b = summarize(rows_b, window_s=args.duration_s, policy_dt=policy_dt)
    for k, v in summary_b.items():
        print(f"  {k}: {v}")

    print("=" * 70)
    print("Real hardware reference (first 10 s, from Sim2Sim_Experiments.md / handoff doc):")
    print("  estimator vx mean/std: -0.1256 / 0.0664 m/s")
    print("  wheel no-slip mean:    -0.1600 m/s")
    print("  wheel L/R mean:        -1.7247 / -1.7350 rad/s")
    print("=" * 70)


if __name__ == "__main__":
    main()
