"""TRAINING_SIM: flat driving with roll/pitch (rad) and base-height (m) goals.

Height is base_link z above the flat environment origin, not COM height.
Positive roll/pitch use the robot's XYZ Euler convention; yaw is unconstrained.
The initial ranges are training candidates, not validated hardware limits.
"""

from dataclasses import dataclass
import math

import torch
from mjlab.managers import ObservationTermCfg
from mjlab.managers.command_manager import CommandTerm, CommandTermCfg
from mjlab.managers.metrics_manager import MetricsTermCfg
from mjlab.utils.lab_api.math import euler_xyz_from_quat, wrap_to_pi

from ..common import mdp
from ..flat_env_cfg import TitaFlatEnvCfg


@dataclass(kw_only=True)
class RollPitchHeightCommandCfg(CommandTermCfg):
    roll_range: tuple[float, float] = (-math.radians(30.), math.radians(30.))
    pitch_range: tuple[float, float] = (-math.radians(15.), math.radians(15.))
    height_range: tuple[float, float] = (.27, .42)
    nominal_height: float = .335
    rel_nominal_envs: float = .2
    # Maximum roll/pitch/height change per second, in rad/s, rad/s, m/s.
    ramp_rates: tuple[float, float, float] = (.15, .15, .02)
    # Optional sit/stand sampling bands and height-dependent motion allowance.
    height_target_bands: tuple[tuple[float, float], tuple[float, float]] | None = None
    height_motion_range: tuple[float, float] | None = None

    def build(self, env):
        for label, bounds in (("roll", self.roll_range), ("pitch", self.pitch_range),
                              ("height", self.height_range), ("resampling", self.resampling_time_range)):
            if len(bounds) != 2 or not all(math.isfinite(x) for x in bounds) or bounds[0] > bounds[1]:
                raise ValueError(f"Invalid {label} range")
        if self.height_range[0] <= 0 or self.resampling_time_range[0] <= 0:
            raise ValueError("Height and resampling time must be positive")
        if any(abs(x) >= math.pi/2 for bounds in (self.roll_range, self.pitch_range) for x in bounds):
            raise ValueError("Roll/pitch ranges must be within (-pi/2, pi/2)")
        if not math.isfinite(self.nominal_height) or self.nominal_height <= 0:
            raise ValueError("Nominal height must be positive and finite")
        if not 0 <= self.rel_nominal_envs <= 1:
            raise ValueError("Nominal command fraction must be in [0, 1]")
        if len(self.ramp_rates) != 3 or not all(math.isfinite(x) and x > 0 for x in self.ramp_rates):
            raise ValueError("Three positive finite ramp rates are required")
        if self.height_target_bands is not None:
            if (len(self.height_target_bands) != 2 or any(
                    len(b) != 2 or not all(math.isfinite(x) for x in b)
                    or not self.height_range[0] <= b[0] <= b[1] <= self.height_range[1]
                    for b in self.height_target_bands)
                    or self.height_target_bands[0][1] >= self.height_target_bands[1][0]):
                raise ValueError("Two ordered height target bands within the height range are required")
        if self.height_motion_range is not None:
            b = self.height_motion_range
            if (len(b) != 2 or not all(math.isfinite(x) for x in b)
                    or not self.height_range[0] <= b[0] < b[1] <= self.height_range[1]):
                raise ValueError("Invalid height motion range")
        return RollPitchHeightCommand(self, env)


