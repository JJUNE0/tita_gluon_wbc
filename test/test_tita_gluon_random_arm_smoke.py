#!/usr/bin/env python3
"""Headless stage-2 smoke for conditioned random GLUON trajectories."""

import argparse
import faulthandler
import math
import sys
import traceback
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LAB_ROOT = REPO_ROOT / "lab"
TEST_ROOT = REPO_ROOT / "test"
for search_path in (LAB_ROOT, TEST_ROOT):
    if str(search_path) not in sys.path:
        sys.path.insert(0, str(search_path))

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--steps", type=int, default=320)
parser.add_argument("--num-envs", type=int, default=4)
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
import numpy as np  # noqa: E402
import torch  # noqa: E402

import ddt_lab.tasks  # noqa: F401, E402
from analyze_gluon_workspace import forward_link6_with_jacobian, load_chain  # noqa: E402
from analyze_tita_gluon_reachability import (  # noqa: E402
    CollisionChecker,
    DEFAULT_COMBINED_URDF,
)
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.env_cfg import (  # noqa: E402
    GLUON_CONDITIONED_WAYPOINTS_RAD,
    GLUON_JOINT_NAMES,
    GLUON_TRAJECTORY_MAX_ACCELERATION_RAD_S2,
    GLUON_TRAJECTORY_MAX_VELOCITY_RAD_S,
    GLUON_WORK_JOINT_POS,
    TITA_GLUON_STACK_POLICY_TERMS,
)
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.mdp.actions import (  # noqa: E402
    SmoothRandomJointPositionAction,
)


TASK_ID = "Isaac-Velocity-Flat-Tita-Gluon-RandomArm-Play-v0-moo-ppo"
PATH_SAMPLE_COUNT = 33
MIN_SIGMA = 0.015
MIN_JOINT_MARGIN_RAD = math.radians(10.0)
COLLISION_CLEARANCE_M = 0.015
TITA_STAND_Q_RAD = np.array([0.0, 0.8, -1.5, 0.0, 0.0, 0.8, -1.5, 0.0])


def validate_waypoint_contract() -> tuple[float, float]:
    """Recheck every WORK-to-waypoint path against its recorded gates."""
    gluon_urdf = (
        REPO_ROOT
        / "sim2sim"
        / "robot" / "gluon"
        / "urdf"
        / "gluon_2L6_4L3_sim.urdf"
    )
    chain = load_chain(gluon_urdf)
    lower = np.asarray([joint["lower"] for joint in chain])
    upper = np.asarray([joint["upper"] for joint in chain])
    center = np.asarray(GLUON_WORK_JOINT_POS)
    fractions = np.linspace(0.0, 1.0, PATH_SAMPLE_COUNT)
    checker = CollisionChecker(
        DEFAULT_COMBINED_URDF,
        TITA_STAND_Q_RAD,
        COLLISION_CLEARANCE_M,
    )
    minimum_sigma = math.inf
    minimum_margin = math.inf

    for waypoint_index, waypoint_values in enumerate(GLUON_CONDITIONED_WAYPOINTS_RAD):
        waypoint = np.asarray(waypoint_values)
        path = center[None, :] + fractions[:, None] * (waypoint - center)[None, :]
        _, jacobians = forward_link6_with_jacobian(chain, path)
        sigma = np.linalg.svd(jacobians[:, :, :5], compute_uv=False)[:, -1]
        joint_margin = np.min(np.minimum(path - lower, upper - path))
        minimum_sigma = min(minimum_sigma, float(np.min(sigma)))
        minimum_margin = min(minimum_margin, float(joint_margin))
        if np.min(sigma) < MIN_SIGMA:
            raise AssertionError(
                f"Waypoint {waypoint_index} path sigma_min={np.min(sigma):.9g}"
            )
        if joint_margin < MIN_JOINT_MARGIN_RAD:
            raise AssertionError(
                f"Waypoint {waypoint_index} path margin={joint_margin:.9g} rad"
            )
        for sample_index, joint_position in enumerate(path):
            collision = checker.collision_name(joint_position)
            if collision is not None:
                raise AssertionError(
                    f"Waypoint {waypoint_index} sample {sample_index} collision={collision}"
                )
    return minimum_sigma, minimum_margin


def line_set_residual(commands: torch.Tensor) -> float:
    """Return the largest distance from a command to any WORK-waypoint segment."""
    center = commands.new_tensor(GLUON_WORK_JOINT_POS)
    waypoints = commands.new_tensor(GLUON_CONDITIONED_WAYPOINTS_RAD)
    segment_delta = waypoints - center
    delta_norm_sq = torch.sum(segment_delta * segment_delta, dim=-1)
    relative = commands[:, None, :] - center
    phase = torch.sum(relative * segment_delta[None, :, :], dim=-1) / delta_norm_sq
    phase = torch.clamp(phase, 0.0, 1.0)
    projection = center + phase[:, :, None] * segment_delta[None, :, :]
    residual = torch.linalg.vector_norm(commands[:, None, :] - projection, dim=-1)
    return float(torch.amin(residual, dim=1).amax().item())


