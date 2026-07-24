#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from std_msgs.msg import Float32, Float32MultiArray, String


class Rl0FirstTickSampler(Node):
    def __init__(self, mode: str, tick_count: int, transform_timeout: float, output_prefix: str) -> None:
        super().__init__("rl0_first_tick_sampler")
        self.mode = mode
        self.target_state = "shadow_rl0" if mode == "shadow" else "rl_0"
        self.tick_count = tick_count
        self.transform_timeout = transform_timeout
        self.output_prefix = output_prefix
        self.key_pub = self.create_publisher(String, "/command/cmd_key", 10)
        self.twist_pub = self.create_publisher(Twist, "/command/cmd_twist", 10)

        self.current_state = ""
        self.latest: dict[str, np.ndarray] = {}
        self.records: list[dict[str, Any]] = []
        self.start_time = time.monotonic()
        self.last_zero_twist = 0.0

        self.create_subscription(String, "/cosim_ros2_jazzy/debug/state", self._state_cb, 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_rpy", self._cb("base_rpy"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/projected_gravity", self._cb("projected_gravity"), 10
        )
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_ang_vel", self._cb("base_ang_vel"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/gyro_raw", self._cb("gyro_raw"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/gyro_filtered", self._cb("gyro_filtered"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/command_scaled", self._cb("command_scaled"), 10
        )
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_pos", self._cb("joint_pos"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_vel", self._cb("joint_vel"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_pos_error", self._cb("joint_pos_error"), 10
        )
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/obs_current", self._cb("obs_current"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/obs_history", self._cb("obs_history"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/action_raw_by_joint", self._cb("action_raw"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/action_scaled_by_joint", self._cb("action_scaled"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/torque_cmd_by_joint", self._cb("torque_cmd"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/torque_clip_by_joint", self._cb("torque_clip"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/target_wheel_vel_by_joint", self._cb("target_wheel_vel"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/wheel_joint_vel", self._cb("wheel_joint_vel"), 10
        )
        self.create_subscription(Float32, "/cosim_ros2_jazzy/debug/policy_tick", self._policy_tick_cb, 10)

    def _cb(self, name: str):
        def callback(msg: Float32MultiArray) -> None:
            self.latest[name] = np.asarray(msg.data, dtype=np.float32)

        return callback

    def _state_cb(self, msg: String) -> None:
        self.current_state = msg.data

    def _policy_tick_cb(self, msg: Float32) -> None:
        if self.current_state != self.target_state:
            return
        obs_current = self.latest.get("obs_current")
        obs_history_flat = self.latest.get("obs_history")
        if obs_current is None or obs_history_flat is None:
            return
        obs_history = obs_history_flat.reshape(10, 33)
        record = {
            "tick_index": int(msg.data),
            "time": float(time.monotonic() - self.start_time),
            "state": self.current_state,
            "base_rpy": self.latest.get("base_rpy", np.full(3, np.nan, dtype=np.float32)).copy(),
            "projected_gravity": self.latest.get("projected_gravity", np.full(3, np.nan, dtype=np.float32)).copy(),
            "gyro_raw": self.latest.get("gyro_raw", np.full(3, np.nan, dtype=np.float32)).copy(),
            "gyro_filtered": self.latest.get("gyro_filtered", np.full(3, np.nan, dtype=np.float32)).copy(),
            "command_scaled": self.latest.get("command_scaled", np.full(3, np.nan, dtype=np.float32)).copy(),
            "joint_pos": self.latest.get("joint_pos", np.full(8, np.nan, dtype=np.float32)).copy(),
            "joint_vel": self.latest.get("joint_vel", np.full(8, np.nan, dtype=np.float32)).copy(),
            "joint_pos_error": self.latest.get("joint_pos_error", np.full(8, np.nan, dtype=np.float32)).copy(),
            "last_action": obs_current[25:33].copy(),
            "obs_current": obs_current.copy(),
            "obs_history": obs_history.copy(),
            "action_raw": self.latest.get("action_raw", np.full(8, np.nan, dtype=np.float32)).copy(),
            "action_scaled": self.latest.get("action_scaled", np.full(8, np.nan, dtype=np.float32)).copy(),
            "torque_cmd": self.latest.get("torque_cmd", np.full(8, np.nan, dtype=np.float32)).copy(),
            "torque_clip": self.latest.get("torque_clip", np.full(8, np.nan, dtype=np.float32)).copy(),
            "wheel_joint_vel": self.latest.get("wheel_joint_vel", np.full(2, np.nan, dtype=np.float32)).copy(),
            "target_wheel_vel": self.latest.get("target_wheel_vel", np.full(8, np.nan, dtype=np.float32)).copy(),
            "ang_vel": obs_current[0:3].copy(),
            "command_obs": obs_current[6:9].copy(),
            "joint_vel_obs": obs_current[17:25].copy(),
        }
        self.records.append(record)

    def publish_key(self, key: str) -> None:
        for _ in range(2):
            self.key_pub.publish(String(data=key))
            rclpy.spin_once(self, timeout_sec=0.05)

    def publish_zero_twist(self) -> None:
        self.twist_pub.publish(Twist())

    def spin_for(self, duration: float, publish_zero: bool = False) -> None:
        end = time.monotonic() + duration
        while time.monotonic() < end:
            now = time.monotonic()
            if publish_zero and (now - self.last_zero_twist) >= 0.1:
                self.publish_zero_twist()
                self.last_zero_twist = now
            rclpy.spin_once(self, timeout_sec=0.01)

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
        self.spin_for(0.5)
        self.publish_key("reference_transform_up")
        if not self.wait_for_state("reference_stand_hold", self.transform_timeout):
            raise RuntimeError("Timed out waiting for reference_stand_hold")
        self.spin_for(0.2)
        self.records.clear()
        self.publish_zero_twist()
        self.publish_key(self.target_state)
        end = time.monotonic() + 3.0
        while time.monotonic() < end and len(self.records) < self.tick_count:
            self.spin_for(0.02, publish_zero=True)
        if len(self.records) < self.tick_count:
            raise RuntimeError(
                f"Only captured {len(self.records)} policy ticks in state {self.target_state}; expected {self.tick_count}"
            )

    def save(self) -> tuple[Path, Path]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        npz_path = Path(f"{self.output_prefix}_{timestamp}.npz")
        json_path = Path(f"{self.output_prefix}_{timestamp}.json")
        npz_path.parent.mkdir(parents=True, exist_ok=True)

        arrays = {
            "tick_index": np.asarray([r["tick_index"] for r in self.records], dtype=np.int32),
            "time": np.asarray([r["time"] for r in self.records], dtype=np.float64),
            "state": np.asarray([r["state"] for r in self.records]),
            "base_rpy": np.stack([r["base_rpy"] for r in self.records]),
            "projected_gravity": np.stack([r["projected_gravity"] for r in self.records]),
            "gyro_raw": np.stack([r["gyro_raw"] for r in self.records]),
            "gyro_filtered": np.stack([r["gyro_filtered"] for r in self.records]),
            "command_scaled": np.stack([r["command_scaled"] for r in self.records]),
            "joint_pos": np.stack([r["joint_pos"] for r in self.records]),
            "joint_vel": np.stack([r["joint_vel"] for r in self.records]),
            "joint_pos_error": np.stack([r["joint_pos_error"] for r in self.records]),
            "last_action": np.stack([r["last_action"] for r in self.records]),
            "obs_current": np.stack([r["obs_current"] for r in self.records]),
            "obs_history": np.stack([r["obs_history"] for r in self.records]),
            "action_raw": np.stack([r["action_raw"] for r in self.records]),
            "action_scaled": np.stack([r["action_scaled"] for r in self.records]),
            "torque_cmd": np.stack([r["torque_cmd"] for r in self.records]),
            "torque_clip": np.stack([r["torque_clip"] for r in self.records]),
            "wheel_joint_vel": np.stack([r["wheel_joint_vel"] for r in self.records]),
            "target_wheel_vel": np.stack([r["target_wheel_vel"] for r in self.records]),
            "ang_vel": np.stack([r["ang_vel"] for r in self.records]),
            "command_obs": np.stack([r["command_obs"] for r in self.records]),
            "joint_vel_obs": np.stack([r["joint_vel_obs"] for r in self.records]),
        }
        np.savez(npz_path, **arrays)

        summary = {
            "mode": self.mode,
            "target_state": self.target_state,
            "tick_count": len(self.records),
            "first_tick_index": int(arrays["tick_index"][0]),
            "last_tick_index": int(arrays["tick_index"][-1]),
            "max_abs_action_raw": float(np.max(np.abs(arrays["action_raw"]))),
            "max_abs_action_scaled": float(np.max(np.abs(arrays["action_scaled"]))),
            "max_abs_torque_cmd": float(np.max(np.abs(arrays["torque_cmd"]))),
            "max_abs_torque_clip": float(np.max(np.abs(arrays["torque_clip"]))),
            "first_tick_action_raw": arrays["action_raw"][0].astype(float).tolist(),
            "first_tick_joint_pos_error": arrays["joint_pos_error"][0].astype(float).tolist(),
            "records": [
                {
                    "tick_index": int(r["tick_index"]),
                    "time": float(r["time"]),
                    "state": str(r["state"]),
                    "base_rpy": r["base_rpy"].astype(float).tolist(),
                    "projected_gravity": r["projected_gravity"].astype(float).tolist(),
                    "gyro_raw": r["gyro_raw"].astype(float).tolist(),
                    "gyro_filtered": r["gyro_filtered"].astype(float).tolist(),
                    "command_scaled": r["command_scaled"].astype(float).tolist(),
                    "joint_pos": r["joint_pos"].astype(float).tolist(),
                    "joint_vel": r["joint_vel"].astype(float).tolist(),
                    "joint_pos_error": r["joint_pos_error"].astype(float).tolist(),
                    "last_action": r["last_action"].astype(float).tolist(),
                    "obs_current": r["obs_current"].astype(float).tolist(),
                    "obs_history": r["obs_history"].astype(float).tolist(),
                    "action_raw": r["action_raw"].astype(float).tolist(),
                    "action_scaled": r["action_scaled"].astype(float).tolist(),
                    "torque_cmd": r["torque_cmd"].astype(float).tolist(),
                    "torque_clip": r["torque_clip"].astype(float).tolist(),
                    "wheel_joint_vel": r["wheel_joint_vel"].astype(float).tolist(),
                    "target_wheel_vel": r["target_wheel_vel"].astype(float).tolist(),
                    "ang_vel": r["ang_vel"].astype(float).tolist(),
                    "command_obs": r["command_obs"].astype(float).tolist(),
                    "joint_vel_obs": r["joint_vel_obs"].astype(float).tolist(),
                }
                for r in self.records
            ],
        }
        json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return npz_path, json_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["shadow", "real"], default="shadow")
    parser.add_argument("--ticks", type=int, default=10)
    parser.add_argument("--transform-timeout", type=float, default=10.0)
    parser.add_argument(
        "--output-prefix",
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/rl0_first_ticks",
    )
    args = parser.parse_args()

    rclpy.init()
    node = Rl0FirstTickSampler(
        mode=args.mode,
        tick_count=args.ticks,
        transform_timeout=args.transform_timeout,
        output_prefix=args.output_prefix,
    )
    try:
        node.run()
        npz_path, json_path = node.save()
        print(f"saved_npz: {npz_path}")
        print(f"saved_json: {json_path}")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
