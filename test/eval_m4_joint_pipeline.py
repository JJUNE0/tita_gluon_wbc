"""VALIDATION_SIM / DESKTOP_DRY_RUN: independent E0--E7 and conditional live tests.

All outputs are new experimental artifacts. Production code and previous results
remain immutable. Each arm has separate admissibility and performance gates.
"""
import argparse
import copy
from collections import deque
import gzip
import hashlib
import json
from pathlib import Path
import pickle
import subprocess
import sys
import fcntl
import shutil
import ast

import numpy as np

from m4_joint_adaptation import (MASKS,JointEstimator,Command,advance,offset,predicted_bias,LOW,HIGH,DT,BIAS)
from diagnose_m4_adaptive_causes import (OLD,COLD,arrays,nominal,fixed_gain,replay,protected,verify)
from m4_shadow_stages import ShadowRunner,reproduce,prediction_gate,IX
from m4_mismatch_stages import apply_physics_effect,PREVIOUS
from flash_overnight_model_stages import (REPO,CKPT,KEYS,current,parallel,prepared_config,write,sha256)
from flash_overnight_control_stages import anchor,physical_paths
from analyze_flash_state_learning import state
from eval_flash_stop_release import inputs_for

SHADOW=OLD/'shadow_run/shadow'
EFFECTS={'nominal':{},'gain0.8':{'gain':.8},'gain1.2':{'gain':1.2}}
FAMILIES=['validation_sine','validation_prbs','pulse_pos','pulse_neg','step_pos','step_neg','bipulse_pos','bipulse_neg']


def save_snapshot(path,r,**metadata):
    with gzip.open(path,'wb',compresslevel=1) as stream:pickle.dump(dict(snapshot=r.effect_snapshot(),**metadata),stream)


def load_snapshot(path):
    with gzip.open(path,'rb') as stream:return pickle.load(stream)


def trace_from(states,steps,extra):
    result={k:np.asarray([s[k] for s in states]) for k in KEYS}
    if steps:result.update({k:np.asarray([s[k] for s in steps]) for k in steps[0]})
    if extra:result.update({k:np.asarray([s[k] for s in extra]) for k in extra[0]})
    return result


def measured(r,target):
    z=current(r)[IX].copy();z[0]-=target;return z


def collect(r,duration,target,pre,K,bias,reference,learner=None,probe=None,change=None,previous=BIAS):
    command=Command(previous);states=[];steps=[];extra=[];n=round(duration/DT)
    # Only the simulator wrapper receives the change schedule; the learner has
    # no access to this callback, the effect value, GT or any robot object.
    for i in range(n+1):
        states.append({key:r.observation[key].copy() for key in KEYS});failure=r.failures()
        if failure or i==n:break
        if change is not None and i==change[0]:r.effect['gain']=change[1]
        z=measured(r,target)
        k,b,ref=learner.values() if learner is not None else (np.asarray(K),bias,np.asarray(reference))
        u,log=command.compute(z,k,b,ref,0. if probe is None else probe[i])
        tr=r.step(u);steps.append(tr);extra.append(log)
        if learner is not None:
            learner.observe(z,tr['actual_u'],measured(r,target),log['global_clipped'])
        assert abs(tr['actual_u']-u)<1e-6
        assert np.max(abs(tr['physical_motor'][:,[3,7]]))<=12.000001
    trace=trace_from(states,steps,extra)
    if steps:
        np.testing.assert_array_equal(trace['previous_action'][:-1],trace['history'])
        np.testing.assert_array_equal(trace['previous_action'][1:],trace['action'])
        assert np.max(abs(np.diff(np.r_[previous,trace['requested_u']])))<=.040000001
    trace['base_path'],trace['axle_path']=physical_paths(trace,pre)
    trace['base_path']+=pre.get('base_path_offset',0.);trace['axle_path']+=pre.get('axle_path_offset',0.)
    trace['sensor_error']=trace['sensor'].copy();trace['sensor_error'][:,0]-=target
    trace['goal_base_position']=np.asarray(pre.get('goal_base_position',pre['base_position'])).copy()
    return trace,dict(complete=not failure and len(steps)==n,failure=failure,duration_s=len(steps)*DT,
        target_sensor=float(target),metrics=metrics(trace,duration,not failure and len(steps)==n),
        accepted={} if learner is None else learner.accepted,paused=0 if learner is None else learner.paused)


