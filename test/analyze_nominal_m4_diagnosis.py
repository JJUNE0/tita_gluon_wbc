"""DESKTOP_DRY_RUN: fixed Nominal method/region/composition contrasts."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from nominal_m4_diagnosis import (verify,write,sha256,read_new,score,TIMES,PROFILES,ABC,BIAS,
    load_absolute,LOCAL,AFFINE,fit_method,choose)
from analyze_flash_state_learning import evaluate as delta_evaluate
from analyze_flash_operating_local import summarize_all


def analyze(root):
    plan=verify(root,full=True);frozen=root/'models_frozen.json';h=sha256(frozen)
    assert h==(root/'models_frozen.sha256').read_text().strip()
    bundle=json.loads(frozen.read_text());models=bundle['models'];results=[]
    test={time:read_new(root,'test',time)for time in TIMES}
    for key,entry in models.items():
        times=TIMES if entry['profile']=='full'and entry['method']in ['paired_c','joint']else[entry['train_time']]
        if entry['profile']=='stream':times=TIMES
        for time in times:
            records,direct=test[time];value=score(entry['model'],records,direct)
            if records:
                # Pure response diagnostic separates AB dynamics from affine baseline.
                states=np.asarray([r['delta']for r in records]);u=np.asarray([r['u']-r['base_u']for r in records])
                dm=dict(entry['model'],indices=list(range(24)))
                dstats=delta_evaluate(dm,states,u);value['paired_delta']=summarize_all(dstats)
            results.append(dict(key=key,train_time=entry['train_time'],test_time=time,profile=entry['profile'],method=entry['method'],**value))
        print('DESKTOP_DRY_RUN scored',key,flush=True)
    legacy=json.loads((root/'legacy_models.json').read_text())
    for name,model in legacy.items():
        if name=='paired':continue
        model=dict(model,indices=list(range(24)),input_reference=model.get('input_reference',BIAS))
        for time,(records,direct)in test.items():
            results.append(dict(key='prior_'+name,train_time='old',test_time=time,profile='prior',method=name,**score(model,records,direct)))
    write(root/'comparison.json',dict(execution_domain='DESKTOP_DRY_RUN',models_sha256=h,rows=results,test_data_never_refitted=True))
    # Compare raw internal-state operating ranges, not just position translation.
    regions=[]
    for split in ['train','test']:
        for time in TIMES:
            records,_=read_new(root,split,time)
            baseline={r['context']:r['base']for r in records}
            if not baseline:continue
            x=np.concatenate(list(baseline.values()))
            regions.append(dict(split=split,time=time,contexts=len(baseline),mean=x.mean(0).tolist(),std=x.std(0).tolist(),
                min=x.min(0).tolist(),max=x.max(0).tolist(),state_order='p,v,pitch,rate,raw_action8,leg_q6,leg_dq6'))
    write(root/'operating_regions.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=regions))
    primary=[r for r in results if r['profile']in PROFILES and r['method']in ['paired_c','joint']and r['train_time']==r['test_time']]
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for ax,method in zip(axes,['paired_c','joint']):
        for profile in PROFILES:
            rows=sorted([r for r in primary if r['profile']==profile and r['method']==method and 'metrics'in r],key=lambda r:r['test_time'])
            ax.plot([r['test_time']for r in rows],[100*r['metrics']['horizons']['100']['nrmse'][1]for r in rows],'o-',label=profile)
        ax.set(xscale='log',yscale='log',xlabel='snapshot time after first RL [s]',ylabel='absolute rolling2s velocity NRMSE [%]',title=method)
        ax.axhline(30.,color='gray',linestyle=':');ax.grid(alpha=.3);ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(root/'method_region_composition.png',dpi=160);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for ax,method in zip(axes,['paired_c','joint']):
        table=np.full((4,4),np.nan)
        for r in results:
            if r['profile']=='full'and r['method']==method and 'metrics'in r:table[TIMES.index(r['train_time']),TIMES.index(r['test_time'])]=100*r['metrics']['horizons']['100']['nrmse'][1]
        shown=np.log10(np.maximum(table,1e-4));ax.imshow(shown,cmap='viridis',aspect='auto')
        for i in range(4):
            for j in range(4):ax.text(j,i,f'{table[i,j]:.2g}%',ha='center',va='center',color='white')
        ax.set(xticks=range(4),yticks=range(4),xticklabels=TIMES,yticklabels=TIMES,xlabel='test snapshot [s]',ylabel='training snapshot [s]',title=method+' rolling2s v')
    fig.tight_layout();fig.savefig(root/'cross_region.png',dpi=160);plt.close(fig)
    lines=['# Nominal M4 — fixed method/region/data diagnostics','',
        'Execution Domain: **DESKTOP_DRY_RUN**; collection: **VALIDATION_SIM**','',
        f'Policy Checkpoint SHA256: `{plan["checkpoint_sha256"]}`','',
        'Evidence Status: Per-row PASS/FAIL/NOT_TESTED below. No new controller or RLS tuning.','',
        'Observed Metrics / Behavior / Log Summary: Matched held-out starts; all24 states recursively predicted. Related branches are not independent starts.','',
        '| Train/test time s | Profile | Method | First2 p/v % | Rolling2 p/v % | Baseline | Contexts | Overall |',
        '|---|---|---|---|---|---|---|---|']
    for r in primary:
        if 'metrics'not in r:lines.append(f'|{r["test_time"]}|{r["profile"]}|{r["method"]}|N/A|N/A|N/A|N/A|NOT_TESTED|');continue
        a=np.asarray(r['metrics']['full2s']['nrmse'])*100;b=np.asarray(r['metrics']['horizons']['100']['nrmse'])*100
        lines.append(f'|{r["test_time"]}|{r["profile"]}|{r["method"]}|{a[0]:.4g}/{a[1]:.4g}|{b[0]:.4g}/{b[1]:.4g}|{sum(x["gate"]for x in r["baselines"])}/{len(r["baselines"])}|{r["passed_contexts"]}/{r["total_contexts"]}|{r["status"]}|')
    lines+=['','![Matched comparisons](method_region_composition.png)','','![Cross-region](cross_region.png)','',
        'All frozen auxiliary numeric-cutoff and stream models, context distributions and baseline RMSE are in [comparison.json](comparison.json).',
        'Constant-bias continuous-stream fits cannot identify B; they are diagnostics and never count as successful input identification.',
        'Training profiles: small2; quantity6 same2families repeated; waveforms6; initials6 across3starts; full78; full_replicates102 responses per time.',
        'Absolute joint fits also use each matched baseline once. Paired fits use the same raw pairs, then baseline one-step defects for c. These objectives differ; transition counts are logged.',
        'Calibration baseline anchors are an offline coordinate translation, not a physical/controller goal reset.',
        'No post-outcome threshold or source changes, controller, K, odometry replacement, hardware or policy retraining.']
    (root/'REPORT.md').write_text('\n'.join(lines)+'\n')
    assert sha256(frozen)==h;verify(root,full=True)
    write(root/'analysis_integrity.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',models_unchanged=True,
        model_count=len(models),comparisons=len(results),primary_comparisons=len(primary),protected_files=len(plan['protected_sha256']),no_test_refit=True))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();analyze(a.root.resolve())
