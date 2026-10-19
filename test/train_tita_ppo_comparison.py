"""TRAINING_SIM: PPO baseline with the saved FlashSAC environment and 33 inputs."""

import argparse
from contextlib import ExitStack
from datetime import datetime
import json
import math
from pathlib import Path
import pickle
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lab/ddt_lab/scripts/flash_sac"))
from runtime import read_checkpoint, setup_imports, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference_sac", type=Path, required=True)
    parser.add_argument("--iterations", type=int, default=2000)
    parser.add_argument("--num_envs", type=int, default=4096)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--logger", choices=("tensorboard", "wandb"), default="wandb")
    parser.add_argument("--tag", default="tita_ppo33_flash_comparison")
    args = parser.parse_args()
    if min(args.iterations, args.num_envs) < 1:
        parser.error("iterations and num_envs must be positive")
    reference, reference_meta = read_checkpoint(args.reference_sac)
    setup_imports(False)
    now = datetime.now()
    evidence = ROOT / "docs/exp" / now.strftime("%Y-%m-%d")
    output = evidence / f"{args.tag}_{now.strftime('%H%M%S')}"
    output.mkdir(parents=True, exist_ok=False)
    record_path = output / "run.json"
    record = {
        "execution_domain": "TRAINING_SIM", "evidence_status": "BLOCKED",
        "reference_sac_checkpoint": str(reference),
        "reference_sac_policy_sha256": reference_meta["actor_sha256"],
        "policy_checkpoint_sha256": "N/A (not saved yet)",
        "args": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
        "velocity_estimator": False, "actor_observation_dim": 33,
        "critic_observation_dim": 36, "action_dim": 8,
        "checkpoint_manifest": [],
    }
    resources = ExitStack()
    initialized = False
    try:
        wandb_run = None
        if args.logger == "wandb":
            import wandb  # Before Torch/Isaac namespace imports.
        import numpy as np
        import torch
        if args.device.startswith("cuda") and not torch.cuda.is_available():
            raise RuntimeError("TRAINING_SIM needs host GPU access")
        from isaaclab.app import AppLauncher
        app = AppLauncher(headless=True, device=args.device).app
        resources.callback(app.close)
        import ddt_lab.tasks  # noqa: F401
        from isaaclab.envs import ManagerBasedRLEnv
        from isaaclab.utils.io import dump_yaml
        from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper
        from rsl_rl.runners import OnPolicyRunner
        from ddt_lab.tasks.manager_based.locomotion.robots.tita.agents.rsl_rl_ppo_cfg import TitaFlatPPORunnerCfg

        random.seed(args.seed)
        np.random.seed(args.seed)
        torch.manual_seed(args.seed)
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        with (reference / "env.pkl").open("rb") as stream:
            cfg = pickle.load(stream)
        cfg.scene.num_envs, cfg.sim.device, cfg.seed = args.num_envs, args.device, args.seed
        cfg.observations.estimator_target = None
        cfg.log_dir = str(output)
        agent_cfg = TitaFlatPPORunnerCfg()
        agent_cfg.seed, agent_cfg.device = args.seed, args.device
        agent_cfg.max_iterations = args.iterations
        agent_cfg.logger = "tensorboard"  # W&B gets the same explicit comparison metrics below.
        agent_cfg.save_interval = 250
        assert agent_cfg.clip_actions is None
        assert agent_cfg.policy.class_name == "ActorCritic"
        assert agent_cfg.num_steps_per_env == 24
        env = RslRlVecEnvWrapper(ManagerBasedRLEnv(cfg=cfg), clip_actions=agent_cfg.clip_actions)
        resources.callback(env.close)
        obs = env.get_observations()
        assert obs["policy"].shape == (args.num_envs, 33)
        assert obs["critic"].shape == (args.num_envs, 36)
        assert env.num_actions == 8
        dump_yaml(str(output / "env.yaml"), cfg)
        dump_yaml(str(output / "agent.yaml"), agent_cfg)
        with (output / "env.pkl").open("wb") as stream:
            pickle.dump(cfg, stream)
        config = agent_cfg.to_dict()
        (output / "agent.json").write_text(json.dumps(config, indent=2) + "\n")
        metrics = resources.enter_context((output / "metrics.jsonl").open("w", buffering=1))
        if args.logger == "wandb":
            wandb_run = wandb.init(project="tita_flat_flash_sac", name=output.name, dir=str(output),
                                   config={"algorithm": "PPO", "estimator": False,
                                           "reference_sac": str(reference), **config})
            resources.callback(wandb_run.finish)
            wandb_run.define_metric("comparison/vector_step")
            wandb_run.define_metric("comparison/*", step_metric="comparison/vector_step")
            record["wandb_url"], record["wandb_id"] = wandb_run.url, wandb_run.id

        milestones = {83, 208, 416, 833, 1250, 1667, 1875, args.iterations}

        class ComparisonRunner(OnPolicyRunner):
            def log(self, locs, *positional, **kwargs):
                super().log(locs, *positional, **kwargs)
                iteration = locs["it"] + 1
                loss = {k: float(v) for k, v in locs["loss_dict"].items()}
                if not all(math.isfinite(v) for v in loss.values()):
                    raise RuntimeError("Non-finite PPO loss")
                row = {"execution_domain": "TRAINING_SIM", "iterations_completed": iteration,
                       "vector_steps": iteration * self.num_steps_per_env,
                       "transitions": self.tot_timesteps, "loop_seconds": self.tot_time, **loss}
                if locs["rewbuffer"]:
                    row["episode_return_mean"] = float(np.mean(locs["rewbuffer"]))
                    row["episode_length_mean"] = float(np.mean(locs["lenbuffer"]))
                metrics.write(json.dumps(row, allow_nan=False) + "\n")
                if wandb_run is not None and (iteration % 25 == 0 or iteration in milestones):
                    wandb_run.log({f"comparison/{k}": v for k, v in row.items() if isinstance(v, (int, float))}
                                  | {"comparison/vector_step": row["vector_steps"]})
                if iteration in milestones:
                    self.save(str(output / f"model_{locs['it']}.pt"))

            def save(self, path, infos=None):
                super().save(path, infos)
                checkpoint = Path(path)
                iteration = self.current_learning_iteration + 1
                entry = {"checkpoint": str(checkpoint), "policy_checkpoint_sha256": sha256(checkpoint),
                         "iterations_completed": iteration, "vector_steps": iteration * self.num_steps_per_env,
                         "transitions": iteration * self.num_steps_per_env * args.num_envs}
                record["checkpoint_manifest"] = [r for r in record["checkpoint_manifest"] if r["checkpoint"] != str(checkpoint)]
                record["checkpoint_manifest"].append(entry)
                record["policy_checkpoint_sha256"] = entry["policy_checkpoint_sha256"]
                record_path.write_text(json.dumps(record, indent=2) + "\n")

        runner = ComparisonRunner(env, config, log_dir=str(output), device=args.device)
        initialized = True
        record["evidence_status"] = "SUSPICIOUS"
        record["detail"] = "Training is in progress; no convergence claim."
        record_path.write_text(json.dumps(record, indent=2) + "\n")
        print(f"[TRAINING_SIM] Comparison output: {output}", flush=True)
        started = time.monotonic()
        runner.learn(num_learning_iterations=args.iterations, init_at_random_ep_len=True)
        if runner.writer is not None:
            runner.writer.flush()
            runner.writer.close()
        record.update(evidence_status="PASS", iterations_completed=args.iterations,
                      vector_steps=args.iterations * 24, wall_seconds=time.monotonic() - started,
                      detail="Requested PPO training finished with finite losses; locomotion quality requires evaluation.")
    except BaseException as error:
        record["evidence_status"] = "FAIL" if initialized else "BLOCKED"
        record["detail"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        record_path.write_text(json.dumps(record, indent=2) + "\n")
        print(f"[TRAINING_SIM] {record['evidence_status']}: {record_path}", flush=True)
        resources.close()


if __name__ == "__main__":
    main()
