"""VALIDATION_SIM: compare the real launch node with the isolated A path."""

import json
from pathlib import Path
import sys
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from sim2sim.lqr.runtime import Playback, policy_config
from sim2sim_ros2_jazzy.sim2sim_node import Sim2SimNode
import rclpy


def main():
    cfg = policy_config()
    config = Path(cfg['policy']['path']).with_name('config.json')
    rclpy.init(args=['--ros-args', '-p', f'config:={config}', '-p', 'viewer:=false'])
    node = Sim2SimNode()
    playback = Playback(cfg)
    errors = dict(observation=0., action=0., torque=0., qpos=0., qvel=0.)
    try:
        for command in ([0., 0., 0.], [.1, 0., 0.], [0., 0., 0.]):
            node.command[:] = command
            for _ in range(100):
                obs, action = playback.infer(node.command)
                captured = {}
                original_build = node.obs_builder.build
                def build(state):
                    result = original_build(state)
                    captured['obs'] = result
                    return result
                node.obs_builder.build = build
                node._step()
                node.obs_builder.build = original_build
                playback.step(action)
                actual = dict(observation=captured['obs'], action=node.last_action,
                              torque=node.env.data.ctrl, qpos=node.env.data.qpos, qvel=node.env.data.qvel)
                expected = dict(observation=obs, action=action, torque=playback.env.data.ctrl,
                                qpos=playback.env.data.qpos, qvel=playback.env.data.qvel)
                for key in errors:
                    error = float(np.max(np.abs(actual[key] - expected[key])))
                    errors[key] = max(errors[key], error)
                    np.testing.assert_allclose(actual[key], expected[key], atol=1e-7, rtol=1e-7)
        result = dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
                      checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
                      onnx_sha256=cfg['policy_interface']['onnx_sha256'],
                      steps=300, commands=['zero', 'forward 0.1 m/s', 'zero'], max_abs_errors=errors)
        (REPO / 'docs/exp/2026-10-14/lqr_ablation/baseline_gate.json').write_text(json.dumps(result, indent=2))
        print(json.dumps(result))
    finally:
        playback.env.close()
        node.env.close()
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
