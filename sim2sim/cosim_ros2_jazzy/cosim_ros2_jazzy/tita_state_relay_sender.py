#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import socket
import sys
import threading
import time
from dataclasses import dataclass
from typing import Any

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rosidl_runtime_py.utilities import get_message
from sensor_msgs.msg import Imu, JointState, Joy
from rclpy.parameter import Parameter
from std_msgs.msg import String

from .relay_protocol import (
    RelayCommand, RelayPacketError, SCHEMA_V1, SCHEMA_V2, command_for_transmit, encode_packet,
)


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"1", "true", "yes", "on"}


def _ros_msg_to_plain(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, (list, tuple)):
        return [_ros_msg_to_plain(item) for item in value]
    fields = getattr(value, "get_fields_and_field_types", None)
    if callable(fields):
        return {field: _ros_msg_to_plain(getattr(value, field)) for field in value.get_fields_and_field_types()}
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    return str(value)


def _stamp_to_dict(stamp: Any) -> dict[str, int]:
    if stamp is None:
        return {"sec": 0, "nanosec": 0}
    return {"sec": int(getattr(stamp, "sec", 0)), "nanosec": int(getattr(stamp, "nanosec", 0))}


def _vector3_to_dict(vector: Any) -> dict[str, float]:
    return {
        "x": float(getattr(vector, "x", 0.0)),
        "y": float(getattr(vector, "y", 0.0)),
        "z": float(getattr(vector, "z", 0.0)),
    }


def _quat_to_dict(quat: Any) -> dict[str, float]:
    return {
        "x": float(getattr(quat, "x", 0.0)),
        "y": float(getattr(quat, "y", 0.0)),
        "z": float(getattr(quat, "z", 0.0)),
        "w": float(getattr(quat, "w", 1.0)),
    }


def _joint_state_packet(msg: JointState | None) -> dict[str, Any]:
    if msg is None:
        return {"available": False}
    header = getattr(msg, "header", None)
    return {
        "available": True,
        "header_stamp": _stamp_to_dict(getattr(header, "stamp", None)),
        "frame_id": str(getattr(header, "frame_id", "")),
        "name": list(getattr(msg, "name", [])),
        "position": [float(v) for v in getattr(msg, "position", [])],
        "velocity": [float(v) for v in getattr(msg, "velocity", [])],
        "effort": [float(v) for v in getattr(msg, "effort", [])],
    }


def _imu_packet(msg: Imu | None) -> dict[str, Any]:
    if msg is None:
        return {"available": False}
    header = getattr(msg, "header", None)
    return {
        "available": True,
        "header_stamp": _stamp_to_dict(getattr(header, "stamp", None)),
        "frame_id": str(getattr(header, "frame_id", "")),
        "orientation": _quat_to_dict(getattr(msg, "orientation", None)),
        "angular_velocity": _vector3_to_dict(getattr(msg, "angular_velocity", None)),
        "linear_acceleration": _vector3_to_dict(getattr(msg, "linear_acceleration", None)),
    }


def _odom_packet(msg: Odometry | None) -> dict[str, Any]:
    if msg is None:
        return {"available": False}
    header = getattr(msg, "header", None)
    pose = getattr(msg, "pose", None)
    twist = getattr(msg, "twist", None)
    pose_pose = getattr(pose, "pose", None)
    twist_twist = getattr(twist, "twist", None)
    return {
        "available": True,
        "header_stamp": _stamp_to_dict(getattr(header, "stamp", None)),
        "frame_id": str(getattr(header, "frame_id", "")),
        "child_frame_id": str(getattr(msg, "child_frame_id", "")),
        "pose": {
            "position": _vector3_to_dict(getattr(pose_pose, "position", None)),
            "orientation": _quat_to_dict(getattr(pose_pose, "orientation", None)),
        },
        "twist": {
            "linear": _vector3_to_dict(getattr(twist_twist, "linear", None)),
            "angular": _vector3_to_dict(getattr(twist_twist, "angular", None)),
        },
    }


def _motors_status_packet(msg: Any | None) -> dict[str, Any]:
    if msg is None:
        return {"available": False}
    compact = str(msg)
    if len(compact) > 512:
        compact = compact[:512] + "..."
    return {
        "available": True,
        "summary": compact,
        "raw": _ros_msg_to_plain(msg),
    }


@dataclass
class _SubscriptionSpec:
    topic: str
    message_type: Any
    callback: Any


