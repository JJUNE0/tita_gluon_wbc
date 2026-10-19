"""VALIDATION_SIM: matched first-episode noise and action-bound probes.

This diagnostic keeps the saved actor, 33 policy inputs, joint scales and
actuator limits fixed. It never applies actions outside [-1, 1]. Records live
under docs/exp; this test harness does not modify training or log to W&B.
"""

import argparse
from contextlib import ExitStack
from datetime import datetime
import json
from pathlib import Path
import pickle
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lab/ddt_lab/scripts/flash_sac"))
from runtime import read_checkpoint, setup_imports, sha256


CASES = (
    ("deterministic", "none", 1.0, 1.0),
    ("independent_noise", "independent", 1.0, 1.0),
    ("repeated_noise", "repeated", 1.0, 1.0),
    ("leg_cap_075", "none", 0.75, 1.0),
    ("wheel_cap_075", "none", 1.0, 0.75),
    ("all_cap_050", "none", 0.5, 0.5),
)
JOINTS = [f"joint_{side}_leg_{number}" for side in ("left", "right") for number in range(1, 5)]
STAT_NAMES = (
    "xy_error", "tracking_raw", "upright", "noise_mse", "action_delta_mse",
    "sigma_leg", "sigma_wheel", "near_bound_leg", "near_bound_wheel",
    "cap_affected_leg", "cap_affected_wheel", "torque_clip_leg", "torque_clip_wheel",
    "abs_action_leg", "abs_action_wheel", "tanh_gain_leg", "tanh_gain_wheel",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--num_envs", type=int, default=96)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 43])
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--tag", default="tita_flash_sac_noise_bounds")
    args = parser.parse_args()
    if args.num_envs < 3 or args.num_envs % 3 or args.steps < 1:
        parser.error("num_envs must be a positive multiple of 3; steps must be positive")
    path, metadata = read_checkpoint(args.checkpoint)
    setup_imports(False)
    now = datetime.now()
    evidence = ROOT / "docs/exp" / now.strftime("%Y-%m-%d")
    evidence.mkdir(parents=True, exist_ok=True)
    prefix = evidence / f"{args.tag}_{now.strftime('%H%M%S')}"
    result_path = prefix.with_suffix(".json")
    result = {
        "execution_domain": "VALIDATION_SIM", "evidence_status": "BLOCKED",
        "checkpoint": str(path), "policy_checkpoint_sha256": metadata["actor_sha256"],
        "args": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
        "controls": {
            "actor_fixed": True, "velocity_estimator": "excluded, actor remains 33 dimensional",
            "policy_corruption": False, "random_pushes": False,
            "remaining_randomization": "saved startup physics and paired seeded reset randomization",
            "command_targets_x": [0.0, 0.6, -0.6], "ramp_rate": "unchanged",
            "joint_scales_and_actuator_limits": "unchanged",
            "first_episode_only": True, "actions_within_minus1_plus1": True,
        },
        "cases": [],
    }
    resources = ExitStack()
    try:
        import numpy as np
        import torch
        if not torch.cuda.is_available() and args.device.startswith("cuda"):
            raise RuntimeError("VALIDATION_SIM needs host GPU access")
        from isaaclab.app import AppLauncher
        app = AppLauncher(headless=True, device=args.device).app
        resources.callback(app.close)
        import ddt_lab.tasks  # noqa: F401
        from isaaclab.envs import ManagerBasedRLEnv
        from flash_rl.agents.flashSAC.network import FlashSACActor

        class CaptureEnv(ManagerBasedRLEnv):
            def __init__(self, *positional, **kwargs):
                self.capturing = False
                self.terminal_measurement = None
                super().__init__(*positional, **kwargs)
                self.probe_joint_ids = [self.scene["robot"].joint_names.index(name) for name in JOINTS]

            def snapshot(self, ids=None):
                data = self.scene["robot"].data
                values = {
                    "velocity": data.root_lin_vel_b[:, :2],
                    "upright": -data.projected_gravity_b[:, 2],
                    "joint_pos": data.joint_pos[:, self.probe_joint_ids],
                    "computed_torque": data.computed_torque[:, self.probe_joint_ids],
                    "applied_torque": data.applied_torque[:, self.probe_joint_ids],
                }
                return {key: (value if ids is None else value[ids]).clone() for key, value in values.items()}

            def step(self, actions):
                self.terminal_measurement = None
                self.capturing = True
                try:
                    return super().step(actions)
                finally:
                    self.capturing = False

            def _reset_idx(self, ids):
                if self.capturing:
                    self.terminal_measurement = (ids.clone(), self.snapshot(ids))
                return super()._reset_idx(ids)

        with (path / "env.pkl").open("rb") as stream:
            cfg = pickle.load(stream)
        cfg.scene.num_envs = args.num_envs
        cfg.sim.device = args.device
        cfg.seed = args.seeds[0]
        cfg.observations.estimator_target = None
        cfg.observations.policy.enable_corruption = False
        cfg.events.push_robot = None
        env = CaptureEnv(cfg=cfg)
        resources.callback(env.close)
        device = torch.device(env.device)
        actor_cfg = metadata["agent"]
        actor = FlashSACActor(
            actor_cfg["actor_num_blocks"], metadata["actor_obs_dim"],
            actor_cfg["actor_hidden_dim"], metadata["action_dim"],
        ).to(device)
        weights = torch.load(path / "actor.pt", map_location=device, weights_only=True)["network_state_dict"]
        while weights and all(key.startswith("_orig_mod.") for key in weights):
            torch.nn.modules.utils.consume_prefix_in_state_dict_if_present(weights, "_orig_mod.")
        actor.load_state_dict(weights)
        actor.eval()
        leg = [0, 1, 2, 4, 5, 6]
        wheel = [3, 7]
        targets = torch.tensor([0.0, 0.6, -0.6], device=device).repeat_interleave(args.num_envs // 3)
        command = env.command_manager.get_term("base_velocity")
        n_values = torch.arange(1, actor_cfg["actor_noise_zeta_max"] + 1, device=device, dtype=torch.float32)
        pmf = n_values.pow(-actor_cfg["actor_noise_zeta_mu"])
        cdf = torch.cumsum(pmf / pmf.sum(), dim=0)
        reference_initial = {}
        samples = []

        for seed in args.seeds:
            for case_name, noise_mode, leg_cap, wheel_cap in CASES:
                obs, _ = env.reset(seed=seed)
                signature = torch.cat([
                    env.scene["robot"].data.root_state_w,
                    env.scene["robot"].data.joint_pos, env.scene["robot"].data.joint_vel,
                    obs["policy"],
                    *[value for actuator in env.scene["robot"].actuators.values()
                      for value in (actuator.stiffness, actuator.damping)],
                ], dim=-1).detach().cpu().numpy()
                if seed not in reference_initial:
                    reference_initial[seed] = signature.copy()
                difference = float(np.max(np.abs(signature - reference_initial[seed])))
                if difference > 1e-5:
                    raise RuntimeError(f"Paired initial state differs for {seed}/{case_name}: {difference}")
                generator = torch.Generator(device=device).manual_seed(seed + 100000)
                noise = torch.zeros((args.num_envs, 8), device=device)
                count, repeat_n = 0, 1
                alive = torch.ones(args.num_envs, device=device, dtype=torch.bool)
                life = torch.zeros(args.num_envs, device=device, dtype=torch.long)
                fell = torch.zeros_like(alive)
                sums = torch.zeros((args.num_envs, len(STAT_NAMES)), device=device)
                per_joint_near = torch.zeros((args.num_envs, 8), device=device)
                per_joint_sigma = torch.zeros_like(per_joint_near)
                previous = torch.zeros_like(noise)
                histories = []
                for step in range(1, args.steps + 1):
                    if not app.is_running():
                        raise RuntimeError("Simulator stopped during comparison")
                    # Hold fixed targets while retaining the saved command's ramp.
                    command.vel_command_b.zero_()
                    command.vel_command_b[:, 0] = targets
                    command.is_standing_env[:] = targets == 0
                    command.time_left.fill_(1e6)
                    desired = command.command[:, :2].clone()
                    with torch.inference_mode():
                        mean, std = actor.get_mean_and_std(obs["policy"], training=False)
                        nominal = mean.tanh()
                        # Consume identical candidate-noise/CDF streams for both
                        # modes; the repetition rule alone changes what is used.
                        candidate = torch.randn(noise.shape, device=device, generator=generator)
                        u = torch.rand((), device=device, generator=generator)
                        new_n = int(torch.argmax((u < cdf).to(torch.int32)).item()) + 1
                        if noise_mode == "independent":
                            noise = candidate
                        elif noise_mode == "repeated" and (count == 0 or count >= repeat_n):
                            noise, repeat_n, count = candidate, new_n, 0
                        pre_tanh = mean if noise_mode == "none" else mean + std * noise
                        sampled = pre_tanh.tanh()
                        count += 1
                        actions = sampled.clone()
                        actions[:, leg] = actions[:, leg].clamp(-leg_cap, leg_cap)
                        actions[:, wheel] = actions[:, wheel].clamp(-wheel_cap, wheel_cap)
                        if not torch.isfinite(actions).all() or torch.any(actions.abs() > 1.0):
                            raise RuntimeError("Non-finite or out-of-range diagnostic action")
                    obs, reward, terminated, truncated, _ = env.step(actions)
                    physical = env.snapshot()
                    if env.terminal_measurement is not None:
                        ids, terminal = env.terminal_measurement
                        for key in physical:
                            physical[key][ids] = terminal[key]
                    error = torch.linalg.vector_norm(desired - physical["velocity"], dim=-1)
                    upright = physical["upright"]
                    tracking = torch.exp(-error.square() / .25) * upright.clamp(0, .7) / .7
                    torque_clipped = (physical["computed_torque"] - physical["applied_torque"]).abs() > 1e-3
                    near = sampled.abs() >= .95
                    affected = (sampled - actions).abs() > 1e-6
                    gain = 1 - nominal.square()
                    stats = torch.stack([
                        error, tracking, upright,
                        (sampled - nominal).square().mean(-1),
                        (actions - previous).square().mean(-1),
                        std[:, leg].mean(-1), std[:, wheel].mean(-1),
                        near[:, leg].float().mean(-1), near[:, wheel].float().mean(-1),
                        affected[:, leg].float().mean(-1), affected[:, wheel].float().mean(-1),
                        torque_clipped[:, leg].float().mean(-1), torque_clipped[:, wheel].float().mean(-1),
                        actions[:, leg].abs().mean(-1), actions[:, wheel].abs().mean(-1),
                        gain[:, leg].mean(-1), gain[:, wheel].mean(-1),
                    ], dim=-1)
                    if not torch.isfinite(stats).all():
                        raise RuntimeError("Non-finite physical/policy diagnostic metric")
                    sums += stats * alive[:, None]
                    per_joint_near += near.float() * alive[:, None]
                    per_joint_sigma += std * alive[:, None]
                    life += alive.long()
                    history = stats[:, :5].clone()
                    history[~alive] = float("nan")
                    histories.append(history.cpu().numpy())
                    if step % 10 == 0:
                        selected = alive.nonzero(as_tuple=True)[0]
                        if selected.numel():
                            samples.append(np.concatenate([
                                np.full((len(selected), 3), [seed, list(CASES).index((case_name, noise_mode, leg_cap, wheel_cap)), step]),
                                selected.cpu().numpy()[:, None],
                                mean[selected].cpu().numpy(), std[selected].cpu().numpy(),
                                sampled[selected].cpu().numpy(),
                            ], axis=1))
                    fell |= alive & terminated
                    alive &= ~(terminated | truncated)
                    previous = actions
                    if step % 200 == 0:
                        print(f"[VALIDATION_SIM] seed={seed} case={case_name} step={step} first-episode alive={int(alive.sum())}", flush=True)
                    if not alive.any():
                        break

                life_np = life.cpu().numpy()
                averages = (sums / life[:, None].clamp_min(1)).cpu().numpy()
                near_np = (per_joint_near / life[:, None].clamp_min(1)).cpu().numpy()
                sigma_np = (per_joint_sigma / life[:, None].clamp_min(1)).cpu().numpy()
                case_result = {
                    "seed": seed, "case": case_name, "noise_mode": noise_mode,
                    "leg_cap": leg_cap, "wheel_cap": wheel_cap,
                    "initial_state_max_difference": difference,
                    "steps_executed": step, "horizon_s": args.steps * env.step_dt,
                    "life_steps": life_np.tolist(), "fell": fell.cpu().numpy().tolist(),
                    "per_env_stats": averages.tolist(), "stat_names": list(STAT_NAMES),
                    "per_env_joint_near_fraction": near_np.tolist(),
                    "per_env_joint_mean_sigma": sigma_np.tolist(),
                    "command_targets_x": targets.cpu().numpy().tolist(), "commands": [],
                }
                for group, velocity in enumerate((0.0, .6, -.6)):
                    select = slice(group * (args.num_envs//3), (group+1) * (args.num_envs//3))
                    group_result = {
                        "target_vx": velocity, "trials": args.num_envs//3,
                        "restricted_mean_survival_s": float(life_np[select].mean()*env.step_dt),
                        "survival_at_5s": float((life_np[select] >= round(5/env.step_dt)).mean()),
                        "survival_at_20s": float((life_np[select] >= round(20/env.step_dt)).mean()),
                        "mean_stats": dict(zip(STAT_NAMES, averages[select].mean(0).tolist())),
                        "joint_near_fraction": dict(zip(JOINTS, near_np[select].mean(0).tolist())),
                    }
                    case_result["commands"].append(group_result)
                history_path = Path(str(prefix) + f"_{seed}_{case_name}_history.npz")
                np.savez_compressed(history_path, history=np.stack(histories), targets=targets.cpu().numpy(),
                                    fields=np.array(STAT_NAMES[:5]), dt=env.step_dt)
                case_result["history_file"] = str(history_path.relative_to(ROOT))
                result["cases"].append(case_result)
                result_path.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
                print(f"[VALIDATION_SIM] completed seed={seed} case={case_name}: "
                      f"mean survival={life_np.mean()*env.step_dt:.3f}s", flush=True)
        if samples:
            np.savez_compressed(Path(str(prefix) + "_policy_samples.npz"),
                                samples=np.concatenate(samples),
                                columns=np.array(["seed", "case_index", "step", "env_index"] +
                                                 [f"{field}_{i}" for field in ("mu", "sigma", "action") for i in range(8)]))
        if sha256(path / "actor.pt") != metadata["actor_sha256"]:
            raise RuntimeError("Pinned checkpoint changed during evaluation")
        result["evidence_status"] = "PASS"
        result["detail"] = "All paired first-episode conditions completed with finite metrics; inference effects only."
    except Exception as error:
        result["detail"] = f"{type(error).__name__}: {error}"
        result["evidence_status"] = "FAIL" if result["cases"] else "BLOCKED"
        raise
    finally:
        result_path.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
        print(f"[VALIDATION_SIM] {result['evidence_status']}: {result_path}", flush=True)
        resources.close()


if __name__ == "__main__":
    main()
