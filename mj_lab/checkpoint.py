"""TRAINING_SIM / VALIDATION_SIM: native config plus the shared playback contract.

env.pkl and mjlab_env.yaml describe the native training environment. env.yaml
is a derived interchange schema understood by the existing sim2sim exporter;
its function/class names describe observations and actions, not Isaac imports.
"""

from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import Path
import subprocess

import cloudpickle
import torch
import yaml

from .flash_sac import runtime
from .robots.tita.robot_cfg import JOINTS, OBS_JOINTS, REPO_ROOT


def plain(value):
    if torch.is_tensor(value):
        return value.detach().cpu().tolist()
    if is_dataclass(value):
        return {f.name: plain(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if isinstance(value, (Path, Enum)):
        return str(value)
    if callable(value):
        return value.__module__ + ":" + value.__qualname__
    if isinstance(value, slice):
        return {"slice": [value.start, value.stop, value.step]}
    return value


def playback_contract(cfg):
    robot = cfg.scene.entities["robot"]
    velocity = cfg.commands["base_velocity"]
    aliases = {"base_ang_vel": "base_ang_vel", "projected_gravity": "projected_gravity",
               "base_lin_vel": "base_lin_vel", "velocity_commands": "generated_commands",
               "gait": "generated_commands", "support_mode": "generated_commands",
               "pose_commands": "generated_commands",
               "joint_pos": "joint_pos_rel_without_wheel",
               "joint_vel": "joint_vel_rel", "actions": "last_action",
               "wheel_position_error": "WheelPositionError", "heading_error": "GyroHeadingError"}
    policy = {"concatenate_terms": True, "history_length": 0}
    for name, term in cfg.observations["policy"].terms.items():
        kind = term.params["kind"]
        params = {}
        if kind in ("joint_pos", "joint_vel"):
            params["asset_cfg"] = {"name": "robot", "joint_names": list(OBS_JOINTS), "preserve_order": True}
        if kind in ("velocity_commands", "gait", "support_mode", "pose_commands", "wheel_position_error", "heading_error"):
            params["command_name"] = {"gait": "gait", "support_mode": "support",
                                      "pose_commands": "base_pose"}.get(kind, "base_velocity")
        if kind == "wheel_position_error":
            params.update(radius=.0925, clip_m=velocity.wheel_error_clip_m, zero_thresholds=[.02, .02, .03])
            if velocity.wheel_error_gait_name is not None:
                params["gait_name"] = velocity.wheel_error_gait_name
            if velocity.wheel_error_velocity_thresholds is not None:
                params["velocity_thresholds"] = list(velocity.wheel_error_velocity_thresholds)
            if velocity.wheel_error_moving_anchor:
                params["moving_anchor"] = True
        if kind == "heading_error":
            params.update(clip_rad=.5, zero_thresholds=[.02, .02, .03], warmup_s=0.0)
        policy[name] = {"func": aliases[kind], "params": params, "scale": plain(term.scale), "clip": plain(term.clip)}
    actions = {}
    for name, action in cfg.actions.items():
        actions[name] = {"class_type": type(action).__name__.removesuffix("Cfg"),
                         "joint_names": list(action.actuator_names), "scale": action.scale,
                         "use_default_offset": action.use_default_offset, "clip": plain(action.clip), "preserve_order": True}
        if hasattr(action, "gait_name"):
            # Preserve the dynamic gate explicitly for sim2sim playback.
            actions[name]["gait_name"] = action.gait_name
            actions[name]["wheel_enable"] = "gait_disabled"
        elif ("gait" in cfg.commands and actions[name]["class_type"] == "JointVelocityAction"
              and action.scale != 0 and set(action.actuator_names) <= {JOINTS[3], JOINTS[7]}):
            actions[name]["wheel_enable"] = "always"
    motors = {f"group_{i}": {"joint_names_expr": list(a.target_names_expr), "stiffness": a.stiffness,
                            "damping": a.damping, "effort_limit": a.effort_limit}
              for i, a in enumerate(robot.articulation.actuators)}
    commands = {"base_velocity": {"ranges": {name: list(getattr(velocity, name)) for name in ("lin_vel_x", "lin_vel_y", "ang_vel_z")},
                                 "ramp_rate": velocity.ramp_rate, "initial_phase_time": velocity.initial_phase_time}}
    if "gait" in cfg.commands:
        gait = cfg.commands["gait"]
        commands["gait"] = {"class_type": "WalkGaitCommand", "velocity_command_name": "base_velocity",
                            **{key: plain(getattr(gait, key)) for key in ("frequency_range_hz", "stance_fraction", "settle_time_s", "step_in_place", "linear_threshold", "yaw_threshold")}}
        if gait.straight_only:
            commands["gait"]["straight_only"] = True
    if "support" in cfg.commands:
        commands["support"] = {"class_type": "SupportModeCommand", "encoding": "one_hot",
            "mode_names": ["left", "right", "both"], "default_mode": 2,
            "resampling_time_range": list(cfg.commands["support"].resampling_time_range)}
        if cfg.commands["support"].episode_fixed:
            commands["support"].update(episode_fixed=True,
                mode_probabilities=list(cfg.commands["support"].mode_probabilities))
    if "base_pose" in cfg.commands:
        commands["base_pose"] = {"class_type": "RollPitchHeightCommand", "order": ["roll", "pitch", "height"],
            "units": ["rad", "rad", "m"], **plain(cfg.commands["base_pose"])}
    result = {"backend": "mjlab", "scene": {"robot": {"init_state": plain(robot.init_state),
            "actuators": motors, "wheel_collision": "sphere"}, "terrain": {"terrain_type": cfg.scene.terrain.terrain_type}},
            "sim": {"dt": cfg.sim.mujoco.timestep}, "decimation": cfg.decimation,
            "observations": {"policy": policy}, "actions": actions, "commands": commands}
    if (getattr(cfg, "sim_reset_on_policy_entry", False)
            or ("gait" in commands and commands["gait"]["step_in_place"]
                and all(bounds == [0., 0.] for bounds in commands["base_velocity"]["ranges"].values()))):
        result["sim_reset_on_policy_entry"] = True
    return result


def save_checkpoint(env, agent, cfg, output, task, step):
    path = Path(output) / f"model_{step}"
    agent.save(str(path))
    # Native terrain configs contain spec factory closures; standard pickle
    # cannot serialize them. Weights and learner state retain the shared format.
    with (path / "env.pkl").open("wb") as stream:
        cloudpickle.dump(cfg, stream)
    meta = runtime.checkpoint_metadata(env, agent, task, step)
    meta.update(actor_sha256=runtime.sha256(path / "actor.pt"),
                env_config_sha256=runtime.sha256(path / "env.pkl"))
    for name, values in (("env.yaml", playback_contract(cfg)), ("mjlab_env.yaml", plain(cfg))):
        (path / name).write_text(yaml.safe_dump(values, sort_keys=False))
    runtime.write_json(path / "agent.json", {"agent": plain(agent.cfg)})
    meta.update(backend="mjlab", mjlab_commit=subprocess.check_output(
        ["git", "-C", str(REPO_ROOT / "third_party/mjlab"), "rev-parse", "HEAD"], text=True).strip(),
        playback_config_sha256=runtime.sha256(path / "env.yaml"))
    meta["training_source_sha256"] = {
        str(source.relative_to(REPO_ROOT)): runtime.sha256(source)
        for source in sorted((REPO_ROOT / "mj_lab").rglob("*.py"))
        if "logs" not in source.relative_to(REPO_ROOT / "mj_lab").parts
    }
    runtime.write_json(path / "ddt.json", meta)
    return path, meta
