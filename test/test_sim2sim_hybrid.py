"""DESKTOP_DRY_RUN: hybrid metadata, target gates and native clock semantics."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import yaml

from test_sim2sim_walk import config, saved_env, REPO
from sim2sim_ros2_jazzy.adapter import ActionAdapter, NATIVE_JOINTS, ObservationBuilder, ObsState
from sim2sim_ros2_jazzy.checkpoint import describe_checkpoint, observation_layout


def hybrid_config():
    cfg = config()
    cfg['gait_command'].update(step_in_place=False, clock='episode_steps')
    for action in cfg['policy_interface']['actions']:
        if action['joint'] in (NATIVE_JOINTS[3], NATIVE_JOINTS[7]):
            action.update(scale=20., gate='gait_disabled')
    return cfg


def hybrid_environment():
    env = saved_env()
    env['backend'] = 'mjlab'
    env['scene']['robot']['wheel_collision'] = 'sphere'
    env['commands']['gait']['step_in_place'] = False
    env['observations'] = {'policy': {'gait': dict(func='generated_commands', params={'command_name': 'gait'})}}
    env['actions'] = {}
    for index, joint in enumerate(NATIVE_JOINTS):
        wheel = index in (3, 7)
        action = dict(class_type='GaitGatedWheelVelocityAction' if wheel else 'JointPositionAction',
                      joint_names=[joint], scale=20. if wheel else .25)
        if wheel:
            action.update(gait_name='gait', wheel_enable='gait_disabled')
        env['actions'][str(index)] = action
    return env


class HybridAdapterTest(unittest.TestCase):
    def test_stop_latch_requires_measured_velocity_and_valid_metadata(self):
        params = dict(command_name='base_velocity', radius=.0925, clip_m=.3,
                      zero_thresholds=[.02, .02, .03], gait_name='gait',
                      velocity_thresholds=[.1, .15], moving_anchor=True)
        group = {'wheel': dict(func='WheelPositionError', params=params)}
        cfg = hybrid_config()
        cfg['policy_interface']['observations'] = observation_layout(group, {}, NATIVE_JOINTS)
        cfg['policy']['obs_dim'] = 1
        state = ObsState(np.zeros(8), np.zeros(8), np.array([1., 0., 0., 0.]),
                         np.zeros(3), np.zeros(3), np.zeros(8))
        builder = ObservationBuilder(cfg)
        for bad_velocity in (None, np.zeros(2), np.array([np.nan, 0., 0.])):
            state.base_lin_vel_b = bad_velocity
            with self.subTest(velocity=bad_velocity), self.assertRaisesRegex(ValueError, 'finite body'):
                builder.build(state)
        state.base_lin_vel_b = np.zeros(3)
        self.assertEqual(builder.build(state)[0], 0.)
        self.assertTrue(builder.position_latched)
        for bad in ([-.1, .15], [.1], [float('nan'), .15]):
            params['velocity_thresholds'] = bad
            with self.subTest(thresholds=bad), self.assertRaisesRegex(ValueError, 'velocity thresholds'):
                observation_layout(group, {}, NATIVE_JOINTS)
        params['velocity_thresholds'] = [.1, .15]
        params['moving_anchor'] = 'yes'
        with self.assertRaisesRegex(ValueError, 'must be boolean'):
            observation_layout(group, {}, NATIVE_JOINTS)

    def test_gate_after_clipping_in_policy_order_and_nominal_wheel_damping(self):
        cfg = hybrid_config()
        for action in cfg['policy_interface']['actions']:
            if action.get('gate'):
                action.update(offset=.2, clip=[1., 3.])
        cfg['policy_interface']['actions'] = list(reversed(cfg['policy_interface']['actions']))
        adapter = ActionAdapter(cfg)
        raw = np.ones(8, dtype=np.float32)
        preserved = raw.copy()
        np.testing.assert_array_equal(adapter.targets(raw, gait_enabled=False)[[3, 7]], [3., 3.])
        np.testing.assert_array_equal(adapter.targets(raw, gait_enabled=True)[[3, 7]], [0., 0.])
        np.testing.assert_array_equal(raw, preserved)
        np.testing.assert_allclose(adapter.compute(raw, np.zeros(8), np.ones(8), gait_enabled=True)[[3, 7]], [-.5, -.5])
        np.testing.assert_allclose(adapter.compute(raw, np.zeros(8), np.ones(8), gait_enabled=False)[[3, 7]], [1., 1.])
        for invalid in (None, np.nan, 2.):
            with self.subTest(flag=invalid), self.assertRaisesRegex(ValueError, 'gait-enabled flag'):
                adapter.targets(raw, gait_enabled=invalid)

    def test_explicit_metadata_only_both_wheels_and_gait_required(self):
        env = hybrid_environment()
        with tempfile.TemporaryDirectory(dir=REPO / 'test', prefix='hybrid_layout_') as directory:
            root = Path(directory)
            actor = root / 'actor.pt'
            actor.write_bytes(b'hybrid-metadata-only-fixture')
            (root / 'agent.json').write_text('{}')

            def describe(values):
                path = root / 'env.yaml'
                path.write_text(yaml.safe_dump(values, sort_keys=False))
                (root / 'ddt.json').write_text(json.dumps(dict(backend='mjlab',
                    actor_sha256=hashlib.sha256(actor.read_bytes()).hexdigest(), actor_obs_dim=5,
                    playback_config_sha256=hashlib.sha256(path.read_bytes()).hexdigest())))
                return describe_checkpoint(actor)

            _, cfg, _, _ = describe(env)
            self.assertEqual(cfg['gait_command']['clock'], 'episode_steps')
            self.assertEqual(sum(term.get('gate') == 'gait_disabled' for term in cfg['policy_interface']['actions']), 2)
            for key, value in (('gait_name', 'other'), ('wheel_enable', 'always')):
                invalid = deepcopy(env)
                invalid['actions']['3'][key] = value
                with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'gait-disabled mask'):
                    describe(invalid)
            invalid = deepcopy(env)
            invalid['actions']['7']['class_type'] = 'JointVelocityAction'
            with self.assertRaisesRegex(ValueError, 'gates on both wheels|wheel metadata'):
                describe(invalid)
            invalid = deepcopy(env)
            invalid['actions']['0'].update(class_type='GaitGatedWheelVelocityAction', gait_name='gait', wheel_enable='gait_disabled')
            with self.assertRaisesRegex(ValueError, 'only for wheel joints'):
                describe(invalid)
            invalid = deepcopy(env)
            invalid['observations']['policy'] = {'gyro': dict(func='base_ang_vel')}
            with self.assertRaisesRegex(ValueError, 'gait observation'):
                describe(invalid)

if __name__ == '__main__':
    unittest.main(verbosity=2)
