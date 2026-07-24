# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Validate a wheel/leg-kinematic base-velocity estimator against ground truth.

Runs a trained checkpoint on the *non-Play* task (domain randomization /
actuator delay / IMU+encoder bias events all stay active -- use the plain
``-v0`` task id, not ``-Play-v0``) and, at every step, compares the true
``root_lin_vel_b`` against two candidate estimators built only from
encoder-equivalent signals (joint angles/velocities via resolved body poses,
base orientation) -- never from any privileged base-velocity ground truth:

  - ``naive``: assumes the legs are stationary and the wheel is the only
    source of ground-contact motion. ``v_base_b = -wheel_radius * omega_wheel``
    (rolling-without-slip, no leg-articulation correction), averaged over the
    left/right wheels.
  - ``full``: adds the wheel-center's own velocity relative to the base frame
    (finite-differenced from the wheel body's position expressed in the base
    frame -- this is exactly what an onboard forward-kinematics/Jacobian
    estimator would compute from joint angles+velocities alone, just without
    hand-deriving the URDF rotation chain by hand: IsaacLab already resolves
    body poses from the current joint angles every step, so reading
    ``body_pos_w``/``body_quat_w`` for the wheel body IS the FK output).

Derivation (base-frame, no-slip assumption -- contact point velocity = 0):

    v_contact_b = v_base_b (unknown) + v_relative_b (computed from FK)  =  0
    =>  v_base_b_estimated = -v_relative_b

where ``v_relative_b`` is the contact point's velocity due to internal joint
motion alone (leg swing + wheel spin), entirely reconstructible from body
poses IsaacLab resolves from joint angles -- no ground-truth base velocity
is used anywhere in the estimator itself; it is only used afterward, for
comparison, to report the error.

Logs per-env, per-step rows to CSV: true vx/vy, naive/full estimated vx (per
wheel and averaged), and the leg joint velocity magnitude (to check whether
error grows specifically when the legs are actively moving, not just from
wheel spin).

Example (run only after training the checkpoint you want to validate):
    python scripts/np3o/estimate_base_vel_from_wheels.py \\
        --task=DDT-Velocity-Flat-Tita-My14-v0 \\
        --checkpoint /path/to/model_5000.pt \\
        --num_envs 64 --steps 1000 \\
        --out analysis_runs/wheel_vel_estimate_my14.csv --headless
