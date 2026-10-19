"""VALIDATION_SIM: bounded hold, estimator fidelity, opt-in and real RL callback."""

import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO / 'sim2sim/sim2sim_ros2_jazzy'), str(REPO)]
from sim2sim_ros2_jazzy.checkpoint import describe_checkpoint, prepared_config, read_yaml
from sim2sim_ros2_jazzy.cli import main
from sim2sim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from sim2sim_ros2_jazzy.residual_wheel_pd import ResidualWheelPD
from sim2sim.lqr.estimator import Sensors, WheelOdometry
from sim2sim.lqr.model import Description

CKPT = REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_50000'
OUT = REPO / 'docs/exp/2026-10-15/residual_wheel_pd_integration'


class ResidualTests(unittest.TestCase):
    def setUp(self):
        self.path, self.cfg, _, _ = describe_checkpoint(CKPT)
        self.env = TitaMujocoEnv(self.cfg)
        self.addCleanup(self.env.close)
        self.residual = ResidualWheelPD(self.env)

    def test_encoder_imu_matches_existing_estimator_and_preserves_physics_cache(self):
        source = read_yaml(next(p for p in self.cfg['policy_interface']['sources'] if p.endswith('env.yaml')))
        reference = WheelOdometry(Description(source['scene']['robot']['spawn']['asset_path']), 0.)
        rng = np.random.default_rng(27)
        for tick in range(80):
            self.env.data.qpos[self.env.qpos_addr] = self.cfg['robot']['default_joint_angles'] + rng.normal(0., .01, 8)
            self.env.data.qvel[:] = rng.normal(0., .05, self.env.model.nv)
            self.env.data.qpos[:3] += [10., -20., 30.]  # Root translation must not enter odometry.
            old_sensors = self.env.data.sensordata.copy()
            self.residual.update(np.zeros(3))
            data = self.residual.data
            state = reference.observe(Sensors(self.env.joint_pos(), self.env.joint_vel(),
                data.sensor('trunk_quat').data, data.sensor('trunk_gyro').data), self.env.control_dt)
            np.testing.assert_allclose([self.residual.position, self.residual.velocity], state[:2], atol=2e-8)
            np.testing.assert_array_equal(self.env.data.sensordata, old_sensors)

    def test_hold_reset_ramp_slew_release_and_wheel_only_clipping(self):
        self.env.data.qvel[self.env.qvel_addr[[3, 7]]] = 10.
        previous = 0.
        for tick in range(100):
            self.env.data.qpos[self.env.qpos_addr[[3, 7]]] += .1
            self.residual.update(np.zeros(3))
            self.assertLessEqual(abs(self.residual.u - previous), .04 + 1e-12)
            self.assertLessEqual(abs(self.residual.u), 2.)
            if tick == 0:
                self.assertEqual(self.residual.position, 0.)
                self.assertEqual(self.residual.u, 0.)
            if tick == 25:
                self.assertAlmostEqual(self.residual.u, -2. * (1/3)**2 * (3-2/3), places=6)
            previous = self.residual.u
        self.assertGreater(self.residual.position, .5)
        self.assertAlmostEqual(abs(self.residual.u), 2.)
        torque = np.arange(8, dtype=np.float32)
        torque[[3, 7]] = -12.
        result = self.residual.apply(torque)
        np.testing.assert_array_equal(result[[0, 1, 2, 4, 5, 6]], torque[[0, 1, 2, 4, 5, 6]])
        self.assertLessEqual(abs(result[[3, 7]]).max(), 12.)
        np.testing.assert_array_equal(torque[[3, 7]], [-12., -12.])
        for _ in range(60):
            self.residual.update(np.array([0., 0., .3]))
            self.assertFalse(self.residual.holding)
            self.assertLessEqual(abs(self.residual.u - previous), .04 + 1e-12)
            previous = self.residual.u
        self.assertEqual(self.residual.u, 0.)
        self.residual.update(np.zeros(3))
        self.assertEqual(self.residual.position, 0.)
        self.assertEqual(self.residual.u, 0.)
        self.residual.update(None)
        self.assertFalse(self.residual.holding)
        self.assertEqual(self.residual.u, 0.)

    def test_cli_passes_opt_in_to_runtime(self):
        with patch('sim2sim_ros2_jazzy.cli.os.execvpe') as execute:
            main(['--ckpt', str(CKPT), '--headless', '--steps', '2', '--residual_wheel_pd'])
        command = execute.call_args.args[1]
        self.assertIn('--residual_wheel_pd', command)


