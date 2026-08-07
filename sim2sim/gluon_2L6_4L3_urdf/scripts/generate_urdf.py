#!/usr/bin/env python3
"""Generate an upright GLUON 2L6-4L3 URDF with measured actuator masses."""

from pathlib import Path
import copy
import struct
import xml.etree.ElementTree as ET

import numpy as np


PACKAGE_DIR = Path(__file__).resolve().parents[1]
SOURCE_URDF = PACKAGE_DIR / "urdf" / "left_gravity_source.urdf"
OUTPUT_URDF = PACKAGE_DIR / "urdf" / "gluon_2L6_4L3.urdf"
SIM_OUTPUT_URDF = PACKAGE_DIR / "urdf" / "gluon_2L6_4L3_sim.urdf"

# Motor-side hard stops mapped into URDF coordinates. These control limits stay
# seven joint degrees inside the measured mechanical stops.
JOINT_SOFT_LIMITS_RAD = {
    "axis_joint_1": (-2.584484342, 2.584484342),
    "axis_joint_2": (-1.623319218, 1.651337338),
    "axis_joint_3": (-2.443782617, 2.395065067),
    "axis_joint_4": (-2.419633194, 2.396012955),
    "axis_joint_5": (-2.421678546, 2.407829882),
    # ID6 has no measured mechanical-stop sweep yet.  The calibration layer
    # maps motor turns 0 to q6=0; the URDF enforces the operator-selected
    # cable-safe software range around that model zero.
    "axis_joint_6": (-2.617993878, 2.617993878),
}

# Measured masses take precedence over published nominal masses.
MOTORS = {
    "link1": {"mass": 0.540, "diameter": 0.080, "length": 0.0693},
    "link2": {"mass": 0.540, "diameter": 0.080, "length": 0.0693},
    "link3": {"mass": 0.245, "diameter": 0.052, "length": 0.0688},
    "link4": {"mass": 0.245, "diameter": 0.052, "length": 0.0688},
    "link5": {"mass": 0.245, "diameter": 0.052, "length": 0.0688},
    "link6": {"mass": 0.245, "diameter": 0.052, "length": 0.0688},
}


def _vector(text: str) -> np.ndarray:
    return np.asarray([float(value) for value in text.split()], dtype=float)


def _inertia_matrix(attributes: dict[str, str]) -> np.ndarray:
    return np.asarray(
        [
            [float(attributes["ixx"]), float(attributes["ixy"]), float(attributes["ixz"])],
            [float(attributes["ixy"]), float(attributes["iyy"]), float(attributes["iyz"])],
            [float(attributes["ixz"]), float(attributes["iyz"]), float(attributes["izz"])],
        ]
    )


def _parallel_axis(mass: float, displacement: np.ndarray) -> np.ndarray:
    return mass * (
        float(displacement @ displacement) * np.eye(3)
        - np.outer(displacement, displacement)
    )


def _motor_inertia(mass: float, radius: float, length: float) -> np.ndarray:
    # Uniform solid-cylinder approximation, with the cylinder axis along link Z.
    transverse = mass * (3.0 * radius**2 + length**2) / 12.0
    axial = mass * radius**2 / 2.0
    return np.diag([transverse, transverse, axial])


