from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    config = DeclareLaunchArgument(
        "config",
        default_value=PathJoinSubstitution([FindPackageShare("tita_low_level_sdk"), "config", "tita_dryrun.yaml"]),
    )
    arguments = [
        ("tita_ns", "tita4252763"),
        ("policy_path", "/home/robot/tita_policy/policy.onnx"),
        ("policy_enabled", "true"),
        ("policy_required", "false"),
        ("rate_hz", "50.0"),
        ("publish_debug", "true"),
    ]
    declarations = [DeclareLaunchArgument(name, default_value=default) for name, default in arguments]
    overrides = {name: LaunchConfiguration(name) for name, _ in arguments}
    node = Node(
        package="tita_low_level_sdk",
        executable="dryrun_node",
        name="tita_lowlevel_dryrun",
        output="screen",
        parameters=[LaunchConfiguration("config"), overrides],
    )
    return LaunchDescription([config, *declarations, node])
