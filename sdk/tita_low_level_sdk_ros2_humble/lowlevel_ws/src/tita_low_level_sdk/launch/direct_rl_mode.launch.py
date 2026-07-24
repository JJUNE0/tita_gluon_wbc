from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    config = DeclareLaunchArgument(
        "config",
        default_value=PathJoinSubstitution(
            [FindPackageShare("tita_low_level_sdk"), "config", "direct_rl_mode.yaml"]
        ),
    )
    safe_defaults = [
        ("execute_vendor_stop", "false"),
        ("execute_start_bash", "false"),
        ("enable_hardware_output", "false"),
        ("operator_arm", "false"),
        ("auto_enter_rl", "false"),
        ("direct_soak_only", "false"),
        ("respawn", "false"),
        ("requested_stage", "1"),
        ("power_session_id", ""),
        ("emergency_procedure_confirmed", "false"),
    ]
    declarations = [DeclareLaunchArgument(name, default_value=value) for name, value in safe_defaults]
    overrides = {name: LaunchConfiguration(name) for name, _ in safe_defaults if name != "respawn"}
    node = Node(
        package="tita_low_level_sdk",
        executable="direct_rl_controller_node",
        name="tita_direct_rl_controller",
        output="screen",
        parameters=[LaunchConfiguration("config"), overrides],
        respawn=False,
    )
    return LaunchDescription(
        [
            config,
            *declarations,
            LogInfo(
                msg=(
                    "Direct RL launch starts command-free and unarmed. Launch arguments do not "
                    "authorize takeover; READY-state operator_arm is a separate gate."
                )
            ),
            node,
        ]
    )
