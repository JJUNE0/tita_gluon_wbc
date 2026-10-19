"""DESKTOP_DRY_RUN / VALIDATION_SIM: actual sensor, target and ROS integration checks."""

import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np
from scipy.spatial.transform import Rotation

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO / 'sim2sim/sim2sim_ros2_jazzy'), str(REPO)]
from sim2sim_ros2_jazzy.adapter import ActionAdapter
from sim2sim_ros2_jazzy.cli import main
from sim2sim_ros2_jazzy.velocity_bias import WheelVelocityBias
from velocity_bias_campaign import make_runner

ROOT = REPO / 'docs/exp/2026-10-16/velocity_bias_overnight'
CONFIG = ROOT / 'exports/tita_flash_sac_115632_883848_model_60000/config.json'
CFG = json.loads(CONFIG.read_text())
CHECKPOINT = CFG['policy_interface']['checkpoint']
WHEELS = [3, 7]
LEGS = [0, 1, 2, 4, 5, 6]


class VelocityRuntimeTests(unittest.TestCase):
    def runner(self):
        runner = make_runner(CFG, dict(seed=271))
        self.addCleanup(runner.env.close)
        for _ in range(400):
            runner.step_bias(0.)
        return runner

    def test_sensor_fk_matches_research_and_ignores_root_translation_and_velocity(self):
        runner = self.runner()
        hold = WheelVelocityBias(runner.env)
        error = 0.
        geometry_error = 0.
        for tick in range(200):
            before = runner.env.data.sensordata.copy()
            hold.update(np.zeros(3))
            np.testing.assert_array_equal(before, runner.env.data.sensordata)
            frames, _ = runner.description.frames(runner.env.joint_pos())
            rotation = Rotation.from_quat(hold.data.sensor('trunk_quat').data[[1, 2, 3, 0]])
            sensor_offset = rotation.apply(np.mean(
                [frames[name][:3, 3] for name in runner.description.wheel_links], axis=0))
            geometry_offset = hold.data.xpos[hold.wheel_bodies].mean(0) - hold.data.xpos[hold.base_body]
            geometry_error = max(geometry_error, float(np.max(abs(sensor_offset - geometry_offset))))
            if tick:
                error = max(error, abs(hold.velocity - runner.observation['fk_sensor'][1]))
            runner.step_bias(0.)
        self.assertLess(error, 2e-8)
        self.assertLess(geometry_error, 1e-7)
        print('[VALIDATION_SIM] FK observer vs independent research maximum m/s:', error)
        print('[VALIDATION_SIM] Encoder/IMU URDF FK vs relative geometry maximum m:', geometry_error)
        values = []
        qpos, qvel = runner.env.data.qpos.copy(), runner.env.data.qvel.copy()
        for shift, linear_velocity in [(np.zeros(3), np.zeros(3)),
                                       (np.array([20., -30., 5.]), np.array([100., -50., 20.]))]:
            runner.env.data.qpos[:] = qpos
            runner.env.data.qpos[:3] += shift
            runner.env.data.qvel[:] = qvel
            runner.env.data.qvel[:3] = linear_velocity
            runner.env.mujoco.mj_forward(runner.env.model, runner.env.data)
            hold.reset()
            hold.update(np.zeros(3))
            hold.update(np.zeros(3))
            values.append(hold.velocity)
        self.assertAlmostEqual(*values, delta=2e-8)

    def test_same_timestamp_root_impulse_does_not_erase_measured_fk_derivative(self):
        runner = self.runner()
        before = runner.observation
        yaw = before['rpy'][2]
        runner.env.data.qvel[:3] += .2 * np.array([np.cos(yaw), np.sin(yaw), 0.])
        runner.env.mujoco.mj_forward(runner.env.model, runner.env.data)
        after = runner.observe()
        np.testing.assert_allclose(after['fk_sensor'], before['fk_sensor'], atol=1e-12, rtol=0.)
        self.assertAlmostEqual(float(after['base_velocity'][0] - before['base_velocity'][0]), .2, delta=1e-8)

    def test_only_validated_flashsac_period_is_accepted(self):
        runner = self.runner()
        with patch.dict(runner.env.cfg['policy_interface'], algorithm='PPO'):
            with self.assertRaisesRegex(ValueError, 'FlashSAC'):
                WheelVelocityBias(runner.env)
        with patch.object(runner.env, 'control_dt', .01):
            with self.assertRaisesRegex(ValueError, '20 ms'):
                WheelVelocityBias(runner.env)

    def test_velocity_target_added_before_saturation_legs_unchanged_and_lifecycle(self):
        runner = self.runner()
        env = runner.env
        hold = WheelVelocityBias(env)
        hold.update(np.zeros(3))
        adapter = ActionAdapter(CFG)
        action = np.zeros(8, dtype=np.float32)
        positions = env.joint_pos()
        velocities = env.joint_vel().copy()
        targets = adapter.targets(action)
        velocities[WHEELS] = targets[WHEELS] - 14. / adapter.kd[WHEELS]
        hold.signs = np.ones(2)
        hold.u = -10. * hold.radius / float(adapter.kd[3])
        actual = hold.compute(adapter, action, positions, velocities)
        np.testing.assert_allclose(actual[WHEELS], 4., atol=1e-5)
        np.testing.assert_array_equal(actual[LEGS], adapter.compute(action, positions, velocities)[LEGS])
        self.assertTrue(np.all(abs(actual) <= adapter.limit))
        hold.u = .1
        hold.update(np.array([.1, 0., 0.]))
        self.assertFalse(hold.holding)
        self.assertEqual(hold.law.integral, 0.)
        self.assertAlmostEqual(hold.u, .1 - hold.slew_rate * env.control_dt)
        for _ in range(10):
            hold.update(np.array([.1, 0., 0.]))
        self.assertEqual(hold.u, 0.)
        hold.update(np.zeros(3))
        self.assertTrue(hold.holding)
        self.assertFalse(hold.eligible)
        self.assertEqual(hold.law.integral, 0.)
        hold.update(None)
        self.assertFalse(hold.holding)
        self.assertEqual(hold.u, 0.)

    def test_cli_ros_launch_and_mutual_exclusion(self):
        with patch('sim2sim_ros2_jazzy.cli.os.execvpe') as execute:
            main(['--ckpt', CHECKPOINT, '--headless', '--steps', '2', '--velocity_bias'])
        self.assertIn('--velocity_bias', execute.call_args.args[1])
        for conflict in ['--fixed_residual_lqr', '--residual_wheel_pd']:
            with self.assertRaises(SystemExit):
                main(['--ckpt', CHECKPOINT, '--velocity_bias', conflict])
        from launch import LaunchContext
        from launch.actions import OpaqueFunction
        spec = importlib.util.spec_from_file_location('velocity_launch',
            REPO / 'sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py')
        launch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(launch)
        context = LaunchContext()
        context.launch_configurations.update(ckpt=CHECKPOINT, headless='true', steps='2',
            residual_wheel_pd='false', fixed_residual_lqr='false', velocity_bias='true')
        function = next(x for x in launch.generate_launch_description().entities if isinstance(x, OpaqueFunction))
        process = function.execute(context)[0]
        command = [''.join(s.perform(context) for s in part) for part in process.cmd]
        self.assertIn('--velocity_bias', command)

    def test_actual_ros_node_preserves_raw_action_and_native_leg_torque(self):
        import rclpy
        from sim2sim_ros2_jazzy.sim2sim_node import Sim2SimNode
        rclpy.init(args=['--ros-args', '-p', f'config:={CONFIG}', '-p', 'viewer:=false',
                        '-p', 'velocity_bias:=true'])
        self.addCleanup(rclpy.try_shutdown)
        node = Sim2SimNode()
        self.addCleanup(node.destroy_node)
        self.addCleanup(node.env.close)
        self.assertIsInstance(node.residual, WheelVelocityBias)
        actual_compute = node.residual.compute
        calls = []

        def audited(adapter, action, positions, velocities):
            torque = actual_compute(adapter, action, positions, velocities)
            baseline = adapter.compute(action, positions, velocities)
            np.testing.assert_array_equal(torque[LEGS], baseline[LEGS])
            self.assertTrue(np.all(abs(torque) <= adapter.limit))
            calls.append(node.residual.u)
            return torque

        node.residual.compute = audited
        for _ in range(900):
            history = node.last_action.copy()
            build = node.obs_builder.build
            with patch.object(node.obs_builder, 'build', side_effect=lambda state: (
                np.testing.assert_array_equal(state.last_action, history if node.sm.state == 'rl' else np.zeros(8)),
                build(state))[1]):
                node._step()
        self.assertGreater(len(calls), 500)
        self.assertGreater(max(abs(np.asarray(calls))), .01)
        node.command[0] = .1
        for _ in range(100):
            node._step()
        self.assertFalse(node.residual.holding)
        self.assertEqual(node.residual.u, 0.)
        node._cmd_key_cb(type('Message', (), {'data': 'reset'})())
        node._step()
        self.assertFalse(node.residual.holding)
        self.assertEqual(node.residual.u, 0.)


if __name__ == '__main__':
    unittest.main(verbosity=2)
