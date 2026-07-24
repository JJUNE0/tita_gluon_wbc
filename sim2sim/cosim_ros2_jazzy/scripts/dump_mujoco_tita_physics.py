#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
import yaml


def _to_list(arr):
    if isinstance(arr, np.ndarray):
        return arr.astype(float).tolist()
    return arr


def _geom_rows(model, mujoco):
    rows = []
    for i in range(model.ngeom):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, i) or f"<unnamed:{i}>"
        body_id = int(model.geom_bodyid[i])
        body_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, body_id) or f"<body:{body_id}>"
        rows.append(
            {
                "geom_index": i,
                "geom_name": name,
                "body_name": body_name,
                "type": int(model.geom_type[i]),
                "size": _to_list(model.geom_size[i]),
                "friction": _to_list(model.geom_friction[i]),
                "solref": _to_list(model.geom_solref[i]),
                "solimp": _to_list(model.geom_solimp[i]),
                "condim": int(model.geom_condim[i]),
                "margin": float(model.geom_margin[i]),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Dump MuJoCo TITA model physics properties.")
    parser.add_argument(
        "--model",
        type=str,
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/src/ddt_ros2_control/urdfs/tita_description/mujoco/scene.xml",
    )
    parser.add_argument("--config", type=str, default="/home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim/cosim_ros2_jazzy/config/tita.yaml")
    parser.add_argument(
        "--output",
        type=str,
        default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/mujoco_tita_physics_dump.json",
    )
    args = parser.parse_args()

    import mujoco

    model_path = Path(args.model).expanduser()
    model = mujoco.MjModel.from_xml_path(str(model_path))
    xml_default_timestep = float(model.opt.timestep)
    if args.config:
        cfg = yaml.safe_load(Path(args.config).expanduser().read_text(encoding="utf-8"))
        control_cfg = cfg.get("control", {})
        if "sim_timestep" in control_cfg:
            model.opt.timestep = float(control_cfg["sim_timestep"])
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)

    geom_rows = _geom_rows(model, mujoco)
    joint_rows = []
    for i in range(model.njnt):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i) or f"<joint:{i}>"
        joint_rows.append(
            {
                "joint_index": i,
                "joint_name": name,
                "qpos_adr": int(model.jnt_qposadr[i]),
                "qvel_adr": int(model.jnt_dofadr[i]),
                "type": int(model.jnt_type[i]),
                "axis": _to_list(model.jnt_axis[i]),
                "range": _to_list(model.jnt_range[i]),
                "damping": float(model.dof_damping[model.jnt_dofadr[i]]),
                "armature": float(model.dof_armature[model.jnt_dofadr[i]]),
                "frictionloss": float(model.dof_frictionloss[model.jnt_dofadr[i]]),
            }
        )

    actuator_rows = []
    for i in range(model.nu):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, i) or f"<act:{i}>"
        trnid = model.actuator_trnid[i]
        joint_id = int(trnid[0]) if int(model.actuator_trntype[i]) == int(mujoco.mjtTrn.mjTRN_JOINT) else -1
        joint_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, joint_id) if joint_id >= 0 else None
        actuator_rows.append(
            {
                "actuator_index": i,
                "actuator_name": name,
                "joint_name": joint_name,
                "trntype": int(model.actuator_trntype[i]),
                "dyntype": int(model.actuator_dyntype[i]),
                "gaintype": int(model.actuator_gaintype[i]),
                "biastype": int(model.actuator_biastype[i]),
                "ctrllimited": bool(model.actuator_ctrllimited[i]),
                "ctrlrange": _to_list(model.actuator_ctrlrange[i]),
                "forcelimited": bool(model.actuator_forcelimited[i]),
                "forcerange": _to_list(model.actuator_forcerange[i]),
                "gear": _to_list(model.actuator_gear[i]),
            }
        )

    body_rows = []
    for i in range(model.nbody):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i) or f"<body:{i}>"
        body_rows.append(
            {
                "body_index": i,
                "body_name": name,
                "mass": float(model.body_mass[i]),
                "inertia": _to_list(model.body_inertia[i]),
                "ipos": _to_list(model.body_ipos[i]),
                "iquat": _to_list(model.body_iquat[i]),
            }
        )

    wheel_geoms = [row for row in geom_rows if "leg_4" in row["body_name"]]
    floor_geoms = [row for row in geom_rows if row["geom_name"] == "floor"]

    output = {
        "model_path": str(model_path.resolve()),
        "config_path": str(Path(args.config).expanduser().resolve()) if args.config else None,
        "sim": {
            "xml_default_timestep": xml_default_timestep,
            "active_timestep": float(model.opt.timestep),
            "integrator": int(model.opt.integrator),
            "cone": int(model.opt.cone),
            "solver": int(model.opt.solver),
            "iterations": int(model.opt.iterations),
            "ls_iterations": int(model.opt.ls_iterations),
            "noslip_iterations": int(model.opt.noslip_iterations),
            "gravity": _to_list(model.opt.gravity),
            "wind": _to_list(model.opt.wind),
        },
        "counts": {
            "nq": int(model.nq),
            "nv": int(model.nv),
            "nu": int(model.nu),
            "nbody": int(model.nbody),
            "njnt": int(model.njnt),
            "ngeom": int(model.ngeom),
            "nsensor": int(model.nsensor),
        },
        "joint_rows": joint_rows,
        "actuator_rows": actuator_rows,
        "body_rows": body_rows,
        "geom_rows": geom_rows,
        "wheel_geom_summary": wheel_geoms,
        "floor_geom_summary": floor_geoms,
    }

    out_path = Path(args.output).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
