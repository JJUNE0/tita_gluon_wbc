"""TRAINING_SIM: TITA commands, sensors and reward kernels without Isaac imports.

Command state advances once per control tick. Observation evaluation is pure,
including actor/critic reads and partial resets of other environments.
"""

from dataclasses import dataclass
import math

import torch
from mjlab.envs.mdp.actions import JointVelocityAction, JointVelocityActionCfg
from mjlab.managers.command_manager import CommandTerm, CommandTermCfg
from mjlab.managers.event_manager import RecomputeLevel, requires_model_fields
from mjlab.utils.lab_api.math import quat_apply_inverse, wrap_to_pi

from .robot_cfg import JOINTS, OBS_JOINTS, WHEELS


def data(env):
    return env.scene["robot"].data


def velocity(env):
    return env.command_manager.get_term("base_velocity")


def upright(env):
    return (-data(env).projected_gravity_b[:, 2]).clamp(0, 0.7) / 0.7


@dataclass(kw_only=True)
class VelocityCommandCfg(CommandTermCfg):
    lin_vel_x: tuple[float, float] = (-1.5, 1.5)
    lin_vel_y: tuple[float, float] = (0.0, 0.0)
    ang_vel_z: tuple[float, float] = (-3.0, 3.0)
    rel_standing_envs: float = 0.1
    rel_straight_envs: float = 0.0
    ramp_rate: float = 0.0
    initial_phase_time: float = 0.0
    sensor_bias: bool = True
    wheel_error_gait_name: str | None = None
    wheel_error_velocity_thresholds: tuple[float, float] | None = None
    wheel_error_moving_anchor: bool = False
    wheel_error_clip_m: float = 0.3
    # New pose tasks finalize odometry after the pose term gates velocity.
    # False keeps saved checkpoints' original command-update ordering.
    stop_state_after_pose: bool = False

    def build(self, env):
        if not 0 <= self.rel_straight_envs <= 1:
            raise ValueError("Straight-command environment fraction must be in [0, 1]")
        thresholds = self.wheel_error_velocity_thresholds
        if thresholds is not None and (len(thresholds) != 2 or not all(math.isfinite(v) and v > 0 for v in thresholds)):
            raise ValueError("Stop latch requires positive planar/yaw velocity thresholds")
        if not math.isfinite(self.wheel_error_clip_m) or self.wheel_error_clip_m <= 0:
            raise ValueError("Wheel position clip must be positive and finite")
        if self.stop_state_after_pose and "base_pose" not in env.cfg.commands:
            raise ValueError("Deferred stop state requires a base_pose command")
        return VelocityCommand(self, env)


