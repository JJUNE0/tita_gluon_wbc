#!/usr/bin/env python3
from __future__ import annotations

"""Dump the initial Isaac Lab NP3O policy input/output trace for TITA.

Run this inside the Isaac Lab environment, not the ROS2 Jazzy MuJoCo venv.
The script mirrors scripts/np3o/play.py and stops before stepping physics.
"""

import argparse
import importlib
import json
import os
from pathlib import Path

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Dump initial TITA NP3O policy trace.")
parser.add_argument("--task", type=str, required=True, help="Gym task ID.")
parser.add_argument("--num_envs", type=int, default=1, help="Use 1 for deterministic trace inspection.")
parser.add_argument("--checkpoint", type=str, default=None, help="Absolute checkpoint path.")
parser.add_argument("--load_run", type=str, default=".*", help="Run dir regex when --checkpoint is omitted.")
parser.add_argument("--load_checkpoint", type=str, default=r"model_.*\.pt", help="Checkpoint filename regex.")
parser.add_argument(
    "--output-prefix",
    type=str,
    default=None,
    help="Output path prefix. Writes <prefix>.npz and <prefix>.json.",
)
parser.add_argument("--zero_command", action="store_true", help="Force base velocity command ranges to zero.")
parser.add_argument("--disable_randomization", action="store_true", help="Disable/bypass reset and domain randomization where practical.")
parser.add_argument("--force_default_joint_pose", action="store_true", help="Force robot root velocity and joints to default pose after reset.")
parser.add_argument("--dump_steps", type=int, default=1, help="Number of policy steps to dump.")
AppLauncher.add_app_launcher_args(parser)
args_cli, _ = parser.parse_known_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import ddt_lab.tasks  # noqa: E402,F401
import gymnasium as gym  # noqa: E402
import numpy as np  # noqa: E402
import torch  # noqa: E402
from isaaclab_tasks.utils import get_checkpoint_path  # noqa: E402

from ddt_lab.algorithms.np3o import IsaacLabNP3OWrapper, OnConstraintPolicyRunner  # noqa: E402


TERM_SLICES = {
    "base_ang_vel": slice(0, 3),
    "projected_gravity": slice(3, 6),
    "command": slice(6, 9),
    "joint_pos_error": slice(9, 17),
    "joint_vel": slice(17, 25),
    "last_action": slice(25, 33),
}
JOINT_NAMES = [
    "joint_left_leg_1",
    "joint_left_leg_2",
    "joint_left_leg_3",
    "joint_left_leg_4",
    "joint_right_leg_1",
    "joint_right_leg_2",
    "joint_right_leg_3",
    "joint_right_leg_4",
]


def _default_output_prefix() -> str:
    controlled = (
        args_cli.zero_command
        or args_cli.disable_randomization
        or args_cli.force_default_joint_pose
        or args_cli.dump_steps != 1
    )
    name = "isaac_policy_trace_controlled" if controlled else "isaac_policy_trace_initial"
    return f"/home/cocel/Desktop/Research/DDT_Lab/deploy/tita/{name}"


def _resolve_runner_cfg(entry_point: str) -> dict:
    module_name, attr = entry_point.split(":")
    obj = getattr(importlib.import_module(module_name), attr)
    cfg = obj() if callable(obj) else obj
    if not isinstance(cfg, dict):
        raise TypeError(f"NP3O cfg entry point '{entry_point}' must return a dict")
    return cfg


def _to_jsonable(value):
    if isinstance(value, np.ndarray):
        return value.astype(float).tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


def _save_trace(prefix: Path, trace: dict[str, np.ndarray | str]) -> None:
    prefix.parent.mkdir(parents=True, exist_ok=True)
    npz_path = prefix.with_suffix(".npz")
    json_path = prefix.with_suffix(".json")
    np.savez(npz_path, **{k: v for k, v in trace.items() if isinstance(v, np.ndarray)})
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({k: _to_jsonable(v) for k, v in trace.items()}, f, indent=2)
    print("saved_npz:", npz_path)
    print("saved_json:", json_path)


