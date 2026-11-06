#!/usr/bin/env python3
from __future__ import annotations

"""Dump Isaac Lab TITA actuator response over one policy step.

Run inside /home/cocel/isaac/env_isaaclab. This script unfolds the Isaac Lab
decimation loop so the response can be compared against MuJoCo at every physics
substep.
"""

import argparse
import importlib
import json
import os
from pathlib import Path

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Dump TITA Isaac actuator response for policy step 0.")
parser.add_argument("--task", type=str, required=True)
parser.add_argument("--num_envs", type=int, default=1)
parser.add_argument("--checkpoint", type=str, default=None)
parser.add_argument("--load_run", type=str, default=".*")
parser.add_argument("--load_checkpoint", type=str, default=r"model_.*\.pt")
parser.add_argument(
    "--output-prefix",
    type=str,
    default="/home/cocel/Desktop/Research/DDT_Lab/deploy/tita/isaac_actuator_response_step0",
)
parser.add_argument("--zero_command", action="store_true")
parser.add_argument("--disable_randomization", action="store_true")
parser.add_argument("--force_default_joint_pose", action="store_true")
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
LEG_INDICES = [0, 1, 2, 4, 5, 6]
WHEEL_INDICES = [3, 7]


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


def _save(prefix: Path, trace: dict[str, np.ndarray | str]) -> None:
    prefix.parent.mkdir(parents=True, exist_ok=True)
    np.savez(prefix.with_suffix(".npz"), **{k: v for k, v in trace.items() if isinstance(v, np.ndarray)})
    with open(prefix.with_suffix(".json"), "w", encoding="utf-8") as f:
        json.dump({k: _to_jsonable(v) for k, v in trace.items()}, f, indent=2)
    print("saved_npz:", prefix.with_suffix(".npz"))
    print("saved_json:", prefix.with_suffix(".json"))


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


def _quat_wxyz_to_rpy(q: np.ndarray) -> np.ndarray:
    w, x, y, z = [float(v) for v in q]
    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)
    sinp = 2.0 * (w * y - z * x)
    pitch = np.sign(sinp) * np.pi / 2.0 if abs(sinp) >= 1.0 else np.arcsin(sinp)
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)
    return np.asarray([roll, pitch, yaw], dtype=np.float32)


