"""DESKTOP_DRY_RUN: report A objectives and actual single-rollout local gates."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from online_local_m4 import verify,write,sha256,B_SETTINGS,REPO


def analyze(root):
    plan=verify(root,full=True);A=json.loads((root/'A_results.json').read_text())['rows'];numerics=json.loads((root/'A_numerics.json').read_text())['rows']
    datasets={s:json.loads((root/(s+'_results.json')).read_text())['rows']for s in ['development','test']}
    admission=json.loads((root/'B_admission.json').read_text());rows=[];audit=[]
    for split,episodes in datasets.items():
        for episode in episodes:
            job=episode['job'];folder=root/split/job['id']
            with np.load(folder/'trajectory.npz')as t:
                N=len(t['actual_u']);np.testing.assert_array_equal(t['previous_action'][:-1],t['history']);np.testing.assert_array_equal(t['previous_action'][1:],t['action'])
                np.testing.assert_array_equal(t['physical_motor'][:,:,[0,1,2,4,5,6]],t['flash'][:,:,[0,1,2,4,5,6]])
                assert float(t['p_hold'])==float(t['sensor'][0,0])
                assert np.max(abs(t['physical_motor'][:,:,[3,7]]))<=12.000001
                if N>13:assert t['actual_u'][13:].min()>=.4328-1e-6 and t['actual_u'].max()<=.5328+1e-6
                for begin in [500,1500,3000]:assert not t['training_used'][begin:min(begin+200,N)].any()
                audit.append(dict(split=split,id=job['id'],steps=N,probe_allowed_fraction=episode['probe_allowed_fraction'],
                    saturation=episode['saturation_fraction'],used=episode['training_transitions'],probe_energy=episode['probe_energy']))
            for event in episode['events']:
                file=folder/event['candidate_file'];assert sha256(file)==event['candidate_sha256'];frozen=json.loads(file.read_text())
                for name,verdict in event['verdicts'].items():
                    candidate=frozen['candidates'][name]
                    if candidate['status']=='FROZEN':
                        times=candidate['training_times'];assert max(times)<=event['created']+1e-9
                        assert all(not any(begin+1e-8<t<=begin+4.+1e-8 for begin in [10.,30.,60.])for t in times)
                    rows.append(dict(split=split,domain=job['domain'],amplitude=job['amplitude'],seed=job['seed'],pitch=job['pitch'],time=event['created'],method=name,**verdict))
    summary=[]
    for split in ['development','test']:
        for domain in ['nominal','friction0.2']:
            for amplitude in [.01,.02]:
                episodes=[r for r in datasets[split]if r['job']['domain']==domain and r['job']['amplitude']==amplitude]
                for setting in B_SETTINGS:
                    selected=[r for r in rows if r['split']==split and r['domain']==domain and r['amplitude']==amplitude and r['method']==setting['name']]
                    summary.append(dict(split=split,domain=domain,amplitude=amplitude,method=setting['name'],passed_candidates=sum(r['gate']for r in selected),candidates=len(selected),
                        passed_episodes=sum(any(e['verdicts'][setting['name']]['gate']for e in r['events'])for r in episodes),episodes=len(episodes),
                        prediction_pass=sum(r.get('prediction',{}).get('prediction_gate',False)for r in selected),
                        information_pass=sum(r.get('information',{}).get('gate',False)for r in selected)))
    write(root/'B_summary.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=summary,candidates=rows,episodes=audit))
    fig,ax=plt.subplots(figsize=(11,4.5));labels=[];values=[]
    for row in summary:
        if row['split']=='test':labels.append(f'{row["domain"]}/{row["amplitude"]}\n{row["method"]}');values.append(row['passed_candidates'])
    ax.bar(np.arange(len(values)),values);ax.set_xticks(np.arange(len(values)),labels,rotation=75,fontsize=7);ax.set_ylabel('Verified frozen candidates (of18)');ax.grid(axis='y',alpha=.3)
    fig.tight_layout();fig.savefig(root/'online_candidate_passes.png',dpi=160);plt.close(fig)
    lines=['# Online Local M4 — A/B numerical tables','',
        'Execution Domain: **DESKTOP_DRY_RUN** (B collection: **VALIDATION_SIM**)','',
        f'Policy Checkpoint SHA256: `{plan["checkpoint_sha256"]}`','',
        'Evidence Status: Numerical and physical model gates are reported separately. No success inferred from workflow completion.','',
        'Observed Metrics / Behavior / Log Summary: A uses existing branches; B uses one causal physical time line per episode.','',
        '| A cohort | Setting | Predicting contexts PASS/total |','|---|---|---|']
    for r in A:lines.append(f'|{r["cohort"]}|{r["setting"]}|{r["passed"]}/{r["total"]}|')
    lines+=['','| B split/domain/amplitude | Method | Candidate PASS | Episode with PASS | Prediction PASS | Information PASS |',
        '|---|---|---|---|---|---|']
    for r in summary:lines.append(f'|{r["split"]}/{r["domain"]}/{r["amplitude"]}|{r["method"]}|{r["passed_candidates"]}/{r["candidates"]}|{r["passed_episodes"]}/{r["episodes"]}|{r["prediction_pass"]}|{r["information_pass"]}|')
    lines+=['','![Online candidates](online_candidate_passes.png)','',
        'C admission: '+json.dumps(admission['domains'],ensure_ascii=False),'',
        'Numerical same-objective SVD refinement is predefined. Raw recursive models/discrepancies remain in each candidate file.',
        'Full4s subsequent validation is never training data for any candidate or later fit. Conditional B is not offline Direct B.',
        'No elapsed time/domain labels, GT or snapshots are inputs to the regression features; time only indexes window membership and predeclared validation.']
    (root/'REPORT.md').write_text('\n'.join(lines)+'\n')
    write(root/'analysis_integrity.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',episodes=sum(len(v)for v in datasets.values()),candidate_verdicts=len(rows),
        fixed_goal_history_leg_budget=True,frozen_candidate_hashes=True,validation_permanently_excluded=True,old_protected_files=len(plan['protected_sha256']),
        numerical_A2_A3=[r for r in numerics if r['setting']=='A3_recursive'],no_new_K_claim_without_C=True))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();analyze(a.root.resolve())
