#!/usr/bin/env python3
"""Train the position-only sequential-inspection high-level hybrid PPO.

Execution domain: TRAINING_SIM.  The script loads and freezes the validated
TITA+GLUON RMA teacher, then trains only the compact high-level policy.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import math
import os
from pathlib import Path
import sys
import time


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB_ROOT = REPO_ROOT / "lab"
for path in (REPO_ROOT, LAB_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from isaaclab.app import AppLauncher


DEFAULT_LOW_CHECKPOINT = (
    LAB_ROOT
    / "logs"
    / "co_rl"
    / "Tita_Gluon_InspectionCurriculumArm_RMATeacher-v0-mooppo"
    / "mooppo"
    / "2026-08-11_09-47-10_phase1-work-phase2-inspection-hubs"
    / "model_9000.pt"
)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--low-checkpoint", type=Path, default=DEFAULT_LOW_CHECKPOINT)
parser.add_argument(
    "--resume-checkpoint",
    type=Path,
    help="Resume only the high-level PPO state; the low-level checkpoint remains frozen.",
)
parser.add_argument("--num-envs", type=int, default=64)
parser.add_argument("--max-iterations", type=int, default=300)
parser.add_argument("--num-steps-per-env", type=int, default=64)
parser.add_argument("--seed", type=int, default=20260813)
parser.add_argument("--save-interval", type=int, default=100)
parser.add_argument("--logger", choices=("tensorboard", "wandb"), default="wandb")
parser.add_argument("--run-name", default="gate0-position-only-from-scratch")
parser.add_argument("--graph-max-velocity-deg-s", type=float, default=60.0)
parser.add_argument("--graph-max-acceleration-deg-s2", type=float, default=180.0)
parser.add_argument("--episode-length-s", type=float, default=70.0)
parser.add_argument("--high-level-decimation", type=int, default=5)
parser.add_argument("--bc-epochs", type=int, default=0)
parser.add_argument("--bc-learning-rate", type=float, default=3.0e-4)
parser.add_argument("--bc-batch-size", type=int, default=4096)
parser.add_argument(
    "--bc-initial-noise-std",
    type=float,
    default=0.1,
    help="Initial Gaussian base-command exploration std used only for BC warm starts.",
)
parser.add_argument(
    "--ppo-bc-anchor-coef",
    type=float,
    default=0.0,
    help="Optional scheduler-imitation loss coefficient retained during PPO fine-tuning.",
)
parser.add_argument(
    "--ppo-actor-learning-rate-scale",
    type=float,
    default=1.0,
    help="Actor learning-rate multiplier; critic retains the configured PPO rate.",
)
parser.add_argument("--smoke", action="store_true")
parser.add_argument(
    "--profile-env-steps",
    type=int,
    default=0,
    help="Run HOLD-only high-level steps with timing and exit before PPO construction.",
)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import gymnasium as gym  # noqa: E402
import torch  # noqa: E402
import torch.nn.functional as torch_functional  # noqa: E402

import ddt_lab.tasks  # noqa: F401,E402
from scripts.co_rl.core.runners import MOO_OnPolicyRunner, OnPolicyRunner  # noqa: E402
from scripts.co_rl.core.wrapper import CoRlVecEnvWrapper  # noqa: E402

from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.agents.co_rl_cfg import (  # noqa: E402
    TitaGluonSequentialInspectionHighLevelRunnerCfg,
)
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.env_cfg import (  # noqa: E402
    GLUON_INSPECTION_TARGET_HUB_INDICES,
)
from ddt_lab.tasks.moo_based.locomanipulation.velocity.tita_gluon.high_level_env import (  # noqa: E402
    FrozenLowLevelSequentialInspectionEnv,
    HighLevelInspectionEnvCfg,
)


LOW_TASK_ID = "Isaac-Velocity-Flat-Tita-Gluon-SequentialInspection-Play-v0-moo-ppo"


def behavior_clone_scripted_scheduler(
    runner,
    high_env,
    epochs: int,
    learning_rate: float,
    batch_size: int,
    ppo_anchor_coefficient: float,
):
    """Collect one passing scheduler batch and pretrain only the hybrid actor."""
    if epochs <= 0:
        return None
    if learning_rate <= 0.0 or batch_size <= 0:
        raise ValueError("BC learning rate and batch size must be positive")
    observations: list[torch.Tensor] = []
    teacher_actions: list[torch.Tensor] = []
    terminal_log = None
    with torch.inference_mode():
        for _ in range(high_env.max_episode_length):
            obs, _ = high_env.get_observations()
            teacher = high_env.scripted_scheduler_actions()
            observations.append(obs.detach().clone())
            teacher_actions.append(teacher.detach().clone())
            _, _, dones, extras = high_env.step(teacher)
            if bool(torch.any(dones)):
                terminal_log = extras.get("log")
                break
    if terminal_log is None:
        raise RuntimeError("scripted scheduler demonstration did not terminate")
    teacher_success = float(terminal_log["task_success"].float().mean().item())
    if teacher_success < 1.0:
        raise RuntimeError(
            f"scripted scheduler demonstration must pass every environment, got {teacher_success:.6f}"
        )

    obs_dataset = torch.cat(observations, dim=0)
    action_dataset = torch.cat(teacher_actions, dim=0)
    trigger_labels = action_dataset[:, 2].round().long()
    class_counts = torch.bincount(trigger_labels, minlength=2).float()
    if bool(torch.any(class_counts == 0)):
        raise RuntimeError(f"BC demonstration is missing a class: counts={class_counts.tolist()}")
    class_weights = len(trigger_labels) / (2.0 * class_counts)
    actor = runner.alg.actor_critic
    optimizer = torch.optim.Adam(actor.actor_body.parameters(), lr=learning_rate)
    last_loss = 0.0
    for _ in range(epochs):
        permutation = torch.randperm(len(obs_dataset), device=high_env.device)
        for start in range(0, len(obs_dataset), batch_size):
            indices = permutation[start : start + batch_size]
            output = actor.actor_body(obs_dataset[indices])
            continuous_loss = torch_functional.mse_loss(
                output[:, : actor.continuous_action_dim], action_dataset[indices, :2]
            )
            categorical_loss = torch_functional.cross_entropy(
                output[:, actor.continuous_action_dim :],
                trigger_labels[indices],
                weight=class_weights,
            )
            loss = continuous_loss + categorical_loss
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(actor.actor_body.parameters(), 1.0)
            optimizer.step()
            last_loss = float(loss.item())

    with torch.inference_mode():
        output = actor.actor_body(obs_dataset)
        prediction = torch.argmax(output[:, actor.continuous_action_dim :], dim=-1)
        accuracy = float((prediction == trigger_labels).float().mean().item())
        trigger_recall = float(
            (prediction[trigger_labels == 1] == 1).float().mean().item()
        )
        continuous_mse = float(
            torch_functional.mse_loss(
                output[:, : actor.continuous_action_dim], action_dataset[:, :2]
            ).item()
        )
    if ppo_anchor_coefficient > 0.0:
        runner.alg.set_behavior_cloning_reference(
            obs_dataset,
            action_dataset,
            coefficient=ppo_anchor_coefficient,
            batch_size=batch_size,
        )
    return {
        "sample_count": len(obs_dataset),
        "class_counts_wait_trigger": class_counts.long().tolist(),
        "class_weights_wait_trigger": class_weights.tolist(),
        "teacher_success_rate": teacher_success,
        "final_loss": last_loss,
        "classification_accuracy": accuracy,
        "trigger_recall": trigger_recall,
        "continuous_mse": continuous_mse,
        "ppo_anchor_coefficient": ppo_anchor_coefficient,
    }


def main() -> int:
    if args_cli.num_envs <= 0 or args_cli.max_iterations <= 0:
        raise ValueError("num-envs and max-iterations must be positive")
    if args_cli.bc_epochs < 0:
        raise ValueError("bc-epochs must be non-negative")
    if args_cli.bc_initial_noise_std <= 0.0:
        raise ValueError("bc-initial-noise-std must be positive")
    if args_cli.ppo_bc_anchor_coef < 0.0:
        raise ValueError("ppo-bc-anchor-coef must be non-negative")
    if args_cli.ppo_bc_anchor_coef > 0.0 and args_cli.bc_epochs <= 0:
        raise ValueError("ppo-bc-anchor-coef requires a BC warm start")
    if not 0.0 < args_cli.ppo_actor_learning_rate_scale <= 1.0:
        raise ValueError("ppo-actor-learning-rate-scale must be in (0, 1]")
    if args_cli.resume_checkpoint is not None and args_cli.bc_epochs > 0:
        raise ValueError("BC warm start and high-level checkpoint resume are mutually exclusive")
    checkpoint = args_cli.low_checkpoint.resolve()
    if not checkpoint.is_file():
        raise FileNotFoundError(checkpoint)
    if args_cli.smoke:
        args_cli.max_iterations = min(args_cli.max_iterations, 3)
        args_cli.num_steps_per_env = min(args_cli.num_steps_per_env, 8)
        args_cli.save_interval = 1
        args_cli.logger = "tensorboard"

    spec = gym.spec(LOW_TASK_ID)
    low_env_cfg = spec.kwargs["env_cfg_entry_point"]()
    low_env_cfg.seed = args_cli.seed
    low_env_cfg.scene.num_envs = args_cli.num_envs
    low_env_cfg.episode_length_s = max(180.0, args_cli.episode_length_s + 30.0)
    low_env_cfg.sim.render_interval = low_env_cfg.decimation
    low_env_cfg.commands.base_velocity.debug_vis = False
    low_env_cfg.curriculum.widen_height_range = None
    low_env_cfg.actions.gluon_joint_reference.local_orientation_gain = 0.0
    low_env_cfg.actions.gluon_joint_reference.orientation_tolerance_rad = math.pi
    low_env_cfg.actions.gluon_joint_reference.max_velocity_rad_s = math.radians(
        args_cli.graph_max_velocity_deg_s
    )
    low_env_cfg.actions.gluon_joint_reference.max_acceleration_rad_s2 = math.radians(
        args_cli.graph_max_acceleration_deg_s2
    )
    low_agent_cfg = spec.kwargs["co_rl_cfg_entry_point"]()
    setup_start = time.perf_counter()
    gym_env = gym.make(LOW_TASK_ID, cfg=low_env_cfg)
    low_env = CoRlVecEnvWrapper(gym_env, low_agent_cfg)
    low_runner = MOO_OnPolicyRunner(
        low_env, low_agent_cfg.to_dict(), log_dir=None, device=low_agent_cfg.device
    )
    low_runner.load(str(checkpoint))
    low_policy = low_runner.get_inference_policy(device=low_env.unwrapped.device)
    print(f"HIGH_LEVEL_TIMING,stage=low_setup,seconds={time.perf_counter() - setup_start:.6f}", flush=True)

    high_env_cfg = HighLevelInspectionEnvCfg(
        episode_length_s=args_cli.episode_length_s,
        high_level_decimation=args_cli.high_level_decimation,
    )
    bootstrap_start = time.perf_counter()
    high_env = FrozenLowLevelSequentialInspectionEnv(
        low_env,
        low_policy,
        GLUON_INSPECTION_TARGET_HUB_INDICES,
        cfg=high_env_cfg,
        seed=args_cli.seed,
    )
    print(
        f"HIGH_LEVEL_TIMING,stage=bootstrap,seconds={time.perf_counter() - bootstrap_start:.6f}",
        flush=True,
    )
    if args_cli.profile_env_steps > 0:
        hold_actions = torch.zeros((args_cli.num_envs, 3), device=high_env.device)
        profile_start = time.perf_counter()
        for _ in range(args_cli.profile_env_steps):
            high_env.step(hold_actions)
        elapsed = time.perf_counter() - profile_start
        print(
            "HIGH_LEVEL_TIMING,stage=env_steps,"
            f"steps={args_cli.profile_env_steps},seconds={elapsed:.6f},"
            f"steps_per_second={args_cli.profile_env_steps / elapsed:.6f}",
            flush=True,
        )
        high_env.close()
        return 0
    high_agent_cfg = TitaGluonSequentialInspectionHighLevelRunnerCfg()
    high_agent_cfg.seed = args_cli.seed
    high_agent_cfg.max_iterations = args_cli.max_iterations
    high_agent_cfg.num_steps_per_env = args_cli.num_steps_per_env
    high_agent_cfg.save_interval = args_cli.save_interval
    high_agent_cfg.logger = args_cli.logger
    high_agent_cfg.run_name = args_cli.run_name
    high_agent_cfg.device = str(low_env.unwrapped.device)
    if args_cli.bc_epochs > 0:
        high_agent_cfg.policy.init_noise_std = args_cli.bc_initial_noise_std

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = (
        LAB_ROOT
        / "logs"
        / "co_rl"
        / high_agent_cfg.experiment_name
        / "ppo"
        / f"{timestamp}_{high_agent_cfg.run_name}"
    )
    log_dir.mkdir(parents=True, exist_ok=False)
    metadata = {
        "execution_domain": "TRAINING_SIM",
        "evidence_status": "NOT_TESTED",
        "low_checkpoint": str(checkpoint),
        "num_envs": args_cli.num_envs,
        "seed": args_cli.seed,
        "max_iterations": args_cli.max_iterations,
        "num_steps_per_env": args_cli.num_steps_per_env,
        "position_only": True,
        "self_collision_enabled": False,
        "cbf_enabled": False,
        "graph_max_velocity_deg_s": args_cli.graph_max_velocity_deg_s,
        "graph_max_acceleration_deg_s2": args_cli.graph_max_acceleration_deg_s2,
        "high_level_decimation": args_cli.high_level_decimation,
        "high_level_dt_s": high_env.high_level_dt_s,
        "bc_epochs": args_cli.bc_epochs,
        "bc_initial_noise_std": (
            args_cli.bc_initial_noise_std if args_cli.bc_epochs > 0 else None
        ),
        "ppo_bc_anchor_coefficient": args_cli.ppo_bc_anchor_coef,
        "ppo_actor_learning_rate_scale": args_cli.ppo_actor_learning_rate_scale,
    }
    (log_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(f"HIGH_LEVEL_LOG_DIR={log_dir}", flush=True)
    runner_start = time.perf_counter()
    print("HIGH_LEVEL_TIMING,stage=runner_init_begin", flush=True)
    runner = OnPolicyRunner(
        high_env,
        high_agent_cfg.to_dict(),
        log_dir=str(log_dir),
        device=high_agent_cfg.device,
    )
    if args_cli.ppo_actor_learning_rate_scale < 1.0:
        runner.alg.set_actor_learning_rate_scale(args_cli.ppo_actor_learning_rate_scale)
    bc_metrics = behavior_clone_scripted_scheduler(
        runner,
        high_env,
        epochs=args_cli.bc_epochs,
        learning_rate=args_cli.bc_learning_rate,
        batch_size=args_cli.bc_batch_size,
        ppo_anchor_coefficient=args_cli.ppo_bc_anchor_coef,
    )
    if bc_metrics is not None:
        metadata["behavior_cloning"] = bc_metrics
        torch.save(
            {
                "model_state_dict": runner.alg.actor_critic.state_dict(),
                "optimizer_state_dict": runner.alg.optimizer.state_dict(),
                "iter": 0,
                "infos": {"behavior_cloning": bc_metrics},
            },
            log_dir / "model_bc.pt",
        )
        print(f"HIGH_LEVEL_BC={json.dumps(bc_metrics, sort_keys=True)}", flush=True)
        (log_dir / "run_metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
    if args_cli.resume_checkpoint is not None:
        resume_checkpoint = args_cli.resume_checkpoint.resolve()
        if not resume_checkpoint.is_file():
            raise FileNotFoundError(resume_checkpoint)
        runner.load(str(resume_checkpoint))
        metadata["resume_checkpoint"] = str(resume_checkpoint)
        metadata["resume_iteration"] = runner.current_learning_iteration
    print(
        f"HIGH_LEVEL_TIMING,stage=runner_init,seconds={time.perf_counter() - runner_start:.6f}",
        flush=True,
    )
    runner.add_git_repo_to_log(__file__)
    print("HIGH_LEVEL_TIMING,stage=learn_begin", flush=True)
    remaining_iterations = high_agent_cfg.max_iterations - runner.current_learning_iteration
    if remaining_iterations <= 0:
        raise ValueError(
            "max-iterations must be greater than the resumed checkpoint iteration"
        )
    runner.learn(
        num_learning_iterations=remaining_iterations,
        init_at_random_ep_len=False,
    )
    metadata["evidence_status"] = "PASS"
    metadata["final_iteration"] = runner.current_learning_iteration
    (log_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    high_env.close()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    finally:
        simulation_app.close()
