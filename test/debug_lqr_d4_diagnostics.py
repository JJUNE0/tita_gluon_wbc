"""VALIDATION_SIM: diagnostic-only state/gain cross-tests; no deployed controller edits."""

import argparse
from collections import deque
import copy
import csv
import hashlib
import json
from pathlib import Path
import sys
import time
from types import SimpleNamespace

import numpy as np
from scipy.spatial.transform import Rotation

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from sim2sim.lqr.controller import WheelLQR
from sim2sim.lqr.estimator import Sensors, WheelOdometry
from sim2sim.lqr.evaluate import ground_truth, sensors, setup_scene, write_json
from sim2sim.lqr.model import Description, residual_matrices
from sim2sim.lqr.runtime import LEGS, WHEELS, Playback, policy_config
from sim2sim_ros2_jazzy.checkpoint import read_yaml, sha256

ARCHIVE = REPO / 'docs/exp/2026-10-14/lqr_ablation/full'


class Plant:
    def __init__(self, policy, cfg, description, parameters, mismatch, seed, disturbance):
        self.playback = Playback(policy)
        self.env = self.playback.env
        self.cfg, self.description, self.parameters, self.mismatch = cfg, description, parameters, mismatch
        self.applied = setup_scene(self.playback, mismatch, description)
        self.stand = np.asarray(policy['robot']['default_joint_angles'])
        self.dt = self.env.control_dt
        self.initial_velocity = cfg['initial_velocity_m_s'] + np.random.default_rng(seed).uniform(
            -cfg['initial_velocity_jitter_m_s'], cfg['initial_velocity_jitter_m_s'])
        rotation = Rotation.from_euler('xyz', [parameters['equilibrium_roll'],
                                               parameters['equilibrium_pitch']+disturbance, 0.])
        self.env.data.qpos[3:7] = rotation.as_quat()[[3, 0, 1, 2]]
        frames, axes = description.frames(self.stand)
        bottoms = []
        for name, joint in zip(description.wheel_links, ('joint_left_leg_4', 'joint_right_leg_4')):
            center = rotation.apply(frames[name][:3, 3])
            axis = rotation.apply(axes[joint])
            half_width = float(description.links[name].find('collision/geometry/cylinder').get('length'))/2
            extent = description.radius*np.sqrt(1-axis[2]**2)+half_width*abs(axis[2])
            bottoms.append(center[2]-extent)
        self.env.data.qpos[2] = -min(bottoms)+.001
        self.env.data.qvel[0] = self.initial_velocity
        self.env.mujoco.mj_forward(self.env.model, self.env.data)
        self.base = self.env.mujoco.mj_name2id(self.env.model, self.env.mujoco.mjtObj.mjOBJ_BODY, 'base_link')
        self.wheels = [self.env.mujoco.mj_name2id(self.env.model, self.env.mujoco.mjtObj.mjOBJ_BODY, name)
                       for name in description.wheel_links]
        self.leg_ids = [self.env.mujoco.mj_name2id(self.env.model, self.env.mujoco.mjtObj.mjOBJ_JOINT,
                                                self.env.joint_names[i]) for i in LEGS]
        self.signs = np.sign([axes[f'joint_{side}_leg_4'][1] for side in ('left', 'right')])
        self.motor_state = np.zeros(2)
        self.truth_data = self.env.mujoco.MjData(self.env.model)
        self.estimator = WheelOdometry(description, parameters['equilibrium_pitch'])
        self.synchronized_estimator = WheelOdometry(description, parameters['equilibrium_pitch'])
        self.path = 0.
        self.previous_position, self.previous_yaw = None, None
        self.origin = None

    def truth(self):
        env = self.env
        # Refresh only a clone. Original mj_step sensor cache/timing stays unchanged.
        env.mujoco.mj_copyData(self.truth_data, env.model, env.data)
        env.mujoco.mj_forward(env.model, self.truth_data)
        return self.truth_data

    def instant(self, data):
        env = self.env
        pos = np.mean(data.xpos[self.wheels],axis=0)
        velocities = []
        for body in self.wheels:
            jacobian = np.zeros((3,env.model.nv))
            env.mujoco.mj_jac(env.model,data,jacobian,None,data.xpos[body],body)
            velocities.append(jacobian @ data.qvel)
        vel = np.mean(velocities,axis=0)
        rotation = Rotation.from_quat(data.qpos[3:7][[1, 2, 3, 0]])
        rpy = rotation.as_euler('xyz')
        angular = np.zeros(6)
        env.mujoco.mj_objectVelocity(env.model, data, env.mujoco.mjtObj.mjOBJ_BODY, self.base, angular, 0)
        body_angular = rotation.inv().apply(angular[:3])
        omega = body_angular[1]*np.cos(rpy[0])-body_angular[2]*np.sin(rpy[0])
        forward = np.array([np.cos(rpy[2]), np.sin(rpy[2]), 0.])
        return pos, vel, rpy, float(omega), forward

    def observe(self):
        data = self.truth()
        pos, vel, rpy, omega, forward = self.instant(data)
        if self.origin is None:
            self.origin = pos.copy()
        if self.previous_position is not None:
            yaw_delta = (rpy[2]-self.previous_yaw+np.pi) % (2*np.pi)-np.pi
            middle = self.previous_yaw+yaw_delta/2
            self.path += float((pos-self.previous_position) @ [np.cos(middle), np.sin(middle), 0.])
        self.previous_position, self.previous_yaw = pos.copy(), rpy[2]
        estimate = self.estimator.observe(sensors(self.env), self.dt)
        synchronized = self.synchronized_estimator.observe(Sensors(self.env.joint_pos(), self.env.joint_vel(),
            data.sensor('trunk_quat').data.copy(), data.sensor('trunk_gyro').data.copy()), self.dt)
        truth = np.array([self.path, vel @ forward, rpy[1]-self.parameters['equilibrium_pitch'], omega])
        return dict(sensor=estimate, synchronized=synchronized, gt=truth, position=pos,
                    velocity=vel, rpy=rpy, base_height=float(self.env.data.qpos[2]))

    def step(self, u):
        def override(q, dq, torque):
            torque[LEGS] = self.cfg['fixed_leg_kp']*(self.stand[LEGS]-q[LEGS])-self.cfg['fixed_leg_kd']*dq[LEGS]
            torque[WHEELS] = self.signs*u/2
            return torque

        def motor(torque):
            target = torque[WHEELS]*self.mismatch.get('motor_gain', 1.)
            lag = self.mismatch.get('motor_lag_s', 0.)
            if lag:
                self.motor_state += (1-np.exp(-self.env.model.opt.timestep/lag))*(target-self.motor_state)
            else:
                self.motor_state = target
            result = torque.copy()
            result[WHEELS] = np.clip(self.motor_state, -12., 12.)
            return result

        return self.playback.step(np.zeros(8, dtype=np.float32), override, motor)

    def failures(self, observation, state_source):
        x = observation[state_source]
        rpy = (Rotation.from_quat(self.env.base_quat_sensor()[[1, 2, 3, 0]]).as_euler('xyz')
               if state_source == 'sensor' else observation['rpy'])
        limits = self.env.model.jnt_range[self.leg_ids]
        q = self.env.joint_pos()[LEGS]
        violations = []
        if not np.isfinite(self.env.data.qpos).all() or not np.isfinite(self.env.data.qvel).all():
            violations.append('nonfinite_state')
        if abs(x[2]) > self.cfg['fall_pitch_rad']:
            violations.append('pitch_error_limit')
        if abs(rpy[0]) > self.cfg['fall_roll_rad']:
            violations.append('roll_limit')
        if observation['base_height'] < self.cfg['min_base_height_m']:
            violations.append('base_height_limit')
        for i, low, high in zip(LEGS, limits[:, 0], limits[:, 1]):
            value = self.env.joint_pos()[i]
            if value < low-.01 or value > high+.01:
                violations.append(f'joint_limit:{self.env.joint_names[i]}')
        margin = np.minimum(q-limits[:, 0], limits[:, 1]-q)
        return violations, margin


