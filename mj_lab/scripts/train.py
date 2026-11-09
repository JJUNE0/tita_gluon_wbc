"""TRAINING_SIM: train TITA with mjlab physics and the existing FlashSAC learner."""

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

from mj_lab.flash_sac import TitaFlashSACEnv, runtime
from mj_lab.checkpoint import save_checkpoint
from mj_lab.robots.tita.common.robot_cfg import REPO_ROOT
from mj_lab.robots.tita.flat_env_cfg import TitaFlatEnvCfg
from mj_lab.robots.tita.roll_pitch_height.flat_env_roll_pitch_height_cfg import TitaFlatRollPitchHeightEnvCfg
from mj_lab.robots.tita.sit_stand.sit_stand_env_cfg import TitaSitStandEnvCfg
from mj_lab.robots.tita.sit_stand.height_only_env_cfg import TitaHeightOnlyEnvCfg
from mj_lab.robots.tita.walk.walk_env_cfg import TitaWalkEnvCfg
from mj_lab.robots.tita.walk.inline_env_cfg import TitaInlineEnvCfg
from mj_lab.robots.tita.stand_one_leg.stand_one_leg_env_cfg import TitaStandOneLegEnvCfg
from mj_lab.robots.tita.stand_one_leg.stand_one_leg_reference_env_cfg import (
    TitaStandOneLegReferenceEnvCfg, TitaStandOneLegRightReferenceEnvCfg,
)
from mj_lab.robots.tita.stand_one_leg.stand_one_leg_anchor_env_cfg import (
    TitaStandOneLegAnchorEnvCfg, TitaStandOneLegRightAnchorEnvCfg,
)
from mj_lab.robots.tita.stand_one_leg.support_command_env_cfg import TitaSupportCommandEnvCfg, TitaSupportVelocityEnvCfg
from train import build_parser  # Shared CLI/defaults; importing does not start Isaac.


