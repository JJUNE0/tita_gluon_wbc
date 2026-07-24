# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

# Copyright (c) 2024-2025 Ziqi Fan
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

import torch
from isaaclab.assets import Articulation
from isaaclab.managers import ManagerTermBase, SceneEntityCfg
from isaaclab.utils.math import quat_apply, quat_apply_inverse

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedEnv, ManagerBasedRLEnv


def joint_pos_rel_without_wheel(
    env: ManagerBasedEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    wheel_asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """The joint positions of the asset w.r.t. the default joint positions.(Without the wheel joints)"""
    # extract the used quantities (to enable type-hinting)
    asset: Articulation = env.scene[asset_cfg.name]
    joint_pos_rel = asset.data.joint_pos - asset.data.default_joint_pos
    joint_pos_rel[:, wheel_asset_cfg.joint_ids] = 0
    joint_pos_rel = joint_pos_rel[:, asset_cfg.joint_ids]
    return joint_pos_rel


# ---------------------------------------------------------------------------
# Sim-to-real biased observation terms (policy group only).
# The critic keeps the ground-truth variants so the NP3O history encoder must
# infer these biases from proprio history (privileged-learning mechanism).
# Buffers are sampled once per episode by the matching reset events in
# ``events.py`` (``randomize_imu_bias`` / ``randomize_joint_offset``); when the
# event is disabled (e.g. PLAY) the term falls back to the unbiased value.
# ---------------------------------------------------------------------------


def base_ang_vel_biased(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Root angular velocity plus a persistent per-episode IMU gyro bias (sim2real #3)."""
    asset: Articulation = env.scene[asset_cfg.name]
    ang_vel = asset.data.root_ang_vel_b
    bias = getattr(env, "_imu_angvel_bias", None)
    if bias is not None:
        ang_vel = ang_vel + bias
    return ang_vel


def projected_gravity_biased(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Projected gravity plus a persistent per-episode IMU tilt bias (sim2real #3).

    Approximates IMU mounting misalignment / bias as a small additive offset on
    the gravity direction (kept un-normalised; the offset range is small).
    """
    asset: Articulation = env.scene[asset_cfg.name]
    grav = asset.data.projected_gravity_b
    bias = getattr(env, "_imu_grav_bias", None)
    if bias is not None:
        grav = grav + bias
    return grav


def joint_pos_rel_without_wheel_biased(
    env: ManagerBasedEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    wheel_asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """``joint_pos_rel_without_wheel`` plus a persistent per-joint encoder offset (sim2real #4).

    Models joint-encoder zero/calibration error: the observed joint position is
    biased by a constant per-joint offset while the physics is unaffected.
    """
    asset: Articulation = env.scene[asset_cfg.name]
    joint_pos_rel = asset.data.joint_pos - asset.data.default_joint_pos
    bias = getattr(env, "_joint_pos_bias", None)
    if bias is not None:
        joint_pos_rel = joint_pos_rel + bias
    joint_pos_rel[:, wheel_asset_cfg.joint_ids] = 0
    joint_pos_rel = joint_pos_rel[:, asset_cfg.joint_ids]
    return joint_pos_rel


def phase(env: ManagerBasedRLEnv, cycle_time: float) -> torch.Tensor:
    if not hasattr(env, "episode_length_buf") or env.episode_length_buf is None:
        env.episode_length_buf = torch.zeros(env.num_envs, device=env.device, dtype=torch.long)
    phase = env.episode_length_buf[:, None] * env.step_dt / cycle_time
    phase_tensor = torch.cat([torch.sin(2 * torch.pi * phase), torch.cos(2 * torch.pi * phase)], dim=-1)
    return phase_tensor


# ---------------------------------------------------------------------------
# Privileged observation terms (critic-only)
# Mirrors the reference ``LocomotionWithNP3O`` priv_latent subset that can be
# obtained from Isaac Lab's Articulation data without extra PhysX API calls.
# ---------------------------------------------------------------------------

def contact_state(
    env: ManagerBasedRLEnv,
    sensor_cfg: SceneEntityCfg = SceneEntityCfg("contact_forces"),
    threshold: float = 1.0,
) -> torch.Tensor:
    """Binary foot-contact state, centred at zero: +0.5 in contact, -0.5 not.

    Shape: ``(num_envs, num_feet)`` — typically 4 for D1.
    Mirrors reference ``contact_filt.float() - 0.5``.
    """
    from isaaclab.sensors import ContactSensor

    sensor: ContactSensor = env.scene.sensors[sensor_cfg.name]
    net_forces = sensor.data.net_forces_w[:, sensor_cfg.body_ids, :]  # (B, K, 3)
    in_contact = (net_forces.norm(dim=-1) > threshold).float()        # (B, K)
    return in_contact - 0.5


def joint_kp_factor(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Randomised kp (joint stiffness) as a scale factor relative to default.

    Shape: ``(num_envs, num_joints)``.
    Mirrors reference ``kp_factor`` in priv_latent; values outside [0, 2]
    are clamped to avoid very large signals from near-zero defaults.
    """
    asset: Articulation = env.scene[asset_cfg.name]
    kp = asset.data.joint_stiffness[:, asset_cfg.joint_ids]
    default_kp = asset.data.default_joint_stiffness[:, asset_cfg.joint_ids]
    return (kp / (default_kp.abs() + 1e-6)).clamp(0.0, 2.0)


def joint_kd_factor(
    env: ManagerBasedRLEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Randomised kd (joint damping) as a scale factor relative to default.

    Shape: ``(num_envs, num_joints)``.
    Mirrors reference ``kd_factor`` in priv_latent.
    """
    asset: Articulation = env.scene[asset_cfg.name]
    kd = asset.data.joint_damping[:, asset_cfg.joint_ids]
    default_kd = asset.data.default_joint_damping[:, asset_cfg.joint_ids]
    return (kd / (default_kd.abs() + 1e-6)).clamp(0.0, 2.0)


class NaiveWheelVelBaseLinVel(ManagerTermBase):
    """Naive kinematic estimate of body-frame base linear velocity from wheel spin alone.

    ``est = -v_spin_b`` (per wheel, averaged L/R), where ``v_spin_b`` is the
    ground-contact-point velocity produced by wheel spin under a no-slip,
    legs-stationary assumption:

        spin_axis_w = quat_apply(wheel_quat_w, (0,0,1))
        v_spin_w = wheel_joint_vel * cross(spin_axis_w, (0,0,-wheel_radius))
        v_spin_b = quat_apply_inverse(base_quat_w, v_spin_w)

    Deliberately ignores the leg-motion contribution (the "full" estimator in
    ``scripts/np3o/estimate_base_vel_from_wheels.py`` adds a finite-differenced
    leg-motion term) -- this is the "naive" variant from that validation
    script, ported here as an actual training-time ``ObsTerm`` so a policy can
    be trained on it directly (``My18``), instead of only validated
    after-the-fact against a ground-truth-trained policy. See
    ``Experiments/RL_Experiments.md`` for the validation numbers (RMSE ~0.10
    m/s when legs are near-stationary, ~0.32 m/s during active gait -- worse
    than the "full" estimator during locomotion, better near standstill).

    Returns a 3-vector (only the x-component is physically meaningful for a
    two-wheel differential base; y/z are returned as zero) so it can drop
    into the same observation slot as ``mdp.base_lin_vel`` unchanged.
    """

    def __init__(self, cfg, env: ManagerBasedRLEnv):
        super().__init__(cfg, env)
        asset_cfg = cfg.params.get("asset_cfg", SceneEntityCfg("robot"))
        self.asset: Articulation = env.scene[asset_cfg.name]
        wheel_radius = float(cfg.params.get("wheel_radius", 0.0925))
        left_wheel_body = cfg.params.get("left_wheel_body", "left_leg_4")
        right_wheel_body = cfg.params.get("right_wheel_body", "right_leg_4")
        left_wheel_joint = cfg.params.get("left_wheel_joint", "joint_left_leg_4")
        right_wheel_joint = cfg.params.get("right_wheel_joint", "joint_right_leg_4")
        base_body = cfg.params.get("base_body", "base_link")

        self.base_id = self.asset.find_bodies(base_body)[0][0]
        self.left_wheel_id = self.asset.find_bodies(left_wheel_body)[0][0]
        self.right_wheel_id = self.asset.find_bodies(right_wheel_body)[0][0]
        self.left_wheel_joint_id = self.asset.find_joints(left_wheel_joint)[0][0]
        self.right_wheel_joint_id = self.asset.find_joints(right_wheel_joint)[0][0]

        self._local_spin_axis = torch.tensor([0.0, 0.0, 1.0], device=env.device).expand(env.num_envs, 3)
        self._contact_offset_w = torch.tensor([0.0, 0.0, -wheel_radius], device=env.device).expand(env.num_envs, 3)

    def _spin_contribution_b(self, wheel_id: int, wheel_joint_id: int) -> torch.Tensor:
        base_quat_w = self.asset.data.body_quat_w[:, self.base_id]
        wheel_quat_w = self.asset.data.body_quat_w[:, wheel_id]
        spin_axis_w = quat_apply(wheel_quat_w, self._local_spin_axis)
        wheel_omega = self.asset.data.joint_vel[:, wheel_joint_id].unsqueeze(-1)
        v_spin_w = wheel_omega * torch.cross(spin_axis_w, self._contact_offset_w, dim=-1)
        return quat_apply_inverse(base_quat_w, v_spin_w)

    def __call__(self, env: ManagerBasedRLEnv) -> torch.Tensor:
        left = -self._spin_contribution_b(self.left_wheel_id, self.left_wheel_joint_id)
        right = -self._spin_contribution_b(self.right_wheel_id, self.right_wheel_joint_id)
        return 0.5 * (left + right)
