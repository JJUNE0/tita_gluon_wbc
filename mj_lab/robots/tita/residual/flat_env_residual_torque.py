"""TRAINING_SIM / VALIDATION_SIM: frozen flat Teacher plus torque residual.

The base task is TitaFlatEnvCfg. The Teacher checkpoint supplies its trained
observation/action/reward/DR configuration and frozen Actor weights. Native
flat (35 inputs) and roll/pitch/height (38 inputs) Teachers are supported.

Use TitaFlatResidualTorqueEnv with this config: raw.step() alone accepts the
Teacher's joint references, whereas env.step() accepts eight residual torques
in Nm. Teacher/residual/physics clocks are 50/250/500 Hz. Histories preserve
the existing 440-Actor/754-Critic contract, including the original 20-second
critic time scale even when the episode is 10 seconds.

Example::

    cfg = TitaFlatResidualTorqueEnvCfg(teacher_checkpoint, num_envs=16)
    env = TitaFlatResidualTorqueEnv(cfg)
    observation = env.packed_observation()
    reward, terminated, truncated, info = env.step(residual_nm)
    terminal_observation = env.packed_observation()
    env.reset_done(terminated | truncated)
    env.close()

Learners, replay buffers and experiment logging belong in the training runner.
This module has no dependencies on test/ or the BFM/zeroshot package.
"""

from copy import deepcopy
from dataclasses import replace
import hashlib
import json
import math
import pickle

import mujoco
import torch
from mjlab.envs import ManagerBasedRlEnv
from mjlab.managers import EventTermCfg
from mjlab.managers.event_manager import RecomputeLevel, requires_model_fields

from mj_lab.flash_sac import runtime
from ..common import mdp
from ..flat_env_cfg import TitaFlatEnvCfg
from ..roll_pitch_height.flat_env_roll_pitch_height_cfg import RollPitchHeightCommandCfg
from ..common.robot_cfg import INITIAL_Q, JOINTS


ACTOR_FRAME = 44
MOTION_FRAME = 30
HISTORY_LENGTH = 10
ACTOR_DIM = ACTOR_FRAME * HISTORY_LENGTH
CRITIC_DIM = ACTOR_DIM + 14 + MOTION_FRAME * HISTORY_LENGTH
PUSH_LINKS = ("base_link",) + tuple(
    f"{side}_leg_{index}" for side in ("left", "right") for index in range(1, 5))
LEG_IDS = (0, 1, 2, 4, 5, 6)


def residual_torque_action_rate(env, torque_scale_nm):
    """Squared command difference, not a dt-normalized torque derivative."""
    delta = (env.residual_torque_command - env.previous_residual_torque_command) / torque_scale_nm
    return delta.square().sum(1) * mdp.upright(env)


def fixed_position_hold(env):
    """Stop reference stays fixed through a push; no velocity gate or clamp."""
    command, data = mdp.velocity(env), mdp.data(env)
    zero = command.command.norm(dim=1) <= 0.
    entering = zero & ~env.residual_fixed_hold_active
    env.residual_fixed_hold_position[entering] = data.root_link_pos_w[entering, :2]
    env.residual_fixed_hold_active.copy_(zero)
    heading_start = zero & ~command.anchor_set
    command.heading_anchor[heading_start] = data.heading_w[heading_start]
    command.anchor_set.copy_(zero)
    distance = (data.root_link_pos_w[:, :2] - env.residual_fixed_hold_position).norm(dim=1)
    return torch.exp(-8. * distance) * zero


def _payload_spec(original):
    def build():
        spec = original()
        body = spec.body("base_link").add_body(name="residual_payload", pos=[0., 0., .10])
        body.add_geom(name="payload_visual", type=mujoco.mjtGeom.mjGEOM_SPHERE,
                      size=[.03, 0., 0.], mass=1e-6, contype=0, conaffinity=0,
                      rgba=[.95, .35, .05, 1.])
        return spec
    return build


