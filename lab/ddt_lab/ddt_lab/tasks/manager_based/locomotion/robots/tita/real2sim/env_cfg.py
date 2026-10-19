"""Real-to-sim robustness variants of the My flat TITA task (TRAINING_SIM only).

Identical to ``MyTitaFlatEnvCfg`` -- 33 policy observations, 8 actions, action scales/offsets,
PD gains, effort limits, rewards, commands and terminations -- except the domain-randomization
events changed below, so an exported policy keeps the deployed interface.

The ranges are robustness exploration ranges around nominal (1.0, frictionless) and the
MuJoCo-equivalent real-to-sim candidates (effective leg output scale 0.6, leg friction ~2 N m,
wheel friction ~0.3 N m). They are not measured hardware ranges: firmware-reported torque tracked
the command (gain ~1.0) while external Nm calibration is still missing. See
``docs/exp/2026-10-17/flashsac_retrain_prep.md``.
"""

import hashlib
import os
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET

from isaaclab.envs.mdp import JointPositionActionCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass
from isaaclab.utils.noise import AdditiveUniformNoiseCfg as Unoise

from ..my_flat_env_cfg import MyTitaFlatEnvCfg
from . import actions as real2sim_actions
from . import events as real2sim_events
from . import observations as real2sim_observations
from . import rewards as real2sim_rewards

LEG_JOINTS = [".*_leg_[1-3]"]
WHEEL_JOINTS = [".*_leg_4"]
# Base-only CoM offset range shared by the CoM-shift arms (see MyTitaFlatBaseComShiftEnvCfg).
BASE_COM_SHIFT_RANGE = {"x": (-0.055, -0.015), "y": (-0.02, 0.02), "z": (-0.03, 0.03)}
# Arm B': same, but x also covers the URDF value so nominal CoM stays inside the distribution.
BASE_COM_SHIFT_RANGE_WITH_ZERO = {"x": (-0.055, 0.005), "y": (-0.02, 0.02), "z": (-0.03, 0.03)}
# Arms C1/C2: the vendor stand put the URDF CoM within ~1 cm of the wheel contacts.
BASE_COM_URDF_RANGE = {"x": (-0.015, 0.015), "y": (-0.015, 0.015), "z": (-0.015, 0.015)}
# Vendor controller quiet stand (2026-10-18), native order hip/thigh/knee for left then right.
VENDOR_STAND_JOINTS = ["joint_left_leg_1", "joint_left_leg_2", "joint_left_leg_3",
                       "joint_right_leg_1", "joint_right_leg_2", "joint_right_leg_3"]
VENDOR_STAND_POSE = [0.0, 1.09, -2.16, 0.0, 1.09, -2.16]


def _shift_base_com(events, com_range=BASE_COM_SHIFT_RANGE) -> None:
    """Randomize only the base CoM inside ``com_range`` (default: x centred 3.5 cm behind URDF)."""
    com = events.add_base_com
    events.add_base_com = com.replace(
        params={
            **com.params,
            "asset_cfg": SceneEntityCfg("robot", body_names="base_link"),
            "com_range": dict(com_range),
        }
    )


@configclass
class MyTitaFlatReal2SimEnvCfg(MyTitaFlatEnvCfg):
    """R1: actuator/friction robustness arm. All other randomization is unchanged."""

    def __post_init__(self):
        super().__post_init__()
        # Wheels keep the previous independent log-uniform +-20 % Kp/Kd variation.
        gains = self.events.randomize_actuator_gains
        self.events.randomize_actuator_gains = gains.replace(
            params={**gains.params, "asset_cfg": SceneEntityCfg("robot", joint_names=WHEEL_JOINTS)}
        )
        # Legs: one shared Kp/Kd scale per env (effective output scale below saturation) on top of
        # the same +-20 % per-joint jitter the original term applied.
        self.events.leg_actuator_output_scale = EventTerm(
            func=real2sim_events.randomize_actuator_output_scale,
            mode="reset",
            params={
                "asset_cfg": SceneEntityCfg("robot", joint_names=LEG_JOINTS),
                "scale_range": (0.5, 1.05),
                "jitter_range": (0.8, 1.2),
            },
        )
        # Coulomb joint friction in N m on this Isaac Sim 5.1 install (checked; see module docstring).
        self.events.leg_joint_friction = EventTerm(
            func=real2sim_events.randomize_joint_coulomb_friction,
            mode="startup",
            params={
                "asset_cfg": SceneEntityCfg("robot", joint_names=LEG_JOINTS),
                "static_range": (0.0, 4.0),
                "dynamic_ratio_range": (0.8, 1.0),
            },
        )
        self.events.wheel_joint_friction = EventTerm(
            func=real2sim_events.randomize_joint_coulomb_friction,
            mode="startup",
            params={
                "asset_cfg": SceneEntityCfg("robot", joint_names=WHEEL_JOINTS),
                "static_range": (0.0, 0.4),
                "dynamic_ratio_range": (0.8, 1.0),
            },
        )


