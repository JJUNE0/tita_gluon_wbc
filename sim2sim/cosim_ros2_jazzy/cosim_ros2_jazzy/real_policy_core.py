from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .action_adapter import ActionAdapter, ActionDebug
from .obs_builder import ObsState, ObservationBuilder


NATIVE_JOINT_NAMES = (
    "joint_left_leg_1", "joint_left_leg_2", "joint_left_leg_3", "joint_left_leg_4",
    "joint_right_leg_1", "joint_right_leg_2", "joint_right_leg_3", "joint_right_leg_4",
)
POLICY_REINDEX = np.asarray([0, 4, 1, 5, 2, 6, 3, 7], dtype=np.int64)
LEG_INDICES_NATIVE = np.asarray([0, 1, 2, 4, 5, 6], dtype=np.int64)
WHEEL_INDICES_NATIVE = np.asarray([3, 7], dtype=np.int64)


@dataclass(frozen=True)
class RealSnapshot:
    joint_pos_native: np.ndarray
    joint_vel_native: np.ndarray
    base_quat_wxyz: np.ndarray
    base_ang_vel: np.ndarray
    base_pos: np.ndarray
    base_lin_vel: np.ndarray


@dataclass(frozen=True)
class PolicyFrame:
    obs_current: np.ndarray
    obs_history: np.ndarray
    command: np.ndarray
    action_policy: np.ndarray
    action_native: np.ndarray
    action_debug: ActionDebug
    virtual_leg_target_native: np.ndarray
    virtual_wheel_vel_native: np.ndarray


def native_joint_arrays(names: list[str], positions: list[float], velocities: list[float]) -> tuple[np.ndarray, np.ndarray]:
    index = {str(name): i for i, name in enumerate(names)}
    missing = [name for name in NATIVE_JOINT_NAMES if name not in index]
    if missing:
        raise ValueError(f"missing TITA joints: {missing}")
    pos = np.asarray([positions[index[name]] for name in NATIVE_JOINT_NAMES], dtype=np.float32)
    vel = np.asarray([
        velocities[index[name]] if index[name] < len(velocities) else 0.0 for name in NATIVE_JOINT_NAMES
    ], dtype=np.float32)
    if not np.all(np.isfinite(pos)) or not np.all(np.isfinite(vel)):
        raise ValueError("non-finite joint state")
    return pos, vel


def policy_action_to_native(action_policy: np.ndarray) -> np.ndarray:
    action = np.asarray(action_policy, dtype=np.float32).reshape(8)
    if not np.all(np.isfinite(action)):
        raise ValueError("non-finite policy action")
    # Observation fields are interleaved, but this custom policy's action head
    # is already native left-then-right order.
    return action.copy()


def gate_status(
    *, sensor_received: bool, sensors_fresh: bool, values_finite: bool,
    fsm_received: bool, fsm_mode: str, allowed_modes: set[str], connected: bool,
) -> str:
    if not connected:
        return "blocked:tcp_disconnected"
    if not sensor_received:
        return "blocked:sensor_not_received"
    if not sensors_fresh:
        return "blocked:sensor_stale"
    if not values_finite:
        return "blocked:non_finite_sensor"
    if not fsm_received:
        return "blocked:fsm_not_received"
    if fsm_mode.strip().lower() not in allowed_modes:
        return f"blocked:fsm_mode_not_allowed:{fsm_mode.strip().lower() or '<empty>'}"
    return "ready:real_policy_ghost"


class RealPolicyEngine:
    """Validated observation/history/action timing without any ROS command output."""

    def __init__(self, cfg: dict[str, Any], policy: Any):
        self.cfg = cfg
        self.policy = policy
        self.obs_builder = ObservationBuilder(cfg)
        self.action_adapter = ActionAdapter(cfg)
        self.last_action_policy = np.zeros(8, dtype=np.float32)
        self.history_initialized = False

    def reset(self, snapshot: RealSnapshot, command: np.ndarray) -> np.ndarray:
        self.last_action_policy[:] = 0.0
        self.obs_builder.reset_runtime()
        obs = self._build_obs(snapshot, command)
        self.obs_builder.reset_history(obs)
        self.history_initialized = True
        return obs

    def _build_obs(self, snapshot: RealSnapshot, command: np.ndarray) -> np.ndarray:
        return self.obs_builder.build(ObsState(
            joint_pos=snapshot.joint_pos_native,
            joint_vel=snapshot.joint_vel_native,
            base_quat_wxyz=snapshot.base_quat_wxyz,
            base_ang_vel=snapshot.base_ang_vel,
            command=np.asarray(command, dtype=np.float32),
            last_action=self.last_action_policy,
        ))

    def step(self, snapshot: RealSnapshot, command: np.ndarray) -> PolicyFrame:
        command = np.asarray(command, dtype=np.float32).reshape(3)
        if not np.all(np.isfinite(command)):
            raise ValueError("non-finite command")
        obs = self._build_obs(snapshot, command)
        if not self.history_initialized:
            self.obs_builder.reset_history(obs)
            self.history_initialized = True
        history_input = self.obs_builder.history.copy()
        action_policy = np.asarray(self.policy.act(obs, history_input), dtype=np.float32).reshape(8)
        if not np.all(np.isfinite(action_policy)):
            raise ValueError("non-finite policy action")
        action_native = policy_action_to_native(action_policy)
        _, debug = self.action_adapter.compute(action_native, snapshot.joint_pos_native, snapshot.joint_vel_native)
        leg_target = debug.target_joint_pos_by_joint[LEG_INDICES_NATIVE]
        wheel_target = debug.target_joint_vel_by_joint[WHEEL_INDICES_NATIVE]
        if not np.all(np.isfinite(leg_target)) or not np.all(np.isfinite(wheel_target)):
            raise ValueError("non-finite virtual target")
        self.last_action_policy = action_policy.copy()
        self.obs_builder.push_history(obs)
        return PolicyFrame(
            obs, history_input, command.copy(), action_policy, action_native, debug,
            leg_target.astype(np.float32), wheel_target.astype(np.float32),
        )


def reset_mujoco_from_snapshot(env: Any, snapshot: RealSnapshot) -> None:
    env.mujoco.mj_resetData(env.model, env.data)
    env.data.qpos[0:3] = snapshot.base_pos
    env.data.qpos[3:7] = snapshot.base_quat_wxyz
    env.data.qpos[env.qpos_addr] = snapshot.joint_pos_native
    env.data.qvel[0:3] = snapshot.base_lin_vel
    env.data.qvel[3:6] = snapshot.base_ang_vel
    env.data.qvel[env.qvel_addr] = snapshot.joint_vel_native
    env.data.ctrl[:] = 0.0
    env.mujoco.mj_forward(env.model, env.data)


def apply_kinematic_preview(env: Any, frame: PolicyFrame, dt: float) -> None:
    """Apply finite policy targets to the local MuJoCo pose without stepping dynamics."""
    dt = max(float(dt), 0.0)
    leg_qpos = env.qpos_addr[LEG_INDICES_NATIVE]
    wheel_qpos = env.qpos_addr[WHEEL_INDICES_NATIVE]
    env.data.qpos[leg_qpos] = frame.virtual_leg_target_native.astype(np.float64)
    env.data.qpos[wheel_qpos] += frame.virtual_wheel_vel_native.astype(np.float64) * dt
    env.data.qvel[:] = 0.0
    env.data.qvel[env.qvel_addr[WHEEL_INDICES_NATIVE]] = frame.virtual_wheel_vel_native.astype(np.float64)
    env.data.ctrl[:] = 0.0
    env.mujoco.mj_forward(env.model, env.data)
