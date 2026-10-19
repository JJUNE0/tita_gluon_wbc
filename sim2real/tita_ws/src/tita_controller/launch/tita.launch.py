"""ROBOT: ros2 launch tita_controller tita.launch.py policy_dir:=<model>/sim2sim/actor [output_enabled:=true]

policy_dir is the folder sim2sim exports (config.json + policy.onnx). Motor output is off by default.
"""

import json
import math
from pathlib import Path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

NATIVE_JOINTS = [f'joint_{side}_leg_{index}' for side in ('left', 'right') for index in range(1, 5)]
# Same order as ObsKind in adapter.hpp.
OBS_KINDS = ['ang_vel', 'gravity', 'commands', 'joint_pos', 'joint_vel', 'last_action', 'zero', 'wheel_position_error',
             'heading_error']
BIG = 1e9  # stands in for "no clip"


def policy_parameters(policy_dir):
    """Flatten config.json into one entry per observation element and per action (see adapter.py)."""
    cfg = json.loads((policy_dir / 'config.json').read_text())
    interface, robot = cfg['policy_interface'], cfg['robot']
    obs = {key: [] for key in ('obs_kind', 'obs_index', 'obs_scale', 'obs_low', 'obs_high')}
    position, heading = {}, {}
    for term in interface['observations']:
        if term['kind'] not in OBS_KINDS:
            raise ValueError(f"observation '{term['kind']}' is not available on the robot")
        if term['kind'] == 'wheel_position_error':
            position = {
                'wheel_position_radius': float(term['params']['radius']),
                'wheel_position_clip_m': float(term['params']['clip_m']),
                'wheel_position_zero_thresholds': [float(v) for v in term['params']['zero_thresholds']],
            }
        if term['kind'] == 'heading_error':
            heading = {
                'heading_clip_rad': float(term['params']['clip_rad']),
                'heading_warmup_s': float(term['params']['warmup_s']),
                'heading_zero_thresholds': [float(v) for v in term['params']['zero_thresholds']],
            }
        scale = term['scale'] if isinstance(term['scale'], list) else [term['scale']] * term['size']
        low, high = term['clip'] or (-BIG, BIG)
        for k in range(term['size']):
            index = NATIVE_JOINTS.index(term['joints'][k]) if 'joints' in term else k
            zero = term.get('zero_wheel_pos') and index in (3, 7)
            obs['obs_kind'].append(OBS_KINDS.index('zero' if zero else term['kind']))
            obs['obs_index'].append(index)
            obs['obs_scale'].append(float(scale[k]))
            obs['obs_low'].append(float(low))
            obs['obs_high'].append(float(high))
    actions = interface['actions']
    return {
        **obs,
        **position,
        **heading,
        'leg_action_filter': interface.get('leg_action_filter', 'none'),
        'policy_path': str(policy_dir / 'policy.onnx'),
        'policy_dt': cfg['control']['sim_timestep'] * cfg['control']['decimation'],
        'action_joint': [NATIVE_JOINTS.index(a['joint']) for a in actions],
        'action_velocity': [a['kind'] == 'velocity' for a in actions],
        'action_scale': [float(a['scale']) for a in actions],
        'action_offset': [float(a['offset']) for a in actions],
        'action_low': [float((a['clip'] or (-BIG, BIG))[0]) for a in actions],
        'action_high': [float((a['clip'] or (-BIG, BIG))[1]) for a in actions],
        **{key: [float(v) for v in robot[key]] for key in (
            'default_joint_angles', 'default_joint_velocities', 'joint_kp', 'joint_kd', 'torque_limit')},
        'max_lin_x': float(cfg['command']['max_lin_x']),
        'max_ang_z': float(cfg['command']['max_ang_z']),
    }


