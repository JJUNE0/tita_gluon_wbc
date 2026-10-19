"""Domain-randomization events for the real-to-sim robustness variant of the My flat TITA task.

Both events start from the articulation defaults on every call, so repeated resets never compound.
Semantics were checked on the local install (Isaac Lab v2.3.0 / Isaac Sim 5.1), see
``docs/exp/2026-10-17/flashsac_retrain_prep.md``:

- Explicit PD actuators compute ``tau = Kp * (q_des - q) + Kd * (qd_des - qd) + tau_ff`` and then clip
  to the effort limit. Scaling Kp and Kd by one factor therefore equals scaling the output torque
  only while ``|tau| < effort_limit`` (no feed-forward torque is used by this task).
- Joint ``friction`` / ``dynamic_friction`` behaved as Coulomb friction torque in N m (static
  threshold and constant dynamic resistance) in an unloaded and a wheel-weight-loaded check.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import torch

from isaaclab.assets import Articulation
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils.math import sample_log_uniform, sample_uniform

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedEnv


def _joint_ids(asset: Articulation, asset_cfg: SceneEntityCfg) -> torch.Tensor:
    if isinstance(asset_cfg.joint_ids, slice):
        return torch.arange(asset.num_joints, device=asset.device)
    return torch.as_tensor(asset_cfg.joint_ids, device=asset.device)


def randomize_actuator_output_scale(
    env: ManagerBasedEnv,
    env_ids: torch.Tensor | None,
    asset_cfg: SceneEntityCfg,
    scale_range: tuple[float, float],
    jitter_range: tuple[float, float] = (1.0, 1.0),
    nominal_probability: float = 0.0,
):
    """Scale Kp and Kd of the selected joints by one log-uniform factor per environment.

    ``scale_range`` is shared by all selected joints of an environment (an effective output-torque
    scale below saturation). ``jitter_range`` adds the previous independent per-joint, per-gain
    log-uniform variation on top. With ``nominal_probability`` > 0 that fraction of environments
    keeps the shared factor at exactly 1.0 (only the jitter applies). Values are written from the
    default gains each call; the shared factor is kept in ``asset.real2sim_leg_output_scale``.
    """
    asset: Articulation = env.scene[asset_cfg.name]
    if env_ids is None:
        env_ids = torch.arange(env.scene.num_envs, device=asset.device)
    selected = _joint_ids(asset, asset_cfg)
    common = sample_log_uniform(*scale_range, (len(env_ids), 1), device=asset.device)
    if nominal_probability > 0.0:
        nominal = torch.rand((len(env_ids), 1), device=asset.device) < nominal_probability
        common = torch.where(nominal, torch.ones_like(common), common)
    if not hasattr(asset, "real2sim_leg_output_scale"):
        asset.real2sim_leg_output_scale = torch.ones(env.scene.num_envs, device=asset.device)
    asset.real2sim_leg_output_scale[env_ids] = common.view(-1)
    for actuator in asset.actuators.values():
        indices = actuator.joint_indices
        if isinstance(indices, slice):
            indices = torch.arange(asset.num_joints, device=asset.device)
        local = torch.nonzero(torch.isin(indices, selected)).view(-1)
        if len(local) == 0:
            continue
        global_ids = indices[local]
        shape = (len(env_ids), len(local))
        kp = asset.data.default_joint_stiffness[env_ids][:, global_ids]
        kd = asset.data.default_joint_damping[env_ids][:, global_ids]
        kp_jitter = sample_log_uniform(*jitter_range, shape, device=asset.device)
        kd_jitter = sample_log_uniform(*jitter_range, shape, device=asset.device)
        stiffness = actuator.stiffness[env_ids].clone()
        damping = actuator.damping[env_ids].clone()
        stiffness[:, local] = kp * common * kp_jitter
        damping[:, local] = kd * common * kd_jitter
        actuator.stiffness[env_ids] = stiffness
        actuator.damping[env_ids] = damping


def randomize_joint_coulomb_friction(
    env: ManagerBasedEnv,
    env_ids: torch.Tensor | None,
    asset_cfg: SceneEntityCfg,
    static_range: tuple[float, float],
    dynamic_ratio_range: tuple[float, float] = (1.0, 1.0),
    viscous_range: tuple[float, float] = (0.0, 0.0),
):
    """Sample static [N m], dynamic (= static * ratio) and viscous joint friction per env and joint.

    Unlike ``isaaclab.envs.mdp.randomize_joint_parameters`` (which draws static, dynamic and viscous
    friction from the same distribution), the three quantities are controlled separately here.
    """
    asset: Articulation = env.scene[asset_cfg.name]
    if env_ids is None:
        env_ids = torch.arange(env.scene.num_envs, device=asset.device)
    joint_ids = _joint_ids(asset, asset_cfg)
    shape = (len(env_ids), len(joint_ids))
    static = sample_uniform(*static_range, shape, device=asset.device)
    dynamic = static * sample_uniform(*dynamic_ratio_range, shape, device=asset.device).clamp(max=1.0)
    viscous = sample_uniform(*viscous_range, shape, device=asset.device)
    asset.write_joint_friction_coefficient_to_sim(
        static, joint_dynamic_friction_coeff=dynamic, joint_viscous_friction_coeff=viscous,
        joint_ids=joint_ids, env_ids=env_ids,
    )
