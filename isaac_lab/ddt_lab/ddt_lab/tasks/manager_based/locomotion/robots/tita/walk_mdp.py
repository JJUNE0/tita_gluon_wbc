"""TRAINING_SIM: phase-conditioned walking with spherical wheels on flat ground.

The command manager advances the gait clock, never reward/observation calls.
Wheel link origins coincide with collision-sphere centers (radius 0.0925 m).
Height calculations here assume a horizontal ground plane.
"""

from __future__ import annotations

import math

import torch
from isaaclab.managers import CommandTerm, CommandTermCfg, SceneEntityCfg
from isaaclab.utils import configclass


class WalkGaitCommand(CommandTerm):
    """Emit [enabled, sin(phase), cos(phase), frequency_hz, stance_fraction].

    Declare after base_velocity. Zero velocity requests standing unless
    step_in_place is set. Right and left legs are half a cycle apart; stance
    fractions >= 0.5 provide double support instead of a commanded flight.
    """

    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        low, high = cfg.frequency_range_hz
        if not (math.isfinite(low) and math.isfinite(high) and 0 < low <= high):
            raise ValueError("frequency_range_hz must be positive, finite and ordered")
        if not 0.5 <= cfg.stance_fraction < 1.0:
            raise ValueError("stance_fraction must be in [0.5, 1)")
        if not math.isfinite(cfg.settle_time_s) or cfg.settle_time_s < 0:
            raise ValueError("settle_time_s must be finite and non-negative")
        self.phase = torch.zeros(self.num_envs, device=self.device)
        self.elapsed = torch.zeros_like(self.phase)
        self.frequency = torch.full_like(self.phase, low)
        self._command = torch.zeros(self.num_envs, 5, device=self.device)
        self._write_command(torch.zeros_like(self.phase, dtype=torch.bool))

    @property
    def command(self):
        return self._command

    def _update_metrics(self):
        pass

    def _resample_command(self, env_ids):
        # Start in double support, with either leg leading equally often.
        self.phase[env_ids] = torch.randint(2, (len(env_ids),), device=self.device) * 0.5
        self.frequency[env_ids] = torch.empty(len(env_ids), device=self.device).uniform_(
            *self.cfg.frequency_range_hz
        )

    def reset(self, env_ids=None):
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        extras = super().reset(env_ids)
        self.elapsed[env_ids] = 0.0
        self._command[env_ids, :3] = 0.0
        self._command[env_ids, 3] = self.frequency[env_ids]
        self._command[env_ids, 4] = self.cfg.stance_fraction
        return extras

    def _write_command(self, enabled):
        self._command[:, 0] = enabled.float()
        self._command[:, 1] = torch.sin(2 * math.pi * self.phase) * enabled
        self._command[:, 2] = torch.cos(2 * math.pi * self.phase) * enabled
        self._command[:, 3] = self.frequency
        self._command[:, 4] = self.cfg.stance_fraction

    def _update_command(self):
        self.elapsed += self._env.step_dt
        velocity = self._env.command_manager.get_command(self.cfg.velocity_command_name)
        moving = (velocity[:, :2].norm(dim=1) > self.cfg.linear_threshold) | (
            velocity[:, 2].abs() > self.cfg.yaw_threshold
        )
        enabled = (moving | self.cfg.step_in_place) & (self.elapsed > self.cfg.settle_time_s)
        self.phase[:] = torch.where(
            enabled, (self.phase + self.frequency * self._env.step_dt) % 1.0, self.phase
        )
        self._write_command(enabled)


@configclass
class WalkGaitCommandCfg(CommandTermCfg):
    class_type: type = WalkGaitCommand
    velocity_command_name: str = "base_velocity"
    frequency_range_hz: tuple[float, float] = (1.25, 1.25)
    stance_fraction: float = 0.6
    settle_time_s: float = 1.0
    linear_threshold: float = 0.02
    yaw_threshold: float = 0.03
    step_in_place: bool = False


def gait_reference(phase, enabled, stance_fraction: float, clearance_m: float):
    """Return ordered L/R stance flags and wheel-bottom height references."""
    phases = torch.stack((phase, (phase + 0.5) % 1.0), dim=1)
    stance = (phases < stance_fraction) | ~enabled.bool().unsqueeze(1)
    swing_progress = ((phases - stance_fraction) / (1.0 - stance_fraction)).clamp(0, 1)
    height = clearance_m * torch.sin(math.pi * swing_progress)
    return stance, torch.where(stance, 0.0, height)


def _reference(env, gait_name, clearance_m=0.0):
    gait = env.command_manager.get_term(gait_name)
    return gait_reference(gait.phase, gait.command[:, 0], gait.cfg.stance_fraction, clearance_m)


def _upright(env):
    return (-env.scene["robot"].data.projected_gravity_b[:, 2]).clamp(0, 1)


def ang_vel_axis_l2(env, axis: int):
    """Squared body roll (0) or pitch (1) rate, with the base reward's upright scaling."""
    if axis not in (0, 1):
        raise ValueError("axis must be 0 (roll) or 1 (pitch)")
    data = env.scene["robot"].data
    upright = (-data.projected_gravity_b[:, 2]).clamp(0, 0.7) / 0.7
    return data.root_ang_vel_b[:, axis].square() * upright


def _contacts(env, sensor_cfg, threshold):
    # A history maximum would retain old stance contacts during early swing.
    return env.scene.sensors[sensor_cfg.name].data.net_forces_w[:, sensor_cfg.body_ids, 2] > threshold


def contact_schedule(env, gait_name: str, sensor_cfg: SceneEntityCfg, threshold: float = 5.0):
    desired, _ = _reference(env, gait_name)
    actual = _contacts(env, sensor_cfg, threshold)
    error = (actual.float() - desired.float()).square().mean(dim=1)
    return torch.exp(-4.0 * error) * _upright(env)


def wheel_clearance(
    env, gait_name: str, asset_cfg: SceneEntityCfg, radius: float = 0.0925,
    clearance_m: float = 0.04, std: float = 0.025,
):
    """Track a swing arch; a grounded wheel has zero bottom clearance."""
    _, desired = _reference(env, gait_name, clearance_m)
    center_z = env.scene[asset_cfg.name].data.body_link_pos_w[:, asset_cfg.body_ids, 2]
    actual = center_z - env.scene.env_origins[:, 2:3] - radius
    error = (actual - desired).square().mean(dim=1)
    return torch.exp(-error / std**2) * _upright(env)
