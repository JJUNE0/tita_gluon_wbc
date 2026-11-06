# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Scripted behavioral probe for a trained plain-RSL-RL-PPO checkpoint.

Sibling to ``scripts/np3o/eval_behavior.py`` -- identical scripted-command
core (command-forcing only touches ``command_manager``, algorithm-independent)
and identical drift/decel-shake metrics, so results are directly comparable
across the NP3O and RSL-RL tracks. Only the checkpoint-loading section
differs (``isaaclab_rl.rsl_rl.RslRlVecEnvWrapper`` +
``rsl_rl.runners.OnPolicyRunner`` instead of NP3O's custom wrapper/runner).

Example:
    python scripts/rsl_rl/eval_behavior.py \\
        --task=DDT-Velocity-Flat-Tita-My7-RSL-Play-v0 \\
        --checkpoint /path/to/model_5799.pt \\
        --out analysis_runs/behavior_my7rsl.csv --headless
"""

import argparse
import csv
import importlib
import os

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description='Scripted zero-command-drift / decel-shake probe (RSL-RL).')
parser.add_argument('--task', type=str, required=True, help='Gym task ID (use a *-Play-v0 variant).')
parser.add_argument('--checkpoint', type=str, required=True, help='Absolute checkpoint path.')
parser.add_argument('--num_envs', type=int, default=8, help='Number of envs (averaged in the summary).')
parser.add_argument('--settle_s', type=float, default=1.0, help='Time to let the robot settle after reset, cmd=0.')
parser.add_argument('--hold_s', type=float, default=3.0, help='Zero-command hold duration (drift probe).')
parser.add_argument('--ramp_vx', type=float, default=0.8, help='Target forward vx to ramp up to before cutting.')
parser.add_argument('--ramp_up_s', type=float, default=1.0, help='Ramp-up duration from 0 to --ramp_vx.')
parser.add_argument('--cruise_s', type=float, default=2.0, help='Hold duration at --ramp_vx before the cut.')
parser.add_argument('--decel_window_s', type=float, default=1.5, help='Window after the abrupt cut to measure shake.')
parser.add_argument('--out', type=str, default=None, help='Optional CSV path for the env-averaged time series.')
AppLauncher.add_app_launcher_args(parser)
args_cli, _ = parser.parse_known_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import ddt_lab.tasks  # noqa: F401  -- registers tasks
import gymnasium as gym
import torch

from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper
from rsl_rl.runners import OnPolicyRunner

# Inject the learned base_lin_vel estimator classes into on_policy_runner's
# eval() namespace so EstimatorActorCriticCfg/EstimatorPPOCfg's class_name
# strings resolve (needed for My26-style checkpoints), with zero changes to
# the installed rsl_rl package. No-op for plain-PPO checkpoints. See
# docs/plan_base_vel_estimator_ppo.md.
import rsl_rl.runners.on_policy_runner as _opr
from ddt_lab.algorithms.estimator import ActorCriticWithEstimator, PPOWithEstimator

_opr.ActorCriticWithEstimator = ActorCriticWithEstimator
_opr.PPOWithEstimator = PPOWithEstimator


def _resolve_agent_cfg(entry_point: str):
    module_name, attr = entry_point.split(':')
    obj = getattr(importlib.import_module(module_name), attr)
    return obj() if callable(obj) else obj


def main():
    spec = gym.spec(args_cli.task)
    agent_cfg = _resolve_agent_cfg(spec.kwargs['rsl_rl_cfg_entry_point'])
    env_cfg_entry = spec.kwargs['env_cfg_entry_point']
    env_cfg = env_cfg_entry() if callable(env_cfg_entry) else env_cfg_entry
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device

    env = gym.make(args_cli.task, cfg=env_cfg)
    env = RslRlVecEnvWrapper(env, clip_actions=agent_cfg.clip_actions)

    runner = OnPolicyRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    print(f'[INFO] loading checkpoint: {args_cli.checkpoint}')
    runner.load(args_cli.checkpoint, load_optimizer=False)
    policy = runner.get_inference_policy(device=agent_cfg.device)

    step_dt = float(env.unwrapped.step_dt)
    robot = env.unwrapped.scene["robot"]
    cmd_term = env.unwrapped.command_manager.get_command("base_velocity")

    joint_names = [
        "joint_left_leg_1", "joint_left_leg_2", "joint_left_leg_3", "joint_left_leg_4",
        "joint_right_leg_1", "joint_right_leg_2", "joint_right_leg_3", "joint_right_leg_4",
    ]
    joint_ids = [robot.find_joints(n)[0][0] for n in joint_names]
    default_joint_pos = robot.data.default_joint_pos[:, joint_ids].clone()

    def n_steps(seconds: float) -> int:
        return max(1, round(seconds / step_dt))

    settle_n = n_steps(args_cli.settle_s)
    hold_n = n_steps(args_cli.hold_s)
    ramp_n = n_steps(args_cli.ramp_up_s)
    cruise_n = n_steps(args_cli.cruise_s)
    decel_n = n_steps(args_cli.decel_window_s)

    phases = [
        ("settle", settle_n, lambda i: 0.0),
        ("zero_hold", hold_n, lambda i: 0.0),
        ("ramp_up", ramp_n, lambda i: args_cli.ramp_vx * (i + 1) / ramp_n),
        ("cruise", cruise_n, lambda i: args_cli.ramp_vx),
        ("decel", decel_n, lambda i: 0.0),
    ]

    obs = env.get_observations()

    cmd_command_term = env.unwrapped.command_manager.get_term("base_velocity")
    cmd_command_term.is_heading_env[:] = False
    cmd_command_term.is_standing_env[:] = False
    cmd_command_term.time_left[:] = 1.0e6

    log = {name: [] for name, _, _ in phases}
    prev_action = None

    with torch.inference_mode():
        for name, count, cmd_fn in phases:
            for i in range(count):
                cmd_term[:, 0] = cmd_fn(i)
                cmd_term[:, 1] = 0.0
                cmd_term[:, 2] = 0.0
                if hasattr(cmd_command_term, "vel_command_b"):
                    cmd_command_term.vel_command_b[:, 0] = cmd_fn(i)
                    cmd_command_term.vel_command_b[:, 1] = 0.0
                    cmd_command_term.vel_command_b[:, 2] = 0.0

                actions = policy(obs)
                obs, _, _, _ = env.step(actions)

                vx_b = robot.data.root_lin_vel_b[:, 0]
                tilt = torch.linalg.norm(robot.data.projected_gravity_b[:, :2], dim=1)
                ang_vel_xy = torch.linalg.norm(robot.data.root_ang_vel_b[:, :2], dim=1)
                pos_x = robot.data.root_pos_w[:, 0]

                joint_dev = (robot.data.joint_pos[:, joint_ids] - default_joint_pos).abs().mean(dim=0)
                last_action = env.unwrapped.action_manager.action.mean(dim=0)
                action_rate = (
                    (env.unwrapped.action_manager.action - prev_action).abs().mean(dim=0)
                    if prev_action is not None else torch.zeros_like(last_action)
                )
                prev_action = env.unwrapped.action_manager.action.clone()

                log[name].append({
                    "vx_b": vx_b.mean().item(),
                    "tilt": tilt.mean().item(),
                    "ang_vel_xy": ang_vel_xy.mean().item(),
                    "pos_x": pos_x.mean().item(),
                    "joint_dev": joint_dev.tolist(),
                    "action": last_action.tolist(),
                    "action_rate": action_rate.tolist(),
                })

    zero_hold = log["zero_hold"]
    cruise = log["cruise"]
    decel = log["decel"]

    mean_vx_hold = sum(r["vx_b"] for r in zero_hold) / len(zero_hold)
    drift_m = sum(r["vx_b"] for r in zero_hold) * step_dt
    peak_tilt_decel = max(r["tilt"] for r in decel)
    peak_ang_vel_decel = max(r["ang_vel_xy"] for r in decel)
    final_tilt_decel = decel[-1]["tilt"]
    final_ang_vel_decel = decel[-1]["ang_vel_xy"]

    print("")
    print("=" * 60)
    print(f"[RESULT] task={args_cli.task}")
    print(f"[RESULT] checkpoint={args_cli.checkpoint}")
    print("-" * 60)
    print(f"zero-command hold ({args_cli.hold_s:.1f}s): drift = {drift_m:+.4f} m "
          f"(negative = backward), mean vx = {mean_vx_hold:+.4f} m/s")
    print(f"decel shake ({args_cli.ramp_vx:.2f} -> 0 over 1 step, {args_cli.decel_window_s:.1f}s window):")
    print(f"  peak tilt (|proj_grav_xy|) = {peak_tilt_decel:.4f}, final = {final_tilt_decel:.4f}")
    print(f"  peak ang_vel_xy (rad/s)    = {peak_ang_vel_decel:.4f}, final = {final_ang_vel_decel:.4f}")

    print("-" * 60)
    print(f"{'joint':<20}{'dev cruise':>12}{'dev decel':>12}{'rate cruise':>13}{'rate decel':>12}{'decel/cruise':>14}")
    for j, jname in enumerate(joint_names):
        dev_cruise = sum(r["joint_dev"][j] for r in cruise) / len(cruise)
        dev_decel = max(r["joint_dev"][j] for r in decel)
        rate_cruise = sum(r["action_rate"][j] for r in cruise) / len(cruise)
        rate_decel = max(r["action_rate"][j] for r in decel)
        ratio = rate_decel / rate_cruise if rate_cruise > 1e-6 else float("inf")
        tag = "  <-- shoulder/thigh" if jname in ("joint_left_leg_2", "joint_right_leg_2") else ""
        print(f"{jname:<20}{dev_cruise:>12.4f}{dev_decel:>12.4f}{rate_cruise:>13.4f}{rate_decel:>12.4f}{ratio:>13.2f}x{tag}")
    print("=" * 60)

    if args_cli.out:
        os.makedirs(os.path.dirname(args_cli.out) or ".", exist_ok=True)
        with open(args_cli.out, "w", newline="") as f:
            writer = csv.writer(f)
            header = ["phase", "step", "vx_b", "tilt", "ang_vel_xy", "pos_x"]
            header += [f"dev_{n}" for n in joint_names]
            header += [f"action_{n}" for n in joint_names]
            header += [f"rate_{n}" for n in joint_names]
            writer.writerow(header)
            for name, _, _ in phases:
                for i, r in enumerate(log[name]):
                    row = [name, i, r["vx_b"], r["tilt"], r["ang_vel_xy"], r["pos_x"]]
                    row += r["joint_dev"] + r["action"] + r["action_rate"]
                    writer.writerow(row)
        print(f"[INFO] time series written to {args_cli.out}")

    env.close()


if __name__ == '__main__':
    main()
    simulation_app.close()
