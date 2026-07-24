from __future__ import annotations

import math
from pathlib import Path
import time
from typing import Any

import numpy as np
import rclpy
from diagnostic_msgs.msg import DiagnosticArray
from nav_msgs.msg import Odometry
from rclpy.exceptions import ParameterUninitializedException
from rclpy.node import Node
from rclpy.parameter import Parameter
from sensor_msgs.msg import Imu, JointState
from std_msgs.msg import Bool, Float32, Float32MultiArray, String

from .action_adapter import DryRunActionAdapter
from .async_step_logger import (
    AsyncStepLogger,
    LogRecord,
    finite_tuple,
    sha256_file,
    sha256_source_tree,
    zero_vector,
)
from .onnx_policy_runner import OnnxPolicyRunner
from .policy_gate import PolicyDryRunGate
from .real_obs_builder import RealObservationBuilder
from .safety_gate import SafetyGate


def _as_bool(value: Any) -> bool:
    return value if isinstance(value, bool) else str(value).lower() in {"1", "true", "yes", "on"}


class TitaDryRunNode(Node):
    """Read-only sensor-to-policy pipeline. No robot command publisher is created."""

    def __init__(self) -> None:
        super().__init__("tita_lowlevel_dryrun")
        self.declare_parameter("tita_ns", "tita4252763")
        self.declare_parameter("policy_path", "/home/robot/tita_policy/policy.onnx")
        self.declare_parameter("policy_enabled", True)
        self.declare_parameter("policy_required", False)
        self.declare_parameter("rate_hz", 50.0)
        self.declare_parameter("history_len", 10)
        self.declare_parameter("obs_dim", 33)
        self.declare_parameter("publish_debug", True)
        self.declare_parameter("command_enabled", False)
        self.declare_parameter("allow_command_output", False)
        self.declare_parameter("require_motors_status", True)
        self.declare_parameter("require_fsm_mode", True)
        self.declare_parameter("policy_fsm_gate_enabled", True)
        # Empty lists are inferred as BYTE_ARRAY by rclpy on ROS 2 Humble unless the
        # intended type is explicit. Keep the fail-closed empty default as STRING_ARRAY.
        self.declare_parameter("allowed_policy_fsm_modes", Parameter.Type.STRING_ARRAY)
        self.declare_parameter("fsm_timeout_sec", 0.5)
        self.declare_parameter("require_fsm_freshness", True)
        self.declare_parameter("fsm_settle_time_sec", 2.0)
        self.declare_parameter("require_pose_gate", True)
        self.declare_parameter("require_motion_gate", True)
        self.declare_parameter("max_leg_position_error_rad", 0.35)
        self.declare_parameter("max_base_angular_velocity_rad_s", 0.5)
        self.declare_parameter("max_projected_gravity_norm_error", 0.15)
        self.declare_parameter("message_timeout_sec", 0.5)
        self.declare_parameter("max_abs_leg_delta_rad", 0.25)
        self.declare_parameter("max_abs_wheel_vel_rad_s", 5.0)
        self.declare_parameter("step_logger_enabled", True)
        self.declare_parameter("step_logger_output_root", "/home/robot/lowlevel_ws/runs")
        self.declare_parameter("step_logger_queue_size", 1024)
        self.declare_parameter("step_logger_event_queue_size", 256)
        self.declare_parameter("step_logger_history_sec", 5.0)
        self.declare_parameter("step_logger_post_fault_sec", 1.0)
        self.declare_parameter("step_logger_test_label", "command_free_dryrun")

        self.tita_ns = str(self.get_parameter("tita_ns").value).strip("/")
        self.policy_enabled = _as_bool(self.get_parameter("policy_enabled").value)
        self.policy_required = _as_bool(self.get_parameter("policy_required").value)
        self.publish_debug = _as_bool(self.get_parameter("publish_debug").value)
        self.require_motors_status = _as_bool(self.get_parameter("require_motors_status").value)
        self.require_fsm_mode = _as_bool(self.get_parameter("require_fsm_mode").value)
        self.policy_fsm_gate_enabled = _as_bool(self.get_parameter("policy_fsm_gate_enabled").value)
        self.require_fsm_freshness = _as_bool(self.get_parameter("require_fsm_freshness").value)
        self.timeout_sec = float(self.get_parameter("message_timeout_sec").value)
        rate_hz = max(float(self.get_parameter("rate_hz").value), 1.0)
        obs_dim = int(self.get_parameter("obs_dim").value)
        history_len = int(self.get_parameter("history_len").value)
        command_enabled = _as_bool(self.get_parameter("command_enabled").value)
        allow_command_output = _as_bool(self.get_parameter("allow_command_output").value)

        self.obs_builder = RealObservationBuilder(obs_dim=obs_dim, history_len=history_len)
        self.action_adapter = DryRunActionAdapter(
            max_abs_leg_delta_rad=float(self.get_parameter("max_abs_leg_delta_rad").value),
            max_abs_wheel_vel_rad_s=float(self.get_parameter("max_abs_wheel_vel_rad_s").value),
        )
        self.safety_gate = SafetyGate(command_enabled, allow_command_output)
        # Humble leaves an explicitly typed empty array uninitialized when an empty
        # YAML list overrides it. Preserve the fail-closed empty-list default.
        try:
            allowed_modes_parameter = self.get_parameter("allowed_policy_fsm_modes")
            allowed_modes = list(allowed_modes_parameter.value)
        except ParameterUninitializedException:
            allowed_modes = []
        self.policy_gate = PolicyDryRunGate(
            allowed_modes=allowed_modes,
            fsm_timeout_sec=float(self.get_parameter("fsm_timeout_sec").value),
            require_fsm_freshness=self.require_fsm_freshness,
            fsm_settle_time_sec=float(self.get_parameter("fsm_settle_time_sec").value),
            require_pose_gate=_as_bool(self.get_parameter("require_pose_gate").value),
            require_motion_gate=_as_bool(self.get_parameter("require_motion_gate").value),
            max_leg_position_error_rad=float(self.get_parameter("max_leg_position_error_rad").value),
            max_base_angular_velocity_rad_s=float(
                self.get_parameter("max_base_angular_velocity_rad_s").value
            ),
            max_projected_gravity_norm_error=float(
                self.get_parameter("max_projected_gravity_norm_error").value
            ),
        )
        self.policy = OnnxPolicyRunner(str(self.get_parameter("policy_path").value), obs_dim, history_len)
        if self.policy_enabled and not self.policy.status.loaded and self.policy_required:
            raise RuntimeError(f"policy_required=true but ONNX is unavailable: {self.policy.status.detail}")

        prefix = f"/{self.tita_ns}"
        self.latest_joint: JointState | None = None
        self.latest_imu: Imu | None = None
        self.latest_odom: Odometry | None = None
        self.latest_motors: DiagnosticArray | None = None
        self.latest_fsm: String | None = None
        self.received_at: dict[str, float] = {}
        self.last_tick = time.monotonic()
        self.effective_rate_hz = 0.0
        self.sequence = 0
        self._log_status = "INIT"
        self._last_logged_status = ""
        self._logger_failure_reported = False
        self._reset_log_step()

        policy_path = str(self.get_parameter("policy_path").value)
        package_root = Path(__file__).resolve().parents[1]
        try:
            policy_sha256 = sha256_file(policy_path)
        except OSError:
            policy_sha256 = "unavailable"
        try:
            source_sha256 = sha256_source_tree(package_root)
        except OSError:
            source_sha256 = "unavailable"
        logger_config = {
            "rate_hz": rate_hz,
            "history_len": history_len,
            "obs_dim": obs_dim,
            "command_enabled": command_enabled,
            "allow_command_output": allow_command_output,
            "max_abs_leg_delta_rad": float(self.get_parameter("max_abs_leg_delta_rad").value),
            "max_abs_wheel_vel_rad_s": float(self.get_parameter("max_abs_wheel_vel_rad_s").value),
            "allowed_policy_fsm_modes": allowed_modes,
        }
        logger_metadata = {
            "policy_path": policy_path,
            "policy_sha256": policy_sha256,
            "package_source_sha256": source_sha256,
            "robot_namespace": prefix,
            "native_joint_order": [
                "L1", "L2", "L3", "L4", "R1", "R2", "R3", "R4"
            ],
            "policy_joint_order": [
                "L1", "R1", "L2", "R2", "L3", "R3", "L4", "R4"
            ],
            "action_scales_native": self.action_adapter.action_scales_native.astype(float).tolist(),
            "configured_limits": {
                "max_abs_leg_delta_rad": logger_config["max_abs_leg_delta_rad"],
                "max_abs_wheel_vel_rad_s": logger_config["max_abs_wheel_vel_rad_s"],
            },
            "command_source": "zero_default_no_processed_command_subscription",
            "fsm": "event_driven_runtime_value",
            "command_output_enabled": False,
        }
        self.step_logger = AsyncStepLogger(
            str(self.get_parameter("step_logger_output_root").value),
            logger_metadata,
            logger_config,
            enabled=_as_bool(self.get_parameter("step_logger_enabled").value),
            queue_size=int(self.get_parameter("step_logger_queue_size").value),
            event_queue_size=int(self.get_parameter("step_logger_event_queue_size").value),
            history_seconds=float(self.get_parameter("step_logger_history_sec").value),
            expected_rate_hz=rate_hz,
            post_fault_seconds=float(self.get_parameter("step_logger_post_fault_sec").value),
            test_label=str(self.get_parameter("step_logger_test_label").value),
        )

        self.create_subscription(JointState, f"{prefix}/joint_states", self._joint_cb, 10)
        self.create_subscription(Imu, f"{prefix}/imu_sensor_broadcaster/imu", self._imu_cb, 10)
        self.create_subscription(Odometry, f"{prefix}/chassis/odometry", self._odom_cb, 10)
        self.create_subscription(DiagnosticArray, f"{prefix}/locomotion/motors_status", self._motors_cb, 10)
        self.create_subscription(String, f"{prefix}/locomotion/body/fsm_mode", self._fsm_cb, 10)

        base = "/tita_lowlevel/dryrun"
        self.obs_pub = self.create_publisher(Float32MultiArray, f"{base}/obs_current", 10)
        self.history_pub = self.create_publisher(Float32MultiArray, f"{base}/obs_history_flat", 10)
        self.gravity_pub = self.create_publisher(Float32MultiArray, f"{base}/projected_gravity", 10)
        self.action_raw_pub = self.create_publisher(Float32MultiArray, f"{base}/action_raw", 10)
        self.action_scaled_pub = self.create_publisher(Float32MultiArray, f"{base}/action_scaled", 10)
        self.virtual_target_pub = self.create_publisher(Float32MultiArray, f"{base}/virtual_joint_target_native", 10)
        self.virtual_leg_pub = self.create_publisher(Float32MultiArray, f"{base}/virtual_leg_target_native", 10)
        self.virtual_wheel_pub = self.create_publisher(Float32MultiArray, f"{base}/virtual_wheel_vel_native", 10)
        self.target_type_mask_pub = self.create_publisher(
            Float32MultiArray, f"{base}/virtual_target_type_mask_native", 10
        )
        self.action_valid_pub = self.create_publisher(Bool, f"{base}/action_valid", 10)
        self.max_action_pub = self.create_publisher(Float32, f"{base}/max_abs_action_raw", 10)
        self.inference_pub = self.create_publisher(Float32, f"{base}/inference_time_ms", 10)
        self.loop_pub = self.create_publisher(Float32, f"{base}/loop_time_ms", 10)
        self.rate_pub = self.create_publisher(Float32, f"{base}/effective_rate_hz", 10)
        self.safety_ok_pub = self.create_publisher(Bool, f"{base}/safety_ok", 10)
        self.safety_status_pub = self.create_publisher(String, f"{base}/safety_status", 10)
        self.status_pub = self.create_publisher(String, f"{base}/status", 10)

        self.timer = self.create_timer(1.0 / rate_hz, self._tick_logged)
        self.get_logger().info(f"[DRYRUN] started at {rate_hz:.1f} Hz for namespace {prefix}")
        self.get_logger().info(f"[POLICY] {self.policy.status.detail}")
        self.get_logger().warn("[COMMAND] OUTPUT DISABLED: no robot command publisher exists in this node")
        if self.step_logger.enabled:
            self.step_logger.event("lifecycle_transition", "INIT->PRECHECK", sequence=0)
            self.get_logger().info(f"[LOGGER] asynchronous step log: {self.step_logger.run_dir}")
        elif self.step_logger.failed:
            self.get_logger().error(f"[LOGGER] {self.step_logger.writer_error}; controller remains command-free")

    def _reset_log_step(self) -> None:
        self._log_joint_pos = zero_vector(8)
        self._log_joint_vel = zero_vector(8)
        self._log_imu_quat = zero_vector(4)
        self._log_ang_vel = zero_vector(3)
        self._log_gravity = zero_vector(3)
        self._log_obs = zero_vector(33)
        self._log_action_raw = zero_vector(8)
        self._log_action_scaled = zero_vector(8)
        self._log_leg_target = zero_vector(6)
        self._log_wheel_target = zero_vector(2)
        self._log_clipping_mask = zero_vector(8)
        self._log_safety_ok = False
        self._log_loop_ms = 0.0
        self._log_inference_ms = 0.0
        self._log_fault_code = ""

    def _received(self, key: str) -> None:
        self.received_at[key] = time.monotonic()

    def _joint_cb(self, msg: JointState) -> None:
        self.latest_joint = msg
        self._received("joint")

    def _imu_cb(self, msg: Imu) -> None:
        self.latest_imu = msg
        self._received("imu")

    def _odom_cb(self, msg: Odometry) -> None:
        self.latest_odom = msg
        self._received("odom")

    def _motors_cb(self, msg: DiagnosticArray) -> None:
        self.latest_motors = msg
        self._received("motors")

    def _fsm_cb(self, msg: String) -> None:
        previous = self.policy_gate.mode
        self.latest_fsm = msg
        now = time.monotonic()
        self.received_at["fsm"] = now
        if self.policy_gate.update_mode(msg.data, now):
            if hasattr(self, "step_logger"):
                self.step_logger.event(
                    "fsm_change", f"{previous or '<unset>'}->{self.policy_gate.mode}", sequence=self.sequence
                )
            self.obs_builder.set_last_action(np.zeros(8, dtype=np.float32))
            if self.publish_debug:
                self.action_valid_pub.publish(Bool(data=False))

    def _fresh(self, key: str, now: float) -> bool:
        return now - self.received_at.get(key, -math.inf) <= self.timeout_sec

    @staticmethod
    def _vector(values: np.ndarray) -> Float32MultiArray:
        return Float32MultiArray(data=np.asarray(values, dtype=np.float32).reshape(-1).astype(float).tolist())

    def _publish_status(self, ok: bool, status: str, loop_ms: float) -> None:
        self._log_safety_ok = bool(ok)
        self._log_status = str(status)
        self._log_loop_ms = max(float(loop_ms), 0.0)
        if "error:" in status.lower() or "exception" in status.lower():
            self._log_fault_code = status
        if self.publish_debug and not ok:
            self.action_valid_pub.publish(Bool(data=False))
        self.safety_ok_pub.publish(Bool(data=ok))
        self.safety_status_pub.publish(String(data=status))
        self.status_pub.publish(String(data=f"{status}; COMMAND OUTPUT: DISABLED"))
        self.loop_pub.publish(Float32(data=float(loop_ms)))
        self.rate_pub.publish(Float32(data=float(self.effective_rate_hz)))

    def _tick_logged(self) -> None:
        self._reset_log_step()
        try:
            self._tick()
        finally:
            self._emit_step_log()

    def _emit_step_log(self) -> None:
        now_monotonic_ns = time.monotonic_ns()
        now_wall_ns = time.time_ns()
        now = now_monotonic_ns / 1e9
        critical_ages = [
            max((now - self.received_at[key]) * 1000.0, 0.0)
            for key in ("joint", "imu", "odom")
            if key in self.received_at
        ]
        sensor_age_ms = max(critical_ages) if len(critical_ages) == 3 else 1.0e9
        state = "READY" if self._log_safety_ok and self._log_status.startswith("ready:") else "PRECHECK"
        if state != self._last_logged_status:
            self.step_logger.event(
                "lifecycle_transition", f"{self._last_logged_status or 'INIT'}->{state}", sequence=self.sequence
            )
            self._last_logged_status = state
        record = LogRecord(
            monotonic_time_ns=now_monotonic_ns,
            wall_time_ns=now_wall_ns,
            sequence=self.sequence,
            controller_state=state,
            fsm_mode=self.policy_gate.mode,
            armed=False,
            command_output_enabled=False,
            safety_ok=self._log_safety_ok,
            fault_code=self._log_fault_code,
            command_source="zero_default_no_processed_command_subscription",
            command_valid=False,
            command_vx=0.0,
            command_vy=0.0,
            command_yaw=0.0,
            command_age_ms=1.0e9,
            sensor_age_ms=sensor_age_ms,
            inference_time_ms=self._log_inference_ms,
            loop_time_ms=self._log_loop_ms,
            deadline_missed=self._log_loop_ms > 20.0,
            safe_hold_active=False,
            dropped_log_records=self.step_logger.dropped_log_records,
            final_command_prepared=False,
            final_command_written=False,
            joint_pos_native=self._log_joint_pos,
            joint_vel_native=self._log_joint_vel,
            imu_quat=self._log_imu_quat,
            base_ang_vel=self._log_ang_vel,
            projected_gravity=self._log_gravity,
            obs=self._log_obs,
            action_raw=self._log_action_raw,
            action_scaled=self._log_action_scaled,
            virtual_leg_target=self._log_leg_target,
            virtual_wheel_target=self._log_wheel_target,
            final_cmd_position=zero_vector(8),
            final_cmd_velocity=zero_vector(8),
            final_cmd_effort=zero_vector(8),
            final_cmd_kp=zero_vector(8),
            final_cmd_kd=zero_vector(8),
            clipping_mask=self._log_clipping_mask,
            slew_limit_mask=zero_vector(8),
            command_type_mask=zero_vector(8),
        )
        self.step_logger.push(record)
        if record.deadline_missed:
            self.step_logger.event("deadline_miss", f"loop_time_ms={record.loop_time_ms:.6f}", sequence=self.sequence)
        if record.fault_code:
            self.step_logger.trigger_fault(record.fault_code, sequence=self.sequence)
        if self.step_logger.failed and not self._logger_failure_reported:
            self._logger_failure_reported = True
            self.get_logger().error(
                f"[LOGGER] {self.step_logger.writer_error}; dry-run continues unarmed with output disabled"
            )
        self.sequence += 1

    def _tick(self) -> None:
        started = time.monotonic()
        delta = max(started - self.last_tick, 1e-6)
        self.last_tick = started
        self.effective_rate_hz = 1.0 / delta
        sensors_fresh = all(self._fresh(key, started) for key in ("joint", "imu", "odom"))
        motors_ready = not self.require_motors_status or self._fresh("motors", started)
        fsm_received = self.policy_gate.mode_received_at is not None
        fsm_ready = not self.require_fsm_mode or fsm_received

        if not sensors_fresh or self.latest_joint is None or self.latest_imu is None:
            result = self.safety_gate.evaluate(sensors_fresh, (), False, motors_ready, fsm_ready, None)
            self._publish_status(result.ok, result.status, (time.monotonic() - started) * 1000.0)
            return

        action: np.ndarray | None = None
        try:
            joint_pos, joint_vel, missing = self.obs_builder.native_joint_arrays(self.latest_joint)
            if missing:
                result = self.safety_gate.evaluate(True, missing, False, motors_ready, fsm_ready, None)
                self._publish_status(result.ok, result.status, (time.monotonic() - started) * 1000.0)
                return
            self._log_joint_pos = finite_tuple(joint_pos, 8, "joint_pos_native")
            self._log_joint_vel = finite_tuple(joint_vel, 8, "joint_vel_native")
            orientation = self.latest_imu.orientation
            angular_velocity = self.latest_imu.angular_velocity
            quat = np.asarray([orientation.w, orientation.x, orientation.y, orientation.z], dtype=np.float32)
            ang_vel = np.asarray(
                [angular_velocity.x, angular_velocity.y, angular_velocity.z], dtype=np.float32
            )
            if np.all(np.isfinite(quat)):
                self._log_imu_quat = finite_tuple(quat, 4, "imu_quat")
            if np.all(np.isfinite(ang_vel)):
                self._log_ang_vel = finite_tuple(ang_vel, 3, "base_ang_vel")
            quat_norm = float(np.linalg.norm(quat))
            projected_gravity = (
                self.obs_builder.projected_gravity(quat / quat_norm)
                if np.isfinite(quat_norm) and quat_norm >= 1e-6
                else np.full(3, np.nan, dtype=np.float32)
            )
            leg_indices = [0, 1, 2, 4, 5, 6]
            leg_error = float(
                np.max(
                    np.abs(
                        joint_pos[leg_indices]
                        - self.obs_builder.DEFAULT_JOINT_ANGLES_NATIVE[leg_indices]
                    )
                )
            )
            values_finite = bool(
                np.all(np.isfinite(np.concatenate([joint_pos, joint_vel, quat, ang_vel, projected_gravity])))
            )
            gate = self.policy_gate.evaluate(
                now=started,
                sensors_fresh=sensors_fresh,
                values_finite=values_finite,
                max_leg_position_error_rad=leg_error,
                base_angular_velocity_norm=float(np.linalg.norm(ang_vel)),
                projected_gravity=projected_gravity,
            )
            if not self.policy_fsm_gate_enabled:
                gate = type(gate)(True, "ready:policy_dryrun")

            if not gate.ready:
                self.obs_builder.set_last_action(np.zeros(8, dtype=np.float32))
            obs, diagnostics = self.obs_builder.build(
                joint_pos,
                joint_vel,
                quat,
                ang_vel,
            )
            self.obs_builder.push_history(obs)
            self._log_obs = finite_tuple(obs, 33, "obs")
            self._log_gravity = finite_tuple(diagnostics.projected_gravity, 3, "projected_gravity")
            if self.publish_debug:
                self.obs_pub.publish(self._vector(obs))
                self.history_pub.publish(self._vector(self.obs_builder.history))
                self.gravity_pub.publish(self._vector(diagnostics.projected_gravity))
            if not gate.ready:
                self._publish_status(False, gate.status, (time.monotonic() - started) * 1000.0)
                return

            if self.policy_enabled and self.policy.status.loaded:
                action = self.policy.act(obs, self.obs_builder.history)
                self._log_inference_ms = max(float(self.policy.last_inference_ms), 0.0)
            else:
                self.obs_builder.set_last_action(np.zeros(8, dtype=np.float32))
                self._publish_status(False, "blocked:policy_unavailable", (time.monotonic() - started) * 1000.0)
                return
            virtual = self.action_adapter.compute(action)
            self.obs_builder.set_last_action(action)
            self._log_action_raw = finite_tuple(virtual.action_raw_native, 8, "action_raw")
            self._log_action_scaled = finite_tuple(virtual.action_scaled_native, 8, "action_scaled")
            self._log_leg_target = finite_tuple(virtual.virtual_leg_target_native, 6, "virtual_leg_target")
            self._log_wheel_target = finite_tuple(virtual.virtual_wheel_vel_native, 2, "virtual_wheel_target")
            limited_scaled = virtual.virtual_joint_target_native.copy()
            leg_indices = [0, 1, 2, 4, 5, 6]
            limited_scaled[leg_indices] -= self.obs_builder.DEFAULT_JOINT_ANGLES_NATIVE[leg_indices]
            self._log_clipping_mask = finite_tuple(
                np.not_equal(limited_scaled, virtual.action_scaled_native).astype(np.float32),
                8,
                "clipping_mask",
            )

            if self.publish_debug:
                self.action_raw_pub.publish(self._vector(virtual.action_raw_native))
                self.action_scaled_pub.publish(self._vector(virtual.action_scaled_native))
                self.virtual_target_pub.publish(self._vector(virtual.virtual_joint_target_native))
                self.virtual_leg_pub.publish(self._vector(virtual.virtual_leg_target_native))
                self.virtual_wheel_pub.publish(self._vector(virtual.virtual_wheel_vel_native))
                self.target_type_mask_pub.publish(self._vector(virtual.target_type_mask_native))
                self.action_valid_pub.publish(Bool(data=True))
                self.max_action_pub.publish(Float32(data=float(np.max(np.abs(action)))))
                self.inference_pub.publish(Float32(data=float(self.policy.last_inference_ms)))

            result = self.safety_gate.evaluate(True, (), True, motors_ready, fsm_ready, action)
            status = gate.status if result.ok else result.status
            self._publish_status(result.ok, status, (time.monotonic() - started) * 1000.0)
        except Exception as exc:
            self.obs_builder.set_last_action(np.zeros(8, dtype=np.float32))
            result = self.safety_gate.evaluate(True, (), False, motors_ready, fsm_ready, action)
            self._publish_status(False, f"dry-run error: {exc}; {result.status}", (time.monotonic() - started) * 1000.0)


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = TitaDryRunNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except RuntimeError as exc:
        if "Unable to convert call argument to Python object" not in str(exc):
            raise
    finally:
        node.step_logger.event("shutdown_request", "normal ROS shutdown", sequence=node.sequence)
        node.step_logger.close()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
