"""ROBOT_STATE_CHANGING: config-selected, hash-validated Teacher/torque launch."""
import hashlib
import importlib.util
import json
from pathlib import Path

from ament_index_python.packages import get_package_prefix
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent, ExecuteProcess, OpaqueFunction
from launch.events import Shutdown
from launch.substitutions import LaunchConfiguration

RESIDUAL_NAME = 'config'


def select(config, key):
    value = Path(json.loads(config.read_text())[key]).expanduser()
    return value.resolve() if value.is_absolute() else (config.parent/value).resolve()


def validate_policy(policy_dir):
    receipt = json.loads((policy_dir/'bundle.json').read_text())
    if not receipt.get('hardware_export_validated'):
        raise ValueError('Selected checkpoint has no validated hardware export')
    manifest = json.loads((policy_dir/'manifest.json').read_text())
    if manifest['evidence_status'] != 'PASS':
        raise ValueError('Teacher export validation is not PASS')
    for name, key in [('policy.onnx', 'onnx_sha256'), ('config.json', 'config_sha256')]:
        actual = hashlib.sha256((policy_dir/name).read_bytes()).hexdigest()
        if actual != manifest[key] or actual != receipt['files'][name]:
            raise ValueError('Teacher file hash mismatch: '+name)
    digest = hashlib.sha256((policy_dir/'policy.pt').read_bytes()).hexdigest()
    cfg = json.loads((policy_dir/'config.json').read_text())
    if digest != manifest['checkpoint_sha256'] or digest != cfg['policy_interface']['checkpoint_sha256']:
        raise ValueError('Teacher checkpoint mismatch')
    return receipt, digest


def setup(context):
    prefix = Path(get_package_prefix('tita_controller'))
    default_config = prefix/'share/tita_controller/config/policies.json'
    config = Path(LaunchConfiguration('policy_config', default=str(default_config)).perform(context)).expanduser().resolve()
    policy_dir = select(config, 'teacher')
    receipt, digest = validate_policy(policy_dir)
    residual = LaunchConfiguration('residual_policy', default='').perform(context)
    if residual == 'config':
        residual = str(select(config, 'residual_torque'))
    if residual:
        spec = importlib.util.spec_from_file_location('_residual_bundle', Path(__file__).with_name('_residual_bundle.py'))
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        helper.residual_parameters(residual, policy_dir, 'none', False)
    return [ExecuteProcess(cmd=['bash', str(prefix/'lib/tita_controller/run_sim2real.sh'),
        LaunchConfiguration('output_enabled').perform(context)],
        additional_env=dict(TITA_INTERNAL_RUNNER='1', TITA_WORKSPACE=str(prefix.parent.parent),
            TITA_NAMESPACE=LaunchConfiguration('namespace').perform(context),
            TITA_POLICY_BUNDLE=receipt['task']+'_'+str(receipt['step']),
            TITA_POLICY_DIR=str(policy_dir), TITA_POLICY_CHECKPOINT=digest,
            TITA_RESIDUAL_POLICY=residual, TITA_ACTUATOR_LOGGING=LaunchConfiguration('actuator_logging').perform(context),
            TITA_VELOCITY_BIAS='false', TITA_LEG_ACTION_FILTER='none', TITA_LEG_NOTCH_HZ='8.3', TITA_LEG_NOTCH_Q='3.0',
            TITA_VELOCITY_BIAS_RESPONSE_SIGN='1.0'), output='screen', sigterm_timeout='20', sigkill_timeout='10',
        on_exit=[EmitEvent(event=Shutdown(reason='Sim2Real logged runner exited'))])]


def description(default_residual=''):
    return LaunchDescription([
        DeclareLaunchArgument('output_enabled', default_value='false', choices=['false', 'true']),
        DeclareLaunchArgument('namespace', default_value='tita4252763'),
        DeclareLaunchArgument('actuator_logging', default_value='true', choices=['false', 'true']),
        DeclareLaunchArgument('policy_config', default_value=str(Path(__file__).resolve().parents[1]/'config/policies.json')),
        DeclareLaunchArgument('residual_policy', default_value=default_residual,
            description='config selects configured torque bundle; empty selects Teacher only'),
        OpaqueFunction(function=setup)])
