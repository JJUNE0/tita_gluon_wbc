"""Go/No-Go coordination contract for sequential mobile inspection.

This module intentionally contains no Isaac Sim imports.  It locks the
high-level action, persistent arm-option state machine, action masks, target
layout, and classical scheduling baselines before those interfaces are wired
to a simulator-specific graph/local-servo executor.

Execution domain: DESKTOP_DRY_RUN (logic) or VALIDATION_SIM (when integrated).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
import math
import random

import torch
import torch.nn.functional as torch_functional


class ArmOption(IntEnum):
    """Policy-visible categorical arm requests."""

    HOLD = 0
    STOW = 1
    PREPARE_NEXT = 2
    EXECUTE_CURRENT = 3


class TriggerAction(IntEnum):
    """Phase-conditioned policy request; the executor still owns ArmOption."""

    WAIT = 0
    TRIGGER = 1


class ExecutorState(IntEnum):
    """Executor-owned persistent states; these are observations, not actions."""

    IDLE = 0
    GRAPH_EXECUTION = 1
    LOCAL_TARGET_SERVO = 2
    DWELL = 3
    EMERGENCY_HOLD = 4
    RECOVERY = 5


class ExecutorEvent(IntEnum):
    NONE = 0
    OPTION_ACCEPTED = 1
    OPTION_REJECTED = 2
    TARGET_COMPLETED = 3
    TASK_COMPLETED = 4
    SAFETY_ABORT = 5
    LOCAL_REGION_EXIT = 6
    RECOVERY_STARTED = 7
    RECOVERY_COMPLETED = 8


@dataclass(frozen=True)
class InspectionTargetSpec:
    """Oracle inspection pose metadata relative to route coordinates."""

    label: str
    route_s_m: float
    lateral_m: float
    height_m: float
    facing_yaw_rad: float


@dataclass(frozen=True)
class TargetRandomization:
    longitudinal_m: float = 0.10
    lateral_m: float = 0.02
    height_m: float = 0.02


DEFAULT_TARGETS = (
    InspectionTargetSpec("LEFT_HIGH", 0.9, 0.42, 0.74, -math.pi / 2.0),
    InspectionTargetSpec("RIGHT_LOW", 2.1, -0.42, 0.48, math.pi / 2.0),
    InspectionTargetSpec("LEFT_LOW", 3.3, 0.42, 0.48, -math.pi / 2.0),
    InspectionTargetSpec("RIGHT_HIGH", 4.5, -0.42, 0.74, math.pi / 2.0),
)


def sample_target_layout(
    seed: int,
    targets: tuple[InspectionTargetSpec, ...] = DEFAULT_TARGETS,
    randomization: TargetRandomization = TargetRandomization(),
) -> tuple[InspectionTargetSpec, ...]:
    """Sample small deterministic offsets while preserving target order."""
    rng = random.Random(seed)
    sampled = []
    for target in targets:
        sampled.append(
            InspectionTargetSpec(
                label=target.label,
                route_s_m=target.route_s_m
                + rng.uniform(-randomization.longitudinal_m, randomization.longitudinal_m),
                lateral_m=target.lateral_m
                + rng.uniform(-randomization.lateral_m, randomization.lateral_m),
                height_m=target.height_m
                + rng.uniform(-randomization.height_m, randomization.height_m),
                facing_yaw_rad=target.facing_yaw_rad,
            )
        )
    return tuple(sampled)


def local_region_contains(
    target_position_b: torch.Tensor,
    hub_position_b: torch.Tensor,
    half_extent_m: torch.Tensor | tuple[float, float, float],
) -> torch.Tensor:
    """Return an AABB candidate-region gate around a hub EE position.

    The region is only a runtime representation.  Its bounds must be produced
    by an offline IK/collision validation job before it may be described as
    validated in an experiment report.
    """
    half_extent = torch.as_tensor(
        half_extent_m, dtype=target_position_b.dtype, device=target_position_b.device
    )
    if half_extent.shape != (3,) or bool(torch.any(half_extent <= 0.0)):
        raise ValueError("half_extent_m must contain three positive values")
    if target_position_b.shape != hub_position_b.shape or target_position_b.shape[-1] != 3:
        raise ValueError("target and hub positions must have matching (..., 3) shapes")
    return torch.all(torch.abs(target_position_b - hub_position_b) <= half_extent, dim=-1)


def build_option_mask(
    executor_state: torch.Tensor,
    current_target_index: torch.Tensor,
    prepared_target_index: torch.Tensor,
    target_count: int,
    local_region_valid: torch.Tensor,
    validated_stow_path: torch.Tensor,
) -> torch.Tensor:
    """Build the four-column policy option mask for a vectorized executor."""
    tensors = (
        executor_state,
        current_target_index,
        prepared_target_index,
        local_region_valid,
        validated_stow_path,
    )
    if any(tensor.ndim != 1 for tensor in tensors):
        raise ValueError("option-mask inputs must be one-dimensional tensors")
    if any(tensor.shape != executor_state.shape for tensor in tensors[1:]):
        raise ValueError("option-mask inputs must have matching batch shapes")
    if target_count <= 0:
        raise ValueError("target_count must be positive")

    mask = torch.zeros(
        (executor_state.shape[0], len(ArmOption)),
        dtype=torch.bool,
        device=executor_state.device,
    )
    # HOLD is the sole policy-visible no-op while an option persists.  It does
    # not interrupt graph execution, local servo, dwell, or recovery.
    mask[:, ArmOption.HOLD] = True
    idle = executor_state == int(ExecutorState.IDLE)
    task_active = current_target_index < target_count
    mask[:, ArmOption.STOW] = idle & validated_stow_path
    mask[:, ArmOption.PREPARE_NEXT] = (
        idle & task_active & (prepared_target_index != current_target_index)
    )
    mask[:, ArmOption.EXECUTE_CURRENT] = (
        idle
        & task_active
        & (prepared_target_index == current_target_index)
        & local_region_valid
    )
    return mask


@dataclass(frozen=True)
class ExecutorStepInput:
    graph_finished: bool = False
    local_region_valid: bool = True
    pose_within_tolerance: bool = False
    cbf_infeasible: bool = False
    recovery_finished: bool = False


class SequentialInspectionExecutor:
    """Scalar reference FSM used to test the environment-side option contract."""

    def __init__(self, target_count: int = 4, dwell_time_s: float = 0.3):
        if target_count <= 0:
            raise ValueError("target_count must be positive")
        if dwell_time_s <= 0.0:
            raise ValueError("dwell_time_s must be positive")
        self.target_count = target_count
        self.dwell_time_s = dwell_time_s
        self.reset()

    def reset(self) -> None:
        self.state = ExecutorState.IDLE
        self.active_option = ArmOption.HOLD
        self.current_target_index = 0
        self.prepared_target_index = -1
        self.progress = 0.0
        self.dwell_elapsed_s = 0.0
        self.at_stow = True
        self.last_event = ExecutorEvent.NONE
        self.last_abort_reason = ""

    @property
    def task_complete(self) -> bool:
        return self.current_target_index >= self.target_count

    def option_mask(self, *, local_region_valid: bool, validated_stow_path: bool) -> tuple[bool, ...]:
        state = torch.tensor([int(self.state)])
        current = torch.tensor([self.current_target_index])
        prepared = torch.tensor([self.prepared_target_index])
        mask = build_option_mask(
            state,
            current,
            prepared,
            self.target_count,
            torch.tensor([local_region_valid]),
            torch.tensor([validated_stow_path]),
        )
        return tuple(bool(value) for value in mask[0].tolist())

    def begin_bootstrap(self) -> ExecutorEvent:
        """Start the pre-episode graph transition to target zero's hub."""
        if self.state != ExecutorState.IDLE or self.current_target_index != 0:
            return self._reject()
        self.active_option = ArmOption.PREPARE_NEXT
        self.state = ExecutorState.GRAPH_EXECUTION
        self.progress = 0.0
        self.last_event = ExecutorEvent.OPTION_ACCEPTED
        return self.last_event

    def request(
        self,
        option: ArmOption | int,
        *,
        local_region_valid: bool,
        validated_stow_path: bool,
    ) -> ExecutorEvent:
        option = ArmOption(int(option))
        mask = self.option_mask(
            local_region_valid=local_region_valid,
            validated_stow_path=validated_stow_path,
        )
        if not mask[int(option)]:
            return self._reject()
        self.last_event = ExecutorEvent.OPTION_ACCEPTED
        if option == ArmOption.HOLD:
            return self.last_event
        self.active_option = option
        self.progress = 0.0
        if option in (ArmOption.STOW, ArmOption.PREPARE_NEXT):
            self.state = ExecutorState.GRAPH_EXECUTION
        elif option == ArmOption.EXECUTE_CURRENT:
            self.state = ExecutorState.LOCAL_TARGET_SERVO
        return self.last_event

    def step(self, dt_s: float, step_input: ExecutorStepInput) -> ExecutorEvent:
        if dt_s <= 0.0 or not math.isfinite(dt_s):
            raise ValueError("dt_s must be finite and positive")
        self.last_event = ExecutorEvent.NONE
        if step_input.cbf_infeasible:
            self.state = ExecutorState.EMERGENCY_HOLD
            self.active_option = ArmOption.HOLD
            self.progress = 0.0
            self.last_abort_reason = "cbf_infeasible"
            self.last_event = ExecutorEvent.SAFETY_ABORT
            return self.last_event

        if self.state == ExecutorState.GRAPH_EXECUTION and step_input.graph_finished:
            if self.active_option == ArmOption.STOW:
                self.prepared_target_index = -1
                self.at_stow = True
            elif self.active_option == ArmOption.PREPARE_NEXT:
                self.prepared_target_index = self.current_target_index
                self.at_stow = False
            self.state = ExecutorState.IDLE
            self.active_option = ArmOption.HOLD
            self.progress = 1.0
            return self.last_event

        if self.state == ExecutorState.LOCAL_TARGET_SERVO:
            if not step_input.local_region_valid:
                self.state = ExecutorState.EMERGENCY_HOLD
                self.active_option = ArmOption.HOLD
                self.last_abort_reason = "local_region_exit"
                self.last_event = ExecutorEvent.LOCAL_REGION_EXIT
                return self.last_event
            if step_input.pose_within_tolerance:
                self.state = ExecutorState.DWELL
                self.dwell_elapsed_s = 0.0
            return self.last_event

        if self.state == ExecutorState.DWELL:
            if not step_input.local_region_valid:
                self.state = ExecutorState.EMERGENCY_HOLD
                self.active_option = ArmOption.HOLD
                self.last_abort_reason = "local_region_exit_during_dwell"
                self.last_event = ExecutorEvent.LOCAL_REGION_EXIT
                return self.last_event
            if not step_input.pose_within_tolerance:
                self.state = ExecutorState.LOCAL_TARGET_SERVO
                self.dwell_elapsed_s = 0.0
                return self.last_event
            self.dwell_elapsed_s += dt_s
            self.progress = min(self.dwell_elapsed_s / self.dwell_time_s, 1.0)
            if self.dwell_elapsed_s >= self.dwell_time_s:
                self.current_target_index += 1
                self.state = ExecutorState.IDLE
                self.active_option = ArmOption.HOLD
                self.progress = 1.0
                self.last_event = (
                    ExecutorEvent.TASK_COMPLETED
                    if self.task_complete
                    else ExecutorEvent.TARGET_COMPLETED
                )
            return self.last_event

        if self.state == ExecutorState.RECOVERY and step_input.recovery_finished:
            self.state = ExecutorState.IDLE
            self.active_option = ArmOption.HOLD
            self.at_stow = True
            self.prepared_target_index = -1
            self.progress = 1.0
            self.last_event = ExecutorEvent.RECOVERY_COMPLETED
        return self.last_event

    def begin_validated_recovery(self, validated_stow_path: bool) -> ExecutorEvent:
        if self.state != ExecutorState.EMERGENCY_HOLD or not validated_stow_path:
            return self._reject()
        self.state = ExecutorState.RECOVERY
        self.active_option = ArmOption.STOW
        self.progress = 0.0
        self.last_event = ExecutorEvent.RECOVERY_STARTED
        return self.last_event

    def _reject(self) -> ExecutorEvent:
        self.last_event = ExecutorEvent.OPTION_REJECTED
        return self.last_event


