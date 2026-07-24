from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import ExecuteProcess
from launch.actions import LogInfo
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import PackageNotFoundError
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    config_arg = DeclareLaunchArgument(
        "config",
        default_value=PathJoinSubstitution([FindPackageShare("cosim_ros2_jazzy"), "config", "tita.yaml"]),
        description="Path to TITA MuJoCo sim-to-sim YAML config.",
    )
    tita_ns_arg = DeclareLaunchArgument(
        "tita_ns",
        default_value="tita",
        description="Manual-compatible TITA namespace for command-manager topics.",
    )
    viewer_arg = DeclareLaunchArgument(
        "viewer",
        default_value="true",
        description="Enable MuJoCo passive viewer.",
    )
    plot_arg = DeclareLaunchArgument(
        "plot",
        default_value="false",
        description="Enable lightweight plot topics and optionally launch PlotJuggler.",
    )
    joystick_arg = DeclareLaunchArgument(
        "joystick",
        default_value="false",
        description="Launch the /joy to command-manager bridge.",
    )
    keyboard_arg = DeclareLaunchArgument(
        "keyboard",
        default_value="false",
        description="Launch the keyboard command node for manual sim control.",
    )

    node = Node(
        package="cosim_ros2_jazzy",
        executable="mujoco_policy_node",
        name="cosim_ros2_jazzy",
        output="screen",
        # ament_python generated entrypoints may have a system-python shebang.
        # Running through python3 lets an activated venv provide mujoco/onnxruntime.
        prefix="python3",
        parameters=[
            {"config": LaunchConfiguration("config")},
            {"viewer": LaunchConfiguration("viewer")},
            {"plot": LaunchConfiguration("plot")},
            {"tita_ns": LaunchConfiguration("tita_ns")},
        ],
    )

    joy_bridge = Node(
        package="cosim_ros2_jazzy",
        executable="tita_joy_bridge_node",
        name="tita_joy_bridge",
        output="screen",
        prefix="python3",
        parameters=[{"tita_ns": LaunchConfiguration("tita_ns")}],
        condition=IfCondition(LaunchConfiguration("joystick")),
    )

    keyboard_node = Node(
        package="cosim_ros2_jazzy",
        executable="keyboard_command_node",
        name="cosim_keyboard_command",
        output="screen",
        prefix="python3",
        emulate_tty=True,
        parameters=[{"tita_ns": LaunchConfiguration("tita_ns")}],
        condition=IfCondition(LaunchConfiguration("keyboard")),
    )

    try:
        get_package_share_directory("plotjuggler")
        plot_action = ExecuteProcess(
            cmd=["ros2", "run", "plotjuggler", "plotjuggler"],
            output="screen",
            condition=IfCondition(LaunchConfiguration("plot")),
        )
    except PackageNotFoundError:
        plot_action = LogInfo(
            msg="PlotJuggler is not installed. Install it with: sudo apt install ros-jazzy-plotjuggler-ros",
            condition=IfCondition(LaunchConfiguration("plot")),
        )

    return LaunchDescription(
        [config_arg, tita_ns_arg, viewer_arg, plot_arg, joystick_arg, keyboard_arg, node, joy_bridge, keyboard_node, plot_action]
    )
