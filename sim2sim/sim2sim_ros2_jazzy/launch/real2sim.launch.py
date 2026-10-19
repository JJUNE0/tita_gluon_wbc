"""ROBOT_READ_ONLY: subscribe to TITA state and mirror it in MuJoCo."""

from pathlib import Path


def generate_launch_description():
    from launch import LaunchDescription
    from launch.actions import DeclareLaunchArgument
    from launch.substitutions import LaunchConfiguration
    from launch_ros.actions import Node
    from launch_ros.parameter_descriptions import ParameterValue
    defaults = {'config': str(Path(__file__).resolve().parents[1] / 'config/tita.yaml'),
                'real_tita_ns': 'tita4252763', 'viewer': 'true',
                'mirror_base_orientation': 'true', 'mirror_base_position': 'false'}
    parameters = {name: ParameterValue(LaunchConfiguration(name), value_type=bool if default in ('true', 'false') else str)
                  for name, default in defaults.items()}
    python = str(Path.home() / 'venvs/cosim_ros2_jazzy/bin/python')
    return LaunchDescription([*[DeclareLaunchArgument(name, default_value=default) for name, default in defaults.items()],
                              Node(package='sim2sim_ros2_jazzy', executable='real2sim', prefix=python,
                                   parameters=[parameters], output='screen')])
