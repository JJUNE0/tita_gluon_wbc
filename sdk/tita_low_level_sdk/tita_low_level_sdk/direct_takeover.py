from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
from typing import Callable, Mapping, Sequence


VENDOR_PROCESS_PATTERNS = (
    "hw_broadcaster_node",
    "command_manager_node",
    "teleop_command_node",
    "hardware_bridge",
    "commands_can",
    "controller_manager",
)


@dataclass(frozen=True, slots=True)
class StartScriptInspection:
    path: str
    sha256: str
    can_interface: str
    can_id: int
    frame_flags: tuple[int, ...]
    frame_payloads: tuple[str, ...]
    inter_frame_delays_sec: tuple[float, ...]
    shell_has_errexit: bool
    acknowledgment_present: bool
    rollback_present: bool


@dataclass(frozen=True, slots=True)
class CommandResult:
    argv: tuple[str, ...]
    monotonic_start_ns: int
    monotonic_end_ns: int
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False


@dataclass(frozen=True, slots=True)
class TakeoverAuthorization:
    operator_armed: bool
    execute_vendor_stop: bool
    execute_start_bash: bool
    enable_hardware_output: bool
    vendor_service_confirmed: bool
    vendor_nodes_absent: bool
    can_owners_zero: bool

    def allows_service_stop(self) -> bool:
        return self.operator_armed and self.execute_vendor_stop and self.vendor_service_confirmed

    def allows_start_script(self) -> bool:
        return (
            self.operator_armed
            and self.execute_start_bash
            and self.vendor_service_confirmed
            and self.vendor_nodes_absent
            and self.can_owners_zero
        )

    def allows_hardware_start(self) -> bool:
        return self.operator_armed and self.enable_hardware_output and self.allows_start_script()

    def allows_readonly_soak(self) -> bool:
        return (
            self.operator_armed
            and self.execute_vendor_stop
            and not self.execute_start_bash
            and not self.enable_hardware_output
            and self.vendor_service_confirmed
            and self.vendor_nodes_absent
            and self.can_owners_zero
        )


@dataclass(frozen=True, slots=True)
class Stage1TakeoverOutcome:
    stop_result: CommandResult
    start_result: CommandResult
    hardware_pid: int
    vendor_processes: tuple[tuple[int, str], ...]
    can_owner_count: int
    can_owner_pids: tuple[int, ...]
    can_owner_detail: str


@dataclass(frozen=True, slots=True)
class DirectSoakOutcome:
    stop_result: CommandResult
    hardware_pid: int
    vendor_processes: tuple[tuple[int, str], ...]
    can_owner_count: int
    can_owner_pids: tuple[int, ...]
    can_owner_detail: str


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_official_start_script(path: str | Path) -> StartScriptInspection:
    script = Path(path).resolve()
    lines = script.read_text(encoding="utf-8").splitlines()
    frames: list[tuple[str, int, int, str]] = []
    delays: list[float] = []
    frame_re = re.compile(r"^\s*cansend\s+(\S+)\s+([0-9A-Fa-f]+)##([0-9A-Fa-f])([0-9A-Fa-f]+)\s*$")
    sleep_re = re.compile(r"^\s*sleep\s+([0-9]+(?:\.[0-9]+)?)\s*$")
    for line in lines:
        match = frame_re.match(line)
        if match:
            frames.append((match.group(1), int(match.group(2), 16), int(match.group(3), 16), match.group(4).lower()))
            continue
        match = sleep_re.match(line)
        if match:
            delays.append(float(match.group(1)))
    if not frames:
        raise ValueError("official start script contains no parseable CAN-FD frame")
    interfaces = {item[0] for item in frames}
    can_ids = {item[1] for item in frames}
    if len(interfaces) != 1 or len(can_ids) != 1:
        raise ValueError("start script uses multiple CAN interfaces or CAN IDs")
    lower = "\n".join(lines).lower()
    return StartScriptInspection(
        path=str(script),
        sha256=sha256_file(script),
        can_interface=next(iter(interfaces)),
        can_id=next(iter(can_ids)),
        frame_flags=tuple(item[2] for item in frames),
        frame_payloads=tuple(item[3] for item in frames),
        inter_frame_delays_sec=tuple(delays),
        shell_has_errexit=bool(re.search(r"(^|\s)set\s+-[^\n]*e", lower)),
        acknowledgment_present=any(token in lower for token in ("ack", "status", "get_mode", "board_mode")),
        rollback_present=any(token in lower for token in ("rollback", "auto_locomotion", "reverse")),
    )


