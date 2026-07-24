from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from tita_low_level_sdk.direct_controller_core import (
    BoardMode,
    DirectControllerConfig,
    DirectControllerCore,
    LifecycleState,
    PolicyReadiness,
    PrecheckSample,
    RuntimeSample,
    StandProfile,
    TestStage,
)
from tita_low_level_sdk.direct_takeover import (
    CommandResult,
    DirectSoakOrchestrator,
    ManagedTakeoverBackend,
    Stage1TakeoverOrchestrator,
    TakeoverAuthorization,
    _proc_can_registration_entries,
    inspect_official_start_script,
    sha256_file,
)


class FakeWriter:
    def __init__(self) -> None:
        self.claimed = False
        self.duplicate_writer_detected = False
        self.claim_count = 0
        self.release_count = 0
        self.write_ok = True
        self.writes = []

    def claim_exclusive(self) -> bool:
        self.claim_count += 1
        self.claimed = not self.duplicate_writer_detected
        return self.claimed

    def release(self) -> bool:
        self.release_count += 1
        self.claimed = False
        return True

    def write(self, command) -> bool:
        if not self.write_ok:
            return False
        self.writes.append(command)
        return True


class FakeTakeoverBackend:
    service_name = "tita-bringup.service"

    def __init__(self) -> None:
        self.calls = []
        self.stop_ok = True
        self.inactive = True
        self.vendor_processes = ()
        self.can_owners = (0, (), "")
        self.start_ok = True

    @staticmethod
    def _result(argv, ok=True):
        return CommandResult(tuple(argv), 10, 20, 0 if ok else 1, "stdout", "stderr")

    def stop_vendor_service(self, authorization, timeout_sec):
        assert authorization.allows_service_stop()
        self.calls.append(("stop_vendor_service", timeout_sec))
        return self._result(("systemctl", "stop", self.service_name), self.stop_ok)

    def wait_vendor_service_inactive(self, timeout_sec):
        self.calls.append(("wait_vendor_service_inactive", timeout_sec))
        return self.inactive

    def inspect_vendor_processes(self):
        self.calls.append(("inspect_vendor_processes",))
        return self.vendor_processes

    def inspect_can_owners(self):
        self.calls.append(("inspect_can_owners",))
        return self.can_owners

    def execute_start_script_once(self, authorization, timeout_sec):
        assert authorization.allows_start_script()
        self.calls.append(("execute_start_script_once", timeout_sec))
        return self._result(("/official/start.bash",), self.start_ok)

    def start_hardware(self, authorization):
        assert authorization.allows_hardware_start()
        self.calls.append(("start_hardware",))
        return 4242

    def start_readonly_soak(self, authorization):
        assert authorization.allows_readonly_soak()
        self.calls.append(("start_readonly_soak",))
        return 4343


def test_proc_can_empty_markers_are_not_owners(tmp_path):
    for name in ("rcvlist_all", "rcvlist_eff", "rcvlist_err", "rcvlist_fil", "rcvlist_inv"):
        (tmp_path / name).write_text(
            "receive list 'test':\n  (any: no entry)\n  (can0: no entry)\n",
            encoding="utf-8",
        )
    assert _proc_can_registration_entries(tmp_path) == ()


def test_proc_can_real_registration_remains_fail_closed(tmp_path):
    (tmp_path / "rcvlist_fil").write_text(
        "receive list 'rx_fil':\n"
        "  can0  00000170  1fffffff  00000000  00000000  00000000  12345\n",
        encoding="utf-8",
    )
    assert _proc_can_registration_entries(tmp_path) == (
        "rcvlist_fil:can0  00000170  1fffffff  00000000  00000000  00000000  12345",
    )


def stand() -> StandProfile:
    return StandProfile(
        source_path="official/controllers.yaml",
        source_sha256="a" * 64,
        fold_position=(0.4, 0.8, -1.8, 0.0, -0.4, 0.8, -1.8, 0.0),
        stand_position=(-0.05, 0.9, -2.6, 0.0, 0.05, 0.9, -2.6, 0.0),
        fold_duration_sec=0.1,
        stand_duration_sec=0.1,
        kp=(10.0, 10.0, 10.0, 0.5, 10.0, 10.0, 10.0, 0.5),
        kd=(1.0, 1.0, 1.0, 0.1, 1.0, 1.0, 1.0, 0.1),
        feedforward_effort=(0.0,) * 8,
    )


