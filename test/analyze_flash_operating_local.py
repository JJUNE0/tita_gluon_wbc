"""DESKTOP_DRY_RUN: fit only M2/M4 on train, freeze before independent tests.

Primary gates are unchanged0.1..2s response prediction and direct B. Longer
4/8s predictions, pulse sign reversal and velocity decay are separate metrics.
"""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from analyze_flash_state_learning import load, fit, predict, metric, evaluate, FLOOR, rms
from eval_flash_operating_local import REPO, BIAS, write, sha256


def evaluate_extended(model,data,inputs):
    stats=evaluate(model,data,inputs)
    A,B=np.asarray(model['A']),np.asarray(model['B'])
    z=data[:,:,model['indices']]
    prediction=predict(A,B,z[:,0],inputs)
    for name,end in [('full4s',200),('full8s',400)]:
        stats[name]=metric(prediction[:,1:end+1],z[:,1:end+1])
    stats['tail4_8s']=metric(prediction[:,201:401],z[:,201:401])
    starts=np.arange(0,inputs.shape[1]-200+1,10)
    value=z[:,starts].copy()
    for k in range(200):
        value=value@A.T+inputs[:,starts+k,None]*B
    stats['horizons']['200']=metric(value,z[:,starts+200])
    return stats,prediction


def summarize_all(stats):
    return {key:({h:{m:np.median(v,axis=0).tolist() for m,v in row.items()}
        for h,row in values.items()} if key=='horizons' else
        {m:np.median(v,axis=0).tolist() for m,v in values.items()}) for key,values in stats.items()}


def crossing_time(velocity,inputs,threshold=1e-6):
    first=int(np.flatnonzero(abs(inputs)>1e-7)[0])
    sign=np.sign(velocity[first+1])
    candidates=np.flatnonzero(velocity[first+2:]*sign < -threshold)
    return None if not len(candidates) else float((candidates[0]+1)*.02)


def pulse_diagnostics(records,prediction):
    rows=[]
    for i,r in enumerate(records):
        if r['family'] not in ['pulse_pos','pulse_neg']:
            continue
        actual=r['z'][:,1]
        predicted=prediction[i,:,1]
        first=int(np.flatnonzero(abs(r['u'])>1e-7)[0])
        actual_cross=crossing_time(actual,r['u'])
        predicted_cross=crossing_time(predicted,r['u'])
        rows.append(dict(context=r['context'],family=r['family'],amplitude=r['amplitude'],start_rl_s=r['start_rl_s'],
            first_velocity_sign_match=bool(np.sign(actual[first+1])==np.sign(predicted[first+1])),
            actual_reversal_s=actual_cross,predicted_reversal_s=predicted_cross,
            reversal_time_error_s=None if actual_cross is None or predicted_cross is None else abs(actual_cross-predicted_cross),
            actual_peak_velocity=float(max(abs(actual))),predicted_peak_velocity=float(max(abs(predicted))),
            actual_tail_velocity_rms=float(rms(actual[201:401],0)),predicted_tail_velocity_rms=float(rms(predicted[201:401],0)),
            tail_velocity_rmse=float(rms(predicted[201:401]-actual[201:401],0)),
            actual_final_position=float(r['z'][-1,0]),predicted_final_position=float(prediction[i,-1,0])))
    errors=[r['reversal_time_error_s'] for r in rows if r['reversal_time_error_s'] is not None]
    return dict(rows=rows,summary=dict(pulse_count=len(rows),
        first_velocity_sign_matches=sum(r['first_velocity_sign_match'] for r in rows),
        actual_reversal_count=sum(r['actual_reversal_s'] is not None for r in rows),
        predicted_reversal_count=sum(r['predicted_reversal_s'] is not None for r in rows),
        median_reversal_time_error_s=float(np.median(errors)) if errors else None,
        median_actual_tail_velocity_rms=float(np.median([r['actual_tail_velocity_rms'] for r in rows])),
        median_predicted_tail_velocity_rms=float(np.median([r['predicted_tail_velocity_rms'] for r in rows])),
        median_tail_velocity_rmse=float(np.median([r['tail_velocity_rmse'] for r in rows]))))