def metrics(trace,duration,complete,start=0.):
    if not complete:return None
    t=np.arange(len(trace['sensor']))*DT;window=t>=start;tail=(t>=duration-5.)&(t<duration)
    base=trace['base_path'];sensor=trace['sensor_error'][:,0];nominal_pitch=fixed_gain()['reference'][2]
    return dict(base_IAE=float(np.trapz(abs(base[window]),t[window])),
        last5_base_RMSE=float(np.sqrt(np.mean(base[tail]**2))),last5_sensor_RMSE=float(np.sqrt(np.mean(sensor[tail]**2))),
        last5_midpoint_RMSE=float(np.sqrt(np.mean(trace['axle_path'][tail]**2))),
        last5_base_speed_RMS=float(np.sqrt(np.mean(trace['base_velocity'][tail]**2))),
        max_planar=float(max(np.linalg.norm(trace['base_position'][window,:2]-trace['goal_base_position'][:2],axis=1))),
        pitch_RMS=float(np.sqrt(np.mean((trace['sensor'][window,2]-nominal_pitch)**2))),
        wheel_RMS=float(np.sqrt(np.mean(trace['physical_motor'][window[:-1]][:,:,[3,7]]**2))),
        yaw_change=float(np.unwrap(trace['rpy'][:,2])[-1]-trace['rpy'][0,2]),
        raw_saturation_fraction=float(np.mean((trace['pre_global_clip']<LOW)|(trace['pre_global_clip']>HIGH))),
        actual_at_bound_fraction=float(np.mean((trace['actual_u']<=LOW+1e-7)|(trace['actual_u']>=HIGH-1e-7))),
        recovery_s=recovery_time(t,base,trace['base_velocity'][:,0],start),
        sensor_base_gap_last5=float(np.mean(sensor[tail]-base[tail])))


def recovery_time(t,p,v,start):
    good=(abs(p)<=.001)&(abs(v)<=.0002);n=250
    indices=np.flatnonzero((t>=start+(n-1)*DT-1e-9)&(np.convolve(good.astype(int),np.ones(n,dtype=int),'full')[:len(t)]==n))
    return None if not len(indices) else float(max(0.,t[indices[0]-n+1]-start))


def init_effect(cfg,job,snapshot,effect):
    r=ShadowRunner(cfg,job)
    apply_physics_effect(r,effect);r.enable_effect(copy.deepcopy(effect));r.effect_restore(snapshot)
    return r


def legacy_job(item,cfg,out):
    r=ShadowRunner(cfg,item['test'])
    try:
        reproduce(r,item['test'],OLD/'run');prefix=arrays(COLD/item['id']/'common_identification_prefix.npz')
        replay(r,prefix);snapshot=r.effect_snapshot()
        for name in ['M4','Adaptive_M4']:
            r.effect_restore(snapshot);replay(r,arrays(COLD/item['id']/(name+'.npz')))
        result=dict(id=item['id'],state_action_history_observation_physics_torque_exact=True)
        write(Path(out)/(item['id']+'.json'),result);return result
    finally:r.env.close()


