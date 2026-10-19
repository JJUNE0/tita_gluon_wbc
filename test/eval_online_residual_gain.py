"""VALIDATION_SIM: fixed residual mismatch baselines and sensor-only alpha learning.

Frozen full FlashSAC inference, raw last_action, original leg/wheel PD and actuator
clipping are reused. No RLS, LQR, true position or mismatch identity enters G.
"""

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'test'))
from debug_lqr_d4_diagnostics import ARCHIVE, Plant
from eval_flash_torque_residual import DEFAULT_RESIDUAL, PositionVelocityResidual, additive_torque, action_history_slice
from sim2sim.lqr.evaluate import ground_truth, write_json
from sim2sim.lqr.model import Description
from sim2sim.lqr.runtime import LEGS, WHEELS, policy_config
from sim2sim_ros2_jazzy.checkpoint import read_yaml, sha256

ADAPTATION=dict(alpha_initial=1.,alpha_min=.5,alpha_max=2.,probe_delta=.1,
    centre_step=.1,alpha_slew_s=.25,start_s=4.,block_s=3.,discard_s=1.,
    confidence_sigma=2.,min_relative_effect=.005,pitch_guard_rad=.25,rate_guard_rad_s=1.,
    velocity_guard_m_s=.5,cooldown_s=4.,
    objective=dict(position_scale_m=.5,velocity_scale_m_s=.05,pitch_std_scale_rad=.02,
        rate_scale_rad_s=.2,torque_scale_nm=.5,weights=[1.,1.,.25,.05,.02]))


def fit_probe_gradient(windows):
    """Eight balanced windows, nuisance quadratic time trend, actual alpha dose."""
    t=np.asarray([w['time'] for w in windows]);t=(t-t.mean())/max(np.ptp(t)/2,1.)
    dose=np.asarray([w['alpha_offset'] for w in windows])
    costs=np.asarray([w['cost'] for w in windows])
    design=np.column_stack([np.ones(len(t)),t,t*t,dose])
    coefficients,_,rank,singular=np.linalg.lstsq(design,costs,rcond=1e-9)
    if rank<4 or len(t)<=4:
        return dict(valid=False,reason='insufficient_probe_rank',rank=int(rank))
    residual=costs-design @ coefficients
    variance=float(residual @ residual/(len(t)-4))
    covariance=variance*np.linalg.inv(design.T @ design)
    return dict(valid=True,gradient=float(coefficients[-1]),standard_error=float(np.sqrt(max(0.,covariance[-1,-1]))),
        rank=int(rank),condition_number=float(singular[0]/singular[-1]),mean_cost=float(costs.mean()),
        fit_rms=float(np.sqrt(np.mean(residual**2))),time_coefficients=coefficients[:3].tolist())


class OnlineAlpha:
    def __init__(self, config=ADAPTATION):
        self.config=json.loads(json.dumps(config))
        self.centre=self.alpha=float(config['alpha_initial'])
        self.block=None;self.samples=[];self.windows=[];self.events=[]
        self.restart=float(config['start_s']);self.accepted=self.rejected=self.guards=0
        self.guard_active=False

    def _window(self, index):
        if not self.samples:
            return None
        a=np.asarray(self.samples)
        objective=self.config['objective']
        terms=np.array([np.mean((a[:,1]/objective['position_scale_m'])**2),
            np.mean((a[:,2]/objective['velocity_scale_m_s'])**2),
            np.var(a[:,3])/objective['pitch_std_scale_rad']**2,
            np.mean((a[:,4]/objective['rate_scale_rad_s'])**2),
            np.mean((a[:,5]/objective['torque_scale_nm'])**2)])
        return dict(block=index,time=float(a[:,0].mean()),alpha_offset=float(a[:,6].mean()-self.centre),
            cost=float(terms @ objective['weights']),terms=terms.tolist(),samples=len(a))

    def observe(self, state, command_rms, t):
        c=self.config
        if abs(state[2])>c['pitch_guard_rad'] or abs(state[3])>c['rate_guard_rad_s'] or abs(state[1])>c['velocity_guard_m_s']:
            # Report activation even during startup/cooldown. This latch changes
            # logging only; restart, centre, samples and alpha control stay intact.
            if not self.guard_active:
                self.guards+=1;self.events.append(dict(time=t,reason='sensor_guard',centre_before=self.centre))
            self.guard_active=True
            self.centre=float(c['alpha_initial']);self.windows=[];self.samples=[];self.block=None
            self.restart=t+c['cooldown_s']
            return
        self.guard_active=False
        if t<self.restart:
            return
        index=int(np.floor((t-self.restart+1e-8)/c['block_s']))
        if self.block is None:
            self.block=index
        elif index!=self.block:
            window=self._window(self.block)
            if window:
                self.windows.append(window)
            self.samples=[];self.block=index
            if len(self.windows)==8:
                fit=fit_probe_gradient(self.windows)
                before=self.centre
                accept=fit['valid'] and abs(fit['gradient'])>c['confidence_sigma']*fit['standard_error'] and (
                    abs(fit['gradient'])*c['probe_delta']>c['min_relative_effect']*max(fit['mean_cost'],1e-6))
                if accept:
                    self.centre=float(np.clip(before-c['centre_step']*np.sign(fit['gradient']),c['alpha_min'],c['alpha_max']))
                    self.accepted+=int(self.centre!=before)
                else:
                    self.rejected+=1
                self.events.append(dict(time=t,reason='accepted' if accept else 'uncertain_gradient',
                    centre_before=before,centre_after=self.centre,fit=fit,windows=self.windows))
                self.windows=[]
        age=(t-self.restart)-index*c['block_s']
        if age>=c['discard_s']:
            self.samples.append([t,state[0],state[1],state[2],state[3],command_rms,self.alpha])

    def command_alpha(self, t, dt):
        if t<self.restart:
            target=self.centre
        else:
            index=int(np.floor((t-self.restart+1e-8)/self.config['block_s']))
            # ABBA, then BAAB: opposite ordering before each gain update.
            offset=np.array([1.,-1.,-1.,1.,-1.,1.,1.,-1.])[index%8]
            target=self.centre+self.config['probe_delta']*offset
        target=float(np.clip(target,self.config['alpha_min'],self.config['alpha_max']))
        step=self.config['alpha_slew_s']*dt
        self.alpha=float(np.clip(target,self.alpha-step,self.alpha+step))
        return self.alpha


