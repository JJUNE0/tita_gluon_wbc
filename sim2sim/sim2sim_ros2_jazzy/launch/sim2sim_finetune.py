"""VALIDATION_SIM: sensor-reward FlashSAC actor fine-tuning in MuJoCo, without ROS.

Requires torch, gymnasium, mujoco and PyYAML in the same Python environment.
Each invocation warm-starts the actor and collects simulation demonstrations.
Only eight output biases adapt; normalization/feature weights remain fixed.
The FlashSAC critic is fitted anew, with BC-constrained deterministic actor updates.
"""

import argparse
from copy import deepcopy
from dataclasses import asdict, replace
from datetime import datetime
import json
import math
from pathlib import Path
import shutil
import sys
from zoneinfo import ZoneInfo

import numpy as np

PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[1]
sys.path.insert(0, str(PACKAGE))
sys.path.insert(0, str(REPO / 'lab/ddt_lab/scripts/flash_sac'))

from sim2sim_ros2_jazzy.adapter import ActionAdapter, ObservationBuilder, ObsState, quat_wxyz_to_rotmat
from sim2sim_ros2_jazzy.checkpoint import describe_checkpoint, observation_layout, read_yaml, sha256
from runtime import action_mapping_kwargs, make_agent, setup_imports


def sensor_reward(quaternion, gyro, joint_pos, joint_vel, command, action, previous_action, radius, dt,
                  forward_speed=None):
    """IMU + encoders + normalized actions only; no simulator root/contact state.

    Rolling speed is a no-slip wheel-axle proxy, NOT measured base velocity.
    The TITA hip rotates about base x; shoulder/knee/wheel axes share base y
    at zero hip angle. Include their rates and body pitch rate in rolling speed.
    Real encoders/IMU must be calibrated to these URDF signs and body frame.
    """
    rotation = quat_wxyz_to_rotmat(quaternion)
    yaw = math.atan2(rotation[1, 0], rotation[0, 0])
    lateral = rotation.T @ np.array([-math.sin(yaw), math.cos(yaw), 0.])
    gravity = rotation.T @ np.array([0., 0., -1.])
    hips = joint_pos[[0, 4]]
    axes = np.column_stack((np.zeros(2), np.cos(hips), np.sin(hips)))
    rolling_rates = lateral @ gyro + (axes @ lateral) * joint_vel.reshape(2, 4)[:, 1:].sum(axis=1)
    speed = float(radius * rolling_rates.mean()) if forward_speed is None else float(forward_speed)
    fallen = bool(gravity[2] > -0.5)  # More than 60 degrees from upright.
    terms = {
        'forward_tracking': 2. * math.exp(-((speed - command[0]) / .25) ** 2),
        'yaw_tracking': math.exp(-((gyro[2] - command[2]) / .5) ** 2),
        'tilt': -5. * float(gravity[:2] @ gravity[:2]),
        'angular_motion': -.05 * float(gyro[:2] @ gyro[:2]),
        'action_change': -.01 * float(np.square(action - previous_action).sum()),
    }
    reward = dt * sum(terms.values()) - float(fallen)
    if not np.isfinite([reward, speed, *terms.values()]).all():
        raise ValueError('Non-finite sensor reward')
    return reward, fallen, speed, terms


