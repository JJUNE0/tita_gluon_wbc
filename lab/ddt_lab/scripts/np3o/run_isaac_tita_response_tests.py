#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Run simple IsaacLab TITA response tests from a MuJoCo handoff state.")
parser.add_argument("--task", type=str, default="DDT-Velocity-Flat-Tita-v0")
parser.add_argument("--num_envs", type=int, default=1)
parser.add_argument("--handoff-state", type=str, required=True)
parser.add_argument(
    "--output",
    type=str,
    default="/home/cocel/Desktop/Research/DDT_Lab/deploy/tita/isaac_response_tests.json",
)
AppLauncher.add_app_launcher_args(parser)
args_cli, _ = parser.parse_known_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import ddt_lab.tasks  # noqa: E402,F401
import gymnasium as gym  # noqa: E402
import numpy as np  # noqa: E402
import torch  # noqa: E402


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


def _inject_state(raw, state_npz, joint_ids):
    robot = raw.scene["robot"]
    env_ids = torch.tensor([0], device=raw.device, dtype=torch.long)
    root_pos = torch.tensor(state_npz["root_pos_world"], device=raw.device, dtype=torch.float32).view(1, 3)
    root_quat = torch.tensor(state_npz["root_quat_world_wxyz"], device=raw.device, dtype=torch.float32).view(1, 4)
    root_lin_vel = torch.tensor(state_npz["root_lin_vel_world"], device=raw.device, dtype=torch.float32).view(1, 3)
    if "root_ang_vel_world" in state_npz:
        root_ang_vel = torch.tensor(state_npz["root_ang_vel_world"], device=raw.device, dtype=torch.float32).view(1, 3)
    else:
        root_ang_vel = torch.tensor(state_npz["gyro_raw"], device=raw.device, dtype=torch.float32).view(1, 3)
    root_pose = torch.cat([root_pos + raw.scene.env_origins[env_ids], root_quat], dim=1)
    root_vel = torch.cat([root_lin_vel, root_ang_vel], dim=1)
    joint_pos = torch.tensor(state_npz["joint_pos"], device=raw.device, dtype=torch.float32).view(1, -1)
    joint_vel = torch.tensor(state_npz["joint_vel"], device=raw.device, dtype=torch.float32).view(1, -1)

    robot.write_root_pose_to_sim(root_pose, env_ids=env_ids)
    robot.write_root_velocity_to_sim(root_vel, env_ids=env_ids)
    robot.write_joint_state_to_sim(joint_pos, joint_vel, joint_ids=joint_ids, env_ids=env_ids)
    raw.sim.forward()
    raw.scene.update(dt=raw.physics_dt)


def _snapshot(raw, joint_ids):
    robot = raw.scene["robot"]
    joint_pos = robot.data.joint_pos[0, joint_ids].detach().cpu().numpy().astype(np.float32)
    joint_vel = robot.data.joint_vel[0, joint_ids].detach().cpu().numpy().astype(np.float32)
    root_state = robot.data.root_state_w[0].detach().cpu().numpy().astype(np.float32)
    root_rpy = _quat_wxyz_to_rpy(root_state[3:7])
    return {
        "root_pos": root_state[:3],
        "root_rpy": root_rpy,
        "joint_pos": joint_pos,
        "joint_vel": joint_vel,
        "wheel_vel": joint_vel[WHEEL_INDICES].copy(),
    }


def _step_effort(raw, torque):
    robot = raw.scene["robot"]
    torque_t = torch.tensor(torque, device=raw.device, dtype=torch.float32).view(1, -1)
    robot.set_joint_effort_target(torque_t)
    raw.scene.write_data_to_sim()
    raw.sim.step(render=False)
    raw.scene.update(dt=raw.physics_dt)


def _leg_hold_torque(q_target, q, qd, kp=60.0, kd=1.5):
    tau = np.zeros(8, dtype=np.float32)
    for idx in LEG_INDICES:
        tau[idx] = kp * (q_target[idx] - q[idx]) - kd * qd[idx]
    return tau


def _wheel_damping_torque(qd, kd=0.5):
    tau = np.zeros(8, dtype=np.float32)
    for idx in WHEEL_INDICES:
        tau[idx] = -kd * qd[idx]
    return tau


def _run_wheel_pulse(raw, q_hold, amplitude: float, duration_s: float = 0.2):
    steps = int(round(duration_s / raw.physics_dt))
    snapshots = []
    for _ in range(steps):
        snap = _snapshot(raw, joint_ids)
        tau = _leg_hold_torque(q_hold, snap["joint_pos"], snap["joint_vel"])
        tau[3] = amplitude
        tau[7] = amplitude
        _step_effort(raw, tau)
        snapshots.append(_snapshot(raw, joint_ids))
    start = snapshots[0]
    end = snapshots[-1]
    return {
        "amplitude_nm": amplitude,
        "duration_s": duration_s,
        "wheel_vel_delta": (end["wheel_vel"] - start["wheel_vel"]).astype(float).tolist(),
        "max_abs_wheel_vel": float(max(np.max(np.abs(s["wheel_vel"])) for s in snapshots)),
        "base_pitch_delta": float(end["root_rpy"][1] - start["root_rpy"][1]),
        "base_x_delta": float(end["root_pos"][0] - start["root_pos"][0]),
    }