def motor_step(torque, state, gain, lag, dt, limits):
    target=torque[WHEELS]*gain
    following=state+(1.-np.exp(-dt/lag))*(target-state) if lag else target
    output=torque.copy();output[WHEELS]=np.clip(following,-limits[WHEELS],limits[WHEELS])
    return output,following


def run_episode(policy,cfg,description,parameters,mismatch,seed,pitch,label,output,
                duration=12.,learn=False,fixed_alpha=1.,adapt_config=None,alpha_learning=True):
    plant=Plant(policy,cfg,description,parameters,mismatch,seed,pitch)
    env,playback=plant.env,plant.playback
    observation=plant.observe()
    initial=np.r_[env.data.qpos,env.data.qvel].copy()
    history_slice,history_scale,history_clip=action_history_slice(policy)
    fixed=PositionVelocityResidual(DEFAULT_RESIDUAL,0. if label=='A' else fixed_alpha,0.)
    online=OnlineAlpha(adapt_config or ADAPTATION) if learn else None
    rows=[];violations=[];commands=np.zeros((env.decimation,8));motors=commands.copy();flash=commands.copy()
    action=history=np.zeros(8);obs=np.zeros(policy['policy']['obs_dim']);u=raw=ramp=0.
    last_alpha=0. if label=='A' else fixed_alpha
    leg_error=history_error=sum_error=0.
    try:
        for tick in range(round(duration/env.control_dt)+1):
            t=tick*env.control_dt;x=observation['synchronized']
            violations,margin=plant.failures(observation,'synchronized')
            pos,_=ground_truth(env,plant.wheels)
            command_rms=float(np.sqrt(np.mean(commands[:,WHEELS]**2)))
            if online and alpha_learning:
                online.observe(x,command_rms,t)
            rows.append(dict(time=t,state=x.copy(),sensor_state=observation['sensor'].copy(),gt_state=observation['gt'].copy(),
                gt_position=pos.copy(),true_position=observation['position'].copy(),
                command_substeps=commands.copy(),motor_substeps=motors.copy(),flash_substeps=flash.copy(),
                residual_total_nm=u,residual_raw_nm=raw,activation=ramp,alpha=last_alpha,
                alpha_centre=online.centre if online else last_alpha,accepted=online.accepted if online else 0,
                rejected=online.rejected if online else 0,guards=online.guards if online else 0,
                policy_observation=obs.copy(),policy_action=action.copy(),history_input=history.copy(),
                leg_error=env.joint_pos()[LEGS]-plant.stand[LEGS],leg_limit_margin=margin))
            if violations or tick==round(duration/env.control_dt):
                break
            env.data.xfrc_applied[:]=0.
            force=cfg['disturbance']
            if force['start_s']<=t<force['start_s']+force['duration_s']:
                env.data.xfrc_applied[plant.base,0]=force['force_n']
            history=playback.last_action.copy();obs,action=playback.infer()
            expected=np.clip(history,*history_clip)*history_scale if history_clip is not None else history*history_scale
            history_error=max(history_error,float(abs(obs[history_slice]-expected).max()))
            if online:
                last_alpha=online.command_alpha(t,env.control_dt) if alpha_learning else online.config['alpha_initial']
                fixed.alpha=last_alpha
            u,raw,ramp=fixed.command(x,t,env.control_dt)
            # Keep the hard physical residual bound even when alpha > 1.
            u=float(np.clip(u,-DEFAULT_RESIDUAL['limit_total_nm'],DEFAULT_RESIDUAL['limit_total_nm']))
            fixed.previous=u
            flash_rows=[]

            def override(q,dq,torque):
                nonlocal leg_error,sum_error
                flash_rows.append(torque.copy());result=additive_torque(torque,u,plant.signs)
                leg_error=max(leg_error,float(abs(result[LEGS]-torque[LEGS]).max()))
                sum_error=max(sum_error,float(abs(result[WHEELS]-(torque[WHEELS]+plant.signs*u/2)).max()))
                return result

            def motor(torque):
                gain=mismatch.get('motor_gain',1.)
                if mismatch.get('step_s') is not None and t>=mismatch['step_s']:
                    gain=mismatch['step_motor_gain']
                result,plant.motor_state=motor_step(torque,plant.motor_state,gain,mismatch.get('motor_lag_s',0.),
                    env.model.opt.timestep,playback.adapter.limit)
                return result

            commands,motors=playback.step(action,override,motor)
            np.testing.assert_array_equal(playback.last_action,action)
            flash=np.asarray(flash_rows);observation=plant.observe()
        trace={k:np.asarray([r[k] for r in rows]) for k in rows[0]}
        identifier=f'{label}_{mismatch["name"]}_s{seed}_p{pitch:+.3f}'
        np.savez_compressed(output/(identifier+'.npz'),**trace)
        d=trace['gt_position']-trace['gt_position'][0];planar=np.linalg.norm(d[:,:2],axis=1)
        rms=lambda v:float(np.sqrt(np.mean(np.asarray(v)**2)))
        tail=trace['time']>=max(0.,duration-12.)
        result=dict(execution_domain='VALIDATION_SIM',evidence_status='FAIL' if violations else 'PASS',
            checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],label=label,mismatch=mismatch['name'],
            seed=seed,pitch_delta_rad=pitch,trace=identifier+'.npz',initial_physics=initial.tolist(),
            requested_s=duration,completed_s=float(trace['time'][-1]),failures=violations,
            max_displacement_m=float(planar.max()),final_displacement_m=float(planar[-1]),
            max_forward_displacement_m=float(abs(d[:,0]).max()),max_lateral_displacement_m=float(abs(d[:,1]).max()),
            pitch_rms_rad=rms(trace['sensor_state'][:,2]),true_pitch_error_rms_rad=rms(trace['gt_state'][:,2]),
            torque_rms_nm=rms(trace['motor_substeps'][1:,:,WHEELS]),peak_torque_nm=float(abs(trace['motor_substeps'][:,:,WHEELS]).max()),
            command_torque_rms_nm=rms(trace['command_substeps'][1:,:,WHEELS]),
            residual_peak_total_nm=float(abs(trace['residual_total_nm']).max()),
            tail_velocity_rms_m_s=rms(trace['state'][tail,1]) if np.any(tail) else None,
            tail_path_drift_m=float(trace['state'][-1,0]-trace['state'][np.flatnonzero(tail)[0],0]) if np.any(tail) else None,
            odometry_error_rms_m=rms(trace['state'][:,0]-trace['gt_state'][:,0]),
            alpha_final=float(trace['alpha'][-1]),alpha_centre_final=online.centre if online else last_alpha,
            accepted_updates=online.accepted if online else 0,rejected_updates=online.rejected if online else 0,
            guard_events=online.guards if online else 0,applied_parameters=plant.applied,
            audit=dict(leg_torque_max_error_nm=leg_error,history_max_error=history_error,
                wheel_sum_max_error_nm=sum_error,gt_used_for_learning=False,online_rls_calls=0),
            adaptive_config=online.config if online else None,
            adaptation_events=online.events if online else [])
        return result
    finally:
        env.close()


