#!/usr/bin/env python3
"""Construct the registered GLUON reach environment and take finite zero-action steps."""

import argparse

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description=__doc__)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import gymnasium as gym  # noqa: E402
import torch  # noqa: E402

import ddt_lab  # noqa: F401, E402
from isaaclab_tasks.utils import parse_env_cfg  # noqa: E402


TASK_ID = "DDT-Reach-Gluon-2L6-4L3-Play-v0"


def main() -> None:
    env_cfg = parse_env_cfg(TASK_ID, device=args_cli.device, num_envs=4)
    env_cfg.commands.ee_pose.debug_vis = False
    env = gym.make(TASK_ID, cfg=env_cfg)
    try:
        observation, _ = env.reset()
        action = torch.zeros(env.unwrapped.num_envs, env.unwrapped.action_manager.total_action_dim, device=env.unwrapped.device)
        for _ in range(8):
            observation, reward, terminated, truncated, _ = env.step(action)

        policy_obs = observation["policy"]
        failures: list[str] = []
        if tuple(action.shape) != (4, 6):
            failures.append(f"action shape is {tuple(action.shape)}, expected (4, 6)")
        if policy_obs.shape[0] != 4:
            failures.append(f"policy batch is {tuple(policy_obs.shape)}, expected first dimension 4")
        tensors = (policy_obs, reward, terminated, truncated)
        if not all(torch.isfinite(value.float()).all().item() for value in tensors):
            failures.append("non-finite observation/reward/done tensor")

        robot = env.unwrapped.scene["robot"]
        if robot.joint_names != [f"axis_joint_{index}" for index in range(1, 7)]:
            failures.append(f"unexpected joint order: {robot.joint_names}")
        if "link6" not in robot.body_names:
            failures.append("link6 body is absent")

        print(f"task_id={TASK_ID}", flush=True)
        print(f"num_envs={env.unwrapped.num_envs}", flush=True)
        print(f"policy_observation_shape={tuple(policy_obs.shape)}", flush=True)
        print(f"action_shape={tuple(action.shape)}", flush=True)
        print(f"joint_names={robot.joint_names}", flush=True)
        print(f"reward_mean={float(reward.mean().item()):.9g}", flush=True)
        if failures:
            print("GLUON_REACH_ENV_SMOKE: FAIL", flush=True)
            for failure in failures:
                print(f"- {failure}", flush=True)
            raise SystemExit(1)
        print("GLUON_REACH_ENV_SMOKE: PASS", flush=True)
    finally:
        env.close()


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close(skip_cleanup=True)
