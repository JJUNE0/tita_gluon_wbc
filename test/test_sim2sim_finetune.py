"""DESKTOP_DRY_RUN / VALIDATION_SIM: reward, replay boundaries and real learner updates."""

from dataclasses import replace
import importlib.util
from pathlib import Path
import sys
import unittest
from copy import deepcopy

import numpy as np

REPO = Path(__file__).resolve().parents[1]
ENTRY = REPO / 'sim2sim/sim2sim_ros2_jazzy/launch/sim2sim_finetune.py'
spec = importlib.util.spec_from_file_location('sim2sim_finetune', ENTRY)
ft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ft)
CHECKPOINT = REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_60000'


class SensorRewardTest(unittest.TestCase):
    def reward(self, **changes):
        values = dict(quaternion=np.array([1., 0., 0., 0.]), gyro=np.zeros(3),
                      joint_pos=np.zeros(8), joint_vel=np.zeros(8), command=np.zeros(3),
                      action=np.zeros(8), previous_action=np.zeros(8), radius=.0925, dt=.02)
        values.update(changes)
        return ft.sensor_reward(**values)

    def test_tracking_smoothness_and_fall_penalty(self):
        reference, fallen, speed, _ = self.reward()
        self.assertAlmostEqual(reference, .06)
        self.assertFalse(fallen)
        self.assertEqual(speed, 0.)
        self.assertLess(self.reward(action=np.ones(8))[0], reference)
        self.assertLess(self.reward(gyro=np.array([0., 0., 1.]))[0], reference)
        reward, fallen, _, _ = self.reward(quaternion=np.array([0., 1., 0., 0.]))
        self.assertTrue(fallen)
        self.assertLess(reward, -.9)

    def test_rolling_proxy_uses_leg_and_imu_rates_with_wheel_rates(self):
        dq = np.zeros(8)
        dq[[3, 7]] = 2.
        self.assertAlmostEqual(self.reward(joint_vel=dq)[2], .185)
        dq[[2, 6]] = -2.
        self.assertAlmostEqual(self.reward(joint_vel=dq)[2], 0.)
        self.assertAlmostEqual(self.reward(gyro=np.array([0., 1., 0.]))[2], .0925)
        matched = self.reward(joint_vel=np.array([0., 0., 0., 2., 0., 0., 0., 2.]), command=np.array([.185, 0., 0.]))[0]
        self.assertAlmostEqual(matched, .06)

    def test_nonfinite_feedback_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Non-finite'):
            self.reward(joint_vel=np.full(8, np.nan))


class FineTuneIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.path, self.cfg, _, self.meta = ft.describe_checkpoint(CHECKPOINT)
        source = next(Path(p) for p in self.cfg['policy_interface']['sources'] if Path(p).name == 'env.yaml')
        self.env = ft.FineTuneEnv(self.cfg, self.meta, ft.read_yaml(source), [0., 0., 0.], .02)
        self.addCleanup(self.env.close)

    def test_timeout_keeps_pre_reset_state_and_correct_action_units(self):
        action = np.linspace(-.1, .1, 8, dtype=np.float32)[None, :]
        next_obs, terminal, reward, terminated, truncated, info = self.env.step(action)
        expected_applied = action[0] * np.where(action[0] >= 0, self.env.positive, self.env.negative)
        self.assertFalse(terminated)
        self.assertTrue(truncated)
        self.assertEqual(next_obs.shape, (1, 69))
        np.testing.assert_allclose(terminal[0, 25:33], expected_applied)
        np.testing.assert_array_equal(next_obs[0, 25:33], np.zeros(8))
        np.testing.assert_allclose(terminal[0, 33], 2 * info['speed_proxy_m_s'], atol=1e-6)
        self.assertTrue(np.isfinite(reward))

    def test_observations_and_reward_do_not_read_simulator_translation_or_linear_velocity(self):
        original = self.env.observe()
        self.env.physics.data.qpos[:3] += [30., -20., 10.]
        self.env.physics.data.qvel[:3] = [4., 5., 6.]
        self.env.physics.mujoco.mj_forward(self.env.physics.model, self.env.physics.data)
        np.testing.assert_allclose(self.env.observe(), original, atol=1e-6)

    def test_tilt_is_termination_instead_of_timeout(self):
        self.env.physics.data.qpos[3:7] = [2 ** -.5, 2 ** -.5, 0., 0.]
        self.env.physics.mujoco.mj_forward(self.env.physics.model, self.env.physics.data)
        _, terminal, reward, terminated, truncated, _ = self.env.step(np.zeros((1, 8)))
        self.assertTrue(terminated)
        self.assertFalse(truncated)
        self.assertLess(reward, -.9)
        self.assertTrue(np.isfinite(terminal).all())

    def test_encoder_imu_velocity_correction_matches_finite_difference_fk(self):
        from scipy.spatial.transform import Rotation

        quaternion, _, q, _ = self.env.sensors()
        gyro = np.array([.03, -.08, .04])
        dq = np.array([.1, -.2, .3, .7, -.15, .1, -.25, .5])
        actual = self.env.forward_speed(quaternion, gyro, q, dq)
        data = self.env.kinematics
        offset = data.xpos[self.env.wheels].mean(0) - data.xpos[self.env.base_body]
        rotation = Rotation.from_quat(quaternion[[1, 2, 3, 0]])
        yaw = rotation.as_euler('xyz')[2]
        lateral = np.array([-np.sin(yaw), np.cos(yaw), 0.])
        forward = np.array([np.cos(yaw), np.sin(yaw), 0.])
        rolling = self.env.radius * (lateral @ rotation.apply(gyro)
                   + ((data.xaxis[self.env.joints] @ lateral) * dq).reshape(2, 4).sum(axis=1)).mean()
        epsilon = 1e-5
        advanced = (rotation * Rotation.from_rotvec(gyro * epsilon)).as_quat()[[3, 0, 1, 2]]
        self.env.forward_speed(advanced, gyro, q + epsilon * dq, dq)
        moved = data.xpos[self.env.wheels].mean(0) - data.xpos[self.env.base_body]
        expected = rolling - (moved - offset) @ forward / epsilon
        self.assertAlmostEqual(actual, expected, delta=5e-4)

    def test_actor_load_replay_critic_warmup_and_actor_update(self):
        ft.setup_imports(False)
        import torch
        from flash_rl.agents.flashSAC.agent import FlashSACConfig

        torch.set_num_threads(1)
        torch.manual_seed(42)
        cfg = replace(FlashSACConfig(**self.meta['agent']), device_type='cpu', buffer_device_type='cpu',
                      buffer_max_length=16, buffer_min_length=1, sample_batch_size=4,
                      n_step=1, use_compile=False, use_amp=False, load_optimizer=False, load_reward_normalizer=False)
        agent = ft.make_agent(self.env, cfg)
        agent._actor.load(str(self.path), load_optimizer=False)
        before_actor = {k: v.clone() for k, v in agent._actor.network.state_dict().items()}
        before_critic = {k: v.clone() for k, v in agent._critic.network.state_dict().items()}
        saved = torch.load(self.path, map_location='cpu', weights_only=True)['network_state_dict']
        for key, value in saved.items():
            torch.testing.assert_close(before_actor[key], value, rtol=0, atol=0)
        obs = self.env.reset()
        action = np.full((1, 8), .05, dtype=np.float32)
        next_obs, terminal, reward, terminated, truncated, _ = self.env.step(action)
        agent.process_transition(dict(observation=obs, action=action, next_observation=terminal,
                                      reward=np.array([reward], dtype=np.float32),
                                      terminated=np.array([terminated]), truncated=np.array([truncated])))
        self.assertTrue(agent.can_start_training())  # min_buffer=1 is mechanically supported.
        replay = agent._replay_buffer.sample()
        torch.testing.assert_close(replay['action'], torch.tensor(np.repeat(action, 4, axis=0)))
        torch.testing.assert_close(replay['next_observation'], torch.tensor(np.repeat(terminal, 4, axis=0)))
        self.assertTrue(replay['truncated'].bool().all())
        self.assertFalse(replay['terminated'].bool().any())
        metrics = ft.critic_warmup_update(agent)
        self.assertTrue(all(np.isfinite(v) for v in metrics.values()))
        for key, value in agent._actor.network.state_dict().items():
            torch.testing.assert_close(value, before_actor[key], rtol=0, atol=0)
        self.assertTrue(any(not torch.equal(v, before_critic[k]) for k, v in agent._critic.network.state_dict().items()))
        agent.update()  # step 1: critic only by the existing actor period.
        metrics = agent.update()  # step 2: actor + critic.
        self.assertTrue(all(np.isfinite(v) for v in metrics.values()))
        self.assertTrue(any(not torch.equal(v, before_actor[k]) for k, v in agent._actor.network.state_dict().items()))

    def test_demonstrations_mixed_replay_and_only_bias_updates_preserve_normalization(self):
        ft.setup_imports(False)
        import torch
        from flash_rl.agents.flashSAC.agent import FlashSACConfig

        torch.set_num_threads(1)
        torch.manual_seed(42)
        cfg = replace(FlashSACConfig(**self.meta['agent']), device_type='cpu', buffer_device_type='cpu',
                      buffer_max_length=64, buffer_min_length=1, sample_batch_size=4,
                      n_step=1, use_compile=False, use_amp=False)
        agent = ft.make_agent(self.env, cfg)
        agent._actor.load(str(self.path), load_optimizer=False)
        ft.constrain_actor(agent)
        prior = ft.demonstration_prior(agent, self.env, 8)
        self.assertEqual(len(prior['reward']), 8)
        self.assertEqual(prior['terminated'].dtype, torch.float32)
        self.assertEqual(prior['truncated'].dtype, torch.float32)
        self.assertEqual(len(agent._replay_buffer), 0)
        self.assertTrue(torch.equal(agent.reward_normalizer.G_r, torch.zeros_like(agent.reward_normalizer.G_r)))
        shifted = {key: value.clone() for key, value in prior.items()}
        shifted['reward'][:] = 123.
        transition = {key: value[:1] for key, value in prior.items() if key != 'discount'}
        agent.process_transition(transition)
        batch = ft.sample_batch(agent, shifted)
        self.assertEqual(int((batch['reward'] == 123.).sum()), 2)
        self.assertTrue(all(np.isfinite(v) for v in ft.critic_warmup_update(agent, batch).values()))
        before = {key: value.clone() for key, value in agent._actor.network.state_dict().items()}
        prior['action'][:, 3] += .02
        for _ in range(3):
            metrics = ft.constrained_actor_update(agent, prior, rl_weight=1e-5)
            self.assertTrue(all(np.isfinite(value) for value in metrics.values()))
        changed = []
        for key, value in agent._actor.network.state_dict().items():
            if not torch.equal(value, before[key]):
                changed.append(key)
        self.assertEqual(changed, ['predictor.mean_bias'])

    def test_actor_training_normalization_changes_without_any_optimizer_update(self):
        ft.setup_imports(False)
        import torch
        from export import load_policy

        actor = load_policy(self.path.parent, self.meta).actor
        original = deepcopy(actor.state_dict())
        data = torch.tensor(np.repeat(self.env.observe()[:, :33], 4, axis=0))
        with torch.no_grad():
            before = actor.get_mean_and_std(data, training=False)[0].clone()
            actor.get_mean_and_std(data, training=True)
            after = actor.get_mean_and_std(data, training=False)[0]
        self.assertFalse(torch.equal(before, after))
        for key, value in actor.named_parameters():
            torch.testing.assert_close(value, original[key], atol=0, rtol=0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
