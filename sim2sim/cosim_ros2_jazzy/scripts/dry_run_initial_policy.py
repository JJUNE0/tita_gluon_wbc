#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yaml

from cosim_ros2_jazzy.action_adapter import ActionAdapter
from cosim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from cosim_ros2_jazzy.obs_builder import ObsState, ObservationBuilder, quat_wxyz_to_rpy
from cosim_ros2_jazzy.policy_runner import PolicyRunner


def _fmt(values: np.ndarray) -> list[float]:
    return [round(float(v), 6) for v in values.tolist()]


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="cosim_ros2_jazzy/config/tita.yaml")
    parser.add_argument(
        "--output-prefix",
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/mujoco_policy_trace_initial",
        help="Output path prefix. Writes <prefix>.npz and <prefix>.json.",
    )
    parser.add_argument("--dump-steps", type=int, default=1, help="Number of RL policy cycles to dump.")
    args = parser.parse_args()

    with open(Path(args.config).expanduser(), "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["viewer"]["enabled"] = False
    cfg["control"]["real_time"] = False

    env = TitaMujocoEnv(cfg, viewer_enabled=False)
    obs_builder = ObservationBuilder(cfg)
    policy = PolicyRunner.from_config(cfg)
    adapter = ActionAdapter(cfg)

    command = np.asarray(
        [
            cfg["command"]["default_lin_x"],
            cfg["command"]["default_lin_y"],
            cfg["command"]["default_ang_z"],
        ],
        dtype=np.float32,
    )
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

    init_obs = build_obs()
    obs_builder.reset_history(init_obs)

    step_traces = []
    for step_idx in range(max(int(args.dump_steps), 1)):
        obs = build_obs()
        history = obs_builder.history.copy()
        action = policy.act(obs, history)
        torque, debug = adapter.compute(action, env.joint_pos(), env.joint_vel())

        joint_pos = env.joint_pos()
        joint_vel = env.joint_vel()
        default = np.asarray(cfg["robot"]["default_joint_angles"], dtype=np.float32)
        joint_pos_for_obs = joint_pos.copy()
        for idx in cfg["robot"].get("wheel_indices", []):
            joint_pos_for_obs[int(idx)] = 0.0
        joint_pos_error = joint_pos_for_obs - default

        step_trace = {
            "step_index": np.asarray(step_idx, dtype=np.int32),
            "sim_time": np.asarray(env.data.time, dtype=np.float32),
            "physics_dt": np.asarray(env.model.opt.timestep, dtype=np.float32),
            "decimation": np.asarray(env.decimation, dtype=np.int32),
            "policy_dt": np.asarray(env.model.opt.timestep * env.decimation, dtype=np.float32),
            "obs_current": obs.copy(),
            "obs_history": history,
            "policy_action_raw": action.astype(np.float32),
            "policy_action_used": debug.action_used_by_joint.astype(np.float32),
            "policy_action_clipped": debug.action_used_by_joint.astype(np.float32),
            "policy_action_scaled_or_env_action": debug.action_scaled_by_joint.astype(np.float32),
            "command": command.copy(),
            "projected_gravity": obs_builder.projected_gravity(env.base_quat_sensor()),
            "base_ang_vel": env.base_ang_vel().astype(np.float32),
            "joint_pos": joint_pos.astype(np.float32),
            "default_joint_pos": default.astype(np.float32),
            "joint_pos_error": joint_pos_error.astype(np.float32),
            "joint_vel": joint_vel.astype(np.float32),
            "last_action": last_action.copy(),
            "base_rpy": quat_wxyz_to_rpy(env.base_quat_sensor()),
            "clipped_action": debug.action_used_by_joint.astype(np.float32),
            "scaled_action": debug.action_scaled_by_joint.astype(np.float32),
            "target_leg_pos": debug.target_joint_pos_by_joint.astype(np.float32),
            "target_wheel_vel": debug.target_wheel_vel_by_joint.astype(np.float32),
            "torque_cmd": debug.torque_cmd_by_joint.astype(np.float32),
        }
        step_traces.append(step_trace)

        def torque_callback(joint_pos_now, joint_vel_now):
            sub_torque, _ = adapter.compute(action, joint_pos_now, joint_vel_now)
            return sub_torque

        env.step_with_torque_callback(torque_callback)
        obs_builder.push_history(obs)
        last_action = debug.action_raw_by_joint.astype(np.float32)

    first = step_traces[0]
    trace = {
        "source": "mujoco",
        **first,
        "steps_step_index": np.stack([t["step_index"] for t in step_traces]),
        "steps_sim_time": np.stack([t["sim_time"] for t in step_traces]),
        "physics_dt": first["physics_dt"],
        "decimation": first["decimation"],
        "policy_dt": first["policy_dt"],
        "steps_obs_current": np.stack([t["obs_current"] for t in step_traces]),
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

    print("config:", args.config)
    print("base_rpy:", _fmt(first["base_rpy"]))
    print("projected_gravity:", _fmt(first["projected_gravity"]))
    print("base_ang_vel:", _fmt(first["base_ang_vel"]))
    print("command:", _fmt(command))
    print("joint_pos:", _fmt(first["joint_pos"]))
    print("default_joint_angles:", _fmt(first["default_joint_pos"]))
    print("joint_pos_error:", _fmt(first["joint_pos_error"]))
    print("joint_vel:", _fmt(first["joint_vel"]))
    print("last_action:", _fmt(first["last_action"]))
    print("obs:", _fmt(first["obs_current"]))
    print("action_raw_by_joint:", _fmt(first["policy_action_raw"]))
    print("action_scaled_by_joint:", _fmt(first["policy_action_scaled_or_env_action"]))
    print("target_joint_pos_by_joint:", _fmt(first["target_leg_pos"]))
    print("target_wheel_vel_by_joint:", _fmt(first["target_wheel_vel"]))
    print("torque_cmd_by_joint:", _fmt(first["torque_cmd"]))
    _save_trace(Path(args.output_prefix).expanduser(), trace)

    env.close()


if __name__ == "__main__":
    main()
