"""DESKTOP_DRY_RUN: same-data M4/M5 fit, freeze, and held-out comparison."""

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from analyze_flash_state_learning import state, rms, predict, metric
from analyze_flash_operating_local import evaluate_extended, summarize_all, pulse_diagnostics
from analyze_flash_odometry import integrate_path
from eval_flash_m5_yaw_rate import REPO, SOURCE, write, sha256


def fit_model(x, y, u, name):
    indices = list(range(25)) if name=='M5' else [0,1,2,3]+list(range(5,25))
    x, y = x[:,indices], y[:,indices]
    n = len(indices)
    target = y.copy()
    target[:,0] -= x[:,0]
    design = np.column_stack([x[:,1:],u])
    scale = rms(design,0)
    scale = np.where(scale>1e-14,scale,1.)
    coeff,_,rank,singular = np.linalg.lstsq(design/scale,target,rcond=1e-10)
    unscaled = (coeff/scale[:,None]).T
    A = np.zeros((n,n)); A[0,0] = 1.
    A[:,1:], B = unscaled[:,:-1].copy(), unscaled[:,-1].copy()
    actions = list(range(5,13)) if name=='M5' else list(range(4,12))
    coeff = np.linalg.lstsq(design[:,:-1]/scale[:-1],target[:,actions],rcond=1e-10)[0]
    A[np.ix_(actions,range(1,n))] = (coeff/scale[:-1,None]).T
    B[actions] = 0.
    innovation = u-x[:,1:]@np.linalg.lstsq(x[:,1:],u,rcond=None)[0]
    return dict(name=name,indices=indices,dimension=n,A=A.tolist(),B=B.tolist(),
        action_B_zero_rows=actions,rank=int(rank),rms_scaled_condition=float(singular[0]/singular[-1]),
        input_innovation_fraction=float(innovation@innovation/(u@u)),samples=len(u),
        spectral_radius=float(max(abs(np.linalg.eigvals(A)))),
        state_std=np.std(x,axis=0).tolist())