@dataclass(frozen=True)
class CoordinatorObservation:
    target_index: int
    target_count: int
    # Signed route-coordinate error: target_s - base_s.
    longitudinal_distance_m: float
    yaw_error_rad: float
    local_region_valid: bool
    prepared_for_current: bool
    at_stow: bool
    executor_state: ExecutorState
    task_complete: bool = False
    base_speed_m_s: float = 0.0
    base_yaw_rate_rad_s: float = 0.0
    target_minus_hub_x_m: float = 0.0
    target_minus_hub_y_m: float = 0.0


@dataclass(frozen=True)
class HighLevelCommand:
    vx_cmd_m_s: float
    yaw_rate_cmd_rad_s: float
    arm_option: ArmOption


HIGH_LEVEL_OBSERVATION_DIM = 45
HIGH_LEVEL_ACTION_MASK_START = HIGH_LEVEL_OBSERVATION_DIM - 4


def build_phase_conditioned_trigger_contract(
    option_mask: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Convert the executor's four-way mask into a binary action mask and phase bits.

    The returned tail contract is deliberately split into two tensors:

    - ``binary_mask``: WAIT/TRIGGER validity consumed by HybridActorCritic.
    - ``phase``: PREPARE/EXECUTE meaning of TRIGGER consumed as policy context.

    STOW remains an executor recovery primitive and is not exposed in Gate-0.
    """
    if option_mask.ndim != 2 or option_mask.shape[1] != len(ArmOption):
        raise ValueError(
            f"option_mask must have shape (num_envs, {len(ArmOption)})"
        )
    option_mask = option_mask.bool()
    if bool(torch.any(~option_mask[:, int(ArmOption.HOLD)])):
        raise ValueError("WAIT requires the executor HOLD option to be valid")
    prepare = option_mask[:, int(ArmOption.PREPARE_NEXT)]
    execute = option_mask[:, int(ArmOption.EXECUTE_CURRENT)]
    if bool(torch.any(prepare & execute)):
        raise ValueError("PREPARE and EXECUTE phases must be mutually exclusive")
    trigger_valid = prepare | execute
    binary_mask = torch.stack(
        (option_mask[:, int(ArmOption.HOLD)], trigger_valid), dim=-1
    )
    phase = torch.stack((prepare, execute), dim=-1)
    return binary_mask, phase


def build_high_level_policy_observation(
    *,
    current_target_pos_b: torch.Tensor,
    current_target_facing_b: torch.Tensor,
    next_target_pos_b: torch.Tensor,
    next_target_facing_b: torch.Tensor,
    base_lin_vel_b: torch.Tensor,
    base_yaw_rate: torch.Tensor,
    arm_joint_pos: torch.Tensor,
    arm_joint_vel: torch.Tensor,
    executor_state: torch.Tensor,
    active_option: torch.Tensor,
    option_progress: torch.Tensor,
    current_target_index: torch.Tensor,
    target_count: int,
    previous_base_command: torch.Tensor,
    option_mask: torch.Tensor,
) -> torch.Tensor:
    """Build the locked actor observation with binary mask and phase at the tail."""
    batch_size = current_target_pos_b.shape[0]
    expected = {
        "current_target_pos_b": (batch_size, 3),
        "current_target_facing_b": (batch_size, 3),
        "next_target_pos_b": (batch_size, 3),
        "next_target_facing_b": (batch_size, 3),
        "base_lin_vel_b": (batch_size, 2),
        "base_yaw_rate": (batch_size,),
        "arm_joint_pos": (batch_size, 6),
        "arm_joint_vel": (batch_size, 6),
        "executor_state": (batch_size,),
        "active_option": (batch_size,),
        "option_progress": (batch_size,),
        "current_target_index": (batch_size,),
        "previous_base_command": (batch_size, 2),
        "option_mask": (batch_size, len(ArmOption)),
    }
    values = locals()
    for name, shape in expected.items():
        if values[name].shape != shape:
            raise ValueError(f"{name} must have shape {shape}, got {values[name].shape}")
    if target_count <= 0:
        raise ValueError("target_count must be positive")
    if bool(torch.any((executor_state < 0) | (executor_state >= len(ExecutorState)))):
        raise ValueError("executor_state contains an invalid index")
    if bool(torch.any((active_option < 0) | (active_option >= len(ArmOption)))):
        raise ValueError("active_option contains an invalid index")
    if bool(torch.any(~torch.any(option_mask.bool(), dim=-1))):
        raise ValueError("every environment must expose at least one valid option")
    trigger_mask, trigger_phase = build_phase_conditioned_trigger_contract(option_mask)

    state_one_hot = torch_functional.one_hot(
        executor_state.long(), num_classes=len(ExecutorState)
    ).to(current_target_pos_b.dtype)
    option_one_hot = torch_functional.one_hot(
        active_option.long(), num_classes=len(ArmOption)
    ).to(current_target_pos_b.dtype)
    target_denominator = max(target_count - 1, 1)
    target_progress = (
        current_target_index.to(current_target_pos_b.dtype) / target_denominator
    ).unsqueeze(-1)
    observation = torch.cat(
        (
            current_target_pos_b,
            current_target_facing_b,
            next_target_pos_b,
            next_target_facing_b,
            base_lin_vel_b,
            base_yaw_rate.unsqueeze(-1),
            arm_joint_pos,
            arm_joint_vel,
            state_one_hot,
            option_one_hot,
            option_progress.unsqueeze(-1),
            target_progress,
            previous_base_command,
            trigger_mask.to(current_target_pos_b.dtype),
            trigger_phase.to(current_target_pos_b.dtype),
        ),
        dim=-1,
    )
    if observation.shape != (batch_size, HIGH_LEVEL_OBSERVATION_DIM):
        raise RuntimeError(f"unexpected high-level observation shape {observation.shape}")
    if not bool(torch.isfinite(observation).all()):
        raise ValueError("high-level observation contains NaN or Inf")
    return observation


@dataclass(frozen=True)
class GoNoGoRewardWeights:
    target_distance_progress: float = 2.0
    route_progress: float = 0.5
    target_completed: float = 5.0
    task_completed: float = 20.0
    elapsed_time: float = 0.02
    base_command_delta: float = 0.05
    option_rejected: float = 0.2
    local_abort: float = 5.0
    fall: float = 20.0


def compute_go_no_go_reward(
    *,
    previous_target_distance_m: torch.Tensor,
    target_distance_m: torch.Tensor,
    route_progress_delta_m: torch.Tensor,
    target_completed: torch.Tensor,
    task_completed: torch.Tensor,
    base_command_delta_norm: torch.Tensor,
    option_rejected: torch.Tensor,
    local_abort: torch.Tensor,
    fall: torch.Tensor,
    high_level_dt_s: float,
    weights: GoNoGoRewardWeights = GoNoGoRewardWeights(),
) -> torch.Tensor:
    """Task reward used by all high-level timing-policy experiments."""
    tensors = (
        previous_target_distance_m,
        target_distance_m,
        route_progress_delta_m,
        target_completed,
        task_completed,
        base_command_delta_norm,
        option_rejected,
        local_abort,
        fall,
    )
    if any(tensor.ndim != 1 for tensor in tensors):
        raise ValueError("reward inputs must be one-dimensional batched tensors")
    if any(tensor.shape != previous_target_distance_m.shape for tensor in tensors[1:]):
        raise ValueError("reward inputs must have matching batch shapes")
    if high_level_dt_s <= 0.0 or not math.isfinite(high_level_dt_s):
        raise ValueError("high_level_dt_s must be finite and positive")
    dtype = previous_target_distance_m.dtype
    reward = weights.target_distance_progress * (
        previous_target_distance_m - target_distance_m
    )
    reward += weights.route_progress * route_progress_delta_m
    reward += weights.target_completed * target_completed.to(dtype)
    reward += weights.task_completed * task_completed.to(dtype)
    reward -= weights.elapsed_time * high_level_dt_s
    reward -= weights.base_command_delta * base_command_delta_norm.square()
    reward -= weights.option_rejected * option_rejected.to(dtype)
    reward -= weights.local_abort * local_abort.to(dtype)
    reward -= weights.fall * fall.to(dtype)
    return reward


def _bounded_yaw_rate(yaw_error_rad: float, gain: float, maximum: float) -> float:
    return max(-maximum, min(maximum, gain * yaw_error_rad))


def _bounded_route_speed(
    signed_distance_m: float, maximum_m_s: float, stopping_gain_s_inv: float = 1.5
) -> float:
    """Use signed proportional braking without exceeding the speed limit."""
    return max(
        -maximum_m_s,
        min(maximum_m_s, stopping_gain_s_inv * signed_distance_m),
    )


class StopAndGoController:
    """Conservative baseline: stow, travel, stop, prepare, inspect."""

    def __init__(
        self,
        max_vx_m_s: float = 0.5,
        stop_distance_m: float = 0.10,
        stopped_speed_m_s: float = 0.03,
        stopped_yaw_rate_rad_s: float = 0.05,
        yaw_gain: float = 1.5,
        max_yaw_rate_rad_s: float = 0.6,
    ):
        self.max_vx_m_s = max_vx_m_s
        self.stop_distance_m = stop_distance_m
        self.stopped_speed_m_s = stopped_speed_m_s
        self.stopped_yaw_rate_rad_s = stopped_yaw_rate_rad_s
        self.yaw_gain = yaw_gain
        self.max_yaw_rate_rad_s = max_yaw_rate_rad_s

    def command(self, obs: CoordinatorObservation) -> HighLevelCommand:
        yaw = _bounded_yaw_rate(obs.yaw_error_rad, self.yaw_gain, self.max_yaw_rate_rad_s)
        distance = abs(obs.longitudinal_distance_m)
        if obs.task_complete:
            return HighLevelCommand(0.0, 0.0, ArmOption.HOLD)
        if obs.executor_state != ExecutorState.IDLE:
            # Stop-and-go is the conservative timing baseline. Graph motion,
            # local servo, and dwell all run with a zero base command; a
            # nonzero station-keeping command would create base/arm overlap
            # and move a world-fixed target through the hub-local region.
            return HighLevelCommand(0.0, 0.0, ArmOption.HOLD)
        if obs.prepared_for_current:
            if (
                obs.local_region_valid
                and obs.base_speed_m_s <= self.stopped_speed_m_s
                and abs(obs.base_yaw_rate_rad_s) <= self.stopped_yaw_rate_rad_s
            ):
                return HighLevelCommand(0.0, 0.0, ArmOption.EXECUTE_CURRENT)
            hub_distance = math.hypot(
                obs.target_minus_hub_x_m, obs.target_minus_hub_y_m
            )
            if not obs.local_region_valid and hub_distance > self.stop_distance_m:
                # Once a graph hub is prepared, align the mobile base to the
                # measured world target. TITA is nonholonomic, so turn toward
                # the hub displacement and reverse when that gives the shorter
                # steering angle.
                steering = math.atan2(
                    obs.target_minus_hub_y_m, obs.target_minus_hub_x_m
                )
                direction = 1.0
                if abs(steering) > math.pi / 2.0:
                    direction = -1.0
                    steering = math.atan2(-math.sin(steering), -math.cos(steering))
                return HighLevelCommand(
                    direction * min(self.max_vx_m_s, 1.5 * hub_distance),
                    _bounded_yaw_rate(
                        steering, self.yaw_gain, self.max_yaw_rate_rad_s
                    ),
                    ArmOption.HOLD,
                )
            # Inside the hub-alignment window, brake until the measured base
            # twist is low enough to begin the arm-only phase. If y/z remain
            # invalid, HOLD exposes the need for hub reselection instead of
            # forcing a large unvalidated Cartesian reach.
            return HighLevelCommand(0.0, 0.0, ArmOption.HOLD)
        if not obs.at_stow:
            return HighLevelCommand(0.0, 0.0, ArmOption.STOW)
        if distance > self.stop_distance_m:
            return HighLevelCommand(
                _bounded_route_speed(obs.longitudinal_distance_m, self.max_vx_m_s),
                yaw,
                ArmOption.HOLD,
            )
        return HighLevelCommand(0.0, 0.0, ArmOption.PREPARE_NEXT)


class TunedConcurrentScheduler:
    """Two-parameter classical baseline for base/arm overlap timing."""

    def __init__(
        self,
        start_distance_m: float,
        arm_motion_speed_scale: float,
        max_vx_m_s: float = 0.5,
        execute_distance_m: float = 0.10,
        yaw_gain: float = 1.5,
        max_yaw_rate_rad_s: float = 0.6,
    ):
        if start_distance_m <= execute_distance_m:
            raise ValueError("start_distance_m must exceed execute_distance_m")
        if not 0.0 <= arm_motion_speed_scale <= 1.0:
            raise ValueError("arm_motion_speed_scale must be in [0, 1]")
        self.start_distance_m = start_distance_m
        self.arm_motion_speed_scale = arm_motion_speed_scale
        self.max_vx_m_s = max_vx_m_s
        self.execute_distance_m = execute_distance_m
        self.yaw_gain = yaw_gain
        self.max_yaw_rate_rad_s = max_yaw_rate_rad_s

    def command(self, obs: CoordinatorObservation) -> HighLevelCommand:
        yaw = _bounded_yaw_rate(obs.yaw_error_rad, self.yaw_gain, self.max_yaw_rate_rad_s)
        distance = abs(obs.longitudinal_distance_m)
        direction = 1.0 if obs.longitudinal_distance_m >= 0.0 else -1.0
        if obs.task_complete:
            return HighLevelCommand(0.0, 0.0, ArmOption.HOLD)
        if obs.executor_state in (ExecutorState.LOCAL_TARGET_SERVO, ExecutorState.DWELL):
            # Preserve concurrency without a bang-bang station crossing.  A
            # constant signed speed flips at the target and repeatedly knocks
            # the EE out of its pose/dwell tolerance.  Scale the same bounded
            # proportional route controller used during ordinary travel so
            # the base command converges continuously to zero at the station.
            return HighLevelCommand(
                _bounded_route_speed(
                    obs.longitudinal_distance_m, self.max_vx_m_s
                )
                * self.arm_motion_speed_scale,
                yaw * self.arm_motion_speed_scale,
                ArmOption.HOLD,
            )
        if obs.executor_state in (ExecutorState.GRAPH_EXECUTION, ExecutorState.RECOVERY):
            return HighLevelCommand(
                _bounded_route_speed(
                    obs.longitudinal_distance_m, self.max_vx_m_s
                )
                * self.arm_motion_speed_scale,
                yaw * self.arm_motion_speed_scale,
                ArmOption.HOLD,
            )
        if obs.executor_state == ExecutorState.EMERGENCY_HOLD:
            return HighLevelCommand(0.0, 0.0, ArmOption.HOLD)
        if obs.prepared_for_current:
            if obs.local_region_valid and distance <= self.execute_distance_m:
                return HighLevelCommand(0.0, 0.0, ArmOption.EXECUTE_CURRENT)
            return HighLevelCommand(
                _bounded_route_speed(obs.longitudinal_distance_m, self.max_vx_m_s),
                yaw,
                ArmOption.HOLD,
            )
        if distance <= self.start_distance_m:
            return HighLevelCommand(
                direction * self.max_vx_m_s * self.arm_motion_speed_scale,
                yaw * self.arm_motion_speed_scale,
                ArmOption.PREPARE_NEXT,
            )
        return HighLevelCommand(
            _bounded_route_speed(obs.longitudinal_distance_m, self.max_vx_m_s),
            yaw,
            ArmOption.HOLD,
        )


def decode_phase_conditioned_action(
    action: torch.Tensor,
    option_mask: torch.Tensor,
    vx_limit_m_s: float = 0.75,
    yaw_rate_limit_rad_s: float = 1.0,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """Map WAIT/TRIGGER PPO output to bounded commands and executor options.

    TRIGGER resolves to the sole valid progress transition for the current
    phase. Invalid external TRIGGER requests degrade to HOLD and are reported
    through ``request_valid``; the masked policy itself cannot sample them.
    """
    if action.ndim != 2 or action.shape[1] != 3:
        raise ValueError("hybrid action must have shape (num_envs, 3)")
    if option_mask.shape != (action.shape[0], len(ArmOption)):
        raise ValueError(
            f"option_mask must have shape {(action.shape[0], len(ArmOption))}"
        )
    vx = torch.clamp(action[:, 0], -1.0, 1.0) * vx_limit_m_s
    yaw_rate = torch.clamp(action[:, 1], -1.0, 1.0) * yaw_rate_limit_rad_s
    trigger_action = action[:, 2].round().long()
    if bool(torch.any((trigger_action < 0) | (trigger_action >= len(TriggerAction)))):
        raise ValueError("phase-conditioned action index is outside [0, 1]")

    trigger_mask, trigger_phase = build_phase_conditioned_trigger_contract(option_mask)
    trigger_requested = trigger_action == int(TriggerAction.TRIGGER)
    request_valid = trigger_mask[
        torch.arange(action.shape[0], device=action.device), trigger_action
    ]
    option = torch.full_like(trigger_action, int(ArmOption.HOLD))
    option[trigger_requested & trigger_phase[:, 0]] = int(ArmOption.PREPARE_NEXT)
    option[trigger_requested & trigger_phase[:, 1]] = int(ArmOption.EXECUTE_CURRENT)
    return vx, yaw_rate, option, request_valid


__all__ = [
    "ArmOption",
    "TriggerAction",
    "CoordinatorObservation",
    "DEFAULT_TARGETS",
    "ExecutorEvent",
    "ExecutorState",
    "ExecutorStepInput",
    "HighLevelCommand",
    "InspectionTargetSpec",
    "SequentialInspectionExecutor",
    "StopAndGoController",
    "TargetRandomization",
    "TunedConcurrentScheduler",
    "build_option_mask",
    "build_phase_conditioned_trigger_contract",
    "decode_phase_conditioned_action",
    "local_region_contains",
    "sample_target_layout",
]
