#!/usr/bin/env python3
"""Compare arm-free and TITA+GLUON RMA Teachers under fixed zero-velocity commands.

Execution domain: VALIDATION_SIM.  This diagnostic never communicates with or
commands physical hardware.
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


DEFAULT_PARENT_CHECKPOINT = Path(
    "/home/cocel/Desktop/Research/isaaclab_add_reward_autotuning/logs/co_rl/"
    "Tita_Flat_Stand_Drive-v3-mooppo/mooppo/2026-08-08_16-12-19/model_9999.pt"
)
DEFAULT_GLUON_CHECKPOINT = (
    REPO_ROOT
    / "lab"
    / "logs"
    / "co_rl"
    / "Tita_Gluon_CurriculumArm_RMATeacher-v0-mooppo"
    / "mooppo"
    / "2026-08-09_17-15-39_massless_sensor_rma_teacher_v2"
    / "model_9000.pt"
)
DEFAULT_OUTPUT = REPO_ROOT / "test" / "eval_logs" / "tita_gluon_zero_command_stance.json"


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--parent-checkpoint", type=Path, default=DEFAULT_PARENT_CHECKPOINT)
parser.add_argument("--gluon-checkpoint", type=Path, default=DEFAULT_GLUON_CHECKPOINT)
parser.add_argument(
    "--case",
    choices=("parent", "gluon_fixed", "gluon_moving"),
    required=True,
    help="Run one scene per process; Isaac scene teardown/recreation is intentionally avoided.",
)
parser.add_argument("--num-envs", type=int, default=64)
parser.add_argument("--steps", type=int, default=600)
parser.add_argument("--settle-steps", type=int, default=200)
parser.add_argument("--heights", type=float, nargs="+", default=(0.35, 0.39))
parser.add_argument("--seed", type=int, default=20260810)
parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import gymnasium as gym  # noqa: E402
import torch  # noqa: E402

import ddt_lab.tasks  # noqa: F401, E402
from scripts.co_rl.core.runners import MOO_OnPolicyRunner  # noqa: E402
from scripts.co_rl.core.wrapper import CoRlVecEnvWrapper  # noqa: E402


PARENT_TASK_ID = "Isaac-Velocity-Flat-Tita-RMATeacher-TargetHeight-v3-moo-ppo"
GLUON_TASK_ID = (
    "Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-RMATeacher-TargetHeight-v0-moo-ppo"
)
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
GLUON_JOINT_NAMES = tuple(f"gluon_2L6_4L3_axis_joint_{index}" for index in range(1, 7))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _privileged_obs(
    obs_dict: dict[str, torch.Tensor] | None, device: str
) -> torch.Tensor | None:
    if not obs_dict:
        return None
    keys = sorted(key for key in obs_dict if key.startswith("priv_"))
    if keys:
        return torch.cat([obs_dict[key] for key in keys], dim=-1).to(device)
    if "privileged" in obs_dict:
        return obs_dict["privileged"].to(device)
    return None


def _summary(values: list[torch.Tensor]) -> dict[str, float]:
    if not values:
        return {"mean": math.nan, "p50": math.nan, "p95": math.nan, "p99": math.nan}
    flat = torch.cat(values).float()
    return {
        "mean": float(flat.mean().item()),
        "p50": float(torch.quantile(flat, 0.50).item()),
        "p95": float(torch.quantile(flat, 0.95).item()),
        "p99": float(torch.quantile(flat, 0.99).item()),
    }


def _scenario_summary(
    values: list[torch.Tensor], scenario_ids: torch.Tensor, heights: tuple[float, ...]
) -> dict[str, dict[str, float]]:
    if not values:
        return {}
    stacked = torch.cat(values).reshape(-1, len(scenario_ids))
    result: dict[str, dict[str, float]] = {}
    for scenario_index, height in enumerate(heights):
        selected = stacked[:, scenario_ids.cpu() == scenario_index].reshape(-1)
        result[f"height_{height:.3f}_m"] = {
            "mean": float(selected.mean().item()),
            "p50": float(torch.quantile(selected, 0.50).item()),
            "p95": float(torch.quantile(selected, 0.95).item()),
            "p99": float(torch.quantile(selected, 0.99).item()),
        }
    return result


def _make_cfg(task_id: str, *, num_envs: int, seed: int, workspace_scale: float | None):
    spec = gym.spec(task_id)
    env_cfg = spec.kwargs["env_cfg_entry_point"]()
    env_cfg.seed = seed
    env_cfg.scene.num_envs = num_envs
    env_cfg.observations.stack_policy.enable_corruption = False
    env_cfg.commands.base_velocity.debug_vis = False
    env_cfg.commands.base_velocity.ranges.pos_z = (
        min(args_cli.heights),
        max(args_cli.heights),
    )
    env_cfg.curriculum.widen_height_range = None
    env_cfg.events.push_robot = None
    env_cfg.domain = None
    if workspace_scale is not None:
        env_cfg.actions.gluon_joint_reference.initial_workspace_scale = workspace_scale
        env_cfg.actions.gluon_joint_reference.debug_vis = False
        env_cfg.curriculum.widen_gluon_workspace = None
    return spec, env_cfg


def _evaluate_case(
    *,
    name: str,
    task_id: str,
    checkpoint: Path,
    workspace_scale: float | None,
) -> dict[str, object]:
    checkpoint = checkpoint.resolve()
    if not checkpoint.is_file():
        raise FileNotFoundError(checkpoint)
    print(
        f"ZERO_COMMAND_CASE_START,domain=VALIDATION_SIM,name={name},checkpoint={checkpoint}",
        flush=True,
    )
    spec, env_cfg = _make_cfg(
        task_id,
        num_envs=args_cli.num_envs,
        seed=args_cli.seed,
        workspace_scale=workspace_scale,
    )
    agent_cfg = spec.kwargs["co_rl_cfg_entry_point"]()
    gym_env = gym.make(task_id, cfg=env_cfg)
    env = CoRlVecEnvWrapper(gym_env, agent_cfg)
    runner = MOO_OnPolicyRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    try:
        runner.load(str(checkpoint))
        policy = runner.get_inference_policy(device=env.unwrapped.device)
        torch.manual_seed(args_cli.seed)
        obs, extras = env.reset()
        raw_env = env.unwrapped
        robot = raw_env.scene["robot"]
        command_term = raw_env.command_manager.get_term("base_velocity")
        command = command_term.vel_command_b
        heights = tuple(float(value) for value in args_cli.heights)
        scenario_ids = torch.arange(raw_env.num_envs, device=raw_env.device) % len(heights)
        assigned_heights = torch.tensor(heights, device=raw_env.device)[scenario_ids]
        assigned_commands = torch.zeros((raw_env.num_envs, 4), device=raw_env.device)
        assigned_commands[:, 3] = assigned_heights

        tita_joint_ids, tita_joint_names = robot.find_joints(
            list(TITA_JOINT_NAMES), preserve_order=True
        )
        if tuple(tita_joint_names) != TITA_JOINT_NAMES:
            raise AssertionError(f"Unexpected TITA joint order: {tita_joint_names}")
        wheel_body_ids, wheel_body_names = robot.find_bodies(
            ["left_leg_4", "right_leg_4"], preserve_order=True
        )
        if tuple(wheel_body_names) != ("left_leg_4", "right_leg_4"):
            raise AssertionError(f"Unexpected wheel body order: {wheel_body_names}")
        gluon_joint_ids: list[int] | None = None
        trajectory = None
        if workspace_scale is not None:
            gluon_joint_ids, gluon_joint_names = robot.find_joints(
                list(GLUON_JOINT_NAMES), preserve_order=True
            )
            if tuple(gluon_joint_names) != GLUON_JOINT_NAMES:
                raise AssertionError(f"Unexpected GLUON joint order: {gluon_joint_names}")
            trajectory = raw_env.action_manager.get_term("gluon_joint_reference")
            if abs(float(trajectory.workspace_scale) - workspace_scale) > 1.0e-7:
                raise AssertionError(
                    f"Requested workspace scale {workspace_scale}, got {trajectory.workspace_scale}"
                )

        def force_commands() -> None:
            command[:] = assigned_commands
            command_term.time_left[:] = 1.0e6
            # Explicitly exercise the reset/init-phase command path.  The
            # current command implementation masks only velocity and keeps the
            # assigned height visible to the policy and reward.
            command_term.time_elapsed[:] = 0.0
            command_term.is_heading_env[:] = False
            command_term.is_standing_env[:] = False

        force_commands()
        obs, extras = env.get_observations()
        privileged_obs = _privileged_obs(extras.get("observations"), runner.device)

        metrics: dict[str, list[torch.Tensor]] = {
            "hip_abs_sum_rad": [],
            "hip_pair_separation_rad": [],
            "left_hip_rad": [],
            "right_hip_rad": [],
            "shoulder_abs_sum_rad": [],
            "leg_abs_sum_rad": [],
            "wheel_horizontal_separation_m": [],
            "base_height_abs_error_m": [],
            "base_xy_speed_m_s": [],
            "yaw_rate_abs_rad_s": [],
            "tilt_norm": [],
            "action_l2": [],
            "tita_torque_envmax_nm": [],
        }
        arm_tracking_errors: list[torch.Tensor] = []
        base_contacts = 0

        with torch.no_grad():
            for step in range(args_cli.steps):
                force_commands()
                if privileged_obs is not None:
                    try:
                        actions = policy(obs, privileged_info=privileged_obs)
                    except TypeError:
                        actions = policy(obs)
                else:
                    actions = policy(obs)
                if not bool(torch.isfinite(actions).all()):
                    raise FloatingPointError(f"Non-finite policy action at step {step}")

                obs, _, dones, infos = env.step(actions)
                privileged_obs = _privileged_obs(infos.get("observations"), runner.device)
                timeouts = infos.get("time_outs", torch.zeros_like(dones, dtype=torch.bool)).bool()
                base_contacts += int((dones.bool() & ~timeouts).sum().item())
                if step < args_cli.settle_steps:
                    continue

                q = robot.data.joint_pos[:, tita_joint_ids]
                hip_left = q[:, 0]
                hip_right = q[:, 1]
                metrics["hip_abs_sum_rad"].append(
                    (torch.abs(hip_left) + torch.abs(hip_right)).cpu()
                )
                metrics["hip_pair_separation_rad"].append(
                    torch.abs(hip_left - hip_right).cpu()
                )
                metrics["left_hip_rad"].append(hip_left.cpu())
                metrics["right_hip_rad"].append(hip_right.cpu())
                metrics["shoulder_abs_sum_rad"].append(
                    (torch.abs(q[:, 2]) + torch.abs(q[:, 3])).cpu()
                )
                metrics["leg_abs_sum_rad"].append(
                    (torch.abs(q[:, 4]) + torch.abs(q[:, 5])).cpu()
                )
                wheel_delta_w = (
                    robot.data.body_pos_w[:, wheel_body_ids[0], :2]
                    - robot.data.body_pos_w[:, wheel_body_ids[1], :2]
                )
                metrics["wheel_horizontal_separation_m"].append(
                    torch.linalg.vector_norm(wheel_delta_w, dim=1).cpu()
                )
                metrics["base_height_abs_error_m"].append(
                    torch.abs(robot.data.root_link_pos_w[:, 2] - assigned_heights).cpu()
                )
                metrics["base_xy_speed_m_s"].append(
                    torch.linalg.vector_norm(robot.data.root_link_lin_vel_b[:, :2], dim=1).cpu()
                )
                metrics["yaw_rate_abs_rad_s"].append(
                    torch.abs(robot.data.root_link_ang_vel_b[:, 2]).cpu()
                )
                metrics["tilt_norm"].append(
                    torch.linalg.vector_norm(robot.data.projected_gravity_b[:, :2], dim=1).cpu()
                )
                metrics["action_l2"].append(torch.linalg.vector_norm(actions, dim=1).cpu())
                metrics["tita_torque_envmax_nm"].append(
                    torch.abs(robot.data.applied_torque[:, tita_joint_ids]).amax(dim=1).cpu()
                )
                if trajectory is not None and gluon_joint_ids is not None:
                    arm_tracking_errors.append(
                        torch.abs(
                            robot.data.joint_pos[:, gluon_joint_ids]
                            - trajectory.processed_actions
                        ).amax(dim=1).cpu()
                    )

        metric_summary = {key: _summary(values) for key, values in metrics.items()}
        metric_by_height = {
            key: _scenario_summary(values, scenario_ids, heights)
            for key, values in metrics.items()
        }
        masses = robot.root_physx_view.get_masses()
        total_mass_kg = float(masses[0].sum().item())
        result = {
            "name": name,
            "task": task_id,
            "checkpoint": str(checkpoint),
            "checkpoint_sha256": _sha256(checkpoint),
            "num_envs": raw_env.num_envs,
            "steps": args_cli.steps,
            "settle_steps": args_cli.settle_steps,
            "step_dt_s": float(raw_env.step_dt),
            "heights_m": list(heights),
            "command_velocity": [0.0, 0.0, 0.0],
            "forced_initial_phase": True,
            "workspace_scale": workspace_scale,
            "total_runtime_mass_kg": total_mass_kg,
            "base_contacts": base_contacts,
            "metrics": metric_summary,
            "metrics_by_height": metric_by_height,
            "arm_joint_tracking_envmax_rad": _summary(arm_tracking_errors),
        }
        print(
            "ZERO_COMMAND_CASE,domain=VALIDATION_SIM,status=PASS,"
            f"name={name},mass_kg={total_mass_kg:.6g},contacts={base_contacts},"
            f"hip_abs_sum_mean_rad={metric_summary['hip_abs_sum_rad']['mean']:.6g},"
            f"hip_pair_separation_mean_rad={metric_summary['hip_pair_separation_rad']['mean']:.6g},"
            f"height_error_mean_m={metric_summary['base_height_abs_error_m']['mean']:.6g},"
            f"xy_speed_mean_m_s={metric_summary['base_xy_speed_m_s']['mean']:.6g}",
            flush=True,
        )
        return result
    finally:
        env.close()


def main() -> int:
    if args_cli.num_envs <= 0 or args_cli.steps <= 0:
        raise ValueError("--num-envs and --steps must be positive")
    if args_cli.settle_steps < 0 or args_cli.settle_steps >= args_cli.steps:
        raise ValueError("--settle-steps must satisfy 0 <= settle-steps < steps")
    if not args_cli.heights or not all(math.isfinite(value) and value > 0.0 for value in args_cli.heights):
        raise ValueError("--heights must contain finite positive values")

    cases = {
        "parent": {
            "name": "tita_parent",
            "task_id": PARENT_TASK_ID,
            "checkpoint": args_cli.parent_checkpoint,
            "workspace_scale": None,
        },
        "gluon_fixed": {
            "name": "tita_gluon_fixed_work",
            "task_id": GLUON_TASK_ID,
            "checkpoint": args_cli.gluon_checkpoint,
            "workspace_scale": 0.0,
        },
        "gluon_moving": {
            "name": "tita_gluon_moving_arm",
            "task_id": GLUON_TASK_ID,
            "checkpoint": args_cli.gluon_checkpoint,
            "workspace_scale": 1.0,
        },
    }
    results = [_evaluate_case(**cases[args_cli.case])]
    payload = {
        "execution_domain": "VALIDATION_SIM",
        "evidence_status": "PASS",
        "seed": args_cli.seed,
        "results": results,
    }
    args_cli.output.parent.mkdir(parents=True, exist_ok=True)
    args_cli.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"ZERO_COMMAND_OUTPUT={args_cli.output.resolve()}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        status = main()
    except Exception:
        traceback.print_exc()
        raise
    finally:
        simulation_app.close()
    raise SystemExit(status)
