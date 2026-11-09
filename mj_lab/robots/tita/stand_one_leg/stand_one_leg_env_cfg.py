"""TRAINING_SIM: alternate single-leg balance at zero velocity, with free body tilt."""

import torch
from mjlab.envs import mdp as native
from mjlab.managers import RewardTermCfg

from ..common import mdp
from ..walk.inline_env_cfg import TitaInlineEnvCfg


def gait_support(env, clearance_m=.04, radius=.0925, contact_threshold=5.):
    """Reward clearance and penalize contact mismatches, without a body-tilt gate."""
    gait = env.command_manager.get_term("gait")
    stance, _ = mdp.gait_reference(gait.phase, gait.command[:, 0], gait.cfg.stance_fraction)
    contact = env.scene["feet"].data.force.norm(dim=-1) > contact_threshold
    correct_contact = (contact == stance).all(dim=1)
    # Each grounded swing foot or airborne stance foot contributes one error.
    contact_errors = (contact != stance).float().sum(dim=1)
    robot = env.scene["robot"]
    ids = [robot.body_names.index(name) for name in mdp.WHEELS]
    height = robot.data.body_link_pos_w[:, ids, 2] - env.scene.env_origins[:, 2:3] - radius
    # Partial clearance earns partial credit; lifting above the target adds none.
    clearance = (height / clearance_m).clamp(0., 1.)
    clearance = torch.where(stance, 1., clearance).prod(dim=1)
    walking = correct_contact.float() * clearance - contact_errors
    # Give immediate standing feedback before the first single-support cycle.
    standing = contact.all(dim=1).float()
    return torch.where(gait.command[:, 0].bool(), walking, standing)


def support_leg_tilt(env):
    """Penalize hip-to-wheel tilt only during requested single support."""
    gait = env.command_manager.get_term("gait")
    stance, _ = mdp.gait_reference(gait.phase, gait.command[:, 0], gait.cfg.stance_fraction)
    robot = env.scene["robot"]
    hips = [robot.body_names.index(f"{side}_leg_2") for side in ("left", "right")]
    wheels = [robot.body_names.index(name) for name in mdp.WHEELS]
    axis = robot.data.body_link_pos_w[:, hips] - robot.data.body_link_pos_w[:, wheels]
    vertical_cosine = axis[:, :, 2] / axis.norm(dim=-1).clamp_min(1e-6)
    tilt = 1. - vertical_cosine.clamp(-1., 1.)
    single_support = (stance.sum(dim=1) == 1) & gait.command[:, 0].bool()
    return (tilt * stance).sum(dim=1) * single_support


def stationary(env, yaw_scale=.1):
    """Discourage ground-plane drift and yaw spin, allowing body roll/pitch."""
    data = mdp.data(env)
    return (data.root_link_lin_vel_w[:, :2].square().sum(dim=1)
            + yaw_scale * data.root_link_ang_vel_w[:, 2].square())


class TitaStandOneLegEnvCfg(TitaInlineEnvCfg):
    def __init__(self, num_envs=1024, play=False):
        super().__init__(num_envs, play)
        velocity = self.commands["base_velocity"]
        velocity.lin_vel_x = velocity.lin_vel_y = velocity.ang_vel_z = (0., 0.)
        velocity.rel_straight_envs, velocity.rel_standing_envs = 0., 1.
        gait = self.commands["gait"]
        gait.step_in_place, gait.straight_only = True, False
        gait.frequency_range_hz, gait.stance_fraction = (.5, .5), .75
        gait.settle_time_s = 2.
        self.events["reset_joints"].params["position_range"] = (1., 1.)
        velocities = self.events["reset_base"].params["velocity_range"]
        self.events["reset_base"].params["velocity_range"] = {name: (0., 0.) for name in velocities}
        # The existing observation/action, wheel balance, PD and DR are retained.
        # No joint imitation, body-upright, height or COM-placement objectives.
        self.rewards = {
            "gait_support": RewardTermCfg(func=gait_support, weight=2., params={"clearance_m": .04}),
            "support_leg_tilt": RewardTermCfg(func=support_leg_tilt, weight=-1.),
            "stationary": RewardTermCfg(func=stationary, weight=-.5),
            "action_rate": RewardTermCfg(func=native.action_rate_l2, weight=-.005),
            "dof_acc_l2": RewardTermCfg(func=mdp.reward, weight=-2.5e-7, params={"kind": "joint_acc_l2"}),
            "termination": RewardTermCfg(func=mdp.reward, weight=-10., params={"kind": "termination"}),
        }


def make_stand_one_leg_env_cfg(num_envs=1024, play=False):
    return TitaStandOneLegEnvCfg(num_envs, play)