@configclass
class MyTitaFlatBaseComShiftEnvCfg(MyTitaFlatEnvCfg):
    """CoM-only arm (operator decision 2026-10-17: IMU considered fine, CoM the main issue, no
    actuator/friction change). Only ``add_base_com`` differs from ``MyTitaFlatEnvCfg``:

    - before: every body (base, legs, wheels) gets an independent CoM offset in +-0.10 m (x, y, z);
    - after: only ``base_link``; x in [-0.055, -0.015] m (centre -0.035 m), y +-0.02 m, z +-0.03 m.

    The x centre comes from the MuJoCo CoM-only sweep with nominal legs (real pitch 1.78 deg is
    matched near -3.5..-4 cm); the range also covers the -2 cm of the leg-coefficient candidate C.
    It is an exploration range, not a measured CoM.
    """

    def __post_init__(self):
        super().__post_init__()
        _shift_base_com(self.events)


@configclass
class MyTitaFlatReal2SimBaseComShiftEnvCfg(MyTitaFlatReal2SimEnvCfg):
    """Arm B: R1 leg actuator-scale/joint-friction randomization plus the arm-A base CoM shift.

    Pairs with ``MyTitaFlatBaseComShiftEnvCfg`` (arm A, CoM only): same CoM range, so any
    difference between the two arms comes from the R1 events.
    """

    def __post_init__(self):
        super().__post_init__()
        _shift_base_com(self.events)


@configclass
class MyTitaFlatReal2SimNominalMixEnvCfg(MyTitaFlatReal2SimBaseComShiftEnvCfg):
    """Arm B': arm B with half of the environments at nominal leg strength (shared factor 1.0,
    per-joint jitter kept) and a base CoM x range that includes the URDF value.

    Targets the B sim2sim findings (2-3.6 Hz limit cycle at nominal leg strength in every
    checkpoint, forward drift at CoM 0) while keeping B's weak-leg robustness
    (``docs/exp/2026-10-18/flashsac_ab_sim2sim_report.md``).
    """

    def __post_init__(self):
        super().__post_init__()
        scale = self.events.leg_actuator_output_scale
        self.events.leg_actuator_output_scale = scale.replace(params={**scale.params, "nominal_probability": 0.5})
        _shift_base_com(self.events, BASE_COM_SHIFT_RANGE_WITH_ZERO)


@configclass
class MyTitaFlatReal2SimBaseComEnvCfg(MyTitaFlatReal2SimEnvCfg):
    """R2: R1 plus CoM randomization restricted to the base (original: +-0.1 m on every body,
    including the 0.0925 m-radius wheels). The real-to-sim fit could not separate a base CoM x
    shift from an IMU pitch offset (about 1 cm per 1 deg); IMU bias randomization is unchanged."""

    def __post_init__(self):
        super().__post_init__()
        com = self.events.add_base_com
        self.events.add_base_com = com.replace(
            params={
                **com.params,
                "asset_cfg": SceneEntityCfg("robot", body_names="base_link"),
                "com_range": {"x": (-0.03, 0.03), "y": (-0.02, 0.02), "z": (-0.03, 0.03)},
            }
        )


