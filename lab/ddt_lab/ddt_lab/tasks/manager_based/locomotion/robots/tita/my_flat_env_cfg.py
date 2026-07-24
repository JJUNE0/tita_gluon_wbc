# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Sim-to-real hardened flat env for TITA.

Upgrades ``TitaFlatEnvCfg`` with three sim-to-real fidelity factors that are
missing from the base config, without touching the shared asset/rough config:

  #1 Actuator delay  -- legs + wheels modelled as ``DelayedPDActuatorCfg``
                        (motor/comm latency), overridden flat-only.
  #3 IMU bias        -- persistent per-episode bias added to the *policy* IMU
                        observations (projected gravity + base angular vel).
  #4 Encoder offset  -- persistent per-joint calibration offset added to the
                        *policy* joint-position observation.

The critic keeps ground-truth observations, so the estimator must infer these
biases from proprioception (privileged learning). Observation dimensions are
unchanged (policy obs stays 33), so the ONNX deployment interface is
unaffected.

Command range, action scale, torque/velocity limits are intentionally NOT
increased (sim-to-real safety rules).

Consolidated 2026-07-24 (`tita_gluon_wbc` workspace cleanup) into a single
settled ``MyTitaFlatEnvCfg`` -- the exact reward/command/obs configuration
previously known as ``My33`` (the best-checkpoint result of a long
`My2`-`My40` exploration in the original `DDT_Lab` workspace). The
iteration-by-iteration history and rationale for every exploratory step this
configuration is the union of lives in `Experiments/RL_Experiments.md` and
`Experiments/Sim2Sim_Experiments.md` there -- not re-derivable from code, so
nothing is lost by not keeping the intermediate versioned classes here.

