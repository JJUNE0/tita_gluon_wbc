"""DESKTOP_DRY_RUN: report primary base metrics, incomplete runs and shadow gates."""
import argparse
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from m4_mismatch_stages import GROUPS, EFFECTS
from flash_overnight_model_stages import write


def analyze(root):
    rows=json.loads((root/'mismatch/metrics.json').read_text())['rows']
    summaries=[]
    for regime in ['settled','entry']:
        for name,_ in EFFECTS:
            for group in GROUPS:
                selected=[r for r in rows if r['regime']==regime and r['condition']==name and r['group']==group]
                complete=[r for r in selected if r['complete']]
                value=dict(regime=regime,condition=name,group=group,complete=len(complete),total=len(selected),
                    failure_reasons=[r['failure'] for r in selected if not r['complete']],
                    failure_times_s=[r['duration_s'] for r in selected if not r['complete']])
                for label,key,factor in [('max_planar_drift_m','max_planar_drift',1.),
                    ('base_tail_speed_RMS_mm_s','last5_base_speed_RMS',1000.),
                    ('pitch_RMS_rad','pitch_RMS',1.),('wheel_RMS_Nm','wheel_torque_RMS',1.),
                    ('train_support_fraction','hidden_train_fraction',1.)]:
                    value[label]=float(np.median([r[key]*factor for r in complete])) if complete else None
                value['base_IAE_m_s']=float(np.median([r['base']['IAE'] for r in complete])) if complete else None
                value['axle_IAE_m_s']=float(np.median([r['wheel_midpoint']['IAE'] for r in complete])) if complete else None
                summaries.append(value)
    write(root/'comparison_summary.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=summaries,
        metrics_only_full_60s_completions=True,base_origin_primary=True,wheel_midpoint_secondary=True))
    with (root/'comparison_metrics.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(summaries[0]));writer.writeheader();writer.writerows(summaries)
    fig,axes=plt.subplots(2,1,figsize=(13,8),sharex=True)
    x=np.arange(len(EFFECTS));width=.18
    for ax,regime in zip(axes,['settled','entry']):
        for i,group in enumerate(GROUPS):
            items=[next(r for r in summaries if r['regime']==regime and r['condition']==name and r['group']==group) for name,_ in EFFECTS]
            values=[r['max_planar_drift_m'] if r['complete']==r['total'] else np.nan for r in items]
            ax.bar(x+(i-1.5)*width,values,width,label=group)
            for pos,r in zip(x+(i-1.5)*width,items):
                if r['complete']!=r['total']:ax.text(pos,.001,f"{r['complete']}/{r['total']}",rotation=90,fontsize=7)
        ax.set(ylabel='maximum planar drift [m]',title=regime+' / full 60s runs only; missing bar = incomplete group')
        ax.set_yscale('symlog',linthresh=.01);ax.grid(axis='y',alpha=.3)
    axes[0].legend(ncol=4);axes[1].set_xticks(x,[k for k,_ in EFFECTS],rotation=25)
    fig.tight_layout();fig.savefig(root/'mismatch_comparison.png',dpi=150);plt.close(fig)
    return summaries


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args();root=args.root.resolve()
    if (root/'mismatch/metrics.json').exists():analyze(root)
    details(root)
    if (root/'cold_adaptive/adaptive/all_results.json').exists():details(root/'cold_adaptive')


def details(root):
    if (root/'shadow_reference.json').exists():
        shadow=Path(json.loads((root/'shadow_reference.json').read_text())['root'])/'shadow'
    else:shadow=root/'shadow'
    records=[json.loads(p.read_text()) for p in sorted(shadow.glob('*/results.json'))]
    handoffs=[]
    if records:
        source=Path(json.loads((shadow/'manifest.json').read_text())['mismatch_source'])
        for record in records:
            pair=record['pair']
            with np.load(source/'mismatch'/pair['train']['id']/'M4.npz') as before, np.load(shadow/pair['id']/'training.npz') as trace:
                jump=float(abs(trace['requested_u'][0]-before['requested_u'][-1]))
                handoffs.append(dict(id=pair['id'],condition=pair['condition'],
                    first_command_jump=jump,continuous_2Nm_s_handoff=jump<=.040000001,
                    internal_step_change_peak=float(max(abs(np.diff(trace['requested_u'])))),
                    zero_effect_validation_inputs=sum(r['probe_peak']<1e-6 for r in record['validation_responses'])))
        write(root/'shadow_handoff_diagnostics.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=handoffs,
            status='SUSPICIOUS' if any(not r['continuous_2Nm_s_handoff'] for r in handoffs) else 'PASS',
            note='Controller epoch resets its correction to zero; boundary and internal slew are evaluated separately.'))
    summaries=[]
    for condition in sorted({r['pair']['condition'] for r in records}):
        rows=[r for r in records if r['pair']['condition']==condition]
        value=dict(condition=condition,pairs=len(rows),
            information_pass=sum(r['information']['gate'] for r in rows),
            nominal_prediction_pass=sum(r['models']['nominal']['gate'] for r in rows),
            full_prediction_pass=sum(r['models']['full']['gate'] for r in rows),
            partial_prediction_pass=sum(r['models']['partial']['gate'] for r in rows),
            condition_max=max(r['information']['scaled_condition'] for r in rows),
            input_innovation_min=min(r['information']['input_innovation_fraction'] for r in rows))
        for name in ['nominal','full','partial']:
            value[name]={
                'full2_pv_NRMSE':np.median([r['models'][name]['prediction']['full2s']['nrmse'] for r in rows],axis=0).tolist(),
                'rolling2_pv_NRMSE':np.median([r['models'][name]['prediction']['horizons']['100']['nrmse'] for r in rows],axis=0).tolist(),
                'rolling2_pv_RMSE':np.median([r['models'][name]['prediction']['horizons']['100']['rmse'] for r in rows],axis=0).tolist(),
                'B_relative_error_median':float(np.median([r['models'][name]['B_relative_error'] for r in rows]))}
        models=[json.loads((shadow/r['pair']['id']/'models_frozen.json').read_text())['full'] for r in rows]
        value['actual_full_A_rho']=[float(max(abs(np.linalg.eigvals(m['A'])))) for m in models]
        summaries.append(value)
    write(root/'shadow_comparison.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=summaries,
        note='Current spectra are recomputed here. Legacy nominal fit diagnostic fields copied into model dictionaries '
            '(e.g. spectral_radius/rank) are not current RLS statistics; use information and actual_full_A_rho.'))
    adaptive=root/'adaptive/all_results.json'
    if not adaptive.exists():return
    trials=json.loads(adaptive.read_text())['rows'];summaries=[]
    conditions=sorted({r['condition'] for r in trials})
    fig,axes=plt.subplots(len(conditions),2,figsize=(11,3*len(conditions)),squeeze=False)
    for index,condition in enumerate(conditions):
        selected=[r for r in trials if r['condition']==condition]
        for group in ['A','bias_only','F1','M4','Adaptive_M4']:
            rows=[next(x for x in r['rows'] if x['group']==group) for r in selected]
            complete=[r for r in rows if r['complete']]
            summaries.append(dict(condition=condition,group=group,complete=len(complete),total=len(rows),
                base_IAE_median=float(np.median([r['base']['IAE'] for r in complete])) if complete else None,
                max_planar_median=float(np.median([r['max_planar_drift'] for r in complete])) if complete else None,
                tail_base_speed_RMS_median=float(np.median([r['last5_base_speed_RMS'] for r in complete])) if complete else None,
                pitch_RMS_median=float(np.median([r['pitch_RMS'] for r in complete])) if complete else None,
                wheel_RMS_median=float(np.median([r['wheel_torque_RMS'] for r in complete])) if complete else None))
        representative=sorted(selected,key=lambda r:r['id'])[0]
        for group in ['M4','Adaptive_M4']:
            with np.load(root/'adaptive'/representative['id']/(group+'.npz')) as z:
                axes[index,0].plot(np.arange(len(z['base_path']))*.02,z['base_path']*1000,label=group)
                axes[index,1].plot(np.arange(len(z['actual_u']))*.02,z['actual_u'],label=group)
        axes[index,0].set(title=condition,ylabel='base sagittal position [mm]')
        axes[index,1].set(title=condition,ylabel='total residual [Nm]')
        for ax in axes[index]:ax.grid(alpha=.3);ax.set_xlabel('time [s]');ax.legend()
    fig.tight_layout();fig.savefig(root/'adaptive_comparison.png',dpi=150);plt.close(fig)
    write(root/'adaptive_comparison.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=summaries,
        main_trials_only=True,common_identification_prefix_before_each_comparison=True))


if __name__=='__main__':main()
