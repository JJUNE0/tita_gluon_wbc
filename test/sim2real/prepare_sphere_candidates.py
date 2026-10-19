"""DESKTOP_DRY_RUN: pin the four operator-selected exports and native Torch fixtures; no SDK."""
import hashlib
import json
from pathlib import Path
import shutil
import sys

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'lab/ddt_lab/scripts/flash_sac'))
from export import load_policy


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    specs = json.loads((HERE / 'sphere_candidates/specs.json').read_text())
    policies = ROOT / 'sim2real/tita_ws/src/tita_controller/policies'
    reference = json.loads((policies / 'flashsac_posma2_75000/config.json').read_text())
    prepared = []
    # Validate every source before creating any bundle.
    for spec in specs:
        checkpoint = ROOT / 'lab/ddt_lab/logs/flash_sac' / spec['run'] / f"model_{spec['step']}"
        source = checkpoint / 'sim2sim/actor'
        config = json.loads((source / 'config.json').read_text())
        manifest = json.loads((source / 'manifest.json').read_text())
        metadata = json.loads((checkpoint / 'ddt.json').read_text())
        assert digest(checkpoint / 'actor.pt') == metadata['actor_sha256'] == spec['checkpoint_sha256']
        assert manifest['checkpoint_sha256'] == config['policy_interface']['checkpoint_sha256'] == spec['checkpoint_sha256']
        assert digest(source / 'policy.onnx') == manifest['onnx_sha256'] == spec['onnx_sha256']
        assert config['policy_interface']['onnx_sha256'] == spec['onnx_sha256']
        assert digest(source / 'config.json') == manifest['config_sha256']
        assert config['robot'] == reference['robot'] and config['control'] == reference['control']
        assert config['policy_interface']['observations'] == reference['policy_interface']['observations']
        assert config['policy']['obs_dim'] == metadata['actor_obs_dim'] == 34 and metadata['action_dim'] == 8
        assert config['policy_interface']['leg_action_filter'] == spec['leg_action_filter']
        expected_actions = json.loads(json.dumps(reference['policy_interface']['actions']))
        if spec['leg_action_filter'] == 'none':
            for action in expected_actions:
                action.pop('filter', None)
        assert config['policy_interface']['actions'] == expected_actions
        assert not (policies / spec['bundle']).exists(), 'Refusing to overwrite a bundle'
        prepared.append((spec, checkpoint, source, config, manifest, metadata))
    torch.set_num_threads(2)
    samples = torch.randn(256, 34, generator=torch.Generator().manual_seed(31415)) * 2
    rows = []
    for spec, checkpoint, source, config, manifest, metadata in prepared:
        actor = load_policy(checkpoint, metadata)
        with torch.inference_mode():
            actual = actor(samples)
            means = actor.actor.get_mean_and_std(samples, training=False)[0].tanh()
            native = means * torch.where(means >= 0, actor.action_gain_positive, actor.action_gain_negative)
            torch.testing.assert_close(actual, native, atol=1e-5, rtol=1e-4)
        bundle = policies / spec['bundle']
        bundle.mkdir()
        source_config_sha = digest(source / 'config.json')
        config['command'] = dict(max_lin_x=1., max_ang_z=1.)
        (bundle / 'config.json').write_text(json.dumps(config, indent=2) + '\n')
        shutil.copyfile(source / 'policy.onnx', bundle / 'policy.onnx')
        manifest.update(execution_domain='DESKTOP_DRY_RUN', config_sha256=digest(bundle / 'config.json'),
            hardware_status='NOT_TESTED', deployment_overrides=dict(command=config['command'],
                source_config_sha256=source_config_sha, source_run=f"{spec['run']}/model_{spec['step']}",
                note='Training observations/actions/gains/filter retained; existing real joystick caps 1/1 and ramp retained.'))
        (bundle / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        fixture = HERE / 'sphere_candidates' / spec['bundle']
        fixture.mkdir()
        np.savetxt(fixture / 'obs.txt', samples.numpy(), fmt='%.9g')
        np.save(fixture / 'expected.npy', native.numpy())
        row = {**spec, 'config_sha256': manifest['config_sha256'], 'source_config_sha256': source_config_sha,
            'source_task': metadata['task'], 'execution_domain': 'DESKTOP_DRY_RUN', 'evidence_status': 'PASS'}
        rows.append(row)
        print(f"PASS {spec['label']} {spec['bundle']}: user pins, training interface/filter and native Torch fixture", flush=True)
    stage = ROOT / 'docs/exp/2026-10-19/sphere_candidates_deployment'
    (stage / 'bundles.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
