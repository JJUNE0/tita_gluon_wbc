from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any


SCHEMA_V1 = "tita_state_relay.v1"
SCHEMA_V2 = "tita_state_relay.v2"
MAX_PACKET_BYTES = 1_048_576


class RelayPacketError(ValueError):
    pass


@dataclass(frozen=True)
class RelayCommand:
    source: str
    valid: bool
    receive_time_ns: int
    linear_x: float
    linear_y: float
    angular_z: float

    def as_packet(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "valid": self.valid,
            "receive_time_ns": self.receive_time_ns,
            "linear_x": self.linear_x,
            "linear_y": self.linear_y,
            "angular_z": self.angular_z,
        }


def finite_float(value: Any, field: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise RelayPacketError(f"{field} is not numeric") from exc
    if not math.isfinite(result):
        raise RelayPacketError(f"{field} is not finite")
    return result


def command_from_packet(packet: dict[str, Any]) -> RelayCommand:
    value = packet.get("command")
    if value is None:
        return RelayCommand("none", False, 0, 0.0, 0.0, 0.0)
    if not isinstance(value, dict):
        raise RelayPacketError("command must be an object")
    source = str(value.get("source", "none"))
    valid = bool(value.get("valid", False))
    receive_time_ns = int(value.get("receive_time_ns", 0))
    xyz = (
        finite_float(value.get("linear_x", 0.0), "command.linear_x"),
        finite_float(value.get("linear_y", 0.0), "command.linear_y"),
        finite_float(value.get("angular_z", 0.0), "command.angular_z"),
    )
    if not valid:
        xyz = (0.0, 0.0, 0.0)
    return RelayCommand(source, valid, receive_time_ns, *xyz)


def command_for_transmit(
    command: RelayCommand, received_monotonic_ns: int, now_monotonic_ns: int, timeout_sec: float
) -> RelayCommand:
    age_sec = (int(now_monotonic_ns) - int(received_monotonic_ns)) * 1e-9
    valid = command.valid and received_monotonic_ns > 0 and 0.0 <= age_sec <= max(float(timeout_sec), 0.0)
    return RelayCommand(
        command.source, valid, command.receive_time_ns,
        command.linear_x if valid else 0.0,
        command.linear_y if valid else 0.0,
        command.angular_z if valid else 0.0,
    )


def decode_packet_line(line: bytes, max_packet_bytes: int = MAX_PACKET_BYTES) -> dict[str, Any]:
    if not line or len(line) > max_packet_bytes:
        raise RelayPacketError("empty or oversized relay packet")
    try:
        packet = json.loads(line.decode("utf-8"), parse_constant=lambda value: (_ for _ in ()).throw(
            RelayPacketError(f"invalid JSON constant {value}")
        ))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RelayPacketError(f"malformed relay packet: {exc}") from exc
    if not isinstance(packet, dict):
        raise RelayPacketError("relay packet root must be an object")
    schema = str(packet.get("schema", SCHEMA_V1))
    if schema not in {SCHEMA_V1, SCHEMA_V2}:
        raise RelayPacketError(f"unsupported relay schema: {schema}")
    _validate_sensor_payloads(packet)
    command_from_packet(packet)
    return packet


def _validate_sensor_payloads(packet: dict[str, Any]) -> None:
    joint = packet.get("joint_states", {})
    if isinstance(joint, dict) and joint.get("available", False):
        for field in ("position", "velocity", "effort"):
            values = joint.get(field, [])
            if not isinstance(values, list):
                raise RelayPacketError(f"joint_states.{field} must be an array")
            for index, value in enumerate(values):
                finite_float(value, f"joint_states.{field}[{index}]")
    imu = packet.get("imu", {})
    if isinstance(imu, dict) and imu.get("available", False):
        for field, keys in (("orientation", ("x", "y", "z", "w")),
                            ("angular_velocity", ("x", "y", "z")),
                            ("linear_acceleration", ("x", "y", "z"))):
            value = imu.get(field, {})
            if not isinstance(value, dict):
                raise RelayPacketError(f"imu.{field} must be an object")
            for key in keys:
                finite_float(value.get(key, 1.0 if key == "w" else 0.0), f"imu.{field}.{key}")
    odom = packet.get("odom", {})
    if isinstance(odom, dict) and odom.get("available", False):
        paths = (
            ("pose", "position", ("x", "y", "z")),
            ("pose", "orientation", ("x", "y", "z", "w")),
            ("twist", "linear", ("x", "y", "z")),
            ("twist", "angular", ("x", "y", "z")),
        )
        for first, second, keys in paths:
            value = odom.get(first, {}).get(second, {})
            if not isinstance(value, dict):
                raise RelayPacketError(f"odom.{first}.{second} must be an object")
            for key in keys:
                finite_float(value.get(key, 1.0 if key == "w" else 0.0), f"odom.{first}.{second}.{key}")


def encode_packet(packet: dict[str, Any]) -> bytes:
    try:
        payload = json.dumps(packet, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"
    except (TypeError, ValueError) as exc:
        raise RelayPacketError(f"packet is not finite/serializable: {exc}") from exc
    if len(payload) > MAX_PACKET_BYTES:
        raise RelayPacketError("relay packet exceeds maximum length")
    return payload
