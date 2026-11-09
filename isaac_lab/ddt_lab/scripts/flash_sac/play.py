"""VALIDATION_SIM: Run deterministic inference from a TITA FlashSAC checkpoint."""

import argparse
from dataclasses import replace
from datetime import datetime
from functools import lru_cache
import math
import pickle
from pathlib import Path

from runtime import REPO_ROOT, action_mapping_kwargs, check_dimensions, load_default_runner_cfg, make_agent, read_checkpoint, setup_imports, sha256, write_json


def read_velocity_sample(env):
    """Read emitted commands and actual root velocity in the same body frame."""
    sample = {
        "command": env.command_manager.get_command("base_velocity")[0, :2].detach().cpu().tolist(),
        "actual": env.scene["robot"].data.root_lin_vel_b[0, :2].detach().cpu().tolist(),
    }
    if not all(math.isfinite(value) for values in sample.values() for value in values):
        raise RuntimeError("Non-finite velocity in video overlay")
    return sample


@lru_cache(maxsize=1)
def _velocity_font():
    from PIL import ImageFont

    try:
        return ImageFont.truetype("DejaVuSansMono.ttf", 18)
    except OSError:
        return ImageFont.load_default()


def draw_velocity_overlay(frame, sample):
    """Add readable vx/vy telemetry without modifying the renderer's frame."""
    import numpy as np
    from PIL import Image, ImageDraw

    picture = Image.fromarray(frame)
    draw = ImageDraw.Draw(picture, "RGBA")
    draw.rounded_rectangle((10, 10, 330, 112), radius=8, fill=(10, 15, 25, 220))
    font = _velocity_font()
    draw.text((20, 16), "BODY FRAME | m/s", font=font, fill=(255, 255, 255, 255))
    draw.text((20, 39), "          vx       vy", font=font, fill=(190, 200, 215, 255))
    for label, values, y, color in (
        ("CMD", sample["command"], 61, (255, 210, 90, 255)),
        ("ACT", sample["actual"], 83, (100, 230, 255, 255)),
    ):
        draw.text((20, y), f"{label}  {values[0]:+8.3f} {values[1]:+8.3f}", font=font, fill=color)
    return np.asarray(picture)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--num_envs", type=int, default=16)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--video", type=Path, help="Record a single-env MP4 to this path")
    parser.add_argument("--video_result", type=Path, help="Machine-readable video evidence JSON")
    args = parser.parse_args()
    if min(args.num_envs, args.steps) < 1:
        parser.error("num_envs and steps must be positive")
    if args.video and args.num_envs != 1:
        parser.error("--video requires --num_envs 1")
    if args.video_result and not args.video:
        parser.error("--video_result requires --video")
    setup_imports(False)
    selected = Path(args.checkpoint).expanduser().resolve()
    path, metadata = read_checkpoint(selected.parent if selected.is_file() else selected)
    import sys
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    from sim2sim.checkpoint_store import register_checkpoint
    registered = register_checkpoint(path, metadata)
    print(f"[DESKTOP_DRY_RUN] Checkpoint registered: {registered['sim2sim']}")
    app = env = video_writer = None
    frames, fps = 0, 0.0
    velocity_samples = []
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
        app = AppLauncher(headless=args.headless, device=args.device, enable_cameras=bool(args.video)).app
        import ddt_lab.tasks  # noqa: F401
        from flash_rl.agents.flashSAC.agent import FlashSACConfig
        from env_adapter import TitaFlashSACEnv, make_flash_sac_env_class

        with (path / "env.pkl").open("rb") as stream:
            cfg = pickle.load(stream)
        cfg.scene.num_envs = args.num_envs
        cfg.sim.device = args.device
        load_default_runner_cfg().apply_env_cfg(cfg)
        if args.video:
            cfg.viewer.resolution = (640, 480)
            cfg.viewer.origin_type = "asset_root"
            cfg.viewer.asset_name = "robot"
            cfg.viewer.env_index = 0
            cfg.viewer.eye = (1.5, 1.5, 1.0)
            cfg.viewer.lookat = (0.0, 0.0, 0.0)
            cfg.sim.render_interval = cfg.decimation
        # Use the saved training environment, including its configured randomization.
        render_kwargs = {"render_mode": "rgb_array"} if args.video else {}
        raw_env = make_flash_sac_env_class()(cfg=cfg, **render_kwargs)
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
        if args.video:
            import imageio.v2 as imageio
            args.video.parent.mkdir(parents=True, exist_ok=True)
            fps = 1.0 / raw_env.step_dt
            video_writer = imageio.get_writer(str(args.video), fps=fps, codec="libx264",
                                             pixelformat="yuv420p", quality=7)
        status = "SUSPICIOUS"
        for step in range(1, args.steps + 1):
            if not app.is_running():
                break
            actions = torch.as_tensor(
                agent.sample_actions(step, {"next_observation": obs}, training=False), device=env.device
            )
            obs, _, reward, terminated, truncated, _ = env.step(actions)
            if video_writer is not None:
                frame = raw_env.render()
                if frame is None or frame.ndim != 3 or frame.shape[2] != 3:
                    raise RuntimeError("Renderer did not return an RGB frame")
                sample = read_velocity_sample(raw_env)
                video_writer.append_data(draw_velocity_overlay(frame, sample))
                velocity_samples.append({"frame": frames, **sample})
                frames += 1
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
        try:
            if video_writer is not None:
                video_writer.close()
            if args.video:
                result_path = args.video_result or args.video.with_suffix(".json")
                result_path.parent.mkdir(parents=True, exist_ok=True)
                write_json(result_path, {
                    "execution_domain": "VALIDATION_SIM", "evidence_status": status,
                    "checkpoint": str(path), "checkpoint_sha256": metadata["actor_sha256"],
                    "checkpoint_step": metadata["step"], "video": str(args.video.resolve()),
                    "video_sha256": sha256(args.video) if args.video.is_file() else None,
                    "frames": frames, "fps": fps, "detail": detail,
                    "velocity_overlay": {
                        "enabled": True, "frame": "body", "units": "m/s", "axes": ["vx", "vy"],
                        "samples": velocity_samples,
                    },
                })
            summary = (
                f"# TITA FlashSAC validation\n\nExecution Domain: VALIDATION_SIM\n\nEvidence Status: {status}\n\n"
                f"Policy Checkpoint SHA256 (actor.pt): {metadata['actor_sha256']}\n\n"
                f"Checkpoint: `{path}`\n\nObserved behavior / log summary: {detail}\n\n"
                f"Steps: {completed}; mean reward: {reward_sum / max(completed, 1):.6f}; "
                f"terminations: {terminated_count}; timeouts: {truncated_count}.\n\n"
                f"Video: `{args.video}`; frames: {frames}; fps: {fps}.\n"
            )
            report = evidence_dir / now.strftime("tita_flash_sac_play_%H%M%S_%f_summary.md")
            report.write_text(summary)
            print(f"[VALIDATION_SIM] Evidence: {report}")
        finally:
            try:
                if env:
                    env.close()
            finally:
                if app:
                    app.close()


if __name__ == "__main__":
    main()
