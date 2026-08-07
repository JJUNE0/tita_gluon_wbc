"""Bounded headless runtime smoke for the imported CO-RL TITA MOO task."""

from __future__ import annotations

import argparse
import traceback

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--task",
    default="Isaac-Velocity-Flat-Tita-GTBaseVel-TargetHeight-v3-moo-ppo",
)
parser.add_argument("--num-envs", type=int, default=1)
parser.add_argument("--steps", type=int, default=4)
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()

app = AppLauncher(args).app

import gymnasium as gym
import torch

import ddt_lab.tasks  # noqa: F401, E402
from ddt_lab.envs import ManagerBasedMOORLEnv  # noqa: E402
from ddt_lab.tasks.moo_based.locomotion.velocity.tita_env.agents.co_rl_cfg import (  # noqa: E402
    TitaMOOPPORunnerCfg_Flat_Stand_Drive,
)
from isaaclab_tasks.utils import parse_env_cfg  # noqa: E402
from scripts.co_rl.core.runners import MOO_OnPolicyRunner  # noqa: E402
from scripts.co_rl.core.wrapper import CoRlVecEnvWrapper  # noqa: E402


def _assert_finite(value, path: str) -> None:
    if isinstance(value, torch.Tensor):
        if not bool(torch.isfinite(value).all()):
            raise RuntimeError(f"non-finite tensor at {path}")
    elif isinstance(value, dict):
        for key, item in value.items():
            _assert_finite(item, f"{path}.{key}")


def main() -> None:
    if args.num_envs <= 0 or args.steps <= 0:
        raise ValueError("--num-envs and --steps must be positive")

    gym_env = None
    env = None
    try:
        env_cfg = parse_env_cfg(
            args.task,
            device=args.device,
            num_envs=args.num_envs,
            use_fabric=True,
        )
        print("smoke_stage=config_parsed", flush=True)
        gym_env = gym.make(args.task, cfg=env_cfg)
        print("smoke_stage=environment_created", flush=True)
        raw_env = gym_env.unwrapped
        if not isinstance(raw_env, ManagerBasedMOORLEnv):
            raise RuntimeError(f"unexpected environment type: {type(raw_env)}")

        agent_cfg = TitaMOOPPORunnerCfg_Flat_Stand_Drive()
        env = CoRlVecEnvWrapper(gym_env, agent_cfg)
        MOO_OnPolicyRunner(env, agent_cfg.to_dict(), log_dir=None, device=env.device)
        print("smoke_stage=moo_runner_initialized", flush=True)

        observations, extras = env.reset()
        print("smoke_stage=environment_reset", flush=True)
        _assert_finite(observations, "reset_observations")
        _assert_finite(extras, "reset_extras")

        action_dim = raw_env.action_manager.total_action_dim
        if action_dim != 8:
            raise RuntimeError(f"expected 8 actions, got {action_dim}")
        actions = torch.zeros((raw_env.num_envs, action_dim), device=raw_env.device)

        last_reward = None
        for _ in range(args.steps):
            observations, reward, dones, extras = env.step(actions)
            _assert_finite(observations, "step_observations")
            _assert_finite(reward, "reward")
            _assert_finite(extras, "step_extras")
            if dones.shape != (raw_env.num_envs,):
                raise RuntimeError(f"unexpected dones shape: {dones.shape}")
            if extras["delta"].shape != (raw_env.num_envs, raw_env.moo_reward_manager.delta_dim):
                raise RuntimeError(f"unexpected delta shape: {extras['delta'].shape}")
            last_reward = reward

        group_dims = raw_env.observation_manager.group_obs_dim
        required_groups = {"stack_policy", "none_stack_policy"}
        missing_groups = required_groups.difference(group_dims)
        if missing_groups:
            raise RuntimeError(f"missing observation groups: {sorted(missing_groups)}")
        if getattr(raw_env, "moo_reward_manager", None) is None:
            raise RuntimeError("MOO reward manager was not constructed")
        if getattr(raw_env, "domain_manager", None) is None:
            raise RuntimeError("domain manager was not constructed")

        print(
            "CO_RL_TITA_HEADLESS_SMOKE: PASS,"
            f"task={args.task},num_envs={raw_env.num_envs},steps={args.steps},"
            f"action_dim={action_dim},reward_shape={tuple(last_reward.shape)},"
            f"groups={sorted(group_dims)}",
            flush=True,
        )
    finally:
        if env is not None:
            env.close()
        elif gym_env is not None:
            gym_env.close()


if __name__ == "__main__":
    try:
        main()
    except BaseException:
        print("CO_RL_TITA_HEADLESS_SMOKE: FAIL", flush=True)
        traceback.print_exc()
        raise
    finally:
        app.close()
