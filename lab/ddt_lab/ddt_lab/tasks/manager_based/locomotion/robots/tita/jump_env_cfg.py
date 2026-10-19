# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""TITA flat env + squat/jump command.

Adds a discrete jump command (-1 squat / 0 flat / +1 jump-trigger) on top of
the rough-derived flat baseline (independent of the promoted flat task):

  jump_cmd == 0  -- identical to plain flat locomotion.
  jump_cmd == -1 -- sustained while held; base velocity command forced to
                    zero (squat is stationary-only in this first version);
                    base height target lowered to 0.22 m.
  jump_cmd == +1 -- one-shot trigger (exactly 1 control step, then the
                    command auto-reverts to 0); rewards base height rising
                    toward 0.5 m, gated behind actually leaving the ground.

Kinematic note: FK over the leg chain shows the maximum *static* (feet-on-
ground) base height is ~0.45 m -- below the 0.5 m jump target. Reaching 0.5 m
therefore requires a genuine push-off + short airborne phase, not just leg
extension; ``mdp.JumpReward`` gates its bonus on the robot having actually
left the ground during the evaluation window.

This is a new/independent obs interface (33 -> 34 dims, extra ``jump_cmd``
term) -- it does not touch ``deploy/tita/policy.onnx`` or any existing task.
No curriculum in this first pass; action scale, torque/velocity limits, and
command ranges are unchanged from the base flat task.
"""

from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

import ddt_lab.tasks.manager_based.locomotion.mdp as mdp

from .rough_env_cfg import CommandsCfg, ObservationsCfg, RewardsCfg, TitaRoughEnvCfg


@configclass
class JumpCommandsCfg(CommandsCfg):
    """base_velocity (inherited) + jump. jump must stay declared after
    base_velocity so it can zero it out on squat envs each step."""

    jump: mdp.JumpCommandCfg = mdp.JumpCommandCfg(
        resampling_time_range=(2.0, 5.0),
        squat_prob=0.3,
        pulse_steps=1,
        cooldown_s=3.0,
        mean_trigger_interval_s=4.0,
        debug_vis=False,
    )


@configclass
class JumpObservationsCfg(ObservationsCfg):
    """Adds the raw jump command scalar to policy + critic groups."""

    @configclass
    class PolicyCfg(ObservationsCfg.PolicyCfg):
        jump_cmd = ObsTerm(func=mdp.generated_commands, params={"command_name": "jump"}, clip=(-1.0, 1.0), scale=1.0)

    @configclass
    class CriticCfg(ObservationsCfg.CriticCfg):
        jump_cmd = ObsTerm(func=mdp.generated_commands, params={"command_name": "jump"}, clip=(-1.0, 1.0), scale=1.0)

    policy: PolicyCfg = PolicyCfg()
    critic: CriticCfg = CriticCfg()


@configclass
class JumpRewardsCfg(RewardsCfg):
    """Base-height target now depends on jump_cmd; adds the jump bonus term."""

    base_height_l2 = RewTerm(
        func=mdp.base_height_mode_l2,
        weight=-10.0,
        params={"command_name": "jump", "target_height_flat": 0.3, "target_height_squat": 0.22},
    )
    jump_bonus = RewTerm(
        func=mdp.JumpReward,
        weight=1.0,
        params={
            "command_name": "jump",
            "sensor_cfg": SceneEntityCfg("contact_forces", body_names=[".*_leg_4"]),
            "ref_height": 0.3,
            "target_height": 0.5,
            "eval_window_s": 0.6,
            "airborne_bonus": 0.5,
        },
    )


@configclass
class TitaJumpEnvCfg(TitaRoughEnvCfg):
    """TITA flat env with the squat/jump command layered on top."""

    commands: JumpCommandsCfg = JumpCommandsCfg()
    observations: JumpObservationsCfg = JumpObservationsCfg()
    rewards: JumpRewardsCfg = JumpRewardsCfg()

    def __post_init__(self):
        super().__post_init__()
        # Preserve the original jump task's flat terrain and observation interface.
        self.scene.terrain.terrain_type = "plane"
        self.scene.terrain.terrain_generator = None
        self.scene.height_scanner = None
        self.observations.policy.height_scan = None
        self.observations.scanner = None
        self.curriculum.terrain_levels = None


class TitaJumpEnvCfg_PLAY(TitaJumpEnvCfg):
    def __post_init__(self) -> None:
        # post init of parent
        super().__post_init__()

        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
        # remove random pushing
        self.events.base_external_force_torque = None
        self.events.push_robot = None
        self.events.add_base_inertia = None
        self.events.add_base_com = None
        self.events.add_base_mass = None
        self.events.randomize_actuator_gains = None
