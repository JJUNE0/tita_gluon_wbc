"""VALIDATION_SIM / DESKTOP_DRY_RUN: preregistered bias x K x reference forks.

The old runtime, gains, evidence and nominal target are immutable. A/B use a
declared retrospective holding-input diagnostic. C uses only past sensor/torque
history; no RLS or gain updates are performed during any evaluation episode.
"""
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path
import pickle
import subprocess

import numpy as np

from diagnose_m4_adaptive_causes import (OLD,COLD,arrays,nominal,fixed_gain,replay,
    protected,verify,BIAS)
from m4_shadow_stages import ConstrainedRLS,ShadowRunner,reproduce,IX
from flash_overnight_control_stages import anchor,physical_paths
from flash_overnight_model_stages import (REPO,CKPT,KEYS,current,parallel,
    prepared_config,write,sha256,lqr_gain,limited)

DIAGNOSTIC=REPO/'docs/exp/2026-10-16/m4_adaptive_cause_diagnostics'
LOW,HIGH=BIAS-.05,BIAS+.05
DT=.02


def gain_changes(candidate,previous,original,scale):
    candidate,previous,original,scale=map(np.asarray,[candidate,previous,original,scale])
    return (float(np.linalg.norm((candidate-previous)*scale)/max(np.linalg.norm(previous*scale),1e-12)),
        float(np.linalg.norm((candidate-original)*scale)/max(np.linalg.norm(original*scale),1e-12)))


def guarded_candidate(model,information,prediction_rmse,z_start,references):
    """Both guards use immutable nominal scaling; never mutate nominal K."""
    g=fixed_gain();original=np.asarray(g['K']);scale=np.maximum(nominal()['state_std'],1e-9)
    candidate,diagnostics=lqr_gain(np.asarray(model['A']),np.asarray(model['B']),
        model['state_std'],np.asarray(g['Q']),g['R'])
    blended=.9*original+.1*np.asarray(candidate).reshape(-1)
    per_step,cumulative=gain_changes(blended,original,np.asarray(fixed_gain()['K']),scale)
    radii={name:float(max(abs(np.linalg.eigvals(np.asarray(m['A'])-np.outer(m['B'],blended)))))
        for name,m in [('nominal',nominal()),('identified',model)]}
    jumps={name:float(abs((blended-original)@(z_start-ref))) for name,ref in references.items()}
    gate=bool(information['gate'] and np.all(np.asarray(prediction_rmse)<=[.00002,.00002])
        and np.isfinite(blended).all() and max(radii.values())<1.-1e-8
        and per_step<=.25 and cumulative<=.25 and max(jumps.values())<=.005)
    return blended,dict(gate=gate,per_update_scaled_change=per_step,
        cumulative_from_nominal_scaled_change=cumulative,raw_jump_by_reference=jumps,
        spectral_radii=radii,prediction_RMSE=prediction_rmse,information=information,DARE=diagnostics,
        guard='per-update<=25% AND immutable nominal cumulative<=25%; blend0.1; jump<=0.005Nm; rho<1')


