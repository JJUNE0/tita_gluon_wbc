"""DESKTOP_DRY_RUN: audit sensor-only online gain trials and report VALIDATION_SIM."""

import argparse
import csv
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from eval_online_residual_gain import REPO,ADAPTATION,WHEELS,LEGS,fit_probe_gradient,policy_config,write_json


def read_groups(root,groups):
    rows=[]
    for name,count in groups:
        folder=root/name
        complete=json.loads((folder/'completion.json').read_text())
        assert complete['episodes']==count
        rows.extend(dict(json.loads(line),folder=str(folder)) for line in (folder/'results.jsonl').read_text().splitlines())
    return rows


def stats(rows):
    complete=[r for r in rows if not r['failures']]
    result=dict(total=len(rows),completed=len(complete),failed=len(rows)-len(complete))
    for key in ('max_displacement_m','final_displacement_m','pitch_rms_rad','torque_rms_nm',
                'tail_velocity_rms_m_s','tail_path_drift_m','odometry_error_rms_m','alpha_centre_final'):
        values=[r[key] for r in complete if r[key] is not None]
        result[key]=dict(mean=float(np.mean(values)),std=float(np.std(values,ddof=1))) if values else None
    return result


def audit_trials(baseline,online):
    initial=leg=history=wheel=cost=gradient_error=prefix=0.
    replay=0
    lookup={(r['mismatch'],r['seed'],r['pitch_delta_rad'],r['label']):r for r in baseline}
    fixed={(r['mismatch'],r['seed'],r['pitch_delta_rad']):r for r in online if r['label']=='F-1'}
    for r in baseline+online:
        if r['label'].startswith('G'):
            original=fixed[(r['mismatch'],r['seed'],r['pitch_delta_rad'])]
        else:
            original=next(v for v in baseline+online if v['mismatch']==r['mismatch'] and v['seed']==r['seed'] and v['pitch_delta_rad']==r['pitch_delta_rad'])
        initial=max(initial,float(abs(np.asarray(r['initial_physics'])-original['initial_physics']).max()))
        assert not r['audit']['gt_used_for_learning'] and r['audit']['online_rls_calls']==0
        leg=max(leg,r['audit']['leg_torque_max_error_nm']);history=max(history,r['audit']['history_max_error'])
        if r.get('archive_replay'):
            replay+=1;assert max(r['archive_replay'].values())==0.
        with np.load(Path(r['folder'])/r['trace']) as trace:
            assert abs(trace['residual_total_nm']).max()<=1.+1e-9
            assert abs(np.diff(trace['residual_total_nm'])).max()<=.04+1e-9
            expected=np.clip(trace['flash_substeps'][:,:,WHEELS]+trace['residual_total_nm'][:,None,None]/2,-12.,12.)
            wheel=max(wheel,float(abs(expected-trace['command_substeps'][:,:,WHEELS]).max()))
            np.testing.assert_array_equal(trace['flash_substeps'][:,:,LEGS],trace['command_substeps'][:,:,LEGS])
            if r['label'].startswith('G'):
                assert trace['alpha'].min()>=.5-1e-9 and trace['alpha'].max()<=2.+1e-9
                assert abs(np.diff(trace['alpha'])).max()<=.005+1e-9
                for event in r['adaptation_events']:
                    if 'windows' not in event:
                        continue
                    assert abs(event['centre_after']-event['centre_before'])<=.1+1e-9
                    fitted=fit_probe_gradient(event['windows'])
                    gradient_error=max(gradient_error,abs(fitted['gradient']-event['fit']['gradient']))
                    for window in event['windows']:
                        half=(window['samples']-1)*.02/2
                        mask=(trace['time']>=window['time']-half-1e-8)&(trace['time']<=window['time']+half+1e-8)
                        assert int(mask.sum())==window['samples']
                        state=trace['state'][mask]
                        # Reproduce the controller's float32 reduction per tick;
                        # a batched reduction changes floating summation order.
                        cmd=np.asarray([float(np.sqrt(np.mean(row.astype(np.float32)[:,WHEELS]**2)))
                                        for row in trace['command_substeps'][mask]])
                        objective=ADAPTATION['objective']
                        terms=[np.mean((state[:,0]/.5)**2),np.mean((state[:,1]/.05)**2),
                            np.var(state[:,2])/.02**2,np.mean((state[:,3]/.2)**2),np.mean((cmd/.5)**2)]
                        cost=max(cost,abs(float(np.asarray(terms) @ objective['weights'])-window['cost']))
                with np.load(Path(original['folder'])/original['trace']) as ref:
                    n=min(len(trace['time']),201)
                    for key in ('state','policy_observation','policy_action','motor_substeps','gt_position'):
                        prefix=max(prefix,float(abs(trace[key][:n]-ref[key][:n]).max()))
            elif r['requested_s']==60.:
                condition='nominal' if r['mismatch']=='step_gain_0.8' else r['mismatch']
                refrow=lookup[(condition,r['seed'],r['pitch_delta_rad'],r['label'])]
                with np.load(Path(refrow['folder'])/refrow['trace']) as ref:
                    n=len(ref['time'])
                    for key in ('state','sensor_state','policy_action','motor_substeps','gt_position'):
                        prefix=max(prefix,float(abs(trace[key][:n]-ref[key]).max()))
    assert initial==leg==history==gradient_error==prefix==0. and wheel<1e-6 and cost<1e-9, dict(
        initial=initial,leg=leg,history=history,gradient=gradient_error,prefix=prefix,wheel=wheel,cost=cost)
    return dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',episodes=len(baseline+online),
        archive_exact_replays=replay,initial_error=initial,leg_torque_error_nm=leg,history_error=history,
        wheel_addition_error_nm=wheel,window_cost_reconstruction_error=cost,
        gradient_reconstruction_error=gradient_error,shared_prefix_error=prefix,
        learning_inputs='encoder/IMU and pre-mismatch commanded torque; GT arrays evaluation only')


