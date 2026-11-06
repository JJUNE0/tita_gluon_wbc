"""First CO-RL/MOO locomotion baseline for the combined TITA+GLUON robot.

This milestone intentionally leaves the TITA policy and MOO objective vector
unchanged.  GLUON is mounted as part of the same articulation and held at its
conditioned WORK posture by a separate implicit-PD action term.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

import isaaclab.sim as sim_utils
from isaaclab.actuators import DelayedPDActuatorCfg, ImplicitActuatorCfg
from isaaclab.assets import ArticulationCfg
from isaaclab.envs import mdp as isaaclab_mdp
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import CurriculumTermCfg as CurrTerm
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass
from isaaclab.utils.noise import AdditiveUniformNoiseCfg as Unoise

import ddt_lab.tasks.moo_based.locomotion.velocity.mdp as locomotion_mdp
from ddt_lab.gluon_ik import GLUON_WORK_JOINT_POS_RAD
from ddt_lab.tasks.moo_based.locomotion.velocity.tita_env.flat_env.stand_drive.flat_env_stand_drive_cfg import (
    TitaFlatEnvCfg_GTBaseVel_TargetHeight,
)

from . import mdp


REPO_ROOT = Path(__file__).resolve().parents[8]
TITA_GLUON_URDF_PATH = (
    REPO_ROOT / "sim2sim" / "robot" / "tita_gluon" / "urdf" / "tita_gluon_2L6_4L3.urdf"
)

TITA_JOINT_NAMES = (
    "joint_left_leg_1",
    "joint_right_leg_1",
    "joint_left_leg_2",
    "joint_right_leg_2",
    "joint_left_leg_3",
    "joint_right_leg_3",
    "joint_left_leg_4",
    "joint_right_leg_4",
)
GLUON_JOINT_NAMES = tuple(f"gluon_2L6_4L3_axis_joint_{index}" for index in range(1, 7))
GLUON_WORK_JOINT_POS = tuple(float(value) for value in GLUON_WORK_JOINT_POS_RAD)

# Conditioned stage-2 waypoint set.  Every waypoint is connected only to WORK;
# no direct waypoint-to-waypoint transition is allowed.  The dense straight
# joint paths were checked at the recorded TITA stand posture with 10 deg joint
# margin, sigma_min >= 0.015, and 15 mm Pinocchio/hpp-fcl clearance.  This is a
# conservative VALIDATION_SIM gate, not a physical-robot collision certificate.
GLUON_CONDITIONED_WAYPOINTS_RAD = (
    (0.30, 0.80, 1.60, 0.80, 0.00, 0.00),
    (-0.30, 0.80, 1.60, 0.80, 0.00, 0.00),
    (0.00, 0.95, 1.60, 0.80, 0.00, 0.00),
    (0.00, 0.80, 1.40, 0.80, 0.00, 0.00),
    (0.00, 0.80, 1.60, 1.00, 0.00, 0.00),
    (0.00, 0.80, 1.60, 0.80, -0.25, 0.00),
    (0.00, 0.80, 1.60, 0.80, 0.25, 0.00),
    (0.00, 0.80, 1.60, 0.80, 0.00, -0.35),
    (0.00, 0.80, 1.60, 0.80, 0.00, 0.35),
    (0.25, 0.90, 1.45, 0.95, 0.20, 0.25),
    (0.35, 0.65, 1.45, 1.00, -0.25, 0.30),
    (-0.35, 0.95, 1.75, 0.60, 0.25, -0.30),
)

# Four Go/No-Go inspection hubs, ordered LEFT_HIGH -> RIGHT_LOW -> LEFT_LOW ->
# RIGHT_HIGH.  Their WORK-to-hub rays are stored in the offline mesh-validated
# graph.  The node ids are graph-artifact ids (node 0 is WORK), not actuator ids.
GLUON_INSPECTION_GRAPH_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "tita_gluon_cartesian_work_hub_graph.npz"
)
GLUON_INSPECTION_GRAPH_NODE_IDS = (23, 111, 18, 208)
with np.load(GLUON_INSPECTION_GRAPH_PATH) as _inspection_graph:
    _inspection_graph_q = _inspection_graph["node_q_rad"]
    if _inspection_graph_q.ndim != 2 or _inspection_graph_q.shape[1] != 6:
        raise RuntimeError("inspection graph node_q_rad must have shape (N, 6)")
    if max(GLUON_INSPECTION_GRAPH_NODE_IDS) >= len(_inspection_graph_q):
        raise RuntimeError("inspection hub id is outside the graph artifact")
    GLUON_INSPECTION_HUBS_RAD = tuple(
        tuple(float(value) for value in _inspection_graph_q[node_id])
        for node_id in GLUON_INSPECTION_GRAPH_NODE_IDS
    )
    # The offline graph uses URDF hard limits, while the combined Isaac asset
    # contracts them by soft_joint_pos_limit_factor=0.8. Keep only nodes that
    # the runtime action term can command, and preserve a source-node mapping
    # for the four semantic targets and experiment evidence.
    _gluon_hard_lower = np.asarray((-3.0, -1.67079632679, -3.0, -3.0, -3.0, -3.0))
    _gluon_hard_upper = np.asarray((3.0, 1.42920367321, 3.0, 3.0, 3.0, 3.0))
    _gluon_soft_factor = 0.8
    _gluon_soft_margin = 0.5 * (1.0 - _gluon_soft_factor) * (
        _gluon_hard_upper - _gluon_hard_lower
    )
    _gluon_soft_lower = _gluon_hard_lower + _gluon_soft_margin
    _gluon_soft_upper = _gluon_hard_upper - _gluon_soft_margin
    _runtime_graph_mask = np.all(
        (_inspection_graph_q >= _gluon_soft_lower)
        & (_inspection_graph_q <= _gluon_soft_upper),
        axis=1,
    )
    GLUON_INSPECTION_GRAPH_SOURCE_NODE_IDS = tuple(
        int(value) for value in np.flatnonzero(_runtime_graph_mask)
    )
    _source_to_runtime_hub = {
        source_id: runtime_id
        for runtime_id, source_id in enumerate(GLUON_INSPECTION_GRAPH_SOURCE_NODE_IDS)
    }
    GLUON_INSPECTION_TARGET_HUB_INDICES = tuple(
        _source_to_runtime_hub[node_id] for node_id in GLUON_INSPECTION_GRAPH_NODE_IDS
    )
    # The sequential executor may choose any runtime-admissible WORK-connected
    # graph node at a station. The locomotion curriculum still uses only the
    # four semantic envelope hubs above.
    GLUON_INSPECTION_GRAPH_HUBS_RAD = tuple(
        tuple(float(value) for value in row)
        for row in _inspection_graph_q[_runtime_graph_mask]
    )
GLUON_TRAJECTORY_SEGMENT_DURATION_RANGE_S = (2.5, 4.0)
GLUON_TRAJECTORY_DWELL_TIME_RANGE_S = (0.25, 0.75)
GLUON_TRAJECTORY_MAX_VELOCITY_RAD_S = math.radians(20.0)
GLUON_TRAJECTORY_MAX_ACCELERATION_RAD_S2 = math.radians(40.0)
GLUON_CURRICULUM_START_STEP = 120_000
GLUON_CURRICULUM_END_STEP = 204_000
GLUON_INSPECTION_CURRICULUM_START_STEP = 120_000
GLUON_INSPECTION_CURRICULUM_END_STEP = 216_000

# Preserve the inherited CO-RL stack_policy order exactly.  The GT velocity /
# height terms are appended by the inherited config; the two GLUON terms are
# the only new actor inputs and appear at the tail in exactly this order.
CORL_TITA_STACK_POLICY_TERMS = (
    "hip_shoulder_joint_pos",
    "leg_joint_pos",
    "hip_shoulder_joint_vel",
    "joint_vel",
    "wheel_joint_vel",
    "base_ang_vel",
    "base_projected_gravity",
    "actions",
    "base_lin_vel_x",
    "base_lin_vel_y",
    "base_lin_vel_z",
    "base_height",
)
GLUON_POLICY_OBSERVATION_TERMS = ("gluon_joint_pos", "gluon_joint_vel")
TITA_GLUON_STACK_POLICY_TERMS = CORL_TITA_STACK_POLICY_TERMS + GLUON_POLICY_OBSERVATION_TERMS


TITA_GLUON_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        asset_path=str(TITA_GLUON_URDF_PATH),
        activate_contact_sensors=True,
        fix_base=False,
        # Keep frame-only TITA sensor links massless.  Without fixed-joint
        # merging, Isaac Sim promotes each inertial-less link to a 1 kg body.
        merge_fixed_joints=True,
        replace_cylinders_with_capsules=False,
        joint_drive=sim_utils.UrdfFileCfg.JointDriveCfg(
            gains=sim_utils.UrdfFileCfg.JointDriveCfg.PDGainsCfg(stiffness=0.0, damping=0.0)
        ),
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=8,
            solver_velocity_iteration_count=1,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.385),
        joint_pos={
            "joint_left_leg_1": 0.0,
            "joint_left_leg_2": 0.8,
            "joint_left_leg_3": -1.5,
            "joint_left_leg_4": 0.0,
            "joint_right_leg_1": 0.0,
            "joint_right_leg_2": 0.8,
            "joint_right_leg_3": -1.5,
            "joint_right_leg_4": 0.0,
            **dict(zip(GLUON_JOINT_NAMES, GLUON_WORK_JOINT_POS, strict=True)),
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.8,
    actuators={
        "tita_hip": DelayedPDActuatorCfg(
            joint_names_expr=[".*_leg_1"],
            effort_limit=55.0,
            velocity_limit=20.0,
            min_delay=0,
            max_delay=4,
            stiffness={".*_leg_1": 70.0},
            damping={".*_leg_1": 0.7},
            friction={".*_leg_1": 0.0},
            armature={".*_leg_1": 0.01},
        ),
        "tita_shoulder": DelayedPDActuatorCfg(
            joint_names_expr=[".*_leg_2"],
            effort_limit=55.0,
            velocity_limit=20.0,
            min_delay=0,
            max_delay=4,
            stiffness={".*_leg_2": 70.0},
            damping={".*_leg_2": 0.7},
            friction={".*_leg_2": 0.0},
            armature={".*_leg_2": 0.01},
        ),
        "tita_leg": DelayedPDActuatorCfg(
            joint_names_expr=[".*_leg_3"],
            effort_limit=55.0,
            velocity_limit=20.0,
            min_delay=0,
            max_delay=4,
            stiffness={".*_leg_3": 70.0},
            damping={".*_leg_3": 0.7},
            friction={".*_leg_3": 0.0},
            armature={".*_leg_3": 0.01},
        ),
        "tita_wheels": DelayedPDActuatorCfg(
            joint_names_expr=[".*_leg_4"],
            effort_limit=36.0,
            velocity_limit=50.0,
            min_delay=0,
            max_delay=4,
            stiffness={".*_leg_4": 0.0},
            damping={".*_leg_4": 0.55},
            friction={".*_leg_4": 0.0},
            armature={".*_leg_4": 0.01},
        ),
        "gluon_work_hold": ImplicitActuatorCfg(
            joint_names_expr=["gluon_2L6_4L3_axis_joint_[1-6]"],
            velocity_limit_sim={
                "gluon_2L6_4L3_axis_joint_[1-3]": 2.0943951023931953,
                "gluon_2L6_4L3_axis_joint_[4-6]": 3.490658503988659,
            },
            effort_limit_sim={
                "gluon_2L6_4L3_axis_joint_[1-2]": 18.0,
                "gluon_2L6_4L3_axis_joint_[3-6]": 10.0,
            },
            stiffness={
                "gluon_2L6_4L3_axis_joint_[1-2]": 80.0,
                "gluon_2L6_4L3_axis_joint_[3-6]": 40.0,
            },
            damping={
                "gluon_2L6_4L3_axis_joint_[1-2]": 4.0,
                "gluon_2L6_4L3_axis_joint_[3-6]": 2.0,
            },
            friction=0.0,
        ),
    },
)


@configclass
class TitaGluonFlatEnvCfg(TitaFlatEnvCfg_GTBaseVel_TargetHeight):
    """TITA velocity/height training with GLUON held at WORK."""

    def __post_init__(self):
        super().__post_init__()

        self.scene.robot = TITA_GLUON_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # Give the heavier combined articulation a deterministic reset stance:
        # zero planar/yaw command and 0.39 m height for the inherited 5 s init
        # phase, then blend to the normally sampled height over 1 s. Both actor
        # observations and height-aware rewards consume the command term's
        # public value, so they share this exact transition.
        self.commands.base_velocity.initial_phase_height = 0.39
        self.commands.base_velocity.initial_phase_height_transition_time = 1.0

        # Zero policy dimensions: the lower-level policy remains exactly the
        # validated eight-action TITA controller.
        self.actions.gluon_joint_reference = mdp.FixedJointPositionActionCfg(
            asset_name="robot",
            joint_names=list(GLUON_JOINT_NAMES),
            target_joint_pos=GLUON_WORK_JOINT_POS,
            preserve_order=True,
        )

        # Reset the physical arm state to the same target each episode.  The
        # action term resets its target buffer after events are applied.
        self.events.reset_gluon_joints = EventTerm(
            # Use the upstream subset-aware implementation explicitly.  The
            # locomotion package's same-named local function resets every
            # joint and would overwrite the TITA reset randomization.
            func=isaaclab_mdp.reset_joints_by_offset,
            mode="reset",
            params={
                "asset_cfg": SceneEntityCfg(
                    "robot", joint_names=list(GLUON_JOINT_NAMES), preserve_order=True
                ),
                "position_range": (0.0, 0.0),
                "velocity_range": (0.0, 0.0),
            },
        )

        # Keep every inherited CO-RL term in place and append arm state at the
        # tail of stack_policy.  No generic IsaacLab "policy" group is added.
        self.observations.stack_policy.gluon_joint_pos = ObsTerm(
            func=locomotion_mdp.joint_pos,
            params={
                "asset_cfg": SceneEntityCfg(
                    "robot", joint_names=list(GLUON_JOINT_NAMES), preserve_order=True
                )
            },
            noise=Unoise(n_min=-0.01, n_max=0.01),
        )
        self.observations.stack_policy.gluon_joint_vel = ObsTerm(
            func=locomotion_mdp.joint_vel,
            params={
                "asset_cfg": SceneEntityCfg(
                    "robot", joint_names=list(GLUON_JOINT_NAMES), preserve_order=True
                )
            },
            scale=0.05,
            noise=Unoise(n_min=-1.5, n_max=1.5),
        )

        # Existing TITA domain randomization used catch-all selectors.  Do not
        # silently perturb provisional GLUON gains/friction in this baseline.
        tita_joint_cfg = SceneEntityCfg(
            "robot", joint_names=list(TITA_JOINT_NAMES), preserve_order=True
        )
        self.domain.randomize_gains.params["asset_cfg"] = tita_joint_cfg
        self.domain.randomize_joints.params["asset_cfg"] = tita_joint_cfg
        # The imported custom startup inertia/COM functions only support an
        # all-body selector: their subset assignment returns a full-body
        # tensor and shape-mismatches on a combined articulation.  Disable
        # these two broad terms until arm payload randomization is defined
        # explicitly; base mass/COM and TITA actuator DR above remain active.
        self.events.add_base_inertia = None
        self.events.add_base_com = None


@configclass
class TitaGluonFlatEnvCfg_PLAY(TitaGluonFlatEnvCfg):
    """Small deterministic configuration for visualization and smoke tests."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 16
        self.observations.stack_policy.enable_corruption = False
        self.events.push_robot = None
        self.domain = None


