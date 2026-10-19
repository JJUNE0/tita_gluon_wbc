"""DESKTOP_DRY_RUN: selected flat settings equal the original experiment chain.

Use Isaac Lab's real configclass, symbolic manager leaves, and a deterministic
asset-path marker. This checks every resolved value and manager term order;
it does not execute observation functions or validate physics.
"""

import ast
import hashlib
from pathlib import Path
from types import ModuleType
import sys
import unittest

from test_tita_my_flat_config_refactor import TITA, Symbols, load_configs, namespace, snapshot


def execute(path, values, name):
    module = ModuleType(name)
    sys.modules[name] = module
    module.__dict__.update(values)
    tree = ast.parse(path.read_text())
    tree.body = [node for node in tree.body if not isinstance(node, (ast.Import, ast.ImportFrom))
                 and not (isinstance(node, ast.FunctionDef) and node.name == "sphere_wheel_urdf")]
    exec(compile(tree, str(path), "exec"), module.__dict__)
    return module


def load_selected_configs():
    values = namespace()
    values.update(
        real2sim_actions=Symbols("real2sim_actions"),
        real2sim_events=Symbols("real2sim_events"),
        real2sim_observations=Symbols("real2sim_observations"),
        real2sim_rewards=Symbols("real2sim_rewards"),
        JointPositionActionCfg=values["mdp"].JointPositionActionCfg,
        sphere_wheel_urdf=lambda source: source + "#sphere_wheels",
    )
    baseline = load_configs(values=values)
    experiments = execute(TITA / "real2sim/env_cfg.py", baseline.__dict__, "_flat_experiments")
    selected = execute(TITA / "flat_env_cfg.py", values, "_selected_flat")
    return experiments, selected


class FlatPromotionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.experiments, cls.selected = load_selected_configs()

    def test_every_value_and_manager_order_matches_original_headw0_experiment(self):
        expected = self.experiments.MyTitaFlatPosKneeSphereHeadingObsW0EnvCfg()
        actual = self.selected.TitaFlatEnvCfg()
        self.assertEqual(snapshot(actual), snapshot(expected))

    def test_archived_base_is_byte_identical_to_task_start(self):
        self.assertEqual(
            hashlib.sha256((TITA / "real2sim/base_env_cfg.py").read_bytes()).hexdigest(),
            "144ebf809c1211a8ac3632b5e5575548dfc95b5dbf83320309b66c045b497cd9",
        )
        self.assertFalse((TITA / "my_flat_env_cfg.py").exists())

    def test_flat_has_no_experiment_or_rough_config_inheritance(self):
        self.assertEqual(self.selected.TitaFlatEnvCfg.__bases__, (self.selected.ManagerBasedRLEnvCfg,))

    def test_play_disables_knee_randomization_without_mutating_training(self):
        before = snapshot(self.selected.TitaFlatEnvCfg())
        play = self.selected.TitaFlatEnvCfg_PLAY()
        self.assertEqual(play.scene.num_envs, 50)
        self.assertFalse(play.observations.policy.enable_corruption)
        self.assertIsNone(play.events.knee_output_scale)
        self.assertIsNone(play.events.randomize_actuator_gains)
        self.assertEqual(snapshot(self.selected.TitaFlatEnvCfg()), before)

    def test_jump_retains_rough_baseline_and_history_interface(self):
        values = namespace()
        rough = execute(TITA / "rough_env_cfg.py", values, "_jump_rough")
        jump = execute(TITA / "jump_env_cfg.py", rough.__dict__, "_preserved_jump")
        cfg = jump.TitaJumpEnvCfg()
        self.assertEqual(jump.TitaJumpEnvCfg.__bases__, (rough.TitaRoughEnvCfg,))
        self.assertEqual(cfg.scene.terrain.terrain_type, "plane")
        self.assertIsNone(cfg.scene.terrain.terrain_generator)
        self.assertIsNone(cfg.scene.height_scanner)
        self.assertIsNone(cfg.observations.scanner)
        self.assertIsNone(cfg.curriculum.terrain_levels)
        self.assertEqual(cfg.observations.policy.history_length, 10)
        self.assertFalse(hasattr(cfg.observations.policy, "heading_error"))
        self.assertEqual(cfg.commands.base_velocity.ranges.ang_vel_z, (-1.0, 1.0))
        self.assertTrue(hasattr(cfg.observations.policy, "jump_cmd"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