def prepare_item(item,output):
    out=Path(output)/item['id'];out.mkdir()
    prefix=arrays(COLD/item['id']/'common_identification_prefix.npz')
    from analyze_flash_state_learning import state
    z=state(prefix);z[:,0]-=z[0,0]
    rls=ConstrainedRLS(nominal())
    for i in range(3000):rls.update(z[i],prefix['actual_u'][i],z[i+1])
    m=rls.model();ref=np.asarray(m['state_reference'])
    r0=np.asarray(fixed_gain()['reference']);r1=r0.copy();r1[2:]=z[2500:3000,2:].mean(0)
    assert np.array_equal(r0[:2],r1[:2]) and np.array_equal(r0[:2],np.zeros(2))
    # The model is frozen before this additional2s common validation. Every
    # evaluated branch starts AFTER it, with the original target retained.
    write(out/'model_before_validation.json',m);model_hash=sha256(out/'model_before_validation.json')
    r=ShadowRunner(json.loads(prepared_config(CKPT).read_text()),item['test'])
    try:
        reproduce(r,item['test'],OLD/'run');replay(r,prefix)
        target=float(r.observation['sensor'][0]);prediction=current(r)[IX].copy();prediction[0]-=target
        original=arrays(COLD/item['id']/'M4.npz')
        validation={k:(v[:101] if k in KEYS+['base_path','axle_path'] else v[:100]) for k,v in original.items()}
        replay(r,validation)
        errors=[]
        for i in range(100):
            prediction=ref+np.asarray(m['A'])@(prediction-ref)+np.asarray(m['B'])*(validation['actual_u'][i]-BIAS)+m['c_center']
            actual=state(validation)[i+1].copy();actual[0]-=target
            errors.append(prediction[:2]-actual[:2])
        rmse=np.sqrt(np.mean(np.asarray(errors)**2,axis=0)).tolist()
        pre=anchor(r);pre['base_path_offset']=float(validation['base_path'][-1]);pre['axle_path_offset']=float(validation['axle_path'][-1])
        with gzip.open(out/'common_snapshot.pkl.gz','wb',compresslevel=1) as stream:
            pickle.dump(dict(snapshot=r.effect_snapshot(),pre=pre,p_target=target,
                previous_total=float(validation['actual_u'][-1])),stream)
        initial=current(r)[IX].copy();initial[0]-=target
        np.savez_compressed(out/'common_validation.npz',**validation)
        assert sha256(out/'model_before_validation.json')==model_hash
    finally:r.env.close()
    K,guard=guarded_candidate(m,rls.diagnostics(),rmse,initial,dict(R0=r0,R1=r1))
    old=json.loads((DIAGNOSTIC/'summary.json').read_text())['groups'][item['condition']]
    oracle=float(np.median([x['zero_velocity_input'] for x in old['finite_window_zero_crossings']]))
    frozen=dict(item=item,identified_model=m,K_fixed=fixed_gain()['K'],K_identified=K.tolist(),
        gain_guard=guard,references=dict(R0=r0.tolist(),R1=r1.tolist()),oracle_bias=oracle,
        oracle_provenance='prior diagnostic 30s finite-window zero crossings; retrospective causal diagnosis only',
        causal_training_bias=float(prefix['actual_u'][2500:3000].mean()),
        identification_samples=3000,validation_samples=100,reference_samples=500,
        prefix_sha256=sha256(COLD/item['id']/'common_identification_prefix.npz'),
        target_rule='one common evaluation origin; p_target never changes between branches or during any episode',
        no_future_evaluation_data_in_K_R1_or_causal_bias=True)
    write(out/'frozen.json',frozen)
    print('[DESKTOP_DRY_RUN] frozen',item['id'],'gain guard',guard['gate'],flush=True)
    return dict(id=item['id'],condition=item['condition'],guard=guard,oracle_bias=oracle,
        causal_training_bias=frozen['causal_training_bias'])


class SlowBias:
    """Transfer sustained feedback effort into a slow bias, using past data only.

    No effect label, ground truth, model inversion or future samples enter here.
    The time constant/rate and all gates are fixed before collecting outcomes.
    """
    def __init__(self,start):
        self.value=float(np.clip(start,LOW,HIGH));self.samples=[];self.updates=0;self.rejections=0

    def observe(self,actual_u,sensor):
        self.samples.append((float(actual_u),float(sensor[0]),float(sensor[1]),float(sensor[2])))
        if len(self.samples)<250:return False
        x=np.asarray(self.samples[-250:])
        good=bool(np.isfinite(x).all() and np.sqrt(np.mean(x[:,2]**2))<=.001
            and np.std(x[:,3])<=.002 and np.all(x[:,0]>LOW+1e-6) and np.all(x[:,0]<HIGH-1e-6))
        if not good:self.rejections+=1;return False
        step=float(np.clip((x[:,0].mean()-self.value)*DT/30.,-.0005*DT,.0005*DT))
        self.value=float(np.clip(self.value+step,LOW,HIGH));self.updates+=1
        return True


def bounded_command(raw,bias,previous_feedback,previous_total,step):
    feedback=limited(float(raw),float(previous_feedback),step*DT)
    s=min(1.,step*DT/1.5);activation=s*s*(3.-2.*s)
    requested=BIAS+activation*(float(bias)-BIAS)+feedback
    total=float(np.clip(np.clip(requested,LOW,HIGH),previous_total-.04,previous_total+.04))
    assert LOW-1e-10<=total<=HIGH+1e-10
    return total,feedback,requested


