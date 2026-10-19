"""VALIDATION_SIM: fixed-gain comparison, drift entry, then mismatch trials.

Only the pipeline coordinator calls stages after validated prerequisites. No
hardware or production configuration is changed; gains remain offline artifacts.
"""

import gzip
import json
from pathlib import Path
import pickle

import numpy as np

from flash_overnight_model_stages import (Runner,KEYS,BIAS,REPO,CKPT,current,parallel,
    prepared_config,write,sha256,lqr_gain,limited,integrate_path,CASES,rms)


def gains(root,plan):
    decision = json.loads((root/'02_independent_affine.json').read_text())
    assert decision['gate'] is True and decision['evidence_status']=='PASS'
    source = root/'affine_models_frozen.json'
    assert sha256(source)==decision['model_sha256']
    models = json.loads(source.read_text())['models']
    output = {}
    for name,model in models.items():
        n = len(model['B']);Q = np.zeros((n,n))
        Q[0,0] = plan['LQR']['Qp'];Q[1,1] = plan['LQR']['Qv']
        K,diagnostics = lqr_gain(np.asarray(model['A']),np.asarray(model['B']),model['state_std'],Q,plan['LQR']['R'])
        output[name] = dict(K=K.tolist(),Q=Q.tolist(),R=plan['LQR']['R'],diagnostics=diagnostics,
            reference=model['operating_reference'],indices=model['indices'],
            low=model['train_min'],high=model['train_max'])
    path = root/'gains_frozen.json';assert not path.exists()
    write(path,dict(execution_domain='DESKTOP_DRY_RUN',models=output,model_sha256=sha256(source),
        confirmation_sha256=sha256(root/'02_independent_affine.json'),plan_sha256=sha256(root/'plan.json'),
        no_tuning=True,reference='nonzero train internal states, including yaw rate; p/v targets0'))
    return output


class EffectRunner(Runner):
    """Wheel motor changes after additive command and saturation, at physics dt."""
    def enable_effect(self,effect):
        self.effect = effect
        self.motor_state = self.env.data.ctrl[np.asarray(self.env.actuator_ids)[[3,7]]].copy()
        self.physical_substeps = []
        original = self.env.step_with_torque_callback
        def wrapped(callback):
            def apply(q,dq):
                command = callback(q,dq)
                result = command.copy()
                target = command[[3,7]]*effect.get('gain',1.)
                lag = effect.get('lag',0.)
                self.motor_state = (self.motor_state+(1.-np.exp(-self.env.model.opt.timestep/lag))*(target-self.motor_state)
                    if lag else target)
                result[[3,7]] = np.clip(self.motor_state,-12.,12.)
                np.testing.assert_array_equal(result[[0,1,2,4,5,6]],command[[0,1,2,4,5,6]])
                self.physical_substeps.append(result.copy())
                return result
            return original(apply)
        self.env.step_with_torque_callback = wrapped

    def step(self,residual):
        if hasattr(self,'physical_substeps'):self.physical_substeps=[]
        value = super().step(residual)
        if hasattr(self,'physical_substeps'):value['physical_motor']=np.asarray(self.physical_substeps)
        return value


def physical_paths(trace,pre):
    yaw = np.r_[pre['yaw'],trace['rpy'][:,2]]
    base = np.vstack([pre['base_position'],trace['base_position']])
    axle = np.vstack([pre['position'],trace['position']])
    return integrate_path(base,yaw)[1:],integrate_path(axle,yaw)[1:]


