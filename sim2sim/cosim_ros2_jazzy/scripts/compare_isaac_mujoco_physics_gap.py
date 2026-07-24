#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _inside_range(value, rng):
    if value is None or rng is None:
        return None
    lo, hi = rng
    return lo <= value <= hi


def _severity(inside, note="", semantic=False):
    if inside is False:
        return "HIGH"
    if semantic:
        return "MEDIUM"
    return "LOW"


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare Isaac training DR ranges against current MuJoCo physics values.")
    parser.add_argument("--isaac", type=str, default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/isaac_tita_physics_dump.json")
    parser.add_argument("--mujoco", type=str, default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/mujoco_tita_physics_dump.json")
    parser.add_argument("--out-json", type=str, default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/isaac_mujoco_physics_gap_report.json")
    parser.add_argument("--out-csv", type=str, default="/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/isaac_mujoco_physics_gap_report.csv")
    args = parser.parse_args()

    isaac = json.loads(Path(args.isaac).expanduser().read_text(encoding="utf-8"))
    mujoco = json.loads(Path(args.mujoco).expanduser().read_text(encoding="utf-8"))

    dr_terms = {row["name"]: row for row in isaac["domain_randomization"]}
    mujoco_joints = {row["joint_name"]: row for row in mujoco["joint_rows"]}

    mujoco_floor = mujoco["floor_geom_summary"][0] if mujoco["floor_geom_summary"] else {}
    wheel_geoms = mujoco["wheel_geom_summary"]
    wheel_frictions = [geom["friction"][0] for geom in wheel_geoms if geom.get("friction")]
    wheel_roll = [geom["friction"][2] for geom in wheel_geoms if geom.get("friction")]

    rows = []

    def add(parameter, isaac_nominal, isaac_range, mujoco_value, note="", semantic=False):
        inside = _inside_range(mujoco_value, isaac_range)
        rows.append(
            {
                "parameter": parameter,
                "isaac_nominal": isaac_nominal,
                "isaac_dr_range": isaac_range,
                "mujoco_value": mujoco_value,
                "inside_dr_range": inside,
                "severity": _severity(inside, note=note, semantic=semantic),
                "note": note,
            }
        )

    physics_material = dr_terms.get("physics_material", {})
    physics_params = physics_material.get("params", {})
    add(
        "robot_material.static_friction",
        1.0,
        physics_params.get("static_friction_range"),
        min(wheel_frictions) if wheel_frictions else None,
        note="MuJoCo wheel sliding friction compared against Isaac robot body material randomization.",
    )
    add(
        "robot_material.dynamic_friction",
        1.0,
        physics_params.get("dynamic_friction_range"),
        min(wheel_frictions) if wheel_frictions else None,
        note="MuJoCo uses a single sliding friction value per geom; Isaac randomizes static/dynamic separately.",
        semantic=True,
    )
    add(
        "robot_material.restitution",
        0.0,
        physics_params.get("restitution_range"),
        mujoco_floor.get("friction", [None, None, None])[0],
        note="Not directly comparable here; MuJoCo dump did not expose restitution on geoms.",
        semantic=True,
    )
    add(
        "ground.static_friction",
        isaac["sim"]["ground_material_nominal"]["static_friction"],
        None,
        mujoco_floor.get("friction", [None])[0],
        note="Ground is fixed in Isaac flat task. MuJoCo floor sliding friction should be compared directly.",
        semantic=True,
    )
    add(
        "ground.rolling_friction",
        0.0,
        None,
        max(wheel_roll) if wheel_roll else None,
        note="Isaac flat terrain config does not expose MuJoCo-style rolling friction. Contact semantics differ.",
        semantic=True,
    )

    mass_term = dr_terms.get("add_base_mass", {})
    mass_params = mass_term.get("params", {})
    base_mass_nominal = isaac["robot"]["default_body_mass"][0]
    mass_range = (
        base_mass_nominal + mass_params.get("mass_distribution_params", [0.0, 0.0])[0],
        base_mass_nominal + mass_params.get("mass_distribution_params", [0.0, 0.0])[1],
    )
    add(
        "base_link.mass",
        base_mass_nominal,
        mass_range,
        next((row["mass"] for row in mujoco["body_rows"] if row["body_name"] == "base_link"), None),
        note="Isaac randomizes base mass additively on base_link only.",
    )

    inertia_term = dr_terms.get("add_base_inertia", {})
    inertia_params = inertia_term.get("params", {})
    scale_rng = inertia_params.get("inertia_distribution_params")
    mujoco_base_inertia = next((row["inertia"] for row in mujoco["body_rows"] if row["body_name"] == "base_link"), [None, None, None])
    isaac_base_inertia = isaac["robot"]["default_body_inertia"][0]
    for axis, idx in zip(["xx", "yy", "zz"], [0, 4, 8]):
        nominal = isaac_base_inertia[idx]
        rng = (nominal * scale_rng[0], nominal * scale_rng[1]) if scale_rng else None
        add(
            f"base_link.inertia_{axis}",
            nominal,
            rng,
            mujoco_base_inertia[["xx", "yy", "zz"].index(axis)],
            note="Isaac randomizes only diagonal inertia by scaling.",
        )

    com_term = dr_terms.get("add_base_com", {})
    com_range = com_term.get("params", {}).get("com_range", {})
    mujoco_base_com = next((row["ipos"] for row in mujoco["body_rows"] if row["body_name"] == "base_link"), [None, None, None])
    for axis, idx in zip(["x", "y", "z"], [0, 1, 2]):
        add(
            f"base_link.com_{axis}",
            0.0,
            com_range.get(axis),
            mujoco_base_com[idx],
            note="Isaac randomizes COM offset; MuJoCo body inertial frame offset compared directly.",
        )

    gain_term = dr_terms.get("randomize_actuator_gains", {})
    gain_params = gain_term.get("params", {})
    stiff_scale = gain_params.get("stiffness_distribution_params")
    damp_scale = gain_params.get("damping_distribution_params")
    for joint_name, default_stiff, default_damp in zip(
        isaac["robot"]["joint_names"],
        isaac["robot"]["default_joint_stiffness"],
        isaac["robot"]["default_joint_damping"],
    ):
        mu = mujoco_joints.get(joint_name)
        if mu is None:
            continue
        if stiff_scale:
            add(
                f"{joint_name}.stiffness",
                default_stiff,
                (default_stiff * stiff_scale[0], default_stiff * stiff_scale[1]),
                None,
                note="MuJoCo XML motor actuator has no built-in stiffness; controller semantics must supply it.",
                semantic=True,
            )
        if damp_scale:
            add(
                f"{joint_name}.damping",
                default_damp,
                (default_damp * damp_scale[0], default_damp * damp_scale[1]),
                mu["damping"],
                note="Joint damping compares XML/runtime damping only, not controller damping.",
                semantic=True,
            )

    add(
        "physics_dt",
        isaac["sim"]["physics_dt"],
        None,
        mujoco["sim"]["active_timestep"],
        note="Direct timing comparison. This may intentionally differ when using ddt_reference_500hz mode.",
    )
    add(
        "policy_dt",
        isaac["sim"]["policy_dt"],
        None,
        None,
        note="Compare with active MuJoCo timing config, not raw XML dump.",
        semantic=True,
    )
    add(
        "solver_position_iterations",
        isaac["sim"]["articulation_root_props"]["solver_position_iteration_count"],
        None,
        mujoco["sim"]["iterations"],
        note="PhysX articulation iterations vs MuJoCo solver iterations are not directly equivalent.",
        semantic=True,
    )

    out_json = Path(args.out_json).expanduser()
    out_csv = Path(args.out_csv).expanduser()
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "parameter",
                "isaac_nominal",
                "isaac_dr_range",
                "mujoco_value",
                "inside_dr_range",
                "severity",
                "note",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(out_json)
    print(out_csv)


if __name__ == "__main__":
    main()
