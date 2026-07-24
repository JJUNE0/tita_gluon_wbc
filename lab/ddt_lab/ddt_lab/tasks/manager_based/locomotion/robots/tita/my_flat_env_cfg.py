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

The critic keeps ground-truth observations, so the NP3O history encoder must
infer these biases from proprio history (privileged learning). Observation
dimensions are unchanged (policy obs stays 33), so the ONNX deployment
interface is unaffected.

Command range, action scale, torque/velocity limits are intentionally NOT
increased (sim-to-real safety rules).

Trimmed 2026-07-22 to keep only the `My26` lineage (the reward/command/obs
setting settled on for the current sim-to-sim work) plus the ancestor classes
it structurally depends on: `MyTitaFlatEnvCfg` -> `V2` -> `V3` -> `V4` -> `V5`
-> `V7` -> `V18` -> `V21` -> `V24` -> `V26`. Every other explored variant
(`V6`, `V8`-`V17`, `V19`-`V20`, `V22`-`V23`, `V25`, the flamingo-mirrored
reward set) was deleted -- their full history/rationale is preserved in
``Experiments/RL_Experiments.md`` (not re-derivable from code, so nothing is
lost by deleting the code).
"""

import math

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
class MyTitaFlatEnvCfg(TitaFlatEnvCfg):
    """TITA flat env with actuator delay + IMU/encoder bias domain randomization."""

    events: MyEventCfg = MyEventCfg()

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


@configclass
class MyTitaFlatV2EnvCfg(MyTitaFlatEnvCfg):
    """my_flat + reward-tuning pass 1.

    Targets two observed behaviours (visible in sim2sim, worse on hardware):
      - zero-command backward drift  -> more pure-standing envs (#3)
      - body shake when decelerating to zero -> stronger body-rate damping (#5)
        and smoother actions (#6)
    Plus a two-scale linear-velocity tracking reward so the reward grows sharper
    as the tracking error approaches zero. Actuator delay + IMU/encoder bias from
    ``MyTitaFlatEnvCfg`` are kept unchanged.
    """

    def __post_init__(self):
        super().__post_init__()

        # (#3) more pure-standing command envs -> reduce zero-command backward drift
        self.commands.base_velocity.rel_standing_envs = 0.1

        # (#5) stronger base pitch/roll-rate damping -> reduce decel shake
        self.rewards.ang_vel_xy_l2.weight = -0.3

        # (#6) slightly smoother actions (small bump; too high hurts responsiveness)
        self.rewards.action_rate_l2.weight = -0.02

        # split linear-velocity tracking into coarse (kept) + fine-grained: the
        # fine term uses a smaller std so the reward peaks sharply near zero error.
        self.rewards.track_lin_vel_xy_exp_fine_grained = RewTerm(
            func=mdp.track_lin_vel_xy_exp,
            weight=0.5,
            params={"command_name": "base_velocity", "std": math.sqrt(0.0625)},
        )


@configclass
class MyTitaFlatV3EnvCfg(MyTitaFlatV2EnvCfg):
    """my_flat + reward-tuning pass 2 -- ablates the V2 fine-grained lin-vel term.

    ``eval_behavior.py`` found V2 (fully converged, 5000 iters) creeps forward at
    ~0.27 m/s under a zero command -- a large regression, worse than both `My`
    (converged, -0.037 m/s) and V2 itself at 3000 iters (-0.029 m/s), even though
    reward/survival looked *better* than `My`. Per-term reward arithmetic shows
    standing still scores clearly higher than the observed drift on every term
    (track_lin_vel coarse/fine, ang_vel_xy_l2, flat_orientation_l2) -- so this is
    not the reward function's rational optimum, more likely an under-converged
    "last mile" near zero-error that the (small-magnitude, exp-kernel-flattened)
    tracking gradient doesn't clean up quickly even after the aggregate curve
    plateaus. This variant isolates whether the V2 fine-grained term (adding a
    second, sharper tracking term) contributes to that, by reverting to a single
    coarse term (matching ``My``) while keeping V2's other changes --
    ``rel_standing_envs=0.1``, ``ang_vel_xy_l2=-0.3``, ``action_rate_l2=-0.02`` --
    since those are what improved decel shake and shouldn't be touched here.
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.track_lin_vel_xy_exp_fine_grained = None


@configclass
class MyTitaFlatV4EnvCfg(MyTitaFlatV3EnvCfg):
    """my_flat + reward-tuning pass 3 -- ablates V3's ang_vel_xy_l2 weight.

    `My2`/`My3` both showed a recurring crash-and-recover instability late in
    training (reward ~20s <-> near-0 in a handful of iterations, then recovery)
    with `ang_vel_xy_l2` pushed 6x higher than the original (-0.05 -> -0.3).
    This variant halves that back toward the original to check whether a
    milder weight keeps V3's decel-shake improvement while avoiding the
    instability. Everything else (fine-grained term removed, rel_standing_envs
    =0.1, action_rate_l2=-0.02) is kept unchanged from V3.
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.ang_vel_xy_l2.weight = -0.1


@configclass
class MyTitaFlatV5EnvCfg(MyTitaFlatV4EnvCfg):
    """my_flat + reward-tuning pass 4 -- raises action_rate_l2 to target joint-level shake.

    ``eval_behavior.py`` extended with per-joint deviation/action-rate logging
    found the joint-level shake (reported present since `My2`, in both MuJoCo
    and on hardware) spikes 15-50x at the exact moment a nonzero forward
    command cuts to zero -- worst in absolute terms on `joint_left/right_leg_2`
    ("shoulder"/thigh, decel peak action-rate 0.43-0.55 vs 0.15-0.20 for the
    other position-controlled leg joints). `ang_vel_xy_l2` (base body-rate)
    doesn't explain this -- it's joint-level, not base-level. `action_rate_l2`
    is the term that directly penalizes step-to-step action change, so this
    variant raises it from V4's -0.02 to -0.1 (5x; 10x the original -0.01) to
    directly suppress the transient. Everything else unchanged from V4
    (ang_vel_xy_l2=-0.1, fine-grained lin-vel term removed, rel_standing_envs
    =0.1).
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.action_rate_l2.weight = -0.1


@configclass
class MyRampedCommandsCfg(CommandsCfg):
    """``base_velocity`` replaced with a ramped command (see
    ``mdp.RampedVelocityCommand``) -- yaw range widened (-1.0,1.0) ->
    (-1.5,1.5) rad/s. Both the ramping behavior and the range widening were
    explicitly requested/approved by the user (sim-to-real safety rule allows
    command-range changes with explicit approval)."""

    base_velocity: mdp.RampedVelocityCommandCfg = mdp.RampedVelocityCommandCfg(
        asset_name="robot",
        resampling_time_range=(6.0, 8.0),
        rel_standing_envs=0.01,
        rel_heading_envs=0.0,
        heading_command=False,
        heading_control_stiffness=0.5,
        debug_vis=True,
        ranges=mdp.RampedVelocityCommandCfg.Ranges(
            lin_vel_x=(-1.0, 1.0), lin_vel_y=(-0.0, 0.0), ang_vel_z=(-1.5, 1.5), heading=(-math.pi, math.pi)
        ),
        ramp_rate=2.5,
    )


@configclass
class MyTitaFlatV7EnvCfg(MyTitaFlatV5EnvCfg):
    """my_flat + reward-tuning pass 6 -- dof_acc_l2 raised + ramped velocity command.

    User report: in `My5`, shoulder/thigh (L2/R2) shake is gone once velocity
    is steady, but still severe right when a command first comes in and right
    when it stops -- a transition-only symptom that `action_rate_l2`
    (action-space smoothness) doesn't fully explain. Two changes tested
    together per user request:

      1. `dof_acc_l2` (physical joint-acceleration penalty) raised 10x, from
         -2.5e-7 to -2.5e-6 -- untouched since `My`; targets the actual
         physical ringing/overshoot through the actuator-delay+PD loop more
         directly than action-space smoothness alone.
      2. `base_velocity` switched to `RampedVelocityCommand` (see
         `MyRampedCommandsCfg`): the emitted command now ramps toward its
         target at ~0.05 per 0.02s control step instead of jumping instantly
         on resample -- matches how the sim2sim keyboard teleop actually
         presents commands, narrowing a train/deploy command-profile
         mismatch. Yaw range also widened to (-1.5, 1.5) rad/s.

    Keeps everything else from `My5` (`ang_vel_xy_l2=-0.1`, `action_rate_l2`
    =-0.1, fine-grained lin-vel term removed, base `rel_standing_envs=0.1`).
    """

    commands: MyRampedCommandsCfg = MyRampedCommandsCfg()

    def __post_init__(self):
        super().__post_init__()
        self.rewards.dof_acc_l2.weight = -2.5e-6


@configclass
class MyTitaFlatV18EnvCfg(MyTitaFlatV7EnvCfg):
    """RSL-RL PPO, no history, **estimated** (not ground-truth) ``base_lin_vel``
    fed directly to the actor -- the actually-deployable follow-up to `My16`.

    Same structure as `My16` (`observations.policy.history_length = 0`,
    `base_lin_vel` added to the actor obs, obs 33 -> 36) but the value comes
    from `mdp.NaiveWheelVelBaseLinVel` (`observations.py`) -- the "naive"
    wheel-spin-only kinematic estimator from
    `scripts/np3o/estimate_base_vel_from_wheels.py`, now wired as a real
    training-time `ObsTerm` instead of only validated post-hoc. Unlike `My16`,
    this variant IS deployable in sim2sim (and eventually real hardware) --
    the estimator only needs wheel joint velocity + body orientations, all
    available on real hardware.

    Known caveat (see `Experiments/RL_Experiments.md`'s wheel-vel validation
    entry): naive-estimator RMSE was ~0.10 m/s near-standstill but ~0.32 m/s
    during active gait -- worse than ground truth by a wide margin. Whether
    the policy can still learn something useful despite this noise level is
    exactly what this variant tests.
    """

    def __post_init__(self):
        super().__post_init__()
        self.observations.policy.history_length = 0
        self.observations.policy.base_lin_vel = ObsTerm(
            func=mdp.NaiveWheelVelBaseLinVel, clip=(-100.0, 100.0), scale=2.0
        )


@configclass
class MyTitaFlatV21EnvCfg(MyTitaFlatV18EnvCfg):
    """`My18` (RSL-RL, no history, naive wheel-vel `base_lin_vel` estimate in
    actor obs) + `My11`'s exact `joint_deviation_hip`/`joint_deviation_shoulder`
    reward terms (the same two lines, unchanged weights -1.0/-0.5).

    `My11` (NP3O track) was by far the best sim2sim result of the whole
    session (see the 2026-07-21 `My11` sim2sim entry in
    ``Experiments/RL_Experiments.md``) -- this tests whether that same
    joint-deviation reward mechanism, layered onto the RSL-RL + wheel-vel-
    estimate combination, can rescue RSL-RL's otherwise-consistent sim2sim
    transfer gap (`My7-RSL`/`My16`/`My18` all showed it regardless of
    observation content).
    """

    def __post_init__(self):
        super().__post_init__()
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


@configclass
class MyTitaFlatV24EnvCfg(MyTitaFlatV21EnvCfg):
    """`My21` (best sim2sim result of the session, `base_height=0.3`, wheel-vel-
    estimate obs, `My11`'s joint_deviation rewards) with the training-time
    command ramp slowed 5x: `commands.base_velocity.ramp_rate` 2.5 -> 0.5
    units/s (both linear m/s^2 and yaw rad/s^2, since `RampedVelocityCommand`
    applies one shared rate to all three axes).

    At `ramp_rate=2.5`, a 0.8 m/s target is reached in 0.32 s -- fast enough
    that `scripts/rsl_rl/eval_behavior.py` (which sets the *target*
    `vel_command_b` directly, still passing through the same
    `RampedVelocityCommand._emitted_command_b` rate limiter used at train
    time) showed severe shoulder shake even in a pure Isaac-Lab-only
    evaluation (`My21`@`model_4999`, `--ramp_up_s 1.0`: shoulder decel/cruise
    ratio 17-22x, decel dev up to 0.125 rad) -- i.e. this is not just a
    sim2sim transfer artifact, the policy itself struggles with the ~0.32s
    command transition it was actually trained on. At `ramp_rate=0.5`, the
    same 0.8 m/s transition takes 1.6 s -- user explicitly OK with a slower
    start/stop in exchange for less shake ("느리게 출발해도 되니까... 어깨
    흔들리는 것좀 어떻게 하고 싶은데").

    `initial_phase_time` (post-reset zero-command settle window) and
    `resampling_time_range` are unchanged -- only the ramp steepness changes,
    so this is the minimal, most targeted way to test the hypothesis before
    touching anything else (reward weights, action smoothing, etc).
    """

    def __post_init__(self):
        super().__post_init__()
        self.commands.base_velocity.ramp_rate = 0.5


@configclass
class EstimatorTargetCfg(ObsGroup):
    """Ground-truth ``base_lin_vel`` supervised target for the learned
    estimator (see ``docs/plan_base_vel_estimator_ppo.md``).

    Exists as its own named obs group -- not sliced out of ``critic`` -- so
    ``PPOWithEstimator.update()`` has a stable, explicitly-named key
    (``obs_batch["estimator_target"]``) that survives independent of
    whatever the critic obs layout happens to be. No noise/corruption:
    same ``mdp.base_lin_vel`` term and scale as ``CriticCfg`` (`rough_env_cfg.py`)
    so the estimator's output lives on the same numeric scale as the actor
    input it replaces.
    """

    base_lin_vel = ObsTerm(func=mdp.base_lin_vel, clip=(-100.0, 100.0), scale=2.0)

    def __post_init__(self):
        self.enable_corruption = False
        self.concatenate_terms = True


@configclass
class MyTitaFlatV26EnvCfg(MyTitaFlatV24EnvCfg):
    """`My24` (best sim2sim reward/ramp setting) with the actor's
    `NaiveWheelVelBaseLinVel` observation term (`My18`/`My21`/`My24`'s
    deployable-but-noisy kinematic wheel-vel estimate) replaced by a small
    MLP estimator, trained jointly with PPO via a supervised auxiliary loss
    (`ActorCriticWithEstimator` / `PPOWithEstimator`,
    ``ddt_lab.algorithms.estimator``) -- see
    ``docs/plan_base_vel_estimator_ppo.md`` for the full design and
    motivation (this is the standard ETH/ANYmal-style asymmetric
    actor-critic state-estimation pattern, applied to TITA's wheeled-biped
    base velocity).

    Two changes vs. `My24`:
    - `observations.policy.base_lin_vel` removed entirely -- the `policy`
      group goes back to pure 33-dim proprioception (ang_vel, gravity,
      commands, joint_pos, joint_vel, last_action), now the estimator's
      input instead of the actor's.
    - `observations.estimator_target` (new obs group) added -- ground-truth
      `base_lin_vel`, no noise, the supervised loss target.

    Must be paired with `TitaFlatEstimatorPPORunnerCfg`
    (`robots/tita/agents/rsl_rl_ppo_cfg.py`), not the plain
    `TitaFlatPPORunnerCfg` -- the latter's `ActorCriticCfg`/`obs_groups` have
    no estimator/`estimator_target` wiring and would silently drop the
    estimator observation-group requirement.

    Current settled reward/command/obs configuration for the active
    sim-to-sim track (2026-07-22) -- the base_lin_vel estimator's own
    accuracy (vs. ground truth, both in Isaac Lab and MuJoCo sim2sim) is the
    remaining open item, tracked in `Experiments/RL_Experiments.md`.
    """

    def __post_init__(self):
        super().__post_init__()
        self.observations.policy.base_lin_vel = None
        self.observations.estimator_target = EstimatorTargetCfg()


class MyTitaFlatV26EnvCfg_PLAY(MyTitaFlatV26EnvCfg):
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


@configclass
class MyTitaFlatV27EnvCfg(MyTitaFlatV26EnvCfg):
    """`My26` (settled estimator/reward/command configuration) + a sharp
    exponential reward for holding world-frame base position fixed during a
    sustained zero-command window (``mdp.ZeroCommandPositionDrift``).

    Root-caused via a 2026-07-22 pure-MuJoCo A/B replay
    (``Experiments/Sim2Sim_Experiments.md``): the real backward-drift symptom
    was reproduced in sim by only changing the initial leg pose, and a longer
    (30 s) rerun showed the policy always settles onto *some* quasi-static leg
    pose within a zero-command hold, but every pose found so far carries its
    own nonzero steady-state wheel velocity -- there is no leg configuration
    that is an exact zero-velocity fixed point. The existing
    ``track_lin_vel_xy_exp`` term only scores the current step's velocity
    error through an exp kernel that goes nearly flat once the error is
    already small (the "last mile" gap called out in
    ``MyTitaFlatV3EnvCfg``'s docstring), so a small constant wheel-velocity
    bias is barely penalized per step and never accumulates into a stronger
    gradient.

    ``ZeroCommandPositionDrift`` fixes that by anchoring the base position
    once a zero-command hold has lasted past ``warmup_s`` (skipping the
    deceleration-settle transient) and rewarding ``exp(-sharpness * drift)``
    against that anchor for as long as the hold continues -- any sustained
    bias now shows up as a shrinking reward instead of a flat one. Only x/y
    are anchored (``use_z=False``); base height is already governed by the
    existing height reward/termination, and standing naturally has some small
    legitimate z bobbing that a hard x/y/z anchor would double-penalize.

    Two changes from the first draft, per explicit user request:
    - ``warmup_s=0.0`` / ``command_threshold=0.0`` -- no settle grace period:
      the anchor is captured on the very first step the emitted command is
      exactly zero (``rewards.py``'s comparison uses ``<=`` specifically so
      ``command_threshold=0.0`` still matches instead of never triggering).
      The robot must hold position the instant the command reaches zero, not
      some tolerance-band/warmup-window approximation of that.
    - ``commands.base_velocity.rel_standing_envs`` raised `0.01` -> `0.1` so a
      meaningfully larger fraction of resample ticks land on a zero-velocity
      target throughout an episode (not just the guaranteed post-reset
      ``initial_phase_time`` settle window) -- not dedicated stop-sequencing
      logic, just a more frequent per-resample coin flip (see
      ``Experiments/RL_Experiments.md``).
    """

    def __post_init__(self):
        super().__post_init__()
        self.commands.base_velocity.rel_standing_envs = 0.1
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


class MyTitaFlatV27EnvCfg_PLAY(MyTitaFlatV27EnvCfg):
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


@configclass
class MyTitaFlatV28EnvCfg(MyTitaFlatV27EnvCfg):
    """`My27` (My26 + ``ZeroCommandPositionDrift``) with the command range
    widened per explicit user request: ``lin_vel_x`` `(-1.0,1.0)` ->
    `(-1.5,1.5)` m/s, ``ang_vel_z`` `(-1.5,1.5)` -> `(-2.5,2.5)` rad/s.
    ``lin_vel_y``/``heading`` ranges and ``ramp_rate`` are unchanged. Per this
    project's sim-to-real safety rule, command-range changes require explicit
    user approval -- given here.
    """

    def __post_init__(self):
        super().__post_init__()
        self.commands.base_velocity.ranges.lin_vel_x = (-1.5, 1.5)
        self.commands.base_velocity.ranges.ang_vel_z = (-2.5, 2.5)


class MyTitaFlatV28EnvCfg_PLAY(MyTitaFlatV28EnvCfg):
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


@configclass
class MyTitaFlatV29EnvCfg(MyTitaFlatV27EnvCfg):
    """`My27` ablation 1/2: ``zero_command_position_drift.weight`` raised
    `1.0` -> `5.0` (``sharpness`` unchanged at `16.0`).

    My27's own training showed this reward plateauing at Episode_Reward
    ~0.06-0.09 (max observed 0.0865) against a ceiling of 1.0, and the
    resulting real-world drift was wildly non-monotonic across checkpoints
    (iter 2500 excellent, iter 3500/4500/4999 far worse than the My26
    baseline) -- see the 2026-07-23 entries in `Experiments/`. Narrow-command
    (My27) lineage, not My28's widened range, to isolate the reward-tuning
    question cleanly. Raising the weight makes this term's contribution to
    total return proportionally larger relative to the always-on tracking
    terms, testing whether it was simply being outweighed rather than
    fundamentally hard to satisfy.
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.zero_command_position_drift.weight = 5.0


class MyTitaFlatV29EnvCfg_PLAY(MyTitaFlatV29EnvCfg):
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


@configclass
class MyTitaFlatV30EnvCfg(MyTitaFlatV27EnvCfg):
    """`My27` ablation 2/2: ``zero_command_position_drift.sharpness`` lowered
    `16.0` -> `8.0` (``weight`` unchanged at `1.0`).

    Companion ablation to `My29` -- same motivation, but tests the opposite
    lever: a softer exponential keeps a higher, more differentiated reward
    value over a wider drift range (``exp(-8*0.3)=0.09`` vs
    ``exp(-16*0.3)=0.008``), which may explain My27's checkpoint-to-checkpoint
    instability (once drift grew past roughly 0.3 m, sharpness=16 gave almost
    no signal to distinguish "somewhat bad" from "much worse", i.e. little
    pull back toward the anchor). Narrow-command (My27) lineage, matching
    `My29`.
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.zero_command_position_drift.params["sharpness"] = 8.0


class MyTitaFlatV30EnvCfg_PLAY(MyTitaFlatV30EnvCfg):
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


@configclass
class MyTitaFlatV31EnvCfg(MyTitaFlatV27EnvCfg):
    """`My27` ablation: raise the always-on tracking reward weights instead of
    touching `zero_command_position_drift` -- ``track_lin_vel_xy_exp``
    `1.0` -> `2.0`, ``track_ang_vel_z_exp`` `0.5` -> `2.0`. Motivated by the
    "structural ceiling" analysis (2026-07-23,
    ``Experiments/RL_Experiments.md``): `zero_command_position_drift` is only
    active ~15-25% of episode time, so pushing its own weight/sharpness barely
    moved real drift (`My29`/`My30` both underperformed `My27@2500`). This
    variant leaves the drift reward untouched and instead makes the
    always-on velocity-tracking terms more dominant, to see whether tighter
    command tracking overall (not specifically the zero-command case)
    indirectly reduces standstill drift.
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.track_lin_vel_xy_exp.weight = 2.0
        self.rewards.track_ang_vel_z_exp.weight = 2.0


class MyTitaFlatV31EnvCfg_PLAY(MyTitaFlatV31EnvCfg):
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


@configclass
class MyTitaFlatV32EnvCfg(MyTitaFlatV27EnvCfg):
    """`My27` ablation: ``observations.policy.history_length`` `0` -> `3`
    (``flatten_history_dim`` stays at its default `True`, so the policy obs
    group becomes a flat `(3*33=99)`-dim vector instead of pure single-step
    proprio). `ActorCriticWithEstimator` sizes its estimator/actor MLPs
    dynamically from the actual observation tensor width
    (``num_proprio = sum(obs[group].shape[-1] ...)`` in
    ``actor_critic_with_estimator.py``), so no estimator/actor code changes
    are needed for this to build and train correctly.

    Isaac-Lab-training-only for now: the current sim2sim/real deployment
    pipeline (``cosim_ros2_jazzy``, real controller) assumes a fixed 33-dim
    single-step ``nn_input0`` and has no history buffer wired for this
    estimator-based actor -- per this project's change-impact rules, history
    semantics changes require deployment-side updates and a restart from P0
    before any sim2sim/real use, not just an ONNX re-export. Not attempted
    here; this variant only tests whether extra temporal context helps the
    zero-command drift behavior in Isaac Lab.
    """

    def __post_init__(self):
        super().__post_init__()
        self.observations.policy.history_length = 3
        # base rough_env_cfg sets flatten_history_dim=False for the NP3O track
        # (its history encoder wants the 3D (batch, history, obs) shape) --
        # rsl_rl's plain ActorCritic asserts exactly 2D observations, so this
        # must be forced back to True here.
        self.observations.policy.flatten_history_dim = True


class MyTitaFlatV32EnvCfg_PLAY(MyTitaFlatV32EnvCfg):
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


@configclass
class MyTitaFlatV33EnvCfg(MyTitaFlatV31EnvCfg):
    """`My31` (My27 + `track_lin_vel_xy_exp`/`track_ang_vel_z_exp` weight 2.0,
    which fixed cold-start zero-command drift down to ~0.01-0.09m/10s with no
    cherry-picking) with ``action_rate_l2`` weight relaxed `-0.1` -> `-0.02`
    (the `My2`-era value, before `My5` raised it 10x from the original -0.01
    to suppress shoulder shake).

    Root cause hypothesis (2026-07-23, ``Experiments/Sim2Sim_Experiments.md``):
    a MuJoCo walk-then-stop probe (ground-truth base position/orientation)
    found `My31@2999` reproducibly loses balance at 0.6 m/s (base height
    collapses from ~0.35m to 0.14-0.28m, roll oscillates up to -0.64 rad)
    while `My26`/`My27` do not show this at the same speed -- i.e. it's a
    regression introduced by `My31`'s stronger tracking weights, not a
    pre-existing issue. `action_rate_l2` penalizes step-to-step action change
    unconditionally, including whatever fast corrective action would be
    needed to recover balance right after an aggressive, tightly-tracked
    deceleration -- raised 10x specifically to fight decel-time shoulder
    shake, it may now be suppressing recovery motion instead. This variant
    tests whether relaxing it restores decel-time stability while keeping
    `My31`'s standstill-drift improvement.
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.action_rate_l2.weight = -0.02


class MyTitaFlatV33EnvCfg_PLAY(MyTitaFlatV33EnvCfg):
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


@configclass
class MyTitaFlatV34EnvCfg(MyTitaFlatV31EnvCfg):
    """`My31` with ``action_rate_l2`` weight at the midpoint `-0.05` between
    `My31`'s `-0.1` (shoulder/thigh shake suppressed, but 0.6 m/s
    walk-then-stop collapses -- confirmed via the 2026-07-23 fair-comparison
    MuJoCo suite in ``Experiments/Sim2Sim_Experiments.md``) and `My33`'s
    `-0.02` (0.6 m/s walk-then-stop recovers cleanly, but user-observed
    shoulder/thigh shake returned in live sim2sim). Testing whether a
    midpoint value keeps both properties instead of trading one for the
    other.
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.action_rate_l2.weight = -0.05


class MyTitaFlatV34EnvCfg_PLAY(MyTitaFlatV34EnvCfg):
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


@configclass
class MyTitaFlatV35EnvCfg(MyTitaFlatV31EnvCfg):
    """`My31` (My27 + track_lin_vel/ang_vel weight 2.0) with ``action_rate_l2``
    disabled and replaced by ``mdp.DecelGatedActionJerkPenalty`` (already in
    ``rewards.py``, never wired into any active My-variant until now).

    Motivation (2026-07-23): `My31`'s uniform ``action_rate_l2=-0.1`` caused a
    real fall at 0.6 m/s walk-then-stop (base height collapse, roll to
    -0.64 rad) -- it suppresses shoulder shake but also blocks the fast
    corrective motion needed right after an aggressive, tightly-tracked
    deceleration. `My33`/`My34` just picked a weaker single value
    (-0.02/-0.05), trading shake suppression for recovery capability along one
    knob. This variant tests a smarter shape instead: penalize jerk
    (2nd-order action difference) *more* at steady state and *less* during an
    active command transition (``transition_weight`` negative), so the policy
    is freer to react exactly when it needs to recover, and more constrained
    the rest of the time. ``base_weight=1.0``, ``transition_weight=-0.7``
    keeps the effective factor positive throughout (1.0 at rest -> 0.3 at
    full transition, never flips sign).
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.action_rate_l2.weight = 0.0
        self.rewards.decel_gated_jerk = RewTerm(
            func=mdp.DecelGatedActionJerkPenalty,
            weight=-1.0,
            params={
                "command_name": "base_velocity",
                "base_weight": 1.0,
                "transition_weight": -0.7,
                "transition_scale": 1.0,
            },
        )


class MyTitaFlatV35EnvCfg_PLAY(MyTitaFlatV35EnvCfg):
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


@configclass
class MyTitaFlatV36EnvCfg(MyTitaFlatV33EnvCfg):
    """`My33` (safe: no 0.6 m/s fall) + ``joint_deviation_shoulder`` weight
    `-0.5` -> `-2.5`. Directly penalizes shoulder/thigh (``.*_leg_2``)
    position deviation from default -- a more direct lever for "shoulder
    shouldn't move" than action-rate/jerk proxies, layered on the
    already-safe `My33` base rather than re-touching `action_rate_l2`.
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.joint_deviation_shoulder.weight = -2.5


class MyTitaFlatV36EnvCfg_PLAY(MyTitaFlatV36EnvCfg):
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


@configclass
class MyTitaFlatV37EnvCfg(MyTitaFlatV33EnvCfg):
    """`My33` (safe base) + ``dof_acc_l2`` weight `-2.5e-6` -> `-1e-5` (4x).

    Targets physical joint acceleration directly instead of action-space rate
    -- a mechanistically different lever from `action_rate_l2`/jerk, tested in
    isolation on the already-safe `My33` base.
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.dof_acc_l2.weight = -1.0e-5


class MyTitaFlatV37EnvCfg_PLAY(MyTitaFlatV37EnvCfg):
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


@configclass
class MyTitaFlatV38EnvCfg(MyTitaFlatV33EnvCfg):
    """`My33` (safe base) + ``commands.base_velocity.ramp_rate`` `0.5` ->
    `0.2` (2.5x slower). Attacks the root cause instead of the response --
    a gentler command transition means less disturbance to recover from in
    the first place, at the cost of an even slower start/stop.
    """

    def __post_init__(self):
        super().__post_init__()
        self.commands.base_velocity.ramp_rate = 0.2


class MyTitaFlatV38EnvCfg_PLAY(MyTitaFlatV38EnvCfg):
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


@configclass
class MyTitaFlatV39EnvCfg(MyTitaFlatV33EnvCfg):
    """`My33` (safe base) + `My36`'s shoulder-deviation boost + `My37`'s
    dof_acc_l2 boost combined -- tests whether the two independently
    plausible, non-conflicting levers stack additively.
    """

    def __post_init__(self):
        super().__post_init__()
        self.rewards.joint_deviation_shoulder.weight = -2.5
        self.rewards.dof_acc_l2.weight = -1.0e-5


class MyTitaFlatV39EnvCfg_PLAY(MyTitaFlatV39EnvCfg):
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


@configclass
class MyTitaFlatV40EnvCfg(MyTitaFlatV33EnvCfg):
    """`My33` (current best checkpoint) with the joint-position reset range
    widened `(-0.5, 1.0)` -> `(-0.5, 2.0)`.

    Root cause found 2026-07-24 (real hardware test of `My33@2999`, then
    reproduced/amplified in a posture-matched MuJoCo replay -- see
    `Experiments/Sim2Sim_Experiments.md`): real TITA's actual `RL_RUNNING`
    entry posture has `leg_3` (knee) at roughly `-2.6` rad, a `1.76x` scale
    factor off `default_joint_pos` (`-1.5`). ``reset_joints_by_scale``
    (`rough_env_cfg.py`'s `reset_robot_joints` event) samples each joint's
    reset scale independently and uniformly from ``position_range`` --
    `(-0.5, 1.0)` never reaches `1.76x`, so **training never once exposed the
    policy to anything near the real robot's actual starting state**. This
    is not a training bug in `My33`'s reward tuning; the training
    distribution itself excluded this region. Widening the upper bound to
    `2.0` (comfortable margin over `1.76x`, and close to the physical joint
    limit region so ``soft_joint_pos_limits`` clamping still applies safely)
    lets the policy actually learn to recover from postures in this range
    instead of only being evaluated cold against it after the fact.
    """

    def __post_init__(self):
        super().__post_init__()
        self.events.reset_robot_joints.params["position_range"] = (-0.5, 2.0)


class MyTitaFlatV40EnvCfg_PLAY(MyTitaFlatV40EnvCfg):
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
