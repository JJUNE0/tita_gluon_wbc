from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class PolicyGateResult:
    ready: bool
    status: str


class PolicyDryRunGate:
    """Pure fail-closed gate for deciding whether dry-run inference is valid."""

    def __init__(
        self,
        allowed_modes: list[str],
        fsm_timeout_sec: float,
        require_fsm_freshness: bool,
        fsm_settle_time_sec: float,
        require_pose_gate: bool,
        require_motion_gate: bool,
        max_leg_position_error_rad: float,
        max_base_angular_velocity_rad_s: float,
        max_projected_gravity_norm_error: float,
    ) -> None:
        self.allowed_modes = {mode.strip().lower() for mode in allowed_modes if mode.strip()}
        self.fsm_timeout_sec = max(float(fsm_timeout_sec), 0.0)
        self.require_fsm_freshness = bool(require_fsm_freshness)
        self.fsm_settle_time_sec = max(float(fsm_settle_time_sec), 0.0)
        self.require_pose_gate = bool(require_pose_gate)
        self.require_motion_gate = bool(require_motion_gate)
        self.max_leg_position_error_rad = max(float(max_leg_position_error_rad), 0.0)
        self.max_base_angular_velocity_rad_s = max(float(max_base_angular_velocity_rad_s), 0.0)
        self.max_projected_gravity_norm_error = max(float(max_projected_gravity_norm_error), 0.0)
        self.mode = ""
        self.mode_received_at: float | None = None
        self.mode_since: float | None = None

    def update_mode(self, mode: str, now: float) -> bool:
        normalized = str(mode).strip().lower()
        changed = normalized != self.mode
        if changed:
            self.mode = normalized
            self.mode_since = float(now)
        self.mode_received_at = float(now)
        return changed

    def evaluate(
        self,
        now: float,
        sensors_fresh: bool,
        values_finite: bool,
        max_leg_position_error_rad: float,
        base_angular_velocity_norm: float,
        projected_gravity: np.ndarray,
    ) -> PolicyGateResult:
        if not self.allowed_modes:
            return PolicyGateResult(False, "blocked:no_allowed_fsm_modes_configured")
        if self.mode_received_at is None:
            return PolicyGateResult(False, "blocked:fsm_not_received")
        if self.require_fsm_freshness and now - self.mode_received_at > self.fsm_timeout_sec:
            return PolicyGateResult(False, "blocked:fsm_stale")
        if self.mode not in self.allowed_modes:
            return PolicyGateResult(False, f"blocked:fsm_mode_not_allowed:{self.mode or '<empty>'}")
        if self.mode_since is None or now - self.mode_since < self.fsm_settle_time_sec:
            return PolicyGateResult(False, "blocked:fsm_settling")
        if not sensors_fresh or not values_finite:
            return PolicyGateResult(False, "blocked:pose_gate")

        gravity = np.asarray(projected_gravity, dtype=np.float32).reshape(-1)
        gravity_ok = (
            gravity.shape == (3,)
            and bool(np.all(np.isfinite(gravity)))
            and abs(float(np.linalg.norm(gravity)) - 1.0) <= self.max_projected_gravity_norm_error
        )
        if self.require_pose_gate and (
            not np.isfinite(max_leg_position_error_rad)
            or max_leg_position_error_rad > self.max_leg_position_error_rad
            or not gravity_ok
        ):
            return PolicyGateResult(False, "blocked:pose_gate")
        if self.require_motion_gate and (
            not np.isfinite(base_angular_velocity_norm)
            or base_angular_velocity_norm > self.max_base_angular_velocity_rad_s
        ):
            return PolicyGateResult(False, "blocked:motion_gate")
        return PolicyGateResult(True, "ready:policy_dryrun")
