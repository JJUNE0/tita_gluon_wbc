"""Simulator-independent FlashSAC configuration and checkpoint helpers."""

from dataclasses import asdict
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
EXTENSION_ROOT = HERE.parents[1]
REPO_ROOT = HERE.parents[3]
RUNNER_CFG_PATH = EXTENSION_ROOT / "ddt_lab/tasks/manager_based/locomotion/robots/tita/agents/flash_sac_cfg.py"


def load_default_runner_cfg():
    """Read TITA defaults without importing the task package before AppLauncher."""
    name = "_ddt_tita_flash_sac_cfg"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, RUNNER_CFG_PATH)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            del sys.modules[name]
            raise
    return sys.modules[name].TitaFlatFlashSACRunnerCfg()


DEFAULT_TASK = load_default_runner_cfg().task
LEGACY_ACTION_MAPPING = "native_isaac_action_terms_raw_clamp_minus1_plus1"
PIECEWISE_ACTION_MAPPING = "native_isaac_action_terms_piecewise_gain_v1"


def action_mapping_kwargs(metadata):
    """Restore simulator gains; old checkpoints retain their original unit gains."""
    mapping = metadata.get("action_mapping", LEGACY_ACTION_MAPPING)
    if mapping == LEGACY_ACTION_MAPPING:
        if any(name in metadata for name in ("action_gain_negative", "action_gain_positive")):
            raise ValueError("Legacy action mapping cannot contain piecewise gains")
        return {name: [1.0] * metadata["action_dim"] for name in ("action_gain_negative", "action_gain_positive")}
    if mapping != PIECEWISE_ACTION_MAPPING:
        raise ValueError(f"Unsupported checkpoint action mapping: {mapping}")
    result = {}
    for name in ("action_gain_negative", "action_gain_positive"):
        values = metadata.get(name)
        if not isinstance(values, (list, tuple)) or len(values) != metadata["action_dim"]:
            raise ValueError(f"Checkpoint {name} must match action_dim")
        if any(not isinstance(value, (int, float)) or isinstance(value, bool)
               or not math.isfinite(value) or value <= 0 for value in values):
            raise ValueError(f"Checkpoint {name} must contain positive finite gains")
        result[name] = list(values)
    return result


def action_mapping_metadata(env):
    return {
        "action_mapping": PIECEWISE_ACTION_MAPPING,
        **{name: list(getattr(env, name, [1.0] * env.action_dim))
           for name in ("action_gain_negative", "action_gain_positive")},
    }


def setup_imports(use_compile=False):
    # The upstream helpers also have unconditional @torch.compile decorators.
    if not use_compile:
        os.environ["TORCHDYNAMO_DISABLE"] = "1"
    for path in (EXTENSION_ROOT, HERE.parent, HERE / "vendor"):
        value = str(path)
        if value not in sys.path:
            sys.path.insert(0, value)
    # Task registration imports local CoRL configs through scripts.co_rl.
    # Bind our namespace explicitly: an installed Wolf regular package named
    # scripts would otherwise take precedence over this repo's namespace.
    if "scripts" not in sys.modules:
        spec = importlib.util.spec_from_loader("scripts", loader=None, is_package=True)
        spec.submodule_search_locations = [str(REPO_ROOT / "lab" / "scripts")]
        sys.modules["scripts"] = importlib.util.module_from_spec(spec)


def validate_training_args(args):
    for key in ("num_envs", "steps", "buffer_size", "min_buffer", "batch_size", "n_step", "save_every", "log_every"):
        if getattr(args, key) < 1:
            raise ValueError(f"{key} must be positive")
    if args.buffer_size < max(args.min_buffer, args.batch_size, args.num_envs):
        raise ValueError("buffer_size must cover min_buffer, batch_size and one vector step")
    if not math.isfinite(args.updates_per_step) or args.updates_per_step <= 0:
        raise ValueError("updates_per_step must be positive and finite")
    if args.device != "cpu" and not args.device.startswith("cuda"):
        raise ValueError("device must be cpu or cuda[:N]")
    if args.buffer_device is not None and args.buffer_device != "cpu" and not args.buffer_device.startswith("cuda"):
        raise ValueError("buffer_device must be cpu or cuda[:N]")


