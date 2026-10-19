#!/usr/bin/env python3
"""Headless contract smoke for the combined TITA+GLUON MOO environment."""

import argparse
import faulthandler
import sys
import traceback
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LAB_ROOT = REPO_ROOT / "lab"
if str(LAB_ROOT) not in sys.path:
    sys.path.insert(0, str(LAB_ROOT))

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--steps", type=int, default=25)
parser.add_argument(
    "--dump-traceback-after-s",
    type=float,
    default=0.0,
    help="Dump Python stacks after this delay; zero disables the debug watchdog.",
)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import gymnasium as gym  # noqa: E402
import torch  # noqa: E402

import ddt_lab.tasks  # noqa: F401, E402
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.env_cfg import (  # noqa: E402
    GLUON_JOINT_NAMES,
    GLUON_WORK_JOINT_POS,
    TITA_GLUON_STACK_POLICY_TERMS,
)


TASK_ID = "Isaac-Velocity-Flat-Tita-Gluon-Play-v0-moo-ppo"


def main() -> int:
    if args_cli.steps <= 0:
        raise ValueError("--steps must be positive")
    if args_cli.dump_traceback_after_s < 0.0:
        raise ValueError("--dump-traceback-after-s must be non-negative")
    if args_cli.dump_traceback_after_s > 0.0:
        faulthandler.dump_traceback_later(args_cli.dump_traceback_after_s, repeat=True)

    cfg = gym.spec(TASK_ID).kwargs["env_cfg_entry_point"]()
    cfg.scene.num_envs = 1
    env = gym.make(TASK_ID, cfg=cfg)
    unwrapped = env.unwrapped

    try:
        obs, _ = env.reset()
        robot = unwrapped.scene["robot"]
        joint_ids, joint_names = robot.find_joints(list(GLUON_JOINT_NAMES), preserve_order=True)
        if tuple(joint_names) != GLUON_JOINT_NAMES:
            raise AssertionError(f"Unexpected GLUON joint order: {joint_names}")
        if unwrapped.action_manager.total_action_dim != 8:
            raise AssertionError(
                f"TITA policy action dimension changed: {unwrapped.action_manager.total_action_dim}"
            )

        stack_terms = tuple(unwrapped.observation_manager.active_terms["stack_policy"])
        if stack_terms != TITA_GLUON_STACK_POLICY_TERMS:
            raise AssertionError(f"Unexpected stack_policy order: {stack_terms}")
        if set(obs) != {
            "stack_policy",
            "none_stack_policy",
            "priv_extrio",
            "priv_prio",
            "priv_physical",
        }:
            raise AssertionError(f"Unexpected CO-RL observation groups: {sorted(obs)}")

        # Action order is inherited unchanged: hip(2), shoulder/leg(4), wheels(2).
        stand_action = torch.tensor(
            [[0.0, 0.0, 0.8, 0.8, -1.5, -1.5, 0.0, 0.0]], device=unwrapped.device
        )
        for _ in range(args_cli.steps):
            # The raw MOO environment's reward path is activated only after
            # the CO-RL runner injects its discriminator/normalizer.  This
            # asset/action smoke intentionally validates the lower execution
            # boundary without fabricating those training components.
            unwrapped.action_manager.process_action(stand_action)
            for _ in range(unwrapped.cfg.decimation):
                unwrapped.action_manager.apply_action()
                unwrapped.scene.write_data_to_sim()
                unwrapped.sim.step(render=False)
                unwrapped.scene.update(dt=unwrapped.physics_dt)
        obs = unwrapped.observation_manager.compute(update_history=True)

        target = torch.tensor(GLUON_WORK_JOINT_POS, device=unwrapped.device)
        arm_error = (robot.data.joint_pos[0, joint_ids] - target).abs()
        if not torch.isfinite(arm_error).all():
            raise AssertionError(f"Non-finite GLUON state: {arm_error}")
        max_arm_error = float(arm_error.max().item())
        if max_arm_error > 0.08:
            raise AssertionError(f"GLUON WORK hold error too large: {max_arm_error:.6f} rad")

        print(
            "TITA_GLUON_MOO_SMOKE,domain=VALIDATION_SIM,status=PASS,"
            f"steps={args_cli.steps},joints={robot.num_joints},actions=8,"
            "group_dims="
            + ";".join(f"{name}:{value.shape[-1]}" for name, value in obs.items())
            + ","
            f"max_arm_error_rad={max_arm_error:.9g},"
            f"stack_order={','.join(stack_terms)}",
            flush=True,
        )
        return 0
    finally:
        faulthandler.cancel_dump_traceback_later()
        env.close()


if __name__ == "__main__":
    try:
        exit_status = main()
    except Exception:
        traceback.print_exc()
        raise
    finally:
        simulation_app.close()
    raise SystemExit(exit_status)
