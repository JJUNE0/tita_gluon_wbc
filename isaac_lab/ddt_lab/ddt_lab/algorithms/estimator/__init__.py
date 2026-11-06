# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Learned ``base_lin_vel`` estimator, trained jointly with plain RSL-RL PPO.

See ``docs/plan_base_vel_estimator_ppo.md`` for the full design. Subclasses
``rsl_rl``'s ``ActorCritic``/``PPO`` (pinned to rsl-rl 3.1.2) rather than
modifying the installed package -- injected into
``rsl_rl.runners.on_policy_runner``'s ``eval()`` namespace by
``scripts/rsl_rl/train.py``/``play.py`` via a monkeypatch shim.
"""

from .actor_critic_with_estimator import ActorCriticWithEstimator
from .ppo_with_estimator import PPOWithEstimator

__all__ = [
    "ActorCriticWithEstimator",
    "PPOWithEstimator",
]
