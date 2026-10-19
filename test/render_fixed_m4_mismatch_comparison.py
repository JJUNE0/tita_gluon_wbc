"""VALIDATION_SIM: static CoM/mass/friction changes, frozen M4, matched five-minute videos."""

import argparse
import json
from pathlib import Path
import time

import render_fixed_m4_drift_comparison as video
import numpy as np
from static_target_domain import StaticEnv, StaticRunner
from sim2sim_ros2_jazzy.residual_wheel_lqr import ResidualWheelLQR

DT = video.DT


def collect(out, case):
    cfg = json.loads(video.prepared_config(video.CKPT).read_text())
    runner = StaticRunner(cfg, dict(seed=270, pitch=0.), case['target'])
    env = runner.env
    try:
        for tick in range(400):
            runner.step(0.)
            if tick >= 50 and runner.failures():
                raise RuntimeError(f'Common FlashSAC prefix failed: {runner.failures()}')
        env.assert_static()
        snapshot = runner.full_snapshot()
        video.write(out / 'config.json', cfg)
        physics = dict(env.metadata, total_mass_kg=float(env.model.body_mass[1:].sum()),
                       base_link_com_m=env.model.body_ipos[env.model.body('base_link').id].tolist(),
                       contacts_at_video_start=runner.contact_metadata(),
                       prefix_seconds=8.)
        video.write(out / 'physics.json', physics)
        np.savez_compressed(out / 'model_physics.npz', mass=env.model.body_mass,
                            inertia=env.model.body_inertia, com=env.model.body_ipos,
                            friction=env.model.geom_friction)
        np.savez_compressed(out / 'startup.npz',
                            qpos=[s['qpos'] for s in env.startup],
                            qvel=[s['qvel'] for s in env.startup],
                            motor=[s['motor'] for s in env.startup])
        for group in range(2):
            path = out / f'group_{group}.npz'
            if path.exists():
                raise FileExistsError(path)
            runner.full_restore(snapshot)
            residual = ResidualWheelLQR(env) if group else None
            positions, rpy, sensors, actions, inputs = [], [], [], [], []
            qpos, qvel, sample_ticks = [], [], []
            failure = []
            started = time.monotonic()
            for tick in range(15001):
                observation = runner.observation
                positions.append(observation['base_position'].copy())
                rpy.append(observation['rpy'].copy())
                sensors.append(observation['sensor'].copy())
                actions.append(runner.playback.last_action.copy())
                failure = runner.failures()
                if tick % 5 == 0 or failure:
                    sample_ticks.append(tick)
                    qpos.append(env.data.qpos.copy())
                    qvel.append(env.data.qvel.copy())
                if failure or tick == 15000:
                    break
                total = 0.
                if residual:
                    residual.update(np.zeros(3), runner.playback.last_action)
                    total = residual.u
                step = runner.step(total)
                if residual:
                    np.testing.assert_allclose(residual.apply(step['flash'][0]), step['motor'][0], atol=1e-7)
                np.testing.assert_array_equal(step['motor'], step['physical_motor'])
                assert np.isfinite(step['motor']).all()
                assert np.max(abs(step['motor'][:, [3, 7]])) <= 12.000001
                inputs.append([total, step['actual_u']])
                if tick % 1500 == 0:
                    env.assert_static()
                    print(f'[VALIDATION_SIM] {case["name"]} / {video.NAMES[group]}: '
                          f'{tick * DT:.0f}/300 s; elapsed {time.monotonic() - started:.1f}s', flush=True)
            env.assert_static()
            np.savez_compressed(path, base_position=positions, rpy=rpy, sensor=sensors,
                                previous_action=actions, residual=inputs, qpos=qpos, qvel=qvel,
                                sample_ticks=sample_ticks)
            video.write(out / f'group_{group}_status.json', dict(execution_domain='VALIDATION_SIM',
                        evidence_status='FAIL' if failure else 'PASS', failure=failure,
                        duration_seconds=tick * DT, samples=tick + 1,
                        disabled_obstacles=runner.disabled_obstacles,
                        physics_fingerprint=env.fingerprint(), nominal_controller_unchanged=True))
            print(f'[VALIDATION_SIM] {case["name"]} / {video.NAMES[group]}: '
                  f'finished {tick * DT:.2f}s; failure={failure}', flush=True)
    finally:
        env.close()
    video.summarize(out, horizons=[300])


def render(out, case):
    created = []

    def factory(cfg):
        env = StaticEnv(cfg, case['target'])
        created.append(env)
        recorded = json.loads((out / 'physics.json').read_text())
        assert env.fingerprint() == recorded['fingerprint']
        return env

    video.render(out, 300, env_factory=factory,
                 condition_label=f'{case["label"]} | fixed from startup | nominal K / bias / reference unchanged',
                 physics_note='Static target physics, flat floor')
    path = out / 'video_300_verification.json'
    result = json.loads(path.read_text())
    result.update(target=case['target'], render_physics_fingerprint=created[0].initial_fingerprint,
                  physics_matches_collection=True)
    video.write(path, result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--condition', required=True)
    parser.add_argument('--stage', choices=['collect', 'render'], required=True)
    args = parser.parse_args()
    root = args.output.resolve()
    if not root.is_relative_to(video.REPO / 'docs/exp'):
        parser.error('docs/exp output required')
    plan = json.loads((root / 'plan.json').read_text())
    matches = [case for case in plan['conditions'] if case['name'] == args.condition]
    if len(matches) != 1:
        parser.error('Condition must match the frozen plan')
    case = matches[0]
    out = root / case['name']
    if args.stage == 'collect':
        collect(out, case)
    else:
        render(out, case)


if __name__ == '__main__':
    main()
