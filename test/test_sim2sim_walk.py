"""DESKTOP_DRY_RUN / VALIDATION_SIM: saved walk layout, clock and wheel contacts."""

import ast
from copy import deepcopy
import importlib.util
import hashlib
import json
import math
from pathlib import Path
import sys
import tempfile
from types import MethodType, SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np
import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import ActionAdapter, NATIVE_JOINTS, ObservationBuilder, ObsState
from sim2sim_ros2_jazzy.checkpoint import describe_checkpoint, observation_layout, simulation_config
from sim2sim_ros2_jazzy import checkpoint


def saved_env():
    defaults = dict(joint_pos=dict(zip(NATIVE_JOINTS, [0., .8, -1.5, 0.] * 2)),
                    joint_vel={'.*': 0.}, pos=[0., 0., .4], rot=[1., 0., 0., 0.])
    gait = dict(class_type='walk_mdp:WalkGaitCommand', velocity_command_name='base_velocity',
                frequency_range_hz=[1.25, 1.25], stance_fraction=.6, settle_time_s=1.,
                linear_threshold=.02, yaw_threshold=.03, step_in_place=True)
    robot = dict(init_state=defaults, spawn={'asset_path': '/moved/tita_sphere_wheels_test.urdf'}, actuators={
        'legs': dict(joint_names_expr=['.*_leg_[12]'], stiffness=60., damping=1.5, effort_limit=60.),
        'knees': dict(joint_names_expr=['.*_leg_3'], stiffness=92., damping=2.3, effort_limit=60.),
        'wheels': dict(joint_names_expr=['.*_leg_4'], stiffness=0., damping=.5, effort_limit=12.),
    })
    return dict(scene=dict(robot=robot, terrain={'terrain_type': 'plane'}), sim={'dt': .005}, decimation=4,
                commands=dict(gait=gait, base_velocity=dict(
                    ranges=dict(lin_vel_x=[-.5, .5], lin_vel_y=[-.5, .5], ang_vel_z=[0., 0.]),
                    ramp_rate=.3, initial_phase_time=1.)))


def config():
    env = saved_env()
    layout = observation_layout({'gait': dict(func='mdp:generated_commands', params={'command_name': 'gait'})}, {}, NATIVE_JOINTS)
    cfg = simulation_config(env, env['scene']['robot']['init_state'], layout)
    cfg['policy_interface'] = dict(observations=layout, actions=[
        dict(joint=joint, kind='velocity' if i in (3, 7) else 'position',
             scale=0. if i in (3, 7) else .25, offset=0., clip=None)
        for i, joint in enumerate(NATIVE_JOINTS)
    ])
    return cfg


