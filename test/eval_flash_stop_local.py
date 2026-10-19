"""VALIDATION_SIM: unchanged F-1 acquisition and matched near-stop responses.

Two plants are kept separate: F-1 feedback plus an external probe, and the
FlashSAC plant with F-1's snapshot torque held constant plus an external probe.
No runtime controller or M2/M4 state structure is changed.
"""

import argparse
import copy
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path

import numpy as np

from eval_flash_state_learning import StateRunner, STATE_KEYS, make_inputs
from eval_flash_pv_models import REPO, CKPT, prepared_config, sha256, write
from sim2sim_ros2_jazzy.residual_wheel_pd import ResidualWheelPD
from eval_flash_torque_residual import PositionVelocityResidual, DEFAULT_RESIDUAL


class StopRunner(StateRunner):
    def __init__(self, cfg, job):
        super().__init__(cfg, job)
        self.hold = ResidualWheelPD(self.env)
        self.mode = 'feedback'
        self.bias = 0.
        self.feedback_bias = 0.
        self.legacy = PositionVelocityResidual(DEFAULT_RESIDUAL, 1., self.observation['sensor'][0])
        self.rl_start = float(self.env.data.time)

    def step(self, probe):
        if self.mode == 'legacy_feedback':
            bias = self.legacy.command(self.observation['sensor'], self.env.data.time-self.rl_start, .02)[0]
        elif self.mode == 'feedback':
            self.hold.update(np.zeros(3))
            bias = self.feedback_bias+self.hold.u
        else:
            bias = self.bias
        result = super().step(bias+probe)
        result.update(probe=probe, bias=bias, hold_position=self.hold.position,
            hold_velocity=self.hold.velocity, hold_age=self.hold.age)
        return result

    def snapshot(self):
        keys = ['holding', 'position', 'velocity', 'age', 'u', 'previous', 'signs']
        return super().snapshot(), copy.deepcopy({k: getattr(self.hold, k) for k in keys})

    def restore(self, snapshot):
        base, hold = snapshot
        super().restore(base)
        for key, value in copy.deepcopy(hold).items():
            setattr(self.hold, key, value)


def pilot(cfg, out):
    runner = StopRunner(cfg, dict(seed=119, pitch=0., pitch_index=1))
    rows, steps, startup = [], [], []
    try:
        for tick in range(6001):
            rows.append({key: runner.observation[key].copy() for key in STATE_KEYS})
            failures = runner.failures()
            if failures and tick < 50:
                startup.append(dict(rl_s=tick*.02, failures=failures))
            elif failures:
                raise RuntimeError((tick, failures))
            if tick < 6000:
                steps.append(runner.step(0.))
        trace = {k: np.asarray([row[k] for row in rows]) for k in STATE_KEYS}
        trace.update({k: np.asarray([row[k] for row in steps]) for k in steps[0]})
        np.savez_compressed(out/'pilot.npz', **trace)
        windows = []
        for end in [5, 10, 20, 40, 60, 80, 100, 120]:
            sl = slice(round((end-2)/.02), round(end/.02))
            windows.append(dict(end_s=end, sensor_v_mean=float(trace['sensor'][sl, 1].mean()),
                sensor_v_rms=float(np.sqrt(np.mean(trace['sensor'][sl, 1]**2))),
                gt_v_mean=float(trace['gt'][sl, 1].mean()),
                gt_v_rms=float(np.sqrt(np.mean(trace['gt'][sl, 1]**2))),
                hold_p_mean=float(trace['hold_position'][sl].mean()),
                residual_mean=float(trace['bias'][sl].mean()), residual_std=float(trace['bias'][sl].std())))
        write(out/'pilot_summary.json', dict(execution_domain='VALIDATION_SIM',
            evidence_status='PASS', windows=windows, startup_violations=startup))
        print(json.dumps(windows, indent=2), flush=True)
    finally:
        runner.env.close()


