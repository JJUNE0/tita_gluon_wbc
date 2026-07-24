from __future__ import annotations

import csv
import time
from pathlib import Path

import numpy as np
import pytest

from tita_low_level_sdk.action_adapter import DryRunActionAdapter
from tita_low_level_sdk.async_step_logger import (
    AsyncStepLogger,
    LogRecord,
    recover_truncated_csv,
    zero_vector,
)


def make_record(sequence: int, *, monotonic_ns: int | None = None, written: bool = False, command=None):
    command = command or {}
    return LogRecord(
        monotonic_time_ns=time.monotonic_ns() if monotonic_ns is None else monotonic_ns,
        wall_time_ns=time.time_ns(),
        sequence=sequence,
        controller_state="PRECHECK",
        fsm_mode="idle",
        armed=False,
        command_output_enabled=False,
        safety_ok=True,
        fault_code="",
        command_source="zero_default_no_processed_command_subscription",
        command_valid=False,
        command_vx=0.0,
        command_vy=0.0,
        command_yaw=0.0,
        command_age_ms=1.0e9,
        sensor_age_ms=1.0,
        inference_time_ms=0.5,
        loop_time_ms=1.0,
        deadline_missed=False,
        safe_hold_active=False,
        dropped_log_records=0,
        final_command_prepared=written,
        final_command_written=written,
        joint_pos_native=zero_vector(8),
        joint_vel_native=zero_vector(8),
        imu_quat=(1.0, 0.0, 0.0, 0.0),
        base_ang_vel=zero_vector(3),
        projected_gravity=(0.0, 0.0, -1.0),
        obs=zero_vector(33),
        action_raw=zero_vector(8),
        action_scaled=zero_vector(8),
        virtual_leg_target=zero_vector(6),
        virtual_wheel_target=zero_vector(2),
        final_cmd_position=tuple(command.get("position", zero_vector(8))),
        final_cmd_velocity=tuple(command.get("velocity", zero_vector(8))),
        final_cmd_effort=tuple(command.get("effort", zero_vector(8))),
        final_cmd_kp=tuple(command.get("kp", zero_vector(8))),
        final_cmd_kd=tuple(command.get("kd", zero_vector(8))),
        clipping_mask=zero_vector(8),
        slew_limit_mask=zero_vector(8),
        command_type_mask=tuple(command.get("type_mask", zero_vector(8))),
    )


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def test_nonblocking_push_and_overflow_are_counted(tmp_path):
    logger = AsyncStepLogger(
        tmp_path, {}, {}, queue_size=2, writer_delay_sec=0.03, test_label="slow-writer"
    )
    started = time.perf_counter()
    for sequence in range(200):
        logger.push(make_record(sequence))
    producer_elapsed = time.perf_counter() - started
    assert producer_elapsed < 0.2
    assert logger.dropped_log_records > 0
    logger.close(timeout_sec=3.0)
    events = read_csv(logger.run_dir / "events.csv")
    assert any(row["event_type"] == "queue_overflow" for row in events)