def check_reference(result,output):
    if result['label']=='A':
        base=ARCHIVE
        reference=next(r for r in map(json.loads,(base/'results.jsonl').read_text().splitlines()) if
            r['mode']=='A' and r['phase']=='evaluation' and r['mismatch']==result['mismatch'] and
            r['seed']==result['seed'] and r['pitch_delta_rad']==result['pitch_delta_rad'])
        fields=[('sensor_state','state'),('gt_position','gt_position'),('leg_error','leg_error')]
    elif result['mismatch']=='nominal' and result['label']=='F-1':
        base=REPO/'docs/exp/2026-10-15/flash_torque_residual/f1_nominal'
        reference=next(r for r in map(json.loads,(base/'results.jsonl').read_text().splitlines()) if
            r['label']=='F-1_a1' and r['seed']==result['seed'] and r['pitch_delta_rad']==result['pitch_delta_rad'])
        fields=[('state','state'),('gt_position','gt_position'),('policy_action','policy_action')]
    else:
        return None
    assert result['completed_s']==reference['completed_s']
    with np.load(output/result['trace']) as current,np.load(base/reference['trace']) as archived:
        errors={x:float(abs(current[x]-archived[y]).max()) for x,y in fields}
        actual=current['motor_substeps'][:,:,WHEELS]
        expected=archived['motor_substeps'] if result['label']=='A' else archived['motor_substeps'][:,:,WHEELS]
        errors['motor_substeps']=float(abs(actual-expected).max())
    assert max(errors.values())==0.,errors
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--phase',choices=('baseline','online'),required=True)
    parser.add_argument('--conditions',nargs='+')
    parser.add_argument('--duration',type=float)
    parser.add_argument('--quick',action='store_true')
    args=parser.parse_args();output=args.output.resolve()
    if not output.is_relative_to(REPO/'docs/exp') or output.exists():
        parser.error('Choose a new docs/exp/ output directory')
    output.mkdir(parents=True)
    cfg=json.loads((ARCHIVE/'config.json').read_text());parameters=json.loads((ARCHIVE/'manifest.json').read_text())['nominal_parameters']
    policy=policy_config();source=read_yaml(next(p for p in policy['policy_interface']['sources'] if p.endswith('env.yaml')))
    description=Description(source['scene']['robot']['spawn']['asset_path'])
    duration=args.duration or (12. if args.phase=='baseline' else 60.)
    conditions=cfg['mismatches']+[dict(name='step_gain_0.8',step_s=20.,step_motor_gain=.8)]
    selected=[m for m in conditions if (args.conditions is None and m['name']!='step_gain_0.8') or
              (args.conditions is not None and m['name'] in args.conditions)]
    if args.conditions and set(args.conditions)!={m['name'] for m in selected}:
        parser.error('Unknown condition')
    manifest=dict(execution_domain='VALIDATION_SIM',evidence_status='NOT_TESTED',
        checkpoint_sha256=policy['policy_interface']['checkpoint_sha256'],onnx_sha256=policy['policy_interface']['onnx_sha256'],
        cfg=cfg,conditions=selected,duration_s=duration,phase=args.phase,adaptation=ADAPTATION,
        residual=DEFAULT_RESIDUAL,script_sha256=sha256(Path(__file__)),quick=args.quick,
        learning_inputs='synchronized encoders/IMU and commanded torque only; no ground-truth or mismatch identity',
        actor_timing='original A sensor cache',objective='window costs, paired ABBA/BAAB, quadratic time nuisance',
        algorithm='Online Adaptive Residual Feedback Control; scalar alpha only')
    write_json(output/'manifest.json',manifest)
    (output/'runner_source.txt').write_bytes(Path(__file__).read_bytes())
    started=time.monotonic();count=0
    for mismatch in selected:
        for seed in cfg['seeds']:
            for pitch in cfg['pitch_disturbances_rad']:
                if args.quick and (seed!=42 or pitch!=0.):
                    continue
                reference=None
                for label in (('A','F-1') if args.phase=='baseline' else ('A','F-1','G')):
                    result=run_episode(policy,cfg,description,parameters,mismatch,seed,pitch,label,output,
                        duration=duration,learn=label=='G')
                    if duration==12. and mismatch['name']!='step_gain_0.8':
                        result['archive_replay']=check_reference(result,output)
                    if reference is None:
                        reference=result['initial_physics']
                    np.testing.assert_array_equal(result['initial_physics'],reference)
                    with (output/'results.jsonl').open('a') as stream:
                        stream.write(json.dumps(result,allow_nan=False)+'\n')
                    count+=1
                    print(f'[VALIDATION_SIM] {args.phase} {mismatch["name"]} {label} s{seed} p{pitch:+.3f} '
                        f'{result["evidence_status"]} t={result["completed_s"]:.2f} drift={result["max_displacement_m"]:.4f} '
                        f'alpha={result["alpha_centre_final"]:.2f} updates={result["accepted_updates"]} '
                        f'{result["failures"]} episodes={count} elapsed={time.monotonic()-started:.1f}s',flush=True)
    write_json(output/'completion.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',episodes=count,
        elapsed_s=time.monotonic()-started))


if __name__=='__main__':
    main()
