#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from std_msgs.msg import Float32, Float32MultiArray, String


JOINT_NAMES = [
    "joint_left_leg_1",
    "joint_left_leg_2",
    "joint_left_leg_3",
    "joint_left_leg_4",
    "joint_right_leg_1",
    "joint_right_leg_2",
    "joint_right_leg_3",
    "joint_right_leg_4",
]
POLICY_REINDEX = [0, 4, 1, 5, 2, 6, 3, 7]
WHEEL_INDICES = [3, 7]
LEG_INDICES = [0, 1, 2, 4, 5, 6]


@dataclass
class TickRecord:
    tick_index: int
    time: float
    sim_time: float
    policy_tick: float
    state: str
    base_rpy: np.ndarray
    base_lin_vel: np.ndarray
    base_ang_vel: np.ndarray
    action_raw: np.ndarray
    action_scaled: np.ndarray
    target_joint_pos: np.ndarray
    target_joint_vel: np.ndarray
    joint_pos: np.ndarray
    joint_vel: np.ndarray
    pos_error: np.ndarray
    vel_error: np.ndarray
    torque_cmd: np.ndarray
    torque_clip: np.ndarray
    obs_current: np.ndarray
    obs_history: np.ndarray
    last_action: np.ndarray
    obs_joint_pos_error_policy_order: np.ndarray
    obs_joint_vel_policy_order: np.ndarray


