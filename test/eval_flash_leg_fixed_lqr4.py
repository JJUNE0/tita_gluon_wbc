"""VALIDATION_SIM: E = unchanged FlashSAC legs plus unchanged C-4 wheel LQR."""

import argparse
import csv
import json
from pathlib import Path
import sys
import time

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'test'))
from debug_lqr_d4_diagnostics import ARCHIVE, Plant
from sim2sim.lqr.controller import WheelLQR
from sim2sim.lqr.evaluate import episode, ground_truth, write_json
from sim2sim.lqr.model import Description
from sim2sim.lqr.runtime import LEGS, WHEELS, policy_config
from sim2sim_ros2_jazzy.checkpoint import read_yaml, sha256


def action_history_slice(policy):
    offset = 0
    for term in policy['policy_interface']['observations']:
        if term['kind'] == 'last_action':
            return slice(offset, offset + term['size']), np.asarray(term['scale']), term['clip']
        offset += term['size']
    raise ValueError('The designated actor must receive the same last_action as A')


def hybrid_torque(torque, total_lqr, signs):
    result = torque.copy()
    result[WHEELS] = signs * total_lqr / 2
    return result


def run_e(policy, cfg, description, parameters, mismatch, seed, pitch, output):
    plant = Plant(policy, cfg, description, parameters, mismatch, seed, pitch)
    env, playback = plant.env, plant.playback
    fixed = WheelLQR(parameters, env.control_dt, 4, cfg['controller'], adaptive=False)
    fixed.frozen = True
    history_slice, history_scale, history_clip = action_history_slice(policy)
    wheel_action_indices = [playback.adapter.order.index(int(i)) for i in WHEELS]
    leg_action_indices = [playback.adapter.order.index(int(i)) for i in LEGS]
    rows = []
    commands = np.zeros((env.decimation, 8))
    motors = commands.copy()
    discarded = commands.copy()
    observation = plant.observe()
    initial_physics = np.r_[env.data.qpos, env.data.qvel].copy()
    history_error = leg_error = wheel_error = 0.
    last_action = np.zeros(8)
    last_obs = np.zeros(policy['policy']['obs_dim'])
    last_targets = np.zeros(8)
    last_counterfactual = np.zeros(6)
    prior_history = np.zeros(8)
    forward_distance = 0.
    previous_forward_velocity = None
    previous_control_u = 0.
    failures = []
    try:
        for tick in range(round(cfg['duration_s'] / env.control_dt) + 1):
            t = tick * env.control_dt
            x = observation['sensor']
            failures, margin = plant.failures(observation, 'sensor')
            pos, vel = ground_truth(env, plant.wheels)
            cached_rpy = Rotation.from_quat(env.base_quat_sensor()[[1, 2, 3, 0]]).as_euler('xyz')
            velocity_forward = float(vel @ [np.cos(cached_rpy[2]), np.sin(cached_rpy[2]), 0.])
            if previous_forward_velocity is not None:
                forward_distance += env.control_dt * (previous_forward_velocity + velocity_forward) / 2
            previous_forward_velocity = velocity_forward
            body_ids = np.setdiff1d(np.arange(1, env.model.nbody), plant.wheels)
            com = np.average(env.data.xipos[body_ids], axis=0, weights=env.model.body_mass[body_ids])
            com_body = env.data.xmat[plant.base].reshape(3, 3).T @ (com - env.data.xpos[plant.base])
            rows.append(dict(time=t, state=x.copy(), gt_position=pos, gt_velocity=vel,
                gt_forward_distance=forward_distance, gt_forward_velocity=velocity_forward,
                rpy=cached_rpy, true_rpy=observation['rpy'].copy(),
                command_torque=commands[:, WHEELS].mean(0), motor_torque=motors[:, WHEELS].mean(0),
                command_substeps=commands.copy(), motor_substeps=motors.copy(),
                discarded_flash_torque_substeps=discarded.copy(),
                policy_action=last_action.copy(), policy_observation=last_obs.copy(),
                history_input=prior_history.copy(), policy_targets=last_targets.copy(),
                zero_wheel_history_leg_delta=last_counterfactual.copy(),
                lqr_total_torque=previous_control_u, raw_lqr_torque=float(-fixed.K @ x),
                saturation=fixed.saturated, K=fixed.K.copy(), base_height=observation['base_height'],
                joint_position=env.joint_pos(), joint_velocity=env.joint_vel(),
                leg_limit_margin=margin, leg_error=env.joint_pos()[LEGS]-plant.stand[LEGS],
                leg_velocity=env.joint_vel()[LEGS], com_body=com_body))
            if failures or tick == round(cfg['duration_s'] / env.control_dt):
                break
            env.data.xfrc_applied[:] = 0.
            force = cfg['disturbance']
            if force['start_s'] <= t < force['start_s'] + force['duration_s']:
                env.data.xfrc_applied[plant.base, 0] = force['force_n']
            prior_history = playback.last_action.copy()
            obs, action = playback.infer()  # Identical 33-value observation and deterministic actor as A.
            expected_history = prior_history.copy()
            if history_clip is not None:
                expected_history = np.clip(expected_history, *history_clip)
            expected_history *= history_scale
            history_error = max(history_error, float(np.max(abs(obs[history_slice]-expected_history))))
            alternative = obs.copy()
            history_indices = np.arange(policy['policy']['obs_dim'])[history_slice]
            alternative[history_indices[wheel_action_indices]] = 0.
            counterfactual = playback.policy.run(['nn_output'], {'nn_input0': alternative.reshape(1, -1)})[0].reshape(8)
            last_counterfactual = (counterfactual-action)[leg_action_indices]
            u = fixed.command(x)
            discarded_rows = []

            def override(q, dq, torque):
                nonlocal leg_error, wheel_error
                # The actor output stays intact; replace only the final native wheel torque.
                discarded_rows.append(torque.copy())
                result = hybrid_torque(torque, u, plant.signs)
                leg_error = max(leg_error, float(np.max(abs(result[LEGS]-torque[LEGS]))))
                wheel_error = max(wheel_error, float(np.max(abs(result[WHEELS]-plant.signs*u/2))))
                return result

            def motor(torque):
                target = torque[WHEELS] * mismatch.get('motor_gain', 1.)
                lag = mismatch.get('motor_lag_s', 0.)
                if lag:
                    plant.motor_state += (1-np.exp(-env.model.opt.timestep/lag))*(target-plant.motor_state)
                else:
                    plant.motor_state = target
                result = torque.copy()
                result[WHEELS] = np.clip(plant.motor_state, -12., 12.)
                return result

            commands, motors = playback.step(action, override, motor)
            # Playback itself performs A's last_action = full raw actor output copy.
            np.testing.assert_array_equal(playback.last_action, action)
            discarded = np.asarray(discarded_rows)
            previous_control_u = u
            last_obs, last_action = obs.copy(), action.copy()
            last_targets = playback.adapter.targets(action)
            observation = plant.observe()
        trace = {key: np.asarray([r[key] for r in rows]) for key in rows[0]}
        name = f'E_{mismatch["name"]}_s{seed}_p{pitch:+.3f}'
        np.savez_compressed(output / (name+'.npz'), **trace)
        displacement = trace['gt_position'] - trace['gt_position'][0]
        planar = np.linalg.norm(displacement[:, :2], axis=1)
        rms = lambda values: float(np.sqrt(np.mean(np.asarray(values)**2)))
        assert not fixed.rls.regressors and fixed.accepted == 0 and fixed.rejected == 0
        np.testing.assert_array_equal(fixed.K, fixed.K0)
        result = dict(execution_domain='VALIDATION_SIM', evidence_status='FAIL' if failures else 'PASS',
            checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'], mode='E', mismatch=mismatch['name'],
            seed=seed, pitch_delta_rad=pitch, initial_velocity_m_s=plant.initial_velocity, initial_physics=initial_physics.tolist(),
            completed_s=float(trace['time'][-1]), failure=';'.join(failures), trace=name+'.npz',
            max_displacement_m=float(planar.max()), final_planar_displacement_m=float(planar[-1]),
            final_displacement_m=float(displacement[-1,0]), position_rms_m=rms(planar),
            pitch_rms_rad=rms(trace['state'][:,2]), peak_pitch_rad=float(np.max(abs(trace['state'][:,2]))),
            body_pitch_rms_rad=rms(trace['rpy'][:,1]), true_pitch_error_rms_rad=rms(trace['true_rpy'][:,1]-parameters['equilibrium_pitch']),
            torque_rms_nm=rms(trace['motor_substeps'][:, :, WHEELS]), peak_torque_nm=float(np.max(abs(trace['motor_substeps'][:, :, WHEELS]))),
            raw_lqr_clipping_ratio=float(np.mean(trace['saturation'])),
            odometry_error_rms_m=rms(trace['state'][:,0]-trace['gt_forward_distance']),
            leg_error_rms_rad=rms(trace['leg_error']), leg_velocity_rms_rad_s=rms(trace['leg_velocity']),
            com_change_max_m=float(np.max(np.linalg.norm(trace['com_body']-trace['com_body'][0],axis=1))),
            zero_wheel_history_leg_delta_rms=rms(trace['zero_wheel_history_leg_delta'][1:]),
            zero_wheel_history_leg_delta_max=float(np.max(abs(trace['zero_wheel_history_leg_delta']))),
            K=fixed.K.tolist(), applied_parameters=plant.applied,
            audit=dict(leg_torque_max_error_nm=leg_error, wheel_override_max_error_nm=wheel_error,
                       last_action_observation_max_error=history_error, online_rls_calls=0,
                       history_policy='full previous actor output, including unexecuted wheel action'),
            failure_snapshot={key: np.asarray(trace[key][-1]).tolist() for key in
                ('state','rpy','base_height','joint_position','leg_limit_margin','motor_torque','K')})
        return result
    finally:
        env.close()


