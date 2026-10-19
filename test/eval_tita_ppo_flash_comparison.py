"""VALIDATION_SIM: matched deterministic PPO/FlashSAC and PPO action-cap probes."""

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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ppo_checkpoint", type=Path, nargs="+", required=True)
    parser.add_argument("--sac_checkpoint", type=Path, nargs="+", required=True)
    parser.add_argument("--num_envs", type=int, default=128)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 43])
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--tag", default="tita_ppo33_flash_evaluation")
    args = parser.parse_args()
    if args.num_envs < 4 or args.num_envs % 4 or args.steps < 1:
        parser.error("num_envs must be a positive multiple of four; steps must be positive")
    paths = [read_checkpoint(path) for path in args.sac_checkpoint]
    ppo_paths = [p.resolve() for p in args.ppo_checkpoint]
    ppo_hashes = {str(p): sha256(p) for p in ppo_paths}
    setup_imports(False)
    now = datetime.now()
    evidence = ROOT / "docs/exp" / now.strftime("%Y-%m-%d")
    prefix = evidence / f"{args.tag}_{now.strftime('%H%M%S')}"
    evidence.mkdir(parents=True, exist_ok=True)
    result_path = prefix.with_suffix(".json")
    result = {
        "execution_domain": "VALIDATION_SIM", "evidence_status": "BLOCKED",
        "policy_checkpoint_sha256": {**ppo_hashes, **{str(p): m["actor_sha256"] for p, m in paths}},
        "args": {k: [str(p) for p in v] if k in ("ppo_checkpoint", "sac_checkpoint") else str(v) if isinstance(v, Path) else v
                 for k, v in vars(args).items()},
        "protocol": {"velocity_estimator": False, "actor_inputs": 33, "critic_inputs": 36,
                     "deterministic_actions": True, "first_episode_only": True,
                     "target_vx_m_s": [0.0, 0.4, 0.8, -0.8], "noise_corruption": False,
                     "random_pushes": False, "remaining_randomization": "saved physical/startup/reset randomization",
                     "command_ramp_and_joint_scales": "unchanged",
                     "primary_metrics": "first-episode survival and tracking integral divided by common horizon"},
        "cases": [],
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
        from flash_rl.agents.flashSAC.network import FlashSACActor

        class CaptureEnv(ManagerBasedRLEnv):
            def __init__(self, *positional, **kwargs):
                self.capturing = False
                self.terminal = None
                super().__init__(*positional, **kwargs)

            def snapshot(self, ids=None):
                data = self.scene["robot"].data
                values = {"velocity": data.root_lin_vel_b[:, :2], "upright": -data.projected_gravity_b[:, 2],
                          "position": data.root_pos_w[:, :2], "computed_torque": data.computed_torque,
                          "applied_torque": data.applied_torque}
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

        with (paths[0][0] / "env.pkl").open("rb") as stream:
            cfg = pickle.load(stream)
        cfg.scene.num_envs, cfg.sim.device, cfg.seed = args.num_envs, args.device, args.seeds[0]
        cfg.observations.estimator_target = None
        cfg.observations.policy.enable_corruption = False
        cfg.events.push_robot = None
        env = CaptureEnv(cfg=cfg)
        resources.callback(env.close)
        device = torch.device(env.device)
        obs, _ = env.reset(seed=args.seeds[0])
        assert obs["policy"].shape[-1] == 33 and obs["critic"].shape[-1] == 36
        policies = []
        result["ppo_checkpoints"] = []
        for ppo_path in ppo_paths:
            agent_cfg = json.loads((ppo_path.parent / "agent.json").read_text())
            policy_cfg = agent_cfg["policy"].copy()
            assert policy_cfg.pop("class_name") == "ActorCritic"
            ppo = ActorCritic(obs, {"policy": ["policy"], "critic": ["critic"]}, 8, **policy_cfg).to(device)
            saved = torch.load(ppo_path, map_location=device, weights_only=False)
            ppo.load_state_dict(saved["model_state_dict"])
            ppo.eval()
            iteration = int(saved["iter"]) + 1
            name = "ppo" if len(ppo_paths) == 1 else f"ppo_{iteration}"
            result["ppo_checkpoints"].append({"checkpoint": str(ppo_path), "policy": name,
                                             "iterations_completed": iteration, "vector_steps": iteration * 24})
            predict = lambda observation, actor=ppo: actor.act_inference(observation)
            policies.append((name, predict, "none"))
            if ppo_path == ppo_paths[-1]:
                policies += [(name + "_cap_1", predict, "all"), (name + "_wheel_cap_1", predict, "wheel")]
        for path, meta in paths:
            assert meta["actor_obs_dim"] == 33 and meta["critic_obs_dim"] == 36 and meta["action_dim"] == 8
            acfg = meta["agent"]
            actor = FlashSACActor(acfg["actor_num_blocks"], 33, acfg["actor_hidden_dim"], 8).to(device)
            weights = torch.load(path / "actor.pt", map_location=device, weights_only=True)["network_state_dict"]
            while weights and all(k.startswith("_orig_mod.") for k in weights):
                torch.nn.modules.utils.consume_prefix_in_state_dict_if_present(weights, "_orig_mod.")
            actor.load_state_dict(weights)
            actor.eval()
            policies.append((f"flash_sac_{meta['step']}",
                             lambda observation, actor=actor: actor.get_mean_and_std(observation["policy"], training=False)[0].tanh(),
                             "none"))
        targets = torch.tensor([0.0, 0.4, 0.8, -0.8], device=device).repeat_interleave(args.num_envs // 4)
        command = env.command_manager.get_term("base_velocity")
        reference = {}
        fields = ["xy_error_m_s", "tracking_raw", "upright", "abs_leg_action", "abs_wheel_action",
                  "wheel_action_outside_1", "cap_affected", "torque_clipped", "vx_m_s", "drift_m"]
        joints = [f"joint_{side}_leg_{i}" for side in ("left", "right") for i in range(1, 5)]
        fields += [f"abs_action/{joint}" for joint in joints] + [f"action_outside_1/{joint}" for joint in joints]
        for seed in args.seeds:
            for name, policy, cap in policies:
                obs, _ = env.reset(seed=seed)
                signature = torch.cat([env.scene["robot"].data.root_state_w,
                                       env.scene["robot"].data.joint_pos, env.scene["robot"].data.joint_vel,
                                       obs["policy"],
                                       *[v for act in env.scene["robot"].actuators.values() for v in (act.stiffness, act.damping)]], dim=-1).cpu().numpy()
                if seed not in reference:
                    reference[seed] = signature.copy()
                difference = float(np.max(np.abs(signature - reference[seed])))
                if difference > 1e-5:
                    raise RuntimeError(f"Unmatched initial state: {seed}/{name}/{difference}")
                alive = torch.ones(args.num_envs, dtype=torch.bool, device=device)
                fell = torch.zeros_like(alive)
                life = torch.zeros(args.num_envs, dtype=torch.long, device=device)
                sums = torch.zeros((args.num_envs, len(fields)), device=device)
                start_position = env.scene["robot"].data.root_pos_w[:, :2].clone()
                final_drift = torch.zeros(args.num_envs, device=device)
                history = []
                for step in range(1, args.steps + 1):
                    if not app.is_running():
                        raise RuntimeError("Simulator closed during evaluation")
                    command.vel_command_b.zero_()
                    command.vel_command_b[:, 0] = targets
                    command.is_standing_env[:] = targets == 0
                    command.is_heading_env[:] = False
                    command.time_left.fill_(1e6)
                    desired = command.command[:, :2].clone()
                    with torch.inference_mode():
                        original = policy(obs)
                        actions = original.clamp(-1, 1) if cap == "all" else original.clone()
                        if cap == "wheel":
                            actions[:, [3, 7]] = actions[:, [3, 7]].clamp(-1, 1)
                        if not torch.isfinite(actions).all():
                            raise RuntimeError("Non-finite policy action")
                        if name.startswith("flash_sac") and (actions.abs() > 1).any():
                            raise RuntimeError("FlashSAC raw action exceeded its configured bound")
                    obs, _, terminated, truncated, _ = env.step(actions)
                    physical = env.snapshot()
                    if env.terminal is not None:
                        ids, terminal = env.terminal
                        for k in physical:
                            physical[k][ids] = terminal[k]
                    error = torch.linalg.vector_norm(desired - physical["velocity"], dim=-1)
                    tracking = torch.exp(-error.square() / .25) * physical["upright"].clamp(0, .7) / .7
                    drift = torch.linalg.vector_norm(physical["position"] - start_position, dim=-1)
                    stats = torch.stack([error, tracking, physical["upright"],
                                         actions[:, [0, 1, 2, 4, 5, 6]].abs().mean(-1),
                                         actions[:, [3, 7]].abs().mean(-1),
                                         (actions[:, [3, 7]].abs() > 1).float().mean(-1),
                                         ((actions - original).abs() > 1e-6).float().mean(-1),
                                         ((physical["computed_torque"] - physical["applied_torque"]).abs() > 1e-3).float().mean(-1),
                                         physical["velocity"][:, 0], drift], dim=-1)
                    stats = torch.cat([stats, actions.abs(), (actions.abs() > 1).float()], dim=-1)
                    if not torch.isfinite(stats).all():
                        raise RuntimeError("Non-finite physical metric")
                    sums += stats * alive[:, None]
                    final_drift[alive] = drift[alive]
                    life += alive.long()
                    row = stats.clone()
                    row[~alive] = float("nan")
                    history.append(row.cpu().numpy())
                    fell |= alive & terminated
                    alive &= ~(terminated | truncated)
                    if step % 250 == 0:
                        print(f"[VALIDATION_SIM] {seed}/{name} step={step} alive={int(alive.sum())}", flush=True)
                    if not alive.any():
                        break
                count = life.cpu().numpy()
                totals = sums.cpu().numpy()
                fall = fell.cpu().numpy()
                case = {"seed": seed, "policy": name, "initial_max_difference": difference,
                        "life_steps": count.tolist(), "fell": fall.tolist(), "horizon_s": args.steps * env.step_dt,
                        "per_env_sums": totals.tolist(), "fields": fields,
                        "final_drift_m": final_drift.cpu().numpy().tolist(), "groups": []}
                for group, target in enumerate((0.0, 0.4, 0.8, -0.8)):
                    sl = slice(group * (args.num_envs // 4), (group + 1) * (args.num_envs // 4))
                    case["groups"].append({"target_vx": target,
                                           "restricted_mean_survival_s": float(count[sl].mean() * env.step_dt),
                                           "survival_at_horizon": float(((count[sl] >= args.steps) & ~fall[sl]).mean()),
                                           "tracking_integral_fixed_horizon": float(totals[sl, 1].mean() / args.steps),
                                           "conditional_means": dict(zip(fields, (totals[sl] / np.maximum(count[sl, None], 1)).mean(0).tolist()))})
                history_path = Path(str(prefix) + f"_{seed}_{name}.npz")
                np.savez_compressed(history_path, history=np.stack(history), fields=np.array(fields),
                                    target_vx=targets.cpu().numpy(), dt=env.step_dt)
                case["history"] = str(history_path.relative_to(ROOT))
                result["cases"].append(case)
                result_path.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
                print(f"[VALIDATION_SIM] Completed {seed}/{name}: survival={count.mean()*env.step_dt:.3f}s", flush=True)
        for path in ppo_paths:
            assert sha256(path) == ppo_hashes[str(path)]
        for path, meta in paths:
            assert sha256(path / "actor.pt") == meta["actor_sha256"]
        result.update(evidence_status="PASS", detail="Matched finite first-episode evaluations completed; training convergence attribution requires controlled training ablations.")
    except BaseException as error:
        result["evidence_status"] = "FAIL" if result["cases"] else "BLOCKED"
        result["detail"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        result_path.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
        print(f"[VALIDATION_SIM] {result['evidence_status']}: {result_path}", flush=True)
        resources.close()


if __name__ == "__main__":
    main()
