"""VALIDATION_SIM: trained .pt + saved config -> verified policy and interface."""

import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys

import yaml
from .adapter import ISAAC_JOINTS, NATIVE_JOINTS

REPO = Path(__file__).resolve().parents[3]
PACKAGE = Path(__file__).resolve().parents[1]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class ConfigLoader(yaml.SafeLoader):
    """Read Isaac YAML tags as data; never instantiate Python objects."""


def _python_tag(loader, tag, node):
    if isinstance(node, yaml.SequenceNode):
        values = loader.construct_sequence(node, deep=True)
        return {'slice': values} if tag == 'object/apply:builtins.slice' else values
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node, deep=True)
    return tag.removeprefix('name:') if tag.startswith('name:') else loader.construct_scalar(node)


ConfigLoader.add_multi_constructor('tag:yaml.org,2002:python/', _python_tag)


def read_yaml(path):
    return yaml.load(Path(path).read_text(), Loader=ConfigLoader)


def _sidecar(checkpoint, name, required=True):
    for root in (checkpoint.parent, checkpoint.parent / 'params', checkpoint.parent.parent,
                 checkpoint.parent.parent / 'params'):
        path = root / name
        if path.is_file():
            return path
    if required:
        raise ValueError(f'{name} is required beside the checkpoint or in its run/params directory; weights alone do not describe observations/actions')
    return None


def _matches(patterns, names, preserve=False):
    if isinstance(patterns, str):
        patterns = [patterns]
    patterns = patterns or ['.*']
    if preserve:
        result = [name for pattern in patterns for name in names if re.fullmatch(pattern, name)]
    else:
        result = [name for name in names if any(re.fullmatch(pattern, name) for pattern in patterns)]
    if not result or len(result) != len(set(result)):
        raise ValueError(f'Invalid/ambiguous joint selection: {patterns}')
    return result


def _joint_value(value, joint, default=None):
    if not isinstance(value, dict):
        return default if value is None else value
    matches = [number for pattern, number in value.items() if re.fullmatch(pattern, joint)]
    if len(matches) != 1:
        raise ValueError(f'Cannot resolve joint setting for {joint}: {value}')
    return matches[0]


def observation_layout(group, captured, asset_joints):
    observations = []
    if not group.get('concatenate_terms', True):
        raise ValueError('The TITA adapter requires concatenated policy observations')
    if group.get('history_length', 0):
        raise ValueError('Historical/recurrent policies need a dedicated adapter; current TITA policies use history_length=0')
    captured_obs = {term['name']: term for term in captured.get('observations', [])}
    functions = {'base_ang_vel': 'ang_vel', 'base_ang_vel_biased': 'ang_vel',
                 'projected_gravity': 'gravity', 'projected_gravity_biased': 'gravity',
                 'generated_commands': 'commands', 'last_action': 'last_action',
                 'joint_pos_rel': 'joint_pos', 'joint_pos_rel_without_wheel': 'joint_pos',
                 'joint_pos_rel_without_wheel_biased': 'joint_pos', 'joint_vel_rel': 'joint_vel',
                 'base_lin_vel': 'lin_vel', 'WheelPositionError': 'wheel_position_error',
                 'GyroHeadingError': 'heading_error'}
    for name, term in group.items():
        if not isinstance(term, dict) or 'func' not in term:
            continue
        function = term['func'].replace(':', '.').split('.')[-1]
        if function not in functions or term.get('history_length', 0) or term.get('modifiers'):
            raise ValueError(f'Unsupported observation term: {name} / {function}')
        resolved = captured_obs.get(name, {})
        scale = 1. if term.get('scale') is None else term['scale']
        item = {
            'name': name, 'kind': functions[function],
            'scale': resolved.get('scale', scale), 'clip': resolved.get('clip', term.get('clip')),
        }
        if item['kind'] == 'wheel_position_error':
            params = term['params']
            if params['command_name'] != 'base_velocity' or params.get('asset_cfg', {}).get('name', 'robot') != 'robot':
                raise ValueError('WheelPositionError requires robot encoders and base_velocity commands')
            item['params'] = {key: params[key] for key in ('radius', 'clip_m', 'zero_thresholds')}
            numbers = [params['radius'], params['clip_m'], *params['zero_thresholds']]
            if (len(params['zero_thresholds']) != 3 or not all(math.isfinite(v) for v in numbers)
                    or params['radius'] <= 0 or params['clip_m'] <= 0 or min(params['zero_thresholds']) < 0):
                raise ValueError('Invalid WheelPositionError parameters')
            item['size'] = 1
        elif item['kind'] == 'heading_error':
            params = term['params']
            if params['command_name'] != 'base_velocity' or params.get('asset_cfg', {}).get('name', 'robot') != 'robot':
                raise ValueError('GyroHeadingError requires the robot gyro and base_velocity commands')
            # bias_range is a training-only randomization; deployment subtracts a calibrated bias instead.
            item['params'] = {key: params[key] for key in ('clip_rad', 'zero_thresholds', 'warmup_s')}
            numbers = [params['clip_rad'], params['warmup_s'], *params['zero_thresholds']]
            if (len(params['zero_thresholds']) != 3 or not all(math.isfinite(v) for v in numbers)
                    or params['clip_rad'] <= 0 or params['warmup_s'] < 0 or min(params['zero_thresholds']) < 0):
                raise ValueError('Invalid GyroHeadingError parameters')
            item['size'] = 1
        elif item['kind'] in ('joint_pos', 'joint_vel'):
            entity = term.get('params', {}).get('asset_cfg', {})
            item['joints'] = resolved.get('joints') or _matches(
                entity.get('joint_names', '.*'), asset_joints, entity.get('preserve_order', False))
            item['zero_wheel_pos'] = 'without_wheel' in function
            item['size'] = len(item['joints'])
        else:
            item['size'] = 8 if item['kind'] == 'last_action' else 3
        observations.append(item)
    return observations