def restore_controller(parameters, cfg, training=None, online=False):
    c = WheelLQR(parameters, .02, 4, cfg['controller'], adaptive=online)
    if training is not None:
        d = training['final_diagnostics']
        c.K = np.asarray(d['K'])
        c.eigenvalues = np.asarray([d['spectral_radius']])
        c.rls.coefficients = np.asarray(d['coefficients']).reshape(2, 2)
        c.rls.P = np.asarray(d['covariance'])
        c.rls.bound_hits = d['bound_hits']
        if online:
            with np.load(ARCHIVE / training['trace']) as a:
                processed = ((len(a['time'])-1)//cfg['controller']['update_every'])*cfg['controller']['update_every']
                phi = np.column_stack((a['state'][:processed, 2],
                                       a['command_torque'][1:processed+1].sum(axis=1)))
                c.rls.regressors = deque(phi[-cfg['controller']['rls']['window']:].copy(),
                                         maxlen=cfg['controller']['rls']['window'])
    c.frozen = not online
    return c


def run_episode(policy, cfg, description, parameters, mismatch, seed, disturbance,
                label, source, output, training=None, adaptation=False, online=False):
    plant = Plant(policy, cfg, description, parameters, mismatch, seed, disturbance)
    c = restore_controller(parameters, cfg, training, online or adaptation)
    c.frozen = not (online or adaptation)
    if isinstance(training, WheelLQR):
        raise TypeError('Use a recorded diagnostics dictionary for an explicit gain source')
    rows = []
    duration = cfg['adaptation_s'] if adaptation else cfg['duration_s']
    observation = plant.observe()
    initial_physics = np.r_[plant.env.data.qpos, plant.env.data.qvel].copy()
    commands = np.zeros((4, 8))
    torques = commands.copy()
    pending_raw = 0.
    violations = []
    try:
        for tick in range(round(duration/.02)+1):
            t = tick*.02
            diag = c.diagnostics()
            violations, margin = plant.failures(observation, source)
            joint_pos = plant.env.joint_pos()
            snapshot = dict(time=t, control_state=observation[source].copy(),
                sensor_state=observation['sensor'].copy(), gt_state=observation['gt'].copy(),
                synchronized_state=observation['synchronized'].copy(), position=observation['position'].copy(),
                rpy=observation['rpy'].copy(), sensor_rpy=Rotation.from_quat(
                    plant.env.base_quat_sensor()[[1, 2, 3, 0]]).as_euler('xyz'),
                base_height=observation['base_height'], joint_position=joint_pos,
                joint_velocity=plant.env.joint_vel(), leg_limit_margin=margin,
                K=c.K.copy(), coefficients=c.rls.coefficients.reshape(4).copy(),
                covariance=c.rls.P.reshape(4).copy(), command=commands[:, WHEELS].copy(),
                motor=torques[:, WHEELS].copy(), raw_total_torque=pending_raw,
                saturation=c.saturated, accepted=c.accepted, rejected=c.rejected,
                nominal_error=c.nominal_error.copy(), adaptive_error=c.adaptive_error.copy(),
                confidence=diag['confidence'], reason=diag['reason'])
            rows.append(snapshot)
            if violations or tick == round(duration/.02):
                break
            plant.env.data.xfrc_applied[:] = 0.
            force = cfg['disturbance']
            if force['start_s'] <= t < force['start_s']+force['duration_s']:
                plant.env.data.xfrc_applied[plant.base, 0] = force['force_n']
            probing = (cfg['probing_nm']*sum(np.sin(2*np.pi*f*t) for f in cfg['probing_hz'])
                       /len(cfg['probing_hz'])) if adaptation else 0.
            x = observation[source]
            pending_raw = float(-c.K @ x+probing)
            u = c.command(x, probing)
            commands, torques = plant.step(u)
            following = plant.observe()
            c.transition(x, float(np.mean(commands[:, WHEELS] @ plant.signs)), following[source])
            observation = following
        trace = {k: np.asarray([r[k] for r in rows]) for k in rows[0]}
        identifier = f'{label}_{mismatch["name"]}_s{seed}_p{disturbance:+.3f}'
        np.savez_compressed(output / (identifier+'.npz'), **trace)
        disp = trace['position']-trace['position'][0]
        rms = lambda a: float(np.sqrt(np.mean(np.asarray(a)**2)))
        result = dict(execution_domain='VALIDATION_SIM', evidence_status='FAIL' if violations else 'PASS',
            checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'], label=label, state_source=source,
            mismatch=mismatch['name'], seed=seed, pitch_disturbance_rad=disturbance,
            completed_s=float(trace['time'][-1]), failures=violations, trace=identifier+'.npz',
            max_drift_m=float(np.max(np.linalg.norm(disp[:, :2], axis=1))),
            gt_pitch_rms_rad=rms(trace['gt_state'][:, 2]),
            sensor_gt_errors_rms=np.sqrt(np.mean((trace['sensor_state']-trace['gt_state'])**2, axis=0)).tolist(),
            peak_motor_nm=float(np.max(abs(trace['motor']))), saturation_ratio=float(np.mean(trace['saturation'])),
            accepted_updates=c.accepted, rejected_updates=c.rejected, final_diagnostics=c.diagnostics(),
            initial_physics=initial_physics.tolist(), applied_parameters=plant.applied,
            failure_snapshot={k: np.asarray(trace[k][-1]).tolist() for k in trace},
            pre_failure_window_s=.3)
        if violations:
            keys = ['time','raw_total_torque','base_height','saturation','accepted','rejected']
            with (output / (identifier+'_failure.csv')).open('w') as stream:
                writer = csv.writer(stream)
                writer.writerow(keys+['pitch','roll','v','p']+['K'+str(i) for i in range(4)]+['tau_left','tau_right','min_leg_limit_margin'])
                for i in np.flatnonzero(trace['time'] >= trace['time'][-1]-.3):
                    writer.writerow([trace[k][i] for k in keys]+[trace['control_state'][i,2],trace['rpy'][i,0],
                        trace['control_state'][i,1],trace['control_state'][i,0]]+trace['K'][i].tolist()+
                        trace['motor'][i].mean(0).tolist()+[float(trace['leg_limit_margin'][i].min())])
        return result
    finally:
        plant.env.close()


def archive_replay_error(result, original, output):
    if result['completed_s'] != original['completed_s'] or bool(result['failures']) != bool(original['failure']):
        return dict(evidence_status='FAIL', reason='terminal_behavior_differs')
    with np.load(output / result['trace']) as actual, np.load(ARCHIVE / original['trace']) as expected:
        keys = [('control_state','state'),('K','gain'),('motor','motor_substeps'),('coefficients','coefficients')]
        errors = {a: float(np.max(abs(actual[a]-expected[b]))) for a,b in keys}
        return dict(evidence_status='PASS' if max(errors.values()) < 1e-5 else 'FAIL', max_errors=errors)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--nominal-only', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(REPO / 'docs/exp') or output.exists():
        parser.error('Choose a new output directory under docs/exp/')
    output.mkdir(parents=True)
    manifest = json.loads((ARCHIVE / 'manifest.json').read_text())
    cfg = json.loads((ARCHIVE / 'config.json').read_text())
    policy = policy_config()
    assert policy['policy_interface']['checkpoint_sha256'] == manifest['checkpoint_sha256']
    source = read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description = Description(source['scene']['robot']['spawn']['asset_path'])
    parameters = manifest['nominal_parameters']
    archived = [json.loads(line) for line in (ARCHIVE / 'results.jsonl').read_text().splitlines()]
    lookup = {(r['mode'], r['mismatch'], r['seed'], r['pitch_delta_rad'], r['phase']): r for r in archived}
    write_json(output / 'manifest.json', dict(execution_domain='VALIDATION_SIM', evidence_status='NOT_TESTED',
        checkpoint_sha256=manifest['checkpoint_sha256'], onnx_sha256=manifest['onnx_sha256'],
        cfg=cfg, nominal_parameters=parameters, archive=str(ARCHIVE),
        script_sha256=sha256(Path(__file__)), ground_truth_scope='diagnostic counterfactual only',
        ground_truth_position='actual axle displacement projected on midpoint heading and cumulatively summed',
        refresh='mj_forward on cloned data only; original sensor timing preserved'))
    results = []
    started = time.monotonic()
    for mismatch in cfg['mismatches']:
        if args.nominal_only and mismatch['name'] != 'nominal':
            continue
        if args.quick and mismatch['name'] != 'nominal':
            continue
        for seed in cfg['seeds']:
            for disturbance in cfg['pitch_disturbances_rad']:
                if args.quick and (seed != 42 or disturbance != 0.):
                    continue
                training = lookup[('D-4', mismatch['name'], seed, disturbance, 'adaptation')]
                jobs = [('fixed_sensor','sensor',None,False,False,'C-4','evaluation'),
                        ('learned_sensor','sensor',training,False,False,'D-4','frozen'),
                        ('fixed_gt','gt',None,False,False,None,None),
                        ('learned_gt','gt',training,False,False,None,None),
                        ('online_sensor','sensor',training,False,True,'D-4','online'),
                        ('online_gt','gt',training,False,True,None,None),
                        ('adaptation_sensor','sensor',None,True,False,'D-4','adaptation'),
                        ('adaptation_gt','gt',None,True,False,None,None)]
                if mismatch['name'] == 'nominal':
                    jobs += [('fixed_synchronized','synchronized',None,False,False,None,None),
                             ('learned_synchronized','synchronized',training,False,False,None,None)]
                gt_training = None
                for label, state, loaded, adaptation, online, old_mode, old_phase in jobs:
                    result = run_episode(policy,cfg,description,parameters,mismatch,seed,disturbance,
                                         label,state,output,loaded,adaptation,online)
                    if old_mode:
                        result['archive_replay'] = archive_replay_error(result,
                            lookup[(old_mode,mismatch['name'],seed,disturbance,old_phase)],output)
                        if result['archive_replay']['evidence_status'] != 'PASS':
                            write_json(output / 'replay_failure.json',result)
                            raise RuntimeError('Archive reproduction gate failed')
                    if label == 'adaptation_gt':
                        gt_training = result
                    results.append(result)
                    with (output / 'results.jsonl').open('a') as stream:
                        stream.write(json.dumps(result,allow_nan=False)+'\n')
                    print(f'[VALIDATION_SIM] {label} {mismatch["name"]} s{seed} p{disturbance:+.3f} '
                          f'{result["evidence_status"]} {result["failures"]} t={result["completed_s"]:.2f} '
                          f'episodes={len(results)} elapsed={time.monotonic()-started:.1f}s',flush=True)
                result = run_episode(policy,cfg,description,parameters,mismatch,seed,disturbance,
                    'gt_trained_frozen','gt',output,gt_training)
                results.append(result)
                with (output / 'results.jsonl').open('a') as stream:
                    stream.write(json.dumps(result,allow_nan=False)+'\n')
    write_json(output / 'completion.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',
        checkpoint_sha256=manifest['checkpoint_sha256'],episodes=len(results),elapsed_s=time.monotonic()-started))


if __name__ == '__main__':
    main()