def run_control(r,K,reference,bias,p_target,pre,previous_total,duration,online=False):
    previous_feedback=0.;states=[];steps=[];raws=[];feedbacks=[];biases=[];requests=[];accepted=[]
    learner=SlowBias(bias) if online else None
    first=current(r)[IX].copy();n=round(duration/DT)
    for i in range(n+1):
        states.append({k:r.observation[k].copy() for k in KEYS})
        failure=r.failures()
        if failure or i==n:break
        z=current(r)[IX].copy();z[0]-=p_target
        b=learner.value if learner else bias
        raw=float(-np.asarray(K)@(z-reference))
        u,feedback,request=bounded_command(raw,b,previous_feedback,previous_total,i)
        old_sensor=r.observation['sensor'].copy();old_sensor[0]-=p_target
        tr=r.step(u)
        assert abs(tr['actual_u']-u)<1e-6
        assert np.max(abs(tr['physical_motor'][:,[3,7]]))<=12.000001
        steps.append(tr);raws.append(raw);feedbacks.append(feedback);biases.append(b);requests.append(request)
        accepted.append(learner.observe(tr['actual_u'],old_sensor) if learner else False)
        previous_feedback=feedback;previous_total=u
    trace={k:np.asarray([s[k] for s in states]) for k in KEYS}
    if steps:trace.update({k:np.asarray([s[k] for s in steps]) for k in steps[0]})
    trace.update(raw_correction=np.asarray(raws),correction=np.asarray(feedbacks),bias=np.asarray(biases),
        pre_global_clip=np.asarray(requests),bias_update_accepted=np.asarray(accepted))
    trace['base_path'],trace['axle_path']=physical_paths(trace,pre)
    trace['base_path']+=pre.get('base_path_offset',0.);trace['axle_path']+=pre.get('axle_path_offset',0.)
    trace['sensor_error']=trace['sensor'].copy();trace['sensor_error'][:,0]-=p_target
    np.testing.assert_array_equal(current_from_trace(trace,0),first)
    np.testing.assert_array_equal(trace['previous_action'][:-1],trace['history'])
    np.testing.assert_array_equal(trace['previous_action'][1:],trace['action'])
    complete=bool(not failure and len(steps)==n)
    stats=measure(trace,duration,reference,complete)
    stats.update(failure=failure,target_sensor=p_target,K=np.asarray(K).tolist(),reference=reference.tolist(),
        bias_start=float(bias),bias_final=float(learner.value if learner else bias),
        bias_updates=learner.updates if learner else 0,bias_rejections=learner.rejections if learner else 0,
        complete=complete,duration_s=len(steps)*DT,online=online,no_gain_updates=True)
    return trace,stats


def current_from_trace(trace,index):
    return np.r_[trace['sensor'][index],trace['previous_action'][index],trace['leg_position'][index],trace['leg_velocity'][index]]


def measure(trace,duration,reference,complete):
    if not complete:return dict(base_IAE=None,base_last5_RMSE=None,base_last5_speed_RMS=None)
    t=np.arange(len(trace['sensor']))*DT;tail=(t>=duration-5.)&(t<duration)
    error=trace['sensor_error'];motor=trace['physical_motor'][:,:,[3,7]]
    return dict(base_IAE=float(np.trapz(abs(trace['base_path']),t)),
        base_last5_RMSE=float(np.sqrt(np.mean(trace['base_path'][tail]**2))),
        base_last5_mean=float(trace['base_path'][tail].mean()),
        sensor_last5_mean=float(error[tail,0].mean()),
        base_last5_speed_RMS=float(np.sqrt(np.mean(trace['base_velocity'][tail]**2))),
        base_last5_speed_mean=float(trace['base_velocity'][tail].mean()),
        sensor_last5_speed_mean=float(error[tail,1].mean()),
        midpoint_last5_RMSE=float(np.sqrt(np.mean(trace['axle_path'][tail]**2))),
        max_planar_drift=float(max(np.linalg.norm(trace['base_position'][:,:2]-trace['base_position'][0,:2],axis=1))),
        pitch_RMS=float(np.sqrt(np.mean((trace['sensor'][:,2]-reference[2])**2))),
        pitch_RMS_nominal=float(np.sqrt(np.mean((trace['sensor'][:,2]-fixed_gain()['reference'][2])**2))),
        wheel_RMS=float(np.sqrt(np.mean(motor**2))),
        raw_over_feedback_cap=float(np.mean(abs(trace['raw_correction'])>.05)),
        global_clip_fraction=float(np.mean((trace['pre_global_clip']<LOW)|(trace['pre_global_clip']>HIGH))),
        actual_total_min=float(trace['actual_u'].min()),actual_total_max=float(trace['actual_u'].max()),
        total_slew_max=float(max(abs(np.diff(trace['requested_u'])))/DT),
        correction_peak=float(max(abs(trace['correction']))),
        yaw_change=float(np.unwrap(trace['rpy'][:,2])[-1]-trace['rpy'][0,2]))


