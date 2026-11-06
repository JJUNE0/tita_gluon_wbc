"""TRAINING_SIM: TITA alternating-walk baseline with wheel braking.

Policy/critic: 39/43 observations; native actions: 8, wheel targets masked to
zero. Wheel PD gains are inherited from the driving task (Kp=0, Kd=0.5),
with its 12 Nm torque limit. This is not a mechanical wheel lock.
Actuator delays, gain randomization and knee output scaling follow the driving task.
After reset settling, the gait runs continuously, including at zero velocity.
Use weights-only warm-start to retain a policy while building a new task config.
"""

from isaaclab.managers import ObservationTermCfg as ObsTerm, RewardTermCfg as RewTerm, SceneEntityCfg
from isaaclab.managers import TerminationTermCfg as DoneTerm
from isaaclab.utils import configclass

import ddt_lab.tasks.manager_based.locomotion.mdp as mdp

from . import walk_mdp
from .flat_env_cfg import CommandsCfg, ObservationsCfg, RewardsCfg, TerminationsCfg, TitaFlatEnvCfg

WHEELS = ["left_leg_4", "right_leg_4"]
KNEES = ["left_leg_3", "right_leg_3"]


@configclass
class WalkCommandsCfg(CommandsCfg):
    # base_velocity updates first; gait reads it without changing it. Sample
    # gait parameters on reset, not mid-stride during these 20-second episodes.
    gait: walk_mdp.WalkGaitCommandCfg = walk_mdp.WalkGaitCommandCfg(
        resampling_time_range=(1.0e9, 1.0e9), debug_vis=False, step_in_place=True,
    )


@configclass
class WalkObservationsCfg(ObservationsCfg):
    @configclass
    class PolicyCfg(ObservationsCfg.PolicyCfg):
        wheel_position_error = None  # Encoder odometry is invalid during legged translation.
        gait = ObsTerm(func=mdp.generated_commands, params={"command_name": "gait"})

    @configclass
    class CriticCfg(ObservationsCfg.CriticCfg):
        wheel_position_error = None
        gait = ObsTerm(func=mdp.generated_commands, params={"command_name": "gait"})

    policy: PolicyCfg = PolicyCfg()
    critic: CriticCfg = CriticCfg()


@configclass
class WalkRewardsCfg(RewardsCfg):
    # Simultaneous L/R pose symmetry opposes alternate steps. Inherit all
    # common weights except the operator-selected hip and angular-rate terms.
    joint_mirror = None
    zero_command_wheel_action = None
    joint_deviation_hip = RewardsCfg().joint_deviation_hip.replace(weight=-0.1)
    ang_vel_xy_l2 = None
    ang_vel_roll_l2 = RewTerm(func=walk_mdp.ang_vel_axis_l2, weight=-0.02, params={"axis": 0})
    ang_vel_pitch_l2 = RewTerm(func=walk_mdp.ang_vel_axis_l2, weight=-0.1, params={"axis": 1})
    gait_contact = RewTerm(
        func=walk_mdp.contact_schedule, weight=2.0,
        params={"gait_name": "gait", "sensor_cfg": SceneEntityCfg(
            "contact_forces", body_names=WHEELS, preserve_order=True)},
    )
    gait_clearance = RewTerm(
        func=walk_mdp.wheel_clearance, weight=1.0,
        params={"gait_name": "gait", "asset_cfg": SceneEntityCfg(
            "robot", body_names=WHEELS, preserve_order=True), "clearance_m": 0.04},
    )
    termination = RewTerm(func=mdp.is_terminated, weight=-10.0)


@configclass
class WalkTerminationsCfg(TerminationsCfg):
    """A knee/leg-3 link must not act as an extra support on the ground."""

    knee_contact = DoneTerm(
        func=mdp.illegal_contact,
        time_out=False,
        params={"sensor_cfg": SceneEntityCfg("contact_forces", body_names=KNEES, preserve_order=True),
                "threshold": 1.0},
    )


@configclass
class TitaWalkEnvCfg(TitaFlatEnvCfg):
    commands: WalkCommandsCfg = WalkCommandsCfg()
    observations: WalkObservationsCfg = WalkObservationsCfg()
    rewards: WalkRewardsCfg = WalkRewardsCfg()
    terminations: WalkTerminationsCfg = WalkTerminationsCfg()

    def __post_init__(self):
        super().__post_init__()
        velocity = self.commands.base_velocity
        velocity.ranges.lin_vel_x = (-0.5, 0.5)
        velocity.ranges.lin_vel_y = (-0.5, 0.5)
        velocity.ranges.ang_vel_z = (0.0, 0.0)
        velocity.ramp_rate = 0.3
        velocity.initial_phase_time = self.commands.gait.settle_time_s
        velocity.debug_vis = False
        self.scene.contact_forces.track_air_time = True
        # Check all four 5-ms physics samples at each 20-ms control step.
        self.scene.contact_forces.history_length = self.decimation

        # Preserve the 8-entry native order used by the FlashSAC gain adapter.
        # Both wheel actions stay zero even after piecewise gain scaling.
        self.actions.joint_vel_3.scale = 0.0
        self.actions.joint_vel_7.scale = 0.0

        # Retain the driving task's delays, gain randomization and knee output
        # scaling. Other bootstrap settings below are unchanged.
        for name in ("push_robot", "add_base_mass", "add_base_inertia", "add_base_com",
                     "imu_bias", "joint_offset"):
            setattr(self.events, name, None)
        self.events.physics_material.params.update(
            static_friction_range=(0.8, 1.2), dynamic_friction_range=(0.8, 1.2), restitution_range=(0.0, 0.0),
        )
        self.events.reset_base.params["velocity_range"] = {
            axis: (0.0, 0.0) for axis in ("x", "y", "z", "roll", "pitch", "yaw")
        }
        self.events.reset_robot_joints.params["position_range"] = (1.0, 1.0)


@configclass
class TitaWalkInPlaceEnvCfg(TitaWalkEnvCfg):
    """Acquire alternating contacts/clearance with zero velocity command."""

    def __post_init__(self):
        super().__post_init__()
        self.commands.base_velocity.ranges.lin_vel_x = (0.0, 0.0)
        self.commands.base_velocity.ranges.lin_vel_y = (0.0, 0.0)
        self.commands.gait.step_in_place = True


@configclass
class TitaWalkEnvCfg_PLAY(TitaWalkEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 16
        self.observations.policy.enable_corruption = False
