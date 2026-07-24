from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
import math
from typing import Protocol

import numpy as np

from .real_obs_builder import WHEEL_INDICES_NATIVE


LEG_INDICES_NATIVE = (0, 1, 2, 4, 5, 6)
COMMAND_TYPE_MASK = (1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0)


class LifecycleState(str, Enum):
    BOOT_CHECK = "BOOT_CHECK"
    VENDOR_IDLE_CONFIRMED = "VENDOR_IDLE_CONFIRMED"
    DIRECT_PRECHECK = "DIRECT_PRECHECK"
    READY_FOR_TAKEOVER = "READY_FOR_TAKEOVER"
    VENDOR_STOP_REQUESTED = "VENDOR_STOP_REQUESTED"
    VENDOR_STOPPED = "VENDOR_STOPPED"
    CAN_RELEASE_CONFIRMED = "CAN_RELEASE_CONFIRMED"
    DIRECT_SOAK = "DIRECT_SOAK"
    DIRECT_REQUESTED = "DIRECT_REQUESTED"
    DIRECT_CONFIRMED = "DIRECT_CONFIRMED"
    HARDWARE_STARTING = "HARDWARE_STARTING"
    STAND_UP = "STAND_UP"
    STANDING_SETTLE = "STANDING_SETTLE"
    RL_RUNNING = "RL_RUNNING"
    SAFE_HOLD = "SAFE_HOLD"
    DIRECT_STOPPING = "DIRECT_STOPPING"
    RECOVERY = "RECOVERY"
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"
    STOPPED = "STOPPED"
    FAULT = "FAULT"


class BoardMode(str, Enum):
    UNKNOWN = "UNKNOWN"
    READY_MODE = "READY_MODE"
    DIRECT_REQUESTED = "DIRECT_REQUESTED"
    DIRECT_MODE = "DIRECT_MODE"
    AUTO_LOCOMOTION = "AUTO_LOCOMOTION"


# Kept as a source-compatible name for tools which used the earlier core.
MotorMode = BoardMode


class TestStage(IntEnum):
    __test__ = False
    PREFLIGHT = 0
    STAND_ONLY = 1
    JOYSTICK_RL = 2


@dataclass(frozen=True, slots=True)
class StandProfile:
    """Standing data copied from a hashed, official controller configuration."""

    source_path: str
    source_sha256: str
    fold_position: tuple[float, ...]
    stand_position: tuple[float, ...]
    fold_duration_sec: float
    stand_duration_sec: float
    kp: tuple[float, ...]
    kd: tuple[float, ...]
    feedforward_effort: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.source_path or len(self.source_sha256) != 64:
            raise ValueError("stand profile requires a source path and SHA256")
        for name in ("fold_position", "stand_position", "kp", "kd", "feedforward_effort"):
            values = getattr(self, name)
            if len(values) != 8 or not all(math.isfinite(float(value)) for value in values):
                raise ValueError(f"{name} must contain eight finite values")
        if self.fold_duration_sec <= 0.0 or self.stand_duration_sec <= 0.0:
            raise ValueError("stand durations must be positive")


@dataclass(frozen=True, slots=True)
class DirectControllerConfig:
    execute_vendor_stop: bool = False
    execute_start_bash: bool = False
    enable_hardware_output: bool = False
    auto_enter_rl: bool = False
    preflight_duration_sec: float = 5.0
    direct_ack_timeout_sec: float = 2.0
    standing_completion_sec: float = 0.25
    standing_settle_sec: float = 5.0
    max_leg_target_delta_rad: float = 0.25
    max_leg_target_slew_rad_s: float = 0.5
    max_wheel_velocity_rad_s: float = 5.0
    max_wheel_accel_rad_s: float = 5.0
    max_effort: float = 60.0
    max_repeated_clipping: int = 5

    def __post_init__(self) -> None:
        if self.preflight_duration_sec < 5.0 or self.standing_settle_sec < 5.0:
            raise ValueError("preflight and standing settle must each be at least five seconds")
        positive_values = (
            self.direct_ack_timeout_sec,
            self.standing_completion_sec,
            self.max_leg_target_delta_rad,
            self.max_leg_target_slew_rad_s,
            self.max_wheel_velocity_rad_s,
            self.max_wheel_accel_rad_s,
            self.max_effort,
        )
        if not all(math.isfinite(value) and value > 0.0 for value in positive_values):
            raise ValueError("timing and limits must be finite and positive")
        if self.max_repeated_clipping < 1:
            raise ValueError("max_repeated_clipping must be positive")