def train_job(item,cfg,out):
    folder=Path(out)/item['id'];folder.mkdir();source=SHADOW/item['id']
    old=json.loads((source/'results.json').read_text());job=old['pair']['train']
    trace=arrays(source/'training.npz');z=state(trace);z[:,0]-=z[0,0]
    r=ShadowRunner(cfg,job)
    try:
        reproduce(r,job,OLD/'run');replay(r,trace);snapshot=r.effect_snapshot()
        limits=r.env.model.jnt_range[r.leg_joints].copy()
        estimators={method:JointEstimator((1,1,1),method,limits) for method in ['B1','B2']}
        for i,u in enumerate(trace['actual_u']):
            clipped=bool(u<=LOW+1e-7 or u>=HIGH-1e-7)
            for learner in estimators.values():learner.observe(z[i],u,z[i+1],clipped)
        primary=estimators['B1'];model=primary.rls.model();ref=primary.reference_goal
        frozen=dict(id=item['id'],condition=item['condition'],pitch=item['pitch'],train_seed=job['seed'],
            model=model,K=primary.K.tolist(),reference=(primary.reference if ref is None else ref).tolist(),
            bias={method:learner.bias for method,learner in estimators.items()},
            components=dict(K=primary.accepted['K']>0,reference=ref is not None,
                B1_bias=primary.accepted['bias']>0,B2_bias=estimators['B2'].accepted['bias']>0),
            information=primary.rls.diagnostics(),accepted={method:learner.accepted for method,learner in estimators.items()},
            source_sha256=sha256(source/'training.npz'),nominal_regression_center=primary.rls.ref.tolist(),
            low=z[:,1:].min(0).tolist(),high=z[:,1:].max(0).tolist(),leg_limits=limits.tolist(),
            effective_offsets={method:offset(primary.K,learner.bias,primary.reference if ref is None else ref)
                for method,learner in estimators.items()},no_GT_or_effect_label_in_estimators=True)
        write(folder/'frozen_before_validation.json',frozen);h=sha256(folder/'frozen_before_validation.json')
        validations={}
        for method,value in [('nominal',BIAS)]+[(name,learner.bias) for name,learner in estimators.items()]:
            if method=='B2':
                # A candidate is always made explicit at the common endpoint;
                # online shadow rejection is not silently relabelled success.
                # No validation/evaluation future enters its model or state.
                candidate,details=predicted_bias(model,z[-1],np.asarray(fixed_gain()['K']),
                    np.asarray(fixed_gain()['reference']),value,float(trace['actual_u'][-1]))
                baseline_valid=validations['nominal']['model_valid'] and frozen['information']['gate']
                value=float(candidate) if baseline_valid and details['gate'] else float(value)
                frozen['B2_endpoint_candidate']=dict(prediction=details,baseline_model_valid=baseline_valid,
                    prior_shadow_accepted=estimators['B2'].accepted['bias'],candidate=value)
                frozen['bias']['B2']=value
            r.effect_restore(snapshot);previous=float(trace['actual_u'][-1]);inputs=[]
            for i in range(1000):previous=float(np.clip(value,previous-.04,previous+.04));inputs.append(previous)
            response,fail=r.rollout(inputs);np.savez_compressed(folder/('constant_'+method+'.npz'),**response)
            actual=state(response);pred=actual[0].copy();errors=[]
            # Preserve the source estimator's position coordinates.
            anchor_p=float(trace['sensor'][0,0]);actual[:,0]-=anchor_p;pred=actual[0].copy()
            for i,u in enumerate(response['actual_u'][:100]):
                pred=advance(model,pred,u);errors.append(pred[:2]-actual[i+1,:2])
            rmse=np.sqrt(np.mean(np.asarray(errors)**2,axis=0)) if len(errors)==100 else np.array([1.,1.])
            tail=response['sensor'][-250:,1]
            validations[method]=dict(complete=not fail,first2s_pv_RMSE=rmse.tolist(),
                sensor_last5_mean_speed=float(tail.mean()),base_last5_mean_speed=float(response['base_velocity'][-250:].mean()),
                actual_constant_input=float(value),model_valid=bool(not fail and np.all(rmse<=[.00002,.00002])))
        assert sha256(folder/'frozen_before_validation.json')==h
        frozen['constant_validation']=validations
        frozen['components']['B1_bias']=bool(frozen['components']['B1_bias'] and validations['B1']['complete'])
        frozen['components']['B2_bias']=bool(frozen['B2_endpoint_candidate']['baseline_model_valid']
            and frozen['B2_endpoint_candidate']['prediction']['gate'] and validations['B2']['model_valid'])
        frozen['effective_offsets']['B2']=offset(primary.K,frozen['bias']['B2'],primary.reference if ref is None else ref)
        write(folder/'frozen.json',frozen)
        for method,learner in estimators.items():
            write(folder/('events_'+method+'.json'),dict(events=learner.events,models=learner.models))
        print('[VALIDATION_SIM] train',item['id'],frozen['components'],flush=True)
        return dict(id=item['id'],condition=item['condition'],frozen_sha256=sha256(folder/'frozen.json'),components=frozen['components'])
    finally:r.env.close()


def acquire_job(job,cfg,out):
    folder=Path(out)/job['id'];folder.mkdir();r=ShadowRunner(cfg,job);r.enable_effect({})
    try:
        for i in range(400):
            if i>=50:assert not r.failures()
            r.step(0.)
        states=deque(maxlen=12001);steps=deque(maxlen=12000);u=0.
        for i in range(45001):
            assert not r.failures(),(job,i,r.failures())
            states.append({k:r.observation[k].copy() for k in KEYS})
            if i<45000:
                u=float(np.clip(BIAS,u-.04,u+.04));steps.append(r.step(u))
        window=trace_from(list(states),list(steps),[]);np.savez_compressed(folder/'qualification.npz',**window)
        tail=window['base_velocity'][-9000:];qual=bool(np.sqrt(np.mean(tail**2))<=.0005)
        save_snapshot(folder/'snapshot.pkl.gz',r)
        result=dict(job=job,complete=True,low_speed_qualification=qual,base_speed_RMS=float(np.sqrt(np.mean(tail**2))),
            sensor_speed_RMS=float(np.sqrt(np.mean(window['sensor'][-9000:,1]**2))),snapshot_sha256=sha256(folder/'snapshot.pkl.gz'))
        write(folder/'results.json',result);print('[VALIDATION_SIM] new seed',job['id'],qual,flush=True);return result
    finally:r.env.close()


