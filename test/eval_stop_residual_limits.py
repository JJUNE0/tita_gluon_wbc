"""VALIDATION_SIM: total residual torque bound sweep, synchronized FlashSAC."""

import argparse
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from play_flash_velocity_hold_sync import (
    REPO, ARCHIVE, Plant, StopHold, Sensors, Description, policy_config,
    read_yaml, write_json, sha256, WHEELS, LEGS, additive_torque, infer_synchronized,
)


class BoundedStopHold(StopHold):
    def __init__(self, description, equilibrium_pitch, limit):
        super().__init__(description, equilibrium_pitch)
        self.limit = limit

    def step(self, command, sensors, dt):
        previous = self.u
        _, diagnostic = super().step(command, sensors, dt)
        target = diagnostic['activation'] * np.clip(
            diagnostic['raw_total_nm'], -self.limit, self.limit) if self.holding else 0.
        self.u = float(np.clip(target, previous - 2 * dt, previous + 2 * dt))
        diagnostic['mode'] = 'HOLD' if self.holding else ('RELEASE' if abs(self.u) > 1e-9 else 'MOVE')
        return self.u, diagnostic


def command_at(t):
    command = np.zeros(3, dtype=np.float32)
    if 12 <= t < 18.98 or 53.12 <= t < 62.26:
        command[0] = -.1
    elif 32.02 <= t < 39.70:
        command[0] = .1
    if 55.98 <= t < 62.26:
        command[2] = .15
    return command


def run(policy, cfg, description, parameters, limit, seed, output):
    plant = Plant(policy, cfg, description, parameters, {'name': 'nominal'}, seed, 0.)
    env, playback = plant.env, plant.playback
    hold = BoundedStopHold(description, parameters['equilibrium_pitch'], limit)
    rows = []
    motor = np.zeros((4, 8))
    failure = []
    leg_error = 0.
    try:
        for tick in range(8001):
            t = tick * .02
            observation = plant.observe()
            failure, _ = plant.failures(observation, 'synchronized')
            data = plant.truth_data
            packet = Sensors(env.joint_pos(), env.joint_vel(),
                data.sensor('trunk_quat').data.copy(), data.sensor('trunk_gyro').data.copy())
            command = command_at(t)
            u, diagnostic = hold.step(command, packet, .02)
            rows.append(dict(time=t, gt=observation['gt'].copy(), position=observation['position'].copy(),
                rpy=observation['rpy'].copy(), command=command.copy(), residual=u,
                relative_p=np.nan if diagnostic['relative_p'] is None else diagnostic['relative_p'],
                motor_substeps=motor.copy()))
            if failure or tick == 8000:
                break
            _, action = infer_synchronized(playback, env, packet, command)

            def override(q, dq, torque):
                nonlocal leg_error
                result = additive_torque(torque, u, plant.signs)
                leg_error = max(leg_error, float(abs(result[LEGS] - torque[LEGS]).max()))
                return result

            _, motor = playback.step(action, override)
            np.testing.assert_array_equal(playback.last_action, action)
        trace = {key: np.asarray([r[key] for r in rows]) for key in rows[0]}
        name = f'limit{limit:g}_s{seed}'
        np.savez_compressed(output / (name + '.npz'), **trace)
        assert abs(trace['residual']).max() <= limit + 1e-12
        assert np.max(abs(np.diff(trace['residual']))) <= .04 + 1e-12
        assert leg_error == 0.
        metrics = dict()
        for label, start, end in [('whole', 0, 160.02), ('stop', 62.26, 160.02), ('late', 140, 160)]:
            mask = (trace['time'] >= start) & (trace['time'] < end)
            if not mask.any():
                continue
            wheels = trace['motor_substeps'][mask][:, :, WHEELS]
            metrics[label] = dict(
                pitch_error_rms_rad=float(np.sqrt(np.mean(trace['gt'][mask, 2] ** 2))),
                pitch_rate_rms_rad_s=float(np.sqrt(np.mean(trace['gt'][mask, 3] ** 2))),
                wheel_torque_rms_nm=float(np.sqrt(np.mean(wheels ** 2))),
                wheel_torque_peak_nm=float(abs(wheels).max()),
                saturation_fraction=float(np.mean(abs(trace['residual'][mask]) >= limit - 1e-9)),
                true_v_mean_m_s=float(trace['gt'][mask, 1].mean()),
                true_v_rms_m_s=float(np.sqrt(np.mean(trace['gt'][mask, 1] ** 2))),
                relative_p_final_m=float(trace['relative_p'][mask][-1]))
        stop_index = np.flatnonzero(trace['time'] == 62.26)
        if len(stop_index):
            i = stop_index[0]
            path = trace['gt'][i:, 0] - trace['gt'][i, 0]
            planar = np.linalg.norm((trace['position'][i:] - trace['position'][i])[:, :2], axis=1)
            metrics['stop'].update(path_final_m=float(path[-1]), path_max_abs_m=float(abs(path).max()),
                planar_final_m=float(planar[-1]), planar_max_m=float(planar.max()))
        return dict(execution_domain='VALIDATION_SIM', evidence_status='FAIL' if failure else 'PASS',
            limit_total_nm=limit, seed=seed, completed_s=float(trace['time'][-1]), failure=failure,
            leg_torque_error_nm=leg_error, metrics=metrics, trace=name + '.npz')
    finally:
        env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--limits', nargs='+', type=float, default=[1., 1.5, 2., 3.])
    parser.add_argument('--seeds', nargs='+', type=int, default=[42])
    args = parser.parse_args()
    if any(not np.isfinite(x) or x <= 0 for x in args.limits):
        parser.error('Positive finite limits required')
    output = args.output.resolve()
    if not output.is_relative_to(REPO / 'docs/exp') or output.exists():
        parser.error('New docs/exp output required')
    output.mkdir(parents=True)
    policy = policy_config()
    cfg = json.loads((ARCHIVE / 'config.json').read_text())
    parameters = json.loads((ARCHIVE / 'manifest.json').read_text())['nominal_parameters']
    source = read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description = Description(source['scene']['robot']['spawn']['asset_path'])
    write_json(output / 'manifest.json', dict(execution_domain='VALIDATION_SIM',
        checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],
        onnx_sha256=policy['policy_interface']['onnx_sha256'], script_sha256=sha256(Path(__file__)),
        limits_total_nm=args.limits, seeds=args.seeds, duration_s=160, kp=2, kv=.5,
        ramp_s=1, slew_total_nm_s=2, note='Same approximate manual history as preceding diagnosis; only residual bound changes.'))
    for seed in args.seeds:
        for limit in args.limits:
            result = run(policy, cfg, description, parameters, limit, seed, output)
            with (output / 'results.jsonl').open('a') as stream:
                stream.write(json.dumps(result, allow_nan=False) + '\n')
            print('[VALIDATION_SIM]', limit, seed, result['evidence_status'], result['metrics'].get('late'), flush=True)


if __name__ == '__main__':
    main()
