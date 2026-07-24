from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SafetyResult:
    ok: bool
    status: str


class SafetyGate:
    """Fail-closed dry-run checks. Command output is intentionally not implemented."""

    def __init__(self, command_enabled: bool, allow_command_output: bool, max_action_abs: float = 100.0) -> None:
        self.command_enabled = bool(command_enabled)
        self.allow_command_output = bool(allow_command_output)
        self.max_action_abs = float(max_action_abs)

    def evaluate(
        self,
        sensors_fresh: bool,
        missing_joint_names: tuple[str, ...],
        values_finite: bool,
        motors_status_ready: bool,
        fsm_mode_ready: bool,
        action: np.ndarray | None,
    ) -> SafetyResult:
        if self.command_enabled or self.allow_command_output:
            return SafetyResult(False, "FAIL-CLOSED: command output flags must remain false; no command output exists")
        if not sensors_fresh:
            return SafetyResult(False, "waiting for fresh joint_states, imu, and odometry")
        if missing_joint_names:
            return SafetyResult(False, f"missing required joints: {', '.join(missing_joint_names)}")
        if not values_finite:
            return SafetyResult(False, "non-finite sensor, observation, or action value")
        if not motors_status_ready:
            return SafetyResult(False, "waiting for motors_status")
        if not fsm_mode_ready:
            return SafetyResult(False, "waiting for fsm_mode")
        if action is not None and float(np.max(np.abs(action))) > self.max_action_abs:
            return SafetyResult(False, "action exceeds dry-run diagnostic magnitude limit")
        return SafetyResult(True, "DRY-RUN SAFE: command output disabled; virtual targets only")
