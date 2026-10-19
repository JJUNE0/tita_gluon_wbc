"""Wheel-odometry position-error observation for the real-to-sim variants of the My flat TITA task.

Uses only signals the robot has, so the sim and the robot compute the same quantity: joint encoders and IMU
orientation. No ground-truth base position is used.

    s = R * mean_side(q_wheel + body_pitch + q_thigh + q_knee)

``s`` is the ground rolling distance of the wheel centres. The wheel joint angle is relative to the shank, so
the shank's absolute pitch is added. The sign was checked against MuJoCo wheel-centre motion with
``test/sim2real/check_wheel_odometry_sign.py``: 20 ms step error 0.08-0.12 mm, versus 0.56-0.63 mm uncorrected.

While the emitted velocity command is outside the zero band, the reference follows ``s`` and the observation
is 0. Inside the zero band the reference is latched and the observation is ``clip(s - reference, +-clip_m)``.
The policy can then integrate drift like the vendor controller's position hold. The wheel radius is scaled
per episode (``radius_scale_range``) as a calibration-error randomization.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

import torch

from isaaclab.assets import Articulation
from isaaclab.managers import ManagerTermBase, ObservationTermCfg, SceneEntityCfg
from isaaclab.utils.math import sample_uniform

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv

SIDES = (('joint_left_leg_4', 'joint_left_leg_2', 'joint_left_leg_3'),
         ('joint_right_leg_4', 'joint_right_leg_2', 'joint_right_leg_3'))


class WheelPositionError(ManagerTermBase):
    """Latched wheel-odometry position error in metres, shape ``(num_envs, 1)``."""

    def __init__(self, cfg: ObservationTermCfg, env: ManagerBasedRLEnv):
        super().__init__(cfg, env)
        params = cfg.params
        self.asset: Articulation = env.scene[params.get('asset_cfg', SceneEntityCfg('robot')).name]
        names = list(self.asset.joint_names)
        self.wheel = [names.index(side[0]) for side in SIDES]
        self.thigh = [names.index(side[1]) for side in SIDES]
        self.knee = [names.index(side[2]) for side in SIDES]
        self.nominal_radius = float(params.get('radius', 0.0925))
        self.radius = torch.full((env.num_envs,), self.nominal_radius, device=env.device)
        self.reference = torch.zeros(env.num_envs, device=env.device)
        self.relatch = torch.ones(env.num_envs, dtype=torch.bool, device=env.device)
        self.zero_band = torch.tensor(params.get('zero_thresholds', (0.02, 0.02, 0.03)), device=env.device)

    def reset(self, env_ids: Sequence[int] | None = None) -> None:
        ids = slice(None) if env_ids is None else env_ids
        low, high = self.cfg.params.get('radius_scale_range', (1.0, 1.0))
        count = self.radius[ids].numel()
        self.radius[ids] = self.nominal_radius * sample_uniform(low, high, (count,), device=self.radius.device)
        self.relatch[ids] = True

    def rolling_distance(self) -> torch.Tensor:
        q = self.asset.data.joint_pos
        w, x, y, z = self.asset.data.root_quat_w.unbind(dim=1)
        pitch = torch.asin(torch.clamp(2.0 * (w * y - z * x), -1.0, 1.0))
        angle = q[:, self.wheel] + pitch.unsqueeze(1) + q[:, self.thigh] + q[:, self.knee]
        return self.radius * angle.mean(dim=1)

    def __call__(
        self,
        env: ManagerBasedRLEnv,
        command_name: str,
        radius: float = 0.0925,
        radius_scale_range: tuple[float, float] = (1.0, 1.0),
        clip_m: float = 0.3,
        zero_thresholds: tuple[float, float, float] = (0.02, 0.02, 0.03),
        asset_cfg: SceneEntityCfg = SceneEntityCfg('robot'),
    ) -> torch.Tensor:
        s = self.rolling_distance()
        zero = (env.command_manager.get_command(command_name).abs() <= self.zero_band).all(dim=1)
        self.reference = torch.where(self.relatch | ~zero, s, self.reference)
        self.relatch[:] = False
        error = torch.where(zero, s - self.reference, torch.zeros_like(s))
        return torch.clamp(error, -clip_m, clip_m).unsqueeze(1)


def heading_drift_error(env: ManagerBasedRLEnv, reward_term: str = "zero_command_heading_drift") -> torch.Tensor:
    """Critic-only: wrapped heading change since the zero-command anchor of the heading drift reward, (N, 1) rad.

    Reads ``rewards.ZeroCommandHeadingDrift.heading_error`` so the critic sees exactly the anchor the reward uses
    (0 outside an anchored hold). Uses ground-truth yaw; not part of the deployed policy interface. Returns zeros
    while the reward manager does not exist yet (observation shape inference at construction).
    """
    manager = getattr(env, "reward_manager", None)
    if manager is None or reward_term not in manager.active_terms:
        return torch.zeros(env.num_envs, 1, device=env.device)
    return manager.get_term_cfg(reward_term).func.heading_error.unsqueeze(1)
