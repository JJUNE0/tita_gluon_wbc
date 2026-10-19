"""VALIDATION_SIM: conditional fixed residual LQR at the verified local point.

Design, simulation and analysis are explicit stages. Fresh affine PASS is
required before gain design. No production code or online gain is changed.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
import json
from pathlib import Path
import pickle

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import solve_discrete_are

from eval_flash_operating_local import StateRunner, STATE_KEYS, REPO, CKPT, BIAS, write, sha256
from eval_flash_pv_models import prepared_config
from sim2sim_ros2_jazzy.residual_wheel_pd import ResidualWheelPD

GROUPS = ['bias_only','F1_runtime_only','bias_PD_local_kv24','fixed_LQR']
CASES = [('zero',0.)]+[('position',v) for v in [-.001,-.0005,.0005,.001]]+[
    ('kick',v) for v in [-.02,-.01,.01,.02]]


def lqr_gain(A,B,scales,Q,R):
    scales = np.maximum(np.asarray(scales),1e-8)
    As = A*scales[None,:]/scales[:,None]
    Bs = B[:,None]/scales[:,None]
    Qs = Q*scales[:,None]*scales[None,:]
    P = solve_discrete_are(As,Bs,Qs,np.array([[R]]))
    Ks = np.linalg.solve(np.array([[R]])+Bs.T@P@Bs,Bs.T@P@As)
    residual = As.T@P@As-P-As.T@P@Bs@Ks+Qs
    K = Ks[0]/scales
    rho = float(max(abs(np.linalg.eigvals(A-np.outer(B,K)))))
    error = float(np.linalg.norm(residual)/max(np.linalg.norm(P),1e-20))
    assert np.isfinite(K).all() and rho<1.-1e-8 and error<1e-6,(rho,error)
    return K,dict(closed_model_spectral_radius=rho,relative_DARE_residual=error)


def design(root):
    confirmation = root/'calibrated/fresh_confirmation.json'
    decision = json.loads(confirmation.read_text())
    assert decision['gate'], 'Fresh affine confirmation must PASS before LQR design'
    source = root/'calibrated/affine_model_frozen.json'
    assert sha256(source)==decision['model_sha256']
    bundle = json.loads(source.read_text())
    m = bundle['model']
    plan = json.loads((root/'control_plan.json').read_text())
    Q = np.zeros((24,24))
    Q[0,0],Q[1,1] = plan['Q_physical']['p'],plan['Q_physical']['v']
    K,diagnostics = lqr_gain(np.asarray(m['A']),np.asarray(m['B']),m['state_std'],Q,plan['R'])
    path = root/'fixed_gain_frozen.json'
    assert not path.exists()
    write(path,dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='NOT_TESTED',K=K.tolist(),
        Q=Q.tolist(),R=plan['R'],model_sha256=sha256(source),confirmation_sha256=sha256(confirmation),
        plan_sha256=sha256(root/'control_plan.json'),reference=m['operating_reference'],
        reference_defect=m['operating_reference_defect'],diagnostics=diagnostics,
        correction_limit_Nm=.05,ramp_s=1.5,slew_Nm_s=2.,bias=BIAS,
        checkpoint_sha256=bundle['checkpoint_sha256'],onnx_sha256=bundle['onnx_sha256'],
        script_sha256=sha256(Path(__file__)),feedback='all24 states; cost only p/v; no equilibrium solve or offset extrapolation'))
    print('[DESKTOP_DRY_RUN] fixed gain designed once',diagnostics,'K_pv',K[:2].tolist(),flush=True)


def current_state(r):
    return np.concatenate([r.observation[k] for k in ['sensor','previous_action','leg_position','leg_velocity']])


def limited(raw,previous,t):
    phase = min(t/1.5,1.)
    ramp = phase**2*(3.-2.*phase)
    return float(np.clip(ramp*np.clip(raw,-.05,.05),previous-.04,previous+.04))


def control_job(cfg,job,fresh_root,output,gain):
    out = Path(output)/job['id']
    out.mkdir()
    original = Path(fresh_root)/job['id']
    r = StateRunner(cfg,job)
    K,reference = np.asarray(gain['K']),np.asarray(gain['reference'])
    model = json.loads((Path(output).parent/'calibrated/affine_model_frozen.json').read_text())['model']
    low,high = np.asarray(model['train_min']),np.asarray(model['train_max'])
    results = []
    try:
        for moment in job['times']:
            tick = round(moment/.02)
            with gzip.open(original/f'snapshot_t{tick}.pkl.gz','rb') as f:snapshot=pickle.load(f)
            r.restore(snapshot)
            replay,fail = r.rollout(np.full(400,BIAS))
            assert not fail
            with np.load(original/f'zero_t{tick}.npz') as expected:
                for key in replay:np.testing.assert_array_equal(replay[key],expected[key])
            for family,amplitude in CASES:
                r.restore(snapshot)
                p_target = float(r.observation['sensor'][0])
                gt_target = float(r.observation['gt'][0])
                if family=='position':
                    p_target -= amplitude
                    gt_target -= amplitude
                elif family=='kick':
                    r.step(BIAS+amplitude)
                    assert not r.failures()
                disturbed = r.snapshot()
                first_state = current_state(r)
                for group in GROUPS:
                    r.restore(disturbed)
                    np.testing.assert_array_equal(current_state(r),first_state)
                    pd = None
                    if group=='F1_runtime_only':
                        pd = ResidualWheelPD(r.env)
                        pd.update(np.zeros(3))
                        pd.position = float(r.observation['sensor'][0]-p_target)
                        pd.age = pd.u = 0.
                    states,steps,raw_rows,corrections,support = [],[],[],[],[]
                    previous = 0.
                    failure = []
                    for i in range(1001):
                        states.append({k:r.observation[k].copy() for k in STATE_KEYS})
                        failure = r.failures()
                        if failure or i==1000:break
                        z = current_state(r)
                        z[0] -= p_target
                        if group=='fixed_LQR':
                            raw = float(-K@(z-reference))
                            extra = limited(raw,previous,i*.02)
                        elif group=='bias_PD_local_kv24':
                            raw = float(-2.*z[0]-24.*z[1])
                            extra = limited(raw,previous,i*.02)
                        elif group=='F1_runtime_only':
                            pd.update(np.zeros(3))
                            raw = float(pd.u)
                            extra = raw
                        else:
                            raw = extra = 0.
                        previous = extra
                        tau = extra if group=='F1_runtime_only' else BIAS+extra
                        raw_rows.append(raw);corrections.append(extra)
                        # Translation has no influence on the policy plant. Diagnose
                        # non-position support without changing the fixed controller.
                        physical = z.copy()
                        support.append(bool(np.all(physical[1:]>=low[1:]-1e-8) and np.all(physical[1:]<=high[1:]+1e-8)))
                        transition = r.step(tau)
                        assert abs(transition['actual_u']-tau)<1e-6
                        if group in ['fixed_LQR','bias_PD_local_kv24']:
                            assert abs(extra)<=.050000001
                        steps.append(transition)
                    trace = {k:np.asarray([s[k] for s in states]) for k in STATE_KEYS}
                    if steps:
                        trace.update({k:np.asarray([s[k] for s in steps]) for k in steps[0]})
                        np.testing.assert_array_equal(trace['previous_action'][:-1],trace['history'])
                        np.testing.assert_array_equal(trace['previous_action'][1:],trace['action'])
                    trace.update(raw_correction=np.asarray(raw_rows),correction=np.asarray(corrections),
                                 hidden_inside_training_range=np.asarray(support))
                    if group in ['fixed_LQR','bias_PD_local_kv24']:
                        assert max(abs(np.diff(np.r_[0.,trace['correction']])))<=.040000001
                    name = f'{group}_{family}_{amplitude:+g}_t{tick}.npz'
                    np.savez_compressed(out/name,**trace)
                    results.append(dict(group=group,family=family,amplitude=amplitude,trace=name,
                        start_hold_s=moment,p_target=p_target,gt_target=gt_target,
                        complete=not failure and len(states)==1001,failure=failure,
                        initial_state=first_state.tolist()))
        write(out/'results.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',job=job,
            runs=results,exact_serialized_snapshot_replay=True,online_update=False))
        result = dict(id=job['id'],runs=len(results),complete=sum(r['complete'] for r in results))
        print('[VALIDATION_SIM]',result,flush=True)
        return result
    finally:
        r.env.close()


def analyze(root):
    gain = json.loads((root/'fixed_gain_frozen.json').read_text())
    ref_pitch = gain['reference'][2]
    rows = []
    for path in sorted((root/'control').glob('*/results.json')):
        info = json.loads(path.read_text())
        for run in info['runs']:
            with np.load(path.parent/run['trace']) as trace:
                t = np.arange(len(trace['sensor']))*.02
                error = trace['gt'][:,0]-run['gt_target']
                sensor_error = trace['sensor'][:,0]-run['p_target']
                tail = t>=15.
                row = dict(**run,context=info['job']['id'],duration_s=float(t[-1]),
                    gt_IAE=float(np.trapz(abs(error),t)),max_gt_error=float(max(abs(error))),
                    sensor_IAE=float(np.trapz(abs(sensor_error),t)),
                    final5_p_rmse=float(np.sqrt(np.mean(error[tail]**2))) if np.any(tail) else None,
                    final5_sensor_p_rmse=float(np.sqrt(np.mean(sensor_error[tail]**2))) if np.any(tail) else None,
                    final5_v_mean=float(trace['gt'][tail,1].mean()) if np.any(tail) else None,
                    final5_sensor_v_mean=float(trace['sensor'][tail,1].mean()) if np.any(tail) else None,
                    final5_velocity_estimation_bias=float(np.mean(trace['sensor'][tail,1]-trace['gt'][tail,1])) if np.any(tail) else None,
                    encoder_GT_path_difference=float((trace['sensor'][-1,0]-trace['sensor'][0,0])-(trace['gt'][-1,0]-trace['gt'][0,0])),
                    pitch_rmse=float(np.sqrt(np.mean((trace['sensor'][:,2]-ref_pitch)**2))),
                    wheel_torque_rms=float(np.sqrt(np.mean(trace['motor'][:,:,[3,7]]**2))),
                    correction_peak=float(max(abs(trace['correction']))),
                    raw_exceeds_local05_fraction=float(np.mean(abs(trace['raw_correction'])>.05)),
                    hidden_support_fraction=float(trace['hidden_inside_training_range'].mean()))
                rows.append(row)
    summaries = {}
    for group in GROUPS:
        selected = [r for r in rows if r['group']==group]
        done = [r for r in selected if r['complete']]
        summaries[group] = dict(complete=len(done),total=len(selected),families={})
        for family in ['zero','position','kick']:
            values = [r for r in done if r['family']==family]
            summaries[group]['families'][family] = {k:float(np.median([r[k] for r in values])) if values else None
                for k in ['gt_IAE','sensor_IAE','final5_p_rmse','final5_sensor_p_rmse','max_gt_error',
                          'pitch_rmse','wheel_torque_rms','correction_peak','hidden_support_fraction',
                          'final5_velocity_estimation_bias','encoder_GT_path_difference']}
    def key(r):return (r['context'],r['start_hold_s'],r['family'],r['amplitude'])
    baseline = {key(r):r for r in rows if r['group']=='bias_only'}
    lqr = [r for r in rows if r['group']=='fixed_LQR']
    checks = {'complete':all(r['complete'] for r in lqr), 'families':{}}
    for family in ['position','kick']:
        selected = [r for r in lqr if r['family']==family]
        refs = [baseline[key(r)] for r in selected]
        valid = all(r['complete'] and b['complete'] for r,b in zip(selected,refs))
        iae_ratio = float(np.median([r['gt_IAE'] for r in selected])/np.median([r['gt_IAE'] for r in refs]))
        final_ratio = float(np.median([r['final5_p_rmse'] for r in selected])/np.median([r['final5_p_rmse'] for r in refs])) if valid else None
        paired = float(np.mean([r['gt_IAE']<b['gt_IAE'] for r,b in zip(selected,refs)]))
        checks['families'][family] = dict(IAE_ratio=iae_ratio,final5_ratio=final_ratio,paired_improvement_fraction=paired,
            pass_gate=bool(valid and iae_ratio<=.8 and final_ratio<=.5 and paired>=.8))
    checks['pitch'] = all(r['pitch_rmse']<=max(1.25*baseline[key(r)]['pitch_rmse'],.002) for r in lqr)
    checks['wheel_torque'] = all(r['wheel_torque_rms']<=1.25*baseline[key(r)]['wheel_torque_rms'] for r in lqr)
    checks['zero'] = all(r['complete'] and r['final5_p_rmse']<=max(baseline[key(r)]['final5_p_rmse']+.00005,.0001)
                         and abs(r['final5_v_mean'])<=.00002 for r in lqr if r['family']=='zero')
    passed = checks['complete'] and checks['pitch'] and checks['wheel_torque'] and checks['zero'] and all(x['pass_gate'] for x in checks['families'].values())
    write(root/'control_metrics.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=rows))
    write(root/'control_summary.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS' if passed else 'FAIL',
        success_gate=passed,gates=checks,groups=summaries,gain_sha256=sha256(root/'fixed_gain_frozen.json'),
        analysis_source_sha256=sha256(Path(__file__)),
        note='Finite local recovery only; runtime F1 removes bias and uses original2Nm bounds; local PD preserves bias and matched0.05Nm bounds.'))
    for family,amp in [('position',.001),('kick',.02)]:
        chosen = next(r for r in rows if r['family']==family and r['amplitude']==amp)
        selected = [r for r in rows if key(r)==key(chosen) and r['group']!='F1_runtime_only']
        fig,axes = plt.subplots(3,1,figsize=(11,8),sharex=True)
        for row in selected:
            with np.load(root/'control'/row['context']/row['trace']) as trace:
                t = np.arange(len(trace['sensor']))*.02
                axes[0].plot(t,(trace['gt'][:,0]-row['gt_target'])*1000,label=row['group'])
                axes[1].plot(t,trace['gt'][:,1]*1000)
                axes[2].plot(t[:-1],trace['correction'])
        axes[0].legend();axes[0].set_ylabel('GT position error [mm]')
        axes[1].set_ylabel('GT velocity [mm/s]');axes[2].set(ylabel='correction [Nm]',xlabel='time after control start [s]')
        for ax in axes:ax.grid(alpha=.3)
        fig.tight_layout();fig.savefig(root/f'control_{family}.png',dpi=150);plt.close(fig)
    print('[VALIDATION_SIM] fixed LQR success gate',passed,checks,flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage',choices=['design','run','analyze'],required=True)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--workers',type=int,default=3)
    args = p.parse_args()
    root = args.root.resolve()
    if args.stage=='design':design(root);return
    if args.stage=='analyze':analyze(root);return
    gain_path = root/'fixed_gain_frozen.json'
    gain = json.loads(gain_path.read_text())
    assert sha256(root/'calibrated/fresh_confirmation.json')==gain['confirmation_sha256']
    assert json.loads((root/'calibrated/fresh_confirmation.json').read_text())['gate']
    assert sha256(root/'control_plan.json')==gain['plan_sha256']
    fresh = root/'fresh'
    jobs = json.loads((fresh/'manifest.json').read_text())['jobs']
    out = root/'control'
    assert not out.exists()
    out.mkdir()
    protected = {str(p.relative_to(REPO)):sha256(p) for p in [gain_path,root/'calibrated/affine_model_frozen.json',Path(__file__).resolve()]}
    write(out/'manifest.json',dict(execution_domain='VALIDATION_SIM',checkpoint_sha256=gain['checkpoint_sha256'],
        onnx_sha256=gain['onnx_sha256'],protected_sha256=protected,groups=GROUPS,cases=CASES,jobs=jobs,
        duration_s=20,gain_sha256=sha256(gain_path),no_QR_tuning=True))
    cfg = json.loads(prepared_config(CKPT).read_text())
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(control_job,cfg,job,str(fresh),str(out),gain) for job in jobs]
        for future in as_completed(futures):results.append(future.result())
    assert all(sha256(REPO/p)==h for p,h in protected.items())
    write(out/'completion.json',dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',results=results,
        protected_hashes_preserved=True,episodes=sum(r['runs'] for r in results),complete=sum(r['complete'] for r in results)))


if __name__=='__main__':
    main()