def snapshot_item(item,cfg,root):
    r=ShadowRunner(cfg,item['test'])
    try:
        from m4_mismatch_stages import apply_physics_effect
        apply_physics_effect(r,item['test']['effect']);r.enable_effect(item['test']['effect'])
        with gzip.open(Path(root)/'prepared'/item['id']/'common_snapshot.pkl.gz','rb') as stream:bundle=pickle.load(stream)
        r.effect_restore(bundle['snapshot'])
        return r,bundle
    except Exception:
        r.env.close();raise


def stage_ab_item(item,cfg,root):
    out=Path(root)/'ab'/item['id'];out.mkdir();frozen_file=Path(root)/'prepared'/item['id']/'frozen.json'
    f=json.loads(frozen_file.read_text());frozen_hash=sha256(frozen_file)
    r,bundle=snapshot_item(item,cfg,root);rows=[]
    try:
        snapshot=r.effect_snapshot();pre=bundle['pre'];target=bundle['p_target'];first=current(r).copy()
        for reference_name in ['R0','R1']:
            for group,bias_name,K_name in [('E1','nominal','fixed'),('E2','nominal','identified'),
                ('E3','oracle','fixed'),('E4','oracle','identified')]:
                if K_name=='identified' and not f['gain_guard']['gate']:
                    rows.append(dict(group=group,reference_name=reference_name,status='NOT_TESTED',reason='frozen gain guard failed'));continue
                r.effect_restore(snapshot);np.testing.assert_array_equal(current(r),first)
                ref=np.asarray(f['references'][reference_name]);b=BIAS if bias_name=='nominal' else f['oracle_bias']
                K=f['K_'+K_name]
                trace,stats=run_control(r,K,ref,b,target,pre,bundle['previous_total'],60.)
                name=f'{reference_name}_{group}.npz';np.savez_compressed(out/name,**trace)
                rows.append(dict(group=group,reference_name=reference_name,status='PASS' if stats['complete'] else 'FAIL',trace=name,**stats))
        assert sha256(frozen_file)==frozen_hash
        result=dict(id=item['id'],condition=item['condition'],rows=rows,common_validation_original_archive_exact=True,
            common_snapshot_and_target=True,frozen_sha256=frozen_hash,first_observation_action_identical=True)
        write(out/'results.json',result);print('[VALIDATION_SIM] A/B',item['id'],flush=True);return result
    finally:r.env.close()


def stable_against(row,baseline):
    return bool(row.get('complete') and baseline.get('complete') and row['pitch_RMS_nominal']<=max(
        1.25*baseline['pitch_RMS_nominal'],.002) and row['wheel_RMS']<=1.25*baseline['wheel_RMS'])


def paired_comparison(left,right):
    if len(left)!=3 or len(right)!=3 or not all(stable_against(b,a) for a,b in zip(left,right)):
        return dict(gate=False,reason='missing/incomplete trial or pitch/wheel limit failed')
    IAE=float(np.median([x['base_IAE'] for x in right])/max(np.median([x['base_IAE'] for x in left]),1e-12))
    rmse=float(np.median([x['base_last5_RMSE'] for x in right])/max(np.median([x['base_last5_RMSE'] for x in left]),1e-12))
    wins=sum(b['base_IAE']<a['base_IAE'] for a,b in zip(left,right))
    return dict(gate=bool(IAE<=.95 and rmse<=.95 and wins>=2),IAE_ratio=IAE,last5_RMSE_ratio=rmse,paired_IAE_wins=wins,count=3)


