"""DESKTOP_DRY_RUN: frozen same-transition LS/RLS comparison, no simulation.

Read the earlier single-rollout sensor/known-command logs. Do not activate a
model, collect branches, change gates, or tune against the reused future data.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

import numpy as np

from online_local_m4 import (REPO, BIAS, B_SETTINGS, CHECKPOINTS, features,
    objective, nominal, ConstrainedRLS, validate_candidate, training_allowed,
    sha256, write, verify as verify_old)
from flash_cold_start_abc import fit_batch
from analyze_flash_state_learning import state
from run_static_target_adaptation import clean

OLD = REPO/'docs/exp/2026-10-16/online_local_m4_identification/run_01'
SOURCES = ['compare_single_rollout_ls_rls.py', 'test_single_rollout_ls_rls.py']
METHODS = ['plain_LS', 'same_cost_batch', 'raw_RLS', 'candidate_RLS']


def select_indices(candidate, eligible, setting):
    """Match the original estimator's recorded end timestamps, not a new mask."""
    times = np.asarray(candidate['training_times'])
    indices = np.rint(times/.02).astype(int)-1
    assert len(indices) and np.all(np.diff(indices)>0)
    np.testing.assert_allclose((indices+1)*.02, times, rtol=0, atol=1e-10)
    assert indices.min()>=0 and indices.max()<len(eligible)
    assert np.asarray(eligible)[indices].all()
    assert all(training_allowed(i*.02) for i in indices)
    end = (np.arange(len(eligible))+1)*.02
    expected = np.asarray(eligible).astype(bool) & (end<=candidate['created']+1e-9)
    if setting['window'] is not None:
        expected &= end>candidate['created']-setting['window']+1e-9
    np.testing.assert_array_equal(indices, np.flatnonzero(expected))
    return indices


def model_difference(a, b):
    rls = ConstrainedRLS(nominal())
    def theta(model):
        return np.column_stack([np.asarray(model['A'])[:,1:]*rls.scale[None,1:]/rls.scale[:,None],
            np.asarray(model['B'])*.05/rls.scale, np.asarray(model['c_center'])/rls.scale])
    x,y = theta(a),theta(b)
    return max(float(np.linalg.norm((x-y)[np.ix_(g['rows'],g['columns'])]) /
        max(np.linalg.norm(y[np.ix_(g['rows'],g['columns'])]),1e-15)) for g in rls.groups)


def source_jobs():
    jobs=[]
    for split in ['development','test']:
        for episode in json.loads((OLD/(split+'_results.json')).read_text())['rows']:
            # Retrospective comparison: prior outcomes exist, but never choose
            # fit settings, samples, or models using these verdicts.
            jobs.append(dict(split=split, job=episode['job'], events=[
                {k:e[k] for k in ['created','candidate_file','candidate_sha256']}
                for e in episode['events']]))
    return jobs


def initialize(root):
    assert not root.exists(), 'Refusing existing output'
    oldplan=verify_old(OLD,full=True)
    branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip()
    assert branch.startswith('agent/')
    protected=dict(oldplan['protected_sha256'])
    protected.update({str(p):sha256(p) for p in OLD.parent.rglob('*') if p.is_file()})
    for p in (REPO/'test').glob('*.py'):
        if p.name not in SOURCES: protected[str(p)]=sha256(p)
    root.mkdir(parents=True)
    plan=dict(execution_domain='DESKTOP_DRY_RUN',checkpoint_sha256=oldplan['checkpoint_sha256'],
        branch=branch,source_root=str(OLD),protected_sha256=protected,
        tracked_diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest(),
        source_sha256={str(REPO/'test'/n):sha256(REPO/'test'/n) for n in SOURCES},
        jobs=source_jobs(), settings=B_SETTINGS, methods=METHODS,
        protocol='Retrospective existing 36 single rollouts only; no fresh physics or unseen-test claim',
        primary_fit='Plain constrained affine LS; existing group RMS scaling and rcond=1e-8; no prior/forgetting',
        comparisons='Same-cost batch with original prior/forgetting; recorded raw covariance RLS; recorded same-cost-refined RLS candidate',
        matching='Exact original recorded training end timestamps, eligibility, nominal coordinates, p_hold, action B rows, and transition commands',
        freeze='All models for all episodes frozen in fit stage before any future scoring in score stage',
        validation='Same original subsequent 4s sensors/known commands at 10/30/60; all validation windows permanently excluded from every fit',
        gates=oldplan['B']['prediction'], information=oldplan['B']['information'],
        interpretation='Report prediction-only and full information/prediction/conditional-B gates separately; common conditional-B failure is not model prediction failure',
        no_selection=True,no_new_controller=True,no_new_K=True,no_budget_or_state_QR_changes=True,
        no_new_simulation=True,no_hardware=True,no_oracle_inputs=True)
    write(root/'plan.json',plan);(root/'plan.sha256').write_text(sha256(root/'plan.json')+'\n')
    for n in SOURCES:shutil.copy2(REPO/'test'/n,root/(n+'.source.txt'))
    shutil.copy2('/tmp/single_rollout_ls_status_before.txt',root/'status_before.txt')