def test_model(r,snapshot,frozen,out,hold,seed):
    r.effect_restore(snapshot);base,fail=r.rollout(np.full(200,hold))
    if fail:
        result=dict(gate=False,reason='physical_baseline_failure',failure=fail)
        write(out/'independent_prediction.json',result);return result
    np.savez_compressed(out/'probe_baseline.npz',**base);data=[];inputs=[]
    for i,family in enumerate(FAMILIES):
        request=np.clip(hold+inputs_for(family,.01,seed+i,200),LOW,HIGH)
        r.effect_restore(snapshot);response,fail=r.rollout(request)
        if fail:
            result=dict(gate=False,reason='physical_probe_failure',family=family,failure=fail)
            np.savez_compressed(out/('probe_'+family+'.npz'),**response)
            write(out/'independent_prediction.json',result);return result
        np.testing.assert_array_equal(response['action'][0],base['action'][0])
        data.append(state(response)-state(base));inputs.append(response['actual_u']-base['actual_u'])
        np.savez_compressed(out/('probe_'+family+'.npz'),**response)
    direct=[]
    for sign in [1.,-1.]:
        r.effect_restore(snapshot);response,fail=r.rollout([float(np.clip(hold+sign*.005,LOW,HIGH))]);assert not fail;direct.append(response)
    B=(state(direct[0])[1]-state(direct[1])[1])/(direct[0]['actual_u'][0]-direct[1]['actual_u'][0])
    result=prediction_gate(dict(frozen['model'],indices=list(range(24))),data,inputs,float(B[1]))
    write(out/'independent_prediction.json',result);return result


def factorial_job(job,cfg,root):
    root=Path(root);out=root/'factorial'/job['id'];out.mkdir()
    fpath=root/'training'/job['training_id']/'frozen.json';f=json.loads(fpath.read_text());fhash=sha256(fpath)
    sfile=root/'acquisition'/job['source_id']/'snapshot.pkl.gz';snapshot=load_snapshot(sfile)['snapshot']
    r=init_effect(cfg,job,snapshot,EFFECTS[job['condition']]);rows=[]
    try:
        # Same original goal throughout the common prefix, validation and arms.
        target=float(r.observation['sensor'][0]);pre=anchor(r)
        probe=inputs_for('train_prbs',.02,job['seed']+job['pitch_index']*71+9281,3000)
        prefix,stats=collect(r,60.,target,pre,fixed_gain()['K'],BIAS,np.asarray(fixed_gain()['reference']),probe=probe)
        np.savez_compressed(out/'common_prefix.npz',**prefix);assert stats['complete']
        common=r.effect_snapshot();pre=anchor(r);pre.update(base_path_offset=float(prefix['base_path'][-1]),
            axle_path_offset=float(prefix['axle_path'][-1]),goal_base_position=prefix['base_position'][0].copy())
        previous=float(prefix['actual_u'][-1]);save_snapshot(out/'common_snapshot.pkl.gz',r,target=target,pre=pre,previous=previous)
        prediction=test_model(r,common,f,out,previous,job['seed']*37+job['pitch_index'])
        first=current(r).copy() # Replaced below by a restore before each branch.
        first_action=None;first_observation=None
        variants=[('B1',name) for name in MASKS]+[('B2',name) for name,mask in MASKS.items() if mask[1]]
        for method,name in variants:
            mask=MASKS[name];missing=[]
            if mask[0] and not (f['components']['K'] and prediction['gate']):missing.append('K_model_gate')
            if mask[1] and not f['components'][method+'_bias']:missing.append(method+'_bias_gate')
            if mask[2] and not f['components']['reference']:missing.append('reference_gate')
            if missing:
                rows.append(dict(group=name,method=method,status='NOT_TESTED',reason=missing));continue
            r.effect_restore(common)
            K=f['K'] if mask[0] else fixed_gain()['K'];b=f['bias'][method] if mask[1] else BIAS
            ref=np.asarray(f['reference'] if mask[2] else fixed_gain()['reference'])
            response,stats=collect(r,60.,target,pre,K,b,ref,previous=previous)
            file=method+'_'+name+'.npz';np.savez_compressed(out/file,**response)
            if first_action is None:first_action=response['action'][0];first_observation=response['policy_observation'][0]
            np.testing.assert_array_equal(response['action'][0],first_action)
            np.testing.assert_array_equal(response['policy_observation'][0],first_observation)
            rows.append(dict(group=name,method=method,status='PASS' if stats['complete'] else 'FAIL',trace=file,
                K=K,bias=b,reference=ref.tolist(),effective_offset=offset(K,b,ref),**stats))
        assert sha256(fpath)==fhash
        result=dict(job=job,rows=rows,frozen_sha256=fhash,independent_model_gate=prediction['gate'],
            evaluation_seed_not_in_training=job['seed']!=f['train_seed'],target_fixed_through_prefix=True)
        write(out/'results.json',result);print('[VALIDATION_SIM] factorial',job['id'],len(rows),flush=True);return result
    finally:r.env.close()


