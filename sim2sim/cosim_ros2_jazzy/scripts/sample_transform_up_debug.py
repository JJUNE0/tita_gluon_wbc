#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String


class TransformUpSampler(Node):
    def __init__(self, duration: float, idle_wait: float) -> None:
        super().__init__("transform_up_sampler")
        self.duration = duration
        self.idle_wait = idle_wait
        self.key_pub = self.create_publisher(String, "/command/cmd_key", 10)
        self.samples: dict[str, list[np.ndarray]] = {
            "base_rpy": [],
            "base_ang_vel": [],
            "target_wheel_vel": [],
            "wheel_joint_vel": [],
            "wheel_torque": [],
            "progress": [],
        }
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_rpy", self._cb("base_rpy"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_ang_vel", self._cb("base_ang_vel"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/target_wheel_vel_by_joint", self._cb("target_wheel_vel"), 10
        )
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/wheel_joint_vel", self._cb("wheel_joint_vel"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/wheel_torque_cmd", self._cb("wheel_torque"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/transform_up_progress", self._cb("progress"), 10
        )

    def _cb(self, name: str):
        def callback(msg: Float32MultiArray) -> None:
            self.samples[name].append(np.asarray(msg.data, dtype=np.float32))

        return callback

    def publish_key(self, key: str) -> None:
        for _ in range(3):
            self.key_pub.publish(String(data=key))
            rclpy.spin_once(self, timeout_sec=0.05)

    def run(self) -> None:
        end = time.monotonic() + 0.5
        while time.monotonic() < end:
            rclpy.spin_once(self, timeout_sec=0.05)
        self.publish_key("idle")
        end = time.monotonic() + self.idle_wait
        while time.monotonic() < end:
            rclpy.spin_once(self, timeout_sec=0.05)
        for values in self.samples.values():
            values.clear()
        self.publish_key("transform_up")
        end = time.monotonic() + self.duration
        while time.monotonic() < end:
            rclpy.spin_once(self, timeout_sec=0.02)

    def report(self) -> None:
        def stack(name: str) -> np.ndarray:
            values = self.samples[name]
            return np.stack(values) if values else np.empty((0,), dtype=np.float32)

        base_rpy = stack("base_rpy")
        progress = stack("progress")
        target = stack("target_wheel_vel")
        wheel_vel = stack("wheel_joint_vel")
        torque = stack("wheel_torque")
        base_ang_vel = stack("base_ang_vel")

        print("samples:", {k: len(v) for k, v in self.samples.items()})
        if base_rpy.size:
            pitch = base_rpy[:, 1]
            print("final_base_rpy:", base_rpy[-1].tolist())
            print("max_abs_pitch:", float(np.max(np.abs(pitch))))
            print("final_pitch:", float(pitch[-1]))
        if base_ang_vel.size:
            print("final_base_ang_vel:", base_ang_vel[-1].tolist())
        if progress.size:
            print("final_progress:", float(progress[-1, 0]))
        if target.size:
            print("final_target_wheel_vel_by_joint:", target[-1].tolist())
            finite = target[:, [3, 7]]
            print("max_abs_target_wheel_vel:", float(np.nanmax(np.abs(finite))))
        if wheel_vel.size:
            print("final_wheel_joint_vel:", wheel_vel[-1].tolist())
            print("max_abs_wheel_joint_vel:", float(np.max(np.abs(wheel_vel))))
        if torque.size:
            print("final_wheel_torque_cmd:", torque[-1].tolist())
            print("max_abs_wheel_torque_cmd:", float(np.max(np.abs(torque))))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=5.0)
    parser.add_argument("--idle-wait", type=float, default=1.0)
    args = parser.parse_args()

    rclpy.init()
    node = TransformUpSampler(args.duration, args.idle_wait)
    try:
        node.run()
        node.report()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
