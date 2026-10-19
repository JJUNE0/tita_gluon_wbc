"""DESKTOP_DRY_RUN: saved interface fidelity and checkpoint cache invalidation."""

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import ActionAdapter, ObservationBuilder, ObsState, ISAAC_JOINTS, NATIVE_JOINTS
from sim2sim_ros2_jazzy.checkpoint import describe_checkpoint, read_yaml, prepared_config, sha256, fingerprint, export_directory
from sim2sim_ros2_jazzy.cli import main
import contextlib
import io

FLASH = REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_172127_928297/model_15000/actor.pt'
PPO = REPO / 'docs/exp/2026-10-14/tita_ppo33_flash_comparison_151238/model_1999.pt'


class AdapterTest(unittest.TestCase):
    def test_saved_layout_order_scale_and_native_feedback(self):
        _, cfg, _, _ = describe_checkpoint(FLASH)
        state = ObsState(np.array(cfg['robot']['default_joint_angles']) + np.arange(8) * .01,
                         np.arange(8), np.array([1., 0., 0., 0.]), np.array([4., 8., 12.]),
                         np.array([.2, 0., -.3]), np.arange(8) - 4.)
        obs = ObservationBuilder(cfg).build(state)
        np.testing.assert_allclose(obs[:3], [1., 2., 3.])
        np.testing.assert_allclose(obs[9:17], [0., .04, .01, .05, .02, .06, 0., 0.], atol=1e-6)
        np.testing.assert_allclose(obs[17:25], np.array([0., 4., 1., 5., 2., 6., 3., 7.]) * .05)
        np.testing.assert_array_equal(obs[-8:], state.last_action)

    def test_observation_clip_precedes_scale(self):
        _, cfg, _, _ = describe_checkpoint(FLASH)
        cfg['policy']['obs_dim'] = 3
        cfg['policy_interface']['observations'] = [{'kind': 'ang_vel', 'clip': [-1., 1.], 'scale': [2., 3., 4.]}]
        state = ObsState(np.zeros(8), np.zeros(8), np.array([1., 0., 0., 0.]), np.array([10., -10., .5]), np.zeros(3), np.zeros(8))
        np.testing.assert_array_equal(ObservationBuilder(cfg).build(state), [2., -3., 2.])

    def test_action_order_processed_clip_and_effort_limits(self):
        _, cfg, _, _ = describe_checkpoint(FLASH)
        cfg['policy_interface']['actions'] = list(reversed(cfg['policy_interface']['actions']))
        cfg['policy_interface']['actions'][7]['clip'] = [-.2, .2]
        action = np.array([-6., 2.8, -2., 2.4, 6., -2.8, 2., -3.2], dtype=np.float32)
        adapter = ActionAdapter(cfg)
        targets = adapter.targets(action)
        torque = adapter.compute(action, np.zeros(8), np.zeros(8))
        np.testing.assert_allclose(targets[[3, 7]], [30., -30.])
        self.assertAlmostEqual(targets[0], -.2)
        self.assertTrue((np.abs(torque) <= cfg['robot']['torque_limit']).all())

    def test_invalid_action_and_observation_are_rejected(self):
        _, cfg, _, _ = describe_checkpoint(FLASH)
        with self.assertRaisesRegex(ValueError, 'policy action'):
            ActionAdapter(cfg).compute(np.full(8, np.nan), np.zeros(8), np.zeros(8))
        state = ObsState(np.zeros(8), np.zeros(8), np.zeros(4), np.full(3, np.nan), np.zeros(3), np.zeros(8))
        with self.assertRaisesRegex(ValueError, 'non-finite'):
            ObservationBuilder(cfg).build(state)

    def test_flash_and_ppo_interface_is_read_from_saved_environment(self):
        for ckpt in (FLASH, PPO):
            path, cfg, _, _ = describe_checkpoint(ckpt)
            self.assertEqual(cfg['policy']['obs_dim'], 33)
            self.assertEqual([x['joint'] for x in cfg['policy_interface']['actions']], NATIVE_JOINTS)
            self.assertEqual(cfg['policy_interface']['checkpoint_sha256'], sha256(path))

    def test_yaml_python_tags_are_data_and_never_executed(self):
        with tempfile.TemporaryDirectory(dir=REPO / 'test') as temp:
            path = Path(temp) / 'data.yaml'
            path.write_text('payload: !!python/object/apply:os.system ["false"]\nscale: !!python/tuple [1, 2, 3]\n')
            self.assertEqual(read_yaml(path), {'payload': ['false'], 'scale': [1, 2, 3]})

    def test_missing_sidecars_and_unsupported_terms_fail_clearly(self):
        with tempfile.TemporaryDirectory(dir=REPO / 'test') as temp:
            path = Path(temp) / 'model.pt'
            path.write_bytes(b'not weights')
            with self.assertRaisesRegex(ValueError, 'env.yaml is required'):
                describe_checkpoint(path)

    def test_saved_resolved_joint_order_overrides_legacy_convention(self):
        with tempfile.TemporaryDirectory(dir=REPO / 'test') as temp:
            root = Path(temp)
            path = root / 'model.pt'
            path.write_bytes(PPO.read_bytes())
            for name in ('env.yaml', 'agent.json'):
                (root / name).write_bytes((PPO.parent / name).read_bytes())
            (root / 'policy_interface.json').write_text(json.dumps({'articulation_joint_names': NATIVE_JOINTS,
                'observations': [{'name': 'joint_pos', 'joints': list(reversed(NATIVE_JOINTS)), 'scale': 0.}]}))
            _, cfg, _, _ = describe_checkpoint(path)
            term = next(term for term in cfg['policy_interface']['observations'] if term['name'] == 'joint_pos')
            self.assertEqual(term['joints'], list(reversed(NATIVE_JOINTS)))
            self.assertEqual(term['scale'], 0.)

    def test_launcher_requires_an_explicit_checkpoint(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            main([])
        self.assertEqual(error.exception.code, 2)

    def test_training_capture_saves_resolved_joint_names_and_scales(self):
        spec = importlib.util.spec_from_file_location('capture_policy_interface', REPO / 'lab/ddt_lab/ddt_lab/policy_interface.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        observation = SimpleNamespace(scale=[1., 2., 3.], clip=(-1., 1.), params={'asset_cfg': SimpleNamespace(name='robot', joint_ids=[2, 0])})
        manager = SimpleNamespace(active_terms={'policy': ['joint_pos']}, _group_obs_term_cfgs={'policy': [observation]})
        actions = SimpleNamespace(active_terms=['left'], get_term=lambda _: SimpleNamespace(_joint_names=NATIVE_JOINTS[:4]))
        env = SimpleNamespace(scene={'robot': SimpleNamespace(joint_names=ISAAC_JOINTS)}, observation_manager=manager, action_manager=actions)
        env.unwrapped = env
        with tempfile.TemporaryDirectory(dir=REPO / 'test') as temp:
            data = module.save_policy_interface(env, Path(temp) / 'policy_interface.json')
            self.assertEqual(data['observations'][0]['joints'], [ISAAC_JOINTS[2], ISAAC_JOINTS[0]])
            self.assertEqual(data['actions'][0]['joints'], NATIVE_JOINTS[:4])

    def test_cache_rejects_modified_onnx_config_or_saved_environment(self):
        with tempfile.TemporaryDirectory(dir=REPO / 'test') as temp:
            root = Path(temp)
            path = root / 'model.pt'
            path.write_bytes(PPO.read_bytes())
            for name in ('env.yaml', 'agent.json'):
                (root / name).write_bytes((PPO.parent / name).read_bytes())
            _, cfg, _, _ = describe_checkpoint(path)
            output = export_directory(path)
            output.mkdir(parents=True)
            config = output / 'config.json'
            config.write_text(json.dumps(cfg))
            onnx = output / 'policy.onnx'
            onnx.write_bytes(b'validated export')
            manifest = {'fingerprint': fingerprint(cfg), 'onnx_sha256': sha256(onnx), 'config_sha256': sha256(config)}
            (output / 'manifest.json').write_text(json.dumps(manifest))
            self.assertEqual(prepared_config(path), config)
            onnx.write_bytes(b'changed graph')
            self.assertIsNone(prepared_config(path))
            onnx.write_bytes(b'validated export')
            config.write_text('changed config')
            self.assertIsNone(prepared_config(path))
            config.write_text(json.dumps(cfg))
            # Appending even a comment changes the saved config fingerprint.
            with (root / 'env.yaml').open('a') as stream:
                stream.write('\n# changed after export\n')
            self.assertIsNone(prepared_config(path))


if __name__ == '__main__':
    unittest.main(verbosity=2)