def compare(rows,baseline):
    if not rows or len(rows)!=len(baseline) or any(not r.get('complete') for r in rows+baseline):
        return dict(admissible=False,performance=False,reason='missing_or_incomplete')
    physical=all(r['metrics']['pitch_RMS']<=max(1.25*b['metrics']['pitch_RMS'],.002)
        and r['metrics']['wheel_RMS']<=1.25*b['metrics']['wheel_RMS'] for r,b in zip(rows,baseline))
    model_gate=all(not r.get('requires_model_validation',False) or r.get('model_independent_gate',False) for r in rows)
    stable=physical and model_gate
    ratio=float(np.median([r['metrics']['base_IAE'] for r in rows])/max(np.median([r['metrics']['base_IAE'] for r in baseline]),1e-12))
    tail=float(np.median([r['metrics']['last5_base_RMSE'] for r in rows])/max(np.median([r['metrics']['last5_base_RMSE'] for r in baseline]),1e-12))
    wins=sum(r['metrics']['base_IAE']<b['metrics']['base_IAE'] for r,b in zip(rows,baseline))
    return dict(admissible=stable,physical_stable=physical,model_gate=model_gate,
        performance=bool(stable and ratio<=.95 and tail<=1.2 and wins>=np.ceil(2*len(rows)/3)),
        IAE_ratio=ratio,last5_RMSE_ratio=tail,paired_wins=wins,count=len(rows))


def stage_decision(root,phase):
    results=json.loads((root/(phase+'_results.json')).read_text())['rows'];conditions={}
    for condition in EFFECTS:
        selected=sorted([r for r in results if r['job']['condition']==condition],key=lambda r:r['job']['id'])
        if not selected:continue
        baseline=[next(x for x in r['rows'] if x['group']=='E0' and x['method']=='B1') for r in selected]
        arms={}
        names=sorted({(x['method'],x['group']) for r in selected for x in r['rows']})
        for method,name in names:
            rows=[next((x for x in r['rows'] if x['group']==name and x['method']==method),{}) for r in selected]
            arms[method+'_'+name]=compare(rows,baseline)
        conditions[condition]=arms
    decision=dict(phase=phase,conditions=conditions,
        rule='Each arm independent: stable and >=5% base IAE improvement, tail RMSE<=120%, >=2/3 paired wins. '
            'Stable failed-performance arms may remain explicit comparators, never promoted as successful.')
    write(root/(phase+'_decision.json'),decision);return decision


def online_job(job,cfg,root):
    root=Path(root);out=root/'online'/job['id'];out.mkdir()
    f=json.loads((root/'training'/job['training_id']/'frozen.json').read_text())
    bundle=load_snapshot(root/'factorial'/job['id']/'common_snapshot.pkl.gz')
    r=init_effect(cfg,job,bundle['snapshot'],EFFECTS[job['condition']]);rows=[]
    try:
        decision=json.loads((root/'factorial_decision.json').read_text())['conditions'][job['condition']]
        selected=[('B1','E0')]
        for label,gate in decision.items():
            method,name=label.split('_')
            if name!='E0' and gate['performance']:selected.append((method,name))
        # Stable K-only/bias-only are retained as explicit controls when another
        # arm passed, so absence of their improvement cannot hide the comparison.
        if len(selected)>1:
            for name in ['E1','E2','E6','E7']:
                label='B1_'+name
                if decision.get(label,{}).get('admissible') and ('B1',name) not in selected:selected.append(('B1',name))
        prefix=arrays(root/'factorial'/job['id']/'common_prefix.npz');z=state(prefix);z[:,0]-=bundle['target']
        for method,name in selected:
            r.effect_restore(bundle['snapshot']);learner=None
            if name!='E0':
                learner=JointEstimator(MASKS[name],method,np.asarray(f['leg_limits']))
                # Warm only from this controller's COMMON past sensor prefix.
                for i,u in enumerate(prefix['actual_u']):
                    learner.rls.update(z[i],u,z[i+1])
                learner.seed_history(z,prefix['actual_u'])
                learner.information=learner.rls.diagnostics()
                # All online parameters start nominal to measure causal adaptation.
            response,stats=collect(r,120.,bundle['target'],bundle['pre'],fixed_gain()['K'],BIAS,
                np.asarray(fixed_gain()['reference']),learner=learner,previous=bundle['previous'])
            file=method+'_'+name+'.npz';np.savez_compressed(out/file,**response)
            if learner is not None:
                write(out/(method+'_'+name+'_updates.json'),dict(events=learner.events,models=learner.models,
                    accepted=learner.accepted,regression_center=learner.rls.ref.tolist(),final_model=learner.rls.model()))
                probe_folder=out/(method+'_'+name+'_final_prediction');probe_folder.mkdir()
                check=test_model(r,r.effect_snapshot(),dict(model=learner.rls.model()),probe_folder,
                    float(response['actual_u'][-1]),job['seed']*139+int(name[1:]))
                stats['requires_model_validation']=bool(MASKS[name][0] or (method=='B2' and MASKS[name][1]))
                stats['model_independent_gate']=check['gate']
            rows.append(dict(group=name,method=method,trace=file,**stats))
        result=dict(job=job,rows=rows,target_unchanged=True,no_GT_in_learning=True)
        write(out/'results.json',result);print('[VALIDATION_SIM] live',job['id'],len(rows),flush=True);return result
    finally:r.env.close()


