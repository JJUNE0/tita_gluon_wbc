"""TRAINING_SIM: bridge native TITA manager observations to FlashSAC.

Import this module after installing PyTorch; Isaac Lab is imported only when
``make_flash_sac_env_class`` is called, after AppLauncher starts Isaac Sim.
The actor consumes the existing ``policy`` group, and the critic consumes the
existing ``critic`` group. Other groups, including ``estimator_target``, are
never appended to the actor input.
"""

from __future__ import annotations

from typing import Any

import torch


_ENV_CLASSES: dict[type, type] = {}
_OBS_GROUPS = ("policy", "critic")


def _check_capture_groups(manager: Any) -> None:
    """Require instantaneous observations so pre-reset reads cannot alter history."""
    for name in _OBS_GROUPS:
        dimensions = manager.group_obs_dim.get(name)
        if not isinstance(dimensions, tuple) or len(dimensions) != 1:
            raise ValueError(f"FlashSAC requires concatenated, flat '{name}' observations; got {dimensions!r}.")
        # Isaac Lab resolves group-level history settings onto each term when
        # loading its managers. Check those resolved terms, not only the group.
        terms = manager._group_obs_term_cfgs[name]
        if any(term.history_length > 0 for term in terms):
            raise ValueError(f"FlashSAC terminal capture requires history_length=0 for '{name}'.")
        if any(term.modifiers for term in terms):
            raise ValueError(f"FlashSAC terminal capture does not support observation modifiers in '{name}'.")


def make_flash_sac_env_class(base_class: type | None = None) -> type:
    """Return a native RL env subclass that captures observations before reset.

    The optional base class permits CPU testing of the native reset ordering.
    Ordinary callers omit it and call this factory after starting Isaac Sim.
    Physics, rewards, commands, action transforms and resets remain in Isaac
    Lab's implementation. Only the pre-reset snapshot is added.
    """
    if base_class is None:
        from isaaclab.envs import ManagerBasedRLEnv

        base_class = ManagerBasedRLEnv
    if base_class in _ENV_CLASSES:
        return _ENV_CLASSES[base_class]

    class FlashSACManagerBasedRLEnv(base_class):
        flash_sac_terminal_capture = True

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self._flash_capture_on_reset = False
            self.flash_sac_terminal_env_ids = None
            self.flash_sac_terminal_observations = None
            super().__init__(*args, **kwargs)
            _check_capture_groups(self.observation_manager)

        def step(self, action: torch.Tensor):
            self.flash_sac_terminal_env_ids = None
            self.flash_sac_terminal_observations = None
            self._flash_capture_on_reset = True
            try:
                return super().step(action)
            finally:
                self._flash_capture_on_reset = False

        def _reset_idx(self, env_ids):
            if self._flash_capture_on_reset:
                if self.flash_sac_terminal_env_ids is not None:
                    raise RuntimeError("FlashSAC expects one native reset batch per environment step.")
                # Native ManagerBasedRLEnv calls this after physics/reward and
                # before scene/manager reset. compute_group(False) does not
                # append history or overwrite the manager's observation cache.
                ids = torch.as_tensor(env_ids, device=self.device, dtype=torch.long)
                self.flash_sac_terminal_env_ids = ids.clone()
                self.flash_sac_terminal_observations = {
                    name: self.observation_manager.compute_group(name, update_history=False)[ids].detach().clone()
                    for name in _OBS_GROUPS
                }
            return super()._reset_idx(env_ids)

    _ENV_CLASSES[base_class] = FlashSACManagerBasedRLEnv
    return FlashSACManagerBasedRLEnv


