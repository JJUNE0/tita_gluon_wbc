"""VALIDATION_SIM / DESKTOP_DRY_RUN: resumable, per-trial signed velocity-bias research."""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import multiprocessing
from pathlib import Path
import sys
import time
import traceback

REPO = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
sys.path[:0] = [str(REPO / 'sim2sim/sim2sim_ros2_jazzy'), str(REPO)]
PYTHON = Path('/home/cocel/venvs/cosim_ros2_jazzy/bin/python')


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    temporary.replace(path)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def export_all(root):
    from unittest.mock import patch
    from sim2sim_ros2_jazzy.checkpoint import prepare_checkpoint
    rows = []
    for item in json.loads((root / 'checkpoint_manifest.json').read_text()):
        output = root / 'exports' / item['id']
        try:
            assert digest(item['checkpoint']) == item['sha256']
            if (output / 'manifest.json').exists():
                info = json.loads((output / 'manifest.json').read_text())
                assert info['checkpoint_sha256'] == item['sha256']
                assert info['config_sha256'] == digest(output / 'config.json')
                assert info['onnx_sha256'] == digest(output / 'policy.onnx')
            else:
                with patch('sim2sim_ros2_jazzy.checkpoint.export_directory', lambda path: output):
                    prepare_checkpoint(item['checkpoint'], PYTHON)
                info = json.loads((output / 'manifest.json').read_text())
            rows.append(dict(**item, evidence_status='PASS', config=str(output / 'config.json'),
                             onnx_sha256=info['onnx_sha256'], parity=info['parity']))
        except Exception:
            rows.append(dict(**item, evidence_status='FAIL', error=traceback.format_exc()))
        write(root / 'export_results.json', rows)
        print('[VALIDATION_SIM] export', item['id'], rows[-1]['evidence_status'], flush=True)


class VelocityLaw:
    """Candidate controller; all gains and limits are recorded per experiment."""

    def __init__(self, parameters):
        self.p = parameters
        self.filtered = self.integral = self.bias = 0.
        self.gain_filtered = None
        self.seeded = False

    def step(self, velocity, dt, age):
        import math
        import numpy as np
        p = self.p
        self.filtered += (1. - math.exp(-dt / max(p.get('tau', .2), dt))) * (velocity - self.filtered)
        sign = p.get('sign', 1.)
        limit = p.get('limit', .5)
        if p.get('mode') == 'constant':
            desired = p.get('bias', 0.)
        else:
            if not self.seeded:
                self.integral = float(np.clip(sign * p.get('seed_gain', 0.) * velocity, -limit, limit))
                self.seeded = True
            gain = 1.
            if p.get('gain_velocity', 0.) > 0.:
                signal = self.filtered
                if p.get('gain_tau', 0.) > 0.:
                    if self.gain_filtered is None:
                        self.gain_filtered = velocity
                    else:
                        self.gain_filtered += (1. - math.exp(-dt / p['gain_tau'])) * (velocity - self.gain_filtered)
                    signal = self.gain_filtered
                gain = float(np.clip((abs(signal) / p['gain_velocity']) ** p.get('gain_power', 1.),
                                     p.get('gain_floor', .1), 1.))
            change = sign * gain * p.get('ki', 0.) * self.filtered * dt
            proposed = float(np.clip(self.integral + change, -limit, limit))
            feedback = sign * gain * p.get('kp', 0.) * self.filtered - p.get('kp_fast', 0.) * (velocity - self.filtered)
            desired = proposed + feedback
            if abs(desired) <= limit or desired * change < 0:
                self.integral = proposed
            desired = self.integral + feedback
        phase = min(age / p.get('ramp', 1.5), 1.)
        desired = phase * phase * (3. - 2. * phase) * float(np.clip(desired, -limit, limit))
        slew = p.get('slew', .2) * dt
        self.bias = float(np.clip(desired, self.bias - slew, self.bias + slew))
        return self.bias

    def disable(self, dt):
        import numpy as np
        self.filtered = self.integral = 0.
        self.gain_filtered = None
        self.seeded = False
        delta = self.p.get('slew', .2) * dt
        self.bias = float(np.clip(0., self.bias - delta, self.bias + delta))
        return self.bias


