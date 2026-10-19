#!/usr/bin/env python3
"""Headless Isaac smoke for graph -> local servo -> dwell execution.

Execution domain: VALIDATION_SIM. The TITA root is fixed deliberately so this
test isolates the GLUON executor wiring; it is not a locomotion or safety test.
"""

from __future__ import annotations

import argparse
import math
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
parser.add_argument("--num-envs", type=int, default=2)
parser.add_argument("--max-physics-steps", type=int, default=2400)
parser.add_argument(
    "--target-offset-b",
    type=float,
    nargs=3,
    default=(0.0, 0.0, 0.0),
    metavar=("X", "Y", "Z"),
)
parser.add_argument("--position-only", action="store_true")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import gymnasium as gym  # noqa: E402
import torch  # noqa: E402

import ddt_lab.tasks  # noqa: F401, E402
from isaaclab.utils.math import quat_apply, quat_mul  # noqa: E402

from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.mdp import (  # noqa: E402
    SequentialInspectionJointPositionAction,
)
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.env_cfg import (  # noqa: E402
    GLUON_INSPECTION_TARGET_HUB_INDICES,
)
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.sequential_inspection import (  # noqa: E402
    ArmOption,
    ExecutorState,
)


TASK_ID = "Isaac-Velocity-Flat-Tita-Gluon-SequentialInspection-Play-v0-moo-ppo"
TARGET_HUBS = GLUON_INSPECTION_TARGET_HUB_INDICES


