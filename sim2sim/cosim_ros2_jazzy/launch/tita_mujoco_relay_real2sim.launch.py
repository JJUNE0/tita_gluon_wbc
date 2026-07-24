from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    config_arg = DeclareLaunchArgument(
        "config",
        default_value=PathJoinSubstitution([FindPackageShare("cosim_ros2_jazzy"), "config", "tita.yaml"]),
        description="Path to the TITA MuJoCo config used for relay-driven real-to-sim mirror.",
    )
    server_host_arg = DeclareLaunchArgument("server_host", default_value="192.168.42.1")
    port_arg = DeclareLaunchArgument("port", default_value="50051")
    relay_ns_arg = DeclareLaunchArgument("relay_ns", default_value="tita_relay")
    real_tita_ns_arg = DeclareLaunchArgument("real_tita_ns", default_value="tita4252763")
    viewer_arg = DeclareLaunchArgument("viewer", default_value="true")
    mirror_base_orientation_arg = DeclareLaunchArgument("mirror_base_orientation", default_value="true")
    mirror_base_position_arg = DeclareLaunchArgument("mirror_base_position", default_value="false")
    publish_debug_arg = DeclareLaunchArgument("publish_debug", default_value="true")
    publish_aliases_arg = DeclareLaunchArgument(
        "publish_original_namespace_aliases", default_value="false"
    )

    receiver = Node(
        package="cosim_ros2_jazzy",
        executable="tita_state_relay_receiver",
        name="tita_state_relay_receiver",
        output="screen",
        parameters=[
            {"server_host": LaunchConfiguration("server_host")},
            {"port": LaunchConfiguration("port")},
            {"relay_ns": LaunchConfiguration("relay_ns")},
            {"publish_original_namespace_aliases": LaunchConfiguration("publish_original_namespace_aliases")},
        ],
    )

    mirror = Node(
        package="cosim_ros2_jazzy",
        executable="tita_mujoco_real2sim_node",
        name="tita_mujoco_relay_real2sim",
        output="screen",
        prefix="python3",
        parameters=[
            {"config": LaunchConfiguration("config")},
            {"viewer": LaunchConfiguration("viewer")},
            {"real_tita_ns": LaunchConfiguration("real_tita_ns")},
            {"mirror_base_orientation": LaunchConfiguration("mirror_base_orientation")},
            {"mirror_base_position": LaunchConfiguration("mirror_base_position")},
            {"publish_debug": LaunchConfiguration("publish_debug")},
            {"use_state_relay": True},
            {"relay_ns": LaunchConfiguration("relay_ns")},
        ],
    )

    return LaunchDescription(
        [
            config_arg,
            server_host_arg,
            port_arg,
            relay_ns_arg,
            real_tita_ns_arg,
            viewer_arg,
            mirror_base_orientation_arg,
            mirror_base_position_arg,
            publish_debug_arg,
            publish_aliases_arg,
            receiver,
            mirror,
        ]
    )
