"""TRAINING_SIM: alternate fully seated/standing heights with zero motion goals."""

from dataclasses import dataclass
import math

import torch
from mjlab.managers import RewardTermCfg, TerminationTermCfg
from mjlab.utils.lab_api.math import euler_xyz_from_quat, wrap_to_pi

from . import mdp
from .flat_env_roll_pitch_height_cfg import RollPitchHeightCommand, RollPitchHeightCommandCfg
from .sit_stand_env_cfg import TitaSitStandEnvCfg


@dataclass(kw_only=True)
class HeightCycleCommandCfg(RollPitchHeightCommandCfg):
    roll_range: tuple[float, float] = (0., 0.)
    pitch_range: tuple[float, float] = (0., 0.)
    height_range: tuple[float, float] = (.08, .335)
    nominal_height: float = .335
    rel_nominal_envs: float = 0.
    ramp_rates: tuple[float, float, float] = (.15, .15, .05)
    height_motion_range: tuple[float, float] | None = (.20, .27)
    dwell_time_range: tuple[float, float] = (1., 3.)

    def build(self, env):
        for name, bounds in (("height", self.height_range), ("dwell", self.dwell_time_range),
                             ("resampling", self.resampling_time_range)):
            if len(bounds) != 2 or not all(math.isfinite(v) for v in bounds) or not 0 < bounds[0] <= bounds[1]:
                raise ValueError(f"Invalid height-cycle {name} range")
        if self.height_range[0] == self.height_range[1] or self.nominal_height != self.height_range[1]:
            raise ValueError("Height cycle requires distinct endpoints and nominal height at the upper endpoint")
        if self.roll_range != (0., 0.) or self.pitch_range != (0., 0.) or self.height_target_bands is not None:
            raise ValueError("Height cycle supports zero roll/pitch and two height endpoints only")
        if len(self.ramp_rates) != 3 or not all(math.isfinite(v) and v > 0 for v in self.ramp_rates):
            raise ValueError("Height-cycle ramp rates must be positive and finite")
        if self.height_motion_range is not None:
            lo, hi = self.height_motion_range
            if not self.height_range[0] <= lo < hi <= self.height_range[1]:
                raise ValueError("Height motion range must lie within the cycle range")
        return HeightCycleCommand(self, env)


class HeightCycleCommand(RollPitchHeightCommand):
    """Reference ramp plus an independent 1–3 s hold after reference arrival.

    The first phase holds standing. Generic command timers then alternate the
    low/high endpoints. Actual pose achievement is measured, not assumed.
    """

    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        self._saw_sit = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)
        self.dwell_s = torch.zeros(self.num_envs, device=self.device)
        for name in ("completed_cycles", "sit_time_s", "stand_time_s"):
            self.metrics[name] = torch.zeros(self.num_envs, device=self.device)

    def reset(self, env_ids):
        self._next_low[env_ids] = False
        self._saw_sit[env_ids] = False
        return super().reset(env_ids)

    def _resample_command(self, env_ids):
        low = self._next_low[env_ids]
        self.target[env_ids, :2] = 0.
        self.target[env_ids, 2] = torch.where(low, self.cfg.height_range[0], self.cfg.height_range[1])
        self.dwell_s[env_ids] = torch.empty(len(env_ids), device=self.device).uniform_(*self.cfg.dwell_time_range)
        travel = (self.target[env_ids, 2] - self.command[env_ids, 2]).abs() / self.cfg.ramp_rates[2]
        self.time_left[env_ids] = travel + self.dwell_s[env_ids]
        self._next_low[env_ids] = ~low

    def _update_metrics(self):
        dt = self._dt
        if isinstance(dt, (int, float)) and dt == 0:
            return
        active = dt > 0
        height = mdp.data(self._env).root_link_pos_w[:, 2] - self._env.scene.env_origins[:, 2]
        sitting = (self.command[:, 2] - self.cfg.height_range[0]).abs() < 1e-6
        sitting &= (height - self.cfg.height_range[0]).abs() <= .015
        standing = (self.command[:, 2] - self.cfg.height_range[1]).abs() < 1e-6
        standing &= (height - self.cfg.height_range[1]).abs() <= .02
        sitting &= active
        standing &= active
        self._saw_sit |= sitting
        completed = self._saw_sit & standing
        self.metrics["completed_cycles"] += completed.float()
        self._saw_sit &= ~completed
        self.metrics["sit_time_s"] += sitting.float() * dt
        self.metrics["stand_time_s"] += standing.float() * dt


def excessive_roll_pitch(env, limit_deg=30.):
    roll, pitch, _ = euler_xyz_from_quat(mdp.data(env).root_link_quat_w)
    return (wrap_to_pi(roll).abs() > math.radians(limit_deg)) | (wrap_to_pi(pitch).abs() > math.radians(limit_deg))


class TitaHeightOnlyEnvCfg(TitaSitStandEnvCfg):
    def __init__(self, num_envs=4096, play=False):
        super().__init__(num_envs, play)
        self.curriculum_transition_step = None
        self.curriculum_stage = 2
        self.episode_length_s = 20.
        velocity = self.commands["base_velocity"]
        velocity.lin_vel_x = velocity.lin_vel_y = velocity.ang_vel_z = (0., 0.)
        velocity.rel_standing_envs, velocity.rel_straight_envs = 1., 0.
        self.commands["base_pose"] = HeightCycleCommandCfg(resampling_time_range=(1e9, 1e9))
        self.terminations = {
            "time_out": self.terminations["time_out"],
            "roll_pitch": TerminationTermCfg(func=excessive_roll_pitch, params={"limit_deg": 30.}),
        }
        self.rewards["termination"] = RewardTermCfg(func=mdp.reward, weight=-10., params={"kind": "termination"})