def config(enabled: bool = True, **changes) -> DirectControllerConfig:
    values = dict(
        execute_vendor_stop=enabled,
        execute_start_bash=enabled,
        enable_hardware_output=enabled,
        standing_completion_sec=0.25,
        max_leg_target_slew_rad_s=2.0,
    )
    values.update(changes)
    return DirectControllerConfig(**values)


def sample(mode: str = "idle", *, ack: bool = True, recovery: bool = True, **changes) -> PrecheckSample:
    values = dict(
        fsm_mode=mode,
        vendor_service_active=True,
        sensors_fresh=True,
        joystick_fresh=True,
        joystick_centered=True,
        motors_online=True,
        values_finite=True,
        policy_loaded=True,
        obs_shape=33,
        history_shape=0,
        action_shape=8,
        logger_ready=True,
        direct_files_ready=True,
        stand_source_ready=True,
        direct_ack_available=ack,
        recovery_confirmed=recovery,
        emergency_procedure_confirmed=True,
    )
    values.update(changes)
    return PrecheckSample(**values)


def runtime(*, stable: bool = True, **changes) -> RuntimeSample:
    q = stand().stand_position if stable else (0.0,) * 8
    values = dict(
        joint_position=q,
        joint_velocity=(0.0,) * 8,
        roll=0.0,
        pitch=0.0,
        angular_velocity_norm=0.0,
        projected_gravity_norm=1.0,
    )
    values.update(changes)
    return RuntimeSample(**values)


def policy(*, large: bool = False) -> PolicyReadiness:
    target = np.asarray(stand().stand_position)
    if large:
        target[[0, 1, 2, 4, 5, 6]] += 1.0
    return PolicyReadiness(
        input_frames=1,
        joystick_valid=True,
        action=(0.0,) * 8,
        leg_target=tuple(target),
        wheel_velocity=(0.0, 0.0),
    )


def ready_core(*, enabled: bool = True, cfg=None, writer=None, precheck=None):
    writer = writer or FakeWriter()
    core = DirectControllerCore(cfg or config(enabled), stand(), writer)
    precheck = precheck or sample()
    assert not core.update_precheck(0.0, precheck)
    assert core.update_precheck(5.0, precheck)
    return core, writer, precheck


def hardware_core(stage=TestStage.STAND_ONLY, **kwargs):
    core, writer, precheck = ready_core(**kwargs)
    assert core.arm(stage, precheck)
    assert core.confirm_vendor_stopped(True, 0)
    assert core.confirm_can_release(0)
    assert core.begin_direct_request(5.1)
    assert core.direct_script_result(True)
    assert core.update_direct_ack(5.2, BoardMode.DIRECT_MODE)
    assert core.begin_hardware_start(5.21)
    measured = (0.1, 0.2, -0.3, 0.0, -0.1, 0.2, -0.3, 0.0)
    assert core.hardware_ready(5.22, measured)
    return core, writer, measured


def advance_to_settle(core: DirectControllerCore) -> None:
    core.step_stand(5.22, 0.02, runtime(stable=False))
    core.step_stand(5.50, 0.02, runtime())
    core.step_stand(5.76, 0.02, runtime())
    assert core.state == LifecycleState.STANDING_SETTLE


def advance_to_rl_running(core: DirectControllerCore) -> None:
    advance_to_settle(core)
    core.step_stand(10.77, 0.02, runtime())
    assert core.state == LifecycleState.RL_RUNNING


def test_default_launch_and_core_are_inert_and_unarmed():
    core, writer, precheck = ready_core(enabled=False)
    assert not core.arm(TestStage.STAND_ONLY, precheck)
    assert core.state == LifecycleState.READY_FOR_TAKEOVER
    assert not core.operator_armed and writer.claim_count == 0 and writer.writes == []


def test_idle_is_required_for_takeover_preflight():
    core = DirectControllerCore(config(), stand(), FakeWriter())
    core.update_precheck(0.0, sample("balance"))
    core.update_precheck(10.0, sample("balance"))
    assert core.state == LifecycleState.BOOT_CHECK


