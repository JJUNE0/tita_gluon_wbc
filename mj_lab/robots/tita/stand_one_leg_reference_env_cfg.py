"""TRAINING_SIM: independent fixed-side support with a loose operator pose hint."""

import math

import torch
from mjlab.envs import mdp as native
from mjlab.managers import RewardTermCfg, TerminationTermCfg
from mjlab.managers.metrics_manager import MetricsTermCfg

from . import mdp
from .flat_env_cfg import TitaFlatEnvCfg
from .stand_one_leg_env_cfg import stationary


def support_state(env, contact_threshold=5., radius=.0925, support_side="left"):
    """Select support/swing geometry; default keeps saved left-only policies."""
    robot = env.scene["robot"]
    ids = [robot.body_names.index(name) for name in mdp.WHEELS]
    contact = env.scene["feet"].data.force.norm(dim=-1) > contact_threshold
    support = 0 if support_side == "left" else 1
    swing = 1-support
    clearance = robot.data.body_link_pos_w[:, ids[swing], 2] - env.scene.env_origins[:, 2] - radius
    return contact[:, support], contact[:, swing], clearance


def fixed_support(env, clearance_m=.04, grounded_swing_cost=.25, support_side="left"):
    support, swing_contact, height = support_state(env, support_side=support_side)
    progress = (height / clearance_m).clamp(0., 1.)
    # Partial lifts earn credit; grounded swing remains a small penalty.
    return (support.float() * progress - grounded_swing_cost * swing_contact.float()
            - (~support).float())


def pose_hint(env, roll_min_deg=20., roll_max_deg=40.,
              hip_min_deg=25., hip_max_deg=40., overshoot_width_deg=15., support_side="left"):
    """Reward broad angle magnitudes, leaving signs and sagittal joints free.

    The operator's kinematic example used ~32 deg roll and ~43--45 deg leg_1
    angles. Its COM balance was not verified, so their signs are not imposed
    on the fixed support side. Wheel angles and leg_2/leg_3 are not imitated.
    """
    robot = env.scene["robot"]
    q = robot.data.root_link_quat_w
    roll = torch.atan2(2 * (q[:, 0]*q[:, 1] + q[:, 2]*q[:, 3]),
                       1 - 2 * (q[:, 1].square() + q[:, 2].square()))
    ids = [robot.joint_names.index(f"joint_{side}_leg_1") for side in ("left", "right")]
    angles = torch.cat((roll.abs()[:, None], robot.data.joint_pos[:, ids].abs()), dim=1)
    lower = angles.new_tensor([roll_min_deg, hip_min_deg, hip_min_deg]) * math.pi/180
    upper = angles.new_tensor([roll_max_deg, hip_max_deg, hip_max_deg]) * math.pi/180
    width = overshoot_width_deg * math.pi/180
    score = (angles/lower).clamp(0., 1.) * torch.exp(-((angles-upper).clamp_min(0.)/width).square())
    support, _, _ = support_state(env, support_side=support_side)
    return score.mean(dim=1) * support


def support_leg_tilt(env, support_side="left"):
    robot = env.scene["robot"]
    hip, wheel = [robot.body_names.index(f"{support_side}_leg_{index}") for index in (2, 4)]
    axis = robot.data.body_link_pos_w[:, hip] - robot.data.body_link_pos_w[:, wheel]
    cosine = axis[:, 2] / axis.norm(dim=-1).clamp_min(1e-6)
    return 1. - cosine.clamp(-1., 1.)


def balance_metric(env, kind, support_side="left"):
    support, swing_contact, height = support_state(env, support_side=support_side)
    actual = support & ~swing_contact & (height >= .01) & ~env.termination_manager.terminated
    if kind == "single_support_fraction":
        return actual.float()
    if kind == "single_support_time_s":
        return actual.float() * env.step_dt
    if kind == "double_support_fraction":
        return (support & swing_contact).float()
    if kind == "swing_clearance_m":
        return height.clamp_min(0.)
    if kind == "pose_hint":
        return pose_hint(env, support_side=support_side)
    raise ValueError(kind)


class TitaStandOneLegReferenceEnvCfg(TitaFlatEnvCfg):
    def __init__(self, num_envs=1024, play=False):
        super().__init__(num_envs, play)
        velocity = self.commands["base_velocity"]
        velocity.lin_vel_x = velocity.lin_vel_y = velocity.ang_vel_z = (0., 0.)
        velocity.rel_straight_envs, velocity.rel_standing_envs = 0., 1.
        velocity.wheel_error_velocity_thresholds = (.1, .15)
        velocity.wheel_error_moving_anchor = True
        self.events["reset_joints"].params["position_range"] = (1., 1.)
        self.events["reset_base"].params["velocity_range"] = {
            name: (0., 0.) for name in self.events["reset_base"].params["velocity_range"]}
        self.terminations["knee_contact"] = TerminationTermCfg(
            func=mdp.illegal_contact, params={"sensor": "knees", "threshold": 1.})
        # Persist the same standing entry for sim2sim without inventing a gait.
        self.sim_reset_on_policy_entry = True
        self.rewards = {
            "alive": RewardTermCfg(func=native.is_alive, weight=2.),
            "single_support": RewardTermCfg(func=fixed_support, weight=2.,
                                            params={"clearance_m": .04, "grounded_swing_cost": .25}),
            "pose_hint": RewardTermCfg(func=pose_hint, weight=.5),
            "support_leg_tilt": RewardTermCfg(func=support_leg_tilt, weight=-1.),
            "stationary": RewardTermCfg(func=stationary, weight=-.5),
            "action_rate": RewardTermCfg(func=native.action_rate_l2, weight=-.005),
            "dof_acc_l2": RewardTermCfg(func=mdp.reward, weight=-2.5e-7,
                                      params={"kind": "joint_acc_l2"}),
            "termination": RewardTermCfg(func=mdp.reward, weight=-10., params={"kind": "termination"}),
        }
        self.metrics = {
            name: MetricsTermCfg(func=balance_metric, params={"kind": kind}, reduce=reduce)
            for name, kind, reduce in (
                ("single_support_fraction", "single_support_fraction", "mean"),
                ("single_support_time_s", "single_support_time_s", "sum"),
                ("double_support_fraction", "double_support_fraction", "mean"),
                ("max_swing_clearance_m", "swing_clearance_m", "max"),
                ("pose_hint", "pose_hint", "mean"))}


class TitaStandOneLegRightReferenceEnvCfg(TitaStandOneLegReferenceEnvCfg):
    """Mirror the saved left-only objective without adding a command input."""

    def __init__(self, num_envs=1024, play=False):
        super().__init__(num_envs, play)
        for name in ("single_support", "pose_hint", "support_leg_tilt"):
            self.rewards[name].params["support_side"] = "right"
        for term in self.metrics.values():
            term.params["support_side"] = "right"