@requires_model_fields("body_mass", "body_inertia", "body_pos", recompute=RecomputeLevel.set_const)
def randomize_payload(env, env_ids):
    if env_ids is None:
        env_ids = torch.arange(env.num_envs, device=env.device)
    robot = env.scene["robot"]
    body = robot.indexing.body_ids[robot.body_names.index("residual_payload")]
    if not hasattr(env, "payload_mass"):
        env.payload_mass = torch.zeros(env.num_envs, device=env.device)
        env.payload_location = torch.zeros(env.num_envs, 3, device=env.device)
    extra = env_ids >= env.num_envs // 2
    mass = torch.rand(len(env_ids), device=env.device) * 5. * extra
    position = torch.rand(len(env_ids), 3, device=env.device)
    position = position * position.new_tensor([.24, .16, .12]) + position.new_tensor([-.12, -.08, .06])
    position[~extra] = 0.
    physical_mass = mass.clamp_min(1e-6)
    env.sim.model.body_mass[env_ids, body] = physical_mass
    env.sim.model.body_inertia[env_ids, body] = physical_mass[:, None] * (.4 * .03**2)
    env.sim.model.body_pos[env_ids, body] = position
    env.payload_mass[env_ids] = mass
    env.payload_location[env_ids] = position


def randomize_teacher_motors(env, env_ids):
    """Map saved 0/5/10/15/20ms lag bins to 0/4/10/16/20ms at 500Hz."""
    mdp.randomize_motors(env, env_ids)
    seen = set()
    for motor in env.scene["robot"].actuators:
        delay = motor._delay_buffer
        if delay is not None and id(delay) not in seen:
            seen.add(id(delay))
            motor.set_lags((delay.current_lags[env_ids].float() * 2.5).round().long(), env_ids)


def _reward_terms(cfg):
    return {name: dict(func=term.func.__module__ + ":" + term.func.__qualname__,
                      params=deepcopy(term.params), weight=term.weight)
            for name, term in cfg.rewards.items()}


