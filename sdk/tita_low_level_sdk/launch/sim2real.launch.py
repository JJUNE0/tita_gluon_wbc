from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    config_arg = DeclareLaunchArgument(
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
        name="tita_lowlevel_sim2real",
        output="screen",
        parameters=[
            LaunchConfiguration("config"),
            overrides,
            {
                "require_motors_status": False,
                "require_fsm_mode": True,
                "policy_fsm_gate_enabled": True,
                "command_enabled": False,
                "allow_command_output": False,
            },
        ],
    )

    start_msg = LogInfo(
        msg=(
            "sim2real starts in read-only mode. "
            "No robot-state-changing action is registered; command output is disabled."
        )
    )

    return LaunchDescription([config_arg, *declarations, start_msg, node])
