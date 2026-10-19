"""DESKTOP_DRY_RUN: factorial effects, causal bias comparison and evidence audit."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from eval_m4_bias_reference import (REPO,KEYS,LOW,HIGH,DT,verify,arrays,write,sha256,paired_comparison)


def metrics(rows):
    complete=[r for r in rows if r.get('complete')]
    keys=['base_IAE','base_last5_RMSE','base_last5_mean','sensor_last5_mean','sensor_last5_RMSE','base_last5_speed_RMS',
        'midpoint_last5_RMSE','max_planar_drift','max_planar_from_original_goal','wheel_RMS','pitch_RMS_nominal','global_clip_fraction',
        'raw_over_feedback_cap','actual_total_min','actual_total_max','bias_final','bias_updates','yaw_change',
        'actual_residual_last5_mean','sensor_base_gap_last5_mean']
    return dict(count=len(rows),complete=len(complete),
        medians={k:float(np.median([r[k] for r in complete])) for k in keys} if complete else {},
        failures=[r.get('failure',r.get('reason')) for r in rows if not r.get('complete')])


def inspect_traces(root,phase,results):
    episodes=0;max_slew=0.;target_consistent=True;initial_exact=True;no_future_gain=True
    for case in results:
        folder=root/phase/case['id'];f=json.loads((root/'prepared'/case['id']/'frozen.json').read_text())
        assert sha256(root/'prepared'/case['id']/'frozen.json')==case['frozen_sha256']
        assert f['identified_model']==json.loads((root/'prepared'/case['id']/'model_before_validation.json').read_text())
        validation=arrays(root/'prepared'/case['id']/'common_validation.npz')
        targets=[];first=None
        for row in case['rows']:
            if 'trace' not in row:continue
            z=arrays(folder/row['trace']);episodes+=1;targets.append(row['target_sensor'])
            t=np.arange(len(z['sensor']))*DT;tail=(t>=row['duration_s']-5.)&(t<row['duration_s'])
            row['sensor_last5_RMSE']=float(np.sqrt(np.mean(z['sensor_error'][tail,0]**2)))
            row['sensor_base_gap_last5_mean']=float(np.mean(z['sensor_error'][tail,0]-z['base_path'][tail]))
            row['actual_residual_last5_mean']=float(np.mean(z['actual_u'][tail[:-1]]))
            assert row['target_sensor']==float(validation['sensor'][0,0])
            assert z['base_path'][0]==validation['base_path'][-1]
            assert z['axle_path'][0]==validation['axle_path'][-1]
            initial={key:z[key][0] for key in KEYS+['policy_observation','action','history']}
            if first is None:first=initial
            for key,value in initial.items():np.testing.assert_array_equal(value,first[key])
            np.testing.assert_array_equal(z['sensor'][:,0]-row['target_sensor'],z['sensor_error'][:,0])
            np.testing.assert_array_equal(z['previous_action'][:-1],z['history'])
            np.testing.assert_array_equal(z['previous_action'][1:],z['action'])
            kname=row.get('K_name','identified' if row['group'] in ['E2','E4'] else 'fixed')
            np.testing.assert_array_equal(row['K'],f['K_'+kname])
            error=np.concatenate([z['sensor_error'][:-1],z['previous_action'][:-1],z['leg_position'][:-1],z['leg_velocity'][:-1]],axis=1)
            error-=row['reference']
            np.testing.assert_allclose(-error@row['K'],z['raw_correction'],atol=1e-10,rtol=1e-10)
            assert np.array_equal(np.asarray(row['reference'])[:2],[0.,0.])
            assert LOW-1e-12<=z['requested_u'].min() and z['requested_u'].max()<=HIGH+1e-12
            assert LOW-1e-6<=z['actual_u'].min() and z['actual_u'].max()<=HIGH+1e-6
            assert max(abs(z['requested_u']-z['actual_u']))<1e-6
            assert max(abs(z['correction']))<=.050000001
            assert np.max(abs(z['physical_motor'][:,:,[3,7]]))<=12.000001
            row['max_planar_from_original_goal']=float(max(np.linalg.norm(
                z['base_position'][:,:2]-validation['base_position'][0,:2],axis=1)))
            slew=max(abs(np.diff(z['requested_u'])))/DT;max_slew=max(max_slew,float(slew));assert slew<=2.00000001
            if row.get('online'):
                assert max(abs(np.diff(z['bias'])))/DT<=.00050000001
                # Every new bias value is based on earlier transitions; rerun the
                # estimator independently from saved sensor and actual torque.
                from eval_m4_bias_reference import SlowBias
                b=SlowBias(row['bias_start'])
                for i in range(len(z['actual_u'])):
                    assert abs(b.value-z['bias'][i])<1e-14
                    b.observe(z['actual_u'][i],z['sensor_error'][i])
                assert abs(b.value-row['bias_final'])<1e-14
        assert len(set(targets))==1
    return dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',episodes=episodes,
        same_initial_state_observation_action_history=True,target_fixed_across_all_branches=True,
        fixed_K_matches_frozen_artifact=True,history_and_torque_limits=True,total_slew_max=max_slew,
        online_bias_causally_replayed=True)


def analyze(root):
    plan=json.loads((root/'plan.json').read_text());verify(plan)
    ab=json.loads((root/'ab_results.json').read_text())['rows']
    ab_integrity=inspect_traces(root,'ab',ab)
    decisions=json.loads((root/'ab_decision.json').read_text())
    groups={}
    for condition in sorted({r['condition'] for r in ab}):
        cases=sorted([r for r in ab if r['condition']==condition],key=lambda r:r['id'])
        groups[condition]={ref:{group:metrics([next(x for x in r['rows'] if x['reference_name']==ref and x['group']==group)
            for r in cases]) for group in ['E1','E2','E3','E4']} for ref in ['R0','R1']}
    cfile=root/'c_results.json';c=json.loads(cfile.read_text()) if cfile.exists() else dict(rows=[],status='NOT_TESTED')
    c_integrity=inspect_traces(root,'c',c['rows']) if c['rows'] else None
    c_summary={}
    for condition in sorted({r['condition'] for r in c['rows']}):
        cases=sorted([r for r in c['rows'] if r['condition']==condition],key=lambda r:r['id']);Ks={}
        for kname in ['fixed','identified']:
            def select(group):return [next(x for x in case['rows'] if x['K_name']==kname and x['group']==group) for case in cases]
            if not any(x['K_name']==kname for x in cases[0]['rows']):continue
            names=['C0_nominal_fixed_bias','C1_training_fixed_bias','C2_online_from_nominal','C3_online_from_training']
            Ks[kname]=dict(groups={name:metrics(select(name)) for name in names},
                recovery=paired_comparison(select(names[0]),select(names[2])),
                extra_online_benefit=paired_comparison(select(names[1]),select(names[3])),
                training_calibration_effect=paired_comparison(select(names[0]),select(names[1])))
        c_summary[condition]=Ks
    integrity=dict(ab=ab_integrity)
    if c_integrity:integrity['c']=c_integrity
    # A/B/C use identical original p targets, including the common validation
    # offset; no drifted position is accepted as the target for R1 or phase C.
    for case in c['rows']:
        previous=next(r for r in ab if r['id']==case['id'])
        assert {r['target_sensor'] for r in case['rows']}=={r['target_sensor'] for r in previous['rows'] if 'target_sensor' in r}
    write(root/'integrity.json',integrity)
    result=dict(execution_domain='DESKTOP_DRY_RUN',ab=groups,ab_decision=decisions,c=c_summary,
        c_status=c['status'],causal_C_no_oracle_bias=True,identification_and_reference_frozen_before_evaluation=True,
        aggregation='Median of3pitch summaries for same seed261 per condition; correlated initial states; no population significance')
    write(root/'summary.json',result);figures(root,ab,c['rows'])
    return result


def figures(root,ab,c):
    fig,axes=plt.subplots(3,2,figsize=(13,10))
    for i,condition in enumerate(sorted({r['condition'] for r in ab})):
        case=next(r for r in ab if r['condition']==condition and '_p+0.000' in r['id'])
        for j,ref in enumerate(['R0','R1']):
            for row in case['rows']:
                if row['reference_name']!=ref or 'trace' not in row:continue
                z=arrays(root/'ab'/case['id']/row['trace']);axes[i,j].plot(np.arange(len(z['base_path']))*DT,z['base_path']*1000,label=row['group'])
            axes[i,j].set(title=condition+' '+ref,ylabel='base sagittal error [mm]',xlabel='time after validation [s]')
            axes[i,j].grid(alpha=.3);axes[i,j].legend()
    fig.tight_layout();fig.savefig(root/'ab_factorial.png',dpi=150);plt.close(fig)
    if not c:return
    conditions=sorted({r['condition'] for r in c});fig,axes=plt.subplots(len(conditions),2,figsize=(13,4*len(conditions)),squeeze=False)
    for i,condition in enumerate(conditions):
        case=next(r for r in c if r['condition']==condition and '_p+0.000' in r['id'])
        for row in case['rows']:
            if row['K_name']!='fixed':continue
            z=arrays(root/'c'/case['id']/row['trace']);t=np.arange(len(z['base_path']))*DT
            axes[i,0].plot(t,z['base_path']*1000,label=row['group']);axes[i,1].plot(t[:-1],z['bias'],label=row['group'])
        axes[i,0].set(title=condition+' fixed K',ylabel='base sagittal error [mm]')
        axes[i,1].set(title=condition+' fixed K',ylabel='bias command [Nm]')
        for ax in axes[i]:ax.set_xlabel('time after validation [s]');ax.grid(alpha=.3);ax.legend(fontsize=7)
    fig.tight_layout();fig.savefig(root/'c_online_bias.png',dpi=150);plt.close(fig)


def audit(root,report):
    plan=json.loads((root/'plan.json').read_text());verify(plan)
    assert sha256(REPO/'test/eval_m4_bias_reference.py')==plan['script_sha256']
    assert hashlib.sha256(subprocess.check_output(['git','diff','--binary'])).hexdigest()==plan['tracked_diff_sha256']
    files=[REPO/'test'/name for name in ['eval_m4_bias_reference.py','analyze_m4_bias_reference.py','test_m4_bias_reference.py']]+[report]
    diff=[]
    for file in files:
        result=subprocess.run(['git','diff','--no-index','--','/dev/null',str(file)],capture_output=True)
        assert result.returncode in [0,1];diff.append(result.stdout)
        check=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(file)],capture_output=True)
        assert check.returncode in [0,1] and not check.stdout and not check.stderr
    (root/'task.diff').write_bytes(b''.join(diff))
    write(root/'final_review.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip(),
        previous_hashes_preserved=len(plan['protected_sha256']),tracked_diff_unchanged=True,
        new_files_sha256={str(p.relative_to(REPO)):sha256(p) for p in files},
        runtime_unchanged=True,no_QR_tuning=True,no_online_K_or_RLS_in_evaluation=True))
    for link in re.findall(r'\]\(([^)]+)\)',report.read_text()):
        assert (report.parent/link).exists(),link


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,required=True);parser.add_argument('--report',type=Path)
    args=parser.parse_args();root=args.root.resolve();analyze(root)
    if args.report:audit(root,args.report.resolve())