@configclass
class MyTitaFlatLegScaleEnvCfg(MyTitaFlatReal2SimEnvCfg):
    """Arm C1: physics correction only (rewards/commands unchanged).

    Real stance torque ratios (URDF static / commanded or firmware Nm) were 0.59-0.73 for the vendor
    controller, R0 and A 80k, matching the dynamic grid's 0.60
    (``docs/exp/2026-10-18/vendor_lqr_vs_rl_claude_analysis.md``). Legs therefore train around that
    output scale instead of 1.0; the base CoM stays near the URDF value, which the vendor stand
    confirmed to within ~1 cm. Joint friction keeps a reduced range (weakly identified).
    """

    def __post_init__(self):
        super().__post_init__()
        scale = self.events.leg_actuator_output_scale
        self.events.leg_actuator_output_scale = scale.replace(
            params={**scale.params, "scale_range": (0.55, 0.78), "jitter_range": (0.9, 1.1)}
        )
        friction = self.events.leg_joint_friction
        self.events.leg_joint_friction = friction.replace(params={**friction.params, "static_range": (0.0, 2.0)})
        _shift_base_com(self.events, BASE_COM_URDF_RANGE)


@configclass
class MyTitaFlatLegScaleRewardEnvCfg(MyTitaFlatLegScaleEnvCfg):
    """Arm C2: C1 plus zero-command shaping taken from the vendor controller stand.

    Vendor stand (60 s): body pitch 1.4 deg, hips 0, thigh ~1.09 rad, knee ~-2.16 rad, base height
    ~0.28 m (FK), net wheel travel -1.8 cm. The terms pull the policy toward that stand only while the
    command is ~zero; command tracking terms are unchanged.
    """

    def __post_init__(self):
        super().__post_init__()
        height = self.rewards.base_height_l2
        self.rewards.base_height_l2 = height.replace(params={**height.params, "target_height": 0.28})
        self.rewards.flat_orientation_l2 = self.rewards.flat_orientation_l2.replace(weight=-15.0)
        self.rewards.joint_deviation_hip = self.rewards.joint_deviation_hip.replace(weight=-2.5)
        drift = self.rewards.zero_command_position_drift
        self.rewards.zero_command_position_drift = drift.replace(params={**drift.params, "sharpness": 20.0})
        self.rewards.zero_command_stand_pose = RewTerm(
            func=real2sim_rewards.zero_command_stand_pose_l1,
            weight=-0.5,
            params={
                "command_name": "base_velocity",
                "target": VENDOR_STAND_POSE,
                "command_threshold": 0.05,
                "asset_cfg": SceneEntityCfg("robot", joint_names=VENDOR_STAND_JOINTS, preserve_order=True),
            },
        )
        self.rewards.zero_command_lin_vel = RewTerm(
            func=real2sim_rewards.zero_command_lin_vel_l2,
            weight=-4.0,
            params={"command_name": "base_velocity", "command_threshold": 0.0},
        )
        self.commands.base_velocity.rel_standing_envs = 0.2


LEG_ACTION_TERMS = ("joint_pos_0", "joint_pos_1", "joint_pos_2", "joint_pos_4", "joint_pos_5", "joint_pos_6")


