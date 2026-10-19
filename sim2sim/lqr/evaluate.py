"""VALIDATION_SIM: paired stationary ablations, mismatch and adaptation phases.

Run from repository root: python -m sim2sim.lqr.evaluate --output docs/exp/YYYY-MM-DD/run
"""

import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
import time

import numpy as np
from scipy.spatial.transform import Rotation

from . import REPO
from .controller import WheelLQR
from .estimator import Sensors, WheelOdometry
from .model import Description
from .runtime import LEGS, WHEELS, Playback, policy_config
from sim2sim_ros2_jazzy.checkpoint import read_yaml, sha256

MODES = ('A', 'B', 'C-3', 'C-4', 'D-3', 'D-4')


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def sensors(env):
    return Sensors(env.joint_pos(), env.joint_vel(), env.base_quat_sensor(), env.base_ang_vel())


def setup_scene(playback, mismatch, description):
    env, model = playback.env, playback.env.model
    mj = env.mujoco
    floor = mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, 'floor')
    # Keep the reference model; disable only its world-attached obstacles for flat evaluation.
    obstacles = np.flatnonzero((model.geom_bodyid == 0) & (np.arange(model.ngeom) != floor))
    model.geom_contype[obstacles] = 0
    model.geom_conaffinity[obstacles] = 0
    body = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, 'base_link')
    wheel_bodies = [mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, name) for name in description.wheel_links]
    wheel_geoms = np.flatnonzero(np.isin(model.geom_bodyid, wheel_bodies)
                                & (model.geom_type == mj.mjtGeom.mjGEOM_CYLINDER))
    if len(wheel_geoms) != 2 or not np.allclose(model.geom_size[wheel_geoms, 0], description.radius):
        raise ValueError('Wheel collision radius mismatch')
    ids = np.asarray(env.actuator_ids)
    if (not np.allclose(model.actuator_gear[ids, 0], 1.)
            or not np.allclose(model.actuator_gainprm[ids, 0], 1.)
            or np.any(model.actuator_biastype[ids] != 0)
            or np.any(model.actuator_dyntype[ids] != 0)):
        raise ValueError('BLOCKED: expected direct unit-gear motor interface')
    if 'mass_scale' in mismatch:
        model.body_mass[body] *= mismatch['mass_scale']
        model.body_inertia[body] *= mismatch['mass_scale']
        model.body_ipos[body, 0] += mismatch['com_shift_m']
    if 'friction' in mismatch:
        model.geom_friction[np.r_[floor, wheel_geoms], 0] = mismatch['friction']
    mj.mj_setConst(model, env.data)
    env.reset()
    return dict(base_mass_kg=float(model.body_mass[body]), base_com_m=model.body_ipos[body].tolist(),
                wheel_geom_friction=model.geom_friction[wheel_geoms].tolist(),
                floor_friction=model.geom_friction[floor].tolist(),
                wheel_condim=model.geom_condim[wheel_geoms].tolist(), floor_condim=int(model.geom_condim[floor]),
                disabled_obstacles=obstacles.tolist(), motor_gain=mismatch.get('motor_gain', 1.),
                motor_lag_s=mismatch.get('motor_lag_s', 0.), physics_dt=float(model.opt.timestep),
                control_dt=env.control_dt, torque_limits=playback.adapter.limit.tolist())


def ground_truth(env, wheel_bodies):
    position = np.mean(env.data.xpos[wheel_bodies], axis=0)
    velocities = []
    for body in wheel_bodies:
        velocity = np.zeros(6)
        env.mujoco.mj_objectVelocity(env.model, env.data, env.mujoco.mjtObj.mjOBJ_BODY, body, velocity, 0)
        velocities.append(velocity[3:])
    return position, np.mean(velocities, axis=0)


