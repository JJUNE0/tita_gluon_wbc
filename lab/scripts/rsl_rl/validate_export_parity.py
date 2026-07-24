# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# SPDX-License-Identifier: BSD-3-Clause

"""Compare a My26 native RSL-RL checkpoint with its exported ONNX graph.

The input samples are captured from an actual Isaac Lab rollout.  The script
stores those samples and both outputs so the P2 result is independently
auditable instead of relying on zero/random-input smoke tests.
"""

import argparse
import importlib
import os
import subprocess
import sys

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="PyTorch-vs-ONNX export parity on Isaac Lab samples.")
parser.add_argument("--task", required=True)
parser.add_argument("--checkpoint", required=True)
parser.add_argument("--onnx", required=True)
parser.add_argument("--num_envs", type=int, default=8)
parser.add_argument("--steps", type=int, default=8)
parser.add_argument("--out_dir", required=True)
parser.add_argument(
    "--onnx_python",
    default=sys.executable,
    help="Python interpreter containing numpy and onnxruntime.",
)
AppLauncher.add_app_launcher_args(parser)
args_cli, _ = parser.parse_known_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import ddt_lab.tasks  # noqa: F401
import gymnasium as gym
import numpy as np
import torch

from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper
from rsl_rl.runners import OnPolicyRunner

import rsl_rl.runners.on_policy_runner as _opr
from ddt_lab.algorithms.estimator import ActorCriticWithEstimator, PPOWithEstimator

_opr.ActorCriticWithEstimator = ActorCriticWithEstimator
_opr.PPOWithEstimator = PPOWithEstimator


def _resolve_agent_cfg(entry_point: str):
    module_name, attr = entry_point.split(":")
    obj = getattr(importlib.import_module(module_name), attr)
    return obj() if callable(obj) else obj


def main() -> None:
    spec = gym.spec(args_cli.task)
    agent_cfg = _resolve_agent_cfg(spec.kwargs["rsl_rl_cfg_entry_point"])
    env_cfg_entry = spec.kwargs["env_cfg_entry_point"]
    env_cfg = env_cfg_entry() if callable(env_cfg_entry) else env_cfg_entry
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device

    env = gym.make(args_cli.task, cfg=env_cfg)
    env = RslRlVecEnvWrapper(env, clip_actions=agent_cfg.clip_actions)
    runner = OnPolicyRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    runner.load(args_cli.checkpoint, load_optimizer=False)
    policy_nn = runner.alg.policy
    if not isinstance(policy_nn, ActorCriticWithEstimator):
        raise TypeError(f"expected ActorCriticWithEstimator, got {type(policy_nn).__name__}")
    policy = runner.get_inference_policy(device=agent_cfg.device)

    obs = env.get_observations()
    captured_obs = []
    native_outputs = []

    with torch.inference_mode():
        for _ in range(args_cli.steps):
            proprio = policy_nn._get_proprio_obs(obs).detach().cpu().numpy().astype(np.float32)
            native = policy(obs).detach().cpu().numpy().astype(np.float32)
            for sample, native_sample in zip(proprio, native):
                captured_obs.append(sample.reshape(33).copy())
                native_outputs.append(native_sample.copy())
            obs, _, _, _ = env.step(torch.as_tensor(native, device=agent_cfg.device))

    captured_obs = np.asarray(captured_obs, dtype=np.float32)
    native_outputs = np.asarray(native_outputs, dtype=np.float32)
    if not all(np.isfinite(array).all() for array in (captured_obs, native_outputs)):
        raise ValueError("non-finite parity input or native output")

    os.makedirs(args_cli.out_dir, exist_ok=True)
    native_path = os.path.join(args_cli.out_dir, "native_samples.npz")
    np.savez_compressed(
        native_path,
        nn_input0=captured_obs,
        pytorch_output=native_outputs,
    )
    env.close()
    helper = os.path.join(os.path.dirname(__file__), "compare_export_samples.py")
    subprocess.run(
        [
            args_cli.onnx_python,
            helper,
            "--samples", native_path,
            "--checkpoint", args_cli.checkpoint,
            "--onnx", args_cli.onnx,
            "--task", args_cli.task,
            "--out_dir", args_cli.out_dir,
        ],
        check=True,
    )


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close()
