"""TRAINING_SIM: fixed support point, free slow yaw, and a low tucked swing wheel.

Anchors are privileged task state, captured after reset forward kinematics and
never followed/re-latched during an episode. The saved 35/39/8 interface stays
unchanged; legacy reference tasks and their playback semantics are preserved.
"""

from dataclasses import dataclass

import torch
from mjlab.managers import RewardTermCfg
from mjlab.managers.metrics_manager import MetricsTermCfg

from . import mdp
from .stand_one_leg_reference_env_cfg import (
    TitaStandOneLegReferenceEnvCfg, balance_metric, support_state,
)


@dataclass(kw_only=True)
class AnchoredVelocityCommandCfg(mdp.VelocityCommandCfg):
    support_side: str = "left"

    def build(self, env):
        if self.support_side not in ("left", "right"):
            raise ValueError("support_side must be left or right")
        return AnchoredVelocityCommand(self, env)


class AnchoredVelocityCommand(mdp.VelocityCommand):
    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        robot = env.scene["robot"]
        self.support_id = robot.body_names.index(f"{cfg.support_side}_leg_4")
        other = "right" if cfg.support_side == "left" else "left"
        self.swing_id = robot.body_names.index(f"{other}_leg_4")
        self.support_anchor_xy = torch.zeros(self.num_envs, 2, device=self.device)
        self.anchor_pending = torch.ones(self.num_envs, dtype=torch.bool, device=self.device)

    def reset(self, env_ids):
        self.anchor_pending[env_ids] = True
        return super().reset(env_ids)

    def _update_command(self, env_ids=None):
        super()._update_command(env_ids)
        # ManagerBasedRlEnv calls compute(dt=0) after reset's sim.forward().
        # Scoped partial resets must not touch anchors in the other rows.
        ids = (self.anchor_pending.nonzero(as_tuple=False).flatten() if env_ids is None
               else env_ids[self.anchor_pending[env_ids]])
        self.support_anchor_xy[ids] = mdp.data(self._env).body_link_pos_w[ids, self.support_id, :2]
        self.anchor_pending[ids] = False


def support_geometry(env):
    command, robot = mdp.velocity(env), env.scene["robot"]
    position = robot.data.body_link_pos_w[:, command.support_id, :2]
    drift = (position - command.support_anchor_xy).norm(dim=1)
    speed = robot.data.body_link_lin_vel_w[:, command.support_id, :2].norm(dim=1)
    return drift, speed


def support_hold(env, position_scale_m=.05, speed_scale_m_s=.1):
    drift, speed = support_geometry(env)
    support, _, _ = support_state(env, support_side=mdp.velocity(env).cfg.support_side)
    return torch.exp(-(drift / position_scale_m).square()
                     - (speed / speed_scale_m_s).square()) * support


def support_motion_cost(env, kind, scale):
    drift, speed = support_geometry(env)
    value = {"position": drift, "speed": speed}[kind]
    return (value / scale).square().clamp(max=4.)


def support_speed_soft_l1(env, scale_m_s=.1):
    """Zero only at rest; keep increasing without a flat high-speed region."""
    speed = support_geometry(env)[1]
    square = (speed / scale_m_s).square()
    # Rationalized sqrt(1+x)-1 avoids cancellation and a numeric deadband
    # for small but nonzero velocities in float32.
    return square / (torch.sqrt(1. + square) + 1.)


def support_drift_failure(env, radius_m=.1):
    # Retained for replay of earlier env.pkl files; fresh tasks no longer
    # register a position-based termination. Drift is still scored/logged.
    return support_geometry(env)[0] > radius_m


def yaw_excess(env, free_rate_rad_s=.5):
    # World vertical, rather than tilted body Z, measures heading rotation.
    return (mdp.data(env).root_link_ang_vel_w[:, 2].abs() - free_rate_rad_s).clamp_min(0.).square()


def swing_geometry(env):
    command, robot = mdp.velocity(env), env.scene["robot"]
    position = robot.data.body_link_pos_w[:, command.swing_id]
    height = position[:, 2] - env.scene.env_origins[:, 2] - .0925
    # subtree_com includes the base and all articulated descendants, not just
    # the torso COM. Horizontal distance does not reward lifting toward COM Z.
    com = env.sim.data.subtree_com[:, robot.indexing.root_body_id]
    distance = (position[:, :2] - com[:, :2]).norm(dim=1)
    return height, distance


def swing_height_excess(env, max_clearance_m=.08, scale_m=.04):
    height, _ = swing_geometry(env)
    return ((height - max_clearance_m).clamp_min(0.) / scale_m).square()


def swing_near_com(env, scale_m=.2):
    _, distance = swing_geometry(env)
    support, swing_contact, height = support_state(env, support_side=mdp.velocity(env).cfg.support_side)
    airborne = support & ~swing_contact & (height >= .01)
    return torch.exp(-(distance / scale_m).square()) * airborne


def lift_first_support(env, clearance_m=.04, grounded_swing_cost=.25,
                       support_side="left", lift_gain=2.):
    """Increase positive lift credit without increasing contact penalties."""
    support, swing_contact, height = support_state(env, support_side=support_side)
    progress = (height / clearance_m).clamp(0., 1.)
    return (lift_gain * support.float() * progress
            - grounded_swing_cost * swing_contact.float() - (~support).float())