@configclass
class TitaGluonRandomArmFlatEnvCfg(TitaGluonFlatEnvCfg):
    """TITA velocity/height training with a conditioned moving GLUON payload."""

    def __post_init__(self):
        super().__post_init__()
        self.actions.gluon_joint_reference = mdp.SmoothRandomJointPositionActionCfg(
            asset_name="robot",
            joint_names=list(GLUON_JOINT_NAMES),
            kinematic_urdf_path=str(TITA_GLUON_URDF_PATH),
            end_effector_link_name="gluon_2L6_4L3_link6",
            center_joint_pos=GLUON_WORK_JOINT_POS,
            waypoint_joint_pos=GLUON_CONDITIONED_WAYPOINTS_RAD,
            segment_duration_range_s=GLUON_TRAJECTORY_SEGMENT_DURATION_RANGE_S,
            dwell_time_range_s=GLUON_TRAJECTORY_DWELL_TIME_RANGE_S,
            max_velocity_rad_s=GLUON_TRAJECTORY_MAX_VELOCITY_RAD_S,
            max_acceleration_rad_s2=GLUON_TRAJECTORY_MAX_ACCELERATION_RAD_S2,
            preserve_order=True,
        )


@configclass
class TitaGluonRandomArmFlatEnvCfg_PLAY(TitaGluonRandomArmFlatEnvCfg):
    """Small deterministic-observation configuration for moving-arm validation."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 16
        self.observations.stack_policy.enable_corruption = False
        self.events.push_robot = None
        self.domain = None


@configclass
class TitaGluonSequentialInspectionFlatEnvCfg(TitaGluonFlatEnvCfg):
    """Low-level TITA environment with an externally requested arm-option FSM."""

    def __post_init__(self):
        super().__post_init__()
        self.actions.gluon_joint_reference = mdp.SequentialInspectionJointPositionActionCfg(
            asset_name="robot",
            joint_names=list(GLUON_JOINT_NAMES),
            kinematic_urdf_path=str(TITA_GLUON_URDF_PATH),
            end_effector_link_name="gluon_2L6_4L3_link6",
            center_joint_pos=GLUON_WORK_JOINT_POS,
            waypoint_joint_pos=GLUON_INSPECTION_GRAPH_HUBS_RAD,
            # The quintic velocity gate, rather than this nominal range,
            # determines long WORK-to-hub durations. Current semantic hubs
            # require roughly 14--16 s at 20 deg/s; this is intentionally
            # preserved until a faster low-level arm-motion curriculum is
            # validated.
            segment_duration_range_s=(0.5, 1.0),
            dwell_time_range_s=(0.0, 0.0),
            max_velocity_rad_s=GLUON_TRAJECTORY_MAX_VELOCITY_RAD_S,
            max_acceleration_rad_s2=GLUON_TRAJECTORY_MAX_ACCELERATION_RAD_S2,
            preserve_order=True,
        )


@configclass
class TitaGluonSequentialInspectionFlatEnvCfg_PLAY(
    TitaGluonSequentialInspectionFlatEnvCfg
):
    """Small deterministic configuration for headless option-executor tests."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 16
        self.observations.stack_policy.enable_corruption = False
        self.events.push_robot = None
        self.domain = None