def _configure_controlled_env(env_cfg) -> dict[str, str]:
    status: dict[str, str] = {}
    if args_cli.zero_command:
        ranges = env_cfg.commands.base_velocity.ranges
        ranges.lin_vel_x = (0.0, 0.0)
        ranges.lin_vel_y = (0.0, 0.0)
        ranges.ang_vel_z = (0.0, 0.0)
        if hasattr(ranges, "heading"):
            ranges.heading = (0.0, 0.0)
        if hasattr(env_cfg.commands.base_velocity, "heading_command"):
            env_cfg.commands.base_velocity.heading_command = False
        status["zero_command"] = "command ranges forced to zero before env creation"
    else:
        status["zero_command"] = "not requested"

    if args_cli.disable_randomization:
        for name in [
            "physics_material",
            "add_base_mass",
            "add_base_inertia",
            "add_base_com",
            "base_external_force_torque",
            "randomize_actuator_gains",
            "push_robot",
        ]:
            if hasattr(env_cfg.events, name):
                setattr(env_cfg.events, name, None)
        if getattr(env_cfg.events, "reset_base", None) is not None:
            env_cfg.events.reset_base.params = {
                "pose_range": {"x": (0.0, 0.0), "y": (0.0, 0.0), "yaw": (0.0, 0.0)},
                "velocity_range": {
                    "x": (0.0, 0.0),
                    "y": (0.0, 0.0),
                    "z": (0.0, 0.0),
                    "roll": (0.0, 0.0),
                    "pitch": (0.0, 0.0),
                    "yaw": (0.0, 0.0),
                },
            }
        if getattr(env_cfg.events, "reset_robot_joints", None) is not None:
            env_cfg.events.reset_robot_joints.params = {
                "position_range": (1.0, 1.0),
                "velocity_range": (0.0, 0.0),
            }
        status["disable_randomization"] = "domain/reset randomization terms disabled or made deterministic"
    else:
        status["disable_randomization"] = "not requested"
    return status


def _force_default_state(env) -> str:
    if not args_cli.force_default_joint_pose:
        return "not requested"
    try:
        robot = env.unwrapped.scene["robot"]
        env_ids = torch.tensor([0], device=env.unwrapped.device, dtype=torch.long)
        root_state = robot.data.default_root_state[env_ids].clone()
        root_state[:, :3] += env.unwrapped.scene.env_origins[env_ids]
        root_state[:, 7:13] = 0.0
        robot.write_root_pose_to_sim(root_state[:, :7], env_ids=env_ids)
        robot.write_root_velocity_to_sim(root_state[:, 7:13], env_ids=env_ids)

        joint_pos = robot.data.default_joint_pos[env_ids].clone()
        joint_vel = torch.zeros_like(joint_pos)
        robot.write_joint_state_to_sim(joint_pos, joint_vel, env_ids=env_ids)
        robot.set_joint_position_target(joint_pos, env_ids=env_ids)
        robot.set_joint_velocity_target(joint_vel, env_ids=env_ids)
        env.unwrapped.action_manager.reset(env_ids=env_ids)
        env.unwrapped.sim.forward()
        env.unwrapped.scene.update(dt=env.unwrapped.physics_dt)
        return "forced default root pose, zero root velocity, default joint pose, zero joint velocity"
    except Exception as exc:
        return f"failed: {exc}"


def _safe_robot_terms(env, obs_current: np.ndarray) -> dict[str, np.ndarray | str]:
    """Best-effort raw robot terms; obs slices remain the authoritative comparison."""
    result = {
        "joint_pos": np.full(8, np.nan, dtype=np.float32),
        "default_joint_pos": np.full(8, np.nan, dtype=np.float32),
        "root_state": np.full(13, np.nan, dtype=np.float32),
    }
    try:
        robot = env.unwrapped.scene["robot"]
        joint_ids, _ = robot.find_joints(JOINT_NAMES, preserve_order=True)
        result["joint_pos"] = robot.data.joint_pos[0, joint_ids].detach().cpu().numpy().astype(np.float32)
        default = getattr(robot.data, "default_joint_pos", None)
        if default is not None:
            result["default_joint_pos"] = default[0, joint_ids].detach().cpu().numpy().astype(np.float32)
        result["root_state"] = robot.data.root_state_w[0].detach().cpu().numpy().astype(np.float32)
    except Exception as exc:
        result["robot_term_warning"] = str(exc)

    result["joint_pos_error"] = obs_current[TERM_SLICES["joint_pos_error"]].astype(np.float32)
    result["joint_vel"] = obs_current[TERM_SLICES["joint_vel"]].astype(np.float32)
    return result