class TitaStateRelaySender(Node):
    def __init__(self) -> None:
        super().__init__("tita_state_relay_sender")
        self.declare_parameter("tita_ns", "tita4252763")
        self.declare_parameter("bind_host", "0.0.0.0")
        self.declare_parameter("port", 50051)
        self.declare_parameter("send_rate_hz", 50.0)
        self.declare_parameter("include_motors_status", True)
        self.declare_parameter("include_command", False)
        self.declare_parameter("include_fsm", True)
        self.declare_parameter("command_source", "processed_twist")
        self.declare_parameter("command_timeout_sec", 0.5)
        self.declare_parameter("raw_joy_mapping_confirmed", False)
        self.declare_parameter("raw_joy_forward_axis", 0)
        self.declare_parameter("raw_joy_yaw_axis", 1)
        self.declare_parameter("raw_joy_lateral_axis", -1)
        self.declare_parameter("raw_joy_forward_scale", 1.0)
        self.declare_parameter("raw_joy_yaw_scale", 1.0)
        self.declare_parameter("raw_joy_lateral_scale", 0.0)
        self.declare_parameter("raw_joy_deadzone", 0.0013)

        self.tita_ns = str(self.get_parameter("tita_ns").value).strip("/") or "tita4252763"
        self.bind_host = str(self.get_parameter("bind_host").value).strip() or "0.0.0.0"
        self.port = int(self.get_parameter("port").value)
        self.send_rate_hz = float(self.get_parameter("send_rate_hz").value)
        self.include_motors_status = _as_bool(self.get_parameter("include_motors_status").value)
        self.include_command = _as_bool(self.get_parameter("include_command").value)
        self.include_fsm = _as_bool(self.get_parameter("include_fsm").value)
        self.command_source = str(self.get_parameter("command_source").value).strip().lower()
        self.command_timeout_sec = max(float(self.get_parameter("command_timeout_sec").value), 0.0)
        self.raw_joy_mapping_confirmed = _as_bool(self.get_parameter("raw_joy_mapping_confirmed").value)
        self.raw_joy_axes = (
            int(self.get_parameter("raw_joy_forward_axis").value),
            int(self.get_parameter("raw_joy_lateral_axis").value),
            int(self.get_parameter("raw_joy_yaw_axis").value),
        )
        self.raw_joy_scales = (
            float(self.get_parameter("raw_joy_forward_scale").value),
            float(self.get_parameter("raw_joy_lateral_scale").value),
            float(self.get_parameter("raw_joy_yaw_scale").value),
        )
        self.raw_joy_deadzone = max(float(self.get_parameter("raw_joy_deadzone").value), 0.0)
        if self.command_source not in {"processed_twist", "active_command", "raw_joy"}:
            raise ValueError(f"Unsupported command_source: {self.command_source}")
        if self.include_command and self.command_source == "raw_joy" and not self.raw_joy_mapping_confirmed:
            raise ValueError("raw_joy requires raw_joy_mapping_confirmed=true and reviewed axis/sign/scale parameters")

        self.joint_topic = f"/{self.tita_ns}/joint_states"
        self.imu_topic = f"/{self.tita_ns}/imu_sensor_broadcaster/imu"
        self.odom_topic = f"/{self.tita_ns}/chassis/odometry"
        self.motors_status_topic = f"/{self.tita_ns}/locomotion/motors_status"
        self.fsm_topic = f"/{self.tita_ns}/locomotion/body/fsm_mode"
        self.command_topics = {
            "processed_twist": f"/{self.tita_ns}/command/manager/cmd_twist",
            "active_command": f"/{self.tita_ns}/command/active/command",
            "raw_joy": f"/{self.tita_ns}/joy",
        }
        self.command_topic = self.command_topics[self.command_source]

        self._lock = threading.Lock()
        self._latest_joint_states: JointState | None = None
        self._latest_imu: Imu | None = None
        self._latest_odom: Odometry | None = None
        self._latest_motors_status: Any | None = None
        self._latest_fsm = ""
        self._fsm_received = False
        self._latest_command = RelayCommand(self.command_source, False, 0, 0.0, 0.0, 0.0)
        self._command_received_monotonic_ns = 0
        self._subscriptions_ready = False
        self._server_socket: socket.socket | None = None
        self._client_socket: socket.socket | None = None
        self._client_address: tuple[str, int] | None = None
        self._stop_event = threading.Event()
        self._seq = 0

        self._subscription_timer = self.create_timer(1.0, self._ensure_subscriptions)
        self._send_timer = self.create_timer(max(1.0 / max(self.send_rate_hz, 1e-3), 0.01), self._send_packet)
        self._server_thread = threading.Thread(target=self._server_loop, daemon=True)
        self._server_thread.start()

        self.get_logger().info(f"State relay sender started on {self.bind_host}:{self.port}")
        self.get_logger().info(f"Local namespace: /{self.tita_ns}")
        self.get_logger().info(f"Joint topic: {self.joint_topic}")
        self.get_logger().info(f"IMU topic: {self.imu_topic}")
        self.get_logger().info(f"Odom topic: {self.odom_topic}")
        self.get_logger().info(f"Motors status topic: {self.motors_status_topic}")
        self.get_logger().info(f"FSM topic: {self.fsm_topic}")
        if self.include_command:
            self.get_logger().info(f"Command source (subscribe-only): {self.command_source} {self.command_topic}")

    def _ensure_subscriptions(self) -> None:
        specs: list[_SubscriptionSpec] = [
            _SubscriptionSpec(self.joint_topic, JointState, self._joint_cb),
            _SubscriptionSpec(self.imu_topic, Imu, self._imu_cb),
            _SubscriptionSpec(self.odom_topic, Odometry, self._odom_cb),
        ]
        if self.include_motors_status:
            topic_type = self._resolve_topic_type(self.motors_status_topic)
            if topic_type is not None:
                specs.append(_SubscriptionSpec(self.motors_status_topic, topic_type, self._motors_status_cb))
        if self.include_fsm:
            specs.append(_SubscriptionSpec(self.fsm_topic, String, self._fsm_cb))
        if self.include_command:
            command_type = {"processed_twist": Twist, "raw_joy": Joy}.get(self.command_source)
            if command_type is None:
                command_type = self._resolve_topic_type(self.command_topic)
            if command_type is not None:
                specs.append(_SubscriptionSpec(self.command_topic, command_type, self._command_cb))

        created_any = False
        for spec in specs:
            attr_name = f"_sub_{spec.topic.replace('/', '_')}"
            if hasattr(self, attr_name):
                continue
            if spec.topic == self.motors_status_topic and spec.message_type is None:
                continue
            try:
                sub = self.create_subscription(spec.message_type, spec.topic, spec.callback, 10)
            except Exception as exc:
                self.get_logger().warn(f"Failed to subscribe to {spec.topic}: {exc}")
                continue
            setattr(self, attr_name, sub)
            created_any = True

        if not self._subscriptions_ready and all(
            hasattr(self, f"_sub_{topic.replace('/', '_')}") for topic in [self.joint_topic, self.imu_topic, self.odom_topic]
        ):
            self._subscriptions_ready = True
            self.get_logger().info("Core relay subscriptions are ready")
        elif created_any and self.include_motors_status and hasattr(self, f"_sub_{self.motors_status_topic.replace('/', '_')}"):
            self.get_logger().info("Motors status relay subscription is ready")

    def _resolve_topic_type(self, topic: str) -> Any | None:
        for topic_name, types in self.get_topic_names_and_types():
            if topic_name == topic and types:
                try:
                    return get_message(types[0])
                except Exception as exc:
                    self.get_logger().warn(f"Failed to import message type {types[0]} for {topic}: {exc}")
                    return None
        return None

    def _joint_cb(self, msg: JointState) -> None:
        with self._lock:
            self._latest_joint_states = msg

    def _imu_cb(self, msg: Imu) -> None:
        with self._lock:
            self._latest_imu = msg

    def _odom_cb(self, msg: Odometry) -> None:
        with self._lock:
            self._latest_odom = msg

    def _motors_status_cb(self, msg: Any) -> None:
        with self._lock:
            self._latest_motors_status = msg

    def _fsm_cb(self, msg: String) -> None:
        with self._lock:
            self._latest_fsm = str(msg.data).strip()
            self._fsm_received = True

    @staticmethod
    def _twist_values(twist: Any) -> tuple[float, float, float]:
        return float(twist.linear.x), float(twist.linear.y), float(twist.angular.z)

    def _raw_joy_values(self, msg: Joy) -> tuple[float, float, float]:
        values: list[float] = []
        for index, scale in zip(self.raw_joy_axes, self.raw_joy_scales):
            value = float(msg.axes[index]) * scale if 0 <= index < len(msg.axes) else 0.0
            values.append(0.0 if abs(value) <= self.raw_joy_deadzone else value)
        return values[0], values[1], values[2]

    def _command_cb(self, msg: Any) -> None:
        try:
            if self.command_source == "processed_twist":
                values = self._twist_values(msg)
            elif self.command_source == "active_command":
                values = self._twist_values(msg.twist)
            else:
                values = self._raw_joy_values(msg)
            if not all(math.isfinite(value) for value in values):
                raise ValueError("non-finite command")
        except Exception as exc:
            self.get_logger().warn(f"Ignoring invalid {self.command_source} command: {exc}")
            return
        receive_time_ns = time.time_ns()
        with self._lock:
            self._latest_command = RelayCommand(self.command_source, True, receive_time_ns, *values)
            self._command_received_monotonic_ns = time.monotonic_ns()

    def _server_loop(self) -> None:
        while rclpy.ok() and not self._stop_event.is_set():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    server.bind((self.bind_host, self.port))
                    server.listen(1)
                    self._server_socket = server
                    self.get_logger().info(f"Listening for relay client on {self.bind_host}:{self.port}")
                    while rclpy.ok() and not self._stop_event.is_set():
                        try:
                            client, address = server.accept()
                        except OSError:
                            break
                        with client:
                            client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                            self.get_logger().info(f"Relay client connected from {address[0]}:{address[1]}")
                            with self._lock:
                                self._client_socket = client
                                self._client_address = address
                            try:
                                while rclpy.ok() and not self._stop_event.is_set():
                                    time.sleep(0.5)
                                    if self._client_socket is not client:
                                        break
                            finally:
                                self._clear_client(client)
                                self.get_logger().info("Relay client disconnected")
                        if self._stop_event.is_set():
                            break
            except OSError as exc:
                self.get_logger().error(f"Relay server error: {exc}")
                time.sleep(1.0)
            finally:
                self._server_socket = None

    def _clear_client(self, client: socket.socket | None = None) -> None:
        with self._lock:
            if client is None or self._client_socket is client:
                self._client_socket = None
                self._client_address = None

    def _send_packet(self) -> None:
        with self._lock:
            client = self._client_socket
            joint = self._latest_joint_states
            imu = self._latest_imu
            odom = self._latest_odom
            motors = self._latest_motors_status
            fsm = self._latest_fsm
            fsm_received = self._fsm_received
            command = self._latest_command
            command_received_monotonic_ns = self._command_received_monotonic_ns

        if client is None:
            return

        packet = {
            "schema": SCHEMA_V2 if self.include_command or self.include_fsm else SCHEMA_V1,
            "seq": self._seq,
            "stamp_unix": time.time(),
            "sender_time_ns": time.time_ns(),
            "joint_states": _joint_state_packet(joint),
            "imu": _imu_packet(imu),
            "odom": _odom_packet(odom),
        }
        if self.include_motors_status:
            packet["motors_status"] = _motors_status_packet(motors)
        if self.include_fsm:
            packet["fsm_mode"] = fsm
            packet["fsm_received"] = fsm_received
        if self.include_command:
            command_packet = command_for_transmit(
                command, command_received_monotonic_ns, time.monotonic_ns(), self.command_timeout_sec
            ).as_packet()
            command_packet["sender_age_ms"] = (
                max(time.monotonic_ns() - command_received_monotonic_ns, 0) * 1e-6
                if command_received_monotonic_ns > 0 else -1.0
            )
            packet["command"] = command_packet

        try:
            payload = encode_packet(packet)
        except RelayPacketError as exc:
            self.get_logger().warn(f"Skipping invalid relay snapshot: {exc}")
            return
        try:
            client.sendall(payload)
            self._seq += 1
        except OSError as exc:
            self.get_logger().warn(f"Relay send failed, dropping client: {exc}")
            self._clear_client(client)
            try:
                client.close()
            except OSError:
                pass

    def close(self) -> None:
        self._stop_event.set()
        self._clear_client()
        try:
            if self._server_socket is not None:
                self._server_socket.close()
        except OSError:
            pass

    def destroy_node(self) -> bool:
        self.close()
        return super().destroy_node()


def main(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="TITA state relay sender.")
    parser.add_argument("--tita-ns", default="tita4252763")
    parser.add_argument("--bind-host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=50051)
    parser.add_argument("--send-rate-hz", type=float, default=50.0)
    parser.add_argument("--include-motors-status", action="store_true", default=True)
    raw_args = sys.argv[1:] if args is None else list(args)
    parsed, _ = parser.parse_known_args(raw_args)

    rclpy.init(args=args)
    node = TitaStateRelaySender()
    if any(str(arg).startswith(flag) for flag in ["--tita-ns", "--bind-host", "--port", "--send-rate-hz", "--include-motors-status"] for arg in raw_args):
        node.set_parameters(
            [
                Parameter("tita_ns", Parameter.Type.STRING, parsed.tita_ns),
                Parameter("bind_host", Parameter.Type.STRING, parsed.bind_host),
                Parameter("port", Parameter.Type.INTEGER, parsed.port),
                Parameter("send_rate_hz", Parameter.Type.DOUBLE, parsed.send_rate_hz),
                Parameter("include_motors_status", Parameter.Type.BOOL, bool(parsed.include_motors_status)),
            ]
        )
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.close()
        try:
            node.destroy_node()
        except Exception:
            pass
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