class FineTuneEnv:
    """Reuse playback physics/PD and checkpoint layouts; add RL episode semantics."""

    num_envs = 1

    def __init__(self, cfg, metadata, saved_env, command, episode_seconds, viewer=False):
        from sim2sim_ros2_jazzy.mujoco_env import TitaMujocoEnv

        self.cfg = cfg
        self.device = 'cpu'
        self.actor_obs_dim = metadata['actor_obs_dim']
        self.critic_obs_dim = metadata['critic_obs_dim']
        self.action_dim = metadata['action_dim']
        self.actor_builder = ObservationBuilder(cfg)
        critic_cfg = deepcopy(cfg)
        critic_cfg['policy_interface']['observations'] = observation_layout(
            saved_env['observations']['critic'], {}, cfg['policy_interface']['articulation_joint_names'])
        critic_cfg['policy']['obs_dim'] = self.critic_obs_dim
        if sum(term['size'] for term in critic_cfg['policy_interface']['observations']) != self.critic_obs_dim:
            raise ValueError('Saved critic observation layout has the wrong dimension')
        self.critic_builder = ObservationBuilder(critic_cfg)
        self.adapter = ActionAdapter(cfg)
        gains = action_mapping_kwargs(metadata)
        self.negative = np.asarray(gains['action_gain_negative'], dtype=np.float32)
        self.positive = np.asarray(gains['action_gain_positive'], dtype=np.float32)
        self.command = np.asarray(command, dtype=np.float32)
        self.episode_steps = max(1, math.ceil(episode_seconds / (cfg['control']['sim_timestep'] * cfg['control']['decimation'])))
        self.physics = TitaMujocoEnv(cfg, viewer_enabled=viewer)
        try:
            radii = []
            for name in ('left_leg_4', 'right_leg_4'):
                body = self.physics.model.body(name).id
                geoms = [g for g in range(self.physics.model.ngeom)
                         if self.physics.model.geom_bodyid[g] == body
                         and self.physics.model.geom_type[g] == self.physics.mujoco.mjtGeom.mjGEOM_CYLINDER]
                if len(geoms) != 1:
                    raise ValueError('Expected one wheel collision cylinder per side')
                radii.append(self.physics.model.geom_size[geoms[0], 0])
            if min(radii) <= 0 or not np.allclose(radii, radii[0]):
                raise ValueError('Expected equal positive wheel radii')
            self.radius = float(radii[0])
            self.kinematics = self.physics.mujoco.MjData(self.physics.model)
            self.joints = np.array([self.physics.model.joint(name).id for name in self.physics.joint_names])
            self.wheels = self.physics.model.jnt_bodyid[self.joints[[3, 7]]]
            self.base_body = self.physics.model.body('base_link').id
            self.reset()
        except BaseException:
            self.close()
            raise

    def reset(self):
        self.physics.reset()  # Start in the checkpoint pose, directly in RL.
        self.last_applied = np.zeros(self.action_dim, dtype=np.float32)
        self.last_normalized = self.last_applied.copy()
        self.age = 0
        return self.observe()

    def sensors(self):
        return (self.physics.base_quat_sensor(), self.physics.base_ang_vel(),
                self.physics.joint_pos(), self.physics.joint_vel())

    def observe(self):
        quaternion, gyro, q, dq = self.sensors()
        speed = self.forward_speed(quaternion, gyro, q, dq)
        state = ObsState(q, dq, quaternion, gyro, self.command, self.last_applied,
                         np.array([speed, 0., 0.], dtype=np.float32))
        return np.concatenate((self.actor_builder.build(state), self.critic_builder.build(state)))[None, :]

    def forward_speed(self, quaternion, gyro, q, dq):
        """No-slip base speed from encoders/IMU and URDF FK; no plant root state.

        A separate kinematic model uses a zero root translation and measured
        orientation/joints. Subtract axle motion relative to the base, including
        body rotation, from rolling speed. The same geometry is available on hardware.
        """
        data, model = self.kinematics, self.physics.model
        data.qpos[:3] = 0.
        data.qpos[3:7] = quaternion
        data.qpos[self.physics.qpos_addr] = q
        self.physics.mujoco.mj_kinematics(model, data)
        rotation = quat_wxyz_to_rotmat(quaternion)
        yaw = math.atan2(rotation[1, 0], rotation[0, 0])
        forward = np.array([math.cos(yaw), math.sin(yaw), 0.])
        lateral = np.array([-math.sin(yaw), math.cos(yaw), 0.])
        omega = rotation @ gyro
        rates = lateral @ omega + ((data.xaxis[self.joints] @ lateral) * dq).reshape(2, 4).sum(axis=1)
        relative = []
        for side, wheel in enumerate(self.wheels):
            ids = self.joints[side * 4:side * 4 + 4]
            arm = data.xpos[wheel] - data.xanchor[ids]
            joint_motion = (np.cross(data.xaxis[ids], arm) * dq[side * 4:side * 4 + 4, None]).sum(axis=0)
            relative.append(np.cross(omega, data.xpos[wheel] - data.xpos[self.base_body]) + joint_motion)
        return float(self.radius * rates.mean() - np.mean(relative, axis=0) @ forward)

    def step(self, action):
        action = np.asarray(action, dtype=np.float32)
        if action.shape != (1, self.action_dim) or not np.isfinite(action).all():
            raise ValueError('Expected a finite normalized (1, 8) action')
        normalized = np.clip(action[0], -1., 1.)
        applied = normalized * np.where(normalized >= 0, self.positive, self.negative)
        self.physics.step_with_torque_callback(lambda q, dq: self.adapter.compute(applied, q, dq))
        self.physics.mujoco.mj_forward(self.physics.model, self.physics.data)
        quaternion, gyro, q, dq = self.sensors()
        reward, terminated, speed, terms = sensor_reward(
            quaternion, gyro, q, dq, self.command, normalized, self.last_normalized, self.radius, self.physics.control_dt,
            forward_speed=self.forward_speed(quaternion, gyro, q, dq))
        self.last_applied, self.last_normalized = applied.copy(), normalized.copy()
        self.age += 1
        truncated = self.age >= self.episode_steps and not terminated
        terminal_observation = self.observe()  # Capture before automatic reset, including timeout.
        # Ground truth is diagnostic only; neither the reward nor learner reads it.
        gt_velocity = quat_wxyz_to_rotmat(quaternion).T @ self.physics.base_lin_vel()
        info = dict(speed_proxy_m_s=speed, diagnostic_gt_vx_m_s=float(gt_velocity[0]),
                    gyro_z_rad_s=float(gyro[2]), diagnostic_gt_xy_m=self.physics.base_pos()[:2].tolist(), reward_terms=terms)
        next_observation = self.reset() if terminated or truncated else terminal_observation.copy()
        return next_observation, terminal_observation, reward, terminated, truncated, info

    def close(self):
        self.physics.close()


