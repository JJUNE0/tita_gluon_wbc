"""ROBOT_STATE_CHANGING: private node construction used by the logged runner.

Public entrypoints validate the pinned policy pair before the runner calls this
module. It is not an operator launch entrypoint.
"""

import json
import importlib.util
import math
from pathlib import Path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

NATIVE_JOINTS = [f'joint_{side}_leg_{index}' for side in ('left', 'right') for index in range(1, 5)]
# Same order as ObsKind in adapter.hpp.
OBS_KINDS = ['ang_vel', 'gravity', 'commands', 'joint_pos', 'joint_vel', 'last_action', 'zero', 'wheel_position_error',
             'heading_error', 'support_mode', 'pose_commands']
BIG = 1e9  # stands in for "no clip"


def pose_parameters(cfg):
    """Require the exported absolute roll/pitch/height contract, including its slew limits."""
    saved = cfg.get('pose_command', {})

    def numbers(value, size):
        return (isinstance(value, list) and len(value) == size
                and all(type(v) in (float, int) and math.isfinite(v) for v in value))

    ranges = [saved.get(key) for key in ('roll_range', 'pitch_range', 'height_range')]
    rates, nominal = saved.get('ramp_rates'), saved.get('nominal_height')
    if (any(not numbers(bounds, 2) for bounds in ranges) or not numbers(rates, 3)
            or type(nominal) not in (float, int) or not math.isfinite(nominal)):
        raise ValueError('Invalid pose command ranges/nominal/ramp rates')
    if (any(lo > hi for lo, hi in ranges) or any(v <= 0 for v in rates)
            or any(not -math.pi/2 <= lo <= 0 <= hi <= math.pi/2 for lo, hi in ranges[:2])
            or not 0 < ranges[2][0] <= nominal <= ranges[2][1]):
        raise ValueError('Invalid pose command ranges/nominal/ramp rates')
    return {'pose_low': [float(bounds[0]) for bounds in ranges],
            'pose_high': [float(bounds[1]) for bounds in ranges],
            'pose_ramp_rates': [float(v) for v in rates], 'pose_nominal_height': float(nominal)}