def decide_ab(root):
    results=json.loads((root/'ab_results.json').read_text())['rows'];conditions={}
    for name in sorted({r['condition'] for r in results}):
        cases=sorted([r for r in results if r['condition']==name],key=lambda r:r['id'])
        def select(ref,group):return [next(x for x in r['rows'] if x['reference_name']==ref and x['group']==group) for r in cases]
        comparisons={}
        for ref in ['R0','R1']:
            comparisons[ref]={label:paired_comparison(select(ref,a),select(ref,b)) for label,a,b in
                [('bias_effect_fixed','E1','E3'),('K_effect_original_bias','E1','E2'),('K_effect_corrected_bias','E3','E4')]}
        reference={group:paired_comparison(select('R0',group),select('R1',group)) for group in ['E1','E2','E3','E4']}
        bias_success=any(comparisons[ref]['bias_effect_fixed']['gate'] for ref in ['R0','R1'])
        reference_success=reference['E3']['gate']
        conditions[name]=dict(comparisons=comparisons,reference_effect=reference,
            C_eligible=bool(bias_success and reference_success),C_reference='R1',
            decision='C requires measured bias effect AND R1 effect with fixed K/corrected bias; no posthoc threshold changes')
    decision=dict(execution_domain='DESKTOP_DRY_RUN',conditions=conditions,
        eligible=[n for n,v in conditions.items() if v['C_eligible']],no_online_gain_updates=True)
    write(root/'ab_decision.json',decision);return decision


def stage_c_item(item,cfg,root):
    out=Path(root)/'c'/item['id'];out.mkdir();frozen_file=Path(root)/'prepared'/item['id']/'frozen.json'
    f=json.loads(frozen_file.read_text());h=sha256(frozen_file)
    r=ShadowRunner(cfg,item['test']);rows=[]
    try:
        # Motor gain is applied to the model wrapper before restoring full state.
        from m4_mismatch_stages import apply_physics_effect
        apply_physics_effect(r,item['test']['effect']);r.enable_effect(item['test']['effect'])
        with gzip.open(Path(root)/'prepared'/item['id']/'common_snapshot.pkl.gz','rb') as stream:bundle=pickle.load(stream)
        snapshot=bundle['snapshot'];r.effect_restore(snapshot);pre=bundle['pre'];target=bundle['p_target'];first=current(r).copy()
        ref=np.asarray(f['references']['R1'])
        for K_name in ['fixed','identified']:
            if K_name=='identified' and not f['gain_guard']['gate']:continue
            for group,bias,online in [('C0_nominal_fixed_bias',BIAS,False),
                ('C1_training_fixed_bias',f['causal_training_bias'],False),
                ('C2_online_from_nominal',BIAS,True),('C3_online_from_training',f['causal_training_bias'],True)]:
                r.effect_restore(snapshot);np.testing.assert_array_equal(current(r),first)
                trace,stats=run_control(r,f['K_'+K_name],ref,bias,target,pre,bundle['previous_total'],120.,online)
                name=K_name+'_'+group+'.npz';np.savez_compressed(out/name,**trace)
                rows.append(dict(group=group,K_name=K_name,reference_name='R1',trace=name,**stats))
        assert sha256(frozen_file)==h
        result=dict(id=item['id'],condition=item['condition'],rows=rows,frozen_sha256=h,
            no_GT_or_effect_label_or_future_data_in_bias_updates=True,target_unchanged=True)
        write(out/'results.json',result);print('[VALIDATION_SIM] C',item['id'],flush=True);return result
    finally:r.env.close()