def acquisition_scan(cfg, out):
    results = []
    for mode, bias in [('legacy_feedback', 0.), ('frozen', 0.), ('frozen', -.5),
                       ('frozen', .25), ('frozen', .5), ('frozen', 1.)]:
        runner = StopRunner(cfg, dict(seed=119, pitch=0., pitch_index=1))
        runner.mode = mode
        target_bias = bias
        rows, steps = [], []
        try:
            for tick in range(2001):
                rows.append({k: runner.observation[k].copy() for k in STATE_KEYS})
                failures = runner.failures()
                if failures and tick >= 50:
                    raise RuntimeError((mode, bias, tick, failures))
                if tick < 2000:
                    runner.bias = float(np.clip(target_bias, runner.bias-.04, runner.bias+.04))
                    steps.append(runner.step(0.))
            trace = {k: np.asarray([r[k] for r in rows]) for k in STATE_KEYS}
            trace.update({k: np.asarray([r[k] for r in steps]) for k in steps[0]})
            name = f'{mode}_bias{bias:+g}.npz'
            np.savez_compressed(out/name, **trace)
            results.append(dict(mode=mode, fixed_bias=bias, trace=name,
                sensor_v_mean_35_40=float(trace['sensor'][1750:2000, 1].mean()),
                gt_v_mean_35_40=float(trace['gt'][1750:2000, 1].mean()),
                applied_residual_mean=float(trace['actual_u'][1750:2000].mean())))
            print('[VALIDATION_SIM]', results[-1], flush=True)
        finally:
            runner.env.close()
    write(out/'scan_summary.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS', results=results))