def test_preflight_requires_five_continuous_seconds_and_resets():
    core = DirectControllerCore(config(), stand(), FakeWriter())
    core.update_precheck(0.0, sample())
    assert not core.update_precheck(4.9, sample())
    core.update_precheck(4.95, sample(logger_ready=False))
    core.update_precheck(5.0, sample())
    assert not core.update_precheck(9.9, sample())
    assert core.update_precheck(10.0, sample())


@pytest.mark.parametrize(
    "change",
    [
        {"vendor_service_active": False},
        {"direct_files_ready": False},
        {"stand_source_ready": False},
        {"logger_ready": False},
    ],
)
def test_preflight_blocks_missing_required_evidence(change):
    core = DirectControllerCore(config(), stand(), FakeWriter())
    core.update_precheck(0.0, sample(**change))
    assert core.state == LifecycleState.BOOT_CHECK


@pytest.mark.parametrize(
    "change",
    [
        {"sensors_fresh": False},
        {"joystick_fresh": False},
        {"joystick_centered": False},
        {"motors_online": False},
        {"values_finite": False},
        {"policy_loaded": False},
        {"obs_shape": 0},
        {"history_shape": 330},
        {"action_shape": 0},
    ],
)
def test_vendor_sensor_command_and_policy_diagnostics_do_not_gate_stage1_preflight(change):
    core = DirectControllerCore(config(), stand(), FakeWriter())
    degraded = sample(**change)
    assert not core.update_precheck(0.0, degraded)
    assert core.update_precheck(5.0, degraded)
    assert core.state == LifecycleState.READY_FOR_TAKEOVER
    assert degraded.diagnostics()


def test_launch_arguments_cannot_auto_arm_and_mode_evidence_is_required():
    precheck = sample(ack=False)
    core, writer, _ = ready_core(precheck=precheck)
    assert not core.arm(TestStage.STAND_ONLY, precheck)
    assert writer.claim_count == 0 and not core.operator_armed


def test_vendor_service_and_nodes_gate_can_release_then_start_script():
    core, _, precheck = ready_core()
    assert core.arm(TestStage.STAND_ONLY, precheck)
    assert not core.confirm_vendor_stopped(False, 0)
    assert not core.confirm_vendor_stopped(True, 1)
    assert core.confirm_vendor_stopped(True, 0)
    assert not core.confirm_can_release(1)
    assert core.confirm_can_release(0)
    assert core.begin_direct_request(5.1)
    assert not core.begin_direct_request(5.2)
    assert core.direct_request_count == 1


def test_start_script_failure_faults_before_hardware():
    core, _, precheck = ready_core()
    core.arm(TestStage.STAND_ONLY, precheck)
    core.confirm_vendor_stopped(True, 0)
    core.confirm_can_release(0)
    core.begin_direct_request(5.1)
    assert not core.direct_script_result(False)
    assert core.state == LifecycleState.FAULT and core.fault_code == "start_bash_failed"


def test_direct_ack_timeout_writes_nothing():
    core, writer, precheck = ready_core(cfg=config(direct_ack_timeout_sec=0.5))
    core.arm(TestStage.STAND_ONLY, precheck)
    core.confirm_vendor_stopped(True, 0)
    core.confirm_can_release(0)
    core.begin_direct_request(5.1)
    core.direct_script_result(True)
    assert not core.update_direct_ack(5.61, BoardMode.DIRECT_REQUESTED)
    assert core.state == LifecycleState.FAULT and writer.writes == [] and not writer.claimed


def test_no_command_or_claim_before_direct_ack():
    core, writer, precheck = ready_core()
    core.arm(TestStage.STAND_ONLY, precheck)
    core.confirm_vendor_stopped(True, 0)
    core.confirm_can_release(0)
    core.begin_direct_request(5.1)
    assert not core.begin_hardware_start(5.2)
    assert not writer.claimed and writer.writes == []


def test_composite_confirmation_starts_hardware_only_after_successful_official_script():
    core, writer, precheck = ready_core()
    assert core.arm(TestStage.STAND_ONLY, precheck)
    assert core.confirm_vendor_stopped(True, 0)
    assert core.confirm_can_release(0)
    assert not core.begin_hardware_start_pending_composite_confirmation(5.0)
    assert core.begin_direct_request(5.1)
    assert not core.begin_hardware_start_pending_composite_confirmation(5.11)
    # A script result must be recorded before the supervisor calls the composite transition.
    # The core deliberately remains command-free; the production C++ controller owns commands.
    assert core.direct_script_result(True)
    assert core.begin_hardware_start_pending_composite_confirmation(5.12)
    assert core.state == LifecycleState.HARDWARE_STARTING
    assert not writer.claimed and writer.writes == []
    assert core.confirm_composite_direct()
    assert core.state == LifecycleState.STAND_UP


