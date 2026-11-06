# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""RSL-RL PPO training cfg for Tita.

Built on top of [agents/rsl_rl_ppo_cfg.py](../../agents/rsl_rl_ppo_cfg.py) base;
only ``experiment_name`` differs. Mirrors ``robots/tita/agents/np3o_cfg.py``'s
wrapping pattern for NP3O.
"""

from __future__ import annotations

from isaaclab.utils import configclass

from ddt_lab.tasks.manager_based.locomotion.agents.rsl_rl_ppo_cfg import (
    BaseRslRlPpoRunnerCfg,
    EstimatorActorCriticCfg,
    EstimatorPPOCfg,
)


@configclass
class TitaFlatPPORunnerCfg(BaseRslRlPpoRunnerCfg):
    experiment_name = "tita_flat_rslrl"


@configclass
class TitaFlatEstimatorPPORunnerCfg(TitaFlatPPORunnerCfg):
    """RSL-RL runner cfg for the learned ``base_lin_vel`` estimator variant.

    Swaps ``policy``/``algorithm`` to the ``ActorCriticWithEstimator`` /
    ``PPOWithEstimator`` pair and adds the third ``estimator_target`` obs
    group. See ``docs/plan_base_vel_estimator_ppo.md``.
    """

    experiment_name = "tita_flat_rslrl_estimator"
    obs_groups = {"policy": ["policy"], "critic": ["critic"], "estimator_target": ["estimator_target"]}

    policy = EstimatorActorCriticCfg(
        init_noise_std=1.0,
        actor_obs_normalization=True,
        critic_obs_normalization=True,
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
        estimator_hidden_dims=[128, 64],
        estimator_output_dim=3,
        estimator_obs_normalization=True,
    )

    algorithm = EstimatorPPOCfg(
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
        estimator_loss_coef=1.0,
    )
