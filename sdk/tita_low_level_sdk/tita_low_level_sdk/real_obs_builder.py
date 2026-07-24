from __future__ import annotations

from dataclasses import dataclass

import numpy as np


NATIVE_JOINT_NAMES = [
    "joint_left_leg_1",
    "joint_left_leg_2",
    "joint_left_leg_3",
    "joint_left_leg_4",
    "joint_right_leg_1",
    "joint_right_leg_2",
    "joint_right_leg_3",
    "joint_right_leg_4",
]
POLICY_REINDEX = [0, 4, 1, 5, 2, 6, 3, 7]
DEFAULT_JOINT_ANGLES_NATIVE = np.asarray(
    [0.1, 0.8, -1.5, 0.0, 0.1, 0.8, -1.5, 0.0], dtype=np.float32
)
WHEEL_INDICES_NATIVE = (3, 7)


def quat_wxyz_to_rotmat(q: np.ndarray) -> np.ndarray:
    w, x, y, z = np.asarray(q, dtype=np.float32).reshape(4)
    return np.asarray(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ],
        dtype=np.float32,
    )


@dataclass(frozen=True)
class ObservationDiagnostics:
    missing_joint_names: tuple[str, ...]
    obs_norm: float
    max_abs_joint_pos: float
    max_abs_joint_vel: float
    projected_gravity: np.ndarray


class RealObservationBuilder:
    """Exact 33-D observation layout used by the verified MuJoCo policy path."""

    DEFAULT_JOINT_ANGLES_NATIVE = DEFAULT_JOINT_ANGLES_NATIVE

    def __init__(self, obs_dim: int = 33, history_len: int = 0) -> None:
        if obs_dim != 33:
            raise ValueError(f"Only the verified 33-D policy observation is supported, got {obs_dim}")
        if history_len != 0:
            raise ValueError(f"My26 has no history input; expected history_len=0, got {history_len}")
        self.obs_dim = obs_dim
        self.history_len = history_len
        self.history = np.zeros((history_len, obs_dim), dtype=np.float32)
        # last_action uses the ActionsCfg/ONNX output order. For My26 this is
        # native left-then-right, unlike the interleaved joint observation fields.
        self.last_action_policy = np.zeros(8, dtype=np.float32)

    @staticmethod
    def native_joint_arrays(joint_state: object) -> tuple[np.ndarray, np.ndarray, tuple[str, ...]]:
        names = [str(name) for name in joint_state.name]
        index_by_name = {name: index for index, name in enumerate(names)}
        missing = tuple(name for name in NATIVE_JOINT_NAMES if name not in index_by_name)
        if missing:
            return np.full(8, np.nan, dtype=np.float32), np.full(8, np.nan, dtype=np.float32), missing

        position = np.asarray(joint_state.position, dtype=np.float32)
        velocity = np.asarray(joint_state.velocity, dtype=np.float32)
        native_pos = np.empty(8, dtype=np.float32)
        native_vel = np.empty(8, dtype=np.float32)
        for native_index, name in enumerate(NATIVE_JOINT_NAMES):
            source_index = index_by_name[name]
            if source_index >= position.size or source_index >= velocity.size:
                return np.full(8, np.nan, dtype=np.float32), np.full(8, np.nan, dtype=np.float32), (name,)
            native_pos[native_index] = position[source_index]
            native_vel[native_index] = velocity[source_index]
        return native_pos, native_vel, ()

    @staticmethod
    def projected_gravity(base_quat_wxyz: np.ndarray) -> np.ndarray:
        # Isaac convention: project world gravity into the body frame.
        gravity_world = np.asarray([0.0, 0.0, -1.0], dtype=np.float32)
        return (quat_wxyz_to_rotmat(base_quat_wxyz).T @ gravity_world).astype(np.float32)

    def build(
        self,
        joint_pos_native: np.ndarray,
        joint_vel_native: np.ndarray,
        base_quat_wxyz: np.ndarray,
        base_ang_vel: np.ndarray,
        command: np.ndarray | None = None,
    ) -> tuple[np.ndarray, ObservationDiagnostics]:
        joint_pos = np.asarray(joint_pos_native, dtype=np.float32).reshape(8).copy()
        joint_vel = np.asarray(joint_vel_native, dtype=np.float32).reshape(8)
        quat = np.asarray(base_quat_wxyz, dtype=np.float32).reshape(4)
        ang_vel = np.asarray(base_ang_vel, dtype=np.float32).reshape(3)
        command = np.zeros(3, dtype=np.float32) if command is None else np.asarray(command, dtype=np.float32).reshape(3)

        all_values = np.concatenate([joint_pos, joint_vel, quat, ang_vel, command, self.last_action_policy])
        if not np.all(np.isfinite(all_values)):
            raise ValueError("Observation inputs contain NaN or Inf")
        quat_norm = float(np.linalg.norm(quat))
        if quat_norm < 1e-6:
            raise ValueError("IMU orientation quaternion has zero norm")
        quat = quat / quat_norm

        # Matches the verified sim builder: zero wheel position before default subtraction.
        joint_pos[list(WHEEL_INDICES_NATIVE)] = 0.0
        pos_rel_policy = (joint_pos - DEFAULT_JOINT_ANGLES_NATIVE)[POLICY_REINDEX]
        vel_policy = joint_vel[POLICY_REINDEX]
        gravity = self.projected_gravity(quat)

        obs = np.concatenate(
            [
                ang_vel * 0.25,
                gravity,
                command * np.asarray([2.0, 2.0, 0.25], dtype=np.float32),
                pos_rel_policy,
                vel_policy * 0.05,
                self.last_action_policy,
            ]
        ).astype(np.float32)
        if obs.shape != (self.obs_dim,):
            raise ValueError(f"Observation shape mismatch: {obs.shape} != ({self.obs_dim},)")
        if not np.all(np.isfinite(obs)):
            raise ValueError("Built observation contains NaN or Inf")

        diagnostics = ObservationDiagnostics(
            missing_joint_names=(),
            obs_norm=float(np.linalg.norm(obs)),
            max_abs_joint_pos=float(np.max(np.abs(joint_pos_native))),
            max_abs_joint_vel=float(np.max(np.abs(joint_vel_native))),
            projected_gravity=gravity,
        )
        return obs, diagnostics

    def push_history(self, obs: np.ndarray) -> None:
        obs = np.asarray(obs, dtype=np.float32).reshape(self.obs_dim)
        if self.history_len:
            self.history[:-1] = self.history[1:]
            self.history[-1] = obs

    def set_last_action(self, action_policy_order: np.ndarray) -> None:
        action = np.asarray(action_policy_order, dtype=np.float32).reshape(8)
        if not np.all(np.isfinite(action)):
            raise ValueError("Policy action contains NaN or Inf")
        self.last_action_policy = action.copy()