def teacher_action(env, action, law):
    """Simulation demonstration: source policy plus existing sensor-only velocity PI.

    Return the equivalent normalized action so replay and last_action include
    the intervention. No hidden residual is used by the exported student.
    """
    quaternion, gyro, q, dq = env.sensors()
    speed = env.forward_speed(quaternion, gyro, q, dq)
    rotation = quat_wxyz_to_rotmat(quaternion)
    enabled = (np.max(np.abs(env.command)) <= .01 and env.age * env.physics.control_dt >= 1.2
               and rotation[2, 2] >= math.cos(.3) and abs(speed) <= 1.)
    bias = law.update(speed, env.physics.control_dt, enabled=enabled)
    result = np.asarray(action, dtype=np.float32).copy()
    for policy_joint, native_joint in enumerate(env.adapter.order):
        if native_joint in (3, 7):
            gain = env.positive[policy_joint]  # Current TITA wheel gains are symmetric.
            if not np.isclose(gain, env.negative[policy_joint]):
                raise ValueError('Demonstration requires symmetric wheel action gains')
            result[:, policy_joint] += bias / (env.radius * env.adapter.scale[policy_joint] * gain)
    return np.clip(result, -1., 1.)


def sample_batch(agent, prior=None):
    """RLPD-inspired 50/50 demonstration/online sampling, with 1-step targets."""
    import torch

    batch = agent._replay_buffer.sample()
    if prior is not None:
        count = agent.cfg.sample_batch_size // 2
        ids = torch.randint(len(prior['reward']), (count,))
        batch = {key: torch.cat((value[count:], prior[key][ids].to(value))) for key, value in batch.items()}
    return batch


