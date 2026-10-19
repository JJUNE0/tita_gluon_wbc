"""VALIDATION_SIM: C++ port against the actual MuJoCo velocity-bias runtime.

The simulated plant follows frozen FlashSAC only; both bias calculations are
passive. This verifies implementation parity, not hardware or correction benefit.
"""
from pathlib import Path
import sys

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(REPO / 'test'), str(REPO / 'test/sim2real')]
from test_velocity_bias_port import VelocityBiasPortTests, CFG, ARTIFACTS
from velocity_bias_campaign import make_runner
from sim2sim_ros2_jazzy.velocity_bias import WheelVelocityBias


def main():
    runner = make_runner(CFG, dict(seed=913))
    VelocityBiasPortTests.setUpClass()
    case = VelocityBiasPortTests()
    try:
        hold = WheelVelocityBias(runner.env)
        radius = hold.radius
        samples, expected = [], []
        for tick in range(500):
            rl = tick < 470
            command = np.array([.1 if 180 <= tick < 220 else 0., 0., 0.])
            hold.update(command if rl else None)
            data = hold.data
            q, dq = runner.env.joint_pos(), runner.env.joint_vel()
            quat = data.sensor('trunk_quat').data.copy()
            gyro = data.sensor('trunk_gyro').data.copy()
            samples.append([rl, .02, *command, *q, *dq, *quat, *gyro, *np.zeros(8)])
            offsets = hold.signs * hold.u / radius if rl else np.zeros(2)
            # C++ clears inactive age/velocity telemetry; Python retains the last sample.
            expected.append([hold.holding, hold.eligible if rl else False,
                             hold.age if hold.holding else 0., hold.velocity if hold.holding else 0.,
                             hold.law.filtered, hold.law.integral, hold.u, *offsets])
            runner.step_bias(0.)
        samples, expected = np.array(samples), np.array(expected)
        actual = case.controller(samples)
        np.testing.assert_allclose(actual[:, :9], expected, atol=1e-4, rtol=1e-5)
        maximum = np.max(abs(actual[:, :9] - expected), axis=0)
        output = ARTIFACTS / 'sim_runtime_parity.npz'
        np.savez_compressed(output, samples=samples, cpp=actual, sim_reference=expected)
        print('VALIDATION_SIM PASS: 500 actual MuJoCo runtime samples, C++ / WheelVelocityBias parity')
        print('Maximum errors by diagnostic column:', maximum)
        print('No robot API, deployment or hardware commands; passive math comparison only')
    finally:
        runner.env.close()
        VelocityBiasPortTests.tearDownClass()


if __name__ == '__main__':
    main()