def _action_targets(action: np.ndarray, default_joint_pos: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    used = np.clip(action.astype(np.float32), -100.0, 100.0)
    scale = np.asarray([0.25, 0.25, 0.25, 5.0, 0.25, 0.25, 0.25, 5.0], dtype=np.float32)
    scaled = used * scale
    target_leg_pos = np.full(8, np.nan, dtype=np.float32)
    target_wheel_vel = np.full(8, np.nan, dtype=np.float32)
    target_leg_pos[LEG_INDICES] = default_joint_pos[LEG_INDICES] + scaled[LEG_INDICES]
    target_wheel_vel[WHEEL_INDICES] = scaled[WHEEL_INDICES]
    return used, target_leg_pos, target_wheel_vel


def _tensor_field(obj, name: str, joint_ids: list[int]) -> np.ndarray:
    value = getattr(obj, name, None)
    if value is None:
        return np.full(8, np.nan, dtype=np.float32)
    try:
        return value[0, joint_ids].detach().cpu().numpy().astype(np.float32)
    except Exception:
        return np.full(8, np.nan, dtype=np.float32)


def _snapshot(raw_env, joint_ids: list[int], action: np.ndarray, substep_index: int) -> dict[str, np.ndarray]:
    robot = raw_env.scene["robot"]
    data = robot.data
    joint_pos = data.joint_pos[0, joint_ids].detach().cpu().numpy().astype(np.float32)
    joint_vel = data.joint_vel[0, joint_ids].detach().cpu().numpy().astype(np.float32)
    default_joint_pos = data.default_joint_pos[0, joint_ids].detach().cpu().numpy().astype(np.float32)
    joint_pos_for_obs = joint_pos.copy()
    joint_pos_for_obs[WHEEL_INDICES] = 0.0
    used, target_leg_pos, target_wheel_vel = _action_targets(action, default_joint_pos)
    root_quat = data.root_quat_w[0].detach().cpu().numpy().astype(np.float32)
    return {
        "substep_index": np.asarray(substep_index, dtype=np.int32),
        "sim_time": np.asarray(float(substep_index) * float(raw_env.physics_dt), dtype=np.float32),
        "physics_dt": np.asarray(float(raw_env.physics_dt), dtype=np.float32),
        "decimation": np.asarray(int(raw_env.cfg.decimation), dtype=np.int32),
        "policy_dt": np.asarray(float(raw_env.step_dt), dtype=np.float32),
        "joint_pos": joint_pos,
        "joint_vel": joint_vel,
        "default_joint_pos": default_joint_pos,
        "joint_pos_error": joint_pos_for_obs - default_joint_pos,
        "target_leg_pos": target_leg_pos,
        "target_wheel_vel": target_wheel_vel,
        "policy_action_raw": action.astype(np.float32),
        "policy_action_used": used,
        "joint_pos_target": _tensor_field(data, "joint_pos_target", joint_ids),
        "joint_vel_target": _tensor_field(data, "joint_vel_target", joint_ids),
        "computed_torque": _tensor_field(data, "computed_torque", joint_ids),
        "applied_torque": _tensor_field(data, "applied_torque", joint_ids),
        "base_rpy": _quat_wxyz_to_rpy(root_quat),
        "base_ang_vel": data.root_ang_vel_b[0].detach().cpu().numpy().astype(np.float32),
        "projected_gravity": data.projected_gravity_b[0].detach().cpu().numpy().astype(np.float32),
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
    with torch.inference_mode():
        action_tensor = policy(obs)
    action = action_tensor[0].detach().cpu().numpy().astype(np.float32)

    raw = env.unwrapped
    robot = raw.scene["robot"]
    joint_ids, _ = robot.find_joints(JOINT_NAMES, preserve_order=True)

    raw.action_manager.process_action(action_tensor.to(raw.device))
    raw.action_manager.apply_action()
    raw.scene.write_data_to_sim()

    snapshots = [_snapshot(raw, joint_ids, action, 0)]
    is_rendering = raw.sim.has_gui() or raw.sim.has_rtx_sensors()
    for substep in range(1, int(raw.cfg.decimation) + 1):
        raw._sim_step_counter += 1
        raw.sim.step(render=False)
        if raw._sim_step_counter % raw.cfg.sim.render_interval == 0 and is_rendering:
            raw.sim.render()
        raw.scene.update(dt=raw.physics_dt)
        if substep < int(raw.cfg.decimation):
            raw.action_manager.apply_action()
            raw.scene.write_data_to_sim()
        snapshots.append(_snapshot(raw, joint_ids, action, substep))

    first = snapshots[0]
    trace = {
        "source": "isaac",
        "checkpoint": str(ckpt),
        "zero_command_status": control_status["zero_command"],
        "disable_randomization_status": control_status["disable_randomization"],
        "force_default_joint_pose_status": force_status,
        **first,
        "steps_sim_time": np.stack([s["sim_time"] for s in snapshots]),
        "steps_substep_index": np.stack([s["substep_index"] for s in snapshots]),
        "steps_joint_pos": np.stack([s["joint_pos"] for s in snapshots]),
        "steps_joint_vel": np.stack([s["joint_vel"] for s in snapshots]),
        "steps_default_joint_pos": np.stack([s["default_joint_pos"] for s in snapshots]),
        "steps_joint_pos_error": np.stack([s["joint_pos_error"] for s in snapshots]),
        "steps_target_leg_pos": np.stack([s["target_leg_pos"] for s in snapshots]),
        "steps_target_wheel_vel": np.stack([s["target_wheel_vel"] for s in snapshots]),
        "steps_policy_action_raw": np.stack([s["policy_action_raw"] for s in snapshots]),
        "steps_policy_action_used": np.stack([s["policy_action_used"] for s in snapshots]),
        "steps_joint_pos_target": np.stack([s["joint_pos_target"] for s in snapshots]),
        "steps_joint_vel_target": np.stack([s["joint_vel_target"] for s in snapshots]),
        "steps_computed_torque": np.stack([s["computed_torque"] for s in snapshots]),
        "steps_applied_torque": np.stack([s["applied_torque"] for s in snapshots]),
        "steps_base_rpy": np.stack([s["base_rpy"] for s in snapshots]),
        "steps_base_ang_vel": np.stack([s["base_ang_vel"] for s in snapshots]),
        "steps_projected_gravity": np.stack([s["projected_gravity"] for s in snapshots]),
    }
    _save(Path(args_cli.output_prefix).expanduser(), trace)
    print("zero_command_status:", control_status["zero_command"])
    print("disable_randomization_status:", control_status["disable_randomization"])
    print("force_default_joint_pose_status:", force_status)
    print("action:", action.tolist())
    print("steps_sim_time:", trace["steps_sim_time"].tolist())
    print("steps_joint_pos_error:", trace["steps_joint_pos_error"].tolist())
    print("steps_joint_vel:", trace["steps_joint_vel"].tolist())
    print("steps_applied_torque:", trace["steps_applied_torque"].tolist())

    env.env.close()


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close()