def shock_job(job,cfg,root):
    root=Path(root);out=root/'shock'/job['id'];out.mkdir()
    basejob=dict(job,condition='nominal');snapshot=load_snapshot(root/'acquisition'/job['source_id']/'snapshot.pkl.gz')['snapshot']
    r=init_effect(cfg,job,snapshot,{})
    try:
        target=float(r.observation['sensor'][0]);pre=anchor(r)
        noise=inputs_for('train_prbs',.02,job['seed']+9819,3000)
        prefix,stats=collect(r,60.,target,pre,fixed_gain()['K'],BIAS,np.asarray(fixed_gain()['reference']),probe=noise)
        assert stats['complete'];np.savez_compressed(out/'nominal_prefix.npz',**prefix)
        common=r.effect_snapshot();pre=anchor(r);pre.update(base_path_offset=float(prefix['base_path'][-1]),
            axle_path_offset=float(prefix['axle_path'][-1]),goal_base_position=prefix['base_position'][0].copy())
        decision=json.loads((root/'online_decision.json').read_text())['conditions'].get(job['condition'],{})
        rows=[];groups=['E0','E1','E2','E6','E7']
        admissible=[name for name in groups if name=='E0' or decision.get('B1_'+name,{}).get('admissible')]
        for name in admissible:
            r.effect['gain']=1.;r.effect_restore(common);learner=None
            if name!='E0':
                learner=JointEstimator(MASKS[name],'B1',r.env.model.jnt_range[r.leg_joints].copy())
                z=state(prefix);z[:,0]-=target
                for i,u in enumerate(prefix['actual_u']):learner.rls.update(z[i],u,z[i+1])
                learner.seed_history(z,prefix['actual_u']);learner.information=learner.rls.diagnostics()
            response,stats=collect(r,160.,target,pre,fixed_gain()['K'],BIAS,np.asarray(fixed_gain()['reference']),
                learner=learner,previous=float(prefix['actual_u'][-1]),change=(2000,job['change_gain']))
            stats['post_change_metrics']=metrics(response,160.,stats['complete'],40.)
            stats['pre_change_metrics']=dict(base_RMSE=float(np.sqrt(np.mean(response['base_path'][:2000]**2))))
            stats['pre_change_qualified']=bool(stats['complete'] and np.max(abs(response['base_path'][1750:2000]))<=.001
                and np.sqrt(np.mean(response['base_velocity'][1750:2000]**2))<=.0002)
            np.savez_compressed(out/(name+'.npz'),**response)
            if learner is not None:write(out/(name+'_updates.json'),dict(events=learner.events,models=learner.models,accepted=learner.accepted))
            rows.append(dict(group=name,method='B1',trace=name+'.npz',**stats))
        result=dict(job=job,rows=rows,change_time_s=40.,after_change_s=120.,
            simulator_only_change_schedule=True,target_never_reset=True)
        write(out/'results.json',result);print('[VALIDATION_SIM] shock',job['id'],len(rows),flush=True);return result
    finally:r.env.close()


