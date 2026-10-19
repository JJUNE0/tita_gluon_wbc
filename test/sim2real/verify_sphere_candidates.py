"""DESKTOP_DRY_RUN / ROBOT_COMMAND_FREE_RUNTIME: pinned launch setup and inference fixtures, no nodes."""
import argparse
import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

import numpy as np
from launch import LaunchContext


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('share', type=Path)
    parser.add_argument('fixtures', type=Path)
    parser.add_argument('--actual', type=Path)
    parser.add_argument('--onnx', action='store_true')
    parser.add_argument('--result', required=True, type=Path)
    args = parser.parse_args()
    share = args.share.absolute()
    specs = json.loads((args.fixtures / 'specs.json').read_text())
    modules = {}
    for name in ('flashsac', 'tita'):
        spec = importlib.util.spec_from_file_location(name, share / 'launch' / f'{name}.launch.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modules[name] = module
    flash, tita = modules['flashsac'], modules['tita']
    # Verify existing bundles too, with no process creation.
    for bundle in flash.BUNDLES:
        flash.validate_policy(share / 'policies' / bundle)
    rows = []
    for spec in specs:
        bundle = share / 'policies' / spec['bundle']
        pins = flash.BUNDLES[spec['bundle']]
        assert pins[:2] == (spec['checkpoint_sha256'], spec['onnx_sha256'])
        params = tita.policy_parameters(bundle)
        assert len(params['obs_kind']) == 34 and params['obs_kind'][-1] == 7
        assert params['policy_dt'] == .02 and params['action_joint'] == list(range(8))
        assert params['joint_kp'] == [60., 60., 92., 0., 60., 60., 92., 0.]
        assert params['joint_kd'] == [1.5, 1.5, 2.3, .5, 1.5, 1.5, 2.3, .5]
        assert params['torque_limit'] == [60., 60., 60., 12., 60., 60., 60., 12.]
        assert params['max_lin_x'] == params['max_ang_z'] == 1.
        assert params['leg_action_filter'] == spec['leg_action_filter']
        assert params['wheel_position_radius'] == .0925
        assert params['wheel_position_clip_m'] == .3
        assert params['wheel_position_zero_thresholds'] == [.02, .02, .03]
        context = LaunchContext()
        context.launch_configurations.update(policy=spec['bundle'], output_enabled='false', namespace='test')
        with patch.object(flash, 'get_package_prefix', return_value=str(share.parents[1])), \
                patch.object(flash, 'ExecuteProcess') as execute:
            flash.setup(context)
            env = execute.call_args.kwargs['additional_env']
            assert env['TITA_POLICY_BUNDLE'] == spec['bundle']
            assert env['TITA_LEG_ACTION_FILTER'] == spec['leg_action_filter']
            assert env['TITA_VELOCITY_BIAS'] == 'false'
        with patch.object(tita, 'Node') as node:
            context.launch_configurations.update(policy_dir=str(bundle))
            tita.setup(context)
            applied = node.call_args_list[0].kwargs['parameters'][0]
            assert applied['leg_action_filter'] == spec['leg_action_filter']
            assert applied['output_enabled'] is False
        row = {**spec, 'execution_domain': 'ROBOT_COMMAND_FREE_RUNTIME' if args.actual else 'DESKTOP_DRY_RUN',
            'evidence_status': 'PASS', 'observations': 34, 'actions': 8}
        if args.onnx or args.actual:
            expected = np.load(args.fixtures / spec['bundle'] / 'expected.npy')
            if args.onnx:
                import onnxruntime as ort
                session = ort.InferenceSession(str(bundle / 'policy.onnx'), providers=['CPUExecutionProvider'])
                values = np.loadtxt(args.fixtures / spec['bundle'] / 'obs.txt', dtype=np.float32)
                actual = np.concatenate([session.run(None, {session.get_inputs()[0].name: x[None]})[0] for x in values])
                again = np.concatenate([session.run(None, {session.get_inputs()[0].name: x[None]})[0] for x in values])
                np.testing.assert_array_equal(actual, again)
            else:
                actual = np.loadtxt(args.actual / f"{spec['bundle']}_actual.txt")
            assert actual.shape == expected.shape == (256, 8)
            np.testing.assert_allclose(actual, expected, atol=2e-5, rtol=1e-4)
            row.update(samples=256, max_abs_error=float(abs(actual - expected).max()))
        rows.append(row)
        print(f"PASS {spec['bundle']}: pinned 34 inputs/8 actions, auto={spec['leg_action_filter']}, {row.get('max_abs_error', 'launch only')}")
    args.result.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
