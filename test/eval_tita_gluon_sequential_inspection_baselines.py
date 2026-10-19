#!/usr/bin/env python3
"""Evaluate scripted sequential-inspection baselines with a frozen TITA policy.

Execution domain: VALIDATION_SIM. This runner uses the current WORK-hub rays
and local differential IK without a CBF. It is a task/executor Go/No-Go, not
collision-safety evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
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


DEFAULT_CHECKPOINT = (
    REPO_ROOT
    / "lab"
    / "logs"
    / "co_rl"
    / "Tita_Gluon_CurriculumArm_RMATeacher-v0-mooppo"
    / "mooppo"
    / "2026-08-09_17-15-39_massless_sensor_rma_teacher_v2"
    / "model_9000.pt"
)
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "docs"
    / "exp"
    / "2026-08-10"
    / "sequential_inspection_baseline_validation.json"
)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
parser.add_argument("--controller", choices=("stop_and_go", "scheduler"), required=True)
parser.add_argument("--num-envs", type=int, default=8)
parser.add_argument("--max-steps", type=int, default=2500)
parser.add_argument("--episode-length-s", type=float, default=180.0)
parser.add_argument("--bootstrap-max-steps", type=int, default=1500)
parser.add_argument("--seed", type=int, default=20260810)
parser.add_argument("--scheduler-start-distance-m", type=float, default=1.1)
parser.add_argument("--scheduler-arm-speed-scale", type=float, default=0.4)
parser.add_argument("--fixed-height-m", type=float, default=0.39)
parser.add_argument("--graph-max-velocity-deg-s", type=float, default=20.0)
parser.add_argument("--graph-max-acceleration-deg-s2", type=float, default=40.0)
parser.add_argument(
    "--local-region-half-extent-m",
    type=float,
    nargs=3,
    metavar=("X", "Y", "Z"),
    help="Validation-only override for the provisional hub-local AABB.",
)
parser.add_argument(
    "--position-only-local-servo",
    action="store_true",
    help="Validation-only diagnostic that removes the local EE orientation objective.",
)
parser.add_argument(
    "--target-pose-frame",
    choices=("gravity_aligned", "settled_base"),
    default="gravity_aligned",
    help=(
        "Frame used to place nominal hub poses along the fixed world route; "
        "gravity_aligned is the intended inspection-task contract."
    ),
)
parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import gymnasium as gym  # noqa: E402
import torch  # noqa: E402

import ddt_lab.tasks  # noqa: F401, E402
from isaaclab.utils.math import quat_apply, quat_apply_inverse, quat_mul, yaw_quat  # noqa: E402
from scripts.co_rl.core.runners import MOO_OnPolicyRunner  # noqa: E402
from scripts.co_rl.core.wrapper import CoRlVecEnvWrapper  # noqa: E402

from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.mdp import (  # noqa: E402
    SequentialInspectionJointPositionAction,
)
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.env_cfg import (  # noqa: E402
    GLUON_INSPECTION_TARGET_HUB_INDICES,
)
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.sequential_inspection import (  # noqa: E402
    ArmOption,
    CoordinatorObservation,
    ExecutorEvent,
    ExecutorState,
    StopAndGoController,
    TunedConcurrentScheduler,
)


TASK_ID = "Isaac-Velocity-Flat-Tita-Gluon-SequentialInspection-Play-v0-moo-ppo"
TARGET_HUBS = GLUON_INSPECTION_TARGET_HUB_INDICES
NOMINAL_ROUTE_S_M = (0.9, 2.1, 3.3, 4.5)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def privileged_obs(obs_dict: dict[str, torch.Tensor] | None, device: str) -> torch.Tensor | None:
    if not obs_dict:
        return None
    keys = sorted(key for key in obs_dict if key.startswith("priv_"))
    if keys:
        return torch.cat([obs_dict[key] for key in keys], dim=-1).to(device)
    return obs_dict.get("privileged")


def main() -> int:
    if args_cli.num_envs <= 0 or args_cli.max_steps <= 0 or args_cli.bootstrap_max_steps <= 0:
        raise ValueError("num-envs, max-steps, and bootstrap-max-steps must be positive")
    checkpoint = args_cli.checkpoint.resolve()
    if not checkpoint.is_file():
        raise FileNotFoundError(checkpoint)

    spec = gym.spec(TASK_ID)
    env_cfg = spec.kwargs["env_cfg_entry_point"]()
    env_cfg.seed = args_cli.seed
    env_cfg.scene.num_envs = args_cli.num_envs
    if args_cli.episode_length_s <= 0.0:
        raise ValueError("episode-length-s must be positive")
    env_cfg.episode_length_s = args_cli.episode_length_s
    # This evaluator has no visual output. Matching the render interval to the
    # control decimation avoids four redundant render calls per policy step in
    # the inherited configuration without changing physics or control timing.
    env_cfg.sim.render_interval = env_cfg.decimation
    env_cfg.commands.base_velocity.debug_vis = False
    env_cfg.curriculum.widen_height_range = None
    if args_cli.local_region_half_extent_m is not None:
        if any(value <= 0.0 for value in args_cli.local_region_half_extent_m):
            raise ValueError("local-region half extents must be positive")
        env_cfg.actions.gluon_joint_reference.local_region_half_extent_m = tuple(
            args_cli.local_region_half_extent_m
        )
    if args_cli.graph_max_velocity_deg_s <= 0.0 or args_cli.graph_max_acceleration_deg_s2 <= 0.0:
        raise ValueError("graph velocity and acceleration overrides must be positive")
    env_cfg.actions.gluon_joint_reference.max_velocity_rad_s = math.radians(
        args_cli.graph_max_velocity_deg_s
    )
    env_cfg.actions.gluon_joint_reference.max_acceleration_rad_s2 = math.radians(
        args_cli.graph_max_acceleration_deg_s2
    )
    if args_cli.position_only_local_servo:
        env_cfg.actions.gluon_joint_reference.local_orientation_gain = 0.0
        env_cfg.actions.gluon_joint_reference.orientation_tolerance_rad = math.pi
    agent_cfg = spec.kwargs["co_rl_cfg_entry_point"]()
    gym_env = gym.make(TASK_ID, cfg=env_cfg)
    env = CoRlVecEnvWrapper(gym_env, agent_cfg)
    runner = MOO_OnPolicyRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)

    try:
        runner.load(str(checkpoint))
        policy = runner.get_inference_policy(device=env.unwrapped.device)
        torch.manual_seed(args_cli.seed)
        obs, extras = env.reset()
        raw_env = env.unwrapped
        executor = raw_env.action_manager.get_term("gluon_joint_reference")
        if not isinstance(executor, SequentialInspectionJointPositionAction):
            raise AssertionError(f"unexpected executor type {type(executor).__name__}")
        if raw_env.action_manager.total_action_dim != 8:
            raise AssertionError("frozen low-level policy action contract is not eight")

        command_term = raw_env.command_manager.get_term("base_velocity")
        command = command_term.vel_command_b
        route_s = torch.tensor(NOMINAL_ROUTE_S_M, device=raw_env.device).repeat(
            args_cli.num_envs, 1
        )
        route_s += 0.10 * (2.0 * torch.rand_like(route_s) - 1.0)
        local_offsets = torch.zeros(
            (args_cli.num_envs, len(TARGET_HUBS), 3), device=raw_env.device
        )
        local_offsets[..., 0] = 0.03 * (2.0 * torch.rand_like(route_s) - 1.0)
        local_offsets[..., 1] = 0.02 * (2.0 * torch.rand_like(route_s) - 1.0)
        local_offsets[..., 2] = 0.02 * (2.0 * torch.rand_like(route_s) - 1.0)
        hub_ids = torch.tensor(TARGET_HUBS, device=raw_env.device).repeat(
            args_cli.num_envs, 1
        )
        hub_pos_b = executor.hub_ee_pos_b[hub_ids]
        hub_quat_b = executor.hub_ee_quat_b[hub_ids]
        bootstrap_root_pos_w = raw_env.scene["robot"].data.root_link_pos_w.clone()
        bootstrap_root_quat_w = raw_env.scene["robot"].data.root_link_quat_w.clone()
        expanded_bootstrap_quat = bootstrap_root_quat_w[:, None, :].expand(
            -1, len(TARGET_HUBS), -1
        )
        executor.set_target_sequence(
            bootstrap_root_pos_w[:, None, :]
            + quat_apply(expanded_bootstrap_quat, hub_pos_b),
            quat_mul(expanded_bootstrap_quat, hub_quat_b),
            hub_ids,
        )
        executor.begin_bootstrap()

        if args_cli.controller == "stop_and_go":
            controller = StopAndGoController()
        else:
            controller = TunedConcurrentScheduler(
                start_distance_m=args_cli.scheduler_start_distance_m,
                arm_motion_speed_scale=args_cli.scheduler_arm_speed_scale,
            )

        def force_commands(vx: torch.Tensor, yaw: torch.Tensor) -> None:
            command[:, 0] = vx
            command[:, 1] = 0.0
            command[:, 2] = yaw
            command[:, 3] = args_cli.fixed_height_m
            command_term.time_left[:] = 1.0e6
            command_term.time_elapsed[:] = command_term.cfg.initial_phase_time + 1.0
            command_term.is_heading_env[:] = False
            command_term.is_standing_env[:] = False

        # Bootstrap target zero's hub outside the timed task interval.
        zero = torch.zeros(args_cli.num_envs, device=raw_env.device)
        force_commands(zero, zero)
        obs, extras = env.get_observations()
        priv = privileged_obs(extras.get("observations"), runner.device)
        with torch.no_grad():
            for _ in range(args_cli.bootstrap_max_steps):
                force_commands(zero, zero)
                actions = policy(obs, privileged_info=priv) if priv is not None else policy(obs)
                obs, _, dones, infos = env.step(actions)
                priv = privileged_obs(infos.get("observations"), runner.device)
                if bool(torch.any(dones)):
                    raise RuntimeError("low-level environment reset during bootstrap")
                ready = (
                    (executor.executor_state == int(ExecutorState.IDLE))
                    & (executor.prepared_target_index == 0)
                )
                if bool(torch.all(ready)):
                    break
            else:
                raise RuntimeError("bootstrap did not reach the first hub")

            # Define the fixed world route only after the low-level policy and
            # arm have settled. Otherwise the reset-height transient shifts a
            # visually correct target outside its base-frame local region.
            route_start_w = raw_env.scene["robot"].data.root_link_pos_w.clone()
            hub_reference_quat_w = raw_env.scene[
                "robot"
            ].data.root_link_quat_w.clone()
            # The inspection route is a gravity-aligned world path. Using the
            # full settled base quaternion for its translation would move a
            # distant target vertically by route_s * sin(base_pitch). The
            # intended task also places nominal hub poses in this upright
            # route frame; the settled-base variant is retained only to
            # reproduce earlier diagnostics.
            route_quat_w = yaw_quat(hub_reference_quat_w)
            route_start_tilt_norm = torch.linalg.vector_norm(
                raw_env.scene["robot"].data.projected_gravity_b[:, :2], dim=-1
            )
            route_start_arm_joint_pos = raw_env.scene["robot"].data.joint_pos[
                :, executor._joint_ids
            ].clone()
            route_start_arm_reference = executor.processed_actions.clone()
            route_x_w = quat_apply(
                route_quat_w,
                torch.tensor([[1.0, 0.0, 0.0]], device=raw_env.device).repeat(
                    args_cli.num_envs, 1
                ),
            )
            route_y_w = quat_apply(
                route_quat_w,
                torch.tensor([[0.0, 1.0, 0.0]], device=raw_env.device).repeat(
                    args_cli.num_envs, 1
                ),
            )
            target_local = hub_pos_b + local_offsets
            nominal_target_frame_quat = (
                route_quat_w
                if args_cli.target_pose_frame == "gravity_aligned"
                else hub_reference_quat_w
            )
            expanded_nominal_target_frame_quat = nominal_target_frame_quat[:, None, :].expand(
                -1, len(TARGET_HUBS), -1
            )
            target_pos_w = (
                route_start_w[:, None, :]
                + route_s[..., None] * route_x_w[:, None, :]
                + quat_apply(expanded_nominal_target_frame_quat, target_local)
            )
            target_quat_w = quat_mul(expanded_nominal_target_frame_quat, hub_quat_b)
            executor.set_target_sequence(target_pos_w, target_quat_w, hub_ids)

            success = torch.zeros(args_cli.num_envs, dtype=torch.bool, device=raw_env.device)
            failed = torch.zeros_like(success)
            completion_step = torch.full(
                (args_cli.num_envs,), -1, dtype=torch.long, device=raw_env.device
            )
            base_moving_steps = torch.zeros(args_cli.num_envs, device=raw_env.device)
            arm_moving_steps = torch.zeros_like(base_moving_steps)
            overlap_steps = torch.zeros_like(base_moving_steps)
            option_rejections = torch.zeros_like(base_moving_steps)
            local_region_exits = torch.zeros_like(base_moving_steps)
            base_contacts = torch.zeros_like(base_moving_steps)
            timeout_count = torch.zeros_like(base_moving_steps)
            max_height_delta_m = torch.zeros_like(base_moving_steps)
            max_tilt_norm = route_start_tilt_norm.clone()
            transition_events: list[list[dict[str, float | int]]] = [
                [] for _ in range(args_cli.num_envs)
            ]
            previous_state_key: list[tuple[int, int, int]] = [
                (
                    int(executor.current_target_index[index].item()),
                    int(executor.executor_state[index].item()),
                    int(executor._graph_phase[index].item()),
                )
                for index in range(args_cli.num_envs)
            ]

            for step in range(args_cli.max_steps):
                base_pos_w = raw_env.scene["robot"].data.root_link_pos_w
                max_height_delta_m = torch.maximum(
                    max_height_delta_m,
                    torch.abs(base_pos_w[:, 2] - route_start_w[:, 2]),
                )
                max_tilt_norm = torch.maximum(
                    max_tilt_norm,
                    torch.linalg.vector_norm(
                        raw_env.scene["robot"].data.projected_gravity_b[:, :2], dim=-1
                    ),
                )
                progress_s = torch.sum((base_pos_w - route_start_w) * route_x_w, dim=-1)
                cross_track_m = torch.sum(
                    (base_pos_w - route_start_w) * route_y_w, dim=-1
                )
                current_x_w = quat_apply(
                    yaw_quat(raw_env.scene["robot"].data.root_link_quat_w),
                    torch.tensor([[1.0, 0.0, 0.0]], device=raw_env.device).repeat(
                        args_cli.num_envs, 1
                    ),
                )
                heading_error = torch.atan2(
                    torch.sum(current_x_w * route_y_w, dim=-1),
                    torch.sum(current_x_w * route_x_w, dim=-1),
                )
                # Keep the route heading convention fixed near a target.  The
                # proportional longitudinal controller may cross zero by a few
                # centimeters; flipping the lateral steering sign there causes
                # heading chatter during station keeping.
                route_yaw_error = -heading_error - 3.0 * cross_track_m
                near_station = torch.abs(
                    route_s[
                        torch.arange(args_cli.num_envs, device=raw_env.device),
                        torch.clamp(
                            executor.current_target_index,
                            max=len(TARGET_HUBS) - 1,
                        ),
                    ]
                    - progress_s
                ) <= 0.10
                reselect_ids = torch.nonzero(
                    near_station
                    & (executor.executor_state == int(ExecutorState.IDLE))
                    & executor.at_stow
                    & ~executor.task_complete,
                    as_tuple=False,
                ).squeeze(-1)
                if len(reselect_ids) > 0:
                    executor.reselect_current_target_hubs(
                        reselect_ids,
                        candidate_hub_indices=torch.tensor(
                            TARGET_HUBS, dtype=torch.long, device=raw_env.device
                        ),
                    )
                active_target_indices = torch.clamp(
                    executor.current_target_index, max=len(TARGET_HUBS) - 1
                )
                active_hub_indices = executor._target_hub_indices[
                    torch.arange(args_cli.num_envs, device=raw_env.device),
                    active_target_indices,
                ]
                current_target_pos_b = quat_apply_inverse(
                    raw_env.scene["robot"].data.root_link_quat_w,
                    executor.current_target_pos_w - base_pos_w,
                )
                target_minus_hub_b = (
                    current_target_pos_b - executor.hub_ee_pos_b[active_hub_indices]
                )
                options = torch.full(
                    (args_cli.num_envs,),
                    int(ArmOption.HOLD),
                    dtype=torch.long,
                    device=raw_env.device,
                )
                vx = torch.zeros(args_cli.num_envs, device=raw_env.device)
                yaw = torch.zeros_like(vx)
                active = ~(success | failed)
                for env_index in torch.nonzero(active, as_tuple=False).squeeze(-1).tolist():
                    target_index = min(
                        int(executor.current_target_index[env_index].item()),
                        len(TARGET_HUBS) - 1,
                    )
                    controller_obs = CoordinatorObservation(
                        target_index=target_index,
                        target_count=len(TARGET_HUBS),
                        longitudinal_distance_m=(
                            float(route_s[env_index, target_index].item())
                            - float(progress_s[env_index].item())
                        ),
                        yaw_error_rad=float(route_yaw_error[env_index].item()),
                        local_region_valid=bool(executor.local_region_valid[env_index].item()),
                        prepared_for_current=bool(
                            executor.prepared_target_index[env_index]
                            == executor.current_target_index[env_index]
                        ),
                        at_stow=bool(executor.at_stow[env_index].item()),
                        executor_state=ExecutorState(
                            int(executor.executor_state[env_index].item())
                        ),
                        task_complete=bool(executor.task_complete[env_index].item()),
                        base_speed_m_s=float(
                            torch.linalg.vector_norm(
                                raw_env.scene["robot"].data.root_link_lin_vel_b[
                                    env_index, :2
                                ]
                            ).item()
                        ),
                        base_yaw_rate_rad_s=float(
                            raw_env.scene["robot"].data.root_link_ang_vel_b[
                                env_index, 2
                            ].item()
                        ),
                        target_minus_hub_x_m=float(
                            target_minus_hub_b[env_index, 0].item()
                        ),
                        target_minus_hub_y_m=float(
                            target_minus_hub_b[env_index, 1].item()
                        ),
                    )
                    high_command = controller.command(controller_obs)
                    vx[env_index] = high_command.vx_cmd_m_s
                    yaw[env_index] = high_command.yaw_rate_cmd_rad_s
                    options[env_index] = int(high_command.arm_option)

                accepted = executor.request_options(options)
                option_rejections += active & ~accepted
                arm_moving = (
                    (executor.executor_state == int(ExecutorState.GRAPH_EXECUTION))
                    | (executor.executor_state == int(ExecutorState.LOCAL_TARGET_SERVO))
                ) & active
                base_moving = (torch.abs(vx) > 1.0e-3) & active
                base_moving_steps += base_moving
                arm_moving_steps += arm_moving
                overlap_steps += base_moving & arm_moving

                force_commands(vx, yaw)
                actions = policy(obs, privileged_info=priv) if priv is not None else policy(obs)
                obs, _, dones, infos = env.step(actions)
                priv = privileged_obs(infos.get("observations"), runner.device)
                for env_index in torch.nonzero(active, as_tuple=False).squeeze(-1).tolist():
                    state_key = (
                        int(executor.current_target_index[env_index].item()),
                        int(executor.executor_state[env_index].item()),
                        int(executor._graph_phase[env_index].item()),
                    )
                    if state_key != previous_state_key[env_index]:
                        transition_events[env_index].append(
                            {
                                "step": step + 1,
                                "time_s": (step + 1) * float(raw_env.step_dt),
                                "target_index": state_key[0],
                                "executor_state": state_key[1],
                                "graph_phase": state_key[2],
                                "prepared_target_index": int(
                                    executor.prepared_target_index[env_index].item()
                                ),
                                "option_progress": float(
                                    executor.option_progress[env_index].item()
                                ),
                                "route_progress_m": float(progress_s[env_index].item()),
                                "position_error_m": float(
                                    executor.position_error_norm_m[env_index].item()
                                ),
                                "target_minus_hub_b_m": target_minus_hub_b[
                                    env_index
                                ].tolist(),
                                "measured_arm_joint_rad": raw_env.scene["robot"].data.joint_pos[
                                    env_index, executor._joint_ids
                                ].tolist(),
                                "reference_arm_joint_rad": executor.processed_actions[
                                    env_index
                                ].tolist(),
                            }
                        )
                        previous_state_key[env_index] = state_key
                new_success = executor.task_complete & active
                success |= new_success
                completion_step[new_success] = step + 1
                local_region_exits += (
                    executor.last_event == int(ExecutorEvent.LOCAL_REGION_EXIT)
                ) & active
                emergency_hold = (
                    executor.executor_state == int(ExecutorState.EMERGENCY_HOLD)
                ) & active
                timeouts = infos.get("time_outs", torch.zeros_like(dones)).bool()
                contacts = dones.bool() & ~timeouts
                base_contacts += contacts
                timeout_count += dones.bool() & timeouts
                failed |= (dones.bool() | emergency_hold) & active
                if bool(torch.all(success | failed)):
                    break

        step_dt_s = float(raw_env.step_dt)
        successful_times = completion_step[success].float() * step_dt_s
        moving_union = torch.clamp(base_moving_steps + arm_moving_steps - overlap_steps, min=1.0)
        final_base_pos_w = raw_env.scene["robot"].data.root_link_pos_w
        final_tilt_norm = torch.linalg.vector_norm(
            raw_env.scene["robot"].data.projected_gravity_b[:, :2], dim=-1
        )
        final_progress_s = torch.sum((final_base_pos_w - route_start_w) * route_x_w, dim=-1)
        final_target_pos_b = quat_apply(
            torch.cat(
                (
                    raw_env.scene["robot"].data.root_link_quat_w[:, :1],
                    -raw_env.scene["robot"].data.root_link_quat_w[:, 1:],
                ),
                dim=-1,
            ),
            executor.current_target_pos_w - final_base_pos_w,
        )
        final_target_ids = torch.clamp(
            executor.current_target_index, max=len(TARGET_HUBS) - 1
        )
        final_hub_ids = hub_ids[
            torch.arange(args_cli.num_envs, device=raw_env.device), final_target_ids
        ]
        final_local_delta_b = final_target_pos_b - executor.hub_ee_pos_b[final_hub_ids]
        final_arm_joint_pos = raw_env.scene["robot"].data.joint_pos[:, executor._joint_ids]
        final_joint_limit_margins = torch.minimum(
            final_arm_joint_pos - executor._soft_limits[:, 0],
            executor._soft_limits[:, 1] - final_arm_joint_pos,
        )
        result = {
            "execution_domain": "VALIDATION_SIM",
            # A vectorized validation candidate passes only when every
            # environment completes.  Reporting PASS for one success in a
            # partially failed batch hides exactly the tail failures this Gate
            # is intended to expose.
            "evidence_status": "PASS" if bool(torch.all(success)) else "FAIL",
            "task": TASK_ID,
            "seed": args_cli.seed,
            "max_steps": args_cli.max_steps,
            "checkpoint": str(checkpoint),
            "checkpoint_sha256": sha256_file(checkpoint),
            "controller": args_cli.controller,
            "controller_parameters": {
                "scheduler_start_distance_m": args_cli.scheduler_start_distance_m,
                "scheduler_arm_speed_scale": args_cli.scheduler_arm_speed_scale,
                "fixed_height_m": args_cli.fixed_height_m,
                "route_cross_track_gain": 3.0,
                "local_region_half_extent_m": list(
                    env_cfg.actions.gluon_joint_reference.local_region_half_extent_m
                ),
                "position_only_local_servo": args_cli.position_only_local_servo,
                "target_pose_frame": args_cli.target_pose_frame,
                "episode_length_s": args_cli.episode_length_s,
                "graph_max_velocity_deg_s": args_cli.graph_max_velocity_deg_s,
                "graph_max_acceleration_deg_s2": args_cli.graph_max_acceleration_deg_s2,
            },
            "num_envs": args_cli.num_envs,
            "success_rate": float(success.float().mean().item()),
            "successful_cycle_time_mean_s": float(successful_times.mean().item())
            if bool(torch.any(success))
            else None,
            "successful_cycle_time_values_s": successful_times.cpu().tolist(),
            "failure_rate": float(failed.float().mean().item()),
            "fall_rate": float((base_contacts > 0).float().mean().item()),
            "base_contact_count": int(base_contacts.sum().item()),
            "underlying_timeout_count": int(timeout_count.sum().item()),
            "concurrent_motion_ratio": float((overlap_steps / moving_union).mean().item()),
            "option_rejection_count": int(option_rejections.sum().item()),
            "local_region_exit_count": int(local_region_exits.sum().item()),
            "final_route_progress_m": final_progress_s.cpu().tolist(),
            "route_start_base_height_m": route_start_w[:, 2].cpu().tolist(),
            "final_base_height_m": final_base_pos_w[:, 2].cpu().tolist(),
            "final_base_height_delta_m": (
                final_base_pos_w[:, 2] - route_start_w[:, 2]
            ).cpu().tolist(),
            "max_abs_base_height_delta_m": max_height_delta_m.cpu().tolist(),
            "route_start_tilt_norm": route_start_tilt_norm.cpu().tolist(),
            "route_start_selected_joint_pos_rad": route_start_arm_joint_pos.cpu().tolist(),
            "route_start_reference_joint_pos_rad": route_start_arm_reference.cpu().tolist(),
            "final_tilt_norm": final_tilt_norm.cpu().tolist(),
            "max_tilt_norm": max_tilt_norm.cpu().tolist(),
            "final_root_quat_w": raw_env.scene[
                "robot"
            ].data.root_link_quat_w.cpu().tolist(),
            "final_cross_track_m": torch.sum(
                (final_base_pos_w - route_start_w) * route_y_w, dim=-1
            ).cpu().tolist(),
            "final_target_index": executor.current_target_index.cpu().tolist(),
            "final_executor_state": executor.executor_state.cpu().tolist(),
            "final_prepared_target_index": executor.prepared_target_index.cpu().tolist(),
            "final_local_region_valid": executor.local_region_valid.cpu().tolist(),
            "final_option_progress": executor.option_progress.cpu().tolist(),
            "final_position_error_norm_m": executor.position_error_norm_m.cpu().tolist(),
            "final_orientation_error_norm_rad": (
                executor.orientation_error_norm_rad.cpu().tolist()
            ),
            "final_joint_limit_margin_rad": executor.joint_limit_margin_rad.cpu().tolist(),
            "selected_joint_names": list(executor._joint_names),
            "final_selected_joint_pos_rad": final_arm_joint_pos.cpu().tolist(),
            "final_joint_limit_margins_rad": final_joint_limit_margins.cpu().tolist(),
            "final_limiting_selected_joint_index": torch.argmin(
                final_joint_limit_margins, dim=-1
            ).cpu().tolist(),
            "final_graph_phase": executor._graph_phase.cpu().tolist(),
            "final_graph_segment_elapsed_s": executor._segment_elapsed_s.cpu().tolist(),
            "final_graph_segment_duration_s": executor._segment_duration_s.cpu().tolist(),
            "final_graph_tracking_error_rad": torch.linalg.vector_norm(
                executor._segment_goal - final_arm_joint_pos, dim=-1
            ).cpu().tolist(),
            "transition_events": transition_events,
            "final_target_minus_hub_b_m": final_local_delta_b.cpu().tolist(),
            "cbf_enabled": False,
            "self_collision_enabled": False,
        }
        args_cli.output.parent.mkdir(parents=True, exist_ok=True)
        existing = []
        if args_cli.output.is_file():
            payload = json.loads(args_cli.output.read_text(encoding="utf-8"))
            existing = payload if isinstance(payload, list) else [payload]
        existing.append(result)
        args_cli.output.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
        cycle_time_display = result["successful_cycle_time_mean_s"]
        if cycle_time_display is None:
            cycle_time_display = math.nan
        print(
            "TITA_GLUON_SEQUENTIAL_BASELINE,domain=VALIDATION_SIM,"
            f"status={result['evidence_status']},controller={args_cli.controller},"
            f"success_rate={result['success_rate']:.6f},"
            f"cycle_time_s={cycle_time_display:.6f},"
            f"fall_rate={result['fall_rate']:.6f},"
            f"overlap_ratio={result['concurrent_motion_ratio']:.6f},"
            f"local_region_exits={result['local_region_exit_count']},"
            f"output={args_cli.output.resolve()}",
            flush=True,
        )
        return 0 if bool(torch.all(success)) else 2
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
