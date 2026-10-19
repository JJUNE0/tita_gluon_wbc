"""DESKTOP_DRY_RUN: post-hoc numerical cross-check and saved-evidence audit.

No new hyperparameters, model selection, dynamics collection or gain activation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

import numpy as np

from online_local_m4 import verify,write,sha256,REPO,nominal,ConstrainedRLS,features,NOMINAL_ROOT,read_new
from run_online_local_m4 import a_streams,friction_score
from nominal_m4_diagnosis import score


def numerical(root):
    plan=verify(root,full=True);bundle=json.loads((root/'A_models_frozen.json').read_text())['models'];before=sha256(root/'A_models_frozen.json');rows=[]
    outcomes=json.loads((root/'A_results.json').read_text())['rows']
    for cohort in plan['A']['cohorts']:
        streams=a_streams(cohort);X,Y=features(streams);qr=ConstrainedRLS(nominal());Rs=[];Cs=[]
        for g in qr.groups:
            R=np.eye(len(g['columns']))/10.;Rs.append(R);Cs.append(R@g['theta'].T)
        for x,y in zip(X,Y):
            for i,g in enumerate(qr.groups):
                Q,R=np.linalg.qr(np.vstack([Rs[i]*np.sqrt(.9995),x[g['columns']]]),mode='reduced')
                Cs[i]=Q.T@np.vstack([Cs[i]*np.sqrt(.9995),y[g['rows']]]);Rs[i]=R
        for i,g in enumerate(qr.groups):g['theta']=np.linalg.solve(Rs[i],Cs[i]).T
        model=qr.model();batch=bundle[cohort+'/A2_weighted_batch']['model'];A=np.asarray(batch['A']);B=np.asarray(batch['B']);c=np.asarray(batch['c_center'])
        full=np.column_stack([A[:,1:]*qr.scale[None,1:]/qr.scale[:,None],B*.05/qr.scale,c/qr.scale])
        difference=max(float(np.linalg.norm(g['theta']-full[np.ix_(g['rows'],g['columns'])])/max(np.linalg.norm(full[np.ix_(g['rows'],g['columns'])]),1e-15))for g in qr.groups)
        if cohort.startswith('nominal'):
            test,direct=read_new(NOMINAL_ROOT,'test',float(cohort[7:]));result=score(model,test,direct);passed=result['passed_contexts']
        else:passed=friction_score(model)['passed']
        original=next(r for r in outcomes if r['key']==cohort+'/A2_weighted_batch')['passed'];weight=.9995**np.arange(len(X)-1,-1,-1)
        nbase=2400 if cohort.startswith('nominal')else 0
        rows.append(dict(cohort=cohort,relative_theta_QR_vs_A2=difference,status='PASS'if difference<=1e-7 else'SUSPICIOUS',QR_passed=passed,A2_passed=original,
            nominal_order='all78probe streams followed by6unique baselines; transitions within each stream ordered'if nbase else'three real training streams in fixed sorted order',
            samples=len(X),baseline_unweighted_fraction=nbase/len(X),baseline_weighted_fraction=float(weight[-nbase:].sum()/weight.sum())if nbase else None,
            effective_forgetting_samples=1./(1.-.9995)))
        print('DESKTOP_DRY_RUN QR audit',cohort,difference,passed,original,flush=True)
    assert sha256(root/'A_models_frozen.json')==before
    write(root/'A_QR_numerical_audit.json',dict(execution_domain='DESKTOP_DRY_RUN',posthoc=True,no_model_replacement=True,settings_unchanged=True,source_sha256=sha256(Path(__file__)),rows=rows))


def final(root):
    plan=verify(root,full=True);integrity=json.loads((root/'analysis_integrity.json').read_text());admission=json.loads((root/'B_admission.json').read_text())
    assert all(not r['C_permitted']for r in admission['domains'].values()),'C is READY; execute preregistered admitted C before completing task'
    count=0;hashes={}
    for split,expected in [('development',12),('test',24)]:
        rows=json.loads((root/(split+'_results.json')).read_text())['rows'];assert len(rows)==expected
        for ep in rows:
            assert ep['physical']['complete']and ep['steps']==3200 and ep['target_static']and ep['goal_immutable']and ep['new_K_adoptions']==0
            folder=root/split/ep['job']['id'];physics=json.loads((folder/'physics.json').read_text());assert physics['configured_before_first_step']
            with np.load(folder/'trajectory.npz')as t:
                np.testing.assert_array_equal(t['raw_requested'],t['requested_u']);assert max(abs(t['actual_u']-t['requested_u']))<1e-6
                np.testing.assert_array_equal(t['K_used'],np.broadcast_to(t['K_used'][0],t['K_used'].shape));np.testing.assert_array_equal(t['reference_used'],np.broadcast_to(t['reference_used'][0],t['reference_used'].shape))
                assert np.max(abs(t['bias']-.4828))==0.
            for e in ep['events']:
                file=folder/e['candidate_file'];assert sha256(file)==e['candidate_sha256'];count+=len(e['verdicts'])
            hashes[str(folder/'trajectory.npz')]=sha256(folder/'trajectory.npz')
    assert count==540 and integrity['candidate_verdicts']==540 and integrity['episodes']==36
    A=json.loads((root/'A_numerics.json').read_text())['rows'];qr=json.loads((root/'A_QR_numerical_audit.json').read_text())
    assert all(r['status']=='PASS'and r['QR_passed']==r['A2_passed']for r in qr['rows'])
    assert 'Ran 5 tests'in (root/'unit_tests.log').read_text()and 'OK'in (root/'unit_tests.log').read_text()
    check=(root/'agent_check.log').read_text();assert check.rstrip().endswith('FAIL')and check.count('trailing whitespace.')==6
    current=hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest();branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip();assert branch.startswith('agent/')
    source=Path(__file__);shutil.copy2(source,root/(source.name+'.source.txt'))
    owned=[REPO/'test'/Path(p).name for p in plan['source_sha256']]+[source,root.parent/'SUMMARY.md',root.parent/'PLAN.md',root/'REPORT.md'];diff=[]
    for p in owned:
        v=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True);assert v.returncode in [0,1]and not v.stdout and not v.stderr
        v=subprocess.run(['git','diff','--no-index','--','/dev/null',str(p)],capture_output=True,text=True);assert v.returncode==1;diff.append(v.stdout)
    (root.parent/'task.diff').write_text('\n'.join(diff))
    write(root/'completion_audit.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS'if current==plan['tracked_diff_sha256']else'SUSPICIOUS',
        meaning='Evidence/workflow audit; scientific model failures and A3 numerical suspicions retained',branch=branch,
        protected_files=len(plan['protected_sha256']),tracked_diff_unchanged=current==plan['tracked_diff_sha256'],
        plan_sha256=sha256(root/'plan.json'),source_sha256=plan['source_sha256'],posthoc_audit_source_sha256=sha256(source),
        A_models_sha256=sha256(root/'A_models_frozen.json'),A_raw_recursive_statuses=A,A_QR_audit=qr,
        new_episodes=36,complete=36,unique_future_validation_sequences=108,candidate_verdicts=540,Direct_B_or_snapshot_branches=0,
        old_policy_runtime_QR_unchanged=True,causal_exclusion_and_goals=integrity,new_K_adoptions=0,C_status='NOT_TESTED: B prerequisites fail both domains',
        tests='5 unit PASS; QR vs same-cost batch PASS; all36 sensor/action/native leg and torque budget audits PASS; global agent-check FAIL old whitespace6',
        trajectory_sha256=hashes,owned_files=list(map(str,owned)),task_diff_sha256=sha256(root.parent/'task.diff'),report_sha256=sha256(root.parent/'SUMMARY.md'),
        no_hardware=True,no_commit_push=True,no_production_or_policy_change=True))
    print('DESKTOP_DRY_RUN final evidence audit PASS; scientific B FAIL/C NOT_TESTED retained',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--stage',choices=['numerical','final'],required=True);a=p.parse_args()
    (numerical if a.stage=='numerical'else final)(a.root.resolve())