@configclass
class MyTitaFlatPosKneeMA2EnvCfg(MyTitaFlatEnvCfg):
    """A80k successor (2026-10-18 real-run review, ``docs/exp/2026-10-18/real_runs_vs_training.md``).

    Same as ``MyTitaFlatEnvCfg`` (the base of arm A) except:

    1. Base-only CoM randomization of +-1.5 cm around URDF. Arm A used x -5.5..-1.5 cm; the vendor stand put
       the URDF CoM within ~1 cm of the wheel contacts.
    2. A 34th policy observation, ``wheel_position_error``: encoder/IMU wheel odometry, latched at zero
       command, in metres, clip +-0.3, scale 5, noise +-5 mm, wheel radius x U(0.97, 1.03). Also added to
       the critic without noise.
    3. Leg action MA2 filter in the training loop (``leg_action_filter:=ma2_legs`` on the robot). Wheels
       pass through and ``last_action`` stays raw.
    4. Knees: PD 92/2.3 (deployed knee-only gains) with a knee-only output scale log-U[0.55, 1.0] x
       per-joint jitter 0.8-1.2. The real knee needs about 1/0.65 of the URDF torque. Hips and shoulders keep
       60/1.5 with the original independent +-20 % Kp/Kd randomization. No leg weakening.

    Policy interface: 34 observations. The deployed 33-observation pipeline (export, sim2sim, tita_node)
    must add the same observation before this policy can run outside training.
    """

    def __post_init__(self):
        super().__post_init__()
        _shift_base_com(self.events, BASE_COM_URDF_RANGE)
        legs = self.scene.robot.actuators["legs"]
        self.scene.robot.actuators = {
            "legs": legs.replace(joint_names_expr=[".*_leg_[12]"]),
            "knees": legs.replace(joint_names_expr=[".*_leg_3"], stiffness=92.0, damping=2.3),
            "wheels": self.scene.robot.actuators["wheels"],
        }
        gains = self.events.randomize_actuator_gains
        self.events.randomize_actuator_gains = gains.replace(
            params={**gains.params, "asset_cfg": SceneEntityCfg("robot", joint_names=[".*_leg_[124]"])}
        )
        self.events.knee_output_scale = EventTerm(
            func=real2sim_events.randomize_actuator_output_scale,
            mode="reset",
            params={
                "asset_cfg": SceneEntityCfg("robot", joint_names=[".*_leg_3"]),
                "scale_range": (0.55, 1.0),
                "jitter_range": (0.8, 1.2),
            },
        )
        for name in LEG_ACTION_TERMS:
            term = getattr(self.actions, name)
            setattr(self.actions, name, real2sim_actions.MA2JointPositionActionCfg(
                asset_name=term.asset_name, joint_names=term.joint_names, clip=term.clip, scale=term.scale,
                use_default_offset=term.use_default_offset, preserve_order=term.preserve_order))
        position = ObsTerm(
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
        self.observations.policy.wheel_position_error = position
        self.observations.critic.wheel_position_error = position.replace(noise=None)


WHEEL_LINKS = ("left_leg_4", "right_leg_4")


def sphere_wheel_urdf(source: str) -> str:
    """Return a cached copy of ``source`` whose wheel collision cylinders are same-radius spheres.

    The 3.4 cm wide cylinder touches the floor along its width, which resists in-place yaw: in MuJoCo
    0.30 N m of right-left wheel torque turned the posma2_50000 robot at 0.17 deg/s, while the real
    robot turned at 3.8 deg/s with 0.37 N m (``docs/exp/2026-10-18/flashsac_posma2_50000_202450_review.md``
    section 7). A sphere gives one contact point and no scrub torque. Visual meshes, inertia and all
    other collisions are unchanged; ``package://tita_description/`` paths become absolute so the copy
    can live outside the package.
    """
    src = Path(source)
    root = ET.fromstring(src.read_text())
    replaced = 0
    for link in root.findall("link"):
        if link.get("name") not in WHEEL_LINKS:
            continue
        for collision in link.findall("collision"):
            geometry = collision.find("geometry")
            cylinder = geometry.find("cylinder")
            if cylinder is None:
                raise ValueError(f"{link.get('name')}: expected a cylinder wheel collision")
            geometry.remove(cylinder)
            ET.SubElement(geometry, "sphere", radius=cylinder.get("radius"))
            replaced += 1
    if replaced != len(WHEEL_LINKS):
        raise ValueError(f"replaced {replaced} wheel collisions, expected {len(WHEEL_LINKS)}")
    package = src.parents[1]
    for mesh in root.iter("mesh"):
        mesh.set("filename", mesh.get("filename").replace("package://tita_description/", f"{package}/"))
    text = ET.tostring(root, encoding="unicode")
    out = Path(tempfile.gettempdir()) / "ddt_lab_real2sim" / (
        f"tita_sphere_wheels_{hashlib.sha256(text.encode()).hexdigest()[:12]}.urdf")
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        partial = out.with_suffix(f".{os.getpid()}.tmp")
        partial.write_text(text)
        os.replace(partial, out)
    return str(out)


@configclass
class MyTitaFlatPosKneeMA2SphereEnvCfg(MyTitaFlatPosKneeMA2EnvCfg):
    """Experiment 1 (2026-10-18): ``MyTitaFlatPosKneeMA2EnvCfg`` with point-contact (sphere) wheels.

    Only the wheel collision shape changes, so in-place yaw is no longer held by cylinder scrub. The
    wheel friction randomization (0.2-1.6) and everything else stay as in the posma2 run.
    """

    def __post_init__(self):
        super().__post_init__()
        self.scene.robot.spawn = self.scene.robot.spawn.replace(
            asset_path=sphere_wheel_urdf(self.scene.robot.spawn.asset_path))


@configclass
class MyTitaFlatPosKneeSphereEnvCfg(MyTitaFlatPosKneeMA2SphereEnvCfg):
    """Experiment 2: experiment 1 without the leg MA2 filter (plain joint-position leg actions).

    The export then records ``leg_action_filter: none``; deploy with the filter off.
    """

    def __post_init__(self):
        plain = {name: getattr(self.actions, name) for name in LEG_ACTION_TERMS}
        super().__post_init__()
        for name, term in plain.items():
            assert type(term) is JointPositionActionCfg, type(term)
            setattr(self.actions, name, term)


@configclass
class MyTitaFlatPosKneeMA2SphereFastEnvCfg(MyTitaFlatPosKneeMA2SphereEnvCfg):
    """Experiment 3: experiment 1 with commands lin_vel_x +-1.5 m/s and ang_vel_z +-3.0 rad/s, no ramp.

    ``ramp_rate`` 1000 units/s makes the emitted command equal the target every step (the 0.5 units/s
    ramp would need 6 s to reach 3 rad/s inside a 6-8 s resampling window). The reset settle window,
    standing-env sampling and resampling time are unchanged.
    """

    def __post_init__(self):
        super().__post_init__()
        command = self.commands.base_velocity
        command.ranges.lin_vel_x = (-1.5, 1.5)
        command.ranges.ang_vel_z = (-3.0, 3.0)
        command.ramp_rate = 1000.0


@configclass
class MyTitaFlatPosKneeSphereFastEnvCfg(MyTitaFlatPosKneeMA2SphereFastEnvCfg):
    """Experiment 4: experiment 3 (fast commands, no ramp) without the leg MA2 filter.

    The export then records ``leg_action_filter: none``; deploy with the filter off.
    """

    def __post_init__(self):
        plain = {name: getattr(self.actions, name) for name in LEG_ACTION_TERMS}
        super().__post_init__()
        for name, term in plain.items():
            assert type(term) is JointPositionActionCfg, type(term)
            setattr(self.actions, name, term)


@configclass
class MyTitaFlatPosKneeEnvCfg(MyTitaFlatPosKneeMA2EnvCfg):
    """Experiment 5: ``MyTitaFlatPosKneeMA2EnvCfg`` (cylinder wheels) without the leg MA2 filter.

    The export then records ``leg_action_filter: none``; deploy with the filter off.
    """

    def __post_init__(self):
        plain = {name: getattr(self.actions, name) for name in LEG_ACTION_TERMS}
        super().__post_init__()
        for name, term in plain.items():
            assert type(term) is JointPositionActionCfg, type(term)
            setattr(self.actions, name, term)


@configclass
class MyTitaFlatPosKneeMA2SphereFastHeadingEnvCfg(MyTitaFlatPosKneeMA2SphereFastEnvCfg):
    """Experiment 3 + zero-command heading drift reward + critic heading error (2026-10-19).

    Base choice and evidence: ``docs/exp/2026-10-19/sphere_hardware_yaw_review.md``. Sphere wheels are needed so
    small wheel differentials actually turn the robot in sim. The policy interface is unchanged (34 observations);
    only the critic gets ``heading_drift_error``.
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.zero_command_heading_drift = RewTerm(
            func=real2sim_rewards.ZeroCommandHeadingDrift,
            weight=1.0,
            params={"command_name": "base_velocity", "sharpness": 5.0, "command_threshold": 0.0, "warmup_s": 1.0},
        )
        self.observations.critic.heading_drift_error = ObsTerm(
            func=real2sim_observations.heading_drift_error,
            params={"reward_term": "zero_command_heading_drift"},
            clip=(-3.2, 3.2),
            scale=2.0,
        )