def rollout_control(r,group,gain,duration,pre,p_target,amplitude=0.,ramp_bias=False):
    states,steps,extra_rows,raw_rows,support = [],[],[],[],[]
    previous = 0.;total_previous = 0. if ramp_bias else BIAS
    f1 = None
    if group=='F1':
        from sim2sim_ros2_jazzy.residual_wheel_pd import ResidualWheelPD
        f1 = ResidualWheelPD(r.env);f1.update(np.zeros(3));f1.position=r.observation['sensor'][0]-p_target
        f1.age=f1.u=0.
    count = round(duration/.02)
    for i in range(count+1):
        states.append({k:r.observation[k].copy() for k in KEYS})
        failure = r.failures()
        if failure or i==count:break
        z = current(r);z[0]-=p_target
        if gain is not None:
            ix = gain['indices'];error=z[ix]-gain['reference']
            raw = float(-np.asarray(gain['K'])@error)
            extra = limited(raw,previous,i*.02)
            low,high = np.asarray(gain['low']),np.asarray(gain['high'])
            support.append(bool(np.all(z[ix][1:]>=low[1:]-1e-8) and np.all(z[ix][1:]<=high[1:]+1e-8)))
        else:raw=extra=0.;support.append(True)
        if group=='F1':
            f1.update(np.zeros(3));raw=extra=float(f1.u)
        previous = extra
        target = 0. if group=='A' else (extra if group=='F1' else BIAS+extra)
        total = float(np.clip(target,total_previous-.04,total_previous+.04)) if ramp_bias else target
        total_previous = total
        transition = r.step(total)
        assert abs(transition['actual_u']-total)<1e-6
        if gain is not None:assert abs(extra)<=.050000001
        raw_rows.append(raw);extra_rows.append(extra);steps.append(transition)
    trace = {k:np.asarray([s[k] for s in states]) for k in KEYS}
    if steps:trace.update({k:np.asarray([s[k] for s in steps]) for k in steps[0]})
    trace.update(raw_correction=np.asarray(raw_rows),correction=np.asarray(extra_rows),
        hidden_inside_train_range=np.asarray(support))
    if steps:
        np.testing.assert_array_equal(trace['previous_action'][:-1],trace['history'])
        np.testing.assert_array_equal(trace['previous_action'][1:],trace['action'])
    base,axle = physical_paths(trace,pre)
    trace.update(base_path=base,axle_path=axle)
    t=np.arange(len(base))*.02;tail=(t>=duration-5.)&(t<duration)
    target = -amplitude
    base_error=base-target;axle_error=axle-target
    motor = trace.get('physical_motor',trace.get('motor'))
    def error_metrics(error):
        return dict(IAE=float(np.trapz(abs(error),t)),last5_RMSE=float(rms(error[tail],0)) if tail.any() else None,
            max_error=float(max(abs(error))))
    stats = dict(complete=not failure and len(states)==count+1,failure=failure,duration_s=float(t[-1]),
        base=error_metrics(base_error),wheel_midpoint=error_metrics(axle_error),
        last5_base_speed_mean=float(trace['base_velocity'][tail].mean()) if tail.any() else None,
        last5_base_speed_RMS=float(rms(trace['base_velocity'][tail],None)) if tail.any() else None,
        last5_base_position_range=float(np.ptp(base[tail])) if tail.any() else None,
        max_planar_drift=float(max(np.linalg.norm(trace['base_position'][:,:2]-pre['base_position'][:2],axis=1))),
        pitch_RMS=float(rms(trace['sensor'][:,2]-(gain['reference'][2] if gain is not None else pre['pitch']),0)),
        wheel_torque_RMS=float(rms(motor[:,:,[3,7]],None)) if motor is not None else 0.,
        hidden_train_fraction=float(np.mean(support)) if support else 0.,
        correction_peak=float(max(abs(trace['correction']))) if len(steps) else 0.)
    return trace,stats


def anchor(r):
    return dict(base_position=r.observation['base_position'].copy(),position=r.observation['position'].copy(),
        yaw=float(r.observation['rpy'][2]),pitch=float(r.observation['sensor'][2]))


def control_job(job,cfg,output,fresh,gain_bundle,pilot=False):
    out=Path(output)/job['id'];out.mkdir()
    r=Runner(cfg,job);rows=[]
    try:
        for time in job['times'][:1] if pilot else job['times']:
            tick=round(time/.02)
            with gzip.open(Path(fresh)/job['id']/f'snapshot_t{tick}.pkl.gz','rb') as f:snapshot=pickle.load(f)
            r.restore(snapshot);replay,fail=r.rollout(np.full(400,BIAS));assert not fail
            with np.load(Path(fresh)/job['id']/f'zero_t{tick}.npz') as old:
                for k in replay:np.testing.assert_array_equal(replay[k],old[k])
            selected = [('zero',0.),('position',.001),('kick',.02)] if pilot else CASES
            for family,amplitude in selected:
                r.restore(snapshot);pre=anchor(r);p_target=float(r.observation['sensor'][0])
                if family=='position':p_target-=amplitude
                if family=='kick':r.step(BIAS+amplitude)
                disturbed=r.snapshot();first=current(r)
                for group in ['bias_only','M4','M5']:
                    r.restore(disturbed);np.testing.assert_array_equal(current(r),first)
                    trace,stats=rollout_control(r,group,gain_bundle.get(group),20.,pre,p_target,
                        amplitude if family=='position' else 0.)
                    name=f'{group}_{family}_{amplitude:+g}_t{tick}.npz';np.savez_compressed(out/name,**trace)
                    rows.append(dict(context=job['id'],group=group,family=family,amplitude=amplitude,
                        start_hold_s=time,trace=name,**stats))
        write(out/'results.json',dict(execution_domain='VALIDATION_SIM',job=job,rows=rows,initial_state_history_exact=True))
        print('[VALIDATION_SIM]',job['id'],'control runs',len(rows),flush=True)
        return rows
    finally:r.env.close()