def paired_comparison(rows):
    summary=[]
    for condition in dict.fromkeys(r['mismatch'] for r in rows):
        modes={mode:stats([r for r in rows if r['mismatch']==condition and r['label']==mode]) for mode in ('A','F-1','G')}
        f={(r['seed'],r['pitch_delta_rad']):r for r in rows if r['mismatch']==condition and r['label']=='F-1'}
        g=[r for r in rows if r['mismatch']==condition and r['label']=='G']
        pairs=[(f[(r['seed'],r['pitch_delta_rad'])],r) for r in g if not r['failures'] and not f[(r['seed'],r['pitch_delta_rad'])]['failures']]
        differences=np.array([b['max_displacement_m']-a['max_displacement_m'] for a,b in pairs])
        ratios=np.array([b['max_displacement_m']/a['max_displacement_m'] for a,b in pairs])
        summary.append(dict(mismatch=condition,modes=modes,paired_completed=len(pairs),
            improved_pairs=int(sum(differences<0.)),mean_drift_change_m=float(differences.mean()) if len(pairs) else None,
            mean_drift_change_percent=float((ratios.mean()-1)*100) if len(pairs) else None,
            accepted_updates=sum(r['accepted_updates'] for r in g),rejected_updates=sum(r['rejected_updates'] for r in g),
            guard_events=sum(r['guard_events'] for r in g),
            alpha_centres=[r['alpha_centre_final'] for r in g]))
    return summary


