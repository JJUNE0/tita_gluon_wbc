"""ROBOT_COMMAND_FREE_RUNTIME: verify the installed flashsac_headw0_50000 bundle on the robot (no ROS nodes/SDK/CAN).

- flashsac.launch.py ``validate_policy`` accepts the installed bundle (SHA pins);
- tita.launch.py ``policy_parameters`` passes the heading observation (kind index, clip, warmup 0, thresholds) and
  leg_action_filter none;
- ARM ONNX inference equals the native Torch reference (desktop fixture);
- ARM C++ ObservationBuilder heading/position sequence equals the desktop Python sim2sim output.
usage: python3 verify_heading_bundle.py <share dir> <fixture dir> --inference ACTUAL --parity ACTUAL --result JSON
"""
import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np

BUNDLE = 'flashsac_headw0_50000'  # override with --bundle


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('share', type=Path)
    ap.add_argument('fixtures', type=Path)
    ap.add_argument('--inference', type=Path, required=True)
    ap.add_argument('--parity', type=Path, required=True)
    ap.add_argument('--result', type=Path, required=True)
    ap.add_argument('--bundle', default=BUNDLE)
    a = ap.parse_args()
    bundle = a.bundle
    policy_dir = a.share / 'policies' / bundle
    flashsac = load(a.share / 'launch/flashsac.launch.py', 'flashsac_launch')
    tita = load(a.share / 'launch/tita.launch.py', 'tita_launch')
    flashsac.validate_policy(policy_dir)
    p = tita.policy_parameters(policy_dir)
    checks = {
        'validate_policy_pins': True,
        'heading_obs_kind': tita.OBS_KINDS.index('heading_error') == 8 and p['obs_kind'][-1] == 8 and len(p['obs_kind']) == 35,
        'heading_params': p['heading_clip_rad'] == 0.5 and p['heading_warmup_s'] == 0.0
        and p['heading_zero_thresholds'] == [0.02, 0.02, 0.03],
        'leg_filter_none': p['leg_action_filter'] == 'none',
        'command_caps': p['max_lin_x'] == 1.0 and p['max_ang_z'] == 1.0,
    }
    fixture = a.fixtures / bundle
    inference_err = float(np.abs(np.loadtxt(a.inference) - np.loadtxt(fixture / 'expected.txt')).max())
    parity_actual, parity_expected = np.loadtxt(a.parity), np.loadtxt(fixture / 'heading_parity_expected.txt')
    parity_err = float(np.abs(parity_actual - parity_expected).max()) if parity_actual.shape == parity_expected.shape else float('inf')
    checks['arm_onnx_vs_torch'] = inference_err < 1e-5
    checks['arm_heading_parity'] = parity_err < 1e-5
    result = dict(execution_domain='ROBOT_COMMAND_FREE_RUNTIME', bundle=bundle, checks=checks,
                  inference_max_abs_error=inference_err, heading_parity_max_abs_error=parity_err,
                  evidence_status='PASS' if all(checks.values()) else 'FAIL')
    a.result.write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps(result))
    if result['evidence_status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
