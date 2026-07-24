#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String


class BridgeSampler(Node):
    def __init__(self, transform_duration: float, bridge_duration: float, idle_wait: float) -> None:
        super().__init__("bridge_sampler")
        self.transform_duration = transform_duration
        self.bridge_duration = bridge_duration
        self.idle_wait = idle_wait
        self.key_pub = self.create_publisher(String, "/command/cmd_key", 10)
        self.samples: dict[str, list[np.ndarray | str]] = {
            "state": [],
            "base_rpy": [],
            "base_ang_vel": [],
            "joint_pos_error": [],
            "target_wheel_vel": [],
            "wheel_joint_vel": [],
            "wheel_torque": [],
            "torque": [],
            "transform_progress": [],
            "bridge_progress": [],
        }
        self.create_subscription(String, "/cosim_ros2_jazzy/debug/state", self._state_cb, 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_rpy", self._cb("base_rpy"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_ang_vel", self._cb("base_ang_vel"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_pos_error", self._cb("joint_pos_error"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/target_wheel_vel_by_joint", self._cb("target_wheel_vel"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/wheel_joint_vel", self._cb("wheel_joint_vel"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/wheel_torque_cmd", self._cb("wheel_torque"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/torque_cmd_by_joint", self._cb("torque"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/transform_up_progress", self._cb("transform_progress"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/handoff_bridge_progress", self._cb("bridge_progress"), 10
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

    def spin_for(self, duration: float) -> None:
        end = time.monotonic() + duration
        while time.monotonic() < end:
            rclpy.spin_once(self, timeout_sec=0.02)

    def run(self) -> None:
        self.spin_for(0.5)
        self.publish_key("idle")
        self.spin_for(self.idle_wait)
        for values in self.samples.values():
            values.clear()
        self.publish_key("transform_up")
        self.spin_for(self.transform_duration)
        self.publish_key("bridge_to_policy_stand")
        self.spin_for(self.bridge_duration)

    def report(self) -> None:
        def stack(name: str) -> np.ndarray:
            values = self.samples[name]
            return np.stack(values) if values else np.empty((0,), dtype=np.float32)

        states = self.samples["state"]
        base_rpy = stack("base_rpy")
        base_ang_vel = stack("base_ang_vel")
        joint_pos_error = stack("joint_pos_error")
        target = stack("target_wheel_vel")
        wheel_vel = stack("wheel_joint_vel")
        wheel_torque = stack("wheel_torque")
        torque = stack("torque")
        transform_progress = stack("transform_progress")
        bridge_progress = stack("bridge_progress")

        print("samples:", {k: len(v) for k, v in self.samples.items()})
        if states:
            print("state_sequence:", list(dict.fromkeys(states)))
            print("last_state:", states[-1])
        if base_rpy.size:
            pitch = base_rpy[:, 1]
            print("final_base_rpy:", base_rpy[-1].tolist())
            print("max_abs_pitch:", float(np.max(np.abs(pitch))))
            print("final_pitch:", float(pitch[-1]))
        if base_ang_vel.size:
            print("final_base_ang_vel:", base_ang_vel[-1].tolist())
            print("max_abs_base_ang_vel:", float(np.max(np.abs(base_ang_vel))))
        if transform_progress.size:
            print("final_transform_up_progress:", float(transform_progress[-1, 0]))
        if bridge_progress.size:
            print("final_handoff_bridge_progress:", float(bridge_progress[-1, 0]))
        if joint_pos_error.size:
            leg = joint_pos_error[:, [0, 1, 2, 4, 5, 6]]
            print("final_joint_pos_error:", joint_pos_error[-1].tolist())
            print("max_abs_joint_pos_error_legs:", float(np.max(np.abs(leg))))
        if target.size:
            print("final_target_wheel_vel_by_joint:", target[-1].tolist())
            print("max_abs_target_wheel_vel:", float(np.nanmax(np.abs(target[:, [3, 7]]))))
        if wheel_vel.size:
            print("final_wheel_joint_vel:", wheel_vel[-1].tolist())
            print("max_abs_wheel_joint_vel:", float(np.max(np.abs(wheel_vel))))
        if wheel_torque.size:
            print("final_wheel_torque_cmd:", wheel_torque[-1].tolist())
            print("max_abs_wheel_torque_cmd:", float(np.max(np.abs(wheel_torque))))
        if torque.size:
            print("max_abs_torque_cmd:", float(np.max(np.abs(torque))))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transform-duration", type=float, default=5.0)
    parser.add_argument("--bridge-duration", type=float, default=5.0)
    parser.add_argument("--idle-wait", type=float, default=1.0)
    args = parser.parse_args()

    rclpy.init()
    node = BridgeSampler(args.transform_duration, args.bridge_duration, args.idle_wait)
    try:
        node.run()
        node.report()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
