"""VALIDATION_SIM: near-stop snapshots, then release F-1 AND bias in both arms.

Baseline is original FlashSAC, residual branch is FlashSAC plus prescribed
probing torque. Prior acquisition prefixes are reproduced exactly. No LQR.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path

import numpy as np

from eval_flash_stop_local import StopRunner
from eval_flash_state_learning import STATE_KEYS, make_inputs
from eval_flash_pv_models import Runner, REPO, CKPT, prepared_config, sha256, write

ACQUISITION = REPO/'docs/exp/2026-10-15/flash_stop_local/full'
OLD_MODELS = REPO/'docs/exp/2026-10-15/flash_state_learning/expanded/state_models_frozen.json'


def inputs_for(family, amplitude, seed, count=200):
    if not family.startswith('bipulse'):
        return make_inputs(family, amplitude, seed, count)
    t = np.arange(count)*.02
    target = amplitude*((.1 <= t)&(t < .35))-amplitude*((.8 <= t)&(t < 1.15))
    if family.endswith('neg'):
        target = -target
    result, previous = [], 0.
    for value in target:
        previous = float(np.clip(value, previous-.04, previous+.04))
        result.append(previous)
    return np.asarray(result)


def prohibit_hold(*args):
    raise AssertionError('F-1 update during released probing is forbidden')


def job_run(cfg, job, root):
    out = Path(root)/job['id']
    out.mkdir()
    runner = StopRunner(cfg, job)
    ticks = [round(t/.02) for t in job['times']]
    snapshots, initial, prefix_states, prefix_steps = {}, [], [], []
    try:
        for tick in range(max(ticks)+1):
            prefix_states.append({k: runner.observation[k].copy() for k in STATE_KEYS})
            if tick >= 50:
                assert not runner.failures(), (job, tick, runner.failures())
            if tick in ticks:
                snapshots[tick] = runner.snapshot()
                initial.append(dict(tick=tick, qpos=runner.env.data.qpos.copy(),
                    qvel=runner.env.data.qvel.copy(), ctrl=runner.env.data.ctrl.copy(),
                    previous_action=runner.playback.last_action.copy(),
                    acquired_hold_u=runner.hold.u, acquired_hold_p=runner.hold.position))
            if tick < max(ticks):
                if tick < 1000:
                    runner.mode = 'frozen'
                    runner.bias = min(.5, runner.bias+.04)
                else:
                    runner.mode = 'feedback'
                    runner.feedback_bias = .5
                prefix_steps.append(runner.step(0.))
        prefix = {k: np.asarray([r[k] for r in prefix_states]) for k in STATE_KEYS}
        prefix.update({k: np.asarray([r[k] for r in prefix_steps]) for k in prefix_steps[0]})
        with np.load(ACQUISITION/job['id']/'prefix.npz') as archived:
            for key, value in prefix.items():
                np.testing.assert_array_equal(value, archived[key][:len(value)])
        np.savez_compressed(out/'acquisition_prefix.npz', **prefix)
        np.savez_compressed(out/'snapshot_initial.npz', **{
            k: np.asarray([r[k] for r in initial]) for k in initial[0]})
        # No F-1 call, frozen residual, ramp tail or slew tail is allowed below.
        runner.mode = 'frozen'
        runner.bias = runner.feedback_bias = 0.
        runner.hold.update = prohibit_hold
        responses, direct = [], []
        for tick, snapshot in snapshots.items():
            runner.restore(snapshot)
            zero, failures = runner.rollout(np.zeros(200))
            assert not failures and len(zero['sensor']) == 201
            np.testing.assert_array_equal(zero['motor'], zero['flash'])
            np.testing.assert_array_equal(zero['actual_u'], np.zeros(200))
            np.testing.assert_array_equal(zero['bias'], np.zeros(200))
            # Independent baseline calls the original Runner directly, bypassing
            # the acquisition subclass, for every step and every observation.
            runner.restore(snapshot)
            for t in range(201):
                for key in STATE_KEYS:
                    np.testing.assert_array_equal(runner.observation[key], zero[key][t])
                if t < 200:
                    transition = Runner.step(runner, 0.)
                    for key in transition:
                        np.testing.assert_array_equal(transition[key], zero[key][t])
            baseline = f'zero_t{tick}.npz'
            np.savez_compressed(out/baseline, **zero)
            families = ['train_sine', 'train_prbs'] if job['split']=='train' else ['validation_sine', 'validation_prbs']
            families += ['pulse_pos', 'pulse_neg', 'step_pos', 'step_neg']
            if job['split']=='test':
                families += ['bipulse_pos', 'bipulse_neg']
            cases = [(f, a) for f in families for a in [.1, .25]]+[('micro_prbs', .02)]
            for i, (family, amplitude) in enumerate(cases):
                seed = int(np.random.SeedSequence([job['seed'], job['pitch_index'], tick, i, 4111]).generate_state(1)[0])
                probe = inputs_for(family, amplitude, seed)
                runner.restore(snapshot)
                trace, failures = runner.rollout(probe)
                assert not failures and len(trace['sensor']) == 201, (job, tick, family, failures)
                np.testing.assert_array_equal(trace['bias'], np.zeros(200))
                assert np.max(abs(trace['actual_u']-probe)) < 1e-6
                assert max(abs(trace['actual_u'])) <= .250001
                assert max(abs(np.diff(np.r_[0., trace['actual_u']]))) <= .040001
                for key in STATE_KEYS:
                    np.testing.assert_array_equal(trace[key][0], zero[key][0])
                np.testing.assert_array_equal(trace['action'][0], zero['action'][0])
                np.testing.assert_array_equal(trace['policy_observation'][0], zero['policy_observation'][0])
                filename = f'{family}_a{amplitude:g}_t{tick}.npz'
                np.savez_compressed(out/filename, **trace)
                responses.append(dict(trace=filename, baseline=baseline, family=family,
                    amplitude=amplitude, input_seed=seed, start_rl_s=tick*.02))
            for amplitude in [.01, .02, .04]:
                runner.restore(snapshot); plus, pf = runner.rollout([amplitude])
                runner.restore(snapshot); minus, mf = runner.rollout([-amplitude])
                assert not pf and not mf
                np.testing.assert_array_equal(plus['action'][0], zero['action'][0])
                np.testing.assert_array_equal(minus['action'][0], zero['action'][0])
                from analyze_flash_state_learning import state
                denominator = plus['actual_u'][0]-minus['actual_u'][0]
                b = (state(plus)[1]-state(minus)[1])/denominator
                np.testing.assert_array_equal(b[4:12], np.zeros(8))
                direct.append(dict(start_rl_s=tick*.02, amplitude=amplitude,
                    sensor_B=b.tolist(), gt_B=((plus['gt'][1]-minus['gt'][1])/denominator).tolist()))
        write(out/'results.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS', job=job,
            responses=responses, direct_B=direct, exact_acquisition_replay=True,
            exact_original_FlashSAC_zero_replays=len(snapshots), F1_update_calls_during_probing=0,
            residual_bias_during_probing=0., acquisition=job['acquisition'],
            actor='unchanged model_60000, synchronized current-state IMU',
            history='previous full raw actor output, no residual in action history',
            legs='original ActionAdapter, asserted unchanged at each physics step'))
        return dict(id=job['id'], split=job['split'], responses=len(responses),
            direct_pairs=len(direct), zero_replays=len(snapshots))
    finally:
        runner.env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=3)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    out = args.output.resolve()
    if not out.is_relative_to(REPO/'docs/exp') or out.exists():
        parser.error('New output under docs/exp required')
    out.mkdir(parents=True)
    jobs = []
    for path in sorted(ACQUISITION.glob('*/results.json')):
        old = json.loads(path.read_text())
        accepted = [a for a in old['acquisition'] if a['low_speed_gate']]
        if accepted:
            jobs.append(dict(old['job'], times=[a['start_rl_s'] for a in accepted], acquisition=accepted))
    if args.smoke:
        jobs = [next(j for j in jobs if j['split']=='test')]
    config = prepared_config(CKPT)
    cfg = json.loads(config.read_text())
    protected = list((REPO/'sim2sim/sim2sim_ros2_jazzy').rglob('*.py'))
    protected += [REPO/'sim2sim/lqr'/f for f in ['runtime.py','model.py','estimator.py']]
    protected += [REPO/'test'/f for f in ['eval_flash_pv_models.py','eval_flash_state_learning.py',
        'analyze_flash_state_learning.py','eval_flash_stop_local.py','analyze_flash_stop_local.py']]
    protected += [OLD_MODELS, ACQUISITION/'manifest.json', config, config.parent/'policy.onnx', CKPT/'actor.pt']
    hashes = {str(p.relative_to(REPO)): sha256(p) for p in protected}
    write(out/'manifest.json', dict(execution_domain='VALIDATION_SIM', evidence_status='NOT_TESTED',
        checkpoint_sha256=sha256(CKPT/'actor.pt'), onnx_sha256=sha256(config.parent/'policy.onnx'),
        script_sha256=sha256(Path(__file__)), protected_sha256=hashes, jobs=jobs,
        old_models_file=str(OLD_MODELS.relative_to(REPO)), old_models_sha256=sha256(OLD_MODELS),
        plan='old M2/M4 first; only on failure refit same structure using train only; no affine/LQR/equilibrium search',
        acquisition='exact replay of prior accepted +0.5Nm bias/F1-assisted low-speed prefixes, 2s RMS<=0.002m/s',
        probing='F1 and acquisition bias disabled identically at branch start; baseline residual0; probe only in other arm',
        input='4s, max0.25Nm total, slew2Nm/s; held-out bipolar pulses not in train',
        gate='same diagnostic30% median p/v at free first2s and rolling0.1/0.5/1/2s; Bv sign and error<=30%',
        direction='initial nonzero input dv sign and magnitude; later inverse responses evaluated as trajectories',
        models='unchanged M2(12), M4(24); all hidden states predicted recursively',
        limitations='near-stop initial conditions, not guaranteed stationary equilibrium after release'))
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(job_run, cfg, job, str(out)) for job in jobs]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print('[VALIDATION_SIM]', result, flush=True)
    assert all(sha256(REPO/p)==h for p,h in hashes.items())
    write(out/'completion.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS', jobs=results,
        responses=sum(r['responses'] for r in results), direct_pairs=sum(r['direct_pairs'] for r in results),
        zero_replays=sum(r['zero_replays'] for r in results), protected_files_preserved=True))


if __name__=='__main__':
    main()
