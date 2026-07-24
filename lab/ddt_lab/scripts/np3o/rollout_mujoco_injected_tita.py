#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib
import json
import os
from pathlib import Path

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Run IsaacLab closed-loop rollout from an injected MuJoCo TITA state.")
parser.add_argument("--task", type=str, required=True)
parser.add_argument("--num_envs", type=int, default=1)
parser.add_argument("--checkpoint", type=str, default=None)
parser.add_argument("--load_run", type=str, default=".*")
parser.add_argument("--load_checkpoint", type=str, default=r"model_.*\.pt")
parser.add_argument("--mujoco-state", type=str, required=True)
parser.add_argument("--duration", type=float, default=1.0)
parser.add_argument(
    "--output-prefix",
    type=str,
    default="/home/cocel/Desktop/Research/DDT_Lab/deploy/tita/isaac_injected_closed_loop",
)
parser.add_argument("--zero_command", action="store_true")
parser.add_argument("--disable_randomization", action="store_true")
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
OBS_SCALES = {
    "base_ang_vel": 0.25,
    "projected_gravity": 1.0,
    "command": np.asarray([2.0, 2.0, 0.25], dtype=np.float32),
    "joint_pos_error": 1.0,
    "joint_vel": 0.05,
    "last_action": 1.0,
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


def quat_wxyz_to_rpy(q: np.ndarray) -> np.ndarray:
    w, x, y, z = q
    roll = np.arctan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
    pitch = np.arcsin(np.clip(2.0 * (w * y - z * x), -1.0, 1.0))
    yaw = np.arctan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
    return np.array([roll, pitch, yaw], dtype=np.float32)


def _resolve_runner_cfg(entry_point: str) -> dict:
    module_name, attr = entry_point.split(":")
    obj = getattr(importlib.import_module(module_name), attr)
    cfg = obj() if callable(obj) else obj
    if not isinstance(cfg, dict):
        raise TypeError(f"NP3O cfg entry point '{entry_point}' must return a dict")
    return cfg


def _to_jsonable(value):
    if isinstance(value, np.ndarray):
        if value.dtype.kind in {"U", "S", "O"}:
            return value.tolist()
        return value.astype(float).tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


def _save(prefix: Path, trace: dict[str, object]) -> tuple[Path, Path]:
    prefix.parent.mkdir(parents=True, exist_ok=True)
    npz_path = prefix.with_suffix(".npz")
    json_path = prefix.with_suffix(".json")
    np.savez(npz_path, **{k: v for k, v in trace.items() if isinstance(v, np.ndarray)})
    json_path.write_text(json.dumps({k: _to_jsonable(v) for k, v in trace.items()}, indent=2), encoding="utf-8")
    return npz_path, json_path


def _configure_controlled_env(env_cfg) -> None:
    if args_cli.zero_command:
        ranges = env_cfg.commands.base_velocity.ranges
        ranges.lin_vel_x = (0.0, 0.0)
        ranges.lin_vel_y = (0.0, 0.0)
        ranges.ang_vel_z = (0.0, 0.0)
        if hasattr(ranges, "heading"):
            ranges.heading = (0.0, 0.0)
        if hasattr(env_cfg.commands.base_velocity, "heading_command"):
            env_cfg.commands.base_velocity.heading_command = False

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


def _build_policy_obs_current(robot, joint_ids, command_raw: np.ndarray, last_action: np.ndarray) -> np.ndarray:
    joint_pos = robot.data.joint_pos[0, joint_ids].detach().cpu().numpy().astype(np.float32)
    joint_vel = robot.data.joint_vel[0, joint_ids].detach().cpu().numpy().astype(np.float32)
    default_joint_pos = robot.data.default_joint_pos[0, joint_ids].detach().cpu().numpy().astype(np.float32)
    base_ang_vel = robot.data.root_ang_vel_b[0].detach().cpu().numpy().astype(np.float32)
    projected_gravity = robot.data.projected_gravity_b[0].detach().cpu().numpy().astype(np.float32)
    joint_pos_error = joint_pos - default_joint_pos
    for wheel_idx in (3, 7):
        joint_pos_error[wheel_idx] = 0.0

    # Match the confirmed policy packing order.
    reindex = [0, 4, 1, 5, 2, 6, 3, 7]
    obs_current = np.concatenate(
        [
            base_ang_vel * OBS_SCALES["base_ang_vel"],
            projected_gravity * OBS_SCALES["projected_gravity"],
            command_raw * OBS_SCALES["command"],
            joint_pos_error[reindex] * OBS_SCALES["joint_pos_error"],
            joint_vel[reindex] * OBS_SCALES["joint_vel"],
            last_action * OBS_SCALES["last_action"],
        ],
        dtype=np.float32,
    )
    return obs_current.astype(np.float32)


def main() -> None:
    state_npz = np.load(Path(args_cli.mujoco_state).expanduser(), allow_pickle=True)

    spec = gym.spec(args_cli.task)
    runner_cfg = _resolve_runner_cfg(spec.kwargs["np3o_cfg_entry_point"])
    env_cfg_entry = spec.kwargs["env_cfg_entry_point"]
    env_cfg = env_cfg_entry() if callable(env_cfg_entry) else env_cfg_entry
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device
    _configure_controlled_env(env_cfg)

    env_raw = gym.make(args_cli.task, cfg=env_cfg)
    env = IsaacLabNP3OWrapper(env_raw, device=args_cli.device or "cuda:0")
    runner = OnConstraintPolicyRunner(env, runner_cfg, log_dir=None, device=args_cli.device or "cuda:0")

    if args_cli.checkpoint is not None:
        ckpt = args_cli.checkpoint
    else:
        log_root = os.path.abspath(os.path.join("logs", "np3o", runner_cfg["runner"]["experiment_name"]))
        ckpt = get_checkpoint_path(log_root, args_cli.load_run, args_cli.load_checkpoint)
    runner.load(ckpt, load_optimizer=False)
    policy = runner.get_inference_policy(args_cli.device or "cuda:0")

    raw = env.unwrapped
    robot = raw.scene["robot"]
    env_ids = torch.tensor([0], device=raw.device, dtype=torch.long)
    joint_ids, _ = robot.find_joints(JOINT_NAMES, preserve_order=True)

    env.reset()
    root_pos = torch.tensor(state_npz["root_pos_world"], device=raw.device, dtype=torch.float32).view(1, 3)
    root_quat = torch.tensor(state_npz["root_quat_world_wxyz"], device=raw.device, dtype=torch.float32).view(1, 4)
    root_lin_vel = torch.tensor(state_npz["root_lin_vel_world"], device=raw.device, dtype=torch.float32).view(1, 3)
    root_ang_vel = torch.tensor(state_npz["gyro_raw"], device=raw.device, dtype=torch.float32).view(1, 3)
    root_pose = torch.cat([root_pos + raw.scene.env_origins[env_ids], root_quat], dim=1)
    root_vel = torch.cat([root_lin_vel, root_ang_vel], dim=1)
    joint_pos = torch.tensor(state_npz["joint_pos"], device=raw.device, dtype=torch.float32).view(1, -1)
    joint_vel = torch.tensor(state_npz["joint_vel"], device=raw.device, dtype=torch.float32).view(1, -1)

    robot.write_root_pose_to_sim(root_pose, env_ids=env_ids)
    robot.write_root_velocity_to_sim(root_vel, env_ids=env_ids)
    robot.write_joint_state_to_sim(joint_pos, joint_vel, joint_ids=joint_ids, env_ids=env_ids)
    robot.set_joint_position_target(joint_pos, joint_ids=joint_ids, env_ids=env_ids)
    robot.set_joint_velocity_target(torch.zeros_like(joint_vel), joint_ids=joint_ids, env_ids=env_ids)
    raw.sim.forward()
    raw.scene.update(dt=raw.physics_dt)
    raw.observation_manager.reset(env_ids)
    raw.action_manager.reset(env_ids)
    raw.command_manager.reset(env_ids)
    raw.scene.update(dt=raw.physics_dt)

    command_raw = np.zeros(3, dtype=np.float32)
    last_action = np.zeros(8, dtype=np.float32)
    obs_current = _build_policy_obs_current(robot, joint_ids, command_raw, last_action)
    history_len = int(getattr(raw.cfg.observations.policy, "history_length", 10))
    obs_history = np.repeat(obs_current[None, :], history_len, axis=0).astype(np.float32)
    obs = torch.from_numpy(obs_history[None, ...]).to(env.device)

    step_dt = float(raw.step_dt)
    num_steps = max(1, int(round(float(args_cli.duration) / step_dt)))

    action_traces = []
    pitch_traces = []
    wheel_action_traces = []
    joint_pos_traces = []
    joint_vel_traces = []
    root_rpy_traces = []

    with torch.inference_mode():
        for _ in range(num_steps):
            action = policy(obs)
            action_np = action[0].detach().cpu().numpy().astype(np.float32)
            action_traces.append(action_np.copy())
            wheel_action_traces.append(action_np[[3, 7]].copy())

            obs_dict, *_ = env.step(action)
            obs = obs_dict.to(env.device)

            root_state = robot.data.root_state_w[0].detach().cpu().numpy().astype(np.float32)
            rpy = quat_wxyz_to_rpy(root_state[3:7])
            root_rpy_traces.append(rpy.copy())
            pitch_traces.append(float(rpy[1]))
            joint_pos_traces.append(robot.data.joint_pos[0, joint_ids].detach().cpu().numpy().astype(np.float32).copy())
            joint_vel_traces.append(robot.data.joint_vel[0, joint_ids].detach().cpu().numpy().astype(np.float32).copy())

    action_arr = np.stack(action_traces)
    wheel_action_arr = np.stack(wheel_action_traces)
    root_rpy_arr = np.stack(root_rpy_traces)
    joint_pos_arr = np.stack(joint_pos_traces)
    joint_vel_arr = np.stack(joint_vel_traces)
    pitch_arr = np.asarray(pitch_traces, dtype=np.float32)
    wheel_vel_arr = joint_vel_arr[:, [3, 7]]

    trace = {
        "source": "isaac_closed_loop_from_mujoco_state",
        "checkpoint": str(ckpt),
        "mujoco_state_path": str(Path(args_cli.mujoco_state).resolve()),
        "duration": np.asarray(float(args_cli.duration), dtype=np.float32),
        "step_dt": np.asarray(step_dt, dtype=np.float32),
        "num_steps": np.asarray(num_steps, dtype=np.int32),
        "action_raw": action_arr.astype(np.float32),
        "wheel_action_raw": wheel_action_arr.astype(np.float32),
        "root_rpy": root_rpy_arr.astype(np.float32),
        "pitch": pitch_arr.astype(np.float32),
        "joint_pos": joint_pos_arr.astype(np.float32),
        "joint_vel": joint_vel_arr.astype(np.float32),
        "wheel_joint_vel": wheel_vel_arr.astype(np.float32),
        "final_pitch": np.asarray(float(pitch_arr[-1]), dtype=np.float32),
        "max_abs_pitch": np.asarray(float(np.max(np.abs(pitch_arr))), dtype=np.float32),
        "max_abs_action_raw": np.asarray(float(np.max(np.abs(action_arr))), dtype=np.float32),
        "max_abs_wheel_action_raw": np.asarray(float(np.max(np.abs(wheel_action_arr))), dtype=np.float32),
        "max_abs_wheel_joint_vel": np.asarray(float(np.max(np.abs(wheel_vel_arr))), dtype=np.float32),
        "final_root_rpy": root_rpy_arr[-1].astype(np.float32),
    }
    prefix = Path(args_cli.output_prefix).expanduser()
    npz_path, json_path = _save(prefix, trace)
    print("saved_npz:", npz_path)
    print("saved_json:", json_path)
    print("final_pitch:", float(trace["final_pitch"]))
    print("max_abs_pitch:", float(trace["max_abs_pitch"]))
    print("max_abs_action_raw:", float(trace["max_abs_action_raw"]))
    print("max_abs_wheel_joint_vel:", float(trace["max_abs_wheel_joint_vel"]))

    env.env.close()


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close()
