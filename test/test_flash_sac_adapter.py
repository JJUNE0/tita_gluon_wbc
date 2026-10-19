"""DESKTOP_DRY_RUN: CPU regression tests for FlashSAC/Isaac boundary semantics."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest

import torch


_MODULE_PATH = Path(__file__).resolve().parents[1] / "lab/ddt_lab/scripts/flash_sac/env_adapter.py"
_SPEC = importlib.util.spec_from_file_location("tita_flash_sac_env_adapter", _MODULE_PATH)
adapter_module = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(adapter_module)


class FakeObservationManager:
    def __init__(self, env):
        self.env = env
        self.group_obs_dim = {"policy": (33,), "critic": (36,), "estimator_target": (3,)}
        self._group_obs_term_cfgs = {
            name: [SimpleNamespace(history_length=0, modifiers=None)] for name in self.group_obs_dim
        }
        self.history_updates = 0
        self.group_calls = []
        self.cached = {"policy": env.policy, "critic": env.critic, "estimator_target": env.estimator_target}

    def compute_group(self, name, update_history=False):
        self.group_calls.append((name, update_history))
        if update_history:
            self.history_updates += 1
        return self.cached[name]

    def compute(self, update_history=False):
        if update_history:
            self.history_updates += 1
        return self.cached


class FakeManagerBasedRLEnv:
    """Reproduce native physics -> done -> reset -> obs ordering with reused buffers."""

    def __init__(self):
        self.device = "cpu"
        self.num_envs = 3
        self.policy = torch.ones(3, 33)
        self.critic = torch.full((3, 36), 10.0)
        self.estimator_target = torch.full((3, 3), 9999.0)
        self.observation_manager = FakeObservationManager(self)
        self.action_manager = SimpleNamespace(total_action_dim=8)
        self.reward = torch.ones(3)
        self.terminated = torch.zeros(3, dtype=torch.bool)
        self.truncated = torch.zeros(3, dtype=torch.bool)
        self.next_terminated = torch.zeros(3, dtype=torch.bool)
        self.next_truncated = torch.zeros(3, dtype=torch.bool)
        self.closed = False
        self._reset_idx(torch.arange(self.num_envs))

    def _reset_idx(self, env_ids):
        self.policy[env_ids] = -100.0
        self.critic[env_ids] = -1000.0

    def reset(self, **kwargs):
        self._reset_idx(torch.arange(self.num_envs))
        self.policy[:] = 1.0
        self.critic[:] = 10.0
        return self.observation_manager.compute(), {"seed": kwargs.get("seed")}

    def step(self, action):
        self.applied_action = action
        self.policy.add_(2.0)
        self.critic.add_(20.0)
        self.reward.add_(0.5)
        self.terminated.copy_(self.next_terminated)
        self.truncated.copy_(self.next_truncated)
        done_ids = (self.terminated | self.truncated).nonzero(as_tuple=False).squeeze(-1)
        if done_ids.numel():
            self._reset_idx(done_ids)
        observations = self.observation_manager.compute(update_history=True)
        return observations, self.reward, self.terminated, self.truncated, {"log": {"episode": "fake"}}

    def close(self):
        self.closed = True


class FlashSACAdapterTests(unittest.TestCase):
    def setUp(self):
        self.raw = adapter_module.make_flash_sac_env_class(FakeManagerBasedRLEnv)()
        self.env = adapter_module.TitaFlashSACEnv(self.raw)
        self.env.reset(seed=123)

    def test_runtime_dimensions_and_critic_are_independent(self):
        self.assertEqual((self.env.actor_obs_dim, self.env.critic_obs_dim, self.env.action_dim), (33, 36, 8))
        observation = self.env.reset()
        self.assertEqual(observation.shape, (3, 69))
        torch.testing.assert_close(observation[:, :33], torch.ones(3, 33))
        torch.testing.assert_close(observation[:, 33:], torch.full((3, 36), 10.0))
        self.assertFalse(torch.any(observation == 9999.0))
        self.raw.critic[:] = 500.0
        next_obs, *_ = self.env.step(torch.zeros(3, 8))
        torch.testing.assert_close(next_obs[:, :33], torch.full((3, 33), 3.0))
        torch.testing.assert_close(next_obs[:, 33:], torch.full((3, 36), 520.0))

    def test_timeout_and_termination_use_true_terminal_not_reset_observations(self):
        self.raw.next_truncated[0] = True
        self.raw.next_terminated[1] = True
        next_obs, replay_next, _, terminated, truncated, _ = self.env.step(torch.zeros(3, 8))
        torch.testing.assert_close(next_obs[:2, :33], torch.full((2, 33), -100.0))
        torch.testing.assert_close(next_obs[:2, 33:], torch.full((2, 36), -1000.0))
        torch.testing.assert_close(replay_next[:2, :33], torch.full((2, 33), 3.0))
        torch.testing.assert_close(replay_next[:2, 33:], torch.full((2, 36), 30.0))
        torch.testing.assert_close(next_obs[2], replay_next[2])
        self.assertEqual(terminated.tolist(), [False, True, False])
        self.assertEqual(truncated.tolist(), [True, False, False])
        self.assertEqual(self.raw.observation_manager.group_calls, [("policy", False), ("critic", False)])
        self.assertEqual(self.raw.observation_manager.history_updates, 1)

    def test_action_clipping_keeps_caller_tensor_and_native_transform(self):
        actions = torch.tensor([-3.0, -1.0, -0.5, 0.0, 0.5, 1.0, 3.0, 0.2]).repeat(3, 1)
        original = actions.clone()
        self.env.step(actions)
        torch.testing.assert_close(actions, original)
        torch.testing.assert_close(self.raw.applied_action, original.clamp(-1.0, 1.0))

    def test_observation_reward_and_done_snapshots_are_not_aliased(self):
        self.raw.next_truncated[0] = True
        result = self.env.step(torch.zeros(3, 8))
        saved = [value.clone() for value in result[:5]]
        self.raw.policy[:] = 42.0
        self.raw.critic[:] = 43.0
        self.raw.reward[:] = 99.0
        self.raw.terminated[:] = True
        self.raw.truncated[:] = False
        self.raw.flash_sac_terminal_observations["policy"][:] = 88.0
        for actual, expected in zip(result[:5], saved):
            torch.testing.assert_close(actual, expected)
        self.assertNotEqual(result[0].data_ptr(), result[1].data_ptr())
        self.raw.next_truncated[:] = False
        self.env.step(torch.zeros(3, 8))
        for actual, expected in zip(result[:5], saved):
            torch.testing.assert_close(actual, expected)

    def test_missing_terminal_capture_fails_instead_of_bootstrapping_reset(self):
        original_step = self.raw.step

        def lose_capture(action):
            output = original_step(action)
            self.raw.flash_sac_terminal_env_ids = None
            return output

        self.raw.step = lose_capture
        self.raw.next_truncated[0] = True
        with self.assertRaisesRegex(RuntimeError, "Missing or inconsistent pre-reset"):
            self.env.step(torch.zeros(3, 8))

    def test_invalid_shapes_and_nonfinite_values_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Expected actions"):
            self.env.step(torch.zeros(3, 7))
        with self.assertRaisesRegex(ValueError, "Non-finite"):
            self.env.step(torch.full((3, 8), float("nan")))
        self.raw.policy[0, 0] = float("inf")
        with self.assertRaisesRegex(ValueError, "Non-finite"):
            self.env.step(torch.zeros(3, 8))

    def test_history_and_modifier_configs_fail_before_training(self):
        term = self.raw.observation_manager._group_obs_term_cfgs["policy"][0]
        term.history_length = 10
        with self.assertRaisesRegex(ValueError, "history_length=0"):
            adapter_module.TitaFlashSACEnv(self.raw)
        term.history_length = 0
        term.modifiers = [object()]
        with self.assertRaisesRegex(ValueError, "modifiers"):
            adapter_module.TitaFlashSACEnv(self.raw)

    def test_native_env_without_capture_is_rejected(self):
        with self.assertRaisesRegex(TypeError, "make_flash_sac_env_class"):
            adapter_module.TitaFlashSACEnv(FakeManagerBasedRLEnv())

    def test_close_forwards_to_native_environment(self):
        self.env.close()
        self.assertTrue(self.raw.closed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
