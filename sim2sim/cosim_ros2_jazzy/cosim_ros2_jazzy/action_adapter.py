from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class ActionDebug:
    action_raw_by_joint: np.ndarray
    action_used_by_joint: np.ndarray
    action_scaled_by_joint: np.ndarray
    target_joint_pos_by_joint: np.ndarray
    target_joint_vel_by_joint: np.ndarray
    target_wheel_vel_by_joint: np.ndarray
    torque_raw_by_joint: np.ndarray
    torque_clip_by_joint: np.ndarray
    torque_cmd_by_joint: np.ndarray
    joint_vel_by_joint: np.ndarray


class ActionAdapter:
    """Converts policy actions into MuJoCo actuator torques.

    Legs use PD position targets around default joint angles.
    Wheel joints use velocity targets, matching the Isaac Lab action definition for TITA.
    Action order stays native to the policy export: [L1, L2, L3, L4, R1, R2, R3, R4].
    """

    def __init__(self, cfg: dict[str, Any]):
        robot = cfg["robot"]
        debug = cfg.get("debug", {})
        self.mode = str(cfg.get("rl_adapter", {}).get("mode", "current"))
        self.wheel_indices = set(robot.get("wheel_indices", []))
        adapter_cfg = cfg.get("action_adapter", {})
        ddt_cfg = cfg.get("rl_adapter", {}).get("ddt_reference", {})
        self.wheel_sign = float(adapter_cfg.get("wheel_sign", 1.0))

        if self.mode == "ddt_reference":
            self.control_type = str(ddt_cfg.get("control_type", "P"))
            self.default_joint_angles = np.asarray(ddt_cfg["default_joint_angles"], dtype=np.float32)
            self.action_scale = np.asarray(ddt_cfg["action_scales"], dtype=np.float32)
            self.kp = np.asarray(ddt_cfg["joint_kp"], dtype=np.float32)
            self.kd = np.asarray(ddt_cfg["joint_kd"], dtype=np.float32)
            self.torque_limit = np.asarray(ddt_cfg["torque_limit"], dtype=np.float32)
            self.clip_action = bool(ddt_cfg.get("clip_action", False))
            self.action_clip_min = float(ddt_cfg.get("action_clip_min", -100.0))
            self.action_clip_max = float(ddt_cfg.get("action_clip_max", 100.0))
        else:
            self.control_type = "P_V"
            self.default_joint_angles = np.asarray(robot["default_joint_angles"], dtype=np.float32)
            self.action_scale = np.asarray(robot["action_scale"], dtype=np.float32)
            self.kp = np.asarray(robot["joint_kp"], dtype=np.float32)
            self.kd = np.asarray(robot["joint_kd"], dtype=np.float32)
            self.torque_limit = np.asarray(robot["torque_limit"], dtype=np.float32)
            self.clip_action = bool(adapter_cfg.get("clip_action", debug.get("clip_action", True)))
            self.action_clip_min = float(adapter_cfg.get("action_clip_min", -100.0))
            self.action_clip_max = float(adapter_cfg.get("action_clip_max", 100.0))
            wheel_scale_override = adapter_cfg.get("wheel_velocity_scale")
            if wheel_scale_override is not None:
                for i in self.wheel_indices:
                    self.action_scale[i] = float(wheel_scale_override)
            wheel_vel_kd = adapter_cfg.get("wheel_vel_kd")
            if wheel_vel_kd is not None:
                for i in self.wheel_indices:
                    self.kd[i] = float(wheel_vel_kd)

    def summary(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "control_type": self.control_type,
            "default_joint_angles": self.default_joint_angles.astype(float).tolist(),
            "action_scale": self.action_scale.astype(float).tolist(),
            "joint_kp": self.kp.astype(float).tolist(),
            "joint_kd": self.kd.astype(float).tolist(),
            "torque_limit": self.torque_limit.astype(float).tolist(),
            "clip_action": bool(self.clip_action),
            "action_clip_min": float(self.action_clip_min),
            "action_clip_max": float(self.action_clip_max),
            "wheel_indices": sorted(int(i) for i in self.wheel_indices),
            "wheel_sign": float(self.wheel_sign),
        }

    def compute(self, action: np.ndarray, joint_pos: np.ndarray, joint_vel: np.ndarray) -> tuple[np.ndarray, ActionDebug]:
        raw = np.asarray(action, dtype=np.float32).reshape(8)
        used = raw.copy()
        if self.clip_action:
            used = np.clip(used, self.action_clip_min, self.action_clip_max)
        scaled = used * self.action_scale
        torque_raw = np.zeros(8, dtype=np.float32)
        target_joint_pos = np.full(8, np.nan, dtype=np.float32)
        target_joint_vel = np.zeros(8, dtype=np.float32)
        target_wheel_vel = np.full(8, np.nan, dtype=np.float32)
        joint_vel = np.asarray(joint_vel, dtype=np.float32).reshape(8)

        for i in range(8):
            is_wheel = i in self.wheel_indices
            command = self.default_joint_angles[i] + scaled[i]
            if self.mode == "ddt_reference":
                if self.control_type == "P":
                    if is_wheel:
                        torque_raw[i] = self.kp[i] * command - self.kd[i] * joint_vel[i]
                        target_joint_vel[i] = self.wheel_sign * scaled[i]
                        target_wheel_vel[i] = target_joint_vel[i]
                    else:
                        target_joint_pos[i] = command
                        torque_raw[i] = self.kp[i] * (target_joint_pos[i] - joint_pos[i]) - self.kd[i] * joint_vel[i]
                elif self.control_type == "P_V":
                    if is_wheel:
                        target_vel = self.wheel_sign * scaled[i]
                        target_joint_vel[i] = target_vel
                        target_wheel_vel[i] = target_vel
                        torque_raw[i] = self.kd[i] * (target_vel - joint_vel[i])
                    else:
                        target_joint_pos[i] = command
                        torque_raw[i] = self.kp[i] * (target_joint_pos[i] - joint_pos[i]) - self.kd[i] * joint_vel[i]
                else:
                    raise ValueError(f"Unknown rl_adapter control_type: {self.control_type}")
            else:
                if is_wheel:
                    target_vel = self.wheel_sign * scaled[i]
                    target_joint_vel[i] = target_vel
                    target_wheel_vel[i] = target_vel
                    torque_raw[i] = self.kd[i] * (target_vel - joint_vel[i])
                else:
                    target_joint_pos[i] = command
                    torque_raw[i] = self.kp[i] * (target_joint_pos[i] - joint_pos[i]) - self.kd[i] * joint_vel[i]

        torque = np.clip(torque_raw, -self.torque_limit, self.torque_limit)
        torque_clip = torque_raw - torque
        debug = ActionDebug(
            action_raw_by_joint=raw.astype(np.float32),
            action_used_by_joint=used.astype(np.float32),
            action_scaled_by_joint=scaled.astype(np.float32),
            target_joint_pos_by_joint=target_joint_pos,
            target_joint_vel_by_joint=target_joint_vel.astype(np.float32),
            target_wheel_vel_by_joint=target_wheel_vel,
            torque_raw_by_joint=torque_raw.astype(np.float32),
            torque_clip_by_joint=torque_clip.astype(np.float32),
            torque_cmd_by_joint=torque.astype(np.float32),
            joint_vel_by_joint=joint_vel.astype(np.float32),
        )
        return torque.astype(np.float32), debug
