# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Custom command terms for TITA (jump task, ramped velocity command)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

import torch
from isaaclab.envs.mdp import UniformVelocityCommand, UniformVelocityCommandCfg
from isaaclab.managers import CommandTerm, CommandTermCfg
from isaaclab.utils import configclass

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


class JumpCommand(CommandTerm):
    """Discrete squat/jump command in {-1, 0, +1}.

    -1 (squat): sustained -- resampled like a normal held command via
       ``cfg.resampling_time_range``; forces ``cfg.velocity_command_name`` to
       zero for squatting envs. Requires that velocity command to be declared
       *before* this term in ``CommandsCfg`` (command terms run in declaration
       order each step, so this term can override it after it updates).
     0 (flat): sustained, identical to the plain flat-locomotion task.
    +1 (jump): a one-shot trigger. Emitted for exactly ``cfg.pulse_steps``
       control steps and then forced back to 0 automatically; gated behind a
       per-step probability and a cooldown so triggers only fire while flat
       and are spaced apart.
    """

    cfg: JumpCommandCfg

    def __init__(self, cfg: JumpCommandCfg, env: ManagerBasedRLEnv):
        super().__init__(cfg, env)
        self.hold_state = torch.zeros(self.num_envs, device=self.device)
        self.pulse_steps_left = torch.zeros(self.num_envs, device=self.device)
        self.cooldown_left = torch.zeros(self.num_envs, device=self.device)
        self.jump_command_b = torch.zeros(self.num_envs, 1, device=self.device)
        self.metrics["squat_frac"] = torch.zeros(self.num_envs, device=self.device)

    def __str__(self) -> str:
        return (
            "JumpCommand:\n"
            f"\tResampling time range: {self.cfg.resampling_time_range}\n"
            f"\tSquat probability: {self.cfg.squat_prob}\n"
            f"\tMean jump-trigger interval: {self.cfg.mean_trigger_interval_s} s"
        )

    """
    Properties
    """

    @property
    def command(self) -> torch.Tensor:
        """Command tensor, shape (num_envs, 1), values in {-1, 0, 1}."""
        return self.jump_command_b

    """
    Implementation specific functions.
    """

    def _update_metrics(self):
        self.metrics["squat_frac"] += (self.hold_state < 0.0).float()

    def _resample_command(self, env_ids: Sequence[int]):
        r = torch.empty(len(env_ids), device=self.device)
        is_squat = r.uniform_(0.0, 1.0) <= self.cfg.squat_prob
        self.hold_state[env_ids] = torch.where(
            is_squat,
            -torch.ones(len(env_ids), device=self.device),
            torch.zeros(len(env_ids), device=self.device),
        )
        self.pulse_steps_left[env_ids] = 0.0
        self.cooldown_left[env_ids] = 0.0

    def _update_command(self):
        dt = self._env.step_dt

        # decrement cooldown
        self.cooldown_left = torch.clamp(self.cooldown_left - dt, min=0.0)

        # roll new jump triggers: only for envs currently flat, not already
        # mid-pulse, and out of cooldown
        can_trigger = (self.hold_state == 0.0) & (self.pulse_steps_left <= 0.0) & (self.cooldown_left <= 0.0)
        trigger_prob = dt / self.cfg.mean_trigger_interval_s
        roll = torch.rand(self.num_envs, device=self.device)
        new_trigger = can_trigger & (roll < trigger_prob)
        self.pulse_steps_left = torch.where(
            new_trigger, torch.full_like(self.pulse_steps_left, float(self.cfg.pulse_steps)), self.pulse_steps_left
        )
        self.cooldown_left = torch.where(
            new_trigger, torch.full_like(self.cooldown_left, self.cfg.cooldown_s), self.cooldown_left
        )

        # command this step: +1 while a pulse is active, else the held state (0 or -1)
        is_pulsing = self.pulse_steps_left > 0.0
        self.jump_command_b[:, 0] = torch.where(is_pulsing, torch.ones_like(self.hold_state), self.hold_state)

        # force base velocity command to zero while squatting -- relies on the
        # velocity command term having already updated this step (see class docstring)
        is_squat = self.hold_state < 0.0
        vel_cmd = self._env.command_manager.get_command(self.cfg.velocity_command_name)
        vel_cmd[is_squat] = 0.0

        # consume one pulse step (auto-reverts to 0 next step)
        self.pulse_steps_left = torch.clamp(self.pulse_steps_left - 1.0, min=0.0)


@configclass
class JumpCommandCfg(CommandTermCfg):
    """Configuration for :class:`JumpCommand`."""

    class_type: type = JumpCommand

    velocity_command_name: str = "base_velocity"
    """Name of the velocity command term to zero out while squatting."""
    squat_prob: float = 0.3
    """Probability that a resampled hold state is squat (-1) rather than flat (0)."""
    pulse_steps: int = 1
    """Number of control steps the jump command reads +1 before auto-reverting to 0."""
    cooldown_s: float = 3.0
    """Minimum time after a jump trigger before another can fire."""
    mean_trigger_interval_s: float = 4.0
    """Expected time between jump triggers while flat and out of cooldown."""


