#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String


class PoseHoldSampler(Node):
    def __init__(self, duration: float) -> None:
        super().__init__("pose_hold_sampler")
        self.duration = duration
        self.key_pub = self.create_publisher(String, "/command/cmd_key", 10)
        self.samples: dict[str, list[np.ndarray | str]] = {
            "state": [],
            "base_rpy": [],
            "joint_pos_error": [],
            "wheel_joint_vel": [],
            "wheel_torque": [],
        }
        self.create_subscription(String, "/cosim_ros2_jazzy/debug/state", self._state_cb, 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_rpy", self._cb("base_rpy"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_pos_error", self._cb("joint_pos_error"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/wheel_joint_vel", self._cb("wheel_joint_vel"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/wheel_torque_cmd", self._cb("wheel_torque"), 10
        )

    def _cb(self, name: str):
        def callback(msg: Float32MultiArray) -> None:
            self.samples[name].append(np.asarray(msg.data, dtype=np.float32))

        return callback

    def _state_cb(self, msg: String) -> None:
        self.samples["state"].append(msg.data)

    def publish_key(self, key: str) -> None:
        for _ in range(3):
            self.key_pub.publish(String(data=key))
            rclpy.spin_once(self, timeout_sec=0.05)

    def run(self) -> None:
        end = time.monotonic() + 0.5
        while time.monotonic() < end:
            rclpy.spin_once(self, timeout_sec=0.05)
        for values in self.samples.values():
            values.clear()
        self.publish_key("pose_hold_test")
        end = time.monotonic() + self.duration
        while time.monotonic() < end:
            rclpy.spin_once(self, timeout_sec=0.02)

    def report(self) -> None:
        def stack(name: str) -> np.ndarray:
            values = self.samples[name]
            return np.stack(values) if values else np.empty((0,), dtype=np.float32)

        states = self.samples["state"]
        base_rpy = stack("base_rpy")
        joint_pos_error = stack("joint_pos_error")
        wheel_vel = stack("wheel_joint_vel")
        wheel_torque = stack("wheel_torque")

        print("samples:", {k: len(v) for k, v in self.samples.items()})
        if states:
            print("state_sequence:", list(dict.fromkeys(states)))
            print("last_state:", states[-1])
        if base_rpy.size:
            pitch = base_rpy[:, 1]
            print("initial_base_rpy:", base_rpy[0].tolist())
            print("final_base_rpy:", base_rpy[-1].tolist())
            print("max_abs_pitch:", float(np.max(np.abs(pitch))))
            print("final_pitch:", float(pitch[-1]))
        if joint_pos_error.size:
            leg = joint_pos_error[:, [0, 1, 2, 4, 5, 6]]
            print("initial_joint_pos_error:", joint_pos_error[0].tolist())
            print("final_joint_pos_error:", joint_pos_error[-1].tolist())
            print("max_abs_joint_pos_error_legs:", float(np.max(np.abs(leg))))
        if wheel_vel.size:
            print("final_wheel_joint_vel:", wheel_vel[-1].tolist())
            print("max_abs_wheel_joint_vel:", float(np.max(np.abs(wheel_vel))))
        if wheel_torque.size:
            print("final_wheel_torque_cmd:", wheel_torque[-1].tolist())
            print("max_abs_wheel_torque_cmd:", float(np.max(np.abs(wheel_torque))))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=5.0)
    args = parser.parse_args()

    rclpy.init()
    node = PoseHoldSampler(args.duration)
    try:
        node.run()
        node.report()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
