from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import queue
import re
import threading
import time
from collections import deque
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, ClassVar, Iterable, Mapping


VECTOR_FIELDS: tuple[tuple[str, int, str], ...] = (
    ("joint_pos_native", 8, "joint_pos_native_"),
    ("joint_vel_native", 8, "joint_vel_native_"),
    ("imu_quat", 4, "imu_quat_"),
    ("base_ang_vel", 3, "base_ang_vel_"),
    ("projected_gravity", 3, "projected_gravity_"),
    ("obs", 33, "obs_"),
    ("action_raw", 8, "action_raw_"),
    ("action_scaled", 8, "action_scaled_"),
    ("virtual_leg_target", 6, "virtual_leg_target_"),
    ("virtual_wheel_target", 2, "virtual_wheel_target_"),
    ("stand_target", 8, "stand_target_"),
    ("rl_target", 8, "rl_target_"),
    ("blended_target", 8, "blended_target_"),
    ("safety_limited_target", 8, "safety_limited_target_"),
    ("final_cmd_position", 8, "final_cmd_position_"),
    ("final_cmd_velocity", 8, "final_cmd_velocity_"),
    ("final_cmd_effort", 8, "final_cmd_effort_"),
    ("final_cmd_kp", 8, "final_cmd_kp_"),
    ("final_cmd_kd", 8, "final_cmd_kd_"),
    ("clipping_mask", 8, "clipping_mask_"),
    ("slew_limit_mask", 8, "slew_limit_mask_"),
    ("command_type_mask", 8, "command_type_mask_"),
)


@dataclass(frozen=True, slots=True)
class LogRecord:
    """One fixed-shape control step. Every persisted numeric value must be finite."""

    monotonic_time_ns: int
    wall_time_ns: int
    sequence: int
    controller_state: str
    fsm_mode: str
    armed: bool
    command_output_enabled: bool
    safety_ok: bool
    fault_code: str
    command_source: str
    command_valid: bool
    command_vx: float
    command_vy: float
    command_yaw: float
    command_age_ms: float
    sensor_age_ms: float
    inference_time_ms: float
    loop_time_ms: float
    deadline_missed: bool
    safe_hold_active: bool
    dropped_log_records: int
    final_command_prepared: bool
    final_command_written: bool
    joint_pos_native: tuple[float, ...]
    joint_vel_native: tuple[float, ...]
    imu_quat: tuple[float, ...]
    base_ang_vel: tuple[float, ...]
    projected_gravity: tuple[float, ...]
    obs: tuple[float, ...]
    action_raw: tuple[float, ...]
    action_scaled: tuple[float, ...]
    virtual_leg_target: tuple[float, ...]
    virtual_wheel_target: tuple[float, ...]
    final_cmd_position: tuple[float, ...]
    final_cmd_velocity: tuple[float, ...]
    final_cmd_effort: tuple[float, ...]
    final_cmd_kp: tuple[float, ...]
    final_cmd_kd: tuple[float, ...]
    clipping_mask: tuple[float, ...]
    slew_limit_mask: tuple[float, ...]
    command_type_mask: tuple[float, ...]
    ownership_state: str = "UNOWNED"
    motor_mode: str = "UNKNOWN"
    mode_request: str = "NONE"
    mode_acknowledged: bool = False
    interfaces_claimed: bool = False
    write_success: bool = False
    watchdog_ok: bool = True
    controller_source: str = "NONE"
    history_valid: bool = False
    settle_elapsed_sec: float = 0.0
    blend_alpha: float = 0.0
    repeated_clipping_count: int = 0
    stand_target: tuple[float, ...] = (0.0,) * 8
    rl_target: tuple[float, ...] = (0.0,) * 8
    blended_target: tuple[float, ...] = (0.0,) * 8
    safety_limited_target: tuple[float, ...] = (0.0,) * 8

    _VECTOR_LENGTHS: ClassVar[dict[str, int]] = {
        name: length for name, length, _ in VECTOR_FIELDS
    }

    def __post_init__(self) -> None:
        if self.monotonic_time_ns < 0 or self.wall_time_ns < 0 or self.sequence < 0:
            raise ValueError("timestamps and sequence must be non-negative")
        if self.dropped_log_records < 0:
            raise ValueError("dropped_log_records must be non-negative")
        scalar_values = (
            self.command_vx,
            self.command_vy,
            self.command_yaw,
            self.command_age_ms,
            self.sensor_age_ms,
            self.inference_time_ms,
            self.loop_time_ms,
            self.settle_elapsed_sec,
            self.blend_alpha,
        )
        if not all(math.isfinite(float(value)) for value in scalar_values):
            raise ValueError("LogRecord scalar contains NaN or Inf")
        for name, expected in self._VECTOR_LENGTHS.items():
            value = getattr(self, name)
            if len(value) != expected:
                raise ValueError(f"{name} length {len(value)} != {expected}")
            if not all(math.isfinite(float(item)) for item in value):
                raise ValueError(f"{name} contains NaN or Inf")
        if self.final_command_written and not self.final_command_prepared:
            raise ValueError("a written command must also be marked prepared")
        if self.repeated_clipping_count < 0:
            raise ValueError("repeated_clipping_count must be non-negative")

    @classmethod
    def csv_columns(cls) -> tuple[str, ...]:
        vector_names = {name for name, _, _ in VECTOR_FIELDS}
        columns = [item.name for item in fields(cls) if item.name not in vector_names]
        for _, length, prefix in VECTOR_FIELDS:
            width = 2 if prefix == "obs_" else 1
            columns.extend(f"{prefix}{index:0{width}d}" for index in range(length))
        return tuple(columns)

    def csv_row(self) -> tuple[Any, ...]:
        vector_names = {name for name, _, _ in VECTOR_FIELDS}
        row: list[Any] = []
        for item in fields(self):
            if item.name in vector_names:
                continue
            value = getattr(self, item.name)
            row.append(int(value) if isinstance(value, bool) else value)
        for name, _, _ in VECTOR_FIELDS:
            row.extend(getattr(self, name))
        return tuple(row)