def main() -> int:
    if args_cli.num_envs <= 0 or args_cli.max_physics_steps <= 0:
        raise ValueError("num-envs and max-physics-steps must be positive")
    cfg = gym.spec(TASK_ID).kwargs["env_cfg_entry_point"]()
    cfg.scene.num_envs = args_cli.num_envs
    cfg.scene.robot.spawn.fix_base = True
    # Bounded interface smoke only: shorten the graph transition while keeping
    # quintic velocity/acceleration admission active.
    cfg.actions.gluon_joint_reference.segment_duration_range_s = (0.25, 0.25)
    cfg.actions.gluon_joint_reference.max_velocity_rad_s = math.radians(60.0)
    cfg.actions.gluon_joint_reference.max_acceleration_rad_s2 = math.radians(180.0)
    if args_cli.position_only:
        cfg.actions.gluon_joint_reference.local_orientation_gain = 0.0
        cfg.actions.gluon_joint_reference.orientation_tolerance_rad = math.pi
    env = gym.make(TASK_ID, cfg=cfg)
    raw_env = env.unwrapped

    try:
        env.reset()
        if raw_env.action_manager.total_action_dim != 8:
            raise AssertionError("low-level TITA action dimension changed")
        executor = raw_env.action_manager.get_term("gluon_joint_reference")
        if not isinstance(executor, SequentialInspectionJointPositionAction):
            raise AssertionError(f"unexpected executor type {type(executor).__name__}")

        root_pos_w = executor._asset.data.root_link_pos_w
        root_quat_w = executor._asset.data.root_link_quat_w
        hub_ids = torch.tensor(TARGET_HUBS, device=raw_env.device).repeat(
            args_cli.num_envs, 1
        )
        hub_pos_b = executor.hub_ee_pos_b[hub_ids]
        hub_quat_b = executor.hub_ee_quat_b[hub_ids]
        expanded_root_quat = root_quat_w[:, None, :].expand(-1, len(TARGET_HUBS), -1)
        target_offset_b = torch.tensor(
            args_cli.target_offset_b, device=raw_env.device
        ).view(1, 1, 3)
        target_pos_w = root_pos_w[:, None, :] + quat_apply(
            expanded_root_quat, hub_pos_b + target_offset_b
        )
        target_quat_w = quat_mul(expanded_root_quat, hub_quat_b)
        executor.set_target_sequence(target_pos_w, target_quat_w, hub_ids)
        accepted = executor.begin_bootstrap()
        if len(accepted) != args_cli.num_envs:
            raise AssertionError("bootstrap request was not accepted for every environment")

        stand_action = torch.tensor(
            [[0.0, 0.0, 0.8, 0.8, -1.5, -1.5, 0.0, 0.0]],
            device=raw_env.device,
        ).repeat(args_cli.num_envs, 1)
        execute_requested = torch.zeros(
            args_cli.num_envs, dtype=torch.bool, device=raw_env.device
        )
        max_tracking_error = 0.0
        max_position_error = 0.0
        physics_steps = 0
        while physics_steps < args_cli.max_physics_steps:
            raw_env.action_manager.process_action(stand_action)
            state = executor.executor_state
            ready = (
                (state == int(ExecutorState.IDLE))
                & (executor.prepared_target_index == 0)
                & executor.local_region_valid
                & ~execute_requested
            )
            if bool(torch.any(ready)):
                options = torch.full(
                    (args_cli.num_envs,),
                    int(ArmOption.HOLD),
                    dtype=torch.long,
                    device=raw_env.device,
                )
                options[ready] = int(ArmOption.EXECUTE_CURRENT)
                accepted_mask = executor.request_options(options)
                if not bool(torch.all(accepted_mask)):
                    raise AssertionError("valid execute/HOLD requests were rejected")
                execute_requested |= ready

            raw_env.action_manager.apply_action()
            raw_env.scene.write_data_to_sim()
            raw_env.sim.step(render=False)
            raw_env.scene.update(dt=raw_env.physics_dt)
            physics_steps += 1

            measured = executor._asset.data.joint_pos[:, executor._joint_ids]
            max_tracking_error = max(
                max_tracking_error,
                float(torch.abs(measured - executor.processed_actions).max().item()),
            )
            target_error = torch.linalg.vector_norm(
                executor.current_target_pos_w
                - (
                    executor._asset.data.root_link_pos_w
                    + quat_apply(
                        executor._asset.data.root_link_quat_w,
                        executor._forward_end_effector(measured),
                    )
                ),
                dim=-1,
            )
            max_position_error = max(max_position_error, float(target_error.max().item()))
            if bool(torch.all(executor.current_target_index >= 1)):
                break

        if not bool(torch.all(execute_requested)):
            raise AssertionError("executor never entered local target servo")
        if not bool(torch.all(executor.current_target_index >= 1)):
            raise AssertionError(
                "target zero did not complete; "
                f"states={executor.executor_state.tolist()},"
                f"position_error_m={executor.position_error_norm_m.tolist()},"
                f"orientation_error_rad={executor.orientation_error_norm_rad.tolist()},"
                f"joint_limit_margin_rad={executor.joint_limit_margin_rad.tolist()}"
                f",measured_joint_rad={executor._asset.data.joint_pos[:, executor._joint_ids].tolist()}"
                f",reference_joint_rad={executor.processed_actions.tolist()}"
            )
        if bool(torch.any(executor.executor_state == int(ExecutorState.EMERGENCY_HOLD))):
            raise AssertionError("executor entered emergency hold")
        if max_tracking_error > 0.25:
            raise AssertionError(f"joint tracking error too large: {max_tracking_error}")

        print(
            "TITA_GLUON_SEQUENTIAL_EXECUTOR_SMOKE,domain=VALIDATION_SIM,status=PASS,"
            f"envs={args_cli.num_envs},physics_steps={physics_steps},"
            f"max_joint_tracking_error_rad={max_tracking_error:.9g},"
            f"max_ee_position_error_m={max_position_error:.9g},"
            f"completed_target_index={int(executor.current_target_index.min().item())},"
            "root_fixed=1,cbf_enabled=0",
            flush=True,
        )
        return 0
    finally:
        env.close()


if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception:
        traceback.print_exc()
        raise
    finally:
        simulation_app.close()
    raise SystemExit(exit_code)