def action_layout(action_cfg, captured, asset_joints, defaults):
    actions = []
    captured_actions = {term['name']: term for term in captured.get('actions', [])}
    for name, term in action_cfg.items():
        if term is None:
            continue
        kind = term['class_type'].replace(':', '.').split('.')[-1]
        if kind not in ('JointPositionAction', 'JointVelocityAction', 'MA2JointPositionAction'):
            raise ValueError(f'Unsupported action term: {name} / {kind}')
        names = captured_actions.get(name, {}).get('joints') or _matches(
            term['joint_names'], asset_joints, term.get('preserve_order', False))
        for joint in names:
            velocity = kind == 'JointVelocityAction'
            offset = _joint_value(defaults['joint_vel'], joint, 0.) if velocity else defaults['joint_pos'][joint]
            if not term.get('use_default_offset', True):
                offset = _joint_value(term.get('offset'), joint, 0.)
            actions.append({'joint': joint, 'kind': 'velocity' if velocity else 'position',
                            'scale': float(_joint_value(term['scale'], joint)), 'offset': float(offset),
                            'clip': _joint_value(term.get('clip'), joint)})
            if kind == 'MA2JointPositionAction':
                actions[-1]['filter'] = 'ma2'
    if len(actions) != 8 or {term['joint'] for term in actions} != set(NATIVE_JOINTS):
        raise ValueError('Checkpoint action terms must cover each TITA joint once')
    filtered = {term['joint'] for term in actions if term.get('filter') == 'ma2'}
    if filtered and filtered != set(NATIVE_JOINTS) - {NATIVE_JOINTS[3], NATIVE_JOINTS[7]}:
        raise ValueError('MA2 must cover exactly the six leg position actions')
    return actions


def simulation_config(env, defaults, observations):
    cfg = read_yaml(PACKAGE / 'config/tita.yaml')
    robot = cfg['robot']
    robot['default_joint_angles'] = [defaults['joint_pos'][name] for name in NATIVE_JOINTS]
    robot['default_joint_velocities'] = [_joint_value(defaults['joint_vel'], name, 0.) for name in NATIVE_JOINTS]
    robot['reset_base_pos'], robot['reset_base_quat'] = defaults['pos'], defaults['rot']
    robot.update(joint_kp=[], joint_kd=[], torque_limit=[])
    for joint in NATIVE_JOINTS:
        actuators = [act for act in env['scene']['robot']['actuators'].values()
                     if any(re.fullmatch(pattern, joint) for pattern in act['joint_names_expr'])]
        if len(actuators) != 1:
            raise ValueError(f'Cannot resolve actuator for {joint}')
        act = actuators[0]
        robot['joint_kp'].append(_joint_value(act['stiffness'], joint))
        robot['joint_kd'].append(_joint_value(act['damping'], joint))
        effort = act.get('effort_limit_sim')
        robot['torque_limit'].append(_joint_value(act.get('effort_limit') if effort is None else effort, joint))
    cfg['control'].update(sim_timestep=env['sim']['dt'], decimation=env['decimation'])
    ranges = env['commands']['base_velocity']['ranges']
    cfg['sim_command_ranges'] = {name: ranges[name] for name in ('lin_vel_x', 'ang_vel_z')}
    for name, bounds in cfg['sim_command_ranges'].items():
        if len(bounds) != 2 or not all(math.isfinite(value) for value in bounds) or not bounds[0] <= 0 <= bounds[1]:
            raise ValueError(f'Invalid saved simulation command range: {name} / {bounds}')
    # Viewer keyboard ramp follows the training command ramp (RampedVelocityCommand.ramp_rate, units/s); None = step.
    ramp = env['commands']['base_velocity'].get('ramp_rate')
    if ramp is not None and not (math.isfinite(ramp) and ramp > 0):
        raise ValueError(f'Invalid saved command ramp: {ramp}')
    cfg['sim_command_ramp'] = None if ramp is None else float(ramp)
    cfg['policy'] = {'obs_dim': sum(item['size'] for item in observations)}
    return cfg


