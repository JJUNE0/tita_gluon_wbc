"""DESKTOP_DRY_RUN: eager/compiled FlashSAC checkpoint interoperability on CPU."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True

import torch
from torch._dynamo.eval_frame import DisableContext, OptimizedModule


REPO = Path(__file__).resolve().parents[1]
NETWORK_PATH = REPO / "lab/ddt_lab/scripts/flash_sac/vendor/flash_rl/agents/utils/network.py"
SPEC = importlib.util.spec_from_file_location("flash_sac_checkpoint_network", NETWORK_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
Network = MODULE.Network


class FlashSACCompileCheckpointTest(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(7)
        self.observations = torch.randn(5, 3)

    @staticmethod
    def make_network(compiled=False):
        module = torch.nn.Sequential(torch.nn.Linear(3, 4), torch.nn.Tanh(), torch.nn.Linear(4, 2))
        optimizer = torch.optim.Adam(module.parameters(), lr=0.003)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.9)
        # This is torch.compile's actual module wrapper and state-dict namespace.
        # DisableContext runs forwards eagerly, avoiding CPU kernel compilation
        # and remaining effective if other tests set TORCHDYNAMO_DISABLE=1.
        if compiled:
            module = OptimizedModule(module, DisableContext())
        return Network(module, optimizer, scheduler)

    def train_network(self, network):
        for _ in range(2):
            network.optimizer.zero_grad()
            network(self.observations).square().mean().backward()
            network.optimizer.step()
            network.scheduler.step()
            network.update_step += 1

    def assert_nested_equal(self, expected, actual):
        if isinstance(expected, torch.Tensor):
            torch.testing.assert_close(expected, actual, rtol=0, atol=0)
        elif isinstance(expected, dict):
            self.assertEqual(expected.keys(), actual.keys())
            for key in expected:
                self.assert_nested_equal(expected[key], actual[key])
        elif isinstance(expected, (tuple, list)):
            self.assertEqual(len(expected), len(actual))
            for left, right in zip(expected, actual):
                self.assert_nested_equal(left, right)
        else:
            self.assertEqual(expected, actual)

    def assert_restored(self, source, restored):
        torch.testing.assert_close(
            torch.tanh(source(self.observations)), torch.tanh(restored(self.observations)), rtol=0, atol=0
        )
        self.assert_nested_equal(source.optimizer.state_dict(), restored.optimizer.state_dict())
        self.assert_nested_equal(source.scheduler.state_dict(), restored.scheduler.state_dict())
        self.assertEqual(source.update_step, restored.update_step)

    def test_compiled_save_loads_into_eager_with_optimizer_and_actions(self):
        source = self.make_network(compiled=True)
        self.assertTrue(all(key.startswith("_orig_mod.") for key in source.network.state_dict()))
        self.train_network(source)
        with tempfile.TemporaryDirectory(prefix="flash_sac_compile_", dir=REPO / "test") as temporary:
            path = str(Path(temporary) / "actor.pt")
            source.save(path)
            checkpoint = torch.load(path, map_location="cpu")
            self.assertTrue(all(not key.startswith("_orig_mod.") for key in checkpoint["network_state_dict"]))
            restored = self.make_network()
            restored.load(path)
            self.assert_restored(source, restored)

    def test_eager_save_loads_into_compiled_with_optimizer_and_actions(self):
        source = self.make_network()
        self.train_network(source)
        with tempfile.TemporaryDirectory(prefix="flash_sac_compile_", dir=REPO / "test") as temporary:
            path = str(Path(temporary) / "actor.pt")
            source.save(path)
            restored = self.make_network(compiled=True)
            restored.load(path)
            self.assert_restored(source, restored)

    def test_legacy_compiled_names_load_and_param_key_keeps_other_weights(self):
        source = self.make_network(compiled=True)
        self.train_network(source)
        with tempfile.TemporaryDirectory(prefix="flash_sac_compile_", dir=REPO / "test") as temporary:
            path = str(Path(temporary) / "actor.pt")
            source.save(path)
            checkpoint = torch.load(path, map_location="cpu")
            checkpoint["network_state_dict"] = source.network.state_dict()
            torch.save(checkpoint, path)
            restored = self.make_network()
            restored.load(path)
            self.assert_restored(source, restored)
            partial = self.make_network(compiled=True)
            before = {key: value.clone() for key, value in partial._checkpoint_network().state_dict().items()}
            partial.load(path, param_key="0.weight", load_optimizer=False)
            original = source._checkpoint_network().state_dict()
            for key, value in partial._checkpoint_network().state_dict().items():
                torch.testing.assert_close(value, original[key] if key == "0.weight" else before[key], rtol=0, atol=0)
            self.assertEqual(partial.update_step, 0)
            self.assertEqual(partial.optimizer.state_dict()["state"], {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
