"""TRAINING_SIM: mjlab adapter using the existing, unmodified FlashSAC learner."""

from pathlib import Path
import sys

import torch

SHARED = Path(__file__).resolve().parents[1] / "isaac_lab/ddt_lab/scripts/flash_sac"
sys.path.insert(0, str(SHARED))
import runtime  # noqa: E402

class TitaFlashSACEnv:
    def __init__(self, env, action_gain_negative=None, action_gain_positive=None):
        if env.cfg.auto_reset:
            raise ValueError("mjlab FlashSAC requires auto_reset=False for terminal observations")
        self.env, self.num_envs = env, env.num_envs
        self.device = torch.device(env.device)
        obs, _ = env.reset()
        self.actor_obs_dim, self.critic_obs_dim = obs["policy"].shape[1], obs["critic"].shape[1]
        self.action_dim = env.action_manager.total_action_dim
        defaults = runtime.load_default_runner_cfg()
        for name, value in (("action_gain_negative", action_gain_negative), ("action_gain_positive", action_gain_positive)):
            values = tuple(getattr(defaults, name) if value is None else value)
            gains = torch.tensor(values, device=self.device)
            if gains.shape != (self.action_dim,) or not torch.isfinite(gains).all() or not (gains > 0).all():
                raise ValueError(f"Invalid {name}")
            setattr(self, name, values)
            setattr(self, "_" + name, gains)

    @staticmethod
    def _pack(obs):
        packed = torch.cat((obs["policy"], obs["critic"]), dim=1).detach().clone()
        if not torch.isfinite(packed).all():
            raise ValueError("Non-finite observations")
        return packed

    def reset(self, **kwargs):
        return self._pack(self.env.reset(**kwargs)[0])

    def step(self, actions):
        if actions.shape != (self.num_envs, self.action_dim) or not torch.isfinite(actions).all():
            raise ValueError("Invalid normalized actions")
        normalized = actions.detach().to(self.device).clamp(-1., 1.)
        applied = normalized * torch.where(normalized >= 0, self._action_gain_positive, self._action_gain_negative)
        obs, reward, terminated, truncated, info = self.env.step(applied)
        reward, terminated, truncated = reward.clone(), terminated.clone(), truncated.clone()
        if not torch.isfinite(reward).all():
            raise ValueError("Non-finite rewards")
        replay_next = self._pack(obs)
        ids = (terminated | truncated).nonzero(as_tuple=False).flatten()
        # Snapshot all returned data before managers overwrite their reset buffers.
        info = {**info, "log": dict(info.get("log", {}))}
        if len(ids):
            obs, reset_info = self.env.reset(env_ids=ids)
            info["log"].update(reset_info.get("log", {}))
            # A native observation recomputation can draw fresh noise for all
            # rows. Preserve the original transition's non-reset observations.
            next_obs = replay_next.clone()
            next_obs[ids] = self._pack(obs)[ids]
        else:
            next_obs = replay_next.clone()
        return next_obs, replay_next, reward, terminated, truncated, info

    def close(self):
        self.env.close()
