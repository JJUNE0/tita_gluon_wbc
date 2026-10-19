#!/usr/bin/env python3
"""Generate a static combined TITA + mounting jig + Gluon URDF."""

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


def make_jig_link(size: tuple[float, float, float]) -> ET.Element:
    link = ET.Element("link", {"name": "mount_jig"})
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
    name: str, parent: str, child: str, xyz: tuple[float, float, float]
) -> ET.Element:
    joint = ET.Element("joint", {"name": name, "type": "fixed"})
    ET.SubElement(joint, "origin", {"xyz": " ".join(map(str, xyz)), "rpy": "0 0 0"})
    ET.SubElement(joint, "parent", {"link": parent})
    ET.SubElement(joint, "child", {"link": child})
    return joint


def replace_mesh_paths(root: ET.Element, model: str) -> None:
    for mesh in root.iter("mesh"):
        filename = mesh.get("filename", "")
        mesh.set("filename", filename.replace("../meshes/", f"../../{model}/meshes/", 1))


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
        default=package_dir / "urdf" / "tita_gluon.urdf",
    )
    args = parser.parse_args()

    tita_root = ET.parse(package_dir.parent / "tita" / "urdf" / "tita.urdf").getroot()
    gluon_root = ET.parse(package_dir.parent / "gluon" / "urdf" / "gluon.urdf").getroot()
    replace_mesh_paths(tita_root, "tita")
    replace_mesh_paths(gluon_root, "gluon")
    prefix_model(gluon_root, "gluon_")

    tita_root.set("name", "tita_gluon")
    tita_root.append(make_jig_link((args.jig_x, args.jig_y, args.jig_height)))
    tita_root.append(
        make_fixed_joint(
            "tita_to_mount_jig",
            "base_link",
            "mount_jig",
            (0.0, 0.0, args.gluon_z - args.jig_height / 2.0),
        )
    )
    for element in list(gluon_root):
        tita_root.append(element)
    tita_root.append(
        make_fixed_joint(
            "mount_jig_to_gluon",
            "mount_jig",
            "gluon_dummy",
            (0.0, 0.0, args.jig_height / 2.0),
        )
    )
    ET.indent(tita_root, space="  ")

    args.output = args.output.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(tita_root).write(
        args.output, encoding="utf-8", xml_declaration=True
    )
    print(args.output)


if __name__ == "__main__":
    main()
