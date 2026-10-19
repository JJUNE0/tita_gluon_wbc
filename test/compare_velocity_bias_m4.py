"""VALIDATION_SIM: paired velocity-bias / frozen M4 / hybrid experiment only.

No runtime flags or production controllers are changed. Hybrid replaces the
fixed M4 torque bias with the existing wheel velocity bias, retaining the
frozen K/reference, correction saturation, slew and encoder/IMU state.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import multiprocessing
from pathlib import Path
import sys
import time
import traceback

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO / 'sim2sim/sim2sim_ros2_jazzy'), str(REPO / 'test')]
from velocity_bias_campaign import make_runner, write, digest
from sim2sim_ros2_jazzy.adapter import ObsState, quat_wxyz_to_rotmat
from sim2sim_ros2_jazzy.residual_wheel_lqr import ResidualWheelLQR, BIAS
from sim2sim_ros2_jazzy.velocity_bias import WheelVelocityBias

EXPORTS = REPO / 'docs/exp/2026-10-16/velocity_bias_overnight/exports'
CHECKPOINT = 'tita_flash_sac_115632_883848_model_60000'
CFG_PATH = EXPORTS / CHECKPOINT / 'config.json'
WHEELS, LEGS = [3, 7], [0, 1, 2, 4, 5, 6]
PHYSICS = dict(nominal={}, mass115={'mass': 1.15}, mass130={'mass': 1.3},
               com_plus={'com': .005}, com_minus={'com': -.005},
               friction02={'friction': .2}, friction08={'friction': .8})
MODES = ('baseline', 'm4', 'velocity', 'hybrid')


class M4WithoutFixedBias(ResidualWheelLQR):
    def _target(self, rotation):
        return super()._target(rotation) - BIAS


def source_hashes():
    paths = [Path(__file__), REPO / 'test/velocity_bias_campaign.py',
             REPO / 'test/flash_overnight_model_stages.py', REPO / 'test/static_target_domain.py']
    paths += list((REPO / 'sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy').glob('*.py'))
    return {str(p.relative_to(REPO)): digest(p) for p in paths}


class Comparison:
    def __init__(self, job):
        self.job = job
        self.runner = make_runner(json.loads(CFG_PATH.read_text()), job)
        self.env = self.runner.env
        self.dt = self.env.control_dt
        self.ticks = 0
        self.velocity = WheelVelocityBias(self.env) if job['mode'] in ('velocity', 'hybrid') else None
        self.m4 = None
        if job['mode'] == 'm4':
            self.m4 = ResidualWheelLQR(self.env)
        elif job['mode'] == 'hybrid':
            self.m4 = M4WithoutFixedBias(self.env)

    def step(self):
        r, env = self.runner, self.env
        p, o = r.playback, r.observation
        command = np.zeros(3, dtype=np.float32)
        acquired = self.ticks >= round(self.job['warmup'] / self.dt)
        if self.velocity:
            self.velocity.update(command)
        if self.m4:
            self.m4.update(command if acquired else None, p.last_action)
        history = p.last_action.copy()
        obs = p.builder.build(ObsState(env.joint_pos(), env.joint_vel(),
            o['quat'].astype(np.float32), o['gyro'].astype(np.float32), command, history,
            quat_wxyz_to_rotmat(o['quat']).T @ env.base_lin_vel()))
        action = p.policy.run(['nn_output'], {'nn_input0': obs.reshape(1, -1)})[0].reshape(8)
        motors = []
        baseline_motors = []

        def callback(q, dq):
            a = p.adapter
            baseline = a.compute(action, q, dq)
            torque = self.velocity.compute(a, action, q, dq) if self.velocity else baseline
            if self.m4 and acquired:
                expected = torque.copy()
                expected[WHEELS] = np.clip(expected[WHEELS] + self.m4.u * self.m4.signs / 2,
                                            -self.m4.limit, self.m4.limit)
                torque = self.m4.apply(torque)
                np.testing.assert_array_equal(torque, expected)
                if self.job['mode'] == 'hybrid':
                    assert abs(self.m4.u) <= .050000001, 'Fixed torque bias leaked into hybrid'
            if not acquired:
                np.testing.assert_array_equal(torque, baseline)
            np.testing.assert_array_equal(torque[LEGS], baseline[LEGS])
            assert np.isfinite(torque).all() and np.all(abs(torque) <= a.limit + 1e-6)
            motors.append(torque.copy())
            baseline_motors.append(baseline.copy())
            return torque

        env.step_with_torque_callback(callback)
        np.testing.assert_array_equal(history, p.last_action)
        p.last_action = action.copy()
        self.ticks += 1
        r.observation = r.observe()
        return dict(action=action, history=history, motor=np.asarray(motors),
                    baseline_motor=np.asarray(baseline_motors),
                    bias=self.velocity.u if self.velocity else 0.,
                    integral=self.velocity.law.integral if self.velocity else 0.,
                    m4_torque=self.m4.u if self.m4 else 0.,
                    m4_correction=self.m4.correction if self.m4 else 0.)


def trial(job, root):
    output = Path(root) / job['id']
    result_path = output / 'result.json'
    if result_path.exists():
        result = json.loads(result_path.read_text())
        assert result['job'] == job
        return result
    assert source_hashes() == job['source_hashes'], 'Mixed source versions'
    output.mkdir(parents=True, exist_ok=True)
    write(output / 'job.json', job)
    cfg = json.loads(CFG_PATH.read_text())
    result = dict(execution_domain='VALIDATION_SIM', evidence_status='FAIL', job=job,
                  checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
                  onnx_sha256=cfg['policy_interface']['onnx_sha256'])
    started, experiment = time.monotonic(), None
    try:
        assert digest(cfg['policy_interface']['checkpoint']) == result['checkpoint_sha256']
        experiment = Comparison(job)
        r, env = experiment.runner, experiment.env
        for tick in range(round(job['warmup'] / env.control_dt)):
            experiment.step()
            if tick >= 50 and r.failures():
                raise RuntimeError(f'Common baseline acquisition: {r.failures()}')
        result['initial_physics_sha256'] = hashlib.sha256(
            np.r_[env.data.qpos, env.data.qvel, r.playback.last_action].tobytes()).hexdigest()
        origin = r.observation['base_position'].copy()
        count, dt = round(job['duration'] / env.control_dt), env.control_dt
        states, inputs, actions, histories = [], [], [], []
        failure, peak_torque, saturation = [], 0., 0
        for tick in range(count + 1):
            o = r.observation
            states.append(np.r_[o['base_position'], o['base_velocity'], o['rpy'], o['sensor'][:2], o['fk_sensor']])
            failure = r.failures()
            if failure or tick == count:
                break
            step = experiment.step()
            inputs.append([step['bias'], step['integral'], step['m4_torque'], step['m4_correction']])
            actions.append(step['action'])
            histories.append(step['history'])
            peak_torque = max(peak_torque, float(abs(step['motor'][:, WHEELS]).max()))
            saturation += int(np.any(abs(step['motor'][:, WHEELS]) >= 11.999))
        states, inputs = np.asarray(states), np.asarray(inputs)
        distance = np.linalg.norm(states[:, :2] - origin[:2], axis=1)
        tail = np.arange(len(states)) * dt >= max(0., job['duration'] - 20.)
        complete = not failure and tick == count
        rms = lambda values: float(np.sqrt(np.mean(values ** 2))) if len(values) else None
        yaw = np.unwrap(states[:, 6]) - states[0, 6]
        stats = dict(complete=complete, failure=failure, duration_s=tick * dt,
            final_drift_m=float(distance[-1]), max_drift_m=float(distance.max()),
            radial_IAE_m_s=float(np.trapz(distance, dx=dt)),
            tail_speed_mean_m_s=float(states[tail, 3].mean()) if tail.any() else None,
            tail_speed_rms_m_s=rms(states[tail, 3]),
            tail_fk_error_rms_m_s=rms(states[tail, 10] - states[tail, 3]),
            peak_tilt_rad=float(abs(states[:, 4:6]).max()),
            peak_yaw_degrees=float(abs(np.rad2deg(yaw)).max()),
            peak_wheel_torque_nm=peak_torque, saturation_fraction=saturation / max(tick, 1),
            correction_limit_fraction=float(np.mean(abs(inputs[:, 3]) >= .049999)) if len(inputs) else 0.,
            final_velocity_bias_m_s=float(inputs[-1, 0]) if len(inputs) else 0.,
            final_m4_torque_nm=float(inputs[-1, 2]) if len(inputs) else 0.)
        result.update(**stats)
        gates = dict(complete=complete,
                     position=stats['max_drift_m'] <= (.25 if job['duration'] < 300 else .5),
                     mean_speed=tail.any() and abs(stats['tail_speed_mean_m_s']) <= .005,
                     speed_rms=tail.any() and stats['tail_speed_rms_m_s'] <= .02,
                     observation=tail.any() and stats['tail_fk_error_rms_m_s'] <= .05)
        result['gates'] = {k: bool(v) for k, v in gates.items()}
        result['evidence_status'] = 'PASS' if all(gates.values()) else 'SUSPICIOUS' if complete else 'FAIL'
        np.savez_compressed(output / 'trace.npz', state=states, input=inputs,
                            action=actions, history=histories, origin=origin)
        result['state_columns'] = ['base_x', 'base_y', 'base_z', 'base_forward_speed', 'roll', 'pitch',
                                   'yaw', 'raw_position', 'raw_speed', 'fk_position', 'fk_speed']
        result['input_columns'] = ['velocity_bias_m_s', 'velocity_integral_m_s',
                                   'm4_total_residual_nm', 'm4_correction_nm']
        if hasattr(env, 'assert_static'):
            env.assert_static()
    except Exception:
        result['evidence_status'] = 'FAIL'
        result['error'] = traceback.format_exc()
        (output / 'error.log').write_text(result['error'])
    finally:
        if experiment:
            experiment.env.close()
    result['elapsed_wall_s'] = time.monotonic() - started
    write(result_path, result)
    return result


def summarize(root, rows):
    groups = {}
    for r in rows:
        key = r['job']['condition'], r['job']['seed']
        groups.setdefault(key, {})[r['job']['mode']] = r
    comparisons = []
    for (condition, seed), modes in groups.items():
        hashes = {r.get('initial_physics_sha256') for r in modes.values()}
        pair = dict(condition=condition, seed=seed,
                    matched_initial_state=len(hashes) == 1 and None not in hashes,
                    modes={mode: {k: r.get(k) for k in ['evidence_status', 'max_drift_m', 'final_drift_m',
                        'radial_IAE_m_s', 'tail_speed_mean_m_s', 'tail_speed_rms_m_s',
                        'tail_fk_error_rms_m_s', 'peak_tilt_rad', 'peak_yaw_degrees',
                        'correction_limit_fraction', 'gates']} for mode, r in modes.items()})
        if 'velocity' in modes and 'hybrid' in modes and modes['velocity'].get('complete') and modes['hybrid'].get('complete'):
            pair['hybrid_vs_velocity_max_drift_change_percent'] = 100 * (
                modes['hybrid']['max_drift_m'] / max(modes['velocity']['max_drift_m'], 1e-12) - 1)
        comparisons.append(pair)
    write(root / 'comparison.json', comparisons)
    return comparisons


def plot(root, rows):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    conditions = list(dict.fromkeys(r['job']['condition'] for r in rows))
    seeds = sorted({r['job']['seed'] for r in rows})
    colors = dict(baseline='C0', m4='C1', velocity='C2', hybrid='C3')
    fig, axes = plt.subplots(len(conditions), 2, figsize=(13, 3.2 * len(conditions)), squeeze=False)
    for row in rows:
        if not (root / row['job']['id'] / 'trace.npz').exists():
            continue
        if row['job']['seed'] != seeds[0]:
            continue
        trace = np.load(root / row['job']['id'] / 'trace.npz')
        state, origin = trace['state'], trace['origin']
        t = np.arange(len(state)) * .02
        i = conditions.index(row['job']['condition'])
        distance = np.linalg.norm(state[:, :2] - origin[:2], axis=1)
        for j in range(2):
            mode = row['job']['mode']
            axes[i, j].plot(t, distance * 1000, color=colors[mode], label=mode)
            axes[i, j].grid(alpha=.25)
            axes[i, j].set_xlabel('Time (s)')
            axes[i, j].set_ylabel('Distance from hold origin (mm)')
        axes[i, 0].set_title(row['job']['condition'] + ' / all modes')
        axes[i, 1].set_title(row['job']['condition'] + ' / 0-100 mm detail')
        axes[i, 1].set_ylim(0, 100)
    axes[0, 0].legend()
    fig.suptitle(f'VALIDATION_SIM / model_60000 / seed {seeds[0]} / matched hold origin')
    fig.tight_layout(rect=(0., 0., 1., .96))
    fig.savefig(root / 'comparison.png', dpi=150)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--duration', type=float, default=300.)
    parser.add_argument('--seeds', type=int, nargs='+', default=[913])
    parser.add_argument('--conditions', nargs='+', choices=list(PHYSICS), default=list(PHYSICS))
    parser.add_argument('--modes', nargs='+', choices=MODES, default=list(MODES))
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    root = args.output.resolve()
    if not root.is_relative_to(REPO / 'docs/exp'):
        parser.error('Experiment artifacts must be inside docs/exp')
    if args.duration < 20:
        parser.error('At least 20 s required for terminal metrics')
    root.mkdir(parents=True, exist_ok=True)
    sources = source_hashes()
    jobs = [dict(id=f'{condition}_{mode}_s{seed}_{args.duration:g}s', mode=mode,
        condition=condition, physics=PHYSICS[condition], seed=seed, warmup=1.2,
        duration=args.duration, source_hashes=sources)
        for seed in args.seeds for condition in args.conditions for mode in args.modes]
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
                  'max_m=', row.get('max_drift_m'), 'tail_rms=', row.get('tail_speed_rms_m_s'), flush=True)
    summarize(root, rows)
    plot(root, rows)
    if any(r.get('error') for r in rows):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
