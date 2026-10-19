#!/usr/bin/env python3
"""Headless contract smoke for the staged TITA+GLUON curriculum pipeline."""

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
parser.add_argument("--fixed-steps", type=int, default=50)
parser.add_argument("--moving-steps", type=int, default=320)
parser.add_argument("--num-envs", type=int, default=4)
parser.add_argument("--dump-traceback-after-s", type=float, default=0.0)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import gymnasium as gym  # noqa: E402
import torch  # noqa: E402
from isaaclab.utils.math import quat_apply  # noqa: E402

import ddt_lab.tasks  # noqa: F401, E402
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.env_cfg import (  # noqa: E402
    GLUON_CURRICULUM_END_STEP,
    GLUON_CURRICULUM_START_STEP,
    GLUON_JOINT_NAMES,
    GLUON_WORK_JOINT_POS,
    TitaGluonCurriculumArmFlatEnvCfg_PLAY,
)
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.mdp.actions import (  # noqa: E402
    SmoothRandomJointPositionAction,
)


TASK_ID = (
    "Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-"
    "RMATeacher-TargetHeight-v0-moo-ppo"
)


def advance_without_reward(unwrapped, action, trajectory, steps: int) -> torch.Tensor:
    """Advance only action/scene/sim managers, bypassing runner-owned MOO reward state."""
    command_samples = []
    for _ in range(steps):
        unwrapped.action_manager.process_action(action)
        for _ in range(unwrapped.cfg.decimation):
            unwrapped.action_manager.apply_action()
            command_samples.append(trajectory.processed_actions.clone())
            unwrapped.scene.write_data_to_sim()
            unwrapped.sim.step(render=False)
            unwrapped.scene.update(dt=unwrapped.physics_dt)
    return torch.stack(command_samples)


