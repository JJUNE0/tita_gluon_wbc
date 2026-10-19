"""DESKTOP_DRY_RUN: audit and report M4 independent/joint/abrupt experiments."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from eval_m4_joint_pipeline import (REPO,CKPT,KEYS,MASKS,arrays,write,sha256,verify,
    load_snapshot,measured,metrics,compare,DT,LOW,HIGH,init_effect,test_model,parallel,prepared_config,replay)
from m4_joint_adaptation import JointEstimator,Command,offset,REF_LIMIT,nominal,fixed_gain
from analyze_flash_state_learning import state
from m4_shadow_stages import prediction_gate


def aggregate(rows):
    good=[r for r in rows if r.get('complete') and r.get('metrics')]
    if not good:return dict(count=len(rows),complete=0,status='NOT_TESTED' if all(r.get('status')=='NOT_TESTED' for r in rows) else 'FAIL')
    keys=['base_IAE','last5_base_RMSE','last5_sensor_RMSE','last5_midpoint_RMSE',
        'last5_base_speed_RMS','max_planar','pitch_RMS','wheel_RMS','yaw_change','sensor_base_gap_last5']
    result=dict(count=len(rows),complete=len(good),median={k:float(np.median([r['metrics'][k] for r in good])) for k in keys})
    result['recovery_count']=sum(r['metrics']['recovery_s'] is not None for r in good)
    recovered=[r['metrics']['recovery_s'] for r in good if r['metrics']['recovery_s'] is not None]
    result['recovery_median_s']=None if not recovered else float(np.median(recovered))
    return result


def audit_episode(root,phase,case,row,replay_online):
    folder=root/phase/case['job']['id'];trace=arrays(folder/row['trace'])
    z=state(trace);z[:,0]-=row['target_sensor'];K=trace['K_used'];ref=trace['reference_used'];bias=trace['bias']
    assert np.array_equal(ref[:,:2],np.zeros((len(ref),2)))
    np.testing.assert_array_equal(trace['previous_action'][:-1],trace['history'])
    np.testing.assert_array_equal(trace['previous_action'][1:],trace['action'])
    np.testing.assert_array_equal(trace['physical_motor'][:,:,[0,1,2,4,5,6]],trace['flash'][:,:,[0,1,2,4,5,6]])
    np.testing.assert_allclose(trace['effective_offset'],bias+np.einsum('ij,ij->i',K,ref),atol=1e-12)
    world_offset=trace['effective_offset']+K[:,0]*row['target_sensor']
    np.testing.assert_allclose(bias+trace['raw_correction'],world_offset-np.einsum('ij,ij->i',K,state(trace)[:-1]),atol=1e-10)
    np.testing.assert_allclose(trace['raw_correction'],-np.einsum('ij,ij->i',K,z[:-1]-ref),atol=1e-10)
    assert trace['requested_u'].min()>=LOW-1e-12 and trace['requested_u'].max()<=HIGH+1e-12
    assert max(abs(trace['requested_u']-trace['actual_u']))<1e-6
    assert np.max(abs(trace['physical_motor'][:,:,[3,7]]))<=12.000001
    if phase=='shock':
        prefix=arrays(folder/'nominal_prefix.npz');previous=float(prefix['actual_u'][-1])
    else:
        prefix=arrays(root/'factorial'/case['job']['id']/'common_prefix.npz');previous=float(prefix['actual_u'][-1])
    assert row['target_sensor']==float(prefix['sensor'][0,0])
    np.testing.assert_array_equal(trace['goal_base_position'],prefix['base_position'][0])
    assert trace['base_path'][0]==prefix['base_path'][-1]
    assert trace['axle_path'][0]==prefix['axle_path'][-1]
    command=Command(previous)
    for i in range(len(trace['actual_u'])):
        u,details=command.compute(z[i],K[i],bias[i],ref[i])
        assert abs(u-trace['requested_u'][i])<1e-12
    scale=np.maximum(nominal()['state_std'],1e-9);K0=np.asarray(fixed_gain()['K'])
    if phase=='factorial':
        np.testing.assert_array_equal(K,np.tile(K[0],(len(K),1)))
        np.testing.assert_array_equal(ref,np.tile(ref[0],(len(ref),1)))
        np.testing.assert_array_equal(bias,np.full(len(bias),bias[0]))
    else:
        mask=MASKS[row['group']]
        if not mask[0]:np.testing.assert_array_equal(K,np.tile(K0,(len(K),1)))
        if not mask[1]:np.testing.assert_array_equal(bias,np.full(len(bias),.4828))
        if not mask[2]:np.testing.assert_array_equal(ref,np.tile(fixed_gain()['reference'],(len(ref),1)))
    cumulative=np.linalg.norm((K-K0)*scale,axis=1)/np.linalg.norm(K0*scale)
    per=np.linalg.norm(np.diff(K,axis=0)*scale,axis=1)/np.maximum(np.linalg.norm(K[:-1]*scale,axis=1),1e-12)
    assert cumulative.max()<=.250000001 and (not len(per) or per.max()<=.250000001)
    assert np.all(abs(ref[:,2:]-np.asarray(fixed_gain()['reference'])[2:])<=REF_LIMIT+1e-10)
    causal=False;final_model=None;model_confidence=None
    if phase!='factorial' and row['group']!='E0' and replay_online:
        frozen=json.loads((root/'training'/case['job']['training_id']/'frozen.json').read_text())
        learner=JointEstimator(MASKS[row['group']],row['method'],np.asarray(frozen['leg_limits']))
        past=state(prefix);past[:,0]-=row['target_sensor']
        for i,u in enumerate(prefix['actual_u']):learner.rls.update(past[i],u,past[i+1])
        learner.seed_history(past,prefix['actual_u']);learner.information=learner.rls.diagnostics()
        for i,u in enumerate(trace['actual_u']):
            k,b,r=learner.values();np.testing.assert_array_equal(k,K[i]);np.testing.assert_array_equal(r,ref[i]);assert b==bias[i]
            learner.observe(z[i],u,z[i+1],bool(trace['global_clipped'][i]))
        assert learner.accepted==row['accepted'];causal=True;final_model=learner.rls.model()
        features=np.asarray(learner.rls.features);weights=learner.rls.forgetting**np.arange(len(features)-1,-1,-1)
        column_rms=np.sqrt(np.sum(weights[:,None]*features**2,axis=0)/weights.sum())
        weighted=np.sqrt(weights[:,None])*features/np.maximum(column_rms,1e-12)
        singular=np.linalg.svd(weighted,compute_uv=False);other=np.delete(weighted,23,axis=1);u=weighted[:,23]
        innovation=u-other@np.linalg.lstsq(other,u,rcond=1e-8)[0]
        model_confidence=dict(nonposition_spectral_radius=float(max(abs(np.linalg.eigvals(np.asarray(final_model['A'])[1:,1:])))),
            final_unweighted_information=learner.rls.diagnostics(),forgetting_weighted_rank=int(np.sum(singular>singular[0]*1e-8)),
            forgetting_weighted_condition=float(singular[0]/max(singular[-1],1e-300)),
            forgetting_weighted_input_innovation=float(innovation@innovation/max(u@u,1e-20)),
            covariance_max_eigenvalue=max(float(np.linalg.eigvalsh(g['P']).max()) for g in learner.rls.groups))
    return dict(steps=len(trace['actual_u']),bounds=True,target_fixed=True,leg_and_history_exact=True,
        max_cumulative_gain_change=float(cumulative.max()),causal_replay=causal,
        actual_K_changes=int(np.sum(np.any(np.diff(K,axis=0)!=0.,axis=1))),
        actual_bias_changes=int(np.sum(np.diff(bias)!=0.)),actual_reference_changes=int(np.sum(np.any(np.diff(ref,axis=0)!=0.,axis=1))),
        post_change_K_changes=int(np.sum(np.any(np.diff(K,axis=0)[2000:]!=0.,axis=1))) if phase=='shock' else None,
        local_effective_offset_range=[float(trace['effective_offset'].min()),float(trace['effective_offset'].max())],
        encoder_coordinate_effective_offset_range=[float(world_offset.min()),float(world_offset.max())],
        model_confidence=model_confidence,final_model=final_model if phase=='shock' else None)


def analyze(root,causal=False):
    plan=json.loads((root/'plan.json').read_text());verify(plan)
    phases={};integrity={};summaries={}
    for phase in ['factorial','online','shock']:
        artifact=root/(phase+'_results.json')
        if not artifact.exists():continue
        cases=json.loads(artifact.read_text())['rows'];phases[phase]=cases;phase_audit=[]
        for case in cases:
            initials=[]
            for row in case['rows']:
                if 'trace' not in row:continue
                trace=arrays(root/phase/case['job']['id']/row['trace'])
                initials.append({k:trace[k][0] for k in KEYS+['policy_observation','action']})
                phase_audit.append(dict(id=case['job']['id'],arm=row['method']+'_'+row['group'],
                    **audit_episode(root,phase,case,row,causal)))
            for values in initials[1:]:
                for key,value in values.items():np.testing.assert_array_equal(value,initials[0][key])
        integrity[phase]=phase_audit;by_condition={}
        for condition in ['nominal','gain0.8','gain1.2']:
            selected=sorted([r for r in cases if r['job']['condition']==condition],key=lambda r:r['job']['id'])
            if not selected:continue
            groups={};all_groups=sorted({(x['method'],x['group']) for c in selected for x in c['rows']})
            for method,name in all_groups:
                rows=[next((x for x in c['rows'] if x['method']==method and x['group']==name),dict(status='NOT_TESTED')) for c in selected]
                groups[method+'_'+name]=aggregate(rows)
                if phase=='shock':
                    post=[dict(r,metrics=r.get('post_change_metrics')) for r in rows if r.get('complete')]
                    groups[method+'_'+name]['post_change']=aggregate(post)
                    groups[method+'_'+name]['pre_change_qualified']=sum(r.get('pre_change_qualified',False) for r in rows)
            by_condition[condition]=groups
        summaries[phase]=by_condition
    # Explicit E7/E6 comparisons cannot be replaced by a Full-vs-Fixed headline.
    extra={}
    for phase,cases in phases.items():
        for condition in ['nominal','gain0.8','gain1.2']:
            selected=sorted([r for r in cases if r['job']['condition']==condition],key=lambda r:r['job']['id'])
            if not selected:continue
            for method in ['B1','B2']:
                a=[next((r for r in c['rows'] if r['group']=='E6' and r['method']==method),{}) for c in selected]
                b=[next((r for r in c['rows'] if r['group']=='E7' and r['method']==method),{}) for c in selected]
                if phase=='shock':
                    a=[dict(r,metrics=r.get('post_change_metrics')) for r in a];b=[dict(r,metrics=r.get('post_change_metrics')) for r in b]
                extra[phase+'_'+condition+'_'+method]=compare(b,a)
    write(root/'analysis_integrity.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        causal_replay_requested=causal,episodes=integrity))
    summary=dict(execution_domain='DESKTOP_DRY_RUN',phases=summaries,E7_vs_E6=extra,
        smoke=plan['smoke'],training_seed=plan['training_seed'],evaluation_seeds=plan['evaluation_seeds'],
        no_independent_population_significance=True)
    write(root/'summary.json',summary);figures(root,phases)
    if phases.get('shock'):
        decisions={}
        for condition,groups in summaries.get('shock',{}).items():
            cases=sorted([r for r in phases['shock'] if r['job']['condition']==condition],key=lambda r:r['job']['id'])
            baseline=[next(x for x in c['rows'] if x['group']=='E0') for c in cases]
            baseline=[dict(x,metrics=x['post_change_metrics']) for x in baseline]
            decisions[condition]={}
            for label in groups:
                method,name=label.split('_');selected=[next((x for x in c['rows'] if x['group']==name and x['method']==method),{}) for c in cases]
                rows=[dict(x,metrics=x.get('post_change_metrics')) for x in selected]
                result=compare(rows,baseline)
                qualified=all(x.get('pre_change_qualified',False) for x in selected)
                result['pre_change_qualified']=qualified
                result['performance']=bool(result['performance'] and qualified)
                if all(x.get('complete') for x in selected):
                    result['post_change_max_planar_ratio']=float(np.median([x['post_change_metrics']['max_planar'] for x in selected])/
                        max(np.median([x['metrics']['max_planar'] for x in baseline]),1e-12))
                    result['recovered_count']=sum(x['post_change_metrics']['recovery_s'] is not None for x in selected)
                    result['fixed_recovered_count']=sum(x['metrics']['recovery_s'] is not None for x in baseline)
                decisions[condition][label]=result
        write(root/'shock_decision.json',dict(execution_domain='DESKTOP_DRY_RUN',conditions=decisions,
            metric_scope='All post-change error stays relative to original pre-prefix target; no waiting period excluded'))
    return summary


def validate_gain_source_models(root):
    """Use the very same saved independent inputs for final and K-source models."""
    output=[]
    for phase in ['factorial','online','shock']:
        path=root/(phase+'_results.json')
        if not path.exists():continue
        for case in json.loads(path.read_text())['rows']:
            if phase=='factorial':
                source=root/'training'/case['job']['training_id']/'events_B1.json'
                folder=root/'factorial'/case['job']['id'];records=json.loads(source.read_text())['models']
                work=[('shared_frozen_K',folder,records)]
            else:
                work=[]
                for row in case['rows']:
                    if row['group']=='E0' or not MASKS[row['group']][0] or 'trace' not in row:continue
                    source=root/phase/case['job']['id']/((row['method']+'_'+row['group'] if phase=='online' else row['group'])+'_updates.json')
                    folder=(root/'online'/case['job']['id']/(row['method']+'_'+row['group']+'_final_prediction')
                        if phase=='online' else root/'shock_validation'/case['job']['id']/row['group'])
                    if not folder.exists():continue
                    work.append((row['method']+'_'+row['group'],folder,json.loads(source.read_text())['models']))
            for arm,folder,records in work:
                gate=json.loads((folder/'independent_prediction.json').read_text())
                if 'direct_B_v' not in gate:
                    output.append(dict(phase=phase,id=case['job']['id'],arm=arm,status='NOT_TESTED',reason=gate));continue
                base=arrays(folder/'probe_baseline.npz');data=[];inputs=[]
                for family in ['validation_sine','validation_prbs','pulse_pos','pulse_neg','step_pos','step_neg','bipulse_pos','bipulse_neg']:
                    probe=arrays(folder/('probe_'+family+'.npz'));data.append(state(probe)-state(base));inputs.append(probe['actual_u']-base['actual_u'])
                scores=[]
                for record in records:
                    value=prediction_gate(dict(record['model'],indices=list(range(24))),data,inputs,gate['direct_B_v'])
                    scores.append(dict(step=record['step'],gate=value['gate'],prediction=value['prediction'],B_relative_error=value['B_relative_error']))
                output.append(dict(phase=phase,id=case['job']['id'],arm=arm,status='TESTED',scores=scores,
                    final_adopted_model_gate=scores[-1]['gate'] if scores else None,
                    no_model_retraining=True,same_independent_inputs_as_final_RLS_model=True))
    write(root/'gain_source_model_validation.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=output))


def validate_shock_case(item,cfg,root):
    root=Path(root);case=item['case'];row=item['row'];record=item['record']
    out=root/'shock_validation'/case['job']['id']/row['group'];out.mkdir(parents=True)
    original=root/'shock'/case['job']['id'];prefix=arrays(original/'nominal_prefix.npz');trace=arrays(original/row['trace'])
    snapshot=load_snapshot(root/'acquisition'/case['job']['source_id']/'snapshot.pkl.gz')['snapshot']
    r=init_effect(cfg,case['job'],snapshot,{})
    try:
        replay(r,prefix)
        for i in range(len(trace['actual_u'])+1):
            for key in KEYS:np.testing.assert_array_equal(r.observation[key],trace[key][i])
            if i==2000:r.effect['gain']=case['job']['change_gain']
            if i<len(trace['actual_u']):
                step=r.step(float(trace['requested_u'][i]))
                for key,value in step.items():np.testing.assert_array_equal(value,trace[key][i])
        write(out/'model_frozen.json',record['final_model']);h=sha256(out/'model_frozen.json')
        validation=test_model(r,r.effect_snapshot(),dict(model=record['final_model']),out,
            float(trace['actual_u'][-1]),case['job']['seed']*831+int(row['group'][1:]))
        assert sha256(out/'model_frozen.json')==h
        result=dict(id=case['job']['id'],group=row['group'],model_sha256=h,validation=validation,
            original_post_change_trajectory_exact=True,no_refit_or_controller_change=True)
        write(out/'results.json',result);return result
    finally:r.env.close()


def validate_shock_models(root,workers):
    out=root/'shock_validation';assert not out.exists();out.mkdir()
    cases=json.loads((root/'shock_results.json').read_text())['rows']
    audit=json.loads((root/'analysis_integrity.json').read_text());items=[]
    for case in cases:
        for row in case['rows']:
            if row['group'] not in ['E1','E7'] or not row['complete']:continue
            record=next(x for x in audit['episodes']['shock'] if x['id']==case['job']['id'] and x['arm']=='B1_'+row['group'])
            assert record['causal_replay'] and record['final_model'] is not None
            items.append(dict(case=case,row=row,record=record))
    cfg=json.loads(prepared_config(CKPT).read_text())
    code_hash=sha256(Path(__file__))
    write(root/'shock_validation_plan.json',dict(execution_domain='VALIDATION_SIM',
        source_sha256=code_hash,items=[dict(id=i['case']['job']['id'],group=i['row']['group']) for i in items],
        probing='Matched4s8families0.01Nm, final reconstructed actual RLS model; exact full shock replay first',
        no_new_parameters_or_controller=True))
    rows=parallel(validate_shock_case,items,workers,cfg,str(root)) if items else []
    assert sha256(Path(__file__))==code_hash
    write(root/'shock_model_validation.json',dict(execution_domain='VALIDATION_SIM',rows=rows,
        status='TESTED' if rows else 'NOT_TESTED',reason=None if rows else 'No eligible completed K-adaptive shock arm'))


def figures(root,phases):
    for phase,cases in phases.items():
        if not cases:continue
        conditions=sorted({r['job']['condition'] for r in cases});fig,axes=plt.subplots(len(conditions),3,
            figsize=(18,4*len(conditions)),squeeze=False)
        for i,condition in enumerate(conditions):
            representative=next((r for r in cases if r['job']['condition']==condition and r['job']['seed']==420 and r['job']['pitch']==0.),
                next(r for r in cases if r['job']['condition']==condition))
            for row in representative['rows']:
                if row['method']!='B1' or 'trace' not in row:continue
                trace=arrays(root/phase/representative['job']['id']/row['trace']);t=np.arange(len(trace['sensor']))*DT
                axes[i,0].plot(t,trace['base_path']*1000,label=row['group'])
                axes[i,1].plot(t[:-1],trace['actual_u'],label=row['group'])
                axes[i,2].plot(t[:-1],trace['effective_offset'],label=row['group'])
            for ax in axes[i]:
                ax.set_title(condition);ax.set_xlabel('time [s]');ax.grid(alpha=.3);ax.legend(fontsize=7)
                if phase=='shock':ax.axvline(40.,color='gray',ls='--')
            axes[i,0].set_ylabel('base sagittal error [mm]');axes[i,1].set_ylabel('total residual command [Nm]')
            axes[i,2].set_ylabel('effective offset [Nm]')
        fig.tight_layout();fig.savefig(root/(phase+'_comparison.png'),dpi=150);plt.close(fig)


def audit(root,report):
    plan=json.loads((root/'plan.json').read_text());verify(plan)
    assert not plan['smoke'],'Smoke cannot satisfy the research completion audit'
    state_=json.loads((root/'pipeline_state.json').read_text());assert state_['status']=='COMPLETE'
    assert set(state_['stages'])=={'legacy','train','acquire','factorial','online','shock'}
    for name,record in state_['stages'].items():assert sha256(root/record['artifact'])==record['sha256']
    assert hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest()==plan['tracked_diff_sha256']
    for p,h in plan['source_sha256'].items():assert sha256(REPO/p)==h
    assert len(json.loads((root/'legacy_results.json').read_text())['rows'])==3
    trained=json.loads((root/'train_results.json').read_text())['rows'];assert len(trained)==9
    acquired=json.loads((root/'acquire_results.json').read_text())['rows']
    assert len(acquired)==6 and all(r['complete'] and r['low_speed_qualification'] for r in acquired)
    for row in trained:
        fpath=root/'training'/row['id']/'frozen.json';assert sha256(fpath)==row['frozen_sha256']
        f=json.loads(fpath.read_text());assert f['train_seed'] not in plan['evaluation_seeds']
        np.testing.assert_array_equal(f['model']['state_reference'],nominal()['state_reference'])
        m=f['model'];A=np.asarray(m['A']);B=np.asarray(m['B']);center=np.asarray(m['state_reference'])
        np.testing.assert_array_equal(A[:,0],np.eye(24)[:,0])
        np.testing.assert_array_equal(B[4:12],np.zeros(8))
        np.testing.assert_allclose(m['c_absolute'],center-A@center-B*m['input_reference']+m['c_center'],atol=1e-12)
    factorial=json.loads((root/'factorial_results.json').read_text())['rows'];assert len(factorial)==18
    for case in factorial:
        assert case['evaluation_seed_not_in_training']
        assert {(r['method'],r['group']) for r in case['rows']}=={('B1',name) for name in MASKS}|{('B2',name) for name,m in MASKS.items() if m[1]}
        fpath=root/'training'/case['job']['training_id']/'frozen.json';assert sha256(fpath)==case['frozen_sha256']
    evidence=json.loads((root/'analysis_integrity.json').read_text());assert evidence['causal_replay_requested']
    for phase,rows in evidence['episodes'].items():
        for row in rows:
            if phase!='factorial' and not row['arm'].endswith('_E0'):assert row['causal_replay']
    online=json.loads((root/'online_results.json').read_text())['rows']
    previous=json.loads((root/'factorial_decision.json').read_text())['conditions']
    permitted={condition for condition,arms in previous.items() if any(v['performance'] for v in arms.values())}
    assert {case['job']['condition'] for case in online}==permitted
    assert len(online)==6*len(permitted)
    shock=json.loads((root/'shock_results.json').read_text())['rows']
    previous=json.loads((root/'online_decision.json').read_text())['conditions']
    permitted={condition for condition,arms in previous.items() if condition!='nominal' and any(v['performance'] for v in arms.values())}
    assert {case['job']['condition'] for case in shock}==permitted
    assert len(shock)==6*len(permitted)
    assert (root/'shock_model_validation.json').exists()
    assert (root/'gain_source_model_validation.json').exists()
    supplementary=root/'guarded_shock'
    assert (supplementary/'shock_results.json').exists()
    expanded=json.loads((supplementary/'shock_results.json').read_text())['rows']
    assert len(expanded)==6*len(permitted)
    for case in expanded:
        assert {r['group'] for r in case['rows']}=={'E0','E1','E2','E6','E7'}
    original_decision=json.loads((root/'online_decision.json').read_text())
    guarded_decision=json.loads((supplementary/'online_decision.json').read_text())
    for condition,arms in original_decision['conditions'].items():
        for name,record in arms.items():
            revised=guarded_decision['conditions'][condition][name]
            assert revised.get('model_gate')==record.get('model_gate')
            assert revised['performance']==record['performance']
            assert revised['admissible']==record.get('physical_stable',False)
    duplicate=json.loads((supplementary/'shared_comparator_replay.json').read_text())
    assert duplicate['evidence_status']=='PASS'
    guard_audit=json.loads((supplementary/'analysis_integrity.json').read_text())
    assert guard_audit['causal_replay_requested']
    for row in guard_audit['episodes'].get('shock',[]):
        if not row['arm'].endswith('_E0'):assert row['causal_replay']
    assert (supplementary/'shock_model_validation.json').exists()
    assert (supplementary/'gain_source_model_validation.json').exists()
    blind=json.loads((supplementary/'prechange_blindness.json').read_text())
    assert blind['evidence_status']=='PASS'
    assert blind['same_controller_before_different_hidden_gain_conditions_exact_pairs']==30
    independent=json.loads((supplementary/'shock_model_validation.json').read_text())['rows']
    assert len(independent)==24 and all(x['original_post_change_trajectory_exact'] for x in independent)
    source_checks=json.loads((supplementary/'gain_source_model_validation.json').read_text())['rows']
    assert len(source_checks)==24 and all(x['status']=='TESTED' and x['scores'] for x in source_checks)
    active=[x for x in guard_audit['episodes']['shock'] if x['arm'] in ['B1_E1','B1_E7']]
    assert len(active)==24
    # Keep scientific failures explicit even when every requested run completed.
    scientific=dict(execution_domain='DESKTOP_DRY_RUN',
        independent_final_RLS_passes=sum(x['validation']['gate'] for x in independent),
        independent_final_RLS_total=len(independent),
        K_enabled_shock_episodes=len(active),
        episodes_with_post_change_K_adoption=sum(x['post_change_K_changes']>0 for x in active),
        interpretation='Operating-point recovery and validated post-change dynamics/gain adaptation are separate claims.')
    write(root/'scientific_completion_facts.json',scientific)
    sources=[REPO/'test'/s for s in ['m4_joint_adaptation.py','eval_m4_joint_pipeline.py','test_m4_joint_adaptation.py',
        'test_joint_shared_budget.py','analyze_joint_operating_results.py','run_joint_guarded_shock.py','test_joint_shock_admission.py']]
    diffs=[]
    for path in sources+[report]:
        result=subprocess.run(['git','diff','--no-index','/dev/null',str(path)],capture_output=True);assert result.returncode in [0,1];diffs.append(result.stdout)
        check=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(path)],capture_output=True)
        assert check.returncode in [0,1] and not check.stdout and not check.stderr
    (root/'task.diff').write_bytes(b''.join(diffs))
    requirements={
        'A0_exact_original_nominal_and_adaptive':'legacy_results.json + exact full observation/action/substep torque replay',
        'A1_bias_methods_and_reference':'training/*/constant_*.npz, events_B1/B2.json, frozen.json; sensor-only API',
        'A2_E0_E7_independent_seeds':'18 new contexts; every arm executed or explicit component gate NOT_TESTED; immutable train hashes',
        'B1_real_time_updates':'online_results.json, online_decision.json, parameter histories and causal replay; prerequisite skips retained',
        'C1_abrupt_private_gain_change':'guarded_shock/shock_results.json:five physically stable guarded comparators; '
            '40s nominal +120s after private gain change; original model/performance flags preserved; '
            'restricted original common arms exact in shared_comparator_replay.json; no double counting',
        'invariants':'analysis_integrity.json: offsets, fixed target/v, nominal RLS center, shared bounds/slew, raw history/leg torque',
        'scientific_limits':'scientific_completion_facts.json: independent final RLS accuracy and actual post-change K adoption counted separately',
        'future_D_E':'Not current deployment: mass/lag full adaptation and hardware are not executed; roadmap gates preserved'}
    write(root/'completion_audit.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',requirements=requirements,
        previous_hashes_unchanged=len(plan['protected_sha256']),tracked_diff_preserved=True,
        branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip(),
        source_sha256={str(p.relative_to(REPO)):sha256(p) for p in sources+[report]},
        claim='Requested experiments and conditional workflow audited, not a claim that all controllers improved.'))
    for link in re.findall(r'\]\(([^)]+)\)',report.read_text()):assert (report.parent/link).exists(),link


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True)
    p.add_argument('--causal-replay',action='store_true');p.add_argument('--report',type=Path)
    p.add_argument('--validate-shock',action='store_true');p.add_argument('--workers',type=int,default=3)
    p.add_argument('--gain-source-validation',action='store_true')
    args=p.parse_args();root=args.root.resolve();analyze(root,args.causal_replay)
    if args.validate_shock:validate_shock_models(root,args.workers)
    if args.gain_source_validation:validate_gain_source_models(root)
    if args.report:audit(root,args.report.resolve())
