"""DESKTOP_DRY_RUN: exercise command updates on CPU without starting Isaac Sim."""

import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

import torch


ROOT = Path(__file__).resolve().parents[1]
LOCOMOTION = ROOT / "lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion"


class UniformVelocityCommandStub:
    """Leave sampled targets unchanged; Isaac Lab's sampler is outside this test."""

    def _update_command(self):
        pass


def load_command_class():
    tree = ast.parse((LOCOMOTION / "mdp/commands.py").read_text())
    command = next(node for node in tree.body if isinstance(node, ast.ClassDef)
                   and node.name == "RampedVelocityCommand")
    module = ast.Module(body=[command], type_ignores=[])
    namespace = {
        "torch": torch,
        "UniformVelocityCommand": UniformVelocityCommandStub,
    }
    # Compile the actual class without importing Isaac Sim or starting a simulator.
    import __future__
    exec(compile(module, "commands.py", "exec", flags=__future__.annotations.compiler_flag), namespace)
    return namespace["RampedVelocityCommand"]


class RampedVelocityCommandTest(unittest.TestCase):
    def make_command(self, rate, settle=0.0):
        command_class = load_command_class()
        command = command_class.__new__(command_class)
        command.cfg = SimpleNamespace(ramp_rate=rate, initial_phase_time=settle)
        command._env = SimpleNamespace(step_dt=0.02)
        command._time_since_reset = torch.zeros(2)
        command.vel_command_b = torch.tensor([[1.5, 0.0, -3.0], [-1.5, 0.0, 3.0]])
        command._emitted_command_b = torch.zeros_like(command.vel_command_b)
        return command

    def test_zero_rate_applies_target_and_subsequent_changes_immediately(self):
        command = self.make_command(0.0)
        command._update_command()
        torch.testing.assert_close(command.command, command.vel_command_b)
        command.vel_command_b.neg_()
        command._update_command()
        torch.testing.assert_close(command.command, command.vel_command_b)
        command.vel_command_b.zero_()
        command._update_command()
        torch.testing.assert_close(command.command, torch.zeros(2, 3))

    def test_positive_rate_limits_each_axis_and_does_not_overshoot(self):
        command = self.make_command(0.5)
        command.vel_command_b[0, 1] = 0.005
        command._update_command()
        expected = torch.tensor([[0.01, 0.005, -0.01], [-0.01, 0.0, 0.01]])
        torch.testing.assert_close(command.command, expected)

    def test_zero_rate_respects_existing_settle_gate(self):
        command = self.make_command(0.0, settle=2.0)
        command._update_command()
        torch.testing.assert_close(command.command, torch.zeros(2, 3))

    def test_flat_config_disables_ramp_and_settle(self):
        tree = ast.parse((LOCOMOTION / "robots/tita/flat_env_cfg.py").read_text())
        cfg = next(node for node in tree.body if isinstance(node, ast.ClassDef)
                   and node.name == "CommandsCfg")
        velocity = next(node for node in cfg.body if isinstance(node, ast.AnnAssign)
                        and node.target.id == "base_velocity")
        values = {kw.arg: kw.value for kw in velocity.value.keywords}
        self.assertEqual(ast.literal_eval(values["ramp_rate"]), 0.0)
        self.assertEqual(ast.literal_eval(values["initial_phase_time"]), 0.0)


if __name__ == "__main__":
    unittest.main()
