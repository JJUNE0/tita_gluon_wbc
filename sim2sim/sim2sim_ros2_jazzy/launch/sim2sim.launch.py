"""VALIDATION_SIM: python3 sim2sim.launch.py --ckpt trained.pt (or ros2 launch)."""

from pathlib import Path
import sys

PACKAGE = Path(__file__).resolve().parents[1]


def generate_launch_description():
    from launch import LaunchDescription
    from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction
    from launch.substitutions import LaunchConfiguration

    def run(context):
        command = ['python3', str(Path(__file__).resolve()), '--ckpt', LaunchConfiguration('ckpt').perform(context)]
        if LaunchConfiguration('headless').perform(context).lower() == 'true':
            command += ['--headless', '--steps', LaunchConfiguration('steps').perform(context)]
        if LaunchConfiguration('residual_wheel_pd').perform(context).lower() == 'true':
            command += ['--residual_wheel_pd']
        if LaunchConfiguration('fixed_residual_lqr').perform(context).lower() == 'true':
            command += ['--fixed_residual_lqr']
        if LaunchConfiguration('velocity_bias', default='false').perform(context).lower() == 'true':
            command += ['--velocity_bias']
        command += ['--leg_action_filter', LaunchConfiguration('leg_action_filter', default='auto').perform(context)]
        command += ['--leg_notch_hz', LaunchConfiguration('leg_notch_hz', default='8.3').perform(context),
                    '--leg_notch_q', LaunchConfiguration('leg_notch_q', default='3.0').perform(context)]
        return [ExecuteProcess(cmd=command, output='screen', emulate_tty=True)]

    return LaunchDescription([DeclareLaunchArgument('ckpt', description='PPO .pt or FlashSAC actor.pt/model directory'),
                              DeclareLaunchArgument('headless', default_value='true', description='Use direct python launch for interactive keyboard'),
                              DeclareLaunchArgument('steps', default_value='1000'),
                              DeclareLaunchArgument('leg_action_filter', default_value='auto', choices=['auto', 'none', 'ma2_legs', 'ma2_notch_legs']),
                              DeclareLaunchArgument('leg_notch_hz', default_value='8.3'),
                              DeclareLaunchArgument('leg_notch_q', default_value='3.0'),
                              DeclareLaunchArgument('residual_wheel_pd', default_value='false'),
                              DeclareLaunchArgument('fixed_residual_lqr', default_value='false'),
                              DeclareLaunchArgument('velocity_bias', default_value='false',
                                                    description='FlashSAC velocity bias after 2 s zero-command hold'),
                              OpaqueFunction(function=run)])


if __name__ == '__main__':
    sys.path.insert(0, str(PACKAGE))
    from sim2sim_ros2_jazzy.cli import main
    main()
