#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import socket
import sys
import threading
import time
from typing import Any

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.parameter import Parameter
from sensor_msgs.msg import Imu, JointState
from std_msgs.msg import Bool, Float32, String, UInt32

from .relay_protocol import MAX_PACKET_BYTES, RelayPacketError, command_from_packet, decode_packet_line


def _stamp_from_dict(value: dict[str, Any] | None):
    from builtin_interfaces.msg import Time

    stamp = Time()
    if not value:
        return stamp
    stamp.sec = int(value.get("sec", 0))
    stamp.nanosec = int(value.get("nanosec", 0))
    return stamp


def _fill_vector3(target: Any, value: dict[str, Any] | None) -> None:
    if not value:
        return
    target.x = float(value.get("x", 0.0))
    target.y = float(value.get("y", 0.0))
    target.z = float(value.get("z", 0.0))


def _fill_quat(target: Any, value: dict[str, Any] | None) -> None:
    if not value:
        return
    target.x = float(value.get("x", 0.0))
    target.y = float(value.get("y", 0.0))
    target.z = float(value.get("z", 0.0))
    target.w = float(value.get("w", 1.0))


class TitaStateRelayReceiver(Node):
    def __init__(self) -> None:
        super().__init__("tita_state_relay_receiver")
        self.declare_parameter("server_host", "192.168.42.1")
        self.declare_parameter("port", 50051)
        self.declare_parameter("reconnect_sec", 1.0)
        self.declare_parameter("publish_original_namespace_aliases", False)
        self.declare_parameter("relay_ns", "tita_relay")

        self.server_host = str(self.get_parameter("server_host").value).strip()
        self.port = int(self.get_parameter("port").value)
        self.reconnect_sec = float(self.get_parameter("reconnect_sec").value)
        self.publish_original_namespace_aliases = str(self.get_parameter("publish_original_namespace_aliases").value).lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        self.relay_ns = str(self.get_parameter("relay_ns").value).strip("/") or "tita_relay"
        self.relay_prefix = f"/{self.relay_ns}"
        self.original_prefix = "/tita4252763"

        self.joint_pub = self.create_publisher(JointState, f"{self.relay_prefix}/joint_states", 10)
        self.imu_pub = self.create_publisher(Imu, f"{self.relay_prefix}/imu_sensor_broadcaster/imu", 10)
        self.odom_pub = self.create_publisher(Odometry, f"{self.relay_prefix}/chassis/odometry", 10)
        self.imu_canonical_pub = self.create_publisher(Imu, f"{self.relay_prefix}/imu", 10)
        self.odom_canonical_pub = self.create_publisher(Odometry, f"{self.relay_prefix}/odometry", 10)
        self.fsm_pub = self.create_publisher(String, f"{self.relay_prefix}/fsm_mode", 10)
        self.command_pub = self.create_publisher(Twist, f"{self.relay_prefix}/cmd_twist", 10)
        self.command_valid_pub = self.create_publisher(Bool, f"{self.relay_prefix}/command_valid", 10)
        self.command_source_pub = self.create_publisher(String, f"{self.relay_prefix}/command_source", 10)
        self.command_status_pub = self.create_publisher(String, f"{self.relay_prefix}/command_status", 10)
        self.network_latency_pub = self.create_publisher(Float32, f"{self.relay_prefix}/network_latency_ms", 10)
        self.packet_rate_pub = self.create_publisher(Float32, f"{self.relay_prefix}/packet_rate_hz", 10)
        self.reconnect_count_pub = self.create_publisher(UInt32, f"{self.relay_prefix}/reconnect_count", 10)
        self.packet_drop_pub = self.create_publisher(UInt32, f"{self.relay_prefix}/packet_drop_estimate", 10)
        self.motors_status_pub = self.create_publisher(String, f"{self.relay_prefix}/locomotion/motors_status_raw", 10)
        self.state_json_pub = self.create_publisher(String, f"{self.relay_prefix}/state_json", 10)
        self.connection_pub = self.create_publisher(String, f"{self.relay_prefix}/connection_status", 10)

        self.alias_joint_pub = (
            self.create_publisher(JointState, f"{self.original_prefix}/joint_states", 10)
            if self.publish_original_namespace_aliases
            else None
        )
        self.alias_imu_pub = (
            self.create_publisher(Imu, f"{self.original_prefix}/imu_sensor_broadcaster/imu", 10)
            if self.publish_original_namespace_aliases
            else None
        )
        self.alias_odom_pub = (
            self.create_publisher(Odometry, f"{self.original_prefix}/chassis/odometry", 10)
            if self.publish_original_namespace_aliases
            else None
        )

        self._latest_packet: dict[str, Any] | None = None
        self._latest_seq = -1
        self._latest_state_json = ""
        self._connection_state = "connecting"
        self._last_packet_monotonic = 0.0
        self._packet_rate_hz = 0.0
        self._rate_window_start = 0.0
        self._rate_window_count = 0
        self._network_last_seq = -1
        self._reconnect_count = 0
        self._packet_drop_estimate = 0
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._socket: socket.socket | None = None

        self._thread = threading.Thread(target=self._network_loop, daemon=True)
        self._thread.start()
        self._timer = self.create_timer(0.02, self._publish_latest)

        self.get_logger().info(f"Relay receiver connecting to {self.server_host}:{self.port}")
        self.get_logger().info(f"Publishing relay namespace {self.relay_prefix}")

    def _set_status(self, status: str) -> None:
        with self._lock:
            self._connection_state = status

    def _network_loop(self) -> None:
        while rclpy.ok() and not self._stop_event.is_set():
            sock: socket.socket | None = None
            try:
                sock = socket.create_connection((self.server_host, self.port), timeout=5.0)
                sock.settimeout(2.0)
                self._socket = sock
                self._set_status("connected")
                self._reconnect_count += 1
                self.get_logger().info(f"Connected to relay server at {self.server_host}:{self.port}")
                buffer = b""
                while rclpy.ok() and not self._stop_event.is_set():
                    try:
                        chunk = sock.recv(4096)
                    except socket.timeout:
                        continue
                    if not chunk:
                        raise ConnectionError("relay server closed the connection")
                    buffer += chunk
                    if len(buffer) > MAX_PACKET_BYTES and b"\n" not in buffer:
                        raise RelayPacketError("relay receive buffer exceeded maximum packet length")
                    while b"\n" in buffer:
                        line, buffer = buffer.split(b"\n", 1)
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            packet = decode_packet_line(line)
                        except RelayPacketError as exc:
                            self.get_logger().warn(f"Skipping invalid relay packet: {exc}")
                            continue
                        now = time.monotonic()
                        with self._lock:
                            seq = int(packet.get("seq", -1))
                            if self._network_last_seq >= 0 and seq > self._network_last_seq + 1:
                                self._packet_drop_estimate += seq - self._network_last_seq - 1
                            self._network_last_seq = seq
                            if self._rate_window_start <= 0.0:
                                self._rate_window_start = now
                                self._rate_window_count = 1
                            else:
                                self._rate_window_count += 1
                                rate_elapsed = now - self._rate_window_start
                                if rate_elapsed >= 0.5:
                                    self._packet_rate_hz = (self._rate_window_count - 1) / rate_elapsed
                                    self._rate_window_start = now
                                    self._rate_window_count = 1
                            self._last_packet_monotonic = now
                            self._latest_packet = packet
                            self._latest_state_json = json.dumps(packet, separators=(",", ":"))
            except Exception as exc:
                self._set_status(f"disconnected: {exc}")
                self.get_logger().warn(f"Relay connection lost: {exc}")
                time.sleep(max(self.reconnect_sec, 0.1))
            finally:
                self._socket = None
                if sock is not None:
                    try:
                        sock.close()
                    except OSError:
                        pass

    def _publish_latest(self) -> None:
        with self._lock:
            packet = self._latest_packet
            state_json = self._latest_state_json
            status = self._connection_state
            packet_rate_hz = self._packet_rate_hz
            reconnect_count = self._reconnect_count
            drop_estimate = self._packet_drop_estimate

        self.connection_pub.publish(String(data=status))
        self.packet_rate_pub.publish(Float32(data=float(packet_rate_hz)))
        self.reconnect_count_pub.publish(UInt32(data=max(int(reconnect_count), 0)))
        self.packet_drop_pub.publish(UInt32(data=max(int(drop_estimate), 0)))
        if not packet:
            return

        seq = int(packet.get("seq", -1))
        if seq == self._latest_seq:
            return
        self._latest_seq = seq

        self.state_json_pub.publish(String(data=state_json))

        joint_packet = packet.get("joint_states", {})
        if isinstance(joint_packet, dict) and joint_packet.get("available", False):
            joint_msg = JointState()
            joint_msg.header.stamp = _stamp_from_dict(joint_packet.get("header_stamp"))
            joint_msg.header.frame_id = str(joint_packet.get("frame_id", ""))
            joint_msg.name = [str(v) for v in joint_packet.get("name", [])]
            joint_msg.position = [float(v) for v in joint_packet.get("position", [])]
            joint_msg.velocity = [float(v) for v in joint_packet.get("velocity", [])]
            joint_msg.effort = [float(v) for v in joint_packet.get("effort", [])]
            self.joint_pub.publish(joint_msg)
            if self.alias_joint_pub is not None:
                self.alias_joint_pub.publish(joint_msg)

        imu_packet = packet.get("imu", {})
        if isinstance(imu_packet, dict) and imu_packet.get("available", False):
            imu_msg = Imu()
            imu_msg.header.stamp = _stamp_from_dict(imu_packet.get("header_stamp"))
            imu_msg.header.frame_id = str(imu_packet.get("frame_id", ""))
            _fill_quat(imu_msg.orientation, imu_packet.get("orientation"))
            _fill_vector3(imu_msg.angular_velocity, imu_packet.get("angular_velocity"))
            _fill_vector3(imu_msg.linear_acceleration, imu_packet.get("linear_acceleration"))
            self.imu_pub.publish(imu_msg)
            self.imu_canonical_pub.publish(imu_msg)
            if self.alias_imu_pub is not None:
                self.alias_imu_pub.publish(imu_msg)

        odom_packet = packet.get("odom", {})
        if isinstance(odom_packet, dict) and odom_packet.get("available", False):
            odom_msg = Odometry()
            odom_msg.header.stamp = _stamp_from_dict(odom_packet.get("header_stamp"))
            odom_msg.header.frame_id = str(odom_packet.get("frame_id", ""))
            odom_msg.child_frame_id = str(odom_packet.get("child_frame_id", ""))
            pose_packet = odom_packet.get("pose", {})
            twist_packet = odom_packet.get("twist", {})
            _fill_vector3(odom_msg.pose.pose.position, pose_packet.get("position"))
            _fill_quat(odom_msg.pose.pose.orientation, pose_packet.get("orientation"))
            _fill_vector3(odom_msg.twist.twist.linear, twist_packet.get("linear"))
            _fill_vector3(odom_msg.twist.twist.angular, twist_packet.get("angular"))
            self.odom_pub.publish(odom_msg)
            self.odom_canonical_pub.publish(odom_msg)
            if self.alias_odom_pub is not None:
                self.alias_odom_pub.publish(odom_msg)

        motors_packet = packet.get("motors_status")
        if motors_packet is not None:
            self.motors_status_pub.publish(String(data=json.dumps(motors_packet, separators=(",", ":"))))

        if bool(packet.get("fsm_received", False)):
            self.fsm_pub.publish(String(data=str(packet.get("fsm_mode", ""))))

        try:
            command = command_from_packet(packet)
        except RelayPacketError as exc:
            command = command_from_packet({})
            self.get_logger().warn(f"Invalid command payload was zeroed: {exc}")
        twist = Twist()
        twist.linear.x = command.linear_x
        twist.linear.y = command.linear_y
        twist.angular.z = command.angular_z
        self.command_pub.publish(twist)
        self.command_valid_pub.publish(Bool(data=command.valid))
        self.command_source_pub.publish(String(data=command.source))
        self.command_status_pub.publish(String(data=json.dumps({
            "source": command.source,
            "valid": command.valid,
            "receive_time_ns": command.receive_time_ns,
            "receiver_time_ns": time.time_ns(),
            "sender_age_ms": float(packet.get("command", {}).get("sender_age_ms", -1.0)),
            "reconnect_count": reconnect_count,
            "packet_drop_estimate": drop_estimate,
        }, separators=(",", ":"))))
        sender_time_ns = int(packet.get("sender_time_ns", 0))
        latency_ms = (time.time_ns() - sender_time_ns) * 1e-6 if sender_time_ns > 0 else -1.0
        if latency_ms < 0.0 or latency_ms > 60_000.0:
            latency_ms = -1.0  # Sender/receiver clocks are not sufficiently synchronized.
        self.network_latency_pub.publish(Float32(data=float(latency_ms)))

    def destroy_node(self) -> bool:
        self._stop_event.set()
        try:
            if self._socket is not None:
                self._socket.close()
        except OSError:
            pass
        return super().destroy_node()


