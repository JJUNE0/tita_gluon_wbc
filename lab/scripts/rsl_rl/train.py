# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Train an Isaac Lab task with plain RSL-RL PPO.

Mirrors ``scripts/np3o/train.py``'s CLI surface/structure, but resolves the
``rsl_rl_cfg_entry_point`` (a configclass, not a dict-returning function) and
uses the official ``isaaclab_rl.rsl_rl`` wrapper + ``rsl_rl.runners.OnPolicyRunner``
instead of NP3O's custom wrapper/runner. See
``Experiments/RL_Experiments.md`` (`My7-RSL`) for why this track exists.
"""

import argparse
import importlib

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description='Train an Isaac Lab task with plain RSL-RL PPO.')
parser.add_argument('--num_envs', type=int, default=None, help='Number of parallel envs.')
parser.add_argument('--task', type=str, required=True, help='Gym task ID, e.g. DDT-Velocity-Flat-Tita-My7-RSL-v0.')
parser.add_argument('--seed', type=int, default=None, help='Environment/agent seed override.')
parser.add_argument('--max_iterations', type=int, default=None, help='Override iterations.')
parser.add_argument('--resume', action='store_true', help='Resume from latest checkpoint.')
parser.add_argument('--load_run', type=str, default=None, help='Run dir regex when resuming.')
parser.add_argument('--load_checkpoint', type=str, default=None, help='Checkpoint regex.')
parser.add_argument('--experiment_name', type=str, default=None, help='Override experiment name.')
AppLauncher.add_app_launcher_args(parser)
args_cli, _ = parser.parse_known_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import os
from datetime import datetime

import ddt_lab.tasks  # noqa: F401  -- registers tasks
import gymnasium as gym
import torch
from isaaclab.utils.io import dump_yaml
from isaaclab_tasks.utils import get_checkpoint_path

from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper
from rsl_rl.runners import OnPolicyRunner

# Inject the learned base_lin_vel estimator classes into on_policy_runner's
# eval() namespace so EstimatorActorCriticCfg/EstimatorPPOCfg's class_name
# strings resolve, with zero changes to the installed rsl_rl package. See
# docs/plan_base_vel_estimator_ppo.md.
import rsl_rl.runners.on_policy_runner as _opr
from ddt_lab.algorithms.estimator import ActorCriticWithEstimator, PPOWithEstimator

_opr.ActorCriticWithEstimator = ActorCriticWithEstimator
_opr.PPOWithEstimator = PPOWithEstimator

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True


def _resolve_agent_cfg(entry_point: str):
    module_name, attr = entry_point.split(':')
    obj = getattr(importlib.import_module(module_name), attr)
    return obj() if callable(obj) else obj


def main():
    spec = gym.spec(args_cli.task)
    rsl_rl_entry = spec.kwargs.get('rsl_rl_cfg_entry_point')
    if rsl_rl_entry is None:
        raise KeyError(
            f"Task '{args_cli.task}' has no 'rsl_rl_cfg_entry_point'. "
            'Register one alongside env_cfg_entry_point.'
        )
    agent_cfg = _resolve_agent_cfg(rsl_rl_entry)

    env_cfg_entry = spec.kwargs['env_cfg_entry_point']
    env_cfg = env_cfg_entry() if callable(env_cfg_entry) else env_cfg_entry

    if args_cli.num_envs is not None:
        env_cfg.scene.num_envs = args_cli.num_envs
    if args_cli.seed is not None:
        agent_cfg.seed = args_cli.seed
    env_cfg.seed = agent_cfg.seed
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device
    if args_cli.max_iterations is not None:
        agent_cfg.max_iterations = args_cli.max_iterations
    if args_cli.resume:
        agent_cfg.resume = True
    if args_cli.load_run is not None:
        agent_cfg.load_run = args_cli.load_run
    if args_cli.load_checkpoint is not None:
        agent_cfg.load_checkpoint = args_cli.load_checkpoint
    if args_cli.experiment_name is not None:
        agent_cfg.experiment_name = args_cli.experiment_name

    log_root = os.path.abspath(os.path.join('logs', 'rsl_rl', agent_cfg.experiment_name))
    log_dir = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    if agent_cfg.run_name:
        log_dir += f"_{agent_cfg.run_name}"
    log_dir = os.path.join(log_root, log_dir)
    env_cfg.log_dir = log_dir
    print(f'[INFO] Logging experiment in directory: {log_dir}')

    env = gym.make(args_cli.task, cfg=env_cfg, render_mode=None)
    env = RslRlVecEnvWrapper(env, clip_actions=agent_cfg.clip_actions)

    if agent_cfg.resume:
        resume_path = get_checkpoint_path(log_root, agent_cfg.load_run, agent_cfg.load_checkpoint)

    runner = OnPolicyRunner(env, agent_cfg.to_dict(), log_dir=log_dir, device=agent_cfg.device)
    runner.add_git_repo_to_log(__file__)

    if agent_cfg.resume:
        print(f'[INFO] Loading checkpoint: {resume_path}')
        runner.load(resume_path)

    dump_yaml(os.path.join(log_dir, 'params', 'env.yaml'), env_cfg)
    dump_yaml(os.path.join(log_dir, 'params', 'agent.yaml'), agent_cfg)

    runner.learn(num_learning_iterations=agent_cfg.max_iterations, init_at_random_ep_len=True)
    env.close()


if __name__ == '__main__':
    main()
    simulation_app.close()