class VelocityCommand(CommandTerm):
    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        self.target = torch.zeros(self.num_envs, 3, device=self.device)
        self._command = torch.zeros_like(self.target)
        self.heading_integral = torch.zeros(self.num_envs, 2, device=self.device)
        self.gyro_bias = torch.zeros(self.num_envs, device=self.device)
        self.gravity_bias = torch.zeros_like(self.target)
        self.angular_bias = torch.zeros_like(self.target)
        self.joint_bias = torch.zeros(self.num_envs, 8, device=self.device)
        self.radius_scale = torch.ones(self.num_envs, device=self.device)
        self.wheel_previous = torch.zeros(self.num_envs, 2, device=self.device)
        self.wheel_error = torch.zeros(self.num_envs, device=self.device)
        self.wheel_stationary = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)
        self.position_latched = torch.zeros_like(self.wheel_stationary)
        self.position_anchor = torch.zeros_like(self.target)
        self.heading_anchor = torch.zeros(self.num_envs, device=self.device)
        self.anchor_set = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)
        self.initializing = torch.ones_like(self.anchor_set)
        self.wheel_integral = torch.zeros(self.num_envs, device=self.device)
        self._dt = 0.0
        self.metrics["error_vel_xy"] = torch.zeros(self.num_envs, device=self.device)
        self.metrics["error_vel_yaw"] = torch.zeros(self.num_envs, device=self.device)

    @property
    def command(self):
        return self._command

    def _update_metrics(self):
        # Match the Isaac velocity-command diagnostics. Native partial reset
        # calls compute(dt=0); those reads must not count as extra time steps.
        if isinstance(self._dt, (float, int)) and self._dt == 0:
            return
        d = data(self._env)
        divisor = self.cfg.resampling_time_range[1] / self._env.step_dt
        active = self._dt > 0 if torch.is_tensor(self._dt) else 1.0
        self.metrics["error_vel_xy"] += (self.command[:, :2] - d.root_link_lin_vel_b[:, :2]).norm(dim=1) * active / divisor
        self.metrics["error_vel_yaw"] += (self.command[:, 2] - d.root_link_ang_vel_b[:, 2]).abs() * active / divisor

    def _resample_command(self, env_ids):
        for i, bounds in enumerate((self.cfg.lin_vel_x, self.cfg.lin_vel_y, self.cfg.ang_vel_z)):
            self.target[env_ids, i] = torch.empty(len(env_ids), device=self.device).uniform_(*bounds)
        standing = torch.rand(len(env_ids), device=self.device) < self.cfg.rel_standing_envs
        straight = env_ids < round(self.num_envs * self.cfg.rel_straight_envs)
        standing &= ~straight
        self.target[env_ids[straight], 1:] = 0.0
        self.target[env_ids[standing]] = 0.0

    def reset(self, env_ids):
        result = super().reset(env_ids)
        self._command[env_ids] = 0.0
        self.heading_integral[env_ids] = 0.0
        self.wheel_error[env_ids] = 0.0
        self.wheel_stationary[env_ids] = False
        self.position_latched[env_ids] = False
        self.wheel_integral[env_ids] = 0.0
        self.anchor_set[env_ids] = False
        self.initializing[env_ids] = True
        self.gyro_bias[env_ids] = torch.empty(len(env_ids), device=self.device).uniform_(-0.0014, 0.0014)
        self.radius_scale[env_ids] = torch.empty(len(env_ids), device=self.device).uniform_(0.97, 1.03)
        for buffer, width in ((self.gravity_bias, .05), (self.angular_bias, .05), (self.joint_bias, .02)):
            buffer[env_ids] = torch.empty_like(buffer[env_ids]).uniform_(-width, width) if self.cfg.sensor_bias else 0.0
        return result

    def compute(self, dt, env_ids=None):
        self._dt = dt
        super().compute(dt, env_ids)

    def _update_command(self, env_ids=None):
        ids = slice(None) if env_ids is None else env_ids
        dt = self._dt if isinstance(self._dt, (float, int)) else self._dt[ids]
        elapsed = self._env.episode_length_buf[ids] * self._env.step_dt
        ready = elapsed >= self.cfg.initial_phase_time
        old = self._command[ids]
        target = self.target[ids]
        if self.cfg.ramp_rate > 0:
            limit = self.cfg.ramp_rate * dt
            if torch.is_tensor(limit):
                limit = limit[:, None]
            current = old + (target - old).clamp(-limit, limit)
        else:
            current = target.clone()
        self._command[ids] = torch.where(ready[:, None], current, 0.0)
        if not self.cfg.stop_state_after_pose:
            self.update_stop_state(env_ids)

    def update_stop_state(self, env_ids=None):
        """Update once, using the final command presented to the policy."""
        ids = slice(None) if env_ids is None else env_ids
        dt = self._dt if isinstance(self._dt, (float, int)) else self._dt[ids]
        d = data(self._env)
        q = d.joint_pos
        # Wheel world rolling angle includes leg articulation and base pitch.
        quat = d.root_link_quat_w
        pitch = torch.asin((2 * (quat[:, 0] * quat[:, 2] - quat[:, 3] * quat[:, 1])).clamp(-1, 1))
        wheel_ids = [self._env.scene["robot"].joint_names.index(n) for n in (JOINTS[3], JOINTS[7])]
        leg2 = [self._env.scene["robot"].joint_names.index(n) for n in (JOINTS[1], JOINTS[5])]
        leg3 = [self._env.scene["robot"].joint_names.index(n) for n in (JOINTS[2], JOINTS[6])]
        angle = q[:, wheel_ids] + q[:, leg2] + q[:, leg3] + pitch[:, None]
        initial = self.initializing[ids]
        delta = wrap_to_pi(angle[ids] - self.wheel_previous[ids]).mean(dim=1)
        near_zero = (self._command[ids].abs() <= self._command.new_tensor([.02, .02, .03])).all(dim=1)
        wheel_hold = near_zero & ~initial
        if self.cfg.wheel_error_velocity_thresholds is not None:
            linear, angular = self.cfg.wheel_error_velocity_thresholds
            stationary = wheel_hold & (d.root_link_lin_vel_b[ids, :2].norm(dim=1) < linear) & (d.root_link_ang_vel_b[ids, 2].abs() < angular)
            # The first settled sample establishes the new reference. Do not
            # integrate the final deceleration interval into the hold error.
            wheel_hold &= stationary & self.wheel_stationary[ids]
            self.wheel_stationary[ids] = stationary
        if self.cfg.wheel_error_gait_name is not None:
            # Commands update before gait. Exclude the last walking physics
            # interval when the new velocity command has just reached zero.
            previous_gait = self._env.command_manager.get_command(self.cfg.wheel_error_gait_name)[ids, 0]
            wheel_hold &= ~previous_gait.bool()
        self.wheel_error[ids] = torch.where(wheel_hold,
            self.wheel_error[ids] + delta * .0925 * self.radius_scale[ids], 0.0)
        if self.cfg.wheel_error_moving_anchor:
            # Bounding the integral moves its implicit reference along with
            # large displacements, instead of only clipping the observation.
            self.wheel_error[ids] = self.wheel_error[ids].clamp(-self.cfg.wheel_error_clip_m, self.cfg.wheel_error_clip_m)
        self.wheel_previous[ids] = angle[ids]
        yaw_rate = d.root_link_ang_vel_b[ids, 2]
        increment = torch.stack((yaw_rate + self.gyro_bias[ids], yaw_rate), dim=1)
        delta_t = dt if isinstance(dt, (float, int)) else dt[:, None]
        self.heading_integral[ids] = torch.where((near_zero & ~initial)[:, None],
            self.heading_integral[ids] + increment * delta_t, 0.0)
        self.initializing[ids] = False


