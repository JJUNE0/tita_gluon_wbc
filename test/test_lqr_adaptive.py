"""DESKTOP_DRY_RUN / VALIDATION_SIM: WIP, residual RLS, gain guards and sensors."""

import copy
import inspect
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
from scipy.spatial.transform import Rotation

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from sim2sim.lqr.controller import ResidualRLS, WheelLQR
from sim2sim.lqr.estimator import Sensors, WheelOdometry
from sim2sim.lqr.model import Description, continuous, discrete, dlqr, residual_matrices
from sim2sim.lqr.runtime import Playback, policy_config
from sim2sim.lqr.evaluate import setup_scene
from sim2sim_ros2_jazzy.checkpoint import read_yaml

CFG = json.loads((REPO / 'sim2sim/lqr/config.json').read_text())
POLICY = policy_config()
SOURCE = read_yaml(next(p for p in POLICY['policy_interface']['sources'] if p.endswith('env.yaml')))
DESCRIPTION = Description(SOURCE['scene']['robot']['spawn']['asset_path'])
STAND = np.asarray(POLICY['robot']['default_joint_angles'])
PARAMETERS = DESCRIPTION.nominal(STAND)


class ModelTests(unittest.TestCase):
    def test_physical_composition(self):
        self.assertAlmostEqual(PARAMETERS['m_b'], 22.67215789)
        self.assertAlmostEqual(PARAMETERS['r'], .0925)
        self.assertAlmostEqual(PARAMETERS['I_w'], .006905)
        self.assertGreater(PARAMETERS['I_b'], 0.)
        self.assertGreater(PARAMETERS['l'], .2)

    def test_dimensions_and_zoh(self):
        Ac, Bc = continuous(PARAMETERS)
        for n in (3, 4):
            A, B = discrete(PARAMETERS, .02, n)
            self.assertEqual(A.shape, (n, n))
            self.assertEqual(B.shape, (n, 1))
            np.testing.assert_allclose(A, expm(Ac[-n:, -n:]*.02))
            reference = solve_ivp(lambda t, x: Ac[-n:, -n:] @ x + Bc[-n:, 0], [0, .02], np.zeros(n), rtol=1e-12, atol=1e-12)
            np.testing.assert_allclose(B[:, 0], reference.y[:, -1], atol=1e-10)

    def test_three_four_consistency(self):
        A4, B4 = discrete(PARAMETERS, .02)
        A3, B3 = discrete(PARAMETERS, .02, 3)
        np.testing.assert_allclose(A3, A4[1:, 1:])
        np.testing.assert_allclose(B3, B4[1:])
        for coefficients in ([0, 0, 0, 0], [.1, -.2, .3, -.4]):
            dA4, dB4 = residual_matrices(coefficients, .02)
            dA3, dB3 = residual_matrices(coefficients, .02, 3)
            np.testing.assert_equal(dA3, dA4[1:, 1:])
            np.testing.assert_equal(dB3, dB4[1:])
            self.assertEqual(dA4[0, 2], .01*coefficients[0])

    def test_motor_reaction_sign(self):
        _, B = continuous(PARAMETERS)
        self.assertGreater(B[1, 0], 0)
        self.assertLess(B[3, 0], 0)

    def test_small_angle_nonlinear_response(self):
        p = PARAMETERS
        mb, mw, iw, ib, l, r, g = [p[k] for k in ('m_b', 'm_w', 'I_w', 'I_b', 'l', 'r', 'g')]
        M, C, J, G = mb+2*mw+2*iw/r**2, mb*l, ib+mb*l*l, mb*g*l
        Ac, Bc = continuous(p)
        def nonlinear(t, x):
            acceleration = np.linalg.solve([[M, C*np.cos(x[2])], [C*np.cos(x[2]), J]],
                [.01/r+C*np.sin(x[2])*x[3]**2, G*np.sin(x[2])-.01])
            return [x[1], acceleration[0], x[3], acceleration[1]]
        initial = [0., 0., .0001, 0.]
        actual = solve_ivp(nonlinear, [0, .05], initial, atol=1e-12, rtol=1e-10).y[:, -1]
        linear = solve_ivp(lambda t, x: Ac @ x + Bc[:, 0]*.01, [0, .05], initial, atol=1e-12, rtol=1e-10).y[:, -1]
        np.testing.assert_allclose(actual, linear, atol=1e-9)

    def test_invalid_parameters(self):
        for key in ('m_b', 'r', 'l', 'I_b'):
            with self.assertRaises(ValueError):
                continuous(dict(PARAMETERS, **{key: -1.}))