def run_context(cfg, job, root):
    out = Path(root)/job['id']
    out.mkdir()
    runner = StopRunner(cfg, job)
    runner.mode = 'frozen'
    states, steps, snapshots, startup = [], [], {}, []
    count = 200
    end = round(max(job['times'])/.02)+count
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
                if tick < 1000:
                    runner.mode = 'frozen'
                    runner.bias = min(.5, runner.bias+.04)
                else:
                    runner.mode = 'feedback'
                    runner.feedback_bias = .5
                steps.append(runner.step(0.))
        prefix = {k: np.asarray([r[k] for r in states]) for k in STATE_KEYS}
        prefix.update({k: np.asarray([r[k] for r in steps]) for k in steps[0]})
        np.savez_compressed(out/'prefix.npz', **prefix)
        responses, direct, acquisitions, replays = [], [], [], []
        for tick, snapshot in snapshots.items():
            # All gate values are computed before any probing at this snapshot.
            sl = slice(tick-100, tick)
            sensor_rms = float(np.sqrt(np.mean(prefix['sensor'][sl, 1]**2)))
            gt_rms = float(np.sqrt(np.mean(prefix['gt'][sl, 1]**2)))
            acquired = sensor_rms <= .002 and gt_rms <= .002
            row = dict(start_rl_s=tick*.02, sensor_v_rms_2s=sensor_rms, gt_v_rms_2s=gt_rms,
                low_speed_gate=acquired, F1_active_age_s=prefix['hold_age'][tick-1],
                total_residual_mean_2s=float(prefix['actual_u'][sl].mean()),
                total_residual_std_2s=float(prefix['actual_u'][sl].std()))
            acquisitions.append(row)
            if not acquired:
                continue
            runner.restore(snapshot)
            runner.hold.update(np.zeros(3))
            frozen_bias = .5+runner.hold.u
            for mode in ['frozen', 'feedback']:
                runner.restore(snapshot)
                runner.mode, runner.bias, runner.feedback_bias = mode, frozen_bias, .5
                zero, failures = runner.rollout(np.zeros(count))
                assert not failures and len(zero['sensor']) == count+1, (job, mode, failures)
                runner.restore(snapshot)
                repeated, failure = runner.rollout(np.zeros(count))
                assert not failure
                for k in zero:
                    np.testing.assert_array_equal(zero[k], repeated[k])
                if mode == 'feedback':
                    for k in STATE_KEYS:
                        np.testing.assert_array_equal(zero[k], prefix[k][tick:tick+count+1])
                    for k in ['action', 'motor', 'policy_observation', 'history', 'bias']:
                        np.testing.assert_array_equal(zero[k], prefix[k][tick:tick+count])
                base_name = f'{mode}_zero_t{tick}.npz'
                np.savez_compressed(out/base_name, **zero)
                replays.append(dict(mode=mode, tick=tick))
                families = ['train_sine', 'train_prbs'] if job['split'] == 'train' else ['validation_sine', 'validation_prbs']
                cases = [(f, a) for f in families+['pulse_pos', 'pulse_neg', 'step_pos', 'step_neg'] for a in [.1, .25]]
                cases.append(('micro_prbs', .02))
                for index, (family, amplitude) in enumerate(cases):
                    seed = int(np.random.SeedSequence([job['seed'], job['pitch_index'], tick, index, 517]).generate_state(1)[0])
                    inputs = make_inputs(family, amplitude, seed, count)
                    runner.restore(snapshot)
                    trace, failures = runner.rollout(inputs)
                    assert not failures and len(trace['sensor']) == count+1, (job, mode, family, failures)
                    assert max(abs(trace['actual_u']-trace['bias']-inputs)) < 1e-6
                    assert max(abs(trace['actual_u'])) < 2.000001
                    np.testing.assert_array_equal(trace['sensor'][0], zero['sensor'][0])
                    name = f'{mode}_{family}_a{amplitude:g}_t{tick}.npz'
                    np.savez_compressed(out/name, **trace)
                    responses.append(dict(mode=mode, trace=name, baseline=base_name,
                        family=family, amplitude=amplitude, start_rl_s=tick*.02, input_seed=seed,
                        frozen_total_bias=frozen_bias if mode == 'frozen' else None))
                for amplitude in [.01, .02, .04]:
                    runner.restore(snapshot); plus, pf = runner.rollout([amplitude])
                    runner.restore(snapshot); minus, mf = runner.rollout([-amplitude])
                    assert not pf and not mf
                    np.testing.assert_array_equal(plus['action'][0], zero['action'][0])
                    np.testing.assert_array_equal(minus['action'][0], zero['action'][0])
                    from analyze_flash_state_learning import state
                    denom = plus['actual_u'][0]-minus['actual_u'][0]
                    b = (state(plus)[1]-state(minus)[1])/denom
                    np.testing.assert_array_equal(b[4:12], np.zeros(8))
                    direct.append(dict(mode=mode, start_rl_s=tick*.02, amplitude=amplitude,
                        sensor_B=b.tolist(), gt_B=((plus['gt'][1]-minus['gt'][1])/denom).tolist()))
        write(out/'results.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
            job=job, responses=responses, direct_B=direct, acquisition=acquisitions,
            anchor_sensor_p=float(prefix['sensor'][1000, 0]),
            exact_replays=replays, startup_violations=startup,
            frozen_bias_note='total torque frozen at pending F1 update of identical snapshot',
            feedback_bias=.5, sensors='current joint state, clone-refreshed IMU',
            leg_path='unchanged original ActionAdapter at every physics substep',
            history='previous full raw actor output', disabled_obstacles=runner.disabled_obstacles))
        return dict(id=job['id'], split=job['split'], accepted=sum(a['low_speed_gate'] for a in acquisitions),
            planned=len(acquisitions), responses=len(responses), direct_pairs=len(direct), zero_replays=len(replays))
    finally:
        runner.env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--pilot', action='store_true')
    parser.add_argument('--scan', action='store_true')
    parser.add_argument('--collect', action='store_true')
    parser.add_argument('--smoke', action='store_true')
    parser.add_argument('--workers', type=int, default=3)
    args = parser.parse_args()
    out = args.output.resolve()
    if not out.is_relative_to(REPO/'docs/exp') or out.exists():
        parser.error('New evidence directory under docs/exp required')
    out.mkdir(parents=True)
    config = prepared_config(CKPT)
    cfg = json.loads(config.read_text())
    protected = list((REPO/'sim2sim/sim2sim_ros2_jazzy').rglob('*.py'))
    protected += [REPO/'sim2sim/lqr'/f for f in ['runtime.py', 'model.py', 'estimator.py']]
    protected += [REPO/'test'/f for f in ['eval_flash_pv_models.py', 'eval_flash_state_learning.py', 'analyze_flash_state_learning.py']]
    protected += [config, config.parent/'policy.onnx', CKPT/'actor.pt']
    hashes = {str(p.relative_to(REPO)): sha256(p) for p in protected}
    jobs = []
    for split, seeds, times in [('train', range(120, 123), [22., 24.]), ('test', range(130, 132), [23., 25.])]:
        for seed in seeds:
            for pi, pitch in enumerate([-.035, 0., .035]):
                jobs.append(dict(id=f'{split}_s{seed}_p{pitch:+.3f}', split=split, seed=seed,
                    pitch=pitch, pitch_index=pi, times=times))
    if args.smoke:
        jobs = [dict(id='train_s118_p0', split='train', seed=118, pitch=0., pitch_index=1, times=[22., 24.])]
    write(out/'manifest.json', dict(execution_domain='VALIDATION_SIM', evidence_status='NOT_TESTED',
        checkpoint_sha256=sha256(CKPT/'actor.pt'), onnx_sha256=sha256(config.parent/'policy.onnx'),
        collector_sha256=sha256(Path(__file__)), stage='local' if args.collect else 'acquisition_pilot',
        protected_sha256=hashes, jobs=jobs if args.collect else [],
        unchanged_F1=dict(kp=2., kv=24., cap_total_Nm=2., ramp_s=1.5, slew_Nm_s=2.),
        command=[0., 0., 0.], sensors='synchronized clone IMU, encoder, raw previous action',
        acquisition='total +0.5Nm ramp at2Nm/s from RL start; F1 feedback added at20s without changing its gains',
        gate='sensor and GT sagittal velocity RMS over prior2s each<=0.002m/s; no post-startup failure',
        modes='frozen snapshot total bias + probe; constant0.5Nm + active F1 feedback + probe, fitted separately',
        probes='4s; sine/PRBS/pulse+/-/step+/- amplitudes0.1/0.25Nm; microPRBS0.02Nm, slew2Nm/s',
        model_plan='same M2/M4; matched-delta fits and absolute centered affine fits; train-only fits frozen before test',
        gate_prediction='same prior diagnostic30% median p/v free2s and rolling0.1/0.5/1/2s; direct Bv error<=30%',
        scope='identification only; no LQR, gain tuning, model state expansion, online adaptation or hardware'))
    if args.pilot:
        pilot(cfg, out)
    if args.scan:
        acquisition_scan(cfg, out)
    if args.collect:
        results = []
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(run_context, cfg, job, str(out)) for job in jobs]
            for f in as_completed(futures):
                result = f.result()
                results.append(result)
                print('[VALIDATION_SIM]', result, flush=True)
        write(out/'completion.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
            jobs=results, responses=sum(r['responses'] for r in results),
            direct_pairs=sum(r['direct_pairs'] for r in results), zero_replays=sum(r['zero_replays'] for r in results),
            acquired=sum(r['accepted'] for r in results), planned=sum(r['planned'] for r in results)))
    assert all(sha256(REPO/p) == value for p, value in hashes.items())
    write(out/'source_integrity.json', dict(execution_domain='DESKTOP_DRY_RUN', evidence_status='PASS',
        protected_files_preserved=True, collector_sha256=sha256(Path(__file__))))


if __name__ == '__main__':
    main()
