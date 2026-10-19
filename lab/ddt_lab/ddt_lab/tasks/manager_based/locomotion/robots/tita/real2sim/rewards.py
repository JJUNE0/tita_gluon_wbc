"""Zero-command reward terms for the vendor-informed real-to-sim variant of the My flat TITA task.

Both terms follow the task's convention of fading out when the robot is not upright
(``clamp(-projected_gravity_z, 0, 0.7) / 0.7``) and act only while the emitted velocity command is
(near) zero, so command tracking is untouched.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import torch

from isaaclab.assets import Articulation
from isaaclab.managers import ManagerTermBase, RewardTermCfg, SceneEntityCfg

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


def _upright(env: ManagerBasedRLEnv) -> torch.Tensor:
    return torch.clamp(-env.scene["robot"].data.projected_gravity_b[:, 2], 0, 0.7) / 0.7


def _zero_command(env: ManagerBasedRLEnv, command_name: str, threshold: float) -> torch.Tensor:
    # `<=` so threshold 0.0 matches an exactly-zero emitted command (standing / settle envs).
    return torch.linalg.norm(env.command_manager.get_command(command_name), dim=1) <= threshold


def zero_command_stand_pose_l1(
    env: ManagerBasedRLEnv,
    command_name: str,
    target: list[float],
    command_threshold: float = 0.05,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Sum of |q - target| over ``asset_cfg`` joints (in ``asset_cfg`` order) while the command is ~zero.

    ``target`` is a standing pose measured on the real robot, e.g. the vendor controller's
    hip 0 / thigh 1.09 / knee -2.16 rad, instead of the training default pose used as action offset.
    """
    asset: Articulation = env.scene[asset_cfg.name]
    q = asset.data.joint_pos[:, asset_cfg.joint_ids]
    error = torch.sum(torch.abs(q - torch.tensor(target, device=q.device)), dim=1)
    return error * _zero_command(env, command_name, command_threshold) * _upright(env)


def zero_command_lin_vel_l2(
    env: ManagerBasedRLEnv,
    command_name: str,
    command_threshold: float = 0.0,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Squared horizontal base speed (body frame) while the command is zero."""
    asset: Articulation = env.scene[asset_cfg.name]
    speed = torch.sum(torch.square(asset.data.root_lin_vel_b[:, :2]), dim=1)
    return speed * _zero_command(env, command_name, command_threshold) * _upright(env)


def _yaw(quat_wxyz: torch.Tensor) -> torch.Tensor:
    w, x, y, z = quat_wxyz.unbind(-1)
    return torch.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))


class ZeroCommandHeadingDrift(ManagerTermBase):
    """Heading counterpart of ``mdp.ZeroCommandPositionDrift``: ``exp(-sharpness * |dpsi|)`` during a zero-command hold.

    ``track_ang_vel_z_exp`` (std 0.5 rad/s) loses only ~0.1-2.5 % at 1-4.6 deg/s, and the xy position drift term
    does not see an in-place turn, so a slow constant yaw rate was almost free (2026-10-18/19 real runs). Here the
    world yaw is anchored once a hold has lasted ``warmup_s`` and the wrapped heading change since the anchor is
    rewarded with a sharp kernel; a small constant rate compounds into a growing error. The anchor is dropped as
    soon as the command leaves the zero band and on reset. ``heading_error`` keeps the latest wrapped error (0 when
    no anchor) for the critic observation ``observations.heading_drift_error`` so the value function sees the
    state this reward depends on. Fades out when not upright, like the other terms in this file.
    """

    def __init__(self, cfg: RewardTermCfg, env: ManagerBasedRLEnv):
        super().__init__(cfg, env)
        self.asset: Articulation = env.scene[cfg.params.get("asset_cfg", SceneEntityCfg("robot")).name]
        self.warmup_steps = max(1, round(float(cfg.params.get("warmup_s", 1.0)) / env.step_dt))
        self.hold_steps = torch.zeros(env.num_envs, device=env.device)
        self.anchor_yaw = torch.zeros(env.num_envs, device=env.device)
        self.anchor_set = torch.zeros(env.num_envs, dtype=torch.bool, device=env.device)
        self.heading_error = torch.zeros(env.num_envs, device=env.device)

    def reset(self, env_ids=None) -> None:
        if env_ids is None:
            env_ids = slice(None)
        self.hold_steps[env_ids] = 0.0
        self.anchor_set[env_ids] = False
        self.heading_error[env_ids] = 0.0

    def __call__(
        self,
        env: ManagerBasedRLEnv,
        command_name: str,
        sharpness: float = 5.0,
        command_threshold: float = 0.0,
        warmup_s: float = 1.0,
        asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    ) -> torch.Tensor:
        is_zero = _zero_command(env, command_name, command_threshold)
        self.hold_steps = torch.where(is_zero, self.hold_steps + 1.0, torch.zeros_like(self.hold_steps))
        yaw = _yaw(self.asset.data.root_quat_w)
        crossed = is_zero & (self.hold_steps == float(self.warmup_steps))
        self.anchor_yaw = torch.where(crossed, yaw, self.anchor_yaw)
        self.anchor_set = (self.anchor_set | crossed) & is_zero
        delta = yaw - self.anchor_yaw
        error = torch.atan2(torch.sin(delta), torch.cos(delta))
        self.heading_error = torch.where(self.anchor_set, error, torch.zeros_like(error))
        reward = torch.exp(-sharpness * self.heading_error.abs())
        return torch.where(self.anchor_set, reward, torch.zeros_like(reward)) * _upright(env)