def summarize_control(rows):
    summaries={};gates={}
    def key(row):return row['context'],row.get('start_hold_s',0),row['family'],row['amplitude']
    bases={key(r):r for r in rows if r['group']=='bias_only'}
    for group in ['M4','M5']:
        selected=[r for r in rows if r['group']==group]
        stable=all(r['complete'] and bases[key(r)]['complete'] and r['pitch_RMS']<=max(1.25*bases[key(r)]['pitch_RMS'],.002) and
            r['wheel_torque_RMS']<=1.25*bases[key(r)]['wheel_torque_RMS'] for r in selected)
        families={}
        for family in ['position','kick']:
            trials=[r for r in selected if r['family']==family]
            if not trials or any(not r['complete'] or not bases[key(r)]['complete'] or
                    r['base']['last5_RMSE'] is None or bases[key(r)]['base']['last5_RMSE'] is None for r in trials):
                families[family]=dict(gate=False,count=len(trials),reason='incomplete physical trial or missing full-horizon metric')
                continue
            a=np.asarray([r['base']['IAE'] for r in trials]);b=np.asarray([bases[key(r)]['base']['IAE'] for r in trials])
            x=np.asarray([r['base']['last5_RMSE'] for r in trials]);y=np.asarray([bases[key(r)]['base']['last5_RMSE'] for r in trials])
            good=bool(len(trials) and all(r['complete'] for r in trials) and np.median(a)<=.8*np.median(b) and
                np.median(x)<=.5*np.median(y) and np.mean(a<b)>=.8)
            families[family]=dict(gate=good,count=len(trials),base_IAE_median=float(np.median(a)),
                bias_base_IAE_median=float(np.median(b)),last5_base_RMSE_median=float(np.median(x)),
                bias_last5_base_RMSE_median=float(np.median(y)),paired_IAE_wins=int((a<b).sum()))
        zero=[r for r in selected if r['family']=='zero']
        zero_good=bool(zero and all(r['complete'] and bases[key(r)]['complete'] and r['base']['last5_RMSE']<=max(
            bases[key(r)]['base']['last5_RMSE']+.00005,.0001) and abs(r['last5_base_speed_mean'])<=.00002 for r in zero))
        gates[group]=bool(stable and zero_good and all(f['gate'] for f in families.values()))
        summaries[group]=dict(gate=gates[group],stability_gate=stable,zero_gate=zero_good,families=families)
    return dict(gate=all(gates.values()),models=summaries,runs=len(rows),all_complete=all(r['complete'] for r in rows),
        reference='base_link origin primary; wheel midpoint metrics retained per trial')


def stage3(root,plan):
    output=gains(root,plan);frozen=sha256(root/'gains_frozen.json')
    jobs=json.loads((root/'fresh/manifest.json').read_text())['jobs']
    cfg=json.loads(prepared_config(CKPT).read_text())
    pilot=root/'control_pilot';pilot.mkdir()
    rows=control_job(jobs[0],cfg,str(pilot),str(root/'fresh'),output,True)
    pilot_result=summarize_control(rows);write(root/'control_pilot_summary.json',pilot_result)
    if not pilot_result['gate']:
        return dict(pilot_result,pilot_gate=False,full_runs=0,reason='small actual-MuJoCo pilot failed; full comparison not launched')
    full=root/'control';full.mkdir()
    groups=parallel(control_job,jobs,plan['workers'],cfg,str(full),str(root/'fresh'),output)
    rows=[r for group in groups for r in group]
    assert sha256(root/'gains_frozen.json')==frozen
    result=summarize_control(rows)
    result.update(pilot_gate=True,full_runs=len(rows),gain_sha256=frozen)
    write(root/'control_metrics.json',dict(execution_domain='VALIDATION_SIM',rows=rows))
    return result


def entry_job(job,cfg,output,gain_bundle):
    out=Path(output)/job['id'];out.mkdir();r=Runner(cfg,job)
    try:
        for i in range(400):
            if i>=50:assert not r.failures()
            r.step(0.)
        snapshot=r.snapshot();pre=anchor(r);p_target=float(r.observation['sensor'][0]);rows=[]
        for group in ['A','bias_only','M4','M5']:
            r.restore(snapshot)
            trace,stats=rollout_control(r,group,gain_bundle.get(group),60.,pre,p_target,ramp_bias=True)
            name=group+'.npz';np.savez_compressed(out/name,**trace)
            rows.append(dict(context=job['id'],group=group,trace=name,**stats))
        write(out/'results.json',dict(execution_domain='VALIDATION_SIM',job=job,rows=rows))
        return rows
    finally:r.env.close()


