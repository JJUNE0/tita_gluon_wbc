"""Hybrid Gaussian/categorical actor-critic for option-based control."""

from __future__ import annotations

import torch
import torch.nn as nn
from torch.distributions import Categorical, Normal

from .actor_critic import get_activation


def _mlp(input_dim: int, hidden_dims: list[int], output_dim: int, activation: str) -> nn.Sequential:
    if not hidden_dims:
        return nn.Sequential(nn.Linear(input_dim, output_dim))
    layers: list[nn.Module] = [nn.Linear(input_dim, hidden_dims[0]), get_activation(activation)]
    for index, hidden_dim in enumerate(hidden_dims):
        if index == len(hidden_dims) - 1:
            layers.append(nn.Linear(hidden_dim, output_dim))
        else:
            layers.extend((nn.Linear(hidden_dim, hidden_dims[index + 1]), get_activation(activation)))
    return nn.Sequential(*layers)


class HybridActorCritic(nn.Module):
    """PPO policy with two continuous commands and one categorical option.

    The environment-facing action is compact: continuous values occupy the
    first ``continuous_action_dim`` columns and the final column stores the
    sampled categorical index as a float.  PPO still receives the exact joint
    Gaussian-plus-categorical log probability.

    If ``action_mask_obs_start`` is configured, the corresponding
    ``discrete_action_dim`` observation columns are interpreted as a binary
    option mask.  This keeps invalid executor requests out of both sampling
    and greedy inference while allowing the environment to remain the final
    authority on option acceptance.
    """

    is_recurrent = False
    requires_fixed_kl_schedule = True

    def __init__(
        self,
        num_actor_obs: int,
        num_critic_obs: int,
        num_actions: int,
        actor_hidden_dims: list[int] = [256, 256, 256],
        critic_hidden_dims: list[int] = [256, 256, 256],
        activation: str = "elu",
        init_noise_std: float = 1.0,
        continuous_action_dim: int = 2,
        discrete_action_dim: int = 4,
        action_mask_obs_start: int | None = None,
        **kwargs,
    ):
        if kwargs:
            print(
                "HybridActorCritic.__init__ got unexpected arguments, which will be ignored: "
                + str(sorted(kwargs))
            )
        super().__init__()
        if continuous_action_dim <= 0:
            raise ValueError("continuous_action_dim must be positive")
        if discrete_action_dim < 2:
            raise ValueError("discrete_action_dim must be at least two")
        if num_actions != continuous_action_dim + 1:
            raise ValueError(
                "HybridActorCritic expects a compact action with continuous commands plus one "
                f"categorical-index column; got num_actions={num_actions}, "
                f"continuous_action_dim={continuous_action_dim}"
            )
        if action_mask_obs_start is not None:
            mask_start = action_mask_obs_start
            if mask_start < 0:
                mask_start += num_actor_obs
            if mask_start < 0 or mask_start + discrete_action_dim > num_actor_obs:
                raise ValueError("categorical action-mask observation slice is out of bounds")
            self.action_mask_obs_start = mask_start
        else:
            self.action_mask_obs_start = None

        self.continuous_action_dim = continuous_action_dim
        self.discrete_action_dim = discrete_action_dim
        self.actor_body = _mlp(
            num_actor_obs,
            actor_hidden_dims,
            continuous_action_dim + discrete_action_dim,
            activation,
        )
        self.critic = _mlp(num_critic_obs, critic_hidden_dims, 1, activation)
        self.std = nn.Parameter(init_noise_std * torch.ones(continuous_action_dim))
        self.continuous_distribution: Normal | None = None
        self.option_distribution: Categorical | None = None
        Normal.set_default_validate_args = False

    def reset(self, dones=None):
        pass

    def forward(self):
        raise NotImplementedError

    def _masked_logits(self, observations: torch.Tensor, logits: torch.Tensor) -> torch.Tensor:
        if self.action_mask_obs_start is None:
            return logits
        start = self.action_mask_obs_start
        mask = observations[..., start : start + self.discrete_action_dim] > 0.5
        if bool(torch.any(~torch.any(mask, dim=-1))):
            raise ValueError("every environment must expose at least one valid arm option")
        return logits.masked_fill(~mask, torch.finfo(logits.dtype).min)

    def update_distribution(self, observations: torch.Tensor) -> None:
        output = self.actor_body(observations)
        mean = output[..., : self.continuous_action_dim]
        logits = self._masked_logits(observations, output[..., self.continuous_action_dim :])
        self.continuous_distribution = Normal(mean, mean * 0.0 + self.std)
        self.option_distribution = Categorical(logits=logits)

    @property
    def action_mean(self) -> torch.Tensor:
        if self.continuous_distribution is None or self.option_distribution is None:
            raise RuntimeError("action distribution has not been initialized")
        option = torch.argmax(self.option_distribution.logits, dim=-1, keepdim=True)
        return torch.cat((self.continuous_distribution.mean, option.to(dtype=torch.float32)), dim=-1)

    @property
    def action_std(self) -> torch.Tensor:
        if self.continuous_distribution is None:
            raise RuntimeError("action distribution has not been initialized")
        categorical_placeholder = torch.zeros_like(self.continuous_distribution.mean[..., :1])
        return torch.cat((self.continuous_distribution.stddev, categorical_placeholder), dim=-1)

    @property
    def entropy(self) -> torch.Tensor:
        if self.continuous_distribution is None or self.option_distribution is None:
            raise RuntimeError("action distribution has not been initialized")
        return self.continuous_distribution.entropy().sum(dim=-1) + self.option_distribution.entropy()

    def act(self, observations: torch.Tensor, **kwargs) -> torch.Tensor:
        self.update_distribution(observations)
        continuous = self.continuous_distribution.sample()
        option = self.option_distribution.sample().unsqueeze(-1)
        return torch.cat((continuous, option.to(dtype=continuous.dtype)), dim=-1)

    def get_actions_log_prob(self, actions: torch.Tensor) -> torch.Tensor:
        if self.continuous_distribution is None or self.option_distribution is None:
            raise RuntimeError("action distribution has not been initialized")
        continuous = actions[..., : self.continuous_action_dim]
        option = actions[..., self.continuous_action_dim].round().long()
        if bool(torch.any((option < 0) | (option >= self.discrete_action_dim))):
            raise ValueError("categorical action index is outside the configured option set")
        return self.continuous_distribution.log_prob(continuous).sum(dim=-1) + self.option_distribution.log_prob(
            option
        )

    def act_inference(self, observations: torch.Tensor) -> torch.Tensor:
        self.update_distribution(observations)
        return self.action_mean

    def evaluate(self, critic_observations: torch.Tensor, **kwargs) -> torch.Tensor:
        return self.critic(critic_observations)
