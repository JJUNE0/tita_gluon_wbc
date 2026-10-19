"""DESKTOP_DRY_RUN: Normalized replay, native ranges and checkpoint compatibility."""

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import torch

from test_flash_sac_adapter import FakeManagerBasedRLEnv, adapter_module
from test_flash_sac_entrypoints import FakeNativeEnv, REPO, mocked_isaac_modules, play, train
from runtime import (
    LEGACY_ACTION_MAPPING, PIECEWISE_ACTION_MAPPING, action_mapping_kwargs,
    action_mapping_metadata, load_default_runner_cfg,
)


class FlashSACActionRangesTest(unittest.TestCase):
    def make_env(self, **kwargs):
        raw = adapter_module.make_flash_sac_env_class(FakeManagerBasedRLEnv)()
        env = adapter_module.TitaFlashSACEnv(raw, **kwargs)
        env.reset()
        return env, raw

    def test_signed_gains_preserve_zero_and_normalized_caller(self):
        cfg = load_default_runner_cfg()
        env, raw = self.make_env(action_gain_negative=cfg.action_gain_negative,
                                 action_gain_positive=cfg.action_gain_positive)
        normalized = torch.tensor([[-2.0] * 8, [0.0] * 8, [2.0] * 8])
        original = normalized.clone()
        env.step(normalized)
        torch.testing.assert_close(normalized, original)
        torch.testing.assert_close(raw.applied_action, torch.stack([
            -torch.tensor(cfg.action_gain_negative), torch.zeros(8), torch.tensor(cfg.action_gain_positive)
        ]))
        # Native action terms retain their original leg scales and offsets.
        indices = [0, 1, 2, 4, 5, 6]
        defaults = torch.tensor([0.1, 0.8, -1.5] * 2)
        targets = defaults + 0.25 * raw.applied_action[:, indices]
        torch.testing.assert_close(targets[0], torch.tensor([-0.7, 0.3, -2.2] * 2))
        torch.testing.assert_close(targets[1], defaults)
        torch.testing.assert_close(targets[2], torch.tensor([0.7, 1.3, -0.8] * 2))
        torch.testing.assert_close(5 * raw.applied_action[:, [3, 7]], torch.tensor([[-30., -30.], [0., 0.], [30., 30.]]))

    def test_adapter_defaults_retain_legacy_unit_ranges(self):
        env, raw = self.make_env()
        actions = torch.full((3, 8), 2.0)
        env.step(actions)
        torch.testing.assert_close(raw.applied_action, torch.ones(3, 8))
        self.assertEqual(env.action_gain_negative, (1.0,) * 8)

    def test_invalid_gains_are_rejected_before_physics(self):
        for values in ([1.] * 7, [0.] * 8, [-1.] * 8, [float('nan')] * 8, [float('inf')] * 8):
            with self.subTest(values=values), self.assertRaisesRegex(ValueError, "positive finite gains"):
                self.make_env(action_gain_positive=values)
            cfg = load_default_runner_cfg()
            cfg.action_gain_positive = values
            with self.assertRaisesRegex(ValueError, "positive finite gains"):
                cfg.validate()

    def test_metadata_roundtrip_and_legacy_restoration_ignore_new_defaults(self):
        cfg = load_default_runner_cfg()
        env, _ = self.make_env(action_gain_negative=cfg.action_gain_negative,
                               action_gain_positive=cfg.action_gain_positive)
        metadata = {"action_dim": 8, **action_mapping_metadata(env)}
        self.assertEqual(metadata['action_mapping'], PIECEWISE_ACTION_MAPPING)
        restored, _ = self.make_env(**action_mapping_kwargs(json.loads(json.dumps(metadata))))
        self.assertEqual(restored.action_gain_positive, env.action_gain_positive)
        self.assertEqual(restored.action_gain_negative, env.action_gain_negative)
        for legacy in ({'action_dim': 8}, {'action_dim': 8, 'action_mapping': LEGACY_ACTION_MAPPING}):
            self.assertEqual(action_mapping_kwargs(legacy), {
                'action_gain_negative': [1.] * 8, 'action_gain_positive': [1.] * 8
            })

    def test_ambiguous_or_incomplete_checkpoint_mapping_is_rejected(self):
        cases = [
            {'action_dim': 8, 'action_mapping': 'unknown'},
            {'action_dim': 8, 'action_mapping': PIECEWISE_ACTION_MAPPING},
            {'action_dim': 8, 'action_mapping': LEGACY_ACTION_MAPPING, 'action_gain_positive': [2.] * 8},
            {'action_dim': 8, 'action_mapping': PIECEWISE_ACTION_MAPPING,
             'action_gain_negative': [1.] * 8, 'action_gain_positive': [float('nan')] * 8},
        ]
        for metadata in cases:
            with self.subTest(metadata=metadata), self.assertRaises(ValueError):
                action_mapping_kwargs(metadata)

    def test_real_learner_replay_stays_normalized_and_legacy_play_resume_stay_unit(self):
        FakeNativeEnv.instances.clear()
        transitions = []
        real_make_agent = train.make_agent

        def record_agent(env, cfg):
            agent = real_make_agent(env, cfg)
            original = agent.process_transition

            def record(transition):
                transitions.append(transition['action'].clone())
                original(transition)

            agent.process_transition = record
            return agent

        with tempfile.TemporaryDirectory(dir=REPO / 'test', prefix='flash_sac_gain_') as temporary:
            fixture = Path(temporary)
            common = ['--device', 'cpu', '--buffer_device', 'cpu', '--num_envs', '4',
                      '--buffer_size', '64', '--min_buffer', '8', '--batch_size', '4',
                      '--n_step', '1', '--save_every', '8', '--log_every', '1', '--logger', 'console']
            with patch.dict(sys.modules, mocked_isaac_modules()), patch.object(train, 'REPO_ROOT', fixture), \
                    patch.object(play, 'REPO_ROOT', fixture), patch.object(train, 'make_agent', side_effect=record_agent), \
                    redirect_stdout(io.StringIO()):
                with patch.object(sys, 'argv', ['train.py', *common, '--steps', '8']):
                    train.main()
                path = next(fixture.glob('lab/ddt_lab/logs/flash_sac/*/model_8'))
                _, metadata = train.read_checkpoint(path)
                self.assertEqual(metadata['action_mapping'], PIECEWISE_ACTION_MAPPING)
                negative = torch.tensor(metadata['action_gain_negative'])
                positive = torch.tensor(metadata['action_gain_positive'])
                for normalized, applied in zip(transitions, FakeNativeEnv.instances[0].actions):
                    self.assertTrue((normalized.abs() <= 1).all())
                    torch.testing.assert_close(applied, normalized * torch.where(normalized >= 0, positive, negative))
                self.assertTrue(any((values.abs() > 1).any() for values in FakeNativeEnv.instances[0].actions))
                # Reproduce an old complete checkpoint's metadata. Its weights,
                # config and hashes are retained; playback must use unit gains.
                legacy = dict(metadata, action_mapping=LEGACY_ACTION_MAPPING)
                legacy.pop('action_gain_negative')
                legacy.pop('action_gain_positive')
                (path / 'ddt.json').write_text(json.dumps(legacy))
                played = []

                def record_play_agent(env, cfg):
                    agent = real_make_agent(env, cfg)
                    original = agent.sample_actions
                    def record(step, transition, training):
                        action = original(step, transition, training)
                        played.append(torch.as_tensor(action).clone())
                        return action
                    agent.sample_actions = record
                    return agent

                with patch.object(play, 'make_agent', side_effect=record_play_agent), patch.object(sys, 'argv', [
                    'play.py', '--checkpoint', str(path), '--num_envs', '4', '--steps', '2', '--device', 'cpu'
                ]):
                    play.main()
                for actual, normalized in zip(FakeNativeEnv.instances[1].actions, played):
                    torch.testing.assert_close(actual, normalized)
                with patch.object(sys, 'argv', ['train.py', *common, '--steps', '10', '--resume', str(path)]):
                    train.main()
                resumed_path = next(fixture.glob('lab/ddt_lab/logs/flash_sac/*/model_10'))
                _, resumed = train.read_checkpoint(resumed_path)
                self.assertEqual(resumed['action_gain_negative'], [1.] * 8)
                self.assertEqual(resumed['action_gain_positive'], [1.] * 8)
                self.assertTrue(all((action.abs() <= 1).all() for action in FakeNativeEnv.instances[2].actions))


if __name__ == '__main__':
    unittest.main(verbosity=2)