def summarize(trace, cfg, failed, dt, requested_duration):
    a = trace
    rms = lambda x: float(np.sqrt(np.mean(np.asarray(x)**2)))
    pitch, velocity = a['state'][:, 2], a['gt_forward_velocity']
    position = a['gt_position'] - a['gt_position'][0]
    dwell = max(1, round(cfg['settle_dwell_s']/dt))
    stable = (abs(pitch) < cfg['settle_pitch_rad']) & (abs(velocity) < cfg['settle_velocity_m_s'])
    settled = np.convolve(stable.astype(int), np.ones(dwell, dtype=int), mode='valid') if len(stable) >= dwell else []
    candidates = np.flatnonzero(np.asarray(settled) == dwell)
    settling_time = float(candidates[0]*dt) if len(candidates) and not failed else None
    norms = np.linalg.norm(position[:, :2], axis=1)
    return dict(evidence_status='FAIL' if failed else 'PASS', failure=failed,
                completed_s=float((len(pitch)-1)*dt), requested_s=requested_duration,
                final_displacement_m=float(position[-1, 0]), final_planar_displacement_m=float(norms[-1]),
                max_displacement_m=float(max(norms)), position_rms_m=rms(norms),
                pitch_rms_rad=rms(pitch), peak_pitch_rad=float(max(abs(pitch))),
                pitch_rate_rms_rad_s=rms(a['state'][:, 3]), settling_time_s=settling_time,
                torque_rms_nm=rms(a['motor_substeps']), peak_torque_nm=float(np.max(abs(a['motor_substeps']))),
                saturation_ratio=float(np.mean(a['saturation'])),
                command_variation_nm=float(np.sum(abs(np.diff(a['command_torque'], axis=0)))),
                odometry_error_rms_m=rms(a['state'][:, 0]-a['gt_forward_distance']),
                velocity_error_rms_m_s=rms(a['state'][:, 1]-velocity),
                leg_error_rms_rad=rms(a['leg_error']), leg_velocity_rms_rad_s=rms(a['leg_velocity']),
                com_change_max_m=float(np.max(np.linalg.norm(a['com_body']-a['com_body'][0], axis=1))),
                nominal_prediction_rms=rms(a['prediction_error'][:, :2]),
                adaptive_prediction_rms=rms(a['prediction_error'][:, 2:]),
                nominal_velocity_prediction_rms_m_s=rms(a['prediction_error'][:, 0]),
                nominal_rate_prediction_rms_rad_s=rms(a['prediction_error'][:, 1]),
                adaptive_velocity_prediction_rms_m_s=rms(a['prediction_error'][:, 2]),
                adaptive_rate_prediction_rms_rad_s=rms(a['prediction_error'][:, 3]),
                confidence_ratio=float(np.mean(a['confidence'])),
                accepted_gain_updates=int(a['updates'][-1, 0]), rejected_gain_updates=int(a['updates'][-1, 1]),
                excitation_rank=int(a['rank'][-1]), bound_hits=int(a['bound_hits'][-1]),
                peak_slip_velocity_m_s=float(np.max(abs(a['state'][:, 1]-velocity))),
                max_yaw_change_rad=float(np.max(abs(np.unwrap(a['rpy'][:, 2])-a['rpy'][0, 2]))))