def critic_warmup_update(agent, batch=None):
    """Use the existing FlashSAC critic/target kernels without updating the actor."""
    from flash_rl.agents.flashSAC.update import update_critic, update_target_network

    batch = agent._replay_buffer.sample() if batch is None else batch
    batch = {key: value.to(agent._device) for key, value in batch.items()}
    offset = agent._actor_observation_dim
    batch['actor_next_observation'] = batch['next_observation'][:, :offset]
    batch['observation'] = batch['observation'][:, offset:]
    batch['next_observation'] = batch['next_observation'][:, offset:]
    if agent.reward_normalizer is not None:
        batch['reward'] = agent.reward_normalizer.normalize_rewards(batch['reward'])
    metrics = update_critic(actor=agent._actor, critic=agent._critic, target_critic=agent._target_critic,
                            temperature=agent._temperature, batch=batch, min_v=agent.cfg.critic_min_v,
                            max_v=agent.cfg.critic_max_v, num_bins=agent.cfg.critic_num_bins,
                            gamma=agent.cfg.gamma, n_step=agent.cfg.n_step, device=agent._device,
                            use_amp=False, grad_scaler=agent._grad_scaler)
    metrics.update(update_target_network(target_network=agent._target_critic))
    agent._update_step += 1
    return {key: float(value) for key, value in metrics.items()}


def demonstration_prior(agent, env, steps):
    """Collect calibrated simulation teacher transitions before changing the actor."""
    import torch
    from sim2sim_ros2_jazzy.velocity_bias import VelocityBias

    rows = []
    original_length = env.episode_steps
    env.episode_steps = steps + 1
    obs = env.reset()
    law = VelocityBias()
    try:
        for step in range(steps):
            action = agent.sample_actions(step, {'next_observation': obs}, training=False)
            action = teacher_action(env, action, law)
            nxt, terminal, reward, done, timeout, _ = env.step(action)
            transition = dict(observation=obs, action=action, next_observation=terminal,
                              reward=np.array([reward], dtype=np.float32), terminated=np.array([done]),
                              truncated=np.array([timeout]))
            agent.process_transition(transition)
            rows.append(transition)
            obs = nxt
            if done:
                raise RuntimeError('Demonstration teacher fell; refusing to clone this rollout')
    finally:
        env.episode_steps = original_length
        env.reset()
    prior = {key: torch.as_tensor(np.concatenate([row[key] for row in rows])) for key in rows[0]}
    for key in ('terminated', 'truncated'):
        prior[key] = prior[key].float()  # FlashSAC TD targets use arithmetic masks.
    prior['discount'] = torch.full_like(prior['reward'], agent.cfg.gamma)
    agent._replay_buffer.reset()  # Keep demonstrations separate from online replay.
    if agent.reward_normalizer is not None:
        agent.reward_normalizer.G_r.zero_()  # Online physics starts a new episode.
    return prior


def constrain_actor(agent):
    """Adapt eight output biases; preserve feature weights, exploration and BN statistics."""
    agent._actor.network.requires_grad_(False)
    agent._actor.network.predictor.mean_bias.requires_grad_(True)


