# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""TRAINING_SIM: the selected TITA flat-terrain configuration.

Promoted from MyTitaFlatPosKneeSphereHeadingObsW0EnvCfg (headw0 50k/65k).
Final settings are declared here without inheriting experiment variants:
35 policy / 39 critic observations, sphere wheel collisions, plain leg position
actions, knee PD 92/2.3 with output randomization, and zero-warmup heading hold.
Commands retain the 0.5 ramp and +/-1.0 m/s, +/-1.5 rad/s ranges.

Selection and limitations: docs/exp/2026-10-19/flashsac_headw0_65000_153755_review.md.
The real-run position-hold and turning gaps documented there remain unresolved.
"""

import math

import isaaclab.sim as sim_utils
from isaaclab.actuators import DelayedPDActuatorCfg
from isaaclab.assets import ArticulationCfg, AssetBaseCfg
from isaaclab.envs import ManagerBasedRLEnvCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.managers import TerminationTermCfg as DoneTerm
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sensors import ContactSensorCfg
from isaaclab.terrains import TerrainImporterCfg
from isaaclab.utils import configclass
from isaaclab.utils.noise import AdditiveUniformNoiseCfg as Unoise

from ddt_lab.assets.ddt_robot import DDT_TITA_CFG
import ddt_lab.tasks.manager_based.locomotion.mdp as mdp

from .real2sim import events as real2sim_events
from .real2sim import observations as real2sim_observations
from .real2sim import rewards as real2sim_rewards
from .real2sim.env_cfg import sphere_wheel_urdf


@configclass
class SceneCfg(InteractiveSceneCfg):
    """Flat ground, delayed TITA actuators, contact sensor and lighting."""

    terrain = TerrainImporterCfg(
        prim_path="/World/ground",
        terrain_type="plane",
        terrain_generator=None,
        max_init_terrain_level=5,
        collision_group=-1,
        physics_material=sim_utils.RigidBodyMaterialCfg(
            friction_combine_mode="multiply",
            restitution_combine_mode="multiply",
            static_friction=1.0,
            dynamic_friction=1.0,
        ),
        visual_material=sim_utils.MdlFileCfg(
            mdl_path="{NVIDIA_NUCLEUS_DIR}/Materials/Base/Architecture/Shingles_01.mdl",
            project_uvw=True,
        ),
        debug_vis=False,
    )

    robot: ArticulationCfg = DDT_TITA_CFG.replace(
        prim_path="{ENV_REGEX_NS}/Robot",
        # DDT_TITA_CFG's inherited leg_1 = (+0.1, +0.1) is asymmetric because both
        # leg_1 axes point the same way; zero is the symmetric stand pose.
        init_state=DDT_TITA_CFG.init_state.replace(
            joint_pos={**DDT_TITA_CFG.init_state.joint_pos, "joint_left_leg_1": 0.0, "joint_right_leg_1": 0.0}
        ),
        spawn=DDT_TITA_CFG.spawn.replace(asset_path=sphere_wheel_urdf(DDT_TITA_CFG.spawn.asset_path)),
        actuators={
            # Delay is measured in 5 ms physics steps: 0..4 gives 0..20 ms.
            # DelayedPDActuator retains the current limits; it does not model
            # the base asset's DC motor torque-speed saturation.
            "legs": DelayedPDActuatorCfg(
                joint_names_expr=[".*_leg_[12]"],
                effort_limit=60.0,
                velocity_limit=30.0,
                stiffness=60.0,
                damping=1.5,
                friction=0.0,
                min_delay=0,
                max_delay=4,
            ),
            "knees": DelayedPDActuatorCfg(
                joint_names_expr=[".*_leg_3"],
                effort_limit=60.0,
                velocity_limit=30.0,
                stiffness=92.0,
                damping=2.3,
                friction=0.0,
                min_delay=0,
                max_delay=4,
            ),
            "wheels": DelayedPDActuatorCfg(
                joint_names_expr=[".*_leg_4"],
                effort_limit=12.0,
                velocity_limit=30.0,
                stiffness=0.0,
                damping=0.5,
                friction=0.0,
                min_delay=0,
                max_delay=4,
            ),
        },
    )

    height_scanner = None
    contact_forces = ContactSensorCfg(
        prim_path="{ENV_REGEX_NS}/Robot/.*", history_length=3, track_air_time=True
    )
    light = AssetBaseCfg(
        prim_path="/World/light",
        spawn=sim_utils.DistantLightCfg(color=(0.75, 0.75, 0.75), intensity=3000.0),
    )
    sky_light = AssetBaseCfg(
        prim_path="/World/skyLight",
        spawn=sim_utils.DomeLightCfg(color=(0.13, 0.13, 0.13), intensity=1000.0),
    )


@configclass
class CommandsCfg:
    """Ramped velocity targets with 10% standing command sampling."""

    base_velocity: mdp.RampedVelocityCommandCfg = mdp.RampedVelocityCommandCfg(
        asset_name="robot",
        resampling_time_range=(6.0, 8.0),
        rel_standing_envs=0.1,
        rel_heading_envs=0.0,
        heading_command=False,
        heading_control_stiffness=0.5,
        debug_vis=True,
        ranges=mdp.RampedVelocityCommandCfg.Ranges(
            lin_vel_x=(-1.0, 1.0),
            lin_vel_y=(-0.0, 0.0),
            ang_vel_z=(-1.5, 1.5),
            heading=(-3.14159265, 3.14159265),
        ),
        ramp_rate=0.5,
    )


@configclass
class ActionsCfg:
    """Eight native action terms, in deployment joint order."""

    joint_pos_0 = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=["joint_left_leg_1"],
        clip={".*": (-100.0, 100.0)},
        scale=0.25,
        use_default_offset=True,
        preserve_order=True,
    )
    joint_pos_1 = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=["joint_left_leg_2"],
        clip={".*": (-100.0, 100.0)},
        scale=0.25,
        use_default_offset=True,
        preserve_order=True,
    )
    joint_pos_2 = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=["joint_left_leg_3"],
        clip={".*": (-100.0, 100.0)},
        scale=0.25,
        use_default_offset=True,
        preserve_order=True,
    )
    joint_vel_3 = mdp.JointVelocityActionCfg(
        asset_name="robot",
        joint_names=["joint_left_leg_4"],
        clip={".*": (-100.0, 100.0)},
        scale=20.0,
        use_default_offset=True,
        preserve_order=True,
    )
    joint_pos_4 = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=["joint_right_leg_1"],
        clip={".*": (-100.0, 100.0)},
        scale=0.25,
        use_default_offset=True,
        preserve_order=True,
    )
    joint_pos_5 = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=["joint_right_leg_2"],
        clip={".*": (-100.0, 100.0)},
        scale=0.25,
        use_default_offset=True,
        preserve_order=True,
    )
    joint_pos_6 = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=["joint_right_leg_3"],
        clip={".*": (-100.0, 100.0)},
        scale=0.25,
        use_default_offset=True,
        preserve_order=True,
    )
    joint_vel_7 = mdp.JointVelocityActionCfg(
        asset_name="robot",
        joint_names=["joint_right_leg_4"],
        clip={".*": (-100.0, 100.0)},
        scale=20.0,
        use_default_offset=True,
        preserve_order=True,
    )


@configclass
class EstimatorTargetCfg(ObsGroup):
    """Noise-free, scaled base velocity target for PPO's learned estimator."""

    base_lin_vel = ObsTerm(func=mdp.base_lin_vel, clip=(-100.0, 100.0), scale=2.0)

    def __post_init__(self):
        self.enable_corruption = False
        self.concatenate_terms = True


