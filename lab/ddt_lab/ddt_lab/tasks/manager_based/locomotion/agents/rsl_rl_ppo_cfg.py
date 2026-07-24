# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Default plain RSL-RL PPO training cfg for the locomotion task family.

Sibling to ``agents/np3o_cfg.py``. Hyperparameters are copied from
``np3o_cfg.py::_BASE_NP3O_RUNNER_CFG`` (algorithm/policy sections) so a switch
from NP3O to RSL-RL PPO is an algorithm-only change, not also a hyperparameter
change. NP3O-specific fields (cost/viol coefs, BarlowTwins imitation,
priv/scan encoder dims) have no RSL-RL equivalent and are dropped.

``seed=42`` (``RslRlBaseRunnerCfg`` default) gives this track a fixed seed for
free -- no NP3O run in this project ever fixed one.

Robot- or task-specific overrides live next to the env cfg, e.g.
``robots/tita/agents/rsl_rl_ppo_cfg.py`` subclasses this and only overrides
``experiment_name`` / ``max_iterations``, mirroring how
``robots/tita/agents/np3o_cfg.py`` wraps ``base_np3o_runner_cfg()``.
"""

from __future__ import annotations

from isaaclab.utils import configclass
from isaaclab_rl.rsl_rl import RslRlOnPolicyRunnerCfg, RslRlPpoActorCriticCfg, RslRlPpoAlgorithmCfg


@configclass
class BaseRslRlPpoRunnerCfg(RslRlOnPolicyRunnerCfg):
    """RSL-RL PPO runner cfg mirroring NP3O's current hyperparameters."""

    num_steps_per_env = 24
    max_iterations = 5000
    save_interval = 100
    experiment_name = "locomotion_rslrl"
    obs_groups = {"policy": ["policy"], "critic": ["critic"]}

    policy = RslRlPpoActorCriticCfg(
        init_noise_std=1.0,
        actor_obs_normalization=True,
        critic_obs_normalization=True,
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
    )

    algorithm = RslRlPpoAlgorithmCfg(
        value_loss_coef=1.0,
        use_clipped_value_loss=True,
        clip_param=0.2,
        entropy_coef=0.01,
        num_learning_epochs=5,
        num_mini_batches=4,
        learning_rate=1.0e-3,
        schedule="adaptive",
        gamma=0.99,
        lam=0.95,
        desired_kl=0.01,
        max_grad_norm=1.0,
    )


@configclass
class EstimatorActorCriticCfg(RslRlPpoActorCriticCfg):
    """Actor-critic cfg wiring in ``ActorCriticWithEstimator``.

    See ``docs/plan_base_vel_estimator_ppo.md``. ``class_name`` is resolved
    via ``eval()`` in ``rsl_rl.runners.on_policy_runner``'s module namespace,
    injected there by a monkeypatch shim in ``scripts/rsl_rl/train.py``/``play.py``.
    """

    class_name: str = "ActorCriticWithEstimator"
    estimator_hidden_dims: list[int] = [128, 64]
    estimator_output_dim: int = 3
    estimator_obs_normalization: bool = True


@configclass
class EstimatorPPOCfg(RslRlPpoAlgorithmCfg):
    """PPO cfg wiring in ``PPOWithEstimator``'s auxiliary estimator loss."""

    class_name: str = "PPOWithEstimator"
    estimator_loss_coef: float = 1.0
