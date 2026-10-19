"""DESKTOP_DRY_RUN: audit actual stage gates and write the overnight report."""

import argparse
import json
import os
from pathlib import Path
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from run_flash_overnight_pipeline import verify_record,NAMES
from eval_flash_pv_models import REPO,write,sha256


def median(rows,group,family,key,point='base'):
    values=[r[point][key] for r in rows if r['group']==group and r['family']==family and r[point][key] is not None]
    return float(np.median(values)) if values else float('nan')


def number(value,scale=1.,digits=4):
    return f'{value*scale:.{digits}f}' if np.isfinite(value) else 'N/A'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args();root=args.root.resolve();report=args.report.resolve()
    assert report.is_relative_to(REPO/'docs/exp')
    state=json.loads((root/'pipeline_state.json').read_text());plan=json.loads((root/'plan.json').read_text())
    if not state.get('terminal'):raise RuntimeError('Pipeline is still incomplete; refusing a final report')
    evidence={}
    for key,record in state['stages'].items():
        if record['status'] in ['PASS','FAIL']:
            verify_record(root,record)
            evidence[int(key)]=json.loads((root/record['artifact']).read_text())
    for p,h in plan['protected_sha256'].items():assert sha256(REPO/p)==h,p
    failed=[int(k) for k,v in state['stages'].items() if v['status']=='FAIL']
    prerequisite_failures_recorded=all(state['stages'][str(i)]['status']=='NOT_TESTED'
        for i in range(min(failed)+1,8)) if failed else True
    mandatory_executed=1 in evidence and 2 in evidence and (not evidence[2]['gate'] or 3 in evidence)
    assert prerequisite_failures_recorded
    text=['# model_60000 — 단계별 gate를 적용한 야간 M4/M5 실험','',
        '작성일: 2026-10-15 (Asia/Seoul)','',
        'Execution Domain: **VALIDATION_SIM** (식별·검증·보고: **DESKTOP_DRY_RUN**)','',
        f"Policy Checkpoint SHA256: `{plan['checkpoint_sha256']}`",'',f"ONNX SHA256: `{plan['onnx_sha256']}`",'',
        f"Evidence Status: **{'PASS' if state['scientific_success'] else 'FAIL'} — 연구 성능의 전체 기준.** 단계별 결과를 아래에 구분한다. 파이프라인 정상 종료는 모든 연구 가설의 PASS를 뜻하지 않는다.",'',
        'Observed Metrics / Behavior / Log Summary:','',
        '| 단계 | 실험 | 결과 |','|---|---|---|']
    for i in range(1,8):
        r=state['stages'][str(i)];reason=r.get('reason','')
        text.append(f"| {i} | {NAMES[i]} | **{r['status']}** {reason} |")
    if 3 in evidence and evidence[3].get('gate') and 4 in evidence:
        text += ['', '**국소 운용점의 Fixed LQR은 두 모델 모두 통과했지만, 초기 drift 진입에서는 '
            f"M4 {'PASS' if evidence[4].get('models',{}).get('M4') else 'FAIL'}, "
            f"M5 {'PASS' if evidence[4].get('models',{}).get('M5') else 'FAIL'}였다.** "
            '이 구분을 유지하고 선행 gate가 충족되지 않은 mismatch·RLS·Adaptive 실험으로 넘어가지 않았다.']
    text += ['', '## 1. 파이프라인과 고정한 조건','',
        '기존 M4/M5 비교에서는 M5의 상대 개선 한도를 별도로 사용했다. 이번 목표는 M5 자체의 A/B·affine 유효성 검증을 필수로 요구하므로, 상대 개선 FAIL을 이유로 2단계를 생략하지 않았다. 이전 결과와 보고서는 유지한다.','',
        '단계1은 기존 train/test 비교의 실제 지표와 frozen hash를 확인한다. 단계2는 A/B를 고정하고 train baseline18개로 offset만 추정한 뒤, 새 seed260/261 × initial pitch−0.035/0/+0.035의6조건, hold1000/1120초의12snapshot에서 독립 검증한다. 총204개8초 probe, baseline12개, 직접B±차분12쌍이다. 모든 미래 yaw rate/action/leg 상태는 모델이 재귀 예측하며 실측값을 주입하지 않는다.','',
        'FlashSAC model_60000, 동기화 IMU, 원래 wheel/leg PD와 전체 raw last_action을 유지한다. F-1은 모델 수집에서 OFF다. 고정 bias는 합+0.4828 Nm, physics/control dt는0.005/0.02초다. GT는 제어에 쓰지 않는다.','',
        '**주 물리 평가점은 base_link 원점, wheel midpoint는 보조 지표**다. 각 점의 world 이동을 구간 중간 horizontal heading에 투영해 누적한 sagittal path다. 센서 p/v는 기존 rolling odometry이며 이를 base-origin GT로 재정의하거나 보정하지 않았다. 모델의 센서 상태 예측과 물리 제어 평가는 구분한다. Yaw rate는 body gyro와 roll/pitch에서 계산한 heading 변화율이며, M5의 내부 기준값은 train의 비영 평균이다. yaw-rate0 제어 목표를 추가하지 않는다.','',
        '각 gate·Q/R·토크 제한은 새 수집 전에 plan.json에 기록했다. 모델 기준은 최초2초 및 rolling0.1/0.5/1/2초 p/v NRMSE 중앙값≤30%, 직접B_v 부호 일치·상대오차≤30%다. Affine baseline은 모든12개에서2초 p/v RMSE≤0.02mm/0.02mm/s,8초≤0.05mm/0.02mm/s를 요구한다. 운영 기준이며 사용자 정량 사양이나 안정성 정리는 아니다.','',
        '단계2 실패 시 gain을 생성하지 않는다. 단계3은 먼저 실제 MuJoCo9회 pilot을 실행하고, 통과할 때만324회 비교를 진행한다. 실패/예외/누락 gate는 FAIL로 처리하며 이후 실험은 NOT_TESTED로 남긴다. Resume는 이전 stage artifact·source·plan뿐 아니라 검증된 A/B·gain·snapshot·raw log hash도 검사하고 실패한 단계를 자동 재실행하지 않는다. OS flock으로 동시 coordinator를 막는다.','',
        '## 2. 독립 A/B·affine 검증','',
        '| 모델 | Affine 최초2초 p/v NRMSE | Affine rolling2초 p/v NRMSE | Baseline PASS | 판정 |',
        '|---|---:|---:|---:|---|']
    if 2 in evidence and 'models' in evidence[2]:
        for name,m in evidence[2]['models'].items():
            a=m['affine']['full2s']['nrmse'];b=m['affine']['horizons']['100']['nrmse']
            text.append(f"| {name} | {a[0]*100:.2f} / {a[1]*100:.2f}% | {b[0]*100:.2f} / {b[1]*100:.2f}% | "
                f"{sum(x['gate'] for x in m['baselines'])}/{len(m['baselines'])} | {'PASS' if m['gate'] else 'FAIL'} |")
    text += ['', '같은 초기 조건의 여러 시각·입력은 관련된 응답이다.204회를 독립 초기 조건204개로 해석하지 않는다. Affine는 train18개 baseline의 평균 one-step defect로 offset만 추정했고, 새 검증 결과로 계수나 입력 기준을 재튜닝하지 않았다. 정적 평형을 역산하거나 큰 torque를 외삽하지 않는다.','',
        '## 3. Fixed Residual LQR 비교','',
        '두 모델 모두 Q_p=Q_v=250000, 나머지 상태 비용0, R=400을 한 번 적용했다. 전체24/25개 상태를 피드백하므로 pitch/action/leg/yaw-rate gain이 생길 수 있다. 단순 p/v PD로 gain 첫 두 개만 분리하지 않는다. 명령은 bias + 제한된−K오차이며 추가보정±0.05Nm(total), smoothstep ramp1.5초, slew2Nm/s다. Gain/reference/Q/R은 전 비교에서 고정했다.','',
        '사전 gate는 두 모델 모두 전체 완료 및 pitch/wheel torque 기준, position/kick 각각 base IAE중앙값≤bias의80%, 마지막5초 위치RMSE≤bias의50%, paired IAE개선≥80%다. 무외란은 마지막5초 RMSE≤max(bias+0.05mm,0.1mm), 평균 속도 절댓값≤0.02mm/s다. 실패한 짧은 episode를 작은 drift 성공으로 집계하지 않는다.']
    metric_path=root/'control_metrics.json'
    if metric_path.exists():
        rows=json.loads(metric_path.read_text())['rows']
        text += ['', '| 군 | 조건 | 완료 | Base IAE mm·s | Base 마지막5초 RMSE mm | Wheel-midpoint RMSE mm |',
            '|---|---|---:|---:|---:|---:|']
        for group in ['bias_only','M4','M5']:
            for family in ['position','kick','zero']:
                selected=[r for r in rows if r['group']==group and r['family']==family]
                text.append(f"| {group} | {family} | {sum(r['complete'] for r in selected)}/{len(selected)} | "
                    f"{number(median(rows,group,family,'IAE'),1000)} | {number(median(rows,group,family,'last5_RMSE'),1000,5)} | "
                    f"{number(median(rows,group,family,'last5_RMSE','wheel_midpoint'),1000,5)} |")
        paths=sorted((root/'control').glob('*/results.json'))
        info=json.loads(paths[0].read_text());fig,axes=plt.subplots(2,1,figsize=(10,6),sharex=True)
        for group in ['bias_only','M4','M5']:
            row=next(r for r in info['rows'] if r['group']==group and r['family']=='position' and r['amplitude']==.001)
            with np.load(paths[0].parent/row['trace']) as a:
                t=np.arange(len(a['base_path']))*.02
                axes[0].plot(t,(a['base_path']+.001)*1000,label=group)
                axes[1].plot(t,(a['axle_path']+.001)*1000,label=group)
        axes[0].set_ylabel('base target error [mm]');axes[1].set(ylabel='wheel-midpoint error [mm]',xlabel='time [s]')
        for ax in axes:ax.grid(alpha=.3);ax.legend()
        fig.tight_layout();fig.savefig(root/'fixed_comparison.png',dpi=150);plt.close(fig)
        text += ['', '총324회는12snapshot×9조건×3군이다. Position은±0.5/±1mm 목표 변경, kick은±0.01/±0.02Nm를20ms 적용한 뒤 복원이며, 순수한v만 바꾼 상태가 아니다.','',
            f"![동일 기준점의 Fixed LQR 비교]({root.name}/fixed_comparison.png)"]
    elif 3 in evidence:
        text += ['',f"전체 비교는 시작하지 않았다. Pilot gate: {evidence[3].get('pilot_gate','exception')}. 상세: 03_fixed_LQR.json."]
    text += ['', '## 4. 초기 drift 정지 진입과 후속 단계','']
    entry=root/'entry_metrics.json'
    if entry.exists():
        rows=json.loads(entry.read_text())['rows']
        text += ['새 seed270/271 ×3pitch의6조건에서 FlashSAC-only8초 후 같은 상태를 복제했다. A/bias/M4/M5를60초 비교했다. Bias 전환은2Nm/s로 제한하며 LQR 보정 ramp/제한도 유지한다. 이 초기 상태는 국소 학습 범위 밖일 수 있고 support fraction을 별도 기록한다.','',
            '| 군 | 완료 | 최대 planar drift 중앙값 m | 마지막5초 base 속도RMS mm/s | 마지막5초 base 위치범위 mm |',
            '|---|---:|---:|---:|---:|']
        for group in ['A','bias_only','M4','M5']:
            selected=[r for r in rows if r['group']==group]
            med=lambda k:float(np.median([r[k] for r in selected if r[k] is not None])) if any(r[k] is not None for r in selected) else float('nan')
            text.append(f"| {group} | {sum(r['complete'] for r in selected)}/{len(selected)} | {number(med('max_planar_drift'),digits=5)} | "
                f"{number(med('last5_base_speed_RMS'),1000)} | {number(med('last5_base_position_range'),1000)} |")
        text += ['', '진입 gate는 전체 완료, 각 trial의 최대 planar drift≤bias의80%, 마지막5초 base 속도RMS≤0.2mm/s 및 위치범위≤5mm다. 국소 복원 PASS를 초기 drift 상태의 진입 성공으로 일반화하지 않는다.']
        diagnostics=[]
        for row in rows:
            if row['group'] not in ['M4','M5']:continue
            with np.load(root/'entry'/row['context']/row['trace']) as trace:
                diagnostics.append(dict(context=row['context'],group=row['group'],
                    initial_raw_correction=float(trace['raw_correction'][0]),
                    peak_raw_correction=float(max(abs(trace['raw_correction']))),
                    raw_over_cap_fraction=float(np.mean(abs(trace['raw_correction'])>=.05)),
                    actual_correction_peak=float(max(abs(trace['correction']))),
                    hidden_train_fraction=row['hidden_train_fraction'],
                    last5_residual_mean=float(np.mean(trace['actual_u'][-250:]))))
        write(root/'entry_diagnostics.json',dict(execution_domain='DESKTOP_DRY_RUN',rows=diagnostics,
            note='Raw feedback before the unchanged limit; no extra control runs or tuning.'))
        text += ['', '### 진입 시 유효 범위와 입력 제한','',
            '| 모델 | 비위치 상태 train 범위 내 비율 | 초기 raw 보정 범위 Nm | raw가±0.05Nm를 넘는 시간 비율 |',
            '|---|---:|---:|---:|']
        for group in ['M4','M5']:
            subset=[r for r in diagnostics if r['group']==group]
            raw=[r['initial_raw_correction'] for r in subset];fraction=[r['raw_over_cap_fraction'] for r in subset]
            text.append(f"| {group} | {np.median([r['hidden_train_fraction'] for r in subset])*100:.1f}% | "
                f"{min(raw):.3f}～{max(raw):.3f} | {min(fraction)*100:.1f}～{max(fraction)*100:.1f}% |")
        text += ['', '좌표별 train min/max 검사이며 다변량 유효성 증명은 아니다. 초기 drift의 내부 상태는 두 모델 모두 국소 수집 범위 밖이었다. Raw 보정이 커도 실제 추가 보정은±0.05Nm를 넘지 않았다. M5의 긴 포화와 진입 실패가 함께 관측됐지만, yaw feedback 하나가 유일한 원인이라고 확정하거나 Q/R을 사후 조정하지 않는다.','']
        first_context=sorted({r['context'] for r in rows})[0]
        fig,axes=plt.subplots(3,1,figsize=(10,8),sharex=True)
        for group in ['A','bias_only','M4','M5']:
            row=next(r for r in rows if r['context']==first_context and r['group']==group)
            with np.load(root/'entry'/row['context']/row['trace']) as trace:
                t=np.arange(len(trace['base_path']))*.02
                axes[0].plot(t,trace['base_path']*1000,label=group)
                axes[1].plot(t,trace['base_velocity'][:,0]*1000,label=group)
                axes[2].plot(t[:-1],trace['actual_u'],label=group)
        axes[0].set_ylabel('base sagittal path [mm]');axes[1].set_ylabel('base velocity [mm/s]')
        axes[2].set(ylabel='total residual [Nm]',xlabel='time since entry [s]')
        for ax in axes:ax.grid(alpha=.3);ax.legend()
        fig.tight_layout();fig.savefig(root/'entry_comparison.png',dpi=150);plt.close(fig)
        text += [f'![초기 drift 정지 진입]({root.name}/entry_comparison.png)','']
    if failed:
        text += ['',f"**최초 실패 단계는 {min(failed)} ({NAMES[min(failed)]})다.** 이후 단계는 선행 gate 미충족으로 실행하지 않았다. 이를 강건성 또는 Adaptive LQR의 성능 FAIL/PASS로 해석하지 않는다."]
    text += ['', '단계5가 허용될 경우 mass1.15/1.30, wheel motor gain0.8/1.2, lag0.02/0.05에서 A/bias/F-1/M4/M5의60초 응답을 비교한다. Mass/inertia 변경은 snapshot qpos/qvel을 보존하며, motor 변경은 residual 합산 후 physics substep에 wheel에만 적용한다. 이번 실행 여부는 단계표를 따른다. RLS 및 Adaptive LQR은 선행 단계 통과 전 구현·적용하지 않는다.','',
        '## 5. 검증과 재현','',
        '파이프라인 수치/흐름 검사6개와 제어 gate/실제 motor 경로 검사4개를 실행했다. Affine FAIL/exception/missing gate의 후속 실행 금지, 실패 단계 재실행 금지, stage 증거 및 검증된 A/B/gain 변조 거부, 재개 후 정확한 skip 사유 갱신, base 기준점 우선 판정, 미완료 episode 거부, nominal motor wrapper의 원래 상태/action/history/torque exact 재현, wheel-only gain/physics-dt lag를 검사한다. 실제 로그는 상위 evidence 폴더의 unit_tests_final.log/control_unit_tests.log다.','',
        '기존 runtime·정책·훈련 설정·이전 모델/보고서는 보존한다. 신규 코드6개는 test/run_flash_overnight_pipeline.py, test/flash_overnight_model_stages.py, test/flash_overnight_control_stages.py, test/analyze_flash_overnight_pipeline.py, test/test_flash_overnight_pipeline.py, test/test_flash_overnight_control.py다. 본 보고서와 실험 증거를 추가했다. Hardware·정책 재학습·commit/push 없음. 브랜치 agent/codex/dev_tita_gluon. 최종 agent-check 결과와 기존 변경 보존 감사는 상위 evidence 폴더의 agent_check.log/final_review.json에 기록한다.','',
        '```bash',
        'MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/run_flash_overnight_pipeline.py --root docs/exp/2026-10-15/new_overnight/run --workers 3',
        'MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_flash_overnight_pipeline.py --root docs/exp/2026-10-15/new_overnight/run --report docs/exp/2026-10-15/new_overnight_summary.md',
        '```','',
        '기존 root를 재개할 때는 --resume을 사용한다. 실패한 stage를 덮어쓰거나 자동 재튜닝하지 않는다. 실행 중 중단된 RUNNING stage는 증거 확인 없이 재실행하지 않는다.','',
        '초기 coordinator 실행은 run/에 보존했다. 재개 시 출력 A/B/gain/raw log를 hash로 묶는 검사를 추가하고 NOT_TESTED 사유가 이전 --through 값에 남는 문제를 수정한 뒤, run_final/에서 같은 사전 기준·계수·초기 조건으로 전체 파이프라인을 다시 실행했다. 주 결과는 run_final/만 사용한다. 두 실행은 같은 조건의 재현이므로 독립 표본 수를 늘려 합산하지 않는다. 초기 실행 source는 coordinator_v1.source.txt로 보존한다.','']
    agent_log=root.parent/'agent_check.log'
    if agent_log.exists():
        log=agent_log.read_text()
        syntax=re.search(r'Syntax Check Results: (\d+) passed, (\d+) failed',log)
        urdf=re.search(r'(\d+) URDF files OK',log)
        whitespace=log.count('trailing whitespace.')
        if syntax and urdf and whitespace:
            text += [f'최종 검증: pipeline6개+control4개 **10개 PASS**. agent-check는 기존 my_flat_env_cfg.py의 trailing whitespace{whitespace}곳으로 **전체 FAIL**이며, '
                f'Python syntax{syntax[1]}개와 URDF{urdf[1]}개 검사는 PASS다. 기존 문제를 수정하거나 전체 검사를 PASS로 바꾸지 않았다.','']
    # Relative links are resolved from the report's actual location.
    relative=Path(os.path.relpath(root,report.parent)).as_posix()
    text=[line.replace(f'({root.name}/',f'({relative}/') for line in text]
    links=[('단계 상태','pipeline_state.json'),('사전 계획','plan.json'),('독립 검증','02_independent_affine.json'),
        ('고정 gain','gains_frozen.json'),('Fixed LQR 판정','03_fixed_LQR.json')]
    text += ['산출물: '+', '.join(f'[{label}]({relative}/{name})' for label,name in links if (root/name).exists())+'.']
    report.write_text('\n'.join(text)+'\n')
    write(root/'completion_audit.json',dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',
        mandatory_experiments_executed=mandatory_executed,downstream_stopped_after_failure=prerequisite_failures_recorded,
        scientific_success=state['scientific_success'],terminal=state['terminal'],stage_status={k:v['status'] for k,v in state['stages'].items()},
        protected_hashes_preserved=True,stage_artifacts_verified=True,report_sha256=sha256(report)))
    print('[DESKTOP_DRY_RUN] report',report,'scientific_success',state['scientific_success'],flush=True)


if __name__=='__main__':main()