Learned ``base_lin_vel`` estimator: replaces the actor's naive/ground-truth
base velocity observation with a small MLP trained jointly with PPO via a
supervised auxiliary loss (``ActorCriticWithEstimator`` / ``PPOWithEstimator``,
``ddt_lab.algorithms.estimator`` -- see ``docs/plan_base_vel_estimator_ppo.md``
for the full design). Must be paired with ``TitaFlatEstimatorPPORunnerCfg``
(`robots/tita/agents/rsl_rl_ppo_cfg.py`), not the plain ``TitaFlatPPORunnerCfg``.
"""

from isaaclab.actuators import DelayedPDActuatorCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass

import ddt_lab.tasks.manager_based.locomotion.mdp as mdp

from .flat_env_cfg import TitaFlatEnvCfg
from .rough_env_cfg import CommandsCfg, EventCfg


@configclass
class MyEventCfg(EventCfg):
    """Base TITA events + sim-to-real IMU/encoder bias sampling."""

    # (#3) IMU bias: constant per-episode bias on the policy's IMU observations.
    imu_bias = EventTerm(
        func=mdp.randomize_imu_bias,
        mode="reset",
        params={
            "gravity_bias_range": (-0.05, 0.05),   # tilt bias on projected gravity
            "ang_vel_bias_range": (-0.05, 0.05),   # rad/s gyro bias
        },
    )
    # (#4) Encoder zero offset: constant per-joint calibration bias on policy joint_pos.
    joint_offset = EventTerm(
        func=mdp.randomize_joint_offset,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("robot", joint_names=".*"),
            "offset_range": (-0.02, 0.02),         # rad (~1.1 deg) per-joint encoder offset
        },
    )


@configclass
class MyRampedCommandsCfg(CommandsCfg):
    """``base_velocity`` replaced with a ramped command (see
    ``mdp.RampedVelocityCommand``): yaw range widened `(-1.0,1.0)` ->
    `(-1.5,1.5)` rad/s, ramp rate slowed to `0.5` units/s (an 0.8 m/s
    transition takes 1.6 s instead of 0.32 s -- trades a slower start/stop
    for dramatically less joint-level shake), and 10% of resample ticks land
    on a zero-velocity target (``rel_standing_envs=0.1``) instead of the
    default 1%, giving more standstill training signal. All three changes
    were explicitly requested/approved by the user (this project's
    sim-to-real safety rule allows command-range changes with explicit
    approval)."""

    base_velocity: mdp.RampedVelocityCommandCfg = mdp.RampedVelocityCommandCfg(
        asset_name="robot",
        resampling_time_range=(6.0, 8.0),
        rel_standing_envs=0.1,
        rel_heading_envs=0.0,
        heading_command=False,
        heading_control_stiffness=0.5,
        debug_vis=True,
        ranges=mdp.RampedVelocityCommandCfg.Ranges(
            lin_vel_x=(-1.0, 1.0), lin_vel_y=(-0.0, 0.0), ang_vel_z=(-1.5, 1.5), heading=(-3.14159265, 3.14159265)
        ),
        ramp_rate=0.5,
    )


@configclass
class EstimatorTargetCfg(ObsGroup):
    """Ground-truth ``base_lin_vel`` supervised target for the learned
    estimator.

    Exists as its own named obs group -- not sliced out of ``critic`` -- so
    ``PPOWithEstimator.update()`` has a stable, explicitly-named key
    (``obs_batch["estimator_target"]``) that survives independent of
    whatever the critic obs layout happens to be. No noise/corruption: same
    ``mdp.base_lin_vel`` term and scale as ``CriticCfg`` (`rough_env_cfg.py`)
    so the estimator's output lives on the same numeric scale as the actor
    input it replaces.
    """

    base_lin_vel = ObsTerm(func=mdp.base_lin_vel, clip=(-100.0, 100.0), scale=2.0)

    def __post_init__(self):
        self.enable_corruption = False
        self.concatenate_terms = True


@configclass
class MyTitaFlatEnvCfg(TitaFlatEnvCfg):
    """Settled sim-to-real TITA flat-terrain locomotion config (formerly
    ``My33`` in the exploration history -- see module docstring).

    On top of the base actuator-delay + IMU/encoder-bias domain
    randomization (``events``, IMU/joint_pos obs routing below), this
    configuration adds:

    - A ramped, slowed, standing-heavy velocity command (``MyRampedCommandsCfg``).
    - A learned ``base_lin_vel`` estimator (``observations.estimator_target``)
      instead of a ground-truth or naive-kinematic actor observation --
      the actor obs group is pure 33-dim proprioception.
    - ``joint_deviation_hip``/``joint_deviation_shoulder`` rewards discouraging
      hip/shoulder drift from the default pose.
    - ``zero_command_position_drift``: a sharp exponential reward
      (``exp(-16*drift)``) anchoring the base position once a zero-command
      hold begins, to suppress standstill creep that a per-step velocity
      tracking reward alone does not fully catch.
    - ``track_lin_vel_xy_exp``/``track_ang_vel_z_exp`` weights raised `1.0`/
      `0.5` -> `2.0`/`2.0` -- tighter always-on command tracking, which
      indirectly reduces standstill drift more effectively than tuning
      ``zero_command_position_drift`` alone (that term is only active
      ~15-25% of episode time).
    - ``action_rate_l2`` at `-0.02` (not the more aggressive `-0.1` explored
      partway through tuning) -- the aggressive value suppressed joint-level
      shake but also blocked the fast corrective motion needed to recover
      balance right after a tightly-tracked deceleration, causing a real
      0.6 m/s walk-then-stop balance loss found in MuJoCo testing.
    """

    events: MyEventCfg = MyEventCfg()
    commands: MyRampedCommandsCfg = MyRampedCommandsCfg()

    def __post_init__(self):
        # post init of parent (flat overrides: plane terrain, no height scan, ...)
        super().__post_init__()

        # ---- (#1) Actuator delay: model motor/comm latency (flat-only override) ----
        # dt = 0.005 s (5 ms) physics step; max_delay=4 -> up to 20 ms (== 1 control
        # period at decimation=4). NOTE: DelayedPDActuator is a plain PD, so the DC
        # motor torque-speed saturation of the base DCMotorCfg is dropped; effort /
        # velocity limits are kept identical to the base asset (not increased).
        self.scene.robot.actuators = {
            "legs": DelayedPDActuatorCfg(
                joint_names_expr=["^(?!.*_leg_4).*"],
                effort_limit=60.0,
                velocity_limit=30.0,
                stiffness=60.0,
                damping=1.5,
                friction=0.0,
                min_delay=0,   # physics steps -> 0 ms
                max_delay=4,   # physics steps -> up to 20 ms
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
        }

        # ---- (#3) route policy IMU obs through biased variants (critic keeps truth) ----
        self.observations.policy.base_ang_vel.func = mdp.base_ang_vel_biased
        self.observations.policy.projected_gravity.func = mdp.projected_gravity_biased
        # ---- (#4) route policy joint_pos through encoder-offset variant ----
        self.observations.policy.joint_pos.func = mdp.joint_pos_rel_without_wheel_biased

        # ---- actor obs: pure 33-dim proprio, no base_lin_vel term -- the
        # learned estimator (ActorCriticWithEstimator) predicts it instead ----
        self.observations.policy.history_length = 0
        self.observations.policy.base_lin_vel = None
        self.observations.estimator_target = EstimatorTargetCfg()

        # ---- reward tuning (see class docstring for the settled rationale) ----
        self.rewards.ang_vel_xy_l2.weight = -0.1
        self.rewards.action_rate_l2.weight = -0.02
        self.rewards.dof_acc_l2.weight = -2.5e-6
        self.rewards.track_lin_vel_xy_exp.weight = 2.0
        self.rewards.track_ang_vel_z_exp.weight = 2.0
        self.rewards.joint_deviation_hip = RewTerm(
            func=mdp.joint_deviation_l1,
            weight=-1.0,
            params={"asset_cfg": SceneEntityCfg("robot", joint_names=[".*_leg_1"])},
        )
        self.rewards.joint_deviation_shoulder = RewTerm(
            func=mdp.joint_deviation_l1,
            weight=-0.5,
            params={"asset_cfg": SceneEntityCfg("robot", joint_names=[".*_leg_2"])},
        )
        self.rewards.zero_command_position_drift = RewTerm(
            func=mdp.ZeroCommandPositionDrift,
            weight=1.0,
            params={
                "command_name": "base_velocity",
                "sharpness": 16.0,
                "command_threshold": 0.0,
                "warmup_s": 0.0,
                "use_z": False,
            },
        )


class MyTitaFlatEnvCfg_PLAY(MyTitaFlatEnvCfg):
    def __post_init__(self) -> None:
        super().__post_init__()

        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
        # remove random pushing / physical randomization
        self.events.base_external_force_torque = None
        self.events.push_robot = None
        self.events.add_base_inertia = None
        self.events.add_base_com = None
        self.events.add_base_mass = None
        self.events.randomize_actuator_gains = None
        # disable sim-to-real biases for a clean playback
        self.events.imu_bias = None
        self.events.joint_offset = None
