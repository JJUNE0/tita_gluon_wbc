"""VALIDATION_SIM: Run deterministic inference from a TITA FlashSAC checkpoint."""

import argparse
from dataclasses import replace
from datetime import datetime
import math
import pickle

from runtime import REPO_ROOT, action_mapping_kwargs, check_dimensions, load_default_runner_cfg, make_agent, read_checkpoint, setup_imports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--num_envs", type=int, default=16)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()
    if min(args.num_envs, args.steps) < 1:
        parser.error("num_envs and steps must be positive")
    setup_imports(False)
    path, metadata = read_checkpoint(args.checkpoint)
    app = env = None
    completed, reward_sum, terminated_count, truncated_count = 0, 0.0, 0, 0
    status, detail = "BLOCKED", "Simulator initialization did not complete."
    now = datetime.now()
    evidence_dir = REPO_ROOT / "docs" / "exp" / now.strftime("%Y-%m-%d")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    try:
        import torch
        if args.device.startswith("cuda") and not torch.cuda.is_available():
            raise RuntimeError("CUDA is unavailable in this process; launch from an Isaac Lab environment with GPU access")
        from isaaclab.app import AppLauncher
        app = AppLauncher(headless=args.headless, device=args.device).app
        import ddt_lab.tasks  # noqa: F401
        from flash_rl.agents.flashSAC.agent import FlashSACConfig
        from env_adapter import TitaFlashSACEnv, make_flash_sac_env_class

        with (path / "env.pkl").open("rb") as stream:
            cfg = pickle.load(stream)
        cfg.scene.num_envs = args.num_envs
        cfg.sim.device = args.device
        load_default_runner_cfg().apply_env_cfg(cfg)
        # Use the saved training environment, including its configured randomization.
        raw_env = make_flash_sac_env_class()(cfg=cfg)
        try:
            env = TitaFlashSACEnv(raw_env, **action_mapping_kwargs(metadata))
        except Exception:
            raw_env.close()
            raise
        check_dimensions(env, metadata)
        learner_cfg = replace(
            FlashSACConfig(**metadata["agent"]), device_type=args.device,
            buffer_device_type="cpu", buffer_max_length=max(args.num_envs, 1),
            buffer_min_length=1, sample_batch_size=1, use_compile=False, use_amp=False,
            load_optimizer=False, load_reward_normalizer=False,
        )
        agent = make_agent(env, learner_cfg)
        agent.load(str(path))
        obs = env.reset()
        status = "SUSPICIOUS"
        for step in range(1, args.steps + 1):
            if not app.is_running():
                break
            actions = torch.as_tensor(
                agent.sample_actions(step, {"next_observation": obs}, training=False), device=env.device
            )
            obs, _, reward, terminated, truncated, _ = env.step(actions)
            value = reward.mean().item()
            if not math.isfinite(value):
                raise RuntimeError("non-finite validation reward")
            reward_sum += value
            terminated_count += int(terminated.sum().item())
            truncated_count += int(truncated.sum().item())
            completed = step
        status = "PASS" if completed == args.steps else "SUSPICIOUS"
        detail = "Deterministic simulator rollout completed; locomotion quality requires separate evaluation."
        print(f"[VALIDATION_SIM] {status}: steps={completed}, reward_mean={reward_sum / max(completed, 1):.5f}")
    except Exception as error:
        status = "FAIL" if env else "BLOCKED"
        detail = f"{type(error).__name__}: {error}"
        raise
    finally:
        summary = (
            f"# TITA FlashSAC validation\n\nExecution Domain: VALIDATION_SIM\n\nEvidence Status: {status}\n\n"
            f"Policy Checkpoint SHA256 (actor.pt): {metadata['actor_sha256']}\n\n"
            f"Checkpoint: `{path}`\n\nObserved behavior / log summary: {detail}\n\n"
            f"Steps: {completed}; mean reward: {reward_sum / max(completed, 1):.6f}; "
            f"terminations: {terminated_count}; timeouts: {truncated_count}.\n"
        )
        report = evidence_dir / now.strftime("tita_flash_sac_play_%H%M%S_%f_summary.md")
        report.write_text(summary)
        print(f"[VALIDATION_SIM] Evidence: {report}")
        try:
            if env:
                env.close()
        finally:
            if app:
                app.close()


if __name__ == "__main__":
    main()
