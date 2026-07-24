#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String


class Rl0HandoffSampler(Node):
    def __init__(
        self,
        startup_mode: str,
        target_state: str,
        transform_duration: float,
        bridge_duration: float,
        rl_duration: float,
        idle_wait: float,
        output_prefix: str | None,
    ) -> None:
        super().__init__("rl0_handoff_sampler")
        self.startup_mode = startup_mode
        self.target_state = target_state
        self.transform_duration = transform_duration
        self.bridge_duration = bridge_duration
        self.rl_duration = rl_duration
        self.idle_wait = idle_wait
        self.output_prefix = output_prefix
        self.key_pub = self.create_publisher(String, "/command/cmd_key", 10)
        self.twist_pub = self.create_publisher(Twist, "/command/cmd_twist", 10)
        self.samples: dict[str, list[np.ndarray | str]] = {
            "state": [],
            "base_rpy": [],
            "base_ang_vel": [],
            "action_raw": [],
            "action_scaled": [],
            "target_wheel_vel": [],
            "wheel_joint_vel": [],
            "wheel_torque": [],
            "torque": [],
            "torque_clip": [],
            "joint_pos_error": [],
            "transform_progress": [],
            "reference_transform_progress": [],
            "bridge_progress": [],
        }
        self.create_subscription(String, "/cosim_ros2_jazzy/debug/state", self._state_cb, 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_rpy", self._cb("base_rpy"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_ang_vel", self._cb("base_ang_vel"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/action_raw_by_joint", self._cb("action_raw"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/action_scaled_by_joint", self._cb("action_scaled"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/target_wheel_vel_by_joint", self._cb("target_wheel_vel"), 10
        )
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/wheel_joint_vel", self._cb("wheel_joint_vel"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/wheel_torque_cmd", self._cb("wheel_torque"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/torque_cmd_by_joint", self._cb("torque"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/torque_clip_by_joint", self._cb("torque_clip"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_pos_error", self._cb("joint_pos_error"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/transform_up_progress", self._cb("transform_progress"), 10
        )
        self.create_subscription(
            Float32MultiArray,
            "/cosim_ros2_jazzy/debug/reference_transform_up_progress",
            self._cb("reference_transform_progress"),
            10,
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/handoff_bridge_progress", self._cb("bridge_progress"), 10
        )
        self.current_state = ""

    def _cb(self, name: str):
        def callback(msg: Float32MultiArray) -> None:
            self.samples[name].append(np.asarray(msg.data, dtype=np.float32))

        return callback

    def _state_cb(self, msg: String) -> None:
        self.samples["state"].append(msg.data)
        self.current_state = msg.data

    def publish_key(self, key: str) -> None:
        for _ in range(3):
            self.key_pub.publish(String(data=key))
            rclpy.spin_once(self, timeout_sec=0.05)

    def publish_zero_twist(self) -> None:
        self.twist_pub.publish(Twist())

    def spin_for(self, duration: float, publish_zero: bool = False) -> None:
        end = time.monotonic() + duration
        next_twist = 0.0
        while time.monotonic() < end:
            now = time.monotonic()
            if publish_zero and now >= next_twist:
                self.publish_zero_twist()
                next_twist = now + 0.1
            rclpy.spin_once(self, timeout_sec=0.02)

    def clear_samples(self) -> None:
        for values in self.samples.values():
            values.clear()

    def wait_for_state(self, expected: str, timeout: float) -> bool:
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            if self.current_state == expected:
                return True
            self.publish_zero_twist()
            rclpy.spin_once(self, timeout_sec=0.02)
        return False

    def run(self) -> None:
        self.spin_for(0.5)
        self.publish_key("idle")
        self.spin_for(self.idle_wait)
        if self.startup_mode == "reference":
            self.publish_key("reference_transform_up")
            if not self.wait_for_state("reference_stand_hold", self.transform_duration):
                raise RuntimeError("Timed out waiting for reference_stand_hold")
            # Settle wait: flush stale ROS2 queue messages and let robot stabilize.
            self.spin_for(self.bridge_duration)
        else:
            self.publish_key("transform_up")
            if not self.wait_for_state("hold_default", self.transform_duration):
                self.spin_for(self.transform_duration)
            self.publish_key("bridge_to_policy_stand")
            if not self.wait_for_state("hold_default", self.bridge_duration):
                self.spin_for(self.bridge_duration)
        self.publish_zero_twist()
        self.clear_samples()
        self.publish_key(self.target_state)
        self.spin_for(self.rl_duration, publish_zero=True)

    def build_summary(self) -> tuple[dict, dict[str, np.ndarray]]:
        def stack(name: str) -> np.ndarray:
            values = self.samples[name]
            return np.stack(values) if values else np.empty((0,), dtype=np.float32)

        base_rpy = stack("base_rpy")
        base_ang_vel = stack("base_ang_vel")
        action = stack("action_raw")
        action_scaled = stack("action_scaled")
        target = stack("target_wheel_vel")
        wheel_vel = stack("wheel_joint_vel")
        wheel_torque = stack("wheel_torque")
        torque = stack("torque")
        torque_clip = stack("torque_clip")
        joint_pos_error = stack("joint_pos_error")
        transform_progress = stack("transform_progress")
        reference_transform_progress = stack("reference_transform_progress")
        bridge_progress = stack("bridge_progress")
        states = self.samples["state"]

        summary = {
            "startup_mode": self.startup_mode,
            "target_state": self.target_state,
            "transform_duration": self.transform_duration,
            "bridge_duration": self.bridge_duration,
            "rl_duration": self.rl_duration,
            "idle_wait": self.idle_wait,
            "sample_counts": {k: len(v) for k, v in self.samples.items()},
            "first_state": states[0] if states else "",
            "last_state": states[-1] if states else "",
            "state_sequence": list(dict.fromkeys(states)),
            "final_base_rpy": base_rpy[-1].tolist() if base_rpy.size else [],
            "final_pitch": float(base_rpy[-1, 1]) if base_rpy.size else None,
            "max_abs_pitch": float(np.max(np.abs(base_rpy[:, 1]))) if base_rpy.size else None,
            "max_abs_roll": float(np.max(np.abs(base_rpy[:, 0]))) if base_rpy.size else None,
            "final_base_ang_vel": base_ang_vel[-1].tolist() if base_ang_vel.size else [],
            "max_abs_base_ang_vel": float(np.max(np.abs(base_ang_vel))) if base_ang_vel.size else None,
            "final_transform_up_progress": float(transform_progress[-1, 0]) if transform_progress.size else None,
            "final_reference_transform_up_progress": float(reference_transform_progress[-1, 0]) if reference_transform_progress.size else None,
            "final_handoff_bridge_progress": float(bridge_progress[-1, 0]) if bridge_progress.size else None,
            "final_action_raw_by_joint": action[-1].tolist() if action.size else [],
            "max_abs_action_raw": float(np.max(np.abs(action))) if action.size else None,
            "max_abs_action_wheels": float(np.max(np.abs(action[:, [3, 7]]))) if action.size else None,
            "final_action_scaled_by_joint": action_scaled[-1].tolist() if action_scaled.size else [],
            "max_abs_action_scaled": float(np.max(np.abs(action_scaled))) if action_scaled.size else None,
            "final_target_wheel_vel_by_joint": target[-1].tolist() if target.size else [],
            "max_abs_target_wheel_vel": float(np.nanmax(np.abs(target[:, [3, 7]]))) if target.size else None,
            "final_wheel_joint_vel": wheel_vel[-1].tolist() if wheel_vel.size else [],
            "max_abs_wheel_joint_vel": float(np.max(np.abs(wheel_vel))) if wheel_vel.size else None,
            "final_wheel_torque_cmd": wheel_torque[-1].tolist() if wheel_torque.size else [],
            "max_abs_wheel_torque_cmd": float(np.max(np.abs(wheel_torque))) if wheel_torque.size else None,
            "final_torque_cmd_by_joint": torque[-1].tolist() if torque.size else [],
            "max_abs_torque_cmd": float(np.max(np.abs(torque))) if torque.size else None,
            "final_torque_clip_by_joint": torque_clip[-1].tolist() if torque_clip.size else [],
            "max_abs_torque_clip": float(np.max(np.abs(torque_clip))) if torque_clip.size else None,
            "initial_joint_pos_error": joint_pos_error[0].tolist() if joint_pos_error.size else [],
            "final_joint_pos_error": joint_pos_error[-1].tolist() if joint_pos_error.size else [],
            "max_abs_joint_pos_error": float(np.max(np.abs(joint_pos_error))) if joint_pos_error.size else None,
        }
        arrays = {
            "base_rpy": base_rpy,
            "base_ang_vel": base_ang_vel,
            "action_raw": action,
            "action_scaled": action_scaled,
            "target_wheel_vel": target,
            "wheel_joint_vel": wheel_vel,
            "wheel_torque": wheel_torque,
            "torque": torque,
            "torque_clip": torque_clip,
            "joint_pos_error": joint_pos_error,
            "transform_progress": transform_progress,
            "reference_transform_progress": reference_transform_progress,
            "bridge_progress": bridge_progress,
            "state": np.asarray(states),
        }
        return summary, arrays

    def report(self) -> tuple[dict, dict[str, np.ndarray]]:
        summary, arrays = self.build_summary()
        for key in [
            "sample_counts",
            "first_state",
            "last_state",
            "state_sequence",
            "final_base_rpy",
            "max_abs_pitch",
            "final_pitch",
            "max_abs_roll",
            "final_reference_transform_up_progress",
            "final_action_raw_by_joint",
            "max_abs_action_raw",
            "final_action_scaled_by_joint",
            "max_abs_action_scaled",
            "final_target_wheel_vel_by_joint",
            "max_abs_target_wheel_vel",
            "final_wheel_joint_vel",
            "max_abs_wheel_joint_vel",
            "final_wheel_torque_cmd",
            "max_abs_wheel_torque_cmd",
            "final_torque_cmd_by_joint",
            "max_abs_torque_cmd",
            "final_torque_clip_by_joint",
            "max_abs_torque_clip",
            "initial_joint_pos_error",
            "final_joint_pos_error",
            "max_abs_joint_pos_error",
        ]:
            print(f"{key}:", summary[key])
        return summary, arrays

    def save(self, summary: dict, arrays: dict[str, np.ndarray]) -> tuple[Path, Path] | tuple[None, None]:
        if not self.output_prefix:
            return None, None
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = Path(f"{self.output_prefix}_{timestamp}")
        prefix.parent.mkdir(parents=True, exist_ok=True)
        npz_path = prefix.with_suffix(".npz")
        json_path = prefix.with_suffix(".json")
        np.savez(npz_path, **arrays)
        json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print("saved_npz:", npz_path)
        print("saved_json:", json_path)
        return npz_path, json_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--startup-mode", choices=["reference", "bridge"], default="reference")
    parser.add_argument("--target-state", choices=["rl_0", "shadow_rl0"], default="rl_0")
    parser.add_argument("--transform-duration", type=float, default=5.0)
    parser.add_argument("--bridge-duration", type=float, default=5.0)
    parser.add_argument("--rl-duration", type=float, default=5.0)
    parser.add_argument("--idle-wait", type=float, default=1.0)
    parser.add_argument(
        "--output-prefix",
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/rl0_closed_loop_summary",
    )
    args = parser.parse_args()

    rclpy.init()
    node = Rl0HandoffSampler(
        args.startup_mode,
        args.target_state,
        args.transform_duration,
        args.bridge_duration,
        args.rl_duration,
        args.idle_wait,
        args.output_prefix,
    )
    try:
        node.run()
        summary, arrays = node.report()
        node.save(summary, arrays)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