def episode(policy_cfg, cfg, description, parameters, mode, mismatch, seed, pitch_delta,
            output, phase='evaluation', learned=None, shadow=False):
    playback = Playback(policy_cfg)
    env, mj = playback.env, playback.env.mujoco
    dt = env.control_dt
    applied = setup_scene(playback, mismatch, description)
    rng = np.random.default_rng(seed)
    initial_velocity = cfg['initial_velocity_m_s'] + rng.uniform(-cfg['initial_velocity_jitter_m_s'], cfg['initial_velocity_jitter_m_s'])
    pitch = parameters['equilibrium_pitch'] + pitch_delta
    rotation = Rotation.from_euler('xyz', [parameters['equilibrium_roll'], pitch, 0.])
    env.data.qpos[3:7] = rotation.as_quat()[[3, 0, 1, 2]]
    frames, axes = description.frames(policy_cfg['robot']['default_joint_angles'])
    bottoms = []
    for name, joint in zip(description.wheel_links, ('joint_left_leg_4', 'joint_right_leg_4')):
        center = rotation.apply(frames[name][:3, 3])
        axis = rotation.apply(axes[joint])
        cylinder = description.links[name].find('collision/geometry/cylinder')
        half_width = float(cylinder.get('length'))/2
        vertical_radius = description.radius*np.sqrt(1-axis[2]**2)+half_width*abs(axis[2])
        bottoms.append(center[2]-vertical_radius)
    env.data.qpos[2] = -min(bottoms)+.001
    env.data.qvel[0] = initial_velocity
    mj.mj_forward(env.model, env.data)
    estimator = WheelOdometry(description, parameters['equilibrium_pitch'])
    x = estimator.observe(sensors(env), dt)
    lqr = None
    if mode not in ('A', 'B'):
        dimension = int(mode[-1])
        lqr = WheelLQR(parameters, dt, dimension, cfg['controller'], adaptive=mode.startswith('D'), shadow=shadow)
        if learned is not None:
            lqr.K = learned.K.copy()
            lqr.eigenvalues = learned.eigenvalues.copy()
            lqr.rls.coefficients = learned.rls.coefficients.copy()
            lqr.rls.P = learned.rls.P.copy()
            lqr.rls.regressors = copy.deepcopy(learned.rls.regressors)
            lqr.rls.bound_hits = learned.rls.bound_hits
            lqr.frozen = phase == 'frozen'
    wheel_bodies = [mj.mj_name2id(env.model, mj.mjtObj.mjOBJ_BODY, name) for name in description.wheel_links]
    _, axes = description.frames(policy_cfg['robot']['default_joint_angles'])
    signs = np.sign([axes[f'joint_{side}_leg_4'][1] for side in ('left', 'right')])
    if np.any(signs == 0):
        raise ValueError('Ambiguous wheel sign')
    base = mj.mj_name2id(env.model, mj.mjtObj.mjOBJ_BODY, 'base_link')
    stand = np.asarray(policy_cfg['robot']['default_joint_angles'])
    kp, kd = cfg['fixed_leg_kp'], cfg['fixed_leg_kd']
    motor_state = np.zeros(2)
    failure = ''
    duration = cfg['adaptation_s'] if phase in ('adaptation', 'shadow') else cfg['duration_s']
    rows = []
    reasons = []
    last_commands = np.zeros((env.decimation, 8))
    last_torques = last_commands.copy()
    forward_distance, previous_forward_velocity = 0., None

    def motor(torque):
        nonlocal motor_state
        target = torque[WHEELS]*mismatch.get('motor_gain', 1.)
        lag = mismatch.get('motor_lag_s', 0.)
        if lag:
            motor_state += (1-np.exp(-env.model.opt.timestep/lag))*(target-motor_state)
        else:
            motor_state = target
        result = torque.copy()
        result[WHEELS] = np.clip(motor_state, -playback.adapter.limit[WHEELS], playback.adapter.limit[WHEELS])
        return result

    try:
        for step in range(round(duration/dt)+1):
            t = step*dt
            pos, vel = ground_truth(env, wheel_bodies)
            rpy = Rotation.from_quat(env.base_quat_sensor()[[1, 2, 3, 0]]).as_euler('xyz')
            forward_velocity = float(vel @ np.array([np.cos(rpy[2]), np.sin(rpy[2]), 0.]))
            if previous_forward_velocity is not None:
                forward_distance += dt*(previous_forward_velocity+forward_velocity)/2
            previous_forward_velocity = forward_velocity
            # Evaluation-only CoM in body frame; never sent to controller or RLS.
            body_ids = np.setdiff1d(np.arange(1, env.model.nbody), wheel_bodies)
            masses = env.model.body_mass[body_ids]
            com = np.average(env.data.xipos[body_ids], axis=0, weights=masses)
            com_body = env.data.xmat[base].reshape(3, 3).T @ (com-env.data.xpos[base])
            diag = lqr.diagnostics() if lqr else dict(coefficients=[0.]*4, covariance=np.zeros((2, 2)).tolist(),
                singular_values=[0., 0.], rank=0, confidence=False, K=[0.]*4, accepted=0, rejected=0,
                nominal_error=[0., 0.], adaptive_error=[0., 0.], saturated=False, bound_hits=0, reason='FlashSAC')
            rows.append(dict(time=t, state=x.copy(), gt_position=pos, gt_velocity=vel,
                             gt_forward_velocity=forward_velocity, gt_forward_distance=forward_distance, rpy=rpy,
                             command_torque=np.mean(last_commands[:, WHEELS], axis=0),
                             motor_torque=np.mean(last_torques[:, WHEELS], axis=0),
                             motor_substeps=last_torques[:, WHEELS].copy(),
                             coefficients=diag['coefficients'], covariance=np.asarray(diag['covariance']).reshape(4),
                             singular_values=diag['singular_values'], rank=diag['rank'], confidence=diag['confidence'],
                             gain=np.pad(diag['K'], (4-len(diag['K']), 0)),
                             updates=[diag['accepted'], diag['rejected']], bound_hits=diag['bound_hits'],
                             prediction_error=diag['nominal_error']+diag['adaptive_error'],
                             saturation=diag['saturated'] or np.any(abs(last_torques[:, WHEELS]) >= playback.adapter.limit[WHEELS]-1e-6),
                             leg_error=env.joint_pos()[LEGS]-stand[LEGS], leg_velocity=env.joint_vel()[LEGS],
                             com_body=com_body))
            reasons.append(diag['reason'])
            joint_ids = [mj.mj_name2id(env.model, mj.mjtObj.mjOBJ_JOINT, env.joint_names[i]) for i in LEGS]
            limits = env.model.jnt_range[joint_ids]
            q = env.joint_pos()[LEGS]
            if not np.isfinite(env.data.qpos).all() or not np.isfinite(env.data.qvel).all():
                failure = 'nonfinite_state'
            elif abs(x[2]) > cfg['fall_pitch_rad'] or abs(rpy[0]) > cfg['fall_roll_rad'] or env.base_pos()[2] < cfg['min_base_height_m']:
                failure = 'fall_or_attitude_limit'
            elif np.any(q < limits[:, 0]-.01) or np.any(q > limits[:, 1]+.01):
                failure = 'joint_limit'
            if failure or step == round(duration/dt):
                break
            disturbance = cfg['disturbance']
            env.data.xfrc_applied[:] = 0.
            if disturbance['start_s'] <= t < disturbance['start_s']+disturbance['duration_s']:
                env.data.xfrc_applied[base, 0] = disturbance['force_n']
            probing = 0.
            if phase in ('adaptation', 'shadow'):
                probing = cfg['probing_nm']*sum(np.sin(2*np.pi*f*t) for f in cfg['probing_hz'])/len(cfg['probing_hz'])
            action = np.zeros(8, dtype=np.float32)
            if mode in ('A', 'B'):
                _, action = playback.infer()
            u = lqr.command(x, probing) if lqr else 0.

            def override(q, dq, torque):
                if mode == 'A':
                    return torque
                torque[LEGS] = kp*(stand[LEGS]-q[LEGS])-kd*dq[LEGS]
                if lqr:
                    torque[WHEELS] = signs*u/2
                return torque

            last_commands, last_torques = playback.step(action, override, motor)
            following = estimator.observe(sensors(env), dt)
            if lqr:
                commanded = float(np.mean(last_commands[:, WHEELS] @ signs))
                lqr.transition(x, commanded, following)
            x = following
        trace = {key: np.asarray([row[key] for row in rows]) for key in rows[0]}
        identifier = f'{mode}_{mismatch["name"]}_s{seed}_p{pitch_delta:+.3f}_{phase}'
        np.savez_compressed(output / (identifier+'.npz'), **trace, reasons=np.asarray(reasons))
        result = dict(execution_domain='VALIDATION_SIM', checkpoint_sha256=policy_cfg['policy_interface']['checkpoint_sha256'],
                      mode=mode, mismatch=mismatch['name'], seed=seed, pitch_delta_rad=pitch_delta,
                      initial_velocity_m_s=initial_velocity, phase=phase, trace=identifier+'.npz',
                      applied_parameters=applied, **summarize(trace, cfg, failure, dt, duration))
        if lqr:
            result['final_diagnostics'] = lqr.diagnostics()
        return result, lqr
    finally:
        env.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path(__file__).with_name('config.json'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--stage', choices=['fixed', 'shadow', 'full'], default='full')
    parser.add_argument('--nominal-only', action='store_true')
    parser.add_argument('--quick', action='store_true', help='One seed, one pitch; development gate only')
    parser.add_argument('--shadow-evidence', type=Path, help='Validated shadow results.jsonl required for full stage')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(REPO / 'docs/exp'):
        parser.error('All evaluation evidence must be inside docs/exp/')
    if output.exists() and any(output.iterdir()):
        parser.error('Choose a new output directory to preserve existing evidence')
    output.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(args.config.read_text())
    if args.quick:
        cfg.update(seeds=[42], pitch_disturbances_rad=[.035])
    if args.nominal_only:
        cfg['mismatches'] = cfg['mismatches'][:1]
    policy_cfg = policy_config()
    gate = REPO / 'docs/exp/2026-10-14/lqr_ablation/baseline_gate.json'
    evidence = json.loads(gate.read_text())
    if (evidence['evidence_status'] != 'PASS'
            or evidence['checkpoint_sha256'] != policy_cfg['policy_interface']['checkpoint_sha256']
            or evidence['onnx_sha256'] != policy_cfg['policy_interface']['onnx_sha256']):
        raise RuntimeError('BLOCKED: designated checkpoint baseline parity gate is not satisfied')
    if args.stage == 'full':
        if args.shadow_evidence is None:
            parser.error('Full adaptive evaluation requires --shadow-evidence from the shadow stage')
        shadow_results = [json.loads(line) for line in args.shadow_evidence.read_text().splitlines()]
        shadow_cfg = json.loads(args.shadow_evidence.with_name('config.json').read_text())
        for key in ('controller', 'fixed_leg_kp', 'fixed_leg_kd'):
            if shadow_cfg[key] != cfg[key]:
                raise RuntimeError('BLOCKED: shadow configuration differs from final controller')
        for mode in ('C-3', 'C-4'):
            valid = []
            for r in shadow_results:
                if (r['mode'] == mode and not r['failure']
                        and r['final_diagnostics']['confidence']
                        and r['adaptive_prediction_rms'] < r['nominal_prediction_rms']):
                    with np.load(args.shadow_evidence.parent / r['trace']) as trace:
                        if np.any(trace['reasons'] == 'shadow_valid'):
                            valid.append(r)
            if not valid:
                raise RuntimeError(f'BLOCKED: {mode} shadow identification/gain validation not established')
    source = read_yaml(next(p for p in policy_cfg['policy_interface']['sources'] if p.endswith('env.yaml')))
    urdf = Path(source['scene']['robot']['spawn']['asset_path'])
    description = Description(urdf)
    parameters = description.nominal(policy_cfg['robot']['default_joint_angles'])
    write_json(output / 'config.json', cfg)
    write_json(output / 'manifest.json', dict(execution_domain='VALIDATION_SIM', evidence_status='NOT_TESTED',
        checkpoint_sha256=policy_cfg['policy_interface']['checkpoint_sha256'],
        onnx_sha256=policy_cfg['policy_interface']['onnx_sha256'], policy_config=policy_cfg,
        nominal_parameters=parameters, nominal_urdf=str(urdf), nominal_urdf_sha256=sha256(urdf),
        source_sha256={p.name: sha256(p) for p in Path(__file__).parent.glob('*.py')},
        stage=args.stage, baseline_gate_sha256=sha256(gate)))
    results = []
    started = time.monotonic()
    for mismatch in cfg['mismatches']:
        for seed in cfg['seeds']:
            for pitch in cfg['pitch_disturbances_rad']:
                modes = ('C-3', 'C-4') if args.stage == 'shadow' else MODES[:4] if args.stage == 'fixed' else MODES
                for mode in modes:
                    if mode.startswith('D'):
                        training, learned = episode(policy_cfg, cfg, description, parameters, mode,
                                                    mismatch, seed, pitch, output, 'adaptation')
                        results.append(training)
                        # Failed training never qualifies as a successful learned-gain trial.
                        result, _ = episode(policy_cfg, cfg, description, parameters, mode,
                                            mismatch, seed, pitch, output, 'frozen', learned)
                        result['adaptation_episode_status'] = training['evidence_status']
                        result['adaptation_gain_accepted'] = learned.accepted
                        result['adaptation_confident'] = learned.rls.diagnostics()['confidence']
                        results.append(result)
                        result, _ = episode(policy_cfg, cfg, description, parameters, mode,
                                            mismatch, seed, pitch, output, 'online', learned)
                        results.append(result)
                    else:
                        result, _ = episode(policy_cfg, cfg, description, parameters, mode,
                                            mismatch, seed, pitch, output,
                                            'shadow' if args.stage == 'shadow' else 'evaluation', shadow=args.stage == 'shadow')
                        results.append(result)
                    with (output / 'results.jsonl').open('a') as stream:
                        for item in results:
                            if not item.get('_written'):
                                stream.write(json.dumps(item, allow_nan=False)+'\n')
                                item['_written'] = True
                    print(f'[VALIDATION_SIM] {mode} {mismatch["name"]} seed={seed} pitch={pitch:+.3f} '
                          f'{result["evidence_status"]} drift={result["final_displacement_m"]:.4f} '
                          f'episodes={len(results)} elapsed={time.monotonic()-started:.1f}s', flush=True)
    fields = [key for key, value in results[0].items() if not isinstance(value, (dict, list)) and key != '_written']
    with (output / 'metrics.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)
    print(f'[VALIDATION_SIM] Completed {len(results)} episodes: {output}', flush=True)


if __name__ == '__main__':
    main()