def _run_wheel_decay(raw, q_hold, initial_vel: float = 10.0, duration_s: float = 1.0):
    robot = raw.scene["robot"]
    env_ids = torch.tensor([0], device=raw.device, dtype=torch.long)
    q = robot.data.joint_pos[0, joint_ids].detach().clone().view(1, -1)
    qd = robot.data.joint_vel[0, joint_ids].detach().clone().view(1, -1)
    qd[0, 3] = initial_vel
    qd[0, 7] = initial_vel
    robot.write_joint_state_to_sim(q, qd, joint_ids=joint_ids, env_ids=env_ids)
    raw.sim.forward()
    raw.scene.update(dt=raw.physics_dt)
    steps = int(round(duration_s / raw.physics_dt))
    wheel_trace = []
    pitch_trace = []
    for _ in range(steps):
        snap = _snapshot(raw, joint_ids)
        tau = _leg_hold_torque(q_hold, snap["joint_pos"], snap["joint_vel"]) + _wheel_damping_torque(snap["joint_vel"])
        _step_effort(raw, tau)
        snap = _snapshot(raw, joint_ids)
        wheel_trace.append(snap["wheel_vel"].copy())
        pitch_trace.append(float(snap["root_rpy"][1]))
    return {
        "initial_vel": initial_vel,
        "duration_s": duration_s,
        "wheel_vel_trace": np.asarray(wheel_trace, dtype=np.float32).tolist(),
        "final_wheel_vel": wheel_trace[-1].astype(float).tolist(),
        "max_abs_pitch": float(np.max(np.abs(pitch_trace))),
    }


def _run_leg_step(raw, q_hold, step_delta: float = 0.1, duration_s: float = 1.0):
    q_target = q_hold.copy()
    q_target[1] += step_delta
    q_target[5] += step_delta
    steps = int(round(duration_s / raw.physics_dt))
    joint_trace = []
    pitch_trace = []
    max_tau = 0.0
    for _ in range(steps):
        snap = _snapshot(raw, joint_ids)
        tau = _leg_hold_torque(q_target, snap["joint_pos"], snap["joint_vel"]) + _wheel_damping_torque(snap["joint_vel"])
        max_tau = max(max_tau, float(np.max(np.abs(tau))))
        _step_effort(raw, tau)
        snap = _snapshot(raw, joint_ids)
        joint_trace.append(snap["joint_pos"].copy())
        pitch_trace.append(float(snap["root_rpy"][1]))
    return {
        "step_delta_rad": step_delta,
        "duration_s": duration_s,
        "final_joint_pos": joint_trace[-1].astype(float).tolist(),
        "max_abs_pitch": float(np.max(np.abs(pitch_trace))),
        "max_abs_torque_cmd": max_tau,
    }


spec = gym.spec(args_cli.task)
env_cfg_entry = spec.kwargs["env_cfg_entry_point"]
env_cfg = env_cfg_entry() if callable(env_cfg_entry) else env_cfg_entry
env_cfg.scene.num_envs = args_cli.num_envs
env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device
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
        "velocity_range": {"x": (0.0, 0.0), "y": (0.0, 0.0), "z": (0.0, 0.0), "roll": (0.0, 0.0), "pitch": (0.0, 0.0), "yaw": (0.0, 0.0)},
    }
if getattr(env_cfg.events, "reset_robot_joints", None) is not None:
    env_cfg.events.reset_robot_joints.params = {"position_range": (1.0, 1.0), "velocity_range": (0.0, 0.0)}
env_cfg.commands.base_velocity.ranges.lin_vel_x = (0.0, 0.0)
env_cfg.commands.base_velocity.ranges.lin_vel_y = (0.0, 0.0)
env_cfg.commands.base_velocity.ranges.ang_vel_z = (0.0, 0.0)
if hasattr(env_cfg.commands.base_velocity.ranges, "heading"):
    env_cfg.commands.base_velocity.ranges.heading = (0.0, 0.0)
if hasattr(env_cfg.commands.base_velocity, "heading_command"):
    env_cfg.commands.base_velocity.heading_command = False

env = gym.make(args_cli.task, cfg=env_cfg)
raw = env.unwrapped
robot = raw.scene["robot"]
joint_ids, _ = robot.find_joints(JOINT_NAMES, preserve_order=True)
state_npz = np.load(Path(args_cli.handoff_state).expanduser(), allow_pickle=True)

raw.reset()
_inject_state(raw, state_npz, joint_ids)
q_hold = _snapshot(raw, joint_ids)["joint_pos"]

result = {
    "task": args_cli.task,
    "handoff_state": str(Path(args_cli.handoff_state).expanduser().resolve()),
    "physics_dt": float(raw.physics_dt),
    "policy_dt": float(raw.step_dt),
    "tests": {},
}

for amp in [2.0, 5.0, 10.0]:
    _inject_state(raw, state_npz, joint_ids)
    q_hold = _snapshot(raw, joint_ids)["joint_pos"]
    result["tests"][f"wheel_torque_pulse_{amp:g}Nm"] = _run_wheel_pulse(raw, q_hold, amp)

_inject_state(raw, state_npz, joint_ids)
q_hold = _snapshot(raw, joint_ids)["joint_pos"]
result["tests"]["wheel_damping_decay"] = _run_wheel_decay(raw, q_hold)

_inject_state(raw, state_npz, joint_ids)
q_hold = _snapshot(raw, joint_ids)["joint_pos"]
result["tests"]["leg_pd_step"] = _run_leg_step(raw, q_hold)

out_path = Path(args_cli.output).expanduser()
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(out_path)

env.close()
simulation_app.close()