@configclass
class ObservationsCfg:
    """Policy, ground-truth critic, privileged parameters and estimator target."""

    @configclass
    class PolicyCfg(ObsGroup):
        # Fixed per-episode biases are added by these observation functions;
        # the uniform noise remains the original per-step measurement noise.
        base_ang_vel = ObsTerm(
            func=mdp.base_ang_vel_biased,
            noise=Unoise(n_min=-0.2, n_max=0.2),
            clip=(-100.0, 100.0),
            scale=0.25,
        )
        projected_gravity = ObsTerm(
            func=mdp.projected_gravity_biased,
            noise=Unoise(n_min=-0.05, n_max=0.05),
            clip=(-100.0, 100.0),
            scale=1.0,
        )
        velocity_commands = ObsTerm(
            func=mdp.generated_commands,
            params={"command_name": "base_velocity"},
            clip=(-100.0, 100.0),
            scale=(2.0, 2.0, 0.25),
        )
        joint_pos = ObsTerm(
            func=mdp.joint_pos_rel_without_wheel_biased,
            params={
                "asset_cfg": SceneEntityCfg("robot", joint_names=".*", preserve_order=True),
                "wheel_asset_cfg": SceneEntityCfg("robot", joint_names=".*_leg_4"),
            },
            noise=Unoise(n_min=-0.01, n_max=0.01),
            clip=(-100.0, 100.0),
            scale=1.0,
        )
        joint_vel = ObsTerm(
            func=mdp.joint_vel_rel,
            params={"asset_cfg": SceneEntityCfg("robot", joint_names=".*", preserve_order=True)},
            noise=Unoise(n_min=-1.5, n_max=1.5),
            clip=(-100.0, 100.0),
            scale=0.05,
        )
        actions = ObsTerm(func=mdp.last_action, clip=(-100.0, 100.0), scale=1.0)

        wheel_position_error = ObsTerm(
            func=real2sim_observations.WheelPositionError,
            params={
                "command_name": "base_velocity",
                "radius": 0.0925,
                "radius_scale_range": (0.97, 1.03),
                "clip_m": 0.3,
                "zero_thresholds": (0.02, 0.02, 0.03),
            },
            noise=Unoise(n_min=-0.005, n_max=0.005),
            clip=(-100.0, 100.0),
            scale=5.0,
        )
        heading_error = ObsTerm(
            func=real2sim_observations.GyroHeadingError,
            params={
                "command_name": "base_velocity",
                "clip_rad": 0.5,
                "zero_thresholds": (0.02, 0.02, 0.03),
                "warmup_s": 0.0,
                "bias_range": (-0.0014, 0.0014),
            },
            noise=Unoise(n_min=-0.003, n_max=0.003),
            clip=(-100.0, 100.0),
            scale=2.0,
        )

        height_scan = None
        base_lin_vel = None
        enable_corruption = True
        concatenate_terms = True
        history_length = 0
        flatten_history_dim = False

    @configclass
    class CriticCfg(ObsGroup):
        """39 critic values, without policy noise or sensor biases."""

        base_lin_vel = ObsTerm(func=mdp.base_lin_vel, clip=(-100.0, 100.0), scale=2.0)
        base_ang_vel = ObsTerm(func=mdp.base_ang_vel, clip=(-100.0, 100.0), scale=0.25)
        projected_gravity = ObsTerm(func=mdp.projected_gravity, clip=(-100.0, 100.0), scale=1.0)
        velocity_commands = ObsTerm(
            func=mdp.generated_commands,
            params={"command_name": "base_velocity"},
            clip=(-100.0, 100.0),
            scale=(2.0, 2.0, 0.25),
        )
        joint_pos = ObsTerm(
            func=mdp.joint_pos_rel_without_wheel,
            params={
                "asset_cfg": SceneEntityCfg("robot", joint_names=".*", preserve_order=True),
                "wheel_asset_cfg": SceneEntityCfg("robot", joint_names=".*_leg_4"),
            },
            clip=(-100.0, 100.0),
            scale=1.0,
        )
        joint_vel = ObsTerm(
            func=mdp.joint_vel_rel,
            params={"asset_cfg": SceneEntityCfg("robot", joint_names=".*", preserve_order=True)},
            clip=(-100.0, 100.0),
            scale=0.05,
        )
        actions = ObsTerm(func=mdp.last_action, clip=(-100.0, 100.0), scale=1.0)
        wheel_position_error = ObsTerm(
            func=real2sim_observations.WheelPositionError,
            params={
                "command_name": "base_velocity",
                "radius": 0.0925,
                "radius_scale_range": (0.97, 1.03),
                "clip_m": 0.3,
                "zero_thresholds": (0.02, 0.02, 0.03),
            },
            noise=None,
            clip=(-100.0, 100.0),
            scale=5.0,
        )
        heading_drift_error = ObsTerm(
            func=real2sim_observations.heading_drift_error,
            params={"reward_term": "zero_command_heading_drift"},
            clip=(-3.2, 3.2),
            scale=2.0,
        )
        heading_error = ObsTerm(
            func=real2sim_observations.GyroHeadingError,
            params={
                "command_name": "base_velocity",
                "clip_rad": 0.5,
                "zero_thresholds": (0.02, 0.02, 0.03),
                "warmup_s": 0.0,
                "bias_range": (0.0, 0.0),
            },
            noise=None,
            clip=(-100.0, 100.0),
            scale=2.0,
        )

    @configclass
    class PrivCfg(ObsGroup):
        """Contact state and actuator gain factors, absent from actor inputs."""

        contact_state = ObsTerm(
            func=mdp.contact_state,
            params={"sensor_cfg": SceneEntityCfg("contact_forces", body_names=[".*_leg_4"])},
            clip=(-1.0, 1.0),
            scale=1.0,
        )
        joint_kp_factor = ObsTerm(
            func=mdp.joint_kp_factor,
            params={"asset_cfg": SceneEntityCfg("robot", joint_names=".*", preserve_order=True)},
            clip=(0.0, 2.0),
            scale=1.0,
        )
        joint_kd_factor = ObsTerm(
            func=mdp.joint_kd_factor,
            params={"asset_cfg": SceneEntityCfg("robot", joint_names=".*", preserve_order=True)},
            clip=(0.0, 2.0),
            scale=1.0,
        )

    policy: PolicyCfg = PolicyCfg()
    critic: CriticCfg = CriticCfg()
    priv: PrivCfg = PrivCfg()
    scanner = None
    estimator_target: EstimatorTargetCfg = EstimatorTargetCfg()


