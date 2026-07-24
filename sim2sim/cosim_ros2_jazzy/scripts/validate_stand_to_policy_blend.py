#!/usr/bin/env python3
"""Headless MuJoCo diagnostic for the production stand-to-policy handoff.

This is VALIDATION_SIM only.  It intentionally reports the production gate
decision before optionally simulating the rejected candidate with the configured
slew/blend limits.  It never changes deployment configuration.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import yaml

from cosim_ros2_jazzy.action_adapter import ActionAdapter
from cosim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from cosim_ros2_jazzy.obs_builder import ObsState, ObservationBuilder, quat_wxyz_to_rpy
from cosim_ros2_jazzy.policy_runner import PolicyRunner


def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reference_target(start: np.ndarray, fold: np.ndarray, stand: np.ndarray, elapsed: float, cfg: dict) -> tuple[np.ndarray, bool]:
    fold_duration = max(float(cfg["fold_timer"]), 1e-6) * max(float(np.max(np.abs(start - fold))), 1e-6)
    stand_duration = max(float(cfg["stand_timer"]), 1e-6)
    settle_duration = max(int(cfg.get("settle_iters", 0)), 0) / max(float(cfg.get("update_rate", 500.0)), 1e-6)
    if elapsed < fold_duration:
        alpha = float(np.clip(elapsed / fold_duration, 0.0, 1.0))
        target = (1.0 - alpha) * start + alpha * fold
    elif elapsed < fold_duration + stand_duration:
        alpha = float(np.clip((elapsed - fold_duration) / stand_duration, 0.0, 1.0))
        target = (1.0 - alpha) * fold + alpha * stand
    else:
        target = stand
    return target.astype(np.float32), elapsed >= fold_duration + stand_duration + settle_duration


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--controller-config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--settle-seconds", type=float, default=5.0)
    parser.add_argument("--bridge-to-policy-stand", action="store_true")
    parser.add_argument("--diagnostic-bypass-gate", action="store_true")
    parser.add_argument("--diagnostic-blend-seconds", type=float)
    parser.add_argument("--diagnostic-running-seconds", type=float)
    parser.add_argument("--diagnostic-leg-slew", type=float)
    parser.add_argument("--diagnostic-wheel-accel", type=float)
    args = parser.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    controller = yaml.safe_load(Path(args.controller_config).read_text(encoding="utf-8"))["/**"]["tita_stage1_controller"]["ros__parameters"]
    stage2 = controller["stage2"]
    safety = controller["safety"]
    transform = controller["transform_up"]
    cfg["viewer"]["enabled"] = False
    cfg["control"]["real_time"] = False

    env = TitaMujocoEnv(cfg, viewer_enabled=False)
    obs_builder = ObservationBuilder(cfg)
    policy = PolicyRunner.from_config(cfg)
    adapter = ActionAdapter(cfg)
    wheel_indices = np.asarray([3, 7], dtype=np.int32)
    leg_indices = np.asarray([0, 1, 2, 4, 5, 6], dtype=np.int32)
    # Match the physical startup script: begin from the configured folded/idle pose,
    # interpolate through fold, then use the exact production stand target.
    idle = np.asarray(cfg["poses"]["idle_joint_angles"], dtype=np.float32)
    fold = np.asarray(transform["fold_jpos"], dtype=np.float32)
    stand = np.asarray(transform["stand_jpos"], dtype=np.float32)
    lower = np.asarray(safety["lower_limits"], dtype=np.float32)
    upper = np.asarray(safety["upper_limits"], dtype=np.float32)
    torque_limit = np.asarray(safety["effort_limits"], dtype=np.float32)
    transform_kp = np.asarray(transform["joint_kp"], dtype=np.float32)
    transform_kd = np.asarray(transform["joint_kd"], dtype=np.float32)
    transform_ff = np.asarray(transform["ff_torque"], dtype=np.float32)
    rl_kp = np.asarray(stage2["joint_kp"], dtype=np.float32)
    rl_kd = np.asarray(stage2["joint_kd"], dtype=np.float32)
    env.reset_to_joint_angles(idle)

    trace: dict[str, list] = {name: [] for name in ("phase", "time", "rpy", "ang_vel", "base_z", "q", "dq", "action", "leg_target", "wheel_target", "alpha", "torque_clip")}
    sim_time = 0.0

    def record(phase: str, action: np.ndarray, leg_target: np.ndarray, wheel_target: np.ndarray, alpha: float, torque_clip: np.ndarray) -> None:
        trace["phase"].append(phase)
        trace["time"].append(sim_time)
        trace["rpy"].append(quat_wxyz_to_rpy(env.base_quat_sensor()).tolist())
        trace["ang_vel"].append(env.base_ang_vel().tolist())
        trace["base_z"].append(float(env.base_pos()[2]))
        trace["q"].append(env.joint_pos().tolist())
        trace["dq"].append(env.joint_vel().tolist())
        trace["action"].append(action.tolist())
        trace["leg_target"].append(leg_target.tolist())
        trace["wheel_target"].append(wheel_target.tolist())
        trace["alpha"].append(float(alpha))
        trace["torque_clip"].append(torque_clip.tolist())

    def step_controller(phase: str, leg_target: np.ndarray, wheel_target: np.ndarray, kp: np.ndarray, kd: np.ndarray, ff: np.ndarray, action: np.ndarray, alpha: float, balance_cfg: dict | None = None) -> None:
        nonlocal sim_time
        last_clip = np.zeros(8, dtype=np.float32)
        effective_wheel_target = wheel_target.copy()

        def callback(q: np.ndarray, dq: np.ndarray) -> np.ndarray:
            nonlocal last_clip
            q_des = leg_target.copy()
            dq_des = np.zeros(8, dtype=np.float32)
            dq_des[wheel_indices] = wheel_target[wheel_indices]
            raw = kp * (q_des - q) + kd * (dq_des - dq) + ff
            raw[wheel_indices] = kd[wheel_indices] * (dq_des[wheel_indices] - dq[wheel_indices])
            if balance_cfg is not None and bool(balance_cfg.get("use_wheel_balance", True)):
                rpy = quat_wxyz_to_rpy(env.base_quat_sensor())
                pitch = float(rpy[1])
                pitch_rate = float(env.base_ang_vel()[1])
                target_velocity = float(balance_cfg.get("balance_sign", 1.0)) * (
                    -float(balance_cfg.get("pitch_kp", 2.0)) * pitch
                    - float(balance_cfg.get("pitch_kd", 0.3)) * pitch_rate
                )
                target_velocity = float(np.clip(
                    target_velocity,
                    -float(balance_cfg.get("wheel_vel_limit", 3.0)),
                    float(balance_cfg.get("wheel_vel_limit", 3.0)),
                ))
                effective_wheel_target[wheel_indices] = target_velocity
                wheel_gain = float(balance_cfg.get("wheel_vel_gain_override", kd[3]))
                raw[wheel_indices] = wheel_gain * (target_velocity - dq[wheel_indices])
            command = np.clip(raw, -torque_limit, torque_limit)
            last_clip = raw - command
            return command.astype(np.float32)

        env.step_with_torque_callback(callback)
        sim_time += env.control_dt
        record(phase, action, leg_target, effective_wheel_target, alpha, last_clip)

    elapsed = 0.0
    complete = False
    zeros = np.zeros(8, dtype=np.float32)
    while not complete:
        target, complete = reference_target(idle, fold, stand, elapsed, cfg["reference_transform_up"])
        step_controller("transform", target, zeros, transform_kp, transform_kd, transform_ff, zeros, 0.0)
        elapsed += env.control_dt

    for _ in range(max(1, int(round(args.settle_seconds / env.control_dt)))):
        step_controller("settle", stand, zeros, transform_kp, transform_kd, transform_ff, zeros, 0.0)

    handoff_source = stand.copy()
    handoff_balance_cfg: dict | None = None
    if args.bridge_to_policy_stand:
        policy_stand = np.asarray(stage2["policy_stand_jpos"], dtype=np.float32)
        bridge_balance_cfg = dict(cfg["handoff_bridge"])
        bridge_balance_cfg.setdefault("pitch_kp", cfg["transform_up"].get("pitch_kp", 2.0))
        bridge_balance_cfg.setdefault("pitch_kd", cfg["transform_up"].get("pitch_kd", 0.3))
        bridge_balance_cfg.setdefault("balance_sign", cfg["transform_up"].get("balance_sign", 1.0))
        handoff_balance_cfg = bridge_balance_cfg
        bridge_seconds = float(stage2["handoff_seconds"])
        bridge_steps = max(1, int(round(bridge_seconds / env.control_dt)))
        bridge_target = stand.copy()
        max_bridge_step = float(stage2["max_leg_target_slew_rad_s"]) * env.control_dt
        for index in range(bridge_steps):
            ratio = min(1.0, float(index + 1) / float(bridge_steps))
            smooth = ratio * ratio * (3.0 - 2.0 * ratio)
            requested = (1.0 - smooth) * stand + smooth * policy_stand
            bridge_target[leg_indices] = np.clip(
                requested[leg_indices],
                bridge_target[leg_indices] - max_bridge_step,
                bridge_target[leg_indices] + max_bridge_step,
            )
            step_controller("bridge", bridge_target, zeros, rl_kp, rl_kd, zeros, zeros, 0.0, bridge_balance_cfg)
        bridge_hold_steps = max(1, int(round(float(stage2["handoff_settle_seconds"]) / env.control_dt)))
        for _ in range(bridge_hold_steps):
            step_controller("bridge_hold", policy_stand, zeros, rl_kp, rl_kd, zeros, zeros, 0.0, bridge_balance_cfg)
        handoff_source = policy_stand

    command = np.zeros(3, dtype=np.float32)
    previous_action = np.zeros(8, dtype=np.float32)
    obs_builder.reset_runtime()

    def infer() -> tuple[np.ndarray, object]:
        observation = obs_builder.build(ObsState(
            joint_pos=env.joint_pos(), joint_vel=env.joint_vel(),
            base_quat_wxyz=env.base_quat_sensor(), base_ang_vel=env.base_ang_vel(),
            command=command, last_action=previous_action,
        ))
        action = policy.act(observation, obs_builder.history)
        _, debug = adapter.compute(action, env.joint_pos(), env.joint_vel())
        obs_builder.push_history(observation)
        return action.astype(np.float32), debug

    max_leg_delta = 0.0
    max_wheel_raw = 0.0
    clipping_frames = 0
    first_action = None
    prepare_steps = max(1, int(round(float(stage2["rl_prepare_seconds"]) / env.control_dt)))
    for _ in range(prepare_steps):
        action, debug = infer()
        if first_action is None:
            first_action = action.copy()
        delta = debug.target_joint_pos_by_joint[leg_indices] - handoff_source[leg_indices]
        wheel_raw = debug.target_wheel_vel_by_joint[wheel_indices]
        max_leg_delta = max(max_leg_delta, float(np.max(np.abs(delta))))
        max_wheel_raw = max(max_wheel_raw, float(np.max(np.abs(wheel_raw))))
        if np.any(np.abs(delta) > float(stage2["max_leg_target_delta_rad"])) or np.any(np.abs(wheel_raw) > float(stage2["max_wheel_velocity_rad_s"])):
            clipping_frames += 1
        prepare_kp = rl_kp if handoff_balance_cfg is not None else transform_kp
        prepare_kd = rl_kd if handoff_balance_cfg is not None else transform_kd
        prepare_ff = zeros if handoff_balance_cfg is not None else transform_ff
        step_controller("prepare", handoff_source, zeros, prepare_kp, prepare_kd, prepare_ff, action, 0.0, handoff_balance_cfg)

    gate_pass = bool(
        max_leg_delta <= float(stage2["max_leg_target_delta_rad"])
        and max_wheel_raw <= float(stage2["max_wheel_velocity_rad_s"])
        and clipping_frames <= int(stage2["max_repeated_clipping"])
    )

    diagnostic_executed = bool(gate_pass or args.diagnostic_bypass_gate)
    limited_leg = handoff_source.copy()
    limited_wheel = zeros.copy()
    if diagnostic_executed:
        blend_seconds = float(args.diagnostic_blend_seconds) if args.diagnostic_blend_seconds is not None else float(stage2["rl_blend_seconds"])
        running_seconds = float(args.diagnostic_running_seconds) if args.diagnostic_running_seconds is not None else float(stage2["rl_running_seconds"])
        leg_slew = float(args.diagnostic_leg_slew) if args.diagnostic_leg_slew is not None else float(stage2["max_leg_target_slew_rad_s"])
        wheel_accel = float(args.diagnostic_wheel_accel) if args.diagnostic_wheel_accel is not None else float(stage2["max_wheel_accel_rad_s"])
        total_steps = max(1, int(round((blend_seconds + running_seconds) / env.control_dt)))
        blend_steps = max(1, int(round(blend_seconds / env.control_dt)))
        for index in range(total_steps):
            alpha = min(1.0, float(index + 1) / float(blend_steps))
            action, debug = infer()
            requested_leg = handoff_source.copy()
            requested_leg[leg_indices] = (1.0 - alpha) * handoff_source[leg_indices] + alpha * debug.target_joint_pos_by_joint[leg_indices]
            requested_leg = np.clip(requested_leg, lower, upper)
            leg_step = leg_slew * env.control_dt
            limited_leg[leg_indices] = np.clip(requested_leg[leg_indices], limited_leg[leg_indices] - leg_step, limited_leg[leg_indices] + leg_step)
            requested_wheel = np.clip(alpha * debug.target_wheel_vel_by_joint[wheel_indices], -float(stage2["max_wheel_velocity_rad_s"]), float(stage2["max_wheel_velocity_rad_s"]))
            if handoff_balance_cfg is not None:
                current_rpy = quat_wxyz_to_rpy(env.base_quat_sensor())
                safe_wheel = float(handoff_balance_cfg.get("balance_sign", 1.0)) * (
                    -float(handoff_balance_cfg.get("pitch_kp", 2.0)) * float(current_rpy[1])
                    - float(handoff_balance_cfg.get("pitch_kd", 0.3)) * float(env.base_ang_vel()[1])
                )
                safe_wheel = float(np.clip(
                    safe_wheel,
                    -float(handoff_balance_cfg.get("wheel_vel_limit", 3.0)),
                    float(handoff_balance_cfg.get("wheel_vel_limit", 3.0)),
                ))
                requested_wheel = (1.0 - alpha) * safe_wheel + alpha * requested_wheel
            wheel_step = wheel_accel * env.control_dt
            limited_wheel[wheel_indices] = np.clip(requested_wheel, limited_wheel[wheel_indices] - wheel_step, limited_wheel[wheel_indices] + wheel_step)
            kp = (1.0 - alpha) * transform_kp + alpha * rl_kp
            kd = (1.0 - alpha) * transform_kd + alpha * rl_kd
            ff = (1.0 - alpha) * transform_ff
            step_controller("blend" if alpha < 1.0 else "running", limited_leg, limited_wheel, kp, kd, ff, action, alpha)
            previous_action[:] = alpha * action

    rpy = np.asarray(trace["rpy"], dtype=np.float32)
    ang_vel = np.asarray(trace["ang_vel"], dtype=np.float32)
    phase = np.asarray(trace["phase"])
    diagnostic_mask = np.isin(phase, ["blend", "running"])
    diagnostic_max_roll = float(np.max(np.abs(rpy[diagnostic_mask, 0]))) if np.any(diagnostic_mask) else None
    diagnostic_max_pitch = float(np.max(np.abs(rpy[diagnostic_mask, 1]))) if np.any(diagnostic_mask) else None
    diagnostic_max_ang_vel = float(np.max(np.linalg.norm(ang_vel[diagnostic_mask], axis=1))) if np.any(diagnostic_mask) else None
    diagnostic_indices = np.flatnonzero(diagnostic_mask)
    max_pitch_index = int(diagnostic_indices[np.argmax(np.abs(rpy[diagnostic_mask, 1]))]) if diagnostic_indices.size else None
    final_diagnostic_index = int(diagnostic_indices[-1]) if diagnostic_indices.size else None
    report = {
        "domain": "VALIDATION_SIM",
        "config": str(Path(args.config).resolve()),
        "controller_config": str(Path(args.controller_config).resolve()),
        "policy_path": str(Path(cfg["policy"]["path"]).resolve()),
        "policy_sha256": sha256(cfg["policy"]["path"]),
        "gate_pass": gate_pass,
        "gate_decision": "PASS" if gate_pass else "BLOCKED",
        "diagnostic_bypass_requested": bool(args.diagnostic_bypass_gate),
        "diagnostic_executed": diagnostic_executed,
        "diagnostic_blend_seconds": float(args.diagnostic_blend_seconds) if args.diagnostic_blend_seconds is not None else float(stage2["rl_blend_seconds"]),
        "diagnostic_running_seconds": float(args.diagnostic_running_seconds) if args.diagnostic_running_seconds is not None else float(stage2["rl_running_seconds"]),
        "diagnostic_leg_slew_rad_s": float(args.diagnostic_leg_slew) if args.diagnostic_leg_slew is not None else float(stage2["max_leg_target_slew_rad_s"]),
        "diagnostic_wheel_accel_rad_s2": float(args.diagnostic_wheel_accel) if args.diagnostic_wheel_accel is not None else float(stage2["max_wheel_accel_rad_s"]),
        "bridge_to_policy_stand": bool(args.bridge_to_policy_stand),
        "handoff_source_pose": handoff_source.astype(float).tolist(),
        "first_action": first_action.tolist() if first_action is not None else None,
        "max_leg_delta_from_handoff_source_rad": max_leg_delta,
        "max_abs_wheel_target_rad_s": max_wheel_raw,
        "clipping_frames_in_prepare": clipping_frames,
        "settle_max_abs_roll_rad": float(np.max(np.abs(rpy[phase == "settle", 0]))),
        "settle_max_abs_pitch_rad": float(np.max(np.abs(rpy[phase == "settle", 1]))),
        "settle_max_angular_velocity_norm_rad_s": float(np.max(np.linalg.norm(ang_vel[phase == "settle"], axis=1))),
        "diagnostic_max_abs_roll_rad": diagnostic_max_roll,
        "diagnostic_max_abs_pitch_rad": diagnostic_max_pitch,
        "diagnostic_max_angular_velocity_norm_rad_s": diagnostic_max_ang_vel,
        "diagnostic_max_pitch_time_s": float(trace["time"][max_pitch_index]) if max_pitch_index is not None else None,
        "diagnostic_max_pitch_phase": str(phase[max_pitch_index]) if max_pitch_index is not None else None,
        "diagnostic_final_rpy_rad": rpy[final_diagnostic_index].astype(float).tolist() if final_diagnostic_index is not None else None,
        "diagnostic_min_base_z": float(np.min(np.asarray(trace["base_z"], dtype=np.float32)[diagnostic_mask])) if np.any(diagnostic_mask) else None,
        "diagnostic_torque_clipping_sample_count": int(np.count_nonzero(np.any(np.abs(np.asarray(trace["torque_clip"], dtype=np.float32)[diagnostic_mask]) > 1e-6, axis=1))) if np.any(diagnostic_mask) else None,
        "diagnostic_within_current_orientation_limit": bool(
            diagnostic_executed and diagnostic_max_roll is not None and diagnostic_max_pitch is not None
            and diagnostic_max_roll <= float(safety["max_roll_rad"])
            and diagnostic_max_pitch <= float(safety["max_pitch_rad"])
        ),
        "trace": trace,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "trace"}, indent=2))
    env.close()


if __name__ == "__main__":
    main()
