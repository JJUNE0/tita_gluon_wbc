# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""TRAINING_SIM: TITA FlashSAC defaults and estimator observation handling.

This module uses only the standard library so CLI help and CPU learner tests
can read the same defaults before Isaac Sim starts. Command-line arguments
override runner defaults. The PPO environment/config remains shared, while
FlashSAC disables its unused estimator_target group on the run's config copy.
"""

from dataclasses import asdict, dataclass, field
import math


@dataclass
class FlashSACAlgorithmCfg:
    """Learner/network defaults from the existing FlashSAC port."""

    normalize_reward: bool = True
    normalized_G_max: float = 5.0
    asymmetric_observation: bool = True

    learning_rate_init: float = 3e-4
    learning_rate_peak: float = 3e-4
    learning_rate_end: float = 1.5e-4
    learning_rate_warmup_rate: float = 1e-6
    learning_rate_decay_rate: float = 1.0

    actor_num_blocks: int = 2
    actor_hidden_dim: int = 128
    actor_bc_alpha: float = 0.0
    actor_noise_zeta_mu: float = 2.0
    actor_noise_zeta_max: int = 16
    actor_update_period: int = 2

    critic_num_blocks: int = 2
    critic_hidden_dim: int = 256
    critic_num_bins: int = 101
    critic_min_v: float = -5.0
    critic_max_v: float = 5.0
    critic_target_update_tau: float = 0.01

    temp_initial_value: float = 0.01
    temp_target_sigma: float = 0.15
    temp_target_entropy: float = 0.0  # Learner derives the actual target from action dimension.
    gamma: float = 0.99
    compile_mode: str = "auto"
    load_optimizer: bool = True
    load_reward_normalizer: bool = True


@dataclass
class TitaFlatFlashSACRunnerCfg:
    """Training settings and observation policy for the selected flat task."""

    task: str = "DDT-Velocity-Flat-Tita-v0"
    seed: int = 42
    num_envs: int = 1024
    steps: int = 100000
    device: str = "cuda:0"
    buffer_size: int = 1000000
    min_buffer: int = 100000
    batch_size: int = 2048
    buffer_device: str | None = None
    updates_per_step: float = 2.0
    n_step: int = 3
    compile: bool = False
    amp: bool = False
    save_every: int = 5000
    log_every: int = 100
    logger: str = "tensorboard"
    wandb_project: str = "tita_flat_flash_sac"
    wandb_entity: str | None = None
    run_name: str | None = None
    wandb_mode: str | None = None  # None lets the SDK honor WANDB_MODE.
    wandb_run_id: str | None = None

    # Native order: L hip/shoulder/knee/wheel, R hip/shoulder/knee/wheel.
    # Map normalized tanh actions piecewise about zero, preserving the default
    # pose. Native scales remain 0.25 rad for legs and 5 rad/s for wheels.
    # Selected with PPO distributions and paired native cap rollouts (2026-10-14).
    # Hip gains keep targets at -0.7..+0.7 rad (soft limit +-0.707) about the
    # symmetric leg_1 = 0 default; the old 3.2/2.4 assumed a +0.1 default.
    action_gain_negative: tuple[float, ...] = (2.8, 2.0, 2.8, 6.0, 2.8, 2.0, 2.8, 6.0)
    action_gain_positive: tuple[float, ...] = (2.8, 2.0, 2.8, 6.0, 2.8, 2.0, 2.8, 6.0)

    # A True value is rejected until estimator network, replay supervision,
    # auxiliary loss and actor input are implemented in the FlashSAC learner.
    use_velocity_estimator: bool = False
    agent: FlashSACAlgorithmCfg = field(default_factory=FlashSACAlgorithmCfg)

    def validate(self):
        for name in ("action_gain_negative", "action_gain_positive"):
            values = getattr(self, name)
            if len(values) != 8 or any(not math.isfinite(value) or value <= 0 for value in values):
                raise ValueError(f"{name} must contain 8 positive finite gains in native joint order")
        if self.use_velocity_estimator:
            raise ValueError(
                "FlashSAC velocity estimator is not implemented; keep use_velocity_estimator=False. "
                "Enabling it requires the estimator network, replay targets and auxiliary loss."
            )
        if not self.agent.asymmetric_observation:
            raise ValueError("TITA FlashSAC requires asymmetric_observation=True for separate policy/critic inputs")

    def apply_env_cfg(self, env_cfg):
        """Disable unused PPO supervision only on this FlashSAC run's config."""
        self.validate()
        env_cfg.observations.estimator_target = None

    def to_agent_kwargs(self, args):
        """Resolve runtime CLI/device/replay/schedule values for FlashSACConfig."""
        self.validate()
        values = asdict(self.agent)
        update_steps = max(1, int(args.steps * args.updates_per_step))
        values.update(
            seed=args.seed,
            device_type=args.device,
            buffer_max_length=args.buffer_size,
            buffer_min_length=args.min_buffer,
            buffer_device_type=args.buffer_device or args.device,
            sample_batch_size=args.batch_size,
            learning_rate_warmup_step=int(self.agent.learning_rate_warmup_rate * update_steps),
            learning_rate_decay_step=int(self.agent.learning_rate_decay_rate * update_steps),
            n_step=args.n_step,
            use_compile=args.compile,
            use_amp=args.amp and args.device.startswith("cuda"),
        )
        return values