@dataclass(kw_only=True)
class GaitCommandCfg(CommandTermCfg):
    frequency_range_hz: tuple[float, float] = (1.25, 1.25)
    stance_fraction: float = 0.6
    settle_time_s: float = 1.0
    step_in_place: bool = True
    linear_threshold: float = 0.02
    yaw_threshold: float = 0.03
    straight_only: bool = False

    def build(self, env):
        if not (0 < self.frequency_range_hz[0] <= self.frequency_range_hz[1]
                and .5 <= self.stance_fraction < 1 and self.settle_time_s >= 0
                and self.linear_threshold >= 0 and self.yaw_threshold >= 0):
            raise ValueError("Invalid gait frequency, stance fraction or settling time")
        return GaitCommand(self, env)


class GaitCommand(CommandTerm):
    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        self.phase = torch.zeros(self.num_envs, device=self.device)
        self.frequency = torch.full_like(self.phase, cfg.frequency_range_hz[0])
        self._command = torch.zeros(self.num_envs, 5, device=self.device)
        self._dt = 0.0

    @property
    def command(self):
        return self._command

    def _update_metrics(self):
        pass

    def _resample_command(self, env_ids):
        self.phase[env_ids] = torch.randint(2, (len(env_ids),), device=self.device) * .5
        self.frequency[env_ids] = torch.empty(len(env_ids), device=self.device).uniform_(*self.cfg.frequency_range_hz)

    def compute(self, dt, env_ids=None):
        self._dt = dt
        super().compute(dt, env_ids)

    def _update_command(self, env_ids=None):
        ids = slice(None) if env_ids is None else env_ids
        elapsed = self._env.episode_length_buf[ids] * self._env.step_dt
        cmd = velocity(self._env).command[ids]
        moving = (cmd[:, :2].norm(dim=1) > self.cfg.linear_threshold) | (cmd[:, 2].abs() > self.cfg.yaw_threshold)
        if self.cfg.straight_only:
            moving = ((cmd[:, 0].abs() > self.cfg.linear_threshold)
                      & (cmd[:, 1].abs() <= self.cfg.linear_threshold)
                      & (cmd[:, 2].abs() <= self.cfg.yaw_threshold))
        enabled = (moving | self.cfg.step_in_place) & (elapsed > self.cfg.settle_time_s)
        dt = self._dt if isinstance(self._dt, (float, int)) else self._dt[ids]
        self.phase[ids] = torch.where(enabled, (self.phase[ids] + self.frequency[ids] * dt) % 1, self.phase[ids])
        self._command[ids] = torch.stack((enabled.float(),
            torch.sin(2 * math.pi * self.phase[ids]) * enabled,
            torch.cos(2 * math.pi * self.phase[ids]) * enabled, self.frequency[ids],
            torch.full_like(self.phase[ids], self.cfg.stance_fraction)), dim=1)


