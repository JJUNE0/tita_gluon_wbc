"""DESKTOP_DRY_RUN: C++ bias/observer/torque parity, gating, bounds and bag replay."""
import importlib.util
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from scipy.spatial.transform import Rotation

REPO = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(REPO), str(REPO / 'sim2sim/sim2sim_ros2_jazzy')]
from sim2sim.lqr.model import Description
from sim2sim.lqr.estimator import Sensors, WheelOdometry
from sim2sim_ros2_jazzy.adapter import ActionAdapter, NATIVE_JOINTS
from sim2sim_ros2_jazzy.velocity_bias import VelocityBias

PACKAGE = REPO / 'sim2real/tita_ws/src/tita_controller'
CFG = json.loads((PACKAGE / 'policies/flashsac_60000/config.json').read_text())
GEOMETRY = json.loads((PACKAGE / 'config/velocity_bias_geometry.json').read_text())
ARTIFACTS = REPO / 'docs/exp/2026-10-17/flashsac_velocity_bias_sim_limits'


class VelocityBiasPortTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(dir=REPO / 'test/sim2real', prefix='bias_port_')
        cls.binary = Path(cls.temp.name) / 'runtime'
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
                        '-I/usr/include/eigen3', '-I', str(PACKAGE / 'include'),
                        str(REPO / 'test/sim2real/velocity_bias_runtime.cpp'), '-o', str(cls.binary)], check=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def execute(self, mode, header, rows):
        stream = io.StringIO()
        np.savetxt(stream, np.array(header).reshape(1, -1), fmt='%.17g')
        np.savetxt(stream, rows, fmt='%.17g')
        result = subprocess.run([str(self.binary), mode], input=stream.getvalue(),
                                capture_output=True, text=True, check=True)
        return np.loadtxt(io.StringIO(result.stdout), ndmin=2)

    def controller(self, rows, enabled=True):
        terms = []
        for a in CFG['policy_interface']['actions']:
            terms.extend([NATIVE_JOINTS.index(a['joint']), int(a['kind'] == 'velocity'),
                          a['scale'], a['offset'], *(a['clip'] or [-1e9, 1e9])])
        header = [*GEOMETRY['xyz'], *GEOMETRY['rpy'], *GEOMETRY['axis'],
                  GEOMETRY['wheel_radius'], 1.,
                  *CFG['robot']['joint_kp'], *CFG['robot']['joint_kd'],
                  *CFG['robot']['torque_limit'], *terms]
        return self.execute('on' if enabled else 'off', header, rows)

    def reference(self, rows):
        description = Description(REPO / GEOMETRY['source_urdf'])
        observer = WheelOdometry(description, 0.)
        adapter = ActionAdapter(CFG)
        radius = description.radius
        law = VelocityBias()  # Actual sim2sim defaults, no Nm-derived limit override.
        slew = law.slew
        holding, age, u, offset_previous = False, 0., 0., None
        signs = np.zeros(2)
        output = []
        for row in rows:
            rl, dt = row[:2]
            cmd, q, dq, quat, gyro, action = row[2:5], row[5:13], row[13:21], row[21:25], row[25:28], row[28:36].astype(np.float32)
            eligible, velocity = False, 0.
            if not rl or dt <= 0 or dt > .06:
                holding, age, u, offset_previous = False, 0., 0., None
                signs[:] = 0
                law.reset()
            else:
                if not holding and np.all(abs(cmd) <= [.02, .02, .03]):
                    holding, age, offset_previous = True, 0., None
                elif holding and np.any(abs(cmd) >= [.04, .04, .06]):
                    holding = False
                target = 0.
                if holding:
                    rot = Rotation.from_quat(quat[[1, 2, 3, 0]])
                    roll, pitch, yaw = rot.as_euler('xyz')
                    frames, axes = description.frames(q)
                    lateral = np.array([-np.sin(yaw), np.cos(yaw), 0.])
                    signs = np.sign([lateral @ rot.apply(axes[NATIVE_JOINTS[i]]) for i in [3, 7]])
                    raw = observer.observe(Sensors(q, dq, quat, gyro), dt)[1]
                    offset = rot.apply(np.mean([frames[n][:3, 3] for n in description.wheel_links], axis=0))
                    correction = 0. if offset_previous is None else (offset - offset_previous) @ [np.cos(yaw), np.sin(yaw), 0.] / dt
                    velocity = raw - correction
                    offset_previous = offset
                    eligible = age + 1e-9 >= 2. and max(abs(roll), abs(pitch)) <= .3 and abs(velocity) <= 1.
                    target = law.update(float(velocity), dt, enabled=eligible)
                    age += dt
                else:
                    law.reset()
                    age, offset_previous = 0., None
                u = float(np.clip(target, u - slew * dt, u + slew * dt))
            offsets = signs * u / radius
            baseline = adapter.compute(action, q, dq)
            actual = baseline.copy()
            targets = adapter.targets(action)[[3, 7]].copy()
            targets += offsets
            actual[[3, 7]] = np.clip(adapter.kd[[3, 7]] * (targets - dq[[3, 7]]),
                                     -adapter.limit[[3, 7]], adapter.limit[[3, 7]])
            output.append([holding, eligible, age, velocity, law.filtered, law.integral, u,
                           *offsets, *actual, *baseline])
        return np.array(output)

    def test_pi_law_matches_sim2sim_for_both_signs_and_inhibition(self):
        rng = np.random.default_rng(17)
        rows = np.c_[rng.uniform(-1, 1, 2000), rng.uniform(.01, .04, 2000), np.ones(2000)]
        rows[400:500, 2] = 0
        for sign in [-1., 1.]:
            law = VelocityBias(limit=2., slew=3., response_sign=sign)
            reference = []
            for velocity, dt, enabled in rows:
                law.update(velocity, dt, enabled=bool(enabled))
                reference.append([law.filtered, law.integral, law.bias, law.age, law.seeded])
            actual = self.execute('law', [2., 3., sign], rows)
            np.testing.assert_allclose(actual, reference, atol=1e-12, rtol=1e-12)
        print('PASS PI: 4000 updates, both response signs, seed/filter/inhibit/saturation/slew')

    def test_lifecycle_guards_and_false_mode_exact_baseline(self):
        rows = np.zeros((450, 36))
        rows[:, :2] = [1., .02]
        rows[:, 5:13] = CFG['robot']['default_joint_angles']
        rows[:, [16, 20]] = -2.
        rows[:, 21] = 1.
        rows[160:180, 2] = .1
        quat = Rotation.from_euler('xyz', [.4, 0., 0.]).as_quat()[[3, 0, 1, 2]]
        rows[310:330, 21:25] = quat
        rows[350:360, [16, 20]] = 20.
        rows[390, 1] = .08
        rows[420:, 0] = 0.
        actual = self.controller(rows)
        expected = self.reference(rows)
        np.testing.assert_allclose(actual, expected, atol=1e-5, rtol=1e-6)
        self.assertFalse(actual[:100, 1].any())
        self.assertTrue(actual[100, 1])
        self.assertEqual(actual[:101, 6].max(), 0.)
        self.assertTrue((actual[120:160, 6] < 0).all())
        self.assertFalse(actual[160:180, 0].any())
        self.assertFalse(actual[180:280, 1].any())
        self.assertFalse(actual[310:330, 1].any())
        self.assertFalse(actual[350:360, 1].any())
        np.testing.assert_array_equal(actual[390, :9], 0.)
        np.testing.assert_array_equal(actual[420:, :9], 0.)
        legs = [0, 1, 2, 4, 5, 6]
        np.testing.assert_array_equal(actual[:, 9:17][:, legs], actual[:, 17:25][:, legs])
        self.assertTrue((abs(actual[:, 9:17]) <= np.array(CFG['robot']['torque_limit']) + 1e-12).all())
        self.assertLessEqual(abs(actual[:, 6]).max(), 2.)
        self.assertGreater(abs(actual[:, 9:17] - actual[:, 17:25]).max(), 2.)
        off = self.controller(rows, enabled=False)
        np.testing.assert_array_equal(off[:, :9], 0.)
        np.testing.assert_array_equal(off[:, 9:17], off[:, 17:25])
        print('PASS lifecycle: 2 s hold, command exit/reentry, tilt/speed/timing inhibit, RL reset, false exact baseline')

    def test_real_bag_passive_replay_observer_and_torque_bounds(self):
        from rclpy.serialization import deserialize_message
        from rosidl_runtime_py.utilities import get_message
        from analyze_flashsac_drift import nearest
        path = next((REPO / 'docs/exp/2026-10-16/flashsac_60000_223217_076704901_output_true_bag').glob('*.db3'))
        with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
            topics = {i: (n, get_message(t)) for i, n, t in conn.execute('SELECT id,name,type FROM topics')}
            messages = {n: [] for n, _ in topics.values()}
            for tid, stamp, raw in conn.execute('SELECT topic_id,timestamp,data FROM messages ORDER BY timestamp'):
                name, cls = topics[tid]
                messages[name].append((stamp / 1e9, deserialize_message(raw, cls)))
        obs = messages['/sim2real/debug/obs']
        stamps = np.array([t for t, _ in obs])
        aligned, valid = [], np.ones(len(stamps), dtype=bool)
        for name in ['/sim2real/debug/state', '/sim2real/debug/action', '/tita4252763/joint_states',
                     '/tita4252763/imu_sensor_broadcaster/imu']:
            source = messages[name]
            times = np.array([t for t, _ in source])
            indices = nearest(times, stamps)
            valid &= (abs(times[indices] - stamps) <= .008) & np.r_[True, np.diff(indices) > 0]
            aligned.append([source[i][1] for i in indices])
        rows, previous = [], None
        for i in np.flatnonzero(valid):
            state, action, joint, imu = [values[i] for values in aligned]
            dt = .02 if previous is None else stamps[i] - previous
            previous = stamps[i]
            order = [list(joint.name).index(n) for n in NATIVE_JOINTS]
            quat = np.array([imu.orientation.w, imu.orientation.x, imu.orientation.y, imu.orientation.z])
            quat /= np.linalg.norm(quat)
            rows.append([float(state.data == 'rl'), dt, *(np.array(obs[i][1].data)[6:9] / [2, 2, .25]),
                         *np.array(joint.position)[order], *np.array(joint.velocity)[order], *quat,
                         imu.angular_velocity.x, imu.angular_velocity.y, imu.angular_velocity.z, *action.data])
        rows = np.array(rows)
        actual = self.controller(rows)
        expected = self.reference(rows)
        np.testing.assert_allclose(actual[:, :9], expected[:, :9], atol=3e-6, rtol=1e-6)
        np.testing.assert_allclose(actual[:, 9:], expected[:, 9:], atol=1e-4, rtol=1e-5)
        self.assertTrue((abs(actual[:, 9:17]) <= np.array(CFG['robot']['torque_limit']) + 1e-12).all())
        self.assertLessEqual(abs(actual[:, 6]).max(), 2.)
        theoretical_extra = 2. * max(CFG['robot']['joint_kd'][i] for i in (3, 7)) / GEOMETRY['wheel_radius']
        self.assertLessEqual(abs(actual[:, 9:17] - actual[:, 17:25]).max(), theoretical_extra + 1e-12)
        self.assertGreater(abs(actual[:, 9:17] - actual[:, 17:25]).max(), 2.)
        self.assertTrue(actual[:, 1].any())
        self.assertTrue((abs(actual[:, 6]) > 0).any())
        out = ARTIFACTS
        np.savez_compressed(out / 'real_bag_passive_port.npz', samples=rows, cpp=actual, reference=expected)
        print('PASS passive replay:', len(rows), 'samples; sim2sim defaults; +/-2 m/s bias; policy torque limits; no corrected trajectory claim')

    def test_generic_launch_feature_parameters_and_validation(self):
        path = PACKAGE / 'launch/tita.launch.py'
        spec = importlib.util.spec_from_file_location('bias_port_launch', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        params = module.velocity_bias_parameters(PACKAGE / 'policies/flashsac_60000', 1.)
        self.assertEqual(params['velocity_bias_radius'], .0925)
        self.assertEqual(len(params['velocity_bias_xyz']), 24)
        self.assertNotIn('velocity_bias_max_torque', params)
        for sign in (0., float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                module.velocity_bias_parameters(PACKAGE / 'policies/flashsac_60000', sign)


if __name__ == '__main__':
    unittest.main(verbosity=2)
