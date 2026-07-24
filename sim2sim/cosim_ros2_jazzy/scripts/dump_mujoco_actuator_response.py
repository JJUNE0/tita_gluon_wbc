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


def _snapshot(env: TitaMujocoEnv, obs_builder: ObservationBuilder, action: np.ndarray, debug, substep: int) -> dict[str, np.ndarray]:
    joint_pos = env.joint_pos()
    joint_vel = env.joint_vel()
    default = np.asarray(env.cfg["robot"]["default_joint_angles"], dtype=np.float32)
    joint_pos_for_obs = joint_pos.copy()
    for idx in env.cfg["robot"].get("wheel_indices", []):
        joint_pos_for_obs[int(idx)] = 0.0
    qfrc = env.data.qfrc_actuator[env.qvel_addr].astype(np.float32).copy()
    return {
        "substep_index": np.asarray(substep, dtype=np.int32),
        "sim_time": np.asarray(env.data.time, dtype=np.float32),
        "physics_dt": np.asarray(env.model.opt.timestep, dtype=np.float32),
        "decimation": np.asarray(env.decimation, dtype=np.int32),
        "policy_dt": np.asarray(env.model.opt.timestep * env.decimation, dtype=np.float32),
        "joint_pos": joint_pos.astype(np.float32),
        "joint_vel": joint_vel.astype(np.float32),
        "default_joint_pos": default.astype(np.float32),
        "joint_pos_error": (joint_pos_for_obs - default).astype(np.float32),
        "target_leg_pos": debug.target_joint_pos_by_joint.astype(np.float32),
        "target_wheel_vel": debug.target_wheel_vel_by_joint.astype(np.float32),
        "policy_action_raw": action.astype(np.float32),
        "policy_action_used": debug.action_used_by_joint.astype(np.float32),
        "torque_cmd": debug.torque_cmd_by_joint.astype(np.float32),
        "qfrc_actuator": qfrc,
        "base_rpy": quat_wxyz_to_rpy(env.base_quat_sensor()),
        "base_ang_vel": env.base_ang_vel().astype(np.float32),
        "projected_gravity": obs_builder.projected_gravity(env.base_quat_sensor()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="cosim_ros2_jazzy/config/tita.yaml")
    parser.add_argument(
        "--output-prefix",
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/mujoco_actuator_response_step0",
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

    command = np.asarray(
        [
            cfg["command"]["default_lin_x"],
            cfg["command"]["default_lin_y"],
            cfg["command"]["default_ang_z"],
        ],
        dtype=np.float32,
    )
    last_action = np.zeros(int(cfg["policy"]["action_dim"]), dtype=np.float32)
    obs_state = ObsState(
        joint_pos=env.joint_pos(),
        joint_vel=env.joint_vel(),
        base_quat_wxyz=env.base_quat_sensor(),
        base_ang_vel=env.base_ang_vel(),
        command=command,
        last_action=last_action,
    )
    obs = obs_builder.build(obs_state)
    obs_builder.reset_history(obs)
    action = policy.act(obs, obs_builder.history.copy())

    torque, debug = adapter.compute(action, env.joint_pos(), env.joint_vel())
    env.set_torque(torque)
    snapshots = [_snapshot(env, obs_builder, action, debug, 0)]

    for substep in range(1, env.decimation + 1):
        torque, debug = adapter.compute(action, env.joint_pos(), env.joint_vel())
        env.set_torque(torque)
        env.mujoco.mj_step(env.model, env.data)
        snapshots.append(_snapshot(env, obs_builder, action, debug, substep))

    first = snapshots[0]
    trace = {
        "source": "mujoco",
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
        "steps_torque_cmd": np.stack([s["torque_cmd"] for s in snapshots]),
        "steps_qfrc_actuator": np.stack([s["qfrc_actuator"] for s in snapshots]),
        "steps_base_rpy": np.stack([s["base_rpy"] for s in snapshots]),
        "steps_base_ang_vel": np.stack([s["base_ang_vel"] for s in snapshots]),
        "steps_projected_gravity": np.stack([s["projected_gravity"] for s in snapshots]),
    }
    _save(Path(args.output_prefix).expanduser(), trace)
    print("action:", action.tolist())
    print("steps_sim_time:", trace["steps_sim_time"].tolist())
    print("steps_joint_pos_error:", trace["steps_joint_pos_error"].tolist())
    print("steps_joint_vel:", trace["steps_joint_vel"].tolist())
    print("steps_torque_cmd:", trace["steps_torque_cmd"].tolist())
    print("steps_qfrc_actuator:", trace["steps_qfrc_actuator"].tolist())
    env.close()


if __name__ == "__main__":
    main()
