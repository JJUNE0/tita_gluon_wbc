#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
import rclpy
import yaml
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String


class ReferenceTransformUpSampler(Node):
    def __init__(self, config_path: Path, duration: float) -> None:
        super().__init__("reference_transform_up_sampler")
        self.duration = duration
        with open(config_path, "r", encoding="utf-8") as f:
            self.cfg = yaml.safe_load(f)
        self.stand_jpos = np.asarray(self.cfg["reference_transform_up"]["stand_jpos"], dtype=np.float32)
        self.key_pub = self.create_publisher(String, "/command/cmd_key", 10)
        self.samples: dict[str, list[np.ndarray | str]] = {
            "state": [],
            "progress": [],
            "base_rpy": [],
            "joint_pos": [],
            "wheel_joint_vel": [],
            "wheel_torque": [],
            "torque_clip": [],
        }
        self.create_subscription(String, "/cosim_ros2_jazzy/debug/state", self._state_cb, 10)
        self.create_subscription(
            Float32MultiArray,
            "/cosim_ros2_jazzy/debug/reference_transform_up_progress",
            self._cb("progress"),
            10,
        )
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_rpy", self._cb("base_rpy"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_pos", self._cb("joint_pos"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/wheel_joint_vel", self._cb("wheel_joint_vel"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/wheel_torque_cmd", self._cb("wheel_torque"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/torque_clip_by_joint", self._cb("torque_clip"), 10
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
        self.publish_key("idle")
        self.publish_key("reference_transform_up")
        end = time.monotonic() + self.duration
        while time.monotonic() < end:
            rclpy.spin_once(self, timeout_sec=0.02)

    def report(self) -> None:
        def stack(name: str) -> np.ndarray:
            values = self.samples[name]
            return np.stack(values) if values else np.empty((0,), dtype=np.float32)

        states = self.samples["state"]
        progress = stack("progress")
        base_rpy = stack("base_rpy")
        joint_pos = stack("joint_pos")
        wheel_vel = stack("wheel_joint_vel")
        wheel_torque = stack("wheel_torque")
        torque_clip = stack("torque_clip")

        print("samples:", {k: len(v) for k, v in self.samples.items()})
        if states:
            print("state_sequence:", list(dict.fromkeys(states)))
            print("last_state:", states[-1])
        if progress.size:
            print("final_reference_transform_up_progress:", float(progress[-1][0]))
        if base_rpy.size:
            pitch = base_rpy[:, 1]
            print("initial_base_rpy:", base_rpy[0].tolist())
            print("final_base_rpy:", base_rpy[-1].tolist())
            print("max_abs_pitch:", float(np.max(np.abs(pitch))))
            print("final_pitch:", float(pitch[-1]))
        if joint_pos.size:
            final_joint_pos = joint_pos[-1]
            final_error = final_joint_pos - self.stand_jpos
            print("final_joint_pos:", final_joint_pos.tolist())
            print("final_joint_pos_error_vs_stand_jpos:", final_error.tolist())
            print("max_abs_joint_pos_error_vs_stand_jpos:", float(np.max(np.abs(final_error))))
        if wheel_vel.size:
            print("final_wheel_joint_vel:", wheel_vel[-1].tolist())
            print("max_abs_wheel_joint_vel:", float(np.max(np.abs(wheel_vel))))
        if wheel_torque.size:
            print("final_wheel_torque_cmd:", wheel_torque[-1].tolist())
            print("max_abs_wheel_torque_cmd:", float(np.max(np.abs(wheel_torque))))
        if torque_clip.size:
            print("max_abs_torque_clip_by_joint:", np.max(np.abs(torque_clip), axis=0).tolist())
            print("any_torque_clipping:", bool(np.max(np.abs(torque_clip)) > 1e-6))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="cosim_ros2_jazzy/config/tita.yaml",
        help="Path to the active YAML config.",
    )
    parser.add_argument("--duration", type=float, default=6.0)
    args = parser.parse_args()

    rclpy.init()
    node = ReferenceTransformUpSampler(Path(args.config), args.duration)
    try:
        node.run()
        node.report()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