def make_plan(root,workers,smoke=False):
    assert root.is_relative_to(REPO/'docs/exp') and not root.exists();root.mkdir(parents=True)
    protection=protected()
    old=json.loads((REPO/'docs/exp/2026-10-16/m4_bias_reference_abc_v2/plan.json').read_text());protection.update(old['protected_sha256'])
    for base in ['m4_bias_reference_abc_v2','m4_adaptive_cause_diagnostics']:
        for p in (REPO/'docs/exp/2026-10-16'/base).rglob('*'):
            if p.is_file():protection[str(p.relative_to(REPO))]=sha256(p)
    for p in (REPO/'docs/exp/2026-10-16').glob('*summary.md'):
        if p.name!='m4_joint_operating_adaptation_summary.md':protection[str(p.relative_to(REPO))]=sha256(p)
    training=[]
    for condition in EFFECTS:
        for pitch in [-.035,0.,.035]:training.append(dict(id=f'settled_{condition}_p{pitch:+.3f}',condition=condition,pitch=pitch))
    acquire=[dict(id=f's{seed}_p{pitch:+.3f}',seed=seed,pitch=pitch,pitch_index=i)
        for seed in [420,421] for i,pitch in enumerate([-.035,0.,.035])]
    jobs=[]
    for source in acquire:
        for condition in EFFECTS:jobs.append(dict(source,id=source['id']+'_'+condition,source_id=source['id'],
            condition=condition,training_id=f"settled_{condition}_p{source['pitch']:+.3f}"))
    if smoke:
        training=[i for i in training if i['condition']=='gain0.8' and i['pitch']==0.]
        acquire=[i for i in acquire if i['seed']==420 and i['pitch']==0.]
        jobs=[i for i in jobs if i['condition']=='gain0.8' and i['seed']==420 and i['pitch']==0.]
    sources=[REPO/'test'/name for name in ['m4_joint_adaptation.py','eval_m4_joint_pipeline.py']]
    plan=dict(execution_domain='VALIDATION_SIM',workers=workers,smoke=smoke,training=training,acquisition=acquire,jobs=jobs,
        protected_sha256=protection,source_sha256={str(p.relative_to(REPO)):sha256(p) for p in sources},
        checkpoint_sha256=sha256(CKPT/'actor.pt'),objective_attachment_sha256=sha256(Path('/home/cocel/.codex/attachments/a56c081f-3031-4a01-a4d8-eef8f778d7a7/pasted-text-1.txt')),
        tracked_diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest(),
        training_seed=260,evaluation_seeds=[420,421],new_nominal_acquisition_s=900.,
        train='Exact replay original Fixed+probe60s; nominal RLS prior; B1/B2/reference shadow estimates; no GT or condition label input',
        A1='B1 position integral gain0.5Nm/(m*s), rate0.0005Nm/s,1s; '
            'B2 finite2s model prediction candidate +/-0.001Nm, max0.0005Nm/1s online; '
            'explicit common-endpoint candidate after model baseline validation, actual constant20s response validation; '
            'reference observed20s quiet mean every10s; position/velocity fixed; target support and nominal bounds',
        A2='E0--E7 B1 plus bias-containing B2 comparison arms; same full test snapshot; independent seeds; parameters frozen;60s',
        B1='Conditional120s online; RLS20ms, K candidate5s validated next2s; bias1s; reference candidate10s with smooth bounded interpolation',
        C1='Conditional160s: nominal40s then hidden simulator gain change0.8/1.2 for120s; no reset; five stable comparators',
        D1='Future extension; mass/50ms lag remain shadow-only, no full adaptive authorization here',E1='No hardware deployment or real robot commands',
        gain_guard='per-update25% AND immutable nominal cumulative25%, blend0.1, raw K jump<=0.003Nm, joint jump<=0.005Nm, rho<1, model2s p/v RMSE<=0.02mm/0.02mm/s',
        reference_guard='target inside observed window, nominal component limits; application interpolates from validated nominal/reference toward target; joint raw jump<=0.005Nm',
        limits=dict(total=[LOW,HIGH],slew=2.,wheel_cap=12.,ramp=1.5,
            equation='After activation: clip(bias - K@(z-reference), nominal_bias +/-0.05); no extra feedback cap'),
        model_support='All24 sensor coordinates within fixed nominal-centered operational envelope; '
            'reference targets in observed20s support; independent response validation still required',
        performance='per arm:6/6complete,pitch<=max(1.25fixed,0.002rad),wheel<=1.25fixed, medianbaseIAE<=95%fixed, tailRMSE<=120%fixed,>=4/6pairedwins',
        independent_model='matched4s probes8families, amplitude0.01Nm, first2/rolling0.1/0.5/1/2s p/v medians<=30%, directB_v error<=30%',
        recovery='within +/-1mm base sagittal and +/-0.2mm/s for continuous5s; report missing recovery as null, never zero',
        no_parameter_search=True,no_policy_retraining=True)
    write(root/'plan.json',plan);return plan


def recover_completed_data(root,source):
    """Only explicit terminal-error recovery; never restart a RUNNING stage."""
    old=json.loads((source/'pipeline_state.json').read_text())
    assert old['status']=='ERROR' and old['stages']['factorial']['status']=='ERROR'
    old_plan=json.loads((source/'plan.json').read_text());new_plan=json.loads((root/'plan.json').read_text())
    assert old_plan['tracked_diff_sha256']==new_plan['tracked_diff_sha256']
    assert sha256(REPO/'test/m4_joint_adaptation.py')==old_plan['source_sha256']['test/m4_joint_adaptation.py']
    before=ast.parse((source/'collector.source.txt').read_text());after=ast.parse(Path(__file__).read_text())
    methods=['legacy_job','train_job','acquire_job','collect','factorial_job','online_job','shock_job','test_model']
    for method in methods:
        a=next(x for x in before.body if isinstance(x,ast.FunctionDef) and x.name==method)
        b=next(x for x in after.body if isinstance(x,ast.FunctionDef) and x.name==method)
        assert ast.dump(a)==ast.dump(b),method
    changed_sources={'test/eval_m4_joint_pipeline.py','test/test_m4_joint_adaptation.py'}
    for name,h in old_plan['protected_sha256'].items():
        if name not in changed_sources:assert sha256(REPO/name)==h,name
    copied={}
    for stage,folder in [('legacy','legacy'),('train','training'),('acquire','acquisition')]:
        record=old['stages'][stage];assert record['status']=='TESTED'
        assert sha256(source/record['artifact'])==record['sha256']
        shutil.copytree(source/folder,root/folder)
        shutil.copy2(source/record['artifact'],root/record['artifact'])
        for p in (source/folder).rglob('*'):
            if p.is_file():
                name=p.relative_to(source);h=sha256(p);assert sha256(root/name)==h;copied[str(name)]=h
    assert len(json.loads((root/'acquire_results.json').read_text())['rows'])==len(new_plan['acquisition'])
    write(root/'recovery.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',source=str(source),
        terminal_source_status=old['status'],unchanged_control_and_training_AST=methods,
        estimator_source_unchanged=True,metrics_mask_repair_only_for_physical_results=True,copied_sha256=copied,
        no_failed_factorial_results_reused=True))


