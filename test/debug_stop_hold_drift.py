"""VALIDATION_SIM: actual post-drive motion versus odometry and residual authority."""

import argparse
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from play_flash_velocity_hold_sync import (
    REPO, ARCHIVE, Plant, StopHold, Sensors, Description, policy_config,
    read_yaml, write_json, sha256, WHEELS, additive_torque, infer_synchronized,
)


def run(policy, cfg, description, parameters, case, direction, output, history=False):
    plant = Plant(policy, cfg, description, parameters, {'name': 'nominal'}, 42, 0.)
    env, playback = plant.env, plant.playback
    hold = StopHold(description, parameters['equilibrium_pitch'])
    rows = []
    u = 0.
    flash = np.zeros((4, 8))
    motor = flash.copy()
    stop_path = None
    failures = []
    try:
        last_tick = 8000 if history else 4500
        for tick in range(last_tick + 1):
            t = tick * .02
            command = np.array([direction * .2 if 2 <= t < 7 else 0., 0., 0.], dtype=np.float32)
            if history:
                # Hold edges from live events; yaw onset only known to 1-second log resolution.
                command[:] = 0.
                if 12 <= t < 18.98 or 53.12 <= t < 62.26:
                    command[0] = -.1
                elif 32.02 <= t < 39.70:
                    command[0] = .1
                if 55.98 <= t < 62.26:
                    command[2] = .15
            obs = plant.observe()
            failures, _ = plant.failures(obs, 'synchronized')
            data = plant.truth_data
            packet = Sensors(env.joint_pos(), env.joint_vel(),
                data.sensor('trunk_quat').data.copy(), data.sensor('trunk_gyro').data.copy())
            hold_u, diag = hold.step(command, packet, .02)
            if case == 'hold':
                u = hold_u
            else:
                target = {'off': 0., 'positive': 1., 'negative': -1.}[case] if t >= 10 else 0.
                u = float(np.clip(target, u - .04, u + .04))
            if tick == (3113 if history else 350):
                stop_path = obs['gt'][0]
            rows.append(dict(time=t, command=command.copy(), gt=obs['gt'].copy(),
                position=obs['position'].copy(), rpy=obs['rpy'].copy(),
                relative_p=np.nan if diag['relative_p'] is None else diag['relative_p'],
                estimated_v=np.nan if diag['estimated_v'] is None else diag['estimated_v'],
                residual=u, raw_residual=diag['raw_total_nm'],
                flash_total=float(np.mean(flash[:, WHEELS] @ plant.signs)),
                actual_total=float(np.mean(motor[:, WHEELS] @ plant.signs))))
            if failures or tick == last_tick:
                break
            _, action = infer_synchronized(playback, env, packet, command)
            flash_rows = []

            def override(q, dq, torque):
                flash_rows.append(torque.copy())
                return additive_torque(torque, u, plant.signs)

            _, motor = playback.step(action, override)
            flash = np.asarray(flash_rows)
        trace = {key: np.asarray([row[key] for row in rows]) for key in rows[0]}
        name = f'{case}_{direction:+d}'
        np.savez_compressed(output / (name + '.npz'), **trace)
        windows = []
        windows_to_check = [(70, 90), (100, 120), (140, 160)] if history else [(10, 20), (30, 45), (70, 90)]
        for start, end in windows_to_check:
            mask = (trace['time'] >= start) & (trace['time'] < end)
            if not mask.any():
                continue
            summary = dict(start_s=start, end_s=end)
            for key in ('estimated_v', 'residual', 'flash_total', 'actual_total'):
                summary[key] = float(np.nanmean(trace[key][mask]))
            summary['true_v'] = float(trace['gt'][mask, 1].mean())
            summary['relative_p_start_end'] = trace['relative_p'][mask][[0, -1]].tolist()
            summary['true_path_since_stop_start_end'] = (trace['gt'][mask, 0][[0, -1]] - stop_path).tolist()
            summary['odometry_velocity_rms_error'] = float(np.sqrt(np.mean(
                (trace['estimated_v'][mask] - trace['gt'][mask, 1]) ** 2)))
            windows.append(summary)
        return dict(execution_domain='VALIDATION_SIM', evidence_status='FAIL' if failures else 'PASS',
            case=case, direction=direction, seed=42, duration_s=float(trace['time'][-1]),
            failures=failures, trace=name + '.npz', windows=windows)
    finally:
        env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--manual-history', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(REPO / 'docs/exp') or output.exists():
        parser.error('New docs/exp output directory required')
    output.mkdir(parents=True)
    policy = policy_config()
    cfg = json.loads((ARCHIVE / 'config.json').read_text())
    parameters = json.loads((ARCHIVE / 'manifest.json').read_text())['nominal_parameters']
    source = read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description = Description(source['scene']['robot']['spawn']['asset_path'])
    write_json(output / 'manifest.json', dict(execution_domain='VALIDATION_SIM',
        checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],
        onnx_sha256=policy['policy_interface']['onnx_sha256'], script_sha256=sha256(Path(__file__)),
        notes='Synchronized actor. Same seed42 initial state. Drive 2-7s; stop through 90s. Constant signed total torques are diagnostic-only, slew 2 Nm/s, bound 1 Nm.'))
    if args.manual_history:
        manifest = json.loads((output / 'manifest.json').read_text())
        manifest['notes'] = 'Approximate live command history: -0.1 at 12-18.98s, +0.1 at 32.02-39.70s, -0.1 at 53.12-62.26s; yaw +0.15 at 55.98-62.26s. Final stop through160s. Yaw onset resolution1s; not exact live replay.'
        write_json(output / 'manifest.json', manifest)
    for direction in ((1,) if args.manual_history else (1, -1)):
        for case in (('hold', 'off') if args.manual_history else ('hold', 'off', 'positive', 'negative')):
            result = run(policy, cfg, description, parameters, case, direction, output, args.manual_history)
            with (output / 'results.jsonl').open('a') as stream:
                stream.write(json.dumps(result, allow_nan=False) + '\n')
            print('[VALIDATION_SIM]', case, direction, result['evidence_status'], result['windows'][-1], flush=True)


if __name__ == '__main__':
    main()
