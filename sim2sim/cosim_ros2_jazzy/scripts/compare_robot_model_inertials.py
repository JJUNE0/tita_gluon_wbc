#!/usr/bin/env python3
"""Compare TITA robot model inertials and joint dynamics: URDF vs MJCF.

Reads the source URDF and one or more MJCF robot.xml files, extracts mass,
COM, and inertia for every named body/link, then writes a side-by-side
comparison to JSON and CSV.  Also compares joint damping/armature/frictionloss
and actuator force limits.

Usage:
    python3 cosim_ros2_jazzy/scripts/compare_robot_model_inertials.py \
        --urdf  ddt_ros2_control/urdfs/tita_description/urdf/robot.urdf \
        --mjcf  ddt_ros2_control/urdfs/tita_description/mujoco/robot.xml \
        --mjcf-corrected \
                ddt_ros2_control/urdfs/tita_description/mujoco_corrected/robot.xml \
        --out-json  deploy/tita/model_inertial_compare.json \
        --out-csv   deploy/tita/model_inertial_compare.csv \
        --out-joint-csv deploy/tita/model_joint_dynamics_compare.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# URDF parsing
# ---------------------------------------------------------------------------

def _parse_urdf(path: str) -> dict[str, dict]:
    """Return {link_name: {mass, com, inertia_dict}} from a URDF file.

    inertia_dict keys: ixx iyy izz ixy ixz iyz (all in kg·m², link frame).
    Fixed-joint children with non-zero mass are noted; their merged contribution
    to the parent is annotated but NOT summed here (the caller decides).
    """
    tree = ET.parse(path)
    root = tree.getroot()

    links: dict[str, dict] = {}
    for link in root.findall("link"):
        name = link.get("name", "")
        inertial = link.find("inertial")
        if inertial is None:
            continue
        origin = inertial.find("origin")
        mass_el = inertial.find("mass")
        inertia_el = inertial.find("inertia")
        if mass_el is None or inertia_el is None:
            continue

        xyz = [float(v) for v in origin.get("xyz", "0 0 0").split()] if origin is not None else [0, 0, 0]
        mass = float(mass_el.get("value", 0))
        ixx = float(inertia_el.get("ixx", 0))
        iyy = float(inertia_el.get("iyy", 0))
        izz = float(inertia_el.get("izz", 0))
        ixy = float(inertia_el.get("ixy", 0))
        ixz = float(inertia_el.get("ixz", 0))
        iyz = float(inertia_el.get("iyz", 0))

        links[name] = {
            "mass": mass,
            "com": xyz,
            "ixx": ixx, "iyy": iyy, "izz": izz,
            "ixy": ixy, "ixz": ixz, "iyz": iyz,
        }

    # Find fixed joints to annotate which children are merged by Isaac.
    fixed_merges: dict[str, list[str]] = {}  # parent -> [child, ...]
    for joint in root.findall("joint"):
        if joint.get("type") == "fixed":
            parent_el = joint.find("parent")
            child_el = joint.find("child")
            if parent_el is not None and child_el is not None:
                p = parent_el.get("link", "")
                c = child_el.get("link", "")
                fixed_merges.setdefault(p, []).append(c)

    return links, fixed_merges


# ---------------------------------------------------------------------------
# MJCF parsing helpers
# ---------------------------------------------------------------------------

def _quat_to_rot(q: list[float]) -> list[list[float]]:
    """Convert MuJoCo quaternion [w, x, y, z] to 3x3 rotation matrix."""
    w, x, y, z = q
    return [
        [1-2*(y*y+z*z),   2*(x*y-w*z),   2*(x*z+w*y)],
        [  2*(x*y+w*z), 1-2*(x*x+z*z),   2*(y*z-w*x)],
        [  2*(x*z-w*y),   2*(y*z+w*x), 1-2*(x*x+y*y)],
    ]


def _rotate_inertia(I: list[list[float]], R: list[list[float]]) -> list[list[float]]:
    """Compute R @ I @ R^T for 3x3 matrices represented as lists."""
    def mm(A, B):
        n = len(A)
        return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    Rt = [[R[j][i] for j in range(3)] for i in range(3)]
    return mm(mm(R, I), Rt)


def _parse_mjcf_inertial(body_el: ET.Element) -> dict | None:
    """Extract inertial data from a MuJoCo <body> element.

    Returns {mass, com, ixx, iyy, izz, ixy, ixz, iyz} in the body frame,
    or None if no <inertial> is present.

    Handles both:
      - diaginertia + quat  (original format)
      - fullinertia          (new corrected format)
    """
    inertial = body_el.find("inertial")
    if inertial is None:
        return None

    mass = float(inertial.get("mass", 0))
    pos_str = inertial.get("pos", "0 0 0")
    com = [float(v) for v in pos_str.split()]

    full_str = inertial.get("fullinertia")
    if full_str is not None:
        vals = [float(v) for v in full_str.split()]
        ixx, iyy, izz, ixy, ixz, iyz = vals
    else:
        diag_str = inertial.get("diaginertia", "0 0 0")
        d = [float(v) for v in diag_str.split()]
        quat_str = inertial.get("quat", "1 0 0 0")
        q = [float(v) for v in quat_str.split()]
        # Rotate principal-axis inertia back to body frame.
        I_principal = [[d[0], 0, 0], [0, d[1], 0], [0, 0, d[2]]]
        R = _quat_to_rot(q)
        I_body = _rotate_inertia(I_principal, R)
        ixx = I_body[0][0]; iyy = I_body[1][1]; izz = I_body[2][2]
        ixy = I_body[0][1]; ixz = I_body[0][2]; iyz = I_body[1][2]

    return {
        "mass": mass, "com": com,
        "ixx": ixx, "iyy": iyy, "izz": izz,
        "ixy": ixy, "ixz": ixz, "iyz": iyz,
    }


def _parse_mjcf_defaults(root: ET.Element) -> dict:
    """Collect default joint attributes from the MJCF <default> hierarchy."""
    defaults = {"damping": None, "armature": None, "frictionloss": None}
    for default in root.iter("default"):
        for joint_el in default.findall("joint"):
            for key in defaults:
                val = joint_el.get(key)
                if val is not None:
                    defaults[key] = float(val)
    return defaults


def _collect_mjcf_bodies(root: ET.Element) -> dict[str, dict]:
    """Recursively collect all named bodies with inertial data from MJCF."""
    result: dict[str, dict] = {}

    def _visit(el: ET.Element):
        for body in el.findall("body"):
            name = body.get("name", "")
            data = _parse_mjcf_inertial(body)
            if data is not None:
                result[name] = data
            _visit(body)

    worldbody = root.find("worldbody")
    if worldbody is not None:
        _visit(worldbody)
    return result


def _collect_mjcf_joints(root: ET.Element, defaults: dict) -> dict[str, dict]:
    """Collect all named joints with damping/armature/frictionloss from MJCF."""
    result: dict[str, dict] = {}

    def _visit(el: ET.Element):
        for body in el.findall("body"):
            for joint in body.findall("joint"):
                name = joint.get("name", "")
                if not name:
                    continue
                result[name] = {
                    "damping": float(joint.get("damping", defaults.get("damping") or 0)),
                    "armature": float(joint.get("armature", defaults.get("armature") or 0)),
                    "frictionloss": float(joint.get("frictionloss", defaults.get("frictionloss") or 0)),
                }
            _visit(body)

    worldbody = root.find("worldbody")
    if worldbody is not None:
        _visit(worldbody)
    return result


def _collect_mjcf_actuators(root: ET.Element) -> dict[str, dict]:
    """Collect actuator names and forcerange from MJCF."""
    result: dict[str, dict] = {}
    actuator_el = root.find("actuator")
    if actuator_el is None:
        return result
    for act in actuator_el:
        name = act.get("name", "")
        fr_str = act.get("forcerange", "")
        gear = float(act.get("gear", 1))
        if fr_str:
            lo, hi = [float(v) for v in fr_str.split()]
        else:
            lo, hi = None, None
        result[name] = {"gear": gear, "forcerange_lo": lo, "forcerange_hi": hi}
    return result


def _parse_mjcf(path: str) -> tuple:
    """Return (bodies, joints, actuators, defaults) from a MJCF robot.xml."""
    tree = ET.parse(path)
    root = tree.getroot()
    defaults = _parse_mjcf_defaults(root)
    bodies = _collect_mjcf_bodies(root)
    joints = _collect_mjcf_joints(root, defaults)
    actuators = _collect_mjcf_actuators(root)
    return bodies, joints, actuators, defaults


# ---------------------------------------------------------------------------
# Comparison logic
# ---------------------------------------------------------------------------

LINK_NAMES = [
    "base_link",
    "left_leg_1", "left_leg_2", "left_leg_3", "left_leg_4",
    "right_leg_1", "right_leg_2", "right_leg_3", "right_leg_4",
]

JOINT_NAMES = [
    "joint_left_leg_1", "joint_left_leg_2", "joint_left_leg_3", "joint_left_leg_4",
    "joint_right_leg_1", "joint_right_leg_2", "joint_right_leg_3", "joint_right_leg_4",
]

# Isaac actuator reference (from ddt_robot.py DDT_TITA_CFG)
ISAAC_ACTUATOR = {
    "legs": {"stiffness": 60.0, "damping": 1.5, "effort_limit": 60.0},
    "wheels": {"stiffness": 0.0, "damping": 0.5, "effort_limit": 12.0},
}


def _rel_err(a: float, b: float) -> float:
    if abs(a) < 1e-12:
        return float("inf") if abs(b) > 1e-12 else 0.0
    return abs(a - b) / abs(a)


def build_inertial_rows(
    urdf_links: dict,
    mjcf_bodies: dict,
    mjcf_corr_bodies: dict | None,
) -> list[dict]:
    rows = []
    for name in LINK_NAMES:
        u = urdf_links.get(name)
        m = mjcf_bodies.get(name)
        c = mjcf_corr_bodies.get(name) if mjcf_corr_bodies else None

        row: dict[str, Any] = {"link": name}

        # mass
        row["urdf_mass"] = u["mass"] if u else None
        row["mjcf_mass"] = m["mass"] if m else None
        row["mjcf_corr_mass"] = c["mass"] if c else None
        if u and m:
            row["mass_rel_err_pct"] = round(_rel_err(u["mass"], m["mass"]) * 100, 2)
            row["mass_within_5pct"] = row["mass_rel_err_pct"] < 5.0
        else:
            row["mass_rel_err_pct"] = None
            row["mass_within_5pct"] = None

        # inertia diagonals
        for key in ("ixx", "iyy", "izz"):
            row[f"urdf_{key}"] = u[key] if u else None
            row[f"mjcf_{key}"] = m[key] if m else None
            row[f"mjcf_corr_{key}"] = c[key] if c else None
            if u and m:
                row[f"{key}_rel_err_pct"] = round(_rel_err(u[key], m[key]) * 100, 2)
            else:
                row[f"{key}_rel_err_pct"] = None

        # off-diagonal
        for key in ("ixy", "ixz", "iyz"):
            row[f"urdf_{key}"] = u[key] if u else None
            row[f"mjcf_{key}"] = m[key] if m else None
            row[f"mjcf_corr_{key}"] = c[key] if c else None

        rows.append(row)
    return rows


def build_joint_rows(
    mjcf_joints: dict,
    mjcf_corr_joints: dict | None,
) -> list[dict]:
    rows = []
    for name in JOINT_NAMES:
        is_wheel = name.endswith("_4")
        isaac_ref = ISAAC_ACTUATOR["wheels"] if is_wheel else ISAAC_ACTUATOR["legs"]

        m = mjcf_joints.get(name, {})
        c = (mjcf_corr_joints or {}).get(name, {})

        rows.append({
            "joint": name,
            "type": "wheel" if is_wheel else "leg",
            "isaac_controller_kd": isaac_ref["damping"],
            "isaac_effort_limit_Nm": isaac_ref["effort_limit"],
            "mjcf_damping": m.get("damping"),
            "mjcf_armature": m.get("armature"),
            "mjcf_frictionloss": m.get("frictionloss"),
            "mjcf_corr_damping": c.get("damping"),
            "mjcf_corr_armature": c.get("armature"),
            "mjcf_corr_frictionloss": c.get("frictionloss"),
            "note": (
                "Isaac physical joint damping=0 (UrdfFileCfg drive gains=0); "
                "controller kd supplied externally. "
                "MuJoCo joint damping should be 0."
            ),
        })
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--urdf", required=True)
    ap.add_argument("--mjcf", required=True, help="Original MJCF robot.xml")
    ap.add_argument("--mjcf-corrected", default=None, help="Corrected MJCF robot.xml")
    ap.add_argument("--out-json", default="deploy/tita/model_inertial_compare.json")
    ap.add_argument("--out-csv",  default="deploy/tita/model_inertial_compare.csv")
    ap.add_argument("--out-joint-csv", default="deploy/tita/model_joint_dynamics_compare.csv")
    args = ap.parse_args()

    print(f"[compare] URDF: {args.urdf}")
    urdf_links, fixed_merges = _parse_urdf(args.urdf)
    print(f"  links found: {list(urdf_links.keys())}")
    if "base_link" in fixed_merges:
        print(f"  fixed children of base_link: {fixed_merges['base_link']}")

    print(f"[compare] MJCF (original): {args.mjcf}")
    mjcf_bodies, mjcf_joints, mjcf_acts, mjcf_defaults = _parse_mjcf(args.mjcf)
    print(f"  bodies found: {list(mjcf_bodies.keys())}")
    print(f"  default joint: {mjcf_defaults}")

    mjcf_corr_bodies = mjcf_corr_joints = mjcf_corr_acts = None
    if args.mjcf_corrected:
        print(f"[compare] MJCF (corrected): {args.mjcf_corrected}")
        mjcf_corr_bodies, mjcf_corr_joints, mjcf_corr_acts, corr_defaults = _parse_mjcf(args.mjcf_corrected)
        print(f"  corrected default joint: {corr_defaults}")

    inertial_rows = build_inertial_rows(urdf_links, mjcf_bodies, mjcf_corr_bodies)
    joint_rows = build_joint_rows(mjcf_joints, mjcf_corr_joints)

    # Print summary
    def _fmt(v) -> str:
        return f"{v:6.1f}%" if v is not None else "   N/A"

    print("\n--- Inertial Comparison (URDF vs original MJCF) ---")
    for r in inertial_rows:
        ln = r["link"]
        print(
            f"  {ln:15s}  mass_err={_fmt(r.get('mass_rel_err_pct'))}  "
            f"ixx_err={_fmt(r.get('ixx_rel_err_pct'))}  "
            f"iyy_err={_fmt(r.get('iyy_rel_err_pct'))}  "
            f"izz_err={_fmt(r.get('izz_rel_err_pct'))}"
        )

    print("\n--- Joint Dynamics (original MJCF vs corrected) ---")
    for r in joint_rows:
        print(
            f"  {r['joint']:25s}  "
            f"mjcf_damp={r['mjcf_damping']}  "
            f"corr_damp={r['mjcf_corr_damping']}  "
            f"mjcf_fric={r['mjcf_frictionloss']}  "
            f"corr_fric={r['mjcf_corr_frictionloss']}"
        )

    # Save JSON
    Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
    out = {
        "urdf_path": args.urdf,
        "mjcf_path": args.mjcf,
        "mjcf_corrected_path": args.mjcf_corrected,
        "inertial_comparison": inertial_rows,
        "joint_dynamics_comparison": joint_rows,
        "isaac_actuator_reference": ISAAC_ACTUATOR,
        "mjcf_defaults": mjcf_defaults,
    }
    with open(args.out_json, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[compare] saved: {args.out_json}")

    # Save inertial CSV
    if inertial_rows:
        with open(args.out_csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(inertial_rows[0].keys()))
            w.writeheader()
            w.writerows(inertial_rows)
        print(f"[compare] saved: {args.out_csv}")

    # Save joint dynamics CSV
    if joint_rows:
        with open(args.out_joint_csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(joint_rows[0].keys()))
            w.writeheader()
            w.writerows(joint_rows)
        print(f"[compare] saved: {args.out_joint_csv}")


if __name__ == "__main__":
    main()
