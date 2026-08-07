# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from isaaclab.utils import configclass

from scripts.co_rl.core.wrapper import (
    CoRlMOOPolicyRunnerCfg,
    CoRlPpoActorCriticCfg,
    CoRlEstimatorActorCriticCfg,
    CoRlMooPpoAlgorithmCfg,
    ADDCfg,
)


@configclass
class TitaMOOPPORunnerCfg(CoRlMOOPolicyRunnerCfg):
    num_steps_per_env = 24
    max_iterations = 1500
    save_interval = 100
    experiment_name = "TitaStand-v3-mooppo"
    experiment_description = "test"
    empirical_normalization = False

    policy = CoRlPpoActorCriticCfg(
        init_noise_std=1.0,
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
    )

    algorithm = CoRlMooPpoAlgorithmCfg(
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

    add_cfg = ADDCfg(
        mode="nonmotion",
        disc_coef=0.5,
        disc_grad_penalty_weight=0.1,
        disc_logit_reg=1e-4,
        disc_weight_reg=1e-5,
        disc_hidden_dims=[256, 256],
        disc_learning_rate=1e-4,
        enable_reward_norm=False,
        reward_norm_momentum=0.95,
    )


@configclass
class TitaMOOPPORunnerCfg_Flat_Stand_Drive(TitaMOOPPORunnerCfg):
    def __post_init__(self):
        super().__post_init__()
        self.max_iterations = 1500
        self.experiment_name = "Tita_Flat_Stand_Drive-v3-mooppo"
        self.policy.actor_hidden_dims = [512, 256, 128]
        self.policy.critic_hidden_dims = [512, 256, 128]


@configclass
class TitaMOOPPORunnerCfg_Flat_Stand_Drive_Estimator(TitaMOOPPORunnerCfg_Flat_Stand_Drive):
    """Base-velocity-estimator variant (ActorCriticWithEstimator): actor sees
    an MLP-estimated base_lin_vel instead of ground truth, trained jointly
    via an auxiliary MSE loss against the env's priv_prio group."""

    def __post_init__(self):
        super().__post_init__()
        self.policy = CoRlEstimatorActorCriticCfg(
            init_noise_std=1.0,
            actor_hidden_dims=[512, 256, 128],
            critic_hidden_dims=[512, 256, 128],
            activation="elu",
            estimator_hidden_dims=[128, 64],
            estimator_output_dim=3,
        )
        self.algorithm.estimator_loss_coef = 1.0