@configclass
class EventCfg:
    """Startup randomization, reset state/bias sampling and interval pushes."""

    physics_material = EventTerm(
        func=mdp.randomize_rigid_body_material,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names=".*"),
            "static_friction_range": (0.2, 1.6),
            "dynamic_friction_range": (0.2, 1.6),
            "restitution_range": (0.0, 1.0),
            "num_buckets": 64,
        },
    )
    add_base_mass = EventTerm(
        func=mdp.randomize_rigid_body_mass,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names="base_link"),
            "mass_distribution_params": (-0.5, 2.0),
            "operation": "add",
        },
    )
    add_base_inertia = EventTerm(
        func=mdp.randomize_rigid_body_inertia,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names=".*"),
            "inertia_distribution_params": (0.85, 1.15),
            "operation": "scale",
        },
    )
    add_base_com = EventTerm(
        func=mdp.randomize_rigid_body_com,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names="base_link"),
            "com_range": {"x": (-0.015, 0.015), "y": (-0.015, 0.015), "z": (-0.015, 0.015)},
        },
    )

    # No reset force/torque pulse in the selected configuration.
    base_external_force_torque = None
    randomize_actuator_gains = EventTerm(
        func=mdp.randomize_actuator_gains,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("robot", joint_names=[".*_leg_[124]"]),
            "stiffness_distribution_params": (0.8, 1.2),
            "damping_distribution_params": (0.8, 1.2),
            "operation": "scale",
            "distribution": "log_uniform",
        },
    )
    reset_base = EventTerm(
        func=mdp.reset_root_state_uniform,
        mode="reset",
        params={
            "pose_range": {"x": (-0.5, 0.5), "y": (-0.5, 0.5), "yaw": (-3.14, 3.14)},
            "velocity_range": {
                "x": (-0.5, 0.5),
                "y": (-0.5, 0.5),
                "z": (-0.5, 0.5),
                "roll": (-0.5, 0.5),
                "pitch": (-0.5, 0.5),
                "yaw": (-0.5, 0.5),
            },
        },
    )
    reset_robot_joints = EventTerm(
        func=mdp.reset_joints_by_scale,
        mode="reset",
        params={"position_range": (-0.5, 1.0), "velocity_range": (-0.0, 0.0)},
    )
    push_robot = EventTerm(
        func=mdp.push_by_setting_velocity,
        mode="interval",
        interval_range_s=(10.0, 15.0),
        params={"velocity_range": {"x": (-0.5, 0.5), "y": (-0.5, 0.5)}},
    )
    imu_bias = EventTerm(
        func=mdp.randomize_imu_bias,
        mode="reset",
        params={"gravity_bias_range": (-0.05, 0.05), "ang_vel_bias_range": (-0.05, 0.05)},
    )
    joint_offset = EventTerm(
        func=mdp.randomize_joint_offset,
        mode="reset",
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=".*"), "offset_range": (-0.02, 0.02)},
    )

    knee_output_scale = EventTerm(
        func=real2sim_events.randomize_actuator_output_scale,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("robot", joint_names=[".*_leg_3"]),
            "scale_range": (0.55, 1.0),
            "jitter_range": (0.8, 1.2),
        },
    )


