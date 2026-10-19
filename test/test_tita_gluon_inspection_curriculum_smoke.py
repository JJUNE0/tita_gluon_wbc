#!/usr/bin/env python3
"""Headless smoke for clean from-scratch inspection-hub training.

Execution domain: VALIDATION_SIM.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
LAB_ROOT = REPO_ROOT / "lab"
if str(LAB_ROOT) not in sys.path:
    sys.path.insert(0, str(LAB_ROOT))

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--num-envs", type=int, default=2)
parser.add_argument("--physics-steps", type=int, default=600)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import gymnasium as gym  # noqa: E402
import torch  # noqa: E402

import ddt_lab.tasks  # noqa: F401, E402
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.env_cfg import (  # noqa: E402
    GLUON_INSPECTION_CURRICULUM_END_STEP,
    GLUON_INSPECTION_CURRICULUM_START_STEP,
    GLUON_INSPECTION_GRAPH_NODE_IDS,
    GLUON_INSPECTION_HUBS_RAD,
)
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.agents import (  # noqa: E402
    TitaGluonSequentialInspectionHighLevelRunnerCfg,
)
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.mdp.actions import (  # noqa: E402
    SmoothRandomJointPositionAction,
)


TASK_ID = (
    "Isaac-Velocity-Flat-Tita-Gluon-InspectionCurriculumArm-"
    "RMATeacher-v0-moo-ppo"
)


def main() -> int:
    if args_cli.num_envs <= 0 or args_cli.physics_steps <= 0:
        raise ValueError("--num-envs and --physics-steps must be positive")
    spec = gym.spec(TASK_ID)
    runner_cfg = spec.kwargs["co_rl_cfg_entry_point"]()
    if runner_cfg.max_iterations != 10_000:
        raise AssertionError("from-scratch teacher must run for 10,000 iterations")
    if runner_cfg.resume:
        raise AssertionError("from-scratch teacher must not resume a checkpoint")
    if runner_cfg.enable_teacher_tsne:
        raise AssertionError("headless teacher training must keep t-SNE disabled")
    if runner_cfg.add_cfg.w_disc != 0.5 or runner_cfg.add_cfg.w_fm != 0.5:
        raise AssertionError("inspection teacher ADD reward mixture must be 0.5/0.5")
    if runner_cfg.experiment_name != (
        "Tita_Gluon_InspectionCurriculumArm_RMATeacher-v0-mooppo"
    ):
        raise AssertionError("inspection curriculum needs an independent experiment namespace")
    if runner_cfg.run_name != "phase1-work-phase2-inspection-hubs":
        raise AssertionError("inspection curriculum run name changed")
    high_level_cfg = TitaGluonSequentialInspectionHighLevelRunnerCfg()
    if high_level_cfg.policy.class_name != "HybridActorCritic":
        raise AssertionError("high-level policy is not hybrid")
    if high_level_cfg.policy.action_mask_obs_start != 41:
        raise AssertionError("high-level option-mask observation offset changed")
    if high_level_cfg.algorithm.schedule != "fixed":
        raise AssertionError("hybrid PPO must use the fixed learning-rate schedule")

    cfg = spec.kwargs["env_cfg_entry_point"]()
    if cfg.domain.w_gail != 0.5 or cfg.domain.w_fm != 0.5:
        raise AssertionError("domain curriculum score mixture must be 0.5/0.5")
    cfg.seed = 20260810
    cfg.scene.num_envs = args_cli.num_envs
    cfg.observations.stack_policy.enable_corruption = False
    cfg.events.push_robot = None
    cfg.domain = None
    env = gym.make(TASK_ID, cfg=cfg)
    raw_env = env.unwrapped
    try:
        env.reset()
        if raw_env.action_manager.total_action_dim != 8:
            raise AssertionError("frozen locomotion action dimension changed")
        trajectory = raw_env.action_manager.get_term("gluon_joint_reference")
        if not isinstance(trajectory, SmoothRandomJointPositionAction):
            raise AssertionError(f"unexpected action term {type(trajectory).__name__}")
        if len(GLUON_INSPECTION_GRAPH_NODE_IDS) != 4 or len(GLUON_INSPECTION_HUBS_RAD) != 4:
            raise AssertionError("inspection task must contain exactly four ordered hubs")

        raw_env.common_step_counter = 0
        raw_env.curriculum_manager.compute()
        if trajectory.workspace_scale != 0.0:
            raise AssertionError("inspection curriculum did not start at WORK")
        raw_env.common_step_counter = GLUON_INSPECTION_CURRICULUM_START_STEP
        raw_env.curriculum_manager.compute()
        if trajectory.workspace_scale != 0.0:
            raise AssertionError("GLUON moved before the TITA height curriculum completed")
        raw_env.common_step_counter = (
            GLUON_INSPECTION_CURRICULUM_START_STEP
            + GLUON_INSPECTION_CURRICULUM_END_STEP
        ) // 2
        raw_env.curriculum_manager.compute()
        if abs(trajectory.workspace_scale - 0.5) > 1.0e-7:
            raise AssertionError("inspection curriculum midpoint is not 0.5")
        raw_env.common_step_counter = GLUON_INSPECTION_CURRICULUM_END_STEP
        raw_env.curriculum_manager.compute()
        if abs(trajectory.workspace_scale - 1.0) > 1.0e-7:
            raise AssertionError("inspection curriculum did not reach full range")
        height_range = raw_env.command_manager.get_term("base_velocity").cfg.ranges.pos_z
        if tuple(height_range) != (0.25, 0.45):
            raise AssertionError(f"parent height curriculum mismatch: {height_range}")

        stand_action = torch.tensor(
            [[0.0, 0.0, 0.8, 0.8, -1.5, -1.5, 0.0, 0.0]],
            device=raw_env.device,
        ).repeat(args_cli.num_envs, 1)
        minimum_margin = float("inf")
        for _ in range(args_cli.physics_steps):
            raw_env.action_manager.process_action(stand_action)
            raw_env.action_manager.apply_action()
            raw_env.scene.write_data_to_sim()
            raw_env.sim.step(render=False)
            raw_env.scene.update(dt=raw_env.physics_dt)
            measured = trajectory._asset.data.joint_pos[:, trajectory._joint_ids]
            limits = trajectory._asset.data.soft_joint_pos_limits[:, trajectory._joint_ids]
            margin = torch.minimum(measured - limits[..., 0], limits[..., 1] - measured)
            minimum_margin = min(minimum_margin, float(margin.min().item()))
            if not bool(torch.isfinite(measured).all()):
                raise AssertionError("non-finite GLUON state")

        print(
            "TITA_GLUON_INSPECTION_CURRICULUM_SMOKE,domain=VALIDATION_SIM,status=PASS,"
            f"envs={args_cli.num_envs},physics_steps={args_cli.physics_steps},"
            f"hub_node_ids={GLUON_INSPECTION_GRAPH_NODE_IDS},"
            f"workspace_scale={trajectory.workspace_scale:.6g},"
            f"height_range={height_range},resume={int(runner_cfg.resume)},"
            f"teacher_tsne={int(runner_cfg.enable_teacher_tsne)},"
            f"minimum_soft_limit_margin_rad={minimum_margin:.6g},actions=8",
            flush=True,
        )
        return 0
    finally:
        env.close()


if __name__ == "__main__":
    try:
        status = main()
    finally:
        simulation_app.close()
    raise SystemExit(status)
