"""VALIDATION_SIM: activation delay measured from transform_up -> RL, without warmup exclusion."""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import multiprocessing
from pathlib import Path
import time
import traceback
from unittest.mock import patch

import numpy as np

import compare_velocity_bias_m4 as paired
from velocity_bias_campaign import write, digest
from sim2sim_ros2_jazzy.velocity_bias import WheelVelocityBias

REPO = paired.REPO
MAIN = paired.CHECKPOINT
EXTRA = ['tita_flash_sac_115632_883848_model_5000',
         'tita_flash_sac_115632_883848_model_25000',
         'tita_flash_sac_115632_883848_model_100000',
         'tita_flash_sac_193248_068255_model_60000']
DELAYS = [None, 0., .5, 1., 1.2, 2., 3.]
SOURCE_SHA256 = digest(__file__)


class TimedWheelVelocityBias(WheelVelocityBias):
    """Research-only acquisition threshold; same sensor path and bounds as production.

    The experiment sends zero command continuously from the first RL tick, so
    hold age and time since RL entry coincide. This does not change production
    reset/command semantics or claim that a timer measures posture stability.
    """

    def __init__(self, env, delay):
        if not np.isfinite(delay) or delay < 0:
            raise ValueError('Finite nonnegative acquisition delay required')
        self.delay = delay
        super().__init__(env)

    def _target(self, rotation):
        if self.age == 0.:
            self.law.reset()
            self.previous_offset = None
        offset = self.data.xpos[self.wheel_bodies].mean(0) - self.data.xpos[self.base_body]
        roll, pitch, yaw = rotation.as_euler('xyz')
        forward = np.array([np.cos(yaw), np.sin(yaw), 0.])
        if self.previous_offset is not None:
            self.velocity -= (offset - self.previous_offset) @ forward / self.env.control_dt
        self.previous_offset = offset.copy()
        self.eligible = (self.age + 1e-9 >= self.delay and max(abs(roll), abs(pitch)) <= .3
                         and abs(self.velocity) <= 1.)
        return self.law.update(float(self.velocity), self.env.control_dt, enabled=self.eligible)


def sources():
    paths = [Path(__file__), Path(paired.__file__), REPO / 'test/velocity_bias_campaign.py',
             REPO / 'test/static_target_domain.py', REPO / 'test/flash_overnight_model_stages.py']
    paths += list((REPO / 'sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy').glob('*.py'))
    return {str(p.relative_to(REPO)): digest(p) for p in paths}


def experiment(job):
    config = paired.EXPORTS / job['checkpoint_id'] / 'config.json'
    # Reuse the validated action/torque/history path with a checkpoint-specific config.
    with patch.object(paired, 'CFG_PATH', config):
        e = paired.Comparison(dict(job, mode='baseline', warmup=0.))
    if job['delay_s'] is not None:
        e.velocity = TimedWheelVelocityBias(e.env, job['delay_s'])
    return e


