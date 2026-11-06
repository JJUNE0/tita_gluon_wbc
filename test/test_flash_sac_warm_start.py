"""DESKTOP_DRY_RUN: real CPU learner transfer into a fresh task configuration."""

from contextlib import redirect_stdout, redirect_stderr
import io
import json
from pathlib import Path
import pickle
import tempfile
import unittest
from unittest.mock import patch

import test_flash_sac_entrypoints as fixture
import torch
import torch._dynamo  # Initialize registrations before fake-module contexts.

train = fixture.train


class FlashSACWarmStartTest(unittest.TestCase):
    def test_warm_start_uses_new_environment_and_resets_state_then_can_resume(self):
        fixture.FakeNativeEnv.instances.clear()
        fixture.FakeApp.instances.clear()
        agents, loads, sampled_steps = [], [], []
        real_make_agent = train.make_agent

        def make_agent(env, cfg):
            agent = real_make_agent(env, cfg)
            index = len(agents)
            agents.append(agent)
            original_load, original_sample = agent.load, agent.sample_actions

            def load(path):
                original_load(path)
                loads.append({
                    "index": index, "update_step": agent._update_step,
                    "actor": {k: v.clone() for k, v in agent._actor.network.state_dict().items()},
                    "optimizer_empty": not agent._actor.optimizer.state_dict()["state"],
                    "normalizer_zero": bool((agent.reward_normalizer.G_r == 0).all()),
                })

            def sample(step, transition, training):
                sampled_steps.append((index, step))
                return original_sample(step, transition, training)

            agent.load, agent.sample_actions = load, sample
            return agent

        modules = fixture.mocked_isaac_modules()
        original_parse = modules["isaaclab_tasks.utils"].parse_env_cfg
        stage = ["standing"]

        def parse(*args, **kwargs):
            cfg = original_parse(*args, **kwargs)
            cfg.stage = stage[0]
            return cfg

        modules["isaaclab_tasks.utils"].parse_env_cfg = parse
        common = ["train.py", "--device", "cpu", "--num_envs", "4", "--steps", "4",
                  "--buffer_size", "64", "--min_buffer", "8", "--batch_size", "4", "--n_step", "1",
                  "--updates_per_step", "1", "--save_every", "4", "--log_every", "1", "--logger", "console"]
        with tempfile.TemporaryDirectory(prefix="flash_sac_warm_start_", dir=fixture.REPO / "test") as directory:
            root = Path(directory)
            with patch.dict(fixture.sys.modules, modules), patch.object(train, "REPO_ROOT", root), \
                    patch.object(train, "make_agent", side_effect=make_agent), redirect_stdout(io.StringIO()):
                with patch.object(fixture.sys, "argv", common):
                    train.main()
                source = next(root.glob("isaac_lab/ddt_lab/logs/flash_sac/*/model_4"))
                metadata = json.loads((source / "ddt.json").read_text())
                metadata["task"] = "standing-source-task"  # Cross-task initialization is intentional.
                (source / "ddt.json").write_text(json.dumps(metadata))
                actor_before = {k: v.clone() for k, v in agents[0]._actor.network.state_dict().items()}
                stage[0] = "xy"
                with patch.object(fixture.sys, "argv", [*common, "--warm_start", str(source)]):
                    train.main()
                initialized = loads[0]
                self.assertEqual(initialized["update_step"], 0)
                self.assertTrue(initialized["optimizer_empty"])
                self.assertTrue(initialized["normalizer_zero"])
                for name, expected in actor_before.items():
                    torch.testing.assert_close(initialized["actor"][name], expected)
                self.assertIn((1, 1), sampled_steps)  # Use the loaded policy during replay warmup.
                self.assertGreater(agents[1]._update_step, 0)
                self.assertEqual(fixture.FakeNativeEnv.instances[1].cfg.stage, "xy")
                warm = next(p for p in root.glob("isaac_lab/ddt_lab/logs/flash_sac/*/model_4") if p != source)
                with (warm / "env.pkl").open("rb") as stream:
                    self.assertEqual(pickle.load(stream).stage, "xy")
                provenance = json.loads((warm.parent / "warm_start.json").read_text())
                self.assertEqual(provenance["source_actor_sha256"], metadata["actor_sha256"])
                self.assertEqual(provenance["source_task"], "standing-source-task")
                warm_updates = agents[1]._update_step
                with patch.object(fixture.sys, "argv", [*common, "--resume", str(warm), "--steps", "6"]):
                    train.main()
                self.assertEqual(loads[1]["update_step"], warm_updates)
                self.assertFalse(loads[1]["optimizer_empty"])
                # Replay refills: only the second new vector step reaches 8 transitions.
                self.assertEqual(agents[2]._update_step, warm_updates + 1)
            self.assertTrue(all(e.closed for e in fixture.FakeNativeEnv.instances))
            self.assertTrue(all(a.closed for a in fixture.FakeApp.instances))

    def test_resume_and_warm_start_are_mutually_exclusive(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            train.build_parser().parse_args(["--resume", "a", "--warm_start", "b"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
