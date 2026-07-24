from __future__ import annotations

import csv
import json
import math
import os
import queue
import threading
import time
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import Float64MultiArray


POLICY_DIAGNOSTIC_COLUMNS = (
    "controller_monotonic_ns",
    "controller_sequence",
    "controller_state",
    "inference_ms",
    "command_vx",
    "command_vy",
    "command_yaw",
    "estimator_scaled_x",
    "estimator_scaled_y",
    "estimator_scaled_z",
    "estimator_mps_x",
    "estimator_mps_y",
    "estimator_mps_z",
    "wheel_common_rad_s",
    "wheel_no_slip_mps",
    "estimator_vx_integral_m",
    "wheel_no_slip_integral_m",
    *(f"obs_{index:02d}" for index in range(33)),
    *(f"action_{index}" for index in range(8)),
    *(f"joint_pos_{index}" for index in range(8)),
    *(f"joint_vel_{index}" for index in range(8)),
    *(f"imu_quat_xyzw_{index}" for index in range(4)),
    *(f"imu_ang_vel_{index}" for index in range(3)),
)


def validated_policy_diagnostic(values: tuple[float, ...]) -> tuple[float, ...]:
    if len(values) != len(POLICY_DIAGNOSTIC_COLUMNS):
        raise ValueError(
            f"policy diagnostic width {len(values)} != {len(POLICY_DIAGNOSTIC_COLUMNS)}"
        )
    result = tuple(float(value) for value in values)
    if not all(math.isfinite(value) for value in result):
        raise ValueError("policy diagnostic contains NaN or Inf")
    return result


class EstimatorDiagnosticLogger(Node):
    """Read-only bounded-queue logger for the controller's 50 Hz policy diagnostic topic."""

    def __init__(self) -> None:
        super().__init__("tita_estimator_diagnostic_logger")
        self.declare_parameter("topic", "/tita_stage1_controller/policy_diagnostics")
        self.declare_parameter("output_root", "/home/robot/tita_ws/runs/estimator")
        self.declare_parameter("policy_sha256", "")
        self.declare_parameter("queue_size", 2048)
        topic = str(self.get_parameter("topic").value)
        output_root = Path(str(self.get_parameter("output_root").value)).expanduser()
        queue_size = max(int(self.get_parameter("queue_size").value), 1)
        monotonic_start_ns = time.monotonic_ns()
        self.run_dir = output_root / f"mono{monotonic_start_ns}_pid{os.getpid()}_estimator"
        self.run_dir.mkdir(parents=True, exist_ok=False)
        self.csv_path = self.run_dir / "estimator_step_log.csv"
        self.metadata_path = self.run_dir / "metadata.json"
        self._metadata = {
            "run_id": self.run_dir.name,
            "monotonic_start_ns": monotonic_start_ns,
            "process_pid": os.getpid(),
            "topic": topic,
            "policy_sha256": str(self.get_parameter("policy_sha256").value),
            "schema": list(POLICY_DIAGNOSTIC_COLUMNS),
            "schema_width": len(POLICY_DIAGNOSTIC_COLUMNS),
            "estimator_target_scale": 2.0,
            "wheel_radius_m": 0.0925,
            "wheel_displacement_semantics": "no-slip proxy; not chassis ground truth",
            "hardware_command_publishers": [],
            "dropped_records": 0,
            "invalid_records": 0,
        }
        self.metadata_path.write_text(
            json.dumps(self._metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        self._queue: queue.Queue[tuple[float, ...]] = queue.Queue(maxsize=queue_size)
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._writer_main, daemon=True)
        self._thread.start()
        self._subscription = self.create_subscription(
            Float64MultiArray, topic, self._callback, qos_profile_sensor_data
        )
        self.get_logger().info(
            f"command-free estimator logger ready: {self.csv_path}; width={len(POLICY_DIAGNOSTIC_COLUMNS)}"
        )

    def _callback(self, message: Float64MultiArray) -> None:
        try:
            record = validated_policy_diagnostic(tuple(message.data))
        except ValueError:
            self._metadata["invalid_records"] += 1
            return
        try:
            self._queue.put_nowait(record)
        except queue.Full:
            self._metadata["dropped_records"] += 1

    def _writer_main(self) -> None:
        with self.csv_path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(POLICY_DIAGNOSTIC_COLUMNS)
            last_flush = time.monotonic()
            while not self._stop.is_set() or not self._queue.empty():
                try:
                    record = self._queue.get(timeout=0.05)
                except queue.Empty:
                    record = None
                if record is not None:
                    writer.writerow(record)
                if time.monotonic() - last_flush >= 1.0:
                    stream.flush()
                    last_flush = time.monotonic()
            stream.flush()
            os.fsync(stream.fileno())

    def close(self) -> None:
        if self._stop.is_set():
            return
        self._stop.set()
        self._thread.join(timeout=3.0)
        self._metadata["closed_monotonic_ns"] = time.monotonic_ns()
        self.metadata_path.write_text(
            json.dumps(self._metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


def main() -> None:
    rclpy.init()
    node = EstimatorDiagnosticLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.close()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