def _run(argv: Sequence[str], timeout_sec: float) -> CommandResult:
    start = time.monotonic_ns()
    try:
        result = subprocess.run(
            list(argv),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_sec,
            check=False,
        )
        return CommandResult(tuple(argv), start, time.monotonic_ns(), result.returncode, result.stdout, result.stderr)
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            tuple(argv), start, time.monotonic_ns(), -1,
            exc.stdout or "", exc.stderr or "", True,
        )
    except OSError as exc:
        return CommandResult(
            tuple(argv), start, time.monotonic_ns(), -1,
            "", f"{type(exc).__name__}: {exc}", False,
        )


def _proc_can_registration_entries(can_root: Path) -> tuple[str, ...]:
    """Return real SocketCAN receive registrations, excluding kernel empty-list markers."""
    entries: list[str] = []
    for name in ("rcvlist_all", "rcvlist_eff", "rcvlist_err", "rcvlist_fil", "rcvlist_inv"):
        path = can_root / name
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith(("device", "receive", "entries")):
                continue
            if re.fullmatch(r"\([^:()]+:\s*no entry\)", stripped, re.IGNORECASE):
                continue
            entries.append(f"{name}:{stripped}")
    return tuple(entries)


class ManagedTakeoverBackend:
    """The only production subprocess boundary; every mutating call requires an arm token.

    Construction and all ``inspect_*`` methods are command-free. No shell is used, the official
    start script is not reconstructed, and no shutdown callback invokes a state-changing command.
    """

    def __init__(
        self,
        *,
        service_name: str,
        start_script: str | Path,
        expected_start_sha256: str,
        hardware_launch: Sequence[str],
        soak_hardware_launch: Sequence[str] = (),
        power_session_id: str = "",
        session_ledger: str | Path | None = None,
        enforce_can_interface_up: bool = True,
        takeover_token_file: str | Path | None = None,
        requested_stage: int = 1,
    ) -> None:
        if service_name != "tita-bringup.service":
            raise ValueError("only the inspected TITA bringup service is accepted")
        self.service_name = service_name
        self.start_script = Path(start_script).resolve()
        self.expected_start_sha256 = expected_start_sha256
        self.hardware_launch = tuple(hardware_launch)
        self.soak_hardware_launch = tuple(soak_hardware_launch)
        self.power_session_id = power_session_id.strip()
        self.session_ledger = Path(session_ledger).resolve() if session_ledger else None
        self.enforce_can_interface_up = enforce_can_interface_up
        self.takeover_token_file = Path(takeover_token_file).resolve() if takeover_token_file else None
        if requested_stage not in (1, 2):
            raise ValueError("only Stage 1 stand or Stage 2 joystick RL takeover is supported")
        self.requested_stage = requested_stage
        self.start_execution_count = 0
        self.hardware_process: subprocess.Popen[str] | None = None

    def inspect_service_active(self) -> bool:
        result = _run(("systemctl", "is-active", "--quiet", self.service_name), 2.0)
        return result.returncode == 0

    @staticmethod
    def inspect_vendor_processes() -> tuple[tuple[int, str], ...]:
        matches: list[tuple[int, str]] = []
        for entry in Path("/proc").iterdir():
            if not entry.name.isdigit():
                continue
            try:
                cmdline = (entry / "cmdline").read_bytes().replace(b"\0", b" ").decode("utf-8", "replace")
            except (FileNotFoundError, PermissionError, ProcessLookupError):
                continue
            if any(pattern in cmdline for pattern in VENDOR_PROCESS_PATTERNS):
                matches.append((int(entry.name), cmdline.strip()))
        return tuple(sorted(matches))

    @staticmethod
    def inspect_can_owners() -> tuple[int, tuple[int, ...], str]:
        result = _run(("ss", "-a", "-p", "-f", "can"), 2.0)
        if result.returncode != 0:
            can_root = Path("/proc/net/can")
            entries = _proc_can_registration_entries(can_root)
            if entries:
                return -1, (), "SocketCAN receive registrations remain: " + " | ".join(entries)
            if can_root.is_dir():
                return 0, (), "ss CAN family unavailable; /proc/net/can receive registrations are empty"
            return -1, (), result.stderr.strip() or "SocketCAN owner inspection unavailable"
        pids = tuple(sorted({int(value) for value in re.findall(r"pid=(\d+)", result.stdout)}))
        # SocketCAN lines without process attribution are unknown ownership, not zero ownership.
        socket_lines = tuple(line for line in result.stdout.splitlines() if line.strip() and not line.lower().startswith("netid"))
        if socket_lines and not pids:
            return -1, (), "SocketCAN sockets exist but owner PIDs are unavailable"
        return len(pids), pids, ""

    def stop_vendor_service(self, authorization: TakeoverAuthorization, timeout_sec: float = 10.0) -> CommandResult:
        if not authorization.allows_service_stop():
            raise PermissionError("vendor service stop is not explicitly armed")
        return _run(("sudo", "-n", "systemctl", "stop", self.service_name), timeout_sec)

    def wait_vendor_service_inactive(self, timeout_sec: float = 10.0) -> bool:
        deadline = time.monotonic() + timeout_sec
        while time.monotonic() < deadline:
            if not self.inspect_service_active():
                return True
            time.sleep(0.05)
        return not self.inspect_service_active()

    def _session_already_attempted(self) -> bool:
        if self.session_ledger is None or not self.session_ledger.is_file():
            return False
        try:
            data = json.loads(self.session_ledger.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            raise RuntimeError("Direct session ledger is unreadable; board mode is UNKNOWN")
        return data.get("power_session_id") == self.power_session_id and bool(data.get("attempted"))

    def _record_session_attempt(self) -> None:
        if self.session_ledger is None:
            return
        if not self.power_session_id:
            raise RuntimeError("an operator-confirmed full-power session id is required")
        self.session_ledger.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.session_ledger.with_suffix(self.session_ledger.suffix + ".tmp")
        temporary.write_text(json.dumps({
            "power_session_id": self.power_session_id,
            "attempted": True,
            "monotonic_ns": time.monotonic_ns(),
            "script_sha256": self.expected_start_sha256,
        }, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temporary, self.session_ledger)

    def execute_start_script_once(
        self,
        authorization: TakeoverAuthorization,
        timeout_sec: float = 3.0,
    ) -> CommandResult:
        if not authorization.allows_start_script():
            raise PermissionError("Direct Mode request preconditions are not satisfied")
        if self.start_execution_count != 0:
            raise RuntimeError("official start script execution already attempted in this process")
        if self._session_already_attempted():
            raise RuntimeError("official start script already attempted in this powered session")
        actual_hash = sha256_file(self.start_script)
        if actual_hash != self.expected_start_sha256:
            raise RuntimeError(f"start script SHA256 mismatch: {actual_hash}")
        if self.enforce_can_interface_up:
            inspection = inspect_official_start_script(self.start_script)
            operstate = Path("/sys/class/net") / inspection.can_interface / "operstate"
            if not operstate.is_file() or operstate.read_text(encoding="utf-8").strip() not in {"up", "unknown"}:
                raise RuntimeError(f"{inspection.can_interface} does not exist or is not up")
        self._record_session_attempt()
        self.start_execution_count += 1
        # Execute the exact verified official file through Bash. The pinned upstream script is
        # intentionally kept byte-for-byte unchanged and may be installed without an executable
        # mode bit; invoking an interpreter avoids chmod/copy/reimplementation drift.
        return _run(("/usr/bin/bash", str(self.start_script)), timeout_sec)

    def start_hardware(self, authorization: TakeoverAuthorization) -> int:
        if not authorization.allows_hardware_start():
            raise PermissionError("hardware activation is not explicitly armed")
        if self.hardware_process is not None:
            raise RuntimeError("hardware process has already been started")
        if self.takeover_token_file is None:
            raise RuntimeError("supervisor takeover token path is not configured")
        self.takeover_token_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            descriptor = os.open(
                self.takeover_token_file,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
            )
        except FileExistsError as exc:
            raise RuntimeError("stale takeover token exists; refusing hardware start") from exc
        with os.fdopen(descriptor, "w", encoding="utf-8") as token_stream:
            token_stream.write({
                1: "DIRECT_STAGE1_ARMED\n",
                2: "DIRECT_STAGE2_ARMED\n",
            }[self.requested_stage])
        try:
            self.hardware_process = subprocess.Popen(
                list(self.hardware_launch),
                stdin=subprocess.DEVNULL,
                stdout=None,
                stderr=None,
                text=True,
                start_new_session=True,
            )
        except Exception:
            self.takeover_token_file.unlink(missing_ok=True)
            raise
        return int(self.hardware_process.pid)

    def start_readonly_soak(self, authorization: TakeoverAuthorization) -> int:
        if not authorization.allows_readonly_soak():
            raise PermissionError("read-only Direct soak is not explicitly armed")
        if not self.soak_hardware_launch:
            raise RuntimeError("read-only Direct soak launch is not configured")
        if self.hardware_process is not None:
            raise RuntimeError("hardware process has already been started")
        if self.takeover_token_file is None:
            raise RuntimeError("supervisor soak token path is not configured")
        self.takeover_token_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            descriptor = os.open(
                self.takeover_token_file,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
            )
        except FileExistsError as exc:
            raise RuntimeError("stale takeover token exists; refusing read-only soak") from exc
        with os.fdopen(descriptor, "w", encoding="utf-8") as token_stream:
            token_stream.write("DIRECT_SOAK_ARMED\n")
        try:
            self.hardware_process = subprocess.Popen(
                list(self.soak_hardware_launch),
                stdin=subprocess.DEVNULL,
                stdout=None,
                stderr=None,
                text=True,
                start_new_session=True,
            )
        except Exception:
            self.takeover_token_file.unlink(missing_ok=True)
            raise
        return int(self.hardware_process.pid)


TakeoverEventCallback = Callable[[str, Mapping[str, object]], None]


class Stage1TakeoverOrchestrator:
    """Execute the one authorized Stage 1 takeover sequence without a shell.

    Merely constructing this object is command-free. ``execute`` is the only mutating entry point
    and must therefore be called only from the explicit READY-state operator-arm service after the
    user has approved the real test. Every transition is reported before the next gate is crossed.
    """

    def __init__(self, backend: ManagedTakeoverBackend) -> None:
        self.backend = backend

    @staticmethod
    def _emit(callback: TakeoverEventCallback | None, event: str, **detail: object) -> None:
        if callback is not None:
            callback(event, detail)

    def execute(
        self,
        authorization: TakeoverAuthorization,
        *,
        event_callback: TakeoverEventCallback | None = None,
        service_timeout_sec: float = 10.0,
        start_timeout_sec: float = 3.0,
    ) -> Stage1TakeoverOutcome:
        if not authorization.allows_service_stop():
            raise PermissionError("Stage 1 takeover is not explicitly armed for vendor stop")

        self._emit(event_callback, "vendor_stop_request", service=self.backend.service_name)
        stop_result = self.backend.stop_vendor_service(authorization, service_timeout_sec)
        self._emit(
            event_callback,
            "vendor_stop_result",
            returncode=stop_result.returncode,
            timed_out=stop_result.timed_out,
            monotonic_start_ns=stop_result.monotonic_start_ns,
            monotonic_end_ns=stop_result.monotonic_end_ns,
            stdout=stop_result.stdout,
            stderr=stop_result.stderr,
        )
        if stop_result.timed_out or stop_result.returncode != 0:
            raise RuntimeError(f"vendor service stop failed: rc={stop_result.returncode}")
        if not self.backend.wait_vendor_service_inactive(service_timeout_sec):
            raise RuntimeError("vendor service did not become inactive")

        vendor_processes = self.backend.inspect_vendor_processes()
        self._emit(
            event_callback,
            "vendor_process_inventory",
            count=len(vendor_processes),
            pids=tuple(pid for pid, _ in vendor_processes),
        )
        if vendor_processes:
            raise RuntimeError("vendor ROS/hardware process remains after service stop")
        self._emit(event_callback, "vendor_stopped", remaining_vendor_nodes=0)

        can_owner_count, can_owner_pids, can_owner_detail = self.backend.inspect_can_owners()
        self._emit(
            event_callback,
            "can_owner_inventory",
            count=can_owner_count,
            pids=can_owner_pids,
            detail=can_owner_detail,
        )
        if can_owner_count != 0:
            raise RuntimeError(
                f"CAN ownership is not proven released: count={can_owner_count}; {can_owner_detail}"
            )
        self._emit(event_callback, "can_released", can_owner_count=0)

        released = replace(authorization, vendor_nodes_absent=True, can_owners_zero=True)
        self._emit(event_callback, "direct_request")
        start_result = self.backend.execute_start_script_once(released, start_timeout_sec)
        self._emit(
            event_callback,
            "start_bash_result",
            returncode=start_result.returncode,
            timed_out=start_result.timed_out,
            monotonic_start_ns=start_result.monotonic_start_ns,
            monotonic_end_ns=start_result.monotonic_end_ns,
            stdout=start_result.stdout,
            stderr=start_result.stderr,
        )
        if start_result.timed_out or start_result.returncode != 0:
            raise RuntimeError(f"official start.bash failed: rc={start_result.returncode}")

        # There is intentionally no sleep here. The official bridge is started immediately and
        # completes the documented composite Direct confirmation from real state/feedback.
        self._emit(event_callback, "hardware_starting")
        hardware_pid = self.backend.start_hardware(released)
        self._emit(event_callback, "hardware_started", pid=hardware_pid)
        return Stage1TakeoverOutcome(
            stop_result=stop_result,
            start_result=start_result,
            hardware_pid=hardware_pid,
            vendor_processes=vendor_processes,
            can_owner_count=can_owner_count,
            can_owner_pids=can_owner_pids,
            can_owner_detail=can_owner_detail,
        )


class DirectSoakOrchestrator:
    """Stop/release the vendor stack and start an output-disabled HardwareBridge soak.

    This path deliberately does not call the official start script and cannot enable a motor API
    write. It is still a real service-stop/hardware-activation operation and must be entered only
    through the separate operator-arm service after explicit approval.
    """

    def __init__(self, backend: ManagedTakeoverBackend) -> None:
        self.backend = backend

    def execute(
        self,
        authorization: TakeoverAuthorization,
        *,
        event_callback: TakeoverEventCallback | None = None,
        service_timeout_sec: float = 10.0,
    ) -> DirectSoakOutcome:
        if not authorization.allows_service_stop():
            raise PermissionError("Direct soak is not explicitly armed for vendor stop")

        Stage1TakeoverOrchestrator._emit(
            event_callback, "vendor_stop_request", service=self.backend.service_name)
        stop_result = self.backend.stop_vendor_service(authorization, service_timeout_sec)
        Stage1TakeoverOrchestrator._emit(
            event_callback,
            "vendor_stop_result",
            returncode=stop_result.returncode,
            timed_out=stop_result.timed_out,
            monotonic_start_ns=stop_result.monotonic_start_ns,
            monotonic_end_ns=stop_result.monotonic_end_ns,
            stdout=stop_result.stdout,
            stderr=stop_result.stderr,
        )
        if stop_result.timed_out or stop_result.returncode != 0:
            raise RuntimeError(f"vendor service stop failed: rc={stop_result.returncode}")
        if not self.backend.wait_vendor_service_inactive(service_timeout_sec):
            raise RuntimeError("vendor service did not become inactive")

        vendor_processes = self.backend.inspect_vendor_processes()
        Stage1TakeoverOrchestrator._emit(
            event_callback,
            "vendor_process_inventory",
            count=len(vendor_processes),
            pids=tuple(pid for pid, _ in vendor_processes),
        )
        if vendor_processes:
            raise RuntimeError("vendor ROS/hardware process remains after service stop")
        Stage1TakeoverOrchestrator._emit(
            event_callback, "vendor_stopped", remaining_vendor_nodes=0)

        can_owner_count, can_owner_pids, can_owner_detail = self.backend.inspect_can_owners()
        Stage1TakeoverOrchestrator._emit(
            event_callback,
            "can_owner_inventory",
            count=can_owner_count,
            pids=can_owner_pids,
            detail=can_owner_detail,
        )
        if can_owner_count != 0:
            raise RuntimeError(
                f"CAN ownership is not proven released: count={can_owner_count}; {can_owner_detail}"
            )
        Stage1TakeoverOrchestrator._emit(
            event_callback, "can_released", can_owner_count=0)

        released = replace(authorization, vendor_nodes_absent=True, can_owners_zero=True)
        Stage1TakeoverOrchestrator._emit(
            event_callback,
            "readonly_soak_starting",
            start_bash_executed=False,
            hardware_output_enabled=False,
        )
        hardware_pid = self.backend.start_readonly_soak(released)
        Stage1TakeoverOrchestrator._emit(
            event_callback, "readonly_soak_started", pid=hardware_pid)
        return DirectSoakOutcome(
            stop_result=stop_result,
            hardware_pid=hardware_pid,
            vendor_processes=vendor_processes,
            can_owner_count=can_owner_count,
            can_owner_pids=can_owner_pids,
            can_owner_detail=can_owner_detail,
        )