def wheel_overlap_cost(env, min_center_distance_m=.185, scale_m=.02):
    # Self collision is disabled in the inherited model. Do not let the new
    # tuck reward exploit that by placing the two sphere-wheel proxies inside
    # one another. This is a geometry cost, not a full self-collision check.
    command = mdp.velocity(env)
    position = mdp.data(env).body_link_pos_w
    distance = (position[:, command.support_id] - position[:, command.swing_id]).norm(dim=1)
    return ((min_center_distance_m - distance).clamp_min(0.) / scale_m).square().clamp(max=4.)


def anchor_metric(env, kind, radius_m=.1, speed_limit_m_s=.1,
                  min_clearance_m=.04, max_clearance_m=.08, com_distance_m=.2):
    drift, speed = support_geometry(env)
    height, distance = swing_geometry(env)
    yaw = mdp.data(env).root_link_ang_vel_w[:, 2].abs()
    values = {"support_drift_m": drift, "support_speed_m_s": speed,
              "base_speed_m_s": mdp.data(env).root_link_lin_vel_w[:, :2].norm(dim=1),
              "yaw_abs_rad_s": yaw, "swing_com_xy_distance_m": distance,
              "wheel_overlap_fraction": (wheel_overlap_cost(env) > 0.).float(),
              "swing_overheight_fraction": (height > max_clearance_m).float()}
    if kind in values:
        return values[kind]
    side = mdp.velocity(env).cfg.support_side
    single = balance_metric(env, "single_support_fraction", support_side=side).bool()
    valid = (single & (drift <= radius_m) & (speed <= speed_limit_m_s)
             & (height >= min_clearance_m) & (height <= max_clearance_m)
             & (distance <= com_distance_m) & (wheel_overlap_cost(env) == 0.))
    if kind == "anchored_low_support_fraction":
        return valid.float()
    if kind == "anchored_low_support_time_s":
        return valid.float() * env.step_dt
    raise ValueError(kind)


class TitaStandOneLegAnchorEnvCfg(TitaStandOneLegReferenceEnvCfg):
    def __init__(self, num_envs=1024, play=False, support_side="left"):
        if support_side not in ("left", "right"):
            raise ValueError("support_side must be left or right")
        super().__init__(num_envs, play)
        self.commands["base_velocity"] = AnchoredVelocityCommandCfg(
            **vars(self.commands["base_velocity"]), support_side=support_side)
        for name in ("single_support", "support_leg_tilt", "pose_hint"):
            self.rewards[name].params["support_side"] = support_side
        self.rewards["single_support"].func = lift_first_support
        self.rewards["single_support"].params["lift_gain"] = 2.
        self.rewards["support_leg_tilt"].weight = -.1
        self.rewards["action_rate"].weight = -.001
        self.rewards["dof_acc_l2"].weight = -5e-8
        self.rewards.pop("stationary")
        self.rewards.update({
            "support_hold": RewardTermCfg(func=support_hold, weight=.1,
                params={"position_scale_m": .05, "speed_scale_m_s": .1}),
            "support_position": RewardTermCfg(func=support_motion_cost, weight=-.05,
                params={"kind": "position", "scale": .1}),
            "support_speed": RewardTermCfg(func=support_speed_soft_l1, weight=-.05,
                params={"scale_m_s": .1}),
            "yaw_excess": RewardTermCfg(func=yaw_excess, weight=-.05, params={"free_rate_rad_s": 0.}),
            "swing_height_excess": RewardTermCfg(func=swing_height_excess, weight=-.05,
                params={"max_clearance_m": .08, "scale_m": .04}),
            "swing_near_com": RewardTermCfg(func=swing_near_com, weight=.1, params={"scale_m": .2}),
            "wheel_overlap": RewardTermCfg(func=wheel_overlap_cost, weight=-.1,
                params={"min_center_distance_m": .185, "scale_m": .02}),
        })
        for term in self.metrics.values():
            term.params["support_side"] = support_side
        for name, kind, reduce in (
            ("support_drift_m", "support_drift_m", "mean"),
            ("max_support_drift_m", "support_drift_m", "max"),
            ("support_speed_m_s", "support_speed_m_s", "mean"),
            ("base_speed_m_s", "base_speed_m_s", "mean"),
            ("max_support_speed_m_s", "support_speed_m_s", "max"),
            ("yaw_abs_rad_s", "yaw_abs_rad_s", "mean"),
            ("swing_com_xy_distance_m", "swing_com_xy_distance_m", "mean"),
            ("swing_overheight_fraction", "swing_overheight_fraction", "mean"),
            ("wheel_overlap_fraction", "wheel_overlap_fraction", "mean"),
            ("anchored_low_support_fraction", "anchored_low_support_fraction", "mean"),
            ("anchored_low_support_time_s", "anchored_low_support_time_s", "sum"),
        ):
            self.metrics[name] = MetricsTermCfg(func=anchor_metric, params={"kind": kind,
                "radius_m": .1, "speed_limit_m_s": .1, "min_clearance_m": .04,
                "max_clearance_m": .08, "com_distance_m": .2}, reduce=reduce)


class TitaStandOneLegRightAnchorEnvCfg(TitaStandOneLegAnchorEnvCfg):
    def __init__(self, num_envs=1024, play=False):
        super().__init__(num_envs, play, support_side="right")
