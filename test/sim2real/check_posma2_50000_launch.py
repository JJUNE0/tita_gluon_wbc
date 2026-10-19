"""DESKTOP_DRY_RUN / ROBOT_COMMAND_FREE_RUNTIME: installed/source launch contracts; construct no nodes."""
import importlib.util
import json
from pathlib import Path
import sys
from unittest.mock import patch

from launch import LaunchContext

root = Path(sys.argv[1]).absolute()


def load(name):
    spec = importlib.util.spec_from_file_location(name, root / 'launch' / f'{name}.launch.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


flash, tita = load('flashsac'), load('tita')
for bundle in flash.BUNDLES:
    path = root / 'policies' / bundle
    flash.validate_policy(path)
    cfg = json.loads((path / 'config.json').read_text())
    context = LaunchContext()
    context.launch_configurations.update(policy=bundle, output_enabled='false', namespace='desktop_test')
    with patch.object(flash, 'get_package_prefix', return_value=str(root.parents[1])), \
            patch.object(flash, 'ExecuteProcess') as execute:
        flash.setup(context)
        env = execute.call_args.kwargs['additional_env']
        assert env['TITA_LEG_ACTION_FILTER'] == cfg['policy_interface'].get('leg_action_filter', 'none')
        assert env['TITA_POLICY_BUNDLE'] == bundle and env['TITA_VELOCITY_BIAS'] == 'false'
    params = tita.policy_parameters(path)
    assert len(params['obs_kind']) == cfg['policy']['obs_dim'] and params['policy_dt'] == .02
    if bundle == 'flashsac_posma2_50000':
        assert len(params['obs_kind']) == 34 and params['obs_kind'][-1] == 7
        assert params['joint_kp'] == [60., 60., 92., 0., 60., 60., 92., 0.]
        assert params['joint_kd'] == [1.5, 1.5, 2.3, .5, 1.5, 1.5, 2.3, .5]
        assert params['leg_action_filter'] == 'ma2_legs'
        assert params['wheel_position_radius'] == .0925
    print(f'PASS {bundle}: pinned hashes, {len(params["obs_kind"])} observations, auto filter {env["TITA_LEG_ACTION_FILTER"]}')