@dataclass(kw_only=True)
class GaitGatedWheelVelocityActionCfg(JointVelocityActionCfg):
    """Use the driving scale in standing mode; command zero during gait."""

    gait_name: str = "gait"

    def build(self, env):
        return GaitGatedWheelVelocityAction(self, env)


class GaitGatedWheelVelocityAction(JointVelocityAction):
    def process_actions(self, actions):
        super().process_actions(actions)
        walking = self._env.command_manager.get_command(self.cfg.gait_name)[:, 0]
        # Gate the processed target, preserving raw actions/last-action feedback.
        self._processed_actions *= (1.0 - walking).unsqueeze(-1)


def observation(env, kind: str, critic: bool = False):
    d, v = data(env), velocity(env)
    if kind == "base_lin_vel":
        return d.root_link_lin_vel_b
    if kind == "base_ang_vel":
        return d.root_link_ang_vel_b + (0 if critic else v.angular_bias)
    if kind == "projected_gravity":
        return d.projected_gravity_b + (0 if critic else v.gravity_bias)
    if kind in ("velocity_commands", "gait"):
        return env.command_manager.get_command("base_velocity" if kind == "velocity_commands" else "gait")
    if kind in ("joint_pos", "joint_vel"):
        indices = [env.scene["robot"].joint_names.index(n) for n in OBS_JOINTS]
        if kind == "joint_vel":
            return (d.joint_vel - d.default_joint_vel)[:, indices]
        value = (d.joint_pos - d.default_joint_pos).clone()
        if not critic:
            value += v.joint_bias
        value[:, [env.scene["robot"].joint_names.index(n) for n in (JOINTS[3], JOINTS[7])]] = 0
        return value[:, indices]
    if kind == "actions":
        return env.action_manager.action
    if kind == "wheel_position_error":
        error = v.wheel_error.clamp(-v.cfg.wheel_error_clip_m, v.cfg.wheel_error_clip_m)
        if v.cfg.wheel_error_gait_name is not None:
            # Observe the new mode, after all command terms have updated.
            enabled = env.command_manager.get_command(v.cfg.wheel_error_gait_name)[:, 0]
            error = torch.where(enabled.bool(), 0., error)
        return error[:, None]
    if kind == "heading_error":
        return v.heading_integral[:, 1 if critic else 0].clamp(-.5, .5)[:, None]
    if kind == "heading_drift_error":
        return torch.where(v.anchor_set, wrap_to_pi(d.heading_w - v.heading_anchor), 0.0)[:, None]
    raise ValueError(kind)


def randomize_motors(env, env_ids):
    for motor in env.scene["robot"].actuators:
        shape = motor.stiffness[env_ids].shape
        sample = lambda bounds: torch.empty(shape, device=env.device).uniform_(*map(math.log, bounds)).exp_()
        kp, kd = sample((.8, 1.2)), sample((.8, 1.2))
        if motor.cfg.stiffness == 92.0:
            common = torch.empty(len(env_ids), 1, device=env.device).uniform_(math.log(.55), 0).exp_()
            kp, kd = kp * common, kd * common
        motor.set_gains(env_ids, motor.default_stiffness[env_ids] * kp, motor.default_damping[env_ids] * kd)
        motor.set_lags(torch.randint(5, (len(env_ids),), device=env.device), env_ids)


def reset_joints(env, env_ids, position_range):
    robot = env.scene["robot"]
    q = robot.data.default_joint_pos[env_ids].clone()
    q *= torch.empty_like(q).uniform_(*position_range)
    robot.write_joint_state_to_sim(q, torch.zeros_like(q), env_ids=env_ids)


@requires_model_fields("body_inertia", recompute=RecomputeLevel.set_const_0)
def randomize_inertia(env, env_ids):
    if env_ids is None:
        env_ids = torch.arange(env.num_envs, device=env.device)
    ids = env.scene["robot"].indexing.body_ids
    defaults = env.sim.get_default_field("body_inertia")[ids]
    scale = torch.empty(len(env_ids), len(ids), 1, device=env.device).uniform_(.85, 1.15)
    env.sim.model.body_inertia[env_ids[:, None], ids] = defaults * scale


