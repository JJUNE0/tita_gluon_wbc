"""VALIDATION_SIM: bounded identification inputs; no candidate model drives control."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path

import numpy as np

from flash_cold_start_abc import verify,write,fit_batch,fit_rls,information,nominal,BIAS,sha256
from static_target_domain import StaticRunner,StartupFailure,CKPT,prepared_config
from run_static_target_adaptation import guard,validate,KEYS
from eval_flash_stop_release import inputs_for
from analyze_flash_state_learning import state
from m4_shadow_stages import prediction_gate
from analyze_static_target_adaptation import absolute_baseline_error


FAMILIES=['validation_sine','validation_prbs','pulse_pos','pulse_neg','step_pos','step_neg','bipulse_pos','bipulse_neg']


def collection(job):
    out=Path(job['out']);out.mkdir();r=None
    try:
        cfg=json.loads(prepared_config(CKPT).read_text());r=StaticRunner(cfg,job,job['effect'])
        source='train_sine'if job['seed']==721 else'train_prbs'
        excitation=inputs_for(source,.01,job['seed']+18273,3000)
        rows=[];steps=[];requests=[];probes=[];snapshots={};previous=0.;clipped=False;failure=[]
        for i in range(3001):
            rows.append({k:r.observation[k].copy()for k in KEYS})
            failure=guard(r,i*.02)
            if failure or i==3000:break
            o=r.observation['sensor'];probe=0.
            if job['split']=='train'and i>=100 and abs(o[1])<.02 and abs(o[2])<.2 and not r.failures()and not clipped:
                probe=float(excitation[i])
            request=float(np.clip(BIAS+probe,previous-.04,previous+.04));previous=request
            assert request<=.5328+1e-12 and (i<13 or request>=.4328-1e-12)
            tr=r.step(request);steps.append(tr);requests.append(request);probes.append(probe)
            clipped=bool(abs(tr['actual_u']-request)>1e-6 or np.any(abs(tr['motor'][:,[3,7]])>=12.-1e-6))
            if i+1 in [500,3000]:snapshots[i+1]=r.full_snapshot()
        trace={k:np.asarray([v[k]for v in rows])for k in KEYS}
        if steps:trace.update({k:np.asarray([v[k]for v in steps])for k in steps[0]})
        trace.update(raw_requested=np.asarray(requests),probe=np.asarray(probes),p_hold=trace['sensor'][0,0])
        np.savez_compressed(out/'stream.npz',**trace)
        if steps:
            np.testing.assert_array_equal(trace['previous_action'][:-1],trace['history'])
            np.testing.assert_array_equal(trace['previous_action'][1:],trace['action'])
            np.testing.assert_array_equal(trace['physical_motor'][:,:,[0,1,2,4,5,6]],trace['flash'][:,:,[0,1,2,4,5,6]])
            assert max(abs(np.diff(np.r_[0.,trace['raw_requested']])))<=.040000001
        complete=len(steps)==3000 and not failure
        result=dict(job=job,complete=complete,steps=len(steps),failure=failure,target_static=r.env.fingerprint()==r.env.initial_fingerprint,
            initial_goal_immutable=True,model_used_by_controller=False,probes_Nm2s=float(.02*np.sum(np.asarray(probes)**2)),validations=[])
        write(out/'physics.json',dict(r.env.metadata,contacts=r.contact_metadata()))
        if job['split']=='test'and complete:
            for tick,snapshot in snapshots.items():
                r.full_restore(snapshot)
                # Separate offline forks from the same fixed-input stream, not gain activation.
                if abs(r.observation['sensor'][1])>.02 or r.failures():
                    result['validations'].append(dict(t=tick*.02,status='NOT_TESTED',reason='snapshot safety/velocity guard'));continue
                folder=out/f'validation_t{tick}';folder.mkdir()
                verdict=validate(r,snapshot,nominal(),folder,job['seed']+27113+tick,BIAS)
                write(folder/'physical_verdict.json',verdict)
                result['validations'].append(dict(t=tick*.02,status='COMPLETE'if'Direct_B'in verdict else'FAIL',folder=folder.name,reason=verdict.get('reason')))
        write(out/'results.json',result)
        print('VALIDATION_SIM C',job['split'],job['id'],complete,flush=True);return result
    except StartupFailure as e:
        result=dict(job=job,complete=False,failure=['startup'],detail=str(e),validations=[])
        write(out/'results.json',result);e.env.close();return result
    finally:
        if r is not None:r.env.close()


def streams_from(root,domain,window):
    output=[]
    for folder in sorted((root/'C_train').glob(domain+'_s*')):
        result=json.loads((folder/'results.json').read_text())
        if not result['complete']:continue
        with np.load(folder/'stream.npz')as trace:
            z=state(trace);z[:,0]-=float(trace['p_hold']);u=trace['actual_u'].copy();t=np.arange(len(u))*.02
            mask=(t>=window[0])&(t<window[1])&np.isfinite(z[1:]).all(1)
            mask&=abs(trace['raw_requested']-u)<=1e-6
            mask&=~np.any(abs(trace['motor'][:,:,[3,7]])>=12.-1e-6,axis=(1,2))
            output.append((z,u,mask))
    return output


def pooled_information(streams):
    # Build only valid transitions; separators never become artificial transitions.
    z0=np.concatenate([z[:-1][mask]for z,u,mask in streams]);z1=np.concatenate([z[1:][mask]for z,u,mask in streams])
    u=np.concatenate([u[mask]for z,u,mask in streams]);states=np.empty((2*len(u),24));states[::2]=z0;states[1::2]=z1
    interleaved=np.zeros(2*len(u)-1);interleaved[::2]=u
    mask=np.arange(len(interleaved))%2==0
    return information(states,interleaved,mask)


def train_models(root,plan):
    models={}
    for domain in plan['domains']:
        name=domain['name'];entry={}
        for regime,window in plan['C']['training_windows'].items():
            streams=streams_from(root,name,window)
            if len(streams)!=3:entry[regime]=dict(status='NOT_TESTED',reason='training stream incomplete');continue
            info=pooled_information(streams)
            for method,partial in [('LS',False),('RLS',False)]+([('LS_Bc',True),('RLS_Bc',True)]if regime=='post'else[]):
                fit=fit_batch if method.startswith('LS')else fit_rls
                model,diagnostics=fit(streams,partial=partial)
                entry[regime+'_'+method]=dict(model=model,fit=diagnostics,information=info,
                    training_window=window,train_seeds=[720,721,722],target_label_only_used_by_offline_grouping=True)
        models[name]=entry
    write(root/'C_models_frozen.json',dict(execution_domain='DESKTOP_DRY_RUN',models=models,
        source='nominal prior; own train sensor/known-command data only',no_target_model_in_controller=True))
    (root/'C_models_frozen.sha256').write_text(sha256(root/'C_models_frozen.json')+'\n')


def absolute_score(model,traces,inputs,response):
    A=np.asarray(model['A']);B=np.asarray(model['B']);c=np.asarray(model['c_center']);ref=np.asarray(model['state_reference'])
    result={}
    for h in [5,25,50,100]:
        starts=np.arange(0,inputs.shape[1]-h+1,10);prediction=traces[:,starts].copy()
        with np.errstate(over='ignore',invalid='ignore'):
            for k in range(h):prediction=(prediction-ref)@A.T+(inputs[:,starts+k,None]-BIAS)*B+ref+c
            err=prediction[:,:,:2]-traces[:,starts+h,:2];rmse=np.sqrt(np.mean(err**2,axis=1))
            signal=np.maximum(np.sqrt(np.mean(response[:,starts+h,:2]**2,axis=1)),[1e-7,1e-5]);nrmse=rmse/signal
            result[str(h)]=dict(RMSE=np.median(rmse,axis=0).tolist(),NRMSE=np.median(nrmse,axis=0).tolist())
    prediction=traces[:,0].copy()
    errors=[]
    with np.errstate(over='ignore',invalid='ignore'):
        for k in range(100):
            prediction=(prediction-ref)@A.T+(inputs[:,k,None]-BIAS)*B+ref+c
            errors.append(prediction[:,:2]-traces[:,k+1,:2])
        rmse=np.sqrt(np.mean(np.asarray(errors)**2,axis=0));signal=np.maximum(np.sqrt(np.mean(response[:,1:101,:2]**2,axis=1)),[1e-7,1e-5])
        first=np.median(rmse/signal,axis=0)
    return dict(horizons=result,first2s_NRMSE=first.tolist(),gate=bool(np.all(first<=.3)and all(np.all(np.asarray(v['NRMSE'])<=.3)for v in result.values())))


def evaluate_models(root):
    assert sha256(root/'C_models_frozen.json')==(root/'C_models_frozen.sha256').read_text().strip()
    models=json.loads((root/'C_models_frozen.json').read_text())['models'];rows=[]
    for file in sorted((root/'C_test').glob('*/results.json')):
        result=json.loads(file.read_text());domain=result['job']['domain']
        for validation in result['validations']:
            if validation['status']!='COMPLETE':continue
            folder=file.parent/validation['folder'];physical=json.loads((folder/'physical_verdict.json').read_text())
            with np.load(folder/'baseline.npz')as b:base=state(b);bu=b['actual_u'].copy()
            states=[];inputs=[]
            for family in FAMILIES:
                with np.load(folder/(family+'.npz'))as p:states.append(state(p));inputs.append(p['actual_u'].copy())
            states=np.asarray(states);inputs=np.asarray(inputs);response=states-base
            for name,entry in models[domain].items():
                if 'model'not in entry:continue
                model=entry['model'];relative=prediction_gate(model,response,inputs-bu,physical['Direct_B'][1])
                absolute=absolute_score(model,states,inputs,response)
                baseline=absolute_baseline_error(model,base,bu)
                # Also include the full4s baseline free rollout (not rolling reinitializations).
                pred=base[0].copy();err=[];A=np.asarray(model['A']);B=np.asarray(model['B']);ref=np.asarray(model['state_reference']);c=np.asarray(model['c_center'])
                with np.errstate(over='ignore',invalid='ignore'):
                    for i,u in enumerate(bu):
                        pred=ref+A@(pred-ref)+B*(u-BIAS)+c;err.append(pred[:2]-base[i+1,:2])
                    e2=np.sqrt(np.mean(np.asarray(err[:100])**2,axis=0));e4=np.sqrt(np.mean(np.asarray(err)**2,axis=0))
                baseline_gate=bool(np.all(e2<=[2e-5,2e-5])and np.all(e4<=[5e-5,2e-5]))
                gate=relative['gate']and absolute['gate']and baseline_gate
                rows.append(dict(domain=domain,case=result['job']['id'],snapshot_s=validation['t'],model=name,
                    prediction_gate=gate,information_gate=entry['information']['gate'],admission_gate=gate and entry['information']['gate'],
                    paired=relative,absolute=absolute,baseline=dict(rolling=baseline,full2s_RMSE=e2.tolist(),full4s_RMSE=e4.tolist(),gate=baseline_gate)))
    write(root/'C_comparison.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=rows,models_sha256=sha256(root/'C_models_frozen.json'),
        no_test_refitting=True,no_gain_or_controller_update=True))


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--stage',choices=['train','test','analyze'],required=True);p.add_argument('--workers',type=int,default=3);a=p.parse_args()
    root=a.root.resolve();plan=verify(root,full=True)
    if a.stage=='analyze':evaluate_models(root);return
    split=a.stage;out=root/('C_'+split);assert not out.exists();out.mkdir()
    if split=='test':assert sha256(root/'C_models_frozen.json')==(root/'C_models_frozen.sha256').read_text().strip()
    jobs=[dict(id=f'{d["name"]}_s{s["seed"]}_p{s["pitch"]:+.3f}',domain=d['name'],effect=d['effect'],**s,split=split,
        out=str(out/f'{d["name"]}_s{s["seed"]}_p{s["pitch"]:+.3f}'))for d in plan['domains']for s in plan['C'][split]]
    with ProcessPoolExecutor(max_workers=a.workers)as pool:results=list(pool.map(collection,jobs))
    write(root/('C_'+split+'_results.json'),dict(execution_domain='VALIDATION_SIM',rows=results))
    if split=='train':train_models(root,plan)
    verify(root,full=True);print('C',split,'COMPLETE',len(results),flush=True)


if __name__=='__main__':main()
