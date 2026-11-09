"""TRAINING_SIM: discrete left/right/both support commands, without a gait."""

from dataclasses import dataclass
import math

import torch
from mjlab.managers import ObservationTermCfg, RewardTermCfg
from mjlab.managers.command_manager import CommandTerm, CommandTermCfg
from mjlab.managers.metrics_manager import MetricsTermCfg

from . import stand_one_leg_reference_env_cfg as reference
from ..flat_env_cfg import TitaFlatEnvCfg


@dataclass(kw_only=True)
class SupportModeCommandCfg(CommandTermCfg):
    episode_fixed: bool = False
    mode_probabilities: tuple[float, float, float] = (1/3, 1/3, 1/3)

    def build(self, env):
        low, high = self.resampling_time_range
        if not (math.isfinite(low) and math.isfinite(high) and 0 < low <= high):
            raise ValueError("Support command hold times must be positive and finite")
        probabilities = self.mode_probabilities
        if (len(probabilities) != 3 or any(not math.isfinite(p) or p < 0 for p in probabilities)
                or not math.isclose(sum(probabilities), 1., abs_tol=1e-6)):
            raise ValueError("Support mode probabilities must be three nonnegative values summing to one")
        return SupportModeCommand(self, env)


class SupportModeCommand(CommandTerm):
    """0=left, 1=right, 2=both; new configs hold a goal until episode reset."""

    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        self.mode = torch.full((self.num_envs,), 2, device=self.device, dtype=torch.long)
        self.fresh = torch.ones(self.num_envs, device=self.device, dtype=torch.bool)
        self._command = torch.nn.functional.one_hot(self.mode, 3).float()
        self.probabilities = torch.tensor(cfg.mode_probabilities, device=self.device)

    @property
    def command(self):
        return self._command

    def reset(self, env_ids):
        self.fresh[env_ids] = True
        return super().reset(env_ids)

    def _resample_command(self, env_ids):
        if self.cfg.episode_fixed:
            fresh_ids = env_ids[self.fresh[env_ids]]
            if len(fresh_ids):
                self.mode[fresh_ids] = torch.multinomial(self.probabilities, len(fresh_ids), replacement=True)
            self.time_left[env_ids] = float("inf")
            self.fresh[env_ids] = False
            return
        initial = torch.randint(3, (len(env_ids),), device=self.device)
        changed = (self.mode[env_ids] + torch.randint(1, 3, (len(env_ids),), device=self.device)) % 3
        self.mode[env_ids] = torch.where(self.fresh[env_ids], initial, changed)
        self.fresh[env_ids] = False

    def _update_command(self, env_ids=None):
        ids = slice(None) if env_ids is None else env_ids
        self._command[ids] = torch.nn.functional.one_hot(self.mode[ids], 3).float()

    def _update_metrics(self):
        pass

    def set_mode(self, mode):
        if isinstance(mode, bool) or not isinstance(mode, int) or mode not in (0, 1, 2):
            raise ValueError("Support mode must be integer 0, 1 or 2")
        self.mode[:] = mode
        self.time_left[:] = float("inf")
        self._update_command()


def support_observation(env, kind="support_mode"):
    return env.command_manager.get_command("support")


def mode(env):
    return env.command_manager.get_term("support").mode


def support_reward(env, clearance_m=.04, grounded_swing_cost=.25):
    left = reference.fixed_support(env, clearance_m, grounded_swing_cost, support_side="left")
    right = reference.fixed_support(env, clearance_m, grounded_swing_cost, support_side="right")
    left_contact, right_contact, _ = reference.support_state(env)
    both = left_contact.float() + right_contact.float() - 1.
    return torch.where(mode(env) == 2, both, torch.where(mode(env) == 0, left, right))


def pose_hint(env):
    left = reference.pose_hint(env, support_side="left")
    right = reference.pose_hint(env, support_side="right")
    return torch.where(mode(env) == 2, 0., torch.where(mode(env) == 0, left, right))


def support_leg_tilt(env):
    left = reference.support_leg_tilt(env, support_side="left")
    right = reference.support_leg_tilt(env, support_side="right")
    return torch.where(mode(env) == 2, 0., torch.where(mode(env) == 0, left, right))


