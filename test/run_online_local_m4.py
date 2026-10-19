"""DESKTOP_DRY_RUN A; VALIDATION_SIM B. C is admitted separately per domain."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import fcntl
import json
from pathlib import Path

import numpy as np

from online_local_m4 import (REPO,CKPT,BIAS,LOW,HIGH,ABC,NOMINAL_ROOT,A_SETTINGS,B_SETTINGS,CHECKPOINTS,
    initialize,verify,write,sha256,features,objective,theta_difference,LocalRLS,validate_candidate,training_allowed,
    nominal,ConstrainedRLS,read_new,unique_baselines,fit_batch)
from nominal_m4_diagnosis import score as local_score
from collect_flash_target_offline_id import streams_from,absolute_score,FAMILIES
from analyze_flash_state_learning import state
from analyze_static_target_adaptation import absolute_baseline_error
from m4_shadow_stages import prediction_gate
from m4_joint_adaptation import fixed_gain,Command
from static_target_domain import StaticRunner,StartupFailure,prepared_config,sensor_state,KEYS
from run_static_target_adaptation import guard,score as physical_score
from eval_flash_stop_release import inputs_for


def a_streams(name):
    if name.startswith('nominal'):
        time=float(name[7:]);records,_=read_new(NOMINAL_ROOT,'train',time)
        records=[r for r in records if r['replica']==0];rows=records+unique_baselines(records)
        return [(r['absolute'],r['u'],np.ones(len(r['u']),dtype=bool))for r in rows]
    return streams_from(ABC,'friction0.2',[10.,60.])


def friction_score(model):
    rows=[]
    for path in sorted((ABC/'C_test').glob('friction0.2_s*/validation_t3000')):
        verdict=json.loads((path/'physical_verdict.json').read_text())
        with np.load(path/'baseline.npz')as t:base=state(t);bu=t['actual_u'].copy()
        xs=[];us=[]
        for family in FAMILIES:
            with np.load(path/(family+'.npz'))as t:xs.append(state(t));us.append(t['actual_u'].copy())
        xs=np.asarray(xs);us=np.asarray(us);response=xs-base
        paired=prediction_gate(model,response,us-bu,verdict['Direct_B'][1]);absolute=absolute_score(model,xs,us,response)
        x=base[0].copy();err=[]
        from m4_joint_adaptation import advance
        with np.errstate(over='ignore',invalid='ignore'):
            for i,u in enumerate(bu):x=advance(model,x,u);err.append(x[:2]-base[i+1,:2])
            r2=np.sqrt(np.mean(np.asarray(err[:100])**2,axis=0));r4=np.sqrt(np.mean(np.asarray(err)**2,axis=0))
        bg=bool(np.all(r2<=[2e-5,2e-5])and np.all(r4<=[5e-5,2e-5]))
        rows.append(dict(case=path.parent.name,gate=paired['gate']and absolute['gate']and bg,paired=paired,absolute=absolute,baseline2=r2.tolist(),baseline4=r4.tolist()))
    return dict(passed=sum(r['gate']for r in rows),total=len(rows),rows=rows)


def experiment_a(root,plan):
    models={};numerics=[]
    for cohort in plan['A']['cohorts']:
        streams=a_streams(cohort);X,Y=features(streams);objects={}
        for setting in A_SETTINGS:
            name=setting['name']
            if setting['method']=='plain':model,diagnostics=fit_batch(streams);model.update(input_reference=BIAS,kind='affine');obj=None
            else:
                exact,diagnostics=objective(X,Y,setting['forgetting'],setting['P'],setting['mean'])
                if setting['method']=='recursive':
                    obj=ConstrainedRLS(nominal(),forgetting=setting['forgetting'],prior_covariance=setting['P'])
                    if setting['mean']=='zero':
                        for group in obj.groups:group['theta'][:]=0.
                    try:
                        for z,u,mask in streams:
                            for i in np.flatnonzero(mask):obj.update(z[i],float(u[i]),z[i+1])
                    except FloatingPointError as exc:
                        numerics.append(dict(cohort=cohort,setting=name,status='FAIL',reason=str(exc)))
                        models[cohort+'/'+name]=dict(model=None,cohort=cohort,setting=setting,reason='raw recursive numerical failure');continue
                    difference=theta_difference(obj,exact)
                    numerics.append(dict(cohort=cohort,setting=name,relative_theta=difference,
                        covariance_min=min(float(np.linalg.eigvalsh(g['P']).min())for g in obj.groups),
                        status='PASS'if difference<=1e-7 else'SUSPICIOUS',samples=len(X)))
                else:obj=exact
                model=obj.model()
            objects[name]=obj;key=cohort+'/'+name
            models[key]=dict(model=model,cohort=cohort,setting=setting,samples=len(X),diagnostics=diagnostics)
            print('DESKTOP_DRY_RUN A freeze',key,flush=True)
    write(root/'A_models_frozen.json',dict(execution_domain='DESKTOP_DRY_RUN',models=models));h=sha256(root/'A_models_frozen.json')
    (root/'A_models_frozen.sha256').write_text(h+'\n');write(root/'A_numerics.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=numerics))
    rows=[]
    for key,e in models.items():
        if e['model']is None:
            rows.append(dict(key=key,cohort=e['cohort'],setting=e['setting']['name'],passed=0,total=6,status='FAIL',reason=e['reason']));continue
        if e['cohort'].startswith('nominal'):
            records,direct=read_new(NOMINAL_ROOT,'test',float(e['cohort'][7:]));v=local_score(e['model'],records,direct)
            result=dict(passed=v['passed_contexts'],total=v['total_contexts'],details=v)
        else:result=friction_score(e['model'])
        rows.append(dict(key=key,cohort=e['cohort'],setting=e['setting']['name'],**result))
        print('DESKTOP_DRY_RUN A result',key,result['passed'],result['total'],flush=True)
    assert sha256(root/'A_models_frozen.json')==h
    write(root/'A_results.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=rows,no_new_simulation=True,no_B_selection_from_A_test=True))


def b_job(job,root,plan):
    out=Path(root)/job['split']/job['id'];out.mkdir();r=None
    try:
        r=StaticRunner(json.loads(prepared_config(CKPT).read_text()),job,job['effect'])
        np.savez_compressed(out/'startup.npz',**{k:np.asarray([row[k]for row in r.env.startup])for k in ['qpos','qvel','motor']})
        learners={s['name']:LocalRLS(s)for s in B_SETTINGS};gain=fixed_gain();K=np.asarray(gain['K']);ref=np.asarray(gain['reference']);p_hold=float(r.observation['sensor'][0])
        leg_limits=r.env.model.jnt_range[r.leg_joints].copy()
        def sensor_safe(z,roll):
            return bool(np.isfinite(z).all()and abs(roll)<.2 and abs(z[2])<.2 and abs(z[1])<.02
                and np.all(z[12:18]>=leg_limits[:,0]-.01)and np.all(z[12:18]<=leg_limits[:,1]+.01))
        command=Command(previous=0.);trainprobe=inputs_for('train_prbs',job['amplitude'],job['seed']+56191,3200)
        valprobe={t:inputs_for(f,job['amplitude'],job['seed']+75101+round(t),200)for t,f in zip(CHECKPOINTS,['validation_sine','validation_prbs','bipulse_pos'])}
        rows=[];steps=[];extras=[];pending=None;events=[];failure=[];path=0.;mid=0.;previous=None;mask=[]
        for i in range(3201):
            time=i*.02;obs={k:r.observation[k].copy()for k in KEYS}
            if previous is not None:
                yaw=previous['rpy'][2]+((obs['rpy'][2]-previous['rpy'][2]+np.pi)%(2*np.pi)-np.pi)/2;f=np.array([np.cos(yaw),np.sin(yaw),0.])
                path+=float((obs['base_position']-previous['base_position'])@f);mid+=float((obs['position']-previous['position'])@f)
            obs.update(base_path=np.array(path),midpoint_path=np.array(mid));rows.append(obs);previous=obs
            failure=guard(r,time)
            if failure or i==3200:break
            z=sensor_state(r,p_hold)
            if any(abs(time-t)<1e-9 for t in CHECKPOINTS):
                assert pending is None;candidates={name:obj.freeze(time)for name,obj in learners.items()}
                filename=f'candidate_t{i}.json';write(out/filename,dict(created=time,candidates=candidates))
                pending=dict(created=time,candidates=candidates,file=filename,sha256=sha256(out/filename),states=[z.copy()],inputs=[],unsafe=False)
            proposed=float(trainprobe[i]);validation=None
            for t in CHECKPOINTS:
                if t<=time<t+4.-1e-9:proposed=float(valprobe[t][round((time-t)/.02)]);validation=t;break
            raw=BIAS-float(K@(z-ref));safe_probe=bool(i>=100 and sensor_safe(z,r.observation['rpy'][0])and LOW+job['amplitude']+.002<raw<HIGH-job['amplitude']-.002)
            probe=proposed if safe_probe else 0.;u,details=command.compute(z,K,BIAS,ref,probe);tr=r.step(u);after=sensor_state(r,p_hold)
            physical_clip=bool(np.any(abs(tr['physical_motor'][:,[3,7]])>=12.-1e-6))
            native_clip=bool(np.any(abs(tr['motor'][:,[3,7]])>=12.-1e-6))
            healthy=sensor_safe(z,obs['rpy'][0])and sensor_safe(after,r.observation['rpy'][0])and not native_clip and np.isfinite(tr['actual_u'])
            eligible=bool(healthy and training_allowed(time));mask.append(eligible)
            for obj in learners.values():obj.observe(time+.02,z,tr['actual_u'],after,eligible)
            if pending is not None:
                pending['states'].append(after.copy());pending['inputs'].append(float(tr['actual_u']));pending['unsafe']|=not healthy
                if len(pending['inputs'])==200:
                    assert sha256(out/pending['file'])==pending['sha256'];verdicts={}
                    for name,c in pending['candidates'].items():
                        if c['status']!='FROZEN':verdicts[name]=dict(gate=False,status='NOT_TESTED',reason=c['reason']);continue
                        validation_score=validate_candidate(c['model'],pending['states'],pending['inputs'])
                        gate=bool(c['information']['gate']and validation_score['gate']and not pending['unsafe'])
                        verdicts[name]=dict(gate=gate,status='PASS'if gate else'FAIL',prediction=validation_score,information=c['information'],
                            reject_reasons=[n for n,b in [('information',c['information']['gate']),('future_prediction_and_conditional_B',validation_score['gate']),('safe_validation',not pending['unsafe'])]if not b])
                    events.append(dict(created=pending['created'],completed=time+.02,candidate_file=pending['file'],candidate_sha256=pending['sha256'],verdicts=verdicts))
                    pending=None
            details.update(probe=probe,proposed_probe=proposed,probe_allowed=safe_probe,raw_requested=u,software_residual=float(tr['actual_u']),physical_saturation=physical_clip,training_used=eligible,validation_window=-1. if validation is None else validation)
            steps.append(tr);extras.append(details)
        trace={k:np.asarray([row[k]for row in rows])for k in rows[0]}
        if steps:
            trace.update({k:np.asarray([row[k]for row in steps])for k in steps[0]});trace.update({k:np.asarray([row[k]for row in extras])for k in extras[0]})
            np.testing.assert_array_equal(trace['previous_action'][:-1],trace['history']);np.testing.assert_array_equal(trace['previous_action'][1:],trace['action'])
            np.testing.assert_array_equal(trace['physical_motor'][:,:,[0,1,2,4,5,6]],trace['flash'][:,:,[0,1,2,4,5,6]])
            assert np.max(abs(np.diff(np.r_[0.,trace['raw_requested']])))/.02<=2.000001
        trace['p_hold']=p_hold;trace['goal_base_position']=trace['base_position'][0].copy();np.savez_compressed(out/'trajectory.npz',**trace)
        stats=physical_score(trace,len(steps)==3200 and not failure,failure)
        result=dict(execution_domain='VALIDATION_SIM',job=job,physical=stats,events=events,steps=len(steps),training_transitions=sum(mask),
            target_static=r.env.fingerprint()==r.env.initial_fingerprint,goal_immutable=True,new_K_adoptions=0,
            probe_energy=float(.02*np.sum(trace['probe']**2))if steps else 0.,probe_allowed_fraction=float(np.mean(trace['probe_allowed']))if steps else 0.,
            saturation_fraction=float(np.mean(trace['global_clipped']))if steps else 0.,
            numerical_rebuilds={k:v.rebuilds for k,v in learners.items()},learner_api='time,before_sensor24,known_software_residual,after_sensor24,eligible; no domain/GT/snapshot')
        write(out/'physics.json',dict(r.env.metadata,contacts=r.contact_metadata()));write(out/'results.json',result)
        print('VALIDATION_SIM B',job['id'],'complete',stats['complete'],'passed',{k:sum(e['verdicts'][k]['gate']for e in events)for k in learners},flush=True)
        return result
    except StartupFailure as e:
        e.env.close();result=dict(job=job,steps=0,events=[],physical=dict(complete=False,failure=['startup',str(e)]));write(out/'results.json',result);return result
    finally:
        if r is not None:r.env.close()


def admission(root,plan):
    dev=json.loads((root/'development_results.json').read_text())['rows'];test=json.loads((root/'test_results.json').read_text())['rows'];decisions={}
    for domain in plan['B']['domains']:
        name=domain['name'];chosen=None
        for setting in B_SETTINGS:
            for amp in [.01,.02]:
                rows=[r for r in dev if r['job']['domain']==name and r['job']['amplitude']==amp]
                if len(rows)==3 and all(r['physical']['complete']and any(e['verdicts'][setting['name']]['gate']for e in r['events'])for r in rows):chosen=dict(setting=setting['name'],amplitude=amp);break
            if chosen:break
        if chosen:
            rows=[r for r in test if r['job']['domain']==name and r['job']['amplitude']==chosen['amplitude']]
            passed=sum(r['physical']['complete']and any(e['verdicts'][chosen['setting']]['gate']for e in r['events'])for r in rows)
            decisions[name]=dict(C_permitted=passed==6 and len(rows)==6,chosen_from_dev=chosen,heldout_pass=passed,total=len(rows),reason='heldout6/6 required')
        else:decisions[name]=dict(C_permitted=False,chosen_from_dev=None,reason='no predeclared setting/amplitude passes all3 development rollouts',C_status='NOT_TESTED')
    write(root/'B_admission.json',dict(execution_domain='DESKTOP_DRY_RUN',domains=decisions))
    write(root/'C_status.json',dict(execution_domain='VALIDATION_SIM',domains={k:dict(status='READY'if v['C_permitted']else'NOT_TESTED',reason=v['reason'])for k,v in decisions.items()},no_controller_result_inferred=True))


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--stage',choices=['init','A','development','test','admission'],required=True);p.add_argument('--workers',type=int,default=3);a=p.parse_args();root=a.root.resolve()
    if a.stage=='init':initialize(root);return
    plan=verify(root,full=True)
    with (root/'coordinator.lock').open('a')as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);file=root/'pipeline_state.json';status=json.loads(file.read_text())if file.exists()else dict(execution_domain='VALIDATION_SIM',stages={})
        assert a.stage not in status['stages'],'Refusing overwrite/retry of old stage';status['stages'][a.stage]=dict(status='RUNNING');write(file,status)
        try:
            if a.stage=='A':experiment_a(root,plan);artifact='A_results.json'
            elif a.stage=='admission':admission(root,plan);artifact='B_admission.json'
            else:
                assert status['stages']['A']['status']=='COMPLETE';out=root/a.stage;assert not out.exists();out.mkdir()
                starts=plan['B'][a.stage];jobs=[dict(s,domain=d['name'],effect=d['effect'],amplitude=amp,split=a.stage,id=f'{d["name"]}_a{amp:g}_s{s["seed"]}_p{s["pitch"]:+.3f}')for d in plan['B']['domains']for amp in [.01,.02]for s in starts]
                with ProcessPoolExecutor(max_workers=a.workers)as pool:results=list(pool.map(b_job,jobs,[str(root)]*len(jobs),[plan]*len(jobs)))
                artifact=a.stage+'_results.json';write(root/artifact,dict(execution_domain='VALIDATION_SIM',rows=results))
            verify(root,full=True);status['stages'][a.stage]=dict(status='COMPLETE',artifact=artifact,sha256=sha256(root/artifact));write(file,status)
        except BaseException as e:status['stages'][a.stage]=dict(status='ERROR',reason=repr(e));write(file,status);raise


if __name__=='__main__':main()
