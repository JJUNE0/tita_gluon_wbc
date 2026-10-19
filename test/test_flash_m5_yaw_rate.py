"""DESKTOP_DRY_RUN: independent yaw kinematics and constrained-fit checks."""

import unittest

import numpy as np
from scipy.spatial.transform import Rotation

from eval_flash_m5_yaw_rate import imu_yaw_rate
from analyze_flash_m5_yaw_rate import fit_model
from analyze_flash_state_learning import predict


class M5Checks(unittest.TestCase):
    def test_heading_derivative_from_body_gyro(self):
        rng = np.random.default_rng(519)
        for _ in range(50):
            rpy = rng.uniform([-.4,-.4,-2.5],[.4,.4,2.5])
            gyro = rng.normal(0,.2,3)
            current = Rotation.from_euler('xyz',rpy)
            next_rpy = (current*Rotation.from_rotvec(gyro*1e-7)).as_euler('xyz')
            self.assertAlmostEqual(imu_yaw_rate(rpy,gyro),(next_rpy[2]-rpy[2])/1e-7,places=7)
            shifted = rpy.copy(); shifted[2] += .8
            self.assertEqual(imu_yaw_rate(rpy,gyro),imu_yaw_rate(shifted,gyro))
        self.assertNotAlmostEqual(imu_yaw_rate([.3,.2,1.],[.1,.2,.3]),.3,places=4)

    def test_M5_causal_rows_and_translation(self):
        rng = np.random.default_rng(2029)
        A = rng.normal(0,.025,(25,25))+np.eye(25)*.5
        A[:,0] = 0.; A[0,0] = 1.
        B = rng.normal(0,.01,25); B[5:13] = 0.
        x = rng.normal(size=(3000,25)); u = rng.normal(size=3000)
        y = x@A.T+u[:,None]*B
        model = fit_model(x,y,u,'M5')
        np.testing.assert_allclose(model['A'],A,atol=5e-15,rtol=1e-12)
        np.testing.assert_allclose(model['B'],B,atol=5e-15,rtol=1e-12)
        self.assertEqual(model['action_B_zero_rows'],list(range(5,13)))
        self.assertGreater(abs(model['B'][4]),1e-5)  # yaw rate must not be mistaken for an action

    def test_M4_excludes_only_yaw_rate(self):
        rng = np.random.default_rng(2030)
        indices = [0,1,2,3]+list(range(5,25))
        A = rng.normal(0,.02,(24,24))+np.eye(24)*.6
        A[:,0] = 0.; A[0,0] = 1.
        B = rng.normal(0,.01,24);B[4:12] = 0.
        x = rng.normal(size=(2000,25));u = rng.normal(size=2000)
        y = rng.normal(size=(2000,25));y[:,indices] = x[:,indices]@A.T+u[:,None]*B
        model = fit_model(x,y,u,'M4')
        np.testing.assert_allclose(model['A'],A,atol=5e-15,rtol=1e-12)
        np.testing.assert_allclose(model['B'],B,atol=5e-15,rtol=1e-12)

    def test_recursive_yaw_state_has_no_future_measurement(self):
        A = np.array([[1.,.02,0.],[0.,.8,.1],[0.,0.,.7]])
        B = np.array([0.,.02,.03])
        u = np.array([[.1,0.,0.,0.]])
        prediction = predict(A,B,np.zeros((1,3)),u)[0]
        expected = np.zeros(3)
        for i in range(4):
            expected = A@expected+B*u[0,i]
            np.testing.assert_allclose(prediction[i+1],expected,atol=1e-18)


if __name__=='__main__':
    unittest.main(verbosity=2)
