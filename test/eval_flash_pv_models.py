"""VALIDATION_SIM: matched residual responses of synchronized model_60000 FlashSAC.

Collects data only. Original wheel/leg PD and raw action history remain active;
neither F-1 feedback nor LQR is applied. Models are fitted in the analysis script.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import copy
import json
from pathlib import Path
import sys

import numpy as np
from scipy.spatial.transform import Rotation

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO / 'sim2sim/sim2sim_ros2_jazzy'), str(REPO)]
from sim2sim.lqr.estimator import Sensors, WheelOdometry
from sim2sim.lqr.model import Description
from sim2sim.lqr.runtime import Playback
from sim2sim_ros2_jazzy.adapter import ObsState, quat_wxyz_to_rotmat
from sim2sim_ros2_jazzy.checkpoint import prepared_config, read_yaml, sha256
from sim2sim_ros2_jazzy.state_machine import SPLAY_POSE, StateMachine

CKPT = REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_60000'
WHEELS = np.array([3, 7])
LEGS = np.array([0, 1, 2, 4, 5, 6])


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def waveform(family, amplitude, seed, count=100):
    rng = np.random.default_rng(seed)
    phases = rng.uniform(-np.pi, np.pi, 4)
    frequencies = np.array([.43, 1.37, 3.17, 6.23]) if family == 'train_sine' else np.array([.67, 1.91, 4.31, 7.13])
    blocks = rng.choice([-1., 1.], count)
    lengths = rng.choice([1, 3, 5, 9] if family == 'train_prbs' else [3, 7, 11], count)
    prbs = np.repeat(blocks, lengths)[:count]
    result, previous = [], 0.
    for i in range(count):
        t = i * .02
        if 'sine' in family:
            target = amplitude * np.mean(np.sin(2*np.pi*frequencies*t+phases))
        elif 'prbs' in family:
            target = amplitude * prbs[i]
        elif family.startswith('step'):
            target = amplitude * (1 if family.endswith('pos') else -1) if .1 <= t < 1.5 else 0.
        elif family.startswith('pulse'):
            target = amplitude * (1 if family.endswith('pos') else -1) if .1 <= t < .5 else 0.
        elif family == 'zero':
            target = 0.
        else:
            raise ValueError(family)
        previous = float(np.clip(target, previous-.04, previous+.04))
        result.append(previous)
    return np.asarray(result)


class Runner:
    def __init__(self, cfg, job):
        self.playback = Playback(cfg)
        self.env = env = self.playback.env
        source = read_yaml(next(p for p in cfg['policy_interface']['sources'] if p.endswith('env.yaml')))
        self.description = Description(source['scene']['robot']['spawn']['asset_path'])
        self.estimator = WheelOdometry(self.description, 0.)
        self.sensors = env.mujoco.MjData(env.model)
        self.wheel_bodies = [env.model.body(name).id for name in self.description.wheel_links]
        self.wheel_joints = [env.model.joint(env.joint_names[i]).id for i in WHEELS]
        self.leg_joints = [env.model.joint(env.joint_names[i]).id for i in LEGS]
        floor = env.model.geom('floor').id
        obstacles = np.flatnonzero((env.model.geom_bodyid == 0) & (np.arange(env.model.ngeom) != floor))
        env.model.geom_contype[obstacles] = env.model.geom_conaffinity[obstacles] = 0
        self.disabled_obstacles = obstacles.tolist()
        env.reset(SPLAY_POSE)
        rng = np.random.default_rng(job['seed'])
        env.data.qpos[3:7] = Rotation.from_euler('y', job['pitch']).as_quat()[[3, 0, 1, 2]]
        env.data.qvel[0] = rng.uniform(-.015, .015)
        env.data.qvel[env.qvel_addr[LEGS]] = rng.normal(0., .01, len(LEGS))
        env.mujoco.mj_forward(env.model, env.data)
        sm = StateMachine(cfg['robot']['torque_limit'], auto_rl=True)
        sm.request('transform_up', env.joint_pos())
        self.startup_steps = 0
        while sm.state != 'rl':
            sm.update(env.control_dt)
            if sm.state != 'rl':
                env.step_with_torque_callback(sm.torque)
                self.startup_steps += 1
        self.gt_path = 0.
        self.previous_gt = None
        self.observation = self.observe()

    def observe(self):
        env, data = self.env, self.sensors
        env.mujoco.mj_copyData(data, env.model, env.data)
        env.mujoco.mj_forward(env.model, data)
        quat = data.sensor('trunk_quat').data.copy()
        gyro = data.sensor('trunk_gyro').data.copy()
        rotation = Rotation.from_quat(quat[[1, 2, 3, 0]])
        rpy = rotation.as_euler('xyz')
        forward = np.array([np.cos(rpy[2]), np.sin(rpy[2]), 0.])
        lateral = np.array([-np.sin(rpy[2]), np.cos(rpy[2]), 0.])
        signs = np.sign(data.xaxis[self.wheel_joints] @ lateral)
        state = self.estimator.observe(Sensors(env.joint_pos(), env.joint_vel(), quat, gyro), env.control_dt)
        axle = np.mean(data.xpos[self.wheel_bodies], axis=0)
        velocity = np.zeros(3)
        for body in self.wheel_bodies:
            jac = np.zeros((3, env.model.nv))
            env.mujoco.mj_jac(env.model, data, jac, None, data.xpos[body], body)
            velocity += jac @ data.qvel / 2
        if self.previous_gt is not None:
            position, yaw = self.previous_gt
            angle = yaw + ((rpy[2]-yaw+np.pi) % (2*np.pi)-np.pi)/2
            self.gt_path += (axle-position) @ [np.cos(angle), np.sin(angle), 0.]
        self.previous_gt = (axle.copy(), rpy[2])
        gt = np.array([self.gt_path, velocity @ forward, state[2], state[3]])
        return dict(sensor=state, gt=gt, position=axle, rpy=rpy, signs=signs, quat=quat, gyro=gyro)

    def failures(self):
        env, o = self.env, self.observation
        reasons = []
        if not np.isfinite(np.r_[env.data.qpos, env.data.qvel]).all():
            reasons.append('nonfinite')
        if abs(o['rpy'][0]) > .65 or abs(o['rpy'][1]) > .65:
            reasons.append('attitude_limit')
        if env.data.qpos[2] < .18:
            reasons.append('base_height_limit')
        q = env.joint_pos()[LEGS]
        limits = env.model.jnt_range[self.leg_joints]
        if np.any((q < limits[:, 0]-.01) | (q > limits[:, 1]+.01)):
            reasons.append('leg_joint_limit')
        return reasons

    def step(self, residual):
        env, playback, o = self.env, self.playback, self.observation
        before_history = playback.last_action.copy()
        obs = playback.builder.build(ObsState(env.joint_pos(), env.joint_vel(), o['quat'].astype(np.float32),
            o['gyro'].astype(np.float32), np.zeros(3, dtype=np.float32), before_history,
            quat_wxyz_to_rotmat(o['quat']).T @ env.base_lin_vel()))
        action = playback.policy.run(['nn_output'], {'nn_input0': obs.reshape(1, -1)})[0].reshape(8)
        flash, applied = [], []

        def callback(q, dq):
            original = playback.adapter.compute(action, q, dq)
            result = original.copy()
            result[WHEELS] = np.clip(original[WHEELS]+o['signs']*residual/2,
                -playback.adapter.limit[WHEELS], playback.adapter.limit[WHEELS])
            np.testing.assert_array_equal(result[LEGS], original[LEGS])
            flash.append(original.copy()); applied.append(result.copy())
            return result

        env.step_with_torque_callback(callback)
        playback.last_action = action.copy()
        self.observation = self.observe()
        flash, applied = np.asarray(flash), np.asarray(applied)
        actual = (applied[:, WHEELS]-flash[:, WHEELS]) @ o['signs']
        return dict(actual_u=float(actual.mean()), requested_u=residual, action=action,
            policy_observation=obs, history=before_history, motor=applied, flash=flash)

    def snapshot(self):
        data = self.env.mujoco.MjData(self.env.model)
        sensors = self.env.mujoco.MjData(self.env.model)
        self.env.mujoco.mj_copyData(data, self.env.model, self.env.data)
        self.env.mujoco.mj_copyData(sensors, self.env.model, self.sensors)
        attributes = copy.deepcopy((self.estimator.position, self.estimator.previous,
            self.gt_path, self.previous_gt, self.observation, self.playback.last_action))
        return data, sensors, attributes

    def restore(self, snapshot):
        data, sensors, attributes = snapshot
        self.env.mujoco.mj_copyData(self.env.data, self.env.model, data)
        self.env.mujoco.mj_copyData(self.sensors, self.env.model, sensors)
        (self.estimator.position, self.estimator.previous, self.gt_path, self.previous_gt,
            self.observation, self.playback.last_action) = copy.deepcopy(attributes)

    def rollout(self, inputs):
        rows, transitions = [], []
        for i in range(len(inputs)+1):
            rows.append({key: self.observation[key].copy() for key in ['sensor', 'gt', 'position', 'rpy']})
            failures = self.failures()
            if failures or i == len(inputs):
                break
            transitions.append(self.step(float(inputs[i])))
        trace = {key: np.asarray([r[key] for r in rows]) for key in rows[0]}
        if transitions:
            trace.update({key: np.asarray([r[key] for r in transitions]) for key in transitions[0]})
        return trace, failures


def run_job(cfg, job, output):
    out = Path(output) / job['id']
    out.mkdir()
    runner = Runner(cfg, job)
    snapshots, states, transitions, startup_violations = {}, [], [], []
    try:
        end = round((max(job['times'])+2.)/.02)
        for tick in range(end+1):
            states.append({key: runner.observation[key].copy() for key in ['sensor', 'gt', 'position', 'rpy']})
            failures = runner.failures()
            if tick < 50:
                if failures:
                    startup_violations.append(dict(rl_s=tick*.02, failures=failures,
                        base_height_m=float(runner.env.data.qpos[2])))
            else:
                assert not failures, (job, tick, failures)
            if tick in [round(t/.02) for t in job['times']]:
                snapshots[tick] = runner.snapshot()
            if tick < end:
                transitions.append(runner.step(0.))
        prefix = {key: np.asarray([r[key] for r in states]) for key in states[0]}
        prefix.update({key: np.asarray([r[key] for r in transitions]) for key in transitions[0]})
        np.savez_compressed(out/'prefix.npz', **prefix)
        results, direct, replays = [], [], []
        for tick, snapshot in snapshots.items():
            runner.restore(snapshot)
            zero, failure = runner.rollout(np.zeros(100))
            assert not failure
            for key in ['sensor', 'gt', 'position', 'rpy']:
                np.testing.assert_array_equal(zero[key], prefix[key][tick:tick+101])
            for key in ['action', 'motor', 'policy_observation', 'history']:
                np.testing.assert_array_equal(zero[key], prefix[key][tick:tick+100])
            base_name = f'zero_t{tick}.npz'
            np.savez_compressed(out/base_name, **zero)
            replays.append(tick)
            for aindex, amplitude in enumerate(job['amplitudes']):
                for findex, family in enumerate(job['families']):
                    probe_seed = int(np.random.SeedSequence([job['seed'], job['pitch_index'], tick,
                        aindex, findex, 101 if job['split'] == 'train' else 997]).generate_state(1)[0])
                    inputs = waveform(family, amplitude, probe_seed)
                    runner.restore(snapshot)
                    trace, failures = runner.rollout(inputs)
                    assert len(trace['sensor']) == 101 and not failures, (job, family, failures)
                    assert np.max(abs(trace['actual_u']-inputs)) < 1e-6
                    assert np.max(abs(trace['actual_u'])) <= .500001
                    assert np.max(abs(np.diff(np.r_[0., trace['actual_u']]))) <= .040001
                    np.testing.assert_array_equal(trace['sensor'][0], zero['sensor'][0])
                    name = f'{family}_a{amplitude:g}_t{tick}.npz'
                    np.savez_compressed(out/name, **trace)
                    results.append(dict(trace=name, baseline=base_name, family=family, amplitude=amplitude,
                        start_rl_s=tick*.02, input_seed=probe_seed, failures=failures))
            for amp in [.01, .02, .04]:
                runner.restore(snapshot); plus, pf = runner.rollout([amp])
                runner.restore(snapshot); minus, mf = runner.rollout([-amp])
                assert not pf and not mf
                np.testing.assert_array_equal(plus['action'][0], zero['action'][0])
                np.testing.assert_array_equal(minus['action'][0], zero['action'][0])
                denominator = plus['actual_u'][0]-minus['actual_u'][0]
                direct.append(dict(start_rl_s=tick*.02, amplitude=amp,
                    sensor_B=((plus['sensor'][1]-minus['sensor'][1])/denominator).tolist(),
                    gt_B=((plus['gt'][1]-minus['gt'][1])/denominator).tolist()))
        result = dict(execution_domain='VALIDATION_SIM', evidence_status='PASS', job=job,
            startup_steps=runner.startup_steps, disabled_obstacles=runner.disabled_obstacles,
            excluded_first_rl_s=1., startup_violations=startup_violations,
            exact_zero_replay_ticks=replays, responses=results, direct_B=direct,
            leg_path='original ActionAdapter unchanged every substep', history='raw actor output',
            actor='current joint state and clone-refreshed IMU', feedback_residual_enabled=False)
        write(out/'results.json', result)
        return dict(id=job['id'], split=job['split'], responses=len(results), direct_pairs=len(direct), zero_replays=len(replays))
    finally:
        runner.env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=3)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    out = args.output.resolve()
    if not out.is_relative_to(REPO/'docs/exp') or out.exists():
        parser.error('New output directory under docs/exp required')
    out.mkdir(parents=True)
    config = prepared_config(CKPT)
    if config is None:
        raise RuntimeError('Prepare and verify model_60000 first')
    cfg = json.loads(config.read_text())
    assert cfg['policy_interface']['algorithm'] == 'FlashSAC'
    assert cfg['control']['sim_timestep']*cfg['control']['decimation'] == .02
    jobs = []
    for split, seeds, families in [('train', [80, 81], ['train_sine', 'train_prbs']),
            ('validation', [82, 83], ['step_pos', 'step_neg', 'pulse_pos', 'pulse_neg', 'validation_sine', 'validation_prbs'])]:
        for seed in seeds:
            for pindex, pitch in enumerate([-.025, 0., .025]):
                jobs.append(dict(id=f'{split}_s{seed}_p{pitch:+.3f}', split=split, seed=seed,
                    pitch=pitch, pitch_index=pindex, times=[4., 6., 8.], amplitudes=[.1, .25, .5], families=families))
    if args.smoke:
        jobs = [dict(id='smoke_s79', split='train', seed=79, pitch=0., pitch_index=1,
                     times=[4.], amplitudes=[.1, .25], families=['train_sine', 'train_prbs'])]
    protected = list((REPO/'sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy').glob('*.py'))
    protected += [config, config.parent/'policy.onnx', CKPT/'actor.pt']
    hashes = {str(p.relative_to(REPO)): sha256(p) for p in protected}
    manifest = dict(execution_domain='VALIDATION_SIM', evidence_status='NOT_TESTED',
        checkpoint=str(CKPT), checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
        onnx_sha256=sha256(config.parent/'policy.onnx'), config=str(config), jobs=jobs,
        script_sha256=sha256(Path(__file__)), protected_sha256=hashes,
        plan=dict(state='synchronized encoder/IMU [p,v,pitch,pitch_rate]; GT evaluation only',
            dynamics='matched residual rollout minus zero rollout from full-state snapshot',
            models=['M1 [p,v]', 'M2 [p,v,pitch,pitch_rate]'],
            fit='train only, no intercept, first A column fixed to position translation symmetry',
            primary_metrics='p/v only; one-step,0.1/0.5/1/2s free prediction, pulse A-only',
            operational_gate='median trace response NRMSE <=0.30 for both p/v at0.1/0.5/1s and full2s; velocity direct-B median relative error<=0.30',
            gate_note='Diagnostic thresholds chosen before data; not a user specification or proof of closed-loop control',
            probe='total amplitude<=0.5Nm, slew<=2Nm/s; no F1 feedback, no LQR',
            simulation='flat contact; scene obstacles disabled in memory; no external pushes',
            startup='runtime transform_up -> RL; first1s startup transient logged separately, no model samples; branches at4/6/8s',
            phases='randomized per initial condition,branch,amplitude,family; held-out frequencies and PRBS block lengths'))
    write(out/'manifest.json', manifest)
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_job, cfg, job, str(out)) for job in jobs]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print('[VALIDATION_SIM]', result, flush=True)
    assert all(sha256(REPO/name) == value for name, value in hashes.items())
    write(out/'completion.json', dict(execution_domain='VALIDATION_SIM', evidence_status='PASS',
        jobs=results, protected_sources_preserved=True, responses=sum(r['responses'] for r in results),
        direct_pairs=sum(r['direct_pairs'] for r in results), zero_replays=sum(r['zero_replays'] for r in results)))


if __name__ == '__main__':
    main()