def contacts(env, sensor, history=True):
    sensed = env.scene[sensor].data
    forces = sensed.force_history if history else sensed.force
    return forces.norm(dim=-1).amax(dim=-1) if history else forces.norm(dim=-1)


def illegal_contact(env, sensor, threshold=1.0):
    return (contacts(env, sensor) > threshold).any(dim=1)


def timeout(env):
    return env.episode_length_buf >= env.max_episode_length


def update_hold(env):
    """Called once by the first hold reward, before the heading hold reward."""
    v, d = velocity(env), data(env)
    zero = v.command.norm(dim=1) <= 0
    start = zero & ~v.anchor_set
    position_active = zero
    if v.cfg.wheel_error_velocity_thresholds is None:
        v.position_anchor[start] = d.root_link_pos_w[start]
    else:
        linear, angular = v.cfg.wheel_error_velocity_thresholds
        position_active = (v.command.abs() <= v.command.new_tensor([.02, .02, .03])).all(dim=1)
        position_active &= (d.root_link_lin_vel_b[:, :2].norm(dim=1) < linear) & (d.root_link_ang_vel_b[:, 2].abs() < angular)
        if v.cfg.wheel_error_gait_name is not None:
            position_active &= ~env.command_manager.get_command(v.cfg.wheel_error_gait_name)[:, 0].bool()
        follow = ~position_active | ~v.position_latched
        v.position_anchor[follow] = d.root_link_pos_w[follow]
        if v.cfg.wheel_error_moving_anchor:
            displacement = d.root_link_pos_w[:, :2] - v.position_anchor[:, :2]
            scale = (v.cfg.wheel_error_clip_m / displacement.norm(dim=1).clamp_min(1e-9)).clamp(max=1.)
            v.position_anchor[:, :2] = d.root_link_pos_w[:, :2] - displacement * scale[:, None]
        v.position_latched[:] = position_active
    v.heading_anchor[start] = d.heading_w[start]
    v.anchor_set[:] = zero
    return position_active


def reward(env, kind: str, std: float = .5, axis: int = 0, target_height: float = .335):
    d, v, up = data(env), velocity(env), upright(env)
    if kind == "track_lin_vel_xy_exp":
        return torch.exp(-(v.command[:, :2] - d.root_link_lin_vel_b[:, :2]).square().sum(1) / std**2) * up
    if kind == "track_ang_vel_z_exp":
        return torch.exp(-(v.command[:, 2] - d.root_link_ang_vel_b[:, 2]).square() / std**2) * up
    if kind == "lin_vel_z_l2":
        return d.root_link_lin_vel_b[:, 2].square() * up
    if kind == "ang_vel_xy_l2":
        return d.root_link_ang_vel_b[:, :2].square().sum(1) * up
    if kind == "ang_vel_axis_l2":
        if axis not in (0, 1):
            raise ValueError("axis must be 0 or 1")
        return d.root_link_ang_vel_b[:, axis].square() * up
    if kind == "flat_orientation_l2":
        return d.projected_gravity_b[:, :2].square().sum(1) * up
    if kind == "base_height_l2":
        return (d.root_link_pos_w[:, 2] - env.scene.env_origins[:, 2] - target_height).square() * up
    if kind == "joint_acc_l2":
        return d.joint_acc.square().sum(1)
    if kind == "joint_torques_l2":
        return env.sim.data.qfrc_actuator[:, env.scene["robot"].indexing.joint_v_adr].square().sum(1)
    if kind == "action_rate_l2":
        return (env.action_manager.action - env.action_manager.prev_action).square().sum(1) * up
    if kind.startswith("joint_deviation_"):
        suffix = "_leg_1" if kind.endswith("hip") else "_leg_2"
        ids = [i for i, n in enumerate(env.scene["robot"].joint_names) if n.endswith(suffix)]
        return (d.joint_pos - d.default_joint_pos)[:, ids].abs().sum(1)
    if kind == "joint_mirror":
        ids = [env.scene["robot"].joint_names.index(n) for n in JOINTS]
        q = d.joint_pos[:, ids]
        return (q[:, :3] - q[:, 4:7] * q.new_tensor([-1, 1, 1])).square().sum(1) * up
    if kind == "undesired_contacts":
        return (contacts(env, "knees") > 1).float().sum(1) * up
    if kind == "zero_command_position_drift":
        zero = update_hold(env)
        return torch.exp(-8 * (d.root_link_pos_w[:, :2] - v.position_anchor[:, :2]).norm(dim=1)) * zero
    if kind == "zero_command_heading_drift":
        return torch.exp(-5 * wrap_to_pi(d.heading_w - v.heading_anchor).abs()) * v.anchor_set
    if kind == "zero_command_wheel_action":
        zero = v.command.norm(dim=1) <= 0
        error = env.action_manager.action[:, [3, 7]].abs().pow(4).sum(1) * up
        v.wheel_integral[:] = torch.where(zero, v.wheel_integral + error * env.step_dt, 0.0)
        return v.wheel_integral.sqrt()
    if kind == "termination":
        return env.termination_manager.terminated.float()
    raise ValueError(kind)


