"""VALIDATION_SIM: bounded stop residual kv/ramp ablation; frozen FlashSAC."""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from play_flash_velocity_hold_limit2 import (
    REPO, ARCHIVE, Plant, StopHold, Sensors, Description, policy_config,
    read_yaml, write_json, sha256, LEGS, WHEELS, infer_synchronized, additive_torque,
)
from eval_stop_residual_limits import command_at as history_command

CONTEXT = None


class TunedStopHold(StopHold):
    def __init__(self, description, equilibrium_pitch, kv=.5, ramp_s=1.):
        super().__init__(description, equilibrium_pitch)
        if kv < 0 or ramp_s < 0 or not np.isfinite([kv, ramp_s]).all():
            raise ValueError('Finite nonnegative kv/ramp required')
        self.kv, self.ramp_s = kv, ramp_s

    def step(self, command, sensors, dt):
        previous, age = self.u, self.age
        _, diagnostic = super().step(command, sensors, dt)
        if diagnostic['event'] == 'hold_enter':
            age = 0.
        if self.holding:
            phase = 1. if self.ramp_s == 0 else min(age / self.ramp_s, 1.)
            activation = phase * phase * (3. - 2. * phase)
            raw = -2. * self.state[0] - self.kv * self.state[1]
            target = activation * np.clip(raw, -2., 2.)
        else:
            activation, raw, target = 0., 0., 0.
        self.u = float(np.clip(target, previous - 2. * dt, previous + 2. * dt))
        diagnostic.update(activation=activation, raw_total_nm=float(raw),
            mode='HOLD' if self.holding else ('RELEASE' if abs(self.u) > 1e-9 else 'MOVE'))
        return self.u, diagnostic


def command_at(t, scenario):
    if scenario == 'history':
        return history_command(t)
    value = {'forward': [.2, 0., 0.], 'backward': [-.2, 0., 0.],
             'turn': [-.1, 0., .15]}[scenario]
    return np.asarray(value if 2 <= t < 7 else [0., 0., 0.], dtype=np.float32)


def initialize(context):
    global CONTEXT
    CONTEXT = context


def metrics(trace, job, failure):
    stop = 62.26 if job['scenario'] == 'history' else 7.
    ids = np.flatnonzero(trace['time'] >= stop)
    if len(ids) < 2:
        return dict(score=None)
    start = ids[0]
    position = trace['position'][ids] - trace['position'][start]
    planar = np.linalg.norm(position[:, :2], axis=1)
    path = trace['gt'][ids, 0] - trace['gt'][start, 0]
    forward = np.array([np.cos(trace['rpy'][start, 2]), np.sin(trace['rpy'][start, 2])])
    signed_direction = 1 if job['scenario'] == 'forward' else -1
    reverse = max(0., float(np.max(-signed_direction * (position[:, :2] @ forward))))
    tail = trace['time'] >= job['duration_s'] - 10.
    tail_speed = float(np.sqrt(np.mean(trace['gt'][tail, 1] ** 2))) if tail.any() else None
    wheel = trace['motor_substeps'][1:, :, WHEELS]
    # Fixed before screening: distance, peak error, reverse excursion, tail speed.
    score = float(planar.mean() + .5 * planar.max() + .5 * reverse + 5. * tail_speed) if tail_speed is not None and not failure else None
    return dict(score=score, stop_planar_mae_m=float(planar.mean()),
        stop_planar_max_m=float(planar.max()), stop_planar_final_m=float(planar[-1]),
        stop_path_final_m=float(path[-1]), reverse_excursion_m=reverse,
        tail_v_rms_m_s=tail_speed, tail_v_mean_m_s=float(trace['gt'][tail, 1].mean()) if tail.any() else None,
        pitch_error_rms_rad=float(np.sqrt(np.mean(trace['gt'][ids, 2] ** 2))),
        pitch_rate_rms_rad_s=float(np.sqrt(np.mean(trace['gt'][ids, 3] ** 2))),
        wheel_torque_rms_nm=float(np.sqrt(np.mean(wheel ** 2))),
        wheel_torque_peak_nm=float(abs(wheel).max()),
        residual_peak_nm=float(abs(trace['residual']).max()),
        saturation_fraction=float(np.mean(abs(trace['residual'][ids]) >= 2. - 1e-9)))


