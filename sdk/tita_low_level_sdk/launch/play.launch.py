from pathlib import Path

from launch import LaunchDescription
from launch.actions import LogInfo
from launch_ros.actions import Node


def _power_session_id() -> str:
    try:
        return Path("/proc/sys/kernel/random/boot_id").read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def generate_launch_description():
    config = "/home/robot/tita_ws/install/tita_low_level_sdk/share/tita_low_level_sdk/config/direct_rl_mode.yaml"
    node = Node(
        package="tita_low_level_sdk",
        executable="direct_rl_controller_node",
        name="tita_direct_rl_controller",
        output="screen",
        parameters=[
            config,
            {
                "execute_vendor_stop": True,
                "execute_start_bash": True,
                "enable_hardware_output": True,
                "operator_arm": False,
                "auto_enter_rl": False,
                "direct_soak_only": False,
                # Stage 2 is the direct native-policy joystick path.
                "requested_stage": 2,
                "power_session_id": _power_session_id(),
                "emergency_procedure_confirmed": True,
            },
        ],
        respawn=False,
    )
    estimator_logger = Node(
        package="tita_low_level_sdk",
        executable="estimator_diagnostic_logger",
        name="tita_estimator_diagnostic_logger",
        output="screen",
        parameters=[
            {
                "policy_sha256": "6bcd8c4028507dc636f58eee64ad9cfb9c7cc2d948889df4217ba91ba9e8a121",
                "output_root": "/home/robot/tita_ws/runs/estimator",
            }
        ],
        respawn=False,
    )
    return LaunchDescription(
        [
            LogInfo(
                msg=(
                    "TITA play starts unarmed. Stage 1 is TransformUp plus five-second stand; "
                    "Stage 2 switches directly to native-policy joystick RL with a 0.5 units/s "
                    "command ramp and fixed 0.5 s stop. A read-only 50 Hz estimator CSV logger is "
                    "enabled. One explicit operator_arm is still required."
                )
            ),
            estimator_logger,
            node,
        ]
    )
