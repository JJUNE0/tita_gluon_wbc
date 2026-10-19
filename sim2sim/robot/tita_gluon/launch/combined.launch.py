from pathlib import Path
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def _prefix_model(root: ET.Element, prefix: str) -> None:
    """Prefix links, joints, and their references to avoid name collisions."""
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


def _make_link(name: str, size: tuple[float, float, float]) -> ET.Element:
    link = ET.Element("link", {"name": name})
    for element_name in ("visual", "collision"):
        element = ET.SubElement(link, element_name)
        ET.SubElement(element, "origin", {"xyz": "0 0 0", "rpy": "0 0 0"})
        geometry = ET.SubElement(element, "geometry")
        ET.SubElement(geometry, "box", {"size": " ".join(map(str, size))})
        if element_name == "visual":
            material = ET.SubElement(element, "material", {"name": "jig_gray"})
            ET.SubElement(material, "color", {"rgba": "0.35 0.35 0.38 1"})
    return link


def _make_fixed_joint(
    name: str, parent: str, child: str, xyz: tuple[float, float, float]
) -> ET.Element:
    joint = ET.Element("joint", {"name": name, "type": "fixed"})
    ET.SubElement(joint, "origin", {"xyz": " ".join(map(str, xyz)), "rpy": "0 0 0"})
    ET.SubElement(joint, "parent", {"link": parent})
    ET.SubElement(joint, "child", {"link": child})
    return joint


def _launch_setup(context, package_share: Path):
    gluon_z = float(LaunchConfiguration("gluon_z").perform(context))
    jig_x = float(LaunchConfiguration("jig_x").perform(context))
    jig_y = float(LaunchConfiguration("jig_y").perform(context))
    jig_height = float(LaunchConfiguration("jig_height").perform(context))

    tita_share = Path(get_package_share_directory("tita_urdf"))
    gluon_share = Path(get_package_share_directory("gluon_2l6_4l3_urdf"))
    tita_root = ET.parse(tita_share / "urdf" / "tita.urdf").getroot()
    gluon_root = ET.parse(gluon_share / "urdf" / "gluon.urdf").getroot()
    for root, share in ((tita_root, tita_share), (gluon_root, gluon_share)):
        for mesh in root.iter("mesh"):
            filename = mesh.get("filename").replace("../meshes/", f"file://{share}/meshes/")
            mesh.set("filename", filename)
    _prefix_model(gluon_root, "gluon_")

    tita_root.set("name", "tita_gluon")
    tita_root.append(_make_link("mount_jig", (jig_x, jig_y, jig_height)))
    tita_root.append(
        _make_fixed_joint(
            "tita_to_mount_jig",
            "base_link",
            "mount_jig",
            (0.0, 0.0, gluon_z - jig_height / 2.0),
        )
    )
    for element in list(gluon_root):
        tita_root.append(element)
    tita_root.append(
        _make_fixed_joint(
            "mount_jig_to_gluon",
            "mount_jig",
            "gluon_dummy",
            (0.0, 0.0, jig_height / 2.0),
        )
    )

    robot_description = ET.tostring(tita_root, encoding="unicode")
    return [
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_description}],
            output="screen",
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            condition=IfCondition(LaunchConfiguration("use_gui")),
            output="screen",
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            arguments=["-d", str(package_share / "rviz" / "model.rviz")],
            output="screen",
        ),
    ]


def generate_launch_description():
    package_share = Path(get_package_share_directory("tita_gluon_urdf"))
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "gluon_z",
                default_value="0.1564",
                description="Gluon base origin height in the TITA base_link frame [m].",
            ),
            DeclareLaunchArgument("jig_x", default_value="0.12"),
            DeclareLaunchArgument("jig_y", default_value="0.12"),
            DeclareLaunchArgument("jig_height", default_value="0.03"),
            DeclareLaunchArgument("use_gui", default_value="true"),
            OpaqueFunction(function=_launch_setup, args=[package_share]),
        ]
    )