def make_runner(cfg, job):
    import numpy as np
    from flash_overnight_model_stages import Runner
    from sim2sim_ros2_jazzy.adapter import ObsState, quat_wxyz_to_rotmat
    from unittest.mock import patch
    from static_target_domain import StaticEnv

    unknown = set(job.get('physics', {})) - {'mass', 'com', 'friction', 'gain', 'lag'}
    if unknown:
        raise ValueError(f'Unknown static physics keys: {sorted(unknown)}')

    class TrialRunner(Runner):
        def __init__(self):
            self.previous_offset = None
            self.previous_observation_time = None
            self.last_fk_correction = 0.
            self.fk_position = 0.
            target = job.get('physics', {})
            if target:
                with patch('sim2sim.lqr.runtime.TitaMujocoEnv', lambda config: StaticEnv(config, target)):
                    super().__init__(cfg, dict(seed=job.get('seed', 270), pitch=job.get('pitch', 0.)))
                self.env.record_startup = False
            else:
                super().__init__(cfg, dict(seed=job.get('seed', 270), pitch=job.get('pitch', 0.)))
            self.velocity_hold = None
            self.fixed_m4 = None
            self.policy_ticks = 0
            if job.get('runtime'):
                from sim2sim_ros2_jazzy.velocity_bias import VelocityBias, WheelVelocityBias
                self.velocity_hold = WheelVelocityBias(self.env)
                parameters = dict(job['law'])
                parameters['response_sign'] = parameters.pop('sign', 1.)
                self.velocity_hold.law = VelocityBias(**parameters)
            if job.get('controller') == 'm4':
                from sim2sim_ros2_jazzy.residual_wheel_lqr import ResidualWheelLQR
                self.fixed_m4 = ResidualWheelLQR(self.env)

        def observe(self):
            o = super().observe()
            # Translation cancels: sensor-driven FK offsets, never root velocity.
            offset = self.sensors.xpos[self.wheel_bodies].mean(0) - o['base_position']
            yaw = o['rpy'][2]
            forward = np.array([np.cos(yaw), np.sin(yaw), 0.])
            stamp = float(self.env.data.time)
            # A root-velocity impulse refreshes GT at the same physics timestamp.
            # Preserve the measured FK derivative; zero elapsed time is not a new sample.
            if stamp != self.previous_observation_time:
                self.last_fk_correction = 0.
                if self.previous_offset is not None:
                    last_offset, last_raw = self.previous_offset
                    delta = (offset - last_offset) @ forward
                    self.last_fk_correction = delta / self.env.control_dt
                    self.fk_position += o['sensor'][0] - last_raw - delta
                self.previous_offset = offset.copy(), float(o['sensor'][0])
                self.previous_observation_time = stamp
            correction = self.last_fk_correction
            o['fk_sensor'] = np.array([self.fk_position, o['sensor'][1] - correction])
            if job.get('estimator') == 'analytic':
                from velocity_bias_analytic_observer import base_forward_speed
                joints = np.array([self.env.model.joint(name).id for name in self.env.joint_names])
                from scipy.spatial.transform import Rotation
                rotation = Rotation.from_quat(o['quat'][[1, 2, 3, 0]])
                o['fk_sensor'][1] = base_forward_speed(self.sensors, joints, self.wheel_bodies,
                    self.env.model.body('base_link').id, rotation, self.env.joint_vel(), o['gyro'], o['sensor'][1])
            return o

        def step_bias(self, bias, command=None):
            env, playback, o = self.env, self.playback, self.observation
            command = np.zeros(3, dtype=np.float32) if command is None else command
            if self.velocity_hold:
                self.velocity_hold.update(command)
                bias = self.velocity_hold.u
            if self.fixed_m4:
                acquired = self.policy_ticks >= round(job.get('warmup', 8.) / env.control_dt)
                self.fixed_m4.update(command if acquired else None, playback.last_action)
            history = playback.last_action.copy()
            obs = playback.builder.build(ObsState(env.joint_pos(), env.joint_vel(), o['quat'].astype(np.float32),
                o['gyro'].astype(np.float32), command, history,
                quat_wxyz_to_rotmat(o['quat']).T @ env.base_lin_vel()))
            action = playback.policy.run(['nn_output'], {'nn_input0': obs.reshape(1, -1)})[0].reshape(8)
            targets = playback.adapter.targets(action)
            targets[[3, 7]] += o['signs'] * bias / self.description.radius
            torques, originals = [], []

            def callback(q, dq):
                a = playback.adapter
                baseline = a.compute(action, q, dq)
                error = np.where(a.velocity, 0., targets - q)
                desired = np.where(a.velocity, targets, 0.)
                torque = np.clip(a.kp * error + a.kd * (desired - dq), -a.limit, a.limit)
                if self.velocity_hold:
                    native = self.velocity_hold.compute(a, action, q, dq)
                    np.testing.assert_array_equal(native, torque)
                if self.fixed_m4 and acquired:
                    torque = self.fixed_m4.apply(baseline)
                assert np.array_equal(torque[[0, 1, 2, 4, 5, 6]], baseline[[0, 1, 2, 4, 5, 6]])
                assert np.isfinite(torque).all() and np.all(abs(torque) <= a.limit + 1e-6)
                torques.append(torque.copy())
                originals.append(baseline.copy())
                return torque

            env.step_with_torque_callback(callback)
            playback.last_action = action.copy()
            self.policy_ticks += 1
            self.observation = self.observe()
            result = dict(action=action, history=history, motor=np.asarray(torques), baseline_motor=np.asarray(originals))
            if self.velocity_hold:
                result['controller'] = [bias, self.velocity_hold.law.filtered, self.velocity_hold.law.integral]
            if self.fixed_m4:
                from sim2sim_ros2_jazzy.residual_wheel_lqr import BIAS
                result['controller'] = [self.fixed_m4.u, self.fixed_m4.correction, BIAS]
            return result

    return TrialRunner()


