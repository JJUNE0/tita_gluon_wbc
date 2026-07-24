from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    defaults = {
        "config": PathJoinSubstitution([FindPackageShare("cosim_ros2_jazzy"), "config", "tita.yaml"]),
        "policy_path": "/home/cocel/Desktop/Research/tita_gluon_wbc/tita_gluon_ws/deploy/tita/policy.onnx",
        "server_host": "192.168.42.1",
        "port": "50051",
        "relay_ns": "tita_relay",
        "command_source": "processed_twist",
        "command_timeout_sec": "0.5",
        "sensor_timeout_sec": "0.5",
        "allowed_real_fsm_modes_csv": "balance",
        "ghost_rollout_enabled": "true",
        "ghost_visualization_mode": "auto",
        "ghost_horizon_sec": "0.5",
        "ghost_reset_rate_hz": "2.0",
        "ghost_base_height": "0.4",
        "kinematic_initial_hold_sec": "1.0",
        "policy_rate_hz": "50.0",
        "viewer": "true",
        "headless": "false",
        "publish_debug": "true",
    }
    declarations = [DeclareLaunchArgument(name, default_value=value) for name, value in defaults.items()]
    receiver = Node(
        package="cosim_ros2_jazzy",
        executable="tita_state_relay_receiver",
        name="tita_state_relay_receiver",
        output="screen",
        parameters=[{
            "server_host": LaunchConfiguration("server_host"),
            "port": LaunchConfiguration("port"),
            "relay_ns": LaunchConfiguration("relay_ns"),
            "publish_original_namespace_aliases": False,
        }],
    )
    ghost = Node(
        package="cosim_ros2_jazzy",
        executable="tita_real_policy_ghost_node",
        name="tita_real_policy_ghost",
        output="screen",
        prefix="python3",
        parameters=[{
            "config": LaunchConfiguration("config"),
            "policy_path": LaunchConfiguration("policy_path"),
            "relay_ns": LaunchConfiguration("relay_ns"),
            "expected_command_source": LaunchConfiguration("command_source"),
            "command_timeout_sec": LaunchConfiguration("command_timeout_sec"),
            "sensor_timeout_sec": LaunchConfiguration("sensor_timeout_sec"),
            "allowed_real_fsm_modes_csv": LaunchConfiguration("allowed_real_fsm_modes_csv"),
            "ghost_rollout_enabled": LaunchConfiguration("ghost_rollout_enabled"),
            "ghost_visualization_mode": LaunchConfiguration("ghost_visualization_mode"),
            "ghost_horizon_sec": LaunchConfiguration("ghost_horizon_sec"),
            "ghost_reset_rate_hz": LaunchConfiguration("ghost_reset_rate_hz"),
            "ghost_base_height": LaunchConfiguration("ghost_base_height"),
            "kinematic_initial_hold_sec": LaunchConfiguration("kinematic_initial_hold_sec"),
            "policy_rate_hz": LaunchConfiguration("policy_rate_hz"),
            "viewer": LaunchConfiguration("viewer"),
            "headless": LaunchConfiguration("headless"),
            "publish_debug": LaunchConfiguration("publish_debug"),
        }],
    )
    return LaunchDescription([*declarations, receiver, ghost])
