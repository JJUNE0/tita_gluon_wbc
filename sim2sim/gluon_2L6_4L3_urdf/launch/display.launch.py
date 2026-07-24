from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package_share = Path(get_package_share_directory("gluon_2l6_4l3_urdf"))
    robot_description = (
        package_share / "urdf" / "gluon_2L6_4L3.urdf"
    ).read_text(encoding="utf-8")
    robot_description = robot_description.replace(
        "../meshes/", f"file://{package_share}/meshes/"
    )

    return LaunchDescription(
        [
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[{"robot_description": robot_description}],
                output="screen",
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                output="screen",
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                arguments=["-d", str(package_share / "rviz" / "model.rviz")],
                output="screen",
            ),
        ]
    )