@configclass
class TitaGluonCurriculumArmFlatEnvCfg(TitaGluonFlatEnvCfg):
    """Single pipeline: fixed WORK posture, then expanding conditioned motion.

    The inherited TITA height curriculum completes at rollout step 120,000.
    GLUON then expands from zero to the complete conditioned waypoint envelope
    by step 204,000 (iterations 5,000 to 8,500 at 24 steps per rollout).
    """

    def __post_init__(self):
        super().__post_init__()
        self.actions.gluon_joint_reference = mdp.SmoothRandomJointPositionActionCfg(
            asset_name="robot",
            joint_names=list(GLUON_JOINT_NAMES),
            kinematic_urdf_path=str(TITA_GLUON_URDF_PATH),
            end_effector_link_name="gluon_2L6_4L3_link6",
            center_joint_pos=GLUON_WORK_JOINT_POS,
            waypoint_joint_pos=GLUON_CONDITIONED_WAYPOINTS_RAD,
            segment_duration_range_s=GLUON_TRAJECTORY_SEGMENT_DURATION_RANGE_S,
            dwell_time_range_s=GLUON_TRAJECTORY_DWELL_TIME_RANGE_S,
            max_velocity_rad_s=GLUON_TRAJECTORY_MAX_VELOCITY_RAD_S,
            max_acceleration_rad_s2=GLUON_TRAJECTORY_MAX_ACCELERATION_RAD_S2,
            initial_workspace_scale=0.0,
            preserve_order=True,
        )
        self.curriculum.widen_gluon_workspace = CurrTerm(
            func=mdp.linearly_widen_gluon_workspace,
            params={
                "action_term_name": "gluon_joint_reference",
                "start_step": GLUON_CURRICULUM_START_STEP,
                "end_step": GLUON_CURRICULUM_END_STEP,
                "start_scale": 0.0,
                "end_scale": 1.0,
            },
        )


