"""DESKTOP_DRY_RUN: TITA-owned FlashSAC defaults, CLI overrides and estimator routing."""

import ast
from copy import deepcopy
from dataclasses import asdict
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

os.environ["TORCHDYNAMO_DISABLE"] = "1"
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "lab/ddt_lab/scripts/flash_sac"
sys.path.insert(0, str(SCRIPTS))

from runtime import create_agent_config, load_default_runner_cfg, setup_imports
from train import build_parser

setup_imports(False)


class FlashSACConfigTest(unittest.TestCase):
    def test_local_scripts_namespace_wins_over_foreign_regular_package(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "test", prefix="flash_sac_import_") as directory:
            foreign = Path(directory) / "scripts"
            foreign.mkdir()
            (foreign / "__init__.py").write_text('ORIGIN = "foreign"\n')
            with patch.dict(sys.modules), patch.object(sys, "path", [directory, *sys.path]):
                sys.modules.pop("scripts", None)
                self.assertEqual(importlib.util.find_spec("scripts").origin, str(foreign / "__init__.py"))
                setup_imports(False)
                local = ROOT / "lab/scripts"
                self.assertEqual(list(sys.modules["scripts"].__path__), [str(local)])
                co_rl = importlib.util.find_spec("scripts.co_rl")
                self.assertEqual(list(co_rl.submodule_search_locations), [str(local / "co_rl")])

    def test_extracting_defaults_preserves_original_cli_and_all_learner_fields(self):
        original = json.loads((ROOT / "test/fixtures/tita_flash_sac_before_cfg_extraction.json").read_text())
        # The selected flat task replaces the historical My task as CLI default.
        original["cli_defaults"]["task"] = "DDT-Velocity-Flat-Tita-v0"
        args = build_parser().parse_args([])
        self.assertEqual({name: getattr(args, name) for name in original["cli_defaults"]}, original["cli_defaults"])
        self.assertEqual(asdict(create_agent_config(args)), original["agent_defaults"])

    def test_config_edits_reach_parser_and_learner_while_cli_takes_priority(self):
        runner = load_default_runner_cfg()
        runner.batch_size = 64
        runner.steps = 1000
        runner.updates_per_step = 0.5
        runner.agent.actor_hidden_dim = 64
        runner.agent.critic_hidden_dim = 128
        runner.agent.learning_rate_peak = 1e-4
        runner.agent.learning_rate_warmup_rate = 0.2
        runner.agent.learning_rate_decay_rate = 0.75
        runner.amp = True
        args = build_parser(runner).parse_args(["--device", "cpu", "--batch_size", "8", "--steps", "100"])
        agent = create_agent_config(args, runner)
        self.assertEqual(args.batch_size, 8)
        self.assertEqual(runner.batch_size, 64)
        self.assertEqual(agent.actor_hidden_dim, 64)
        self.assertEqual(agent.critic_hidden_dim, 128)
        self.assertEqual(agent.learning_rate_peak, 1e-4)
        self.assertEqual(agent.learning_rate_warmup_step, 10)
        self.assertEqual(agent.learning_rate_decay_step, 37)
        self.assertEqual(agent.sample_batch_size, 8)
        self.assertFalse(agent.use_amp)

    def test_cli_can_disable_compile_and_amp_enabled_by_config(self):
        runner = load_default_runner_cfg()
        runner.compile = runner.amp = True
        args = build_parser(runner).parse_args(["--no-compile", "--no-amp"])
        agent = create_agent_config(args, runner)
        self.assertFalse(agent.use_compile)
        self.assertFalse(agent.use_amp)

    def test_flash_run_disables_only_target_and_preserves_shared_ppo_config(self):
        from test_tita_my_flat_config_refactor import load_configs, normalize
        module = load_configs()
        shared = module.MyTitaFlatEnvCfg()
        flash = deepcopy(shared)
        expected = normalize(shared)
        expected["observations"]["estimator_target"] = None
        load_default_runner_cfg().apply_env_cfg(flash)
        self.assertEqual(normalize(flash), expected)
        self.assertIsNotNone(shared.observations.estimator_target)
        self.assertIsNotNone(module.MyTitaFlatEnvCfg().observations.estimator_target)

    def test_unimplemented_estimator_fails_before_changing_environment(self):
        runner = load_default_runner_cfg()
        runner.use_velocity_estimator = True
        target = object()
        env = SimpleNamespace(observations=SimpleNamespace(estimator_target=target))
        with self.assertRaisesRegex(ValueError, "estimator is not implemented"):
            runner.apply_env_cfg(env)
        self.assertIs(env.observations.estimator_target, target)

    def test_my_train_and_play_registry_points_to_the_new_agent_config(self):
        # Execute only registration statements with inert environment config
        # symbols; native Isaac modules are never imported or launched.
        registrations = {}
        def register(id, **kwargs):
            registrations[id] = kwargs["kwargs"]
        agents = SimpleNamespace(__name__="ddt_lab.tasks.manager_based.locomotion.robots.tita.agents")
        values = {"gym": SimpleNamespace(register=register), "agents": agents}
        for name, classes in {
            "flat_env_cfg": ("TitaFlatEnvCfg", "TitaFlatEnvCfg_PLAY"),
            "base_env_cfg": ("MyTitaFlatEnvCfg", "MyTitaFlatEnvCfg_PLAY"),
            "jump_env_cfg": ("TitaJumpEnvCfg", "TitaJumpEnvCfg_PLAY"),
            "rough_env_cfg": ("TitaRoughEnvCfg", "TitaRoughEnvCfg_PLAY"),
        }.items():
            values[name] = SimpleNamespace(**{key: object() for key in classes})
        path = ROOT / "lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/__init__.py"
        tree = ast.parse(path.read_text())
        tree.body = [node for node in tree.body if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)]
        exec(compile(tree, str(path), "exec"), values)
        for task in ("DDT-Velocity-Flat-Tita-v0", "DDT-Velocity-Flat-Tita-Play-v0",
                     "DDT-Velocity-Flat-Tita-My-v0", "DDT-Velocity-Flat-Tita-My-Play-v0"):
            self.assertEqual(registrations[task]["flash_sac_cfg_entry_point"],
                             f"{agents.__name__}.flash_sac_cfg:TitaFlatFlashSACRunnerCfg")
            self.assertIn("rsl_rl_cfg_entry_point", registrations[task])


if __name__ == "__main__":
    unittest.main(verbosity=2)
