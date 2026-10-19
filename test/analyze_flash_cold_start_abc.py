"""DESKTOP_DRY_RUN: A/B/C evidence analysis; never activates an estimator/gain."""
import argparse
from collections import Counter,defaultdict
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from flash_cold_start_abc import verify,write,sha256


def med(values):return None if not values else float(np.median(values))
def fmt(value):return 'N/A'if value is None else f'{value:.5g}'


def analyze(root):
    plan=verify(root,full=True);A=json.loads((root/'A_results.json').read_text())['rows'];B=json.loads((root/'B_results.json').read_text())['rows']
    comparison=json.loads((root/'C_comparison.json').read_text())['rows'];lines=[
        '# model_60000 — Cold-start 위치·입력 정보량·Target Offline 식별 A/B/C','',
        '작성일: 2026-10-16 (Asia/Seoul)','',
        'Execution Domain: **VALIDATION_SIM** (분석: **DESKTOP_DRY_RUN**)','',
        'Policy Checkpoint SHA256: `'+plan['policy_sha256']+'`','',
        'Evidence Status: 단계별 PASS/FAIL/NOT_TESTED를 아래에 구분한다. 새 제어기·gain·GT 피드백·Phase D/E/F는 **NOT_TESTED**.','',
        'Observed Metrics / Behavior / Log Summary:','',
        '기존 run_05 전체 증거와 source를 보호했다. A는 원래 입력의 exact replay이고 센서 FK 보정은 오프라인 진단값이다. '
        'C의 Target은 첫 physics 이전에 설정하고 종료까지 고정했다. Offline 모델은 진단용으로만 저장했으며 제어에는 사용하지 않았다.','',
        '## Phase A — 기준점 이동과 센서만의 보정','',
        '`p_base_diagnostic = p_encoder − sum[delta(R_IMU*d_FK(q)) dot f_mid]`. '
        '관절각과 IMU만 사용하는 함수이며 GT는 결과 검증에만 사용한다. leg·roll/pitch·yaw 항의 합은 대칭 곱 분해로 각20ms 구간에서 정확히 닫힌다. '
        '속도는 gyro×offset 및 leg FK Jacobian 항을 원래 rolling 속도에서 뺀다.','',
        '| Target | 군 | 시각 s | 기존 sensor−base mm | 보정 후 mm | leg mm | roll/pitch mm | yaw mm |',
        '|---|---|---:|---:|---:|---:|---:|---:|']
    groups=defaultdict(list)
    for case in A:
        for row in case['rows']:
            for check in row['checks']:groups[(case['job']['job']['domain'],row['arm'],check['t'])].append(check)
    afacts=[]
    for (domain,arm,t),rows in groups.items():
        vals={key:med([r[key]*1000 for r in rows])for key in ['original_gap','corrected_gap','leg','tilt','yaw','transport_GT','rolling_remainder']}
        afacts.append(dict(domain=domain,arm=arm,t=t,**vals))
        if arm=='Fixed':lines.append(f'| {domain} | {arm} | {t:g} | '+' | '.join(fmt(vals[k])for k in ['original_gap','corrected_gap','leg','tilt','yaw'])+' |')
    lines+=['','transform_up 중에는 원래 runtime odometry가 아직 초기화되지 않았다. 저장된 startup qpos/qvel로 복원한 센서 odometry는 '
        '**별도 오프라인 stream**이며 기존 RL 목표에 이어 붙이지 않았다. 첫 기록은 startup 첫20ms 후이며 그 이전 이동을 측정했다고 주장하지 않는다. '
        '보정 후 남은 오차는 기존 encoder와 wheel midpoint의 차이 및 FK/이산화 오차다. 이를 전부 slip이라고 부르거나 base GT 유지 해결로 일반화하지 않는다.','',
        '## Phase B — 포화 제외와 정보량','',
        'raw feedback, probe, bias를 합친 pre_global_clip → absolute band/ramp/slew 후 requested → native wheel clipping 후 actual_u를 구분했다. '
        '`actual_u`는 알려진 software 추가 명령이다. gain/lag 이후의 physical_motor는 FlashSAC를 포함한 전체 토크이며 분리된 실제 residual로 취급하지 않는다.','',
        '| Stage / Target / 군 | 필터 | transition 중앙값 | rank | condition | innovation % | B 오차 %, 검증 가능한 경우 |',
        '|---|---|---:|---:|---:|---:|---:|']
    bgroups=defaultdict(list)
    for row in B:
        for r in row['rows']:bgroups[(row['phase'],row['domain'],row['arm'],r['mask'])].append(r)
    for (phase,domain,arm,mask),rows in bgroups.items():
        vals=[med([r['information'][k]for r in rows if r['information'].get(k)is not None])for k in ['samples','rank','condition','innovation']]
        if vals[3]is not None:vals[3]*=100
        be=med([r['B_relative_error']*100 for r in rows if r['B_relative_error']is not None])
        lines.append(f'| {phase}/{domain}/{arm} | {mask} | '+' | '.join(fmt(v)for v in vals+[be])+' |')
    lines+=['','`all_after1s`와`unsaturated_after1s`는 같은 시간 기준이다. deployed_eligibility는 실제 과거 learner의 필터와 일치함을 A/B/c로 재검사했다. '
        '포화 제거는 표본과 excitation도 제거할 수 있어 condition이 반드시 좋아지는 것은 아니다. Direct B가 없는 환경의 B 정확도는NOT_TESTED다.','',
        '## Phase C — 같은 데이터의 Offline LS와 RLS','',
        '학습 seed720/721/722, 검증 seed730/731×3pitch는 분리했다. 모든 모델은 test 수집 전에 동결했다. '
        '제어는 원래 FlashSAC+0.4828Nm bias와 안전한0.01Nm 입력만 사용한다. LQR/Reference/Bias 갱신은 없다. '
        '같은 train stream의1–60초와10–60초를 사전 구분했고 p 목표나 회귀 중심을 재설정하지 않았다. '
        '주 판정은10–60초 학습, 독립60초 snapshot6개의 결과다.10초 snapshot은 과도 영역 진단이다.','',
        '| Target | 모델 | 60초 예측 PASS/6 | 정보 gate | paired2초 p/v NRMSE % | absolute 첫2초 p/v NRMSE % | Direct B 오차 % |',
        '|---|---|---:|---|---:|---:|---:|']
    cgroups=defaultdict(list)
    for row in comparison:cgroups[(row['domain'],row['model'],row['snapshot_s'])].append(row)
    verdicts={}
    for (domain,model,t),rows in cgroups.items():
        if t!=60.:continue
        passed=sum(r['prediction_gate']for r in rows);ig=all(r['information_gate']for r in rows)
        verdicts.setdefault(domain,{})[model]=dict(pass_count=passed,total=len(rows),prediction_gate=passed==6 and len(rows)==6,information_gate=ig)
        def pair(key):
            data=[r[key]for r in rows];return data
        pv=[r['paired']['prediction']['horizons']['100']['nrmse']for r in rows]
        av=[r['absolute']['first2s_NRMSE']for r in rows]
        safe_med=lambda data:' / '.join(fmt(med([x[i]*100 for x in data if x[i]is not None]))for i in range(2))
        lines.append(f'| {domain} | {model} | {passed}/{len(rows)} | {"PASS"if ig else"FAIL"} | {safe_med(pv)} | {safe_med(av)} | '
            f'{fmt(med([r["paired"]["B_relative_error"]*100 for r in rows]))} |')
    lines+=['','각 snapshot은 paired 응답·c를 포함한 absolute 예측·baseline·Direct B를 모두 통과해야 예측PASS다. '
        '정보량은 별도 gate이며 예측이 좋아도 정보 gate 미달이면 온라인 K로 넘어갈 근거로 사용하지 않는다. '
        '정보량이 부족한데 Offline/RLS 모두FAIL이라고 해서 상태 표현이 원인이라고 확정하지 않는다.','',
        '| Target | post Offline LS | post RLS | 해석 |','|---|---|---|---|']
    for domain in [d['name']for d in plan['domains']]:
        v=verdicts.get(domain,{});ls=v.get('post_LS',{}).get('prediction_gate',False);rls=v.get('post_RLS',{}).get('prediction_gate',False)
        interpretation='둘 다PASS: 정보/영역 검증 뒤 Phase D 후보'if ls and rls else('Offline PASS/RLS FAIL: 온라인 방법·유효 표본 우선'if ls else('RLS PASS/Offline FAIL: prior/regularization·batch conditioning 재검토'if rls else'둘 다FAIL/미실험: 정보·영역·모델 가정을 분리해 재검토'))
        lines.append(f'| {domain} | {"PASS"if ls else"FAIL/NOT_TESTED"} | {"PASS"if rls else"FAIL/NOT_TESTED"} | {interpretation} |')
    lines+=['','## 별도 probing/토크 예산 계획','',
        '이번 예산은 기존0.4328–0.5328Nm·2Nm/s·wheel±12Nm 그대로다. 늘리지 않았다. '
        '다음 연구는 안전한 target에서 bounded 입력의 진폭/지속시간을 따로 등록하고, 원래 예산 대조군을 남겨 정보 rank/condition/innovation와 물리 drift를 함께 평가해야 한다. '
        '상태 guard/clip 발생 시 excitation 중단, 더 큰 예산은 개발 seed의 별도 pilot·operator 검토 후 독립 manifest로만 수행한다. '
        '이번 데이터에서 실패한 모델의 Q/R·상태·threshold를 바꾸지 않았다.','',
        '## 검증·보존·범위','',
        'Phase A의 센서 FK 보정은 진단 배열일 뿐 기존 estimator/controller/runtime에 연결하지 않았다. '
        'Offline Target 모델은 online controller에 전달하지 않았다. M4와 actor·native PD·raw history·기존모델/보고서를 보존했다. '
        '질량/CoM/50ms lag의 C 수집은 기존 안전성 prerequisite 실패로NOT_TESTED다. Phase D/E/F·실기·commit/push 없음.','',
        '브랜치: `agent/codex/dev_tita_gluon`. 신규 코드5개는 plan의source hash와 snapshot을 참조한다. '
        '실제 단위 검사·agent-check·완료 감사는각 로그와 completion_audit.json에 기록한다.','',
        '증거: [동결 계획](plan.json), [A exact replay/수치](A_results.json), [B 정보량/모델](B_results.json), '
        '[C 동결 모델](C_models_frozen.json), [C 독립 비교](C_comparison.json), [최종 감사](completion_audit.json).']
    write(root/'summary.json',dict(execution_domain='DESKTOP_DRY_RUN',A=afacts,C=verdicts,
        A_exact_replays=sum(len(r['rows'])for r in A),B_trajectories=len(B),C_comparisons=len(comparison)))
    (root/'REPORT.md').write_text('\n'.join(lines)+'\n')
    # Predetermined seed601/pitch0 nominal, not a best-case selection.
    file=root/'A'/'nominal_s601_p+0.000'/'Fixed.npz'
    with np.load(file)as a:
        t=np.arange(len(a['base_path']))*.02;fig,axes=plt.subplots(1,2,figsize=(11,4))
        for ax in axes:
            for k,label in [('sensor_path','original odometry'),('corrected_base_path','sensor FK diagnostic'),('base_path','base GT')]:ax.plot(t,a[k]*1000,label=label)
            ax.set_xlabel('time after first RL [s]');ax.set_ylabel('sagittal displacement [mm]');ax.grid(alpha=.2)
        axes[0].set_xlim(0.,1.);axes[1].legend();fig.tight_layout();fig.savefig(root/'A_sensor_base_correction.png',dpi=150);plt.close(fig)
    with (root/'C_scores.csv').open('w',newline='')as f:
        fields=['domain','case','snapshot_s','model','prediction_gate','information_gate','admission_gate'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:r[k]for k in fields}for r in comparison)
    verify(root,full=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();analyze(a.root.resolve())
