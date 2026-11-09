"""VALIDATION_SIM: config-selected Teacher + saved250Hz torque residual."""
from pathlib import Path
import sys

PACKAGE = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
CONFIG = REPO/'sim2sim/config/policies.json'


def generate_launch_description():
    from launch import LaunchDescription
    from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction
    from launch.substitutions import LaunchConfiguration

    def run(context):
        command = ['python3', str(Path(__file__).resolve()),
                   '--config', LaunchConfiguration('config').perform(context),
                   '--payload-mass', LaunchConfiguration('payload_mass').perform(context),
                   '--push-force', LaunchConfiguration('push_force').perform(context)]
        for argument, flag in [('ckpt', '--ckpt'), ('residual_ckpt', '--learned-residual')]:
            value = LaunchConfiguration(argument).perform(context)
            if value:
                command += [flag, value]
        cutoff = LaunchConfiguration('lpf').perform(context)
        if cutoff != 'auto':
            command += ['--lpf', cutoff]
        if LaunchConfiguration('headless').perform(context).lower() == 'true':
            command += ['--headless', '--steps', LaunchConfiguration('steps').perform(context)]
        return [ExecuteProcess(cmd=command, output='screen', emulate_tty=True)]

    return LaunchDescription([
        DeclareLaunchArgument('config', default_value=str(CONFIG)),
        DeclareLaunchArgument('ckpt', default_value=''),
        DeclareLaunchArgument('residual_ckpt', default_value=''),
        DeclareLaunchArgument('lpf', default_value='auto', description='Residual-only LPF Hz; auto restores training, 0 bypasses'),
        DeclareLaunchArgument('payload_mass', default_value='2.0'),
        DeclareLaunchArgument('push_force', default_value='20.0'),
        DeclareLaunchArgument('headless', default_value='true'),
        DeclareLaunchArgument('steps', default_value='1000'), OpaqueFunction(function=run)])


if __name__ == '__main__':
    sys.path[:0] = [str(PACKAGE), str(REPO)]
    from sim2sim_ros2_jazzy.cli import main
    main([*sys.argv[1:], '--with-torque-residual'])