def gait_reference(phase, enabled, stance_fraction=.6, clearance_m=.04):
    phases = torch.stack((phase, (phase + .5) % 1), dim=1)
    stance = (phases < stance_fraction) | ~enabled.bool()[:, None]
    progress = ((phases - stance_fraction) / (1 - stance_fraction)).clamp(0, 1)
    return stance, torch.where(stance, 0.0, clearance_m * torch.sin(math.pi * progress))


def mode_scaled_joint_deviation(env, kind, moving_scale, gait_name="gait", axis=0):
    """Scale penalties by gait; retain the callable name for saved configs."""
    walking = env.command_manager.get_command(gait_name)[:, 0].bool()
    return reward(env, kind, axis=axis) * torch.where(walking, moving_scale, 1.0)


def contact_schedule(env, only_when_enabled=False):
    gait = env.command_manager.get_term("gait")
    stance, _ = gait_reference(gait.phase, gait.command[:, 0], gait.cfg.stance_fraction)
    # mjlab's primary->secondary contact wrench can point downwards for a
    # supported wheel. Detect contact by magnitude, independent of its sign.
    actual = env.scene["feet"].data.force.norm(dim=-1) > 5
    up = (-data(env).projected_gravity_b[:, 2]).clamp(0, 1)
    value = torch.exp(-4 * (actual.float() - stance.float()).square().mean(1)) * up
    return value * gait.command[:, 0] if only_when_enabled else value


def wheel_clearance(env, clearance_m=.04, std=.025, radius=.0925, only_when_enabled=False):
    gait = env.command_manager.get_term("gait")
    _, desired = gait_reference(gait.phase, gait.command[:, 0], gait.cfg.stance_fraction, clearance_m)
    ids = [env.scene["robot"].body_names.index(n) for n in WHEELS]
    actual = data(env).body_link_pos_w[:, ids, 2] - env.scene.env_origins[:, 2:3] - radius
    up = (-data(env).projected_gravity_b[:, 2]).clamp(0, 1)
    value = torch.exp(-(actual - desired).square().mean(1) / std**2) * up
    return value * gait.command[:, 0] if only_when_enabled else value


def stance_push(env, stride_m=.06, std=.1):
    """Reward a bounded backward leg stroke during stance; reverse for vx<0."""
    gait, d = env.command_manager.get_term("gait"), data(env)
    ids = [env.scene["robot"].body_names.index(n) for n in WHEELS]
    offset = d.body_link_pos_w[:, ids] - d.root_link_pos_w[:, None]
    body_rotation = torch.cross(d.root_link_ang_vel_w[:, None].expand_as(offset), offset, dim=-1)
    relative_w = d.body_link_lin_vel_w[:, ids] - d.root_link_lin_vel_w[:, None] - body_rotation
    relative_b = quat_apply_inverse(d.root_link_quat_w[:, None].expand(-1, 2, -1), relative_w)
    vx = velocity(env).command[:, 0]
    speed = torch.minimum(vx.abs(), gait.frequency * stride_m / gait.cfg.stance_fraction)
    target = -vx.sign() * speed
    stance, _ = gait_reference(gait.phase, gait.command[:, 0], gait.cfg.stance_fraction)
    match = torch.exp(-(relative_b[:, :, 0] - target[:, None]).square() / std**2)
    value = (match * stance).sum(dim=1) / stance.sum(dim=1).clamp_min(1)
    return value * gait.command[:, 0] * upright(env)
