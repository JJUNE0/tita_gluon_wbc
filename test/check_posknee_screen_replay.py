"""VALIDATION_SIM: compare screening signals with the actual public ROS/MuJoCo node."""
import argparse
import json
from pathlib import Path
from unittest.mock import patch

import numpy as np
import rclpy

import evaluate_posknee_checkpoints as screen
from sim2sim_ros2_jazzy.sim2sim_node import Sim2SimNode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    reference = np.load(out/'smoke/signals/model_75000_k1_stand_s42.npz')
    config = screen.prepared_config(screen.RUN/'model_75000')
    rclpy.init(args=['--ros-args', '-p', f'config:={config}', '-p', 'viewer:=false'])
    node = None
    errors = dict(q=0., raw_action=0., applied_action=0., torque=0.)
    try:
        node = Sim2SimNode()
        env = node.env
        floor = env.model.geom('floor').id
        obstacles = np.flatnonzero((env.model.geom_bodyid == 0) & (np.arange(env.model.ngeom) != floor))
        env.model.geom_contype[obstacles] = env.model.geom_conaffinity[obstacles] = 0
        rng = np.random.default_rng(42)
        env.data.qvel[0] = rng.uniform(-.015, .015)
        env.data.qvel[env.qvel_addr[screen.LEGS]] = rng.normal(0, .01, 6)
        env.mujoco.mj_forward(env.model, env.data)
        index = 0
        compute, build, update = node.action_adapter.compute, node.obs_builder.build, node.leg_filter.update
        for _ in range(1900):
            captured, torques, applied = [], [], []
            def capture_build(state):
                if node.sm.state == 'rl':
                    captured.append(state.joint_pos.copy())
                return build(state)
            def capture_compute(action, q, dq):
                tau = compute(action, q, dq)
                torques.append(tau.copy())
                return tau
            def capture_filter(action):
                value = update(action)
                applied.append(value.copy())
                return value
            with patch.object(node.obs_builder, 'build', side_effect=capture_build), \
                    patch.object(node.action_adapter, 'compute', side_effect=capture_compute), \
                    patch.object(node.leg_filter, 'update', side_effect=capture_filter):
                node._step()
            if captured:
                actual = dict(q=captured[0], raw_action=node.last_action,
                    applied_action=applied[0], torque=np.array(torques))
                for key, values in actual.items():
                    difference = float(np.max(np.abs(reference[key][index]-values)))
                    errors[key] = max(errors[key], difference)
                index += 1
                if index == len(reference['t']):
                    break
        assert index == 1600, index
        assert max(errors.values()) < 1e-6, errors
        print('[VALIDATION_SIM] PASS: 1600 RL ticks match public sim2sim node; max errors:',json.dumps(errors))
    finally:
        if node:
            node.env.close();node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
