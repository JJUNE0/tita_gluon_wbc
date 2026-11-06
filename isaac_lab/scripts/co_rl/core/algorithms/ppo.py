#  Copyright 2021 ETH Zurich, NVIDIA CORPORATION
#  SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as functional

from scripts.co_rl.core.modules import ActorCritic
from scripts.co_rl.core.storage import RolloutStorage

class PPO:
    actor_critic: ActorCritic

    def __init__(
        self,
        actor_critic,
        num_learning_epochs=1,
        num_mini_batches=1,
        clip_param=0.2,
        gamma=0.998,
        lam=0.95,
        value_loss_coef=1.0,
        entropy_coef=0.0,
        learning_rate=1e-3,
        max_grad_norm=1.0,
        use_clipped_value_loss=True,
        schedule="fixed",
        desired_kl=0.01,
        device="cpu",
    ):
        self.device = device

        self.desired_kl = desired_kl
        self.schedule = schedule
        self.learning_rate = learning_rate

        # PPO components
        self.actor_critic = actor_critic
        self.actor_critic.to(self.device)
        self.storage = None  # initialized later
        self.optimizer = optim.Adam(self.actor_critic.parameters(), lr=learning_rate)
        self.transition = RolloutStorage.Transition()

        # PPO parameters
        self.clip_param = clip_param
        self.num_learning_epochs = num_learning_epochs
        self.num_mini_batches = num_mini_batches
        self.value_loss_coef = value_loss_coef
        self.entropy_coef = entropy_coef
        self.gamma = gamma
        self.lam = lam
        self.max_grad_norm = max_grad_norm
        self.use_clipped_value_loss = use_clipped_value_loss

        self.cfg = None
        self.behavior_cloning_observations = None
        self.behavior_cloning_actions = None
        self.behavior_cloning_reference_outputs = None
        self.behavior_cloning_coefficient = 0.0
        self.behavior_cloning_batch_size = 0
        self.last_behavior_cloning_loss = 0.0

    def set_behavior_cloning_reference(
        self,
        observations,
        actions,
        coefficient=1.0,
        batch_size=4096,
    ):
        """Anchor a hybrid policy to scheduler demonstrations during PPO updates."""
        if coefficient <= 0.0 or batch_size <= 0:
            raise ValueError("behavior-cloning coefficient and batch size must be positive")
        if not hasattr(self.actor_critic, "actor_body") or not hasattr(
            self.actor_critic, "continuous_action_dim"
        ):
            raise TypeError("behavior-cloning anchoring requires a hybrid actor")
        if observations.ndim != 2 or actions.ndim != 2 or len(observations) != len(actions):
            raise ValueError("behavior-cloning observations/actions must be aligned rank-2 tensors")
        labels = actions[:, self.actor_critic.continuous_action_dim].round().long()
        class_counts = torch.bincount(
            labels, minlength=self.actor_critic.discrete_action_dim
        ).float()
        if bool(torch.any(class_counts == 0)):
            raise ValueError("behavior-cloning reference must contain every discrete class")
        self.behavior_cloning_observations = observations.detach().clone().to(self.device)
        self.behavior_cloning_actions = actions.detach().clone().to(self.device)
        with torch.inference_mode():
            self.behavior_cloning_reference_outputs = self.actor_critic.actor_body(
                self.behavior_cloning_observations
            ).detach().clone()
        self.behavior_cloning_coefficient = float(coefficient)
        self.behavior_cloning_batch_size = int(batch_size)

    def set_actor_learning_rate_scale(self, scale):
        """Use a lower actor step size while retaining the configured critic rate."""
        if scale <= 0.0 or scale > 1.0:
            raise ValueError("actor learning-rate scale must be in (0, 1]")
        if not hasattr(self.actor_critic, "actor_body") or not hasattr(
            self.actor_critic, "critic"
        ):
            raise TypeError("actor learning-rate scaling requires separate actor and critic modules")
        actor_parameters = list(self.actor_critic.actor_body.parameters())
        if hasattr(self.actor_critic, "std"):
            actor_parameters.append(self.actor_critic.std)
        actor_parameter_ids = {id(parameter) for parameter in actor_parameters}
        critic_parameters = [
            parameter
            for parameter in self.actor_critic.parameters()
            if id(parameter) not in actor_parameter_ids
        ]
        self.optimizer = optim.Adam(
            [
                {"params": actor_parameters, "lr": self.learning_rate * scale},
                {"params": critic_parameters, "lr": self.learning_rate},
            ]
        )
        self.actor_learning_rate_scale = float(scale)

    def init_storage(self, cfg, num_envs, num_transitions_per_env, actor_obs_shape, critic_obs_shape, action_shape):
        self.update_late_cfg(cfg)
        self.storage = RolloutStorage(
            cfg , num_envs, num_transitions_per_env, actor_obs_shape, critic_obs_shape, action_shape, self.device
        )

    def update_late_cfg(self, cfg):
        self.cfg = cfg

    def test_mode(self):
        self.actor_critic.test()

    def train_mode(self):
        self.actor_critic.train()

    def act(self, obs, critic_obs):
        if self.actor_critic.is_recurrent:
            self.transition.hidden_states = self.actor_critic.get_hidden_states()
        # Compute the actions and values
        self.transition.actions = self.actor_critic.act(obs).detach()
        self.transition.values = self.actor_critic.evaluate(critic_obs).detach()
        self.transition.actions_log_prob = self.actor_critic.get_actions_log_prob(self.transition.actions).detach()
        self.transition.action_mean = self.actor_critic.action_mean.detach()
        self.transition.action_sigma = self.actor_critic.action_std.detach()
        # need to record obs and critic_obs before env.step()
        self.transition.observations = obs
        self.transition.critic_observations = critic_obs
        return self.transition.actions

    def process_env_step(self, rewards, dones, infos):
        self.transition.rewards = rewards.clone()
        self.transition.dones = dones
        self.transition.time_outs = infos["time_outs"].int()
        # Bootstrapping on time outs
        if "time_outs" in infos:
            self.transition.rewards += self.gamma * torch.squeeze(
                self.transition.values * infos["time_outs"].unsqueeze(1).to(self.device), 1
            )

        # Record the transition
        self.storage.add_transitions(self.transition)
        self.transition.clear()
        self.actor_critic.reset(dones)

    def compute_returns(self, last_critic_obs):
        last_values = self.actor_critic.evaluate(last_critic_obs).detach()
        self.storage.compute_returns(last_values, self.gamma, self.lam)

    def update(self):
        mean_value_loss = 0
        mean_surrogate_loss = 0
        mean_behavior_cloning_loss = 0
        if self.actor_critic.is_recurrent:
            generator = self.storage.reccurent_mini_batch_generator(self.num_mini_batches, self.num_learning_epochs)
        else:
            generator = self.storage.mini_batch_generator(self.num_mini_batches, self.num_learning_epochs)
        for (
            obs_batch,
            critic_obs_batch,
            actions_batch,
            target_values_batch,
            advantages_batch,
            returns_batch,
            old_actions_log_prob_batch,
            old_mu_batch,
            old_sigma_batch,
            hid_states_batch,
            masks_batch,
        ) in generator:
            self.actor_critic.act(obs_batch, masks=masks_batch, hidden_states=hid_states_batch[0])
            actions_log_prob_batch = self.actor_critic.get_actions_log_prob(actions_batch)
            value_batch = self.actor_critic.evaluate(
                critic_obs_batch, masks=masks_batch, hidden_states=hid_states_batch[1]
            )
            mu_batch = self.actor_critic.action_mean
            sigma_batch = self.actor_critic.action_std
            entropy_batch = self.actor_critic.entropy

            # KL
            if self.desired_kl is not None and self.schedule == "adaptive":
                with torch.inference_mode():
                    kl = torch.sum(
                        torch.log(sigma_batch / old_sigma_batch + 1.0e-5)
                        + (torch.square(old_sigma_batch) + torch.square(old_mu_batch - mu_batch))
                        / (2.0 * torch.square(sigma_batch))
                        - 0.5,
                        axis=-1,
                    )
                    kl_mean = torch.mean(kl)

                    if kl_mean > self.desired_kl * 2.0:
                        self.learning_rate = max(1e-5, self.learning_rate / 1.5)
                    elif kl_mean < self.desired_kl / 2.0 and kl_mean > 0.0:
                        self.learning_rate = min(1e-2, self.learning_rate * 1.5)

                    for param_group in self.optimizer.param_groups:
                        param_group["lr"] = self.learning_rate

            # Surrogate loss
            ratio = torch.exp(actions_log_prob_batch - torch.squeeze(old_actions_log_prob_batch))
            surrogate = -torch.squeeze(advantages_batch) * ratio
            surrogate_clipped = -torch.squeeze(advantages_batch) * torch.clamp(
                ratio, 1.0 - self.clip_param, 1.0 + self.clip_param
            )
            surrogate_loss = torch.max(surrogate, surrogate_clipped).mean()

            # Value function loss
            if self.use_clipped_value_loss:
                value_clipped = target_values_batch + (value_batch - target_values_batch).clamp(
                    -self.clip_param, self.clip_param
                )
                value_losses = (value_batch - returns_batch).pow(2)
                value_losses_clipped = (value_clipped - returns_batch).pow(2)
                value_loss = torch.max(value_losses, value_losses_clipped).mean()
            else:
                value_loss = (returns_batch - value_batch).pow(2).mean()

            behavior_cloning_loss = torch.zeros((), device=self.device)
            if self.behavior_cloning_observations is not None:
                reference_count = len(self.behavior_cloning_observations)
                reference_indices = torch.randint(
                    reference_count,
                    (min(self.behavior_cloning_batch_size, reference_count),),
                    device=self.device,
                )
                reference_output = self.actor_critic.actor_body(
                    self.behavior_cloning_observations[reference_indices]
                )
                frozen_reference_output = self.behavior_cloning_reference_outputs[
                    reference_indices
                ]
                continuous_dim = self.actor_critic.continuous_action_dim
                continuous_loss = functional.mse_loss(
                    reference_output[:, :continuous_dim],
                    frozen_reference_output[:, :continuous_dim],
                )
                categorical_loss = functional.kl_div(
                    functional.log_softmax(reference_output[:, continuous_dim:], dim=-1),
                    functional.softmax(frozen_reference_output[:, continuous_dim:], dim=-1),
                    reduction="batchmean",
                )
                behavior_cloning_loss = continuous_loss + categorical_loss

            loss = (
                surrogate_loss
                + self.value_loss_coef * value_loss
                - self.entropy_coef * entropy_batch.mean()
                + self.behavior_cloning_coefficient * behavior_cloning_loss
            )

            # Gradient step
            self.optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(self.actor_critic.parameters(), self.max_grad_norm)
            self.optimizer.step()

            mean_value_loss += value_loss.item()
            mean_surrogate_loss += surrogate_loss.item()
            mean_behavior_cloning_loss += behavior_cloning_loss.item()

        num_updates = self.num_learning_epochs * self.num_mini_batches
        mean_value_loss /= num_updates
        mean_surrogate_loss /= num_updates
        self.last_behavior_cloning_loss = mean_behavior_cloning_loss / num_updates
        self.storage.clear()

        return mean_value_loss, mean_surrogate_loss
