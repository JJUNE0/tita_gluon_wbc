#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yaml

from cosim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from cosim_ros2_jazzy.obs_builder import quat_wxyz_to_rpy


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


def _snapshot(env: TitaMujocoEnv):
    root_pos = env.data.qpos[0:3].astype(np.float32).copy()
    root_rpy = quat_wxyz_to_rpy(env.base_quat())
    joint_pos = env.joint_pos()
    joint_vel = env.joint_vel()
    return {
        "root_pos": root_pos,
        "root_rpy": root_rpy,
        "joint_pos": joint_pos,
        "joint_vel": joint_vel,
        "wheel_vel": joint_vel[WHEEL_INDICES].copy(),
    }


def _inject_state(env: TitaMujocoEnv, state_npz):
    env.mujoco.mj_resetData(env.model, env.data)
    env.data.qpos[0:3] = state_npz["root_pos_world"].astype(np.float64)
    env.data.qpos[3:7] = state_npz["root_quat_world_wxyz"].astype(np.float64)
    env.data.qpos[env.qpos_addr] = state_npz["joint_pos"].astype(np.float64)
    env.data.qvel[0:3] = state_npz["root_lin_vel_world"].astype(np.float64)
    if "root_ang_vel_world" in state_npz:
        env.data.qvel[3:6] = state_npz["root_ang_vel_world"].astype(np.float64)
    else:
        env.data.qvel[3:6] = state_npz["gyro_raw"].astype(np.float64)
    env.data.qvel[env.qvel_addr] = state_npz["joint_vel"].astype(np.float64)
    env.data.ctrl[:] = 0.0
    env.mujoco.mj_forward(env.model, env.data)


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


def _clip_tau(env: TitaMujocoEnv, tau):
    limit = np.asarray(env.cfg["robot"]["torque_limit"], dtype=np.float32)
    return np.clip(np.asarray(tau, dtype=np.float32), -limit, limit)


def _run_wheel_pulse(env: TitaMujocoEnv, q_hold, amplitude: float, duration_s: float = 0.2):
    steps = int(round(duration_s / env.model.opt.timestep))
    snapshots = []
    for _ in range(steps):
        snap = _snapshot(env)
        tau = _leg_hold_torque(q_hold, snap["joint_pos"], snap["joint_vel"])
        tau[3] = amplitude
        tau[7] = amplitude
        env.set_torque(_clip_tau(env, tau))
        env.mujoco.mj_step(env.model, env.data)
        snapshots.append(_snapshot(env))
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


def _run_wheel_decay(env: TitaMujocoEnv, q_hold, initial_vel: float = 10.0, duration_s: float = 1.0):
    env.data.qvel[env.qvel_addr[3]] = initial_vel
    env.data.qvel[env.qvel_addr[7]] = initial_vel
    env.mujoco.mj_forward(env.model, env.data)
    steps = int(round(duration_s / env.model.opt.timestep))
    wheel_trace = []
    pitch_trace = []
    for _ in range(steps):
        snap = _snapshot(env)
        tau = _leg_hold_torque(q_hold, snap["joint_pos"], snap["joint_vel"]) + _wheel_damping_torque(snap["joint_vel"])
        env.set_torque(_clip_tau(env, tau))
        env.mujoco.mj_step(env.model, env.data)
        snap = _snapshot(env)
        wheel_trace.append(snap["wheel_vel"].copy())
        pitch_trace.append(float(snap["root_rpy"][1]))
    return {
        "initial_vel": initial_vel,
        "duration_s": duration_s,
        "wheel_vel_trace": np.asarray(wheel_trace, dtype=np.float32).tolist(),
        "final_wheel_vel": wheel_trace[-1].astype(float).tolist(),
        "max_abs_pitch": float(np.max(np.abs(pitch_trace))),
    }


def _run_leg_step(env: TitaMujocoEnv, q_hold, step_delta: float = 0.1, duration_s: float = 1.0):
    q_target = q_hold.copy()
    q_target[1] += step_delta
    q_target[5] += step_delta
    steps = int(round(duration_s / env.model.opt.timestep))
    joint_trace = []
    pitch_trace = []
    max_tau = 0.0
    for _ in range(steps):
        snap = _snapshot(env)
        tau = _leg_hold_torque(q_target, snap["joint_pos"], snap["joint_vel"]) + _wheel_damping_torque(snap["joint_vel"])
        tau = _clip_tau(env, tau)
        max_tau = max(max_tau, float(np.max(np.abs(tau))))
        env.set_torque(tau)
        env.mujoco.mj_step(env.model, env.data)
        snap = _snapshot(env)
        joint_trace.append(snap["joint_pos"].copy())
        pitch_trace.append(float(snap["root_rpy"][1]))
    return {
        "step_delta_rad": step_delta,
        "duration_s": duration_s,
        "final_joint_pos": joint_trace[-1].astype(float).tolist(),
        "max_abs_pitch": float(np.max(np.abs(pitch_trace))),
        "max_abs_torque_cmd": max_tau,
    }


def main():
    parser = argparse.ArgumentParser(description="Run simple MuJoCo TITA response tests from a MuJoCo handoff state.")
    parser.add_argument("--config", type=str, default="/home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim/cosim_ros2_jazzy/config/tita.yaml")
    parser.add_argument("--handoff-state", type=str, required=True)
    parser.add_argument(
        "--output",
        type=str,
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/mujoco_response_tests.json",
    )
    args = parser.parse_args()

    cfg = yaml.safe_load(Path(args.config).expanduser().read_text(encoding="utf-8"))
    cfg.setdefault("viewer", {})
    cfg["viewer"]["enabled"] = False
    cfg.setdefault("control", {})
    cfg["control"]["real_time"] = False
    env = TitaMujocoEnv(cfg, viewer_enabled=False)
    state_npz = np.load(Path(args.handoff_state).expanduser(), allow_pickle=True)

    result = {
        "config": str(Path(args.config).expanduser().resolve()),
        "handoff_state": str(Path(args.handoff_state).expanduser().resolve()),
        "physics_dt": float(env.model.opt.timestep),
        "tests": {},
    }

    _inject_state(env, state_npz)
    q_hold = _snapshot(env)["joint_pos"]
    for amp in [2.0, 5.0, 10.0]:
        _inject_state(env, state_npz)
        q_hold = _snapshot(env)["joint_pos"]
        result["tests"][f"wheel_torque_pulse_{amp:g}Nm"] = _run_wheel_pulse(env, q_hold, amp)

    _inject_state(env, state_npz)
    q_hold = _snapshot(env)["joint_pos"]
    result["tests"]["wheel_damping_decay"] = _run_wheel_decay(env, q_hold)

    _inject_state(env, state_npz)
    q_hold = _snapshot(env)["joint_pos"]
    result["tests"]["leg_pd_step"] = _run_leg_step(env, q_hold)

    out_path = Path(args.output).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(out_path)
    env.close()


if __name__ == "__main__":
    main()