def main() -> int:
    if args_cli.steps <= 0:
        raise ValueError("--steps must be positive")
    if args_cli.num_envs <= 0:
        raise ValueError("--num-envs must be positive")
    if args_cli.dump_traceback_after_s < 0.0:
        raise ValueError("--dump-traceback-after-s must be non-negative")
    if args_cli.dump_traceback_after_s > 0.0:
        faulthandler.dump_traceback_later(args_cli.dump_traceback_after_s, repeat=True)

    minimum_sigma, minimum_margin = validate_waypoint_contract()
    cfg = gym.spec(TASK_ID).kwargs["env_cfg_entry_point"]()
    cfg.seed = 20260807
    cfg.scene.num_envs = args_cli.num_envs
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
        trajectory = unwrapped.action_manager.get_term("gluon_joint_reference")
        if not isinstance(trajectory, SmoothRandomJointPositionAction):
            raise AssertionError(f"Unexpected action term: {type(trajectory).__name__}")
        stack_terms = tuple(unwrapped.observation_manager.active_terms["stack_policy"])
        if stack_terms != TITA_GLUON_STACK_POLICY_TERMS:
            raise AssertionError(f"Unexpected stack_policy order: {stack_terms}")

        stand_action = torch.tensor(
            [[0.0, 0.0, 0.8, 0.8, -1.5, -1.5, 0.0, 0.0]],
            device=unwrapped.device,
        ).repeat(args_cli.num_envs, 1)
        command_samples = []
        measured_samples = []
        for _ in range(args_cli.steps):
            unwrapped.action_manager.process_action(stand_action)
            for _ in range(unwrapped.cfg.decimation):
                unwrapped.action_manager.apply_action()
                command_samples.append(trajectory.processed_actions.clone())
                unwrapped.scene.write_data_to_sim()
                unwrapped.sim.step(render=False)
                unwrapped.scene.update(dt=unwrapped.physics_dt)
                measured_samples.append(robot.data.joint_pos[:, joint_ids].clone())
        obs = unwrapped.observation_manager.compute(update_history=True)

        commands = torch.stack(command_samples)
        measured = torch.stack(measured_samples)
        if not bool(torch.isfinite(commands).all() and torch.isfinite(measured).all()):
            raise AssertionError("Non-finite GLUON command or measured state")
        command_span_per_env = (commands.amax(dim=0) - commands.amin(dim=0)).amax(dim=1)
        measured_span_per_env = (measured.amax(dim=0) - measured.amin(dim=0)).amax(dim=1)
        command_span = float(command_span_per_env.max().item())
        measured_span = float(measured_span_per_env.max().item())
        if float(command_span_per_env.min().item()) < 0.05 or float(
            measured_span_per_env.min().item()
        ) < 0.03:
            raise AssertionError(
                "At least one random arm did not move enough: "
                f"command={command_span_per_env}, measured={measured_span_per_env}"
            )
        completed_segments = int(trajectory.completed_segment_count.min().item())
        if completed_segments < 1:
            raise AssertionError("No conditioned trajectory segment completed")
        selected_waypoint_count = int(torch.unique(trajectory.waypoint_indices).numel())
        if args_cli.num_envs > 1 and selected_waypoint_count < 2:
            raise AssertionError("Batched environments did not select independent waypoints")

        dt = unwrapped.physics_dt
        command_velocity = torch.diff(commands, dim=0) / dt
        command_acceleration = torch.diff(command_velocity, dim=0) / dt
        max_velocity = float(command_velocity.abs().max().item())
        max_acceleration = float(command_acceleration.abs().max().item())
        if max_velocity > GLUON_TRAJECTORY_MAX_VELOCITY_RAD_S * 1.01:
            raise AssertionError(f"Command velocity limit exceeded: {max_velocity}")
        if max_acceleration > GLUON_TRAJECTORY_MAX_ACCELERATION_RAD_S2 * 1.03:
            raise AssertionError(f"Command acceleration limit exceeded: {max_acceleration}")
        path_residual = line_set_residual(commands.reshape(-1, len(GLUON_JOINT_NAMES)))
        if path_residual > 2.0e-6:
            raise AssertionError(f"Command left conditioned hub paths: {path_residual}")
        max_tracking_error = float(torch.abs(measured - commands).max().item())
        if max_tracking_error > 0.20:
            raise AssertionError(f"GLUON tracking error too large: {max_tracking_error}")

        print(
            "TITA_GLUON_RANDOM_ARM_SMOKE,domain=VALIDATION_SIM,status=PASS,"
            f"steps={args_cli.steps},envs={args_cli.num_envs},"
            f"joints={robot.num_joints},actions=8,"
            f"waypoints={len(GLUON_CONDITIONED_WAYPOINTS_RAD)},"
            f"selected_waypoints={selected_waypoint_count},"
            f"min_completed_segments={completed_segments},"
            f"command_span_rad={command_span:.9g},measured_span_rad={measured_span:.9g},"
            f"max_command_velocity_rad_s={max_velocity:.9g},"
            f"max_command_acceleration_rad_s2={max_acceleration:.9g},"
            f"max_tracking_error_rad={max_tracking_error:.9g},"
            f"path_residual_rad={path_residual:.9g},"
            f"offline_sigma_min={minimum_sigma:.9g},"
            f"offline_joint_margin_deg={math.degrees(minimum_margin):.9g},"
            "group_dims="
            + ";".join(f"{name}:{value.shape[-1]}" for name, value in obs.items()),
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
