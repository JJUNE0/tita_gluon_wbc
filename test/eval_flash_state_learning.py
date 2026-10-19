"""VALIDATION_SIM: action/leg state ablation and independent data-size cohorts.

Reuses the frozen model_60000 actor and validated synchronized Runner. No
production source, policy, F-1 feedback, LQR or online adaptation is changed.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path

import numpy as np

from eval_flash_pv_models import Runner, REPO, CKPT, WHEELS, LEGS, waveform, write, prepared_config, sha256

OLD = REPO/'docs/exp/2026-10-15/flash_pv_model_comparison/full'
STATE_KEYS = ['sensor', 'gt', 'position', 'rpy', 'previous_action', 'leg_position', 'leg_velocity']
MODELS = {
    'M0': list(range(2)), 'M1': list(range(4)), 'M2': list(range(12)),
    'M3': list(range(4))+list(range(12, 24)), 'M4': list(range(24)),
}


class StateRunner(Runner):
    def observe(self):
        result = super().observe()
        result.update(previous_action=self.playback.last_action.copy(),
            leg_position=self.env.joint_pos()[LEGS], leg_velocity=self.env.joint_vel()[LEGS])
        return result

    def rollout(self, inputs):
        states, transitions = [], []
        for i in range(len(inputs)+1):
            states.append({key: self.observation[key].copy() for key in STATE_KEYS})
            failures = self.failures()
            if failures or i == len(inputs):
                break
            transitions.append(self.step(float(inputs[i])))
        trace = {k: np.asarray([s[k] for s in states]) for k in STATE_KEYS}
        if transitions:
            trace.update({k: np.asarray([r[k] for r in transitions]) for k in transitions[0]})
            np.testing.assert_array_equal(trace['previous_action'][:-1], trace['history'])
            np.testing.assert_array_equal(trace['previous_action'][1:], trace['action'])
        return trace, failures


def make_inputs(family, amplitude, seed, count):
    if family != 'micro_prbs':
        return waveform(family, amplitude, seed, count)
    requested = np.random.default_rng(seed).choice([-amplitude, amplitude], count)
    previous, result = 0., []
    for value in requested:
        previous = float(np.clip(value, previous-.04, previous+.04))
        result.append(previous)
    return np.asarray(result)


def probes(split):
    families = ['train_sine', 'train_prbs'] if split == 'train' else ['validation_sine', 'validation_prbs']
    families += ['pulse_pos', 'pulse_neg', 'step_pos', 'step_neg']
    return [(f, a) for f in families for a in [.1, .25, .5]] + [('micro_prbs', a) for a in [.01, .02, .04]]


def prefix_inputs(job, count):
    result = np.zeros(count)
    if job['cohort'] == 'archive':
        return result
    rng = np.random.default_rng(np.random.SeedSequence([job['seed'], job['pitch_index'], 391]))
    phases = rng.uniform(-np.pi, np.pi, 3)
    previous = 0.
    for i in range(count):
        t = i*.02
        target = .2*np.mean(np.sin(2*np.pi*np.array([.4, 1.3, 3.7])*t+phases)) if 1. <= t < 3.88 else 0.
        previous = float(np.clip(target, previous-.04, previous+.04))
        result[i] = previous
    assert np.max(abs(result[200:])) == 0.
    return result


def job_run(cfg, job, root):
    out = Path(root)/job['id']
    out.mkdir()
    runner = StateRunner(cfg, job)
    old = None
    if job['cohort'] == 'archive':
        old = json.loads((OLD/job['old_id']/'results.json').read_text())
    count = 100 if old else 200
    end = round(max(job['times'])/.02)+count
    inputs = prefix_inputs(job, end)
    states, transitions, snapshots, startup = [], [], {}, []
    exact_keys = ['sensor', 'gt', 'position', 'rpy', 'action', 'motor', 'flash', 'policy_observation', 'history', 'actual_u', 'requested_u']
    try:
        for tick in range(end+1):
            states.append({k: runner.observation[k].copy() for k in STATE_KEYS})
            failures = runner.failures()
            if tick < 50 and failures:
                startup.append(dict(rl_s=tick*.02, failures=failures))
            elif tick >= 50:
                assert not failures, (job, tick, failures)
            if tick in [round(t/.02) for t in job['times']]:
                snapshots[tick] = runner.snapshot()
            if tick < end:
                transitions.append(runner.step(inputs[tick]))
        prefix = {k: np.asarray([r[k] for r in states]) for k in STATE_KEYS}
        prefix.update({k: np.asarray([r[k] for r in transitions]) for k in transitions[0]})
        if old:
            with np.load(OLD/job['old_id']/'prefix.npz') as archive:
                for k in exact_keys:
                    np.testing.assert_array_equal(prefix[k], archive[k])
        np.savez_compressed(out/'prefix.npz', **prefix)
        responses, direct, replay = [], [], []
        for tick, snapshot in snapshots.items():
            runner.restore(snapshot)
            zero, failure = runner.rollout(np.zeros(count))
            assert not failure
            assert np.max(abs(inputs[tick:tick+count])) == 0.
            for k in STATE_KEYS:
                np.testing.assert_array_equal(zero[k], prefix[k][tick:tick+count+1])
            for k in ['action', 'motor', 'flash', 'policy_observation', 'history']:
                np.testing.assert_array_equal(zero[k], prefix[k][tick:tick+count])
            base_name = f'zero_t{tick}.npz'
            np.savez_compressed(out/base_name, **zero)
            replay.append(tick)
            if old:
                cases = [r for r in old['responses'] if round(r['start_rl_s']/.02) == tick]
            else:
                cases = []
                for index, (family, amplitude) in enumerate(probes(job['split'])):
                    seed = int(np.random.SeedSequence([job['seed'], job['pitch_index'], tick, index,
                        117 if job['split'] == 'train' else 991]).generate_state(1)[0])
                    cases.append(dict(family=family, amplitude=amplitude, input_seed=seed))
            for row in cases:
                if old:
                    with np.load(OLD/job['old_id']/row['trace']) as archive:
                        request = archive['requested_u'].copy()
                else:
                    request = make_inputs(row['family'], row['amplitude'], row['input_seed'], count)
                runner.restore(snapshot)
                trace, failure = runner.rollout(request)
                assert not failure and len(trace['sensor']) == count+1, (job, row, failure)
                assert max(abs(trace['actual_u']-request)) < 1e-6
                assert max(abs(trace['actual_u'])) <= .500001
                assert max(abs(np.diff(np.r_[0., trace['actual_u']]))) <= .040001
                if old:
                    with np.load(OLD/job['old_id']/row['trace']) as archive:
                        for k in exact_keys:
                            np.testing.assert_array_equal(trace[k], archive[k])
                name = f'{row["family"]}_a{row["amplitude"]:g}_t{tick}.npz'
                np.savez_compressed(out/name, **trace)
                responses.append(dict(trace=name, baseline=base_name, family=row['family'],
                    amplitude=row['amplitude'], input_seed=row['input_seed'], start_rl_s=tick*.02,
                    transitions=count, failures=failure))
            for amp in [.01, .02, .04]:
                runner.restore(snapshot); positive, pf = runner.rollout([amp])
                runner.restore(snapshot); negative, nf = runner.rollout([-amp])
                assert not pf and not nf
                np.testing.assert_array_equal(positive['action'][0], zero['action'][0])
                np.testing.assert_array_equal(negative['action'][0], zero['action'][0])
                denominator = positive['actual_u'][0]-negative['actual_u'][0]
                row = dict(start_rl_s=tick*.02, amplitude=amp)
                for source in ['sensor', 'gt']:
                    b = []
                    for k in [source, 'previous_action', 'leg_position', 'leg_velocity']:
                        b.extend((positive[k][1]-negative[k][1])/denominator)
                    np.testing.assert_array_equal(b[4:12], np.zeros(8))
                    row[source+'_B'] = np.asarray(b).tolist()
                direct.append(row)
        result = dict(execution_domain='VALIDATION_SIM', evidence_status='PASS', job=job,
            startup_violations=startup, exact_zero_replay_ticks=replay, responses=responses,
            direct_B=direct, archive_exact=bool(old),
            history_alignment='z[t].previous_action=a[t-1]; z[t+1].previous_action=a[t]',
            state_order='p,v,pitch,pitch_rate,raw_actor_previous8,leg_position6,leg_velocity6',
            F1_feedback=False, LQR=False)
        write(out/'results.json', result)
        return dict(id=job['id'], cohort=job['cohort'], split=job['split'], responses=len(responses),
            direct_pairs=len(direct), zero_replays=len(replay), archive_exact=bool(old))
    finally:
        runner.env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--stage', choices=['archive', 'expanded', 'smoke'], required=True)
    parser.add_argument('--workers', type=int, default=3)
    args = parser.parse_args()
    out = args.output.resolve()
    if not out.is_relative_to(REPO/'docs/exp') or out.exists():
        parser.error('New output under docs/exp required')
    out.mkdir(parents=True)
    config = prepared_config(CKPT)
    if config is None:
        raise RuntimeError('Verified model_60000 export required')
    cfg = json.loads(config.read_text())
    jobs = []
    if args.stage == 'archive':
        for path in sorted(OLD.glob('*/results.json')):
            old = json.loads(path.read_text())['job']
            jobs.append(dict(**old, cohort='archive', old_id=old['id']))
    else:
        for split, seeds in [('train', range(100, 108)), ('test', range(110, 114))]:
            for seed in seeds:
                for pindex, pitch in enumerate([-.035, 0., .035]):
                    jobs.append(dict(id=f'{split}_s{seed}_p{pitch:+.3f}', split=split, cohort='expanded',
                        seed=seed, pitch=pitch, pitch_index=pindex, times=[4., 8.] if split=='train' else [5., 9.]))
    if args.stage == 'smoke':
        jobs = [dict(id='train_s99_p0', split='train', cohort='expanded', seed=99,
                     pitch=0., pitch_index=1, times=[4.])]
    protected = list((REPO/'sim2sim/sim2sim_ros2_jazzy').rglob('*.py'))
    protected += [REPO/'sim2sim/lqr'/f for f in ['runtime.py', 'model.py', 'estimator.py']]
    protected += [REPO/'test/eval_flash_pv_models.py', config, config.parent/'policy.onnx', CKPT/'actor.pt']
    hashes = {str(p.relative_to(REPO)): sha256(p) for p in protected}
    write(out/'manifest.json', dict(execution_domain='VALIDATION_SIM', evidence_status='NOT_TESTED',
        checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
        onnx_sha256=sha256(config.parent/'policy.onnx'), script_sha256=sha256(Path(__file__)),
        stage=args.stage, jobs=jobs, protected_sha256=hashes,
        models=MODELS, model_order='M0=old M1(2-state); M1=old M2(4-state)',
        constraints='position translation first A column; next previous-action B rows exactly0 by causality',
        validation='Predict all selected states recursively; no future measured action/leg states',
        learning_curve=dict(nested_context_counts=[1, 2, 3, 6, 12, 24], contexts_per_full_train=24,
            responses_per_context=42, transitions_per_response=200, permutation_seeds=[701, 702, 703]),
        input_plan='4s sine/PRBS/positive-negative pulse/step amplitudes0.1/0.25/0.5; microPRBS0.01/0.02/0.04; slew2Nm/s',
        prefix_plan='new cohort: seeded0.2Nm total max conditioning at RL1..3.88s, zero by4s; zero command throughout',
        criteria='only direct B sign/magnitude,held-out p/v prediction0.1..2s,learning curve',
        operating_gate='diagnostic30% p/v NRMSE at0.1/0.5/1/2s and first2s full response; direct velocity B relative error<=30%',
        scope='stage1 state/data identification; no stop-affine model, LQR gain or online control'))
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        future_jobs = [pool.submit(job_run, cfg, job, str(out)) for job in jobs]
        for future in as_completed(future_jobs):
            result = future.result()
            results.append(result)
            print('[VALIDATION_SIM]', result, flush=True)
    assert all(sha256(REPO/p) == value for p, value in hashes.items())
    write(out/'completion.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS', jobs=results,
        protected_files_preserved=True, responses=sum(r['responses'] for r in results),
        direct_pairs=sum(r['direct_pairs'] for r in results), zero_replays=sum(r['zero_replays'] for r in results)))


if __name__ == '__main__':
    main()