class RuntimeTests(unittest.TestCase):
    def test_disabled_matches_before_and_enabled_reaches_actual_rl_callback(self):
        import rclpy
        from sim2sim_ros2_jazzy.sim2sim_node import Sim2SimNode
        spec = importlib.util.spec_from_file_location('sim2sim_ros2_jazzy._before_residual_node',
            OUT / 'before/sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/sim2sim_node.py')
        before = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(before)
        config = prepared_config(CKPT)
        rclpy.init(args=['--ros-args', '-p', f'config:={config}', '-p', 'viewer:=false'])
        try:
            traces = []
            enabled_audit = dict(rl_steps=0, max_total_residual=0., max_slew_step=0., leg_torque_error=0.)
            for cls, enabled in [(before.Sim2SimNode, False), (Sim2SimNode, False), (Sim2SimNode, True)]:
                node = cls()
                if enabled:
                    node.residual = ResidualWheelPD(node.env)
                states, commands, actions = [], [], []
                previous = 0.
                try:
                    for tick in range(600):
                        node.command[:] = [0.1 if 220 <= tick < 300 else 0., 0., 0.]
                        if enabled:
                            # Observe the actual callback output at each physics substep.
                            def observe_torque(torque):
                                output = ResidualWheelPD.apply(node.residual, torque)
                                error = abs(output[[0, 1, 2, 4, 5, 6]] - torque[[0, 1, 2, 4, 5, 6]]).max()
                                enabled_audit['leg_torque_error'] = max(enabled_audit['leg_torque_error'], float(error))
                                return output
                            node.residual.apply = observe_torque
                        node._step()
                        states.append(np.r_[node.env.data.qpos, node.env.data.qvel])
                        commands.append(node.env.data.ctrl.copy())
                        actions.append(node.last_action.copy())
                        if enabled and node.sm.state == 'rl':
                            enabled_audit['rl_steps'] += 1
                            enabled_audit['max_total_residual'] = max(enabled_audit['max_total_residual'], abs(node.residual.u))
                            enabled_audit['max_slew_step'] = max(enabled_audit['max_slew_step'], abs(node.residual.u - previous))
                            previous = node.residual.u
                    if enabled:
                        node._cmd_key_cb(type('Message', (), {'data': 'reset'})())
                        node._step()
                        self.assertEqual(node.residual.u, 0.)
                        self.assertFalse(node.residual.holding)
                finally:
                    node.env.close()
                    node.destroy_node()
                traces.append((np.asarray(states), np.asarray(commands), np.asarray(actions)))
            for a, b in zip(traces[0], traces[1]):
                np.testing.assert_array_equal(a, b)
            self.assertGreater(enabled_audit['rl_steps'], 100)
            self.assertGreater(enabled_audit['max_total_residual'], .01)
            self.assertLessEqual(enabled_audit['max_total_residual'], 2.)
            self.assertLessEqual(enabled_audit['max_slew_step'], .04 + 1e-12)
            self.assertEqual(enabled_audit['leg_torque_error'], 0.)
            (OUT / 'runtime_audit.json').write_text(json.dumps(dict(execution_domain='VALIDATION_SIM',
                evidence_status='PASS', disabled_exact_before=True, steps_per_run=600, **enabled_audit), indent=2)+'\n')
        finally:
            rclpy.try_shutdown()


if __name__ == '__main__':
    unittest.main(verbosity=2)