def check_archive(result, output, reference):
    assert result['failure'] == reference['failure'] and result['completed_s'] == reference['completed_s']
    with np.load(output / result['trace']) as current, np.load(ARCHIVE / reference['trace']) as archived:
        errors = {key: float(np.max(abs(current[key]-archived[key])))
                  for key in ('state','motor_torque','gt_position','leg_error')}
        assert max(errors.values()) == 0., errors
    return errors


def summarize_results(results, output, manifest):
    aggregates = []
    mismatches = [m['name'] for m in manifest['cfg']['mismatches']]
    for mismatch in mismatches:
        for mode in ('A','C-4','E'):
            rows = [r for r in results if r['mismatch'] == mismatch and r['mode'] == mode]
            if not rows:
                continue
            completed = [r for r in rows if not r['failure']]
            a = dict(mismatch=mismatch, mode=mode, total=len(rows), failed=len(rows)-len(completed))
            for key in ('max_displacement_m','pitch_rms_rad','position_rms_m','leg_error_rms_rad'):
                values = [r[key] for r in completed]
                a[key+'_mean'] = float(np.mean(values)) if values else None
                a[key+'_std'] = float(np.std(values,ddof=1)) if len(values)>1 else 0. if values else None
            aggregates.append(a)
    write_json(output/'aggregates.json',aggregates)
    fields = sorted({key for r in results for key,value in r.items() if not isinstance(value,(dict,list))})
    with (output/'metrics.csv').open('w') as stream:
        writer=csv.DictWriter(stream,fields,extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)
    fig,axes=plt.subplots(3,1,figsize=(10,9),sharex=True)
    for mode in ('A','C-4','E'):
        r=next(r for r in results if r['mismatch']=='nominal' and r['mode']==mode and r['seed']==42)
        with np.load(output/r['trace']) as trace:
            axes[0].plot(trace['time'],np.linalg.norm(trace['gt_position'][:,:2]-trace['gt_position'][0,:2],axis=1),label=mode)
            axes[1].plot(trace['time'],trace['state'][:,2],label=mode)
            axes[2].plot(trace['time'],trace['motor_torque'].sum(1),label=mode)
    for ax,label in zip(axes,('Planar displacement [m]','Pitch error [rad]','Total wheel torque [Nm]')):
        ax.set_ylabel(label)
        ax.grid(alpha=.3)
    axes[0].legend()
    axes[2].set_xlabel('Time [s]')
    fig.tight_layout()
    fig.savefig(output/'comparison.png',dpi=180)
    plt.close(fig)
    return aggregates


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--quick',action='store_true')
    parser.add_argument('--nominal-only',action='store_true')
    args=parser.parse_args()
    output=args.output.resolve()
    if not output.is_relative_to(REPO/'docs/exp') or output.exists():
        parser.error('Choose a new output directory under docs/exp/')
    output.mkdir(parents=True)
    archived_manifest=json.loads((ARCHIVE/'manifest.json').read_text())
    cfg=json.loads((ARCHIVE/'config.json').read_text())
    policy=policy_config()
    source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description=Description(source['scene']['robot']['spawn']['asset_path'])
    parameters=archived_manifest['nominal_parameters']
    archived=[json.loads(line) for line in (ARCHIVE/'results.jsonl').read_text().splitlines()]
    lookup={(r['mode'],r['mismatch'],r['seed'],r['pitch_delta_rad']):r for r in archived if r['phase']=='evaluation'}
    manifest=dict(execution_domain='VALIDATION_SIM',evidence_status='NOT_TESTED',
        checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],onnx_sha256=policy['policy_interface']['onnx_sha256'],
        cfg=cfg,policy_config=policy,nominal_parameters=parameters,script_sha256=sha256(Path(__file__)),
        existing_actor_freeze=True,online_rls=False,quick=args.quick,nominal_only=args.nominal_only)
    write_json(output/'manifest.json',manifest)
    results=[]
    started=time.monotonic()
    for mismatch in cfg['mismatches']:
        if (args.quick or args.nominal_only) and mismatch['name']!='nominal':
            continue
        for seed in cfg['seeds']:
            for pitch in cfg['pitch_disturbances_rad']:
                if args.quick and (seed!=42 or pitch!=0.):
                    continue
                for mode in ('A','C-4','E'):
                    if mode=='E':
                        r=run_e(policy,cfg,description,parameters,mismatch,seed,pitch,output)
                    else:
                        r,_=episode(policy,cfg,description,parameters,mode,mismatch,seed,pitch,output)
                        r['archive_errors']=check_archive(r,output,lookup[(mode,mismatch['name'],seed,pitch)])
                    results.append(r)
                    with (output/'results.jsonl').open('a') as stream:
                        stream.write(json.dumps(r,allow_nan=False)+'\n')
                    print(f'[VALIDATION_SIM] {mode} {mismatch["name"]} s{seed} p{pitch:+.3f} '
                          f'{r["evidence_status"]} {r["failure"]} t={r["completed_s"]:.2f} '
                          f'episodes={len(results)} elapsed={time.monotonic()-started:.1f}s',flush=True)
    aggregates=summarize_results(results,output,manifest)
    write_json(output/'completion.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',
        checkpoint_sha256=manifest['checkpoint_sha256'],episodes=len(results),aggregates=aggregates))


if __name__=='__main__':
    main()