@dataclass(frozen=True, slots=True)
class EventRecord:
    monotonic_time_ns: int
    wall_time_ns: int
    sequence: int
    event_type: str
    first_fault: bool
    detail: str

    COLUMNS: ClassVar[tuple[str, ...]] = (
        "monotonic_time_ns",
        "wall_time_ns",
        "sequence",
        "event_type",
        "first_fault",
        "detail",
    )

    def csv_row(self) -> tuple[Any, ...]:
        return (
            self.monotonic_time_ns,
            self.wall_time_ns,
            self.sequence,
            self.event_type,
            int(self.first_fault),
            self.detail,
        )


@dataclass(slots=True)
class _FaultCapture:
    first_reason: str
    records: list[LogRecord]
    post_deadline_ns: int


def zero_vector(length: int) -> tuple[float, ...]:
    return (0.0,) * length


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).expanduser().open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_source_tree(root: str | Path) -> str:
    root_path = Path(root).resolve()
    digest = hashlib.sha256()
    for path in sorted(root_path.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or ".pytest_cache" in path.parts:
            continue
        relative = path.relative_to(root_path).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def _safe_label(label: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_.-]+", "-", str(label).strip()).strip("-.")
    return normalized[:64]


def _yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(_yaml_scalar(item) for item in value) + "]"
    return json.dumps(str(value), ensure_ascii=False)


def recover_truncated_csv(path: str | Path) -> dict[str, int | bool]:
    """Atomically retain only complete CSV rows after an abrupt power loss.

    The step logger never calls this from a control loop. It is an offline/startup analysis
    primitive for files whose final sector may contain NUL padding or a partial final row.
    """
    csv_path = Path(path)
    payload = csv_path.read_bytes()
    original_size = len(payload)
    nul = payload.find(b"\0")
    if nul >= 0:
        payload = payload[:nul]
    last_newline = payload.rfind(b"\n")
    payload = payload[: last_newline + 1] if last_newline >= 0 else b""
    lines = payload.splitlines(keepends=True)
    if not lines:
        return {"changed": False, "original_bytes": original_size, "recovered_bytes": original_size}
    try:
        header = next(csv.reader([lines[0].decode("utf-8")]))
    except (UnicodeDecodeError, csv.Error, StopIteration):
        raise ValueError(f"invalid CSV header: {csv_path}")
    valid = [lines[0]]
    for line in lines[1:]:
        try:
            row = next(csv.reader([line.decode("utf-8")]))
        except (UnicodeDecodeError, csv.Error, StopIteration):
            break
        if len(row) != len(header):
            break
        valid.append(line)
    recovered = b"".join(valid)
    changed = recovered != csv_path.read_bytes()
    if changed:
        temporary = csv_path.with_suffix(csv_path.suffix + ".recovered.tmp")
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
        try:
            os.write(descriptor, recovered)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        os.replace(temporary, csv_path)
    return {
        "changed": changed,
        "original_bytes": original_size,
        "recovered_bytes": len(recovered),
        "complete_rows": max(len(valid) - 1, 0),
    }


class AsyncStepLogger:
    """Non-blocking producer with one dedicated disk-writer thread.

    Construction and close may perform bounded setup/teardown work, but ``push`` and
    all event/fault methods use only non-blocking queue operations on the control side.
    A writer failure is latched for diagnostics and never raised back into the loop.
    """

    def __init__(
        self,
        output_root: str | Path,
        metadata: Mapping[str, Any],
        config: Mapping[str, Any],
        *,
        enabled: bool = True,
        queue_size: int = 1024,
        event_queue_size: int = 256,
        history_seconds: float = 5.0,
        expected_rate_hz: float = 50.0,
        post_fault_seconds: float = 1.0,
        test_label: str = "",
        writer_delay_sec: float = 0.0,
    ) -> None:
        self.enabled = bool(enabled)
        self.queue_size = max(int(queue_size), 1)
        self._step_queue: queue.Queue[LogRecord] = queue.Queue(maxsize=self.queue_size)
        self._event_queue: queue.Queue[EventRecord] = queue.Queue(maxsize=max(int(event_queue_size), 1))
        history_count = max(int(math.ceil(max(history_seconds, 5.0) * expected_rate_hz)), 1)
        self._history: deque[LogRecord] = deque(maxlen=history_count)
        self._post_fault_ns = int(max(float(post_fault_seconds), 0.0) * 1e9)
        self._fault_capture: _FaultCapture | None = None
        self._fault_snapshot_pending: queue.Queue[tuple[LogRecord, ...]] = queue.Queue(maxsize=1)
        self._first_fault_reason = ""
        self._dropped_steps = 0
        self._dropped_events = 0
        self._overflow_reported_steps = 0
        self._overflow_reported_events = 0
        self._writer_delay_sec = max(float(writer_delay_sec), 0.0)
        self._stop = threading.Event()
        self._flush_request = threading.Event()
        self._flush_ack = threading.Event()
        self._closed = False
        self._writer_error = ""
        self._thread: threading.Thread | None = None

        monotonic_start_ns = time.monotonic_ns()
        label = _safe_label(test_label)
        run_id = f"mono{monotonic_start_ns}_pid{os.getpid()}" + (f"_{label}" if label else "")
        self.run_dir = Path(output_root).expanduser() / run_id
        self.metadata = dict(metadata)
        self.metadata.update(
            {
                "run_id": run_id,
                "monotonic_start_ns": monotonic_start_ns,
                "process_pid": os.getpid(),
                "logger_queue_size": self.queue_size,
                "test_label": test_label,
            }
        )
        self.config = dict(config)
        if not self.enabled:
            return
        try:
            self.run_dir.mkdir(parents=True, exist_ok=False)
            (self.run_dir / "metadata.json").write_text(
                json.dumps(self.metadata, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            yaml_text = "".join(f"{key}: {_yaml_scalar(value)}\n" for key, value in self.config.items())
            (self.run_dir / "config.yaml").write_text(yaml_text, encoding="utf-8")
            self._thread = threading.Thread(target=self._writer_main, name="tita-step-log-writer", daemon=True)
            self._thread.start()
        except Exception as exc:
            self._writer_error = f"logger initialization failed: {exc}"
            self.enabled = False

    @property
    def dropped_log_records(self) -> int:
        return self._dropped_steps

    @property
    def dropped_event_records(self) -> int:
        return self._dropped_events

    @property
    def writer_error(self) -> str:
        return self._writer_error

    @property
    def failed(self) -> bool:
        return bool(self._writer_error)

    def push(self, record: LogRecord) -> bool:
        if not isinstance(record, LogRecord):
            raise TypeError("record must be a validated LogRecord")
        self._history.append(record)
        capture = self._fault_capture
        if capture is not None:
            capture.records.append(record)
            if record.monotonic_time_ns >= capture.post_deadline_ns:
                self._finish_fault_capture()
        if not self.enabled or self._closed or self.failed:
            return False
        try:
            self._step_queue.put_nowait(record)
            return True
        except queue.Full:
            self._dropped_steps += 1
            return False

    def event(self, event_type: str, detail: str, *, sequence: int = 0, first_fault: bool = False) -> bool:
        if not self.enabled or self._closed or self.failed:
            return False
        event = EventRecord(
            monotonic_time_ns=time.monotonic_ns(),
            wall_time_ns=time.time_ns(),
            sequence=max(int(sequence), 0),
            event_type=str(event_type),
            first_fault=bool(first_fault),
            detail=str(detail),
        )
        try:
            self._event_queue.put_nowait(event)
            return True
        except queue.Full:
            self._dropped_events += 1
            return False

    def trigger_fault(self, reason: str, *, sequence: int = 0) -> None:
        reason = str(reason)
        first = not self._first_fault_reason
        if first:
            self._first_fault_reason = reason
            now_ns = time.monotonic_ns()
            self._fault_capture = _FaultCapture(reason, list(self._history), now_ns + self._post_fault_ns)
        self.event("fault", reason, sequence=sequence, first_fault=first)

    def _finish_fault_capture(self) -> None:
        capture = self._fault_capture
        if capture is None:
            return
        self._fault_capture = None
        try:
            self._fault_snapshot_pending.put_nowait(tuple(capture.records))
        except queue.Full:
            self._dropped_events += 1

    def close(self, *, unexpected: bool = False, timeout_sec: float = 2.0) -> None:
        if self._closed:
            return
        if unexpected:
            self.trigger_fault("unexpected_stop")
        self._finish_fault_capture()
        self._closed = True
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=max(float(timeout_sec), 0.0))

    def request_flush(self) -> None:
        """Non-blocking request; the writer acknowledges only after flushing and fsyncing."""
        self._flush_ack.clear()
        self._flush_request.set()

    @property
    def flush_acknowledged(self) -> bool:
        return self._flush_ack.is_set()

    def _writer_main(self) -> None:
        try:
            with (
                (self.run_dir / "step_log.csv").open("w", newline="", encoding="utf-8") as step_file,
                (self.run_dir / "events.csv").open("w", newline="", encoding="utf-8") as event_file,
                (self.run_dir / "fault_snapshot.csv").open("w", newline="", encoding="utf-8") as fault_file,
            ):
                step_writer = csv.writer(step_file)
                event_writer = csv.writer(event_file)
                fault_writer = csv.writer(fault_file)
                step_writer.writerow(LogRecord.csv_columns())
                event_writer.writerow(EventRecord.COLUMNS)
                fault_writer.writerow(LogRecord.csv_columns())
                while not self._stop.is_set() or self._has_pending_data():
                    wrote = self._drain_once(step_writer, event_writer, fault_writer)
                    if wrote:
                        step_file.flush()
                        event_file.flush()
                        fault_file.flush()
                    if self._flush_request.is_set():
                        step_file.flush()
                        event_file.flush()
                        fault_file.flush()
                        os.fsync(step_file.fileno())
                        os.fsync(event_file.fileno())
                        os.fsync(fault_file.fileno())
                        self._flush_request.clear()
                        self._flush_ack.set()
                    else:
                        self._stop.wait(0.01)
        except Exception as exc:
            self._writer_error = f"logger writer failed: {exc}"

    def _has_pending_data(self) -> bool:
        return not self._step_queue.empty() or not self._event_queue.empty() or not self._fault_snapshot_pending.empty()

    def _drain_once(self, step_writer: Any, event_writer: Any, fault_writer: Any) -> bool:
        wrote = False
        for _ in range(64):
            try:
                record = self._step_queue.get_nowait()
            except queue.Empty:
                break
            if self._writer_delay_sec:
                time.sleep(self._writer_delay_sec)
            step_writer.writerow(record.csv_row())
            wrote = True
        for _ in range(64):
            try:
                event = self._event_queue.get_nowait()
            except queue.Empty:
                break
            event_writer.writerow(event.csv_row())
            wrote = True
        if self._dropped_steps != self._overflow_reported_steps:
            event_writer.writerow(
                EventRecord(
                    time.monotonic_ns(), time.time_ns(), 0, "queue_overflow", False,
                    f"dropped_log_records={self._dropped_steps}",
                ).csv_row()
            )
            self._overflow_reported_steps = self._dropped_steps
            wrote = True
        if self._dropped_events != self._overflow_reported_events:
            event_writer.writerow(
                EventRecord(
                    time.monotonic_ns(), time.time_ns(), 0, "queue_overflow", False,
                    f"dropped_event_records={self._dropped_events}",
                ).csv_row()
            )
            self._overflow_reported_events = self._dropped_events
            wrote = True
        try:
            snapshot = self._fault_snapshot_pending.get_nowait()
        except queue.Empty:
            snapshot = ()
        for record in snapshot:
            fault_writer.writerow(record.csv_row())
            wrote = True
        return wrote


def finite_tuple(values: Iterable[Any], length: int, name: str) -> tuple[float, ...]:
    result = tuple(float(value) for value in values)
    if len(result) != length:
        raise ValueError(f"{name} length {len(result)} != {length}")
    if not all(math.isfinite(value) for value in result):
        raise ValueError(f"{name} contains NaN or Inf")
    return result