def main() -> int:
    if args_cli.fixed_steps <= 0 or args_cli.moving_steps <= 0 or args_cli.num_envs <= 0:
        raise ValueError("step counts and --num-envs must be positive")
    if args_cli.dump_traceback_after_s < 0.0:
        raise ValueError("--dump-traceback-after-s must be non-negative")
    if args_cli.dump_traceback_after_s > 0.0:
        faulthandler.dump_traceback_later(args_cli.dump_traceback_after_s, repeat=True)

    spec = gym.spec(TASK_ID)
    play_cfg = TitaGluonCurriculumArmFlatEnvCfg_PLAY()
    if play_cfg.scene.num_envs != 16:
        raise AssertionError(f"Play visualization must use 16 environments: {play_cfg.scene.num_envs}")
    if not play_cfg.actions.gluon_joint_reference.debug_vis:
        raise AssertionError("Play visualization did not enable the per-robot EE goal marker")
    runner_cfg = spec.kwargs["co_rl_cfg_entry_point"]()
    if runner_cfg.policy.class_name != "RMATeacher":
        raise AssertionError(f"Unexpected policy class: {runner_cfg.policy.class_name}")
    if not runner_cfg.use_rma_teacher or runner_cfg.num_policy_stacks != 1:
        raise AssertionError("RMA Teacher flags do not match the validated parent")
    if runner_cfg.max_iterations != 10_000:
        raise AssertionError(f"Unexpected training horizon: {runner_cfg.max_iterations}")
    if runner_cfg.logger != "wandb" or runner_cfg.wandb_project != "tita-gluon-moo-teacher":
        raise AssertionError(
            "Future curriculum-arm training must default to the tita-gluon-moo-teacher W&B project"
        )
    if not runner_cfg.run_name.startswith("phase"):
        raise AssertionError(f"W&B run name must identify the phase: {runner_cfg.run_name}")

    cfg = spec.kwargs["env_cfg_entry_point"]()
    cfg.seed = 20260809
    cfg.scene.num_envs = args_cli.num_envs
    cfg.observations.stack_policy.enable_corruption = False
    cfg.events.push_robot = None
    cfg.domain = None
    env = gym.make(TASK_ID, cfg=cfg)
    unwrapped = env.unwrapped

    try:
        env.reset()
        robot = unwrapped.scene["robot"]
        joint_ids, joint_names = robot.find_joints(list(GLUON_JOINT_NAMES), preserve_order=True)
        if tuple(joint_names) != GLUON_JOINT_NAMES:
            raise AssertionError(f"Unexpected GLUON joint order: {joint_names}")
        if unwrapped.action_manager.total_action_dim != 8:
            raise AssertionError(
                f"TITA policy action dimension changed: {unwrapped.action_manager.total_action_dim}"
            )
        trajectory = unwrapped.action_manager.get_term("gluon_joint_reference")
        if not isinstance(trajectory, SmoothRandomJointPositionAction):
            raise AssertionError(f"Unexpected action term: {type(trajectory).__name__}")
        goal_pos_b = trajectory.segment_goal_ee_pos_b
        if goal_pos_b.shape != (args_cli.num_envs, 3) or not bool(torch.isfinite(goal_pos_b).all()):
            raise AssertionError(f"Invalid per-environment EE segment goals: {goal_pos_b}")
        ee_body_ids, _ = robot.find_bodies(["gluon_2L6_4L3_link6"], preserve_order=True)
        goal_pos_w = robot.data.root_link_pos_w + quat_apply(robot.data.root_link_quat_w, goal_pos_b)
        fk_error_m = float(
            torch.linalg.vector_norm(
                goal_pos_w - robot.data.body_link_pos_w[:, ee_body_ids[0]], dim=1
            ).max().item()
        )
        if fk_error_m > 1.0e-4:
            raise AssertionError(f"URDF link6 FK disagrees with simulator by {fk_error_m} m")

        stand_action = torch.tensor(
            [[0.0, 0.0, 0.8, 0.8, -1.5, -1.5, 0.0, 0.0]],
            device=unwrapped.device,
        ).repeat(args_cli.num_envs, 1)

        unwrapped.common_step_counter = 0
        unwrapped.curriculum_manager.compute()
        if trajectory.workspace_scale != 0.0:
            raise AssertionError(f"Curriculum did not start fixed: {trajectory.workspace_scale}")
        fixed_commands = advance_without_reward(
            unwrapped, stand_action, trajectory, args_cli.fixed_steps
        )
        fixed_span = float((fixed_commands.amax(dim=0) - fixed_commands.amin(dim=0)).max().item())
        fixed_error = float(
            torch.abs(fixed_commands - fixed_commands.new_tensor(GLUON_WORK_JOINT_POS)).max().item()
        )
        if fixed_span > 1.0e-7 or fixed_error > 1.0e-7:
            raise AssertionError(
                f"Initial fixed-arm stage moved: span={fixed_span}, error={fixed_error}"
            )

        unwrapped.common_step_counter = (
            GLUON_CURRICULUM_START_STEP + GLUON_CURRICULUM_END_STEP
        ) // 2
        unwrapped.curriculum_manager.compute()
        if abs(trajectory.workspace_scale - 0.5) > 1.0e-7:
            raise AssertionError(f"Curriculum midpoint is not linear: {trajectory.workspace_scale}")

        unwrapped.common_step_counter = GLUON_CURRICULUM_END_STEP
        unwrapped.curriculum_manager.compute()
        if abs(trajectory.workspace_scale - 1.0) > 1.0e-7:
            raise AssertionError(f"Curriculum did not reach full range: {trajectory.workspace_scale}")
        height_range = unwrapped.command_manager.get_term("base_velocity").cfg.ranges.pos_z
        if tuple(height_range) != (0.25, 0.45):
            raise AssertionError(f"Parent height curriculum mismatch: {height_range}")

        moving_commands = advance_without_reward(
            unwrapped, stand_action, trajectory, args_cli.moving_steps
        )
        command_span_per_env = (
            moving_commands.amax(dim=0) - moving_commands.amin(dim=0)
        ).amax(dim=1)
        if float(command_span_per_env.min().item()) < 0.05:
            raise AssertionError(f"At least one expanded arm did not move: {command_span_per_env}")
        measured = robot.data.joint_pos[:, joint_ids]
        if not bool(torch.isfinite(measured).all()):
            raise AssertionError("Non-finite GLUON state")

        print(
            "TITA_GLUON_CURRICULUM_ARM_SMOKE,domain=VALIDATION_SIM,status=PASS,"
            f"envs={args_cli.num_envs},actions=8,policy={runner_cfg.policy.class_name},"
            f"policy_stacks={runner_cfg.num_policy_stacks},max_iterations={runner_cfg.max_iterations},"
            f"fixed_span_rad={fixed_span:.9g},mid_scale=0.5,"
            f"full_scale={trajectory.workspace_scale:.9g},"
            f"min_command_span_rad={float(command_span_per_env.min().item()):.9g},"
            f"initial_link6_fk_error_m={fk_error_m:.9g},"
            f"height_range={height_range}",
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