def trial(root_string, stage, job):
    import numpy as np
    root = Path(root_string)
    assert job['harness_source_sha256'] == SOURCE_SHA256, 'Worker source changed after job submission'
    if job.get('runtime'):
        assert digest(REPO / 'sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/velocity_bias.py') == job['controller_source_sha256']
    output = root / stage / job['id']
    result_path = output / 'result.json'
    if result_path.exists():
        old = json.loads(result_path.read_text())
        assert old['job'] == job
        return old
    output.mkdir(parents=True, exist_ok=True)
    write(output / 'job.json', job)
    runner = None
    started = time.monotonic()
    result = dict(execution_domain='VALIDATION_SIM', evidence_status='FAIL', job=job)
    try:
        cfg = json.loads((root / 'exports' / job['checkpoint_id'] / 'config.json').read_text())
        result.update(checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
                      onnx_sha256=cfg['policy_interface']['onnx_sha256'],
                      input_columns=(['total_residual_nm', 'lqr_correction_nm', 'fixed_bias_nm']
                                     if job.get('controller') == 'm4' else
                                     ['velocity_bias_m_s', 'filtered_velocity_m_s', 'integral_m_s']),
                      state_columns=['base_x', 'base_y', 'base_z', 'base_forward_speed', 'roll',
                                     'pitch', 'yaw', 'raw_position', 'raw_speed', 'fk_position', 'fk_speed'])
        runner = make_runner(cfg, job)
        for tick in range(round(job.get('warmup', 8.) / runner.env.control_dt)):
            runner.step_bias(0.)
            if tick >= 50 and runner.failures():
                raise RuntimeError(f'baseline warmup: {runner.failures()}')
        if job.get('kick', 0.):
            yaw = runner.observation['rpy'][2]
            runner.env.data.qvel[:3] += job['kick'] * np.array([np.cos(yaw), np.sin(yaw), 0.])
            runner.env.mujoco.mj_forward(runner.env.model, runner.env.data)
            runner.observation = runner.observe()
        origin = runner.observation['base_position'].copy()
        result['initial_physics_sha256'] = hashlib.sha256(
            np.r_[runner.env.data.qpos, runner.env.data.qvel, runner.playback.last_action].tobytes()).hexdigest()
        law = VelocityLaw(job.get('law', {'mode': 'constant', 'bias': 0.}))
        duration = job.get('duration', 60.)
        dt = runner.env.control_dt
        count = round(duration / dt)
        states, inputs, actions, histories = [], [], [], []
        failure = []
        peak_torque = saturation = 0.
        eligible_age = 0.
        for tick in range(count + 1):
            o = runner.observation
            states.append(np.r_[o['base_position'], o['base_velocity'], o['rpy'], o['sensor'][:2], o['fk_sensor']])
            failure = runner.failures()
            if failure or tick == count:
                break
            measured = o['fk_sensor'][1] if job.get('estimator') in ('fk', 'analytic') else o['sensor'][1]
            if job.get('guarded'):
                eligible = max(abs(o['rpy'][:2])) <= .3 and abs(measured) <= 1.
                if eligible:
                    bias = law.step(float(measured), dt, eligible_age)
                    eligible_age += dt
                else:
                    bias = law.disable(dt)
                    eligible_age = 0.
            else:
                bias = law.step(float(measured), dt, tick * dt)
            previous = runner.playback.last_action.copy()
            step = runner.step_bias(bias)
            assert np.array_equal(previous, step['history'])
            peak_torque = max(peak_torque, float(abs(step['motor'][:, [3, 7]]).max()))
            saturation += float(np.any(abs(step['motor'][:, [3, 7]]) >= 11.999))
            inputs.append(step.get('controller', [bias, law.filtered, law.integral]))
            actions.append(step['action'])
            histories.append(step['history'])
        states = np.asarray(states)
        delta = states[:, :2] - origin[:2]
        distance = np.linalg.norm(delta, axis=1)
        tail = np.arange(len(states)) * dt >= max(0., duration - 20.)
        speed = states[:, 3]
        complete = not failure and tick == count
        stats = dict(complete=complete, failure=failure, duration_s=tick * dt,
            final_drift_m=float(distance[-1]), max_drift_m=float(distance.max()),
            radial_IAE_m_s=float(np.trapz(distance, dx=dt)),
            signed_longitudinal_delta_m=float((states[-1, :3]-origin) @
                                             [np.cos(states[0, 6]), np.sin(states[0, 6]), 0.]),
            tail_speed_mean_m_s=float(speed[tail].mean()) if tail.any() else None,
            tail_speed_rms_m_s=float(np.sqrt(np.mean(speed[tail]**2))) if tail.any() else None,
            tail_sensor_speed_mean_m_s=float(states[tail, 8].mean()) if tail.any() else None,
            tail_fk_speed_mean_m_s=float(states[tail, 10].mean()) if tail.any() else None,
            peak_tilt_rad=float(abs(states[:, 4:6]).max()),
            peak_wheel_torque_nm=peak_torque, saturation_fraction=saturation / max(tick, 1),
            final_velocity_bias_m_s=float(law.bias), final_integral_m_s=float(law.integral))
        np.savez_compressed(output / 'trace.npz', state=states, input=inputs,
                            action=actions, history=histories, origin=origin)
        result.update(evidence_status='PASS' if complete else 'FAIL', **stats)
        if hasattr(runner.env, 'assert_static'):
            runner.env.assert_static()
    except Exception:
        result['error'] = traceback.format_exc()
        (output / 'error.log').write_text(result['error'])
    finally:
        if runner is not None:
            runner.env.close()
    result['elapsed_wall_s'] = time.monotonic() - started
    write(result_path, result)
    (output / 'summary.md').write_text(
        f'# {job["id"]}\n\nExecution Domain: VALIDATION_SIM\n\n'
        f'Policy Checkpoint SHA256: {result.get("checkpoint_sha256", "NOT_TESTED")}\n\n'
        f'Evidence Status: {result["evidence_status"]}\n\n'
        f'Observed metrics / behavior / log summary:\n\n```json\n{json.dumps(result, indent=2)}\n```\n')
    return result