def run(job):
    context = CONTEXT
    policy, cfg, parameters = context['policy'], context['cfg'], context['parameters']
    description = Description(context['asset_path'])
    plant = Plant(policy, cfg, description, parameters, {'name': 'nominal'}, job['seed'], job['pitch'])
    env, playback = plant.env, plant.playback
    hold = TunedStopHold(description, parameters['equilibrium_pitch'], job['kv'], job['ramp_s'])
    initial = np.r_[env.data.qpos, env.data.qvel]
    initial_hash = hashlib.sha256(initial.tobytes()).hexdigest()
    rows, failure = [], []
    leg_error = wheel_error = 0.
    motor = np.zeros((env.decimation, 8))
    try:
        for tick in range(round(job['duration_s'] / .02) + 1):
            t = tick * .02
            observation = plant.observe()
            failure, _ = plant.failures(observation, 'synchronized')
            data = plant.truth_data
            packet = Sensors(env.joint_pos(), env.joint_vel(),
                data.sensor('trunk_quat').data.copy(), data.sensor('trunk_gyro').data.copy())
            command = command_at(t, job['scenario'])
            u, diagnostic = hold.step(command, packet, .02)
            rows.append(dict(time=t, gt=observation['gt'].copy(), rpy=observation['rpy'].copy(),
                position=observation['position'].copy(), residual=u, command=command.copy(),
                relative_p=np.nan if diagnostic['relative_p'] is None else diagnostic['relative_p'],
                estimated_v=np.nan if diagnostic['estimated_v'] is None else diagnostic['estimated_v'],
                motor_substeps=motor.copy()))
            if failure or tick == round(job['duration_s'] / .02):
                break
            _, action = infer_synchronized(playback, env, packet, command)

            def override(q, dq, torque):
                nonlocal leg_error, wheel_error
                result = additive_torque(torque, u, plant.signs)
                leg_error = max(leg_error, float(abs(result[LEGS] - torque[LEGS]).max()))
                expected = np.clip(torque[WHEELS] + plant.signs * u / 2.,
                    -playback.adapter.limit[WHEELS], playback.adapter.limit[WHEELS])
                wheel_error = max(wheel_error, float(abs(result[WHEELS] - expected).max()))
                return result

            _, motor = playback.step(action, override)
            np.testing.assert_array_equal(playback.last_action, action)
        trace = {k: np.asarray([r[k] for r in rows]) for k in rows[0]}
        assert abs(trace['residual']).max() <= 2. + 1e-12
        assert abs(np.diff(trace['residual'])).max() <= .04 + 1e-12
        assert leg_error == 0. and wheel_error < 1e-6
        path = Path(context['output']) / (job['id'] + '.npz')
        np.savez_compressed(path, **trace)
        return dict(execution_domain='VALIDATION_SIM', evidence_status='FAIL' if failure else 'PASS',
            **job, failure=failure, completed_s=float(trace['time'][-1]), initial_hash=initial_hash,
            leg_error_nm=leg_error, wheel_error_nm=wheel_error, trace=path.name,
            metrics=metrics(trace, job, failure))
    finally:
        env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--design', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=3)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(REPO / 'docs/exp') or output.exists():
        parser.error('New docs/exp evidence output required')
    design = json.loads(args.design.read_text())
    output.mkdir(parents=True)
    policy = policy_config()
    cfg = json.loads((ARCHIVE / 'config.json').read_text())
    parameters = json.loads((ARCHIVE / 'manifest.json').read_text())['nominal_parameters']
    source = read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    context = dict(policy=policy, cfg=cfg, parameters=parameters,
        asset_path=source['scene']['robot']['spawn']['asset_path'], output=str(output))
    write_json(output / 'inputs.json', context)
    write_json(output / 'manifest.json', dict(execution_domain='VALIDATION_SIM',
        checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],
        onnx_sha256=policy['policy_interface']['onnx_sha256'], source_sha256=sha256(Path(__file__)),
        design=design, inputs_sha256=sha256(output / 'inputs.json'),
        kp=2, residual_total_limit_nm=2, residual_total_slew_nm_s=2,
        score='mean planar +0.5*max planar +0.5*reverse excursion +5*tail velocity RMS',
        gates='All complete; paired pitch RMS <=110%, pitch rate RMS <=125%, wheel RMS <=125% of baseline.'))
    with ProcessPoolExecutor(max_workers=args.workers, initializer=initialize, initargs=(context,)) as pool:
        jobs = {pool.submit(run, job): job for job in design['jobs']}
        for i, future in enumerate(as_completed(jobs), 1):
            result = future.result()
            with (output / 'results.jsonl').open('a') as stream:
                stream.write(json.dumps(result, allow_nan=False) + '\n')
            print('[VALIDATION_SIM]', i, '/', len(jobs), result['id'], result['evidence_status'],
                'score', result['metrics']['score'], flush=True)


if __name__ == '__main__':
    main()
