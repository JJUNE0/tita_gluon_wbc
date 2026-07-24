from __future__ import annotations

import json
import math
from dataclasses import replace
from pathlib import Path
import subprocess
import time

import numpy as np
import rclpy
from ament_index_python.packages import PackageNotFoundError, get_package_share_directory
from diagnostic_msgs.msg import DiagnosticArray
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import Imu, JointState, Joy
from std_msgs.msg import Bool, Float32, Float32MultiArray, String
from std_srvs.srv import SetBool

from .action_adapter import DryRunActionAdapter
from .async_step_logger import AsyncStepLogger, LogRecord, finite_tuple, sha256_file, sha256_source_tree, zero_vector
from .direct_controller_core import (
    DirectControllerConfig,
    DirectControllerCore,
    DisabledCommandWriter,
    LifecycleState,
    PrecheckSample,
    StandProfile,
    TestStage,
)
from .direct_takeover import (
    DirectSoakOrchestrator,
    ManagedTakeoverBackend,
    Stage1TakeoverOrchestrator,
    TakeoverAuthorization,
    inspect_official_start_script,
)
from .onnx_policy_runner import OnnxPolicyRunner
from .real_obs_builder import NATIVE_JOINT_NAMES, POLICY_REINDEX, RealObservationBuilder


def _bool(value: object) -> bool:
    return value if isinstance(value, bool) else str(value).lower() in {"1", "true", "yes", "on"}


def _package_share_path() -> Path:
    """Resolve installed data through the ament index, with a source-tree test fallback."""
    try:
        return Path(get_package_share_directory("tita_low_level_sdk"))
    except PackageNotFoundError:
        return Path(__file__).resolve().parents[1]


