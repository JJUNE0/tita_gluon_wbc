#!/usr/bin/env python3
"""Generate the static TITA + jig + upright GLUON 2L6-4L3 URDF."""

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET


def prefix_model(root: ET.Element, prefix: str) -> None:
    for link in root.findall("link"):
        link.set("name", prefix + link.get("name", ""))
    for joint in root.findall("joint"):
        joint.set("name", prefix + joint.get("name", ""))
        parent = joint.find("parent")
        child = joint.find("child")
        if parent is not None:
            parent.set("link", prefix + parent.get("link", ""))
        if child is not None:
            child.set("link", prefix + child.get("link", ""))


def make_jig_link(
    size: tuple[float, float, float], mass: float = 1.0
) -> ET.Element:
    link = ET.Element("link", {"name": "mount_jig_2L6_4L3"})
    size_x, size_y, size_z = size
    inertial = ET.SubElement(link, "inertial")
    ET.SubElement(inertial, "origin", {"xyz": "0 0 0", "rpy": "0 0 0"})
    ET.SubElement(inertial, "mass", {"value": f"{mass:.12g}"})
    ET.SubElement(
        inertial,
        "inertia",
        {
            "ixx": f"{mass * (size_y**2 + size_z**2) / 12.0:.12g}",
            "ixy": "0",
            "ixz": "0",
            "iyy": f"{mass * (size_x**2 + size_z**2) / 12.0:.12g}",
            "iyz": "0",
            "izz": f"{mass * (size_x**2 + size_y**2) / 12.0:.12g}",
        },
    )
    for element_name in ("visual", "collision"):
        element = ET.SubElement(link, element_name)
        ET.SubElement(element, "origin", {"xyz": "0 0 0", "rpy": "0 0 0"})
        geometry = ET.SubElement(element, "geometry")
        ET.SubElement(geometry, "box", {"size": " ".join(map(str, size))})
        if element_name == "visual":
            material = ET.SubElement(element, "material", {"name": "jig_gray"})
            ET.SubElement(material, "color", {"rgba": "0.35 0.35 0.38 1"})
    return link


def make_fixed_joint(
    name: str,
    parent: str,
    child: str,
    xyz: tuple[float, float, float],
    rpy: str = "0 0 0",
) -> ET.Element:
    joint = ET.Element("joint", {"name": name, "type": "fixed"})
    ET.SubElement(joint, "origin", {"xyz": " ".join(map(str, xyz)), "rpy": rpy})
    ET.SubElement(joint, "parent", {"link": parent})
    ET.SubElement(joint, "child", {"link": child})
    return joint


def replace_tita_mesh_paths(root: ET.Element) -> None:
    source = "package://tita_gluon_urdf/meshes/tita/"
    destination = "../meshes/tita/"
    for mesh in root.iter("mesh"):
        filename = mesh.get("filename", "")
        if filename.startswith(source):
            mesh.set("filename", filename.replace(source, destination, 1))


def main() -> None:
    package_dir = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--gluon-z", type=float, default=0.1564)
    parser.add_argument("--jig-x", type=float, default=0.12)
    parser.add_argument("--jig-y", type=float, default=0.12)
    parser.add_argument("--jig-height", type=float, default=0.03)
    parser.add_argument(
        "--output",
        type=Path,
        default=package_dir / "urdf" / "tita_gluon_2L6_4L3.urdf",
    )
    args = parser.parse_args()

    tita_root = ET.parse(package_dir / "urdf" / "tita.urdf").getroot()
    gluon_root = ET.parse(package_dir / "urdf" / "gluon_2L6_4L3.urdf").getroot()
    source_world_joint = gluon_root.find("joint[@name='world_joint']")
    source_root_rpy = source_world_joint.find("origin").get("rpy")
    gluon_root.remove(source_world_joint)
    gluon_root.remove(gluon_root.find("link[@name='world']"))
    prefix_model(gluon_root, "gluon_2L6_4L3_")

    jig_name = "mount_jig_2L6_4L3"
    tita_root.set("name", "tita_gluon_2L6_4L3")
    tita_root.append(make_jig_link((args.jig_x, args.jig_y, args.jig_height)))
    tita_root.append(
        make_fixed_joint(
            "tita_to_mount_jig_2L6_4L3",
            "base_link",
            jig_name,
            (0.0, 0.0, args.gluon_z - args.jig_height / 2.0),
        )
    )
    for element in list(gluon_root):
        tita_root.append(element)
    tita_root.append(
        make_fixed_joint(
            "mount_jig_to_gluon_2L6_4L3",
            jig_name,
            "gluon_2L6_4L3_base_link",
            (0.0, 0.0, args.jig_height / 2.0),
            source_root_rpy,
        )
    )
    replace_tita_mesh_paths(tita_root)
    ET.indent(tita_root, space="  ")
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(tita_root).write(output, encoding="utf-8", xml_declaration=True)
    print(output)


if __name__ == "__main__":
    main()
