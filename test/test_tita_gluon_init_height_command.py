#!/usr/bin/env python3
"""Validate the TITA+GLUON init-height command contract.

Execution domain: VALIDATION_SIM. This test never communicates with physical
hardware and does not apply robot commands outside Isaac Sim.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import traceback


REPO_ROOT = Path(__file__).resolve().parents[1]
LAB_ROOT = REPO_ROOT / "lab"
for path in (REPO_ROOT, LAB_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description=__doc__)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import gymnasium as gym  # noqa: E402
import torch  # noqa: E402

import ddt_lab.tasks  # noqa: F401, E402
from ddt_lab.tasks.moo_based.locomotion.velocity.mdp.feature_functions_common import (  # noqa: E402
    error_base_height,
    normalize_height,
)
from ddt_lab.tasks.moo_based.locomotion.velocity.mdp.observations import (  # noqa: E402
    generated_commands_height_normalized,
)


TASK_ID = "Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-RMATeacher-TargetHeight-v0-moo-ppo"


def main() -> int:
    spec = gym.spec(TASK_ID)
    env_cfg = spec.kwargs["env_cfg_entry_point"]()
    env_cfg.scene.num_envs = 4
    env_cfg.observations.stack_policy.enable_corruption = False
    env_cfg.commands.base_velocity.debug_vis = False
    env_cfg.events.push_robot = None
    env_cfg.domain = None

    env = gym.make(TASK_ID, cfg=env_cfg)
    try:
        raw_env = env.unwrapped
        command_term = raw_env.command_manager.get_term("base_velocity")
        sampled_height = torch.full((raw_env.num_envs,), 0.32, device=raw_env.device)
        command_term.vel_command_b[:, :3] = 1.0
        command_term.vel_command_b[:, 3] = sampled_height
        command_term.time_elapsed[:] = torch.tensor(
            [0.0, 5.0, 5.5, 6.0], device=raw_env.device
        )

        command = raw_env.command_manager.get_command("base_velocity")
        expected_height = torch.tensor([0.39, 0.39, 0.355, 0.32], device=raw_env.device)
        expected_velocity = torch.tensor(
            [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]],
            device=raw_env.device,
        )
        torch.testing.assert_close(command[:, 3], expected_height, atol=1.0e-6, rtol=0.0)
        torch.testing.assert_close(command[:, :3], expected_velocity, atol=1.0e-6, rtol=0.0)

        observed_command = generated_commands_height_normalized(raw_env, "base_velocity")
        expected_observed = command.clone()
        expected_observed[:, 3] = normalize_height(expected_observed[:, 3])
        torch.testing.assert_close(observed_command, expected_observed, atol=1.0e-6, rtol=0.0)

        reward_error = error_base_height(
            raw_env,
            command_name="base_velocity",
            scale=1.0,
        )
        robot = raw_env.scene["robot"]
        expected_reward_error = normalize_height(robot.data.root_link_pos_w[:, 2]) - normalize_height(
            command[:, 3]
        )
        torch.testing.assert_close(reward_error, expected_reward_error, atol=1.0e-6, rtol=0.0)

        print(
            "INIT_HEIGHT_COMMAND_TEST,domain=VALIDATION_SIM,status=PASS,"
            "times_s=0.0|5.0|5.5|6.0,heights_m=0.39|0.39|0.355|0.32",
            flush=True,
        )
        return 0
    finally:
        env.close()


if __name__ == "__main__":
    status = 1
    try:
        status = main()
    except Exception:
        traceback.print_exc()
    finally:
        simulation_app.close()
    raise SystemExit(status)
