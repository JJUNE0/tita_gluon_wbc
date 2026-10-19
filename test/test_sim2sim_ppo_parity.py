"""DESKTOP_DRY_RUN: portable PPO inference must match native RSL-RL inference."""

import importlib.util
from pathlib import Path
import sys
import unittest

import torch
from tensordict import TensorDict
from rsl_rl.modules import ActorCritic

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.checkpoint import describe_checkpoint, load_ppo_policy


class NativePPOParityTest(unittest.TestCase):
    def verify(self, checkpoint, estimator):
        path, _, agent, _ = describe_checkpoint(checkpoint)
        cls = ActorCritic
        if estimator:
            spec = importlib.util.spec_from_file_location('native_estimator', REPO / 'lab/ddt_lab/ddt_lab/algorithms/estimator/actor_critic_with_estimator.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            cls = module.ActorCriticWithEstimator
        proprio = torch.randn(512, 33, generator=torch.Generator().manual_seed(123)) * 4
        obs = TensorDict({'policy': proprio, 'critic': torch.zeros(512, 36), 'estimator_target': torch.zeros(512, 3)}, batch_size=[512])
        cfg = dict(agent['policy'])
        cfg.pop('class_name')
        native = cls(obs, agent['obs_groups'], 8, **cfg).eval()
        native.load_state_dict(torch.load(path, map_location='cpu', weights_only=True)['model_state_dict'])
        portable = load_ppo_policy(path, agent)
        with torch.inference_mode():
            expected = native.act_inference(obs)
            if agent.get('clip_actions') is not None:
                expected = expected.clamp(-agent['clip_actions'], agent['clip_actions'])
            actual = portable(proprio)
        torch.testing.assert_close(actual, expected, atol=1e-6, rtol=1e-6)
        print(f'[DESKTOP_DRY_RUN] Native PPO parity PASS: {path.name}, estimator={estimator}, max_error={(actual-expected).abs().max().item()}')

    def test_plain_ppo_checkpoint(self):
        self.verify(REPO / 'docs/exp/2026-10-14/tita_ppo33_flash_comparison_151238/model_1999.pt', False)

    def test_estimator_ppo_checkpoint(self):
        self.verify(REPO / 'lab/ddt_lab/logs/rsl_rl/tita_flat_rslrl_estimator/2026-07-24_19-16-43/model_1800.pt', True)


if __name__ == '__main__':
    torch.set_num_threads(2)
    unittest.main(verbosity=2)
