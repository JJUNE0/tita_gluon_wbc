from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    tita_ns_arg = DeclareLaunchArgument("tita_ns", default_value="tita4252763")
    bind_host_arg = DeclareLaunchArgument("bind_host", default_value="0.0.0.0")
    port_arg = DeclareLaunchArgument("port", default_value="50051")
    send_rate_hz_arg = DeclareLaunchArgument("send_rate_hz", default_value="50.0")
    include_motors_status_arg = DeclareLaunchArgument("include_motors_status", default_value="true")
    include_command_arg = DeclareLaunchArgument("include_command", default_value="false")
    include_fsm_arg = DeclareLaunchArgument("include_fsm", default_value="true")
    command_source_arg = DeclareLaunchArgument("command_source", default_value="processed_twist")
    command_timeout_arg = DeclareLaunchArgument("command_timeout_sec", default_value="0.5")
    raw_mapping_confirmed_arg = DeclareLaunchArgument("raw_joy_mapping_confirmed", default_value="false")
    raw_forward_axis_arg = DeclareLaunchArgument("raw_joy_forward_axis", default_value="0")
    raw_lateral_axis_arg = DeclareLaunchArgument("raw_joy_lateral_axis", default_value="-1")
    raw_yaw_axis_arg = DeclareLaunchArgument("raw_joy_yaw_axis", default_value="1")
    raw_forward_scale_arg = DeclareLaunchArgument("raw_joy_forward_scale", default_value="1.0")
    raw_lateral_scale_arg = DeclareLaunchArgument("raw_joy_lateral_scale", default_value="0.0")
    raw_yaw_scale_arg = DeclareLaunchArgument("raw_joy_yaw_scale", default_value="1.0")
    raw_deadzone_arg = DeclareLaunchArgument("raw_joy_deadzone", default_value="0.0013")

    node = Node(
        package="cosim_ros2_jazzy",
        executable="tita_state_relay_sender",
        name="tita_state_relay_sender",
        output="screen",
        parameters=[
            {"tita_ns": LaunchConfiguration("tita_ns")},
            {"bind_host": LaunchConfiguration("bind_host")},
            {"port": LaunchConfiguration("port")},
            {"send_rate_hz": LaunchConfiguration("send_rate_hz")},
            {"include_motors_status": LaunchConfiguration("include_motors_status")},
            {"include_command": LaunchConfiguration("include_command")},
            {"include_fsm": LaunchConfiguration("include_fsm")},
            {"command_source": LaunchConfiguration("command_source")},
            {"command_timeout_sec": LaunchConfiguration("command_timeout_sec")},
            {"raw_joy_mapping_confirmed": LaunchConfiguration("raw_joy_mapping_confirmed")},
            {"raw_joy_forward_axis": LaunchConfiguration("raw_joy_forward_axis")},
            {"raw_joy_lateral_axis": LaunchConfiguration("raw_joy_lateral_axis")},
            {"raw_joy_yaw_axis": LaunchConfiguration("raw_joy_yaw_axis")},
            {"raw_joy_forward_scale": LaunchConfiguration("raw_joy_forward_scale")},
            {"raw_joy_lateral_scale": LaunchConfiguration("raw_joy_lateral_scale")},
            {"raw_joy_yaw_scale": LaunchConfiguration("raw_joy_yaw_scale")},
            {"raw_joy_deadzone": LaunchConfiguration("raw_joy_deadzone")},
        ],
    )

    return LaunchDescription([
        tita_ns_arg, bind_host_arg, port_arg, send_rate_hz_arg, include_motors_status_arg,
        include_command_arg, include_fsm_arg, command_source_arg, command_timeout_arg,
        raw_mapping_confirmed_arg, raw_forward_axis_arg, raw_lateral_axis_arg, raw_yaw_axis_arg,
        raw_forward_scale_arg, raw_lateral_scale_arg, raw_yaw_scale_arg, raw_deadzone_arg, node,
    ])
