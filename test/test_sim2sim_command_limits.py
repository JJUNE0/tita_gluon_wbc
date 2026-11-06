"""DESKTOP_DRY_RUN: YAML caps, trained-axis restrictions and export cache refresh."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_sim2sim_walk import REPO, saved_env
from sim2sim_ros2_jazzy import checkpoint


class CommandLimitsTest(unittest.TestCase):
    def build(self, caps, ranges=None):
        env = saved_env()
        env['commands']['base_velocity']['ranges'] = ranges or {
            'lin_vel_x': [-1.5, 1.5], 'lin_vel_y': [-.5, .5], 'ang_vel_z': [-3., 3.]}
        before = deepcopy(env)
        base = checkpoint.read_yaml(checkpoint.PACKAGE / 'config/tita.yaml')
        base['command'] = caps
        with patch.object(checkpoint, 'read_yaml', return_value=base):
            cfg = checkpoint.simulation_config(env, env['scene']['robot']['init_state'], [])
        self.assertEqual(env, before, 'Playback caps must not mutate the saved training config')
        return cfg

    def test_yaml_limits_apply_to_all_three_axes(self):
        cfg = self.build(dict(max_lin_x=.2, max_lin_y=.1, max_ang_z=.3))
        self.assertEqual(cfg['sim_command_ranges'], {
            'lin_vel_x': [-.2, .2], 'lin_vel_y': [-.1, .1], 'ang_vel_z': [-.3, .3]})

    def test_larger_caps_preserve_asymmetric_trained_ranges_and_disabled_axes(self):
        ranges = {'lin_vel_x': [-.15, .12], 'lin_vel_y': [0., 0.], 'ang_vel_z': [-.25, .2]}
        cfg = self.build(dict(max_lin_x=10., max_lin_y=10., max_ang_z=10.), ranges)
        self.assertEqual(cfg['sim_command_ranges'], ranges)

    def test_zero_caps_disable_commands(self):
        cfg = self.build(dict(max_lin_x=0., max_lin_y=0., max_ang_z=0.))
        self.assertTrue(all(bounds == [0., 0.] for bounds in cfg['sim_command_ranges'].values()))

    def test_invalid_yaml_caps_fail_before_export(self):
        for key in ('max_lin_x', 'max_lin_y', 'max_ang_z'):
            for value in (-.1, float('nan'), float('inf'), True, None, '0.2'):
                caps = dict(max_lin_x=.2, max_lin_y=.2, max_ang_z=.3)
                caps[key] = value
                with self.subTest(key=key, value=value), self.assertRaisesRegex(ValueError, f'tita.yaml command limit: {key}'):
                    self.build(caps)

    def test_changed_yaml_caps_invalidate_an_existing_export(self):
        cfg = self.build(dict(max_lin_x=.2, max_lin_y=.2, max_ang_z=.3))
        changed = self.build(dict(max_lin_x=.1, max_lin_y=.2, max_ang_z=.3))
        with tempfile.TemporaryDirectory(dir=REPO / 'test', prefix='command_limits_cache_') as directory:
            actor = Path(directory) / 'actor.pt'
            output = checkpoint.export_directory(actor)
            output.mkdir(parents=True)
            config_path = output / 'config.json'
            config_path.write_text(json.dumps(cfg))
            (output / 'policy.onnx').write_bytes(b'cache-fixture-not-a-policy')
            (output / 'manifest.json').write_text(json.dumps(dict(
                fingerprint=checkpoint.fingerprint(cfg),
                onnx_sha256=checkpoint.sha256(output / 'policy.onnx'),
                config_sha256=checkpoint.sha256(config_path))))
            with patch.object(checkpoint, 'describe_checkpoint', return_value=(actor, cfg, {}, {})):
                self.assertEqual(checkpoint.prepared_config(actor), config_path)
            with patch.object(checkpoint, 'describe_checkpoint', return_value=(actor, changed, {}, {})):
                self.assertIsNone(checkpoint.prepared_config(actor))


if __name__ == '__main__':
    unittest.main(verbosity=2)
