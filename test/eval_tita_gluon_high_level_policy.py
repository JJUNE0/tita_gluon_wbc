#!/usr/bin/env python3
"""Evaluate a frozen high-level hybrid PPO on held-out inspection layouts.

Execution domain: VALIDATION_SIM.  This Gate-0 evaluator intentionally keeps
the local servo position-only and leaves self-collision/CBF disabled.  It is
evidence for coordination timing, not collision-safety evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import traceback


REPO_ROOT = Path(__file__).resolve().parents[1]
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
DEFAULT_OUTPUT = (
    REPO_ROOT / "docs" / "exp" / "2026-08-14" / "high_level_trigger_ppo_heldout.json"
)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--high-checkpoint", type=Path, required=True)
parser.add_argument("--low-checkpoint", type=Path, default=DEFAULT_LOW_CHECKPOINT)
parser.add_argument("--num-envs", type=int, default=8)
parser.add_argument("--batch-episodes", type=int, default=3)
parser.add_argument("--seed", type=int, default=20260831)
parser.add_argument("--episode-length-s", type=float, default=70.0)
parser.add_argument("--graph-max-velocity-deg-s", type=float, default=60.0)
parser.add_argument("--graph-max-acceleration-deg-s2", type=float, default=180.0)
parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


import gymnasium as gym  # noqa: E402
import torch  # noqa: E402

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
CLASSICAL_SCHEDULER_CYCLE_TIME_S = 37.83


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if args_cli.num_envs <= 0 or args_cli.batch_episodes <= 0:
        raise ValueError("num-envs and batch-episodes must be positive")
    high_checkpoint = args_cli.high_checkpoint.resolve()
    low_checkpoint = args_cli.low_checkpoint.resolve()
    if not high_checkpoint.is_file():
        raise FileNotFoundError(high_checkpoint)
    if not low_checkpoint.is_file():
        raise FileNotFoundError(low_checkpoint)

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
    gym_env = gym.make(LOW_TASK_ID, cfg=low_env_cfg)
    low_env = CoRlVecEnvWrapper(gym_env, low_agent_cfg)

    try:
        low_runner = MOO_OnPolicyRunner(
            low_env, low_agent_cfg.to_dict(), log_dir=None, device=low_agent_cfg.device
        )
        low_runner.load(str(low_checkpoint), load_optimizer=False)
        low_policy = low_runner.get_inference_policy(device=low_env.unwrapped.device)
        high_env = FrozenLowLevelSequentialInspectionEnv(
            low_env,
            low_policy,
            GLUON_INSPECTION_TARGET_HUB_INDICES,
            cfg=HighLevelInspectionEnvCfg(episode_length_s=args_cli.episode_length_s),
            seed=args_cli.seed,
        )
        high_agent_cfg = TitaGluonSequentialInspectionHighLevelRunnerCfg()
        high_agent_cfg.device = str(low_env.unwrapped.device)
        high_runner = OnPolicyRunner(
            high_env,
            high_agent_cfg.to_dict(),
            log_dir=None,
            device=high_agent_cfg.device,
        )
        high_runner.load(str(high_checkpoint), load_optimizer=False)
        policy = high_runner.get_inference_policy(device=high_env.device)
        obs, _ = high_env.get_observations()

        episode_logs: list[dict[str, list[float]]] = []
        continuous_abs_sum = torch.zeros(2, device=high_env.device)
        trigger_action_counts = torch.zeros(2, dtype=torch.long, device=high_env.device)
        trigger_probability_sum = torch.zeros(2, device=high_env.device)
        trigger_phase_counts = torch.zeros(2, device=high_env.device)
        trigger_greedy_counts = torch.zeros(2, device=high_env.device)
        evaluated_action_count = 0
        max_total_steps = high_env.max_episode_length * args_cli.batch_episodes
        with torch.inference_mode():
            for _ in range(max_total_steps):
                actions = policy(obs)
                option_probabilities = high_runner.alg.actor_critic.option_distribution.probs
                continuous_abs_sum += torch.sum(torch.abs(actions[:, :2]), dim=0)
                trigger_action_counts += torch.bincount(
                    actions[:, 2].round().long(), minlength=2
                )
                phase = obs[:, -2:].bool()
                greedy_trigger = option_probabilities[:, 1] > option_probabilities[:, 0]
                for phase_index in range(2):
                    available = phase[:, phase_index]
                    trigger_probability_sum[phase_index] += option_probabilities[
                        available, 1
                    ].sum()
                    trigger_phase_counts[phase_index] += available.sum()
                    trigger_greedy_counts[phase_index] += (
                        greedy_trigger & available
                    ).sum()
                evaluated_action_count += actions.shape[0]
                obs, _, dones, extras = high_env.step(actions)
                if bool(torch.any(dones)):
                    raw_log = extras.get("log")
                    if raw_log is None:
                        raise RuntimeError("terminal high-level step did not expose metrics")
                    episode_logs.append(
                        {
                            key: value.detach().cpu().float().tolist()
                            for key, value in raw_log.items()
                        }
                    )
                    print(
                        "HIGH_LEVEL_EVAL_BATCH,domain=VALIDATION_SIM,"
                        f"batch={len(episode_logs)},"
                        f"success_rate={sum(episode_logs[-1]['task_success']) / args_cli.num_envs:.6f},"
                        f"cycle_time_mean_s={sum(episode_logs[-1]['cycle_time_s']) / args_cli.num_envs:.6f}",
                        flush=True,
                    )
                    if len(episode_logs) >= args_cli.batch_episodes:
                        break
        if len(episode_logs) != args_cli.batch_episodes:
            raise RuntimeError(
                f"collected {len(episode_logs)} batch episodes, expected {args_cli.batch_episodes}"
            )

        def flatten(key: str) -> list[float]:
            return [item for episode in episode_logs for item in episode[key]]

        successes = flatten("task_success")
        cycle_times = flatten("cycle_time_s")
        successful_times = [
            cycle_time for success, cycle_time in zip(successes, cycle_times) if success > 0.5
        ]
        success_rate = sum(successes) / len(successes)
        mean_success_time = (
            sum(successful_times) / len(successful_times) if successful_times else None
        )
        beats_scheduler = (
            success_rate == 1.0
            and mean_success_time is not None
            and mean_success_time < CLASSICAL_SCHEDULER_CYCLE_TIME_S
        )
        result = {
            "execution_domain": "VALIDATION_SIM",
            "evidence_status": "PASS" if beats_scheduler else "FAIL",
            "gate": "position-only high-level PPO versus tuned classical scheduler",
            "seed": args_cli.seed,
            "num_envs": args_cli.num_envs,
            "batch_episodes": args_cli.batch_episodes,
            "layout_count": len(successes),
            "high_checkpoint": str(high_checkpoint),
            "high_checkpoint_sha256": sha256_file(high_checkpoint),
            "low_checkpoint": str(low_checkpoint),
            "low_checkpoint_sha256": sha256_file(low_checkpoint),
            "success_rate": success_rate,
            "successful_cycle_time_mean_s": mean_success_time,
            "successful_cycle_time_values_s": successful_times,
            "classical_scheduler_cycle_time_s": CLASSICAL_SCHEDULER_CYCLE_TIME_S,
            "beats_classical_scheduler": beats_scheduler,
            "concurrent_motion_ratio_mean": sum(flatten("concurrent_ratio")) / len(successes),
            "option_rejection_count": int(sum(flatten("option_rejections"))),
            "local_abort_count": int(sum(flatten("local_aborts"))),
            "low_level_failure_count": int(sum(flatten("low_level_failure"))),
            "emergency_hold_count": int(sum(flatten("emergency_hold"))),
            "batch_timeout_count": int(sum(flatten("batch_timeout")) / args_cli.num_envs),
            "target_count_mean": sum(flatten("target_count")) / len(successes),
            "return_mean": sum(flatten("return")) / len(successes),
            "deterministic_action_abs_mean": (
                continuous_abs_sum / evaluated_action_count
            ).cpu().tolist(),
            "deterministic_trigger_action_counts_wait_trigger": (
                trigger_action_counts.cpu().tolist()
            ),
            "phase_trigger_probability_prepare_execute": (
                trigger_probability_sum / torch.clamp(trigger_phase_counts, min=1.0)
            ).cpu().tolist(),
            "phase_greedy_trigger_ratio_prepare_execute": (
                trigger_greedy_counts / torch.clamp(trigger_phase_counts, min=1.0)
            ).cpu().tolist(),
            "phase_sample_count_prepare_execute": trigger_phase_counts.cpu().tolist(),
            "position_only": True,
            "cbf_enabled": False,
            "self_collision_enabled": False,
            "raw_batch_logs": episode_logs,
        }
        args_cli.output.parent.mkdir(parents=True, exist_ok=True)
        args_cli.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        cycle_display = mean_success_time if mean_success_time is not None else math.nan
        print(
            "TITA_GLUON_HIGH_LEVEL_EVAL,domain=VALIDATION_SIM,"
            f"status={result['evidence_status']},success_rate={success_rate:.6f},"
            f"cycle_time_s={cycle_display:.6f},"
            f"classical_cycle_time_s={CLASSICAL_SCHEDULER_CYCLE_TIME_S:.6f},"
            f"overlap_ratio={result['concurrent_motion_ratio_mean']:.6f},"
            f"output={args_cli.output.resolve()}",
            flush=True,
        )
        return 0 if beats_scheduler else 2
    finally:
        low_env.close()


if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception:
        traceback.print_exc()
        raise
    finally:
        simulation_app.close()
    raise SystemExit(exit_code)