def velocity_bias_parameters(policy_dir, response_sign):
    cfg = json.loads((policy_dir / 'config.json').read_text())
    if (cfg['policy_interface'].get('algorithm') != 'FlashSAC' or
            abs(cfg['control']['sim_timestep'] * cfg['control']['decimation'] - .02) > 1e-9):
        raise ValueError('velocity bias requires a FlashSAC 20 ms policy')
    native = {a['joint']: a for a in cfg['policy_interface']['actions']}
    for j in (3, 7):
        if native[NATIVE_JOINTS[j]]['kind'] != 'velocity' or cfg['robot']['joint_kd'][j] <= 0:
            raise ValueError('velocity bias requires wheel velocity actions with positive Kd')
    if response_sign not in (-1., 1.):
        raise ValueError('velocity_bias_response_sign must be -1 or +1')
    geometry = json.loads((Path(__file__).resolve().parents[1] / 'config/velocity_bias_geometry.json').read_text())
    return {
        'velocity_bias_response_sign': response_sign,
        'velocity_bias_radius': float(geometry['wheel_radius']),
        **{f'velocity_bias_{key}': [float(v) for v in geometry[key]] for key in ('xyz', 'rpy', 'axis')},
    }


def setup(context):
    if 'velocity_bias_max_torque' in context.launch_configurations:
        raise ValueError('velocity_bias_max_torque is not configurable; additional torque is fixed at +/-0.8 Nm/wheel')
    policy_dir = Path(LaunchConfiguration('policy_dir').perform(context)).expanduser().resolve()
    namespace = LaunchConfiguration('namespace').perform(context)
    parameters = policy_parameters(policy_dir)
    leg_filter = LaunchConfiguration('leg_action_filter', default='auto').perform(context)
    if leg_filter == 'auto':
        leg_filter = parameters['leg_action_filter']
    if leg_filter not in ('none', 'ma2_legs', 'ma2_notch_legs'):
        raise ValueError('unknown leg_action_filter')
    if leg_filter != 'none' and abs(parameters['policy_dt'] - .02) > 1e-9:
        raise ValueError('leg action MA2 requires a 20 ms policy period')
    parameters['leg_action_filter'] = leg_filter
    parameters['leg_notch_hz'] = float(LaunchConfiguration('leg_notch_hz', default='8.3').perform(context))
    parameters['leg_notch_q'] = float(LaunchConfiguration('leg_notch_q', default='3.0').perform(context))
    if leg_filter == 'ma2_notch_legs':
        hz, q = parameters['leg_notch_hz'], parameters['leg_notch_q']
        if not (math.isfinite(hz) and math.isfinite(q) and 0 < hz < 25 and q > 0 and hz/q < 25):
            raise ValueError('invalid notch frequency/Q/bandwidth at 50 Hz')
    enabled = LaunchConfiguration('velocity_bias', default='false').perform(context) == 'true'
    parameters['velocity_bias'] = enabled
    if enabled:
        parameters.update(velocity_bias_parameters(policy_dir,
            float(LaunchConfiguration('velocity_bias_response_sign', default='1.0').perform(context))))
    tita = Node(package='tita_controller', executable='tita_node', output='screen', emulate_tty=True,
                parameters=[{**parameters,
                             'output_enabled': LaunchConfiguration('output_enabled').perform(context) == 'true',
                             'namespace': f'/{namespace}', 'joy_topic': f'/{namespace}/joy'}])
    joy = Node(package='teleop_command', executable='teleop_command_node', namespace=namespace, output='screen',
               parameters=[{'uart_interface': '/dev/ttyTHS1', 'update_rate': 10, 'use_sdk': False,
                            'joy_only': True, 'receive_only': True, 'joystick_deadzone': 0.013}])
    return [joy, tita]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('policy_dir', description='sim2sim export folder with config.json and policy.onnx'),
        DeclareLaunchArgument('output_enabled', default_value='false', description='true sends motor torques'),
        DeclareLaunchArgument('namespace', default_value='tita4252763'),
        DeclareLaunchArgument('leg_action_filter', default_value='auto', choices=['auto', 'none', 'ma2_legs', 'ma2_notch_legs']),
        DeclareLaunchArgument('leg_notch_hz', default_value='8.3'),
        DeclareLaunchArgument('leg_notch_q', default_value='3.0'),
        DeclareLaunchArgument('velocity_bias', default_value='false', choices=['false', 'true']),
        DeclareLaunchArgument('velocity_bias_response_sign', default_value='1.0'),
        OpaqueFunction(function=setup),
    ])