def make_plan(root,workers):
    assert root.is_relative_to(REPO/'docs/exp') and not root.exists();root.mkdir(parents=True)
    items=json.loads((COLD/'manifest.json').read_text())['items']
    protected_files=protected()
    for p in DIAGNOSTIC.rglob('*'):
        if p.is_file():protected_files[str(p.relative_to(REPO))]=sha256(p)
    for p in (REPO/'docs/exp/2026-10-16/m4_bias_reference_abc').rglob('*'):
        if p.is_file():protected_files[str(p.relative_to(REPO))]=sha256(p)
    old_plan=json.loads((OLD/'run_final/plan.json').read_text());protected_files.update(old_plan['protected_sha256'])
    plan=dict(execution_domain='VALIDATION_SIM',items=items,workers=workers,protected_sha256=protected_files,
        checkpoint_sha256=sha256(CKPT/'actor.pt'),script_sha256=sha256(Path(__file__)),
        tracked_diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest(),
        gain=dict(train_s=60.,additional_common_heldout_s=2.,blend=.1,per_update_limit=.25,cumulative_nominal_limit=.25,
            scale='immutable nominal state_std',max_raw_jump=.005,rho_limit=1.-1e-8,heldout_pv_rmse=[.00002,.00002]),
        reference='R0 original; R1 prefix last10s hidden22 mean; p_target unchanged, v_target0',
        limits=dict(absolute_total=[LOW,HIGH],feedback_cap=.05,ramp_s=1.5,total_slew=2.,wheel_cap=12.),
        A_B=dict(duration_s=60.,groups=['E1','E2','E3','E4'],references=['R0','R1'],
            oracle_bias='previous diagnostic zero crossing; retrospective mechanism test, no online-performance claim'),
        effect_gate='3/3 stable, median base IAE and last5RMSE<=95% baseline, >=2/3 paired IAE wins; '
            'pitch<=max(1.25 baseline,0.002rad),wheel RMS<=1.25baseline',
        C_gate='per condition: bias effect fixed K at either R0/R1 AND R1 improvement for E3',
        C=dict(duration_s=120.,bias_tau_s=30.,bias_rate=.0005,window_s=5.,
            update_gate='sensor speed RMS<=1mm/s, pitch std<=2mrad, no absolute input saturation, finite',
            rule='bias += clip((past5s mean actual residual-bias)*dt/30, +/-0.0005dt)',
            reference='R1 frozen from common prefix',K='same frozen Fixed or identified K; no online K update',
            groups=['nominal fixed bias','prefix fixed bias','online from nominal','online from prefix'],
            success='C3 vs C1 >=5% IAE/RMSE and >=2/3wins plus stability; C2 vs C0 recovery reported separately'),
        no_QR_or_model_structure_search=True,no_D_or_step_mismatch_or_hardware=True)
    plan['preparation_version']='v2: preserve v1 58s/2s failures; full60s training then extra2s validation, unchanged thresholds'
    plan['target_rule']='Target is fixed BEFORE additional2s validation; preserve its physical path offset in all A/B/C metrics'
    write(root/'plan.json',plan);return plan


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True)
    p.add_argument('--stage',choices=['prepare','ab','c'],required=True);p.add_argument('--workers',type=int,default=3)
    args=p.parse_args();root=args.root.resolve()
    if args.stage=='prepare':
        plan=make_plan(root,args.workers);out=root/'prepared';out.mkdir()
        rows=parallel(prepare_item,plan['items'],args.workers,str(out));write(root/'prepared_results.json',dict(rows=rows))
    else:
        plan=json.loads((root/'plan.json').read_text());verify(plan)
        assert sha256(Path(__file__))==plan['script_sha256'],'Collector changed after plan freeze'
        cfg=json.loads(prepared_config(CKPT).read_text())
        if args.stage=='ab':
            out=root/'ab';assert not out.exists();out.mkdir()
            rows=parallel(stage_ab_item,plan['items'],args.workers,cfg,str(root))
            write(root/'ab_results.json',dict(rows=rows));decide_ab(root)
        else:
            decision=json.loads((root/'ab_decision.json').read_text());out=root/'c';assert not out.exists();out.mkdir()
            items=[i for i in plan['items'] if i['condition'] in decision['eligible']]
            rows=parallel(stage_c_item,items,args.workers,cfg,str(root)) if items else []
            write(root/'c_results.json',dict(rows=rows,eligible=decision['eligible'],
                status='TESTED' if rows else 'NOT_TESTED',reason=None if rows else 'A/B prerequisite failed'))
    verify(plan)
    print('[DESKTOP_DRY_RUN] protected files unchanged',len(plan['protected_sha256']),flush=True)


if __name__=='__main__':main()