def test_direct_confirmation_claims_one_owner_and_first_command_is_measured_stand():
    core, writer, measured = hardware_core()
    command = core.step_stand(5.22, 0.02, runtime(stable=False))
    assert core.state == LifecycleState.STAND_UP
    assert writer.claim_count == 1 and len(writer.writes) == 1
    assert np.allclose(command.position, measured)
    assert command.velocity[3] == 0.0 and command.velocity[7] == 0.0


def test_duplicate_writer_blocks_before_first_command():
    writer = FakeWriter()
    writer.duplicate_writer_detected = True
    core, _, precheck = ready_core(writer=writer)
    core.arm(TestStage.STAND_ONLY, precheck)
    core.confirm_vendor_stopped(True, 0)
    core.confirm_can_release(0)
    core.begin_direct_request(5.1)
    core.direct_script_result(True)
    core.update_direct_ack(5.2, BoardMode.DIRECT_MODE)
    core.begin_hardware_start(5.21)
    assert not core.hardware_ready(5.22, (0.0,) * 8)
    assert core.state == LifecycleState.FAULT and writer.writes == []


def test_transform_up_is_bounded_measured_to_official_fold_then_stand():
    core, _, measured = hardware_core(cfg=config(max_leg_target_slew_rad_s=0.5))
    first = core.step_stand(5.22, 0.02, runtime(stable=False))
    second = core.step_stand(5.27, 0.02, runtime(stable=False))
    assert np.max(np.abs(np.asarray(second.position) - np.asarray(first.position))) <= 0.025 + 1e-9
    assert np.allclose(first.position, measured)


def test_standing_completion_and_five_second_settle_are_continuous():
    core, _, _ = hardware_core(stage=TestStage.JOYSTICK_RL)
    advance_to_settle(core)
    core.step_stand(10.60, 0.02, runtime())
    assert core.state == LifecycleState.STANDING_SETTLE
    core.step_stand(10.70, 0.02, runtime(stable=False))
    assert core.settle_started_at is None
    core.step_stand(10.71, 0.02, runtime())
    core.step_stand(15.70, 0.02, runtime())
    assert core.state == LifecycleState.STANDING_SETTLE
    core.step_stand(15.72, 0.02, runtime())
    assert core.state == LifecycleState.RL_RUNNING


def test_stage1_ends_in_safe_hold_without_rl_command():
    core, writer, _ = hardware_core(stage=TestStage.STAND_ONLY)
    advance_to_settle(core)
    count_before = len(writer.writes)
    core.step_stand(10.77, 0.02, runtime())
    assert core.state == LifecycleState.SAFE_HOLD
    assert core.fault_code == "stage1_complete"
    assert len(writer.writes) == count_before + 2  # last stand command, then SAFE_HOLD


def test_watchdog_during_settle_enters_safe_hold_and_blocks_rl():
    core, _, _ = hardware_core(stage=TestStage.JOYSTICK_RL)
    advance_to_settle(core)
    core.step_stand(6.0, 0.02, runtime(sensors_fresh=False))
    assert core.state == LifecycleState.SAFE_HOLD and core.fault_code == "stand_watchdog"


def test_five_second_stand_switches_directly_to_native_rl():
    core, _, _ = hardware_core(stage=TestStage.JOYSTICK_RL)
    advance_to_rl_running(core)
    target = np.asarray(stand().stand_position)
    target[[0, 1, 2, 4, 5, 6]] += 0.1
    moving = PolicyReadiness(1, True, (0.0,) * 8, tuple(target), (19.61, -15.43))
    command = core.step_rl(10.79, 0.02, runtime(), moving)
    assert np.allclose(
        np.asarray(command.position)[[0, 1, 2, 4, 5, 6]],
        target[[0, 1, 2, 4, 5, 6]],
    )
    assert command.velocity[3] == pytest.approx(19.61)
    assert command.velocity[7] == pytest.approx(-15.43)
    assert core.state == LifecycleState.RL_RUNNING


