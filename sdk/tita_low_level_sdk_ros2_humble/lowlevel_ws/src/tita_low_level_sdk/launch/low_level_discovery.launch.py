from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    arguments = [
        ("tita_ns", "tita4252763"),
        ("output_root", "~/tita_lowlevel_debug"),
        ("source_root", "~/tita-sdk/src"),
    ]
    declarations = [DeclareLaunchArgument(name, default_value=default) for name, default in arguments]
    node = Node(
        package="tita_low_level_sdk",
        executable="low_level_discovery",
        output="screen",
        arguments=[
            "--tita-ns", LaunchConfiguration("tita_ns"),
            "--output-root", LaunchConfiguration("output_root"),
            "--source-root", LaunchConfiguration("source_root"),
        ],
    )
    return LaunchDescription([*declarations, node])