def load_records(root, split):
    records, direct = [], []
    for path in sorted(root.glob('*/results.json')):
        info = json.loads(path.read_text())
        if info['job']['split']!=split:
            continue
        assert info['evidence_status']=='PASS'
        direct.extend(info['direct_B'])
        old = SOURCE/info['job']['id']
        for row in info['responses']:
            with np.load(old/row['trace']) as trace, np.load(old/row['baseline']) as base:
                z = state(trace)-state(base)
                u = trace['actual_u']-base['actual_u']
                sensor_yaw = trace['rpy'][:,2].copy()
                base_yaw = base['rpy'][:,2].copy()
                gt = trace['gt']-base['gt']
            with np.load(path.parent/row['trace']) as extra, np.load(path.parent/row['baseline']) as bextra:
                delta_yaw_rate = extra['yaw_rate']-bextra['yaw_rate']
                z = np.concatenate([z[:,:4],delta_yaw_rate,z[:,4:]],axis=1)
                base_path = integrate_path(extra['base_position'],sensor_yaw)
                zero_path = integrate_path(bextra['base_position'],base_yaw)
                base_pv = np.column_stack([base_path-zero_path,
                    (extra['base_velocity']-bextra['base_velocity'])[:,0]])
            np.testing.assert_array_equal(z[0],np.zeros(25))
            records.append(dict(**row,context=info['job']['id'],z=z,u=u,gt=gt,base_pv=base_pv))
    return records,direct


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True,type=Path)
    parser.add_argument('--stage',choices=['all','fit','evaluate'],default='all')
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = json.loads((root/'manifest.json').read_text())
    if args.stage!='fit':
        assert json.loads((root/'completion.json').read_text())['evidence_status']=='PASS'
    train,direct_train = load_records(root,'train')
    assert len({r['context'] for r in train})==len([j for j in manifest['jobs'] if j['split']=='train'])
    x = np.concatenate([r['z'][:-1] for r in train])
    y = np.concatenate([r['z'][1:] for r in train])
    u = np.concatenate([r['u'] for r in train])
    frozen = root/'models_frozen.json'
    if args.stage!='evaluate':
        models = [fit_model(x,y,u,name) for name in ['M4','M5']]
        original = json.loads((SOURCE/'local_models_frozen.json').read_text())['models']
        old_m4 = next(m for m in original if m['name']=='M4')
        for k in ['A','B']:
            np.testing.assert_array_equal(models[0][k],old_m4[k])
        assert not frozen.exists(), 'Refusing to overwrite model comparison'
        write(frozen,dict(execution_domain='DESKTOP_DRY_RUN',models=models,
            train_responses=len(train),train_transitions=len(u),checkpoint_sha256=manifest['checkpoint_sha256'],
            onnx_sha256=manifest['onnx_sha256'],frozen_before_test_arrays=True,
            M4_exactly_reproduces_previous_fit=True,source_sha256=sha256(Path(__file__))))
    else:
        bundle = json.loads(frozen.read_text())
        assert bundle['source_sha256']==sha256(Path(__file__))
        models = bundle['models']
    if args.stage=='fit':
        print('[DESKTOP_DRY_RUN] M4/M5 frozen using train only; M4 exact original reproduction',flush=True)
        return
    model_hash = sha256(frozen)
    # Held-out data is opened only after BOTH candidates have been fixed.
    test,direct_test = load_records(root,'test')
    train_contexts = sorted({r['context'] for r in train})
    test_contexts = sorted({r['context'] for r in test})
    assert not set(train_contexts)&set(test_contexts)
    train_seeds = {j['seed'] for j in manifest['jobs'] if j['split']=='train'}
    test_seeds = {j['seed'] for j in manifest['jobs'] if j['split']=='test'}
    assert not train_seeds&test_seeds
    data = np.asarray([r['z'] for r in test]); inputs = np.asarray([r['u'] for r in test])
    direct = np.median([r['B'] for r in direct_test],axis=0)
    summaries,details,predictions,pulses = {},{},{},{}
    for model in models:
        name = model['name']
        stats,prediction = evaluate_extended(model,data,inputs)
        summary = summarize_all(stats)
        b_error = abs(model['B'][1]-direct[1])/abs(direct[1])
        gate = bool(b_error<=.3 and model['B'][1]*direct[1]>0 and
            np.all(np.asarray(summary['full2s']['nrmse'])<=.3) and all(
            np.all(np.asarray(summary['horizons'][str(h)]['nrmse'])<=.3) for h in [5,25,50,100]))
        summary.update(primary_gate=gate,Bv_relative_error=float(b_error),direct_Bv=float(direct[1]),
            rank=model['rank'],condition=model['rms_scaled_condition'],contexts={})
        for context in test_contexts:
            ix = [i for i,r in enumerate(test) if r['context']==context]
            summary['contexts'][context] = dict(rolling2_v_rmse=float(np.median(stats['horizons']['100']['rmse'][ix,1])),
                rolling2_v_nrmse=float(np.median(stats['horizons']['100']['nrmse'][ix,1])))
        summary['physical_response_crosscheck'] = {}
        for label,actual in [('base_link',np.asarray([r['base_pv'] for r in test])),
                             ('wheel_midpoint',np.asarray([r['gt'][:,:2] for r in test]))]:
            check = metric(prediction[:,1:101,:2],actual[:,1:101])
            summary['physical_response_crosscheck'][label] = {
                k:np.median(v,axis=0).tolist() for k,v in check.items()}
        summary['full8s_both_under30_count'] = int(np.all(stats['full8s']['nrmse']<=.3,axis=1).sum())
        summary['full8s_max_nrmse'] = stats['full8s']['nrmse'].max(axis=0).tolist()
        summaries[name] = summary
        details[name] = {key:({h:{k:v.tolist() for k,v in row.items()} for h,row in values.items()}
            if key=='horizons' else {k:v.tolist() for k,v in values.items()}) for key,values in stats.items()}
        # Existing pulse analysis expects z=p/v/...; canonical M5 shares its first two rows.
        pulses[name] = pulse_diagnostics(test,prediction)
        predictions[name] = prediction
        print('[DESKTOP_DRY_RUN]',name,'first2',summary['full2s']['nrmse'],
            'rolling2',summary['horizons']['100']['nrmse'],'full8',summary['full8s']['nrmse'],flush=True)
    m4,m5 = summaries['M4'],summaries['M5']
    nr_ratio = m5['horizons']['100']['nrmse'][1]/m4['horizons']['100']['nrmse'][1]
    rm_ratio = m5['horizons']['100']['rmse'][1]/m4['horizons']['100']['rmse'][1]
    context_wins = sum(m5['contexts'][c]['rolling2_v_rmse']<m4['contexts'][c]['rolling2_v_rmse'] for c in test_contexts)
    no_degradation = bool(np.all(np.asarray(m5['full8s']['nrmse'])<=1.05*np.asarray(m4['full8s']['nrmse'])))
    improvement = bool(m5['primary_gate'] and nr_ratio<=.9 and rm_ratio<=.9 and context_wins>=5 and no_degradation)
    write(root/'summary.json',dict(execution_domain='DESKTOP_DRY_RUN',
        evidence_status='PASS' if m5['primary_gate'] else 'FAIL',models=summaries,
        improvement_gate=improvement,rolling2_v_nrmse_ratio=float(nr_ratio),rolling2_v_rmse_ratio=float(rm_ratio),
        context_wins=context_wins,contexts=len(test_contexts),full8_no_degradation=no_degradation,
        conditional_LQR='PROCEED' if improvement else 'NOT_TESTED: predeclared improvement gate not met',
        primary_physical_point='base_link origin',secondary='wheel midpoint',
        estimator='unchanged ideal wheel rolling p/v; no GT/control correction',
        train_responses=len(train),test_responses=len(test),train_transitions=len(u),
        direct_train_pairs=len(direct_train),direct_test_pairs=len(direct_test),
        train_contexts=train_contexts,test_contexts=test_contexts,model_sha256=model_hash))
    write(root/'prediction_metrics.json',dict(execution_domain='DESKTOP_DRY_RUN',models=details))
    write(root/'pulse_diagnostics.json',dict(execution_domain='DESKTOP_DRY_RUN',models=pulses))
    write(root/'direct_B.json',dict(execution_domain='DESKTOP_DRY_RUN',median=direct.tolist(),rows=direct_test))
    fig,axes = plt.subplots(1,2,figsize=(10,4))
    for name,summary in summaries.items():
        for k,ax in enumerate(axes):
            ax.plot([.1,.5,1.,2.,4.],[100*summary['horizons'][str(h)]['nrmse'][k]
                for h in [5,25,50,100,200]],'o-',label=name)
            ax.axhline(30,color='gray',linestyle=':',linewidth=.8)
            ax.set(xlabel='rolling horizon [s]',ylabel=['p NRMSE [%]','v NRMSE [%]'][k])
            ax.grid(alpha=.3)
    axes[0].legend();fig.tight_layout();fig.savefig(root/'horizons.png',dpi=150);plt.close(fig)
    for family in ['pulse_pos','bipulse_pos']:
        ix = next(i for i,r in enumerate(test) if r['family']==family and r['amplitude']==.05)
        t = np.arange(401)*.02
        fig,axes = plt.subplots(3,1,figsize=(10,8),sharex=True)
        for k in range(2):
            axes[k].plot(t,data[ix,:,k]*1000,'k',label='MuJoCo sensor response')
            for name,p in predictions.items():axes[k].plot(t,p[ix,:,k]*1000,label=name)
            axes[k].set_ylabel(['position [mm]','velocity [mm/s]'][k]);axes[k].grid(alpha=.3)
        axes[0].legend(); axes[2].step(t[:-1],inputs[ix],where='post')
        axes[2].set(xlabel='time [s]',ylabel='probe [Nm]');axes[2].grid(alpha=.3)
        fig.tight_layout();fig.savefig(root/f'{family}.png',dpi=150);plt.close(fig)
    assert sha256(frozen)==model_hash
    assert all(sha256(REPO/p)==h for p,h in manifest['protected_sha256'].items())
    write(root/'analysis_integrity.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        frozen_preserved=True,protected_preserved=True,disjoint_initial_seeds=True,
        M4_original_fit_exact=True,all_hidden_states_predicted=True,M6=False,
        source_sha256=sha256(Path(__file__))))


if __name__=='__main__':
    main()
