from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


def quat_wxyz_to_rotmat(q: np.ndarray) -> np.ndarray:
    w, x, y, z = q
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ],
        dtype=np.float32,
    )


def quat_wxyz_to_rpy(q: np.ndarray) -> np.ndarray:
    w, x, y, z = q
    roll = np.arctan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
    pitch = np.arcsin(np.clip(2.0 * (w * y - z * x), -1.0, 1.0))
    yaw = np.arctan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
    return np.array([roll, pitch, yaw], dtype=np.float32)


def estimate_base_lin_vel_naive_wheel(
    base_quat_wxyz: np.ndarray,
    left_wheel_quat_wxyz: np.ndarray,
    right_wheel_quat_wxyz: np.ndarray,
    left_wheel_omega: float,
    right_wheel_omega: float,
    wheel_radius: float = 0.0925,
) -> np.ndarray:
    """Naive kinematic base_lin_vel estimate from wheel spin alone (no-slip,
    legs-stationary assumption) -- deployment-side mirror of
    ``mdp.NaiveWheelVelBaseLinVel`` (Isaac Lab training-side, see
    ``my_flat_env_cfg.py`` / ``Experiments/RL_Experiments.md``, My18). Same
    formula, just rotation matrices instead of quaternion-apply ops to match
    this module's existing style.

    ``est = -0.5*(v_spin_left_b + v_spin_right_b)``, each
    ``v_spin_b = R_base.T @ (wheel_omega * cross(R_wheel @ (0,0,1), (0,0,-wheel_radius)))``.
    """
    contact_offset_w = np.array([0.0, 0.0, -wheel_radius], dtype=np.float32)
    local_spin_axis = np.array([0.0, 0.0, 1.0], dtype=np.float32)
    r_base = quat_wxyz_to_rotmat(base_quat_wxyz)

    def spin_contribution_b(wheel_quat_wxyz: np.ndarray, wheel_omega: float) -> np.ndarray:
        r_wheel = quat_wxyz_to_rotmat(wheel_quat_wxyz)
        spin_axis_w = r_wheel @ local_spin_axis
        v_spin_w = float(wheel_omega) * np.cross(spin_axis_w, contact_offset_w)
        return r_base.T @ v_spin_w

    left = -spin_contribution_b(left_wheel_quat_wxyz, left_wheel_omega)
    right = -spin_contribution_b(right_wheel_quat_wxyz, right_wheel_omega)
    return (0.5 * (left + right)).astype(np.float32)


@dataclass
class ObsState:
    joint_pos: np.ndarray
    joint_vel: np.ndarray
    base_quat_wxyz: np.ndarray
    base_ang_vel: np.ndarray
    command: np.ndarray
    last_action: np.ndarray
    # Body-frame base linear velocity, only used when policy.include_base_lin_vel
    # is set (e.g. My16 sim2sim: MuJoCo knows this exactly, unlike real hardware --
    # see Experiments/RL_Experiments.md). None is fine when unused.
    base_lin_vel_b: np.ndarray | None = None