class RLSTests(unittest.TestCase):
    def fit(self, coefficients, noise=0., rank_deficient=False):
        rls = ResidualRLS(CFG['controller']['rls'])
        rng = np.random.default_rng(42)
        for _ in range(1200):
            phi = rng.normal(size=2)
            if rank_deficient:
                phi[1] = 2*phi[0]
            rls.update(phi, np.asarray(coefficients).reshape(2, 2) @ phi + rng.normal(scale=noise, size=2))
        return rls

    def test_zero_residual(self):
        rls = self.fit(np.zeros(4))
        np.testing.assert_array_equal(rls.coefficients, np.zeros((2, 2)))

    def test_known_residual_recovery(self):
        expected = [.12, -.03, .4, -.1]
        rls = self.fit(expected)
        np.testing.assert_allclose(rls.coefficients.reshape(4), expected, atol=1e-5)
        self.assertTrue(rls.diagnostics()['confidence'])

    def test_noisy_recovery(self):
        expected = [.12, -.03, .4, -.1]
        np.testing.assert_allclose(self.fit(expected, .005).coefficients.reshape(4), expected, atol=.003)

    def test_insufficient_excitation(self):
        rls = ResidualRLS(CFG['controller']['rls'])
        for _ in range(100):
            rls.update([0., 0.], [0., 0.])
        self.assertFalse(rls.diagnostics()['confidence'])
        self.assertEqual(rls.diagnostics()['rank'], 0)

    def test_rank_deficient(self):
        diag = self.fit([.12, -.03, .4, -.1], rank_deficient=True).diagnostics()
        self.assertFalse(diag['confidence'])
        self.assertEqual(diag['rank'], 1)

    def test_abrupt_change(self):
        rls = self.fit([.1, .02, .2, .03])
        expected = np.array([[-.1, -.02], [.1, -.03]])
        rng = np.random.default_rng(43)
        for _ in range(2000):
            phi = rng.normal(size=2)
            rls.update(phi, expected @ phi)
        np.testing.assert_allclose(rls.coefficients, expected, atol=1e-4)

    def test_bounds_and_invalid_data(self):
        rls = self.fit([5., 1., 5., 1.])
        self.assertGreater(rls.bound_hits, 0)
        self.assertFalse(rls.diagnostics()['confidence'])
        self.assertTrue(np.all(abs(rls.coefficients.reshape(4)) <= CFG['controller']['rls']['bounds']))
        with self.assertRaises(ValueError):
            rls.update([np.nan, 0.], [0., 0.])


class ControllerTests(unittest.TestCase):
    def make(self, dimension=4, **kwargs):
        return WheelLQR(PARAMETERS, .02, dimension, CFG['controller'], **kwargs)

    def test_dare_and_stability(self):
        for n in (3, 4):
            c = self.make(n)
            self.assertLess(max(abs(np.linalg.eigvals(c.A0-c.B0 @ c.K.reshape(1, n)))), 1.)
            x = np.ones(n)*.01
            for _ in range(2000):
                x = (c.A0-c.B0 @ c.K.reshape(1, n)) @ x
            self.assertLess(np.linalg.norm(x), 1e-8)

    def test_torque_slew_and_saturation(self):
        c = self.make()
        previous = 0.
        for _ in range(100):
            u = c.command(np.ones(4)*100)
            self.assertLessEqual(abs(u), 24.)
            self.assertLessEqual(abs(u-previous), 2.4+1e-12)
            previous = u
        self.assertTrue(c.saturated)

    def test_invalid_gain_and_cost_rejection(self):
        with self.assertRaises(ValueError):
            dlqr(np.eye(3), np.zeros((3, 1)), np.eye(3), .1)
        with self.assertRaises(ValueError):
            dlqr(*discrete(PARAMETERS, .02), -np.eye(4), .1)

    def test_cold_start_and_low_excitation_rejection(self):
        fixed, adaptive = self.make(), self.make(adaptive=True)
        np.testing.assert_equal(fixed.K, adaptive.K)
        for _ in range(100):
            adaptive.transition(np.zeros(4), 0., np.zeros(4))
        np.testing.assert_equal(adaptive.K, fixed.K)
        self.assertGreater(adaptive.rejected, 0)

    def test_known_model_update_acceptance_and_shadow(self):
        rng = np.random.default_rng(42)
        for shadow in (False, True):
            c = self.make(adaptive=not shadow, shadow=shadow)
            dA, dB = residual_matrices([-.01, .001, .02, -.002], .02)
            for _ in range(300):
                x = rng.normal(size=4)*.03
                u = rng.normal()*.2
                following = (c.A0+dA) @ x + (c.B0+dB)[:, 0]*u
                c.transition(x, u, following)
            if shadow:
                np.testing.assert_array_equal(c.K, c.K0)
                self.assertEqual(c.reason, 'shadow_valid')
            else:
                self.assertGreater(c.accepted, 0)

    def test_freeze_keeps_gain_and_parameters(self):
        c = self.make(adaptive=True)
        c.frozen = True
        for _ in range(100):
            c.transition(np.ones(4), 2., np.ones(4)*3)
        np.testing.assert_array_equal(c.K, c.K0)
        np.testing.assert_array_equal(c.rls.coefficients, np.zeros((2, 2)))

    def test_rejected_gain_preserves_last_gain(self):
        c = self.make(adaptive=True)
        rng = np.random.default_rng(42)
        with patch('sim2sim.lqr.controller.dlqr', return_value=(c.K0*100., np.ones(4)*.5)):
            for _ in range(100):
                x = rng.normal(size=4)*.03
                u = rng.normal()*.2
                c.transition(x, u, c.A0 @ x+c.B0[:, 0]*u)
        self.assertEqual(c.reason, 'gain_step_limit')
        np.testing.assert_array_equal(c.K, c.K0)


