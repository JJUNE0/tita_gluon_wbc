"""DESKTOP_DRY_RUN: pin the warmup-0 heading checkpoint as a robot policy bundle (no SDK, no robot command).

Bundle ``flashsac_headw0_<step>`` from ``tita_flash_sac_125547_806511/model_<step>`` (argument, default 50000)
(DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObsW0-v0: sphere wheels, no leg MA2, heading drift reward and
actor/critic gyro heading error without warmup, 35 observations). Run with the Isaac Lab interpreter (Torch).
"""
import hashlib
import json
from pathlib import Path
import shutil
import sys

import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'lab/ddt_lab/scripts/flash_sac'))
from export import load_policy  # noqa: E402

RUN = 'tita_flash_sac_125547_806511'
STEP = int(sys.argv[1]) if len(sys.argv) > 1 else 50000     # usage: prepare_heading_bundle.py [step]
BUNDLE = f'flashsac_headw0_{STEP}'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    policies = ROOT / 'sim2real/tita_ws/src/tita_controller/policies'
    reference = json.loads((policies / 'flashsac_sphere2_60000/config.json').read_text())   # deployed no-MA2 bundle
    checkpoint = ROOT / 'lab/ddt_lab/logs/flash_sac' / RUN / f'model_{STEP}'
    source = checkpoint / 'sim2sim/actor'
    config = json.loads((source / 'config.json').read_text())
    manifest = json.loads((source / 'manifest.json').read_text())
    metadata = json.loads((checkpoint / 'ddt.json').read_text())
    pi = config['policy_interface']
    assert digest(checkpoint / 'actor.pt') == metadata['actor_sha256'] == manifest['checkpoint_sha256'] == pi['checkpoint_sha256']
    assert digest(source / 'policy.onnx') == manifest['onnx_sha256'] == pi['onnx_sha256']
    assert digest(source / 'config.json') == manifest['config_sha256']
    assert config['policy']['obs_dim'] == metadata['actor_obs_dim'] == 35 and metadata['action_dim'] == 8
    assert metadata['task'] == 'DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObsW0-v0', metadata['task']
    assert pi['leg_action_filter'] == 'none'
    assert config['robot'] == reference['robot'] and config['control'] == reference['control']
    assert pi['observations'][:-1] == reference['policy_interface']['observations']
    heading = pi['observations'][-1]
    assert heading['kind'] == 'heading_error' and heading['params']['warmup_s'] == 0.0 and heading['size'] == 1
    assert pi['actions'] == reference['policy_interface']['actions']
    assert not (policies / BUNDLE).exists(), 'Refusing to overwrite a bundle'
    torch.set_num_threads(2)
    samples = torch.randn(256, 35, generator=torch.Generator().manual_seed(31415)) * 2
    actor = load_policy(checkpoint, metadata)
    with torch.inference_mode():
        actual = actor(samples)
        means = actor.actor.get_mean_and_std(samples, training=False)[0].tanh()
        native = means * torch.where(means >= 0, actor.action_gain_positive, actor.action_gain_negative)
        torch.testing.assert_close(actual, native, atol=1e-5, rtol=1e-4)
    bundle = policies / BUNDLE
    bundle.mkdir()
    source_config_sha = digest(source / 'config.json')
    config['command'] = dict(max_lin_x=1., max_ang_z=1.)
    (bundle / 'config.json').write_text(json.dumps(config, indent=2) + '\n')
    shutil.copyfile(source / 'policy.onnx', bundle / 'policy.onnx')
    manifest.update(execution_domain='DESKTOP_DRY_RUN', config_sha256=digest(bundle / 'config.json'),
                    hardware_status='NOT_TESTED', deployment_overrides=dict(
                        command=config['command'], source_config_sha256=source_config_sha,
                        source_run=f'{RUN}/model_{STEP}',
                        note='Training observations/actions/gains retained (no MA2, heading_error warmup 0); '
                             'real joystick caps 1/1 and 0.5/s ramp; gyro bias from pre-RL stationary samples.'))
    (bundle / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    row = dict(bundle=BUNDLE, run=RUN, step=STEP, checkpoint_sha256=pi['checkpoint_sha256'],
               onnx_sha256=pi['onnx_sha256'], config_sha256=manifest['config_sha256'],
               source_config_sha256=source_config_sha, task=metadata['task'], leg_action_filter='none',
               execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS')
    print(json.dumps(row, indent=1))


if __name__ == '__main__':
    main()