class ObservationBuilder:
    """Builds the 33-dim TITA policy observation.

    Confirmed from Isaac/DDT and ddt_ros2_control:
      ang_vel(3), projected_gravity(3), command(3), dof_pos(8), dof_vel(8), last_action(8)

    Observation joint order is interleaved for parity with Isaac:
      [L1, R1, L2, R2, L3, R3, L4, R4]

    The MuJoCo frame convention is expected to match the MJCF trunk sensors. If behavior is wrong,
    first check projected gravity and gyro conventions against Isaac/Webots.
    """

    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg
        obs_cfg = cfg["observation"]
        robot_cfg = cfg["robot"]
        policy_cfg = cfg["policy"]
        obs_adapter_cfg = cfg.get("obs_adapter", {})
        self.mode = str(obs_adapter_cfg.get("mode", "current"))
        self.mode_cfg = dict(obs_adapter_cfg.get(self.mode, {})) if self.mode != "current" else {}
        self.obs_dim = int(policy_cfg["obs_dim"])
        self.history_len = int(policy_cfg["history_len"])
        default_joint_angles = self.mode_cfg.get("default_joint_angles", robot_cfg["default_joint_angles"])
        self.default_joint_angles = np.asarray(default_joint_angles, dtype=np.float32)
        self.wheel_indices = list(robot_cfg.get("wheel_indices", []))
        self.reindex = list(obs_cfg.get("reindex", list(range(8))))
        self.re_sign = np.asarray(obs_cfg.get("re_sign") or [1.0] * 8, dtype=np.float32)
        self.ang_vel_scale = float(obs_cfg["ang_vel_scale"])
        self.projected_gravity_sign = float(obs_cfg.get("projected_gravity_sign", 1.0))
        self.projected_gravity_mode = str(self.mode_cfg.get("projected_gravity_mode", obs_cfg.get("projected_gravity_mode", "legacy")))
        self.dof_pos_scale = float(obs_cfg["dof_pos_scale"])
        self.dof_vel_scale = float(obs_cfg["dof_vel_scale"])
        self.command_scale = np.asarray(self.mode_cfg.get("command_scale", obs_cfg["command_scale"]), dtype=np.float32)
        self.zero_wheel_pos = bool(self.mode_cfg.get("zero_wheel_pos", obs_cfg.get("zero_wheel_pos", True)))
        self.gyro_lpf_alpha_current = float(self.mode_cfg.get("gyro_lpf_alpha_current", 1.0))
        self.gyro_lpf_alpha_prev = float(self.mode_cfg.get("gyro_lpf_alpha_prev", 0.0))
        self.filtered_ang_vel = np.zeros(3, dtype=np.float32)
        self.history = np.zeros((self.history_len, self.obs_dim), dtype=np.float32)
        # (My16/My18-style sim2sim only) append a body-frame base_lin_vel as
        # extra obs dims -- see ObsState.base_lin_vel_b docstring.
        self.include_base_lin_vel = bool(policy_cfg.get("include_base_lin_vel", False))
        self.base_lin_vel_scale = float(obs_cfg.get("base_lin_vel_scale", 2.0))
        # "ground_truth" (My16, MuJoCo's own state -- undeployable on real
        # hardware) or "wheel_vel_estimate" (My18, naive wheel-spin kinematic
        # estimate -- deployable). See mujoco_policy_node.py::_build_obs.
        self.base_lin_vel_source = str(policy_cfg.get("base_lin_vel_source", "ground_truth"))

    def projected_gravity(self, base_quat_wxyz: np.ndarray) -> np.ndarray:
        rot = quat_wxyz_to_rotmat(np.asarray(base_quat_wxyz, dtype=np.float32))
        gravity_w = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        if self.projected_gravity_mode == "isaac":
            gravity = rot.T @ gravity_w
        else:
            gravity = rot @ gravity_w
        return (self.projected_gravity_sign * gravity).astype(np.float32)

    def reset_history(self, obs: np.ndarray) -> None:
        if self.history_len == 0:
            return
        self.history[:] = np.asarray(obs, dtype=np.float32)

    def push_history(self, obs: np.ndarray) -> None:
        if self.history_len == 0:
            return
        self.history[:-1] = self.history[1:]
        self.history[-1] = np.asarray(obs, dtype=np.float32)

    def reset_runtime(self) -> None:
        self.filtered_ang_vel[:] = 0.0

    def filter_ang_vel(self, base_ang_vel: np.ndarray) -> np.ndarray:
        base_ang_vel = np.asarray(base_ang_vel, dtype=np.float32)
        self.filtered_ang_vel = (
            self.gyro_lpf_alpha_current * base_ang_vel + self.gyro_lpf_alpha_prev * self.filtered_ang_vel
        ).astype(np.float32)
        return self.filtered_ang_vel.copy()

    def build(self, state: ObsState) -> np.ndarray:
        joint_pos = np.asarray(state.joint_pos, dtype=np.float32).copy()
        joint_vel = np.asarray(state.joint_vel, dtype=np.float32).copy()
        if self.zero_wheel_pos:
            for i in self.wheel_indices:
                joint_pos[i] = 0.0

        pos_rel = joint_pos - self.default_joint_angles
        pos_rel = pos_rel[self.reindex] * self.re_sign
        vel = joint_vel[self.reindex] * self.re_sign

        gravity = self.projected_gravity(state.base_quat_wxyz)
        command = np.asarray(state.command, dtype=np.float32) * self.command_scale

        parts = [
            self.filter_ang_vel(state.base_ang_vel) * self.ang_vel_scale,
            gravity.astype(np.float32),
            command.astype(np.float32),
            pos_rel.astype(np.float32) * self.dof_pos_scale,
            vel.astype(np.float32) * self.dof_vel_scale,
            np.asarray(state.last_action, dtype=np.float32),
        ]
        if self.include_base_lin_vel:
            if state.base_lin_vel_b is None:
                raise ValueError("policy.include_base_lin_vel=true but ObsState.base_lin_vel_b is None")
            parts.append(np.asarray(state.base_lin_vel_b, dtype=np.float32) * self.base_lin_vel_scale)
        obs = np.concatenate(parts)
        if obs.shape != (self.obs_dim,):
            raise ValueError(f"Observation shape mismatch: {obs.shape} != ({self.obs_dim},)")
        return obs.astype(np.float32)