class SensorTests(unittest.TestCase):
    def sample(self, q=None, dq=None, pitch=0., gyro=None):
        quat = Rotation.from_euler('y', pitch).as_quat()[[3, 0, 1, 2]]
        return Sensors(STAND.copy() if q is None else q, np.zeros(8) if dq is None else dq,
                       quat, np.zeros(3) if gyro is None else gyro)

    def test_encoder_sign_and_relative_reset(self):
        e = WheelOdometry(DESCRIPTION, 0.)
        e.observe(self.sample(), .02)
        q = STAND.copy(); q[[3, 7]] += .1
        x = e.observe(self.sample(q), .02)
        self.assertAlmostEqual(x[0], .0925*.1*np.cos(.1), places=5)
        e.reset()
        self.assertEqual(e.observe(self.sample(q), .02)[0], 0.)

    def test_wrapped_encoder(self):
        e = WheelOdometry(DESCRIPTION, 0., wrapped_encoders=True)
        q = STAND.copy(); q[[3, 7]] = np.pi-.02
        e.observe(self.sample(q), .02)
        q[[3, 7]] = -np.pi+.02
        self.assertAlmostEqual(e.observe(self.sample(q), .02)[0], .0925*.04*np.cos(.1), places=5)

    def test_body_and_leg_rotation_compensation(self):
        e = WheelOdometry(DESCRIPTION, 0.)
        dq = np.zeros(8); dq[[2, 6]] = -1/np.cos(.1)
        x = e.observe(self.sample(dq=dq, gyro=np.array([0., 1., 0.])), .02)
        self.assertAlmostEqual(x[1], 0., places=5)

    def test_sensor_noise_delay_and_invalid(self):
        e = WheelOdometry(DESCRIPTION, 0.)
        rng = np.random.default_rng(42)
        previous = self.sample()
        for _ in range(100):
            x = e.observe(previous, .02)
            self.assertTrue(np.isfinite(x).all())
            previous = self.sample(q=STAND+rng.normal(scale=1e-4, size=8), pitch=rng.normal(scale=1e-4))
        with self.assertRaises(ValueError):
            e.observe(self.sample(gyro=np.full(3, np.nan)), .02)

    def test_no_ground_truth_interface(self):
        self.assertEqual(set(Sensors.__dataclass_fields__), {'joint_position', 'joint_velocity', 'imu_quaternion', 'imu_gyro'})
        for word in ('qpos', 'base_pos', 'base_lin_vel', 'data.xpos'):
            self.assertNotIn(word, inspect.getsource(WheelOdometry))

    def test_urdf_fk_and_wheel_rates_against_mujoco(self):
        playback = Playback(POLICY)
        env = playback.env
        try:
            env.data.qvel[3:6] = [0., .3, 0.]
            env.data.qvel[env.qvel_addr] = np.arange(8)*.1
            env.mujoco.mj_forward(env.model, env.data)
            frames, _ = DESCRIPTION.frames(STAND)
            rates = []
            for name in DESCRIPTION.wheel_links:
                body = env.mujoco.mj_name2id(env.model, env.mujoco.mjtObj.mjOBJ_BODY, name)
                np.testing.assert_allclose(env.data.xpos[body]-env.base_pos(), frames[name][:3, 3], atol=1e-5)
                velocity = np.zeros(6)
                env.mujoco.mj_objectVelocity(env.model, env.data, env.mujoco.mjtObj.mjOBJ_BODY, body, velocity, 0)
                rates.append(velocity[1])
            x = WheelOdometry(DESCRIPTION, 0.).observe(Sensors(env.joint_pos(), env.joint_vel(), env.base_quat_sensor(), env.base_ang_vel()), .02)
            self.assertAlmostEqual(x[1], DESCRIPTION.radius*np.mean(rates), places=5)
        finally:
            env.close()

    def test_mismatch_changes_actual_parameters(self):
        for mismatch in CFG['mismatches']:
            playback = Playback(POLICY)
            try:
                applied = setup_scene(playback, mismatch, DESCRIPTION)
                self.assertAlmostEqual(applied['base_mass_kg'], 11.36326789*mismatch.get('mass_scale', 1.))
                if 'friction' in mismatch:
                    self.assertEqual(applied['floor_friction'][0], mismatch['friction'])
                    self.assertEqual(applied['wheel_geom_friction'][0][0], mismatch['friction'])
            finally:
                playback.env.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
