from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction, TimerAction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def _validate_bag_path(context, *args, **kwargs):
    bag_path = LaunchConfiguration("bag_path").perform(context).strip()
    if not bag_path:
        raise RuntimeError("Launch argument 'bag_path' is required for offline real2sim playback.")
    return []


def generate_launch_description():
    config_arg = DeclareLaunchArgument(
        "config",
        default_value=PathJoinSubstitution([FindPackageShare("cosim_ros2_jazzy"), "config", "tita.yaml"]),
        description="Path to the TITA MuJoCo config used for the real-to-sim mirror.",
    )
    bag_path_arg = DeclareLaunchArgument(
        "bag_path",
        default_value="",
        description="Path to a TITA rosbag directory that contains joint_states, imu, and odometry.",
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
    loop_arg = DeclareLaunchArgument(
        "loop",
        default_value="true",
        description="Loop the rosbag so the offline mirror keeps running.",
    )
    play_rate_arg = DeclareLaunchArgument(
        "play_rate",
        default_value="1.0",
        description="Playback rate for rosbag replay.",
    )

    node = Node(
        package="cosim_ros2_jazzy",
        executable="tita_mujoco_real2sim_node",
        name="tita_mujoco_real2sim_offline",
        output="screen",
        prefix="python3",
        parameters=[
            {"config": LaunchConfiguration("config")},
            {"viewer": LaunchConfiguration("viewer")},
            {"real_tita_ns": "tita4252763"},
            {"mirror_base_orientation": LaunchConfiguration("mirror_base_orientation")},
            {"mirror_base_position": LaunchConfiguration("mirror_base_position")},
            {"publish_debug": LaunchConfiguration("publish_debug")},
        ],
    )

    bag_play_loop = ExecuteProcess(
        cmd=[
            "ros2",
            "bag",
            "play",
            LaunchConfiguration("bag_path"),
            "--clock",
            "--rate",
            LaunchConfiguration("play_rate"),
            "--loop",
        ],
        output="screen",
        condition=IfCondition(LaunchConfiguration("loop")),
    )

    bag_play_once = ExecuteProcess(
        cmd=[
            "ros2",
            "bag",
            "play",
            LaunchConfiguration("bag_path"),
            "--clock",
            "--rate",
            LaunchConfiguration("play_rate"),
        ],
        output="screen",
        condition=UnlessCondition(LaunchConfiguration("loop")),
    )

    return LaunchDescription(
        [
            config_arg,
            bag_path_arg,
            viewer_arg,
            mirror_base_orientation_arg,
            mirror_base_position_arg,
            publish_debug_arg,
            loop_arg,
            play_rate_arg,
            OpaqueFunction(function=_validate_bag_path),
            node,
            TimerAction(period=1.5, actions=[bag_play_loop, bag_play_once]),
        ]
    )