def policy_parameters(policy_dir):
    """Flatten config.json into one entry per observation element and per action (see adapter.py)."""
    cfg = json.loads((policy_dir / 'config.json').read_text())
    interface, robot = cfg['policy_interface'], cfg['robot']
    obs = {key: [] for key in ('obs_kind', 'obs_index', 'obs_scale', 'obs_low', 'obs_high')}
    position, heading, support, pose = {}, {}, {}, {}
    for term in interface['observations']:
        if term['kind'] not in OBS_KINDS:
            raise ValueError(f"observation '{term['kind']}' is not available on the robot")
        if term['kind'] == 'wheel_position_error':
            if term['params'].get('gait_name') is not None:
                raise ValueError('Gait-gated wheel position error is not available on the robot')
            position = {
                'wheel_position_radius': float(term['params']['radius']),
                'wheel_position_clip_m': float(term['params']['clip_m']),
                'wheel_position_zero_thresholds': [float(v) for v in term['params']['zero_thresholds']],
                'wheel_position_moving_anchor': term['params'].get('moving_anchor', False),
            }
            thresholds = term['params'].get('velocity_thresholds')
            if thresholds is not None:
                if (len(thresholds) != 2 or any(isinstance(v, bool) or not isinstance(v, (int, float))
                        or not math.isfinite(v) or v <= 0 for v in thresholds)):
                    raise ValueError('Invalid wheel position velocity thresholds')
                position['wheel_position_velocity_thresholds'] = [float(v) for v in thresholds]
                geometry = json.loads((Path(__file__).resolve().parents[1] / 'config/velocity_bias_geometry.json').read_text())
                position.update({f'wheel_odometry_{key}': [float(v) for v in geometry[key]]
                                 for key in ('xyz', 'rpy', 'axis')})
        if term['kind'] == 'support_mode':
            saved = cfg.get('support_command', {})
            if (term['size'] != 3 or saved.get('encoding') != 'one_hot'
                    or saved.get('mode_names') != ['left', 'right', 'both']
                    or type(saved.get('default_mode')) is not int or saved['default_mode'] not in (0, 1, 2)):
                raise ValueError('Invalid support-mode command contract')
            support['support_mode'] = saved['default_mode']
        if term['kind'] == 'pose_commands':
            if term['size'] != 3 or 'joints' in term:
                raise ValueError('Pose command must have three elements: roll rad, pitch rad, height m')
            pose = pose_parameters(cfg)
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
    if pose and support:
        raise ValueError('Pose and support commands cannot be combined')
    if bool(cfg.get('pose_command')) != bool(pose):
        raise ValueError('Pose command config/layout mismatch')
    actions = interface['actions']
    limits = {key: float(cfg['command'][key]) for key in ('max_lin_x', 'max_ang_z')}
    if support:
        # The saved ranges distinguish old zero-command policies from support locomotion.
        ranges = cfg.get('sim_command_ranges', {})
        for key, axis in (('max_lin_x', 'lin_vel_x'), ('max_ang_z', 'ang_vel_z')):
            bounds = ranges.get(axis, [0., 0.])
            if (len(bounds) != 2 or not all(math.isfinite(v) for v in bounds)
                    or not bounds[0] <= 0 <= bounds[1]):
                raise ValueError('Invalid support velocity command range')
            limits[key] = min(limits[key], -bounds[0], bounds[1])
    return {
        **obs,
        **position,
        **heading,
        **support,
        **pose,
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
        **limits,
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
    parameters['actuator_logging'] = LaunchConfiguration('actuator_logging', default='false').perform(context) == 'true'
    parameters['support_fall_tilt_deg'] = float(LaunchConfiguration('support_fall_tilt_deg', default='55.0').perform(context))
    if not math.isfinite(parameters['support_fall_tilt_deg']) or not 0 < parameters['support_fall_tilt_deg'] < 90:
        raise ValueError('support_fall_tilt_deg must be finite and between 0 and 90 degrees')
    requested_support = LaunchConfiguration('support_mode', default='auto').perform(context)
    if requested_support != 'auto':
        if 'support_mode' not in parameters:
            raise ValueError('support_mode requires a support-command policy')
        parameters['support_mode'] = int(requested_support)
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
    residual = LaunchConfiguration('residual_policy', default='').perform(context)
    if residual:
        spec = importlib.util.spec_from_file_location('residual_bundle', Path(__file__).with_name('_residual_bundle.py'))
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        parameters.update(helper.residual_parameters(residual, policy_dir, leg_filter, enabled))
        # The validated bundle supplies its saved observation period (50/250Hz).
    if enabled:
        if 'support_mode' in parameters or 'pose_low' in parameters:
            raise ValueError('velocity bias is not supported for support-command or pose-command policies')
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
        DeclareLaunchArgument('actuator_logging', default_value='false', choices=['false', 'true'],
                              description='500 Hz fixed-size actuator snapshots via a separate publisher'),
        DeclareLaunchArgument('residual_policy', default_value='', description='optional validated stationary residual ONNX bundle'),
        DeclareLaunchArgument('support_mode', default_value='auto', choices=['auto', '0', '1', '2'],
                              description='0 left support, 1 right support, 2 both; auto uses saved default'),
        DeclareLaunchArgument('support_fall_tilt_deg', default_value='55.0',
                              description='Total-tilt cutoff during support-policy RL only; restart to change'),
        DeclareLaunchArgument('leg_action_filter', default_value='auto', choices=['auto', 'none', 'ma2_legs', 'ma2_notch_legs']),
        DeclareLaunchArgument('leg_notch_hz', default_value='8.3'),
        DeclareLaunchArgument('leg_notch_q', default_value='3.0'),
        DeclareLaunchArgument('velocity_bias', default_value='false', choices=['false', 'true']),
        DeclareLaunchArgument('velocity_bias_response_sign', default_value='1.0'),
        OpaqueFunction(function=setup),
    ])
