"""DESKTOP_DRY_RUN: timing, correction bounds, anti-windup and inhibition.

Runs only a pure-math C++ fixture. Recorded-state replay is not a corrected
hardware trajectory. The real-robot law intentionally differs from sim2sim.
"""
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from scipy.spatial.transform import Rotation

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO/'sim2real/tita_ws/src/tita_controller'
CFG = json.loads((PACKAGE/'policies/flashsac_60000/config.json').read_text())
GEO = json.loads((PACKAGE/'config/velocity_bias_geometry.json').read_text())
OUT = REPO/'docs/exp/2026-10-17/velocity_bias_08nm_deployment'


def header(kd=None, sign=1.):
    kd = CFG['robot']['joint_kd'] if kd is None else kd
    native = [f'joint_{side}_leg_{i}' for side in ('left', 'right') for i in range(1, 5)]
    terms = []
    for a in CFG['policy_interface']['actions']:
        terms.extend([native.index(a['joint']), int(a['kind'] == 'velocity'),
                      a['scale'], a['offset'], *(a['clip'] or [-1e9, 1e9])])
    return [*GEO['xyz'], *GEO['rpy'], *GEO['axis'], GEO['wheel_radius'], sign,
            *CFG['robot']['joint_kp'], *kd, *CFG['robot']['torque_limit'], *terms]


class BoundedBiasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        OUT.mkdir(parents=True, exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(dir=REPO/'test/sim2real', prefix='bound08_')
        cls.binary = Path(cls.temp.name)/'runtime'
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
                        '-isystem', '/usr/include/eigen3', '-I', str(PACKAGE/'include'),
                        str(REPO/'test/sim2real/velocity_bias_runtime.cpp'), '-o', str(cls.binary)], check=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def run_rows(self, rows, mode='status', kd=None, sign=1.):
        stream = io.StringIO()
        np.savetxt(stream, np.array(header(kd, sign))[None], fmt='%.17g')
        np.savetxt(stream, rows, fmt='%.17g')
        run = subprocess.run([str(self.binary), mode], input=stream.getvalue(), text=True, capture_output=True, check=True)
        return np.loadtxt(io.StringIO(run.stdout), ndmin=2)

    @staticmethod
    def rows(n=600):
        rows = np.zeros((n, 36))
        rows[:, :2] = [1., .02]
        rows[:, 5:13] = CFG['robot']['default_joint_angles']
        rows[:, [16, 20]] = -2.  # Native wheel encoder rad/s.
        rows[:, 21] = 1.
        return rows

    def assert_bounds(self, actual):
        np.testing.assert_allclose(actual[:, 9:17][:, [0, 1, 2, 4, 5, 6]],
                                   actual[:, 17:25][:, [0, 1, 2, 4, 5, 6]], atol=0, rtol=0)
        self.assertLessEqual(float(abs(actual[:, 9:17]-actual[:, 17:25]).max()), .8+1e-10)
        self.assertTrue((abs(actual[:, 9:17]) <= np.array(CFG['robot']['torque_limit'])+1e-10).all())

    def test_acquisition_excludes_first_second_zero_seed_ramp_both_signs(self):
        rows = self.rows()
        rows[:50, [16, 20]] = 8.
        for sign in (1., -1.):
            actual = self.run_rows(rows, sign=sign)
            self.assertFalse(actual[:150, 1].any())
            self.assertTrue(actual[150, 1])
            np.testing.assert_array_equal(actual[:151, 6], 0.)
            np.testing.assert_allclose(actual[150:, 27], -.185, atol=1e-6)
            self.assertEqual(actual[150, 5], 0.)
            self.assertGreater(sign*-actual[210, 6], 0.)
            np.testing.assert_allclose(actual[:, 5], actual[:, 6], atol=1e-8)
            delta = (actual[:, 9:17]-actual[:, 17:25])[:, [3, 7]]
            self.assertLessEqual(abs(np.diff(delta, axis=0)).max(), .8*.02+1e-8)
            np.testing.assert_allclose(abs(delta[210:]).max(axis=0), .8, atol=1e-8)
            self.assert_bounds(actual)

    def test_no_windup_and_reversal_after_long_saturation(self):
        rows = self.rows(1200)
        rows[800:, [16, 20]] = 2.
        actual = self.run_rows(rows)
        self.assertLess(actual[799, 6], 0.)
        self.assertGreater(actual[875, 6], 0.)
        np.testing.assert_allclose(actual[:, 5], actual[:, 6], atol=1e-8)
        self.assert_bounds(actual)

    def test_pitch_cutoff_latches_and_command_reentry_reacquires(self):
        rows = self.rows(650)
        rows[250:270, 21:25] = Rotation.from_euler('y', 6, degrees=True).as_quat()[[3, 0, 1, 2]]
        rows[310:320, 2] = .1
        rows[560, 1] = .08
        actual = self.run_rows(rows)
        self.assertTrue(actual[250, 26])
        np.testing.assert_array_equal(actual[250:471, 6], 0.)
        self.assertTrue(actual[470, 1])
        self.assertLess(actual[520, 6], 0.)
        np.testing.assert_array_equal(actual[560:, 6], 0.)
        self.assert_bounds(actual)

    def test_command_and_rl_exit_cut_immediately_and_off_is_exact_baseline(self):
        rows = self.rows()
        rows[250:260, 2] = .1
        rows[500:, 0] = 0.
        actual = self.run_rows(rows)
        np.testing.assert_array_equal(actual[250:411, 6], 0.)
        self.assertLess(actual[450, 6], 0.)
        np.testing.assert_array_equal(actual[500:, :9], 0.)
        off = self.run_rows(rows, mode='off')
        np.testing.assert_array_equal(off[:, :9], 0.)
        np.testing.assert_array_equal(off[:, 9:17], off[:, 17:25])

    def test_asymmetric_kd_and_effort_clipping_preserve_actual_delta_cap(self):
        rows = self.rows()
        kd = list(CFG['robot']['joint_kd'])
        kd[3], kd[7] = .3, 1.2
        actual = self.run_rows(rows, kd=kd)
        delta = actual[:, 9:17]-actual[:, 17:25]
        np.testing.assert_allclose(abs(delta[210:, [3, 7]]).max(axis=0), [.2, .8], atol=1e-8)
        rows[250:350, [31, 35]] = 10.
        rows[350:450, [31, 35]] = -10.
        self.assert_bounds(self.run_rows(rows, kd=kd))

    def test_unsafe_acquisition_latches_without_applying(self):
        rows = self.rows()
        rows[90:100, 21:25] = Rotation.from_euler('x', 20, degrees=True).as_quat()[[3, 0, 1, 2]]
        actual = self.run_rows(rows)
        self.assertTrue(actual[90:, 26].all())
        np.testing.assert_array_equal(actual[:, 6], 0.)

    def test_recorded_runs_passive_bounds_only(self):
        source = REPO/'docs/exp/2026-10-17/flashsac_three_case_bias_diagnosis'
        metrics = {}
        for name in ('free', 'hand', 'joystick', 'bias_on'):
            d = np.load(source/f'{name}_signals.npz')
            dt = d['dt'].copy()
            dt[np.flatnonzero(d['rl'])[0]] = .02
            rows = np.c_[d['rl'], dt, d['command'], d['q'], d['dq'], d['quat'], d['gyro'], d['action']]
            actual = self.run_rows(rows)
            self.assert_bounds(actual)
            self.assertFalse(actual[(d['t'] < 3.) & d['rl'], 1].any())
            metrics[name] = dict(samples=len(rows), max_added_nm=float(abs(actual[:, 9:17]-actual[:, 17:25]).max()),
                                 eligible=int(actual[:, 1].sum()), inhibited=int(actual[:, 26].sum()))
            np.savez_compressed(OUT/f'{name}_bounded_replay.npz', rows=rows, result=actual)
            if name == 'free':
                stream = io.StringIO()
                np.savetxt(stream, np.array(header())[None], fmt='%.17g')
                np.savetxt(stream, rows, fmt='%.17g')
                (OUT/'arm_replay_input.txt').write_text(stream.getvalue())
                np.savetxt(OUT/'arm_replay_expected.txt', actual, fmt='%.17g')
        (OUT/'passive_replay.json').write_text(json.dumps(metrics, indent=2)+'\n')


if __name__ == '__main__':
    if '--compare-arm' in sys.argv:
        expected = np.loadtxt(OUT/'arm_replay_expected.txt', ndmin=2)
        actual = np.loadtxt(OUT/'arm_replay_actual.txt', ndmin=2)
        np.testing.assert_allclose(actual, expected, atol=1e-5, rtol=1e-5)
        assert abs(actual[:, 9:17]-actual[:, 17:25]).max() <= .8+1e-10
        result = dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
                      samples=len(actual), columns=actual.shape[1],
                      max_column_errors=abs(actual-expected).max(axis=0).tolist(),
                      max_added_nm=float(abs(actual[:, 9:17]-actual[:, 17:25]).max()),
                      note='ARM/x86 pure math only; no robot control or physical motion validation.')
        (OUT/'arm_comparison.json').write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps(result, indent=2))
    else:
        unittest.main(verbosity=2)
