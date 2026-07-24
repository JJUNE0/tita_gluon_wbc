import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def _launch_setup(context):
    requested_stage = int(LaunchConfiguration("requested_stage").perform(context))
    if requested_stage not in (1, 2):
        raise RuntimeError("Only Stage 1 stand or Stage 2 joystick RL is supported")
    token_path = LaunchConfiguration("takeover_token_file").perform(context)
    if not token_path or not os.path.isfile(token_path):
        raise RuntimeError("A supervisor-created Stage 1 takeover token is required")
    with open(token_path, "r", encoding="utf-8") as token_file:
        expected_token = {1: "DIRECT_STAGE1_ARMED", 2: "DIRECT_STAGE2_ARMED"}[requested_stage]
        if token_file.read().strip() != expected_token:
            raise RuntimeError("Invalid stage-specific takeover token")
    # Consume the supervisor token before creating any hardware process. A stale token cannot be
    # replayed to start a second controller_manager in the same powered session.
    os.unlink(token_path)

    description_path = os.path.join(
        get_package_share_directory("tita_description"), "xacro", "robot.xacro"
    )
    robot_description = xacro.process_file(
        description_path,
        mappings={
            "hw_env": "hw",
            "hardware_output_enabled": "true",
            "wheel_effort_limit": "12.0" if requested_stage == 2 else "20.0",
        },
    ).toxml()
    controller_config = os.path.join(
        get_package_share_directory("tita_stage1_controller"),
        "config",
        "tita_stage2_controllers.yaml" if requested_stage == 2 else "tita_stage1_controllers.yaml",
    )
    controller_parameters = [{"robot_description": robot_description}, controller_config]
    manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        output="both",
        parameters=controller_parameters,
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
    stage1 = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["tita_stage1_controller", "--controller-manager", "/controller_manager"],
    )
    processes = [manager, state_publisher, joint_broadcaster, imu_broadcaster, stage1]
    if requested_stage == 2:
        direct_joy = Node(
            package="teleop_command",
            executable="teleop_command_node",
            name="direct_joy_reader",
            namespace="tita4252763",
            output="both",
            parameters=[{
                "uart_interface": "/dev/ttyTHS1",
                "update_rate": 10,
                "use_sdk": False,
                "joy_only": True,
                "receive_only": True,
                "joystick_deadzone": 0.013,
                "speed_ratio": [0.33, 0.66, 1.0],
                "max_twist_linear": 3.0,
                "max_twist_angular": 6.0,
            }],
        )
        processes.insert(0, direct_joy)
    return processes


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "takeover_token_file",
                default_value="",
                description="One-time token created only by the armed takeover supervisor.",
            ),
            DeclareLaunchArgument(
                "requested_stage",
                default_value="1",
                description="1=TransformUp plus five-second stand; 2=direct native-policy joystick RL",
            ),
            OpaqueFunction(function=_launch_setup),
        ]
    )
