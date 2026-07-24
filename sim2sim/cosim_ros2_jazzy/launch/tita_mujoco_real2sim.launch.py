from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    config_arg = DeclareLaunchArgument(
        "config",
        default_value=PathJoinSubstitution([FindPackageShare("cosim_ros2_jazzy"), "config", "tita.yaml"]),
        description="Path to the TITA MuJoCo config used for the real-to-sim mirror.",
    )
    real_tita_ns_arg = DeclareLaunchArgument(
        "real_tita_ns",
        default_value="tita4252763",
        description="Namespace of the read-only real TITA robot topics.",
    )
    viewer_arg = DeclareLaunchArgument(
        "viewer",
        default_value="true",
        description="Enable the MuJoCo passive viewer.",
    )
    mirror_base_orientation_arg = DeclareLaunchArgument(
        "mirror_base_orientation",
        default_value="true",
        description="Mirror real IMU orientation into the MuJoCo base freejoint.",
    )
    mirror_base_position_arg = DeclareLaunchArgument(
        "mirror_base_position",
        default_value="false",
        description="Mirror odometry x/y/z into the MuJoCo base freejoint.",
    )
    publish_debug_arg = DeclareLaunchArgument(
        "publish_debug",
        default_value="true",
        description="Publish lightweight real2sim plot topics.",
    )
    use_state_relay_arg = DeclareLaunchArgument(
        "use_state_relay",
        default_value="false",
        description="Subscribe to relay topics instead of direct TITA DDS topics.",
    )
    relay_ns_arg = DeclareLaunchArgument(
        "relay_ns",
        default_value="tita_relay",
        description="Namespace used by the desktop TCP relay receiver.",
    )

    node = Node(
        package="cosim_ros2_jazzy",
        executable="tita_mujoco_real2sim_node",
        name="tita_mujoco_real2sim",
        output="screen",
        prefix="python3",
        parameters=[
            {"config": LaunchConfiguration("config")},
            {"viewer": LaunchConfiguration("viewer")},
            {"real_tita_ns": LaunchConfiguration("real_tita_ns")},
            {"mirror_base_orientation": LaunchConfiguration("mirror_base_orientation")},
            {"mirror_base_position": LaunchConfiguration("mirror_base_position")},
            {"publish_debug": LaunchConfiguration("publish_debug")},
            {"use_state_relay": LaunchConfiguration("use_state_relay")},
            {"relay_ns": LaunchConfiguration("relay_ns")},
        ],
    )

    return LaunchDescription(
        [
            config_arg,
            real_tita_ns_arg,
            viewer_arg,
            mirror_base_orientation_arg,
            mirror_base_position_arg,
            publish_debug_arg,
            use_state_relay_arg,
            relay_ns_arg,
            node,
        ]
    )
