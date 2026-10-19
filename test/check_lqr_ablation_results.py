"""VALIDATION_SIM: audit completed paired episodes and actual motor responses."""

import argparse
import json
from pathlib import Path
import sys

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from sim2sim.lqr.model import discrete, dlqr
from sim2sim.lqr.evaluate import write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    directory = args.directory
    cfg = json.loads((directory / 'config.json').read_text())
    manifest = json.loads((directory / 'manifest.json').read_text())
    results = [json.loads(line) for line in (directory / 'results.jsonl').read_text().splitlines()]
    expected = len(cfg['mismatches'])*len(cfg['seeds'])*len(cfg['pitch_disturbances_rad'])*10
    assert len(results) == expected, (len(results), expected)
    identities = [(r['mode'], r['mismatch'], r['seed'], r['pitch_delta_rad'], r['phase']) for r in results]
    assert len(set(identities)) == len(results)
    mismatch_map = {m['name']: m for m in cfg['mismatches']}
    params = manifest['nominal_parameters']
    max_motor_error = 0.
    initial_conditions = {}
    for r in results:
        assert r['checkpoint_sha256'] == manifest['checkpoint_sha256']
        mismatch = mismatch_map[r['mismatch']]
        with np.load(directory / r['trace']) as a:
            assert np.isfinite(a['state']).all()
            assert np.max(abs(a['motor_substeps'])) <= 12.+1e-5
            assert np.all(np.max(abs(a['coefficients']), axis=0) <= cfg['controller']['rls']['bounds'])
            assert abs(a['time'][-1]-r['completed_s']) < 1e-8
            if not r['failure']:
                assert abs(r['completed_s']-12.) < 1e-8
            key = (r['mismatch'], r['seed'], r['pitch_delta_rad'])
            initial = np.r_[a['gt_position'][0], a['gt_velocity'][0], a['state'][0]]
            if key in initial_conditions:
                np.testing.assert_allclose(initial, initial_conditions[key], atol=1e-7)
            else:
                initial_conditions[key] = initial
            if r['mode'] in ('A', 'B'):
                continue
            dimension = int(r['mode'][-1])
            A, B = discrete(params, .02, dimension)
            K0, _ = dlqr(A, B, np.diag(cfg['controller']['Q4'][-dimension:]), cfg['controller']['R'])
            if r['phase'] in ('evaluation', 'adaptation'):
                np.testing.assert_allclose(a['gain'][0, -dimension:], K0)
                np.testing.assert_array_equal(a['coefficients'][0], np.zeros(4))
            if r['phase'] == 'frozen':
                np.testing.assert_allclose(a['gain'], np.broadcast_to(a['gain'][0], a['gain'].shape))
                np.testing.assert_allclose(a['coefficients'], np.broadcast_to(a['coefficients'][0], a['coefficients'].shape))
            if r['mode'].startswith('C'):
                np.testing.assert_allclose(a['gain'][:, -dimension:], np.broadcast_to(K0, a['gain'][:, -dimension:].shape))
            command = a['command_torque']
            assert np.max(abs(np.diff(command, axis=0))) <= cfg['controller']['slew_nm_s']*.02/2+1e-5
            state = np.zeros(2)
            predicted = [np.zeros(2)]
            gain = mismatch.get('motor_gain', 1.)
            lag = mismatch.get('motor_lag_s', 0.)
            for row in command[1:]:
                substeps = []
                for _ in range(4):
                    target = row*gain
                    state = state+(1-np.exp(-.005/lag))*(target-state) if lag else target.copy()
                    substeps.append(np.clip(state, -12., 12.))
                predicted.append(np.mean(substeps, axis=0))
            error = float(np.max(abs(np.asarray(predicted)-a['motor_torque'])))
            max_motor_error = max(max_motor_error, error)
            assert error < 1e-5, (r['trace'], error)
    result = dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
                  checkpoint_sha256=manifest['checkpoint_sha256'], episodes=len(results),
                  paired_initial_conditions=len(initial_conditions), max_motor_response_error_nm=max_motor_error,
                  checks=['complete unique episode matrix', 'paired initial conditions', 'finite observations',
                          'motor clipping and exact gain/lag response', 'nominal cold start', 'fixed Q/R gain',
                          'frozen gain and residual coefficients', 'residual bounds', 'torque slew'])
    write_json(directory / 'integrity.json', result)
    print('[VALIDATION_SIM] '+json.dumps(result))


if __name__ == '__main__':
    main()