class WalkAdapterTest(unittest.TestCase):
    def test_generated_commands_resolve_by_command_name_and_keep_order(self):
        group = {name: dict(func='mdp:generated_commands', params={'command_name': command})
                 for name, command in (('gait', 'gait'), ('velocity', 'base_velocity'))}
        layout = observation_layout(group, {}, NATIVE_JOINTS)
        self.assertEqual([(x['name'], x['kind'], x['size']) for x in layout],
                         [('gait', 'gait', 5), ('velocity', 'commands', 3)])
        with self.assertRaisesRegex(ValueError, 'Unsupported generated command'):
            observation_layout({'x': dict(func='generated_commands', params={'command_name': 'unknown'})}, {}, NATIVE_JOINTS)

    def test_saved_gait_ranges_pd_and_model_settings(self):
        env = saved_env()
        env['commands']['base_velocity']['ranges']['lin_vel_y'] = [-.13, .19]
        env['commands']['gait']['stance_fraction'] = .67
        # Isolate saved-range restoration from the operator's YAML caps.
        template = checkpoint.read_yaml(checkpoint.PACKAGE / 'config/tita.yaml')
        template['command']['max_lin_y'] = .5
        with patch.object(checkpoint, 'read_yaml', return_value=template):
            cfg = simulation_config(env, env['scene']['robot']['init_state'], [{'kind': 'gait', 'size': 5}])
        self.assertEqual(cfg['sim_command_ranges']['lin_vel_y'], [-.13, .19])
        self.assertEqual(cfg['gait_command']['stance_fraction'], .67)
        self.assertEqual(cfg['model']['wheel_collision'], 'sphere')
        self.assertTrue(cfg['model']['flat_ground'])
        self.assertEqual(cfg['robot']['joint_kp'], [60., 60., 92., 0.] * 2)
        self.assertEqual(cfg['robot']['joint_kd'], [1.5, 1.5, 2.3, .5] * 2)

    def test_driving_checkpoint_keeps_model_and_has_no_gait(self):
        env = saved_env()
        cfg = simulation_config(env, env['scene']['robot']['init_state'], [])
        self.assertNotIn('gait_command', cfg)
        self.assertNotIn('wheel_collision', cfg['model'])
        self.assertNotIn('flat_ground', cfg['model'])

    def test_invalid_saved_gait_parameters_fail(self):
        for changes in ({'frequency_range_hz': [2., 1.]}, {'stance_fraction': .4},
                        {'settle_time_s': -1.}, {'linear_threshold': float('nan')}, {'step_in_place': 'true'}):
            env = saved_env()
            env['commands']['gait'].update(changes)
            with self.subTest(changes=changes), self.assertRaisesRegex(ValueError, 'Invalid saved walking gait'):
                simulation_config(env, env['scene']['robot']['init_state'], [{'kind': 'gait', 'size': 5}])

    def test_build_does_not_advance_clock_and_reset_clears_state(self):
        builder = ObservationBuilder(config())
        state = ObsState(np.zeros(8), np.zeros(8), np.array([1., 0., 0., 0.]), np.zeros(3), np.zeros(3), np.zeros(8))
        before = builder.build(state)
        np.testing.assert_allclose(before, [0., 0., 0., 1.25, .6])
        for _ in range(60):
            builder.advance_gait(state.command)
        value = builder.build(state)
        self.assertEqual(value[0], 1.)
        np.testing.assert_array_equal(value, builder.build(state))
        builder.reset()
        np.testing.assert_array_equal(before, builder.build(state))

    def test_wheel_targets_stay_zero_for_any_policy_output(self):
        adapter = ActionAdapter(config())
        for action in (np.full(8, 6.), np.full(8, -6.)):
            np.testing.assert_array_equal(adapter.targets(action)[[3, 7]], [0., 0.])
        np.testing.assert_allclose(adapter.compute(np.ones(8), np.zeros(8), np.ones(8))[[3, 7]], [-.5, -.5])

    def test_walk_rejects_nonzero_saved_wheel_velocity_targets(self):
        env = saved_env()
        env['observations'] = {'policy': {'gait': dict(func='generated_commands', params={'command_name': 'gait'})}}
        env['actions'] = {
            str(i): dict(class_type='JointVelocityAction' if i in (3, 7) else 'JointPositionAction',
                         joint_names=[joint], scale=0. if i in (3, 7) else .25)
            for i, joint in enumerate(NATIVE_JOINTS)
        }
        with tempfile.TemporaryDirectory(dir=REPO / 'test', prefix='walk_wheel_mask_') as directory:
            root = Path(directory)
            actor = root / 'actor.pt'
            actor.write_bytes(b'metadata-only unit fixture')
            (root / 'agent.json').write_text('{}')
            (root / 'ddt.json').write_text(json.dumps({'actor_sha256': hashlib.sha256(actor.read_bytes()).hexdigest(), 'actor_obs_dim': 5}))
            (root / 'env.yaml').write_text(yaml.safe_dump(env, sort_keys=False))
            describe_checkpoint(actor)
            for change in ({'scale': 5.}, {'scale': 0., 'use_default_offset': False, 'offset': .1}, {'scale': 0., 'clip': [1., 2.]}):
                modified = deepcopy(env)
                modified['actions']['3'].update(change)
                (root / 'env.yaml').write_text(yaml.safe_dump(modified, sort_keys=False))
                with self.subTest(change=change), self.assertRaisesRegex(ValueError, 'zero wheel velocity targets'):
                    describe_checkpoint(actor)

    @unittest.skipUnless(importlib.util.find_spec('torch'), 'training clock parity uses the Isaac Torch interpreter')
    def test_gait_matches_actual_training_clock_for_stop_start_and_zero(self):
        import torch
        source = REPO / 'isaac_lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/walk_mdp.py'
        cls = next(n for n in ast.parse(source.read_text()).body if isinstance(n, ast.ClassDef) and n.name == 'WalkGaitCommand')
        methods = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in ('_update_command', '_write_command')]
        scope = dict(torch=torch, math=math)
        exec(compile(ast.Module(body=methods, type_ignores=[]), str(source), 'exec'), scope)
        for step_in_place in (False, True):
            cfg = config()
            cfg['gait_command']['step_in_place'] = step_in_place
            builder = ObservationBuilder(cfg)
            command = torch.zeros(1, 3)
            ref = SimpleNamespace(cfg=SimpleNamespace(**cfg['gait_command']), elapsed=torch.zeros(1), phase=torch.zeros(1),
                                  frequency=torch.tensor([1.25]), _command=torch.zeros(1, 5),
                                  _env=SimpleNamespace(step_dt=.02, command_manager=SimpleNamespace(get_command=lambda _: command)))
            ref.cfg.velocity_command_name = 'base_velocity'
            ref._write_command = MethodType(scope['_write_command'], ref)
            ref._write_command(torch.tensor([False]))
            for target in ([0., 0., 0.], [.3, 0., 0.], [0., 0., 0.], [0., -.3, 0.]):
                command[:] = torch.tensor(target)
                for _ in range(75):
                    np.testing.assert_allclose(builder.gait_command(), ref._command[0].numpy(), atol=1e-6)
                    scope['_update_command'](ref)
                    builder.advance_gait(np.array(target, dtype=np.float32))

    @unittest.skipUnless(importlib.util.find_spec('mujoco'), 'MuJoCo contact check uses the MuJoCo interpreter')
    def test_walk_uses_sphere_contacts_flat_ground_and_saved_reset(self):
        from sim2sim_ros2_jazzy.mujoco_env import TitaMujocoEnv
        cfg = config()
        env = TitaMujocoEnv(cfg)
        try:
            for side in ('left', 'right'):
                body = env.model.body(f'{side}_leg_4').id
                active = [g for g in range(env.model.ngeom) if env.model.geom_bodyid[g] == body
                          and (env.model.geom_contype[g] or env.model.geom_conaffinity[g])]
                self.assertEqual(len(active), 1)
                self.assertEqual(env.model.geom_type[active[0]], env.mujoco.mjtGeom.mjGEOM_SPHERE)
                self.assertAlmostEqual(env.model.geom_size[active[0], 0], .0925)
            floor = env.model.geom('floor').id
            obstacles = (env.model.geom_bodyid == 0) & (np.arange(env.model.ngeom) != floor)
            self.assertFalse(env.model.geom_contype[obstacles].any())
            np.testing.assert_allclose(env.joint_pos(), cfg['robot']['default_joint_angles'])
        finally:
            env.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
