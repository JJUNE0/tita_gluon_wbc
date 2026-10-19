"""DESKTOP_DRY_RUN: ONNX wrapper and existing MuJoCo interface regression checks."""

from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
import torch

from test_flash_sac_entrypoints import REPO, load_entrypoint
from runtime import DEFAULT_TASK, LEGACY_ACTION_MAPPING, PIECEWISE_ACTION_MAPPING
from flash_rl.agents.flashSAC.network import FlashSACActor

export = load_entrypoint('tested_flash_sac_export', 'export.py')
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import ActionAdapter
from sim2sim_ros2_jazzy.adapter import ObservationBuilder, ObsState
from sim2sim_ros2_jazzy.checkpoint import describe_checkpoint


class FlashSACExportTest(unittest.TestCase):
    def test_wrapper_matches_native_actor_for_both_signed_gain_branches(self):
        actor = FlashSACActor(2, 33, 128, 8).eval()
        negative = [3.2, 2., 2.8, 6.] * 2
        positive = [2.4, 2., 2.8, 6.] * 2
        policy = export.NativeActionPolicy(actor, {'action_gain_negative': negative, 'action_gain_positive': positive})
        observations = torch.randn(64, 33)
        with torch.no_grad():
            mean = actor.get_mean_and_std(observations, training=False)[0]
            expected = mean.tanh() * torch.where(mean >= 0, torch.tensor(positive), torch.tensor(negative))
            torch.testing.assert_close(policy(observations), expected, atol=1e-5, rtol=1e-4)
            actor.predictor.mean_w.w.weight.zero_()
            actor.predictor.mean_bias.copy_(torch.tensor([-100., -100., -100., -100., 100., 100., 100., 100.]))
            torch.testing.assert_close(policy(torch.zeros(1, 33)), torch.tensor([[-3.2, -2., -2.8, -6., 2.4, 2., 2.8, 6.]]))

    def test_generated_config_keeps_native_scales_and_last_action_feedback(self):
        _, cfg, _, _ = describe_checkpoint(REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_172127_928297/model_15000/actor.pt')
        action = np.array([-3.2, 2., -2.8, 6., 2.4, -2., 2.8, -6.], dtype=np.float32)
        defaults = np.array(cfg['robot']['default_joint_angles'], dtype=np.float32)
        targets = ActionAdapter(cfg).targets(action)
        np.testing.assert_allclose(targets[[3, 7]], [30., -30.])
        np.testing.assert_allclose(targets[[0, 1, 2]], [-.7, 1.3, -2.2], atol=1e-6)
        state = ObsState(defaults, np.zeros(8), np.array([1., 0., 0., 0.]), np.zeros(3), np.zeros(3), action)
        obs = ObservationBuilder(cfg).build(state)
        np.testing.assert_array_equal(obs[-8:], action)
        np.testing.assert_array_equal(obs[9:25], np.zeros(16))

    def test_compiled_prefix_and_old_checkpoint_unit_gains_are_restored(self):
        actor = FlashSACActor(2, 33, 128, 8).eval()
        with tempfile.TemporaryDirectory(dir=REPO / 'test', prefix='flash_sac_export_') as temporary:
            path = Path(temporary)
            torch.save({'network_state_dict': {'_orig_mod.' + key: value for key, value in actor.state_dict().items()}}, path / 'actor.pt')
            metadata = {'task': DEFAULT_TASK, 'actor_obs_dim': 33, 'action_dim': 8,
                        'agent': {'actor_num_blocks': 2, 'actor_hidden_dim': 128},
                        'action_mapping': LEGACY_ACTION_MAPPING}
            policy = export.load_policy(path, metadata)
            obs = torch.randn(32, 33)
            with torch.no_grad():
                torch.testing.assert_close(policy(obs), actor.get_mean_and_std(obs, False)[0].tanh(), atol=1e-5, rtol=1e-4)
            metadata['action_mapping'] = PIECEWISE_ACTION_MAPPING
            with self.assertRaisesRegex(ValueError, 'action_gain_negative'):
                export.load_policy(path, metadata)


if __name__ == '__main__':
    unittest.main(verbosity=2)