def verify(root,full=False):
    plan=json.loads((root/'plan.json').read_text())
    assert sha256(root/'plan.json')==(root/'plan.sha256').read_text().strip()
    for p,h in plan['source_sha256'].items():assert sha256(Path(p))==h,p
    if full:
        for p,h in plan['protected_sha256'].items():assert sha256(Path(p))==h,p
    return plan


def fit_one(args):
    root,job=args;root=Path(root);folder=OLD/job['split']/job['job']['id'];output=root/'models'/job['split']/job['job']['id']
    output.mkdir(parents=True)
    with np.load(folder/'trajectory.npz') as archive:
        z=state(archive);z[:,0]-=float(archive['p_hold'])
        u=archive['actual_u'].copy();eligible=archive['training_used'].astype(bool)
    rows=[]
    for event in job['events']:
        original=folder/event['candidate_file'];assert sha256(original)==event['candidate_sha256']
        candidates=json.loads(original.read_text())['candidates'];end=round(event['created']/.02)
        for setting in B_SETTINGS:
            c=candidates[setting['name']];assert c['status']=='FROZEN'
            ids=select_indices(c,eligible,setting);mask=np.zeros(end,dtype=bool);mask[ids]=True
            # Fit gets only prefix arrays. Even unselected future observations
            # cannot enter the fitter, feature scaling, or normalizer.
            streams=[(z[:end+1],u[:end],mask)]
            plain,diagnostics=fit_batch(streams)
            X,Y=features(streams);batch,_=objective(X,Y,setting['forgetting'],setting['P'])
            same=batch.model();difference=model_difference(same,c['model'])
            info=c['information'];common=bool(info['samples']>=250 and info['rank']==25 and
                info['condition']<=1e6 and info['input_innovation']>=.01)
            assert common==info['gate'], 'Original P gate differs: report separately before scoring'
            rows.append(dict(created=event['created'],setting=setting['name'],
                training_indices=ids.tolist(),training_indices_sha256=hashlib.sha256(ids.astype('<i8').tobytes()).hexdigest(),
                original_candidate_sha256=event['candidate_sha256'],information=info,common_information_gate=common,
                LS_diagnostics=diagnostics,same_cost_relative_difference=difference,
                same_cost_status='PASS' if difference<=1e-7 else 'SUSPICIOUS',
                models=dict(plain_LS=plain,same_cost_batch=same,raw_RLS=c['raw_recursive_model'],candidate_RLS=c['model'])))
    file=output/'models_frozen.json';write(file,dict(execution_domain='DESKTOP_DRY_RUN',job=job,rows=rows))
    print('DESKTOP_DRY_RUN frozen',job['job']['id'],len(rows),flush=True)
    return dict(file=str(file.relative_to(root)),sha256=sha256(file),rows=len(rows))


