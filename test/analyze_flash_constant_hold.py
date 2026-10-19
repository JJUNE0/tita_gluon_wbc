"""DESKTOP_DRY_RUN: select sustainable measured bias; test frozen M2/M4 only."""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from eval_flash_constant_hold import MODEL_PATHS, GATES
from eval_flash_pv_models import REPO, write, sha256
from analyze_flash_state_learning import state
from analyze_flash_stop_release import assess


def select(root):
    paths=sorted(root.glob('*/results.json'))
    rows=[json.loads(p.read_text()) for p in paths]
    by_tau={}
    for row in rows:
        by_tau.setdefault(row['job']['tau'],[]).append(row['metrics'])
    values=[]
    for tau,group in sorted(by_tau.items()):
        complete=all(r['completed'] for r in group)
        values.append(dict(tau=tau,all_pass=all(r['operating_gate'] for r in group),
            completed=complete,mean_v=float(np.mean([r['gt_v_mean_last60'] for r in group])),
            max_absolute_mean_v=float(max(abs(r['gt_v_mean_last60']) for r in group)),
            mean_v_rms=float(np.mean([r['gt_v_rms_last60'] for r in group])),
            path_span_max=float(max(r['gt_path_span_after60'] for r in group)),
            planar_radius_max=float(max(r['planar_radius_after60'] for r in group))))
    qualified=[v for v in values if v['all_pass']]
    pool=qualified or [v for v in values if v['completed']]
    if not pool:
        raise RuntimeError('No completed condition; no torque selected')
    best=min(pool,key=lambda v:v['max_absolute_mean_v'])
    path=root/'selection.json'
    if path.exists():
        raise RuntimeError('Refusing to overwrite selection')
    manifest=json.loads((root/'manifest.json').read_text())
    write(path,dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS' if qualified else 'FAIL',
        selected_tau=best['tau'],qualified=bool(qualified),conditions=values,
        stage=manifest['stage'],gates=GATES,analysis_sha256=sha256(Path(__file__)),
        rule='minimum worst absolute final60s mean speed among gate-passing torques; otherwise diagnostic fallback',
        note='Empirical finite-horizon operating point, not an exact equilibrium or identified feedforward law'))
    fig,axes=plt.subplots(2,1,figsize=(9,6),sharex=True)
    axes[0].plot([r['tau'] for r in values],[r['mean_v']*1000 for r in values],'o-')
    axes[0].axhspan(-.2,.2,color='green',alpha=.15);axes[0].axhline(0.,color='k',lw=.7)
    axes[0].set_ylabel('mean GT velocity last60s [mm/s]')
    axes[1].plot([r['tau'] for r in values],[r['path_span_max']*1000 for r in values],'o-',label='sagittal span after60s')
    axes[1].plot([r['tau'] for r in values],[r['planar_radius_max']*1000 for r in values],'s-',label='planar radius after60s')
    axes[1].axhline(20,color='k',lw=.7,ls=':')
    axes[1].set(xlabel='constant total residual [Nm]',ylabel='position excursion [mm]');axes[1].legend(fontsize=8)
    for ax in axes:ax.grid(alpha=.3)
    fig.tight_layout();fig.savefig(root/'torque_response.png',dpi=150);plt.close(fig)
    print('[DESKTOP_DRY_RUN]',manifest['stage'],'selected',best,'qualified',bool(qualified),flush=True)