def run_jobs(root, stage, jobs, workers):
    jobs = [dict(job, harness_source_sha256=SOURCE_SHA256) for job in jobs]
    for job in jobs:
        if job.get('runtime'):
            job['controller_source_sha256'] = digest(
                REPO / 'sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/velocity_bias.py')
    write(root / f'{stage}_jobs.json', jobs)
    rows = []
    with ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context('spawn')) as pool:
        futures = [pool.submit(trial, str(root), stage, job) for job in jobs]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            write(root / f'{stage}_results.json', rows)
            print('[VALIDATION_SIM]', stage, len(rows), '/', len(jobs), row['job']['id'],
                  row['evidence_status'], row.get('final_drift_m'), row.get('tail_speed_mean_m_s'), flush=True)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--stage', choices=['export', 'survey', 'jobs'], required=True)
    parser.add_argument('--jobs', type=Path)
    parser.add_argument('--name', default='trials')
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_relative_to(REPO / 'docs/exp'):
        parser.error('docs/exp output required')
    if args.stage == 'export':
        export_all(root)
    elif args.stage == 'survey':
        items = [i for i in json.loads((root / 'export_results.json').read_text()) if i['evidence_status'] == 'PASS']
        jobs = [dict(id=i['id'], checkpoint_id=i['id'], duration=60., warmup=8., seed=270,
                     law=dict(mode='constant', bias=0.)) for i in items]
        run_jobs(root, 'survey', jobs, args.workers)
    else:
        jobs = json.loads(args.jobs.read_text())
        run_jobs(root, args.name, jobs, args.workers)


if __name__ == '__main__':
    main()
