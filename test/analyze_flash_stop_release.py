"""DESKTOP_DRY_RUN: old M2/M4 first; conditional train-only same-state refit."""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from analyze_flash_state_learning import load, fit, evaluate, summarize, predict
from eval_flash_stop_release import OLD_MODELS, REPO, sha256, write


def assess(model, records, direct):
    data = np.asarray([r['z'] for r in records])
    inputs = np.asarray([r['u'] for r in records])
    summary = summarize(evaluate(model, data, inputs))
    b = np.median([r['sensor_B'][:2] for r in direct], 0)
    relative = abs(np.asarray(model['B'])[:2]-b)/abs(b)
    signs, first_errors = [], []
    A, B = np.asarray(model['A']), np.asarray(model['B'])
    for row in records:
        index = int(np.flatnonzero(abs(row['u'])>1e-7)[0])
        initial = row['z'][None, 0, model['indices']]
        response = predict(A, B, initial, row['u'][None, :index+1])[0, -1, 1]
        actual = row['z'][index+1, 1]
        signs.append(bool(np.sign(response)==np.sign(actual)))
        first_errors.append(abs(response-actual)/max(abs(actual),1e-12))
    passed = all(np.all(np.asarray(summary['horizons'][str(h)]['nrmse'])<=.3) for h in [5,25,50,100])
    passed = passed and np.all(np.asarray(summary['full2s']['nrmse'])<=.3)
    passed = passed and relative[1]<=.3 and np.sign(model['B'][1])==np.sign(b[1])
    gt_data=data.copy()
    gt_data[:,:,:4]=np.asarray([r['gt'] for r in records])
    gt_summary=summarize(evaluate(model,gt_data,inputs))
    families={}
    for family in sorted(set(r['family'] for r in records)):
        indices=[i for i,r in enumerate(records) if r['family']==family]
        families[family]=summarize(evaluate(model,data[indices],inputs[indices]))['full2s']
    summary.update(name=model['name'], direct_B_reference=b.tolist(),B_pv=model['B'][:2],
        B_relative_error=relative.tolist(), diagnostic_gate=bool(passed),
        initial_velocity_direction_matches=sum(signs), initial_velocity_direction_total=len(signs),
        initial_velocity_magnitude_relative_error_median=float(np.median(first_errors)),
        GT_crosscheck_full2s=gt_summary['full2s'],family_full2s=families,
        scaled_condition=model.get('rms_scaled_condition'),spectral_radius=model.get('spectral_radius'))
    return summary


def old_validation(root):
    manifest=json.loads((root/'manifest.json').read_text())
    assert sha256(OLD_MODELS)==manifest['old_models_sha256']
    source=json.loads(OLD_MODELS.read_text())['models']
    models=[m for m in source if m['name'] in ['M2','M4'] and m['context_count']==24]
    assert len(models)==2
    path=root/'old_models_used.json'
    if path.exists():
        raise RuntimeError('Refusing to overwrite old-model evidence')
    write(path,dict(execution_domain='DESKTOP_DRY_RUN',source_sha256=sha256(OLD_MODELS),models=models))
    test,contexts,direct=load(root,'test')
    results=[assess(m,test,direct) for m in models]
    for result in results:
        print('[DESKTOP_DRY_RUN] old',result['name'],result['full2s']['nrmse'],result['diagnostic_gate'],flush=True)
    write(root/'old_validation.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS' if all(r['diagnostic_gate'] for r in results) else 'FAIL',
        results=results,test_contexts=contexts,responses=len(test),source_sha256=sha256(OLD_MODELS),
        new_models_fitted=False,analysis_sha256=sha256(Path(__file__))))