def describe_checkpoint(path):
    path = Path(path).expanduser().resolve()
    if path.is_dir():
        path = path / 'actor.pt'
    if not path.is_file() or path.suffix != '.pt':
        raise ValueError('--ckpt must be a trained PPO .pt or FlashSAC actor.pt/model directory')
    flash = path.name == 'actor.pt' and (path.parent / 'ddt.json').is_file()
    env_path = _sidecar(path, 'env.yaml')
    agent_path = _sidecar(path, 'agent.json', required=False) or _sidecar(path, 'agent.yaml')
    agent = json.loads(agent_path.read_text()) if agent_path.suffix == '.json' else read_yaml(agent_path)
    env = read_yaml(env_path)
    defaults = env['scene']['robot']['init_state']
    if set(NATIVE_JOINTS) != set(defaults['joint_pos']):
        raise ValueError('This package supports the eight-joint TITA PPO/FlashSAC environment')
    captured_path = _sidecar(path, 'policy_interface.json', required=False)
    captured = json.loads(captured_path.read_text()) if captured_path else {}
    asset_joints = captured.get('articulation_joint_names', ISAAC_JOINTS)
    observations = observation_layout(env['observations']['policy'], captured, asset_joints)
    actions = action_layout(env['actions'], captured, asset_joints, defaults)
    cfg = simulation_config(env, defaults, observations)
    sources = [env_path, agent_path] + ([captured_path] if captured_path else [])
    if flash:
        metadata = json.loads((path.parent / 'ddt.json').read_text())
        if sha256(path) != metadata['actor_sha256']:
            raise ValueError('FlashSAC actor hash mismatch')
        sources.append(path.parent / 'ddt.json')
        if metadata['actor_obs_dim'] != cfg['policy']['obs_dim']:
            raise ValueError('Saved environment observation layout does not match FlashSAC actor')
    else:
        metadata = {'actor_sha256': sha256(path)}
        if agent.get('policy', {}).get('class_name') not in ('ActorCritic', 'ActorCriticWithEstimator'):
            raise ValueError('Supported PPO classes: ActorCritic and ActorCriticWithEstimator')
    adapter_sources = (Path(__file__), Path(__file__).with_name('adapter.py'),
                       REPO / 'lab/ddt_lab/scripts/flash_sac/export.py')
    cfg['policy_interface'] = {
        'schema_version': 1, 'observations': observations, 'actions': actions,
        'leg_action_filter': 'ma2_legs' if any(term.get('filter') == 'ma2' for term in actions) else 'none',
        'articulation_joint_names': asset_joints,
        'joint_order_source': 'resolved training interface' if captured else 'validated legacy TITA order',
        'checkpoint': str(path), 'algorithm': 'FlashSAC' if flash else 'PPO',
        'checkpoint_sha256': metadata['actor_sha256'],
        'sources': {str(source): sha256(source) for source in sources},
        'adapter_sources': {source.name: sha256(source) for source in adapter_sources},
    }
    return path, cfg, agent, metadata


def export_directory(checkpoint):
    return checkpoint.parent / 'sim2sim' / checkpoint.stem


def fingerprint(cfg):
    return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()


def prepared_config(checkpoint):
    path, cfg, _, _ = describe_checkpoint(checkpoint)
    output = export_directory(path)
    try:
        manifest = json.loads((output / 'manifest.json').read_text())
        if manifest['fingerprint'] == fingerprint(cfg) and manifest['onnx_sha256'] == sha256(output / 'policy.onnx'):
            if manifest['config_sha256'] == sha256(output / 'config.json'):
                return output / 'config.json'
    except (OSError, ValueError, KeyError):
        pass
    return None


