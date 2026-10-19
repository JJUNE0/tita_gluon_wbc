"""DESKTOP_DRY_RUN: check exported bundle provenance and save native Torch actions; no robot SDK."""
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'lab/ddt_lab/scripts/flash_sac'))
from export import load_policy


def main():
    checkpoint = ROOT / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_180212_290240/model_50000'
    bundle = ROOT / 'sim2real/tita_ws/src/tita_controller/policies/flashsac_posma2_50000'
    source = checkpoint / 'sim2sim/actor'
    metadata = json.loads((checkpoint / 'ddt.json').read_text())
    config = json.loads((bundle / 'config.json').read_text())
    original = json.loads((source / 'config.json').read_text())
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = json.loads((bundle / 'manifest.json').read_text())
    for name, key in [('policy.onnx', 'onnx_sha256'), ('config.json', 'config_sha256')]:
        assert digest(bundle / name) == manifest[key]
    assert digest(checkpoint / 'actor.pt') == metadata['actor_sha256'] == manifest['checkpoint_sha256']
    assert config['policy_interface'] == original['policy_interface']
    assert config['robot'] == original['robot']
    assert config['policy']['obs_dim'] == 34 and metadata['action_dim'] == 8
    assert config['policy_interface']['leg_action_filter'] == 'ma2_legs'
    assert config['command'] == dict(max_lin_x=1., max_ang_z=1.)
    original['command'] = config['command']
    assert config == original
    torch.set_num_threads(2)
    actor = load_policy(checkpoint, metadata)
    samples = torch.randn(256, 34, generator=torch.Generator().manual_seed(31415)) * 2
    with torch.inference_mode():
        actual = actor(samples)
        means = actor.actor.get_mean_and_std(samples, training=False)[0].tanh()
        native = means * torch.where(means >= 0, actor.action_gain_positive, actor.action_gain_negative)
        torch.testing.assert_close(actual, native, atol=1e-5, rtol=1e-4)
    out = ROOT / 'test/sim2real/posma2_50000'
    out.mkdir(exist_ok=True)
    np.savetxt(out / 'obs.txt', samples.numpy(), fmt='%.9g')
    np.save(out / 'expected.npy', native.numpy())
    print('PASS DESKTOP_DRY_RUN: checkpoint/config provenance, native action gains; 256 x 34 Torch fixture')


if __name__ == '__main__':
    main()
