"""DESKTOP_DRY_RUN: real FlashSAC loops with fake Isaac dependencies and CPU tensors."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

REPO = Path(__file__).resolve().parents[1]
ENTRYPOINTS = REPO / "lab/ddt_lab/scripts/flash_sac"
sys.path.insert(0, str(ENTRYPOINTS))


def load_entrypoint(name, filename):
    spec = importlib.util.spec_from_file_location(name, ENTRYPOINTS / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


train = load_entrypoint("tested_flash_sac_train", "train.py")
play = load_entrypoint("tested_flash_sac_play", "play.py")
train.setup_imports(False)

import numpy as np
import torch

torch.set_num_threads(2)


class FakeObservationManager:
    def __init__(self, env):
        self.env = env
        self.group_obs_dim = {"policy": (33,), "critic": (36,)}
        self._group_obs_term_cfgs = {
            group: [SimpleNamespace(history_length=0, modifiers=None)] for group in self.group_obs_dim
        }

    def compute_group(self, name, update_history=False):
        return getattr(self.env, name)

    def compute(self):
        return {name: self.compute_group(name) for name in self.group_obs_dim}


class FakeNativeEnv:
    """Native auto-reset ordering with the actual TITA observation/action dimensions."""

    instances = []

    def __init__(self, cfg):
        self.cfg = cfg
        self.num_envs = cfg.scene.num_envs
        self.device = cfg.sim.device
        self.policy = torch.zeros(self.num_envs, 33)
        self.critic = torch.zeros(self.num_envs, 36)
        self.observation_manager = FakeObservationManager(self)
        self.action_manager = SimpleNamespace(total_action_dim=8)
        self.actions = []
        self.steps = 0
        self.closed = False
        self._reset_idx(torch.arange(self.num_envs))
        self.instances.append(self)

    def _reset_idx(self, ids):
        self.policy[ids] = torch.linspace(-0.3, 0.3, 33)
        self.critic[ids] = torch.linspace(-0.4, 0.4, 36)

    def reset(self):
        self._reset_idx(torch.arange(self.num_envs))
        return self.observation_manager.compute(), {}

    def step(self, action):
        if not isinstance(action, torch.Tensor) or tuple(action.shape) != (self.num_envs, 8):
            raise ValueError("Entry point must deliver Torch actions with the native vector shape")
        self.actions.append(action.clone())
        self.steps += 1
        self.policy[:, :8] += action * 0.05
        self.critic[:, :8] += action * 0.1
        reward = 1 - action.square().mean(dim=-1)
        terminated = torch.zeros(self.num_envs, dtype=torch.bool)
        truncated = torch.zeros(self.num_envs, dtype=torch.bool)
        if self.steps % 3 == 0:
            truncated[0] = True
        if self.steps % 5 == 0 and self.num_envs > 1:
            terminated[1] = True
        ids = (terminated | truncated).nonzero(as_tuple=False).squeeze(-1)
        if ids.numel():
            self._reset_idx(ids)
        return self.observation_manager.compute(), reward, terminated, truncated, {"log": {"mock_metric": 1.0}}

    def close(self):
        self.closed = True


class FakeApp:
    instances = []

    def __init__(self):
        self.closed = False
        self.instances.append(self)

    def is_running(self):
        return not self.closed

    def close(self):
        self.closed = True


class FakeAppLauncher:
    def __init__(self, **kwargs):
        if kwargs["device"] != "cpu":
            raise ValueError("CPU integration tests cannot request GPU simulation")
        self.app = FakeApp()


def mocked_isaac_modules():
    modules = {}
    for name in (
        "isaaclab", "isaaclab.app", "isaaclab.envs", "isaaclab.utils", "isaaclab.utils.io",
        "isaaclab_tasks", "isaaclab_tasks.utils", "ddt_lab", "ddt_lab.tasks", "ddt_lab.policy_interface",
    ):
        module = ModuleType(name)
        module.__path__ = []
        modules[name] = module
    modules["isaaclab.app"].AppLauncher = FakeAppLauncher
    modules["isaaclab.envs"].ManagerBasedRLEnv = FakeNativeEnv

    def parse_env_cfg(task, device, num_envs):
        return SimpleNamespace(
            scene=SimpleNamespace(num_envs=num_envs), sim=SimpleNamespace(device=device), seed=0,
            observations=SimpleNamespace(estimator_target=SimpleNamespace(base_lin_vel="PPO supervision")),
        )

    def dump_yaml(filename, cfg):
        Path(filename).write_text(f"mock_num_envs: {cfg.scene.num_envs}\n")

    modules["isaaclab_tasks.utils"].parse_env_cfg = parse_env_cfg
    def load_cfg_from_registry(task, key):
        if key != "flash_sac_cfg_entry_point" or task != train.DEFAULT_TASK:
            raise ValueError("Expected the TITA FlashSAC task configuration entry point")
        return train.load_default_runner_cfg()

    modules["isaaclab_tasks.utils"].load_cfg_from_registry = load_cfg_from_registry
    modules["isaaclab.utils.io"].dump_yaml = dump_yaml
    modules["ddt_lab.policy_interface"].save_policy_interface = lambda env, path: Path(path).write_text("{}\n")
    for name, module in list(modules.items()):
        if "." in name:
            parent, child = name.rsplit(".", 1)
            setattr(modules[parent], child, module)
    return modules


class FlashSACEntrypointTest(unittest.TestCase):
    def test_train_resume_and_play_use_real_cpu_learner_and_torch_adapter(self):
        FakeNativeEnv.instances.clear()
        FakeApp.instances.clear()
        agents, played_numpy_actions = [], []
        real_make_agent = train.make_agent

        def make_training_agent(env, cfg):
            agent = real_make_agent(env, cfg)
            agents.append(agent)
            return agent

        def make_play_agent(env, cfg):
            agent = real_make_agent(env, cfg)
            original_sample = agent.sample_actions

            def record_sample(step, transition, training):
                self.assertFalse(training)
                values = original_sample(step, transition, training)
                self.assertIsInstance(values, np.ndarray)
                played_numpy_actions.append(values.copy())
                return values

            agent.sample_actions = record_sample
            agents.append(agent)
            return agent

        with tempfile.TemporaryDirectory(prefix="flash_sac_entrypoints_", dir=REPO / "test") as temporary:
            fixture_root = Path(temporary)
            output = io.StringIO()
            with patch.dict(sys.modules, mocked_isaac_modules()), patch.object(train, "REPO_ROOT", fixture_root), \
                    patch.object(play, "REPO_ROOT", fixture_root), \
                    patch.object(train, "make_agent", side_effect=make_training_agent), \
                    patch.object(play, "make_agent", side_effect=make_play_agent), contextlib.redirect_stdout(output):
                common = [
                    "--device", "cpu", "--buffer_device", "cpu", "--buffer_size", "64",
                    "--batch_size", "4", "--n_step", "1", "--updates_per_step", "1",
                    "--save_every", "8", "--log_every", "1", "--logger", "console",
                ]
                with patch.object(sys, "argv", ["train.py", *common, "--num_envs", "4", "--steps", "8", "--min_buffer", "8"]):
                    train.main()
                checkpoints = list(fixture_root.glob("lab/ddt_lab/logs/flash_sac/*/model_8"))
                self.assertEqual(len(checkpoints), 1)
                original_path = checkpoints[0]
                _, original_metadata = train.read_checkpoint(original_path, train.DEFAULT_TASK)
                original_updates = agents[0]._update_step
                self.assertGreater(original_updates, 0)
                self.assertEqual(agents[0].reward_normalizer.G_r.shape, (4,))

                with patch.object(sys, "argv", [
                    "train.py", *common, "--num_envs", "2", "--steps", "10", "--min_buffer", "4",
                    "--resume", str(original_path),
                ]):
                    train.main()
                resumed_paths = list(fixture_root.glob("lab/ddt_lab/logs/flash_sac/*/model_10"))
                self.assertEqual(len(resumed_paths), 1)
                resumed_path = resumed_paths[0]
                _, resumed_metadata = train.read_checkpoint(resumed_path, train.DEFAULT_TASK)
                self.assertEqual(resumed_metadata["step"], 10)
                self.assertEqual(agents[1].reward_normalizer.G_r.shape, (2,))
                self.assertEqual(agents[1]._update_step, original_updates + 1)
                # Resumed update index 7 skips the actor's period-two update.
                self.assertEqual(original_metadata["actor_sha256"], resumed_metadata["actor_sha256"])
                self.assertNotEqual((original_path / "critic.pt").read_bytes(), (resumed_path / "critic.pt").read_bytes())
                with patch.object(sys, "argv", [
                    "play.py", "--checkpoint", str(resumed_path), "--num_envs", "2",
                    "--steps", "2", "--device", "cpu", "--headless",
                ]):
                    play.main()

            self.assertEqual([env.num_envs for env in FakeNativeEnv.instances], [4, 2, 2])
            self.assertEqual([env.steps for env in FakeNativeEnv.instances], [8, 2, 2])
            self.assertTrue(all(env.closed for env in FakeNativeEnv.instances))
            self.assertTrue(all(env.cfg.observations.estimator_target is None for env in FakeNativeEnv.instances))
            self.assertEqual(len(FakeApp.instances), 3)
            self.assertTrue(all(app.closed for app in FakeApp.instances))
            self.assertEqual(len(played_numpy_actions), 2)
            for actual, expected in zip(FakeNativeEnv.instances[2].actions, played_numpy_actions):
                normalized = torch.from_numpy(expected)
                negative = torch.tensor(resumed_metadata["action_gain_negative"])
                positive = torch.tensor(resumed_metadata["action_gain_positive"])
                torch.testing.assert_close(actual, normalized * torch.where(normalized >= 0, positive, negative))
            summaries = list(fixture_root.glob("docs/exp/*/*_summary.md"))
            self.assertEqual(len(summaries), 3)
            self.assertTrue(all("Evidence Status: PASS" in report.read_text() for report in summaries))
            metrics = [json.loads(line) for path in fixture_root.glob("docs/exp/*/*_metrics.jsonl")
                       for line in path.read_text().splitlines()]
            self.assertTrue(any(row["step"] == 10 and row["updates"] == 1 for row in metrics))
            self.assertTrue(any("actor/loss" in row and "critic/loss" in row for row in metrics))
            self.assertIn("[VALIDATION_SIM] PASS: steps=2", output.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
