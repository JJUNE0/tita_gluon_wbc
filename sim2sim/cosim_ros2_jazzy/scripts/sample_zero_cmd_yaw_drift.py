#!/usr/bin/env python3
"""Zero-command steady-state yaw-drift / wheel-differential sampler.

Reproduces the exact manual-sampling methodology used for the `My21`/`My23`
sim2sim probe entries (`Experiments/RL_Experiments.md`, 2026-07-21): samples
``/joint_states`` and ``/cosim_ros2_jazzy/debug/base_rpy`` over a zero-command
window on an already-running ``mujoco_policy_node`` (in ``rl_0``), reporting
hip (`leg_1`) L/R diff, knee (`leg_3`) L/R diff, wheel (`leg_4`) L/R velocity
diff, and base yaw drift over the window -- directly comparable to the
documented `My21`/`My23` numbers.

Requires the node already in ``rl_0`` with a zero command held (does not
drive the FSM itself -- unlike ``probe_shoulder_oscillation.py``).

Usage:
    source /opt/ros/jazzy/setup.bash && source install/setup.bash
    source ~/venvs/cosim_ros2_jazzy/bin/activate
    python3 cosim_ros2_jazzy/scripts/sample_zero_cmd_yaw_drift.py --duration_s 4.0
"""
import argparse
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float32MultiArray


class YawDriftSampler(Node):
    def __init__(self):
        super().__init__("yaw_drift_sampler")
        self.joint_sub = self.create_subscription(JointState, "/joint_states", self._joint_cb, 10)
        self.rpy_sub = self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/base_rpy", self._rpy_cb, 10
        )
        self.latest_joint = None
        self.latest_rpy = None
        self.samples = []


    def _joint_cb(self, msg: JointState) -> None:
        self.latest_joint = dict(zip(msg.name, msg.position))
        # velocity is co-published in the same JointState message
        self.latest_joint_vel = dict(zip(msg.name, msg.velocity))

    def _rpy_cb(self, msg: Float32MultiArray) -> None:
        self.latest_rpy = list(msg.data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration_s", type=float, default=4.0)
    parser.add_argument("--hz", type=float, default=50.0)
    args = parser.parse_args()

    rclpy.init()
    node = YawDriftSampler()

    print("[INFO] waiting for /joint_states + /cosim_ros2_jazzy/debug/base_rpy...")
    deadline = time.time() + 10.0
    while time.time() < deadline and (node.latest_joint is None or node.latest_rpy is None):
        rclpy.spin_once(node, timeout_sec=0.1)
    if node.latest_joint is None or node.latest_rpy is None:
        raise RuntimeError("Topics not received -- is mujoco_policy_node running in rl_0?")

    period = 1.0 / args.hz
    t0 = time.time()
    while time.time() - t0 < args.duration_s:
        rclpy.spin_once(node, timeout_sec=period)
        if node.latest_joint is None or node.latest_rpy is None:
            continue
        node.samples.append({
            "t": time.time() - t0,
            "hip_l": node.latest_joint.get("joint_left_leg_1"),
            "hip_r": node.latest_joint.get("joint_right_leg_1"),
            "knee_l": node.latest_joint.get("joint_left_leg_3"),
            "knee_r": node.latest_joint.get("joint_right_leg_3"),
            "wheel_l": node.latest_joint_vel.get("joint_left_leg_4"),
            "wheel_r": node.latest_joint_vel.get("joint_right_leg_4"),
            "yaw": node.latest_rpy[2] if len(node.latest_rpy) > 2 else float("nan"),
        })

    samples = node.samples
    n = len(samples)
    if n < 2:
        raise RuntimeError(f"Only {n} samples collected -- topics not publishing fast enough?")

    def avg(key):
        return sum(s[key] for s in samples) / n

    hip_l, hip_r = avg("hip_l"), avg("hip_r")
    knee_l, knee_r = avg("knee_l"), avg("knee_r")
    wheel_l, wheel_r = avg("wheel_l"), avg("wheel_r")
    yaw_start, yaw_end = samples[0]["yaw"], samples[-1]["yaw"]
    dt = samples[-1]["t"] - samples[0]["t"]
    yaw_rate = (yaw_end - yaw_start) / dt if dt > 0 else float("nan")

    print("")
    print("=" * 60)
    print(f"[RESULT] n_samples={n} window={dt:.2f}s")
    print("-" * 60)
    print(f"hip (leg_1)  L={hip_l:.4f}  R={hip_r:.4f}  diff={abs(hip_l - hip_r):.4f}")
    print(f"knee (leg_3) L={knee_l:.4f}  R={knee_r:.4f}  diff={abs(knee_l - knee_r):.4f}")
    print(f"wheel (leg_4, rad/s) L={wheel_l:.4f}  R={wheel_r:.4f}  diff={abs(wheel_l - wheel_r):.4f}")
    print(f"yaw: start={yaw_start:.4f} end={yaw_end:.4f} rate={yaw_rate:+.4f} rad/s")
    print("=" * 60)
    print("Reference (My21, Experiments/RL_Experiments.md): hip diff~0.0076, knee diff~0.089,")
    print("  wheel L/R -0.12/-0.26 (diff~0.14), yaw drift monotonic (not zeroing)")
    print("Reference (My23, ground-truth base_lin_vel): hip diff~0.0067, knee diff~0.058,")
    print("  wheel L/R 0.067/0.007 (diff~0.06), yaw drift ~0.0076 rad/s (still monotonic)")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