def _binary_stl_bounds(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Return AABB center and size without loading the full mesh into PhysX."""
    with path.open("rb") as stream:
        stream.seek(80)
        triangle_count = struct.unpack("<I", stream.read(4))[0]
        triangles = np.fromfile(
            stream,
            dtype=np.dtype(
                [
                    ("normal", "<f4", (3,)),
                    ("vertices", "<f4", (3, 3)),
                    ("attribute", "<u2"),
                ]
            ),
            count=triangle_count,
        )
    if len(triangles) != triangle_count:
        raise ValueError(f"Unexpected or non-binary STL: {path}")
    vertices = triangles["vertices"].reshape(-1, 3).astype(float)
    lower = vertices.min(axis=0)
    upper = vertices.max(axis=0)
    return (lower + upper) / 2.0, upper - lower


def _make_sim_variant(root: ET.Element) -> ET.Element:
    """Create a PhysX-friendly variant with base_link as root and box colliders."""
    sim_root = copy.deepcopy(root)
    sim_root.set("name", "gluon_2L6_4L3_sim")
    sim_root.remove(sim_root.find("link[@name='world']"))
    sim_root.remove(sim_root.find("joint[@name='world_joint']"))

    for link in sim_root.findall("link"):
        collision = link.find("collision")
        mesh = collision.find("geometry/mesh") if collision is not None else None
        if mesh is None:
            continue
        mesh_path = (SIM_OUTPUT_URDF.parent / mesh.get("filename")).resolve()
        center, size = _binary_stl_bounds(mesh_path)
        collision.find("origin").set("xyz", " ".join(f"{value:.12g}" for value in center))
        collision.find("origin").set("rpy", "0 0 0")
        geometry = collision.find("geometry")
        geometry.remove(mesh)
        ET.SubElement(geometry, "box", size=" ".join(f"{value:.12g}" for value in size))
    return sim_root


def _add_motor(link: ET.Element, motor: dict[str, float]) -> None:
    inertial = link.find("inertial")
    if inertial is None:
        raise ValueError(f"Missing structural inertial for {link.get('name')}")

    origin = inertial.find("origin")
    mass_element = inertial.find("mass")
    inertia_element = inertial.find("inertia")
    structural_mass = float(mass_element.get("value"))
    structural_com = _vector(origin.get("xyz"))
    structural_inertia = _inertia_matrix(inertia_element.attrib)

    motor_mass = motor["mass"]
    motor_com = np.zeros(3)
    combined_mass = structural_mass + motor_mass
    combined_com = (
        structural_mass * structural_com + motor_mass * motor_com
    ) / combined_mass

    combined_inertia = (
        structural_inertia
        + _parallel_axis(structural_mass, structural_com - combined_com)
        + _motor_inertia(motor_mass, motor["diameter"] / 2.0, motor["length"])
        + _parallel_axis(motor_mass, motor_com - combined_com)
    )

    origin.set("xyz", " ".join(f"{value:.12g}" for value in combined_com))
    mass_element.set("value", f"{combined_mass:.12g}")
    inertia_element.attrib.update(
        {
            "ixx": f"{combined_inertia[0, 0]:.12g}",
            "ixy": f"{combined_inertia[0, 1]:.12g}",
            "ixz": f"{combined_inertia[0, 2]:.12g}",
            "iyy": f"{combined_inertia[1, 1]:.12g}",
            "iyz": f"{combined_inertia[1, 2]:.12g}",
            "izz": f"{combined_inertia[2, 2]:.12g}",
        }
    )


def main() -> None:
    root = ET.parse(SOURCE_URDF).getroot()
    root.set("name", "gluon_2L6_4L3")

    # The source is mounted horizontally for a dual-arm robot. Rotate the complete
    # mechanism about world Y so its first link offset points upward.
    world_joint = root.find("joint[@name='world_joint']")
    world_joint.find("origin").set("rpy", "0 -1.57079632679 0")

    for joint_name, (lower, upper) in JOINT_SOFT_LIMITS_RAD.items():
        limit = root.find(f"joint[@name='{joint_name}']/limit")
        limit.set("lower", f"{lower:.9f}")
        limit.set("upper", f"{upper:.9f}")

    # Re-zero joint 2: q_new = 0 represents q_source = +pi/2.  Since the
    # source axis is (0, 0, -1), post-compose the source joint origin with
    # that +pi/2 axis rotation. Measured limits are applied above.
    joint_2 = root.find("joint[@name='axis_joint_2']")
    joint_2.find("origin").set("rpy", "3.14159265359 -1.57079632679 0")

    for link in root.findall("link"):
        name = link.get("name")
        if name in MOTORS:
            _add_motor(link, MOTORS[name])

        for index, material in enumerate(link.findall("visual/material")):
            if not material.get("name", "").strip():
                material.set("name", f"{name}_material_{index}")

        for mesh in link.findall("visual/geometry/mesh") + link.findall(
            "collision/geometry/mesh"
        ):
            source_name = Path(mesh.get("filename")).name
            if source_name[0].isdigit():
                source_name = f"gluon_link_{source_name[0]}.STL"
            mesh.set("filename", f"../meshes/{source_name}")

    ET.indent(root, space="  ")
    ET.ElementTree(root).write(OUTPUT_URDF, encoding="utf-8", xml_declaration=True)
    print(OUTPUT_URDF)

    sim_root = _make_sim_variant(root)
    ET.indent(sim_root, space="  ")
    ET.ElementTree(sim_root).write(SIM_OUTPUT_URDF, encoding="utf-8", xml_declaration=True)
    print(SIM_OUTPUT_URDF)


if __name__ == "__main__":
    main()
