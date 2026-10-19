"""DESKTOP_DRY_RUN: build the robot bundle ``policies/flashsac_c2_60000`` from the evaluation-only export.

Source is the C2 (``DDT-Velocity-Flat-Tita-My-LegScale-Reward-v0``) ``model_60000`` export of
``test/export_ab_checkpoints.py``. That export ran only after checking that the policy interface and
action mapping are byte-identical to 115632, with ONNX parity of 256 samples and max error 3.3e-6.

The ONNX is copied unchanged. The config takes the same command-range override as the deployed A80k
bundle (``max_lin_x``/``max_ang_z`` 1.0). The robot gains stay at the training defaults (legs 60/1.5,
wheel Kd 0.5, caps 60/12). Operator decision 2026-10-18: there is no deployment-side leg compensation,
because C2 learned the leg scale in training.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EXPORT = REPO / 'docs/exp/2026-10-18/flashsac_legscale_sim2sim/exports/tita_flash_sac_114500_483968_model_60000'
BUNDLE = REPO / 'sim2real/tita_ws/src/tita_controller/policies/flashsac_c2_60000'
CHECKPOINT_SHA256 = 'b4c8ae072787c3119864e75c2ebfbaf8284a02976dc68f1f282ad9480ae2e116'
ONNX_SHA256 = 'b12e40267bb3247762b0dd6283bd9f9cafffac52597ca74b387790bb4e925b7f'
LEG_KP, LEG_KD = [60., 60., 60., 0., 60., 60., 60., 0.], [1.5, 1.5, 1.5, .5, 1.5, 1.5, 1.5, .5]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert not BUNDLE.exists(), f'{BUNDLE} exists; refusing to overwrite'
    source = json.loads((EXPORT / 'config.json').read_text())
    manifest = json.loads((EXPORT / 'manifest.json').read_text())
    assert digest(EXPORT / 'policy.onnx') == ONNX_SHA256 == manifest['onnx_sha256'] == source['policy_interface']['onnx_sha256']
    assert manifest['checkpoint_sha256'] == CHECKPOINT_SHA256 == source['policy_interface']['checkpoint_sha256']
    assert digest(EXPORT / 'config.json') == manifest['config_sha256']
    assert source['robot']['joint_kp'] == LEG_KP and source['robot']['joint_kd'] == LEG_KD
    assert source['robot']['torque_limit'] == [60., 60., 60., 12., 60., 60., 60., 12.]
    config = json.loads(json.dumps(source))
    config['command'] = dict(max_lin_x=1.0, max_ang_z=1.0)
    BUNDLE.mkdir(parents=True)
    shutil.copyfile(EXPORT / 'policy.onnx', BUNDLE / 'policy.onnx')
    (BUNDLE / 'config.json').write_text(json.dumps(config, indent=2) + '\n')
    manifest.update(config_sha256=digest(BUNDLE / 'config.json'), deployment_overrides=dict(
        command=config['command'], source_config_sha256=digest(EXPORT / 'config.json'),
        robot=dict(joint_kp=LEG_KP, joint_kd=LEG_KD, note='training defaults; no deployment-side leg compensation'),
        source_task='DDT-Velocity-Flat-Tita-My-LegScale-Reward-v0', source_run='tita_flash_sac_114500_483968/model_60000',
        selection='docs/exp/2026-10-18/flashsac_legscale_sim2sim.md (section 3a)', hardware_status='NOT_TESTED'))
    (BUNDLE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    assert digest(BUNDLE / 'policy.onnx') == ONNX_SHA256
    for name in ('policy.onnx', 'config.json', 'manifest.json'):
        print(f'{digest(BUNDLE / name)}  policies/flashsac_c2_60000/{name}')


if __name__ == '__main__':
    main()
