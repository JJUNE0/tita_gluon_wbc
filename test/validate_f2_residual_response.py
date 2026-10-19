"""VALIDATION_SIM: frozen F-2 A/B versus matched full-state MuJoCo branches."""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import copy
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_flash_torque_residual import (
    REPO, ARCHIVE, Plant, Description, write_json, policy_config, read_yaml,
    sha256, WHEELS, LEGS, additive_torque, action_history_slice,
)
from play_flash_velocity_hold_sync import infer_synchronized, Sensors

CONTEXT = None


def initialize(context):
    global CONTEXT
    CONTEXT = context


def make_plant(job):
    c = CONTEXT
    return Plant(c['policy'], c['cfg'], Description(c['asset_path']), c['parameters'],
                 {'name': 'nominal'}, job['seed'], job['pitch'])


def infer(plant, observation, actor):
    if actor == 'cached':
        return plant.playback.infer()
    data = plant.truth_data
    packet = Sensors(plant.env.joint_pos(), plant.env.joint_vel(),
        data.sensor('trunk_quat').data.copy(), data.sensor('trunk_gyro').data.copy())
    return infer_synchronized(plant.playback, plant.env, packet, np.zeros(3, dtype=np.float32))


def take_snapshot(plant, observation):
    data = plant.env.mujoco.MjData(plant.env.model)
    plant.env.mujoco.mj_copyData(data, plant.env.model, plant.env.data)
    truth_data = plant.env.mujoco.MjData(plant.env.model)
    plant.env.mujoco.mj_copyData(truth_data, plant.env.model, plant.truth_data)
    attrs = {key: copy.deepcopy(getattr(plant, key)) for key in
        ['path', 'previous_position', 'previous_yaw', 'origin']}
    for name in ['estimator', 'synchronized_estimator']:
        estimator = getattr(plant, name)
        attrs[name] = (estimator.position, copy.deepcopy(estimator.previous))
    return dict(data=data, truth_data=truth_data, last_action=plant.playback.last_action.copy(),
                attrs=attrs, observation=copy.deepcopy(observation))


def restore(plant, snapshot):
    plant.env.mujoco.mj_copyData(plant.env.data, plant.env.model, snapshot['data'])
    plant.env.mujoco.mj_copyData(plant.truth_data, plant.env.model, snapshot['truth_data'])
    plant.playback.last_action = snapshot['last_action'].copy()
    for name, value in snapshot['attrs'].items():
        if name in ('estimator', 'synchronized_estimator'):
            estimator = getattr(plant, name)
            estimator.position, estimator.previous = copy.deepcopy(value)
        else:
            setattr(plant, name, copy.deepcopy(value))
    # No mj_forward on the original data: preserve the cached actor sensor phase.
    return copy.deepcopy(snapshot['observation'])


def step(plant, observation, u, actor):
    playback = plant.playback
    history = playback.last_action.copy()
    policy_obs, action = infer(plant, observation, actor)
    history_slice, scale, clip = action_history_slice(CONTEXT['policy'])
    expected_history = np.clip(history, *clip) * scale if clip is not None else history * scale
    np.testing.assert_array_equal(policy_obs[history_slice], expected_history)
    flash = []
    leg_error = 0.

    def override(q, dq, torque):
        nonlocal leg_error
        flash.append(torque.copy())
        result = additive_torque(torque, u, plant.signs)
        leg_error = max(leg_error, float(abs(result[LEGS] - torque[LEGS]).max()))
        return result

    commands, motors = playback.step(action, override)
    np.testing.assert_array_equal(playback.last_action, action)
    assert leg_error == 0.
    flash = np.asarray(flash)
    actual = (motors[:, WHEELS] - flash[:, WHEELS]) @ plant.signs
    actual_u = float(actual.mean())
    assert abs(actual_u - u) < 1e-6, (actual_u, u)
    assert abs(motors[:, WHEELS]).max() <= 12. + 1e-9
    return plant.observe(), dict(actual_u=actual_u, requested_u=u, action=action,
        policy_observation=policy_obs, motor_substeps=motors, flash_substeps=flash)


