from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .real_obs_builder import DEFAULT_JOINT_ANGLES_NATIVE, WHEEL_INDICES_NATIVE


@dataclass(frozen=True)
class VirtualTargets:
    action_raw_native: np.ndarray
    action_scaled_native: np.ndarray
    policy_target_native: np.ndarray
    virtual_joint_target_native: np.ndarray
    virtual_leg_target_native: np.ndarray
    virtual_wheel_vel_native: np.ndarray
    target_type_mask_native: np.ndarray


class DryRunActionAdapter:
    """Computes virtual targets only. This class has no ROS or hardware command output."""

    def __init__(self, max_abs_leg_delta_rad: float = 0.25, max_abs_wheel_vel_rad_s: float = 5.0) -> None:
        self.max_abs_leg_delta_rad = float(max_abs_leg_delta_rad)
        self.max_abs_wheel_vel_rad_s = float(max_abs_wheel_vel_rad_s)
        self.action_scales_native = np.asarray([0.25, 0.25, 0.25, 5.0, 0.25, 0.25, 0.25, 5.0], dtype=np.float32)

    def compute(self, action_raw_native: np.ndarray) -> VirtualTargets:
        raw = np.asarray(action_raw_native, dtype=np.float32).reshape(8)
        if not np.all(np.isfinite(raw)):
            raise ValueError("Policy action contains NaN or Inf")
        scaled = raw * self.action_scales_native
        # Combined target is finite but mixed-semantic: leg slots are positions and wheel
        # slots are velocities. Separate compact arrays and the type mask remove ambiguity.
        policy_target = np.zeros(8, dtype=np.float32)
        joint_target = np.zeros(8, dtype=np.float32)
        leg_target = np.zeros(6, dtype=np.float32)
        wheel_velocity = np.zeros(2, dtype=np.float32)
        target_type_mask = np.zeros(8, dtype=np.float32)  # 1=leg position, 2=wheel velocity
        leg_index = 0
        wheel_index = 0
        for index in range(8):
            if index in WHEEL_INDICES_NATIVE:
                policy_target[index] = scaled[index]
                value = np.clip(
                    scaled[index], -self.max_abs_wheel_vel_rad_s, self.max_abs_wheel_vel_rad_s
                )
                joint_target[index] = value
                wheel_velocity[wheel_index] = value
                target_type_mask[index] = 2.0
                wheel_index += 1
            else:
                policy_target[index] = DEFAULT_JOINT_ANGLES_NATIVE[index] + scaled[index]
                delta = np.clip(scaled[index], -self.max_abs_leg_delta_rad, self.max_abs_leg_delta_rad)
                joint_target[index] = DEFAULT_JOINT_ANGLES_NATIVE[index] + delta
                leg_target[leg_index] = joint_target[index]
                target_type_mask[index] = 1.0
                leg_index += 1
        return VirtualTargets(
            raw, scaled, policy_target, joint_target, leg_target, wheel_velocity, target_type_mask
        )
