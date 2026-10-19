"""VALIDATION_SIM: frozen M4 parity, command gates and actual ROS torque path."""

import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO / 'sim2sim/sim2sim_ros2_jazzy'), str(REPO)]
from sim2sim_ros2_jazzy.cli import main
from sim2sim_ros2_jazzy.residual_wheel_lqr import BIAS, K, REFERENCE, ResidualWheelLQR
from flash_overnight_model_stages import CKPT, Runner, current, limited, prepared_config

SOURCE = REPO / 'docs/exp/2026-10-15/flash_overnight_pipeline/run_final'


class FixedM4Tests(unittest.TestCase):
    def test_disabled_is_exactly_original_playback(self):
        import rclpy
        from sim2sim_ros2_jazzy.sim2sim_node import Sim2SimNode
        spec = importlib.util.spec_from_file_location('sim2sim_ros2_jazzy._original_node',
            REPO / 'docs/exp/2026-10-15/residual_wheel_pd_integration/before/sim2sim/'
                   'sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/sim2sim_node.py')
        original = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(original)
        config = prepared_config(CKPT)
        rclpy.init(args=['--ros-args', '-p', f'config:={config}', '-p', 'viewer:=false'])
        self.addCleanup(rclpy.try_shutdown)
        traces = []
        for cls in [original.Sim2SimNode, Sim2SimNode]:
            node = cls()
            trace = []
            try:
                for _ in range(500):
                    node._step()
                    trace.append(np.r_[node.env.data.qpos, node.env.data.qvel,
                                       node.env.data.ctrl, node.last_action])
            finally:
                node.env.close()
                node.destroy_node()
            traces.append(trace)
        np.testing.assert_array_equal(*traces)

    def test_frozen_values_and_60s_reference_controller_parity(self):
        gain = json.loads((SOURCE / 'gains_frozen.json').read_text())['models']['M4']
        np.testing.assert_array_equal(K, gain['K'])
        np.testing.assert_array_equal(REFERENCE, gain['reference'])
        cfg = json.loads(prepared_config(CKPT).read_text())
        runner = Runner(cfg, dict(seed=270, pitch=0.))
        self.addCleanup(runner.env.close)
        for _ in range(400):
            runner.step(0.)
        residual = ResidualWheelLQR(runner.env)
        target = runner.observation['sensor'][0]
        previous_correction = previous_total = max_error = 0.
        for tick in range(3000):
            self.assertFalse(runner.failures())
            sensors_before = runner.env.data.sensordata.copy()
            residual.update(np.zeros(3), runner.playback.last_action)
            np.testing.assert_array_equal(runner.env.data.sensordata, sensors_before)
            z = current(runner)
            z[0] -= target
            correction = limited(-K @ (z[gain['indices']] - REFERENCE), previous_correction, tick * .02)
            total = float(np.clip(BIAS + correction, previous_total - .04, previous_total + .04))
            max_error = max(max_error, abs(total - residual.u))
            self.assertAlmostEqual(residual.position, z[0], delta=2e-8)
            self.assertAlmostEqual(residual.velocity, z[1], delta=2e-8)
            self.assertAlmostEqual(residual.u, total, delta=1e-6)
            self.assertLessEqual(abs(residual.u - previous_total), .040001)
            self.assertLessEqual(abs(residual.u), BIAS + .05)
            previous_correction, previous_total = correction, total
            transition = runner.step(residual.u)
            np.testing.assert_array_equal(transition['history'], z[gain['indices']][4:12])
            np.testing.assert_allclose(residual.apply(transition['flash'][0]), transition['motor'][0], atol=1e-7)
        print(f'[VALIDATION_SIM] 60s / 3000 steps; max reference residual error={max_error:.3g} Nm')

    def test_cli_and_ros_launch_forward_flag_and_reject_combination(self):
        with patch('sim2sim_ros2_jazzy.cli.os.execvpe') as execute:
            main(['--ckpt', str(CKPT), '--headless', '--steps', '2', '--fixed_residual_lqr'])
        self.assertIn('--fixed_residual_lqr', execute.call_args.args[1])
        with self.assertRaises(SystemExit):
            main(['--ckpt', str(CKPT), '--fixed_residual_lqr', '--residual_wheel_pd'])
        from launch import LaunchContext
        from launch.actions import OpaqueFunction
        spec = importlib.util.spec_from_file_location('fixed_m4_launch',
            REPO / 'sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py')
        launch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(launch)
        context = LaunchContext()
        context.launch_configurations.update(ckpt=str(CKPT), headless='true', steps='2',
                                             residual_wheel_pd='false', fixed_residual_lqr='true')
        function = next(x for x in launch.generate_launch_description().entities if isinstance(x, OpaqueFunction))
        process = function.execute(context)[0]
        command = [''.join(s.perform(context) for s in part) for part in process.cmd]
        self.assertIn('--fixed_residual_lqr', command)

    def test_actual_node_torque_gates_reset_and_checkpoint_guard(self):
        import rclpy
        from sim2sim_ros2_jazzy.sim2sim_node import Sim2SimNode
        config = prepared_config(CKPT)
        rclpy.init(args=['--ros-args', '-p', f'config:={config}', '-p', 'viewer:=false',
                        '-p', 'fixed_residual_lqr:=true'])
        self.addCleanup(rclpy.try_shutdown)
        node = Sim2SimNode()
        self.addCleanup(node.destroy_node)
        self.addCleanup(node.env.close)
        residual = node.residual
        self.assertIsInstance(residual, ResidualWheelLQR)
        original_apply = residual.apply
        applied = []

        def audit(torque):
            output = original_apply(torque)
            np.testing.assert_array_equal(output[[0, 1, 2, 4, 5, 6]], torque[[0, 1, 2, 4, 5, 6]])
            self.assertLessEqual(abs(output[[3, 7]]).max(), 12.)
            applied.append(residual.u)
            return output

        residual.apply = audit
        for _ in range(700):
            history = node.last_action.copy()
            node._step()
            np.testing.assert_array_equal(residual.previous_action, history if node.sm.state == 'rl' else np.zeros(8))
        self.assertGreater(len(applied), 100)
        self.assertGreater(max(applied), .4)
        node.command[0] = .1
        for _ in range(20):
            node._step()
        self.assertFalse(residual.holding)
        self.assertEqual(residual.u, 0.)
        node.command[:] = 0.
        node._step()
        self.assertTrue(residual.holding)
        self.assertEqual(residual.position, 0.)
        self.assertAlmostEqual(residual.u, .04)
        node._cmd_key_cb(type('Message', (), {'data': 'reset'})())
        node._step()
        self.assertEqual(residual.u, 0.)
        self.assertFalse(residual.holding)
        node.env.cfg['policy_interface']['checkpoint_sha256'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'checkpoint'):
            ResidualWheelLQR(node.env)


if __name__ == '__main__':
    unittest.main(verbosity=2)