def score_one(args):
    root,record=args;root=Path(root);file=root/record['file'];assert sha256(file)==record['sha256']
    bundle=json.loads(file.read_text());job=bundle['job'];folder=OLD/job['split']/job['job']['id']
    original=json.loads((folder/'results.json').read_text())
    with np.load(folder/'trajectory.npz') as archive:
        z=state(archive);z[:,0]-=float(archive['p_hold']);u=archive['actual_u'].copy()
    rows=[];cache={}
    for fit in bundle['rows']:
        start=round(fit['created']/.02);future_z=z[start:start+201];future_u=u[start:start+200]
        old=next(e for e in original['events'] if e['created']==fit['created'])['verdicts'][fit['setting']]
        safe='safe_validation' not in old['reject_reasons']
        scores={}
        for name,model in fit['models'].items():
            key=(start,hashlib.sha256(json.dumps({k:model[k] for k in ['A','B','c_center','state_reference']},sort_keys=True).encode()).hexdigest())
            if key not in cache:cache[key]=validate_candidate(model,future_z,future_u)
            score=cache[key]
            if name=='candidate_RLS':
                assert clean(score)==old['prediction'], 'Original validation must reproduce exactly'
                assert bool(score['gate'] and fit['common_information_gate'] and safe)==old['gate']
            scores[name]=dict(prediction=score,
                full_gate=bool(score['gate'] and fit['common_information_gate'] and safe),
                prediction_gate=score['prediction_gate'],safe_validation=safe)
        rows.append(dict(split=job['split'],**{k:job['job'][k] for k in ['id','domain','amplitude','seed','pitch']},
            created=fit['created'],setting=fit['setting'],information=fit['information'],
            common_information_gate=fit['common_information_gate'],LS_diagnostics=fit['LS_diagnostics'],
            same_cost_status=fit['same_cost_status'],same_cost_relative_difference=fit['same_cost_relative_difference'],scores=scores))
    out=root/'scores'/job['split']/job['job']['id'];out.mkdir(parents=True)
    write(out/'comparison.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=rows))
    print('DESKTOP_DRY_RUN scored',job['job']['id'],flush=True)
    return rows


def summarize(root,rows):
    summary=[]
    for split in ['development','test']:
        for domain in ['nominal','friction0.2']:
            for amp in [.01,.02]:
                for setting in B_SETTINGS:
                    selected=[r for r in rows if r['split']==split and r['domain']==domain and r['amplitude']==amp and r['setting']==setting['name']]
                    item=dict(split=split,domain=domain,amplitude=amp,setting=setting['name'],total=len(selected),
                        information_pass=sum(r['common_information_gate'] for r in selected),methods={})
                    for name in METHODS:
                        scores=[r['scores'][name] for r in selected]
                        item['methods'][name]=dict(prediction_pass=sum(s['prediction_gate'] for s in scores),
                            full_pass=sum(s['full_gate'] for s in scores),
                            conditional_B_pass=sum(s['prediction']['conditional_B']['gate'] for s in scores),
                            rolling2s_pv_NRMSE_median=np.median([s['prediction']['rolling']['100']['NRMSE'] for s in scores],axis=0).tolist(),
                            full4s_pv_RMSE_median=np.median([s['prediction']['full']['200']['RMSE'] for s in scores],axis=0).tolist())
                    for compare in ['raw_RLS','candidate_RLS']:
                        item['prediction_pair_'+compare]={label:sum(bool(r['scores']['plain_LS']['prediction_gate'])==a and bool(r['scores'][compare]['prediction_gate'])==b for r in selected)
                            for label,a,b in [('both_pass',True,True),('LS_only',True,False),('RLS_only',False,True),('both_fail',False,False)]}
                    summary.append(item)
    write(root/'comparison.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=rows,summary=summary,
        physical_rollouts_reused=36,unique_future_sequences=108,matched_training_sets=len(rows),model_evaluations=len(rows)*4,
        no_new_simulation=True,no_model_selection=True))
    with (root/'metrics.csv').open('w',newline='') as file:
        writer=csv.writer(file);writer.writerow(['split','domain','amplitude','seed','pitch','time','setting','method','prediction_pass','full_pass','conditional_B_pass','rank','condition','innovation','p2s_NRMSE','v2s_NRMSE','p4s_RMSE_m','v4s_RMSE_m_s'])
        for row in rows:
            for name,s in row['scores'].items():
                info=row['information'];pred=s['prediction'];writer.writerow([row['split'],row['domain'],row['amplitude'],row['seed'],row['pitch'],row['created'],row['setting'],name,s['prediction_gate'],s['full_gate'],pred['conditional_B']['gate'],info['rank'],info['condition'],info['input_innovation'],*pred['rolling']['100']['NRMSE'],*pred['full']['200']['RMSE']])
    lines=['# Single-rollout LS/RLS — saved-data comparison','',
        'Execution Domain: **DESKTOP_DRY_RUN**','',
        'Policy Checkpoint SHA256: `'+verify(root)['checkpoint_sha256']+'`','',
        'Evidence Status: PASS/FAIL model gates below; same data are reused, no new physical validation.','',
        'Observed Metrics / Behavior / Log Summary: same training transitions and same subsequent sensor/command windows for every paired comparison.','',
        '| Split / domain / amplitude | Window / RLS setting | N | Plain LS prediction | Raw RLS prediction | Candidate RLS prediction | Same-cost Batch prediction | Full PASS, all methods |',
        '|---|---|---:|---:|---:|---:|---:|---|']
    for r in summary:
        m=r['methods'];lines.append(f'|{r["split"]}/{r["domain"]}/{r["amplitude"]}|{r["setting"]}|{r["total"]}|{m["plain_LS"]["prediction_pass"]}|{m["raw_RLS"]["prediction_pass"]}|{m["candidate_RLS"]["prediction_pass"]}|{m["same_cost_batch"]["prediction_pass"]}|'+ '/'.join(str(m[n]['full_pass']) for n in METHODS)+'|')
    (root/'REPORT.md').write_text('\n'.join(lines)+'\n')