def trial(job, root):
    out = Path(root) / job['id']
    if (out / 'result.json').exists():
        result = json.loads((out / 'result.json').read_text())
        assert result['job'] == job
        return result
    assert sources() == job['source_hashes'], 'Mixed source versions'
    out.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((paired.EXPORTS / job['checkpoint_id'] / 'config.json').read_text())
    result = dict(execution_domain='VALIDATION_SIM', evidence_status='FAIL', job=job,
                  checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
                  onnx_sha256=cfg['policy_interface']['onnx_sha256'])
    write(out / 'job.json', job)
    started, e = time.monotonic(), None
    try:
        assert digest(cfg['policy_interface']['checkpoint']) == result['checkpoint_sha256']
        assert digest(cfg['policy']['path']) == result['onnx_sha256']
        assert all(o['kind'] != 'lin_vel' for o in cfg['policy_interface']['observations'])
        e = experiment(job)
        r, env, dt = e.runner, e.env, e.dt
        initial = np.r_[env.data.qpos, env.data.qvel, r.playback.last_action]
        result.update(initial_physics_sha256=hashlib.sha256(initial.tobytes()).hexdigest(),
                      initial_strict_guard_reasons=r.failures(), rl_entry_sim_time_s=float(env.data.time))
        states, inputs = [], []
        first_eligible = first_nonzero = first_seed_velocity = None
        guard_prefix, failure = [], []
        peak_torque, saturated = 0., 0
        count = round(job['duration'] / dt)
        for tick in range(count + 1):
            o = r.observation
            states.append(np.r_[o['base_position'], o['base_velocity'], o['rpy'], o['sensor'][:2],
                                o['fk_sensor'], env.data.qpos[2]])
            now = tick * dt
            strict = r.failures()
            finite = np.isfinite(np.r_[env.data.qpos, env.data.qvel]).all()
            if not finite or max(abs(o['rpy'][:2])) > .9 or env.data.qpos[2] < .025:
                failure = ['always_on_finite_tilt_height_guard']
            elif now + 1e-9 >= 2.:
                failure = strict
            elif strict:
                guard_prefix.append(dict(rl_s=now, reasons=strict))
            if failure or tick == count:
                break
            step = e.step()
            if e.velocity:
                if e.velocity.eligible and first_eligible is None:
                    first_eligible = now
                    first_seed_velocity = float(e.velocity.velocity)
                if abs(e.velocity.u) > 1e-10 and first_nonzero is None:
                    first_nonzero = now
                if now + 1e-9 < job['delay_s']:
                    assert e.velocity.u == 0. and not e.velocity.law.seeded
                assert abs(e.velocity.u) <= 2.00000001
                inputs.append([e.velocity.u, e.velocity.velocity, e.velocity.law.integral,
                               float(e.velocity.eligible)])
            else:
                inputs.append([0., o['fk_sensor'][1], 0., 0.])
            peak_torque = max(peak_torque, float(abs(step['motor'][:, paired.WHEELS]).max()))
            saturated += int(np.any(abs(step['motor'][:, paired.WHEELS]) >= 11.999))
        states, inputs = np.asarray(states), np.asarray(inputs)
        t = np.arange(len(states)) * dt
        distance = np.linalg.norm(states[:, :2] - states[0, :2], axis=1)
        after2 = t + 1e-9 >= 2.
        tail = t + 1e-9 >= max(2., job['duration'] - 20.)
        rms = lambda v: float(np.sqrt(np.mean(v ** 2))) if len(v) else None
        complete = not failure and tick == count
        violations = np.flatnonzero((abs(states[:, 3]) > .005) | (t < 2.))
        settle_index = int(violations[-1] + 1) if len(violations) else 0
        settle = float(t[settle_index]) if len(t) - settle_index >= round(1. / dt) else None
        at2 = min(round(2. / dt), len(states) - 1)
        stats = dict(complete=complete, failure=failure, duration_s=tick * dt,
            first_eligible_rl_s=first_eligible, first_nonzero_bias_rl_s=first_nonzero,
            first_seed_velocity_m_s=first_seed_velocity,
            max_drift_from_rl_m=float(distance.max()), final_drift_from_rl_m=float(distance[-1]),
            radial_IAE_from_rl_m_s=float(np.trapz(distance, dx=dt)),
            drift_at_2s_m=float(distance[at2]) if after2.any() else None,
            max_drift_from_2s_m=float(np.linalg.norm(states[after2, :2] - states[at2, :2], axis=1).max()) if after2.any() else None,
            radial_IAE_after2_from_rl_m_s=float(np.trapz(distance[after2], dx=dt)),
            max_tilt_first2_rad=float(abs(states[t <= 2., 4:6]).max()),
            max_tilt_after2_rad=float(abs(states[after2, 4:6]).max()) if after2.any() else None,
            tail_speed_mean_m_s=float(states[tail, 3].mean()) if tail.any() else None,
            tail_speed_rms_m_s=rms(states[tail, 3]),
            tail_fk_error_rms_m_s=rms(states[tail, 10] - states[tail, 3]),
            observed_speed_settled_rl_s=settle,
            peak_yaw_degrees=float(abs(np.rad2deg(np.unwrap(states[:, 6]) - states[0, 6])).max()),
            peak_wheel_torque_nm=peak_torque, saturation_fraction=saturated / max(tick, 1))
        result.update(stats)
        gates = dict(complete=complete,
            position=stats['max_drift_from_rl_m'] <= (.25 if job['duration'] < 300 else .5),
            mean_speed=tail.any() and abs(stats['tail_speed_mean_m_s']) <= .005,
            speed_rms=tail.any() and stats['tail_speed_rms_m_s'] <= .02,
            observation=tail.any() and stats['tail_fk_error_rms_m_s'] <= .05)
        result['gates'] = {k: bool(v) for k, v in gates.items()}
        result['evidence_status'] = 'PASS' if all(gates.values()) else 'SUSPICIOUS' if complete else 'FAIL'
        np.savez_compressed(out / 'trace.npz', state=states, input=inputs)
        result['state_columns'] = ['base_x', 'base_y', 'base_z', 'base_forward_speed', 'roll', 'pitch',
                                  'yaw', 'raw_position', 'raw_speed', 'fk_position', 'fk_speed', 'root_height']
        result['input_columns'] = ['velocity_bias_m_s', 'estimated_velocity_m_s', 'integral_m_s', 'eligible']
        write(out / 'startup_strict_guard_events.json', guard_prefix)
        if hasattr(env, 'assert_static'):
            env.assert_static()
    except Exception:
        result.update(evidence_status='FAIL', error=traceback.format_exc())
        (out / 'error.log').write_text(result['error'])
    finally:
        if e:
            e.env.close()
    result['elapsed_wall_s'] = time.monotonic() - started
    write(out / 'result.json', result)
    return result