def test_rl_watchdog_never_holds_last_rl_action():
    core, writer, _ = hardware_core(stage=TestStage.JOYSTICK_RL)
    advance_to_rl_running(core)
    moving = PolicyReadiness(
        1, True, (0.0,) * 8, stand().stand_position, (4.0, -4.0)
    )
    core.step_rl(12.0, 0.02, runtime(), moving)
    last_rl = writer.writes[-1]
    hold = core.step_rl(12.02, 0.02, runtime(loop_timing_valid=False), moving)
    assert core.state == LifecycleState.SAFE_HOLD
    assert abs(hold.velocity[3]) < abs(last_rl.velocity[3])
    assert abs(hold.velocity[7]) < abs(last_rl.velocity[7])
    assert hold != last_rl


def test_unknown_recovery_keeps_command_owner_and_blocks_automatic_exit():
    core, writer, _ = hardware_core()
    core.enter_safe_hold(runtime().joint_position, "test_stop")
    assert not core.begin_recovery(False)
    assert core.state == LifecycleState.RECOVERY_REQUIRED and writer.claimed and writer.release_count == 0


def test_confirmed_recovery_releases_only_after_auto_ack_and_vendor_ready():
    core, writer, _ = hardware_core()
    core.enter_safe_hold(runtime().joint_position, "test_stop")
    assert core.begin_recovery(True)
    assert not core.confirm_recovery(BoardMode.UNKNOWN, False)
    assert writer.claimed


def test_process_restart_constructs_unarmed_boot_check():
    writer = FakeWriter()
    core = DirectControllerCore(config(), stand(), writer)
    assert core.state == LifecycleState.BOOT_CHECK
    assert not core.operator_armed and not writer.claimed


def test_official_start_script_parser_records_frames_delay_and_missing_ack(tmp_path):
    script = tmp_path / "start.bash"
    script.write_text(
        "#!/bin/bash\n"
        "cansend can0 170##200000000000200000000\n"
        "sleep 0.2\n"
        "cansend can0 170##200000000000203000000\n",
        encoding="utf-8",
    )
    inspection = inspect_official_start_script(script)
    assert inspection.can_interface == "can0"
    assert inspection.can_id == 0x170
    assert inspection.frame_flags == (2, 2)
    assert len(inspection.frame_payloads) == 2
    assert inspection.inter_frame_delays_sec == (0.2,)
    assert not inspection.shell_has_errexit
    assert not inspection.acknowledgment_present
    assert not inspection.rollback_present


def test_managed_wrapper_requires_full_authorization_hash_and_runs_once(tmp_path):
    script = tmp_path / "start.bash"
    script.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    script.chmod(0o664)
    backend = ManagedTakeoverBackend(
        service_name="tita-bringup.service",
        start_script=script,
        expected_start_sha256=sha256_file(script),
        hardware_launch=("false",),
        enforce_can_interface_up=False,
    )
    blocked = TakeoverAuthorization(False, True, True, True, True, True, True)
    with pytest.raises(PermissionError):
        backend.execute_start_script_once(blocked)
    allowed = TakeoverAuthorization(True, True, True, True, True, True, True)
    result = backend.execute_start_script_once(allowed)
    assert result.returncode == 0 and backend.start_execution_count == 1
    assert result.argv == ("/usr/bin/bash", str(script.resolve()))
    with pytest.raises(RuntimeError):
        backend.execute_start_script_once(allowed)


def test_managed_wrapper_persists_one_attempt_per_power_session(tmp_path):
    script = tmp_path / "start.bash"
    script.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    script.chmod(0o664)
    ledger = tmp_path / "direct_session.json"
    kwargs = dict(
        service_name="tita-bringup.service",
        start_script=script,
        expected_start_sha256=sha256_file(script),
        hardware_launch=("false",),
        power_session_id="operator-session-1",
        session_ledger=ledger,
        enforce_can_interface_up=False,
    )
    allowed = TakeoverAuthorization(True, True, True, True, True, True, True)
    first = ManagedTakeoverBackend(**kwargs)
    assert first.execute_start_script_once(allowed).returncode == 0
    restarted = ManagedTakeoverBackend(**kwargs)
    with pytest.raises(RuntimeError, match="powered session"):
        restarted.execute_start_script_once(allowed)


