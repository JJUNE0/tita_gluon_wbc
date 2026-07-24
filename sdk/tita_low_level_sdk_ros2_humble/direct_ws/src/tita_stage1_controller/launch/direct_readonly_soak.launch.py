import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def _launch_setup(context):
    token_path = LaunchConfiguration("soak_token_file").perform(context)
    if not token_path or not os.path.isfile(token_path):
        raise RuntimeError("A supervisor-created Direct soak token is required")
    with open(token_path, "r", encoding="utf-8") as token_file:
        if token_file.read().strip() != "DIRECT_SOAK_ARMED":
            raise RuntimeError("Invalid Direct soak token")
    os.unlink(token_path)

    description_path = os.path.join(
        get_package_share_directory("tita_description"), "xacro", "robot.xacro"
    )
    # This gate is consumed inside HardwareBridge::write(), below every controller/launch gate.
    # Even an accidentally loaded controller cannot reach a TITA motor API in this launch.
    robot_description = xacro.process_file(
        description_path,
        mappings={"hw_env": "hw", "hardware_output_enabled": "false"},
    ).toxml()
    controller_config = os.path.join(
        get_package_share_directory("tita_stage1_controller"),
        "config",
        "tita_stage1_controllers.yaml",
    )
    manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        output="both",
        parameters=[{"robot_description": robot_description}, controller_config],
    )
    state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[{"robot_description": robot_description}],
    )
    joint_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )
    imu_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["imu_sensor_broadcaster", "--controller-manager", "/controller_manager"],
    )
    # Stage1Controller is deliberately not loaded or activated in soak mode.
    return [manager, state_publisher, joint_broadcaster, imu_broadcaster]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "soak_token_file",
                default_value="",
                description="One-time token created only after an approved vendor shutdown.",
            ),
            LogInfo(
                msg=(
                    "DIRECT READ-ONLY SOAK: start.bash is not executed, Stage1Controller is not "
                    "activated, and HardwareBridge motor API output is disabled."
                )
            ),
            OpaqueFunction(function=_launch_setup),
        ]
    )
