from __future__ import annotations

import json
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np
import rclpy
import yaml
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import Imu, JointState
from std_msgs.msg import Bool, Float32, Float32MultiArray, String

from .mujoco_env import TitaMujocoEnv
from .obs_builder import quat_wxyz_to_rpy
from .policy_runner import PolicyRunner
from .real_policy_core import (
    LEG_INDICES_NATIVE,
    WHEEL_INDICES_NATIVE,
    RealPolicyEngine,
    RealSnapshot,
    apply_kinematic_preview,
    gate_status,
    native_joint_arrays,
    reset_mujoco_from_snapshot,
)


def _as_bool(value: Any) -> bool:
    return value if isinstance(value, bool) else str(value).lower() in {"1", "true", "yes", "on"}


class TitaRealPolicyGhostNode(Node):
    """Relay sensor -> policy -> MuJoCo-only ghost. It creates no real-robot command publisher."""

    def __init__(self) -> None:
        super().__init__("tita_real_policy_ghost")
        self.declare_parameter("config", "")
        self.declare_parameter("policy_path", "")
        self.declare_parameter("relay_ns", "tita_relay")
        self.declare_parameter("allowed_real_fsm_modes_csv", "balance")
        self.declare_parameter("sensor_timeout_sec", 0.5)
        self.declare_parameter("command_timeout_sec", 0.5)
        self.declare_parameter("expected_command_source", "processed_twist")
        self.declare_parameter("policy_rate_hz", 50.0)
        self.declare_parameter("ghost_rollout_enabled", True)
        self.declare_parameter("ghost_visualization_mode", "auto")
        self.declare_parameter("ghost_horizon_sec", 0.5)
        self.declare_parameter("ghost_reset_rate_hz", 2.0)
        self.declare_parameter("ghost_base_height", 0.4)
        self.declare_parameter("kinematic_initial_hold_sec", 1.0)
        self.declare_parameter("viewer", True)
        self.declare_parameter("headless", False)
        self.declare_parameter("publish_debug", True)

        config_path = str(self.get_parameter("config").value).strip()
        if not config_path:
            raise RuntimeError("config parameter is required")
        with Path(config_path).expanduser().open("r", encoding="utf-8") as stream:
            self.cfg = yaml.safe_load(stream)
        policy_path = str(self.get_parameter("policy_path").value).strip()
        if policy_path:
            self.cfg["policy"]["path"] = policy_path
        self.relay_ns = str(self.get_parameter("relay_ns").value).strip("/") or "tita_relay"
        self.allowed_modes = {
            value.strip().lower()
            for value in str(self.get_parameter("allowed_real_fsm_modes_csv").value).split(",")
            if value.strip()
        }
        self.sensor_timeout = max(float(self.get_parameter("sensor_timeout_sec").value), 0.0)
        self.command_timeout = max(float(self.get_parameter("command_timeout_sec").value), 0.0)
        self.expected_command_source = str(self.get_parameter("expected_command_source").value).strip()
        rollout_enabled = _as_bool(self.get_parameter("ghost_rollout_enabled").value)
        requested_mode = str(self.get_parameter("ghost_visualization_mode").value).strip().lower()
        self.ghost_mode = ("rollout" if rollout_enabled else "instantaneous") if requested_mode == "auto" else requested_mode
        if self.ghost_mode not in {"instantaneous", "kinematic_preview", "rollout"}:
            raise ValueError(
                "ghost_visualization_mode must be instantaneous, kinematic_preview, rollout, or auto"
            )
        self.ghost_horizon = max(float(self.get_parameter("ghost_horizon_sec").value), 0.02)
        reset_rate = max(float(self.get_parameter("ghost_reset_rate_hz").value), 0.1)
        self.ghost_reset_period = 1.0 / reset_rate
        self.ghost_base_height = float(self.get_parameter("ghost_base_height").value)
        if not np.isfinite(self.ghost_base_height) or self.ghost_base_height <= 0.0:
            raise ValueError("ghost_base_height must be finite and positive")
        self.kinematic_initial_hold = max(
            float(self.get_parameter("kinematic_initial_hold_sec").value), 0.0
        )
        self.publish_debug = _as_bool(self.get_parameter("publish_debug").value)
        viewer = _as_bool(self.get_parameter("viewer").value) and not _as_bool(self.get_parameter("headless").value)

        self.policy = PolicyRunner.from_config(self.cfg)
        self.instant_engine = RealPolicyEngine(self.cfg, self.policy)
        self.ghost_engine = RealPolicyEngine(self.cfg, self.policy)
        self.env = TitaMujocoEnv(self.cfg, viewer_enabled=viewer)
        self.latest_joint: JointState | None = None
        self.latest_imu: Imu | None = None
        self.latest_odom: Odometry | None = None
        self.latest_command = np.zeros(3, dtype=np.float32)
        self.command_valid = False
        self.command_source = "none"
        self.command_sender_age_ms = -1.0
        self.fsm_mode = ""
        self.fsm_received = False
        self.connected = False
        self.received_at: dict[str, float] = {}
        self.ghost_command = np.zeros(3, dtype=np.float32)
        self.ghost_started = 0.0
        self.ghost_last_reset = 0.0
        self.ghost_start_pos = np.zeros(3, dtype=np.float32)
        self.ghost_reset_count = 0
        self.kinematic_initialized = False
        self.kinematic_initial_leg_pos = np.zeros(6, dtype=np.float32)
        self.last_log = 0.0
        self.last_tick = time.monotonic()
        self.effective_policy_rate_hz = 0.0

        prefix = f"/{self.relay_ns}"
        self.create_subscription(JointState, f"{prefix}/joint_states", self._joint_cb, 10)
        self.create_subscription(Imu, f"{prefix}/imu", self._imu_cb, 10)
        self.create_subscription(Odometry, f"{prefix}/odometry", self._odom_cb, 10)
        self.create_subscription(String, f"{prefix}/fsm_mode", self._fsm_cb, 10)
        self.create_subscription(Twist, f"{prefix}/cmd_twist", self._command_cb, 10)
        self.create_subscription(Bool, f"{prefix}/command_valid", self._command_valid_cb, 10)
        self.create_subscription(String, f"{prefix}/command_source", self._command_source_cb, 10)
        self.create_subscription(String, f"{prefix}/command_status", self._command_status_cb, 10)
        self.create_subscription(String, f"{prefix}/connection_status", self._connection_cb, 10)

        base = "/cosim_ros2_jazzy/real_policy"
        self.pubs = {
            "obs": self.create_publisher(Float32MultiArray, f"{base}/obs_current", 10),
            "history": self.create_publisher(Float32MultiArray, f"{base}/obs_history_flat", 10),
            "command": self.create_publisher(Float32MultiArray, f"{base}/command", 10),
            "command_valid": self.create_publisher(Bool, f"{base}/command_valid", 10),
            "action_raw": self.create_publisher(Float32MultiArray, f"{base}/action_raw", 10),
            "action_scaled": self.create_publisher(Float32MultiArray, f"{base}/action_scaled", 10),
            "leg_target": self.create_publisher(Float32MultiArray, f"{base}/virtual_leg_target_native", 10),
            "wheel_target": self.create_publisher(Float32MultiArray, f"{base}/virtual_wheel_vel_native", 10),
            "leg_delta": self.create_publisher(Float32MultiArray, f"{base}/leg_target_delta_native", 10),
            "clipping": self.create_publisher(Float32MultiArray, f"{base}/clipping_mask_native", 10),
            "inference": self.create_publisher(Float32, f"{base}/inference_time_ms", 10),
            "policy_rate": self.create_publisher(Float32, f"{base}/effective_policy_rate_hz", 10),
            "sensor_age": self.create_publisher(Float32MultiArray, f"{base}/sensor_age_ms", 10),
            "command_age": self.create_publisher(Float32, f"{base}/command_age_ms", 10),
            "status": self.create_publisher(String, f"{base}/status", 10),
            "ghost_metrics": self.create_publisher(String, f"{base}/ghost_metrics", 10),
        }
        rate = max(float(self.get_parameter("policy_rate_hz").value), 1.0)
        self.timer = self.create_timer(1.0 / rate, self._tick)
        self.get_logger().warn("COMMAND OUTPUT: DISABLED — policy torque is connected only to local MuJoCo")

    def _mark(self, key: str) -> None:
        self.received_at[key] = time.monotonic()

    def _joint_cb(self, msg: JointState) -> None:
        self.latest_joint = msg
        self._mark("joint")

    def _imu_cb(self, msg: Imu) -> None:
        self.latest_imu = msg
        self._mark("imu")

    def _odom_cb(self, msg: Odometry) -> None:
        self.latest_odom = msg
        self._mark("odom")

    def _fsm_cb(self, msg: String) -> None:
        self.fsm_mode = str(msg.data).strip().lower()
        self.fsm_received = True

    def _command_cb(self, msg: Twist) -> None:
        command = np.asarray([msg.linear.x, msg.linear.y, msg.angular.z], dtype=np.float32)
        if np.all(np.isfinite(command)):
            self.latest_command = command
            self._mark("command")

    def _command_valid_cb(self, msg: Bool) -> None:
        self.command_valid = bool(msg.data)

    def _command_source_cb(self, msg: String) -> None:
        self.command_source = str(msg.data)

    def _command_status_cb(self, msg: String) -> None:
        try:
            self.command_sender_age_ms = float(json.loads(msg.data).get("sender_age_ms", -1.0))
        except (ValueError, TypeError, json.JSONDecodeError):
            self.command_sender_age_ms = -1.0

    def _connection_cb(self, msg: String) -> None:
        self.connected = str(msg.data).startswith("connected")

    def _fresh(self, key: str, now: float, timeout: float) -> bool:
        return key in self.received_at and now - self.received_at[key] <= timeout

    def _snapshot(self) -> RealSnapshot:
        if self.latest_joint is None or self.latest_imu is None or self.latest_odom is None:
            raise ValueError("sensor snapshot incomplete")
        pos, vel = native_joint_arrays(
            list(self.latest_joint.name), list(self.latest_joint.position), list(self.latest_joint.velocity)
        )
        q = self.latest_imu.orientation
        quat = np.asarray([q.w, q.x, q.y, q.z], dtype=np.float32)
        norm = float(np.linalg.norm(quat))
        if not np.isfinite(norm) or norm < 1e-6:
            raise ValueError("invalid IMU quaternion")
        quat /= norm
        w = self.latest_imu.angular_velocity
        p = self.latest_odom.pose.pose.position
        v = self.latest_odom.twist.twist.linear
        snapshot = RealSnapshot(
            pos, vel, quat, np.asarray([w.x, w.y, w.z], dtype=np.float32),
            np.asarray([p.x, p.y, p.z], dtype=np.float32),
            np.asarray([v.x, v.y, v.z], dtype=np.float32),
        )
        if not all(np.all(np.isfinite(value)) for value in snapshot.__dict__.values()):
            raise ValueError("non-finite sensor snapshot")
        return snapshot

    def _ghost_snapshot(self) -> RealSnapshot:
        return RealSnapshot(
            self.env.joint_pos(), self.env.joint_vel(), self.env.base_quat_sensor(),
            self.env.base_ang_vel(), self.env.base_pos(), self.env.base_lin_vel(),
        )

    def _reset_ghost(self, snapshot: RealSnapshot, command: np.ndarray, now: float) -> None:
        # TITA odometry reports planar z=0; that is not the MuJoCo free-base height.
        # Preserve measured x/y and orientation, but use an explicit simulation-only height.
        ghost_base_pos = snapshot.base_pos.copy()
        ghost_base_pos[2] = self.ghost_base_height
        ghost_snapshot = replace(snapshot, base_pos=ghost_base_pos)
        reset_mujoco_from_snapshot(self.env, ghost_snapshot)
        self.ghost_engine.reset(ghost_snapshot, command)
        self.ghost_command = command.copy()
        self.ghost_started = now
        self.ghost_last_reset = now
        self.ghost_start_pos = ghost_snapshot.base_pos.copy()
        self.ghost_reset_count += 1

    def _initialize_kinematic_preview(
        self, snapshot: RealSnapshot, command: np.ndarray, now: float
    ) -> None:
        self._reset_ghost(snapshot, command, now)
        self.kinematic_initial_leg_pos = snapshot.joint_pos_native[LEG_INDICES_NATIVE].copy()
        self.kinematic_initialized = True

    @staticmethod
    def _array(values: np.ndarray) -> Float32MultiArray:
        return Float32MultiArray(data=np.asarray(values, dtype=np.float32).reshape(-1).astype(float).tolist())

    def _publish_frame(self, frame, snapshot, command_valid, inference_ms, status, now) -> None:
        if not self.publish_debug:
            return
        clip = np.abs(frame.action_debug.action_used_by_joint - frame.action_debug.action_raw_by_joint) > 0.0
        self.pubs["obs"].publish(self._array(frame.obs_current))
        self.pubs["history"].publish(self._array(frame.obs_history))
        self.pubs["command"].publish(self._array(frame.command))
        self.pubs["command_valid"].publish(Bool(data=command_valid))
        self.pubs["action_raw"].publish(self._array(frame.action_policy))
        self.pubs["action_scaled"].publish(self._array(frame.action_debug.action_scaled_by_joint))
        self.pubs["leg_target"].publish(self._array(frame.virtual_leg_target_native))
        self.pubs["wheel_target"].publish(self._array(frame.virtual_wheel_vel_native))
        self.pubs["leg_delta"].publish(self._array(
            frame.virtual_leg_target_native - snapshot.joint_pos_native[LEG_INDICES_NATIVE]
        ))
        self.pubs["clipping"].publish(self._array(clip.astype(np.float32)))
        self.pubs["inference"].publish(Float32(data=float(inference_ms)))
        self.pubs["policy_rate"].publish(Float32(data=float(self.effective_policy_rate_hz)))
        self.pubs["sensor_age"].publish(self._array(np.asarray([
            (now - self.received_at.get(key, now)) * 1000.0 for key in ("joint", "imu", "odom")
        ], dtype=np.float32)))
        self.pubs["command_age"].publish(Float32(data=float(self.command_sender_age_ms)))
        self.pubs["status"].publish(String(data=status))

    def _tick(self) -> None:
        now = time.monotonic()
        tick_dt = max(now - self.last_tick, 1e-6)
        self.last_tick = now
        self.effective_policy_rate_hz = 1.0 / tick_dt
        received = self.latest_joint is not None and self.latest_imu is not None and self.latest_odom is not None
        fresh = all(self._fresh(key, now, self.sensor_timeout) for key in ("joint", "imu", "odom"))
        try:
            snapshot = self._snapshot() if received else None
            finite = snapshot is not None
        except ValueError as exc:
            snapshot = None
            finite = False
            sensor_error = str(exc)
        status = gate_status(
            sensor_received=received, sensors_fresh=fresh, values_finite=finite,
            fsm_received=self.fsm_received, fsm_mode=self.fsm_mode,
            allowed_modes=self.allowed_modes, connected=self.connected,
        )
        if not status.startswith("ready:") or snapshot is None:
            self.instant_engine.history_initialized = False
            self.ghost_engine.history_initialized = False
            self.kinematic_initialized = False
            if self.publish_debug:
                detail = f"{status}:{sensor_error}" if not finite and received else status
                self.pubs["status"].publish(String(data=detail))
                self.pubs["command_valid"].publish(Bool(data=False))
            return

        command_fresh = self._fresh("command", now, self.command_timeout)
        command_valid = (
            self.command_valid and command_fresh
            and (not self.expected_command_source or self.command_source == self.expected_command_source)
        )
        command = self.latest_command.copy() if command_valid else np.zeros(3, dtype=np.float32)
        suffix = "" if command_valid else ":command_stale_zeroed"
        started = time.perf_counter()
        try:
            frame = self.instant_engine.step(snapshot, command)
            inference_ms = (time.perf_counter() - started) * 1000.0
            if self.ghost_mode == "rollout":
                if (
                    self.ghost_last_reset == 0.0
                    or now - self.ghost_last_reset >= self.ghost_reset_period
                    or now - self.ghost_started >= self.ghost_horizon
                ):
                    self._reset_ghost(snapshot, command, now)
                ghost_snapshot = self._ghost_snapshot()
                ghost_frame = self.ghost_engine.step(ghost_snapshot, self.ghost_command)
                action_native = ghost_frame.action_native.copy()

                def torque_callback(joint_pos, joint_vel):
                    torque, _ = self.ghost_engine.action_adapter.compute(action_native, joint_pos, joint_vel)
                    return torque

                self.env.step_with_torque_callback(torque_callback, sleep=False)
            elif self.ghost_mode == "instantaneous":
                self._reset_ghost(snapshot, command, now)
                if self.env.viewer is not None:
                    self.env.viewer.sync()
            else:
                if not self.kinematic_initialized:
                    # Make the first visible pose the current real joint snapshot. Policy
                    # targets begin on the following control cycle so the initial jump is explicit.
                    self._initialize_kinematic_preview(snapshot, command, now)
                    if self.env.viewer is not None:
                        self.env.viewer.sync()
                elif now - self.ghost_started >= self.kinematic_initial_hold:
                    apply_kinematic_preview(self.env, frame, min(tick_dt, 0.1))
                    if self.env.viewer is not None:
                        self.env.viewer.sync()
            displacement = self.env.base_pos() - self.ghost_start_pos
            rpy = quat_wxyz_to_rpy(self.env.base_quat_sensor())
            metrics = {
                "visualization_mode": self.ghost_mode,
                "reset_count": self.ghost_reset_count,
                "rollout_duration": max(now - self.ghost_started, 0.0),
                "base_displacement": displacement.astype(float).tolist(),
                "base_roll_pitch_yaw": rpy.astype(float).tolist(),
                "wheel_velocity": self.env.joint_vel()[WHEEL_INDICES_NATIVE].astype(float).tolist(),
                "contact_count": int(self.env.data.ncon),
                "fall_suspected": bool(
                    displacement[2] < -0.10 or abs(float(rpy[0])) > 0.7 or abs(float(rpy[1])) > 0.7
                ),
            }
            if self.ghost_mode == "kinematic_preview":
                initial_delta = frame.virtual_leg_target_native - self.kinematic_initial_leg_pos
                metrics.update({
                    "initial_leg_position": self.kinematic_initial_leg_pos.astype(float).tolist(),
                    "policy_leg_target": frame.virtual_leg_target_native.astype(float).tolist(),
                    "initial_leg_target_delta": initial_delta.astype(float).tolist(),
                    "max_abs_initial_leg_target_delta": float(np.max(np.abs(initial_delta))),
                    "initial_hold_remaining_sec": float(max(
                        self.kinematic_initial_hold - (now - self.ghost_started), 0.0
                    )),
                })
            self.pubs["ghost_metrics"].publish(String(data=json.dumps(metrics, separators=(",", ":"))))
            self._publish_frame(
                frame, snapshot, command_valid, inference_ms,
                f"ready:real_policy_ghost:{self.ghost_mode}{suffix}", now
            )
            if now - self.last_log >= 1.0:
                self.last_log = now
                self.get_logger().info(
                    f"cmd={command.tolist()} valid={command_valid} action={frame.action_policy.tolist()} "
                    f"inference_ms={inference_ms:.3f} ghost_reset={self.ghost_reset_count}"
                )
        except Exception as exc:
            self.instant_engine.history_initialized = False
            self.ghost_engine.history_initialized = False
            self.pubs["status"].publish(String(data=f"blocked:policy_or_ghost_error:{exc}"))

    def destroy_node(self) -> bool:
        self.env.close()
        return super().destroy_node()


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = TitaRealPolicyGhostNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except RuntimeError as exc:
        if "Unable to convert call argument to Python object" not in str(exc):
            raise
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