@dataclass(frozen=True, slots=True)
class PrecheckSample:
    fsm_mode: str
    vendor_service_active: bool
    sensors_fresh: bool
    joystick_fresh: bool
    joystick_centered: bool
    motors_online: bool
    values_finite: bool
    policy_loaded: bool
    obs_shape: int
    history_shape: int
    action_shape: int
    logger_ready: bool
    direct_files_ready: bool
    stand_source_ready: bool
    direct_ack_available: bool
    recovery_confirmed: bool
    emergency_procedure_confirmed: bool

    @property
    def boot_valid(self) -> bool:
        """Evidence required before replacing the vendor runtime.

        Stage 1 does not consume the vendor sensor, command-manager, joystick, or policy path.
        Those fields remain in the record as command-free diagnostics, but they are deliberately
        not takeover gates.  The only live vendor evidence required here is exact FSM idle while
        the service is active; the Direct stack files, official stand source, and logger are
        independent static/runtime gates.
        """
        return (
            self.vendor_service_active
            and self.logger_ready
            and self.direct_files_ready
            and self.stand_source_ready
        )

    @property
    def valid(self) -> bool:
        return self.fsm_mode.strip().lower() == "idle" and self.boot_valid

    @property
    def real_test_ready(self) -> bool:
        return self.valid and self.direct_ack_available and self.recovery_confirmed and self.emergency_procedure_confirmed

    def blockers(self) -> tuple[str, ...]:
        """Return command-free takeover-precheck blockers."""
        checks = (
            (self.fsm_mode.strip().lower() == "idle", "fsm_not_idle"),
            (self.vendor_service_active, "vendor_service_inactive"),
            (self.logger_ready, "logger"),
            (self.direct_files_ready, "direct_files"),
            (self.stand_source_ready, "stand_source"),
        )
        return tuple(name for passed, name in checks if not passed)

    def real_test_blockers(self) -> tuple[str, ...]:
        """Add evidence needed only for an armed Direct Stage 1 operation."""
        checks = (
            (self.direct_ack_available, "direct_ack"),
            (self.recovery_confirmed, "recovery"),
            (self.emergency_procedure_confirmed, "emergency_procedure"),
        )
        return self.blockers() + tuple(name for passed, name in checks if not passed)

    def diagnostics(self) -> tuple[str, ...]:
        """Optional pre-stop evidence retained for logs; never a Stage 1 takeover dependency."""
        checks = (
            (self.sensors_fresh, "vendor_sensor_stale"),
            (self.joystick_fresh, "vendor_joystick_stale"),
            (self.joystick_centered, "vendor_joystick_not_centered"),
            (self.motors_online, "vendor_motor_status_unavailable"),
            (self.values_finite, "vendor_state_unavailable"),
            (self.policy_loaded, "policy_not_loaded"),
            (self.obs_shape == 33, "obs_shape_unavailable"),
            (self.history_shape == 0, "unexpected_policy_history"),
            (self.action_shape == 8, "action_shape_unavailable"),
        )
        return tuple(name for passed, name in checks if not passed)