def main(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="TITA state relay receiver.")
    parser.add_argument("--server-host", default="192.168.42.1")
    parser.add_argument("--port", type=int, default=50051)
    parser.add_argument("--reconnect-sec", type=float, default=1.0)
    parser.add_argument("--publish-original-namespace-aliases", action="store_true", default=False)
    parser.add_argument("--relay-ns", default="tita_relay")
    raw_args = sys.argv[1:] if args is None else list(args)
    parsed, _ = parser.parse_known_args(raw_args)

    rclpy.init(args=args)
    node = TitaStateRelayReceiver()
    if any(str(arg).startswith(flag) for flag in ["--server-host", "--port", "--reconnect-sec", "--publish-original-namespace-aliases", "--relay-ns"] for arg in raw_args):
        node.set_parameters(
            [
                Parameter("server_host", Parameter.Type.STRING, parsed.server_host),
                Parameter("port", Parameter.Type.INTEGER, parsed.port),
                Parameter("reconnect_sec", Parameter.Type.DOUBLE, parsed.reconnect_sec),
                Parameter(
                    "publish_original_namespace_aliases",
                    Parameter.Type.BOOL,
                    bool(parsed.publish_original_namespace_aliases),
                ),
                Parameter("relay_ns", Parameter.Type.STRING, parsed.relay_ns),
            ]
        )
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            node.destroy_node()
        except Exception:
            pass
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