def write_report(root,report,baseline,online,probes,comparisons,audit):
    policy=policy_config()
    stat=lambda condition,label,rows:stats([r for r in rows if r['mismatch']==condition and r['label']==label])
    average=lambda s,key:s[key]['mean'] if s[key] else None
    nominal=average(stat('nominal','F-1',baseline),'max_displacement_m')
    severe=[m for m in ('mass_1.15','mass_1.30','gain_0.8','gain_1.2','lag_0.02','lag_0.05','friction_0.2','friction_0.8')
            if average(stat(m,'F-1',baseline),'max_displacement_m')>nominal*1.2]
    by_name={c['mismatch']:c for c in comparisons}
    lines=['# G — Online Adaptive Residual Feedback Control', '',
        'Execution Domain: VALIDATION_SIM (소스·경로·무결성 검사: DESKTOP_DRY_RUN)', '',
        f'Policy Checkpoint SHA256: `{policy["policy_interface"]["checkpoint_sha256"]}`', '',
        f'ONNX SHA256: `{policy["policy_interface"]["onnx_sha256"]}`', '',
        'Evidence Status: SUSPICIOUS — G의 강건성 개선은 조건별 효과와 탐색 대조를 함께 해석해야 한다. PASS — 실행·경로 무결성. 아래 표는 실제 완료/실패와 paired 성능을 구분한다.', '',
        'Observed Metrics / Behavior / Log Summary:', '',
        '**고정 F-1의 mismatch baseline을 먼저 측정한 뒤, 제한된 단일 α를 온라인 조정하는 G를 같은 초기 조건에서 비교했다.** '
        '이 알고리즘은 gain 최적화이며 Online Dynamics Identification 또는 Adaptive LQR이 아니다. k_p/k_v 두 계수 학습이나 RLS/LQR 모델 갱신은 수행하지 않았다.', '',
        '## Phase 2 — 12초 Dynamics Mismatch Baseline', '',
        '기존 9조건 × 9초기조건 × A/F-1 = 162 episodes. 전 조건에서 두 군 모두 9/9 완료했다. '
        '기존 A 81회와 nominal F-1 9회는 archive의 physics substep 토크 및 상태를 정확히 재현했다.', '',
        '| 조건 | A 최대 drift 평균 m | F-1 최대 drift 평균 m | F-1 nominal 대비 |',
        '|---|---:|---:|---:|']
    for name in dict.fromkeys(r['mismatch'] for r in baseline):
        a=stat(name,'A',baseline);f=stat(name,'F-1',baseline)
        drift=average(f,'max_displacement_m')
        lines.append(f'| {name} | {average(a,"max_displacement_m"):.4f} | {drift:.4f} | {(drift/nominal-1)*100:+.1f}% |')
    lines+=['',f'Nominal 대비 20% 이상 drift가 악화된 조건은 {", ".join(severe)}였다. '
        '이 20%는 추가 분석 기준이며 사용자 요구 사양이 아니다. Motor gain 0.8은 12초에서 nominal보다 drift가 작았다. '
        '따라서 motor gain 감소가 반드시 이 horizon의 성능을 저하시킨다고 가정할 수 없다. Lag 50 ms에서는 F-1이 A보다 drift가 컸다.', '',
        '## Phase 3 — G의 학습 규칙과 제한', '',
        '- Base residual은 기존 F-1의 −2e_p−0.5v이다. p_hold=episode 시작 encoder 경로 0을 고정하고 encoder+현재 시점의 IMU로 p/v를 계산한다. Actor는 기존 A의 cache·33-value observation·전체 raw 8-action history를 유지한다.',
        '- α 중심값은 1에서 시작하며 [0.5,2]에 제한한다. ±0.1 탐색을 ABBA 다음 BAAB 순서로 적용한다. 각 block은 3초이며 앞 1초는 평가에서 제외하고 나머지 2초의 센서 cost를 평가한다. 시작은 4초 이후다. 초기 3초의 외란 구간을 피해 학습한다.',
        '- 8 blocks(24초) 후에만 중심값을 최대 0.1 갱신한다. 실제 α dose와 비용의 관계를 회귀하면서 constant/linear/quadratic 시간 추세를 nuisance 항으로 제거한다. |gradient|>2×회귀 표준오차이고 예상 탐색 효과가 평균 cost의 0.5%보다 클 때만 갱신한다. 불확실하면 유지한다. 이 표준오차는 직렬 상관이 있는 폐루프 데이터의 휴리스틱이며 통계적 인과 보증은 아니다.',
        '- α 변화율도 0.25/s로 제한한다. α가 1을 넘어도 적용 residual 합 토크는 반드시 ±1 Nm(바퀴당 ±0.5 Nm)로 제한하고, 기존 1초 smoothstep ramp·합 토크 slew 2 Nm/s·기존 최종 actuator saturation을 유지한다. Alpha를 키워도 토크 한도를 늘리지 않는다.',
        '- |pitch error|>0.25 rad, |pitch rate|>1 rad/s 또는 |encoder forward velocity|>0.5 m/s이면 탐색/평가를 중단하고 중심값을 1로 복귀시키며 4초 cooldown 후 다시 시작한다. 복귀 α와 torque도 slew를 거친다. 이는 학습 guard이고 로봇 하드웨어 안전 제어기의 구현이 아니다.',
        '- Cost는 mean[(p/0.5)²]+mean[(v/0.05)²]+0.25×var(pitch)/0.02²+0.05×mean[(pitch_rate/0.2)²]+0.02×mean[(command_wheel_RMS/0.5)²]이다. 위치·속도·자세 센서 및 기존 제어 명령만 사용한다. 실제 motor gain/lag, true root position/velocity, GT drift, mismatch 이름은 optimizer에 전달하지 않는다. 토크 사용량 항은 gain/lag를 적용하기 전 명령 토크이며 실측 motor torque라고 부르지 않는다.',
        '- FlashSAC wheel PD 토크는 매 physics step 그대로 계산하고 residual만 더한다. Leg torque와 last_action 의미를 바꾸지 않는다. Learned α는 torque 생성에만 쓰고 observation history에 넣지 않는다.', '',
        '## 동일 60초 A/F-1/G 비교', '',
        '기존 12초와 60초 drift를 직접 성능 비교하지 않는다. 60초는 이 보수적인 업데이트 규칙의 두 평가 주기(기본 28/52초)를 확보하기 위해 사용했다. '
        '9 static conditions × 9초기조건 × 3군 = 243회, 20초에 motor gain을 1.0→0.8로 바꾸는 추가 조건 27회다. '
        '변화 시각·gain은 motor 모델에만 적용하고 optimizer에는 알려주지 않았다.', '',
        '| 조건 | 완료 A/F-1/G | A drift m | F-1 drift m | G drift m | G−F-1 paired 변화 | 개선 쌍 | G accepted/guard |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for c in comparisons:
        modes=c['modes'];number=lambda label:f'{modes[label]["max_displacement_m"]["mean"]:.4f}' if modes[label]['max_displacement_m'] else 'N/A'
        completed='/'.join(str(modes[label]['completed']) for label in ('A','F-1','G'))
        percent=f'{c["mean_drift_change_percent"]:+.2f}%' if c['mean_drift_change_percent'] is not None else 'N/A'
        lines.append(f'| {c["mismatch"]} | {completed} (각 9) | {number("A")} | {number("F-1")} | {number("G")} | {percent} | '
            f'{c["improved_pairs"]}/{c["paired_completed"]} | {c["accepted_updates"]}/{c["guard_events"]} |')
    lines+=['',
        'Drift는 기존 평가와 같은 cached world axle의 최대 planar displacement이며, sensor input은 synchronized state다. '
        '표의 drift 평균은 완료 trial만 포함하고 paired 변화는 두 군 모두 완료한 동일 seed/pitch끼리 계산한다. '
        '완료 수가 9보다 적으면 survivor 평균만으로 개선이라고 판단하지 않는다. 평균±sample SD, final drift, tail 12초 속도/encoder path drift, odometry error는 paired_comparisons.json/metrics.csv에 있다.', '',
        '| 조건 | G/F-1 Pitch RMS 비 | G/F-1 실제 wheel torque RMS 비 | G α 중심값 범위 |',
        '|---|---:|---:|---:|']
    for c in comparisons:
        f=c['modes']['F-1'];g=c['modes']['G']
        ratio=lambda key:f'{g[key]["mean"]/f[key]["mean"]:.4f}' if g[key] and f[key] else 'N/A'
        lines.append(f'| {c["mismatch"]} | {ratio("pitch_rms_rad")} | {ratio("torque_rms_nm")} | '
            f'{min(c["alpha_centres"]):.2f}–{max(c["alpha_centres"]):.2f} |')
    lines+=['','## 탐색만 유지한 대조 진단', '',
        '주 비교군 A/F-1/G와 별도로 nominal, mass_1.15, gain_0.8, step_gain_0.8의 각 9초기조건에서 G-probe를 실행했다(36회). '
        'G와 같은 탐색·guard·cost 계산을 유지하되 centre_step=0으로 α 중심값을 1에 고정했다. '
        'G 대 F-1 차이에 gain 학습과 탐색 효과가 섞이는 것을 확인하는 진단이다.', '',
        '| 조건 | F-1 drift m | G-probe drift m | G drift m | G−G-probe 평균 drift m |',
        '|---|---:|---:|---:|---:|']
    control_summary=[]
    for name in dict.fromkeys(r['mismatch'] for r in probes):
        probe=stat(name,'G-probe',probes);c=by_name[name]
        p=average(probe,'max_displacement_m');g=average(c['modes']['G'],'max_displacement_m');f=average(c['modes']['F-1'],'max_displacement_m')
        lines.append(f'| {name} | {f:.4f} | {p:.4f} | {g:.4f} | {g-p:+.5f} |')
        control_summary.append(dict(mismatch=name,probe=probe,gain_learning_delta_m=g-p))
    write_json(root/'probe_control_comparison.json',control_summary)
    report.write_text('\n'.join(lines)+'\n')
    append_conclusion_and_plot(root,report,baseline,online,probes,comparisons,audit,control_summary)


def append_conclusion_and_plot(root,report,baseline,online,probes,comparisons,audit,control_summary):
    meaningful=[]
    for c in comparisons:
        f=c['modes']['F-1'];g=c['modes']['G']
        if g['completed']==9 and c['mean_drift_change_percent']<=-5. and c['improved_pairs']>=7 and (
            g['pitch_rms_rad']['mean']<=1.10*f['pitch_rms_rad']['mean'] and
            g['torque_rms_nm']['mean']<=1.25*f['torque_rms_nm']['mean']):
            meaningful.append(c['mismatch'])
    if not meaningful:
        text=report.read_text().replace(
            'Evidence Status: SUSPICIOUS — G의 강건성 개선은 조건별 효과와 탐색 대조를 함께 해석해야 한다. PASS — 실행·경로 무결성. 아래 표는 실제 완료/실패와 paired 성능을 구분한다.',
            'Evidence Status: FAIL — 현재 G의 고정 F-1 대비 실용적인 강건성 회복 목표. PASS — 전 실험 완료·구현 무결성. SUSPICIOUS — 일부 조건의 소폭 개선과 gain 효과 해석.')
        text=text.replace('**고정 F-1의 mismatch baseline을 먼저 측정한 뒤, 제한된 단일 α를 온라인 조정하는 G를 같은 초기 조건에서 비교했다.**',
            '**현재 G는 고정 F-1보다 mismatch에 더 강건하다는 근거를 확보하지 못했다.** 고정 F-1의 baseline을 먼저 측정하고 제한된 단일 α를 온라인 조정했으나, 주요 악화 조건의 drift를 회복하지 못했다.')
        report.write_text(text)
    write_json(root/'practical_success.json',dict(execution_domain='VALIDATION_SIM',
        evidence_status='PASS' if meaningful else 'FAIL',qualifying_conditions=meaningful,
        criterion='G 9/9 complete; >=5% paired mean drift decrease and >=7/9 improving pairs; '
            'mean pitch <=110%, wheel torque <=125%; exploratory reporting threshold, not user specification'))
    lag=next(c for c in comparisons if c['mismatch']=='lag_0.05')
    fractions=[]
    for r in online:
        if r['label']!='G':
            continue
        with np.load(Path(r['folder'])/r['trace']) as trace:
            fractions.append(dict(mismatch=r['mismatch'],seed=r['seed'],pitch=r['pitch_delta_rad'],
                residual_limit_fraction=float(np.mean(abs(trace['residual_total_nm'][1:])>=1.-1e-6))))
    write_json(root/'residual_limit_fractions.json',fractions)
    unitlog=(root/'unit_tests_final.log').read_text()
    unit_status='PASS' if '\nOK\n' in unitlog else 'FAIL'
    checklog=root/'agent_check.log'
    check_status='PASS' if checklog.exists() and checklog.read_text().rstrip().endswith('PASS') else 'NOT_TESTED'
    lines=['','## 해석 및 다음 단계 판단', '',
        f'이번 분석에서 실용적인 추가 개선 기준(9/9 완료, paired 평균 drift ≥5% 감소, ≥7/9쌍 개선, '
        f'평균 pitch RMS ≤110%, wheel RMS ≤125%)을 충족한 조건: {", ".join(meaningful) if meaningful else "없음"}. '
        '5%/7쌍 및 허용 비율은 결과를 과장하지 않기 위한 보고 기준이며 사용자 지정 기준이 아니다. '
        '작은 음의 paired 차이는 raw metric 개선으로 남기되 강건성 회복 성공과 동일하게 취급하지 않는다.', '',
        f'특히 50 ms lag에서 G의 accepted updates 합계는 {lag["accepted_updates"]}, guard activation events 합계는 {lag["guard_events"]}였다. '
        '반복되는 센서 guard가 평가 창과 cooldown을 재설정해 탐색/학습이 진행되지 않았다. 실제 α와 residual 및 물리 궤적도 F-1과 같았다. '
        '안정적으로 넘어지지 않는 것과 drift 복구는 서로 다른 결과다.', '',
        'Residual hard cap 때문에 α 증가가 사용할 수 있는 최대 보정 토크를 늘리지는 않는다. '
        '포화 비율은 residual_limit_fractions.json에 기록했다. 탐색 구간의 비용 gradient와 전체 episode의 최대 GT planar drift는 서로 다른 목표이며 '
        'gain 변화가 센서 cost를 줄여도 GT 2D 위치 유지가 보장되지는 않는다. Encoder 경로에는 yaw/slip 및 추정 오차가 남는다.', '',
        'ABBA/BAAB와 quadratic time trend를 사용해 단순한 시간 감소를 학습 효과로 해석하는 오류를 줄였지만, '
        '상태 carry-over, 동역학 변화 중의 비선형 추세, 비용 window의 직렬 상관은 완전히 분리하지 못한다. '
        'G-probe 대조도 탐색 순서 하나의 국소 진단이다. Gain 학습이 유익하다는 주장은 G/F-1만 아니라 G/G-probe와 함께 판단해야 한다.', '',
        '단일 α 검증에서 고정 F-1보다 분명한 강건성 회복 근거가 확보되지 않으면 k_p/k_v 두 계수로 확대하거나 '
        'Online Dynamics Identification/LQR로 돌아가지 않는다. 이번 실험은 두 계수 적응을 구현하지 않았다: NOT_TESTED.', '',
        '## Phase 4 — Sim2Real 준비 상태', '',
        '현재 결과만으로 실제 TITA 온라인 적응 실행의 근거가 충분하다고 판단하지 않는다. Hardware 명령·배포는 수행하지 않았다. '
        '실기 준비에서 필요한 항목은 encoder/IMU timestamp 정렬, wheel torque/current 단위와 축 부호, '
        '기존 velocity PD에 residual을 더할 수 있는 인터페이스, command saturation/rate limit 확인이다. '
        '이 항목의 실기 검증은 NOT_TESTED이며 본 결과는 시뮬레이터 검증에 한정한다.', '',
        '## 실행·무결성·변경 범위', '',
        f'- 본 결과: 12초 baseline 162 + 60초 A/F-1/G 270 + G-probe 36 = {audit["episodes"]} episodes. '
        'Smoke와 단위 검사 rollouts는 주 결과에서 제외한다. 같은 3 seeds×3 pitch, grounded pose/initial velocity, '
        'physics/control dt=0.005/0.02초, 기존 3초의 12 N/0.1초 외란을 유지했다.',
        f'- Integrity PASS: archive {audit["archive_exact_replays"]}회 정확 재현; 60초 A/F-1의 12초 baseline prefix 및 '
        'G의 탐색 전 4초 prefix 정확 일치. Initial state·leg torque·history·gradient 오차 0. '
        f'wheel 합산 최대 오차 {audit["wheel_addition_error_nm"]:.3g} Nm(float32), 센서 window cost 재구성 최대 오차 '
        f'{audit["window_cost_reconstruction_error"]:.3g}. GT 배열은 평가에만 사용했다.',
        f'- Unit tests {unit_status} (5개): 시간 추세와 실제 probe gradient 분리, 무효과 비용의 갱신 거부/guard, '
        '적응 비활성 G와 F-1의 실제 mismatch rollout 정확 동등성. 추가 hard-bound 검사는 unit_tests_final.log를 참조한다.',
        '- 초기 guard 카운터가 시작 전/cooldown 중의 활성화를 누락하는 로깅 문제를 발견해 latch만 수정했다. '
        '제어 계산은 변경하지 않았다. 모든 G/G-probe 126회 저장 센서·명령을 새 코드로 재입력하여 적용 α·중심값·accepted/rejected가 '
        '전체 tick에서 정확히 동일함을 확인했다(guard_sensor_replay.json). 원본 simulation results/NPZ/source snapshot은 보존하고 '
        '표의 guard 횟수만 sensor replay로 보정했다. 본 수정 후 468회 전체를 물리 재실행한 것으로 주장하지 않는다.',
        '- 초기 report_generation*.log의 분석 실패는 NumPy window indexing 및 float32 토크 RMS의 batched reduction 반올림 차이였다. '
        '명령 RMS를 제어기와 같은 per-tick 순서로 재구성해 수정했고, 최종 window cost 재구성 오차는 0이다. 실험 데이터는 변경하지 않았다.',
        f'- ./scripts/agent-check.sh {check_status}: agent_check.log. 최종 diff 및 기존 hash/Git 상태 보존 기록: final_review.json/task.diff.',
        '- 기존 소스/설정/보고서는 수정하지 않았다. 신규 test/eval_online_residual_gain.py, '
        'test/eval_online_residual_probe_control.py, test/test_online_residual_gain.py, '
        'test/analyze_online_residual_gain.py, test/audit_online_residual_sensor_replay.py와 본 날짜의 결과만 추가했다.',
        '- 브랜치: agent/codex/dev_tita_gluon. Actor checkpoint는 동일한 model_100000이며 재학습·RLS·LQR gain 갱신 없음.',
        '- 초기 조건은 9개 결정론적 조합이며 세 seeds 아래 pitch 3개가 묶여 있다. 9개 독립 무작위 표본으로 해석하지 않는다. '
        'Longer horizon·다른 지형/명령·센서 잡음·실제 하드웨어 강건성은 NOT_TESTED.', '',
        '## 재현', '',
        '```bash',
        'PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_online_residual_gain.py',
        'PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase baseline --conditions nominal mass_1.15 mass_1.30 --output docs/exp/2026-10-15/new_gain/baseline_mass',
        'PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase baseline --conditions gain_0.8 gain_1.2 lag_0.02 --output docs/exp/2026-10-15/new_gain/baseline_motor',
        'PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase baseline --conditions lag_0.05 friction_0.2 friction_0.8 --output docs/exp/2026-10-15/new_gain/baseline_contact',
        'PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase online --conditions nominal mass_1.15 mass_1.30 --output docs/exp/2026-10-15/new_gain/online_mass',
        'PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase online --conditions gain_0.8 gain_1.2 lag_0.02 --output docs/exp/2026-10-15/new_gain/online_motor',
        'PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase online --conditions lag_0.05 friction_0.2 friction_0.8 --output docs/exp/2026-10-15/new_gain/online_contact',
        'PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase online --conditions step_gain_0.8 --output docs/exp/2026-10-15/new_gain/online_step',
        '```', '',
        '이번 실행은 baseline을 baseline_mass/baseline_motor/baseline_contact 3묶음, '
        'online을 online_mass/online_motor/online_contact/online_step로 나누어 독립 프로세스로 실행했다. '
        '모든 실제 argv 대응 conditions/duration/source hash는 각 manifest.json, 실행 당시 source는 runner_source.txt에 있다. '
        '분석기는 동일한 폴더 이름을 요구한다.', '',
        '```bash',
        'PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_probe_control.py --output docs/exp/2026-10-15/new_gain/probe_control',
        'PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/audit_online_residual_sensor_replay.py --root docs/exp/2026-10-15/new_gain',
        'PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_online_residual_gain.py --root docs/exp/2026-10-15/new_gain --report docs/exp/2026-10-15/new_gain_summary.md',
        './scripts/agent-check.sh', '```', '',
        f'산출물: [{root.name}/comparison.png]({root.name}/comparison.png), metrics.csv, paired_comparisons.json, '
        'probe_control_comparison.json, practical_success.json, adaptation_events.json, integrity.json, 각 episode NPZ 및 manifest/results.jsonl.']
    with report.open('a') as stream:
        stream.write('\n'.join(lines)+'\n')
    conditions=('nominal','mass_1.15','lag_0.05','step_gain_0.8')
    fig,axes=plt.subplots(3,4,figsize=(17,10),sharex=True)
    for col,condition in enumerate(conditions):
        axes[0,col].set_title(condition)
        for label in ('A','F-1','G','G-probe'):
            candidates=[r for r in online+probes if r['mismatch']==condition and r['label']==label and r['seed']==42 and r['pitch_delta_rad']==0.]
            if not candidates:
                continue
            with np.load(Path(candidates[0]['folder'])/candidates[0]['trace']) as trace:
                d=trace['gt_position'][:,:2]-trace['gt_position'][0,:2]
                axes[0,col].plot(trace['time'],np.linalg.norm(d,axis=1),label=label)
                axes[1,col].plot(trace['time'],trace['sensor_state'][:,2],label=label)
                if label.startswith('G'):
                    axes[2,col].plot(trace['time'],trace['alpha'],label=label+' applied',alpha=.65)
                    axes[2,col].plot(trace['time'],trace['alpha_centre'],label=label+' centre')
        for row in range(3):
            axes[row,col].grid(alpha=.3)
            if condition=='step_gain_0.8':axes[row,col].axvline(20.,ls='--',color='grey',alpha=.5)
        axes[2,col].set_xlabel('Time [s]')
    for row,label in enumerate(('Planar drift [m]','Pitch error [rad]','Alpha')):axes[row,0].set_ylabel(label)
    axes[0,0].legend();axes[2,0].legend(fontsize=7)
    fig.tight_layout();fig.savefig(root/'comparison.png',dpi=170);plt.close(fig)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args();root=args.root.resolve();report=args.report.resolve()
    assert root.is_relative_to(REPO/'docs/exp') and report.is_relative_to(REPO/'docs/exp')
    baseline=read_groups(root,[('baseline_mass',54),('baseline_motor',54),('baseline_contact',54)])
    online=read_groups(root,[('online_mass',81),('online_motor',81),('online_contact',81),('online_step',27)])
    probes=read_groups(root,[('probe_control',36)])
    replay=json.loads((root/'guard_sensor_replay.json').read_text())
    assert replay['evidence_status']=='PASS' and replay['episodes']==126 and replay['alpha_centre_update_max_error']==0.
    corrected={(r['folder'],r['trace']):r for r in replay['results']}
    for r in online+probes:
        if not r['label'].startswith('G'):
            continue
        correction=corrected[(Path(r['folder']).name,r['trace'])]
        r['original_guard_events']=r['guard_events']
        r['guard_events']=correction['guard_events']
        r['guard_active_fraction']=correction['guard_active_fraction']
        r['adaptation_events']=[e for e in r['adaptation_events'] if e['reason']!='sensor_guard']+correction['guard_activation_events']
    audit=audit_trials(baseline,online+probes);write_json(root/'integrity.json',audit)
    comparisons=paired_comparison(online);write_json(root/'paired_comparisons.json',comparisons)
    fields=['mismatch','label','seed','pitch_delta_rad','requested_s','completed_s','failures',
        'max_displacement_m','pitch_rms_rad','torque_rms_nm','command_torque_rms_nm',
        'tail_velocity_rms_m_s','tail_path_drift_m','alpha_centre_final','accepted_updates','rejected_updates','guard_events']
    with (root/'metrics.csv').open('w') as stream:
        writer=csv.DictWriter(stream,fields,extrasaction='ignore');writer.writeheader();writer.writerows(baseline+online+probes)
    events=[dict(mismatch=r['mismatch'],seed=r['seed'],pitch=r['pitch_delta_rad'],**event) for r in online if r['label']=='G' for event in r['adaptation_events']]
    write_json(root/'adaptation_events.json',events)
    write_report(root,report,baseline,online,probes,comparisons,audit)
    print('[DESKTOP_DRY_RUN] PASS integrity',audit)
    for c in comparisons:
        print('[VALIDATION_SIM]',c['mismatch'],'change%',c['mean_drift_change_percent'],'improved',c['improved_pairs'],
            'updates',c['accepted_updates'],'guards',c['guard_events'])


if __name__=='__main__':
    main()
