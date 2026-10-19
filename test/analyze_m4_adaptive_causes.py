"""DESKTOP_DRY_RUN: quantitative cause separation; no controller/model changes."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from diagnose_m4_adaptive_causes import (OLD,COLD,REPO,arrays,state,fixed_gain,nominal,applied_gains,BIAS,verify,sha256,write)


def median(values):return np.median(np.asarray(values),axis=0).tolist()


def analyze(root):
    logged=json.loads((root/'log_results.json').read_text())['rows']
    physical=json.loads((root/'physical_results.json').read_text())['rows']
    groups={}
    for condition in sorted({r['condition'] for r in logged}):
        logs=[r for r in logged if r['condition']==condition]
        samples=[r for r in physical if r['item']['condition']==condition]
        torque={}
        for window in ['full','first10s','after10s','last5s']:
            summaries={}
            for group in ['Fixed','Adaptive']:
                row=[r['torque']['windows'][window]['groups'][group] for r in logs]
                summaries[group]={k:median([r[k] for r in row]) for k in row[0]}
            summaries.update({k:median([r['torque']['windows'][window][k] for r in logs]) for k in
                ['residual_difference_RMS','residual_difference_peak','same_state_raw_K_effect_RMS','same_state_limited_K_effect_RMS']})
            torque[window]=summaries
        parts=[]
        for r in logs:
            folder=COLD/r['id'];f=arrays(folder/'M4.npz');a=arrays(folder/'Adaptive_M4.npz')
            K0=np.asarray(fixed_gain()['K']);ref=np.asarray(fixed_gain()['reference'])
            kf=a['gain_K_after_step'][-1];ef=state(f);ea=state(a)
            ef[:,0]-=ef[0,0];ea[:,0]-=ea[0,0];ef-=ref;ea-=ref
            tail=slice(2750,3000);K_used=applied_gains(a['gain_K_after_step'],K0)
            delta_raw=float(-(kf-K0)@ef[tail].mean(0))
            contributions={}
            for name,e,K in [('Fixed',ef,np.tile(K0,(3000,1))),('Adaptive',ea,K_used)]:
                feedback=-K*e[:-1]
                contributions[name]=dict(position=feedback[tail,0].mean().item(),velocity=feedback[tail,1].mean().item(),
                    hidden=feedback[tail,2:].sum(1).mean().item(),total=feedback[tail].sum(1).mean().item(),
                    tail_sensor_position_mean=float(e[tail,0].mean()),tail_base_position_mean=float((f if name=='Fixed' else a)['base_path'][tail].mean()))
            events=json.loads((folder/'gain_updates.json').read_text())['events']
            parts.append(dict(id=r['id'],same_state_raw_change=delta_raw,
                same_state_position_shift_prediction=delta_raw/kf[0],
                observed_tail_sensor_position_shift=float(ea[tail,0].mean()-ef[tail,0].mean()),
                contribution=contributions,final_scaled_K_change=r['torque']['final_scaled_K_change'],
                event_guard_max=max(e['candidate']['scaled_gain_change_fraction'] for e in events if 'candidate' in e),
                actual_physical_wheel_difference_RMS=float(np.sqrt(np.mean((a['physical_motor'][:,:,[3,7]]-f['physical_motor'][:,:,[3,7]])**2)))))
        validation={}
        for tick in [350,1600,3000]:
            points=[next(x for x in r['validation'] if x['tick']==tick) for r in samples]
            models={}
            for name in points[0]['models']:
                rows=[p['models'][name] for p in points]
                models[name]=dict(pass_count=sum(r['gate'] for r in rows),count=len(rows),
                    full2_nrmse=median([r['summary']['full2s']['nrmse'] for r in rows]),
                    rolling2_nrmse=median([r['summary']['horizons']['100']['nrmse'] for r in rows]),
                    rolling2_rmse=median([r['summary']['horizons']['100']['rmse'] for r in rows]),
                    Bv_relative_error=median([r['Bv_error'] for r in rows]))
            validation[str(tick)]=models
        holds={}
        for label in ['nominal_bias','fixed_tail_input','tail_minus','tail_plus']:
            rows=[next(h for h in r['holds'] if h['label']==label) for r in samples]
            holds[label]=dict(input=median([r['input'] for r in rows]),
                final_base_path=median([r['metrics']['base_final_path'] for r in rows]),
                last10_mean_base_velocity=median([r['metrics']['windows']['last10s']['base_velocity_mean'] for r in rows]),
                last10_RMS_base_velocity=median([r['metrics']['windows']['last10s']['base_velocity_RMS'] for r in rows]),
                pitch_std=median([r['metrics']['pitch_std'] for r in rows]),
                mean_velocity_blocks={window:median([r['metrics']['windows'][window]['base_velocity_mean'] for r in rows])
                    for window in ['first10s','middle10s','last10s']})
        crossings=[]
        for r in samples:
            low=next(h for h in r['holds'] if h['label']=='tail_minus');high=next(h for h in r['holds'] if h['label']=='tail_plus')
            v0=low['metrics']['windows']['last10s']['base_velocity_mean'];v1=high['metrics']['windows']['last10s']['base_velocity_mean']
            crossing=float(low['input']-v0*(high['input']-low['input'])/(v1-v0))
            crossings.append(dict(id=r['item']['id'],zero_velocity_input=crossing,bracketed=v0*v1<0.,
                applied_as_new_input=False,interpretation='Interpolation of last10s means, not a verified static equilibrium.'))
        last=[r['affine'][-1] for r in logs]
        affine=dict(reference_defect_pv=median([r['reference_defect'][:2] for r in last]),
            reference_hidden_support=[r['hidden_reference_coordinates_inside_past_range'] for r in last],
            one_step_minimizer=median([r['one_step_defect_minimizer_input'] for r in last]),
            scaled_defect_norm=median([r['scaled_reference_defect_norm'] for r in last]),
            scaled_irreducible_defect_norm=median([r['scaled_irreducible_defect_norm'] for r in last]),
            empirical_tail_defect_pv=median([r['empirical_tail_model_defect'][:2] for r in last]),predictions={})
        for name in ['Fixed_K','Adopted_K']:
            rows=[r['predicted_steady'][name] for r in last]
            affine['predictions'][name]=dict(p_error=median([r['error'][0] for r in rows]),
                v_error=median([r['error'][1] for r in rows]),input=median([r['input'] for r in rows]),
                raw_condition_max=max(r['condition'] for r in rows),
                hidden_support=[r['hidden_coordinates_inside_past_range'] for r in rows])
        groups[condition]=dict(torque=torque,contributions=parts,validation=validation,holds=holds,
            finite_window_zero_crossings=crossings,affine=affine,
            RLS_gain_reconstruction_max_difference=max(json.loads((root/'logs'/r['id']/'recovered_models.json').read_text())['gain_replay_max_difference'] for r in logs))
    write(root/'summary.json',dict(execution_domain='DESKTOP_DRY_RUN',groups=groups,
        models_reconstructed_not_refit=True,no_new_control_algorithm=True,aggregation='median of trial summaries;3pitch same test seed per condition'))
    figures(root,groups,physical)
    return groups


def figures(root,groups,physical):
    fig,axes=plt.subplots(3,3,figsize=(14,10))
    for i,condition in enumerate(groups):
        name='settled_'+condition.split('/')[1]+'_p+0.000'
        f=arrays(COLD/name/'M4.npz');a=arrays(COLD/name/'Adaptive_M4.npz');t=np.arange(3000)*.02
        for label,z in [('Fixed',f),('Adaptive',a)]:
            axes[i,0].plot(t,z['actual_u'],label=label)
        axes[i,1].plot(t,(a['actual_u']-f['actual_u'])*1000)
        K0=np.asarray(fixed_gain()['K']);scale=np.asarray(nominal()['state_std'])
        norm=np.linalg.norm((a['gain_K_after_step']-K0)*scale,axis=1)/np.linalg.norm(K0*scale)*100
        axes[i,2].plot(t,norm);axes[i,2].axhline(25.,ls='--',color='gray',label='25% cumulative reference')
        axes[i,0].set(title=condition,ylabel='total residual command [Nm]')
        axes[i,1].set(title=condition,ylabel='Adaptive - Fixed [mNm]')
        axes[i,2].set(title=condition,ylabel='cumulative scaled K change [%]')
        axes[i,0].legend()
        for ax in axes[i]:ax.grid(alpha=.3);ax.set_xlabel('time [s]')
    fig.tight_layout();fig.savefig(root/'torque_and_gain.png',dpi=150);plt.close(fig)
    fig,axes=plt.subplots(3,2,figsize=(12,10))
    for i,condition in enumerate(groups):
        representative=next(r for r in physical if r['item']['condition']==condition and r['item']['test']['pitch']==0.)
        for h in representative['holds']:
            p=root/'physical'/representative['item']['id']/('hold_'+h['label']+'.npz')
            z=arrays(p);t=np.arange(len(z['sensor']))*.02
            from analyze_flash_odometry import integrate_path
            path=integrate_path(z['base_position'],z['rpy'][:,2])
            axes[i,0].plot(t,z['base_velocity']*1000,label=f"{h['label']} {h['input']:.6f}")
            axes[i,1].plot(t,path*1000,label=h['label'])
        axes[i,0].set(title=condition,ylabel='base velocity [mm/s]')
        axes[i,1].set(title=condition,ylabel='base path [mm]')
        for ax in axes[i]:ax.grid(alpha=.3);ax.set_xlabel('time [s]');ax.legend(fontsize=7)
    fig.tight_layout();fig.savefig(root/'constant_input_diagnosis.png',dpi=150);plt.close(fig)


def audit(root,report):
    plan=json.loads((root/'plan.json').read_text());verify(plan)
    old_plan=json.loads((OLD/'run_final/plan.json').read_text());verify(old_plan)
    assert sha256(REPO/'test/diagnose_m4_adaptive_causes.py')==plan['script_sha256']
    import hashlib,subprocess
    expected=(root/'tracked_diff_before.sha256').read_text().strip()
    now=hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest()
    assert expected==now
    sources=[REPO/'test'/name for name in ['diagnose_m4_adaptive_causes.py','analyze_m4_adaptive_causes.py','test_m4_adaptive_causes.py']]
    diff=[]
    for p in sources+[report]:
        value=subprocess.run(['git','diff','--no-index','--','/dev/null',str(p)],capture_output=True)
        assert value.returncode in [0,1];diff.append(value.stdout)
    (root/'task.diff').write_bytes(b''.join(diff))
    write(root/'final_review.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        previous_files_unchanged=len(plan['protected_sha256']),runtime_policy_and_prior_checkpoint_hashes_unchanged=True,
        tracked_diff_preserved=True,branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip(),
        source_sha256={str(p.relative_to(REPO)):sha256(p) for p in sources},
        no_model_refit_no_controller_QR_or_bias_change=True))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True);parser.add_argument('--report',type=Path)
    args=parser.parse_args();analyze(args.root.resolve())
    if args.report:audit(args.root.resolve(),args.report.resolve())
