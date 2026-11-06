"""VALIDATION_SIM: deterministic mjlab checkpoint playback and vx/vy video."""

import argparse
from dataclasses import replace
from datetime import datetime
import math
import os
from pathlib import Path
import pickle
import sys

os.environ.setdefault("MUJOCO_GL", "egl")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mj_lab.flash_sac import TitaFlashSACEnv, runtime
from mj_lab.robots.tita.robot_cfg import REPO_ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--num_envs", type=int, default=1)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--headless", action="store_true", default=True)
    parser.add_argument("--video", type=Path)
    parser.add_argument("--video_result", type=Path)
    parser.add_argument("--command", nargs=3, type=float, metavar=("VX", "VY", "WZ"))
    parser.add_argument("--pose-command", nargs=3, type=float, metavar=("ROLL", "PITCH", "HEIGHT"),
                        help="Fixed roll/pitch targets in radians and base_link height in meters")
    parser.add_argument("--support-mode", type=int, choices=(0, 1, 2),
                        help="Fixed support goal: 0 left, 1 right, 2 both")
    args = parser.parse_args()
    if min(args.num_envs, args.steps) < 1 or args.video and args.num_envs != 1:
        parser.error("Positive sizes are required; --video requires --num_envs 1")
    if args.video_result and not args.video:
        parser.error("--video_result requires --video")
    path, metadata = runtime.read_checkpoint(args.checkpoint)
    if metadata.get("backend") != "mjlab":
        parser.error("This player requires a native mjlab checkpoint")
    runtime.setup_imports(False)
    import torch
    from mjlab.envs import ManagerBasedRlEnv
    from flash_rl.agents.flashSAC.agent import FlashSACConfig
    from play import draw_velocity_overlay

    with (path / "env.pkl").open("rb") as stream:
        cfg = pickle.load(stream)
    cfg.scene.num_envs = args.num_envs
    if args.pose_command is not None:
        if "base_pose" not in cfg.commands:
            parser.error("This checkpoint has no roll/pitch/height command")
        pose = cfg.commands["base_pose"]
        for key, value in zip(("roll_range", "pitch_range", "height_range"), args.pose_command):
            if not math.isfinite(value) or not getattr(pose, key)[0] <= value <= getattr(pose, key)[1]:
                parser.error(f"{key} outside saved command range")
    if args.support_mode is not None and "support" not in cfg.commands:
        parser.error("This checkpoint has no support-mode command")
    support_preview = ("support" in cfg.commands and args.support_mode is None and args.num_envs == 1
                       and not getattr(cfg.commands["support"], "episode_fixed", False))
    inline_preview = metadata["task"] == "inline" and args.command is None and args.num_envs == 1
    preview_commands = None
    if inline_preview:
        v = cfg.commands["base_velocity"]
        preview_commands = [(0., 0., 0.), (min(.5, v.lin_vel_x[1]), 0., 0.),
                            (max(-.5, v.lin_vel_x[0]), 0., 0.), (0., 0., min(.5, v.ang_vel_z[1]))]
        # A one-environment preview cannot represent a half/half cohort. Show
        # stop, forward, backward and turn explicitly over each ten seconds.
        v.rel_straight_envs = v.rel_standing_envs = 0.
        v.lin_vel_x = v.lin_vel_y = v.ang_vel_z = (0., 0.)
    if args.command:
        v = cfg.commands["base_velocity"]
        for key, value in zip(("lin_vel_x", "lin_vel_y", "ang_vel_z"), args.command):
            if not getattr(v, key)[0] <= value <= getattr(v, key)[1]:
                parser.error(f"{key} outside saved command range")
            setattr(v, key, (value, value))
        v.rel_standing_envs = 0.0
        v.rel_straight_envs = 0.0
    env = raw = writer = None
    frames, samples, reward_sum, terminated_count = 0, [], 0.0, 0
    status, detail = "BLOCKED", "Initialization incomplete"
    evidence = REPO_ROOT / "docs/exp" / datetime.now().strftime("%Y-%m-%d")
    evidence.mkdir(parents=True, exist_ok=True)
    result_path = args.video_result or evidence / datetime.now().strftime("tita_mjlab_play_%H%M%S_%f.json")
    try:
        raw = ManagerBasedRlEnv(cfg, device=args.device, render_mode="rgb_array" if args.video else None)
        env = TitaFlashSACEnv(raw, **runtime.action_mapping_kwargs(metadata))
        runtime.check_dimensions(env, metadata)
        learner = replace(FlashSACConfig(**metadata["agent"]), device_type=args.device, buffer_device_type="cpu",
            buffer_max_length=max(1, args.num_envs), buffer_min_length=1, sample_batch_size=1,
            use_compile=False, use_amp=False, load_optimizer=False, load_reward_normalizer=False)
        agent = runtime.make_agent(env, learner)
        agent.load(str(path))
        obs = env.reset()
        if args.video:
            import imageio.v2 as imageio
            import numpy as np
            from PIL import Image, ImageDraw
            args.video.parent.mkdir(parents=True, exist_ok=True)
            writer = imageio.get_writer(str(args.video), fps=1 / raw.step_dt, codec="libx264", pixelformat="yuv420p")
        for step in range(1, args.steps + 1):
            active_support = None
            episode_step = int(raw.episode_length_buf[0])
            if args.pose_command is not None:
                pose = raw.command_manager.get_term("base_pose")
                pose.target[:] = pose.target.new_tensor(args.pose_command)
                pose.time_left[:] = 1e9
            if "support" in cfg.commands:
                support = raw.command_manager.get_term("support")
                selected = args.support_mode
                if support_preview:
                    selected = (2, 0, 2, 1)[int(((step-1)*raw.step_dt) % 10. // 2.5)]
                if selected is not None:
                    changed = bool((support.mode != selected).any())
                    support.set_mode(selected)
                    if changed:
                        # get_observations() returns a per-tick cache. Refresh
                        # it so this action sees the externally changed goal.
                        obs = env._pack(raw.observation_manager.compute(update_history=True))
                active_support = int(support.mode[0])
            if inline_preview:
                t = ((step - 1) * raw.step_dt) % 10.
                mode = 0
                if 1. <= t < 5.:
                    mode = 1
                elif 5. <= t < 8.:
                    mode = 2
                elif 8. <= t < 9.:
                    mode = 3
                v = raw.command_manager.get_term("base_velocity")
                v.target[:] = v.target.new_tensor(preview_commands[mode])
                v.time_left[:] = 1e9
            actions = torch.as_tensor(agent.sample_actions(step, {"next_observation": obs}, training=False), device=env.device)
            obs, _, reward, terminated, _, _ = env.step(actions)
            reward_sum += reward.mean().item()
            terminated_count += int(terminated.sum())
            if writer:
                frame = raw.render()
                if frame is None or frame.ndim != 3:
                    raise RuntimeError("Renderer did not return an RGB frame")
                sample = {"command": raw.command_manager.get_command("base_velocity")[0, :2].tolist(),
                          "actual": raw.scene["robot"].data.root_link_lin_vel_b[0, :2].tolist(),
                          "command_yaw": float(raw.command_manager.get_command("base_velocity")[0, 2]),
                          "actual_yaw": float(raw.scene["robot"].data.root_link_ang_vel_b[0, 2])}
                if metadata["task"] == "inline":
                    gait = raw.command_manager.get_term("gait")
                    sample.update(gait_enabled=bool(gait.command[0, 0]), gait_phase=float(gait.phase[0]),
                                  command_yaw=float(raw.command_manager.get_command("base_velocity")[0, 2]))
                frame = draw_velocity_overlay(frame, sample)
                if active_support is not None:
                    sample["support_mode"] = active_support
                    sample["episode_step"] = episode_step
                    canvas = Image.fromarray(frame)
                    draw = ImageDraw.Draw(canvas)
                    draw.rectangle((8, 120, 400, 164), fill=(0, 0, 0))
                    label = f"SUPPORT {active_support}: {('LEFT', 'RIGHT', 'BOTH')[active_support]} | EP {episode_step*raw.step_dt:.1f}s"
                    draw.text((12, 124), label, fill=(255, 255, 255))
                    draw.text((12, 146), f"YAW cmd {sample['command_yaw']:+.3f} | act {sample['actual_yaw']:+.3f} rad/s",
                              fill=(255, 255, 255))
                    frame = np.asarray(canvas)
                if "base_pose" in cfg.commands:
                    from mjlab.utils.lab_api.math import euler_xyz_from_quat
                    pose = raw.command_manager.get_term("base_pose")
                    data = raw.scene["robot"].data
                    roll, pitch, _ = euler_xyz_from_quat(data.root_link_quat_w)
                    height = data.root_link_pos_w[0, 2] - raw.scene.env_origins[0, 2]
                    sample.update(pose_target=pose.target[0].tolist(),
                                  pose_command=pose.command[0].tolist(),
                                  pose_actual=[float(roll[0]), float(pitch[0]), float(height)])
                    canvas = Image.fromarray(frame)
                    draw = ImageDraw.Draw(canvas)
                    draw.rectangle((8, 170, 600, 246), fill=(0, 0, 0))
                    draw.text((12, 174), "POSE roll deg / pitch deg / base height m", fill="white")
                    for row, key in enumerate(("pose_target", "pose_command", "pose_actual")):
                        r, p, h = sample[key]
                        draw.text((12, 192+16*row),
                                  f"{key}: {math.degrees(r):+.1f} / {math.degrees(p):+.1f} / {h:.3f}", fill="white")
                    frame = np.asarray(canvas)
                writer.append_data(frame)
                samples.append({"frame": frames, **sample})
                frames += 1
        status, detail = "PASS", "Finite deterministic rollout completed; locomotion quality requires longer evaluation."
    except BaseException as error:
        status, detail = "FAIL", f"{type(error).__name__}: {error}"
        raise
    finally:
        if writer:
            writer.close()
        if raw:
            raw.close()
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result = {"execution_domain": "VALIDATION_SIM", "evidence_status": status, "detail": detail,
                  "checkpoint_sha256": metadata["actor_sha256"], "checkpoint": str(path),
                  "frames": frames, "steps": args.steps if status == "PASS" else 0, "velocity_samples": samples,
                  "reward_mean": reward_sum / args.steps, "terminated_count": terminated_count}
        runtime.write_json(result_path, result)
        (evidence / (result_path.stem + "_summary.md")).write_text(
            f"# mjlab playback\n\nExecution Domain: VALIDATION_SIM\n\nEvidence Status: {status}\n\n"
            f"Policy Checkpoint SHA256: {metadata['actor_sha256']}\n\n{detail}\n\nMetrics: `{result_path}`\n")
        print(f"[VALIDATION_SIM] {status}: {detail}\nEvidence: {result_path}")


if __name__ == "__main__":
    main()