def constrained_actor_update(agent, prior, rl_weight=0.):
    """BC-regularized deterministic actor improvement using the FlashSAC critic.

    All forwards use inference normalization even while differentiating. The
    pretrained representation and its running statistics remain unchanged.
    This is a conservative hybrid, not a reproduction of standard FlashSAC/RLPD.
    """
    import torch

    ids = torch.randint(len(prior['reward']), (agent.cfg.sample_batch_size,))
    obs = prior['observation'][ids].to(agent._device)
    targets = prior['action'][ids].to(agent._device)
    mean, _ = agent._actor.network.get_mean_and_std(obs[:, :agent._actor_observation_dim], training=False)
    action = mean.tanh()
    bc = (action - targets).square().mean()
    agent._critic.network.requires_grad_(False)
    try:
        q = agent._critic(observations=obs[:, agent._critic_offset:], actions=action, training=False)[0].min(dim=0).values.mean()
        loss = bc - rl_weight * q
        agent._actor.optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_([agent._actor.network.predictor.mean_bias], 1.)
        agent._actor.optimizer.step()
    finally:
        agent._critic.network.requires_grad_(True)
    return {'actor/loss': float(loss.detach()), 'actor/bc_loss': float(bc.detach()), 'actor/q': float(q.detach())}


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ckpt', type=Path, default=REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_60000')
    parser.add_argument('--steps', type=int, default=10000, help='New simulator transitions this run')
    parser.add_argument('--min_buffer', type=int, default=256)
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--buffer_size', type=int, default=50000)
    parser.add_argument('--critic_warmup', type=int, default=1000, help='Critic-only updates on the demonstration replay')
    parser.add_argument('--teacher_steps', type=int, default=3000, help='Simulation-only source+sensor-feedback demonstration transitions')
    parser.add_argument('--bc_steps', type=int, default=500, help='Behavior-cloning updates before online interaction')
    parser.add_argument('--bc_learning_rate', type=float, default=1e-4)
    parser.add_argument('--rl_weight', type=float, default=1e-5, help='Q improvement weight relative to demonstration BC')
    parser.add_argument('--learning_rate', type=float, default=1e-5)
    parser.add_argument('--noise_scale', type=float, default=.1, help='Scale of FlashSAC repeated Gaussian exploration; 0 is deterministic')
    parser.add_argument('--device', default='cpu')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--vx', type=float, default=0.)
    parser.add_argument('--yaw_rate', type=float, default=0.)
    parser.add_argument('--episode_seconds', type=float, default=10.)
    parser.add_argument('--save_every', type=int, default=5000)
    parser.add_argument('--viewer', action='store_true')
    parser.add_argument('--eval', action='store_true', help='Deterministic evaluation without updates or checkpoint writes')
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if min(args.steps, args.min_buffer, args.batch_size, args.buffer_size, args.save_every, args.teacher_steps) < 1 or min(args.critic_warmup, args.bc_steps) < 0:
        parser.error('Counts must be positive; critic_warmup may be zero')
    if args.batch_size % 2 or args.batch_size < 2:
        parser.error('batch_size must be positive and even for 50/50 replay sampling')
    if args.buffer_size < max(args.min_buffer, args.batch_size):
        parser.error('buffer_size must cover min_buffer and batch_size')
    if not np.isfinite([args.learning_rate, args.bc_learning_rate, args.rl_weight, args.noise_scale, args.episode_seconds, args.vx, args.yaw_rate]).all():
        parser.error('Numeric arguments must be finite')
    if min(args.learning_rate, args.bc_learning_rate) <= 0 or min(args.noise_scale, args.rl_weight) < 0 or args.episode_seconds <= 0:
        parser.error('learning_rate/episode_seconds must be positive and noise_scale nonnegative')
    path, cfg, _, metadata = describe_checkpoint(args.ckpt)
    if cfg['policy_interface']['algorithm'] != 'FlashSAC' or (metadata['actor_obs_dim'], metadata['critic_obs_dim'], metadata['action_dim']) != (33, 36, 8):
        parser.error('Requires the TITA FlashSAC 33/36/8 checkpoint interface')
    if abs(args.vx) > cfg['command']['max_lin_x'] or abs(args.yaw_rate) > cfg['command']['max_ang_z']:
        parser.error('Command exceeds sim2sim command limits')
    setup_imports(False)
    import torch
    from flash_rl.agents.flashSAC.agent import FlashSACConfig, _sample_flashsac_actions

    torch.set_num_threads(1)
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    now = datetime.now(ZoneInfo('Asia/Seoul'))
    output = REPO / 'docs/exp' / now.strftime('%Y-%m-%d') / now.strftime('sim2sim_finetune_%H%M%S_%f')
    output.mkdir(parents=True, exist_ok=False)
    source_env = next(Path(source) for source in cfg['policy_interface']['sources'] if Path(source).name == 'env.yaml')
    env = None
    result = dict(execution_domain='VALIDATION_SIM', evidence_status='BLOCKED', source_checkpoint=str(path),
                  checkpoint_sha256=sha256(path), steps=0, updates=0, actor_updates=0, falls=0, timeouts=0,
                  implementation_sha256=sha256(Path(__file__)), reward_objective='sensor_reward_v2_fk',
                  critic_velocity='encoder_imu_base_fk', prior_transitions=0, bc_updates=0,
                  actor_scope='eight_mean_biases', algorithm='FlashSAC_critic_BC_constrained_actor',
                  mode='evaluation' if args.eval else 'demonstration_assisted_online_finetune',
                  args={key: str(value) if isinstance(value, Path) else value for key, value in vars(args).items()})
    try:
        env = FineTuneEnv(cfg, metadata, read_yaml(source_env), [args.vx, 0., args.yaw_rate], args.episode_seconds, args.viewer)
        result.update(control_dt=env.physics.control_dt, wheel_radius_m=env.radius)
        learner_cfg = replace(FlashSACConfig(**metadata['agent']), seed=args.seed, device_type=args.device,
                              buffer_device_type='cpu', buffer_max_length=args.buffer_size,
                              buffer_min_length=args.min_buffer, sample_batch_size=args.batch_size,
                              learning_rate_init=args.learning_rate, learning_rate_peak=args.learning_rate,
                              learning_rate_end=args.learning_rate, learning_rate_warmup_step=0,
                              learning_rate_decay_step=max(1, args.steps), n_step=1,
                              load_optimizer=False, load_reward_normalizer=False, use_compile=False, use_amp=False)
        agent = make_agent(env, learner_cfg)
        agent._actor.load(str(path), load_optimizer=False)
        for name in ('env.yaml', 'policy_interface.json'):
            source = next((Path(s) for s in cfg['policy_interface']['sources'] if Path(s).name == name), None)
            if source:
                shutil.copyfile(source, output / name)
        (output / 'agent.json').write_text(json.dumps(asdict(agent.cfg), indent=2) + '\n')
        (output / 'finetune.json').write_text(json.dumps(result, indent=2) + '\n')

        def save(step):
            destination = output / f'model_{step}'
            agent.save(str(destination))
            agent.save_replay_buffer(str(destination))
            saved = dict(metadata, agent=asdict(agent.cfg), step=step, execution_domain='VALIDATION_SIM',
                         actor_sha256=sha256(destination / 'actor.pt'), replay_saved=True,
                         finetune_objective='sensor_reward_v2_fk', critic_velocity='encoder_imu_base_fk',
                         actor_scope='eight_mean_biases', algorithm=result['algorithm'],
                         source_actor_sha256=result['checkpoint_sha256'])
            saved.pop('env_config_sha256', None)  # No env.pkl: Isaac --resume must not restore the old objective.
            (destination / 'ddt.json').write_text(json.dumps(saved, indent=2) + '\n')
            result['output_checkpoint'] = str(destination)
            result['output_actor_sha256'] = saved['actor_sha256']

        prior = None
        if not args.eval:
            constrain_actor(agent)
            prior = demonstration_prior(agent, env, args.teacher_steps)
            torch.save(prior, output / 'prior.pt')
            result['prior_transitions'] = len(prior['reward'])
            for group in agent._actor.optimizer.param_groups:
                group['lr'] = args.bc_learning_rate
            for _ in range(args.bc_steps):
                metrics = constrained_actor_update(agent, prior)
                if not all(math.isfinite(value) for value in metrics.values()):
                    raise RuntimeError('Non-finite behavior cloning update')
                result['bc_updates'] += 1
            save(0)  # Preserve BC-only ablation, before online Q-driven updates.
            for group in agent._actor.optimizer.param_groups:
                group['lr'] = args.learning_rate
            for _ in range(args.critic_warmup):
                ids = torch.randint(len(prior['reward']), (args.batch_size,))
                metrics = critic_warmup_update(agent, {key: value[ids] for key, value in prior.items()})
                if not all(math.isfinite(value) for value in metrics.values()):
                    raise RuntimeError('Non-finite critic warmup update')
                result['updates'] += 1
            print(f'[VALIDATION_SIM] prior={result["prior_transitions"]} BC={result["bc_updates"]} critic_warmup={result["updates"]}', flush=True)

        obs = env.reset()
        reward_sum = proxy_error_sum = gt_error_sum = 0.
        latest = {}
        with (output / 'metrics.jsonl').open('w') as stream:
            for step in range(1, args.steps + 1):
                if not env.physics.is_running():
                    break
                actor_obs = torch.as_tensor(obs[:, :env.actor_obs_dim], device=agent._device)
                with torch.no_grad():
                    agent._cached_noise, action, agent._cur_noise_repeat_count, agent._cur_noise_repeat_n = _sample_flashsac_actions(
                        agent._actor, agent._cached_noise, actor_obs, 0. if args.eval else args.noise_scale,
                        agent._cur_noise_repeat_count, agent._cur_noise_repeat_n, agent._zeta_cdf)
                action = action.cpu().numpy()
                next_obs, replay_next, reward, terminated, truncated, info = env.step(action)
                if not args.eval:
                    agent.process_transition(dict(observation=obs, action=action, next_observation=replay_next,
                                                  reward=np.array([reward], dtype=np.float32),
                                                  terminated=np.array([terminated]), truncated=np.array([truncated])))
                    if agent.can_start_training():
                        latest = critic_warmup_update(agent, sample_batch(agent, prior))
                        if agent._update_step % agent.cfg.actor_update_period == 0:
                            latest.update(constrained_actor_update(agent, prior, args.rl_weight))
                            result['actor_updates'] += 1
                        if not all(math.isfinite(value) for value in latest.values()):
                            raise RuntimeError('Non-finite FlashSAC update')
                        result['updates'] += 1
                reward_sum += reward
                proxy_error_sum += (info['speed_proxy_m_s'] - args.vx) ** 2
                gt_error_sum += (info['diagnostic_gt_vx_m_s'] - args.vx) ** 2
                result.update(steps=step, falls=result['falls'] + int(terminated), timeouts=result['timeouts'] + int(truncated),
                              reward_mean=reward_sum / step, speed_proxy_rmse_m_s=math.sqrt(proxy_error_sum / step),
                              diagnostic_gt_vx_rmse_m_s=math.sqrt(gt_error_sum / step))
                stream.write(json.dumps(dict(step=step, reward=reward, terminated=terminated, truncated=truncated,
                                             **info, **latest), allow_nan=False) + '\n')
                obs = next_obs
                if terminated or truncated:
                    agent._cur_noise_repeat_count.zero_()
                if step % 100 == 0 or step == args.steps:
                    stream.flush()
                    print(f'[VALIDATION_SIM] step={step} updates={result["updates"]} falls={result["falls"]} reward={reward:.5f}', flush=True)
                if not args.eval and step % args.save_every == 0:
                    save(step)
        if not args.eval and result['steps'] and result.get('output_checkpoint') != str(output / f'model_{result["steps"]}'):
            save(result['steps'])
        completed = result['steps'] == args.steps and (args.eval or result['actor_updates'] > 0)
        result.update(evidence_status='PASS' if completed else 'SUSPICIOUS',
                      detail='Finite execution only; policy improvement and hardware readiness are not established.')
    except KeyboardInterrupt:
        result.update(evidence_status='SUSPICIOUS', detail='Operator interrupted; use the last periodic checkpoint.')
    except Exception as error:
        result.update(evidence_status='FAIL', detail=f'{type(error).__name__}: {error}')
        raise
    finally:
        if env:
            env.close()
        (output / 'result.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
        output.with_name(output.name + '_summary.md').write_text(
            f'# MuJoCo FlashSAC fine-tuning\n\nExecution Domain: VALIDATION_SIM\n\n'
            f'Evidence Status: {result["evidence_status"]}\n\nPolicy Checkpoint SHA256: {result["checkpoint_sha256"]}\n\n'
            f'Observed metrics / behavior / log summary:\n\n```json\n{json.dumps(result, indent=2)}\n```\n')
        print('[VALIDATION_SIM] ' + json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