def _action_targets(env, action: torch.Tensor, default_joint_pos: np.ndarray) -> dict[str, np.ndarray | str]:
    raw = action[0].detach().cpu().numpy().astype(np.float32)
    used = np.clip(raw, -100.0, 100.0).astype(np.float32)
    scales = np.asarray([0.25, 0.25, 0.25, 5.0, 0.25, 0.25, 0.25, 5.0], dtype=np.float32)
    scaled = used * scales
    target_leg_pos = np.full(8, np.nan, dtype=np.float32)
    target_wheel_vel = np.full(8, np.nan, dtype=np.float32)
    leg_indices = [0, 1, 2, 4, 5, 6]
    wheel_indices = [3, 7]
    target_leg_pos[leg_indices] = default_joint_pos[leg_indices] + scaled[leg_indices]
    target_wheel_vel[wheel_indices] = scaled[wheel_indices]
    return {
        "target_source": "computed_from_action_cfg",
        "applied_raw_action": raw.copy(),
        "processed_action": scaled.copy(),
        "clipped_action": used.copy(),
        "scaled_action": scaled.copy(),
        "target_leg_pos": target_leg_pos,
        "target_wheel_vel": target_wheel_vel,
    }


def _trace_step(env, obs: torch.Tensor, action: torch.Tensor, step_idx: int) -> dict[str, np.ndarray]:
    obs_history = obs[0].detach().cpu().numpy().astype(np.float32)
    obs_current = obs_history[-1].copy()
    policy_action = action[0].detach().cpu().numpy().astype(np.float32)
    terms = _safe_robot_terms(env, obs_current)
    targets = _action_targets(env, action, terms["default_joint_pos"])
    return {
        "step": np.asarray(step_idx, dtype=np.int32),
        "step_index": np.asarray(int(env.unwrapped.common_step_counter), dtype=np.int32),
        "sim_time": np.asarray(float(env.unwrapped.common_step_counter) * float(env.unwrapped.step_dt), dtype=np.float32),
        "physics_dt": np.asarray(float(env.unwrapped.physics_dt), dtype=np.float32),
        "decimation": np.asarray(int(env.unwrapped.cfg.decimation), dtype=np.int32),
        "policy_dt": np.asarray(float(env.unwrapped.step_dt), dtype=np.float32),
        "obs_current": obs_current,
        "obs_history": obs_history,
        "policy_action_raw": policy_action,
        "policy_action_used": targets["clipped_action"],
        "policy_action_clipped": targets["clipped_action"],
        "policy_action_scaled_or_env_action": targets["processed_action"],
        "command": obs_current[TERM_SLICES["command"]].astype(np.float32),
        "projected_gravity": obs_current[TERM_SLICES["projected_gravity"]].astype(np.float32),
        "base_ang_vel": obs_current[TERM_SLICES["base_ang_vel"]].astype(np.float32),
        "joint_pos": terms["joint_pos"],
        "default_joint_pos": terms["default_joint_pos"],
        "joint_pos_error": terms["joint_pos_error"],
        "joint_vel": terms["joint_vel"],
        "last_action": obs_current[TERM_SLICES["last_action"]].astype(np.float32),
        "root_state": terms["root_state"],
        "clipped_action": targets["clipped_action"],
        "scaled_action": targets["scaled_action"],
        "target_leg_pos": targets["target_leg_pos"],
        "target_wheel_vel": targets["target_wheel_vel"],
        "target_source": np.asarray([targets["target_source"]]),
    }