def audit(root):
    plan=verify(root,full=True);frozen=json.loads((root/'fit_manifest.json').read_text())
    assert sha256(root/'fit_manifest.json')==(root/'fit_manifest.sha256').read_text().strip()
    results=json.loads((root/'comparison.json').read_text());assert len(results['rows'])==540
    for record in frozen['files']:assert sha256(root/record['file'])==record['sha256']
    assert all(r['same_cost_status']=='PASS' for r in results['rows'])
    assert 'Ran 4 tests' in (root/'unit_tests.log').read_text() and '\nOK' in (root/'unit_tests.log').read_text()
    tracked=hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest()
    assert tracked==plan['tracked_diff_sha256']
    owned=[REPO/'test'/n for n in SOURCES]+[root.parent/'PLAN.md',root.parent/'SUMMARY.md',root/'REPORT.md']
    diff=[]
    for p in owned:
        v=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(p)],capture_output=True,text=True)
        assert v.returncode in [0,1] and not v.stdout and not v.stderr,(p,v.stdout,v.stderr)
        v=subprocess.run(['git','diff','--no-index','--','/dev/null',str(p)],capture_output=True,text=True);assert v.returncode==1;diff.append(v.stdout)
    (root.parent/'task.diff').write_text('\n'.join(diff))
    write(root/'completion_audit.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        meaning='data/source/matching audit; model PASS/FAIL are separate',protected_files=len(plan['protected_sha256']),
        branch=plan['branch'],tracked_diff_unchanged=True,old_results_unchanged=True,
        source_sha256=plan['source_sha256'],plan_sha256=sha256(root/'plan.json'),fit_manifest_sha256=sha256(root/'fit_manifest.json'),
        matched_training_sets=540,unique_future_sequences=108,model_evaluations=2160,
        exact_original_candidate_validation=True,all_same_cost_fits_match=True,validation_permanently_excluded=True,
        full_model_passes={name:sum(r['scores'][name]['full_gate'] for r in results['rows']) for name in METHODS},
        new_simulation=0,new_K=0,no_hardware=True,no_runtime_change=True,
        owned_files=list(map(str,owned)),task_diff_sha256=sha256(root.parent/'task.diff'),summary_sha256=sha256(root.parent/'SUMMARY.md'),
        agent_check_log_sha256=sha256(root/'agent_check.log')))
    print('DESKTOP_DRY_RUN completion audit PASS',flush=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--stage',choices=['init','fit','score','audit'],required=True);parser.add_argument('--workers',type=int,default=3)
    args=parser.parse_args();root=args.root.resolve()
    if args.stage=='init':initialize(root);return
    plan=verify(root,full=True)
    if args.stage=='fit':
        assert not (root/'models').exists(),'Refusing fit overwrite'
        with ProcessPoolExecutor(max_workers=args.workers) as pool:files=list(pool.map(fit_one,[(str(root),j) for j in plan['jobs']]))
        write(root/'fit_manifest.json',dict(execution_domain='DESKTOP_DRY_RUN',files=files,fit_before_score=True))
        (root/'fit_manifest.sha256').write_text(sha256(root/'fit_manifest.json')+'\n')
    elif args.stage=='score':
        assert not (root/'scores').exists(),'Refusing score overwrite'
        assert sha256(root/'fit_manifest.json')==(root/'fit_manifest.sha256').read_text().strip()
        files=json.loads((root/'fit_manifest.json').read_text())['files']
        with ProcessPoolExecutor(max_workers=args.workers) as pool:groups=list(pool.map(score_one,[(str(root),r) for r in files]))
        summarize(root,[r for group in groups for r in group])
    else:audit(root)
    verify(root,full=True)


if __name__=='__main__':main()