class TitaFlashSACEnv:
    """Pack ``[policy, critic]`` while preserving timeout bootstrap state.

    ``reset()`` returns a packed tensor. ``step(actions)`` returns
    ``(next_obs, replay_next, reward, terminated, truncated, info)``.
    ``next_obs`` includes the new episode observations after native auto-reset;
    ``replay_next`` contains the actual pre-reset state for every ended episode.
    Both snapshots own their storage, including across subsequent steps.
    """

    def __init__(self, env: Any, action_gain_negative=None, action_gain_positive=None) -> None:
        if not getattr(env, "flash_sac_terminal_capture", False):
            raise TypeError("Create the Isaac environment with make_flash_sac_env_class() for terminal capture.")
        _check_capture_groups(env.observation_manager)
        self.env = env
        self.device = torch.device(env.device)
        self.num_envs = int(env.num_envs)
        dimensions = env.observation_manager.group_obs_dim
        self.actor_obs_dim = int(dimensions["policy"][0])
        self.critic_obs_dim = int(dimensions["critic"][0])
        self.action_dim = int(env.action_manager.total_action_dim)
        if min(self.num_envs, self.actor_obs_dim, self.critic_obs_dim, self.action_dim) <= 0:
            raise ValueError("FlashSAC requires positive environment, observation, and action dimensions.")
        for name, values in (("action_gain_negative", action_gain_negative), ("action_gain_positive", action_gain_positive)):
            gain = torch.as_tensor(
                [1.0] * self.action_dim if values is None else values, device=self.device, dtype=torch.float32
            ).clone()
            if gain.shape != (self.action_dim,) or not torch.isfinite(gain).all().item() or not (gain > 0).all().item():
                raise ValueError(f"{name} must contain {self.action_dim} positive finite gains")
            setattr(self, name, tuple(gain.tolist()))
            setattr(self, "_" + name, gain)

    @staticmethod
    def _finite(value: torch.Tensor, name: str) -> None:
        if not torch.isfinite(value).all().item():
            raise ValueError(f"Non-finite values in FlashSAC {name}.")

    def _pack(self, observations: dict[str, torch.Tensor], batch_size: int | None = None) -> torch.Tensor:
        count = self.num_envs if batch_size is None else batch_size
        groups = []
        for name, size in zip(_OBS_GROUPS, (self.actor_obs_dim, self.critic_obs_dim)):
            value = observations.get(name)
            if not isinstance(value, torch.Tensor) or tuple(value.shape) != (count, size):
                shape = getattr(value, "shape", None)
                raise ValueError(f"Expected '{name}' observations {(count, size)}, got {shape}.")
            if value.device != self.device or not value.is_floating_point():
                raise ValueError(f"'{name}' observations must be floating tensors on {self.device}.")
            groups.append(value)
        packed = torch.cat(groups, dim=-1).detach()
        self._finite(packed, "observations")
        return packed

    def reset(self, **kwargs: Any) -> torch.Tensor:
        observations, _ = self.env.reset(**kwargs)
        return self._pack(observations)

    def step(self, actions: torch.Tensor):
        if not isinstance(actions, torch.Tensor) or tuple(actions.shape) != (self.num_envs, self.action_dim):
            raise ValueError(f"Expected actions {(self.num_envs, self.action_dim)}, got {getattr(actions, 'shape', None)}.")
        if not actions.is_floating_point():
            raise ValueError("FlashSAC actions must be floating point tensors.")
        self._finite(actions, "actions")
        # Replay and SAC densities use normalized actions. Only the simulator
        # receives the piecewise gains; zero still requests the default pose.
        normalized = actions.detach().to(device=self.device, dtype=torch.float32).clamp(-1.0, 1.0)
        applied = normalized * torch.where(
            normalized >= 0, self._action_gain_positive, self._action_gain_negative
        )
        observations, reward, terminated, truncated, info = self.env.step(applied)
        next_obs = self._pack(observations)
        replay_next = next_obs.clone()
        for name, value in (("reward", reward), ("terminated", terminated), ("truncated", truncated)):
            if not isinstance(value, torch.Tensor) or tuple(value.shape) != (self.num_envs,):
                raise ValueError(f"Expected {name} shape {(self.num_envs,)}, got {getattr(value, 'shape', None)}.")
            if value.device != self.device:
                raise ValueError(f"FlashSAC {name} must be on {self.device}.")
        self._finite(reward, "reward")
        terminated = terminated.detach().to(dtype=torch.bool).clone()
        truncated = truncated.detach().to(dtype=torch.bool).clone()
        done_ids = (terminated | truncated).nonzero(as_tuple=False).squeeze(-1)
        captured_ids = self.env.flash_sac_terminal_env_ids
        if done_ids.numel():
            if captured_ids is None or not torch.equal(captured_ids, done_ids):
                raise RuntimeError("Missing or inconsistent pre-reset observations for ended FlashSAC episodes.")
            terminal = self._pack(self.env.flash_sac_terminal_observations, batch_size=done_ids.numel())
            replay_next[done_ids] = terminal
        elif captured_ids is not None and captured_ids.numel():
            raise RuntimeError("Native reset occurred without a corresponding termination or timeout.")
        return next_obs, replay_next, reward.detach().clone(), terminated, truncated, dict(info)

    def close(self) -> None:
        self.env.close()