@configclass
class RewardsCfg:
    """Current reward weights and parameters, declared at their final values."""

    track_lin_vel_xy_exp = RewTerm(
        func=mdp.track_lin_vel_xy_exp,
        weight=2.0,
        params={"command_name": "base_velocity", "std": math.sqrt(0.25)},
    )

    track_lin_vel_xy_exp_2 = RewTerm(
        func=mdp.track_lin_vel_xy_exp,
        weight=0.5,
        params={"command_name": "base_velocity", "std": math.sqrt(0.0625)},
    )

    track_lin_vel_xy_exp_3 = RewTerm(
        func=mdp.track_lin_vel_xy_exp,
        weight=0.5,
        params={"command_name": "base_velocity", "std": math.sqrt(0.03125)},
    )

    track_ang_vel_z_exp = RewTerm(
        func=mdp.track_ang_vel_z_exp,
        weight=1.0,
        params={"command_name": "base_velocity", "std": math.sqrt(0.25)},
    )

    lin_vel_z_l2 = RewTerm(func=mdp.lin_vel_z_l2, weight=-2.0)
    ang_vel_xy_l2 = RewTerm(func=mdp.ang_vel_xy_l2, weight=-0.05)
    dof_torques_l2 = RewTerm(func=mdp.joint_torques_l2, weight=-1.0e-5)
    dof_acc_l2 = RewTerm(func=mdp.joint_acc_l2, weight=-2.5e-7)
    action_rate_l2 = RewTerm(func=mdp.action_rate_l2, weight=-0.01)
    joint_mirror = RewTerm(
        func=mdp.joint_mirror,
        weight=-1.0,
        params={
            "asset_cfg": SceneEntityCfg("robot"),
            "mirror_joints": [
                [
                    ["joint_left_leg_1", "joint_left_leg_2", "joint_left_leg_3"],
                    ["joint_right_leg_1", "joint_right_leg_2", "joint_right_leg_3"],
                ]
            ],
            # leg_1 axes are parallel in the URDF, so symmetry is q_left = -q_right.
            "mirror_signs": [[-1.0, 1.0, 1.0]],
        },
    )
    stand_still = RewTerm(
        func=mdp.stand_still,
        weight=0.0,
        params={
            "command_name": "base_velocity",
            "command_threshold": 0.1,
            "asset_cfg": SceneEntityCfg("robot", joint_names=[".*_leg_4"]),
        },
    )
    undesired_contacts = RewTerm(
        func=mdp.undesired_contacts,
        weight=-1.0,
        params={"sensor_cfg": SceneEntityCfg("contact_forces", body_names=[".*_leg_3"]), "threshold": 1.0},
    )
    flat_orientation_l2 = RewTerm(func=mdp.flat_orientation_l2, weight=-5.0)
    base_height_l2 = RewTerm(func=mdp.base_height_l2, weight=-10.0, params={"target_height": 0.335})
    joint_deviation_hip = RewTerm(
        func=mdp.joint_deviation_l1,
        weight=-1.0,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=[".*_leg_1"])},
    )
    joint_deviation_shoulder = RewTerm(
        func=mdp.joint_deviation_l1,
        weight=-0.5,
        params={"asset_cfg": SceneEntityCfg("robot", joint_names=[".*_leg_2"])},
    )
    zero_command_position_drift = RewTerm(
        func=mdp.ZeroCommandPositionDrift,
        weight=1.0,
        params={
            "command_name": "base_velocity",
            "sharpness": 8.0,
            "command_threshold": 0.0,
            "warmup_s": 0.0,
            "use_z": False,
        },
    )
    zero_command_wheel_action = RewTerm(
        func=mdp.ZeroCommandWheelActionIntegralPenalty,
        weight=-0.05,
        params={
            "command_name": "base_velocity",
            "wheel_asset_cfg": SceneEntityCfg("robot", joint_names=".*_leg_4"),
            "exponent": 4.0,
            "integral_exponent": 0.5,
            "command_threshold": 0.0,
        },
    )

    zero_command_heading_drift = RewTerm(
        func=real2sim_rewards.ZeroCommandHeadingDrift,
        weight=1.0,
        params={"command_name": "base_velocity", "sharpness": 5.0, "command_threshold": 0.0, "warmup_s": 0.0},
    )


