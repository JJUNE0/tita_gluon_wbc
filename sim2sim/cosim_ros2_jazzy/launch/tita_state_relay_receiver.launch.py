from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    server_host_arg = DeclareLaunchArgument("server_host", default_value="192.168.42.1")
    port_arg = DeclareLaunchArgument("port", default_value="50051")
    reconnect_sec_arg = DeclareLaunchArgument("reconnect_sec", default_value="1.0")
    publish_original_namespace_aliases_arg = DeclareLaunchArgument(
        "publish_original_namespace_aliases", default_value="false"
    )
    relay_ns_arg = DeclareLaunchArgument("relay_ns", default_value="tita_relay")

    node = Node(
        package="cosim_ros2_jazzy",
        executable="tita_state_relay_receiver",
        name="tita_state_relay_receiver",
        output="screen",
        parameters=[
            {"server_host": LaunchConfiguration("server_host")},
            {"port": LaunchConfiguration("port")},
            {"reconnect_sec": LaunchConfiguration("reconnect_sec")},
            {"publish_original_namespace_aliases": LaunchConfiguration("publish_original_namespace_aliases")},
            {"relay_ns": LaunchConfiguration("relay_ns")},
        ],
    )

    return LaunchDescription(
        [server_host_arg, port_arg, reconnect_sec_arg, publish_original_namespace_aliases_arg, relay_ns_arg, node]
    )
