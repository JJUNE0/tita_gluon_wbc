#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path

import numpy as np
import yaml

from cosim_ros2_jazzy.action_adapter import ActionAdapter
from cosim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from cosim_ros2_jazzy.obs_builder import ObsState, ObservationBuilder, quat_wxyz_to_rpy
from cosim_ros2_jazzy.policy_runner import PolicyRunner


def _to_jsonable(value):
    if isinstance(value, np.ndarray):
        if np.issubdtype(value.dtype, np.number):
            return value.astype(float).tolist()
        return value.tolist()
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


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(Path(path).expanduser(), "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _reference_target(start: np.ndarray, fold: np.ndarray, stand: np.ndarray, elapsed: float, cfg: dict) -> tuple[np.ndarray, bool, float]:
    fold_timer = max(float(cfg.get("fold_timer", 4.0)), 1e-6)
    stand_timer = max(float(cfg.get("stand_timer", 2.0)), 1e-6)
    settle_iters = max(int(cfg.get("settle_iters", 100)), 0)
    update_rate = max(float(cfg.get("update_rate", 500.0)), 1e-6)

    fold_duration = fold_timer * max(float(np.max(np.abs(start - fold))), 1e-6)
    stand_duration = stand_timer
    settle_duration = settle_iters / update_rate
    total_duration = max(fold_duration + stand_duration + settle_duration, 1e-6)

    if elapsed < fold_duration:
        b = float(np.clip(elapsed / fold_duration, 0.0, 1.0))
        a = 1.0 - b
        target = a * start + b * fold
        complete = False
    elif elapsed < fold_duration + stand_duration:
        phase_t = elapsed - fold_duration
        b = float(np.clip(phase_t / stand_duration, 0.0, 1.0))
        a = 1.0 - b
        target = a * fold + b * stand
        complete = False
    else:
        target = stand
        complete = elapsed >= total_duration

    progress = float(np.clip(elapsed / total_duration, 0.0, 1.0))
    return target.astype(np.float32), complete, progress


def _reference_controller_torque(env: TitaMujocoEnv, cfg: dict, target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    q = env.joint_pos()
    dq = env.joint_vel()
    target = np.asarray(target, dtype=np.float32)
    kp = np.asarray(cfg["joint_kp"], dtype=np.float32).copy()
    kd = np.asarray(cfg["joint_kd"], dtype=np.float32).copy()
    ff = np.asarray(cfg["ff_torque"], dtype=np.float32).copy()
    qd_des = np.zeros_like(target, dtype=np.float32)
    wheel_indices = [int(i) for i in env.cfg["robot"].get("wheel_indices", [])]
    wheel_kp = float(cfg.get("wheel_kp", 0.0))
    wheel_kd = float(cfg.get("wheel_kd", 0.5))
    wheel_qd_des = float(cfg.get("wheel_qd_des", 0.0))
    for idx in wheel_indices:
        kp[idx] = wheel_kp
        kd[idx] = wheel_kd
        ff[idx] = 0.0
        qd_des[idx] = wheel_qd_des
    raw = kp * (target - q) + kd * (qd_des - dq) + ff
    limit = np.asarray(env.cfg["robot"]["torque_limit"], dtype=np.float32)
    torque = np.clip(raw, -limit, limit).astype(np.float32)
    clip = (raw - torque).astype(np.float32)
    return torque, clip


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="cosim_ros2_jazzy/config/tita.yaml")
    parser.add_argument("--hold-duration", type=float, default=3.0)
    parser.add_argument("--max-leg-target-delta", type=float, default=0.25)
    parser.add_argument("--max-wheel-velocity", type=float, default=5.0)
    parser.add_argument(
        "--output-prefix",
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/mujoco_handoff_state",
    )
    args = parser.parse_args()

    with open(Path(args.config).expanduser(), "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["viewer"]["enabled"] = False
    cfg["control"]["real_time"] = False

    env = TitaMujocoEnv(cfg, viewer_enabled=False)
    obs_builder = ObservationBuilder(cfg)
    policy = PolicyRunner.from_config(cfg)
    adapter = ActionAdapter(cfg)

    idle = np.asarray(cfg["poses"]["idle_joint_angles"], dtype=np.float32)
    fold = np.asarray(cfg["reference_transform_up"]["fold_jpos"], dtype=np.float32)
    stand = np.asarray(cfg["reference_transform_up"]["stand_jpos"], dtype=np.float32)
    env.reset_to_joint_angles(idle)

    elapsed = 0.0
    complete = False
    last_clip = np.zeros(8, dtype=np.float32)
    stand_trace_rpy: list[np.ndarray] = []
    stand_trace_ang_vel: list[np.ndarray] = []
    stand_trace_base_z: list[float] = []
    stand_trace_torque_clip: list[np.ndarray] = []

    def record_physics_sample() -> None:
        stand_trace_rpy.append(quat_wxyz_to_rpy(env.base_quat_sensor()).astype(np.float32))
        stand_trace_ang_vel.append(env.base_ang_vel().astype(np.float32))
        stand_trace_base_z.append(float(env.base_pos()[2]))
        stand_trace_torque_clip.append(last_clip.copy())

    while not complete:
        target, complete, _ = _reference_target(idle, fold, stand, elapsed, cfg["reference_transform_up"])

        def callback(_q, _dq):
            torque, clip = _reference_controller_torque(env, cfg["reference_transform_up"], target)
            nonlocal last_clip
            last_clip = clip
            return torque

        env.step_with_torque_callback(callback)
        record_physics_sample()
        elapsed += env.control_dt

    hold_start_index = len(stand_trace_rpy)
    hold_steps = max(1, int(round(float(args.hold_duration) / env.control_dt)))
    for _ in range(hold_steps):
        def callback_hold(_q, _dq):
            torque, clip = _reference_controller_torque(env, cfg["reference_transform_up"], stand)
            nonlocal last_clip
            last_clip = clip
            return torque

        env.step_with_torque_callback(callback_hold)
        record_physics_sample()

    command = np.asarray(
        [
            cfg["command"]["default_lin_x"],
            cfg["command"]["default_lin_y"],
            cfg["command"]["default_ang_z"],
        ],
        dtype=np.float32,
    )
    obs_builder.reset_runtime()
    last_action = np.zeros(int(cfg["policy"]["action_dim"]), dtype=np.float32)

    def build_obs() -> np.ndarray:
        obs_state = ObsState(
            joint_pos=env.joint_pos(),
            joint_vel=env.joint_vel(),
            base_quat_wxyz=env.base_quat_sensor(),
            base_ang_vel=env.base_ang_vel(),
            command=command,
            last_action=last_action,
        )
        return obs_builder.build(obs_state)

    obs_current = build_obs()
    obs_builder.reset_history(obs_current)
    obs_history = obs_builder.history.copy()
    action = policy.act(obs_current, obs_history)
    _, debug = adapter.compute(action, env.joint_pos(), env.joint_vel())

    leg_indices = np.asarray([0, 1, 2, 4, 5, 6], dtype=np.int32)
    wheel_indices_array = np.asarray([3, 7], dtype=np.int32)
    policy_leg_delta_from_reference_stand = (
        debug.target_joint_pos_by_joint[leg_indices] - stand[leg_indices]
    ).astype(np.float32)
    policy_wheel_target = debug.target_wheel_vel_by_joint[wheel_indices_array].astype(np.float32)
    handoff_gate_pass = bool(
        np.all(np.abs(policy_leg_delta_from_reference_stand) <= float(args.max_leg_target_delta))
        and np.all(np.abs(policy_wheel_target) <= float(args.max_wheel_velocity))
    )

    trace_rpy = np.asarray(stand_trace_rpy, dtype=np.float32)
    trace_ang_vel = np.asarray(stand_trace_ang_vel, dtype=np.float32)
    trace_base_z = np.asarray(stand_trace_base_z, dtype=np.float32)
    trace_torque_clip = np.asarray(stand_trace_torque_clip, dtype=np.float32)
    hold_rpy = trace_rpy[hold_start_index:]
    hold_ang_vel = trace_ang_vel[hold_start_index:]
    hold_base_z = trace_base_z[hold_start_index:]
    hold_torque_clip = trace_torque_clip[hold_start_index:]

    joint_pos = env.joint_pos().astype(np.float32)
    joint_vel = env.joint_vel().astype(np.float32)
    default_joint_angles = np.asarray(obs_builder.default_joint_angles, dtype=np.float32)
    joint_pos_error = joint_pos.copy()
    for idx in cfg["robot"].get("wheel_indices", []):
        joint_pos_error[int(idx)] = 0.0
    joint_pos_error = joint_pos_error - default_joint_angles

    root_pos = env.data.qpos[0:3].astype(np.float32).copy()
    root_quat = env.data.qpos[3:7].astype(np.float32).copy()
    root_lin_vel = env.data.qvel[0:3].astype(np.float32).copy()
    root_ang_vel = env.data.qvel[3:6].astype(np.float32).copy()
    wheel_indices = [int(i) for i in cfg["robot"].get("wheel_indices", [])]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = Path(f"{args.output_prefix}_{timestamp}")
    trace = {
        "source": "mujoco_reference_stand_hold",
        "config": str(Path(args.config).resolve()),
        "policy_path": str(Path(cfg["policy"]["path"]).resolve()),
        "policy_sha256": _sha256(cfg["policy"]["path"]),
        "root_pos_world": root_pos,
        "root_quat_world_wxyz": root_quat,
        "root_lin_vel_world": root_lin_vel,
        "root_ang_vel_freejoint": root_ang_vel,
        "root_ang_vel_freejoint_note": "MuJoCo freejoint qvel[3:6]; base_ang_vel below is IMU gyro sensor",
        "base_rpy": quat_wxyz_to_rpy(root_quat),
        "projected_gravity": obs_builder.projected_gravity(env.base_quat_sensor()),
        "gyro_raw": env.base_ang_vel().astype(np.float32),
        "gyro_filtered": obs_builder.filtered_ang_vel.astype(np.float32),
        "joint_pos": joint_pos,
        "joint_vel": joint_vel,
        "joint_order": np.asarray(cfg["robot"]["joint_names"]),
        "default_joint_angles": default_joint_angles,
        "joint_pos_error": joint_pos_error.astype(np.float32),
        "wheel_joint_pos": joint_pos[wheel_indices].astype(np.float32),
        "wheel_joint_vel": joint_vel[wheel_indices].astype(np.float32),
        "obs_current": obs_current.astype(np.float32),
        "obs_history": obs_history.astype(np.float32),
        "last_action": last_action.astype(np.float32),
        "command": command.astype(np.float32),
        "command_scaled": (command * obs_builder.command_scale).astype(np.float32),
        "policy_action_raw": debug.action_raw_by_joint.astype(np.float32),
        "policy_action_scaled": debug.action_scaled_by_joint.astype(np.float32),
        "policy_leg_delta_from_reference_stand": policy_leg_delta_from_reference_stand,
        "policy_wheel_target": policy_wheel_target,
        "handoff_gate_pass": handoff_gate_pass,
        "handoff_gate_max_leg_target_delta": float(args.max_leg_target_delta),
        "handoff_gate_max_wheel_velocity": float(args.max_wheel_velocity),
        "torque_cmd": debug.torque_cmd_by_joint.astype(np.float32),
        "torque_clip": debug.torque_clip_by_joint.astype(np.float32),
        "reference_stand_target": stand.astype(np.float32),
        "reference_hold_duration": np.asarray(float(args.hold_duration), dtype=np.float32),
        "final_reference_transform_up_progress": np.asarray(1.0, dtype=np.float32),
        "final_pitch": np.asarray(float(quat_wxyz_to_rpy(root_quat)[1]), dtype=np.float32),
        "stand_trace_rpy": trace_rpy,
        "stand_trace_ang_vel": trace_ang_vel,
        "stand_trace_base_z": trace_base_z,
        "stand_trace_torque_clip": trace_torque_clip,
        "max_abs_roll": float(np.max(np.abs(trace_rpy[:, 0]))),
        "max_abs_pitch": float(np.max(np.abs(trace_rpy[:, 1]))),
        "max_angular_velocity_norm": float(np.max(np.linalg.norm(trace_ang_vel, axis=1))),
        "min_base_z": float(np.min(trace_base_z)),
        "torque_clipping_sample_count": int(np.count_nonzero(np.any(np.abs(trace_torque_clip) > 1e-6, axis=1))),
        "hold_max_abs_roll": float(np.max(np.abs(hold_rpy[:, 0]))),
        "hold_max_abs_pitch": float(np.max(np.abs(hold_rpy[:, 1]))),
        "hold_max_angular_velocity_norm": float(np.max(np.linalg.norm(hold_ang_vel, axis=1))),
        "hold_min_base_z": float(np.min(hold_base_z)),
        "hold_torque_clipping_sample_count": int(np.count_nonzero(np.any(np.abs(hold_torque_clip) > 1e-6, axis=1))),
    }
    npz_path, json_path = _save(prefix, trace)
    print("saved_npz:", npz_path)
    print("saved_json:", json_path)
    print("root_pos_world:", root_pos.tolist())
    print("root_quat_world_wxyz:", root_quat.tolist())
    print("base_rpy:", quat_wxyz_to_rpy(root_quat).tolist())
    print("joint_pos:", joint_pos.tolist())
    print("joint_vel:", joint_vel.tolist())
    print("joint_pos_error:", joint_pos_error.tolist())
    print("policy_action_raw:", debug.action_raw_by_joint.tolist())
    print("policy_leg_delta_from_reference_stand:", policy_leg_delta_from_reference_stand.tolist())
    print("policy_wheel_target:", policy_wheel_target.tolist())
    print("handoff_gate_pass:", handoff_gate_pass)
    print("max_abs_roll:", float(np.max(np.abs(trace_rpy[:, 0]))))
    print("max_abs_pitch:", float(np.max(np.abs(trace_rpy[:, 1]))))
    print("max_angular_velocity_norm:", float(np.max(np.linalg.norm(trace_ang_vel, axis=1))))
    print("min_base_z:", float(np.min(trace_base_z)))
    print("torque_clipping_sample_count:", int(np.count_nonzero(np.any(np.abs(trace_torque_clip) > 1e-6, axis=1))))
    print("hold_max_abs_roll:", float(np.max(np.abs(hold_rpy[:, 0]))))
    print("hold_max_abs_pitch:", float(np.max(np.abs(hold_rpy[:, 1]))))
    print("hold_max_angular_velocity_norm:", float(np.max(np.linalg.norm(hold_ang_vel, axis=1))))
    print("hold_min_base_z:", float(np.min(hold_base_z)))
    print("hold_torque_clipping_sample_count:", int(np.count_nonzero(np.any(np.abs(hold_torque_clip) > 1e-6, axis=1))))

    env.close()


if __name__ == "__main__":
    main()
