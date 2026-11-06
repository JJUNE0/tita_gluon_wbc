# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""``ActorCritic`` subclass that prepends a learned ``base_lin_vel`` estimator
to the actor's input, trained jointly with PPO (see
``docs/plan_base_vel_estimator_ppo.md``).

Pinned to rsl-rl 3.1.2's ``ActorCritic`` (``rsl_rl/modules/actor_critic.py``).
"""

from __future__ import annotations

from typing import Any

import torch
from rsl_rl.modules import ActorCritic
from rsl_rl.networks import MLP, EmpiricalNormalization
from tensordict import TensorDict


class ActorCriticWithEstimator(ActorCritic):
    """Actor-critic with a state estimator MLP feeding the actor.

    The ``policy`` obs group must contain pure proprioception only (no
    ``base_lin_vel`` term) -- the estimator predicts it from that group, and
    its (un-detached) output is concatenated with the raw proprio before
    being fed to the actor. A separate ``estimator_target`` obs group
    (ground-truth ``base_lin_vel``, no noise) supplies the supervised target
    consumed by :class:`~ddt_lab.algorithms.estimator.PPOWithEstimator`.
    """

    def __init__(
        self,
        obs: TensorDict,
        obs_groups: dict[str, list[str]],
        num_actions: int,
        estimator_hidden_dims: list[int] = [128, 64],
        estimator_output_dim: int = 3,
        estimator_obs_normalization: bool = True,
        actor_hidden_dims: list[int] = [256, 256, 256],
        activation: str = "elu",
        **kwargs: dict[str, Any],
    ) -> None:
        num_proprio = sum(obs[group].shape[-1] for group in obs_groups["policy"])

        super().__init__(
            obs, obs_groups, num_actions, actor_hidden_dims=actor_hidden_dims, activation=activation, **kwargs
        )

        self.estimator_output_dim = estimator_output_dim
        self.estimator_obs_normalization = estimator_obs_normalization
        self.estimator = MLP(num_proprio, estimator_output_dim, estimator_hidden_dims, "elu")
        self.estimator_normalizer = (
            EmpiricalNormalization(num_proprio) if estimator_obs_normalization else torch.nn.Identity()
        )
        print(f"Estimator MLP: {self.estimator}")

        # Base class built self.actor / self.actor_obs_normalizer for a
        # proprio-only input (num_proprio wide) -- rebuild both for the
        # actual [estimator_output, proprio] width.
        actor_input_dim = estimator_output_dim + num_proprio
        self.actor = MLP(actor_input_dim, num_actions, actor_hidden_dims, activation)
        print(f"Actor MLP (rebuilt for estimator input): {self.actor}")
        if self.actor_obs_normalization:
            self.actor_obs_normalizer = EmpiricalNormalization(actor_input_dim)
        else:
            self.actor_obs_normalizer = torch.nn.Identity()

        self._last_estimator_output: torch.Tensor | None = None

    def _get_proprio_obs(self, obs: TensorDict) -> torch.Tensor:
        return torch.cat([obs[group] for group in self.obs_groups["policy"]], dim=-1)

    def get_actor_obs(self, obs: TensorDict) -> torch.Tensor:
        proprio = self._get_proprio_obs(obs)
        est_out = self.estimator(self.estimator_normalizer(proprio))
        # Not detached -- both the PPO loss (via the actor's dependency) and
        # the explicit supervised loss in PPOWithEstimator shape it.
        self._last_estimator_output = est_out
        return torch.cat([est_out, proprio], dim=-1)

    def update_normalization(self, obs: TensorDict) -> None:
        super().update_normalization(obs)
        if self.estimator_obs_normalization:
            self.estimator_normalizer.update(self._get_proprio_obs(obs))