def test_stage1_orchestrator_enforces_exact_takeover_order_without_sleep():
    backend = FakeTakeoverBackend()
    events = []
    authorization = TakeoverAuthorization(True, True, True, True, True, False, False)
    result = Stage1TakeoverOrchestrator(backend).execute(
        authorization,
        event_callback=lambda event, detail: events.append((event, detail)),
        service_timeout_sec=7.0,
        start_timeout_sec=2.0,
    )
    assert [call[0] for call in backend.calls] == [
        "stop_vendor_service",
        "wait_vendor_service_inactive",
        "inspect_vendor_processes",
        "inspect_can_owners",
        "execute_start_script_once",
        "start_hardware",
    ]
    assert [event for event, _ in events] == [
        "vendor_stop_request",
        "vendor_stop_result",
        "vendor_process_inventory",
        "vendor_stopped",
        "can_owner_inventory",
        "can_released",
        "direct_request",
        "start_bash_result",
        "hardware_starting",
        "hardware_started",
    ]
    assert result.hardware_pid == 4242


def test_readonly_soak_stops_and_releases_without_start_script_or_motor_output():
    backend = FakeTakeoverBackend()
    events = []
    authorization = TakeoverAuthorization(True, True, False, False, True, False, False)
    result = DirectSoakOrchestrator(backend).execute(
        authorization,
        event_callback=lambda event, detail: events.append((event, detail)),
        service_timeout_sec=7.0,
    )
    assert [call[0] for call in backend.calls] == [
        "stop_vendor_service",
        "wait_vendor_service_inactive",
        "inspect_vendor_processes",
        "inspect_can_owners",
        "start_readonly_soak",
    ]
    assert "execute_start_script_once" not in [call[0] for call in backend.calls]
    assert "start_hardware" not in [call[0] for call in backend.calls]
    assert [event for event, _ in events][-2:] == [
        "readonly_soak_starting", "readonly_soak_started"]
    assert result.hardware_pid == 4343


@pytest.mark.parametrize(
    "field,value,expected_last_call",
    [
        ("inactive", False, "wait_vendor_service_inactive"),
        ("vendor_processes", ((123, "hardware_bridge"),), "inspect_vendor_processes"),
        ("can_owners", (1, (456,), "owner remains"), "inspect_can_owners"),
        ("start_ok", False, "execute_start_script_once"),
    ],
)
def test_stage1_orchestrator_fails_closed_before_next_mutation(field, value, expected_last_call):
    backend = FakeTakeoverBackend()
    setattr(backend, field, value)
    authorization = TakeoverAuthorization(True, True, True, True, True, False, False)
    with pytest.raises(RuntimeError):
        Stage1TakeoverOrchestrator(backend).execute(authorization)
    assert backend.calls[-1][0] == expected_last_call
    assert not any(call[0] == "start_hardware" for call in backend.calls)


def test_static_launch_defaults_are_inert_and_have_no_hidden_command_path():
    root = Path(__file__).resolve().parents[1]
    launch = (root / "launch/direct_rl_mode.launch.py").read_text(encoding="utf-8")
    config_text = (root / "config/direct_rl_mode.yaml").read_text(encoding="utf-8")
    for name in (
        "execute_vendor_stop", "execute_start_bash", "enable_hardware_output", "operator_arm",
        "auto_enter_rl", "direct_soak_only", "emergency_procedure_confirmed",
    ):
        assert f'("{name}", "false")' in launch
        assert f"{name}: false" in config_text
    assert '("power_session_id", "")' in launch
    assert "respawn=False" in launch and "respawn: false" in config_text
    for forbidden in ("ExecuteProcess", "OnShutdown", "ros2 topic pub", "cmd_key=", "cansend"):
        assert forbidden not in launch


def test_play_launch_selects_joystick_stage2_and_remains_unarmed():
    root = Path(__file__).resolve().parents[1]
    launch = (root / "launch/play.launch.py").read_text(encoding="utf-8")
    assert '"requested_stage": 2' in launch
    assert '"execute_vendor_stop": True' in launch
    assert '"execute_start_bash": True' in launch
    assert '"enable_hardware_output": True' in launch
    assert '"operator_arm": False' in launch
    assert "Stage 2 switches directly to native-policy joystick RL" in launch
    for forbidden in ("ExecuteProcess", "OnShutdown", "cansend", "operator_arm\": True"):
        assert forbidden not in launch