def validate(root):
    manifest=json.loads((root/'manifest.json').read_text())
    terminal_mode=manifest.get('secondary') is not None
    assert terminal_mode or manifest['stage']=='confirm'
    models=[]
    for label,path in MODEL_PATHS.items():
        source=json.loads(path.read_text())['models']
        if label=='moving':
            source=[m for m in source if m['name'] in ['M2','M4'] and m['context_count']==24]
        elif label=='bias_local':
            source=[m for m in source if m['mode']=='frozen' and m['kind']=='delta']
        assert len(source)==2
        models += [dict(m,origin=label) for m in source]
    model_path=root/'models_used.json'
    if model_path.exists():
        raise RuntimeError('Refusing to overwrite frozen model evidence')
    write(model_path,dict(execution_domain='DESKTOP_DRY_RUN',models=models,no_refit=True,
        source_hashes={k:sha256(p) for k,p in MODEL_PATHS.items()},analysis_sha256=sha256(Path(__file__))))
    model_hash=sha256(model_path)
    holds,records,direct=[],[],[]
    for path in sorted(root.glob('*/results.json')):
        info=json.loads(path.read_text())
        holds.append(dict(id=info['job']['id'],job=info['job'],
            metrics=info['terminal_metrics'] if terminal_mode else info['metrics'],
            original_after60_metrics=info['metrics']))
        direct.extend(info['direct_B'])
        for row in info['responses']:
            with np.load(path.parent/row['trace']) as z,np.load(path.parent/row['baseline']) as base:
                delta=state(z)-state(base)
                np.testing.assert_array_equal(delta[0],np.zeros(24))
                assert np.max(abs(base['requested_u']-info['job']['tau']))<1e-12
                records.append(dict(**row,context=info['job']['id'],z=delta,
                    u=z['actual_u']-base['actual_u'],gt=z['gt']-base['gt']))
    predictions=[]
    if records:
        for model in models:
            result=assess(model,records,direct)
            result['origin']=model['origin']
            predictions.append(result)
            print('[DESKTOP_DRY_RUN] model',model['origin'],model['name'],result['full2s']['nrmse'],
                'rolling2s',result['horizons']['100']['nrmse'],'gate',result['diagnostic_gate'],flush=True)
    all_pass=all(r['metrics']['operating_gate'] for r in holds)
    write(root/'summary.json',dict(execution_domain='DESKTOP_DRY_RUN',
        evidence_status='PASS' if all_pass else 'FAIL',
        selected_tau=manifest['jobs'][0]['tau'] if terminal_mode else manifest['selection']['selected_tau'],
        assessment_window='660..900s' if terminal_mode else '60s..end',
        all_confirmation_hold_pass=all_pass,hold_count=len(holds),holds=holds,model_results=predictions,
        probe_responses=len(records),direct_pairs=len(direct),probe_contexts=len(set(r['context'] for r in records)),
        gates=GATES,no_LQR=True,no_refit=True,
        interpretation='Finite-horizon bounded-position evidence; model results have separate gates, not blanket controller approval'))
    fig,axes=plt.subplots(3,1,figsize=(11,8),sharex=True)
    for row in holds:
        with np.load(root/row['id']/'hold.npz') as z:
            t=np.arange(len(z['gt']))*.02
            label=row['id'] if row['job']['pitch']==0. else None
            axes[0].plot(t,z['gt'][:,1]*1000,label=label,alpha=.65)
            start=round(60/.02)
            axes[1].plot(t[start:],(z['gt'][start:,0]-z['gt'][start,0])*1000,alpha=.65)
            axes[2].plot(t,z['sensor'][:,2],alpha=.65)
    axes[0].axhspan(-.2,.2,color='green',alpha=.15);axes[0].set_ylabel('GT velocity [mm/s]');axes[0].legend(fontsize=6,ncol=2)
    axes[1].set_ylabel('sagittal position from60s [mm]')
    axes[2].set(xlabel='constant-bias evaluation time [s]',ylabel='IMU pitch [rad]')
    for ax in axes:ax.grid(alpha=.3)
    fig.tight_layout();fig.savefig(root/'confirmation.png',dpi=150);plt.close(fig)
    if terminal_mode:
        fig,axes=plt.subplots(4,1,figsize=(10,9),sharex=True)
        for row in holds:
            with np.load(root/row['id']/'hold.npz') as z:
                start=33000
                t=np.arange(len(z['gt']))[start:]*.02
                axes[0].plot(t,z['gt'][start:,1]*1000,alpha=.7)
                axes[1].plot(t,(z['gt'][start:,0]-z['gt'][start,0])*1000,alpha=.7)
                axes[2].plot(t,z['sensor'][start:,2],alpha=.7)
                yaw=np.unwrap(z['rpy'][start:,2])
                axes[3].plot(t,yaw-yaw[0],alpha=.7)
        for ax,label in zip(axes,['GT velocity [mm/s]','sagittal position from660s [mm]',
                'IMU pitch [rad]','yaw change from660s [rad]']):
            ax.set_ylabel(label);ax.grid(alpha=.3)
        axes[-1].set_xlabel('constant-bias evaluation time [s]')
        fig.tight_layout();fig.savefig(root/'confirmation_terminal.png',dpi=150);plt.close(fig)
    assert sha256(model_path)==model_hash
    protected=manifest.get('protected_sha256')
    if protected is None:
        protected=json.loads((root.parent/'scan/manifest.json').read_text())['protected_sha256']
    assert all(sha256(REPO/p)==h for p,h in protected.items())
    write(root/'analysis_integrity.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        frozen_model_hash=model_hash,protected_files_preserved=True,no_models_fitted=True,
        constant_bias_in_both_probe_branches=True,all_selected_states_predicted_recursively=True,
        analysis_sha256=sha256(Path(__file__))))
    print('[DESKTOP_DRY_RUN] confirmation',sum(r['metrics']['operating_gate'] for r in holds),'/',len(holds),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--stage',choices=['select','validate'],required=True)
    args=parser.parse_args()
    if args.stage=='select':select(args.root.resolve())
    else:validate(args.root.resolve())


if __name__=='__main__':
    main()