@dataclass(frozen=True, slots=True)
class RuntimeSample:
    joint_position: tuple[float, ...]
    joint_velocity: tuple[float, ...]
    roll: float
    pitch: float
    angular_velocity_norm: float
    projected_gravity_norm: float
    sensors_fresh: bool = True
    odometry_fresh: bool = True
    board_mode_direct: bool = True
    single_writer: bool = True
    joystick_fresh: bool = True
    write_success: bool = True
    loop_timing_valid: bool = True
    can_feedback_valid: bool = True
    logger_ok: bool = True

    def __post_init__(self) -> None:
        if len(self.joint_position) != 8 or len(self.joint_velocity) != 8:
            raise ValueError("runtime joint arrays must contain eight values")

    def finite(self) -> bool:
        values = self.joint_position + self.joint_velocity + (
            self.roll,
            self.pitch,
            self.angular_velocity_norm,
            self.projected_gravity_norm,
        )
        return all(math.isfinite(float(value)) for value in values)

    def watchdog_ok(self) -> bool:
        return (
            self.finite()
            and self.sensors_fresh
            and self.odometry_fresh
            and self.board_mode_direct
            and self.single_writer
            and self.joystick_fresh
            and self.write_success
            and self.loop_timing_valid
            and self.can_feedback_valid
            and self.logger_ok
        )


@dataclass(frozen=True, slots=True)
class StandingLimits:
    max_leg_error_rad: float = 0.2
    max_wheel_speed_rad_s: float = 0.3
    max_roll_rad: float = 0.25
    max_pitch_rad: float = 0.25
    max_angular_velocity_rad_s: float = 0.5
    max_gravity_norm_error: float = 0.15


@dataclass(frozen=True, slots=True)
class PolicyReadiness:
    input_frames: int
    joystick_valid: bool
    action: tuple[float, ...]
    leg_target: tuple[float, ...]
    wheel_velocity: tuple[float, ...]

    @property
    def finite(self) -> bool:
        return (
            len(self.action) == 8
            and len(self.leg_target) == 8
            and len(self.wheel_velocity) == 2
            and all(math.isfinite(float(value)) for value in self.action + self.leg_target + self.wheel_velocity)
        )


@dataclass(frozen=True, slots=True)
class MotorCommand:
    position: tuple[float, ...]
    velocity: tuple[float, ...]
    effort: tuple[float, ...]
    kp: tuple[float, ...]
    kd: tuple[float, ...]
    type_mask: tuple[float, ...] = COMMAND_TYPE_MASK

    def __post_init__(self) -> None:
        for name in ("position", "velocity", "effort", "kp", "kd", "type_mask"):
            values = getattr(self, name)
            if len(values) != 8 or not all(math.isfinite(float(value)) for value in values):
                raise ValueError(f"{name} must contain eight finite values")


class CommandWriter(Protocol):
    @property
    def claimed(self) -> bool: ...

    @property
    def duplicate_writer_detected(self) -> bool: ...

    def claim_exclusive(self) -> bool: ...
    def release(self) -> bool: ...
    def write(self, command: MotorCommand) -> bool: ...


class DisabledCommandWriter:
    claimed = False
    duplicate_writer_detected = False

    def claim_exclusive(self) -> bool:
        return False

    def release(self) -> bool:
        return True

    def write(self, command: MotorCommand) -> bool:
        del command
        return False