def reward_by_mode(env, source_func, source_params, single_support, command_mode=None):
    """Use reference rewards for 0/1 and the unmodified flat rewards for 2."""
    active = mode(env) != 2 if single_support else mode(env) == 2
    if command_mode is not None:
        if command_mode not in ("standing", "moving"):
            raise ValueError("command_mode must be standing or moving")
        command = env.command_manager.get_command("base_velocity")
        standing = (command.abs() <= command.new_tensor([.02, .02, .03])).all(dim=1)
        active &= standing if command_mode == "standing" else ~standing
    # Flat hold rewards carry state. Preserve inactive rows so they cannot
    # change single-leg critic observations or integrate wheel penalties there.
    fields = {
        "zero_command_position_drift": ("position_anchor", "heading_anchor", "anchor_set", "position_latched"),
        "zero_command_wheel_action": ("wheel_integral",),
    }.get(source_params.get("kind"), ())
    snapshots = []
    if fields:
        velocity = reference.mdp.velocity(env)
        for name in fields:
            value = getattr(velocity, name)
            snapshots.append((value, value.clone()))
    result = source_func(env, **source_params)
    for value, previous in snapshots:
        row_mask = active[:, None] if value.ndim == 2 else active
        value.copy_(torch.where(row_mask, value, previous))
    return torch.where(active, result, 0.)


def achieved_support(env):
    left, right, right_height = reference.support_state(env)
    _, _, left_height = reference.support_state(env, support_side="right")
    actual_left = left & ~right & (right_height >= .01)
    actual_right = right & ~left & (left_height >= .01)
    actual = torch.stack((actual_left, actual_right, left & right), dim=1)
    return actual & ~env.termination_manager.terminated[:, None]


def support_metric(env, kind, mode_id=None):
    selected = mode(env)
    achieved = achieved_support(env).gather(1, selected[:, None]).squeeze(1)
    if kind == "mode_match_fraction":
        return achieved.float()
    if kind == "single_support_time_s":
        return (achieved & (selected != 2)).float() * env.step_dt
    if kind == "command_time_s":
        return (selected == mode_id).float() * env.step_dt
    if kind == "success_time_s":
        return (achieved & (selected == mode_id)).float() * env.step_dt
    raise ValueError(kind)


class TitaSupportCommandEnvCfg(reference.TitaStandOneLegReferenceEnvCfg):
    def __init__(self, num_envs=1024, play=False):
        super().__init__(num_envs, play)
        self.commands["support"] = SupportModeCommandCfg(
            resampling_time_range=(1e9, 1e9), episode_fixed=True, mode_probabilities=(.4, .4, .2))
        for group in self.observations.values():
            group.terms["support_mode"] = ObservationTermCfg(
                func=support_observation, params={"kind": "support_mode"})
        self.rewards["single_support"].func = support_reward
        self.rewards["pose_hint"].func = pose_hint
        self.rewards["support_leg_tilt"].func = support_leg_tilt
        single_rewards = self.rewards
        flat_rewards = TitaFlatEnvCfg(num_envs, play).rewards
        self.rewards = {}
        for prefix, terms, single_support in (("one_leg", single_rewards, True), ("flat", flat_rewards, False)):
            for name, term in terms.items():
                self.rewards[f"{prefix}_{name}"] = RewardTermCfg(func=reward_by_mode, weight=term.weight,
                    params={"source_func": term.func, "source_params": dict(term.params),
                            "single_support": single_support})
        self.metrics = {
            "mode_match_fraction": MetricsTermCfg(func=support_metric, params={"kind": "mode_match_fraction"}),
            "single_support_time_s": MetricsTermCfg(func=support_metric,
                params={"kind": "single_support_time_s"}, reduce="sum"),
        }
        for mode_id, label in enumerate(("left", "right", "both")):
            for kind in ("command_time_s", "success_time_s"):
                self.metrics[f"{label}_{kind}"] = MetricsTermCfg(func=support_metric,
                    params={"kind": kind, "mode_id": mode_id}, reduce="sum")


class TitaSupportVelocityEnvCfg(TitaSupportCommandEnvCfg):
    """Episode-fixed support with a 50/50 moving/stationary velocity-command mixture."""

    def __init__(self, num_envs=4096, play=False):
        super().__init__(num_envs, play)
        velocity = self.commands["base_velocity"]
        velocity.lin_vel_x, velocity.lin_vel_y = (-.5, .5), (0., 0.)
        velocity.ang_vel_z = (-.5, .5)
        velocity.rel_standing_envs, velocity.rel_straight_envs = .5, 0.
        self.rewards["one_leg_stationary"].params["command_mode"] = "standing"
        for name in ("track_lin_vel_xy_exp", "track_ang_vel_z_exp"):
            source = self.rewards["flat_"+name]
            self.rewards["one_leg_"+name] = RewardTermCfg(
                func=reward_by_mode, weight=source.weight,
                params={**source.params, "single_support": True, "command_mode": "moving"})