def conditional_refit(root):
    old=json.loads((root/'old_validation.json').read_text())
    old_hash=sha256(root/'old_validation.json')
    models=json.loads((root/'old_models_used.json').read_text())['models']
    need_refit=not all(r['diagnostic_gate'] for r in old['results'])
    fitted=[]
    train_contexts=[]
    if need_refit:
        train,train_contexts,_=load(root,'train')
        x=np.concatenate([r['z'][:-1] for r in train])
        y=np.concatenate([r['z'][1:] for r in train])
        u=np.concatenate([r['u'] for r in train])
        fitted=[fit(x,y,u,name) for name in ['M2','M4']]
    path=root/'conditional_models_frozen.json'
    if path.exists():
        raise RuntimeError('Refusing to overwrite conditional fit')
    write(path,dict(execution_domain='DESKTOP_DRY_RUN',models=fitted,refit_performed=need_refit,
        trigger='pre-registered old-model gate failure' if need_refit else 'old models passed; no refit',
        old_validation_sha256=old_hash,train_contexts=train_contexts,analysis_sha256=sha256(Path(__file__)),
        coefficients_use_train_only=True,test_previously_used_only_for_old_model_validation=True,
        no_model_structure_or_hyperparameter_search=True))
    frozen_hash=sha256(path)
    test,test_contexts,direct=load(root,'test')
    assert not set(train_contexts)&set(test_contexts)
    results=[assess(m,test,direct) for m in fitted]
    decisions={}
    for prior in old['results']:
        new=next((r for r in results if r['name']==prior['name']),None)
        decisions[prior['name']]='KEEP_OLD' if prior['diagnostic_gate'] else ('USE_RELEASE_LOCAL' if new and new['diagnostic_gate'] else 'MODEL_NOT_VALIDATED')
    write(root/'decision.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS' if all(v!='MODEL_NOT_VALIDATED' for v in decisions.values()) else 'FAIL',
        decisions=decisions,refit_performed=need_refit,refit_results=results,
        old_validation_sha256=old_hash,frozen_models_sha256=frozen_hash,no_LQR=True,
        scope='near-stop initial states, both acquisition controllers fully released; no equilibrium search'))
    for result in results:
        print('[DESKTOP_DRY_RUN] release-local',result['name'],result['full2s']['nrmse'],result['diagnostic_gate'],flush=True)
    for family in ['pulse_pos','bipulse_pos']:
        row=next(r for r in test if r['family']==family and r['amplitude']==.25)
        t=np.arange(201)*.02
        fig,axes=plt.subplots(3,1,figsize=(10,8),sharex=True)
        for k in range(2):
            axes[k].plot(t,row['z'][:,k]*1000,'k',label='MuJoCo matched response')
            for group,candidates in [('old',models),('release-local',fitted)]:
                for m in candidates:
                    initial=row['z'][None,0,m['indices']]
                    output=predict(np.asarray(m['A']),np.asarray(m['B']),initial,row['u'][None])[0]
                    axes[k].plot(t,output[:,k]*1000,'--' if group=='old' else '-',label=f"{m['name']} {group}")
            axes[k].set_ylabel(['position [mm]','velocity [mm/s]'][k]);axes[k].grid(alpha=.3)
        axes[2].step(t[:-1],row['u'],where='post');axes[2].set(xlabel='time after release [s]',ylabel='probe [Nm]');axes[2].grid(alpha=.3)
        axes[0].legend(fontsize=8);fig.tight_layout();fig.savefig(root/f'{family}_prediction.png',dpi=150);plt.close(fig)
    assert sha256(path)==frozen_hash and sha256(root/'old_validation.json')==old_hash
    manifest=json.loads((root/'manifest.json').read_text())
    assert all(sha256(REPO/p)==h for p,h in manifest['protected_sha256'].items())
    baselines=[]
    for result in sorted(root.glob('test*/results.json')):
        info=json.loads(result.read_text())
        for name in sorted(set(r['baseline'] for r in info['responses'])):
            with np.load(result.parent/name) as z:
                baselines.append(dict(context=info['job']['id'],baseline=name,
                    sensor_initial_v=float(z['sensor'][0,1]),GT_initial_v=float(z['gt'][0,1]),
                    sensor_v_range=[float(z['sensor'][:,1].min()),float(z['sensor'][:,1].max())],
                    GT_v_mean_last1s=float(z['gt'][-50:,1].mean()),GT_path_change_4s=float(z['gt'][-1,0]-z['gt'][0,0]),
                    residual_peak=float(max(abs(z['actual_u'])))))
    write(root/'integrity.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        protected_files_preserved=True,collector_sha256=sha256(REPO/'test/eval_flash_stop_release.py'),
        analysis_sha256=sha256(Path(__file__)),old_validation_unchanged_after_refit=True,
        conditional_models_unchanged_after_evaluation=True,baselines=baselines,
        no_F1_or_acquisition_bias_during_probing=True,all_hidden_states_predicted_recursively=True))
    print('[DESKTOP_DRY_RUN] decision',decisions,flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--stage',choices=['old','conditional'],required=True)
    args=parser.parse_args()
    if args.stage=='old':
        old_validation(args.root.resolve())
    else:
        conditional_refit(args.root.resolve())


if __name__=='__main__':
    main()
