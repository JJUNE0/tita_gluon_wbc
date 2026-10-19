#!/usr/bin/env python3
"""Compare TITA+GLUON RMA Teacher checkpoints under one scripted full-arm protocol."""

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


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--checkpoints", type=Path, nargs="+", required=True)
parser.add_argument(
    "--task",
    default="Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-Play-v0-moo-ppo",
    help="Registered play task used for the common checkpoint protocol.",
)
parser.add_argument("--num-envs", type=int, default=256)
parser.add_argument("--steps", type=int, default=1000)
parser.add_argument("--seed", type=int, default=20260809)
parser.add_argument("--output", type=Path)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import gymnasium as gym  # noqa: E402
import torch  # noqa: E402

import ddt_lab.tasks  # noqa: F401, E402
from scripts.co_rl.core.runners import MOO_OnPolicyRunner  # noqa: E402
from scripts.co_rl.core.wrapper import CoRlVecEnvWrapper  # noqa: E402


TASK_ID = args_cli.task
GLUON_JOINT_NAMES = tuple(f"gluon_2L6_4L3_axis_joint_{index}" for index in range(1, 7))
TITA_JOINT_NAMES = (
    "joint_left_leg_1",
    "joint_right_leg_1",
    "joint_left_leg_2",
    "joint_right_leg_2",
    "joint_left_leg_3",
    "joint_right_leg_3",
    "joint_left_leg_4",
    "joint_right_leg_4",
)
SCENARIOS = (
    ("stand_low", 0.0, 0.0, 0.25),
    ("stand_mid", 0.0, 0.0, 0.35),
    ("stand_high", 0.0, 0.0, 0.45),
    ("forward_low", 0.75, 0.0, 0.25),
    ("forward_mid", 0.75, 0.0, 0.35),
    ("forward_high", 0.75, 0.0, 0.45),
    ("reverse_low", -0.50, 0.0, 0.25),
    ("reverse_mid", -0.50, 0.0, 0.35),
    ("reverse_high", -0.50, 0.0, 0.45),
    ("yaw_left_low", 0.0, 1.5, 0.25),
    ("yaw_left_mid", 0.0, 1.5, 0.35),
    ("yaw_left_high", 0.0, 1.5, 0.45),
    ("yaw_right_low", 0.0, -1.5, 0.25),
    ("yaw_right_mid", 0.0, -1.5, 0.35),
    ("yaw_right_high", 0.0, -1.5, 0.45),
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _privileged_obs(obs_dict: dict[str, torch.Tensor] | None, device: str) -> torch.Tensor | None:
    if not obs_dict:
        return None
    keys = sorted(key for key in obs_dict if key.startswith("priv_"))
    if keys:
        return torch.cat([obs_dict[key] for key in keys], dim=-1).to(device)
    if "privileged" in obs_dict:
        return obs_dict["privileged"].to(device)
    return None


def _quantile(values: list[torch.Tensor], probability: float) -> float:
    if not values:
        return math.nan
    flat = torch.cat(values)
    return float(torch.quantile(flat, probability).item())


def _scenario_means(
    square_sums: torch.Tensor, counts: torch.Tensor
) -> dict[str, float]:
    rms = torch.sqrt(square_sums / torch.clamp(counts, min=1.0))
    return {SCENARIOS[index][0]: float(rms[index].item()) for index in range(len(SCENARIOS))}


def _evaluate_checkpoint(
    *,
    checkpoint: Path,
    env: CoRlVecEnvWrapper,
    runner: MOO_OnPolicyRunner,
    seed: int,
    steps: int,
) -> dict[str, object]:
    checkpoint = checkpoint.resolve()
    if not checkpoint.is_file():
        raise FileNotFoundError(checkpoint)
    print(f"EVAL_CHECKPOINT_START,domain=VALIDATION_SIM,path={checkpoint}", flush=True)
    runner.load(str(checkpoint))
    policy = runner.get_inference_policy(device=env.unwrapped.device)

    torch.manual_seed(seed)
    obs, extras = env.reset()
    raw_env = env.unwrapped
    robot = raw_env.scene["robot"]
    command_term = raw_env.command_manager.get_term("base_velocity")
    command = command_term.vel_command_b
    scenario_values = torch.tensor(
        [(vx, 0.0, yaw, height) for _, vx, yaw, height in SCENARIOS],
        dtype=torch.float32,
        device=raw_env.device,
    )
    scenario_ids = torch.arange(raw_env.num_envs, device=raw_env.device) % len(SCENARIOS)
    assigned_commands = scenario_values[scenario_ids]
    command_term.is_heading_env[:] = False
    command_term.is_standing_env[:] = False

    gluon_joint_ids, gluon_joint_names = robot.find_joints(
        list(GLUON_JOINT_NAMES), preserve_order=True
    )
    tita_joint_ids, tita_joint_names = robot.find_joints(
        list(TITA_JOINT_NAMES), preserve_order=True
    )
    if tuple(gluon_joint_names) != GLUON_JOINT_NAMES:
        raise AssertionError(f"Unexpected GLUON joint order: {gluon_joint_names}")
    if tuple(tita_joint_names) != TITA_JOINT_NAMES:
        raise AssertionError(f"Unexpected TITA joint order: {tita_joint_names}")
    trajectory = raw_env.action_manager.get_term("gluon_joint_reference")
    if abs(trajectory.workspace_scale - 1.0) > 1.0e-7:
        raise AssertionError(f"Evaluation requires full GLUON workspace, got {trajectory.workspace_scale}")

    def force_commands() -> None:
        command[:] = assigned_commands
        command_term.time_left[:] = 1.0e6
        command_term.time_elapsed[:] = command_term.cfg.initial_phase_time + 1.0
        command_term.is_heading_env[:] = False
        command_term.is_standing_env[:] = False

    force_commands()
    obs, extras = env.get_observations()
    privileged_obs = _privileged_obs(extras.get("observations"), runner.device)

    scenario_counts = torch.zeros(len(SCENARIOS), device=raw_env.device)
    velocity_square_sums = torch.zeros_like(scenario_counts)
    yaw_square_sums = torch.zeros_like(scenario_counts)
    height_square_sums = torch.zeros_like(scenario_counts)
    contact_counts = torch.zeros_like(scenario_counts)
    timeout_counts = torch.zeros_like(scenario_counts)
    arm_abs_errors: list[torch.Tensor] = []
    tita_abs_torque_max: list[torch.Tensor] = []
    arm_abs_torque_max: list[torch.Tensor] = []
    tilt_values: list[torch.Tensor] = []
    action_rate_values: list[torch.Tensor] = []
    previous_action: torch.Tensor | None = None
    previous_segment_count = trajectory.completed_segment_count.clone()
    completed_segments = 0

    # Keep the simulator outside PyTorch's inference-tensor semantics.  The MOO
    # environment lazily allocates episode-statistic buffers during ``step``;
    # inference tensors cannot be updated by the next checkpoint's reset.
    # ``no_grad`` still disables policy autograd while allowing the same
    # environment instance to be reset and reused for all checkpoints.
    with torch.no_grad():
        for step in range(steps):
            force_commands()
            if privileged_obs is not None:
                try:
                    actions = policy(obs, privileged_info=privileged_obs)
                except TypeError:
                    actions = policy(obs)
            else:
                actions = policy(obs)
            if not bool(torch.isfinite(actions).all()):
                raise FloatingPointError(f"Non-finite policy action at evaluation step {step}")

            obs, _, dones, infos = env.step(actions)
            privileged_obs = _privileged_obs(infos.get("observations"), runner.device)

            velocity_error = torch.linalg.vector_norm(
                robot.data.root_link_lin_vel_b[:, :2] - assigned_commands[:, :2], dim=1
            )
            yaw_error = robot.data.root_link_ang_vel_b[:, 2] - assigned_commands[:, 2]
            height_error = robot.data.root_link_pos_w[:, 2] - assigned_commands[:, 3]
            ones = torch.ones(raw_env.num_envs, device=raw_env.device)
            scenario_counts.scatter_add_(0, scenario_ids, ones)
            velocity_square_sums.scatter_add_(0, scenario_ids, velocity_error.square())
            yaw_square_sums.scatter_add_(0, scenario_ids, yaw_error.square())
            height_square_sums.scatter_add_(0, scenario_ids, height_error.square())

            timeouts = infos.get("time_outs", torch.zeros_like(dones, dtype=torch.bool)).bool()
            contacts = dones.bool() & ~timeouts
            contact_counts.scatter_add_(0, scenario_ids, contacts.float())
            timeout_counts.scatter_add_(0, scenario_ids, timeouts.float())

            arm_error = torch.abs(
                robot.data.joint_pos[:, gluon_joint_ids] - trajectory.processed_actions
            )
            arm_abs_errors.append(arm_error.flatten().cpu())
            tita_abs_torque_max.append(
                torch.abs(robot.data.applied_torque[:, tita_joint_ids]).amax(dim=1).cpu()
            )
            arm_abs_torque_max.append(
                torch.abs(robot.data.applied_torque[:, gluon_joint_ids]).amax(dim=1).cpu()
            )
            tilt_values.append(
                torch.linalg.vector_norm(robot.data.projected_gravity_b[:, :2], dim=1).cpu()
            )
            if previous_action is not None:
                action_rate_values.append(
                    torch.linalg.vector_norm(actions - previous_action, dim=1).cpu()
                )
            previous_action = actions.clone()

            current_segment_count = trajectory.completed_segment_count
            completed_segments += int(
                torch.clamp(current_segment_count - previous_segment_count, min=0).sum().item()
            )
            previous_segment_count = current_segment_count.clone()

            if not bool(torch.isfinite(robot.data.joint_pos).all()):
                raise FloatingPointError(f"Non-finite robot state at evaluation step {step}")

    total_contacts = int(contact_counts.sum().item())
    total_timeouts = int(timeout_counts.sum().item())
    total_episodes = total_contacts + total_timeouts
    timeout_fraction = total_timeouts / total_episodes if total_episodes else 0.0
    result = {
        "checkpoint": str(checkpoint),
        "checkpoint_sha256": _sha256(checkpoint),
        "seed": seed,
        "num_envs": raw_env.num_envs,
        "steps": steps,
        "step_dt_s": float(raw_env.step_dt),
        "simulated_env_seconds": float(raw_env.num_envs * steps * raw_env.step_dt),
        "workspace_scale": float(trajectory.workspace_scale),
        "episodes": total_episodes,
        "timeouts": total_timeouts,
        "base_contacts": total_contacts,
        "timeout_fraction": timeout_fraction,
        "completed_arm_segments": completed_segments,
        "velocity_xy_rmse_m_s": float(
            torch.sqrt(velocity_square_sums.sum() / scenario_counts.sum()).item()
        ),
        "yaw_rate_rmse_rad_s": float(
            torch.sqrt(yaw_square_sums.sum() / scenario_counts.sum()).item()
        ),
        "height_rmse_m": float(
            torch.sqrt(height_square_sums.sum() / scenario_counts.sum()).item()
        ),
        "arm_joint_tracking_abs_p50_rad": _quantile(arm_abs_errors, 0.50),
        "arm_joint_tracking_abs_p95_rad": _quantile(arm_abs_errors, 0.95),
        "arm_joint_tracking_abs_p99_rad": _quantile(arm_abs_errors, 0.99),
        "tita_abs_torque_envmax_p99_nm": _quantile(tita_abs_torque_max, 0.99),
        "arm_abs_torque_envmax_p99_nm": _quantile(arm_abs_torque_max, 0.99),
        "tilt_norm_p99": _quantile(tilt_values, 0.99),
        "action_delta_l2_p99": _quantile(action_rate_values, 0.99),
        "scenario_velocity_xy_rmse_m_s": _scenario_means(
            velocity_square_sums, scenario_counts
        ),
        "scenario_yaw_rate_rmse_rad_s": _scenario_means(yaw_square_sums, scenario_counts),
        "scenario_height_rmse_m": _scenario_means(height_square_sums, scenario_counts),
        "scenario_base_contacts": {
            SCENARIOS[index][0]: int(contact_counts[index].item())
            for index in range(len(SCENARIOS))
        },
    }
    print(
        "TITA_GLUON_TEACHER_EVAL,domain=VALIDATION_SIM,status=PASS,"
        f"checkpoint={checkpoint.name},timeout_fraction={timeout_fraction:.6g},"
        f"base_contacts={total_contacts},velocity_xy_rmse_m_s={result['velocity_xy_rmse_m_s']:.6g},"
        f"yaw_rate_rmse_rad_s={result['yaw_rate_rmse_rad_s']:.6g},"
        f"height_rmse_m={result['height_rmse_m']:.6g},"
        f"arm_tracking_p99_rad={result['arm_joint_tracking_abs_p99_rad']:.6g}",
        flush=True,
    )
    return result


def main() -> int:
    if args_cli.num_envs <= 0 or args_cli.steps <= 0:
        raise ValueError("--num-envs and --steps must be positive")
    spec = gym.spec(TASK_ID)
    env_cfg = spec.kwargs["env_cfg_entry_point"]()
    env_cfg.seed = args_cli.seed
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.actions.gluon_joint_reference.debug_vis = False
    env_cfg.commands.base_velocity.debug_vis = False
    env_cfg.commands.base_velocity.ranges.pos_z = (0.25, 0.45)
    env_cfg.curriculum.widen_height_range = None
    agent_cfg = spec.kwargs["co_rl_cfg_entry_point"]()

    gym_env = gym.make(TASK_ID, cfg=env_cfg)
    env = CoRlVecEnvWrapper(gym_env, agent_cfg)
    runner = MOO_OnPolicyRunner(
        env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device
    )
    try:
        results = [
            _evaluate_checkpoint(
                checkpoint=checkpoint,
                env=env,
                runner=runner,
                seed=args_cli.seed,
                steps=args_cli.steps,
            )
            for checkpoint in args_cli.checkpoints
        ]
        payload = {
            "execution_domain": "VALIDATION_SIM",
            "evidence_status": "PASS",
            "task": TASK_ID,
            "scenarios": [
                {"name": name, "vx_m_s": vx, "yaw_rad_s": yaw, "height_m": height}
                for name, vx, yaw, height in SCENARIOS
            ],
            "results": results,
        }
        encoded = json.dumps(payload, indent=2, sort_keys=True)
        if args_cli.output is not None:
            args_cli.output.parent.mkdir(parents=True, exist_ok=True)
            args_cli.output.write_text(encoded + "\n", encoding="utf-8")
            print(f"EVAL_OUTPUT={args_cli.output.resolve()}", flush=True)
        else:
            print(encoded, flush=True)
        return 0
    finally:
        env.close()


if __name__ == "__main__":
    try:
        status = main()
    except Exception:
        traceback.print_exc()
        raise
    finally:
        simulation_app.close()
    raise SystemExit(status)