class RampedVelocityCommand(UniformVelocityCommand):
    """``UniformVelocityCommand`` whose *emitted* command ramps toward the
    resampled target at a fixed rate per step, instead of jumping instantly.

    Training's base velocity command normally jumps straight to a new sampled
    value on every resample; real teleop (keyboard/joystick) always presents a
    ramped command instead (e.g. the sim2sim keyboard node's per-keypress
    +/-0.05 increments). This narrows that train/deploy command-profile
    mismatch -- suspected to contribute to the joint-level ("shoulder") shake
    observed specifically at command onset/decel, not in steady state.

    ``self.vel_command_b`` (inherited) is the *target*: the base class's
    resample/heading-tracking/standing-zero logic still writes into it via
    plain ``super()`` calls, unchanged. ``self._emitted_command_b`` is the
    actual output (the ``command`` property read by observations/rewards),
    ramped toward the target by at most ``cfg.ramp_rate`` units/s per axis
    per step.

    Two additional fixes vs. the original My7 version (2026-07-20):

    1. **Reset carryover bug**: the base ``CommandTerm.reset()`` only
       resamples the *target* (``vel_command_b``) -- it never touched
       ``_emitted_command_b``, so after every episode reset (robot falls /
       times out) the emitted command kept whatever value it held at the end
       of the *previous* episode and ramped from there, not from zero. Since
       the physical robot state always resets to the default (zero-velocity)
       pose, this fed the policy a command that didn't match reality on the
       very first steps of practically every fresh episode (env resets
       happen constantly at 4096 envs). Fixed by overriding ``reset()`` to
       zero ``_emitted_command_b`` for the reset env_ids.
    2. **``initial_phase_time`` settle window** (mirrors the
       ``initial_phase_time`` field in the flamingo reference's
       ``UniformVelocityWithZCommand``, adapted to keep the ramp instead of
       jumping): for ``cfg.initial_phase_time`` seconds after each reset, the
       *target* is also forced to zero, so the freshly-spawned robot gets a
       genuine settle period before any command (even a ramped one) starts
       pulling on it. Once the window ends, the real resampled target
       reappears and the existing ramp carries the emitted command up to it
       smoothly (no jump, unlike the flamingo reference which has no ramp).
    """

    cfg: RampedVelocityCommandCfg

    def __init__(self, cfg: RampedVelocityCommandCfg, env: ManagerBasedRLEnv):
        super().__init__(cfg, env)
        self._emitted_command_b = torch.zeros_like(self.vel_command_b)
        self._time_since_reset = torch.zeros(self.num_envs, device=self.device)

    @property
    def command(self) -> torch.Tensor:
        """Ramped command actually applied, shape (num_envs, 3)."""
        return self._emitted_command_b

    def reset(self, env_ids: Sequence[int] | None = None) -> dict[str, float]:
        extras = super().reset(env_ids)
        if env_ids is None:
            env_ids = slice(None)
        self._emitted_command_b[env_ids] = 0.0
        self._time_since_reset[env_ids] = 0.0
        return extras

    def _update_metrics(self):
        # mirror the base class's tracking-error metric, but against the
        # emitted (ramped) command rather than the instantly-updated target --
        # a more meaningful "did the robot track what it was actually told" stat.
        max_command_time = self.cfg.resampling_time_range[1]
        max_command_step = max_command_time / self._env.step_dt
        self.metrics["error_vel_xy"] += (
            torch.norm(self._emitted_command_b[:, :2] - self.robot.data.root_lin_vel_b[:, :2], dim=-1)
            / max_command_step
        )
        self.metrics["error_vel_yaw"] += (
            torch.abs(self._emitted_command_b[:, 2] - self.robot.data.root_ang_vel_b[:, 2]) / max_command_step
        )

    def _update_command(self):
        # updates the *target* (self.vel_command_b): heading tracking + standing zeroing
        super()._update_command()

        # settle window: hold the target at zero for cfg.initial_phase_time
        # seconds after each reset, so a freshly-spawned robot isn't
        # immediately pulled on (even by a ramp) before it's had time to settle.
        self._time_since_reset += self._env.step_dt
        settling_env_ids = (self._time_since_reset <= self.cfg.initial_phase_time).nonzero(as_tuple=False).flatten()
        if len(settling_env_ids) > 0:
            self.vel_command_b[settling_env_ids, :] = 0.0

        max_step = self.cfg.ramp_rate * self._env.step_dt
        delta = torch.clamp(self.vel_command_b - self._emitted_command_b, -max_step, max_step)
        self._emitted_command_b = self._emitted_command_b + delta


@configclass
class RampedVelocityCommandCfg(UniformVelocityCommandCfg):
    """Configuration for :class:`RampedVelocityCommand`."""

    class_type: type = RampedVelocityCommand

    ramp_rate: float = 2.5
    """Max rate of change of the emitted command per axis, in units/s (m/s^2 for
    linear axes, rad/s^2 for yaw). Default 2.5 matches ~0.05 per 0.02s control
    step, mirroring the keyboard teleop node's per-keypress increment."""

    initial_phase_time: float = 2.0
    """Seconds after each reset during which the target command is held at
    zero, so a freshly-spawned robot settles before any command (ramped or
    not) starts pulling on it. Mirrors the flamingo reference's
    ``initial_phase_time`` field."""
