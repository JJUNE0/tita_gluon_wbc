"""High-level VecEnv over a frozen TITA locomotion policy.

Execution domain: TRAINING_SIM or VALIDATION_SIM.

This wrapper owns only task coordination.  Every high-level action contains
two base commands and one persistent arm option.  The wrapped IsaacLab
environment continues to execute the frozen eight-action TITA policy and the
GLUON graph/local-servo action term.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable

import torch

from isaaclab.utils.math import (
    quat_apply,
    quat_apply_inverse,
    quat_mul,
    yaw_quat,
)

from scripts.co_rl.core.env import VecEnv

from .mdp.actions import SequentialInspectionJointPositionAction
from .sequential_inspection import (
    ArmOption,
    CoordinatorObservation,
    ExecutorEvent,
    ExecutorState,
    GoNoGoRewardWeights,
    HIGH_LEVEL_OBSERVATION_DIM,
    TriggerAction,
    TunedConcurrentScheduler,
    build_high_level_policy_observation,
    compute_go_no_go_reward,
    decode_phase_conditioned_action,
)


@dataclass(frozen=True)
class HighLevelInspectionEnvCfg:
    """Runtime contract for the position-only Gate-0 task."""

    target_count: int = 4
    route_s_m: tuple[float, ...] = (0.9, 2.1, 3.3, 4.5)
    route_randomization_m: float = 0.10
    local_randomization_m: tuple[float, float, float] = (0.03, 0.02, 0.02)
    fixed_height_m: float = 0.39
    vx_limit_m_s: float = 0.5
    yaw_rate_limit_rad_s: float = 0.6
    # The frozen locomotion controller runs at 50 Hz; option/base timing is a
    # 10 Hz decision problem.  Holding each high-level command for five low
    # steps also gives PPO a physically meaningful discount horizon.
    high_level_decimation: int = 5
    episode_length_s: float = 70.0
    bootstrap_max_low_steps: int = 800
    route_cross_track_gain: float = 3.0
    scheduler_start_distance_m: float = 1.4
    scheduler_arm_speed_scale: float = 0.6
    reward: GoNoGoRewardWeights = GoNoGoRewardWeights()


@dataclass(frozen=True)
class HighLevelRunnerEnvView:
    """Serializable subset consumed by the CO-RL runner/logger."""

    rewards: GoNoGoRewardWeights
    runtime: HighLevelInspectionEnvCfg


class FrozenLowLevelSequentialInspectionEnv(VecEnv):
    """CO-RL VecEnv that advances a frozen low-level policy internally.

    Resets are synchronized across the vector batch.  This deliberately keeps
    the low-policy history wrapper and task bootstrap coherent without hidden
    per-environment history leakage.  Arm-local emergency holds are isolated
    until every robot has either completed or failed; a true low-level reset
    still ends the whole batch, as does the high-level horizon.
    """

    def __init__(
        self,
        low_env,
        low_policy: Callable,
        target_hub_indices: tuple[int, ...],
        cfg: HighLevelInspectionEnvCfg = HighLevelInspectionEnvCfg(),
        seed: int = 20260813,
    ):
        if cfg.target_count != len(cfg.route_s_m):
            raise ValueError("target_count must match route_s_m")
        if cfg.target_count != len(target_hub_indices):
            raise ValueError("target hub count must match target_count")
        if cfg.high_level_decimation <= 0:
            raise ValueError("high_level_decimation must be positive")
        self.low_env = low_env
        self.low_policy = low_policy
        self.runtime_cfg = cfg
        self.num_envs = low_env.num_envs
        self.device = low_env.device
        self.num_actions = 3
        self.num_obs = HIGH_LEVEL_OBSERVATION_DIM
        self.num_privileged_obs = HIGH_LEVEL_OBSERVATION_DIM
        self._raw_env = low_env.unwrapped
        self._executor = self._raw_env.action_manager.get_term("gluon_joint_reference")
        if not isinstance(self._executor, SequentialInspectionJointPositionAction):
            raise TypeError(f"unexpected GLUON executor {type(self._executor).__name__}")
        if self._raw_env.action_manager.total_action_dim != 8:
            raise ValueError("frozen low-level action contract must have dimension eight")
        self._command_term = self._raw_env.command_manager.get_term("base_velocity")
        self._command = self._command_term.vel_command_b
        self._target_hub_indices = torch.tensor(
            target_hub_indices, dtype=torch.long, device=self.device
        ).repeat(self.num_envs, 1)
        self._target_count = cfg.target_count
        self._scripted_scheduler = TunedConcurrentScheduler(
            start_distance_m=cfg.scheduler_start_distance_m,
            arm_motion_speed_scale=cfg.scheduler_arm_speed_scale,
            max_vx_m_s=cfg.vx_limit_m_s,
            max_yaw_rate_rad_s=cfg.yaw_rate_limit_rad_s,
        )
        self._low_step_dt_s = float(self._raw_env.step_dt)
        self.high_level_dt_s = self._low_step_dt_s * cfg.high_level_decimation
        self.max_episode_length = int(math.ceil(cfg.episode_length_s / self.high_level_dt_s))
        self.episode_length_buf = torch.zeros(
            self.num_envs, dtype=torch.long, device=self.device
        )
        self._previous_base_command = torch.zeros((self.num_envs, 2), device=self.device)
        self._route_start_w = torch.zeros((self.num_envs, 3), device=self.device)
        self._route_quat_w = torch.zeros((self.num_envs, 4), device=self.device)
        self._route_quat_w[:, 0] = 1.0
        self._route_x_w = torch.zeros((self.num_envs, 3), device=self.device)
        self._route_y_w = torch.zeros((self.num_envs, 3), device=self.device)
        self._route_s = torch.zeros((self.num_envs, self._target_count), device=self.device)
        self._last_progress_s = torch.zeros(self.num_envs, device=self.device)
        self._episode_reward = torch.zeros(self.num_envs, device=self.device)
        self._episode_overlap_steps = torch.zeros(self.num_envs, device=self.device)
        self._episode_motion_steps = torch.zeros(self.num_envs, device=self.device)
        self._episode_option_rejections = torch.zeros(self.num_envs, device=self.device)
        self._episode_local_aborts = torch.zeros(self.num_envs, device=self.device)
        self._episode_completion_step = torch.full(
            (self.num_envs,), -1, dtype=torch.long, device=self.device
        )
        self._episode_emergency_failed = torch.zeros(
            self.num_envs, dtype=torch.bool, device=self.device
        )
        # Runner-consumed diagnostics are iteration-scoped, not episode-scoped.
        # Index 0 is PREPARE and index 1 is EXECUTE.
        self._trigger_probability_sum = torch.zeros(2, device=self.device)
        self._trigger_phase_count = torch.zeros(2, device=self.device)
        self._trigger_greedy_count = torch.zeros(2, device=self.device)
        self._trigger_sampled_count = torch.zeros(2, device=self.device)
        self._episode_counter = 0
        self._seed = seed
        self._cfg_view = HighLevelRunnerEnvView(rewards=cfg.reward, runtime=cfg)
        torch.manual_seed(seed)
        self._low_obs: torch.Tensor
        self._low_extras: dict
        self._obs = torch.zeros((self.num_envs, self.num_obs), device=self.device)
        self._reset_synchronized()

    @property
    def cfg(self):
        return self._cfg_view

    @property
    def unwrapped(self):
        return self._raw_env

    def seed(self, seed: int = -1) -> int:
        self._seed = int(seed)
        torch.manual_seed(self._seed)
        return self.low_env.seed(seed)

    def _privileged_obs(self) -> torch.Tensor | None:
        observations = self._low_extras.get("observations") if self._low_extras else None
        if not observations:
            return None
        keys = sorted(key for key in observations if key.startswith("priv_"))
        if keys:
            return torch.cat([observations[key] for key in keys], dim=-1).to(self.device)
        return observations.get("privileged")

    def _low_action(self) -> torch.Tensor:
        privileged = self._privileged_obs()
        try:
            if privileged is not None:
                return self.low_policy(self._low_obs, privileged_info=privileged)
        except TypeError:
            pass
        return self.low_policy(self._low_obs)

    def _force_commands(self, vx: torch.Tensor, yaw: torch.Tensor) -> None:
        self._command[:, 0] = vx
        self._command[:, 1] = 0.0
        self._command[:, 2] = yaw
        self._command[:, 3] = self.runtime_cfg.fixed_height_m
        self._command_term.time_left[:] = 1.0e6
        self._command_term.time_elapsed[:] = self._command_term.cfg.initial_phase_time + 1.0
        self._command_term.is_heading_env[:] = False
        self._command_term.is_standing_env[:] = False

    def _advance_low(self, vx: torch.Tensor, yaw: torch.Tensor) -> torch.Tensor:
        low_done = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)
        for _ in range(self.runtime_cfg.high_level_decimation):
            self._force_commands(vx, yaw)
            action = self._low_action()
            self._low_obs, _, dones, self._low_extras = self.low_env.step(action)
            low_done |= dones.bool()
        return low_done

    def _setup_bootstrap_targets(self) -> None:
        hub_pos_b = self._executor.hub_ee_pos_b[self._target_hub_indices]
        hub_quat_b = self._executor.hub_ee_quat_b[self._target_hub_indices]
        root_pos_w = self._raw_env.scene["robot"].data.root_link_pos_w.clone()
        root_quat_w = self._raw_env.scene["robot"].data.root_link_quat_w.clone()
        expanded_quat = root_quat_w[:, None, :].expand(-1, self._target_count, -1)
        self._executor.set_target_sequence(
            root_pos_w[:, None, :] + quat_apply(expanded_quat, hub_pos_b),
            quat_mul(expanded_quat, hub_quat_b),
            self._target_hub_indices,
        )
        self._executor.begin_bootstrap()

    def _sample_task_targets(self) -> None:
        root = self._raw_env.scene["robot"].data
        self._route_start_w = root.root_link_pos_w.clone()
        self._route_quat_w = yaw_quat(root.root_link_quat_w.clone())
        x_axis = torch.tensor((1.0, 0.0, 0.0), device=self.device).repeat(self.num_envs, 1)
        y_axis = torch.tensor((0.0, 1.0, 0.0), device=self.device).repeat(self.num_envs, 1)
        self._route_x_w = quat_apply(self._route_quat_w, x_axis)
        self._route_y_w = quat_apply(self._route_quat_w, y_axis)
        nominal_route = torch.tensor(self.runtime_cfg.route_s_m, device=self.device)
        self._route_s = nominal_route.repeat(self.num_envs, 1)
        self._route_s += self.runtime_cfg.route_randomization_m * (
            2.0 * torch.rand_like(self._route_s) - 1.0
        )
        local_offsets = torch.zeros(
            (self.num_envs, self._target_count, 3), device=self.device
        )
        for axis, extent in enumerate(self.runtime_cfg.local_randomization_m):
            local_offsets[..., axis] = extent * (
                2.0 * torch.rand((self.num_envs, self._target_count), device=self.device) - 1.0
            )
        hub_pos_b = self._executor.hub_ee_pos_b[self._target_hub_indices]
        hub_quat_b = self._executor.hub_ee_quat_b[self._target_hub_indices]
        expanded_route_quat = self._route_quat_w[:, None, :].expand(
            -1, self._target_count, -1
        )
        target_pos_w = (
            self._route_start_w[:, None, :]
            + self._route_s[..., None] * self._route_x_w[:, None, :]
            + quat_apply(expanded_route_quat, hub_pos_b + local_offsets)
        )
        target_quat_w = quat_mul(expanded_route_quat, hub_quat_b)
        self._executor.set_target_sequence(
            target_pos_w, target_quat_w, self._target_hub_indices
        )
        self._last_progress_s = self._route_progress()

    def _reset_synchronized(self) -> None:
        self._low_obs, self._low_extras = self.low_env.reset()
        zero = torch.zeros(self.num_envs, device=self.device)
        self._force_commands(zero, zero)
        self._setup_bootstrap_targets()
        for _ in range(self.runtime_cfg.bootstrap_max_low_steps):
            low_done = self._advance_low(zero, zero)
            if bool(torch.any(low_done)):
                raise RuntimeError("low-level environment reset during high-level bootstrap")
            ready = (
                (self._executor.executor_state == int(ExecutorState.IDLE))
                & (self._executor.prepared_target_index == 0)
            )
            if bool(torch.all(ready)):
                break
        else:
            raise RuntimeError("high-level bootstrap did not reach the first hub")
        self._sample_task_targets()
        self.episode_length_buf.zero_()
        self._previous_base_command.zero_()
        self._episode_reward.zero_()
        self._episode_overlap_steps.zero_()
        self._episode_motion_steps.zero_()
        self._episode_option_rejections.zero_()
        self._episode_local_aborts.zero_()
        self._episode_completion_step.fill_(-1)
        self._episode_emergency_failed.zero_()
        self._episode_counter += 1
        self._obs = self._build_observation()

    def _route_progress(self) -> torch.Tensor:
        base_pos = self._raw_env.scene["robot"].data.root_link_pos_w
        return torch.sum((base_pos - self._route_start_w) * self._route_x_w, dim=-1)

    def _ee_distance(self) -> torch.Tensor:
        q = self._raw_env.scene["robot"].data.joint_pos[:, self._executor._joint_ids]
        ee_pos_b, _, _ = self._executor._forward_end_effector_pose_jacobian(q)
        ee_pos_w = self._raw_env.scene["robot"].data.root_link_pos_w + quat_apply(
            self._raw_env.scene["robot"].data.root_link_quat_w, ee_pos_b
        )
        return torch.linalg.vector_norm(
            self._executor.current_target_pos_w - ee_pos_w, dim=-1
        )

    def _target_pose_b(self, target_indices: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        env_ids = torch.arange(self.num_envs, device=self.device)
        target_pos_w = self._executor._target_position_w[env_ids, target_indices]
        target_quat_w = self._executor._target_quat_w[env_ids, target_indices]
        root = self._raw_env.scene["robot"].data
        pos_b = quat_apply_inverse(root.root_link_quat_w, target_pos_w - root.root_link_pos_w)
        facing_w = quat_apply(
            target_quat_w,
            torch.tensor((0.0, 0.0, 1.0), device=self.device).repeat(self.num_envs, 1),
        )
        facing_b = quat_apply_inverse(root.root_link_quat_w, facing_w)
        return pos_b, facing_b

    def _build_observation(self) -> torch.Tensor:
        current = torch.clamp(
            self._executor.current_target_index, max=self._target_count - 1
        )
        next_target = torch.clamp(current + 1, max=self._target_count - 1)
        current_pos_b, current_facing_b = self._target_pose_b(current)
        next_pos_b, next_facing_b = self._target_pose_b(next_target)
        robot = self._raw_env.scene["robot"].data
        return build_high_level_policy_observation(
            current_target_pos_b=current_pos_b,
            current_target_facing_b=current_facing_b,
            next_target_pos_b=next_pos_b,
            next_target_facing_b=next_facing_b,
            base_lin_vel_b=robot.root_link_lin_vel_b[:, :2],
            base_yaw_rate=robot.root_link_ang_vel_b[:, 2],
            arm_joint_pos=robot.joint_pos[:, self._executor._joint_ids],
            arm_joint_vel=robot.joint_vel[:, self._executor._joint_ids],
            executor_state=self._executor.executor_state,
            active_option=self._executor.active_option,
            option_progress=self._executor.option_progress,
            current_target_index=current,
            target_count=self._target_count,
            previous_base_command=self._previous_base_command,
            option_mask=self._executor.option_mask(),
        )

    def get_observations(self) -> tuple[torch.Tensor, dict]:
        return self._obs, {"observations": {"policy": self._obs, "critic": self._obs}}

    def scripted_scheduler_actions(self) -> torch.Tensor:
        """Return normalized WAIT/TRIGGER demonstrations from the frozen scheduler."""
        root = self._raw_env.scene["robot"].data
        base_pos_w = root.root_link_pos_w
        progress_s = self._route_progress()
        cross_track_m = torch.sum(
            (base_pos_w - self._route_start_w) * self._route_y_w, dim=-1
        )
        current_x_w = quat_apply(
            yaw_quat(root.root_link_quat_w),
            torch.tensor((1.0, 0.0, 0.0), device=self.device).repeat(self.num_envs, 1),
        )
        heading_error = torch.atan2(
            torch.sum(current_x_w * self._route_y_w, dim=-1),
            torch.sum(current_x_w * self._route_x_w, dim=-1),
        )
        route_yaw_error = (
            -heading_error - self.runtime_cfg.route_cross_track_gain * cross_track_m
        )
        current = torch.clamp(
            self._executor.current_target_index, max=self._target_count - 1
        )
        env_ids = torch.arange(self.num_envs, device=self.device)
        active_hubs = self._executor._target_hub_indices[env_ids, current]
        current_target_pos_b = quat_apply_inverse(
            root.root_link_quat_w,
            self._executor.current_target_pos_w - base_pos_w,
        )
        target_minus_hub_b = (
            current_target_pos_b - self._executor.hub_ee_pos_b[active_hubs]
        )
        actions = torch.zeros((self.num_envs, self.num_actions), device=self.device)
        for env_index in range(self.num_envs):
            target_index = int(current[env_index].item())
            command = self._scripted_scheduler.command(
                CoordinatorObservation(
                    target_index=target_index,
                    target_count=self._target_count,
                    longitudinal_distance_m=float(
                        self._route_s[env_index, target_index].item()
                        - progress_s[env_index].item()
                    ),
                    yaw_error_rad=float(route_yaw_error[env_index].item()),
                    local_region_valid=bool(
                        self._executor.local_region_valid[env_index].item()
                    ),
                    prepared_for_current=bool(
                        self._executor.prepared_target_index[env_index]
                        == self._executor.current_target_index[env_index]
                    ),
                    at_stow=bool(self._executor.at_stow[env_index].item()),
                    executor_state=ExecutorState(
                        int(self._executor.executor_state[env_index].item())
                    ),
                    task_complete=bool(self._executor.task_complete[env_index].item()),
                    base_speed_m_s=float(
                        torch.linalg.vector_norm(root.root_link_lin_vel_b[env_index, :2]).item()
                    ),
                    base_yaw_rate_rad_s=float(
                        root.root_link_ang_vel_b[env_index, 2].item()
                    ),
                    target_minus_hub_x_m=float(target_minus_hub_b[env_index, 0].item()),
                    target_minus_hub_y_m=float(target_minus_hub_b[env_index, 1].item()),
                )
            )
            actions[env_index, 0] = command.vx_cmd_m_s / self.runtime_cfg.vx_limit_m_s
            actions[env_index, 1] = (
                command.yaw_rate_cmd_rad_s / self.runtime_cfg.yaw_rate_limit_rad_s
            )
            actions[env_index, 2] = float(
                TriggerAction.TRIGGER
                if command.arm_option
                in (ArmOption.PREPARE_NEXT, ArmOption.EXECUTE_CURRENT)
                else TriggerAction.WAIT
            )
        actions[:, :2].clamp_(-1.0, 1.0)
        return actions

    def record_policy_diagnostics(
        self, option_probabilities: torch.Tensor, actions: torch.Tensor
    ) -> None:
        """Accumulate phase-specific WAIT/TRIGGER policy diagnostics."""
        if option_probabilities.shape != (self.num_envs, 2):
            raise ValueError(
                f"option probabilities must have shape {(self.num_envs, 2)}"
            )
        if actions.shape != (self.num_envs, self.num_actions):
            raise ValueError(
                f"actions must have shape {(self.num_envs, self.num_actions)}"
            )
        # Observation columns 43/44 encode PREPARE/EXECUTE trigger phases.
        phase = self._obs[:, -2:].bool()
        greedy_trigger = option_probabilities[:, 1] > option_probabilities[:, 0]
        sampled_trigger = actions[:, 2].round().long() == 1
        for phase_index in range(2):
            available = phase[:, phase_index]
            self._trigger_probability_sum[phase_index] += option_probabilities[
                available, 1
            ].sum()
            self._trigger_phase_count[phase_index] += available.sum()
            self._trigger_greedy_count[phase_index] += (
                greedy_trigger & available
            ).sum()
            self._trigger_sampled_count[phase_index] += (
                sampled_trigger & available
            ).sum()

    def consume_policy_diagnostics(self) -> dict[str, float]:
        """Return and clear phase-conditioned diagnostics for one PPO iteration."""
        denominator = torch.clamp(self._trigger_phase_count, min=1.0)
        metrics: dict[str, float] = {}
        for phase_index, phase_name in enumerate(("prepare", "execute")):
            metrics[f"trigger_probability_{phase_name}"] = float(
                (self._trigger_probability_sum[phase_index] / denominator[phase_index]).item()
            )
            metrics[f"trigger_greedy_ratio_{phase_name}"] = float(
                (self._trigger_greedy_count[phase_index] / denominator[phase_index]).item()
            )
            metrics[f"trigger_sampled_ratio_{phase_name}"] = float(
                (self._trigger_sampled_count[phase_index] / denominator[phase_index]).item()
            )
            metrics[f"trigger_phase_samples_{phase_name}"] = float(
                self._trigger_phase_count[phase_index].item()
            )
        self._trigger_probability_sum.zero_()
        self._trigger_phase_count.zero_()
        self._trigger_greedy_count.zero_()
        self._trigger_sampled_count.zero_()
        return metrics

    def reset(self) -> tuple[torch.Tensor, dict]:
        self._reset_synchronized()
        return self.get_observations()

    def step(self, actions: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, dict]:
        if actions.shape != (self.num_envs, self.num_actions):
            raise ValueError(
                f"high-level actions must have shape {(self.num_envs, self.num_actions)}"
            )
        previous_distance = self._ee_distance()
        previous_progress = self._route_progress()
        previous_target = self._executor.current_target_index.clone()
        option_mask = self._executor.option_mask()
        vx, yaw, options, request_valid = decode_phase_conditioned_action(
            actions,
            option_mask,
            vx_limit_m_s=self.runtime_cfg.vx_limit_m_s,
            yaw_rate_limit_rad_s=self.runtime_cfg.yaw_rate_limit_rad_s,
        )
        # A single local-region exit must not discard the useful rollouts of
        # every other vector environment.  Isolate already-resolved robots at
        # zero base command/HOLD until the synchronized batch ends.  A true
        # low-level reset is still handled as an immediate batch failure below
        # because the frozen policy's stacked history is shared by the wrapper.
        inactive_before_step = self._episode_emergency_failed | self._executor.task_complete
        vx = torch.where(inactive_before_step, torch.zeros_like(vx), vx)
        yaw = torch.where(inactive_before_step, torch.zeros_like(yaw), yaw)
        options = torch.where(
            inactive_before_step,
            torch.full_like(options, int(ArmOption.HOLD)),
            options,
        )
        request_valid = torch.where(
            inactive_before_step, torch.ones_like(request_valid), request_valid
        )
        accepted = self._executor.request_options(options) & request_valid
        low_done = self._advance_low(vx, yaw)
        new_distance = self._ee_distance()
        new_progress = self._route_progress()
        route_env_ids = torch.arange(self.num_envs, device=self.device)
        active_route_index = torch.clamp(previous_target, max=self._target_count - 1)
        active_station_s = self._route_s[route_env_ids, active_route_index]
        station_distance_progress = torch.abs(active_station_s - previous_progress) - torch.abs(
            active_station_s - new_progress
        )
        target_completed = self._executor.current_target_index > previous_target
        task_completed = self._executor.task_complete
        # ``task_completed`` remains true after the fourth target.  The PPO
        # terminal bonus must be an event pulse, otherwise an environment that
        # finishes before the rest of the synchronized batch receives +20 on
        # every waiting step and learns the wrong objective.
        task_just_completed = task_completed & (previous_target < self._target_count)
        completion_ids = torch.nonzero(
            task_just_completed & (self._episode_completion_step < 0),
            as_tuple=False,
        ).squeeze(-1)
        if len(completion_ids) > 0:
            self._episode_completion_step[completion_ids] = (
                self.episode_length_buf[completion_ids] + 1
            )
        local_abort = self._executor.last_event == int(ExecutorEvent.LOCAL_REGION_EXIT)
        base_delta = torch.linalg.vector_norm(
            torch.stack((vx, yaw), dim=-1) - self._previous_base_command, dim=-1
        )
        reward = compute_go_no_go_reward(
            previous_target_distance_m=previous_distance,
            target_distance_m=new_distance,
            # Reward progress toward the active inspection station, rather
            # than raw forward travel.  Raw route progress can be exploited by
            # driving past every target indefinitely.
            route_progress_delta_m=station_distance_progress,
            target_completed=target_completed,
            task_completed=task_just_completed,
            base_command_delta_norm=base_delta,
            option_rejected=~accepted,
            local_abort=local_abort,
            fall=low_done,
            high_level_dt_s=self.high_level_dt_s,
            weights=self.runtime_cfg.reward,
        )
        reward = torch.where(inactive_before_step, torch.zeros_like(reward), reward)
        self._previous_base_command = torch.stack((vx, yaw), dim=-1)
        self.episode_length_buf += 1
        self._episode_reward += reward
        arm_moving = (
            (self._executor.executor_state == int(ExecutorState.GRAPH_EXECUTION))
            | (self._executor.executor_state == int(ExecutorState.LOCAL_TARGET_SERVO))
        )
        base_moving = (torch.abs(vx) > 1.0e-3) | (torch.abs(yaw) > 1.0e-3)
        self._episode_overlap_steps += arm_moving & base_moving
        self._episode_motion_steps += arm_moving | base_moving
        self._episode_option_rejections += ~accepted
        self._episode_local_aborts += local_abort

        emergency = self._executor.executor_state == int(ExecutorState.EMERGENCY_HOLD)
        self._episode_emergency_failed |= emergency
        failed_batch = bool(torch.any(low_done))
        success_batch = bool(torch.all(task_completed))
        resolved_batch = bool(torch.all(task_completed | self._episode_emergency_failed))
        timeout_batch = bool(torch.max(self.episode_length_buf) >= self.max_episode_length)
        batch_done = failed_batch or resolved_batch or timeout_batch
        dones = torch.full(
            (self.num_envs,), int(batch_done), dtype=torch.long, device=self.device
        )
        time_outs = torch.full(
            (self.num_envs,), timeout_batch and not failed_batch and not success_batch,
            dtype=torch.bool,
            device=self.device,
        )
        log = None
        if batch_done:
            elapsed = self.episode_length_buf.float() * self.high_level_dt_s
            completion_elapsed = torch.where(
                self._episode_completion_step >= 0,
                self._episode_completion_step.float() * self.high_level_dt_s,
                elapsed,
            )
            overlap = self._episode_overlap_steps / torch.clamp(
                self._episode_motion_steps, min=1.0
            )
            log = {
                "task_success": task_completed.float().clone(),
                "cycle_time_s": completion_elapsed.clone(),
                "target_count": self._executor.current_target_index.float().clone(),
                "concurrent_ratio": overlap.clone(),
                "option_rejections": self._episode_option_rejections.clone(),
                "local_aborts": self._episode_local_aborts.clone(),
                "low_level_failure": low_done.float().clone(),
                "emergency_hold": emergency.float().clone(),
                "batch_timeout": torch.full_like(
                    elapsed, float(timeout_batch and not failed_batch and not success_batch)
                ),
                "return": self._episode_reward.clone(),
            }
            self._reset_synchronized()
        else:
            self._obs = self._build_observation()
        extras = {"observations": {"policy": self._obs, "critic": self._obs}, "time_outs": time_outs}
        if log is not None:
            extras["log"] = log
        return self._obs, reward, dones, extras

    def close(self):
        return self.low_env.close()


__all__ = ["FrozenLowLevelSequentialInspectionEnv", "HighLevelInspectionEnvCfg"]
