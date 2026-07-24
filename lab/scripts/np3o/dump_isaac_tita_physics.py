#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Dump IsaacLab TITA training physics and domain randomization settings.")
parser.add_argument("--task", type=str, default="DDT-Velocity-Flat-Tita-v0")
parser.add_argument("--num_envs", type=int, default=1)
parser.add_argument(
    "--output",
    type=str,
    default="/home/cocel/Desktop/Research/DDT_Lab/deploy/tita/isaac_tita_physics_dump.json",
)
AppLauncher.add_app_launcher_args(parser)
args_cli, _ = parser.parse_known_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import ddt_lab.tasks  # noqa: E402,F401
import gymnasium as gym  # noqa: E402
import numpy as np  # noqa: E402
from isaaclab_tasks.utils import get_checkpoint_path  # noqa: F401,E402


def _value_to_python(value):
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, np.ndarray):
        return value.astype(float).tolist()
    if isinstance(value, (list, tuple)):
        return [_value_to_python(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _value_to_python(v) for k, v in value.items()}
    if hasattr(value, "__dict__"):
        return {
            k: _value_to_python(v)
            for k, v in vars(value).items()
            if not k.startswith("_") and not callable(v)
        }
    try:
        import torch

        if isinstance(value, torch.Tensor):
            return value.detach().cpu().numpy().astype(float).tolist()
    except Exception:
        pass
    return str(value)


def _event_table(events_cfg) -> list[dict]:
    rows: list[dict] = []
    for name in dir(events_cfg):
        if name.startswith("_"):
            continue
        term = getattr(events_cfg, name)
        if term is None or callable(term):
            continue
        rows.append(
            {
                "name": name,
                "enabled": True,
                "mode": getattr(term, "mode", None),
                "interval_range_s": _value_to_python(getattr(term, "interval_range_s", None)),
                "func": getattr(getattr(term, "func", None), "__name__", str(getattr(term, "func", None))),
                "params": _value_to_python(getattr(term, "params", {})),
                "source_file": "source/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/rough_env_cfg.py",
            }
        )
    return rows


def main() -> None:
    spec = gym.spec(args_cli.task)
    env_cfg_entry = spec.kwargs["env_cfg_entry_point"]
    env_cfg = env_cfg_entry() if callable(env_cfg_entry) else env_cfg_entry
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device

    env = gym.make(args_cli.task, cfg=env_cfg)
    raw = env.unwrapped
    raw.reset()
    raw.scene.update(dt=raw.physics_dt)
    robot = raw.scene["robot"]

    joint_names = list(robot.root_physx_view.shared_metatype.dof_names)
    body_names = list(robot.root_physx_view.shared_metatype.link_names)
    joint_paths = list(robot.root_physx_view.dof_paths[0])
    body_paths = list(robot.root_physx_view.link_paths[0])

    joint_names_short = [name.split("/")[-1] for name in joint_paths]
    body_names_short = [name.split("/")[-1] for name in body_paths]

    masses_runtime = robot.root_physx_view.get_masses()[0].detach().cpu().numpy().astype(np.float64)
    inertias_runtime = robot.root_physx_view.get_inertias()[0].detach().cpu().numpy().astype(np.float64)
    com_runtime = robot.root_physx_view.get_coms()[0].detach().cpu().numpy().astype(np.float64)
    material_runtime = robot.root_physx_view.get_material_properties()[0].detach().cpu().numpy().astype(np.float64)
    joint_friction_props = robot.root_physx_view.get_dof_friction_properties()[0].detach().cpu().numpy().astype(np.float64)

    terrain_mat = env_cfg.scene.terrain.physics_material
    actuator_rows = []
    for name, actuator in robot.actuators.items():
        joint_indices = [int(i) for i in getattr(actuator, "joint_indices", [])]
        actuator_rows.append(
            {
                "name": name,
                "type": actuator.__class__.__name__,
                "joint_indices": joint_indices,
                "joint_names": [joint_names_short[i] for i in joint_indices],
                "effort_limit": _value_to_python(getattr(actuator, "effort_limit", None)),
                "effort_limit_sim": _value_to_python(getattr(actuator, "effort_limit_sim", None)),
                "saturation_effort": _value_to_python(getattr(actuator, "saturation_effort", None)),
                "velocity_limit": _value_to_python(getattr(actuator, "velocity_limit", None)),
                "velocity_limit_sim": _value_to_python(getattr(actuator, "velocity_limit_sim", None)),
                "stiffness": _value_to_python(getattr(actuator, "stiffness", None)),
                "damping": _value_to_python(getattr(actuator, "damping", None)),
                "friction": _value_to_python(getattr(actuator, "friction", None)),
                "class_config": _value_to_python(getattr(actuator, "cfg", None)),
            }
        )

    event_rows = _event_table(env_cfg.events)
    output = {
        "task": args_cli.task,
        "task_config_path": "source/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/flat_env_cfg.py",
        "task_config_class": env_cfg.__class__.__name__,
        "base_env_config_class": env_cfg.__class__.__bases__[0].__name__ if env_cfg.__class__.__bases__ else None,
        "play_env": args_cli.task.endswith("-Play-v0"),
        "onnx_origin_hint": "logs/np3o/tita_flat/... implies flat task checkpoint",
        "randomization_enabled_in_this_env": not args_cli.task.endswith("-Play-v0"),
        "play_env_randomization_note": "Play env removes pushes, base inertia/com/mass randomization, actuator gain randomization, and observation corruption.",
        "sim": {
            "physics_dt": float(raw.physics_dt),
            "decimation": int(raw.cfg.decimation),
            "policy_dt": float(raw.step_dt),
            "episode_length_s": float(raw.max_episode_length_s),
            "disable_contact_processing": bool(getattr(raw.cfg.sim, "disable_contact_processing", True)),
            "terrain_type": getattr(env_cfg.scene.terrain, "terrain_type", None),
            "ground_material_nominal": {
                "static_friction": float(terrain_mat.static_friction),
                "dynamic_friction": float(terrain_mat.dynamic_friction),
                "restitution": float(terrain_mat.restitution_combine_mode == "multiply" and 0.0 or 0.0),
                "friction_combine_mode": str(terrain_mat.friction_combine_mode),
                "restitution_combine_mode": str(terrain_mat.restitution_combine_mode),
            },
            "articulation_root_props": {
                "solver_position_iteration_count": int(robot.cfg.spawn.articulation_props.solver_position_iteration_count),
                "solver_velocity_iteration_count": int(robot.cfg.spawn.articulation_props.solver_velocity_iteration_count),
            },
            "rigid_props": {
                "linear_damping": float(robot.cfg.spawn.rigid_props.linear_damping),
                "angular_damping": float(robot.cfg.spawn.rigid_props.angular_damping),
                "max_linear_velocity": float(robot.cfg.spawn.rigid_props.max_linear_velocity),
                "max_angular_velocity": float(robot.cfg.spawn.rigid_props.max_angular_velocity),
                "max_depenetration_velocity": float(robot.cfg.spawn.rigid_props.max_depenetration_velocity),
            },
        },
        "domain_randomization": event_rows,
        "robot": {
            "joint_names": joint_names_short,
            "body_names": body_names_short,
            "default_joint_pos": robot.data.default_joint_pos[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "runtime_joint_pos": robot.data.joint_pos[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "default_joint_stiffness": robot.data.default_joint_stiffness[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "runtime_joint_stiffness": robot.data.joint_stiffness[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "default_joint_damping": robot.data.default_joint_damping[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "runtime_joint_damping": robot.data.joint_damping[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "default_joint_armature": robot.data.default_joint_armature[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "runtime_joint_armature": robot.data.joint_armature[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "default_joint_friction_coeff": robot.data.default_joint_friction_coeff[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "runtime_joint_friction_props": joint_friction_props.tolist(),
            "default_joint_velocity_limits": robot.data.joint_vel_limits[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "default_joint_effort_limits": robot.data.joint_effort_limits[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "actuators": actuator_rows,
            "default_body_mass": robot.data.default_mass[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "runtime_body_mass": masses_runtime.tolist(),
            "default_body_inertia": robot.data.default_inertia[0].detach().cpu().numpy().astype(np.float64).tolist(),
            "runtime_body_inertia": inertias_runtime.tolist(),
            "runtime_body_com_pose": com_runtime.tolist(),
            "runtime_material_properties": material_runtime.tolist(),
            "runtime_material_summary": {
                "shape_count": int(material_runtime.shape[0]) if material_runtime.ndim >= 2 else 0,
                "static_friction_min": float(material_runtime[:, 0].min()) if material_runtime.ndim >= 2 else None,
                "static_friction_max": float(material_runtime[:, 0].max()) if material_runtime.ndim >= 2 else None,
                "dynamic_friction_min": float(material_runtime[:, 1].min()) if material_runtime.ndim >= 2 else None,
                "dynamic_friction_max": float(material_runtime[:, 1].max()) if material_runtime.ndim >= 2 else None,
                "restitution_min": float(material_runtime[:, 2].min()) if material_runtime.ndim >= 2 else None,
                "restitution_max": float(material_runtime[:, 2].max()) if material_runtime.ndim >= 2 else None,
            },
        },
    }

    out_path = Path(args_cli.output).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(out_path)

    env.close()
    simulation_app.close()


if __name__ == "__main__":
    main()
