"""VALIDATION_SIM: add read-only IMU yaw-rate/base-point measurements to M4 logs.

Reconstruct the original prefixes and replay identical residual inputs. Existing
policy, estimator, action history, wheel/leg torques and archives are unchanged.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
import json
from pathlib import Path
import pickle

import numpy as np

from eval_flash_state_learning import StateRunner, STATE_KEYS
from eval_flash_operating_local import BIAS
from eval_flash_pv_models import REPO, CKPT, prepared_config, write, sha256
from analyze_flash_state_learning import state

SOURCE = REPO/'docs/exp/2026-10-15/flash_operating_local/full'


def imu_yaw_rate(rpy, gyro):
    """ZYX heading derivative from simultaneous body-frame angular velocity.

    This is neither body gyro-z nor world-vertical angular velocity in general.
    No future angle differences, GT velocity or absolute heading is used.
    """
    roll, pitch = np.asarray(rpy)[..., 0], np.asarray(rpy)[..., 1]
    assert np.all(abs(np.cos(pitch)) > .5)
    return (np.sin(roll)*np.asarray(gyro)[..., 1]+
            np.cos(roll)*np.asarray(gyro)[..., 2])/np.cos(pitch)


def extra(r):
    d, m = r.sensors, r.env.model
    base = m.body('base_link').id
    pos = d.xpos[base].copy()
    jac = np.zeros((3, m.nv))
    r.env.mujoco.mj_jac(m, d, jac, None, pos, base)
    yaw = r.observation['rpy'][2]
    return dict(yaw_rate=np.asarray([imu_yaw_rate(r.observation['rpy'], r.observation['gyro'])]),
        gyro=r.observation['gyro'].copy(), base_position=pos,
        base_velocity=np.asarray([(jac@d.qvel)@np.array([np.cos(yaw), np.sin(yaw), 0.])]))


def replay(r, request, archive=None):
    rows, steps = [], []
    for i in range(len(request)+1):
        if archive is not None:
            for k in STATE_KEYS:
                np.testing.assert_array_equal(r.observation[k], archive[k][i])
        assert not r.failures(), r.failures()
        rows.append(extra(r))
        if i < len(request):
            step = r.step(float(request[i]))
            if archive is not None:
                for k in step:
                    np.testing.assert_array_equal(step[k], archive[k][i])
            steps.append(step)
    result = {k:np.asarray([row[k] for row in rows]) for k in rows[0]}
    if archive is None:
        result['final_state'] = np.r_[r.observation['sensor'], result['yaw_rate'][-1],
            r.observation['previous_action'], r.observation['leg_position'], r.observation['leg_velocity']]
        result['actual_u'] = np.asarray([s['actual_u'] for s in steps])
    return result


def collect(cfg, job, output):
    original = SOURCE/job['id']
    out = Path(output)/job['id']
    out.mkdir()
    info = json.loads((original/'results.json').read_text())
    r = StateRunner(cfg, job)
    snapshots = {}
    try:
        prefix_s = 30. if job['approach']=='high' else 8.
        tau = 0.
        for i in range(round(prefix_s/.02)):
            if i >= 50:
                assert not r.failures()
            tau = min(.6, tau+.04) if job['approach']=='high' else 0.
            r.step(tau)
        ticks = [round(t/.02) for t in job['times']]
        with np.load(original/'prefix.npz') as old, np.load(original/'initial_states.npz') as initial:
            requests = old['requested_u']
            for i in range(max(ticks)+1):
                if i in ticks:
                    ix = ticks.index(i)
                    for k in STATE_KEYS:
                        np.testing.assert_array_equal(r.observation[k], old[k][i])
                    for k in ['qpos','qvel','ctrl','act']:
                        np.testing.assert_array_equal(getattr(r.env.data, k), initial[k][ix])
                    np.testing.assert_array_equal(r.playback.last_action, initial['last_action'][ix])
                    snapshots[i] = r.snapshot()
                    with gzip.open(out/f'snapshot_t{i}.pkl.gz', 'wb', compresslevel=1) as f:
                        pickle.dump(snapshots[i], f)
                    print('[VALIDATION_SIM]', job['id'], 'exact snapshot', i*.02, flush=True)
                if i < max(ticks):
                    assert not r.failures()
                    r.step(float(requests[i]))
        direct = []
        for tick, snapshot in snapshots.items():
            names = [f'zero_t{tick}.npz']+[row['trace'] for row in info['responses']
                if round(row['start_hold_s']/.02)==tick]
            for name in names:
                r.restore(snapshot)
                with np.load(original/name) as old:
                    # Materialize once: NPZ item access otherwise decompresses on every sample.
                    values = {k:old[k] for k in old.files}
                measured = replay(r, values['requested_u'], values)
                np.savez_compressed(out/name, **measured)
            for amplitude in [.005,.01,.02]:
                r.restore(snapshot); plus = replay(r, [BIAS+amplitude])
                r.restore(snapshot); minus = replay(r, [BIAS-amplitude])
                du = plus['actual_u'][0]-minus['actual_u'][0]
                b = (plus['final_state']-minus['final_state'])/du
                assert np.array_equal(b[5:13], np.zeros(8))
                old_b = next(x['sensor_B'] for x in info['direct_B']
                    if round(x['start_hold_s']/.02)==tick and x['amplitude']==amplitude)
                np.testing.assert_array_equal(np.delete(b,4), old_b)
                direct.append(dict(start_hold_s=tick*.02, amplitude=amplitude, B=b.tolist()))
        selected = [row for row in info['responses'] if round(row['start_hold_s']/.02) in snapshots]
        write(out/'results.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
            job=job, responses=selected, direct_B=direct,
            acquisitions=info['acquisitions'], exact_state_action_history_motor_replay=True,
            original=str(original.relative_to(REPO)), F1=False, base_point='base_link origin',
            yaw_rate='Euler heading derivative from synchronized IMU roll/pitch/body gyro'))
        result = dict(id=job['id'], responses=len(selected), snapshots=len(snapshots),
            direct_pairs=len(direct))
        print('[VALIDATION_SIM]', result, flush=True)
        return result
    finally:
        r.env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--workers', type=int, default=3)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(REPO/'docs/exp') and not out.exists()
    out.mkdir(parents=True)
    source = json.loads((SOURCE/'manifest.json').read_text())
    jobs = source['jobs']
    if args.smoke:
        jobs = [dict(jobs[0], times=[jobs[0]['times'][0]])]
        # Smoke replays only the selected snapshot's cases, separately from full analysis.
    config = prepared_config(CKPT)
    protected = [p for p in SOURCE.rglob('*') if p.is_file()]
    protected += list((REPO/'sim2sim/sim2sim_ros2_jazzy').rglob('*.py'))
    protected += [config, config.parent/'policy.onnx', CKPT/'actor.pt']
    hashes = {str(p.relative_to(REPO)):sha256(p) for p in protected}
    write(out/'manifest.json', dict(execution_domain='VALIDATION_SIM', evidence_status='NOT_TESTED',
        checkpoint_sha256=sha256(CKPT/'actor.pt'), onnx_sha256=sha256(config.parent/'policy.onnx'),
        jobs=jobs, protected_sha256=hashes, source_sha256=sha256(Path(__file__)), bias=BIAS,
        primary_reference='base_link origin', secondary_reference='wheel midpoint',
        state_definition='M4 unchanged sensor p/v; M5 inserts synchronized heading yaw_rate at index4',
        fit='same train samples, RMS-scaled LS, A first column translation, causal previous-action B zeros',
        primary_gate='median first2s and rolling0.1/0.5/1/2s p/v response NRMSE<=30%, direct Bv sign/error<=30%',
        improvement_gate='M5 passes primary gate; rolling2s v NRMSE and RMSE both improve >=10%; '
            'full8s p/v NRMSE each <=105% of M4; rolling2s v RMSE improves in >=5 of6 test initial contexts',
        conditional_LQR='only after improvement; same bias0.4828, Qp=Qv=250000,R400, cap0.05Nm,ramp1.5s,slew2Nm/s; '
            'base-link GT primary, wheel midpoint secondary; no Q/R search',
        note='Operational thresholds, not user quantitative requirements. M6 not implemented. '
            'Existing cohort remeasured; no new independent initial conditions. No estimator correction.'))
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for future in as_completed([pool.submit(collect,json.loads(config.read_text()),job,str(out)) for job in jobs]):
            results.append(future.result())
    assert all(sha256(REPO/p)==h for p,h in hashes.items())
    write(out/'completion.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
        results=results, protected_preserved=True, source_preserved=sha256(Path(__file__))==
            json.loads((out/'manifest.json').read_text())['source_sha256']))


if __name__=='__main__':
    main()