class RollPitchHeightCommand(CommandTerm):
    """Observe and reward the same rate-limited [roll, pitch, height] command."""

    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        self._nominal = torch.tensor([0., 0., cfg.nominal_height], device=self.device)
        self._rates = torch.tensor(cfg.ramp_rates, device=self.device)
        self.target = self._nominal.repeat(self.num_envs, 1)
        self._command = self.target.clone()
        self._dt = 0.
        self._next_low = torch.zeros(self.num_envs, dtype=torch.bool, device=self.device)

    @property
    def command(self):
        return self._command

    def reset(self, env_ids):
        self._command[env_ids] = self._nominal
        if self.cfg.height_target_bands is not None:
            self._next_low[env_ids] = torch.rand(len(env_ids), device=self.device) < .5
        return super().reset(env_ids)

    def _resample_command(self, env_ids):
        for axis, bounds in enumerate((self.cfg.roll_range, self.cfg.pitch_range, self.cfg.height_range)):
            self.target[env_ids, axis] = torch.empty(len(env_ids), device=self.device).uniform_(*bounds)
        nominal = torch.rand(len(env_ids), device=self.device) < self.cfg.rel_nominal_envs
        self.target[env_ids[nominal]] = self._nominal
        if self.cfg.height_target_bands is not None:
            low = self._next_low[env_ids]
            for mask, bounds in zip((low, ~low), self.cfg.height_target_bands):
                selected = env_ids[mask]
                self.target[selected, 2] = torch.empty(len(selected), device=self.device).uniform_(*bounds)
            self.target[env_ids[low], :2] = 0.
            self.target[env_ids[nominal & ~low]] = self._nominal
            self._next_low[env_ids] = ~low

    def compute(self, dt, env_ids=None):
        self._dt = dt
        super().compute(dt, env_ids)

    def _update_command(self, env_ids=None):
        ids = slice(None) if env_ids is None else env_ids
        dt = self._dt if isinstance(self._dt, (float, int)) else self._dt[ids, None]
        limit = self._rates * dt
        desired = self.target[ids].clone()
        # Ramp height first; the next emitted height controls motion allowance.
        height = self._command[ids, 2] + (desired[:, 2] - self._command[ids, 2]).clamp(-limit[..., 2], limit[..., 2])
        if self.cfg.height_motion_range is not None:
            lo, hi = self.cfg.height_motion_range
            motion = ((height - lo) / (hi - lo)).clamp(0., 1.)
            desired[:, :2] *= motion[:, None]
            # base_velocity is computed first by CommandManager, from its
            # ungated target each tick. Do not gate/mutate that stored target.
            mdp.velocity(self._env).command[ids] *= motion[:, None]
        self._command[ids] += (desired - self._command[ids]).clamp(-limit, limit)
        env_cfg = getattr(self._env, "cfg", None)
        if env_cfg is not None and env_cfg.commands["base_velocity"].stop_state_after_pose:
            mdp.velocity(self._env).update_stop_state(env_ids)

    def _update_metrics(self):
        pass  # Per-step tracking errors are recorded by the metrics manager.


def pose_observation(env, kind="pose_commands"):
    return env.command_manager.get_command("base_pose")


def desired_gravity(command):
    roll, pitch = command[:, 0], command[:, 1]
    return torch.stack((pitch.sin(), -roll.sin()*pitch.cos(), -roll.cos()*pitch.cos()), dim=1)


def pose_tracking_l2(env, kind):
    command, d = pose_observation(env), mdp.data(env)
    if kind == "flat_orientation_l2":
        error = d.projected_gravity_b[:, :2] - desired_gravity(command)[:, :2]
        return error.square().sum(1) * mdp.upright(env)
    if kind == "base_height_l2":
        height = d.root_link_pos_w[:, 2] - env.scene.env_origins[:, 2]
        return (height - command[:, 2]).square() * mdp.upright(env)
    raise ValueError(kind)


def pose_error(env, axis):
    command, d = pose_observation(env), mdp.data(env)
    if axis == 2:
        actual = d.root_link_pos_w[:, 2] - env.scene.env_origins[:, 2]
        return (actual - command[:, 2]).abs()
    actual = euler_xyz_from_quat(d.root_link_quat_w)[axis]
    return wrap_to_pi(actual - command[:, axis]).abs()


class TitaFlatRollPitchHeightEnvCfg(TitaFlatEnvCfg):
    def __init__(self, num_envs=1024, play=False):
        super().__init__(num_envs, play)
        # Freeze the stop reference only after the body has settled, as in the
        # hybrid walk tasks. Pose/sit_stand must not anchor during deceleration.
        velocity = self.commands["base_velocity"]
        velocity.wheel_error_velocity_thresholds = (.1, .15)
        velocity.wheel_error_moving_anchor = True
        velocity.stop_state_after_pose = True
        # Full height/roll sweeps take up to 7.5/7.0 s at the inherited ramp
        # rates; leave time to reach a target before drawing another one.
        self.commands["base_pose"] = RollPitchHeightCommandCfg(resampling_time_range=(10., 12.))
        for group in self.observations.values():
            group.terms["pose_commands"] = ObservationTermCfg(
                func=pose_observation, params={"kind": "pose_commands"}, scale=(1., 1., 1.))
        for name in ("base_height_l2", "flat_orientation_l2"):
            self.rewards[name].func = pose_tracking_l2
        # A roll goal requires different left/right leg extensions.
        self.rewards["joint_mirror"].weight = 0.
        self.metrics.update({
            name: MetricsTermCfg(func=pose_error, params={"axis": axis})
            for axis, name in enumerate(("roll_error_rad", "pitch_error_rad", "height_error_m"))
        })


def make_flat_roll_pitch_height_env_cfg(num_envs=1024, play=False):
    return TitaFlatRollPitchHeightEnvCfg(num_envs, play)