def summarize(root, rows):
    groups = {}
    for r in rows:
        key = r['job']['checkpoint_id'], r['job']['condition'], r['job']['seed']
        groups.setdefault(key, []).append(r)
    matched = all(len({r.get('initial_physics_sha256') for r in g}) == 1 and
                  all('initial_physics_sha256' in r for r in g) for g in groups.values())
    summaries = []
    for delay in sorted({r['job']['delay_s'] for r in rows}, key=lambda d: -1 if d is None else d):
        subset = [r for r in rows if r['job']['delay_s'] == delay]
        completed = [r for r in subset if r.get('complete')]
        summaries.append(dict(delay_s=delay, count=len(subset), completed=len(completed),
            quality_pass=sum(r['evidence_status'] == 'PASS' for r in subset),
            max_drift_median_m=float(np.median([r['max_drift_from_rl_m'] for r in completed])) if completed else None,
            max_drift_worst_m=max((r['max_drift_from_rl_m'] for r in completed), default=None),
            radial_IAE_median_m_s=float(np.median([r['radial_IAE_from_rl_m_s'] for r in completed])) if completed else None))
    write(root / 'aggregate.json', dict(execution_domain='VALIDATION_SIM', all_initial_states_matched=matched,
                                        cohorts=len(groups), delays=summaries))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--stage', choices=['screen', 'long', 'finalists'], required=True)
    p.add_argument('--workers', type=int, default=8)
    args = p.parse_args()
    root = args.output.resolve()
    if not root.is_relative_to(REPO / 'docs/exp'):
        p.error('docs/exp output required')
    duration = 60. if args.stage == 'screen' else 300.
    if args.stage == 'screen':
        delays = DELAYS
    elif args.stage == 'long':
        delays = [0., 1.2, 2., 3.]
    else:
        delays = [.5, 1.]
    seeds = [913, 914, 915] if args.stage == 'screen' else [913]
    cohorts = [(MAIN, condition, seed) for condition in paired.PHYSICS for seed in seeds]
    if args.stage in ('screen', 'finalists'):
        cohorts += [(checkpoint, 'nominal', 913) for checkpoint in EXTRA]
    hashes = sources()
    jobs = []
    for checkpoint, condition, seed in cohorts:
        for delay in delays:
            label = 'baseline' if delay is None else f'delay{delay:g}'
            jobs.append(dict(id=f'{checkpoint}_{condition}_s{seed}_{label}_{duration:g}s',
                checkpoint_id=checkpoint, condition=condition, physics=paired.PHYSICS[condition],
                seed=seed, delay_s=delay, duration=duration, source_hashes=hashes))
    write(root / 'jobs.json', jobs)
    (root / 'harness_source.py.txt').write_text(Path(__file__).read_text())
    rows = []
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context('spawn')) as pool:
        futures = [pool.submit(trial, job, str(root)) for job in jobs]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            write(root / 'results.json', rows)
            print('[VALIDATION_SIM]', len(rows), '/', len(jobs), row['job']['id'], row['evidence_status'],
                  'max_m=', row.get('max_drift_from_rl_m'), 'active_s=', row.get('first_eligible_rl_s'), flush=True)
    summarize(root, rows)
    if any(r.get('error') for r in rows):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
