"""DESKTOP_DRY_RUN: audit static Target evidence, scores and scientific limits."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import subprocess

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from run_static_target_adaptation import verify, write, ARMS, score, sha256
from analyze_flash_state_learning import state as measured_state
from m4_joint_adaptation import nominal, fixed_gain, SUPPORT_HALF_WIDTH
from m4_shadow_stages import prediction_gate


def median(values):
    return None if not values else float(np.median(values))


def absolute_baseline_error(model,states,inputs):
    """Free prediction with c; diagnostic only, no post-hoc change to frozen gates."""
    A=np.asarray(model['A']);B=np.asarray(model['B']);c=np.asarray(model['c_center'])
    reference=np.asarray(model['state_reference']);result={}
    for horizon in [5,25,50,100]:
        start=np.arange(0,len(inputs)-horizon+1,5);prediction=states[start].copy()
        with np.errstate(over='ignore',invalid='ignore'):
            for offset in range(horizon):
                prediction=(prediction-reference)@A.T+(inputs[start+offset]-.4828)[:,None]*B+reference+c
            result[str(horizon)]=np.sqrt(np.mean((prediction[:,:2]-states[start+horizon,:2])**2,axis=0)).tolist()
    return result


def analyze(root,require_complete=True):
    plan=json.loads((root/'plan.json').read_text());verify(plan,root)
    state=json.loads((root/'pipeline_state.json').read_text())
    if require_complete:assert state['status']=='COMPLETE'
    phases={}
    for name,record in state['stages'].items():
        if record['status']!='COMPLETE':continue
        assert sha256(root/record['artifact'])==record['sha256']
        phases[name]=json.loads((root/record['artifact']).read_text())['rows']
    summaries={};metrics=[];integrity=[];learning=[];model_checks=[];observation_gaps=[];inactive_equivalence=[]
    paths={'00_phase0':'phase0','01_safety':'safety','02_shadow':'shadow','03_primary':'primary',
           '04_composite_pilot':'composite_pilot','05_composite_shadow':'composite_shadow','06_composite_primary':'composite_primary'}
    for phase,cases in phases.items():
        grouped={}
        for case in cases:
            folder=root/paths[phase]/case['job']['id'];first=None
            physics=json.loads((folder/'physics.json').read_text())
            assert physics['configured_before_first_step']
            assert physics['target']==case['job']['effect']
            for row in case['rows']:
                domain=case['job']['domain'];grouped.setdefault(domain,{}).setdefault(row['arm'],[]).append(row)
                metric=dict(phase=phase,domain=domain,seed=case['job']['seed'],pitch=case['job']['pitch'],arm=row['arm'],
                    complete=row['complete'],absolute_hold=row['absolute_hold'],failure=str(row['failure']),
                    end_s=row['end_s'],full_IAE=row.get('full',{}).get('IAE'),terminal_error=row.get('terminal_error'),
                    max_planar=row.get('full',{}).get('max_planar'),last5_velocity=row.get('last5',{}).get('speed_RMS'),
                    last20_velocity=row.get('last20',{}).get('speed_RMS'),
                    calibration_IAE=(row.get('calibration')or{}).get('IAE'),
                    post_IAE=(row.get('post_calibration')or{}).get('IAE'),
                    pitch_RMS=row.get('full',{}).get('pitch_RMS'),wheel_RMS=row.get('full',{}).get('wheel_RMS'),
                    software_saturation_fraction=row.get('software_saturation_fraction'),
                    physical_saturation_fraction=row.get('physical_saturation_fraction'),probe_energy=row.get('probe_energy'),
                    recovery_s=row.get('recovery_s'),yaw_change=row.get('yaw_change'),
                    new_target_K_adoptions=row.get('new_target_K_adoptions',0))
                metrics.append(metric)
                file=folder/(row['arm']+'.npz')
                if not file.exists():
                    assert 'startup' in row['failure'];continue
                with np.load(file)as z:
                    initial=np.r_[z['sensor'][0],z['previous_action'][0],z['leg_position'][0],z['leg_velocity'][0],
                        z['base_position'][0],z['position'][0],z['rpy'][0],z['gyro'][0]]
                    if first is None:first=initial.copy()
                    np.testing.assert_array_equal(first,initial)
                    assert float(z['p_hold'])==float(z['sensor'][0,0])
                    np.testing.assert_array_equal(z['goal_base_position'],z['base_position'][0])
                    if not len(z['physical_motor']):
                        assert not row['complete']
                        integrity.append(dict(phase=phase,id=case['job']['id'],arm=row['arm'],zero_step_guard=True))
                        continue
                    np.testing.assert_array_equal(z['previous_action'][:-1],z['history'])
                    np.testing.assert_array_equal(z['previous_action'][1:],z['action'])
                    np.testing.assert_array_equal(z['physical_motor'][:,:,[0,1,2,4,5,6]],z['flash'][:,:,[0,1,2,4,5,6]])
                    assert np.max(abs(z['physical_motor'][:,:,[3,7]]))<=12.000001
                    assert not np.any(z['physical_saturation']&(abs(z['probe'])>1e-12))
                    u=z['raw_requested'];assert np.max(abs(np.diff(np.r_[0.,u])))<=.040000001
                    if row['arm']=='Flash':np.testing.assert_array_equal(u,np.zeros(len(u)))
                    else:
                        assert u.max()<=.532800001
                        if len(u)>13:assert u[13:].min()>=.432799999
                        np.testing.assert_array_equal(z['reference_used'][:,:2],np.zeros((len(u),2)))
                        np.testing.assert_allclose(z['effective_offset'],z['bias']+np.einsum('ij,ij->i',z['K_used'],z['reference_used']),atol=1e-10)
                    rescored=score(dict(z),row['complete'],row['failure'])
                    assert abs(rescored['full']['IAE']-row['full']['IAE'])<1e-12
                    measured=measured_state(dict(z));measured[:,0]-=float(z['p_hold'])
                    gaps=[]
                    for seconds in [1.,5.,60.,180.]:
                        index=round(seconds/.02)
                        if index>=len(measured):continue
                        gaps.append(dict(t=seconds,sensor_path=float(measured[index,0]),base_path=float(z['base_path'][index]),
                            midpoint_path=float(z['midpoint_path'][index]),sensor_minus_base=float(measured[index,0]-z['base_path'][index]),
                            midpoint_minus_base=float(z['midpoint_path'][index]-z['base_path'][index])))
                    observation_gaps.append(dict(phase=phase,id=case['job']['id'],domain=domain,arm=row['arm'],complete=row['complete'],samples=gaps))
                    prior=nominal();train_lo=np.asarray(prior['train_min']);train_hi=np.asarray(prior['train_max'])
                    train_fraction=float(np.mean(np.all((measured[:,1:]>=train_lo[1:])&(measured[:,1:]<=train_hi[1:]),axis=1)))
                    operational_fraction=float(np.mean(np.all(abs(measured-np.asarray(fixed_gain()['reference']))<=SUPPORT_HALF_WIDTH,axis=1)))
                    updates={}
                    for name,key in [('bias','bias'),('reference','reference_used'),('K','K_used')]:
                        values=z[key];difference=np.diff(values,axis=0)
                        changed=np.flatnonzero(abs(difference)>1e-14)if difference.ndim==1 else np.flatnonzero(np.any(abs(difference)>1e-14,axis=1))
                        updates[name]=dict(actual_command_changes=len(changed),first_applied_s=float((changed[0]+1)*.02)if len(changed)else None)
                integrity.append(dict(phase=phase,id=case['job']['id'],arm=row['arm'],target_static=row['target_hash_constant'],initial_goal_fixed=True,
                    raw_action_leg_and_budget=True,score_recomputed=True,
                    original_nonposition_train_box_fraction=train_fraction,operational_support_fraction=operational_fraction))
                learning_file=folder/(row['arm']+'_learning.json')
                if learning_file.exists():
                    d=json.loads(learning_file.read_text());models=d['new_target_K_adoptions']
                    for model in [d['full_model'],d['partial_model']]+[v['model']for v in models]:
                        column=np.zeros(24);column[0]=1.
                        np.testing.assert_array_equal(np.asarray(model['A'])[:,0],column)
                        np.testing.assert_array_equal(np.asarray(model['B'])[4:12],np.zeros(8))
                        reference=np.asarray(model['state_reference']);A=np.asarray(model['A']);B=np.asarray(model['B'])
                        np.testing.assert_allclose(model['c_absolute'],reference-A@reference-B*.4828+np.asarray(model['c_center']),atol=1e-10)
                    times=[x['step']*.02 for x in models]
                    reasons=Counter()
                    for e in d['candidates']:
                        if e.get('adopted'):continue
                        reason=e.get('reason')
                        if reason is None:reason=('causal_prediction_or_conditional_B' if not e.get('validation',{}).get('gate',False)
                            else 'information_or_gain_guard')
                        reasons[reason]+=1
                    learning.append(dict(phase=phase,id=case['job']['id'],arm=row['arm'],adoptions=len(times),
                        first_K_s=times[0]if times else None,first_bias_s=next((e['step']*.02 for e in d['events']if e['kind']=='bias'),None),
                        first_reference_s=next((e['step']*.02 for e in d['events']if e['kind']=='reference_target'and e['gate']),None),
                        rejection_reasons=dict(reasons),information=d['information'],
                        full_model_nonposition_rho=float(max(abs(np.linalg.eigvals(np.asarray(d['full_model']['A'])[1:,1:])))),
                        B2_shadow_proposals=len(d['B2_shadow']),B2_applied=0,
                        actual_parameter_updates=updates,
                        full_independent_gate=row.get('full_model_gate'),partial_independent_gate=row.get('partial_model_gate'),
                        adopted_independent_gate=row.get('adopted_model_gate')))
                    for mode in ['full','partial','adopted']:
                        verdict_file=folder/(row['arm']+'_'+mode+'_validation')/'verdict.json'
                        verdict=json.loads(verdict_file.read_text())if verdict_file.exists()else None
                        baseline_file=verdict_file.parent/'baseline.npz'
                        if verdict is not None and baseline_file.exists():
                            model=d[mode+'_model']if mode!='adopted'else models[-1]['model']
                            with np.load(baseline_file)as b:
                                verdict['absolute_baseline_pv_RMSE']=absolute_baseline_error(model,measured_state(dict(b)),b['actual_u'])
                        model_checks.append(dict(phase=phase,id=case['job']['id'],arm=row['arm'],mode=mode,
                            status=('PASS'if verdict['gate']else'FAIL')if verdict else'NOT_TESTED',
                            reason=None if verdict else row.get('model_validation','no adopted K model'),verdict=verdict))
                    folder_full=folder/(row['arm']+'_full_validation')
                    file=folder_full/'verdict.json'
                    source=json.loads(file.read_text())if file.exists()else{}
                    if 'Direct_B'in source:
                        families=['validation_sine','validation_prbs','pulse_pos','pulse_neg','step_pos','step_neg','bipulse_pos','bipulse_neg']
                        with np.load(folder_full/'baseline.npz')as b:
                            baseline=measured_state(dict(b));baseline_u=b['actual_u'].copy()
                        deltas=[];inputs=[]
                        for family in families:
                            with np.load(folder_full/(family+'.npz'))as p:
                                deltas.append(measured_state(dict(p))-baseline);inputs.append(p['actual_u']-baseline_u)
                        value=prediction_gate(dict(nominal(),indices=list(range(24))),deltas,inputs,source['Direct_B'][1])
                        value['absolute_baseline_pv_RMSE']=absolute_baseline_error(nominal(),baseline,baseline_u)
                        model_checks.append(dict(phase=phase,id=case['job']['id'],arm=row['arm'],mode='nominal',
                            status='PASS'if value['gate']else'FAIL',reason=None,verdict=value,
                            source='same offline responses as full model; no new physics/learning data'))
            by_arm={r['arm']:r for r in case['rows']}
            if all(a in by_arm and by_arm[a]['complete']for a in ['E6','E7'])and by_arm['E7'].get('new_target_K_adoptions',0)==0:
                with np.load(folder/'E6.npz')as a,np.load(folder/'E7.npz')as b:
                    for key in a.files:np.testing.assert_array_equal(a[key],b[key])
                inactive_equivalence.append(dict(phase=phase,id=case['job']['id'],all_arrays_exact=True))
        result={}
        for domain,groups in grouped.items():
            result[domain]={}
            for arm,rows in groups.items():
                complete=[r for r in rows if r['complete']]
                result[domain][arm]=dict(count=len(rows),complete=len(complete),absolute_hold=sum(r['absolute_hold']for r in rows),
                    failure_counts=dict(Counter(f for r in rows for f in r['failure'])),
                    median_complete_IAE=median([r['full']['IAE']for r in complete]),
                    median_complete_max_planar=median([r['full']['max_planar']for r in complete]),
                    median_complete_terminal_error=median([abs(r['terminal_error'])for r in complete]),
                    median_complete_last5_velocity=median([r['last5']['speed_RMS']for r in complete]),
                    recovery_count=sum(r.get('recovery_s')is not None for r in complete),
                    recovery_median_s=median([r['recovery_s']for r in complete if r.get('recovery_s')is not None]),
                    new_K=sum(r.get('new_target_K_adoptions',0)for r in rows))
                for label,section,key in [('calibration_IAE','calibration','IAE'),('post_IAE','post_calibration','IAE'),
                        ('last20_velocity','last20','speed_RMS'),('pitch_RMS','full','pitch_RMS'),('wheel_RMS','full','wheel_RMS')]:
                    result[domain][arm]['median_'+label]=median([(r.get(section)or{}).get(key)for r in complete if (r.get(section)or{}).get(key)is not None])
                for key in ['software_saturation_fraction','physical_saturation_fraction','probe_energy']:
                    result[domain][arm]['median_'+key]=median([r[key]for r in complete if r.get(key)is not None])
                values=[r['full']['IAE']for r in complete]
                result[domain][arm]['IAE_distribution']=dict(percentiles=np.percentile(values,[0,25,50,75,100]).tolist(),
                    trials=values)if values else None
                for baseline in ['Fixed','E6']:
                    if baseline not in groups:continue
                    paired=[(r,b)for r,b in zip(rows,groups[baseline])if r['complete']and b['complete']]
                    if len(paired)!=len(rows):continue
                    ratio=median([r['full']['IAE']for r,b in paired])/max(median([b['full']['IAE']for r,b in paired]),1e-12)
                    wins=sum(r['full']['IAE']<b['full']['IAE']for r,b in paired)
                    result[domain][arm][baseline+'_comparison']=dict(IAE_ratio=ratio,paired_wins=wins,
                        gate=len(rows)>=6 and ratio<=.9 and wins>=4)
            destination=root/'domain_metrics'/phase/domain;destination.mkdir(parents=True,exist_ok=True)
            write(destination/'metrics.json',dict(summary=result[domain],trials=groups))
            domain_rows=[m for m in metrics if m['phase']==phase and m['domain']==domain]
            with (destination/'metrics.csv').open('w',newline='')as f:
                writer=csv.DictWriter(f,fieldnames=list(domain_rows[0]));writer.writeheader();writer.writerows(domain_rows)
        summaries[phase]=result
    with (root/'metrics.csv').open('w',newline='')as f:
        writer=csv.DictWriter(f,fieldnames=list(metrics[0]));writer.writeheader();writer.writerows(metrics)
    write(root/'metrics.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=metrics))
    write(root/'summary.json',dict(execution_domain='DESKTOP_DRY_RUN',phases=summaries))
    write(root/'learning_summary.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=learning))
    write(root/'independent_model_checks.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=model_checks,
        note='Matched offline input responses, no data returned to online learner. Missing safe validation is NOT_TESTED, not prediction FAIL.'))
    write(root/'observation_reference_gaps.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=observation_gaps,
        note='Measured path definitions only, not a unique causal slip decomposition. No sensor/reference/goal correction applied.'))
    write(root/'inactive_K_equivalence.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        rows=inactive_equivalence,note='E6/E7 have identical probing and nominal K when target K adoption is zero. KOnly vs Fixed may differ because of probing.'))
    write(root/'analysis_integrity.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',episodes=integrity,
        protected_hashes_verified=True,plan_frozen=True))
    plots(root,phases,paths)
    report(root,plan,summaries,learning,metrics,state)
    return summaries


def plots(root,phases,paths):
    for phase in ['00_phase0','03_primary','06_composite_primary']:
        if phase not in phases:continue
        cases=phases[phase]
        for domain in sorted({c['job']['domain']for c in cases}):
            case=sorted([c for c in cases if c['job']['domain']==domain],key=lambda c:(c['job']['seed'],abs(c['job']['pitch'])))[0]
            fig,axes=plt.subplots(1,3,figsize=(14,3.5));folder=root/paths[phase]/case['job']['id']
            for row in case['rows']:
                file=folder/(row['arm']+'.npz')
                if not file.exists():continue
                with np.load(file)as z:
                    t=np.arange(len(z['sensor']))*.02
                    axes[0].plot(t,z['base_path']*1000,label=row['arm'])
                    axes[1].plot(t[:-1],z['actual_u'],label=row['arm'])
                    if row['arm']not in ['Flash','Bias']:
                        axes[2].plot(t[:-1],z['effective_offset'],label=row['arm'])
            for ax,label in zip(axes,['base sagittal error [mm]','known residual command [Nm]','effective offset [Nm]']):
                ax.set_xlabel('deployment time [s]');ax.set_ylabel(label);ax.axvline(60.,ls='--',color='gray');ax.grid(alpha=.2)
            axes[0].legend(fontsize=7);fig.suptitle(phase+' '+domain);fig.tight_layout()
            out=root/'plots';out.mkdir(exist_ok=True);fig.savefig(out/(phase+'_'+domain+'.png'),dpi=140);plt.close(fig)
            if phase in ['03_primary','06_composite_primary']and (folder/'E6.npz').exists():
                with np.load(folder/'E6.npz')as z:
                    t=np.arange(len(z['sensor']))*.02
                    fig,axes=plt.subplots(1,2,figsize=(11,3.5))
                    for ax in axes:
                        ax.plot(t,(z['sensor'][:,0]-z['p_hold'])*1000,label='encoder / IMU')
                        ax.plot(t,z['midpoint_path']*1000,label='wheel midpoint GT')
                        ax.plot(t,z['base_path']*1000,label='base origin GT')
                        ax.axhline(0.,color='gray',lw=.7);ax.grid(alpha=.2);ax.set_xlabel('deployment time [s]');ax.set_ylabel('sagittal path [mm]')
                    axes[0].set_xlim(0.,5.);axes[0].legend(fontsize=8);fig.suptitle('E6: '+domain+' / fixed original goal')
                    fig.tight_layout();fig.savefig(out/(phase+'_'+domain+'_reference_points.png'),dpi=140);plt.close(fig)
    summary=json.loads((root/'summary.json').read_text())['phases']
    domains=[(phase,d,arms)for phase in ['03_primary','06_composite_primary']for d,arms in summary.get(phase,{}).items()]
    if domains:
        fig,axes=plt.subplots(1,3,figsize=(15,4.5));x=np.arange(len(domains));width=.22
        settings=[('median_complete_IAE',1000.,'full IAE [mm s]',None),
            ('median_complete_max_planar',1000.,'maximum planar drift [mm]',50.),
            ('median_complete_terminal_error',1000.,'terminal sagittal error [mm]',10.)]
        for offset,arm in enumerate(['Fixed','E6','E7']):
            for ax,(key,scale,label,threshold)in zip(axes,settings):
                ax.bar(x+(offset-1)*width,[np.nan if a[arm][key]is None else a[arm][key]*scale for _,_,a in domains],width,label=arm)
        for ax,(_,_,label,threshold)in zip(axes,settings):
            ax.set_xticks(x,[d for _,d,_ in domains],rotation=55,ha='right',fontsize=7);ax.set_ylabel(label);ax.grid(axis='y',alpha=.2)
            if threshold:ax.axhline(threshold,color='red',ls='--',lw=1.,label='absolute goal')
        axes[0].legend();fig.suptitle('Held-out full deployment: trial medians, original position target')
        fig.tight_layout();fig.savefig(root/'plots'/'deployment_comparison.png',dpi=160);plt.close(fig)


def report(root,plan,summaries,learning,metrics,status):
    evaluated=[(domain,arms)for phase in ['03_primary','06_composite_primary']for domain,arms in summaries.get(phase,{}).items()]
    full_success=[domain for domain,arms in evaluated if arms.get('E7',{}).get('new_K',0)>0
        and arms['E7'].get('E6_comparison',{}).get('gate',False) and arms['E7'].get('Fixed_comparison',{}).get('gate',False)]
    hold_domains=[domain for domain,arms in evaluated if arms.get('E6',{}).get('absolute_hold',0)==6]
    scientific=dict(execution_domain='DESKTOP_DRY_RUN',workflow=status['status'],
        dynamics_K_control_evidence='PASS'if full_success else('FAIL'if evaluated else'NOT_TESTED'),
        active_target_K_efficacy='NOT_TESTED'if not any(a.get('E7',{}).get('new_K',0)for _,a in evaluated)else('PASS'if full_success else'FAIL'),
        full_joint_success_domains=full_success,E6_absolute_hold_domains=hold_domains,
        note='Model accuracy, actual new K adoption and E7 extra physical benefit are separate requirements; no adoption means no K adaptation proof.')
    write(root/'scientific_decision.json',scientific)
    lines=['# TITA FlashSAC — Static Target-Domain Adaptation MORNING_REPORT','',
        '작성일: 2026-10-16 (Asia/Seoul)','',
        'Execution Domain: **VALIDATION_SIM** (분석·무결성: **DESKTOP_DRY_RUN**)','',
        'Policy Checkpoint SHA256: `'+plan['policy_sha256']+'`','',
        'Evidence Status: **'+scientific['dynamics_K_control_evidence']+' — 새로운 Target K 채택과 추가 제어 이득을 포함한 Full Joint 검증.** '
        '**'+scientific['active_target_K_efficacy']+' — 실제 새 K를 활성화한 제어 성능 비교.** '
        '단계별 안전성·식별·제어 성능은 아래에 분리한다. Workflow 완료는 연구 성능 PASS가 아니다.','',
        f'현재 실행 상태: **{status["status"]}**. RUNNING이면 완료된 단계만의 중간 집계다.','',
        'Observed Metrics / Behavior / Log Summary:','',
        '첫 startup physics 이전에 Target을 설정하고 종료까지 고정했다. RLS/제어는 sensor와 software clipping 뒤 알려진 residual만 사용했다. '
        '동역학 라벨/값 및 GT는 learner에 전달하지 않았다. Actor는 frozen model_60000이며 prior A/B/c/K는 **nominal MuJoCo offline calibration**이다. '
        'Isaac-only source identification이나 실기 성공으로 해석하지 않는다.','',
        '## Phase 0 — residual 없는 원래 정책','',
        '새 Target의 FlashSAC-only 전체 pilot33회를 먼저 종료한 뒤 Safety/Shadow를 시작했다. '
        '아래 drift는 정상60초 완료 trial의 중앙값이며 실패한 짧은 trial을 좋은 drift로 집계하지 않는다.','',
        '| Target | 완료/3 | 최대 planar drift m | 실패 |','|---|---:|---:|---|']
    fmt=lambda value:'N/A'if value is None else f'{value:.5g}'
    for domain,arms in summaries.get('00_phase0',{}).items():
        row=arms['Flash'];lines.append(f'| {domain} | {row["complete"]}/{row["count"]} | {fmt(row["median_complete_max_planar"])} | {row["failure_counts"]} |')
    lines+=['','## Fixed pilot — balancing과 위치 유지의 구분','',
        '각 Target의3개 개발 시작조건에서60초를 평가했다. 후속 단계 admission은3/3 완료·후반속도≤50mm/s·종료위치≤250mm다. '
        '이는180초 절대 hold 기준보다 느슨한 운용 가능성 gate이며 위치 유지 PASS가 아니다.','',
        '| Target | 완료/3 | 종료 위치 절댓값 mm | 후반 속도 RMS mm/s | 입력 포화 % | 후속 |',
        '|---|---:|---:|---:|---:|---|']
    safe=json.loads((root/'safety_gates.json').read_text())if (root/'safety_gates.json').exists()else{}
    for domain,arms in summaries.get('01_safety',{}).items():
        v=arms['Fixed']
        lines.append(f'| {domain} | {v["complete"]}/{v["count"]} | '
            f'{fmt(None if v["median_complete_terminal_error"]is None else v["median_complete_terminal_error"]*1000)} | '
            f'{fmt(None if v["median_complete_last5_velocity"]is None else v["median_complete_last5_velocity"]*1000)} | '
            f'{fmt(None if v["median_software_saturation_fraction"]is None else v["median_software_saturation_fraction"]*100)} | '
            f'{"허용"if safe.get(domain,{}).get("safe",False)else"NOT_TESTED"} |')
    lines+=['','## Held-out deployment —0–180초, 최초 목표 고정','',
        'Calibration0–60초의 이동/입력도 full IAE에 포함한다. 같은 Target의6개 시작조건이며 seed610/611×3pitch의 관련 반복이다. '
        '완료율과 절대 위치 유지(최대planar≤0.05m, 종료sagittal≤0.01m, 마지막5초speedRMS≤0.2mm/s)를 별도로 기록한다.','',
        '| Target | 군 | 완료/6 | 절대 유지/6 | Full IAE mm·s | 최대 drift mm | 후반속도 mm/s | 새 K 수 |','|---|---|---:|---:|---:|---:|---:|---:|']
    for phase in ['03_primary','06_composite_primary']:
        for domain,arms in summaries.get(phase,{}).items():
            for name,row in arms.items():
                lines.append(f'| {domain} | {name} | {row["complete"]}/{row["count"]} | {row["absolute_hold"]}/{row["count"]} | '
                    f'{fmt(None if row["median_complete_IAE"]is None else row["median_complete_IAE"]*1000)} | '
                    f'{fmt(None if row["median_complete_max_planar"]is None else row["median_complete_max_planar"]*1000)} | '
                    f'{fmt(None if row["median_complete_last5_velocity"]is None else row["median_complete_last5_velocity"]*1000)} | {row["new_K"]} |')
    lines+=['','## E6 / E7의 추가 이득','',
        '| Target | Fixed/Flash IAE 비 | E6/Fixed IAE 비 | E6 paired 개선 | E6 상대 gate | E7/E6 IAE 비 | E7 새 K |','|---|---:|---:|---:|---|---:|---:|']
    for phase in ['03_primary','06_composite_primary']:
        for domain,arms in summaries.get(phase,{}).items():
            a,b=arms.get('E6',{}),arms.get('E7',{})
            fixed_flash=arms['Fixed']['median_complete_IAE']/max(arms['Flash']['median_complete_IAE'],1e-12)if arms['Fixed']['median_complete_IAE']is not None and arms['Flash']['median_complete_IAE']is not None else None
            comparison=a.get('Fixed_comparison',{})
            lines.append(f'| {domain} | {fmt(fixed_flash)} | {fmt(comparison.get("IAE_ratio"))} | '
                f'{comparison.get("paired_wins",0)}/6 | {"PASS"if comparison.get("gate",False)else"FAIL"} | '
                f'{fmt(b.get("E6_comparison",{}).get("IAE_ratio"))} | {b.get("new_K",0)} |')
    lines+=['','E6의6/6 절대 유지 환경: '+(', '.join(hold_domains)or('없음'if status['status']=='COMPLETE'else'없음/미완료'))+'. '
        '새 K 채택과 E6/Fixed 대비 사전 추가 성능 기준을 함께 만족한 환경: '+(', '.join(full_success)or('없음'if status['status']=='COMPLETE'else'없음/미완료'))+'.','',
        '## 초기60초와 후속120초','',
        '| Target | 군 | 0–60초 IAE mm·s | 60–180초 IAE mm·s | 포화 시간 % | probing 에너지 Nm²·s | 복귀 수/6 |',
        '|---|---|---:|---:|---:|---:|---:|']
    for domain,arms in evaluated:
        for arm in ['Fixed','BiasOnline','RefOnline','E6','E7']:
            v=arms[arm]
            lines.append(f'| {domain} | {arm} | {fmt(None if v["median_calibration_IAE"]is None else v["median_calibration_IAE"]*1000)} | '
                f'{fmt(None if v["median_post_IAE"]is None else v["median_post_IAE"]*1000)} | '
                f'{fmt(None if v["median_software_saturation_fraction"]is None else v["median_software_saturation_fraction"]*100)} | '
                f'{fmt(v["median_probe_energy"])} | {v["recovery_count"]}/{v["count"]} |')
    if evaluated:lines+=['','![전체 배포의 Fixed/E6/E7 비교](plots/deployment_comparison.png)','']
    lines+=['','## 식별·채택 시간과 제한','',
        '온라인 후보 모델은 nominal prior에서 단일 실제 rollout으로 학습한다. 동결된 후보의 후속4초 센서 검증과 조건부 B 회귀는 '
        'offline matched-state Direct B와 다른 측정이다. 사용자가 이 분리를 승인했으며 offline 물리 분기 결과/GT는 online learner에 들어가지 않는다. '
        '정보량·예측 실패 또는 domain Shadow 실패에서는 새 K를 적용하지 않는다. 새 K가0회면 A/B 기반 K 적응 성공이라고 부르지 않는다.','',
        '| Stage / Target / 군 | 첫 K 채택 s, 중앙값 | 채택 합 | 독립 full 모델 PASS / 시행 |','|---|---:|---:|---:|']
    groups={}
    for row in learning:groups.setdefault((row['phase'],row['id'].rsplit('_s',1)[0],row['arm']),[]).append(row)
    for key,rows in groups.items():
        lines.append('| '+' / '.join(key)+f' | {fmt(median([x["first_K_s"]for x in rows if x["first_K_s"]is not None]))} | '
            f'{sum(x["adoptions"]for x in rows)} | {sum(x["full_independent_gate"]is True for x in rows)}/{sum(x["full_independent_gate"]is not None for x in rows)} |')
    lines+=['','| Stage / Target / 군 | 사용 transition 중앙값 | scaled condition | 입력 innovation % | 비위치 A rho |',
        '|---|---:|---:|---:|---:|']
    for key,rows in groups.items():
        if key[2]!='E7'and not(key[0]in ['02_shadow','05_composite_shadow']and key[2]=='KOnly'):continue
        values=[]
        for name in ['samples','scaled_condition','input_innovation_fraction']:
            values.append(median([r['information'][name]for r in rows if r['information'].get(name)is not None]))
        if values[2]is not None:values[2]*=100
        values.append(median([r['full_model_nonposition_rho']for r in rows]))
        lines.append('| '+' / '.join(key)+' | '+' | '.join(fmt(v)for v in values)+' |')
    lines+=['','180초는9000 transition이지만 포화/범위/안전 gate로 실제 RLS 사용량은 더 작을 수 있다. '
        '추정 A의rho>1은 모델 자유 예측의 문제이며 실제 MuJoCo 전도를 뜻하지 않는다. 정보량 gate 통과와 독립 예측 통과도 별개의 판정이다.']
    checks=json.loads((root/'independent_model_checks.json').read_text())['rows']
    lines+=['','### 같은 입력 응답에서의 모델 비교','',
        '다음은 실제 수행한 독립 입력 검증만 집계했다. 같은 응답에 여러 모델을 적용했다.'
        'NRMSE는 paired 응답의2초rolling으로 A/B를 검사한다. c를 포함한 absolute baseline 자유 예측 RMSE도 별도로 측정했다. '
        '이 RMSE는 기존 PASS/FAIL gate를 사후 변경하지 않는 추가 진단이다. 온라인 후보 검증은 원래부터 c를 포함한 absolute 후속 예측이다. '
        'Direct B는 같은 snapshot의±토크 차분이다. A고정B/c shadow는 실제 제어에 사용하지 않았다.','',
        '| Stage / Target | 모델 | PASS/시행 | rolling2초 p/v NRMSE % | Direct B 상대오차 % | absolute baseline2초 p/v RMSE mm,mm/s |','|---|---|---:|---:|---:|---:|']
    check_groups={}
    for v in checks:
        if v['status']=='NOT_TESTED'or v['mode']=='adopted':continue
        check_groups.setdefault((v['phase'],v['id'].rsplit('_s',1)[0],v['mode']),[]).append(v)
    for (phase,domain,mode),rows in check_groups.items():
        pv=[];be=[];absolute=[]
        for row in rows:
            v=row['verdict']
            nrmse=v.get('prediction',{}).get('horizons',{}).get('100',{}).get('nrmse')
            if nrmse and all(x is not None for x in nrmse):pv.append(nrmse)
            if v.get('B_relative_error')is not None:be.append(v['B_relative_error']*100)
            rmse=v.get('absolute_baseline_pv_RMSE',{}).get('100')
            if rmse and all(x is not None for x in rmse):absolute.append(rmse)
        text='N/A'if not pv else ' / '.join(fmt(x*100)for x in np.median(pv,axis=0))
        abs_text='N/A'if not absolute else ' / '.join(fmt(x*1000)for x in np.median(absolute,axis=0))
        lines.append(f'| {phase} / {domain} | {mode} | {sum(v["status"]=="PASS"for v in rows)}/{len(rows)} | {text} | {fmt(median(be))} | {abs_text} |')
    lines+=['','`0/0`은 안전한 독립 probing을 하지 못한 NOT_TESTED다. 예측 FAIL 수와 합치지 않는다. '
        '60초 Shadow gate가 불통과이면 뒤의 모델이 나아져도 이번 primary에서 K 권한을 사후 열지 않는다.','',
        '| Stage / Target / 군 | Bias 실제 변화 trial | 첫 Bias 적용 s | Reference 실제 변화 trial | 첫 Reference 적용 s |',
        '|---|---:|---:|---:|---:|']
    for key,rows in groups.items():
        if key[0]not in ['03_primary','06_composite_primary']or key[2]not in ['BiasOnline','RefOnline','E6','E7']:continue
        bias=[v['actual_parameter_updates']['bias']['first_applied_s']for v in rows]
        ref=[v['actual_parameter_updates']['reference']['first_applied_s']for v in rows]
        lines.append('| '+' / '.join(key)+f' | {sum(v is not None for v in bias)}/{len(rows)} | '
            f'{fmt(median([v for v in bias if v is not None]))} | {sum(v is not None for v in ref)}/{len(rows)} | '
            f'{fmt(median([v for v in ref if v is not None]))} |')
    lines+=['','첫 갱신은 데이터 확보 시간이며 적응 완료 시간이 아니다. 실제 복귀는 처음 목표의±1mm 및 속도±0.2mm/s를5초 연속 유지한 경우만 센다. '
        '반환 시각과 미복귀(null)는 trial JSON에 남긴다. 시간은 최초 zero-command RL 진입부터이며 그 이전110개 transform_up 제어step도 Target에서 실행하고 startup 증거에 보존했다.',
        '','## 실패·미실험과 원인 분리','']
    lines+=['','### 배포 직후 센서 경로와 base-link 경로','',
        '기존 rolling odometry는 base-link 원점 이동량과 동일한 관측량이 아니다. 특히 초기 자세/leg 전환 중 기준점 이동이 크면 '
        '센서 목표 복원이 최초 base-link 위치 복원을 뜻하지 않는다. 아래는 E6의 같은 궤적에서 두 경로의 차이를 직접 계산한 값이며 '
        'slip·기구학·좌표 transport의 유일한 인과 분해는 아니다. 목표 재설정·GT 피드백·odometry 보정은 하지 않았다.','',
        '| Target | sensor−base,1초 mm | 5초 mm | 60초 mm | 180초 mm |',
        '|---|---:|---:|---:|---:|']
    gaps=json.loads((root/'observation_reference_gaps.json').read_text())['rows']
    for domain,_ in evaluated:
        chosen=[v for v in gaps if v['domain']==domain and v['arm']=='E6'and v['complete']and v['phase']in ['03_primary','06_composite_primary']]
        values=[median([s['sensor_minus_base']*1000 for v in chosen for s in v['samples']if s['t']==t])for t in [1.,5.,60.,180.]]
        lines.append('| '+domain+' | '+' | '.join(fmt(v)for v in values)+' |')
    if (root/'safety_gates.json').exists():
        for domain,v in json.loads((root/'safety_gates.json').read_text()).items():
            if not v['safe']:lines.append(f'- {domain}: Target pilot에서 **FAIL/NOT_TESTED 후속 적응** — {v["reason"]}. Shadow probing과 held-out adaptive를 강행하지 않았다.')
    if (root/'composite_gates.json').exists():
        for v in json.loads((root/'composite_gates.json').read_text())['not_tested']:lines.append(f'- {v["domain"]}: NOT_TESTED — {v["reason"]}.')
    lines+=['','질량/CoM/lag/friction 실패의 원인을 한 가지로 확정하지 않는다. 물리 guard·센서 support·입력 포화·독립 full/partial 예측·K 채택을 '
        '각각 raw 자료에 보존했다. 질량/CoM의 큰 drift와 lag50ms의 자세 guard 실패는 서로 다른 실패다. '
        '마찰 변화가 접촉 slip을 통해 영향을 줄 수 있어도 이번 static 시험은 slip 항등식 분해를 새로 수행하지 않았으므로 단일 원인을 확정하지 않는다. '
        '추가 상태·Q/R·토크 예산을 결과에 맞춰 바꾸지 않았다. '
        '동일180초의 E6/E7 차이가 없고 K도0이면 유지 입력/내부reference 보정의 효과와 dynamics/gain adaptation의 미실증을 구분해야 한다.','',
        '## 검증·재현·Sim2Real에 남은 일','',
        f'- Pipeline 상태: `{status["status"]}`. 저장된 제어 trial 수 {len(metrics)}; 시작 실패도 포함한다.','- 첫 RL1초의 의도된 crouch 높이/leg 위반은 별도 기록하고 그 이후와 구분했다. Startup finite/tilt/최저높이 guard는 처음부터 적용했다.',
        '- RLS 후보 full A/B/c와 A-frozen B/c, B2 finite-horizon은 각각 shadow 기록을 남겼다. B2 active 적용0회다.',
        '- 온라인 군은 같은 seed PRBS를 안전 gate가 허용하는 동안만 사용한다. Fixed에는 probing이 없으므로 실제 probe 에너지·drift 차이를 전체 비용에 포함했다. KOnly의 새 K가0인데 차이가 생겨도 K 적응 효과로 부르지 않는다. 새 K0회의 E6/E7은 전체 NPZ 배열 exact 비교를 수행했다.',
        '- Flash/Bias baseline의 K/reference 저장값은 비교용 nominal metadata이며 그 K가 실제 적용된 것이 아니다. 해당 baseline의 offset placeholder는 제어 효과 분석에서 제외한다.',
        '- Source-domain prior provenance, 시작부터의 배포·독립 held-out seed·물성 불변·공통 토크/goal/history/leg 경로를 검사했다.',
        '- Online support는 nominal 중심의 사전 operational half-width다. 원래 국소 train min/max와 같은 범위가 아니므로 원 train 비위치 좌표 범위 내 비율도 analysis_integrity.json에 별도로 계산했다. 넓은 operational gate 통과를 원 식별 영역의 유효성 증명으로 해석하지 않는다.',
        '- 재사용한 B1/Reference의 실채택에도 quiet window와 RLS 정보량 gate가 걸린다. 따라서 갱신0회의 결과는 이 guard를 포함한 방법의 결과이며 Bias/Reference 자체가 원리적으로 무효라는 증거가 아니다. B2는 전체 shadow이며 실채택0회다.',
        '- 이전 nominal 진입 시험은 FlashSAC8초 뒤에, 국소 시험은900초 이상 정착 뒤에 시작했다. 이번 최초 목표는 Target transform_up 뒤 첫 RL step에서 정하며 초기 전환을 포함한다. 서로 다른 시작점/seed/시간축이므로 이전 PASS를 이번 cold-start의 보장으로 사용하거나 이전 결과를 수정하지 않는다.',
        '- 단일 mismatch 수준은 개발에서 이미 고려한 값이며 제어기는 그 값/라벨을 받지 않는다. 보간 복합값과 평가 초기조건을 분리했지만, 모든 파라미터 공간의 미지 환경 일반화를 입증한 것은 아니다.',
        '- run_04는 완료한 Phase0/Safety/Shadow 뒤 관련 없는 tracked 설정의 외부 변경 감사에서 중단됐다. 보호된 실행 입력은 그대로였고 verify 함수만 수정했다. run_05의 recovery.json은 모든 physics/learner/scoring AST와 완료 자료453파일 hash 일치를 기록한다. 외부 변경은 되돌리지 않았다.',
        '- 실기 전에는 source-only prior 대조, 관측 odometry/GT 차이, 접촉/센서 noise·delay, 장시간·더 넓은 초기조건·실기 인터페이스/안전성 검증이 필요하다. Hardware/ROS 배포 없음.',
        '- Branch: `agent/codex/dev_tita_gluon`; commit/push·policy 재학습 없음. agent-check와 최종 diff/이전 hash 감사는 상위 날짜 경로의 최종 로그를 참조한다.','',
        '증거: [동결 계획](plan.json), [domain manifest](domain_manifest.json), [전체 집계](summary.json), [trial metrics](metrics.json), '
        '[CSV](metrics.csv), [학습/거부/채택 요약](learning_summary.json), [원시 episode 감사](analysis_integrity.json), [실행 로그](run.log).']
    lines+=['','독립 검증 상세: [Direct B 및 자유 예측](independent_model_checks.json), [과학 판정](scientific_decision.json), [복구 감사](recovery.json).',
        '물성/인과성 감사: [실제 시작 접촉의 마찰](contact_setting_audit.json), [과거 센서/명령만으로 추정기 복원](causal_replay_audit.json).',
        '각 domain의 trial 분포와 전체/초기/후속 지표는 `domain_metrics/`에 보존했다. 같은 초기 snapshot의 arm 반복을 독립 표본으로 세지 않는다.']
    lines+=['','다음 별도 실험에서는 초기 leg 자세 전환의 기준점 transport와 관측 경로를 먼저 검증하고, B1의 운용점 보상 신뢰도와 full A 식별 신뢰도를 분리할 수 있는지 사전에 정해야 한다. '
        '새로운 excitation/토크 예산이 필요하면 이번 결과를 유지한 독립 budget 연구로 수행한다. 실패 모델을 투영·튜닝해서 이번 gate를 소급 통과시키지 않았다.',
        '새 Target K의 정확한 식별·채택에 필요한 데이터 시간은 이번60+120초 예산에서 충족하지 못한 경우 미확정이다. 단순 첫 bias/ref 갱신 시각을 그 시간으로 대체하지 않는다.']
    lines+=['','## 변경 파일과 검사','',
        '신규 실험 코드6개: `test/static_target_domain.py`, `test/static_target_learner.py`, `test/run_static_target_adaptation.py`, '
        '`test/test_static_target_adaptation.py`, `test/analyze_static_target_adaptation.py`, `test/audit_static_target_adaptation.py`. '
        'production/runtime·훈련 설정·기존 정책/모델/보고서는 이번 코드에서 변경하지 않았다. 수집4개 source는 계획에 동결했고 파생 분석/인과성 감사 source hash는 완료 감사에 별도로 남긴다.','',
        '- [신규 불변조건 검사12개](unit_tests_final.log): 실제 실행 로그 참조.',
        '- [기존 RLS 알려진 affine/무excitation 검사2개](rls_unit_tests.log): 실제 실행 로그 참조.',
        '- [Nominal23개 배열×M4/Flash exact replay](00_exact_replay.json), [전체 센서/명령 인과성 감사](causal_replay_audit.json).',
        '- [agent-check](../agent_check.log): 기존 학습 설정의 trailing whitespace 때문에 전체 FAIL일 수 있다. Python/URDF 결과와 이번 변경의 검사는 별도로 확인한다.',
        '- [최종 변경/보호 hash/완료 감사](completion_audit.json). Hardware/commit/push 없음.','',
        '재현은 미생성 출력 폴더에 **이 실행의 승인된 계획**을 복사한 뒤 시작한다. 기본 새 계획 생성 경로는 승인 전의 엄격한 K 불허 기본값을 보존하므로, '
        '같은 프로토콜의 재현에는 아래처럼 동결 plan을 사용한다. 이미 완료한 출력에 coordinator를 덮어쓰지 않는다.','',
        '```bash',
        'export MPLCONFIGDIR=/tmp/lqr_mpl OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1',
        'mkdir docs/exp/2026-10-16/new_static_target_run',
        'cp docs/exp/2026-10-16/static_target_adaptation/run_05/{plan.json,plan.sha256,domain_manifest.json} docs/exp/2026-10-16/new_static_target_run/',
        '/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/run_static_target_adaptation.py --root docs/exp/2026-10-16/new_static_target_run --resume',
        '/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_static_target_adaptation.py --root docs/exp/2026-10-16/new_static_target_run',
        '/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/audit_static_target_adaptation.py --root docs/exp/2026-10-16/new_static_target_run --workers 3',
        './scripts/agent-check.sh','```']
    if evaluated:
        ratios=[a['E6'].get('Fixed_comparison',{}).get('IAE_ratio')for _,a in evaluated]
        ratios=[v for v in ratios if v is not None]
        balance=[d for d,a in evaluated if a['Fixed']['complete']==a['Fixed']['count']==6]
        accepted=sum(a['E7']['new_K']for _,a in evaluated)
        conclusion=['## 주요 답변','',
            '- Fixed의180초 balancing/수치 guard 완료6/6 환경: '+(', '.join(balance)or'없음')+'. 위치 유지 성공과는 별개다.',
            '- E6의 원래 base-link 위치 절대 유지6/6 환경: '+(', '.join(hold_domains)or'없음')+'.',
            f'- E6의 Fixed 대비 최대 full-IAE 감소: {fmt((1.-min(ratios))*100)if ratios else"N/A"}%. 조건별 사전10%/paired4쌍 기준은 상세 표를 따른다.',
            f'- E7의 실제 새 Target K 채택: {accepted}회. 채택이0이면 K 적응 활성 비교는NOT_TESTED이며 E6/E7의 같은 물리 결과를 K의 추가 이득으로 읽지 않는다.',
            '- 실제 bias/reference 첫 갱신 시간과5초 연속 복귀 시간은 아래에 구분했다. 새 A/B/c를 정확히 학습해 K로 채택하는 데 필요한 시간은 기준 미충족 시 미확정이다.',
            '- 질량/CoM은 큰 drift,50ms lag는 자세 guard로 후속 적응을 중단했다. 미끄럼·reference·입력 예산 중 단일 원인을 확정하지 않았다.','']
        at=lines.index('## Phase 0 — residual 없는 원래 정책');lines[at:at]=conclusion
    check=root.parent/'agent_check.log'
    if check.exists():
        text=check.read_text();details=[v.strip()for v in text.splitlines()if 'Syntax Check Results:'in v or 'XML Parse Check:'in v]
        lines+=['','실제 agent-check 최종 줄: **'+text.strip().splitlines()[-1]+'**. '+ ' '.join(details),
            '기존 `my_flat_env_cfg.py`의 trailing whitespace6곳은 이번 작업에서 수정하지 않았다. 전체 FAIL과 신규 실험 검사PASS를 합쳐 전체PASS라고 표시하지 않는다.']
    lines+=['','[c를 포함한 absolute 자유 예측의 별도 재귀 수치 교차검사](absolute_diagnostic_check.log)도 실행했다.']
    (root/'MORNING_REPORT.md').write_text('\n'.join(lines)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--partial',action='store_true')
    args=p.parse_args();analyze(args.root.resolve(),not args.partial)
