"""VALIDATION_SIM: actual ROS/MuJoCo loop; auto filter, raw history, reset/reentry.

No hardware node is imported or constructed. Use a previously prepared --ckpt.
"""
import argparse
import json
from pathlib import Path
import sys
from unittest.mock import patch

import numpy as np
import rclpy

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.checkpoint import prepared_config
from sim2sim_ros2_jazzy.sim2sim_node import Sim2SimNode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ckpt', required=True, type=Path)
    args = parser.parse_args()
    config = prepared_config(args.ckpt)
    if config is None:
        raise ValueError('prepare checkpoint first')
    cfg = json.loads(config.read_text())
    rclpy.init(args=['--ros-args', '-p', f'config:={config}', '-p', 'viewer:=false'])
    node = None
    try:
        node = Sim2SimNode()
        expected_mode = cfg['policy_interface']['leg_action_filter']
        assert node.leg_filter.mode == expected_mode
        count, reentries = 0, 0
        for i in range(1100):
            raw_before = node.last_action.copy()
            previous_filter = None if node.leg_filter.previous is None else node.leg_filter.previous.copy()
            captured = []
            applied_calls = []
            build = node.obs_builder.build
            compute = node.action_adapter.compute
            def audited(state):
                obs = build(state)
                captured.append((state, obs.copy()))
                return obs
            def audited_compute(action, positions, velocities):
                applied_calls.append(action.copy())
                return compute(action, positions, velocities)
            with patch.object(node.obs_builder, 'build', side_effect=audited), \
                    patch.object(node.action_adapter, 'compute', side_effect=audited_compute):
                node._step()
            state, obs = captured[0]
            assert obs.shape == (cfg['policy']['obs_dim'],) and np.isfinite(obs).all()
            if node.sm.state == 'rl':
                count += 1
                np.testing.assert_array_equal(obs[25:33], raw_before)
                expected = node.last_action.copy()
                if expected_mode == 'ma2_legs' and previous_filter is not None:
                    expected[node.leg_filter.legs] = .5 * (expected[node.leg_filter.legs]
                        + previous_filter[node.leg_filter.legs])
                np.testing.assert_array_equal(node.leg_filter.previous, node.last_action)
                assert len(applied_calls) == node.env.decimation
                for applied in applied_calls:
                    np.testing.assert_allclose(applied, expected, atol=2e-7, rtol=1e-6)
                if cfg['policy']['obs_dim'] == 34 and (i == 1000 or count == 1):
                    assert abs(obs[-1]) < 1e-7
                if i == 999:
                    # Exercise RL exit/reentry from sit, retaining the physical state.
                    node.sm.request('sit', node.env.joint_pos())
                    node._step()
                    assert node.sm.request('rl', node.env.joint_pos())
                    node.obs_builder.reference = 1000.
                    reentries += 1
        assert count > 100, count
        node._cmd_key_cb(type('Message', (), {'data': 'reset'})())
        node._step()
        assert node.sm.state != 'rl'
        np.testing.assert_array_equal(node.last_action, np.zeros(8))
        assert node.leg_filter.previous is None
        print(f'[VALIDATION_SIM] PASS: {cfg["policy"]["obs_dim"]} obs, auto={expected_mode}, '
            f'1100 steps, {count} RL inferences, {reentries} relatch checks, reset clears raw/filter state')
    finally:
        if node:
            node.env.close()
            node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