def test_column_order_and_disabled_neutral_command_are_explicit(tmp_path):
    logger = AsyncStepLogger(tmp_path, {}, {}, test_label="columns")
    logger.push(make_record(0))
    logger.close()
    with (logger.run_dir / "step_log.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.reader(stream))
    assert tuple(rows[0]) == LogRecord.csv_columns()
    row = dict(zip(rows[0], rows[1]))
    assert row["armed"] == "0"
    assert row["command_output_enabled"] == "0"
    assert row["final_command_prepared"] == "0"
    assert row["final_command_written"] == "0"
    assert all(float(row[f"final_cmd_effort_{index}"]) == 0.0 for index in range(8))
    assert all(float(row[f"command_type_mask_{index}"]) == 0.0 for index in range(8))


def test_vector_shape_and_nonfinite_values_fail_closed():
    with pytest.raises(ValueError, match="action_raw length"):
        record = make_record(0)
        values = {name: getattr(record, name) for name in record.__dataclass_fields__ if not name.startswith("_")}
        values["action_raw"] = (0.0,) * 7
        LogRecord(**values)
    with pytest.raises(ValueError, match="NaN or Inf"):
        record = make_record(0)
        values = {name: getattr(record, name) for name in record.__dataclass_fields__ if not name.startswith("_")}
        values["loop_time_ms"] = float("nan")
        LogRecord(**values)


def test_fault_snapshot_keeps_at_least_five_seconds_of_prefault_records(tmp_path):
    logger = AsyncStepLogger(
        tmp_path, {}, {}, expected_rate_hz=50.0, history_seconds=5.0, post_fault_seconds=0.0
    )
    base_ns = time.monotonic_ns()
    for sequence in range(250):
        logger.push(make_record(sequence, monotonic_ns=base_ns + sequence * 20_000_000))
    logger.trigger_fault("watchdog_trip", sequence=250)
    logger.close()
    snapshot = read_csv(logger.run_dir / "fault_snapshot.csv")
    assert len(snapshot) == 250
    assert snapshot[0]["sequence"] == "0"
    assert snapshot[-1]["sequence"] == "249"
    events = read_csv(logger.run_dir / "events.csv")
    fault = [row for row in events if row["event_type"] == "fault"]
    assert fault[0]["first_fault"] == "1"


def test_disk_initialization_failure_never_raises_into_control_loop(tmp_path):
    not_a_directory = tmp_path / "file"
    not_a_directory.write_text("occupied", encoding="utf-8")
    logger = AsyncStepLogger(not_a_directory, {}, {})
    assert logger.failed
    assert not logger.enabled
    assert logger.push(make_record(0)) is False
    logger.close()


def test_writer_thread_failure_is_latched_and_never_raised_by_push(tmp_path):
    class FailingWriterLogger(AsyncStepLogger):
        def _drain_once(self, step_writer, event_writer, fault_writer):
            raise OSError("simulated disk full")

    logger = FailingWriterLogger(tmp_path, {}, {})
    logger.push(make_record(0))
    deadline = time.monotonic() + 1.0
    while not logger.failed and time.monotonic() < deadline:
        time.sleep(0.005)
    assert logger.failed
    assert "simulated disk full" in logger.writer_error
    assert logger.push(make_record(1)) is False
    logger.close()


def test_logger_enabled_or_disabled_does_not_change_policy_adapter_result(tmp_path):
    action = np.linspace(-0.5, 0.5, 8, dtype=np.float32)
    adapter = DryRunActionAdapter()
    expected = adapter.compute(action).virtual_joint_target_native.copy()
    logger = AsyncStepLogger(tmp_path, {}, {}, enabled=True)
    logger.push(make_record(0))
    actual = adapter.compute(action).virtual_joint_target_native.copy()
    logger.close()
    disabled = AsyncStepLogger(tmp_path, {}, {}, enabled=False)
    disabled.push(make_record(1))
    disabled_actual = adapter.compute(action).virtual_joint_target_native.copy()
    assert np.array_equal(expected, actual)
    assert np.array_equal(expected, disabled_actual)


def test_fake_hardware_writer_input_matches_logged_final_command(tmp_path):
    class FakeWriter:
        def __init__(self):
            self.last = None

        def write(self, command):
            self.last = {key: tuple(value) for key, value in command.items()}
            return True

    command = {
        "position": tuple(float(index) for index in range(8)),
        "velocity": tuple(float(-index) for index in range(8)),
        "effort": zero_vector(8),
        "kp": (1.0,) * 8,
        "kd": (0.1,) * 8,
        "type_mask": (1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0),
    }
    writer = FakeWriter()
    assert writer.write(command)
    logger = AsyncStepLogger(tmp_path, {}, {}, test_label="fake-hardware")
    logger.push(make_record(0, written=True, command=writer.last))
    logger.close()
    row = read_csv(logger.run_dir / "step_log.csv")[0]
    assert row["final_command_written"] == "1"
    for field, prefix in (
        ("position", "final_cmd_position_"),
        ("velocity", "final_cmd_velocity_"),
        ("effort", "final_cmd_effort_"),
        ("kp", "final_cmd_kp_"),
        ("kd", "final_cmd_kd_"),
    ):
        assert tuple(float(row[f"{prefix}{index}"]) for index in range(8)) == writer.last[field]


def test_flush_ack_is_asynchronous_and_durable(tmp_path):
    logger = AsyncStepLogger(tmp_path, {}, {}, test_label="flush")
    logger.push(make_record(0))
    logger.request_flush()
    deadline = time.monotonic() + 2.0
    while not logger.flush_acknowledged and time.monotonic() < deadline:
        time.sleep(0.002)
    assert logger.flush_acknowledged
    logger.close()
    assert len(read_csv(logger.run_dir / "step_log.csv")) == 1


def test_truncated_final_row_and_nul_tail_recovery_preserves_complete_rows(tmp_path):
    path = tmp_path / "step_log.csv"
    path.write_bytes(b"a,b,c\n1,2,3\n4,5,6\n7,8\0\0garbage")
    result = recover_truncated_csv(path)
    assert result["changed"]
    assert result["complete_rows"] == 2
    assert path.read_bytes() == b"a,b,c\n1,2,3\n4,5,6\n"
    assert recover_truncated_csv(path)["changed"] is False