class DirectRlControllerNode(Node):
    """Command-free preflight plus the explicitly armed Stage 1 takeover supervisor.

    This node never creates joint or CAN commands. Its only mutating path is the READY-state
    operator-arm service, additionally gated by the three false-by-default launch permissions.
    Real commands are owned exclusively by the production C++ ros2_control controller.
    """

    def __init__(self) -> None:
        super().__init__("tita_direct_rl_controller")
        defaults = {
            "tita_ns": "tita4252763",
            "policy_path": "/home/robot/tita_policy/policy.onnx",
            "policy_rate_hz": 50.0,
            "execute_vendor_stop": False,
            "execute_start_bash": False,
            "enable_hardware_output": False,
            "operator_arm": False,
            "auto_enter_rl": False,
            "direct_soak_only": False,
            "requested_stage": 1,
            "vendor_service": "tita-bringup.service",
            "official_start_bash_path": "/home/robot/direct_ws/src/ddt_ros2_control/start.bash",
            "official_start_bash_sha256": "0a2bca4a146f9127ad558b50ca745826cc93ee920f3bb9538521555ea94f97b3",
            "official_hardware_launch_path": "/home/robot/direct_ws/install/tita_stage1_controller/share/tita_stage1_controller/launch/stage1_hardware.launch.py",
            "official_soak_launch_path": "/home/robot/direct_ws/install/tita_stage1_controller/share/tita_stage1_controller/launch/direct_readonly_soak.launch.py",
            "upstream_commit": "e7b32d9746df900680641ff2845ffb0b5ffe99ed",
            "production_preflight_report_path": "/home/robot/direct_ws/stage1_preflight.json",
            "stage2_preflight_report_path": "/home/robot/direct_ws/stage2_preflight.json",
            "power_session_id": "",
            "direct_session_ledger_path": "/home/robot/direct_ws/runtime/direct_session.json",
            "takeover_token_file": "/home/robot/direct_ws/runtime/stage1_takeover.token",
            "stand_profile_path": "",
            "stand_profile_sha256": "b4e7c17112dddf4beb485d398a4bdb6e77e623e590e0ccfe6c6ac1d6deae5920",
            "direct_ack_available": False,
            "recovery_confirmed": True,
            "emergency_procedure_confirmed": False,
            "vendor_stop_timeout_sec": 10.0,
            "start_bash_timeout_sec": 3.0,
            "hardware_confirmation_timeout_sec": 10.0,
            "preflight_duration_sec": 5.0,
            "message_timeout_sec": 0.5,
            "command_timeout_sec": 0.25,
            "command_zero_tolerance": 0.05,
            "direct_ack_timeout_sec": 2.0,
            "standing_completion_sec": 0.25,
            "standing_settle_sec": 5.0,
            "rl_prepare_sec": 1.0,
            "rl_blend_sec": 1.0,
            "max_leg_target_delta_rad": 0.25,
            "max_leg_target_slew_rad_s": 0.5,
            "max_wheel_velocity_rad_s": 5.0,
            "max_wheel_accel_rad_s": 5.0,
            "max_effort": 60.0,
            "max_repeated_clipping": 5,
            "stand_fold_duration_sec": 4.0,
            "stand_duration_sec": 2.0,
            "logger_enabled": True,
            "logger_output_root": "/home/robot/lowlevel_ws/runs",
            "logger_queue_size": 1024,
            "logger_test_label": "direct_rl_preflight",
        }
        for name, default in defaults.items():
            self.declare_parameter(name, default)
        array_defaults = {
            "stand_fold_position": [0.75, 1.20, -2.7, 0.0, -0.75, 1.2, -2.7, 0.0],
            "stand_position": [-0.05, 0.9, -2.6, 0.0, 0.05, 0.90, -2.6, 0.0],
            "stand_kp": [600.0, 80.0, 80.0, 5.0, 600.0, 80.0, 80.0, 5.0],
            "stand_kd": [8.0, 8.0, 8.0, 0.5, 8.0, 8.0, 8.0, 0.5],
            "stand_feedforward_effort": [-20.0, 0.0, -25.0, 0.0, 20.0, 0.0, -25.0, 0.0],
        }
        for name, default in array_defaults.items():
            self.declare_parameter(name, default)

        package_root = Path(__file__).resolve().parents[1]
        package_share = _package_share_path()
        profile_path_text = str(self.get_parameter("stand_profile_path").value)
        profile_path = (
            Path(profile_path_text) if profile_path_text else
            package_share / "config/tita_transform_up_official_e7b32d9.yaml"
        )
        profile_hash = str(self.get_parameter("stand_profile_sha256").value)
        stand = StandProfile(
            source_path=str(profile_path),
            source_sha256=profile_hash,
            fold_position=tuple(float(v) for v in self.get_parameter("stand_fold_position").value),
            stand_position=tuple(float(v) for v in self.get_parameter("stand_position").value),
            fold_duration_sec=float(self.get_parameter("stand_fold_duration_sec").value),
            stand_duration_sec=float(self.get_parameter("stand_duration_sec").value),
            kp=tuple(float(v) for v in self.get_parameter("stand_kp").value),
            kd=tuple(float(v) for v in self.get_parameter("stand_kd").value),
            feedforward_effort=tuple(float(v) for v in self.get_parameter("stand_feedforward_effort").value),
        )
        config = DirectControllerConfig(
            execute_vendor_stop=_bool(self.get_parameter("execute_vendor_stop").value),
            execute_start_bash=_bool(self.get_parameter("execute_start_bash").value),
            enable_hardware_output=_bool(self.get_parameter("enable_hardware_output").value),
            auto_enter_rl=_bool(self.get_parameter("auto_enter_rl").value),
            preflight_duration_sec=float(self.get_parameter("preflight_duration_sec").value),
            direct_ack_timeout_sec=float(self.get_parameter("direct_ack_timeout_sec").value),
            standing_completion_sec=float(self.get_parameter("standing_completion_sec").value),
            standing_settle_sec=float(self.get_parameter("standing_settle_sec").value),
            rl_prepare_sec=float(self.get_parameter("rl_prepare_sec").value),
            rl_blend_sec=float(self.get_parameter("rl_blend_sec").value),
            max_leg_target_delta_rad=float(self.get_parameter("max_leg_target_delta_rad").value),
            max_leg_target_slew_rad_s=float(self.get_parameter("max_leg_target_slew_rad_s").value),
            max_wheel_velocity_rad_s=float(self.get_parameter("max_wheel_velocity_rad_s").value),
            max_wheel_accel_rad_s=float(self.get_parameter("max_wheel_accel_rad_s").value),
            max_effort=float(self.get_parameter("max_effort").value),
            max_repeated_clipping=int(self.get_parameter("max_repeated_clipping").value),
        )
        self.writer = DisabledCommandWriter()
        self.core = DirectControllerCore(config, stand, self.writer)
        self.tita_ns = str(self.get_parameter("tita_ns").value).strip("/")
        self.rate_hz = max(float(self.get_parameter("policy_rate_hz").value), 1.0)
        self.sensor_timeout = float(self.get_parameter("message_timeout_sec").value)
        self.command_timeout = float(self.get_parameter("command_timeout_sec").value)
        self.command_zero_tolerance = float(self.get_parameter("command_zero_tolerance").value)
        self.startup_arm_requested = _bool(self.get_parameter("operator_arm").value)
        self.direct_soak_only = _bool(self.get_parameter("direct_soak_only").value)
        self.requested_stage = TestStage(int(self.get_parameter("requested_stage").value))
        self.latest: dict[str, object] = {}
        self.received_at: dict[str, float] = {}
        self.fsm_mode = ""
        self.sequence = 0
        self.last_tick = time.monotonic()
        self.last_loop_ms = 0.0
        self.last_inference_ms = 0.0
        self.last_command = np.zeros(3, dtype=np.float32)
        self.last_command_age_ms = 1.0e9
        self.last_joint_pos = np.zeros(8, dtype=np.float32)
        self.last_joint_vel = np.zeros(8, dtype=np.float32)
        self.last_quat = np.zeros(4, dtype=np.float32)
        self.last_ang_vel = np.zeros(3, dtype=np.float32)
        self.last_gravity = np.zeros(3, dtype=np.float32)
        self.last_obs = np.zeros(33, dtype=np.float32)
        self.last_action_native = np.zeros(8, dtype=np.float32)
        self.last_scaled_native = np.zeros(8, dtype=np.float32)
        self.last_leg_target = np.zeros(6, dtype=np.float32)
        self.last_wheel_target = np.zeros(2, dtype=np.float32)
        self.shutdown_requested = False
        self.hardware_process_started = False
        self.hardware_started_at: float | None = None
        self.composite_direct_confirmed = False
        self.hardware_monitor_faulted = False
        self.readonly_soak_active = False
        self.vendor_runtime_attached = True
        self.last_soak_resource_log = -math.inf
        self.production_stage1_status = ""

        token_file = str(self.get_parameter("takeover_token_file").value)
        hardware_launch = (
            "ros2", "launch", "tita_stage1_controller", "stage1_hardware.launch.py",
            f"takeover_token_file:={token_file}",
            f"requested_stage:={int(self.requested_stage)}",
        )
        soak_launch = (
            "ros2", "launch", "tita_stage1_controller", "direct_readonly_soak.launch.py",
            f"soak_token_file:={token_file}",
        )
        self.takeover_backend = ManagedTakeoverBackend(
            service_name=str(self.get_parameter("vendor_service").value),
            start_script=str(self.get_parameter("official_start_bash_path").value),
            expected_start_sha256=str(self.get_parameter("official_start_bash_sha256").value),
            hardware_launch=hardware_launch,
            soak_hardware_launch=soak_launch,
            power_session_id=str(self.get_parameter("power_session_id").value),
            session_ledger=str(self.get_parameter("direct_session_ledger_path").value),
            takeover_token_file=token_file,
            requested_stage=int(self.requested_stage),
        )
        self.takeover = Stage1TakeoverOrchestrator(self.takeover_backend)
        self.soak_takeover = DirectSoakOrchestrator(self.takeover_backend)

        self.obs_builder = RealObservationBuilder()
        self.action_adapter = DryRunActionAdapter(
            config.max_leg_target_delta_rad, config.max_wheel_velocity_rad_s
        )
        policy_path = str(self.get_parameter("policy_path").value)
        self.policy = OnnxPolicyRunner(policy_path)
        self.static = self._inspect_static(profile_path, profile_hash)
        try:
            policy_hash = sha256_file(policy_path)
        except OSError:
            policy_hash = "unavailable"
        metadata = {
            "upstream_commit": str(self.get_parameter("upstream_commit").value),
            "start_bash_path": str(self.get_parameter("official_start_bash_path").value),
            "start_bash_sha256": str(self.get_parameter("official_start_bash_sha256").value),
            "stand_source_path": str(profile_path),
            "stand_source_sha256": profile_hash,
            "policy_path": policy_path,
            "policy_sha256": policy_hash,
            "package_source_sha256": sha256_source_tree(package_root),
            "native_joint_order": NATIVE_JOINT_NAMES,
            "policy_reindex": POLICY_REINDEX,
            "command_output_enabled": False,
            "production_confirmation": "DIRECT_CONFIRMATION_REQUIRES_STAGE1_COMPOSITE_EVIDENCE",
            "supervisor_command_writer": False,
        }
        logger_config = {name: self.get_parameter(name).value for name in defaults}
        self.logger = AsyncStepLogger(
            str(self.get_parameter("logger_output_root").value), metadata, logger_config,
            enabled=_bool(self.get_parameter("logger_enabled").value),
            queue_size=int(self.get_parameter("logger_queue_size").value),
            expected_rate_hz=self.rate_hz,
            test_label=str(self.get_parameter("logger_test_label").value),
        )

        prefix = f"/{self.tita_ns}"
        # The vendor runtime is used for one fact only: exact MCU FSM idle before takeover.
        # Joint/IMU/motor/command data after takeover comes from the Direct HardwareBridge and
        # Stage1Controller state interfaces, never from vendor broadcasters or command_manager.
        self.vendor_subscriptions = [
            self.create_subscription(
                String, f"{prefix}/locomotion/body/fsm_mode", self._fsm_cb, 10
            ),
        ]
        if self.requested_stage in {TestStage.ZERO_COMMAND_RL, TestStage.SMALL_JOYSTICK_RL}:
            self.vendor_subscriptions.extend([
                self.create_subscription(
                    JointState, f"{prefix}/joint_states",
                    lambda msg: self._receive("joint", msg), 10,
                ),
                self.create_subscription(
                    Imu, f"{prefix}/imu_sensor_broadcaster/imu",
                    lambda msg: self._receive("imu", msg), 10,
                ),
                self.create_subscription(
                    Odometry, f"{prefix}/chassis/odometry",
                    lambda msg: self._receive("odom", msg), 10,
                ),
                self.create_subscription(
                    DiagnosticArray, f"{prefix}/locomotion/motors_status",
                    lambda msg: self._receive("motors", msg), 10,
                ),
                self.create_subscription(Joy, f"{prefix}/joy", self._joy_cb, 10),
            ])
        self.create_subscription(
            String, "/tita_stage1_controller/stage1_status", self._stage1_status_cb, 10
        )
        base = "/tita_lowlevel/runtime"
        self.status_pub = self.create_publisher(String, f"{base}/status", 10)
        self.state_pub = self.create_publisher(String, f"{base}/state", 10)
        self.preflight_pub = self.create_publisher(Float32, f"{base}/preflight_progress", 10)
        self.safety_pub = self.create_publisher(Bool, f"{base}/safety_ok", 10)
        self.armed_pub = self.create_publisher(Bool, f"{base}/armed", 10)
        self.output_pub = self.create_publisher(Bool, f"{base}/command_output_enabled", 10)
        self.obs_pub = self.create_publisher(Float32MultiArray, f"{base}/obs_current", 10)
        self.history_pub = self.create_publisher(Float32MultiArray, f"{base}/obs_history_flat", 10)
        self.action_pub = self.create_publisher(Float32MultiArray, f"{base}/action_raw", 10)
        self.fault_pub = self.create_publisher(String, f"{base}/fault_code", 10)
        self.arm_service = self.create_service(SetBool, f"{base}/operator_arm", self._operator_arm_cb)
        self.timer = self.create_timer(1.0 / self.rate_hz, self._tick)
        self.logger.event("lifecycle_transition", "->BOOT_CHECK")
        self.get_logger().warn("COMMAND OUTPUT DISABLED: production Stage 1 preflight/approval is required")
        if self.startup_arm_requested:
            self.get_logger().error("operator_arm launch parameter ignored; only READY-state service requests are considered")

    def _inspect_static(self, profile_path: Path, profile_hash: str) -> dict[str, object]:
        start_path = Path(str(self.get_parameter("official_start_bash_path").value))
        expected_start_hash = str(self.get_parameter("official_start_bash_sha256").value)
        start_ok = False
        start_detail = "missing"
        if start_path.is_file():
            try:
                inspection = inspect_official_start_script(start_path)
                start_ok = inspection.sha256 == expected_start_hash and not inspection.acknowledgment_present
                start_detail = f"sha={inspection.sha256};frames={len(inspection.frame_payloads)}"
            except Exception as exc:
                start_detail = str(exc)
        hardware_path = Path(str(self.get_parameter("official_hardware_launch_path").value))
        soak_path = Path(str(self.get_parameter("official_soak_launch_path").value))
        profile_ok = profile_path.is_file() and sha256_file(profile_path) == profile_hash
        audit_parameter = (
            "stage2_preflight_report_path"
            if self.requested_stage in {TestStage.ZERO_COMMAND_RL, TestStage.SMALL_JOYSTICK_RL}
            else "production_preflight_report_path"
        )
        audit_path = Path(str(self.get_parameter(audit_parameter).value))
        audit_ok = False
        audit_plugins_ok = False
        audit_detail = "missing"
        if audit_path.is_file():
            try:
                audit = json.loads(audit_path.read_text(encoding="utf-8"))
                blockers = [str(item) for item in audit.get("blockers", [])]
                # Stage 2 policy-output limits are runtime gates, not file/plugin gates.
                # They must be evaluated only after real standing observations are available
                # in RL_PREPARE; never bypass them when entering RL_BLEND/RL_RUNNING.
                runtime_policy_blockers = {
                    "POLICY_STAND_HANDOFF_DELTA",
                    "POLICY_WHEEL_TARGET_CLIPPING",
                    "POLICY_REPEATED_CLIPPING",
                }
                static_blockers = [item for item in blockers if item not in runtime_policy_blockers]
                audit_ok = bool(audit.get("ready")) or (
                    self.requested_stage in {
                        TestStage.ZERO_COMMAND_RL, TestStage.SMALL_JOYSTICK_RL
                    } and not static_blockers
                )
                plugin_files = audit.get("plugin_files", {})
                audit_plugins_ok = bool(plugin_files) and all(bool(value) for value in plugin_files.values())
                audit_detail = ",".join(blockers) or "PASS"
            except (OSError, json.JSONDecodeError) as exc:
                audit_detail = str(exc)
        try:
            service_active = subprocess.run(
                ["systemctl", "is-active", "--quiet", str(self.get_parameter("vendor_service").value)],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=2.0, check=False,
            ).returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            service_active = False
        return {
            "service_active": service_active,
            "direct_files_ready": start_ok and hardware_path.is_file() and audit_ok,
            "soak_files_ready": soak_path.is_file() and audit_plugins_ok,
            "stand_source_ready": profile_ok,
            "start_detail": start_detail,
            "production_audit": audit_detail,
        }

    @staticmethod
    def _array(values: np.ndarray) -> Float32MultiArray:
        return Float32MultiArray(data=np.asarray(values, dtype=np.float32).reshape(-1).astype(float).tolist())

    def _receive(self, key: str, msg: object) -> None:
        self.latest[key] = msg
        self.received_at[key] = time.monotonic()

    def _detach_vendor_runtime(self) -> None:
        if not self.vendor_runtime_attached:
            return
        for subscription in self.vendor_subscriptions:
            self.destroy_subscription(subscription)
        self.vendor_subscriptions.clear()
        self.vendor_runtime_attached = False
        self.latest.clear()
        self.received_at.clear()
        self.logger.event(
            "vendor_runtime_detached",
            "post-stop runtime uses only direct HardwareBridge/controller evidence",
            sequence=self.sequence,
        )

    def _log_soak_resources(self, now: float) -> None:
        if not self.readonly_soak_active or now - self.last_soak_resource_log < 5.0:
            return
        self.last_soak_resource_log = now
        rss: list[dict[str, object]] = []
        patterns = (
            "ros2_control_node", "robot_state_publisher", "spawner",
            "direct_rl_controller_node", "ros2cli.daemon",
        )
        for entry in Path("/proc").iterdir():
            if not entry.name.isdigit():
                continue
            try:
                command = (entry / "cmdline").read_bytes().replace(b"\0", b" ").decode(
                    "utf-8", "replace"
                ).strip()
                if not any(pattern in command for pattern in patterns):
                    continue
                status = (entry / "status").read_text(encoding="utf-8", errors="replace")
                rss_line = next(line for line in status.splitlines() if line.startswith("VmRSS:"))
                rss_kib = int(rss_line.split()[1])
                rss.append({"pid": int(entry.name), "rss_kib": rss_kib, "command": command})
            except (FileNotFoundError, PermissionError, ProcessLookupError, StopIteration, ValueError):
                continue
        available_kib = -1
        try:
            meminfo = Path("/proc/meminfo").read_text(encoding="utf-8")
            available_line = next(
                line for line in meminfo.splitlines() if line.startswith("MemAvailable:")
            )
            available_kib = int(available_line.split()[1])
        except (OSError, StopIteration, ValueError):
            pass
        self.logger.event(
            "direct_soak_resources",
            json.dumps(
                {
                    "available_memory_kib": available_kib,
                    "processes": rss,
                    "command_output_enabled": False,
                    "expected_motor_api_write_count": 0,
                },
                sort_keys=True,
            ),
            sequence=self.sequence,
        )

    def _fsm_cb(self, msg: String) -> None:
        mode = msg.data.strip().lower()
        if mode != self.fsm_mode:
            self.logger.event("fsm_change", f"{self.fsm_mode or '<unset>'}->{mode}", sequence=self.sequence)
            self.fsm_mode = mode
            self.obs_builder.history.fill(0.0)
            self.obs_builder.set_last_action(np.zeros(8, dtype=np.float32))
        self.received_at["fsm"] = time.monotonic()

    def _joy_cb(self, msg: Joy) -> None:
        command = np.full(3, np.nan, dtype=np.float32)
        if len(msg.axes) >= 8 and not any(int(value) != 0 for value in msg.buttons):
            axes = np.asarray(msg.axes[:8], dtype=np.float32)
            if np.all(np.isfinite(axes)):
                ratio_index = int(np.clip(int(1.0 - float(axes[7])), 0, 2))
                ratio = (0.33, 0.66, 1.0)[ratio_index]
                command[:] = (-axes[2] * 3.0 * ratio, axes[0] * ratio, axes[3] * 6.0 * ratio)
                if axes[5] != 0.0:
                    command[1] = 0.0
        self.last_command = command
        self.latest["command"] = command
        self.received_at["command"] = time.monotonic()
        self.latest["joy"] = msg
        self.received_at["joy"] = self.received_at["command"]

    def _fresh(self, key: str, now: float, timeout: float | None = None) -> bool:
        return now - self.received_at.get(key, -math.inf) <= (self.sensor_timeout if timeout is None else timeout)

    @staticmethod
    def _motors_online(msg: object) -> bool:
        if not isinstance(msg, DiagnosticArray) or not msg.status:
            return False
        values = [item.value.strip().lower() for status in msg.status for item in status.values]
        return len(values) >= 8 and all(value == "online" for value in values[:8])

    def _operator_arm_cb(self, request: SetBool.Request, response: SetBool.Response) -> SetBool.Response:
        if not request.data:
            if self.hardware_process_started:
                response.success = False
                response.message = (
                    "BLOCKED: the production controller owns Direct hardware; use its SAFE_HOLD "
                    "state and the approved operator power-cycle procedure"
                )
                self.logger.event("operator_disarm_blocked", response.message, sequence=self.sequence)
                return response
            self.core.request_stop(self.last_joint_pos)
            response.success = True
            response.message = "command-free node stopped; no hardware ownership was held"
            return response

        now = time.monotonic()
        sample = self._evaluate(now)
        if not self.takeover_backend.inspect_service_active():
            response.success = False
            response.message = "BLOCKED: vendor service is not active at the final arm check"
            self.logger.event("operator_arm_blocked", response.message, sequence=self.sequence)
            return response
        if self.direct_soak_only:
            soak_sample = replace(
                sample,
                direct_files_ready=bool(self.static["soak_files_ready"]),
                stand_source_ready=True,
            )
            if not (
                self.core.config.execute_vendor_stop
                and not self.core.config.execute_start_bash
                and not self.core.config.enable_hardware_output
            ):
                response.success = False
                response.message = (
                    "BLOCKED: read-only soak requires vendor stop enabled with start.bash and "
                    "hardware output disabled"
                )
                self.logger.event("operator_arm_blocked", response.message, sequence=self.sequence)
                return response
            if not self.core.arm_readonly_soak(soak_sample):
                response.success = False
                response.message = "BLOCKED: " + ",".join(
                    soak_sample.blockers() or ("not_ready_or_not_enabled",)
                )
                self.logger.event("operator_arm_blocked", response.message, sequence=self.sequence)
                return response
            authorization = TakeoverAuthorization(
                operator_armed=True,
                execute_vendor_stop=True,
                execute_start_bash=False,
                enable_hardware_output=False,
                vendor_service_confirmed=True,
                vendor_nodes_absent=False,
                can_owners_zero=False,
            )
            self.logger.event(
                "operator_arm_accepted", "Direct read-only soak authorized", sequence=self.sequence)
            try:
                outcome = self.soak_takeover.execute(
                    authorization,
                    event_callback=self._takeover_event,
                    service_timeout_sec=float(self.get_parameter("vendor_stop_timeout_sec").value),
                )
            except Exception as exc:
                self.core.watchdog_fault(f"soak_takeover:{type(exc).__name__}")
                response.success = False
                response.message = f"READ-ONLY SOAK BLOCKED: {exc}"
                self.logger.event(
                    "takeover_failed", response.message, sequence=self.sequence, first_fault=True)
                return response
            self.hardware_process_started = True
            self.readonly_soak_active = True
            response.success = True
            response.message = (
                f"Read-only Direct stack soak started pid={outcome.hardware_pid}; "
                "start.bash not executed; motor API output disabled"
            )
            return response
        if self.requested_stage not in {
            TestStage.STAND_ONLY, TestStage.ZERO_COMMAND_RL, TestStage.SMALL_JOYSTICK_RL
        }:
            response.success = False
            response.message = "BLOCKED: only production Stage 1 or zero-command Stage 2 is supported"
            self.logger.event("operator_arm_blocked", response.message, sequence=self.sequence)
            return response
        if self.requested_stage in {TestStage.ZERO_COMMAND_RL, TestStage.SMALL_JOYSTICK_RL}:
            stage2_blockers = []
            if not sample.policy_loaded:
                stage2_blockers.append("policy_load")
            if (sample.obs_shape, sample.history_shape, sample.action_shape) != (33, 330, 8):
                stage2_blockers.append("policy_shapes")
            if not sample.joystick_fresh:
                stage2_blockers.append("joy_stale")
            if not sample.joystick_centered:
                stage2_blockers.append("joy_nonzero_or_button_unsafe")
            if not sample.values_finite:
                stage2_blockers.append("observation_nonfinite")
            if stage2_blockers:
                response.success = False
                response.message = "BLOCKED: " + ",".join(stage2_blockers)
                self.logger.event("operator_arm_blocked", response.message, sequence=self.sequence)
                return response
        if not self.core.arm(self.requested_stage, sample):
            response.success = False
            response.message = "BLOCKED: " + ",".join(
                sample.real_test_blockers() or ("not_ready_or_not_enabled",)
            )
            self.logger.event("operator_arm_blocked", response.message, sequence=self.sequence)
            return response

        authorization = TakeoverAuthorization(
            operator_armed=self.core.operator_armed,
            execute_vendor_stop=self.core.config.execute_vendor_stop,
            execute_start_bash=self.core.config.execute_start_bash,
            enable_hardware_output=self.core.config.enable_hardware_output,
            vendor_service_confirmed=True,
            vendor_nodes_absent=False,
            can_owners_zero=False,
        )
        self.logger.event(
            "operator_arm_accepted", f"Stage {int(self.requested_stage)} takeover authorized",
            sequence=self.sequence,
        )
        try:
            outcome = self.takeover.execute(
                authorization,
                event_callback=self._takeover_event,
                service_timeout_sec=float(self.get_parameter("vendor_stop_timeout_sec").value),
                start_timeout_sec=float(self.get_parameter("start_bash_timeout_sec").value),
            )
        except Exception as exc:
            self.core.watchdog_fault(f"takeover:{type(exc).__name__}")
            response.success = False
            response.message = f"TAKEOVER BLOCKED: {exc}"
            self.logger.event("takeover_failed", response.message, sequence=self.sequence, first_fault=True)
            return response

        self.hardware_process_started = True
        response.success = True
        response.message = (
            f"Stage {int(self.requested_stage)} hardware started pid={outcome.hardware_pid}; "
            "Direct confirmation now requires composite controller/hardware evidence"
        )
        return response

    def _takeover_event(self, event: str, detail: object) -> None:
        detail_dict = dict(detail)
        if event == "vendor_stopped":
            if not self.core.confirm_vendor_stopped(True, int(detail_dict["remaining_vendor_nodes"])):
                raise RuntimeError("lifecycle rejected vendor-stopped confirmation")
            self._detach_vendor_runtime()
        elif event == "can_released":
            if not self.core.confirm_can_release(int(detail_dict["can_owner_count"])):
                raise RuntimeError("lifecycle rejected CAN-release confirmation")
        elif event == "direct_request":
            if not self.core.begin_direct_request(time.monotonic()):
                raise RuntimeError("lifecycle rejected Direct request")
        elif event == "start_bash_result":
            succeeded = not bool(detail_dict["timed_out"]) and int(detail_dict["returncode"]) == 0
            if not self.core.direct_script_result(succeeded) and succeeded:
                raise RuntimeError("lifecycle rejected successful start.bash result")
        elif event == "hardware_starting":
            if not self.core.begin_hardware_start_pending_composite_confirmation(time.monotonic()):
                raise RuntimeError("lifecycle rejected composite hardware start")
            self.hardware_started_at = time.monotonic()
        elif event == "readonly_soak_starting":
            if not self.core.begin_readonly_soak():
                raise RuntimeError("lifecycle rejected read-only Direct soak")
            self.readonly_soak_active = True
        elif event == "hardware_started":
            self.hardware_process_started = True
        elif event == "readonly_soak_started":
            self.hardware_process_started = True
        self.logger.event(event, json.dumps(detail_dict, sort_keys=True), sequence=self.sequence)

    def _stage1_status_cb(self, msg: String) -> None:
        if msg.data != self.production_stage1_status:
            self.production_stage1_status = msg.data
            self.logger.event("production_stage1_status", msg.data, sequence=self.sequence)
        if msg.data.startswith("DIRECT_COMPOSITE_CONFIRMED") and not self.composite_direct_confirmed:
            if self.core.confirm_composite_direct():
                self.composite_direct_confirmed = True
                self.logger.event("direct_confirmed", msg.data, sequence=self.sequence)

    def _evaluate(self, now: float) -> PrecheckSample:
        sensors_fresh = all(self._fresh(key, now) for key in ("joint", "imu", "odom"))
        command_fresh = self._fresh("command", now, self.command_timeout)
        command_msg = self.latest.get("command")
        if isinstance(command_msg, Twist):
            self.last_command = np.asarray(
                [command_msg.linear.x, command_msg.linear.y, command_msg.angular.z], dtype=np.float32
            )
        self.last_command_age_ms = (now - self.received_at.get("command", -math.inf)) * 1000.0 if command_fresh else 1.0e9
        command_finite = bool(np.all(np.isfinite(self.last_command)))
        command_centered = command_fresh and command_finite and float(np.max(np.abs(self.last_command))) <= self.command_zero_tolerance
        values_finite = False
        action_shape = 0
        if sensors_fresh and isinstance(self.latest.get("joint"), JointState) and isinstance(self.latest.get("imu"), Imu):
            try:
                q, dq, missing = self.obs_builder.native_joint_arrays(self.latest["joint"])
                if missing:
                    raise ValueError(f"missing joints: {missing}")
                imu = self.latest["imu"]
                quat = np.asarray([imu.orientation.w, imu.orientation.x, imu.orientation.y, imu.orientation.z], dtype=np.float32)
                ang = np.asarray([imu.angular_velocity.x, imu.angular_velocity.y, imu.angular_velocity.z], dtype=np.float32)
                obs, diagnostics = self.obs_builder.build(q, dq, quat, ang, self.last_command if command_finite else np.zeros(3))
                self.obs_builder.push_history(obs)
                self.last_joint_pos, self.last_joint_vel = q, dq
                self.last_quat, self.last_ang_vel = quat, ang
                self.last_gravity, self.last_obs = diagnostics.projected_gravity, obs
                values_finite = bool(np.all(np.isfinite(np.concatenate([q, dq, quat, ang, obs]))))
                if self.policy.status.loaded:
                    action_policy = self.policy.act(obs, self.obs_builder.history)
                    # The custom policy output is already native left-then-right order.
                    action_native = action_policy.copy()
                    targets = self.action_adapter.compute(action_native)
                    self.last_action_native = action_native
                    self.last_scaled_native = targets.action_scaled_native
                    self.last_leg_target = targets.virtual_leg_target_native
                    self.last_wheel_target = targets.virtual_wheel_vel_native
                    self.last_inference_ms = self.policy.last_inference_ms
                    self.obs_builder.set_last_action(action_policy)
                    action_shape = int(action_policy.size)
            except Exception as exc:
                self.core.fault_code = f"preflight:{exc}"
        return PrecheckSample(
            fsm_mode=self.fsm_mode,
            vendor_service_active=bool(self.static["service_active"]),
            sensors_fresh=sensors_fresh,
            joystick_fresh=command_fresh,
            joystick_centered=command_centered,
            motors_online=self._fresh("motors", now, 1.5) and self._motors_online(self.latest.get("motors")),
            values_finite=values_finite,
            policy_loaded=self.policy.status.loaded,
            obs_shape=int(self.last_obs.size) if values_finite else 0,
            history_shape=int(self.obs_builder.history.size) if values_finite else 0,
            action_shape=action_shape,
            logger_ready=self.logger.enabled and not self.logger.failed and self.logger.dropped_log_records == 0,
            direct_files_ready=bool(self.static["direct_files_ready"]),
            stand_source_ready=bool(self.static["stand_source_ready"]),
            direct_ack_available=_bool(self.get_parameter("direct_ack_available").value),
            recovery_confirmed=_bool(self.get_parameter("recovery_confirmed").value),
            emergency_procedure_confirmed=_bool(self.get_parameter("emergency_procedure_confirmed").value),
        )

    def _tick(self) -> None:
        started = time.monotonic()
        previous = self.core.state
        if self.hardware_process_started and not self.hardware_monitor_faulted:
            process = self.takeover_backend.hardware_process
            if process is not None and process.poll() is not None:
                self.hardware_monitor_faulted = True
                self.core.watchdog_fault("hardware_process_exited")
                self.logger.event(
                    "hardware_process_exited", f"returncode={process.returncode}",
                    sequence=self.sequence, first_fault=True,
                )
            elif (
                not self.readonly_soak_active and
                not self.composite_direct_confirmed and self.hardware_started_at is not None and
                started - self.hardware_started_at >
                float(self.get_parameter("hardware_confirmation_timeout_sec").value)
            ):
                self.hardware_monitor_faulted = True
                self.core.watchdog_fault("composite_direct_confirmation_timeout")
                self.logger.event(
                    "direct_confirmation_timeout",
                    "no first successful production write evidence",
                    sequence=self.sequence,
                    first_fault=True,
                )
        sample = self._evaluate(started)
        if self.direct_soak_only:
            # The read-only soak audits only the Direct hardware/plugin path.  A Stage 1
            # TransformUp envelope blocker must not prevent this command-disabled diagnostic.
            sample = replace(
                sample,
                direct_files_ready=bool(self.static["soak_files_ready"]),
                stand_source_ready=True,
            )
        self.core.update_precheck(started, sample)
        self._log_soak_resources(started)
        if self.core.state != previous:
            self.logger.event("lifecycle_transition", f"{previous.value}->{self.core.state.value}", sequence=self.sequence)
        self.last_loop_ms = (time.monotonic() - started) * 1000.0
        elapsed = 0.0 if self.core.precheck_started_at is None else started - self.core.precheck_started_at
        progress = min(elapsed / self.core.config.preflight_duration_sec, 1.0)
        blockers = list(
            sample.blockers() if self.direct_soak_only else sample.real_test_blockers()
        )
        status = f"{self.core.state.value}; blockers={','.join(blockers) or 'none'}; COMMAND OUTPUT: DISABLED"
        self.status_pub.publish(String(data=status))
        self.state_pub.publish(String(data=self.core.state.value))
        self.preflight_pub.publish(Float32(data=float(progress)))
        self.safety_pub.publish(Bool(data=sample.valid))
        self.armed_pub.publish(Bool(data=self.core.operator_armed))
        self.output_pub.publish(Bool(data=False))
        self.obs_pub.publish(self._array(self.last_obs))
        self.history_pub.publish(self._array(self.obs_builder.history))
        self.action_pub.publish(self._array(self.last_action_native))
        self.fault_pub.publish(String(data=self.core.fault_code))
        now_ns = time.monotonic_ns()
        ages = [
            max((now_ns / 1e9 - self.received_at[key]) * 1000.0, 0.0) if key in self.received_at else 1.0e9
            for key in ("joint", "imu", "odom")
        ]
        record = LogRecord(
            monotonic_time_ns=now_ns, wall_time_ns=time.time_ns(), sequence=self.sequence,
            controller_state=self.core.state.value, fsm_mode=self.fsm_mode, armed=self.core.operator_armed,
            command_output_enabled=False, safety_ok=sample.valid, fault_code=self.core.fault_code,
            command_source="NONE",
            command_valid=False,
            command_vx=float(self.last_command[0]), command_vy=float(self.last_command[1]), command_yaw=float(self.last_command[2]),
            command_age_ms=max(self.last_command_age_ms, 0.0), sensor_age_ms=max(ages),
            inference_time_ms=self.last_inference_ms, loop_time_ms=self.last_loop_ms,
            deadline_missed=self.last_loop_ms > 20.0, safe_hold_active=False,
            dropped_log_records=self.logger.dropped_log_records, final_command_prepared=False,
            final_command_written=False, joint_pos_native=finite_tuple(self.last_joint_pos, 8, "q"),
            joint_vel_native=finite_tuple(self.last_joint_vel, 8, "dq"), imu_quat=finite_tuple(self.last_quat, 4, "quat"),
            base_ang_vel=finite_tuple(self.last_ang_vel, 3, "ang"), projected_gravity=finite_tuple(self.last_gravity, 3, "gravity"),
            obs=finite_tuple(self.last_obs, 33, "obs"), action_raw=finite_tuple(self.last_action_native, 8, "action"),
            action_scaled=finite_tuple(self.last_scaled_native, 8, "scaled"),
            virtual_leg_target=finite_tuple(self.last_leg_target, 6, "leg"),
            virtual_wheel_target=finite_tuple(self.last_wheel_target, 2, "wheel"),
            final_cmd_position=zero_vector(8), final_cmd_velocity=zero_vector(8), final_cmd_effort=zero_vector(8),
            final_cmd_kp=zero_vector(8), final_cmd_kd=zero_vector(8), clipping_mask=zero_vector(8),
            slew_limit_mask=zero_vector(8), command_type_mask=zero_vector(8),
            ownership_state=("VENDOR" if self.vendor_runtime_attached else "DIRECT_READ_ONLY"),
            motor_mode=(
                "AUTO_LOCOMOTION_OR_READY_UNOBSERVED"
                if self.vendor_runtime_attached else "MCU_MODE_PRE_DIRECT"
            ),
            mode_request="NONE", mode_acknowledged=False,
            interfaces_claimed=False, write_success=False, watchdog_ok=sample.valid,
            controller_source="COMMAND_FREE_PREFLIGHT", history_valid=sample.history_shape == 330,
            stand_target=self.core.stand.stand_position,
        )
        if not self.logger.push(record):
            self.logger.event("logger_push_failed", f"drops={self.logger.dropped_log_records}", sequence=self.sequence)
        self.sequence += 1

    def close(self) -> None:
        if self.shutdown_requested:
            return
        self.shutdown_requested = True
        if self.hardware_process_started:
            self.logger.event(
                "supervisor_shutdown",
                "production hardware is not stopped by a ROS shutdown callback; SAFE_HOLD/power-cycle required",
                sequence=self.sequence,
            )
        else:
            self.logger.event("shutdown_request", "command-free node exit", sequence=self.sequence)
            self.core.request_stop(self.last_joint_pos)
        self.logger.close()


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = DirectRlControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except RuntimeError as exc:
        # Humble can raise this while a subscription take is interrupted by the
        # launch process forwarding SIGINT. Do not suppress ordinary runtime errors.
        if "Unable to convert call argument to Python object" not in str(exc):
            raise
    finally:
        node.close()
        try:
            node.destroy_node()
        except KeyboardInterrupt:
            pass
        if rclpy.ok():
            try:
                rclpy.shutdown()
            except KeyboardInterrupt:
                pass