class DirectControllerCore:
    """Hardware-independent, fail-closed direct-mode and output-source FSM."""

    def __init__(
        self,
        config: DirectControllerConfig,
        stand: StandProfile,
        writer: CommandWriter,
        standing_limits: StandingLimits | None = None,
    ) -> None:
        self.config = config
        self.stand = stand
        self.writer = writer
        self.standing_limits = standing_limits or StandingLimits()
        self.state = LifecycleState.BOOT_CHECK
        self.stage = TestStage.PREFLIGHT
        self.operator_armed = False
        self.fault_code = ""
        self.first_fault_code = ""
        self.precheck_started_at: float | None = None
        self.direct_requested_at: float | None = None
        self.hardware_started_at: float | None = None
        self.stand_started_at: float | None = None
        self.standing_since: float | None = None
        self.settle_started_at: float | None = None
        self.measured_start = np.zeros(8, dtype=np.float64)
        self.last_command: MotorCommand | None = None
        self.direct_request_count = 0
        self.direct_script_succeeded = False
        self.clipping_count = 0

    @property
    def output_active(self) -> bool:
        return self.state in {
            LifecycleState.STAND_UP,
            LifecycleState.STANDING_SETTLE,
            LifecycleState.RL_RUNNING,
            LifecycleState.SAFE_HOLD,
        }

    def update_precheck(self, now: float, sample: PrecheckSample) -> bool:
        if self.state == LifecycleState.READY_FOR_TAKEOVER:
            return True
        if self.state not in {
            LifecycleState.BOOT_CHECK,
            LifecycleState.VENDOR_IDLE_CONFIRMED,
            LifecycleState.DIRECT_PRECHECK,
        }:
            return False
        if not sample.valid:
            self.precheck_started_at = None
            self.state = LifecycleState.BOOT_CHECK
            return False
        if self.state == LifecycleState.BOOT_CHECK:
            self.state = LifecycleState.VENDOR_IDLE_CONFIRMED
        self.state = LifecycleState.DIRECT_PRECHECK
        if self.precheck_started_at is None:
            self.precheck_started_at = float(now)
            return False
        if float(now) - self.precheck_started_at >= self.config.preflight_duration_sec:
            self.state = LifecycleState.READY_FOR_TAKEOVER
            return True
        return False

    def arm(self, stage: TestStage, sample: PrecheckSample) -> bool:
        if self.state != LifecycleState.READY_FOR_TAKEOVER or self.operator_armed:
            return False
        if stage < TestStage.STAND_ONLY:
            return False
        if not (
            self.config.execute_vendor_stop
            and self.config.execute_start_bash
            and self.config.enable_hardware_output
            and sample.real_test_ready
        ):
            return False
        self.stage = TestStage(stage)
        self.operator_armed = True
        self.state = LifecycleState.VENDOR_STOP_REQUESTED
        return True

    def arm_readonly_soak(self, sample: PrecheckSample) -> bool:
        if self.state != LifecycleState.READY_FOR_TAKEOVER or self.operator_armed:
            return False
        if not (
            self.config.execute_vendor_stop
            and not self.config.execute_start_bash
            and not self.config.enable_hardware_output
            and sample.valid
        ):
            return False
        self.stage = TestStage.PREFLIGHT
        self.operator_armed = True
        self.state = LifecycleState.VENDOR_STOP_REQUESTED
        return True

    def confirm_vendor_stopped(self, service_inactive: bool, remaining_vendor_nodes: int) -> bool:
        if self.state != LifecycleState.VENDOR_STOP_REQUESTED:
            return False
        if not service_inactive or remaining_vendor_nodes != 0:
            return False
        self.state = LifecycleState.VENDOR_STOPPED
        return True

    def confirm_can_release(self, can_owner_count: int) -> bool:
        if self.state != LifecycleState.VENDOR_STOPPED or can_owner_count != 0:
            return False
        self.state = LifecycleState.CAN_RELEASE_CONFIRMED
        return True

    def begin_readonly_soak(self) -> bool:
        if (
            self.state != LifecycleState.CAN_RELEASE_CONFIRMED
            or self.config.execute_start_bash
            or self.config.enable_hardware_output
        ):
            return False
        self.state = LifecycleState.DIRECT_SOAK
        return True

    def begin_direct_request(self, now: float) -> bool:
        if self.state != LifecycleState.CAN_RELEASE_CONFIRMED or self.direct_request_count != 0:
            return False
        self.direct_request_count = 1
        self.direct_script_succeeded = False
        self.direct_requested_at = float(now)
        self.state = LifecycleState.DIRECT_REQUESTED
        return True

    def direct_script_result(self, success: bool) -> bool:
        if self.state != LifecycleState.DIRECT_REQUESTED:
            return False
        if not success:
            self._fault("start_bash_failed")
            return False
        self.direct_script_succeeded = True
        return True

    def update_direct_ack(self, now: float, board_mode: BoardMode) -> bool:
        if self.state != LifecycleState.DIRECT_REQUESTED:
            return self.state == LifecycleState.DIRECT_CONFIRMED
        if board_mode == BoardMode.DIRECT_MODE:
            self.state = LifecycleState.DIRECT_CONFIRMED
            return True
        if self.direct_requested_at is not None and now - self.direct_requested_at > self.config.direct_ack_timeout_sec:
            self._fault("direct_ack_timeout")
        return False

    def begin_hardware_start(self, now: float) -> bool:
        if self.state != LifecycleState.DIRECT_CONFIRMED:
            return False
        self.hardware_started_at = float(now)
        self.state = LifecycleState.HARDWARE_STARTING
        return True

    def begin_hardware_start_pending_composite_confirmation(self, now: float) -> bool:
        """Start the official bridge when Stage 1 uses the documented composite confirmation.

        TITA upstream exposes no standalone board-mode getter.  In the controlled first Stage 1
        test, Direct confirmation is therefore completed by the official bridge/controller's
        first valid eight-joint read, interface claim, TransformUp cycle, and continuing motor
        feedback.  This transition is allowed only after the official script has returned
        successfully; it does not itself claim that the board is already confirmed Direct.
        """
        if (
            self.state != LifecycleState.DIRECT_REQUESTED
            or self.direct_requested_at is None
            or not self.direct_script_succeeded
        ):
            return False
        self.hardware_started_at = float(now)
        self.state = LifecycleState.HARDWARE_STARTING
        return True

    def confirm_composite_direct(self) -> bool:
        """Record composite evidence emitted after the first successful hardware write."""
        if self.state != LifecycleState.HARDWARE_STARTING:
            return False
        self.state = LifecycleState.STAND_UP
        return True

    def hardware_ready(self, now: float, measured_position: tuple[float, ...], expected_joint_count: int = 8) -> bool:
        measured = np.asarray(measured_position, dtype=np.float64)
        if self.state != LifecycleState.HARDWARE_STARTING or expected_joint_count != 8:
            return False
        if measured.shape != (8,) or not np.all(np.isfinite(measured)):
            self._fault("invalid_first_hardware_state")
            return False
        if self.writer.duplicate_writer_detected or not self.writer.claim_exclusive():
            self._fault("exclusive_command_owner_failed")
            return False
        self.measured_start = measured.copy()
        self.stand_started_at = float(now)
        self.state = LifecycleState.STAND_UP
        return True

    def _standing_valid(self, sample: RuntimeSample) -> bool:
        q = np.asarray(sample.joint_position, dtype=np.float64)
        dq = np.asarray(sample.joint_velocity, dtype=np.float64)
        target = np.asarray(self.stand.stand_position, dtype=np.float64)
        limits = self.standing_limits
        return (
            sample.watchdog_ok()
            and float(np.max(np.abs(q[list(LEG_INDICES_NATIVE)] - target[list(LEG_INDICES_NATIVE)])))
            <= limits.max_leg_error_rad
            and float(np.max(np.abs(dq[list(WHEEL_INDICES_NATIVE)]))) <= limits.max_wheel_speed_rad_s
            and abs(sample.roll) <= limits.max_roll_rad
            and abs(sample.pitch) <= limits.max_pitch_rad
            and sample.angular_velocity_norm <= limits.max_angular_velocity_rad_s
            and abs(sample.projected_gravity_norm - 1.0) <= limits.max_gravity_norm_error
        )

    def _write(self, command: MotorCommand) -> MotorCommand:
        if not self.writer.claimed or not self.writer.write(command):
            self._fault("command_write_failed")
            raise RuntimeError("command write failed")
        self.last_command = command
        return command

    def _bounded_command(
        self,
        desired_position: np.ndarray,
        desired_wheels: np.ndarray,
        dt: float,
        *,
        effort: np.ndarray | None = None,
        kp: np.ndarray | None = None,
        kd: np.ndarray | None = None,
    ) -> MotorCommand:
        position = np.asarray(desired_position, dtype=np.float64).reshape(8).copy()
        previous_p = self.measured_start if self.last_command is None else np.asarray(self.last_command.position)
        max_step = self.config.max_leg_target_slew_rad_s * max(float(dt), 0.0)
        for index in LEG_INDICES_NATIVE:
            position[index] = previous_p[index] + np.clip(position[index] - previous_p[index], -max_step, max_step)
        position[list(WHEEL_INDICES_NATIVE)] = 0.0
        velocity = np.zeros(8, dtype=np.float64)
        previous_v = np.zeros(8) if self.last_command is None else np.asarray(self.last_command.velocity)
        max_v_step = self.config.max_wheel_accel_rad_s * max(float(dt), 0.0)
        wheels = np.asarray(desired_wheels, dtype=np.float64).reshape(2)
        for slot, index in enumerate(WHEEL_INDICES_NATIVE):
            target = np.clip(wheels[slot], -self.config.max_wheel_velocity_rad_s, self.config.max_wheel_velocity_rad_s)
            velocity[index] = previous_v[index] + np.clip(target - previous_v[index], -max_v_step, max_v_step)
        effort_values = np.zeros(8) if effort is None else np.asarray(effort, dtype=np.float64).reshape(8)
        effort_values = np.clip(effort_values, -self.config.max_effort, self.config.max_effort)
        kp_values = np.asarray(self.stand.kp if kp is None else kp, dtype=np.float64).copy()
        kd_values = np.asarray(self.stand.kd if kd is None else kd, dtype=np.float64).copy()
        kp_values[list(WHEEL_INDICES_NATIVE)] = 0.0
        return MotorCommand(
            position=tuple(position),
            velocity=tuple(velocity),
            effort=tuple(effort_values),
            kp=tuple(kp_values),
            kd=tuple(kd_values),
        )

    def step_stand(self, now: float, dt: float, sample: RuntimeSample) -> MotorCommand:
        if self.state not in {LifecycleState.STAND_UP, LifecycleState.STANDING_SETTLE}:
            raise RuntimeError("stand command requested in the wrong lifecycle state")
        if not sample.watchdog_ok():
            return self.enter_safe_hold(sample.joint_position, "stand_watchdog")
        started = float(now) if self.stand_started_at is None else self.stand_started_at
        elapsed = max(float(now) - started, 0.0)
        fold = np.asarray(self.stand.fold_position, dtype=np.float64).copy()
        fold[list(WHEEL_INDICES_NATIVE)] = self.measured_start[list(WHEEL_INDICES_NATIVE)]
        target = np.asarray(self.stand.stand_position, dtype=np.float64)
        if elapsed <= self.stand.fold_duration_sec:
            alpha = min(elapsed / self.stand.fold_duration_sec, 1.0)
            desired = (1.0 - alpha) * self.measured_start + alpha * fold
        else:
            alpha = min((elapsed - self.stand.fold_duration_sec) / self.stand.stand_duration_sec, 1.0)
            desired = (1.0 - alpha) * fold + alpha * target
        command = self._write(
            self._bounded_command(
                desired,
                np.zeros(2),
                dt,
                effort=np.asarray(self.stand.feedforward_effort),
            )
        )
        motion_complete = elapsed >= self.stand.fold_duration_sec + self.stand.stand_duration_sec
        stable = motion_complete and self._standing_valid(sample)
        if self.state == LifecycleState.STAND_UP:
            if not stable:
                self.standing_since = None
            elif self.standing_since is None:
                self.standing_since = float(now)
            elif now - self.standing_since >= self.config.standing_completion_sec:
                self.state = LifecycleState.STANDING_SETTLE
                self.settle_started_at = float(now)
        elif self.state == LifecycleState.STANDING_SETTLE:
            if not stable:
                self.settle_started_at = None
            elif self.settle_started_at is None:
                self.settle_started_at = float(now)
            elif now - self.settle_started_at >= self.config.standing_settle_sec:
                if self.stage == TestStage.STAND_ONLY:
                    return self.enter_safe_hold(sample.joint_position, "stage1_complete")
                self.state = LifecycleState.RL_RUNNING
        return command

    def step_rl(self, now: float, dt: float, sample: RuntimeSample, policy: PolicyReadiness) -> MotorCommand:
        del now, dt
        if self.state != LifecycleState.RL_RUNNING:
            raise RuntimeError("RL command requested in the wrong state")
        if not sample.watchdog_ok() or not policy.finite or not policy.joystick_valid:
            return self.enter_safe_hold(sample.joint_position, "rl_watchdog")
        position = np.asarray(policy.leg_target, dtype=np.float64).reshape(8).copy()
        position[list(WHEEL_INDICES_NATIVE)] = 0.0
        velocity = np.zeros(8, dtype=np.float64)
        velocity[list(WHEEL_INDICES_NATIVE)] = np.asarray(policy.wheel_velocity, dtype=np.float64)
        kp = np.asarray(self.stand.kp, dtype=np.float64).copy()
        kd = np.asarray(self.stand.kd, dtype=np.float64).copy()
        kp[list(WHEEL_INDICES_NATIVE)] = 0.0
        return self._write(MotorCommand(
            position=tuple(position), velocity=tuple(velocity), effort=(0.0,) * 8,
            kp=tuple(kp), kd=tuple(kd),
        ))

    def enter_safe_hold(self, measured_position: tuple[float, ...], reason: str) -> MotorCommand:
        measured = np.asarray(measured_position, dtype=np.float64).reshape(8)
        if not np.all(np.isfinite(measured)):
            measured = np.asarray(self.stand.stand_position, dtype=np.float64)
        self._record_fault(reason)
        self.state = LifecycleState.SAFE_HOLD
        command = self._bounded_command(measured, np.zeros(2), 0.02, effort=np.zeros(8))
        if self.writer.claimed:
            if not self.writer.write(command):
                self._fault("safe_hold_write_failed")
                raise RuntimeError("SAFE_HOLD write failed")
            self.last_command = command
        return command

    def begin_recovery(self, recovery_confirmed: bool) -> bool:
        if self.state != LifecycleState.SAFE_HOLD:
            return False
        if not recovery_confirmed:
            self.state = LifecycleState.RECOVERY_REQUIRED
            return False
        self.state = LifecycleState.DIRECT_STOPPING
        return True

    def confirm_recovery(self, board_mode: BoardMode, vendor_ready: bool) -> bool:
        if self.state != LifecycleState.DIRECT_STOPPING:
            return False
        self.state = LifecycleState.RECOVERY
        if board_mode != BoardMode.AUTO_LOCOMOTION or not vendor_ready:
            self.state = LifecycleState.RECOVERY_REQUIRED
            return False
        if not self.writer.release():
            self._fault("command_owner_release_failed")
            return False
        self.operator_armed = False
        self.state = LifecycleState.STOPPED
        return True

    def request_stop(self, measured_position: tuple[float, ...] | np.ndarray) -> bool:
        if self.state in {
            LifecycleState.BOOT_CHECK,
            LifecycleState.VENDOR_IDLE_CONFIRMED,
            LifecycleState.DIRECT_PRECHECK,
            LifecycleState.READY_FOR_TAKEOVER,
        }:
            self.state = LifecycleState.STOPPED
            self.operator_armed = False
            return True
        if self.state == LifecycleState.STOPPED:
            return True
        self.enter_safe_hold(tuple(np.asarray(measured_position, dtype=np.float64).reshape(8)), "operator_stop")
        return True

    def watchdog_fault(self, code: str, measured_position: tuple[float, ...] | None = None) -> None:
        if measured_position is not None and self.writer.claimed:
            self.enter_safe_hold(measured_position, code)
        else:
            self._fault(code)

    def _record_fault(self, code: str) -> None:
        if not self.first_fault_code:
            self.first_fault_code = str(code)
        self.fault_code = str(code)

    def _fault(self, code: str) -> None:
        self._record_fault(code)
        self.state = LifecycleState.FAULT
