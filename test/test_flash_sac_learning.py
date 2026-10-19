"""DESKTOP_DRY_RUN: FlashSAC learner contracts without Isaac Sim or hardware."""

import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "lab/ddt_lab/scripts"))

from flash_sac.runtime import (
    DEFAULT_TASK,
    create_agent_config,
    make_agent,
    read_checkpoint,
    save_checkpoint,
    setup_imports,
)

setup_imports(False)

import gymnasium as gym
import numpy as np
import torch

from flash_rl.buffers.torch_buffer import TorchUniformBuffer
from flash_rl.agents.flashSAC.update import _compute_categorical_td_target

torch.set_num_threads(2)


class FlashSACLearningTest(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        np.random.seed(42)
        self.env = SimpleNamespace(num_envs=4, actor_obs_dim=33, critic_obs_dim=36, action_dim=8)
        self.args = SimpleNamespace(
            seed=42, steps=20, updates_per_step=2.0, device="cpu", buffer_device="cpu",
            buffer_size=64, min_buffer=8, batch_size=8, n_step=3, compile=False, amp=False,
        )
        self.cfg = create_agent_config(self.args)

    def make_ready_agent(self):
        agent = make_agent(self.env, self.cfg)
        for step in range(4):
            agent.process_transition({
                "observation": torch.randn(4, 69),
                "action": torch.rand(4, 8) * 2 - 1,
                "next_observation": torch.randn(4, 69),
                "reward": torch.tensor([0.5, -0.2, 1.0, 0.3]) + step * 0.1,
                "terminated": torch.tensor([False, step == 1, False, False]),
                "truncated": torch.tensor([False, False, step == 0, False]),
            })
        self.assertTrue(agent.can_start_training())
        return agent

    @staticmethod
    def deterministic_actions(agent, observations):
        return agent.sample_actions(0, {"next_observation": observations}, training=False)

    def assert_nested_equal(self, expected, actual):
        if isinstance(expected, torch.Tensor):
            torch.testing.assert_close(expected, actual, rtol=0, atol=0)
        elif isinstance(expected, dict):
            self.assertEqual(expected.keys(), actual.keys())
            for key in expected:
                self.assert_nested_equal(expected[key], actual[key])
        elif isinstance(expected, (list, tuple)):
            self.assertEqual(len(expected), len(actual))
            for left, right in zip(expected, actual):
                self.assert_nested_equal(left, right)
        else:
            self.assertEqual(expected, actual)

    def test_real_updates_are_finite_and_change_actor_and_critic_weights(self):
        agent = self.make_ready_agent()
        actor_before = [parameter.detach().clone() for parameter in agent._actor.network.parameters()]
        critic_before = [parameter.detach().clone() for parameter in agent._critic.network.parameters()]
        actor_dims, critic_dims = [], []

        def record_actor(module, args, kwargs):
            actor_dims.append(kwargs["observations"].shape[-1])

        def record_critic(module, args, kwargs):
            critic_dims.append(kwargs["observations"].shape[-1])

        actor_hook = agent._actor.network.register_forward_pre_hook(record_actor, with_kwargs=True)
        critic_hook = agent._critic.network.register_forward_pre_hook(record_critic, with_kwargs=True)
        sampled_batch = agent._replay_buffer.sample(np.arange(8))
        target_discounts = []

        def record_target(**kwargs):
            self.assertIsInstance(kwargs["gamma"], torch.Tensor)
            target_discounts.append(kwargs["gamma"].clone())
            return _compute_categorical_td_target(**kwargs)

        try:
            with patch.object(agent._replay_buffer, "sample", side_effect=lambda: {
                key: value.clone() for key, value in sampled_batch.items()
            }), patch(
                "flash_rl.agents.flashSAC.update._compute_categorical_td_target", side_effect=record_target
            ):
                updates = [agent.update() for _ in range(3)]
        finally:
            actor_hook.remove()
            critic_hook.remove()

        self.assertEqual(agent._update_step, 3)
        self.assertIn("actor/loss", updates[0])
        self.assertIn("critic/loss", updates[0])
        for update in updates:
            self.assertTrue(all(np.isfinite(value) for value in update.values()), update)
        self.assertTrue(any(not torch.equal(before, after) for before, after in
                            zip(actor_before, agent._actor.network.parameters())))
        self.assertTrue(any(not torch.equal(before, after) for before, after in
                            zip(critic_before, agent._critic.network.parameters())))
        self.assertTrue(actor_dims)
        self.assertTrue(critic_dims)
        self.assertEqual(set(actor_dims), {33})
        self.assertEqual(set(critic_dims), {36})
        self.assertEqual(len(target_discounts), 3)
        for discount in target_discounts:
            torch.testing.assert_close(discount, sampled_batch["discount"])
        self.assertGreater(len(torch.unique(target_discounts[0])), 1)

    def test_actor_actions_do_not_depend_on_privileged_critic_observations(self):
        agent = self.make_ready_agent()
        agent.update()
        observations = torch.randn(4, 69)
        changed_critic = observations.clone()
        changed_critic[:, 33:] = 1000 * torch.randn(4, 36)
        np.testing.assert_array_equal(
            self.deterministic_actions(agent, observations),
            self.deterministic_actions(agent, changed_critic),
        )
        changed_policy = observations.clone()
        changed_policy[:, :33] += torch.randn(4, 33)
        self.assertFalse(np.array_equal(
            self.deterministic_actions(agent, observations),
            self.deterministic_actions(agent, changed_policy),
        ))

    def test_checkpoint_restores_actions_optimizers_and_update_step(self):
        agent = self.make_ready_agent()
        for _ in range(3):
            agent.update()
        observations = torch.randn(4, 69)
        expected_actions = self.deterministic_actions(agent, observations)
        with tempfile.TemporaryDirectory(prefix="flash_sac_checkpoint_", dir=REPO / "test") as temporary:
            path, saved = save_checkpoint(self.env, agent, {"test_config": True}, temporary, DEFAULT_TASK, 4)
            verified_path, metadata = read_checkpoint(path, DEFAULT_TASK)
            self.assertEqual(verified_path, path)
            self.assertEqual(metadata["actor_sha256"], saved["actor_sha256"])
            self.assertEqual(metadata["step"], 4)
            restored = make_agent(self.env, self.cfg)
            restored.load(str(path))
            self.assertEqual(restored._update_step, 3)
            np.testing.assert_array_equal(expected_actions, self.deterministic_actions(restored, observations))
            for name in ("_actor", "_critic", "_temperature"):
                original_network, restored_network = getattr(agent, name), getattr(restored, name)
                self.assert_nested_equal(original_network.optimizer.state_dict(), restored_network.optimizer.state_dict())
                self.assert_nested_equal(original_network.scheduler.state_dict(), restored_network.scheduler.state_dict())
            self.assert_nested_equal(agent._target_critic.network.state_dict(), restored._target_critic.network.state_dict())
            torch.testing.assert_close(agent.reward_normalizer.G_rms.mean, restored.reward_normalizer.G_rms.mean)
            torch.testing.assert_close(agent.reward_normalizer.G_rms.var, restored.reward_normalizer.G_rms.var)

    def test_checkpoint_hashes_detect_actor_and_environment_corruption(self):
        agent = self.make_ready_agent()
        with tempfile.TemporaryDirectory(prefix="flash_sac_integrity_", dir=REPO / "test") as temporary:
            path, _ = save_checkpoint(self.env, agent, {"test_config": True}, temporary, DEFAULT_TASK, 4)
            actor_path = path / "actor.pt"
            actor_original = actor_path.read_bytes()
            actor_path.write_bytes(actor_original + b"corrupted")
            with self.assertRaisesRegex(ValueError, "actor checkpoint SHA256 mismatch"):
                read_checkpoint(path, DEFAULT_TASK)
            actor_path.write_bytes(actor_original)
            env_path = path / "env.pkl"
            env_path.write_bytes(env_path.read_bytes() + b"corrupted")
            with self.assertRaisesRegex(ValueError, "saved environment config SHA256 mismatch"):
                read_checkpoint(path, DEFAULT_TASK)

    def test_parallel_n_step_returns_stop_at_timeout_and_termination(self):
        observations = gym.spaces.Box(-np.inf, np.inf, (4, 1), np.float32)
        actions = gym.spaces.Box(-1.0, 1.0, (4, 1), np.float32)
        buffer = TorchUniformBuffer(observations, actions, 3, 0.9, 16, 4, 4, "cpu")
        # Lanes: uninterrupted, timeout after one/two steps, terminal after two.
        for step, reward in enumerate((1.0, 2.0, 4.0)):
            buffer.add({
                "observation": torch.full((4, 1), float(step)),
                "action": torch.zeros(4, 1),
                "reward": torch.full((4,), reward),
                "next_observation": torch.full((4, 1), 10.0 + step),
                "terminated": torch.tensor([False, False, False, step == 1]),
                "truncated": torch.tensor([False, step == 0, step == 1, False]),
            })
        batch = buffer.sample(np.arange(4))
        torch.testing.assert_close(batch["reward"], torch.tensor([6.04, 1.0, 2.8, 2.8]))
        torch.testing.assert_close(batch["discount"], torch.tensor([0.729, 0.9, 0.81, 0.81]))
        torch.testing.assert_close(batch["next_observation"].flatten(), torch.tensor([12.0, 10.0, 11.0, 11.0]))
        torch.testing.assert_close(batch["terminated"], torch.tensor([0.0, 0.0, 0.0, 1.0]))
        torch.testing.assert_close(batch["truncated"], torch.tensor([0.0, 1.0, 1.0, 0.0]))
        buffer.add({
            "observation": torch.full((4, 1), 3.0), "action": torch.zeros(4, 1),
            "reward": torch.full((4,), 8.0), "next_observation": torch.full((4, 1), 13.0),
            "terminated": torch.zeros(4, dtype=torch.bool), "truncated": torch.zeros(4, dtype=torch.bool),
        })
        # Overlapping windows must retain untouched intermediate transitions.
        following = buffer.sample(np.arange(4, 8))
        torch.testing.assert_close(following["reward"], torch.tensor([12.08, 12.08, 2.0, 2.0]))
        torch.testing.assert_close(following["discount"], torch.tensor([0.729, 0.729, 0.9, 0.9]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