class JointTrackingSampler(Node):
    def __init__(self, config_path: str, duration_s: float, output_prefix: str, manual: bool = False) -> None:
        super().__init__("rl0_joint_tracking_sampler")
        self.config_path = config_path
        self.duration_s = duration_s
        self.output_prefix = output_prefix
        self.manual = manual
        self.key_pub = self.create_publisher(String, "/command/cmd_key", 10)
        self.twist_pub = self.create_publisher(Twist, "/command/cmd_twist", 10)

        self.current_state = ""
        self.capture_active = False
        self.capture_start_wall = 0.0
        self.capture_start_sim_time = 0.0
        self.policy_tick_seen = -1.0
        self.last_recorded_policy_tick = -1.0
        self.last_recorded_sim_time = -1.0
        self.latest: dict[str, np.ndarray] = {}
        self.records: list[TickRecord] = []
        self.start_wall = time.monotonic()

        self.create_subscription(String, "/cosim_ros2_jazzy/debug/state", self._state_cb, 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_rpy", self._base_rpy_cb, 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_lin_vel", self._cb("base_lin_vel"), 10)
        self.create_subscription(Float32, "/cosim_ros2_jazzy/debug/sim_time", self._sim_time_cb, 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/base_ang_vel", self._cb("base_ang_vel"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/action_raw_by_joint", self._cb("action_raw"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/action_scaled_by_joint", self._cb("action_scaled"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/target_joint_pos_by_joint", self._cb("target_joint_pos"), 10
        )
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/target_joint_vel_by_joint", self._cb("target_joint_vel"), 10
        )
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_pos", self._cb("joint_pos"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_vel", self._cb("joint_vel"), 10)
        self.create_subscription(
            Float32MultiArray, "/cosim_ros2_jazzy/debug/joint_pos_error", self._cb("joint_pos_error"), 10
        )
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/torque_cmd_by_joint", self._cb("torque_cmd"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/torque_clip_by_joint", self._cb("torque_clip"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/obs_current", self._cb("obs_current"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/obs_history", self._cb("obs_history"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/gyro_filtered", self._cb("gyro_filtered"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/command_scaled", self._cb("command_scaled"), 10)
        self.create_subscription(Float32MultiArray, "/cosim_ros2_jazzy/debug/policy_tick", self._policy_tick_cb, 10)

    def _cb(self, name: str):
        def callback(msg: Float32MultiArray) -> None:
            self.latest[name] = np.asarray(msg.data, dtype=np.float32)

        return callback

    def _state_cb(self, msg: String) -> None:
        self.current_state = msg.data

    def _sim_time_cb(self, msg: Float32) -> None:
        self.latest["sim_time"] = np.asarray([float(msg.data)], dtype=np.float32)
        self._maybe_record()

    def _policy_tick_cb(self, msg: Float32) -> None:
        self.policy_tick_seen = float(msg.data)
        self.latest["policy_tick"] = np.asarray([self.policy_tick_seen], dtype=np.float32)
        self._maybe_record()

    def _base_rpy_cb(self, msg: Float32MultiArray) -> None:
        self.latest["base_rpy"] = np.asarray(msg.data, dtype=np.float32)

    def _maybe_record(self) -> None:
        if not self.capture_active or self.current_state != "rl_0":
            return
        obs_current = self.latest.get("obs_current")
        obs_history = self.latest.get("obs_history")
        action_raw = self.latest.get("action_raw")
        action_scaled = self.latest.get("action_scaled")
        target_joint_pos = self.latest.get("target_joint_pos")
        target_joint_vel = self.latest.get("target_joint_vel")
        joint_pos = self.latest.get("joint_pos")
        joint_vel = self.latest.get("joint_vel")
        pos_error = self.latest.get("joint_pos_error")
        torque_cmd = self.latest.get("torque_cmd")
        torque_clip = self.latest.get("torque_clip")
        base_lin_vel = self.latest.get("base_lin_vel", np.full(3, np.nan, dtype=np.float32))
        base_ang_vel = self.latest.get("base_ang_vel", np.full(3, np.nan, dtype=np.float32))
        gyro_filtered = self.latest.get("gyro_filtered", np.full(3, np.nan, dtype=np.float32))
        command_scaled = self.latest.get("command_scaled", np.full(3, np.nan, dtype=np.float32))
        sim_time = self.latest.get("sim_time", np.full(1, np.nan, dtype=np.float32))
        policy_tick = self.latest.get("policy_tick", np.full(1, np.nan, dtype=np.float32))
        if any(v is None for v in [obs_current, obs_history, action_raw, action_scaled, target_joint_pos, target_joint_vel, joint_pos, joint_vel, pos_error, torque_cmd, torque_clip]):
            return
        if not np.isfinite(sim_time[0]):
            return
        if sim_time[0] <= self.last_recorded_sim_time + 1e-9:
            return

        obs_current = np.asarray(obs_current, dtype=np.float32)
        obs_history = np.asarray(obs_history, dtype=np.float32).reshape(-1, obs_current.size)
        joint_pos = np.asarray(joint_pos, dtype=np.float32)
        joint_vel = np.asarray(joint_vel, dtype=np.float32)
        pos_error = np.asarray(pos_error, dtype=np.float32)
        target_joint_pos = np.asarray(target_joint_pos, dtype=np.float32)
        target_joint_vel = np.asarray(target_joint_vel, dtype=np.float32)
        action_raw = np.asarray(action_raw, dtype=np.float32)
        action_scaled = np.asarray(action_scaled, dtype=np.float32)
        torque_cmd = np.asarray(torque_cmd, dtype=np.float32)
        torque_clip = np.asarray(torque_clip, dtype=np.float32)
        joint_pos_error_policy_order = obs_current[9:17].copy()
        joint_vel_policy_order = obs_current[17:25].copy()
        base_rpy = self.latest.get("base_rpy", np.full(3, np.nan, dtype=np.float32))
        record = TickRecord(
            tick_index=len(self.records),
            time=float(sim_time[0] - self.capture_start_sim_time) if np.isfinite(sim_time[0]) else float(time.monotonic() - self.capture_start_wall),
            sim_time=float(sim_time[0]) if np.isfinite(sim_time[0]) else float("nan"),
            policy_tick=float(policy_tick[0]) if np.isfinite(policy_tick[0]) else float(self.policy_tick_seen),
            state=self.current_state,
            base_rpy=np.asarray(base_rpy, dtype=np.float32).copy(),
            base_lin_vel=np.asarray(base_lin_vel, dtype=np.float32).copy(),
            base_ang_vel=np.asarray(base_ang_vel, dtype=np.float32).copy(),
            action_raw=action_raw.copy(),
            action_scaled=action_scaled.copy(),
            target_joint_pos=target_joint_pos.copy(),
            target_joint_vel=target_joint_vel.copy(),
            joint_pos=joint_pos.copy(),
            joint_vel=joint_vel.copy(),
            pos_error=pos_error.copy(),
            vel_error=(joint_vel - target_joint_vel).astype(np.float32),
            torque_cmd=torque_cmd.copy(),
            torque_clip=torque_clip.copy(),
            obs_current=obs_current.copy(),
            obs_history=obs_history.copy(),
            last_action=obs_current[25:33].copy(),
            obs_joint_pos_error_policy_order=joint_pos_error_policy_order.copy(),
            obs_joint_vel_policy_order=joint_vel_policy_order.copy(),
        )
        self.records.append(record)
        self.last_recorded_policy_tick = self.policy_tick_seen
        self.last_recorded_sim_time = float(sim_time[0])

    def publish_key(self, key: str) -> None:
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
        if self.manual:
            self.get_logger().info("Manual mode: waiting for rl_0 state before capturing samples")
            if not self.wait_for_state("rl_0", 300.0):
                raise RuntimeError("Timed out waiting for rl_0")
            self.records.clear()
            self.capture_active = True
            self.capture_start_wall = time.monotonic()
            self.capture_start_sim_time = float(self.latest.get("sim_time", np.asarray([0.0], dtype=np.float32))[0])
            self.last_recorded_policy_tick = -1.0
            self.last_recorded_sim_time = -1.0
            self.spin_for(self.duration_s, publish_zero=True)
            self.capture_active = False
            return
        self.spin_for(0.5)
        self.publish_key("idle")
        self.spin_for(0.5)
        self.publish_key("reference_transform_up")
        if not self.wait_for_state("reference_stand_hold", 60.0):
            raise RuntimeError("Timed out waiting for reference_stand_hold")
        self.spin_for(0.2)
        self.records.clear()
        self.capture_active = True
        self.capture_start_wall = time.monotonic()
        self.capture_start_sim_time = float(self.latest.get("sim_time", np.asarray([0.0], dtype=np.float32))[0])
        self.last_recorded_policy_tick = -1.0
        self.last_recorded_sim_time = -1.0
        self.publish_zero_twist()
        self.publish_key("rl_0")
        self.spin_for(self.duration_s, publish_zero=True)
        self.capture_active = False

    def _sample_metrics(self, series: np.ndarray, dt: float) -> dict[str, float]:
        series = np.asarray(series, dtype=np.float32)
        centered = series - np.mean(series)
        rms = float(np.sqrt(np.mean(np.square(centered))))
        p2p = float(np.max(series) - np.min(series))
        freq = 0.0
        if series.size >= 4:
            fft = np.fft.rfft(centered)
            freqs = np.fft.rfftfreq(series.size, d=max(dt, 1e-6))
            if freqs.size > 1:
                mag = np.abs(fft)
                mag[0] = 0.0
                freq = float(freqs[int(np.argmax(mag))])
        return {"rms": rms, "p2p": p2p, "dominant_freq": freq}

    def save(self) -> tuple[Path, Path, Path]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = Path(f"{self.output_prefix}_{timestamp}")
        npz_path = prefix.with_suffix(".npz")
        json_path = prefix.with_suffix(".json")
        csv_path = prefix.with_suffix(".csv")
        npz_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.records:
            raise RuntimeError("No rl_0 samples captured")

        arrays = {field: [] for field in TickRecord.__annotations__.keys()}
        for rec in self.records:
            for key, value in asdict(rec).items():
                arrays[key].append(value)
        np_arrays: dict[str, np.ndarray] = {}
        for key, values in arrays.items():
            np_arrays[key] = np.stack(values) if isinstance(values[0], np.ndarray) else np.asarray(values)
        np.savez(npz_path, **np_arrays)

        dt = float(np.median(np.diff(np_arrays["time"]))) if np_arrays["time"].size > 1 else 0.0
        sim_dt = float(np.median(np.diff(np_arrays["sim_time"]))) if np_arrays.get("sim_time", np.empty(0)).size > 1 else 0.0
        summary = {
            "config_path": self.config_path,
            "duration_s": self.duration_s,
            "num_samples": int(len(self.records)),
            "dt_median": dt,
            "sim_dt_median": sim_dt,
            "final_pitch": float(np_arrays["base_rpy"][-1, 1]),
            "max_abs_pitch": float(np.max(np.abs(np_arrays["base_rpy"][:, 1]))),
            "max_abs_roll": float(np.max(np.abs(np_arrays["base_rpy"][:, 0]))),
            "max_abs_action_raw": float(np.max(np.abs(np_arrays["action_raw"]))),
            "max_abs_action_scaled": float(np.max(np.abs(np_arrays["action_scaled"]))),
            "max_abs_torque_cmd": float(np.max(np.abs(np_arrays["torque_cmd"]))),
            "max_abs_torque_clip": float(np.max(np.abs(np_arrays["torque_clip"]))),
            "max_abs_wheel_joint_vel": float(np.max(np.abs(np_arrays["joint_vel"][:, WHEEL_INDICES]))),
            "joint_metrics": {},
            "records": [
                {
                    "tick_index": int(rec.tick_index),
                    "time": float(rec.time),
                    "sim_time": float(rec.sim_time),
                    "policy_tick": float(rec.policy_tick),
                    "state": rec.state,
                    "base_rpy": rec.base_rpy.astype(float).tolist(),
                    "base_lin_vel": rec.base_lin_vel.astype(float).tolist(),
                    "base_ang_vel": rec.base_ang_vel.astype(float).tolist(),
                    "action_raw": rec.action_raw.astype(float).tolist(),
                    "action_scaled": rec.action_scaled.astype(float).tolist(),
                    "target_joint_pos": rec.target_joint_pos.astype(float).tolist(),
                    "target_joint_vel": rec.target_joint_vel.astype(float).tolist(),
                    "joint_pos": rec.joint_pos.astype(float).tolist(),
                    "joint_vel": rec.joint_vel.astype(float).tolist(),
                    "pos_error": rec.pos_error.astype(float).tolist(),
                    "vel_error": rec.vel_error.astype(float).tolist(),
                    "torque_cmd": rec.torque_cmd.astype(float).tolist(),
                    "torque_clip": rec.torque_clip.astype(float).tolist(),
                    "obs_current": rec.obs_current.astype(float).tolist(),
                    "obs_history": rec.obs_history.astype(float).tolist(),
                    "last_action": rec.last_action.astype(float).tolist(),
                    "obs_joint_pos_error_policy_order": rec.obs_joint_pos_error_policy_order.astype(float).tolist(),
                    "obs_joint_vel_policy_order": rec.obs_joint_vel_policy_order.astype(float).tolist(),
                }
                for rec in self.records
            ],
        }
        for idx, joint in enumerate(JOINT_NAMES):
            metrics = {
                "action_raw": self._sample_metrics(np_arrays["action_raw"][:, idx], dt),
                "target_joint_pos": self._sample_metrics(np_arrays["target_joint_pos"][:, idx], dt),
                "joint_pos": self._sample_metrics(np_arrays["joint_pos"][:, idx], dt),
                "joint_vel": self._sample_metrics(np_arrays["joint_vel"][:, idx], dt),
                "pos_error": self._sample_metrics(np_arrays["pos_error"][:, idx], dt),
                "torque_cmd": self._sample_metrics(np_arrays["torque_cmd"][:, idx], dt),
            }
            summary["joint_metrics"][joint] = {
                "p2p_action": metrics["action_raw"]["p2p"],
                "p2p_target": metrics["target_joint_pos"]["p2p"],
                "p2p_pos": metrics["joint_pos"]["p2p"],
                "p2p_vel": metrics["joint_vel"]["p2p"],
                "rms_error": metrics["pos_error"]["rms"],
                "rms_torque": metrics["torque_cmd"]["rms"],
                "dominant_freq": metrics["joint_pos"]["dominant_freq"],
                "note": "wheel target metrics are NaN on leg joints" if idx in LEG_INDICES else "wheel slot",
            }

        json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "tick_index",
                "time",
                "sim_time",
                "policy_tick",
                "state",
                "pitch",
                "roll",
                "action_raw",
                "action_scaled",
                "target_joint_pos",
                "target_joint_vel",
                "joint_pos",
                "joint_vel",
                "pos_error",
                "vel_error",
                "torque_cmd",
                "torque_clip",
            ])
            for rec in self.records:
                writer.writerow(
                    [
                        rec.tick_index,
                        rec.time,
                        rec.state,
                        rec.base_rpy[1],
                        rec.base_rpy[0],
                        json.dumps(rec.action_raw.astype(float).tolist()),
                        json.dumps(rec.action_scaled.astype(float).tolist()),
                        json.dumps(rec.target_joint_pos.astype(float).tolist()),
                        json.dumps(rec.target_joint_vel.astype(float).tolist()),
                        json.dumps(rec.joint_pos.astype(float).tolist()),
                        json.dumps(rec.joint_vel.astype(float).tolist()),
                        json.dumps(rec.pos_error.astype(float).tolist()),
                        json.dumps(rec.vel_error.astype(float).tolist()),
                        json.dumps(rec.torque_cmd.astype(float).tolist()),
                        json.dumps(rec.torque_clip.astype(float).tolist()),
                    ]
                )

        return npz_path, json_path, csv_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="cosim_ros2_jazzy/config/tita.yaml")
    parser.add_argument("--duration", type=float, default=10.0)
    parser.add_argument("--manual", action="store_true")
    parser.add_argument(
        "--output-prefix",
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/rl0_joint_tracking_debug",
    )
    args = parser.parse_args()

    rclpy.init()
    node = JointTrackingSampler(args.config, args.duration, args.output_prefix, manual=args.manual)
    try:
        node.run()
        npz_path, json_path, csv_path = node.save()
        print(f"saved_npz: {npz_path}")
        print(f"saved_json: {json_path}")
        print(f"saved_csv: {csv_path}")
        print(f"samples: {len(node.records)}")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