def operating_facts(root):
    rows=[]
    fig,axes=plt.subplots(2,1,figsize=(10,6),sharex=True)
    for path in sorted(root.glob('*/results.json')):
        info=json.loads(path.read_text())
        for acquisition in info['acquisitions']:
            if not acquisition['metrics']['operating_gate']:
                continue
            tick=round(acquisition['start_hold_s']/.02)
            with np.load(path.parent/f'zero_t{tick}.npz') as base:
                yaw=np.unwrap(base['rpy'][:,2])
                row=dict(context=info['job']['id'],split=info['job']['split'],
                    seed=info['job']['seed'],pitch=info['job']['pitch'],approach=info['job']['approach'],
                    start_hold_s=acquisition['start_hold_s'],start_rl_s=acquisition['start_rl_s'],
                    preceding_gate=acquisition['metrics'],
                    baseline_gt_v_mean=float(base['gt'][:,1].mean()),
                    baseline_gt_v_rms=float(rms(base['gt'][:,1],0)),
                    baseline_yaw_change=float(yaw[-1]-yaw[0]),
                    baseline_planar_radius=float(max(np.linalg.norm(base['position'][:,:2]-base['position'][0,:2],axis=1))),
                    baseline_residual_error=float(max(abs(base['actual_u']-BIAS))))
                rows.append(row)
                if info['job']['split']=='test':
                    t=np.arange(len(yaw))*.02
                    axes[0].plot(t,base['gt'][:,1]*1000,alpha=.5)
                    axes[1].plot(t,yaw-yaw[0],alpha=.5)
    axes[0].set(ylabel='baseline velocity [mm/s]',title='Independent test snapshots: constant0.4828Nm, F-1 off')
    axes[1].set(ylabel='yaw change [rad]',xlabel='time after branch [s]')
    for ax in axes:ax.grid(alpha=.3)
    fig.tight_layout();fig.savefig(root/'acquisition_baselines.png',dpi=150);plt.close(fig)
    write(root/'operating_facts.json',dict(execution_domain='VALIDATION_SIM',rows=rows,
        note='Finite-time near-zero sagittal velocity with sustained yaw rotation; not static full-pose equilibrium.'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args()
    root=args.root.resolve()
    manifest=json.loads((root/'manifest.json').read_text())
    train,train_contexts,train_direct=load(root,'train')
    assert train
    x=np.concatenate([r['z'][:-1] for r in train])
    y=np.concatenate([r['z'][1:] for r in train])
    u=np.concatenate([r['u'] for r in train])
    models=[fit(x,y,u,name) for name in ['M2','M4']]
    model_path=root/'local_models_frozen.json'
    if model_path.exists():
        raise RuntimeError('Refusing to overwrite frozen local models')
    write(model_path,dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='NOT_TESTED',models=models,
        checkpoint_sha256=manifest['checkpoint_sha256'],bias=BIAS,train_contexts=train_contexts,
        train_responses=len(train),train_transitions=len(u),train_direct_B_median=np.median([r['sensor_B'] for r in train_direct],0).tolist(),
        script_sha256=sha256(Path(__file__)),frozen_before_test_arrays=True,
        constraints='unchanged translation symmetry and8causal action B zero rows; no affine/Q/R/LQR'))
    frozen_hash=sha256(model_path)
    test,test_contexts,direct=load(root,'test')
    assert test and not set(train_contexts)&set(test_contexts)
    train_seeds={json.loads((root/c/'results.json').read_text())['job']['seed'] for c in train_contexts}
    test_seeds={json.loads((root/c/'results.json').read_text())['job']['seed'] for c in test_contexts}
    assert not train_seeds&test_seeds
    data=np.asarray([r['z'] for r in test]);inputs=np.asarray([r['u'] for r in test])
    reference=np.median([r['sensor_B'] for r in direct],0)
    direct_array=np.asarray([r['sensor_B'] for r in direct])
    write(root/'direct_B_summary.json',dict(execution_domain='DESKTOP_DRY_RUN',
        test_pairs=len(direct),sensor_median=reference.tolist(),
        sensor_min=direct_array.min(0).tolist(),sensor_max=direct_array.max(0).tolist(),
        gt_median=np.median([r['gt_B'] for r in direct],0).tolist()))
    summaries,all_details,pulses={}, {}, {}
    predictions={}
    for model in models:
        name=model['name']
        stats,prediction=evaluate_extended(model,data,inputs)
        summary=summarize_all(stats)
        relative=abs(np.asarray(model['B'])[:2]-reference[:2])/abs(reference[:2])
        primary=all(np.all(np.asarray(summary['horizons'][str(h)]['nrmse'])<=.3) for h in [5,25,50,100])
        primary=primary and np.all(np.asarray(summary['full2s']['nrmse'])<=.3)
        primary=bool(primary and relative[1]<=.3 and model['B'][1]*reference[1]>0)
        gt_data=data.copy();gt_data[:,:,:4]=np.asarray([r['gt'] for r in test])
        gt_stats,_=evaluate_extended(model,gt_data,inputs)
        families={}
        for family in sorted({r['family'] for r in test}):
            indices=[i for i,r in enumerate(test) if r['family']==family]
            families[family]={key:{m:np.median(values[indices],axis=0).tolist() for m,values in stats[key].items()}
                for key in ['full2s','full4s','full8s','tail4_8s']}
        context_metrics={}
        for context in test_contexts:
            indices=[i for i,r in enumerate(test) if r['context']==context]
            context_metrics[context]={key:{m:np.median(values[indices],axis=0).tolist() for m,values in stats[key].items()}
                for key in ['full2s','full4s','full8s']}
        initial_direction_matches=0
        for i,row in enumerate(test):
            first=int(np.flatnonzero(abs(row['u'])>1e-7)[0])
            initial_direction_matches+=int(np.sign(prediction[i,first+1,1])==np.sign(row['z'][first+1,1]))
        summary.update(primary_gate=primary,B_pv=model['B'][:2],B_reference_pv=reference[:2].tolist(),
            B_relative_error_pv=relative.tolist(),rank=model['rank'],condition=model['rms_scaled_condition'],
            spectral_radius=model['spectral_radius'],input_innovation_fraction=model['input_innovation_energy_fraction'],
            supplemental4s_gate=bool(np.all(np.asarray(summary['full4s']['nrmse'])<=.3) and
                np.all(np.asarray(summary['horizons']['200']['nrmse'])<=.3)),
            supplemental8s_gate=bool(np.all(np.asarray(summary['full8s']['nrmse'])<=.3)),
            GT_full2s={m:np.median(v,axis=0).tolist() for m,v in gt_stats['full2s'].items()},
            floor_trace_counts={key:np.sum(stats[key]['signal_rms']<FLOOR,axis=0).tolist()
                for key in ['full2s','full4s','full8s','tail4_8s']},family_metrics=families,
            context_metrics=context_metrics,initial_direction_matches=initial_direction_matches,
            full2s_both_pv_below30_count=int(np.sum(np.all(stats['full2s']['nrmse']<=.3,axis=1))),
            full2s_max_nrmse=np.max(stats['full2s']['nrmse'],axis=0).tolist())
        summaries[name]=summary
        pulses[name]=pulse_diagnostics(test,prediction)
        predictions[name]=prediction
        all_details[name]={key:({h:{m:v.tolist() for m,v in val.items()} for h,val in values.items()}
            if key=='horizons' else {m:v.tolist() for m,v in values.items()}) for key,values in stats.items()}
        print('[DESKTOP_DRY_RUN]',name,'full2s',summary['full2s']['nrmse'],'rolling2s',summary['horizons']['100']['nrmse'],
            'full4s',summary['full4s']['nrmse'],'full8s',summary['full8s']['nrmse'],'primary',primary,flush=True)
    decision='M2' if summaries['M2']['primary_gate'] else ('M4' if summaries['M4']['primary_gate'] else 'NEITHER')
    write(root/'summary.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS' if decision!='NEITHER' else 'FAIL',
        decision=decision,models=summaries,train_responses=len(train),test_responses=len(test),
        train_contexts=train_contexts,test_contexts=test_contexts,train_seeds=sorted(train_seeds),test_seeds=sorted(test_seeds),
        direct_pairs_train=len(train_direct),direct_pairs_test=len(direct),models_sha256=frozen_hash,
        no_LQR=True,primary='predeclared0.1..2s+B gate;4/8s supplemental, not controller validation'))
    write(root/'prediction_metrics.json',dict(execution_domain='DESKTOP_DRY_RUN',results=all_details,
        traces=[{k:r[k] for k in ['context','family','amplitude','start_rl_s']} for r in test]))
    write(root/'pulse_diagnostics.json',dict(execution_domain='DESKTOP_DRY_RUN',models=pulses))
    for family in ['pulse_pos','bipulse_pos']:
        index=next(i for i,r in enumerate(test) if r['family']==family and r['amplitude']==.05)
        row=test[index];t=np.arange(401)*.02
        fig,axes=plt.subplots(3,1,figsize=(11,8),sharex=True)
        for k in range(2):
            axes[k].plot(t,row['z'][:,k]*1000,'k',label='MuJoCo matched response')
            for name,output in predictions.items():axes[k].plot(t,output[index,:,k]*1000,label=name+' local')
            axes[k].set_ylabel(['position [mm]','velocity [mm/s]'][k]);axes[k].grid(alpha=.3)
        axes[0].legend(fontsize=8);axes[2].step(t[:-1],row['u'],where='post')
        axes[2].set(xlabel='time after branch [s]',ylabel='additional probe [Nm]');axes[2].grid(alpha=.3)
        fig.tight_layout();fig.savefig(root/f'{family}_local.png',dpi=150);plt.close(fig)
    assert sha256(model_path)==frozen_hash
    assert all(sha256(REPO/p)==h for p,h in manifest['protected_sha256'].items())
    operating_facts(root)
    write(root/'analysis_integrity.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        models_unchanged_after_test=True,protected_files_preserved=True,disjoint_initial_seed_sets=True,
        all_hidden_states_predicted_recursively=True,no_test_arrays_before_frozen_models=True,
        analysis_sha256=sha256(Path(__file__))))


if __name__=='__main__':
    main()