class TitaFlatResidualTorqueEnvCfg(TitaFlatEnvCfg):
    """Flat-based native task configuration plus an explicit frozen Teacher.

    The saved Teacher contract is restored before applying residual-specific
    changes. In particular, the current 38-input Teacher keeps its pose inputs;
    importing the 35-input flat defaults cannot replace its trained contract.
    """

    def __init__(self, teacher_checkpoint, num_envs=1024, episode_length_s=10.,
                 seed=42, torque_limit_nm=10.):
        if isinstance(num_envs, bool) or not isinstance(num_envs, int) or num_envs < 2 or num_envs % 2:
            raise ValueError("An even number of at least two environments is required")
        if not math.isfinite(episode_length_s) or episode_length_s <= 0.:
            raise ValueError("Episode duration must be finite and positive")
        if not math.isfinite(torque_limit_nm) or torque_limit_nm <= 0.:
            raise ValueError("Residual torque limit must be finite and positive")
        super().__init__(num_envs=num_envs)
        path, metadata = runtime.read_checkpoint(teacher_checkpoint)
        if (metadata.get("backend") != "mjlab" or metadata.get("task") not in ("flat", "flat_roll_pitch_height")
                or metadata["action_dim"] != 8
                or metadata["actor_obs_dim"] not in (35, 38)):
            raise ValueError("Expected a native TITA flat/pose FlashSAC Teacher with 35 or 38 inputs")
        with (path / "env.pkl").open("rb") as stream:
            saved = pickle.load(stream)
        if (not isinstance(saved, TitaFlatEnvCfg) or "gait" in saved.commands
                or "support" in saved.commands):
            raise ValueError("The Teacher must use the flat driving or flat pose task")
        # Restore checkpoint contracts rather than guessing them from today's
        # flat defaults. Everything else retains the normal flat task structure.
        for name in ("scene", "sim", "actions", "observations", "rewards", "events",
                     "commands", "terminations", "metrics", "viewer", "scale_rewards_by_dt"):
            setattr(self, name, deepcopy(getattr(saved, name)))
        self.teacher_checkpoint, self.teacher_metadata = path, metadata
        self.teacher_reward_terms = _reward_terms(saved)
        self.torque_limit_nm = float(torque_limit_nm)
        self.scene.num_envs, self.seed, self.auto_reset = num_envs, seed, False
        self.episode_length_s = float(episode_length_s)
        self.decimation, self.sim.mujoco.timestep = 2, .002
        self.sim.mujoco.gravity = (0., 0., -9.81)
        robot = self.scene.entities["robot"]
        robot.articulation.actuators = tuple(
            replace(motor, delay_max_lag=10) for motor in robot.articulation.actuators)
        robot.spec_fn = _payload_spec(robot.spec_fn)
        self.events["randomize_motors"].func = randomize_teacher_motors
        root = self.events["reset_base"]
        root.params["pose_range"] = {key: (0., 0.) for key in ("x", "y", "z", "roll", "pitch", "yaw")}
        root.params["velocity_range"] = {key: (0., 0.) for key in ("x", "y", "z", "roll", "pitch", "yaw")}
        self.events["reset_joints"].params["position_range"] = (1., 1.)
        self.events["residual_payload"] = EventTermCfg(func=randomize_payload, mode="reset")
        velocity = self.commands["base_velocity"]
        velocity.lin_vel_x = velocity.lin_vel_y = velocity.ang_vel_z = (0., 0.)
        velocity.rel_standing_envs, velocity.resampling_time_range = 1., (1e9, 1e9)
        if "base_pose" not in self.commands:
            # Supplies residual command channels without adding inputs to a
            # 35-input Teacher observation group.
            self.commands["base_pose"] = RollPitchHeightCommandCfg(resampling_time_range=(1e9, 1e9))
        pose = self.commands["base_pose"]
        pose.roll_range, pose.pitch_range, pose.height_range = (0., 0.), (0., 0.), (.335, .335)
        pose.rel_nominal_envs, pose.resampling_time_range = 1., (1e9, 1e9)
        self.rewards["action_rate_l2"].func = residual_torque_action_rate
        self.rewards["action_rate_l2"].params = dict(torque_scale_nm=self.torque_limit_nm)
        self.rewards["zero_command_position_drift"].func = fixed_position_hold
        self.rewards["zero_command_position_drift"].params = {}
        self.rewards["zero_command_wheel_action"].weight = 0.

    def residual_manifest(self):
        terms = _reward_terms(self)
        return dict(
            execution_domain="TRAINING_SIM", teacher_checkpoint=str(self.teacher_checkpoint),
            teacher_sha256=self.teacher_metadata["actor_sha256"], teacher_frozen=True,
            teacher_reward_terms=deepcopy(self.teacher_reward_terms), actual_reward_terms=terms,
            actual_reward_definition_sha256=hashlib.sha256(json.dumps(terms, sort_keys=True).encode()).hexdigest(),
            reward_variant="residual_torque_rate_fixed_position_no_teacher_wheel_penalty",
            actor_obs_dim=ACTOR_DIM, critic_obs_dim=CRITIC_DIM, action_dim=8,
            actor_hz=250, teacher_hz=50, physics_hz=500,
            episode_seconds=self.episode_length_s, torque_residual_limit_nm=self.torque_limit_nm,
            history_length=HISTORY_LENGTH, critic_time_scale_s=20.,
            baseline_fraction=.5, extra_disturbance_fraction=.5,
            payload_range_kg=[0., 5.], force_range_n=[0., 30.],
            force_onset_s=[2., 5.], force_duration_s=[5., 10.], force_links=list(PUSH_LINKS),
            initial_pose_randomization=False, initial_velocity_randomization=False,
            physical_dr="Restored from Teacher checkpoint; original interval kicks retained",
            residual_wheel_latch=False, residual_wheel_input_clipped=False)