"""

import argparse
import csv
import importlib

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description='Validate wheel/leg-kinematic base-velocity estimation.')
parser.add_argument('--task', type=str, required=True, help='Gym task ID -- use the plain -v0 task (domain randomization ON), not -Play-v0.')
parser.add_argument('--checkpoint', type=str, required=True, help='Absolute checkpoint path.')
parser.add_argument('--num_envs', type=int, default=64, help='Number of parallel envs to roll out.')
parser.add_argument('--steps', type=int, default=1000, help='Number of policy steps to roll out (1000 steps * 0.02s = 20s).')
parser.add_argument('--wheel_radius', type=float, default=0.0925, help='Wheel radius in meters (from URDF collision geometry).')
parser.add_argument('--out', type=str, default=None, help='Optional CSV path for per-env, per-step rows.')
AppLauncher.add_app_launcher_args(parser)
args_cli, _ = parser.parse_known_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import ddt_lab.tasks  # noqa: F401  -- registers tasks
import gymnasium as gym
import torch
from isaaclab.utils.math import quat_apply, quat_apply_inverse

from ddt_lab.algorithms.np3o import IsaacLabNP3OWrapper, OnConstraintPolicyRunner


def _resolve_runner_cfg(entry_point: str) -> dict:
    module_name, attr = entry_point.split(':')
    obj = getattr(importlib.import_module(module_name), attr)
    cfg = obj() if callable(obj) else obj
    if not isinstance(cfg, dict):
        raise TypeError(f"NP3O cfg entry point '{entry_point}' must return a dict")
    return cfg


def main():
    spec = gym.spec(args_cli.task)
    runner_cfg = _resolve_runner_cfg(spec.kwargs['np3o_cfg_entry_point'])
    env_cfg_entry = spec.kwargs['env_cfg_entry_point']
    env_cfg = env_cfg_entry() if callable(env_cfg_entry) else env_cfg_entry
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device

    env = gym.make(args_cli.task, cfg=env_cfg)
    env = IsaacLabNP3OWrapper(env, device=args_cli.device or 'cuda:0')

    runner = OnConstraintPolicyRunner(env, runner_cfg, log_dir=None, device=args_cli.device or 'cuda:0')
    print(f'[INFO] loading checkpoint: {args_cli.checkpoint}')
    runner.load(args_cli.checkpoint, load_optimizer=False)
    policy = runner.get_inference_policy(args_cli.device or 'cuda:0')

    device = args_cli.device or 'cuda:0'
    step_dt = float(env.unwrapped.step_dt)
    robot = env.unwrapped.scene["robot"]
    wheel_radius = args_cli.wheel_radius

    base_ids, _ = robot.find_bodies("base_link")
    left_wheel_ids, _ = robot.find_bodies("left_leg_4")
    right_wheel_ids, _ = robot.find_bodies("right_leg_4")
    left_wheel_joint_ids, _ = robot.find_joints("joint_left_leg_4")
    right_wheel_joint_ids, _ = robot.find_joints("joint_right_leg_4")
    leg_joint_ids, _ = robot.find_joints([".*_leg_[123]"])
    base_id, left_wheel_id, right_wheel_id = base_ids[0], left_wheel_ids[0], right_wheel_ids[0]
    left_wheel_joint_id, right_wheel_joint_id = left_wheel_joint_ids[0], right_wheel_joint_ids[0]
    print(f'[INFO] base_id={base_id} left_wheel_id={left_wheel_id} right_wheel_id={right_wheel_id}')
    print(f'[INFO] left_wheel_joint_id={left_wheel_joint_id} right_wheel_joint_id={right_wheel_joint_id}')
    print(f'[INFO] leg_joint_ids={leg_joint_ids}')

    local_spin_axis = torch.tensor([0.0, 0.0, 1.0], device=device).expand(args_cli.num_envs, 3)
    contact_offset_w = torch.tensor([0.0, 0.0, -wheel_radius], device=device).expand(args_cli.num_envs, 3)

    def wheel_rel_base_b(wheel_id: int) -> torch.Tensor:
        base_pos_w = robot.data.body_pos_w[:, base_id]
        base_quat_w = robot.data.body_quat_w[:, base_id]
        wheel_pos_w = robot.data.body_pos_w[:, wheel_id]
        return quat_apply_inverse(base_quat_w, wheel_pos_w - base_pos_w)

    def spin_contribution_b(wheel_id: int, wheel_joint_id: int) -> torch.Tensor:
        base_quat_w = robot.data.body_quat_w[:, base_id]
        wheel_quat_w = robot.data.body_quat_w[:, wheel_id]
        spin_axis_w = quat_apply(wheel_quat_w, local_spin_axis)
        wheel_omega = robot.data.joint_vel[:, wheel_joint_id].unsqueeze(-1)
        v_spin_w = wheel_omega * torch.cross(spin_axis_w, contact_offset_w, dim=-1)
        return quat_apply_inverse(base_quat_w, v_spin_w)

    policy_obs = env.reset()

    prev_left_rel_b = wheel_rel_base_b(left_wheel_id)
    prev_right_rel_b = wheel_rel_base_b(right_wheel_id)
    valid_mask = torch.zeros(args_cli.num_envs, dtype=torch.bool, device=device)  # False until we have a valid prev frame

    rows = []
    fieldnames = [
        "step", "env_id", "true_vx", "true_vy",
        "est_naive_vx_left", "est_naive_vx_right", "est_naive_vx",
        "est_full_vx_left", "est_full_vx_right", "est_full_vx",
        "leg_joint_vel_norm",
    ]

    with torch.inference_mode():
        for step in range(args_cli.steps):
            actions = policy(policy_obs)
            policy_obs, _critic_obs, _rewards, _costs, dones, _infos = env.step(actions)

            left_rel_b = wheel_rel_base_b(left_wheel_id)
            right_rel_b = wheel_rel_base_b(right_wheel_id)

            v_leg_left_b = (left_rel_b - prev_left_rel_b) / step_dt
            v_leg_right_b = (right_rel_b - prev_right_rel_b) / step_dt

            v_spin_left_b = spin_contribution_b(left_wheel_id, left_wheel_joint_id)
            v_spin_right_b = spin_contribution_b(right_wheel_id, right_wheel_joint_id)

            est_naive_left = -v_spin_left_b[:, 0]
            est_naive_right = -v_spin_right_b[:, 0]
            est_full_left = -(v_leg_left_b[:, 0] + v_spin_left_b[:, 0])
            est_full_right = -(v_leg_right_b[:, 0] + v_spin_right_b[:, 0])

            true_vx = robot.data.root_lin_vel_b[:, 0]
            true_vy = robot.data.root_lin_vel_b[:, 1]
            leg_joint_vel_norm = torch.linalg.norm(robot.data.joint_vel[:, leg_joint_ids], dim=-1)

            if step > 0:
                for env_id in range(args_cli.num_envs):
                    if not valid_mask[env_id]:
                        continue
                    rows.append({
                        "step": step,
                        "env_id": env_id,
                        "true_vx": true_vx[env_id].item(),
                        "true_vy": true_vy[env_id].item(),
                        "est_naive_vx_left": est_naive_left[env_id].item(),
                        "est_naive_vx_right": est_naive_right[env_id].item(),
                        "est_naive_vx": 0.5 * (est_naive_left[env_id].item() + est_naive_right[env_id].item()),
                        "est_full_vx_left": est_full_left[env_id].item(),
                        "est_full_vx_right": est_full_right[env_id].item(),
                        "est_full_vx": 0.5 * (est_full_left[env_id].item() + est_full_right[env_id].item()),
                        "leg_joint_vel_norm": leg_joint_vel_norm[env_id].item(),
                    })

            # envs that reset this step get a fresh (valid) prev-frame next iteration,
            # but this step's finite-difference (which spanned the reset) is invalid.
            valid_mask = ~dones
            prev_left_rel_b = left_rel_b
            prev_right_rel_b = right_rel_b

            if (step + 1) % 100 == 0:
                print(f'[INFO] step {step + 1}/{args_cli.steps}')

    import numpy as np
    true_vx_arr = np.array([r["true_vx"] for r in rows])
    naive_err = np.array([r["est_naive_vx"] for r in rows]) - true_vx_arr
    full_err = np.array([r["est_full_vx"] for r in rows]) - true_vx_arr
    leg_vel = np.array([r["leg_joint_vel_norm"] for r in rows])

    print("\n" + "=" * 60)
    print(f"[RESULT] task={args_cli.task}  checkpoint={args_cli.checkpoint}")
    print(f"[RESULT] rows={len(rows)}")
    print("-" * 60)
    print(f"naive estimator : RMSE={np.sqrt(np.mean(naive_err ** 2)):.4f}  bias={naive_err.mean():.4f}  std={naive_err.std():.4f}")
    print(f"full estimator  : RMSE={np.sqrt(np.mean(full_err ** 2)):.4f}  bias={full_err.mean():.4f}  std={full_err.std():.4f}")

    median_leg_vel = np.median(leg_vel)
    low_mask = leg_vel <= median_leg_vel
    high_mask = ~low_mask
    print("-" * 60)
    print(f"leg_joint_vel_norm median split: low<={median_leg_vel:.3f} rad/s, high>{median_leg_vel:.3f} rad/s")
    print(f"naive RMSE  low-leg-motion={np.sqrt(np.mean(naive_err[low_mask] ** 2)):.4f}  high-leg-motion={np.sqrt(np.mean(naive_err[high_mask] ** 2)):.4f}")
    print(f"full  RMSE  low-leg-motion={np.sqrt(np.mean(full_err[low_mask] ** 2)):.4f}  high-leg-motion={np.sqrt(np.mean(full_err[high_mask] ** 2)):.4f}")
    print("=" * 60)

    if args_cli.out:
        with open(args_cli.out, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f'[INFO] rows written to {args_cli.out}')

    env.unwrapped.close()


if __name__ == '__main__':
    main()
    simulation_app.close()