@configclass
class TitaGluonCurriculumArmFlatEnvCfg_PLAY(TitaGluonCurriculumArmFlatEnvCfg):
    """Small full-envelope visualization config for the curriculum task."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 16
        self.observations.stack_policy.enable_corruption = False
        self.events.push_robot = None
        self.domain = None
        self.actions.gluon_joint_reference.initial_workspace_scale = 1.0
        self.actions.gluon_joint_reference.debug_vis = True
        self.curriculum.widen_gluon_workspace = None


@configclass
class TitaGluonInspectionCurriculumArmFlatEnvCfg(TitaGluonFlatEnvCfg):
    """From-scratch low-level curriculum for the four inspection hubs.

    GLUON remains at WORK while the inherited TITA height curriculum widens
    through rollout step 120,000.  It then expands to the four inspection hubs
    through step 216,000, leaving 24,000 rollout steps for full-range
    consolidation in the 10,000-iteration teacher run.
    """

    def __post_init__(self):
        super().__post_init__()
        # Keep the domain-curriculum score consistent with the 0.5/0.5 ADD
        # reward mixture used by this experiment.  The inherited defaults are
        # 0.2 GAIL/discriminator and 0.8 feature matching.
        self.domain.w_gail = 0.5
        self.domain.w_fm = 0.5
        self.actions.gluon_joint_reference = mdp.SmoothRandomJointPositionActionCfg(
            asset_name="robot",
            joint_names=list(GLUON_JOINT_NAMES),
            kinematic_urdf_path=str(TITA_GLUON_URDF_PATH),
            end_effector_link_name="gluon_2L6_4L3_link6",
            center_joint_pos=GLUON_WORK_JOINT_POS,
            waypoint_joint_pos=GLUON_INSPECTION_HUBS_RAD,
            segment_duration_range_s=GLUON_TRAJECTORY_SEGMENT_DURATION_RANGE_S,
            dwell_time_range_s=GLUON_TRAJECTORY_DWELL_TIME_RANGE_S,
            max_velocity_rad_s=GLUON_TRAJECTORY_MAX_VELOCITY_RAD_S,
            max_acceleration_rad_s2=GLUON_TRAJECTORY_MAX_ACCELERATION_RAD_S2,
            initial_workspace_scale=0.0,
            preserve_order=True,
        )
        self.curriculum.widen_gluon_workspace = CurrTerm(
            func=mdp.linearly_widen_gluon_workspace,
            params={
                "action_term_name": "gluon_joint_reference",
                "start_step": GLUON_INSPECTION_CURRICULUM_START_STEP,
                "end_step": GLUON_INSPECTION_CURRICULUM_END_STEP,
                "start_scale": 0.0,
                "end_scale": 1.0,
            },
        )


@configclass
class TitaGluonInspectionCurriculumArmFlatEnvCfg_PLAY(
    TitaGluonInspectionCurriculumArmFlatEnvCfg
):
    """Small full-envelope visualization for the inspection curriculum."""

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 16
        self.observations.stack_policy.enable_corruption = False
        self.events.push_robot = None
        self.domain = None
        self.actions.gluon_joint_reference.initial_workspace_scale = 1.0
        self.actions.gluon_joint_reference.debug_vis = True
        self.curriculum.widen_gluon_workspace = None