def test_production_supervisor_exposes_only_stage1_and_stage2():
    root = Path(__file__).resolve().parents[1]
    source = (root / "tita_low_level_sdk/direct_rl_controller_node.py").read_text(
        encoding="utf-8"
    )
    assert "only Stage 1 stand or Stage 2 native-policy joystick RL is supported" in source
    assert "SMALL_JOYSTICK_RL" not in source


def test_production_supervisor_uses_vendor_runtime_only_for_idle_confirmation():
    root = Path(__file__).resolve().parents[1]
    source = (root / "tita_low_level_sdk/direct_rl_controller_node.py").read_text(
        encoding="utf-8"
    )
    assert 'f"{prefix}/locomotion/body/fsm_mode"' in source
    # Stage 2 may inspect vendor sensor/Joy topics only before takeover.  The conditional block
    # and explicit detach preserve the post-stop invariant: no vendor runtime dependency.
    stage2_preflight = source.index("if self.requested_stage == TestStage.JOYSTICK_RL:")
    detach = source.index("def _detach_vendor_runtime")
    for preflight_topic in (
        'f"{prefix}/joint_states"',
        'f"{prefix}/imu_sensor_broadcaster/imu"',
        'f"{prefix}/chassis/odometry"',
        'f"{prefix}/locomotion/motors_status"',
        'f"{prefix}/joy"',
    ):
        position = source.index(preflight_topic)
        assert stage2_preflight < position < detach
    assert 'f"{prefix}/command/manager/cmd_twist"' not in source
    assert "post-stop runtime uses only direct HardwareBridge/controller evidence" in source
    assert "post-stop runtime uses only direct HardwareBridge/controller evidence" in source


def test_production_supervisor_resolves_stand_profile_from_installed_package_share():
    root = Path(__file__).resolve().parents[1]
    source = (root / "tita_low_level_sdk/direct_rl_controller_node.py").read_text(
        encoding="utf-8"
    )
    assert 'get_package_share_directory("tita_low_level_sdk")' in source
    assert 'package_share / "config/tita_transform_up_official_e7b32d9.yaml"' in source
    assert 'package_root / "config/tita_transform_up_official_e7b32d9.yaml"' not in source


def test_readonly_soak_launch_is_token_gated_and_cannot_activate_stage1_output():
    root = Path(__file__).resolve().parents[2]
    direct_ws = root / "direct_ws"
    if not direct_ws.is_dir():
        direct_ws = Path.home() / "direct_ws"
    launch = (
        direct_ws / "src/tita_stage1_controller/launch/direct_readonly_soak.launch.py"
    ).read_text(encoding="utf-8")
    bridge = (
        direct_ws /
        "src/ddt_ros2_control/hardware/hardware_bridge/src/hardware_bridge_node.cpp"
    ).read_text(encoding="utf-8")
    assert "DIRECT_SOAK_ARMED" in launch
    assert '"hardware_output_enabled": "false"' in launch
    assert 'arguments=["tita_stage1_controller"' not in launch
    assert "!hardware_output_enabled_ || command_enable_ < 0.5" in bridge


def test_stage1_command_transport_and_hardware_log_are_correlated():
    root = Path(__file__).resolve().parents[2]
    direct_ws = root / "direct_ws"
    if not direct_ws.is_dir():
        direct_ws = Path.home() / "direct_ws"
    bridge = (
        direct_ws /
        "src/ddt_ros2_control/hardware/hardware_bridge/src/hardware_bridge_node.cpp"
    ).read_text(encoding="utf-8")
    controller = (
        direct_ws / "src/tita_stage1_controller/src/stage1_controller.cpp"
    ).read_text(encoding="utf-8")
    core = (
        direct_ws / "src/tita_stage1_controller/src/stage1_core.cpp"
    ).read_text(encoding="utf-8")
    assert "last_command_q_[id] = p.back()" in bridge
    assert "record.q[id] = p.back()" in bridge
    assert "record.written = success" in bridge
    assert "last_command_q_state_[i]->get_value()" in controller
    assert "UNEXPECTED_COMMAND_CLAMP" in core
    assert "std::clamp(mJoints[id].positionCommand" not in bridge
    assert "-2.670354" not in bridge
