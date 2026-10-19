"""DESKTOP_DRY_RUN: saved 33/34 interfaces, encoder hold semantics, C++ stream parity."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import ActionAdapter, LegActionFilter, ObservationBuilder, ObsState, NATIVE_JOINTS
from sim2sim_ros2_jazzy.checkpoint import describe_checkpoint, read_yaml, observation_layout, action_layout

RUN = REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_180212_290240'
NEW = RUN / 'model_75000'
OLD = REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_201940_278440/model_80000'
PPO = REPO / 'docs/exp/2026-10-14/tita_ppo33_flash_comparison_151238/model_1999.pt'


def load_launch():
    spec = importlib.util.spec_from_file_location('checkpoint_auto_tita_launch',
        REPO / 'sim2real/tita_ws/src/tita_controller/launch/tita.launch.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CheckpointPositionTests(unittest.TestCase):
    def test_saved_interfaces_select_dimension_and_filter(self):
        for checkpoint, size, mode in ((NEW, 34, 'ma2_legs'), (OLD, 33, 'none'), (PPO, 33, 'none')):
            _, cfg, _, _ = describe_checkpoint(checkpoint)
            self.assertEqual(cfg['policy']['obs_dim'], size)
            self.assertEqual(cfg['policy_interface']['leg_action_filter'], mode)
        _, cfg, _, _ = describe_checkpoint(NEW)
        self.assertEqual(cfg['robot']['joint_kp'][2], 92.)
        self.assertEqual(cfg['robot']['joint_kd'][2], 2.3)
        self.assertEqual(cfg['policy_interface']['observations'][-1]['params'],
            dict(radius=.0925, clip_m=.3, zero_thresholds=[.02, .02, .03]))

    def test_unknown_terms_invalid_params_and_partial_ma2_are_rejected(self):
        env = read_yaml(RUN / 'env.yaml')
        group = copy.deepcopy(env['observations']['policy'])
        group['wheel_position_error']['func'] = 'unknown.Position'
        with self.assertRaisesRegex(ValueError, 'Unsupported observation'):
            observation_layout(group, {}, NATIVE_JOINTS)
        for value in (-.1, float('nan')):
            group = copy.deepcopy(env['observations']['policy'])
            group['wheel_position_error']['params']['radius'] = value
            with self.assertRaisesRegex(ValueError, 'parameters'):
                observation_layout(group, {}, NATIVE_JOINTS)
        actions = copy.deepcopy(env['actions'])
        actions['joint_pos_0']['class_type'] = 'JointPositionAction'
        with self.assertRaisesRegex(ValueError, 'six leg'):
            action_layout(actions, {}, NATIVE_JOINTS, env['scene']['robot']['init_state'])
        with tempfile.TemporaryDirectory(dir=REPO / 'test') as directory:
            path = Path(directory) / 'actor.pt'
            path.write_bytes(b'weights alone')
            with self.assertRaisesRegex(ValueError, 'weights alone'):
                describe_checkpoint(path)

    def test_position_hold_formula_wrap_reset_and_thresholds(self):
        _, cfg, _, _ = describe_checkpoint(NEW)
        builder = ObservationBuilder(cfg)
        state = ObsState(np.zeros(8), np.zeros(8), np.array([1., 0., 0., 0.]), np.zeros(3),
            np.zeros(3, dtype=np.float32), np.arange(8, dtype=np.float32))
        self.assertEqual(builder.build(state)[-1], 0.)
        state.joint_pos[[3, 7]] += .1
        self.assertAlmostEqual(builder.build(state)[-1], 5 * .0925 * .1, places=6)
        state.joint_pos[[1, 5]] += .05
        self.assertAlmostEqual(builder.build(state)[-1], 5 * .0925 * .15, places=6)
        pitch = .07
        state.base_quat_wxyz = np.array([np.cos(pitch/2), 0., np.sin(pitch/2), 0.])
        self.assertAlmostEqual(builder.build(state)[-1], 5 * .0925 * .22, places=6)
        state.command[:] = [.02, .02, .03]
        self.assertGreater(builder.build(state)[-1], 0.)  # Inclusive band, including float32 boundaries.
        state.command[1] = .021
        self.assertEqual(builder.build(state)[-1], 0.)
        state.command[:] = 0.
        self.assertEqual(builder.build(state)[-1], 0.)
        builder.reset()
        state.joint_pos[[3, 7]] = np.pi - .01
        self.assertEqual(builder.build(state)[-1], 0.)
        state.joint_pos[[3, 7]] = -np.pi + .01
        self.assertAlmostEqual(builder.build(state)[-1], 5 * .0925 * .02, places=6)
        for _ in range(50):
            state.joint_pos[[3, 7]] += .1
            obs = builder.build(state)
        self.assertEqual(obs[-1], 1.5)
        np.testing.assert_array_equal(obs[25:33], state.last_action)
        builder.reset()
        self.assertEqual(builder.build(state)[-1], 0.)
        state.joint_pos[3] = np.nan
        with self.assertRaisesRegex(ValueError, 'non-finite'):
            builder.build(state)

    def test_cpp_python_full_observation_filter_and_pd_sequences(self):
        launch = load_launch()
        rng = np.random.default_rng(1842)
        with tempfile.TemporaryDirectory(dir=REPO / 'test', prefix='checkpoint_position_') as directory:
            directory = Path(directory)
            binary = directory / 'parity'
            subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
                '-I', str(REPO / 'sim2real/tita_ws/src/tita_controller/include'),
                str(REPO / 'test/sim2real/checkpoint_position_parity.cpp'), '-o', str(binary)], check=True)
            for checkpoint in (NEW, OLD):
                _, cfg, _, _ = describe_checkpoint(checkpoint)
                (directory / 'config.json').write_text(json.dumps(cfg))
                params = launch.policy_parameters(directory)
                self.assertEqual(len(params['obs_kind']), cfg['policy']['obs_dim'])
                self.assertEqual(params['leg_action_filter'], cfg['policy_interface']['leg_action_filter'])
                from launch import LaunchContext
                context = LaunchContext()
                context.launch_configurations.update(policy_dir=str(directory), namespace='desktop_test', output_enabled='false')
                with patch.object(launch, 'Node') as node:
                    launch.setup(context)
                    self.assertEqual(node.call_args_list[0].kwargs['parameters'][0]['leg_action_filter'],
                        cfg['policy_interface']['leg_action_filter'])
                    context.launch_configurations['leg_action_filter'] = 'none'
                    launch.setup(context)
                    self.assertEqual(node.call_args_list[2].kwargs['parameters'][0]['leg_action_filter'], 'none')
                stream = io.StringIO()
                stream.write(str(len(params['obs_kind'])) + '\n')
                np.savetxt(stream, np.array([params[key] for key in (
                    'obs_kind', 'obs_index', 'obs_scale', 'obs_low', 'obs_high')]).T,
                    fmt=['%d', '%d', '%.17g', '%.17g', '%.17g'])
                for key in ('default_joint_angles', 'default_joint_velocities', 'joint_kp', 'joint_kd', 'torque_limit'):
                    np.savetxt(stream, np.array(params[key]).reshape(1, -1))
                np.savetxt(stream, np.array([params[key] for key in (
                    'action_joint', 'action_velocity', 'action_scale', 'action_offset', 'action_low', 'action_high')]).T,
                    fmt=['%d', '%d', '%.17g', '%.17g', '%.17g', '%.17g'])
                position = [params.get('wheel_position_radius', 0.), params.get('wheel_position_clip_m', 0.),
                    *params.get('wheel_position_zero_thresholds', [0., 0., 0.])]
                np.savetxt(stream, np.array(position).reshape(1, -1))
                stream.write(params['leg_action_filter'] + '\n')
                builder, adapter = ObservationBuilder(cfg), ActionAdapter(cfg)
                filter_ = LegActionFilter(params['leg_action_filter'], adapter.order)
                expected = []
                q = np.array(cfg['robot']['default_joint_angles'])
                last = np.zeros(8, dtype=np.float32)
                for i in range(1000):
                    reset = i % 193 == 0
                    if reset:
                        builder.reset(); filter_.reset(); last[:] = 0.
                    q += rng.normal(0, .03, 8)
                    q[[3, 7]] += .3
                    wrapped = q.copy()
                    wrapped[[3, 7]] = (q[[3, 7]] + np.pi) % (2*np.pi) - np.pi
                    pitch = .25 * np.sin(i / 40)
                    quat = np.array([np.cos(pitch/2), 0., np.sin(pitch/2), 0.])
                    cmd = np.zeros(3) if i % 130 < 80 else np.array([.1, 0., 0.])
                    state = ObsState(wrapped, rng.normal(0, 1., 8), quat, rng.normal(0, 1., 3), cmd, last)
                    raw = rng.uniform(-3, 3, 8).astype(np.float32)
                    obs = builder.build(state)
                    applied = filter_.update(raw)
                    expected.append(np.r_[obs, applied, adapter.compute(applied, wrapped, state.joint_vel)])
                    np.savetxt(stream, np.r_[int(reset), wrapped, state.joint_vel, quat,
                        state.base_ang_vel, cmd, last, raw].reshape(1, -1), fmt=['%d'] + ['%.17g'] * 42)
                    last = raw.copy()
                result = subprocess.run([str(binary)], input=stream.getvalue(), text=True, capture_output=True, check=True)
                actual = np.loadtxt(io.StringIO(result.stdout))
                np.testing.assert_allclose(actual, expected, atol=1e-5, rtol=1e-6)
                obs_error = np.max(np.abs(actual[:, :cfg['policy']['obs_dim']] - np.array(expected)[:, :cfg['policy']['obs_dim']]))
                print(f'[DESKTOP_DRY_RUN] {cfg["policy"]["obs_dim"]} obs, {params["leg_action_filter"]}: '
                    f'1000 sequence samples, max observation error {obs_error:.3g}, '
                    f'max combined observation/action/torque error {np.max(np.abs(actual-expected)):.3g}')


if __name__ == '__main__':
    unittest.main(verbosity=2)
