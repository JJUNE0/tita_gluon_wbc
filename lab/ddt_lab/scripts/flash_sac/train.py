"""TRAINING_SIM: Train the existing My TITA flat task with FlashSAC."""

import argparse
from collections import deque
from contextlib import ExitStack
from dataclasses import replace
from datetime import datetime
import json
import math
from pathlib import Path
import pickle
import random
import time

from runtime import (
    DEFAULT_TASK, REPO_ROOT, action_mapping_kwargs, action_mapping_metadata,
    check_dimensions, create_agent_config, make_agent,
    load_default_runner_cfg,
    read_checkpoint, save_checkpoint, select_buffer_device, setup_imports,
    validate_training_args, write_json,
)


def build_parser(defaults=None):
    defaults = defaults or load_default_runner_cfg()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", default=defaults.task)
    parser.add_argument("--num_envs", type=int, default=defaults.num_envs)
    parser.add_argument("--steps", type=int, default=defaults.steps, help="Total vector steps, including saved steps on resume")
    parser.add_argument("--seed", type=int, default=defaults.seed)
    parser.add_argument("--device", default=defaults.device)
    parser.add_argument("--headless", action="store_true", default=True)
    parser.add_argument("--gui", dest="headless", action="store_false")
    parser.add_argument("--buffer_size", type=int, default=defaults.buffer_size)
    parser.add_argument("--min_buffer", type=int, default=defaults.min_buffer)
    parser.add_argument("--batch_size", type=int, default=defaults.batch_size)
    parser.add_argument("--buffer_device", default=defaults.buffer_device, help="Replay device; automatically falls back to CPU if VRAM is insufficient")
    parser.add_argument("--updates_per_step", type=float, default=defaults.updates_per_step)
    parser.add_argument("--n_step", type=int, default=defaults.n_step)
    parser.add_argument("--compile", action=argparse.BooleanOptionalAction, default=defaults.compile)
    parser.add_argument("--amp", action=argparse.BooleanOptionalAction, default=defaults.amp, help="Enable CUDA mixed precision")
    parser.add_argument("--save_every", type=int, default=defaults.save_every)
    parser.add_argument("--log_every", type=int, default=defaults.log_every)
    parser.add_argument("--logger", choices=("console", "tensorboard", "wandb"), default=defaults.logger)
    parser.add_argument("--wandb_project", default=defaults.wandb_project)
    parser.add_argument("--wandb_entity", default=defaults.wandb_entity)
    parser.add_argument("--run_name", default=defaults.run_name)
    parser.add_argument("--wandb_mode", choices=("online", "offline", "disabled"), default=defaults.wandb_mode)
    parser.add_argument("--wandb_run_id", default=defaults.wandb_run_id, help="Continue this W&B run ID; use with --resume to continue model training")
    parser.add_argument("--resume", type=Path, help="model_N directory; replay is refilled before updates")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        load_default_runner_cfg().validate()
        validate_training_args(args)
        resume_path, resume_meta = read_checkpoint(args.resume, args.task) if args.resume else (None, None)
        if resume_meta and args.steps <= resume_meta["step"]:
            raise ValueError("steps must exceed the saved vector step")
    except ValueError as error:
        parser.error(str(error))
    setup_imports(args.compile)
    now = datetime.now()
    run_id = now.strftime("tita_flash_sac_%H%M%S_%f")
    evidence_dir = REPO_ROOT / "docs" / "exp" / now.strftime("%Y-%m-%d")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    output = REPO_ROOT / "lab" / "ddt_lab" / "logs" / "flash_sac" / run_id
    write_json(evidence_dir / f"{run_id}_args.json", {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()})
    app = env = writer = metrics_stream = wandb_run = None
    resources = ExitStack()
    step = resume_meta["step"] if resume_meta else 0
    start_step = step
    updates = 0
    checkpoint = None
    checkpoint_hash = "N/A (no checkpoint produced)"
    status = "BLOCKED"
    detail = "Simulator initialization did not complete."
    initialized = False
    try:
        if args.logger == "wandb":
            # Import the SDK before Isaac/Torch namespace modules to avoid
            # pydantic source-inspection failures during late W&B imports.
            try:
                import wandb
            except ModuleNotFoundError as error:
                if error.name != "wandb":
                    raise
                raise RuntimeError("W&B logging requires wandb in this Python environment; install it with python -m pip install wandb") from error
        import torch
        if args.device.startswith("cuda") and not torch.cuda.is_available():
            raise RuntimeError("CUDA is unavailable in this process; launch from an Isaac Lab environment with GPU access")
        from isaaclab.app import AppLauncher

        app = AppLauncher(headless=args.headless, device=args.device).app
        resources.callback(app.close)
        import numpy as np
        import ddt_lab.tasks  # noqa: F401 -- register the user's existing task, after simulator launch
        from isaaclab_tasks.utils import load_cfg_from_registry, parse_env_cfg
        from isaaclab.utils.io import dump_yaml
        from env_adapter import TitaFlashSACEnv, make_flash_sac_env_class

        runner_cfg = load_cfg_from_registry(args.task, "flash_sac_cfg_entry_point")
        random.seed(args.seed)
        np.random.seed(args.seed)
        torch.manual_seed(args.seed)
        if resume_meta:
            with (resume_path / "env.pkl").open("rb") as stream:
                cfg = pickle.load(stream)
            cfg.scene.num_envs = args.num_envs
            cfg.sim.device = args.device
        else:
            cfg = parse_env_cfg(args.task, device=args.device, num_envs=args.num_envs)
        cfg.seed = args.seed
        # The shared PPO config keeps its estimator target; FlashSAC's run copy omits it.
        runner_cfg.apply_env_cfg(cfg)
        raw_env = make_flash_sac_env_class()(cfg=cfg)
        try:
            mapping_kwargs = action_mapping_kwargs(resume_meta) if resume_meta else {
                name: getattr(runner_cfg, name) for name in ("action_gain_negative", "action_gain_positive")
            }
            env = TitaFlashSACEnv(raw_env, **mapping_kwargs)
        except Exception:
            raw_env.close()
            raise
        resources.callback(env.close)
        select_buffer_device(args, env)
        learner_cfg = create_agent_config(args, runner_cfg)
        if resume_meta:
            from flash_rl.agents.flashSAC.agent import FlashSACConfig
            check_dimensions(env, resume_meta)
            learner_cfg = replace(
                FlashSACConfig(**resume_meta["agent"]), device_type=args.device,
                buffer_device_type=args.buffer_device, buffer_max_length=args.buffer_size,
                buffer_min_length=args.min_buffer, sample_batch_size=args.batch_size,
                use_compile=args.compile, use_amp=args.amp and args.device.startswith("cuda"),
            )
            print("[TRAINING_SIM] Resume restores networks/optimizers/schedule; simulator and replay restart.", flush=True)
        agent = make_agent(env, learner_cfg)
        if resume_meta:
            agent.load(str(resume_path))
            # Discounted per-environment returns refer to old simulator episodes.
            if agent.reward_normalizer is not None:
                agent.reward_normalizer.G_r = torch.zeros(args.num_envs, device=env.device)
        obs = env.reset()
        output.mkdir(parents=True, exist_ok=False)
        dump_yaml(str(output / "env.yaml"), cfg)
        from ddt_lab.policy_interface import save_policy_interface
        save_policy_interface(raw_env, output / "policy_interface.json")
        write_json(output / "agent.json", checkpoint_config(agent))
        mapping = action_mapping_metadata(env)
        write_json(output / "action_mapping.json", mapping)
        write_json(evidence_dir / f"{run_id}_action_mapping.json", mapping)
        print(f"[TRAINING_SIM] Action mapping: {mapping}", flush=True)
        if args.logger == "tensorboard":
            from torch.utils.tensorboard import SummaryWriter
            writer = SummaryWriter(str(evidence_dir / f"{run_id}_tensorboard"))
            resources.callback(writer.close)
        elif args.logger == "wandb":
            rewards = getattr(cfg, "rewards", None)
            reward_weights = {
                name: float(term.weight) for name, term in vars(rewards).items() if hasattr(term, "weight")
            } if rewards is not None else {}
            wandb_run = wandb.init(
                project=args.wandb_project, entity=args.wandb_entity,
                name=args.run_name or run_id, dir=str(evidence_dir), mode=args.wandb_mode,
                id=args.wandb_run_id, resume="allow" if args.wandb_run_id else None,
                config={
                    **{key: str(value) if isinstance(value, Path) else value for key, value in vars(args).items()},
                    "algorithm": "FlashSAC", "execution_domain": "TRAINING_SIM",
                    "agent": checkpoint_config(agent), "reward_weights": reward_weights,
                    "actor_obs_dim": env.actor_obs_dim, "critic_obs_dim": env.critic_obs_dim,
                    "action_dim": env.action_dim, "use_velocity_estimator": runner_cfg.use_velocity_estimator,
                    **mapping,
                },
            )
            resources.callback(lambda: wandb_run.finish(exit_code=1 if status in ("FAIL", "BLOCKED") else 0))
            # Vector steps stay the chart axis even when W&B resumes a run
            # whose internal history counter is already ahead of a checkpoint.
            wandb_run.define_metric("step")
            wandb_run.define_metric("*", step_metric="step")
            wandb_info = {
                "project": args.wandb_project, "entity": args.wandb_entity,
                "id": wandb_run.id, "name": wandb_run.name,
                "url": None if getattr(wandb_run, "offline", False) else wandb_run.url,
            }
            write_json(evidence_dir / f"{run_id}_wandb.json", wandb_info)
            print(f"[TRAINING_SIM] W&B project={args.wandb_project} run_id={wandb_run.id}", flush=True)
        metrics_stream = (evidence_dir / f"{run_id}_metrics.jsonl").open("w")
        resources.callback(metrics_stream.close)
        initialized = True
        status = "SUSPICIOUS"
        episode_return = torch.zeros(env.num_envs, device=env.device)
        episode_length = torch.zeros(env.num_envs, device=env.device)
        completed_returns, completed_lengths = deque(maxlen=100), deque(maxlen=100)
        update_budget = 0.0
        latest_update = {}
        last_saved = -1
        started = time.perf_counter()
        for target_step in range(start_step + 1, args.steps + 1):
            if not app.is_running():
                break
            if resume_meta or agent.can_start_training():
                actions = torch.as_tensor(agent.sample_actions(target_step, {"next_observation": obs}, True), device=env.device)
            else:
                actions = torch.rand((env.num_envs, env.action_dim), device=env.device) * 2 - 1
            actions = actions.clamp(-1.0, 1.0)
            next_obs, replay_next, reward, terminated, truncated, info = env.step(actions)
            agent.process_transition({
                "observation": obs, "action": actions, "next_observation": replay_next,
                "reward": reward, "terminated": terminated, "truncated": truncated,
            })
            obs = next_obs
            step = target_step
            episode_return += reward
            episode_length += 1
            done = terminated | truncated
            if done.any():
                completed_returns.extend(episode_return[done].tolist())
                completed_lengths.extend(episode_length[done].tolist())
                episode_return[done] = 0
                episode_length[done] = 0
            if agent.can_start_training():
                update_budget += args.updates_per_step
                while update_budget + 1e-9 >= 1.0:
                    update = agent.update()
                    if not all(math.isfinite(value) for value in update.values()):
                        raise RuntimeError("FlashSAC produced non-finite update metrics")
                    latest_update.update(update)
                    updates += 1
                    update_budget -= 1.0
            if step % args.log_every == 0 or step == args.steps:
                metrics = {
                    "execution_domain": "TRAINING_SIM", "step": step, "updates": updates,
                    "transitions": (step - start_step) * env.num_envs,
                    "reward_mean": reward.mean().item(),
                    "terminated_count": terminated.sum().item(), "truncated_count": truncated.sum().item(),
                    "transitions_per_second": (step - start_step) * env.num_envs / max(time.perf_counter() - started, 1e-6),
                    **latest_update,
                }
                if completed_returns:
                    metrics["episode_return_mean"] = sum(completed_returns) / len(completed_returns)
                    metrics["episode_length_mean"] = sum(completed_lengths) / len(completed_lengths)
                for key, value in info.get("log", {}).items():
                    if isinstance(value, (int, float)) or (torch.is_tensor(value) and value.numel() == 1):
                        scalar = float(value)
                        if math.isfinite(scalar):
                            metrics[f"env/{key}"] = scalar
                metrics_stream.write(json.dumps(metrics, allow_nan=False) + "\n")
                metrics_stream.flush()
                if writer:
                    for key, value in metrics.items():
                        if isinstance(value, (int, float)):
                            writer.add_scalar(key, value, step)
                    writer.flush()
                if wandb_run is not None:
                    wandb_run.log(metrics)
                print(f"[TRAINING_SIM] step={step} updates={updates} reward={metrics['reward_mean']:.5f}", flush=True)
            if step % args.save_every == 0:
                checkpoint, metadata = save_checkpoint(env, agent, cfg, output, args.task, step)
                checkpoint_hash = metadata["actor_sha256"]
                last_saved = step
        if step != last_saved:
            checkpoint, metadata = save_checkpoint(env, agent, cfg, output, args.task, step)
            checkpoint_hash = metadata["actor_sha256"]
        status = "PASS" if step == args.steps and updates else "SUSPICIOUS"
        detail = "Requested finite training updates completed." if status == "PASS" else "Stopped early or replay warmup produced no learning updates."
    except Exception as error:
        status = "FAIL" if initialized else "BLOCKED"
        detail = f"{type(error).__name__}: {error}"
        raise
    finally:
        try:
            summary = (
                f"# TITA FlashSAC run\n\nExecution Domain: TRAINING_SIM\n\n"
                f"Evidence Status: {status}\n\nPolicy Checkpoint SHA256 (actor.pt): {checkpoint_hash}\n\n"
                f"Task: `{args.task}`\n\nVector steps: {start_step} -> {step}; learner updates this run: {updates}.\n\n"
                f"Observed behavior / log summary: {detail}\n\nCheckpoint: `{checkpoint}`\n\n"
                "Actor uses policy observations; critic uses its independent privileged group. "
                "PPO velocity estimator is absent. Training completion does not establish locomotion quality.\n"
            )
            (evidence_dir / f"{run_id}_summary.md").write_text(summary)
            print(f"[TRAINING_SIM] {status}: {detail}\nEvidence: {evidence_dir / (run_id + '_summary.md')}", flush=True)
            if wandb_run is not None:
                wandb_run.summary.update({
                    "evidence_status": status, "detail": detail, "vector_steps": step,
                    "updates_this_run": updates, "checkpoint": str(checkpoint) if checkpoint else None,
                    "actor_sha256": checkpoint_hash, "checkpoint_dir": str(output),
                })
        finally:
            # All callbacks run even if logging/reporting or SDK finish raises.
            resources.close()


def checkpoint_config(agent):
    from dataclasses import asdict
    return asdict(agent.cfg)


if __name__ == "__main__":
    main()
