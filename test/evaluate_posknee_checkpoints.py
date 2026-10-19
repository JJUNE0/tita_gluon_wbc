"""VALIDATION_SIM: checkpoint screening with production MuJoCo/observation/MA2/PD code.

No robot SDK, ROS node, physical commands or training process is used. All outputs
are saved in the caller's docs/exp/YYYY-MM-DD/ directory. Run --prepare using the
Isaac/Torch interpreter, then --evaluate using the MuJoCo interpreter.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import copy
import csv
import hashlib
import json
import os
from pathlib import Path
import sys
import time

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'sim2sim/sim2sim_ros2_jazzy'))
from sim2sim_ros2_jazzy.adapter import (
    ActionAdapter, LegActionFilter, ObservationBuilder, ObsState,
    NATIVE_JOINTS, quat_wxyz_to_rotmat, quat_wxyz_to_rpy,
)
from sim2sim_ros2_jazzy.checkpoint import describe_checkpoint, prepared_config, sha256
from sim2sim_ros2_jazzy.mujoco_env import TitaMujocoEnv
from sim2sim_ros2_jazzy.state_machine import StateMachine, SPLAY_POSE

RUN = REPO / 'lab/ddt_lab/logs/flash_sac/tita_flash_sac_180212_290240'
STEPS = list(range(40000, 85001, 5000))
SEEDS = [42, 104, 270]
KNEE_SCALES = [1., .75, .55]
LEGS = [0, 1, 2, 4, 5, 6]
WHEELS = [3, 7]
DT = .02
# Command ramps are identical to the public sim2sim keyboard (0.5 units/s).
DRIVE = [(0., 0., 0.), (8., .6, 0.), (14., 0., 0.), (20., -.6, 0.),
    (26., 0., 0.), (32., 0., 1.), (38., 0., 0.), (44., 0., -1.),
    (50., 0., 0.), (56., 1., 0.), (62., 0., 0.), (68., -1., 0.),
    (74., 0., 0.), (80., 0., 1.5), (86., 0., 0.), (92., 0., -1.5), (98., 0., 0.)]
SCENARIOS = {'stand': {'duration': 32., 'schedule': [(0., 0., 0.)]},
             'drive': {'duration': 106., 'schedule': DRIVE}}


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def protocol():
    return dict(execution_domain='VALIDATION_SIM', run=str(RUN.relative_to(REPO)),
        checkpoints=STEPS, seeds=SEEDS, knee_pd_scales=KNEE_SCALES,
        scenarios=SCENARIOS, control_dt_s=DT,
        physics='Public sim2sim robot XML, timestep and initial splay/state machine; '
                'world-body obstacle boxes have collision disabled for a flat-ground policy comparison. '
                'Knee sensitivity scales only RL Kp and Kd BEFORE torque clipping; effort limits unchanged. '
                'No added friction, delay, sensor noise, CoM shift, residual control or DR.',
        initialization='Per-seed initial base vx uniform +/-0.015 m/s; leg velocity N(0,0.01 rad/s); same samples for all checkpoints.',
        settled_stand_window_s=[8., 32.], stop_windows='last 3 s of each stop interval after a manoeuvre',
        pitch_reference_deg=0., torque='Clipped PD torque at every physics substep; no hardware torque measurement.',
        failure='Nonfinite state, tilt >0.65 rad, base-floor collision, inference failure or missing duration.',
        selection='Prefer zero failed rollouts. Compare worst-domain mean settled zero-command RMS planar speed '
                  '(stand and post-move stops equally weighted), then zero-command pitch RMS and leg torque RMS. '
                  'Report nominal and sensitivity metrics separately; selection is sim-only.',
        ground_truth='Base position/velocity used for metrics only; 34 policy inputs use encoders/IMU/commands/raw last_action.')


def stats(a):
    a = np.asarray(a)
    return dict(mean=np.mean(a, axis=0).tolist(), std=np.std(a, axis=0).tolist(),
        rms=np.sqrt(np.mean(a*a, axis=0)).tolist(), min=np.min(a, axis=0).tolist(),
        max=np.max(a, axis=0).tolist(), abs_peak=np.max(np.abs(a), axis=0).tolist())


def intervals(mask):
    idx = np.flatnonzero(mask)
    return [v for v in np.split(idx, np.flatnonzero(np.diff(idx) > 1)+1) if len(v)]


def metrics(signals, cfg, scenario):
    s = signals
    t = s['t']
    settled = t >= 8.
    zero = np.max(np.abs(s['command']), axis=1) < 1e-7
    stops = np.zeros(len(t), dtype=bool)
    stop_rows = []
    if scenario == 'drive':
        for block in intervals(zero):
            if t[block[0]] < 8.:
                continue
            tail = block[t[block] >= t[block[-1]]-3.+DT/2]
            stops[tail] = True
            first, last = block[0], block[-1]
            stop_rows.append(dict(start_s=float(t[first]), end_s=float(t[last]),
                displacement_m=(s['position'][last]-s['position'][first]).tolist(),
                settled_speed_rms_m_s=float(np.sqrt(np.mean(s['planar_speed'][tail]**2))),
                settled_pitch_rms_deg=float(np.sqrt(np.mean(s['rpy_deg'][tail, 1]**2)))))
    measure = settled if scenario == 'stand' else stops
    assert np.any(measure), 'No completed measurement window'
    pitch = s['rpy_deg'][:, 1]
    pos = s['position'][measure]
    measured_t = t[measure]
    if scenario == 'stand':
        slope = np.polyfit(measured_t-measured_t[0], pos[:, 0]-pos[0, 0], 1)[0]
        displacement = pos[-1]-pos[0]
    else:
        slope, displacement = None, None
    torque = s['torque'][measure].reshape(-1, 8)
    limits = np.array(cfg['robot']['torque_limit'])
    max_phase = s['torque'].reshape(-1, 8)
    # Torque-step proxy is a difference of phase means, not a real 25 Hz test.
    mean_tick_torque = s['torque'].mean(axis=1)
    delta = np.diff(mean_tick_torque, axis=0)
    delta_mask = measure[1:] & measure[:-1]
    out = dict(samples=int(measure.sum()), duration_measured_s=float(measure.sum()*DT),
        zero_speed_rms_m_s=float(np.sqrt(np.mean(s['planar_speed'][measure]**2))),
        zero_vx_mean_m_s=float(np.mean(s['velocity_body'][measure, 0])),
        drift_slope_x_m_s=None if slope is None else float(slope),
        displacement_m=None if displacement is None else displacement.tolist(),
        max_planar_displacement_m=None if scenario != 'stand' else float(np.max(np.linalg.norm(pos[:, :2]-pos[0, :2], axis=1))),
        pitch_deg=stats(pitch[measure]), startup_pitch_abs_peak_deg=float(np.max(np.abs(pitch[t<8.]))),
        pitch_full_abs_peak_deg=float(np.max(np.abs(pitch))),
        joint_angle_rad=stats(s['q'][measure]), joint_angle_deg=stats(np.degrees(s['q'][measure])),
        torque_nm=stats(torque), torque_full_nm=stats(max_phase),
        torque_saturation_fraction=np.mean(np.abs(torque) >= limits-1e-4, axis=0).tolist(),
        leg_torque_rms_nm=float(np.sqrt(np.mean(torque[:, LEGS]**2))),
        wheel_torque_rms_nm=float(np.sqrt(np.mean(torque[:, WHEELS]**2))),
        leg_torque_step_rms_nm=float(np.sqrt(np.mean(delta[delta_mask][:, LEGS]**2))),
        position_error_obs_m=stats(s['position_error_m'][measure]), stops=stop_rows)
    if scenario == 'drive':
        tracking = []
        for i, (start, x, yaw) in enumerate(DRIVE):
            if x == 0 and yaw == 0:
                continue
            end = DRIVE[i+1][0]
            mask = (t >= end-2.) & (t < end)
            tracking.append(dict(target_vx=x, target_yaw=yaw, window_s=[end-2., end],
                vx_rmse_m_s=float(np.sqrt(np.mean((s['velocity_body'][mask, 0]-s['command'][mask, 0])**2))),
                yaw_rmse_rad_s=float(np.sqrt(np.mean((s['gyro'][mask, 2]-s['command'][mask, 2])**2))),
                pitch_rms_deg=float(np.sqrt(np.mean(pitch[mask]**2))),
                vx_mean_m_s=float(np.mean(s['velocity_body'][mask, 0])),
                yaw_mean_rad_s=float(np.mean(s['gyro'][mask, 2]))))
        out['tracking'] = tracking
    return out


def rollout(job):
    import onnxruntime as ort
    step, seed, scale, scenario = job['step'], job['seed'], job['scale'], job['scenario']
    label = f'model_{step}_k{scale:g}_{scenario}_s{seed}'
    config = Path(job['config'])
    cfg = json.loads(config.read_text())
    assert cfg['policy']['obs_dim'] == 34 and cfg['policy_interface']['leg_action_filter'] == 'ma2_legs'
    assert not any(term['kind'] == 'lin_vel' for term in cfg['policy_interface']['observations'])
    assert sha256(cfg['policy']['path']) == cfg['policy_interface']['onnx_sha256']
    assert abs(cfg['control']['sim_timestep']*cfg['control']['decimation']-DT) < 1e-9
    options = ort.SessionOptions()
    options.intra_op_num_threads = options.inter_op_num_threads = 1
    policy = ort.InferenceSession(cfg['policy']['path'], sess_options=options, providers=['CPUExecutionProvider'])
    runtime_cfg = copy.deepcopy(cfg)
    for key in ('joint_kp', 'joint_kd'):
        for joint in (2, 6):
            runtime_cfg['robot'][key][joint] *= scale
    env = TitaMujocoEnv(cfg)
    floor = env.model.geom('floor').id
    base_body = env.model.body('base_link').id
    obstacles = np.flatnonzero((env.model.geom_bodyid == 0) & (np.arange(env.model.ngeom) != floor))
    env.model.geom_contype[obstacles] = env.model.geom_conaffinity[obstacles] = 0
    adapter = ActionAdapter(runtime_cfg)
    builder = ObservationBuilder(cfg)
    filter_ = LegActionFilter(cfg['policy_interface']['leg_action_filter'], adapter.order)
    sm = StateMachine(cfg['robot']['torque_limit'], auto_rl=True)
    env.reset(SPLAY_POSE)
    rng = np.random.default_rng(seed)
    env.data.qvel[0] = rng.uniform(-.015, .015)
    env.data.qvel[env.qvel_addr[LEGS]] = rng.normal(0, .01, 6)
    env.mujoco.mj_forward(env.model, env.data)
    sm.request('transform_up', env.joint_pos())
    duration = SCENARIOS[scenario]['duration']
    schedule = SCENARIOS[scenario]['schedule']
    command = np.zeros(3, dtype=np.float32)
    last = np.zeros(8, dtype=np.float32)
    rows = {key: [] for key in ('t', 'q', 'dq', 'rpy_deg', 'position', 'velocity_body', 'planar_speed',
        'gyro', 'command', 'raw_action', 'applied_action', 'torque', 'position_error_m')}
    failure = None
    rl_tick = 0
    was_rl = False
    try:
        for _ in range(round((duration+5.)/DT)):
            sm.update(DT)
            if sm.state != 'rl':
                last[:] = 0.; filter_.reset(); builder.reset()
                env.step_with_torque_callback(sm.torque)
                continue
            if not was_rl:
                builder.reset()
            was_rl = True
            t = round(rl_tick*DT, 8)
            if t >= duration:
                break
            target = schedule[0]
            for entry in schedule:
                if t >= entry[0]:
                    target = entry
            command += np.clip(np.array([target[1], 0., target[2]])-command, -.5*DT, .5*DT)
            quat = env.base_quat_sensor()
            rpy = quat_wxyz_to_rpy(quat)
            rot = quat_wxyz_to_rotmat(quat)
            q, dq = env.joint_pos(), env.joint_vel()
            position = env.base_pos()
            tilt = np.arccos(np.clip(rot[2, 2], -1., 1.))
            base_contact = any(contact.dist < 0 and (
                (env.model.geom_bodyid[contact.geom1] == base_body and contact.geom2 == floor)
                or (env.model.geom_bodyid[contact.geom2] == base_body and contact.geom1 == floor))
                for contact in env.data.contact)
            if tilt > .65 or base_contact:
                failure = dict(kind='fall', t_rl_s=t, tilt_deg=float(np.degrees(tilt)),
                    height_m=float(position[2]), base_floor_contact=base_contact)
                break
            gyro = env.base_ang_vel()
            # Ground truth velocity is for metrics only; the policy has no lin_vel term.
            velocity = rot.T @ env.base_lin_vel()
            state = ObsState(q, dq, quat, gyro, command, last)
            obs = builder.build(state)
            raw = policy.run(['nn_output'], {'nn_input0': obs.reshape(1, -1)})[0].reshape(8)
            applied = filter_.update(raw)
            phase_torques = []
            def torque_callback(positions, velocities):
                torque = adapter.compute(applied, positions, velocities)
                phase_torques.append(torque.copy())
                return torque
            env.step_with_torque_callback(torque_callback)
            if not np.isfinite(env.data.qpos).all() or not np.isfinite(env.data.qvel).all():
                raise ValueError('Nonfinite physics state')
            values = [t, q, dq, np.degrees(rpy), position, velocity, float(np.linalg.norm(velocity[:2])),
                gyro, command.copy(), raw.copy(), applied.copy(), np.array(phase_torques), float(obs[-1]/5.)]
            for key, value in zip(rows, values):
                rows[key].append(value)
            last = raw.copy()
            rl_tick += 1
    except Exception as error:
        failure = dict(kind=type(error).__name__, detail=str(error), t_rl_s=rl_tick*DT)
    finally:
        env.close()
    signals = {key: np.asarray(value) for key, value in rows.items()}
    signal_path = Path(job['output']) / 'signals' / f'{label}.npz'
    np.savez_compressed(signal_path, **signals)
    result = dict(execution_domain='VALIDATION_SIM', job=label, step=step, seed=seed,
        knee_scale=scale, scenario=scenario, evidence_status='FAIL' if failure else 'PASS', failure=failure,
        rl_steps=rl_tick, checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
        onnx_sha256=cfg['policy_interface']['onnx_sha256'], signal_file=str(signal_path.relative_to(REPO)))
    if not failure and rl_tick != round(duration/DT):
        result.update(evidence_status='FAIL', failure={'kind': 'incomplete_duration'})
    if result['evidence_status'] == 'PASS':
        result['metrics'] = metrics(signals, cfg, scenario)
    return result


def prepare(output):
    from sim2sim_ros2_jazzy.checkpoint import prepare_checkpoint
    manifests = []
    for step in STEPS:
        checkpoint = RUN / f'model_{step}'
        config = prepared_config(checkpoint)
        if config is None:
            config = prepare_checkpoint(checkpoint, Path.home() / 'venvs/cosim_ros2_jazzy/bin/python')
        cfg = json.loads(config.read_text())
        manifests.append(dict(step=step, config=str(config), checkpoint_sha256=cfg['policy_interface']['checkpoint_sha256'],
            onnx_sha256=cfg['policy_interface']['onnx_sha256'], config_sha256=sha256(config),
            parity=json.loads((config.parent/'manifest.json').read_text())['parity']))
        print(f'[VALIDATION_SIM] Prepared {step}: {manifests[-1]["parity"]}', flush=True)
    write_json(output/'policies.json', manifests)


def evaluate(output, workers):
    fixed = protocol()
    path = output/'evaluation_protocol.json'
    if path.exists() and json.loads(path.read_text()) != json.loads(json.dumps(fixed)):
        raise ValueError('Refusing to overwrite a different fixed evaluation protocol')
    write_json(path, fixed)
    policies = json.loads((output/'policies.json').read_text())
    (output/'signals').mkdir(exist_ok=True)
    jobs = [dict(step=p['step'], config=p['config'], output=str(output), seed=seed, scale=scale, scenario=scenario)
        for p in policies for seed in SEEDS for scale in KNEE_SCALES for scenario in SCENARIOS]
    began = time.monotonic()
    results = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(rollout, job): job for job in jobs}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            write_json(output/'results_partial.json', results)
            print(f'[VALIDATION_SIM] {len(results)}/{len(jobs)} {result["job"]} '
                f'{result["evidence_status"]} elapsed={time.monotonic()-began:.1f}s', flush=True)
    write_json(output/'results.json', sorted(results, key=lambda r:(r['step'],r['knee_scale'],r['scenario'],r['seed'])))
    summarize(output)


def summarize(output):
    results = json.loads((output/'results.json').read_text())
    summary, rows = {}, []
    for step in STEPS:
        by_domain = {}
        for scale in KNEE_SCALES:
            all_rows = [r for r in results if r['step']==step and r['knee_scale']==scale]
            valid = [r for r in all_rows if r['evidence_status']=='PASS']
            stand = [r['metrics'] for r in valid if r['scenario']=='stand']
            drive = [r['metrics'] for r in valid if r['scenario']=='drive']
            if len(valid) != len(SEEDS)*len(SCENARIOS):
                by_domain[str(scale)] = dict(failures=len(all_rows)-len(valid))
                continue
            mean = lambda name, data: float(np.mean([r[name] for r in data]))
            value = dict(failures=0, stand_speed_rms_m_s=mean('zero_speed_rms_m_s',stand),
                stand_drift_slope_m_s=mean('drift_slope_x_m_s',stand),
                stand_displacement_x_m=float(np.mean([r['displacement_m'][0] for r in stand])),
                stop_speed_rms_m_s=mean('zero_speed_rms_m_s',drive),
                stand_pitch_mean_deg=float(np.mean([r['pitch_deg']['mean'] for r in stand])),
                stand_pitch_std_deg=float(np.mean([r['pitch_deg']['std'] for r in stand])),
                stand_pitch_rms_deg=float(np.mean([r['pitch_deg']['rms'] for r in stand])),
                stop_pitch_rms_deg=float(np.mean([r['pitch_deg']['rms'] for r in drive])),
                leg_torque_rms_nm=mean('leg_torque_rms_nm',stand),
                wheel_torque_rms_nm=mean('wheel_torque_rms_nm',stand),
                leg_torque_step_rms_nm=mean('leg_torque_step_rms_nm',stand),
                stand_joint_mean_rad=np.mean([r['joint_angle_rad']['mean'] for r in stand],axis=0).tolist(),
                stand_joint_std_rad=np.mean([r['joint_angle_rad']['std'] for r in stand],axis=0).tolist(),
                stand_torque_rms_nm=np.mean([r['torque_nm']['rms'] for r in stand],axis=0).tolist(),
                stand_torque_abs_peak_nm=np.max([r['torque_nm']['abs_peak'] for r in stand],axis=0).tolist(),
                full_torque_abs_peak_nm=np.max([r['metrics']['torque_full_nm']['abs_peak'] for r in valid],axis=0).tolist(),
                max_full_pitch_deg=max(r['metrics']['pitch_full_abs_peak_deg'] for r in valid),
                max_saturation_fraction=float(np.max([r['metrics']['torque_saturation_fraction'] for r in valid])),
                tracking=[{key: float(np.mean([r['tracking'][i][key] for r in drive])) for key in drive[0]['tracking'][i] if key!='window_s'}
                    for i in range(len(drive[0]['tracking']))])
            value['zero_speed_score_m_s'] = (value['stand_speed_rms_m_s']+value['stop_speed_rms_m_s'])/2
            by_domain[str(scale)] = value
            rows.append(dict(step=step,knee_scale=scale,**{k:v for k,v in value.items() if isinstance(v,(float,int))}))
        failed = sum(r['evidence_status']!='PASS' for r in results if r['step']==step)
        summary[str(step)] = dict(failed_rollouts=failed, domains=by_domain,
            worst_zero_speed_score_m_s=max([d.get('zero_speed_score_m_s',1e6) for d in by_domain.values()]),
            worst_zero_pitch_rms_deg=max([max(d.get('stand_pitch_rms_deg',1e6),d.get('stop_pitch_rms_deg',1e6)) for d in by_domain.values()]))
    ranking = sorted(STEPS,key=lambda step:(summary[str(step)]['failed_rollouts'],
        summary[str(step)]['worst_zero_speed_score_m_s'],summary[str(step)]['worst_zero_pitch_rms_deg']))
    write_json(output/'summary.json',dict(execution_domain='VALIDATION_SIM', joint_order=NATIVE_JOINTS,
        ranking=ranking, by_checkpoint=summary))
    if rows:
        with (output/'summary.csv').open('w') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print('[VALIDATION_SIM] Ranking:',ranking,flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--prepare',action='store_true')
    mode.add_argument('--evaluate',action='store_true')
    mode.add_argument('--summarize',action='store_true')
    parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args()
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=True)
    if args.prepare:prepare(output)
    elif args.evaluate:evaluate(output,args.workers)
    else:summarize(output)


if __name__=='__main__':
    main()
