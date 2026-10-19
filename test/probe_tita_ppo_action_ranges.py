"""VALIDATION_SIM: signed PPO action distributions and matched range interventions."""

import argparse
from contextlib import ExitStack
from datetime import datetime
import json
from pathlib import Path
import pickle
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lab/ddt_lab/scripts/flash_sac"))
from runtime import setup_imports, sha256

JOINTS = [f"joint_{side}_leg_{i}" for side in ("left", "right") for i in range(1, 5)]
PROFILES = [
    ("stand", 0.0, 0.0), ("forward_04", .4, 0.0), ("backward_04", -.4, 0.0),
    ("forward_08", .8, 0.0), ("backward_08", -.8, 0.0),
    ("forward_10", 1.0, 0.0), ("backward_10", -1.0, 0.0),
    ("yaw_left", 0.0, 1.5), ("yaw_right", 0.0, -1.5),
    ("forward_turn", .8, 1.5), ("backward_turn", -.8, -1.5),
    ("walk_stop", .8, 0.0), ("turn_stop", 0.0, 1.5),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--envs_per_profile", type=int, default=16)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 43, 44])
    parser.add_argument("--candidates", type=Path)
    parser.add_argument("--include_gaussian", action="store_true", help="Also execute the saved PPO Gaussian policy")
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--tag", default="tita_ppo_action_distribution")
    args = parser.parse_args()
    if min(args.envs_per_profile, args.steps) < 1:
        parser.error("envs_per_profile and steps must be positive")
    checkpoint = args.checkpoint.resolve()
    checkpoint_hash = sha256(checkpoint)
    cases = [{"name": "baseline", "raw_lower": None, "raw_upper": None}]
    if args.include_gaussian:
        cases.append({"name": "gaussian_baseline", "raw_lower": None, "raw_upper": None,
                      "execution_mode": "gaussian"})
    if args.candidates:
        cases.extend(json.loads(args.candidates.read_text())["candidates"])
    if len({c["name"] for c in cases}) != len(cases):
        parser.error("candidate names must be unique and cannot be baseline")
    setup_imports(False)
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    evidence = ROOT / "docs/exp" / now.strftime("%Y-%m-%d")
    evidence.mkdir(parents=True, exist_ok=True)
    prefix = evidence / f"{args.tag}_{now.strftime('%H%M%S')}"
    result_path = prefix.with_suffix(".json")
    record = {
        "execution_domain": "VALIDATION_SIM", "evidence_status": "BLOCKED",
        "policy_checkpoint": str(checkpoint), "policy_checkpoint_sha256": checkpoint_hash,
        "environment_config_sha256": sha256(checkpoint.parent / "env.pkl"),
        "args": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
        "profiles": [{"name": n, "target_vx": x, "target_yaw": yaw} for n, x, yaw in PROFILES],
        "joint_order": JOINTS, "cases": [],
        "protocol": {"actor_inputs": 33, "velocity_estimator": False,
                     "executed_actions": "deterministic mean, optionally capped; optional Gaussian baseline",
                     "gaussian_samples": "counterfactual except in explicitly named gaussian_baseline",
                     "first_episode_only": True, "observation_corruption": False,
                     "pushes": False, "remaining_randomization": "saved startup physics and seeded resets",
                     "command_ramp": "saved native ramp; walk_stop/turn_stop targets become zero after 10 s"},
    }
    resources = ExitStack()
    try:
        import numpy as np
        import torch
        if args.device.startswith("cuda") and not torch.cuda.is_available():
            raise RuntimeError("VALIDATION_SIM needs host GPU access")
        from isaaclab.app import AppLauncher
        app = AppLauncher(headless=True, device=args.device).app
        resources.callback(app.close)
        import ddt_lab.tasks  # noqa: F401
        from isaaclab.envs import ManagerBasedRLEnv
        from rsl_rl.modules import ActorCritic

        class CaptureEnv(ManagerBasedRLEnv):
            def __init__(self, *positional, **kwargs):
                self.capturing, self.terminal = False, None
                super().__init__(*positional, **kwargs)
                self.joint_ids = [self.scene["robot"].joint_names.index(n) for n in JOINTS]

            def snapshot(self, ids=None):
                data = self.scene["robot"].data
                values = {"velocity": data.root_lin_vel_b[:, :2], "yaw": data.root_ang_vel_b[:, 2],
                          "upright": -data.projected_gravity_b[:, 2], "position": data.root_pos_w[:, :2],
                          "joint_pos": data.joint_pos[:, self.joint_ids],
                          "joint_vel": data.joint_vel[:, self.joint_ids],
                          "computed_torque": data.computed_torque[:, self.joint_ids],
                          "applied_torque": data.applied_torque[:, self.joint_ids]}
                return {k: (v if ids is None else v[ids]).clone() for k, v in values.items()}

            def step(self, actions):
                self.capturing, self.terminal = True, None
                try:
                    return super().step(actions)
                finally:
                    self.capturing = False

            def _reset_idx(self, ids):
                if self.capturing:
                    self.terminal = (ids.clone(), self.snapshot(ids))
                return super()._reset_idx(ids)

        with (checkpoint.parent / "env.pkl").open("rb") as stream:
            cfg = pickle.load(stream)
        cfg.scene.num_envs = len(PROFILES) * args.envs_per_profile
        cfg.seed, cfg.sim.device = args.seeds[0], args.device
        cfg.observations.policy.enable_corruption = False
        cfg.observations.estimator_target = None
        cfg.events.push_robot = None
        env = CaptureEnv(cfg=cfg)
        resources.callback(env.close)
        robot = env.scene["robot"]
        device = torch.device(env.device)
        obs, _ = env.reset(seed=args.seeds[0])
        assert obs["policy"].shape[-1] == 33 and obs["critic"].shape[-1] == 36
        config = json.loads((checkpoint.parent / "agent.json").read_text())["policy"]
        assert config.pop("class_name") == "ActorCritic"
        policy = ActorCritic(obs, {"policy": ["policy"], "critic": ["critic"]}, 8, **config).to(device)
        policy.load_state_dict(torch.load(checkpoint, map_location=device, weights_only=False)["model_state_dict"])
        policy.eval()
        sigma = policy.std.detach()
        assert sigma.shape == (8,) and torch.isfinite(sigma).all() and (sigma > 0).all()
        ids = env.joint_ids
        scales = torch.tensor([.25, .25, .25, 5, .25, .25, .25, 5], device=device)
        offsets = robot.data.default_joint_pos[0, ids].clone()
        offsets[[3, 7]] = robot.data.default_joint_vel[0, [ids[3], ids[7]]]
        soft = robot.data.soft_joint_pos_limits[0, ids].clone()
        record["native_action_scale"] = scales.tolist()
        record["native_action_offset"] = offsets.tolist()
        record["joint_pos_limits_rad"] = robot.data.joint_pos_limits[0, ids].tolist()
        record["soft_joint_pos_limits_rad"] = soft.tolist()
        record["joint_vel_limits_rad_s"] = robot.data.joint_vel_limits[0, ids].tolist()
        record["soft_joint_vel_limits_rad_s"] = robot.data.soft_joint_vel_limits[0, ids].tolist()
        record["policy_sigma_raw"] = sigma.tolist()
        record["actuator_limits"] = {n: {"effort": a.effort_limit[0].tolist(),
                                          "velocity": a.velocity_limit[0].tolist()} for n, a in robot.actuators.items()}
        for case in cases[1:]:
            if case["raw_lower"] is None:
                continue
            low, high = np.asarray(case["raw_lower"]), np.asarray(case["raw_upper"])
            if low.shape != (8,) or high.shape != (8,) or not np.isfinite([low, high]).all():
                raise ValueError("Candidate bounds must be finite eight-vectors")
            if not ((low < 0) & (high > 0)).all():
                raise ValueError("Candidate bounds must contain zero")
            leg_ids = [0, 1, 2, 4, 5, 6]
            targets_low = offsets.cpu().numpy() + scales.cpu().numpy() * low
            targets_high = offsets.cpu().numpy() + scales.cpu().numpy() * high
            position_limits = (robot.data.joint_pos_limits[0, ids] if case.get("position_limit") == "hard" else soft).cpu().numpy()
            if (targets_low[leg_ids] < position_limits[leg_ids, 0] - 1e-5).any() or (targets_high[leg_ids] > position_limits[leg_ids, 1] + 1e-5).any():
                raise ValueError("Leg candidate target bounds exceed their declared measured position limits")
            wheel_limits = robot.data.soft_joint_vel_limits[0, [ids[3], ids[7]]].cpu().numpy()
            if (np.abs(targets_low[[3, 7]]) > wheel_limits + 1e-5).any() or (np.abs(targets_high[[3, 7]]) > wheel_limits + 1e-5).any():
                raise ValueError("Wheel candidate targets must stay within measured actuator velocity limits")
        command = env.command_manager.get_term("base_velocity")
        group = torch.arange(len(PROFILES), device=device).repeat_interleave(args.envs_per_profile)
        targets = torch.tensor([[x, 0, yaw] for _, x, yaw in PROFILES], device=device)[group]
        stop = torch.tensor([n.endswith("stop") for n, _, _ in PROFILES], device=device)[group]
        initial_reference = {}
        record["evidence_status"] = "SUSPICIOUS"
        for seed in args.seeds:
            for case in cases:
                obs, _ = env.reset(seed=seed)
                initial = torch.cat([robot.data.root_state_w, robot.data.joint_pos, robot.data.joint_vel, obs["policy"],
                                     *[v for a in robot.actuators.values() for v in (a.stiffness, a.damping)]], dim=-1).cpu().numpy()
                if seed not in initial_reference:
                    initial_reference[seed] = initial.copy()
                difference = float(np.abs(initial - initial_reference[seed]).max())
                if difference > 1e-5:
                    raise RuntimeError("Paired initial state differs")
                low = torch.tensor(case["raw_lower"], device=device) if case["raw_lower"] is not None else None
                high = torch.tensor(case["raw_upper"], device=device) if case["raw_upper"] is not None else None
                generator = torch.Generator(device=device).manual_seed(seed + 200000)
                alive = torch.ones(env.num_envs, dtype=torch.bool, device=device)
                fell = torch.zeros_like(alive)
                life = torch.zeros(env.num_envs, dtype=torch.long, device=device)
                sums = torch.zeros((env.num_envs, 3), device=device)
                histories = {key: [] for key in ("mean_action", "gaussian_sample", "applied_action", "command", "joint_pos", "joint_vel", "applied_torque", "torque_clipped", "metrics")}
                for step in range(1, args.steps + 1):
                    if not app.is_running():
                        raise RuntimeError("Simulator closed during probe")
                    requested = targets.clone()
                    if (step - 1) * env.step_dt >= 10:
                        requested[stop] = 0
                    command.vel_command_b[:] = requested
                    command.is_standing_env[:] = requested.abs().sum(-1) == 0
                    command.is_heading_env[:] = False
                    command.time_left.fill_(1e6)
                    desired = command.command.clone()
                    with torch.inference_mode():
                        mean = policy.act_inference(obs)
                        sampled = mean + sigma * torch.randn(mean.shape, device=device, generator=generator)
                        original = sampled if case.get("execution_mode") == "gaussian" else mean
                        action = original if low is None else original.clamp(min=low, max=high)
                        if not torch.isfinite(action).all() or not torch.isfinite(sampled).all():
                            raise RuntimeError("Non-finite policy output")
                    obs, _, terminated, truncated, _ = env.step(action)
                    physical = env.snapshot()
                    if env.terminal is not None:
                        selected, terminal = env.terminal
                        for key in physical:
                            physical[key][selected] = terminal[key]
                    error_xy = (desired[:, :2] - physical["velocity"]).square().sum(-1)
                    error_yaw = (desired[:, 2] - physical["yaw"]).square()
                    upright_gain = physical["upright"].clamp(0, .7) / .7
                    metrics = torch.stack([torch.exp(-error_xy / .25) * upright_gain,
                                           torch.exp(-error_yaw / .25) * upright_gain,
                                           ((original - action).abs() > 1e-6).float().mean(-1)], dim=-1)
                    if not torch.isfinite(metrics).all():
                        raise RuntimeError("Non-finite physical metric")
                    values = {"mean_action": mean, "gaussian_sample": sampled, "applied_action": action,
                              "command": desired, "joint_pos": physical["joint_pos"], "joint_vel": physical["joint_vel"],
                              "applied_torque": physical["applied_torque"],
                              "torque_clipped": ((physical["computed_torque"] - physical["applied_torque"]).abs() > 1e-3).float(),
                              "metrics": metrics}
                    for key, value in values.items():
                        masked = value.clone()
                        masked[~alive] = float("nan")
                        histories[key].append(masked.cpu().numpy())
                    sums += metrics * alive[:, None]
                    life += alive.long()
                    fell |= alive & terminated
                    alive &= ~(terminated | truncated)
                    if step % 250 == 0:
                        print(f"[VALIDATION_SIM] {seed}/{case['name']} step={step} alive={int(alive.sum())}", flush=True)
                    if not alive.any():
                        break
                history_path = Path(str(prefix) + f"_{seed}_{case['name']}.npz")
                np.savez_compressed(history_path, **{k: np.stack(v) for k, v in histories.items()},
                                    profile_index=group.cpu().numpy(), dt=env.step_dt)
                counts, failures, total = life.cpu().numpy(), fell.cpu().numpy(), sums.cpu().numpy()
                entry = {"seed": seed, **case, "initial_max_difference": difference,
                         "life_steps": counts.tolist(), "fell": failures.tolist(), "per_env_sums": total.tolist(),
                         "metrics": ["tracking_xy", "tracking_yaw", "cap_affected"],
                         "history": str(history_path.relative_to(ROOT)), "groups": []}
                for index, (name, _, _) in enumerate(PROFILES):
                    sl = slice(index * args.envs_per_profile, (index + 1) * args.envs_per_profile)
                    entry["groups"].append({"profile": name, "mean_survival_s": float(counts[sl].mean() * env.step_dt),
                                            "survival_at_horizon": float(((counts[sl] >= args.steps) & ~failures[sl]).mean()),
                                            "tracking_xy_fixed_horizon": float(total[sl, 0].mean() / args.steps),
                                            "tracking_yaw_fixed_horizon": float(total[sl, 1].mean() / args.steps)})
                record["cases"].append(entry)
                result_path.write_text(json.dumps(record, indent=2, allow_nan=False) + "\n")
                print(f"[VALIDATION_SIM] Completed {seed}/{case['name']}: survival={counts.mean()*env.step_dt:.3f}s", flush=True)
        if sha256(checkpoint) != checkpoint_hash:
            raise RuntimeError("Pinned checkpoint changed during probe")
        record.update(evidence_status="PASS", detail="All signed-distribution/range cases completed with finite metrics and paired initial states.")
    except BaseException as error:
        record["evidence_status"] = "FAIL" if record["cases"] else "BLOCKED"
        record["detail"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        result_path.write_text(json.dumps(record, indent=2, allow_nan=False) + "\n")
        print(f"[VALIDATION_SIM] {record['evidence_status']}: {result_path}", flush=True)
        resources.close()


if __name__ == "__main__":
    main()
