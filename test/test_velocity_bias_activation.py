"""VALIDATION_SIM: timing observer parity and inhibition on an actual RL sensor stream."""

import unittest

import numpy as np

from compare_velocity_bias_activation import experiment, MAIN, TimedWheelVelocityBias
from sim2sim_ros2_jazzy.velocity_bias import WheelVelocityBias


class ActivationTests(unittest.TestCase):
    def test_research_observer_matches_production_at_2_seconds(self):
        e = experiment(dict(checkpoint_id=MAIN, seed=913, physics={}, delay_s=None))
        self.addCleanup(e.env.close)
        original = WheelVelocityBias(e.env)
        timed = TimedWheelVelocityBias(e.env, 2.)
        for _ in range(250):
            original.update(np.zeros(3))
            timed.update(np.zeros(3))
            self.assertEqual(original.u, timed.u)
            self.assertEqual(original.eligible, timed.eligible)
            self.assertEqual(original.velocity, timed.velocity)
            self.assertEqual(original.position, timed.position)
            e.step()
        print('[VALIDATION_SIM] production and research 2 s observer/control parity: exact')

    def test_default_runtime_reproduces_selected_nominal_300s_trace(self):
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        recorded = root / 'docs/exp/2026-10-17/velocity_bias_activation_timing/long300'
        path = recorded / f'{MAIN}_nominal_s913_delay2_300s/trace.npz'
        expected = np.load(path)['state']
        self.assertEqual(len(expected), 15001)
        e = experiment(dict(checkpoint_id=MAIN, seed=913, physics={}, delay_s=None))
        self.addCleanup(e.env.close)
        e.velocity = WheelVelocityBias(e.env)  # Actual production default, no research override.
        states = []
        for tick in range(len(expected)):
            o = e.runner.observation
            states.append(np.r_[o['base_position'], o['base_velocity'], o['rpy'], o['sensor'][:2],
                                o['fk_sensor'], e.env.data.qpos[2]])
            if tick < len(expected) - 1:
                step = e.step()
                if tick < 100:
                    np.testing.assert_array_equal(step['motor'], step['baseline_motor'])
        np.testing.assert_array_equal(np.asarray(states), expected)
        print('[VALIDATION_SIM] production default2 / selected nominal300s: full state trace exact')

    def test_two_seconds_from_rl_entry_not_two_additional_seconds(self):
        e = experiment(dict(checkpoint_id=MAIN, seed=913, physics={}, delay_s=2.))
        self.addCleanup(e.env.close)
        first = None
        for tick in range(160):
            step = e.step()
            if tick < 100:
                self.assertEqual(step['bias'], 0.)
                self.assertFalse(e.velocity.law.seeded)
                np.testing.assert_array_equal(step['motor'], step['baseline_motor'])
            if e.velocity.eligible and first is None:
                first = tick * e.dt
        self.assertEqual(first, 2.)
        self.assertNotEqual(e.velocity.u, 0.)
        print('[VALIDATION_SIM] delay2: first eligible at RL+2.00 s, not RL+3.20 s')


if __name__ == '__main__':
    unittest.main()
