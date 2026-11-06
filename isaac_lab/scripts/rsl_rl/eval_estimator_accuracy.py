# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Isaac-Lab-side accuracy check for `My26`'s learned ``base_lin_vel``
estimator MLP (``ActorCriticWithEstimator``) against ground truth.

Runs the same scripted settle/zero-hold/ramp-up/cruise/decel command profile
as ``eval_behavior.py``, reading the estimator's raw prediction
(``policy._last_estimator_output``, populated by ``get_actor_obs`` every
``act_inference`` call) alongside ``robot.data.root_lin_vel_b`` (ground
truth), and reports per-phase RMSE in m/s -- comparable to the naive
kinematic wheel-vel estimator's documented ~0.10 m/s (near-standstill) /
~0.32 m/s (active gait) numbers (see ``Experiments/RL_Experiments.md``, My18).

Example:
    python scripts/rsl_rl/eval_estimator_accuracy.py \\
        --task=DDT-Velocity-Flat-Tita-My26-Play-v0 \\
        --checkpoint logs/rsl_rl/tita_flat_rslrl_estimator/2026-07-21_22-40-17/model_1999.pt \\
        --headless
"""

import argparse
import importlib

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description='base_lin_vel estimator accuracy probe (Isaac Lab, My26).')
parser.add_argument('--task', type=str, required=True, help='Gym task ID (use a *-Play-v0 variant).')
parser.add_argument('--checkpoint', type=str, required=True, help='Absolute checkpoint path.')
parser.add_argument('--num_envs', type=int, default=64, help='Number of envs (averaged in the summary).')
parser.add_argument('--settle_s', type=float, default=1.0, help='Time to let the robot settle after reset, cmd=0.')
parser.add_argument('--hold_s', type=float, default=3.0, help='Zero-command hold duration.')
parser.add_argument('--ramp_vx', type=float, default=0.8, help='Target forward vx to ramp up to.')
parser.add_argument('--ramp_up_s', type=float, default=1.0, help='Ramp-up duration from 0 to --ramp_vx.')
parser.add_argument('--cruise_s', type=float, default=3.0, help='Hold duration at --ramp_vx.')
parser.add_argument('--decel_s', type=float, default=2.0, help='Window after cutting back to zero.')
AppLauncher.add_app_launcher_args(parser)
args_cli, _ = parser.parse_known_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import ddt_lab.tasks  # noqa: F401  -- registers tasks
import gymnasium as gym
import torch

from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper
from rsl_rl.runners import OnPolicyRunner

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
    policy_nn = runner.alg.policy
    if not hasattr(policy_nn, 'estimator'):
        raise ValueError(
            f"Checkpoint's policy has no 'estimator' attribute -- not an ActorCriticWithEstimator "
            f"checkpoint (My26-style). Got: {type(policy_nn)}"
        )
    policy = runner.get_inference_policy(device=agent_cfg.device)

    step_dt = float(env.unwrapped.step_dt)
    robot = env.unwrapped.scene["robot"]
    cmd_term = env.unwrapped.command_manager.get_command("base_velocity")

    def n_steps(seconds: float) -> int:
        return max(1, round(seconds / step_dt))

    settle_n = n_steps(args_cli.settle_s)
    hold_n = n_steps(args_cli.hold_s)
    ramp_n = n_steps(args_cli.ramp_up_s)
    cruise_n = n_steps(args_cli.cruise_s)
    decel_n = n_steps(args_cli.decel_s)

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

    # scale=2.0 applied to the estimator_target ObsTerm (mdp.base_lin_vel) --
    # the estimator's raw output lives in that scaled space, un-scale here to
    # compare directly against robot.data.root_lin_vel_b (real m/s).
    est_scale = 2.0

    errors = {name: [] for name, _, _ in phases}

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
                est_pred = policy_nn._last_estimator_output.clone() / est_scale  # (B, 3), m/s
                true_vel = robot.data.root_lin_vel_b.clone()  # (B, 3), m/s

                err = (est_pred - true_vel)
                errors[name].append(err)

                obs, _, _, _ = env.step(actions)

    print("")
    print("=" * 70)
    print(f"[RESULT] task={args_cli.task}")
    print(f"[RESULT] checkpoint={args_cli.checkpoint}")
    print("-" * 70)
    print(f"{'phase':<12}{'rmse_x':>10}{'rmse_y':>10}{'rmse_z':>10}{'rmse_|xyz|':>12}{'n_steps':>10}")
    for name, _, _ in phases:
        err = torch.cat(errors[name], dim=0)  # (steps*B, 3)
        rmse_xyz = torch.sqrt((err ** 2).mean(dim=0))
        rmse_norm = torch.sqrt((err ** 2).sum(dim=1)).mean()
        print(
            f"{name:<12}{rmse_xyz[0].item():>10.4f}{rmse_xyz[1].item():>10.4f}"
            f"{rmse_xyz[2].item():>10.4f}{rmse_norm.item():>12.4f}{len(errors[name]):>10}"
        )
    print("-" * 70)
    all_err = torch.cat([torch.cat(errors[n], dim=0) for n, _, _ in phases], dim=0)
    overall_rmse_x = torch.sqrt((all_err[:, 0] ** 2).mean())
    print(f"overall rmse_x (all phases combined): {overall_rmse_x.item():.4f} m/s")
    print("Naive wheel-vel estimator reference (My18, Experiments/RL_Experiments.md):")
    print("  RMSE ~0.10 m/s near-standstill, ~0.32 m/s during active gait")
    print("=" * 70)

    env.close()


if __name__ == '__main__':
    main()
    simulation_app.close()
