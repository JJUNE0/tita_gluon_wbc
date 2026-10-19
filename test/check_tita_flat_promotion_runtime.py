"""TRAINING_SIM: compare real resolved configs and step the promoted flat task.

Run with the Isaac Lab interpreter, --headless, and --output beneath docs/exp/.
No trained policy or hardware commands are used.
"""

import argparse
import json
from pathlib import Path
import pickle
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lab/ddt_lab/scripts/flash_sac"))
from runtime import setup_imports

setup_imports(False)
from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, required=True)
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()
app = AppLauncher(args).app

try:
    import gymnasium as gym
    import torch
    import ddt_lab.tasks  # noqa: F401
    from isaaclab_tasks.utils import load_cfg_from_registry, parse_env_cfg
    from ddt_lab.tasks.manager_based.locomotion.robots.tita.real2sim import base_env_cfg

    task = "DDT-Velocity-Flat-Tita-v0"
    reference = "DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObsW0-v0"
    cfg = parse_env_cfg(task, device="cpu", num_envs=2)
    expected = parse_env_cfg(reference, device="cpu", num_envs=2)
    checks = {"resolved_config_matches_original_experiment": cfg.to_dict() == expected.to_dict()}
    old_module = "ddt_lab.tasks.manager_based.locomotion.robots.tita.my_flat_env_cfg"
    checks["legacy_pickle_imports"] = all(
        pickle.loads(f"c{old_module}\n{name}\n.".encode()) is getattr(base_env_cfg, name)
        for name in ("MyTitaFlatEnvCfg", "MyTitaFlatEnvCfg_PLAY", "SceneCfg", "ObservationsCfg", "MyEventCfg")
    )
    historical = parse_env_cfg("DDT-Velocity-Flat-Tita-My-v0", device="cpu", num_envs=2)
    checks["historical_my_task_preserved"] = type(historical) is base_env_cfg.MyTitaFlatEnvCfg
    load_cfg_from_registry(task, "flash_sac_cfg_entry_point").apply_env_cfg(cfg)
    env = gym.make(task, cfg=cfg)
    try:
        raw = env.unwrapped
        env.reset()
        checks["policy_35_critic_39_actions_8"] = (
            raw.observation_manager.group_obs_dim["policy"] == (35,)
            and raw.observation_manager.group_obs_dim["critic"] == (39,)
            and raw.action_manager.total_action_dim == 8
        )
        checks["plain_leg_actions"] = type(raw.action_manager.get_term("joint_pos_0")).__name__ == "JointPositionAction"
        finite = True
        for _ in range(10):
            observations, rewards, *_ = env.step(torch.zeros((2, 8), device=raw.device))
            finite &= bool(torch.isfinite(observations["policy"]).all()
                           and torch.isfinite(observations["critic"]).all()
                           and torch.isfinite(rewards).all())
        checks["finite_10_zero_action_steps"] = finite
        result = {
            "execution_domain": "TRAINING_SIM",
            "policy_checkpoint_sha256": "N/A: config smoke check without policy",
            "evidence_status": "PASS" if all(checks.values()) else "FAIL",
            "checks": checks,
            "dimensions": raw.observation_manager.group_obs_dim,
            "policy_terms": raw.observation_manager.active_terms["policy"],
            "critic_terms": raw.observation_manager.active_terms["critic"],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2), flush=True)
        if not all(checks.values()):
            raise AssertionError(checks)
    finally:
        env.close()
finally:
    app.close()