def coordinator(root,args):
    make_plan(root,args.workers,args.smoke)
    if args.recover_from is not None:recover_completed_data(root,args.recover_from.resolve())
    with (root/'coordinator.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        ledger=dict(execution_domain='VALIDATION_SIM',status='RUNNING',smoke=args.smoke,stages={})
        stages=['legacy','train','acquire','factorial','online','shock']
        for stage in stages[:stages.index(args.through)+1]:
            if args.recover_from is not None and stage in ['legacy','train','acquire']:
                artifact=root/(stage+'_results.json')
                ledger['stages'][stage]=dict(status='TESTED',artifact=artifact.name,sha256=sha256(artifact),hash_verified_reuse=True)
                write(root/'pipeline_state.json',ledger);continue
            ledger['stages'][stage]=dict(status='RUNNING');write(root/'pipeline_state.json',ledger)
            with (root/(stage+'.log')).open('w') as log:
                result=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--root',str(root),
                    '--stage',stage,'--workers',str(args.workers)],stdout=log,stderr=subprocess.STDOUT)
            artifact=root/(stage+'_results.json')
            if result.returncode:
                ledger['stages'][stage]=dict(status='ERROR',returncode=result.returncode)
                ledger['status']='ERROR';write(root/'pipeline_state.json',ledger)
                raise RuntimeError('Stage execution failed: '+stage)
            value=json.loads(artifact.read_text())
            ledger['stages'][stage]=dict(status=value.get('status','COMPLETE'),artifact=artifact.name,sha256=sha256(artifact))
            write(root/'pipeline_state.json',ledger)
            print('[VALIDATION_SIM] coordinator completed',stage,flush=True)
        ledger['status']='COMPLETE';ledger['note']='Workflow completion is not research performance PASS.'
        write(root/'pipeline_state.json',ledger)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--stage',choices=['all','plan','legacy','train','acquire','factorial','online','shock'],required=True)
    parser.add_argument('--workers',type=int,default=3);parser.add_argument('--smoke',action='store_true')
    parser.add_argument('--through',choices=['legacy','train','acquire','factorial','online','shock'],default='shock')
    parser.add_argument('--recover-from',type=Path)
    args=parser.parse_args();root=args.root.resolve()
    if args.stage=='all':coordinator(root,args);return
    if args.stage=='plan':make_plan(root,args.workers,args.smoke);return
    plan=json.loads((root/'plan.json').read_text());verify(plan)
    for p,h in plan['source_sha256'].items():assert sha256(REPO/p)==h,p
    cfg=json.loads(prepared_config(CKPT).read_text());out=root/{'train':'training','acquire':'acquisition'}.get(args.stage,args.stage)
    assert not out.exists();out.mkdir()
    if args.stage=='legacy':
        old=json.loads((COLD/'manifest.json').read_text())['items'];items=[i for i in old if i['test']['pitch']==0.]
        rows=parallel(legacy_job,items,args.workers,cfg,str(out))
    elif args.stage=='train':rows=parallel(train_job,plan['training'],args.workers,cfg,str(out))
    elif args.stage=='acquire':rows=parallel(acquire_job,plan['acquisition'],args.workers,cfg,str(out))
    elif args.stage=='factorial':
        assert len(json.loads((root/'legacy_results.json').read_text())['rows'])==3
        rows=parallel(factorial_job,plan['jobs'],args.workers,cfg,str(root))
    elif args.stage=='online':
        decision=json.loads((root/'factorial_decision.json').read_text())['conditions']
        jobs=[j for j in plan['jobs'] if any(v['performance'] for v in decision[j['condition']].values())]
        rows=parallel(online_job,jobs,args.workers,cfg,str(root)) if jobs else []
    else:
        decision=json.loads((root/'online_decision.json').read_text())['conditions'];jobs=[]
        for j in plan['jobs']:
            if j['condition']=='nominal':continue
            if any(v['performance'] for v in decision.get(j['condition'],{}).values()):
                jobs.append(dict(j,change_gain=EFFECTS[j['condition']]['gain']))
        rows=parallel(shock_job,jobs,args.workers,cfg,str(root)) if jobs else []
    write(root/(args.stage+'_results.json'),dict(rows=rows,status='TESTED' if rows else 'NOT_TESTED',
        reason=None if rows else 'No arm passed prerequisite performance and stability gates'))
    if args.stage in ['factorial','online']:stage_decision(root,args.stage)
    verify(plan);print('[DESKTOP_DRY_RUN] stage complete',args.stage,'protected',len(plan['protected_sha256']),flush=True)


if __name__=='__main__':main()
