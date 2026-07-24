#!/usr/bin/env python3
"""MuJoCo-side accuracy check for `My26`'s learned ``base_lin_vel`` estimator
MLP against ground truth (MuJoCo knows the true root velocity exactly --
unlike real hardware, this is the natural place to validate the estimator
before ever touching hardware).

Standalone offline sim (no ROS2, no viewer) -- does not touch the live
sim2sim node the user is driving via the MuJoCo passive viewer. Reuses the
same ``TitaMujocoEnv``/``ObservationBuilder``/``ActionAdapter`` deployment
pipeline as ``dry_run_initial_policy.py``, but runs the debug ONNX
(``policy_my26_*_debug.onnx``, two outputs: ``nn_output`` + ``est_vel``,
exported by ``scripts/rsl_rl/play.py``'s ``EstimatorAdapterDebug``) through a
scripted settle/zero-hold/ramp-up/cruise/decel command profile, mirroring
``scripts/rsl_rl/eval_estimator_accuracy.py``'s Isaac Lab probe for a direct
comparison.

Example:
    python cosim_ros2_jazzy/scripts/eval_estimator_accuracy_mujoco.py \\
        --config cosim_ros2_jazzy/config/tita_my26.yaml \\
        --debug-policy deploy/tita/policy_my26_1999_debug.onnx
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import yaml

from cosim_ros2_jazzy.action_adapter import ActionAdapter
from cosim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from cosim_ros2_jazzy.obs_builder import ObsState, ObservationBuilder, quat_wxyz_to_rotmat


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="cosim_ros2_jazzy/config/tita_my26.yaml")
    parser.add_argument(
        "--debug-policy", default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/policy_my26_1999_debug.onnx",
        help="ONNX exposing both nn_output (action) and est_vel (raw, scaled estimator prediction).",
    )
    parser.add_argument("--settle_s", type=float, default=1.0)
    parser.add_argument("--hold_s", type=float, default=3.0)
    parser.add_argument("--ramp_vx", type=float, default=0.8)
    parser.add_argument("--ramp_up_s", type=float, default=1.0)
    parser.add_argument("--cruise_s", type=float, default=3.0)
    parser.add_argument("--decel_s", type=float, default=2.0)
    parser.add_argument("--viewer", action="store_true", help="Show the MuJoCo passive viewer, real-time paced.")
    parser.add_argument(
        "--yaw_offset_deg", type=float, default=0.0,
        help="Rotate the spawn heading about Z by this many degrees (e.g. 180 to face -X, "
        "away from terrain features in +X like stairs).",
    )
    args = parser.parse_args()

    import onnxruntime as ort

    with open(Path(args.config).expanduser(), "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["viewer"]["enabled"] = bool(args.viewer)
    cfg["control"]["real_time"] = bool(args.viewer)

    if cfg["policy"].get("include_base_lin_vel", False):
        raise ValueError(
            "This probe is for My26-style debug ONNX (pure 33-dim proprio input, estimator baked in). "
            "Got include_base_lin_vel=true in config -- wrong config for this checkpoint."
        )

    if args.yaw_offset_deg != 0.0:
        half = np.radians(args.yaw_offset_deg) / 2.0
        # MuJoCo freejoint quat is [w, x, y, z]; pure yaw rotation about Z.
        cfg["robot"]["reset_base_quat"] = [float(np.cos(half)), 0.0, 0.0, float(np.sin(half))]

    env = TitaMujocoEnv(cfg, viewer_enabled=bool(args.viewer))
    # TitaMujocoEnv doesn't auto-reset to the training-default standing pose
    # on construction -- without this the sim starts from the XML's raw
    # keyframe pose and the policy (never trained on that state) falls
    # partway through the scripted profile.
    env.reset()
    obs_builder = ObservationBuilder(cfg)
    adapter = ActionAdapter(cfg)
    session = ort.InferenceSession(args.debug_policy, providers=["CPUExecutionProvider"])
    input_name = cfg["policy"]["input_obs_name"]
    obs_dim = int(cfg["policy"]["obs_dim"])
    action_dim = int(cfg["policy"]["action_dim"])

    # scale=2.0 applied to the estimator_target ObsTerm (mdp.base_lin_vel) at
    # training time -- the raw est_vel output lives in that scaled space.
    est_scale = float(cfg["observation"].get("base_lin_vel_scale", 2.0))

    physics_dt = float(env.model.opt.timestep)
    policy_dt = physics_dt * env.decimation

    def n_steps(seconds: float) -> int:
        return max(1, round(seconds / policy_dt))

    settle_n = n_steps(args.settle_s)
    hold_n = n_steps(args.hold_s)
    ramp_n = n_steps(args.ramp_up_s)
    cruise_n = n_steps(args.cruise_s)
    decel_n = n_steps(args.decel_s)

    phases = [
        ("settle", settle_n, lambda i: 0.0),
        ("zero_hold", hold_n, lambda i: 0.0),
        ("ramp_up", ramp_n, lambda i: args.ramp_vx * (i + 1) / ramp_n),
        ("cruise", cruise_n, lambda i: args.ramp_vx),
        ("decel", decel_n, lambda i: 0.0),
    ]

    last_action = np.zeros(action_dim, dtype=np.float32)

    def build_obs(cmd_vx: float) -> np.ndarray:
        command = np.array([cmd_vx, 0.0, 0.0], dtype=np.float32)
        obs_state = ObsState(
            joint_pos=env.joint_pos(),
            joint_vel=env.joint_vel(),
            base_quat_wxyz=env.base_quat_sensor(),
            base_ang_vel=env.base_ang_vel(),
            command=command,
            last_action=last_action,
        )
        return obs_builder.build(obs_state)

    init_obs = build_obs(0.0)
    obs_builder.reset_history(init_obs)

    errors = {name: [] for name, _, _ in phases}

    num_loops = 0
    while True:
        num_loops += 1
        for name, count, cmd_fn in phases:
            for i in range(count):
                if args.viewer and not env.is_running():
                    break
                obs = build_obs(float(cmd_fn(i)))
                feed = {input_name: obs.reshape(1, obs_dim).astype(np.float32)}
                action, est_vel_scaled = session.run(["nn_output", "est_vel"], feed)
                action = np.asarray(action, dtype=np.float32).reshape(action_dim)
                est_vel_scaled = np.asarray(est_vel_scaled, dtype=np.float32).reshape(3)
                est_pred = est_vel_scaled / est_scale  # body-frame m/s

                quat = env.base_quat_sensor()
                rot = quat_wxyz_to_rotmat(quat)
                true_vel = rot.T @ env.base_lin_vel()  # world -> body frame, m/s
                base_z = float(env.base_pos()[2])

                errors[name].append(est_pred - true_vel)
                if args.viewer and base_z < 0.20:
                    print(f"[{name} step={i}] base_pos_z={base_z:.3f} -- robot appears to have fallen")

                torque, debug = adapter.compute(action, env.joint_pos(), env.joint_vel())

                def torque_callback(joint_pos_now, joint_vel_now):
                    sub_torque, _ = adapter.compute(action, joint_pos_now, joint_vel_now)
                    return sub_torque

                env.step_with_torque_callback(torque_callback, sleep=bool(args.viewer))
                obs_builder.push_history(obs)
                last_action = debug.action_raw_by_joint.astype(np.float32)
        if not args.viewer or not env.is_running():
            break
        print(f"[INFO] loop {num_loops} complete -- resetting and repeating (close the viewer window to stop)")
        env.reset()
        last_action[:] = 0.0
        init_obs = build_obs(0.0)
        obs_builder.reset_history(init_obs)

    print("")
    print("=" * 70)
    print(f"[RESULT] config={args.config}")
    print(f"[RESULT] debug_policy={args.debug_policy}")
    print("-" * 70)
    print(f"{'phase':<12}{'rmse_x':>10}{'rmse_y':>10}{'rmse_z':>10}{'rmse_|xyz|':>12}{'n_steps':>10}")
    for name, _, _ in phases:
        err = np.stack(errors[name], axis=0)  # (steps, 3)
        rmse_xyz = np.sqrt((err ** 2).mean(axis=0))
        rmse_norm = np.sqrt((err ** 2).sum(axis=1)).mean()
        print(
            f"{name:<12}{rmse_xyz[0]:>10.4f}{rmse_xyz[1]:>10.4f}"
            f"{rmse_xyz[2]:>10.4f}{rmse_norm:>12.4f}{len(errors[name]):>10}"
        )
    print("-" * 70)
    all_err = np.concatenate([np.stack(errors[n], axis=0) for n, _, _ in phases], axis=0)
    overall_rmse_x = np.sqrt((all_err[:, 0] ** 2).mean())
    print(f"overall rmse_x (all phases combined): {overall_rmse_x:.4f} m/s")
    print("Naive wheel-vel estimator reference (My18, Experiments/RL_Experiments.md):")
    print("  RMSE ~0.10 m/s near-standstill, ~0.32 m/s during active gait")
    print("=" * 70)

    env.close()


if __name__ == "__main__":
    main()