def main():
    parser = build_parser()
    parser.description = __doc__
    parser.set_defaults(task="inline")
    parser.add_argument('--standing-height-only', action='store_true',
                        help='Fresh sit_stand run: keep 0.25–0.5 m goals and base/knee contact termination throughout')
    args = parser.parse_args()
    tasks = {"flat": TitaFlatEnvCfg, "flat_roll_pitch_height": TitaFlatRollPitchHeightEnvCfg,
             "sit_stand": TitaSitStandEnvCfg, "height_only": TitaHeightOnlyEnvCfg,
             "walk": TitaWalkEnvCfg, "inline": TitaInlineEnvCfg,
             "stand_one_leg": TitaStandOneLegEnvCfg,
             "stand_one_leg_reference": TitaStandOneLegReferenceEnvCfg,
             "stand_one_leg_reference_right": TitaStandOneLegRightReferenceEnvCfg,
             "stand_one_leg_anchor_left": TitaStandOneLegAnchorEnvCfg,
             "stand_one_leg_anchor_right": TitaStandOneLegRightAnchorEnvCfg,
             "support_command": TitaSupportCommandEnvCfg, "support_velocity": TitaSupportVelocityEnvCfg}
    if args.task not in tasks:
        parser.error("--task must be " + ", ".join(tasks))
    if not args.headless:
        parser.error("Use headless training and mj_lab.scripts.play --video for preview")
    if args.standing_height_only and (args.task != 'sit_stand' or args.resume or args.warm_start):
        parser.error('--standing-height-only requires --task sit_stand and a fresh run')
    runtime.validate_training_args(args)
    runtime.setup_imports(args.compile)
    import numpy as np
    import torch
    from mjlab.envs import ManagerBasedRlEnv
    from flash_rl.agents.flashSAC.agent import FlashSACConfig
    from video_logging import CheckpointVideoLogger

    source, metadata = runtime.read_checkpoint(args.resume or args.warm_start) if args.resume or args.warm_start else (None, None)
    if args.resume and (metadata.get("backend") != "mjlab" or metadata["task"] != args.task):
        parser.error("--resume requires a mjlab checkpoint of the selected task; use --warm_start for compatible weights")
    start_step = metadata["step"] if args.resume else 0
    if args.steps <= start_step:
        parser.error("--steps must exceed the checkpoint step")
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    now = datetime.now()
    run_id = now.strftime("tita_mjlab_%H%M%S_%f")
    evidence = REPO_ROOT / "docs/exp" / now.strftime("%Y-%m-%d")
    evidence.mkdir(parents=True, exist_ok=True)
    output = REPO_ROOT / "mj_lab/logs/flash_sac" / run_id
    output.mkdir(parents=True)
    runtime.write_json(evidence / f"{run_id}_args.json", {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()})
    if args.resume:
        with (source / "env.pkl").open("rb") as stream:
            cfg = pickle.load(stream)
        cfg.scene.num_envs = args.num_envs
    else:
        cfg = tasks[args.task](args.num_envs)
        if args.standing_height_only:
            cfg.curriculum_transition_step = None
    cfg.seed = args.seed
    # Old sit_stand checkpoints lack this schedule and retain their saved MDP.
    curriculum = cfg.set_training_step if "curriculum_transition_step" in vars(cfg) else None
    if curriculum:
        curriculum(start_step)
    resources = ExitStack()
    step, updates, last_saved = start_step, 0, -1
    checkpoint, checkpoint_hash = None, "N/A"
    status, detail = "BLOCKED", "Initialization incomplete"
    run = videos = writer = env = None
    try:
        raw = ManagerBasedRlEnv(cfg, device=args.device)
        resources.callback(raw.close)
        action_mapping = runtime.action_mapping_kwargs(metadata) if metadata else {}
        # A new task may deliberately widen targets when loading source weights.
        # Checkpoints record the mapping actually used, including this override.
        for name in ("action_gain_negative", "action_gain_positive"):
            if hasattr(cfg, name):
                action_mapping[name] = getattr(cfg, name)
        env = TitaFlashSACEnv(raw, **action_mapping)
        if metadata:
            runtime.check_dimensions(env, metadata)
        runtime.select_buffer_device(args, env)
        learner_cfg = runtime.create_agent_config(args)
        if args.resume:
            learner_cfg = replace(FlashSACConfig(**metadata["agent"]),
                device_type=args.device, buffer_device_type=args.buffer_device,
                buffer_max_length=args.buffer_size, buffer_min_length=args.min_buffer,
                sample_batch_size=args.batch_size, use_compile=args.compile, use_amp=args.amp)
        elif args.warm_start:
            learner_cfg = replace(learner_cfg, load_optimizer=False, load_reward_normalizer=False)
        agent = runtime.make_agent(env, learner_cfg)
        if metadata:
            agent.load(str(source))
        if args.logger == "wandb":
            import wandb
            run = wandb.init(project=args.wandb_project, entity=args.wandb_entity,
                name=args.run_name or run_id, mode=args.wandb_mode, id=args.wandb_run_id,
                resume="allow" if args.wandb_run_id else None, dir=str(evidence),
                config={**vars(args), "backend": "mjlab", "actor_obs_dim": env.actor_obs_dim,
                        "critic_obs_dim": env.critic_obs_dim, "algorithm": "FlashSAC"})
            resources.callback(run.finish)
            if args.video_interval:
                videos = CheckpointVideoLogger(run, wandb, evidence / f"{run_id}_videos", args.device,
                                               args.video_length, player_script=Path(__file__).with_name("play.py"))
                resources.callback(videos.close)
        elif args.logger == "tensorboard":
            from torch.utils.tensorboard import SummaryWriter
            writer = SummaryWriter(str(evidence / f"{run_id}_tensorboard"))
            resources.callback(writer.close)
        stream = resources.enter_context((evidence / f"{run_id}_metrics.jsonl").open("w"))
        obs = env.reset()
        returns = torch.zeros(env.num_envs, device=env.device)
        lengths = torch.zeros_like(returns)
        episode_returns, episode_lengths = deque(maxlen=100), deque(maxlen=100)
        budget, latest, started = 0.0, {}, time.perf_counter()
        status = "SUSPICIOUS"
        for step in range(start_step + 1, args.steps + 1):
            if curriculum and curriculum(step, raw):
                # Termination semantics change at the boundary: keep learned
                # weights/optimizers, discard old replay and pending n-step data.
                agent._replay_buffer.reset()
                obs = env.reset()
                returns.zero_()
                lengths.zero_()
                episode_returns.clear()
                episode_lengths.clear()
                if agent.reward_normalizer is not None:
                    agent.reward_normalizer.G_r.zero_()
                latest.clear()
                budget = 0.
                change = {"execution_domain": "TRAINING_SIM", "step": step,
                          "stage": cfg.curriculum_stage, "height_range": list(cfg.commands["base_pose"].height_range),
                          "contact_termination": cfg.curriculum_stage == 1, "replay_reset": True}
                runtime.write_json(evidence / f"{run_id}_curriculum_{step}.json", change)
                print(f"[TRAINING_SIM] Curriculum: {json.dumps(change)}", flush=True)
            actions = (agent.sample_actions(step, {"next_observation": obs}, training=True)
                       if metadata or updates or agent.can_start_training() else torch.rand(env.num_envs, 8, device=env.device) * 2 - 1)
            actions = torch.as_tensor(actions, device=env.device).clamp(-1, 1)
            next_obs, replay_next, reward, terminated, truncated, info = env.step(actions)
            agent.process_transition({"observation": obs, "action": actions, "next_observation": replay_next,
                                      "reward": reward, "terminated": terminated, "truncated": truncated})
            obs = next_obs
            returns += reward
            lengths += 1
            done = terminated | truncated
            if done.any():
                episode_returns.extend(returns[done].tolist())
                episode_lengths.extend(lengths[done].tolist())
                returns[done], lengths[done] = 0, 0
            if agent.can_start_training():
                budget += args.updates_per_step
                while budget + 1e-9 >= 1:
                    latest.update(agent.update())
                    if not all(math.isfinite(v) for v in latest.values()):
                        raise RuntimeError("Non-finite FlashSAC learning metrics")
                    updates += 1
                    budget -= 1
            if step % args.log_every == 0 or step == args.steps:
                metrics = {"execution_domain": "TRAINING_SIM", "step": step, "updates": updates,
                           "reward_mean": reward.mean().item(), "terminated_count": int(terminated.sum()),
                           "truncated_count": int(truncated.sum()),
                           "transitions_per_second": (step - start_step) * env.num_envs / (time.perf_counter() - started), **latest}
                if curriculum:
                    metrics.update(curriculum_stage=cfg.curriculum_stage,
                                   curriculum_contact_termination=int(cfg.curriculum_stage == 1),
                                   curriculum_height_min=cfg.commands["base_pose"].height_range[0])
                if episode_returns:
                    metrics.update(episode_return_mean=float(np.mean(episode_returns)), episode_length_mean=float(np.mean(episode_lengths)))
                for key, value in info.get("log", {}).items():
                    if isinstance(value, (int, float)) or torch.is_tensor(value) and value.numel() == 1:
                        if math.isfinite(float(value)):
                            metrics["env/" + key] = float(value)
                stream.write(json.dumps(metrics, allow_nan=False) + "\n")
                stream.flush()
                if run:
                    run.log(metrics)
                if writer:
                    for key, value in metrics.items():
                        if isinstance(value, (int, float)):
                            writer.add_scalar(key, value, step)
                if videos:
                    videos.poll()
                print(f"[TRAINING_SIM] mjlab step={step} updates={updates} reward={metrics['reward_mean']:.5f}", flush=True)
            video_due = videos is not None and step % args.video_interval == 0
            if step % args.save_every == 0 or video_due:
                checkpoint, meta = save_checkpoint(env, agent, cfg, output, args.task, step)
                checkpoint_hash, last_saved = meta["actor_sha256"], step
                if video_due:
                    videos.submit(checkpoint, meta)
        if last_saved != step:
            checkpoint, meta = save_checkpoint(env, agent, cfg, output, args.task, step)
            checkpoint_hash = meta["actor_sha256"]
        status = "PASS" if updates else "SUSPICIOUS"
        detail = f"Completed {step - start_step} vector steps and {updates} finite learner updates; locomotion quality not evaluated."
    except BaseException as error:
        status, detail = "FAIL", f"{type(error).__name__}: {error}"
        raise
    finally:
        try:
            if videos:
                videos.close()
                if videos.failures:
                    status, detail = "SUSPICIOUS", detail + f" Video failures: {videos.failures}."
            result = {"execution_domain": "TRAINING_SIM", "evidence_status": status, "detail": detail,
                      "step": step, "updates": updates, "checkpoint": str(checkpoint), "checkpoint_sha256": checkpoint_hash,
                      "backend": "mjlab", "wandb_url": run.url if run else None}
            runtime.write_json(evidence / f"{run_id}_result.json", result)
            (evidence / f"{run_id}_summary.md").write_text(
                f"# TITA mjlab FlashSAC\n\nExecution Domain: TRAINING_SIM\n\nEvidence Status: {status}\n\n"
                f"Policy Checkpoint SHA256: {checkpoint_hash}\n\n{detail}\n\nCheckpoint: `{checkpoint}`\n")
            if run:
                run.summary.update(result)
            print(f"[TRAINING_SIM] {status}: {detail}\nCheckpoint: {checkpoint}", flush=True)
        finally:
            resources.close()


if __name__ == "__main__":
    main()