def create_agent_config(args, runner_cfg=None):
    from flash_rl.agents.flashSAC.agent import FlashSACConfig

    runner_cfg = runner_cfg or load_default_runner_cfg()
    return FlashSACConfig(**runner_cfg.to_agent_kwargs(args))


def make_agent(env, cfg):
    import gymnasium as gym
    import numpy as np
    from flash_rl.agents.flashSAC.agent import FlashSACAgent

    return FlashSACAgent(
        gym.spaces.Box(-np.inf, np.inf, (env.num_envs, env.actor_obs_dim + env.critic_obs_dim), np.float32),
        gym.spaces.Box(-1.0, 1.0, (env.num_envs, env.action_dim), np.float32),
        {"actor_observation_size": (env.actor_obs_dim,), "critic_observation_offset": env.actor_obs_dim}, cfg,
    )


def select_buffer_device(args, env):
    import torch

    size = args.buffer_size * (2 * (env.actor_obs_dim + env.critic_obs_dim) + env.action_dim + 4) * 4
    device = args.buffer_device or args.device
    if device.startswith("cuda"):
        free = torch.cuda.mem_get_info(device)[0]
        if size > 0.8 * free:
            if args.buffer_device is not None:
                raise ValueError(f"Replay needs {size / 1e9:.2f} GB; use --buffer_device cpu or reduce --buffer_size")
            device = "cpu"
    args.buffer_device = device
    print(f"[TRAINING_SIM] Replay: {args.buffer_size} transitions, {size / 1e9:.2f} GB, {device}", flush=True)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, values):
    Path(path).write_text(json.dumps(values, indent=2, allow_nan=False) + "\n")


def checkpoint_metadata(env, agent, task, step):
    return {
        "execution_domain": "TRAINING_SIM", "task": task, "step": step,
        "actor_obs_dim": env.actor_obs_dim, "critic_obs_dim": env.critic_obs_dim,
        "action_dim": env.action_dim, "agent": asdict(agent.cfg),
        **action_mapping_metadata(env),
        "observation_layout": "policy_then_critic", "ppo_velocity_estimator": False,
        "replay_saved": False,
    }


def save_checkpoint(env, agent, cfg, output, task, step):
    import pickle

    path = Path(output) / f"model_{step}"
    agent.save(str(path))
    with (path / "env.pkl").open("wb") as stream:
        pickle.dump(cfg, stream)
    metadata = checkpoint_metadata(env, agent, task, step)
    metadata["actor_sha256"] = sha256(path / "actor.pt")
    metadata["env_config_sha256"] = sha256(path / "env.pkl")
    write_json(path / "ddt.json", metadata)
    return path, metadata


def read_checkpoint(path, task=None):
    path = Path(path).expanduser().resolve()
    required = ("ddt.json", "env.pkl", "actor.pt", "critic.pt", "target_critic.pt", "temperature.pt", "agent_state.pt")
    if any(not (path / name).is_file() for name in required):
        raise ValueError("checkpoint must be a complete FlashSAC model directory, not a PPO .pt file")
    metadata = json.loads((path / "ddt.json").read_text())
    if task is not None and metadata["task"] != task:
        raise ValueError("task must match the FlashSAC checkpoint")
    if sha256(path / "actor.pt") != metadata["actor_sha256"]:
        raise ValueError("actor checkpoint SHA256 mismatch")
    if sha256(path / "env.pkl") != metadata["env_config_sha256"]:
        raise ValueError("saved environment config SHA256 mismatch")
    action_mapping_kwargs(metadata)
    return path, metadata


def check_dimensions(env, metadata):
    for name in ("actor_obs_dim", "critic_obs_dim", "action_dim"):
        if getattr(env, name) != metadata[name]:
            raise ValueError(f"checkpoint {name} does not match the environment")
