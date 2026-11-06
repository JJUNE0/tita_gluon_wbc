"""VALIDATION_SIM: saved pose contract, observation units and CLI forwarding."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'sim2sim/sim2sim_ros2_jazzy')]
from sim2sim_ros2_jazzy import checkpoint, cli
from sim2sim_ros2_jazzy.adapter import NATIVE_JOINTS, ObservationBuilder, ObsState

MODEL = ROOT / 'mj_lab/logs/flash_sac/tita_mjlab_202755_365015/model_15000'


class PosePlaybackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (MODEL / 'env.yaml').is_file():
            raise unittest.SkipTest('Pose playback tests require the local training checkpoint')
        cls.saved = checkpoint.read_yaml(MODEL / 'env.yaml')
        cls.cfg = checkpoint.describe_checkpoint(MODEL)[1]

    def state(self, pose=None):
        return ObsState(np.asarray(self.cfg['robot']['default_joint_angles']), np.zeros(8),
                        np.array([1., 0., 0., 0.]), np.zeros(3), np.zeros(3), np.zeros(8),
                        np.zeros(3), pose_command=pose)

    def test_saved_layout_and_units_are_pose_not_support(self):
        layout = self.cfg['policy_interface']['observations']
        self.assertEqual(layout[-1]['kind'], 'pose_commands')
        self.assertEqual(layout[-1]['scale'], [1., 1., 1.])
        self.assertEqual(self.cfg['policy']['obs_dim'], 38)
        self.assertNotIn('support_command', self.cfg)
        self.assertEqual(self.cfg['pose_command']['height_range'], [.27, .42])
        np.testing.assert_allclose(np.degrees(self.cfg['pose_command']['roll_range']), [-30., 30.])

    def test_absolute_height_and_signed_radians_reach_actor_without_mutation(self):
        builder = ObservationBuilder(self.cfg)
        np.testing.assert_allclose(builder.build(self.state())[-3:], [0., 0., .335], atol=1e-7)
        pose = np.array([np.radians(30.), np.radians(-15.), .42], dtype=np.float32)
        original = pose.copy()
        for _ in range(4):
            np.testing.assert_array_equal(builder.build(self.state(pose))[-3:], original)
        np.testing.assert_array_equal(pose, original)

    def test_invalid_observed_pose_rejected(self):
        for pose in ([0., 0.], [0., 0., np.nan], [1., 0., .335], [0., 0., .1]):
            with self.subTest(pose=pose), self.assertRaisesRegex(ValueError, 'Pose command'):
                ObservationBuilder(self.cfg).build(self.state(np.array(pose)))

    def test_saved_pose_validation_and_cache_fingerprint(self):
        for key, value in (('order', ['pitch', 'roll', 'height']), ('units', ['deg', 'deg', 'm']),
                           ('height_range', [-.1, .42]), ('nominal_height', .5),
                           ('roll_range', [-2., 2.]), ('ramp_rates', [.15, 0., .02]),
                           ('pitch_range', [False, .1]), ('ramp_rates', [.15, float('inf'), .02])):
            saved = deepcopy(self.saved)
            saved['commands']['base_pose'][key] = value
            layout = checkpoint.observation_layout(saved['observations']['policy'], {}, NATIVE_JOINTS)
            with self.subTest(key=key, value=value), self.assertRaisesRegex(ValueError, 'pose|roll/pitch/height'):
                checkpoint.simulation_config(saved, saved['scene']['robot']['init_state'], layout)
        changed = deepcopy(self.cfg)
        changed['pose_command']['ramp_rates'][0] = .2
        self.assertNotEqual(checkpoint.fingerprint(changed), checkpoint.fingerprint(self.cfg))

    def test_same_width_support_policy_remains_one_hot(self):
        model = ROOT / 'mj_lab/logs/flash_sac/tita_mjlab_194029_719452/model_15000'
        cfg = checkpoint.describe_checkpoint(model)[1]
        self.assertEqual(cfg['policy']['obs_dim'], 38)
        for mode in (0, 1, 2):
            state = self.state()
            state.support_mode = mode
            np.testing.assert_array_equal(ObservationBuilder(cfg).build(state)[-3:], np.eye(3)[mode])

    def test_cli_forwards_pose_for_interactive_and_headless_runs(self):
        for headless in (False, True):
            args = ['--ckpt', str(MODEL), '--pose', '10', '-5', '.35']
            if headless:
                args += ['--headless', '--steps', '5']
            with self.subTest(headless=headless), patch.object(checkpoint, 'prepared_config', return_value=MODEL/'sim2sim/actor/config.json'), \
                    patch.object(cli.sys.stdin, 'isatty', return_value=True), patch.object(cli.os, 'execvpe') as execute:
                cli.main(args)
                argv = execute.call_args.args[1]
                i = argv.index('--pose')
                self.assertEqual(argv[i+1:i+4], ['10.0', '-5.0', '0.35'])

    def test_cli_rejects_nonfinite_pose_before_export(self):
        with self.assertRaises(SystemExit) as error:
            cli.main(['--ckpt', str(MODEL), '--pose', 'nan', '0', '.335'])
        self.assertEqual(error.exception.code, 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