def main() -> None:
    spec = gym.spec(args_cli.task)
    runner_cfg = _resolve_runner_cfg(spec.kwargs["np3o_cfg_entry_point"])
    env_cfg_entry = spec.kwargs["env_cfg_entry_point"]
    env_cfg = env_cfg_entry() if callable(env_cfg_entry) else env_cfg_entry
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device
    control_status = _configure_controlled_env(env_cfg)

    env_raw = gym.make(args_cli.task, cfg=env_cfg)
    env = IsaacLabNP3OWrapper(env_raw, device=args_cli.device or "cuda:0")
    runner = OnConstraintPolicyRunner(env, runner_cfg, log_dir=None, device=args_cli.device or "cuda:0")

    if args_cli.checkpoint is not None:
        ckpt = args_cli.checkpoint
    else:
        log_root = os.path.abspath(os.path.join("logs", "np3o", runner_cfg["runner"]["experiment_name"]))
        ckpt = get_checkpoint_path(log_root, args_cli.load_run, args_cli.load_checkpoint)
    print("[INFO] loading checkpoint:", ckpt)
    runner.load(ckpt, load_optimizer=False)
    force_status = _force_default_state(env)

    policy = runner.get_inference_policy(args_cli.device or "cuda:0")
    obs = env.get_observations()
    if obs.dim() != 3:
        raise RuntimeError(f"Expected policy obs (B,T,D), got {tuple(obs.shape)}")

    step_traces: list[dict[str, np.ndarray]] = []
    steps = max(int(args_cli.dump_steps), 1)
    for step_idx in range(steps):
        with torch.inference_mode():
            action = policy(obs)
        step_traces.append(_trace_step(env, obs, action, step_idx))
        if step_idx < steps - 1:
            obs, _, _, _, _, _ = env.step(action)

    first = step_traces[0]
    trace = {
        "source": "isaac",
        "checkpoint": str(ckpt),
        "zero_command_status": control_status["zero_command"],
        "disable_randomization_status": control_status["disable_randomization"],
        "force_default_joint_pose_status": force_status,
        "step_index": first["step_index"],
        "sim_time": first["sim_time"],
        "physics_dt": first["physics_dt"],
        "decimation": first["decimation"],
        "policy_dt": first["policy_dt"],
        "obs_current": first["obs_current"],
        "obs_history": first["obs_history"],
        "policy_action_raw": first["policy_action_raw"],
        "policy_action_used": first["policy_action_used"],
        "policy_action_clipped": first["policy_action_clipped"],
        "policy_action_scaled_or_env_action": first["policy_action_scaled_or_env_action"],
        "command": first["command"],
        "projected_gravity": first["projected_gravity"],
        "base_ang_vel": first["base_ang_vel"],
        "joint_pos": first["joint_pos"],
        "default_joint_pos": first["default_joint_pos"],
        "joint_pos_error": first["joint_pos_error"],
        "joint_vel": first["joint_vel"],
        "last_action": first["last_action"],
        "root_state": first["root_state"],
        "clipped_action": first["clipped_action"],
        "scaled_action": first["scaled_action"],
        "target_leg_pos": first["target_leg_pos"],
        "target_wheel_vel": first["target_wheel_vel"],
        "target_source": first["target_source"],
        "steps_obs_current": np.stack([t["obs_current"] for t in step_traces]),
        "steps_step_index": np.stack([t["step_index"] for t in step_traces]),
        "steps_sim_time": np.stack([t["sim_time"] for t in step_traces]),
        "steps_obs_history": np.stack([t["obs_history"] for t in step_traces]),
        "steps_policy_action_raw": np.stack([t["policy_action_raw"] for t in step_traces]),
        "steps_policy_action_used": np.stack([t["policy_action_used"] for t in step_traces]),
        "steps_policy_action_clipped": np.stack([t["policy_action_clipped"] for t in step_traces]),
        "steps_policy_action_scaled_or_env_action": np.stack(
            [t["policy_action_scaled_or_env_action"] for t in step_traces]
        ),
        "steps_command": np.stack([t["command"] for t in step_traces]),
        "steps_projected_gravity": np.stack([t["projected_gravity"] for t in step_traces]),
        "steps_base_ang_vel": np.stack([t["base_ang_vel"] for t in step_traces]),
        "steps_joint_pos": np.stack([t["joint_pos"] for t in step_traces]),
        "steps_default_joint_pos": np.stack([t["default_joint_pos"] for t in step_traces]),
        "steps_joint_pos_error": np.stack([t["joint_pos_error"] for t in step_traces]),
        "steps_joint_vel": np.stack([t["joint_vel"] for t in step_traces]),
        "steps_last_action": np.stack([t["last_action"] for t in step_traces]),
        "steps_clipped_action": np.stack([t["clipped_action"] for t in step_traces]),
        "steps_scaled_action": np.stack([t["scaled_action"] for t in step_traces]),
        "steps_target_leg_pos": np.stack([t["target_leg_pos"] for t in step_traces]),
        "steps_target_wheel_vel": np.stack([t["target_wheel_vel"] for t in step_traces]),
    }
    output_prefix = args_cli.output_prefix or _default_output_prefix()
    _save_trace(Path(output_prefix).expanduser(), trace)
    print("zero_command_status:", control_status["zero_command"])
    print("disable_randomization_status:", control_status["disable_randomization"])
    print("force_default_joint_pose_status:", force_status)
    print("obs_current:", first["obs_current"].tolist())
    print("policy_action_raw:", first["policy_action_raw"].tolist())
    print("command:", first["command"].tolist())
    print("joint_pos_error:", first["joint_pos_error"].tolist())

    env.env.close()


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close()
