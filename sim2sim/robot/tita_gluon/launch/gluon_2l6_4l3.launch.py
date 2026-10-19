from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_share = Path(get_package_share_directory("tita_gluon_urdf"))
    model_share = Path(get_package_share_directory("gluon_2l6_4l3_urdf"))
    robot_description = (model_share / "urdf" / "gluon_2L6_4L3_assembly.urdf").read_text(encoding="utf-8")
    robot_description = robot_description.replace("../meshes/", f"file://{model_share}/meshes/")
    use_gui = LaunchConfiguration("use_gui")
    return LaunchDescription([
        DeclareLaunchArgument("use_gui", default_value="true"),
        Node(package="robot_state_publisher", executable="robot_state_publisher", parameters=[{"robot_description": robot_description}], output="screen"),
        Node(package="joint_state_publisher_gui", executable="joint_state_publisher_gui", condition=IfCondition(use_gui), output="screen"),
        Node(package="rviz2", executable="rviz2", arguments=["-d", str(package_share / "rviz" / "model.rviz")], output="screen"),
    ])