@configclass
class TerminationsCfg:
    """Time limit and forbidden base contact."""

    time_out = DoneTerm(func=mdp.time_out, time_out=True)
    base_contact = DoneTerm(
        func=mdp.illegal_contact,
        params={"sensor_cfg": SceneEntityCfg("contact_forces", body_names="base_link"), "threshold": 1.0},
    )


@configclass
class CurriculumCfg:
    """No terrain-level curriculum on the flat plane."""

    terrain_levels = None


@configclass
class TitaFlatEnvCfg(ManagerBasedRLEnvCfg):
    """Selected flat task, with all final settings declared in this module."""

    scene: SceneCfg = SceneCfg(num_envs=4096, env_spacing=2.5)
    observations: ObservationsCfg = ObservationsCfg()
    actions: ActionsCfg = ActionsCfg()
    commands: CommandsCfg = CommandsCfg()
    rewards: RewardsCfg = RewardsCfg()
    terminations: TerminationsCfg = TerminationsCfg()
    events: EventCfg = EventCfg()
    curriculum: CurriculumCfg = CurriculumCfg()

    decimation = 4
    episode_length_s = 20.0
    sim: sim_utils.SimulationCfg = sim_utils.SimulationCfg(
        dt=0.005,
        render_interval=4,
        physx=sim_utils.PhysxCfg(gpu_max_rigid_patch_count=10 * 2**15),
    )

    def __post_init__(self):
        # Connect shared settings; task-specific values are declared above.
        self.sim.render_interval = self.decimation
        self.sim.physics_material = self.scene.terrain.physics_material
        # Older task configs set this attribute after construction; Isaac Lab
        # 2.3 no longer accepts it as a SimulationCfg constructor argument.
        self.sim.disable_contact_processing = True
        if self.scene.contact_forces is not None:
            self.scene.contact_forces.update_period = self.sim.dt


@configclass
class TitaFlatEnvCfg_PLAY(TitaFlatEnvCfg):
    """Selected flat task with clean observations and no gain/bias randomization."""

    def __post_init__(self) -> None:
        super().__post_init__()

        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        self.observations.policy.enable_corruption = False

        self.events.base_external_force_torque = None
        self.events.push_robot = None
        self.events.add_base_inertia = None
        self.events.add_base_com = None
        self.events.add_base_mass = None
        self.events.randomize_actuator_gains = None
        self.events.knee_output_scale = None
        self.events.imu_bias = None
        self.events.joint_offset = None