def signal(family, amplitude, count=100):
    if family == 'impulse':
        return np.array([amplitude])
    requested = []
    previous = 0.
    rng = np.random.default_rng(1729)
    blocks = rng.choice([-1., 0., 1.], size=20)
    for i in range(count):
        t = i * .02
        if family == 'zero':
            target = 0.
        elif family in ('step_pos', 'step_neg'):
            target = amplitude * (1 if family.endswith('pos') else -1) if .1 <= t < 1.5 else 0.
        elif family in ('pulse_pos', 'pulse_neg'):
            target = amplitude * (1 if family.endswith('pos') else -1) if .1 <= t < .5 else 0.
        elif family == 'prbs':
            target = amplitude * blocks[min(i // 10, len(blocks) - 1)]
        elif family == 'new_sine':
            target = amplitude * np.mean(np.sin(2 * np.pi * np.array([.63, 1.73, 3.41]) * t
                                                + np.array([.7, 1.4, 2.1])))
        else:
            raise ValueError(family)
        previous = float(np.clip(target, previous - .04, previous + .04))
        requested.append(previous)
    return np.asarray(requested)


def rollout(plant, snapshot, actor, inputs):
    obs = restore(plant, snapshot)
    sensor, gt, position, rpy = [], [], [], []
    transitions = []
    failures = []
    for i in range(len(inputs) + 1):
        sensor.append(obs['synchronized'].copy())
        gt.append(obs['gt'].copy())
        position.append(obs['position'].copy())
        rpy.append(obs['rpy'].copy())
        failures, _ = plant.failures(obs, 'synchronized')
        if failures or i == len(inputs):
            break
        plant.env.data.xfrc_applied[:] = 0.
        obs, transition = step(plant, obs, float(inputs[i]), actor)
        transitions.append(transition)
    result = dict(sensor=np.asarray(sensor), gt=np.asarray(gt),
        position=np.asarray(position), rpy=np.asarray(rpy))
    for key in transitions[0]:
        result[key] = np.asarray([t[key] for t in transitions])
    return result, failures


def run_context(job):
    c = CONTEXT
    output = Path(c['output']) / job['id']
    output.mkdir()
    prefix = make_plant(job)
    branch = make_plant(job)
    snapshots = {}
    rows = []
    obs = prefix.observe()
    motor = np.zeros((prefix.env.decimation, 8))
    action = np.zeros(8)
    try:
        for tick in range(601):
            t = tick * .02
            rows.append(dict(time=t, sensor=obs['synchronized'].copy(), gt=obs['gt'].copy(),
                position=obs['position'].copy(), motor_substeps=motor.copy(), action=action.copy()))
            if t in job['times']:
                snapshots[t] = take_snapshot(prefix, obs)
            if tick == 600:
                break
            prefix.env.data.xfrc_applied[:] = 0.
            force = c['cfg']['disturbance']
            if force['start_s'] <= t < force['start_s'] + force['duration_s']:
                prefix.env.data.xfrc_applied[prefix.base, 0] = force['force_n']
            obs, transition = step(prefix, obs, 0., job['actor'])
            motor, action = transition['motor_substeps'], transition['action']
        prefix_trace = {k: np.asarray([r[k] for r in rows]) for k in rows[0]}
        np.savez_compressed(output / 'prefix.npz', **prefix_trace)
        results = []
        b_results = []
        branch_replay = []
        for t, snapshot in snapshots.items():
            start = round(t / .02)
            base, failure = rollout(branch, snapshot, job['actor'], signal('zero', 0.))
            assert not failure
            for key in ['sensor', 'gt', 'position']:
                np.testing.assert_array_equal(base[key], prefix_trace[key][start:start + 101])
            np.testing.assert_array_equal(base['motor_substeps'], prefix_trace['motor_substeps'][start + 1:start + 101])
            np.testing.assert_array_equal(base['action'], prefix_trace['action'][start + 1:start + 101])
            branch_replay.append(t)
            baseline_name = f'base_t{t:g}.npz'
            np.savez_compressed(output / baseline_name, **base)
            for family, amplitude in job['waves']:
                inputs = signal(family, amplitude)
                trace, failure = rollout(branch, snapshot, job['actor'], inputs)
                assert not failure, failure
                assert abs(trace['requested_u']).max() <= 1. + 1e-12
                assert abs(np.diff(np.r_[0., trace['requested_u']])).max() <= .04 + 1e-12
                assert trace['sensor'].shape == base['sensor'].shape
                name = f'{family}_a{amplitude:g}_t{t:g}.npz'
                np.savez_compressed(output / name, **trace)
                results.append(dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
                    context=job['id'], actor=job['actor'], seed=job['seed'], pitch=job['pitch'],
                    start_s=t, family=family, amplitude=amplitude, baseline=baseline_name,
                    trace=name, transitions=len(inputs)))
            for amp in [.01, .02, .04]:
                positive, pf = rollout(branch, snapshot, job['actor'], signal('impulse', amp))
                negative, nf = rollout(branch, snapshot, job['actor'], signal('impulse', -amp))
                assert not pf and not nf
                np.testing.assert_array_equal(positive['action'], base['action'][:1])
                np.testing.assert_array_equal(negative['action'], base['action'][:1])
                denominator = positive['actual_u'][0] - negative['actual_u'][0]
                entry = dict(execution_domain='VALIDATION_SIM', evidence_status='PASS', context=job['id'],
                    actor=job['actor'], start_s=t, amplitude=amp, actual_input_difference_nm=float(denominator))
                for source in ['sensor', 'gt']:
                    empirical = (positive[source][1] - negative[source][1]) / denominator
                    entry[source + '_B'] = empirical.tolist()
                    entry[source + '_positive_delta'] = (positive[source][1] - base[source][1]).tolist()
                    entry[source + '_negative_delta'] = (negative[source][1] - base[source][1]).tolist()
                b_results.append(entry)
        write_json(output / 'results.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
            job=job, branch_zero_exact_replays=branch_replay, responses=results, direct_B=b_results))
        return dict(execution_domain='VALIDATION_SIM', evidence_status='PASS', job=job,
                    responses=len(results), B_tests=len(b_results), branch_zero_exact_replays=branch_replay)
    finally:
        prefix.env.close()
        branch.env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--design', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=3)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(REPO / 'docs/exp') or output.exists():
        parser.error('New docs/exp output required')
    output.mkdir(parents=True)
    policy = policy_config()
    cfg = json.loads((ARCHIVE / 'config.json').read_text())
    parameters = json.loads((ARCHIVE / 'manifest.json').read_text())['nominal_parameters']
    source = read_yaml(next(x for x in policy['policy_interface']['sources'] if x.endswith('env.yaml')))
    context = dict(policy=policy, cfg=cfg, parameters=parameters,
        asset_path=source['scene']['robot']['spawn']['asset_path'], output=str(output))
    design = json.loads(args.design.read_text())
    write_json(output / 'inputs.json', context)
    write_json(output / 'manifest.json', dict(execution_domain='VALIDATION_SIM',
        checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],
        onnx_sha256=policy['policy_interface']['onnx_sha256'], source_sha256=sha256(Path(__file__)),
        design=design, note='Model is frozen; each intervention starts from identical full mjData, cached sensors, actor last_action and odometry history. Input array[k] drives state[k] to state[k+1].'))
    with ProcessPoolExecutor(max_workers=args.workers, initializer=initialize, initargs=(context,)) as pool:
        futures = [pool.submit(run_context, job) for job in design['jobs']]
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            with (output / 'contexts.jsonl').open('a') as stream:
                stream.write(json.dumps(result, allow_nan=False) + '\n')
            print('[VALIDATION_SIM]', i, '/', len(futures), result['job']['id'], result['evidence_status'],
                  result['responses'], 'responses', result['B_tests'], 'B tests', flush=True)


if __name__ == '__main__':
    main()