def load_ppo_policy(path, agent):
    import torch
    from rsl_rl.networks import MLP, EmpiricalNormalization
    state = torch.load(path, map_location='cpu', weights_only=True)['model_state_dict']
    policy_cfg = agent['policy']

    def mlp(prefix, hidden_dims, output_dim, activation):
        input_dim = state[f'{prefix}.0.weight'].shape[1]
        model = MLP(input_dim, output_dim, hidden_dims, activation)
        model.load_state_dict({key.removeprefix(prefix + '.'): value for key, value in state.items() if key.startswith(prefix + '.')})
        return model.eval()

    def normalizer(prefix, size):
        values = {key.removeprefix(prefix + '.'): value for key, value in state.items() if key.startswith(prefix + '.')}
        if not values:
            return torch.nn.Identity()
        model = EmpiricalNormalization(size)
        model.load_state_dict(values)
        return model.eval()

    class PPOPolicy(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.actor = mlp('actor', policy_cfg['actor_hidden_dims'], 8, policy_cfg['activation'])
            self.actor_normalizer = normalizer('actor_obs_normalizer', self.actor[0].in_features)
            self.estimator = None
            self.input_dim = self.actor[0].in_features
            if policy_cfg['class_name'] == 'ActorCriticWithEstimator':
                self.estimator = mlp('estimator', policy_cfg['estimator_hidden_dims'],
                                     policy_cfg['estimator_output_dim'], 'elu')
                self.input_dim = self.estimator[0].in_features
            self.estimator_normalizer = normalizer('estimator_normalizer', self.input_dim)

        def forward(self, observation):
            if self.estimator is not None:
                estimated = self.estimator(self.estimator_normalizer(observation))
                observation = torch.cat((estimated, observation), dim=-1)
            action = self.actor(self.actor_normalizer(observation))
            return action.clamp(-agent['clip_actions'], agent['clip_actions']) if agent.get('clip_actions') is not None else action

    return PPOPolicy().eval()


def prepare_checkpoint(checkpoint, validation_python):
    import torch
    import onnx
    path, cfg, agent, metadata = describe_checkpoint(checkpoint)
    output = export_directory(path)
    output.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(2)
    if cfg['policy_interface']['algorithm'] == 'FlashSAC':
        sys.path.insert(0, str(REPO / 'lab/ddt_lab/scripts/flash_sac'))
        from export import load_policy
        policy = load_policy(path.parent, metadata)
        input_dim = metadata['actor_obs_dim']
    else:
        policy = load_ppo_policy(path, agent)
        input_dim = policy.input_dim
    if input_dim != cfg['policy']['obs_dim']:
        raise ValueError(f'Actor expects {input_dim} inputs; saved observation layout supplies {cfg["policy"]["obs_dim"]}')
    onnx_path = output / 'policy.onnx'
    torch.onnx.export(policy, torch.zeros(1, input_dim), str(onnx_path), input_names=['nn_input0'],
                      output_names=['nn_output'], opset_version=17, dynamo=False)
    onnx.checker.check_model(onnx.load(onnx_path))
    samples = torch.randn(256, input_dim, generator=torch.Generator().manual_seed(42)) * 2
    with torch.inference_mode():
        expected = policy(samples)
        if cfg['policy_interface']['algorithm'] == 'FlashSAC':
            mean = policy.actor.get_mean_and_std(samples, training=False)[0].tanh()
            native = mean * torch.where(mean >= 0, policy.action_gain_positive, policy.action_gain_negative)
            torch.testing.assert_close(expected, native, atol=1e-5, rtol=1e-4)
            expected = native
    # ONNX Runtime lives in the MuJoCo interpreter, independently of Isaac/Torch.
    script = '''import json
import sys
import numpy as np
import onnxruntime as ort

values = json.load(sys.stdin)
session = ort.InferenceSession(sys.argv[1], providers=['CPUExecutionProvider'])
actual = np.concatenate([
    session.run(['nn_output'], {'nn_input0': np.asarray([row], dtype=np.float32)})[0]
    for row in values['x']
])
expected = np.asarray(values['y'], dtype=np.float32)
if not np.isfinite(actual).all() or not np.allclose(actual, expected, atol=1e-5, rtol=1e-4):
    raise RuntimeError('ONNX parity failed')
print(json.dumps({'samples': len(actual), 'max_abs_error': float(np.max(np.abs(actual-expected)))}))
'''
    result = subprocess.run([str(validation_python), '-c', script, str(onnx_path)],
                            input=json.dumps({'x': samples.tolist(), 'y': expected.tolist()}),
                            capture_output=True, text=True, check=True)
    source_fingerprint = fingerprint(cfg)
    cfg['policy']['path'] = str(onnx_path)
    cfg['policy_interface']['onnx_sha256'] = sha256(onnx_path)
    config_path = output / 'config.json'
    config_path.write_text(json.dumps(cfg, indent=2) + '\n')
    manifest = {'execution_domain': 'VALIDATION_SIM', 'evidence_status': 'PASS',
                'checkpoint_sha256': metadata['actor_sha256'], 'onnx_sha256': sha256(onnx_path),
                'config_sha256': sha256(config_path), 'fingerprint': source_fingerprint,
                'parity': json.loads(result.stdout)}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'[VALIDATION_SIM] Prepared {path}; observations={input_dim}, actions=8; parity={manifest["parity"]}', flush=True)
    return config_path
