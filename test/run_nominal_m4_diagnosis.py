"""VALIDATION_SIM collection and DESKTOP_DRY_RUN fits; old sources untouched."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import fcntl
import gzip
import json
from pathlib import Path
import pickle

import numpy as np

from nominal_m4_diagnosis import (REPO,CKPT,BIAS,LOCAL,AFFINE,ABC,TIMES,PROFILES,METHODS,
    initialize,verify,write,sha256,prepared_config,fit_method,read_new,choose,load_absolute,fit,load)
from static_target_domain import StaticRunner,StartupFailure,KEYS
from eval_flash_state_learning import StateRunner,STATE_KEYS
from eval_flash_stop_release import inputs_for
from eval_flash_constant_hold import metrics as hold_metrics
from run_static_target_adaptation import guard
from analyze_flash_state_learning import state
from analyze_flash_stop_local import fit_local
from analyze_flash_operating_local import evaluate_extended,summarize_all
from calibrate_flash_operating_affine import validate as old_affine_validate
from flash_cold_start_abc import fit_batch


def rollout(r,inputs,start_time):
    rows=[];steps=[];failure=[]
    for i in range(len(inputs)+1):
        rows.append({k:r.observation[k].copy()for k in KEYS});failure=guard(r,start_time+i*.02)
        if failure or i==len(inputs):break
        steps.append(r.step(float(inputs[i])))
    trace={k:np.asarray([v[k]for v in rows])for k in KEYS}
    if steps:
        trace.update({k:np.asarray([v[k]for v in steps])for k in steps[0]})
        np.testing.assert_array_equal(trace['previous_action'][:-1],trace['history']);np.testing.assert_array_equal(trace['previous_action'][1:],trace['action'])
        np.testing.assert_array_equal(trace['physical_motor'][:,:,[0,1,2,4,5,6]],trace['flash'][:,:,[0,1,2,4,5,6]])
        assert np.max(abs(trace['physical_motor'][:,:,[3,7]]))<=12.000001
    return trace,failure


def collect(job,root,plan):
    out=Path(root)/job['split']/job['id'];out.mkdir();r=None
    try:
        r=StaticRunner(json.loads(prepared_config(CKPT).read_text()),job,{})
        p_hold=float(r.observation['sensor'][0]);rows=[];steps=[];snapshots={};failure=[];tau=0.
        for tick in range(50001):
            rows.append({k:r.observation[k].copy()for k in KEYS});failure=guard(r,tick*.02)
            if failure:break
            if tick in [500,1500,3000,50000]:
                snapshots[tick]=r.full_snapshot();print('VALIDATION_SIM snapshot',job['id'],tick*.02,flush=True)
            if tick%5000==0:print('VALIDATION_SIM prefix',job['id'],tick*.02,flush=True)
            if tick==50000:break
            tau=float(np.clip(BIAS,tau-.04,tau+.04));steps.append(r.step(tau))
        prefix={k:np.asarray([v[k]for v in rows])for k in KEYS}
        if steps:prefix.update({k:np.asarray([v[k]for v in steps])for k in steps[0]})
        prefix['p_hold']=p_hold;np.savez_compressed(out/'prefix.npz',**prefix)
        write(out/'physics.json',dict(r.env.metadata,contacts=r.contact_metadata()))
        results=[]
        for tick,snapshot in snapshots.items():
            time=tick*.02;folder=out/f't{tick}';folder.mkdir();r.full_restore(snapshot)
            with gzip.open(folder/'snapshot.pkl.gz','wb',compresslevel=1)as f:pickle.dump(snapshot,f)
            item=dict(time=time,folder=folder.name,responses=[],status='NOT_TESTED')
            if time==1000.:
                history={k:v[tick-12000:tick+1]if k in KEYS else v[tick-12000:tick]for k,v in prefix.items()if k!='p_hold'}
                quiet=hold_metrics(history,r.env.model.jnt_range[r.leg_joints],True,240.);item['settled_gate']=quiet
                if not quiet['operating_gate']:
                    item['reason']='predeclared settled operating gate failed';results.append(item);continue
            if abs(r.observation['sensor'][1])>.02 or abs(r.observation['sensor'][2])>.2:
                item['reason']='predeclared probe speed/pitch guard';results.append(item);continue
            base,bf=rollout(r,np.full(400,BIAS),time)
            if bf:
                item.update(status='FAIL',reason=bf);results.append(item);continue
            r.full_restore(snapshot);replay,rf=rollout(r,np.full(400,BIAS),time);assert not rf
            for k in base:np.testing.assert_array_equal(base[k],replay[k])
            np.savez_compressed(folder/'baseline.npz',**base);item['baseline_exact_replay']=True
            for i,c in enumerate(plan[job['split']+'_cases']):
                seed=int(np.random.SeedSequence([job['seed'],job['pitch_index'],tick,i,61401]).generate_state(1)[0])
                u=BIAS+inputs_for(c['family'],c['amplitude'],seed,400);r.full_restore(snapshot);trace,pf=rollout(r,u,time)
                if pf:item.update(status='FAIL',reason=pf,failed_case=c);break
                assert np.max(abs(trace['actual_u']-u))<1e-6
                assert np.max(abs(trace['actual_u']-BIAS))<=.050001
                assert np.max(abs(np.diff(np.r_[BIAS,u])))<=.040000001
                for k in KEYS:np.testing.assert_array_equal(base[k][0],trace[k][0])
                name=f'{c["family"]}_a{c["amplitude"]:g}_rep{c["replica"]}.npz'
                np.savez_compressed(folder/name,**trace);item['responses'].append(dict(c,file=name,input_seed=seed))
            else:
                direct=[]
                for sign in [1.,-1.]:
                    r.full_restore(snapshot);trace,pf=rollout(r,[BIAS+sign*.01],time);assert not pf
                    direct.append((state(trace)[1],trace['actual_u'][0]));np.savez_compressed(folder/('B_plus.npz'if sign>0 else'B_minus.npz'),**trace)
                b=(direct[0][0]-direct[1][0])/(direct[0][1]-direct[1][1]);np.testing.assert_array_equal(b[4:12],np.zeros(8))
                item.update(status='COMPLETE',Direct_B=b.tolist())
            write(folder/'results.json',item);results.append(item)
            print('VALIDATION_SIM probes',job['id'],time,item['status'],len(item['responses']),flush=True)
        r.env.assert_static()
        result=dict(execution_domain='VALIDATION_SIM',job=job,prefix_complete=len(steps)==50000 and not failure,
            failure=failure,snapshots=results,target_static=True,p_hold=p_hold,goal_never_reset=True,no_model_in_control=True)
        write(out/'results.json',result);return result
    except StartupFailure as e:
        e.env.close();result=dict(job=job,prefix_complete=False,failure=['startup',str(e)],snapshots=[]);write(out/'results.json',result);return result
    finally:
        if r is not None:r.env.close()


def legacy(root):
    records,_,_=load(LOCAL,'train');x=np.concatenate([r['z'][:-1]for r in records]);y=np.concatenate([r['z'][1:]for r in records]);u=np.concatenate([r['u']for r in records])
    paired=fit(x,y,u,'M4');old=next(m for m in json.loads((LOCAL/'local_models_frozen.json').read_text())['models']if m['name']=='M4')
    differences={k:float(np.max(abs(np.asarray(paired[k])-old[k])))for k in ['A','B']}
    for k in differences:np.testing.assert_allclose(paired[k],old[k],atol=1e-9,rtol=1e-9)
    train,baselines,_=load_absolute(LOCAL,'train');bx=np.concatenate([r['absolute'][:-1]for r in baselines]);by=np.concatenate([r['absolute'][1:]for r in baselines]);bu=np.concatenate([r['u']for r in baselines])
    A,B=np.asarray(paired['A']),np.asarray(paired['B']);ref=bx.mean(0);c=np.mean((by-ref)-(bx-ref)@A.T-(bu[:,None]-BIAS)*B,axis=0)
    affine=dict(paired,kind='affine',state_reference=ref.tolist(),input_reference=BIAS,c_center=c.tolist())
    oldaff=json.loads((AFFINE/'calibrated/affine_model_frozen.json').read_text())['model']
    for key in ['A','B','state_reference','c_center']:np.testing.assert_allclose(affine[key],oldaff[key],atol=1e-9,rtol=1e-9)
    joint=fit_local(train+baselines,'M4',affine=True)
    oldjoint=json.loads((AFFINE/'affine/affine_model_frozen.json').read_text())['model']
    for key in ['A','B','c_center']:np.testing.assert_allclose(joint[key],oldjoint[key],atol=1e-9,rtol=1e-9)
    write(root/'legacy_models.json',dict(paired=paired,paired_c=affine,joint=joint,old_phaseC=json.loads((ABC/'C_models_frozen.json').read_text())['models']['nominal']['post_LS']['model']))
    test,_,_=load(LOCAL,'test');stats,_=evaluate_extended(paired,np.asarray([r['z']for r in test]),np.asarray([r['u']for r in test]));delta=summarize_all(stats)
    expected=json.loads((LOCAL/'summary.json').read_text())
    for key in ['full2s','full8s']:
        np.testing.assert_allclose(delta[key]['nrmse'],expected['models']['M4'][key]['nrmse'],atol=1e-9,rtol=1e-9)
    result=dict(execution_domain='DESKTOP_DRY_RUN',AB_max_difference=differences,old_paired_metrics=delta,
        paired_c_oldtest=old_affine_validate(affine,LOCAL),joint_oldtest=old_affine_validate(joint,LOCAL),
        paired_c_fresh=old_affine_validate(affine,AFFINE/'fresh'),joint_fresh=old_affine_validate(joint,AFFINE/'fresh'),physical_replays=[])
    for path in sorted((AFFINE/'fresh').glob('*/results.json'))[:3]:
        info=json.loads(path.read_text());job=info['job'];r=StateRunner(json.loads(prepared_config(CKPT).read_text()),job)
        try:
            tick=50000
            with gzip.open(path.parent/f'snapshot_t{tick}.pkl.gz','rb')as f:snap=pickle.load(f)
            checks=[]
            for name in [f'zero_t{tick}.npz',f'validation_prbs_a0.05_t{tick}.npz']:
                r.restore(snap)
                with np.load(path.parent/name)as archive:
                    trace,failure=r.rollout(archive['requested_u']);assert not failure
                    for k in trace:np.testing.assert_array_equal(trace[k],archive[k])
                checks.append(dict(file=name,exact=True,arrays=len(trace)))
            result['physical_replays'].append(dict(case=job['id'],checks=checks))
        finally:r.env.close()
    write(root/'legacy_results.json',result)
    print('DESKTOP_DRY_RUN legacy full8',delta['full8s']['nrmse'],'AB diff',differences,flush=True)
    return result


def freeze(root):
    models={};skips=[]
    for time in TIMES:
        records,_=read_new(root,'train',time)
        for profile in PROFILES:
            subset=choose(records,profile)
            for method in METHODS:
                key=f't{time:g}_{profile}_{method}'
                if not subset:skips.append(dict(key=key,reason='training prerequisite incomplete'));continue
                models[key]=dict(model=fit_method(subset,method),train_time=time,profile=profile,method=method,primary=True)
        subset=choose(records,'full')
        if subset:
            for method,ncenter in [('paired_c',False),('joint',False),('joint_nominal',True)]:
                key=f't{time:g}_full_{method}_rcond1e8'
                models[key]=dict(model=fit_method(subset,'joint'if ncenter else method,1e-8,ncenter),train_time=time,profile='full',method=method+'_1e8',primary=False)
    # Stream composition contrast: same original measured states, no paired forks.
    for label,start,end in [('early',10.,60.),('late',950.,1000.)]:
        rows=[]
        for f in sorted((root/'train').glob('*/prefix.npz')):
            with np.load(f)as t:z=state(t);z[:,0]-=float(t['p_hold']);u=t['actual_u'].copy()
            a,b=round(start/.02),round(end/.02);v=z[a:b+1];w=u[a:b]
            rows.append(dict(absolute=v,delta=v-v[0],u=w,base=v,base_u=w,context=f.parent.name,start_rl_s=start,seed=0,pitch=0.,family='stream'))
        # Constant-input streams have no B excitation: explicitly report this, never count as identified B.
        for cutoff in [1e-10,1e-8]:
            model=fit_method(rows,'joint',cutoff)
            models[f'stream_{label}_{cutoff}']=dict(model=model,train_time=10. if label=='early'else 1000.,profile='stream',method='joint_stream',primary=False,B_information='NOT_IDENTIFIABLE: constant input')
    write(root/'models_frozen.json',dict(execution_domain='DESKTOP_DRY_RUN',models=models,skips=skips,train_only=True,no_online_model=True))
    (root/'models_frozen.sha256').write_text(sha256(root/'models_frozen.json')+'\n')
    return dict(models=len(models),skips=skips)


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--stage',choices=['init','legacy','train','fit','test'],required=True);p.add_argument('--workers',type=int,default=3);a=p.parse_args();root=a.root.resolve()
    if a.stage=='init':initialize(root);return
    plan=verify(root,full=True)
    with (root/'coordinator.lock').open('a')as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        sf=root/'pipeline_state.json';status=json.loads(sf.read_text())if sf.exists()else dict(execution_domain='VALIDATION_SIM',stages={})
        assert a.stage not in status['stages'],'Refusing implicit rerun of completed/failed/running stage'
        if a.stage=='fit':assert status['stages']['train']['status']=='COMPLETE'
        if a.stage=='test':assert sha256(root/'models_frozen.json')==(root/'models_frozen.sha256').read_text().strip()
        status['stages'][a.stage]=dict(status='RUNNING');write(sf,status)
        try:
            if a.stage=='legacy':value=legacy(root);artifact='legacy_results.json'
            elif a.stage=='fit':value=freeze(root);artifact='models_frozen.json'
            else:
                out=root/a.stage;assert not out.exists();out.mkdir()
                with ProcessPoolExecutor(max_workers=a.workers)as pool:value=list(pool.map(collect,plan['starts'][a.stage],[str(root)]*6,[plan]*6))
                artifact=a.stage+'_results.json';write(root/artifact,dict(execution_domain='VALIDATION_SIM',rows=value))
            verify(root,full=True);status['stages'][a.stage]=dict(status='COMPLETE',artifact=artifact,sha256=sha256(root/artifact));write(sf,status)
        except BaseException as e:
            status['stages'][a.stage]=dict(status='ERROR',reason=repr(e));write(sf,status);raise


if __name__=='__main__':main()