class TitaFlatResidualTorqueEnv:
    """Native Teacher joint references plus bounded joint effort feedforward.

    Call packed_observation() before resetting done worlds to preserve terminal
    observations for replay. Native actuator delay and final effort clipping
    apply to the combined PD and feedforward command. step() does not auto-reset.
    """

    dt = .004
    teacher_stride = 5
    stack = HISTORY_LENGTH
    actor_obs_dim = ACTOR_DIM
    critic_obs_dim = CRITIC_DIM
    action_dim = 8

    def __init__(self, cfg: TitaFlatResidualTorqueEnvCfg, device="cuda:0"):
        if not isinstance(cfg, TitaFlatResidualTorqueEnvCfg):
            raise TypeError("Use TitaFlatResidualTorqueEnvCfg to construct the residual task")
        if not str(device).startswith("cuda"):
            raise ValueError("Native mjlab residual physics requires a CUDA device")
        self.cfg, self.device = cfg, torch.device(device)
        self.path, self.metadata = runtime.read_checkpoint(cfg.teacher_checkpoint)
        if self.metadata["actor_sha256"] != cfg.teacher_metadata["actor_sha256"]:
            raise ValueError("Teacher changed after this environment config was constructed")
        runtime.setup_imports(False)
        from flash_rl.agents.flashSAC.network import FlashSACActor
        settings = self.metadata["agent"]
        self.teacher = FlashSACActor(settings["actor_num_blocks"], self.metadata["actor_obs_dim"],
                                    settings["actor_hidden_dim"], 8).to(self.device)
        weights = torch.load(self.path / "actor.pt", map_location=self.device,
                             weights_only=True)["network_state_dict"]
        while weights and all(name.startswith("_orig_mod.") for name in weights):
            torch.nn.modules.utils.consume_prefix_in_state_dict_if_present(weights, "_orig_mod.")
        self.teacher.load_state_dict(weights)
        self.teacher.eval().requires_grad_(False)
        self.raw = ManagerBasedRlEnv(cfg, device=str(self.device))
        try:
            self._initialize_buffers()
            self.raw.reset(seed=cfg.seed)
            self.reset_buffers(torch.arange(self.n, device=self.device))
            if self.raw.obs_buf["policy"].shape[1] != self.metadata["actor_obs_dim"]:
                raise ValueError("Native observations do not match the frozen Teacher input width")
        except BaseException:
            self.raw.close()
            raise
        self.reward_manifest = cfg.residual_manifest()

    def _initialize_buffers(self):
        self.robot = self.raw.scene["robot"]
        self.n, self.num_envs = self.raw.num_envs, self.raw.num_envs
        self.torque_limit = self.cfg.torque_limit_nm
        self.ids = [self.robot.joint_names.index(name) for name in JOINTS]
        self.joint_ids = torch.tensor(self.ids, device=self.device)
        self.leg_ids = list(LEG_IDS)
        self.push_body_ids = [self.robot.body_names.index(name) for name in PUSH_LINKS]
        self.dr_mask = torch.arange(self.n, device=self.device) >= self.n // 2
        self.clean_mask = ~self.dr_mask
        self.actor_stack = torch.zeros(self.n, self.stack, ACTOR_FRAME, device=self.device)
        self.motion_stack = torch.zeros(self.n, self.stack, MOTION_FRAME, device=self.device)
        self.teacher_action = torch.zeros(self.n, 8, device=self.device)
        self.residual = torch.zeros_like(self.teacher_action)
        self.age = torch.zeros(self.n, dtype=torch.long, device=self.device)
        self.teacher_updated_at = torch.full_like(self.age, -1)
        self.force = torch.zeros(self.n, 3, device=self.device)
        self.force_link = torch.zeros(self.n, dtype=torch.long, device=self.device)
        self.force_start = torch.zeros(self.n, device=self.device)
        self.force_duration = torch.zeros(self.n, device=self.device)
        self.link_forces = torch.zeros(self.n, len(PUSH_LINKS), 3, device=self.device)
        self.link_torques = torch.zeros_like(self.link_forces)
        self.origin = torch.zeros(self.n, 2, device=self.device)
        self.residual_wheel_error = torch.zeros(self.n, device=self.device)
        self.residual_wheel_previous = torch.zeros(self.n, 2, device=self.device)
        self.residual_wheel_stop_active = torch.zeros(self.n, dtype=torch.bool, device=self.device)
        self.raw.residual_fixed_hold_position = torch.zeros_like(self.origin)
        self.raw.residual_fixed_hold_active = torch.zeros_like(self.clean_mask)
        self.raw.residual_torque_command = torch.zeros_like(self.residual)
        self.raw.previous_residual_torque_command = torch.zeros_like(self.residual)
        self.positive = torch.tensor(self.metadata["action_gain_positive"], device=self.device)
        self.negative = torch.tensor(self.metadata["action_gain_negative"], device=self.device)
        self.motor_limits = self.positive.new_tensor([60., 60., 60., 12.] * 2)
        offset = 0
        for name, shape in zip(self.raw.observation_manager.active_terms["policy"],
                               self.raw.observation_manager.group_obs_term_dim["policy"]):
            if name == "heading_error":
                self.heading_index = offset
                break
            offset += math.prod(shape)
        else:
            raise ValueError("The saved flat Teacher must contain heading_error")

    @torch.no_grad()
    def refresh_teacher(self, ids=None):
        if ids is None:
            ids = ((self.age % self.teacher_stride == 0)
                   & (self.teacher_updated_at != self.age)).nonzero().flatten()
        if len(ids):
            obs = self.raw.observation_manager.compute(update_history=False)["policy"]
            mean, _ = self.teacher.get_mean_and_std(obs[ids], training=False)
            self.teacher_action[ids] = mean.tanh()
            self.teacher_updated_at[ids] = self.age[ids]

    def wheel_angles(self):
        data = self.robot.data
        q, quat = data.joint_pos[:, self.ids], data.root_link_quat_w
        pitch = torch.asin((2 * (quat[:, 0] * quat[:, 2] - quat[:, 3] * quat[:, 1])).clamp(-1., 1.))
        return q[:, [3, 7]] + q[:, [1, 5]] + q[:, [2, 6]] + pitch[:, None]

    def residual_error_inputs(self):
        scale = self.raw.observation_manager.get_term_cfg("policy", "wheel_position_error").scale
        wheel = self.residual_wheel_error
        if scale is not None:
            wheel = wheel * scale
        heading = self.raw.obs_buf["policy"][:, self.heading_index:self.heading_index + 1]
        return torch.cat((wheel[:, None], heading), 1).clone()

    def frames(self):
        data = self.robot.data
        q, qd = data.joint_pos[:, self.ids], data.joint_vel[:, self.ids]
        gyro, gravity = data.root_link_ang_vel_b, data.projected_gravity_b
        q0 = q.new_tensor(INITIAL_Q)
        pose = self.raw.command_manager.get_command("base_pose")
        command = torch.cat((self.raw.command_manager.get_command("base_velocity"),
                             (pose - pose.new_tensor([0., 0., .335])) / pose.new_tensor([.5, .3, .1])), 1)
        # Preserve the original input scaling, including unclipped residual
        # wheel displacement and cached native heading appended after clipping.
        actor = torch.cat((gyro * .25, gravity, (q - q0)[:, self.leg_ids] * 2., qd * .05,
                           self.teacher_action, self.residual / 10., command), 1).clamp(-10., 10.)
        actor = torch.cat((actor, self.residual_error_inputs()), 1)
        motion = torch.cat((data.root_link_lin_vel_b, gyro * .25, gravity,
                            (data.root_link_pos_w[:, 2:3] - .335) * 10.,
                            (q - q0)[:, self.leg_ids] * 2., qd * .05, command), 1).clamp(-10., 10.)
        return actor, motion

    def observation(self):
        self.refresh_teacher()
        self.actor_stack[:, -1] = self.frames()[0]
        return self.actor_stack.flatten(1).clone()

    def privileged(self):
        data = self.robot.data
        time = self.raw.episode_length_buf * self.dt
        active = (time >= self.force_start) & (time < self.force_start + self.force_duration)
        value = torch.cat((data.root_link_lin_vel_b,
                           (data.root_link_pos_w[:, 2:3] - .335) * 10.,
                           data.root_link_pos_w[:, :2] - self.origin,
                           self.raw.payload_mass[:, None] / 5., self.raw.payload_location,
                           self.force * active[:, None] / 30., time[:, None] / 20.), 1)
        return value.clamp(-10., 10.).clone()

    def packed_observation(self):
        actor = self.observation()
        critic = torch.cat((actor, self.privileged(), self.motion_stack.flatten(1)), 1)
        return torch.cat((actor, critic), 1).detach().clone()

    @torch.no_grad()
    def reset_buffers(self, ids):
        self.teacher_action[ids] = self.residual[ids] = 0.
        self.age[ids], self.teacher_updated_at[ids] = 0, -1
        self.raw.residual_torque_command[ids] = self.raw.previous_residual_torque_command[ids] = 0.
        self.robot.set_joint_effort_target(torch.zeros(len(ids), 8, device=self.device),
                                          joint_ids=self.joint_ids, env_ids=ids)
        self.origin[ids] = self.robot.data.root_link_pos_w[ids, :2]
        zero = mdp.velocity(self.raw).command[ids].norm(dim=1) <= 0.
        self.raw.residual_fixed_hold_position[ids] = self.origin[ids]
        self.raw.residual_fixed_hold_active[ids] = zero
        self.residual_wheel_error[ids] = 0.
        self.residual_wheel_previous[ids] = self.wheel_angles()[ids]
        self.residual_wheel_stop_active[ids] = zero
        angle = torch.rand(len(ids), device=self.device) * (2. * math.pi)
        magnitude = torch.rand(len(ids), device=self.device) * 30. * self.dr_mask[ids]
        self.force[ids, 0], self.force[ids, 1] = magnitude * angle.cos(), magnitude * angle.sin()
        self.force[ids, 2] = 0.
        self.force_start[ids] = torch.rand(len(ids), device=self.device) * 3. + 2.
        self.force_duration[ids] = torch.rand(len(ids), device=self.device) * 5. + 5.
        self.force_link[ids] = torch.randint(len(PUSH_LINKS), (len(ids),), device=self.device)
        self.link_forces[ids] = 0.
        self.link_forces[ids, self.force_link[ids]] = self.force[ids]
        self.refresh_teacher(ids)
        actor, motion = self.frames()
        self.actor_stack[ids] = actor[ids, None].expand(-1, self.stack, -1)
        self.motion_stack[ids] = motion[ids, None].expand(-1, self.stack, -1)

    def reset(self, seed=None, env_ids=None):
        ids = torch.arange(self.n, device=self.device) if env_ids is None else env_ids
        self.raw.reset(seed=seed, env_ids=ids)
        self.reset_buffers(ids)
        return self.packed_observation()

    def reset_done(self, done):
        ids = done.nonzero().flatten()
        if len(ids):
            self.raw.reset(env_ids=ids)
            self.reset_buffers(ids)

    def _advance_wheel_error(self):
        angle = self.wheel_angles()
        change = torch.remainder(angle - self.residual_wheel_previous + math.pi, 2 * math.pi) - math.pi
        command = mdp.velocity(self.raw)
        zero = command.command.norm(dim=1) <= 0.
        self.residual_wheel_error.copy_(torch.where(
            zero & self.residual_wheel_stop_active,
            self.residual_wheel_error + change.mean(1) * .0925 * command.radius_scale, 0.))
        self.residual_wheel_previous.copy_(angle)
        self.residual_wheel_stop_active.copy_(zero)

    @torch.no_grad()
    def step(self, residual_nm):
        if residual_nm.shape != (self.n, 8) or not bool(torch.isfinite(residual_nm).all()):
            raise ValueError("Expected finite Nx8 residual torque commands in Nm")
        self.refresh_teacher()
        self.raw.previous_residual_torque_command.copy_(self.residual)
        self.residual.copy_(residual_nm.clamp(-self.torque_limit, self.torque_limit))
        self.raw.residual_torque_command.copy_(self.residual)
        self.robot.set_joint_effort_target(self.residual, joint_ids=self.joint_ids)
        time = self.raw.episode_length_buf * self.dt
        active = (time >= self.force_start) & (time < self.force_start + self.force_duration)
        self.robot.write_external_wrench_to_sim(self.link_forces * active[:, None, None],
                                               self.link_torques, body_ids=self.push_body_ids)
        applied = self.teacher_action * torch.where(self.teacher_action >= 0, self.positive, self.negative)
        _, reward, native_done, timeout, _ = self.raw.step(applied)
        self.age += 1
        actor, motion = self.frames()
        self.actor_stack = torch.cat((self.actor_stack[:, 1:], actor[:, None]), 1)
        self.motion_stack = torch.cat((self.motion_stack[:, 1:], motion[:, None]), 1)
        self._advance_wheel_error()
        self.actor_stack[:, -1, -2:] = self.residual_error_inputs()
        data = self.robot.data
        gravity, height = data.projected_gravity_b, data.root_link_pos_w[:, 2]
        failed = native_done | (height < .23) | (gravity[:, 2] > -.8)
        motors = data.qfrc_actuator[:, self.ids]
        info = dict(
            planar_speed=data.root_link_lin_vel_b[:, :2].norm(dim=1),
            yaw_rate=data.root_link_ang_vel_b[:, 2].abs(),
            drift=(data.root_link_pos_w[:, :2] - self.origin).norm(dim=1),
            tilt=gravity[:, :2].norm(dim=1), height=height,
            force_n=self.force.norm(dim=1) * active, force_active=active & self.dr_mask,
            force_link_index=self.force_link.float(), payload_kg=self.raw.payload_mass.clone(),
            failed=failed.clone(), residual_rms=self.residual.square().mean(1).sqrt(),
            residual_saturation=(self.residual.abs() >= self.torque_limit * .95).float().mean(1),
            motor_saturation=(motors.abs() >= self.motor_limits * .99).float().mean(1),
            leg_motor_saturation=(motors[:, self.leg_ids].abs() >= 59.4).float().mean(1),
            wheel_motor_saturation=(motors[:, [3, 7]].abs() >= 11.88).float().mean(1),
            fixed_position_error_m=(data.root_link_pos_w[:, :2] - self.raw.residual_fixed_hold_position).norm(dim=1),
            residual_wheel_position_error_m=self.residual_wheel_error.clone())
        for index, name in enumerate(JOINTS):
            info["residual_nm/" + name] = self.residual[:, index].clone()
            info["motor_nm/" + name] = motors[:, index].clone()
        renamed = {"action_rate_l2": "residual_reward/torque_action_rate",
                   "zero_command_position_drift": "residual_reward/fixed_position_hold"}
        for index, name in enumerate(self.raw.reward_manager.active_terms):
            info[renamed.get(name, "native_reward/" + name)] = self.raw.reward_manager._step_reward[:, index].clone()
        return reward.clone(), failed, timeout.clone(), info

    def close(self):
        self.raw.close()


def make_flat_residual_torque_env_cfg(teacher_checkpoint, num_envs=1024, **kwargs):
    return TitaFlatResidualTorqueEnvCfg(teacher_checkpoint, num_envs=num_envs, **kwargs)