def stage4(root,plan):
    gains_bundle=json.loads((root/'gains_frozen.json').read_text())['models']
    out=root/'entry';out.mkdir()
    jobs=[dict(id=f'entry_s{seed}_p{pitch:+.3f}',seed=seed,pitch=pitch,pitch_index=i)
        for seed in [270,271] for i,pitch in enumerate([-.035,0.,.035])]
    cfg=json.loads(prepared_config(CKPT).read_text())
    rows=[r for group in parallel(entry_job,jobs,plan['workers'],cfg,str(out),gains_bundle) for r in group]
    bases={r['context']:r for r in rows if r['group']=='bias_only'}
    checks={group:all(r['complete'] and r['last5_base_speed_RMS']<=.0002 and
        r['last5_base_position_range']<=.005 and r['max_planar_drift']<=.8*bases[r['context']]['max_planar_drift']
        for r in rows if r['group']==group) for group in ['M4','M5']}
    write(root/'entry_metrics.json',dict(execution_domain='VALIDATION_SIM',rows=rows))
    return dict(gate=all(checks.values()),models=checks,runs=len(rows),duration_s=60,
        note='Early drift state may lie outside local training range; support fractions retained. No gain retuning.')


def mismatch_job(job,cfg,output,fresh,gain_bundle):
    out=Path(output)/job['id'];out.mkdir();rows=[]
    source=job['source_job'];tick=50000
    for group in ['A','bias_only','F1','M4','M5']:
        r=EffectRunner(cfg,source)
        try:
            with gzip.open(Path(fresh)/source['id']/f'snapshot_t{tick}.pkl.gz','rb') as f:r.restore(pickle.load(f))
            effect=job['effect']
            if 'mass' in effect:
                q=r.env.data.qpos.copy();v=r.env.data.qvel.copy()
                r.env.model.body_mass[1:]*=effect['mass'];r.env.model.body_inertia[1:]*=effect['mass']
                scratch=r.env.mujoco.MjData(r.env.model)
                r.env.mujoco.mj_setConst(r.env.model,scratch)
                np.testing.assert_array_equal(r.env.data.qpos,q);np.testing.assert_array_equal(r.env.data.qvel,v)
            r.enable_effect(effect)
            pre=anchor(r);p_target=float(r.observation['sensor'][0])
            trace,stats=rollout_control(r,group,gain_bundle.get(group),60.,pre,p_target)
            name=group+'.npz';np.savez_compressed(out/name,**trace)
            rows.append(dict(context=source['id'],condition=job['condition'],effect=effect,group=group,trace=name,**stats))
        finally:r.env.close()
    write(out/'results.json',dict(execution_domain='VALIDATION_SIM',job=job,rows=rows))
    return rows


def stage5(root,plan):
    gains_bundle=json.loads((root/'gains_frozen.json').read_text())['models']
    source_jobs=json.loads((root/'fresh/manifest.json').read_text())['jobs']
    effects=[('mass1.15',{'mass':1.15}),('mass1.30',{'mass':1.30}),('gain0.8',{'gain':.8}),
        ('gain1.2',{'gain':1.2}),('lag0.02',{'lag':.02}),('lag0.05',{'lag':.05})]
    jobs=[dict(id=f"{source['id']}_{name}",source_job=source,condition=name,effect=effect)
        for source in source_jobs for name,effect in effects]
    out=root/'mismatch';out.mkdir();cfg=json.loads(prepared_config(CKPT).read_text())
    rows=[r for group in parallel(mismatch_job,jobs,plan['workers'],cfg,str(out),str(root/'fresh'),gains_bundle) for r in group]
    bases={(r['context'],r['condition']):r for r in rows if r['group']=='bias_only'}
    checks={}
    for group in ['M4','M5']:
        selected=[r for r in rows if r['group']==group]
        checks[group]=all(r['complete'] and bases[(r['context'],r['condition'])]['complete'] and
            r['base']['IAE']<=bases[(r['context'],r['condition'])]['base']['IAE'] for r in selected)
    write(root/'mismatch_metrics.json',dict(execution_domain='VALIDATION_SIM',rows=rows))
    return dict(gate=all(checks.values()),models=checks,runs=len(rows),conditions=[n for n,_ in effects],
        duration_s=60,mass='all non-world body mass/inertia scaled; initial qpos/qvel preserved',
        motor='wheel only, physical-substep gain/first-order lag after residual addition and saturation',
        online_updates=0)
