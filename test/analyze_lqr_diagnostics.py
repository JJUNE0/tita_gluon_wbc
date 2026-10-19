"""VALIDATION_SIM: measured failure, state-source, gain and local-model diagnostics."""

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

REPO=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(REPO/'test'))
from debug_lqr_d4_diagnostics import write_json,ARCHIVE


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args()
    root=args.root.resolve()
    results=[json.loads(line) for line in (root/'paired_corrected/results.jsonl').read_text().splitlines()]
    completion=json.loads((root/'paired_corrected/completion.json').read_text())
    assert completion['episodes']==747 and len(results)==747
    manifest=json.loads((root/'paired_corrected/manifest.json').read_text())
    replay=[r for r in results if 'archive_replay' in r]
    assert len(replay)==324 and all(r['archive_replay']['evidence_status']=='PASS' for r in replay)
    originals={}
    for r in results:
        key=(r['mismatch'],r['seed'],r['pitch_disturbance_rad'])
        if key in originals:
            np.testing.assert_allclose(r['initial_physics'],originals[key],atol=0,rtol=0)
        else:
            originals[key]=r['initial_physics']
    output=root/'analysis'
    output.mkdir(exist_ok=True)
    labels=['fixed_sensor','fixed_gt','learned_sensor','learned_gt','online_sensor','online_gt',
            'adaptation_sensor','adaptation_gt','gt_trained_frozen','fixed_synchronized','learned_synchronized']
    mismatches=list(dict.fromkeys(r['mismatch'] for r in results))
    aggregates=[]
    for mismatch in mismatches:
        for label in labels:
            rows=[r for r in results if r['mismatch']==mismatch and r['label']==label]
            if not rows:continue
            successes=[r for r in rows if not r['failures']]
            aggregates.append(dict(mismatch=mismatch,label=label,total=len(rows),failed=len(rows)-len(successes),
                max_drift_mean_m=float(np.mean([r['max_drift_m'] for r in successes])) if successes else None,
                failures=dict(Counter(f for r in rows for f in r['failures']))))
    write_json(output/'aggregates.json',aggregates)
    with (output/'aggregates.csv').open('w') as stream:
        fields=['mismatch','label','total','failed','max_drift_mean_m']
        writer=csv.DictWriter(stream,fields,extrasaction='ignore');writer.writeheader();writer.writerows(aggregates)
    failure_records=[]
    for r in results:
        if not r['failures']:continue
        with np.load(root/'paired_corrected'/r['trace']) as trace:
            snapshot=r['failure_snapshot']
            entry=dict(label=r['label'],mismatch=r['mismatch'],seed=r['seed'],pitch=r['pitch_disturbance_rad'],
                failure_time_s=r['completed_s'],failures=r['failures'],K=snapshot['K'],
                last_applied_K=trace['K'][-2].tolist(),
                raw_total_torque_nm=snapshot['raw_total_torque'],last_motor_torque_nm=np.mean(snapshot['motor'],axis=0).tolist(),
                peak_motor_nm=r['peak_motor_nm'],saturation_ratio=r['saturation_ratio'],
                motor_limit_ratio=float(np.mean(np.any(abs(trace['motor'])>=12.-1e-6,axis=(1,2)))),
                slew_active_ratio=float(np.mean(abs(trace['command'].mean(axis=1).sum(axis=1)-
                    np.clip(trace['raw_total_torque'],-24.,24.))>1e-5)),
                sensor_pitch_error_rad=snapshot['sensor_state'][2],true_pitch_error_rad=snapshot['gt_state'][2],
                true_pitch_rad=snapshot['rpy'][1],roll_rad=snapshot['rpy'][0],height_m=snapshot['base_height'],
                min_leg_limit_margin_rad=float(min(snapshot['leg_limit_margin'])),
                joint_position=snapshot['joint_position'],source_trace=r['trace'])
            failure_records.append(entry)
    write_json(output/'failures.json',failure_records)
    with (output/'failures.csv').open('w') as stream:
        scalar_fields=[k for k,v in failure_records[0].items() if not isinstance(v,list)]
        writer=csv.DictWriter(stream,scalar_fields,extrasaction='ignore');writer.writeheader();writer.writerows(failure_records)
    timing=[json.loads(line) for line in (root/'timing/results.jsonl').read_text().splitlines()]
    timing_stats={label:dict(failed=sum(bool(r['failures']) for r in timing if r['label']==label),
        total=sum(r['label']==label for r in timing)) for label in set(r['label'] for r in timing)}
    local=json.loads((root/'linearization_gain_aligned/results.json').read_text())
    validation=json.loads((root/'linearization_gain_aligned/prediction_validation.json').read_text())
    representative=next(r for r in results if r['label']=='learned_sensor' and r['mismatch']=='nominal'
                        and r['seed']==42 and r['pitch_disturbance_rad']==0.)
    learned=np.asarray(representative['failure_snapshot']['K'])
    archived_manifest=json.loads((ARCHIVE/'manifest.json').read_text())
    source_checkpoint=archived_manifest['checkpoint_sha256']
    fig,axes=plt.subplots(3,1,figsize=(10,9),sharex=True)
    for label in ['fixed_sensor','learned_sensor','fixed_gt','learned_gt','learned_synchronized']:
        r=next(r for r in results if r['label']==label and r['mismatch']=='nominal'
               and r['seed']==42 and r['pitch_disturbance_rad']==0.)
        with np.load(root/'paired_corrected'/r['trace']) as trace:
            axes[0].plot(trace['time'],trace['gt_state'][:,2],label=label)
            axes[1].plot(trace['time'],np.mean(trace['motor'],axis=(1,2))*2,label=label)
            axes[2].plot(trace['time'],trace['sensor_state'][:,3]-trace['gt_state'][:,3],label=label)
    for ax,ylabel in zip(axes,['True pitch error [rad]','Total wheel motor torque [Nm]','Cached pitch-rate error [rad/s]']):
        ax.set_ylabel(ylabel);ax.grid(alpha=.3)
    axes[0].legend(fontsize=8,ncol=2);axes[2].set_xlabel('Time [s]')
    fig.suptitle('Same physical initial state and gains; nominal seed 42, pitch perturbation 0')
    fig.tight_layout();fig.savefig(output/'state_gain_comparison.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(2,1,figsize=(11,7),sharex=True)
    for label in ['fixed_sensor','fixed_gt','learned_sensor','learned_gt','online_sensor','online_gt']:
        values=[next(r for r in aggregates if r['mismatch']==m and r['label']==label) for m in mismatches]
        axes[0].plot(mismatches,[r['failed']/r['total'] for r in values],marker='o',label=label)
        axes[1].plot(mismatches,[r['max_drift_mean_m'] for r in values],marker='o',label=label)
    axes[0].set_ylabel('Failure fraction');axes[0].legend(fontsize=8,ncol=3)
    axes[1].set_ylabel('Maximum drift [m]\ncompleted trials only');axes[1].tick_params(axis='x',rotation=25)
    for ax in axes:ax.grid(alpha=.3)
    fig.tight_layout();fig.savefig(output/'mismatch_comparison.png',dpi=180);plt.close(fig)
    failure_types=dict(Counter(f for r in results if r['label'] in ('learned_sensor','online_sensor','adaptation_sensor') for f in r['failures']))
    table=['| 조건 | K₀ 센서 | K₀ GT | K_adapt 센서 | K_adapt GT | online 센서 | online GT |',
           '|---|---:|---:|---:|---:|---:|---:|']
    for mismatch in mismatches:
        cells=[]
        for label in ['fixed_sensor','fixed_gt','learned_sensor','learned_gt','online_sensor','online_gt']:
            a=next(r for r in aggregates if r['mismatch']==mismatch and r['label']==label)
            cells.append(f'{a["failed"]}/{a["total"]}')
        table.append('| '+mismatch+' | '+' | '.join(cells)+' |')
    training_table=['| 조건 | GT adaptation 실패 | 그 gain의 새 GT 평가 실패 |','|---|---:|---:|']
    for mismatch in mismatches:
        a=next(r for r in aggregates if r['mismatch']==mismatch and r['label']=='adaptation_gt')
        b=next(r for r in aggregates if r['mismatch']==mismatch and r['label']=='gt_trained_frozen')
        training_table.append(f'| {mismatch} | {a["failed"]}/{a["total"]} | {b["failed"]}/{b["total"]} |')
    rep=next(x for x in failure_records if x['label']=='learned_sensor' and x['mismatch']=='nominal'
             and x['seed']==42 and x['pitch']==0.)
    matrix_rows=[]
    for result in local['results']:
        c=next(x for x in result['comparisons'] if x['seed']==42 and x['pitch']==0.)
        matrix_rows.append(f'| {result["epsilon"]} | {c["A0_error"]:.4f} | {c["Ahat_error"]:.4f} | '
            f'{c["B0_error"]:.4f} | {c["Bhat_error"]:.4f} | {result["contact_branch_changes"]} |')
    integrity=dict(execution_domain='VALIDATION_SIM',evidence_status='PASS',checkpoint_sha256=source_checkpoint,
        episodes=747,archive_exact_replays=324,paired_initial_conditions=len(originals),timing_trials=len(timing),
        archive_max_abs_error=max(max(r['archive_replay'].get('max_errors',{'x':0}).values()) for r in replay))
    write_json(output/'integrity.json',integrity)
    lines=['# D-4 실패·Ground-truth·학습 gain 진단', '',
        'Execution Domain: VALIDATION_SIM (코드·로그 검사: DESKTOP_DRY_RUN)', '',
        'Evidence Status: SUSPICIOUS — 진단 실행과 재현 gate는 PASS, 제어 성공/실패는 아래에 구분한다.', '',
        f'Policy Checkpoint SHA256: `{source_checkpoint}`', '',
        'Observed Metrics / Behavior / Log Summary:', '',
        '**Nominal의 D-4 실패는 학습된 gain 단독의 불안정성으로 설명되지 않았다.** '
        '기존 sensor cache 경로는 학습 gain 고정 시 6/9회 실패했지만, 같은 gain과 같은 물리 초기 상태에서 '
        'GT 또는 동기화 센서를 사용하면 9/9회 완료했다. Gyro만 최신화한 9회도 모두 완료했다. '
        '반면 일부 mass mismatch에서는 GT로도 실패가 남으므로 센서 시점 문제만으로 모든 조건을 설명할 수 없다.', '',
        '## 공통 조건과 실행 근거', '',
        '- 새 제어 알고리즘·PINN·RLS 구조·Q/R·leg PD·평형 pitch 기준을 추가하거나 변경하지 않았다. 기존 코드와 보고서를 보존했다.',
        '- 신규 진단 코드는 모두 `test/`에 있다. 기존 Playback.step, actuator adapter, setup_scene, WheelLQR/RLS를 재사용했다.',
        '- 9 dynamics 조건 × 3 seeds × 3 pitch = 81개 물리 초기 조건. 같은 archived K를 센서/GT에 교차 적용했다. '
        'Sensor/GT online 및 cold-start adaptation도 따로 실행했다. Nominal에 synchronized 센서 18회 추가: 총 747회.',
        f'- 기존 Fixed-4 및 D-4 adaptation/frozen/online 324회를 재현했다. 최종 시각·실패 여부·state·K·torque·residual이 일치한다. '
        f'최대 차이 {integrity["archive_max_abs_error"]:.3g}. 초기 qpos/qvel는 81개 pair에서 완전히 동일했다.',
        '- Primary GT는 root quaternion/각속도 및 wheel axle world 위치·Jacobian 속도를 사용한다. '
        '위치는 기존 estimator와 맞춰 midpoint heading 방향의 실제 axle 이동량을 누적한다. '
        'world x/y hold와는 다르며 yaw가 바뀌면 동일한 위치 목표로 해석할 수 없다.',
        '- GT 읽기는 복제 mjData에서 mj_forward를 실행한다. 원본 dynamics 및 cached sensor timing을 바꾸지 않는다. '
        'Clone 비변경 검사와 pitch/axle 속도의 독립 유한차분 검사 2개 PASS (`oracle_tests.log`).',
        '- GT는 이번 사용자 요청으로 허용된 진단용 입력이며 deployable controller/RLS에는 추가하지 않았다.',
        '- 모든 평가 12초, dt=0.02 s, physics dt=0.005 s, 동일 torque/slew limit과 동일 disturbance. '
        'Adaptation만 기존 probing을 사용한다. 학습된 gain 비교는 probing 없이 새 episode에서 시작한다.', '',
        '## 1. D-4 실패 원인', '',
        f'기존 경로의 79개 실패를 전부 재현하고 trigger를 분리했다: `{failure_types}`. '
        'Pitch error 한계가 직접 종료 사유였다. Roll/height/leg limit은 함께 기록했다.', '',
        f'대표 nominal seed42/pitch0 학습 gain: `{learned.tolist()}`. '
        f'Gain 고정 실패 시각 {rep["failure_time_s"]:.2f} s, cached pitch error {rep["sensor_pitch_error_rad"]:.4f} rad, '
        f'true pitch error {rep["true_pitch_error_rad"]:.4f} rad, roll {rep["roll_rad"]:.4f} rad, '
        f'base height {rep["height_m"]:.4f} m. Leg limit 최소 margin {rep["min_leg_limit_margin_rad"]:.4f} rad.',
        f'실패 직전 실제 wheel torque: `{rep["last_motor_torque_nm"]}` Nm, episode peak {rep["peak_motor_nm"]:.3f} Nm, '
        f'raw 합 torque clipping ratio {rep["saturation_ratio"]:.3f}, 실제 motor limit 도달 비율 {rep["motor_limit_ratio"]:.3f}, '
        f'slew 제한 적용 비율 {rep["slew_active_ratio"]:.3f}. '
        'Raw command clipping과 실제 motor saturation은 구분해야 한다. 종료 trigger는 pitch 한계였으며 slew/clipping의 기여를 배제하지 않는다.',
        '- `analysis/failures.json`에 현재 K/직전 실제 적용 K, 실제 torque, saturation, pitch/roll, height, '
        'joint 값·limit margin·정확한 사유를 기록했다. 각 실패에는 마지막 0.3초 CSV가 있다.',
        '- NPZ row t의 torque는 직전 [t−dt,t] 구간에 적용된 값이다. 대응하는 적용 gain은 이전 row의 K이다. '
        'Gain 변경과 torque/측정의 시간을 분리해서 해석해야 한다.', '',
        '## 2–3. GT 상태 대조 및 K₀/K_adapt 재평가', '',
        '아래는 실패 횟수/전체이다. K_adapt는 각 pair의 기존 센서 adaptation에서 얻은 **동일한 gain**이며 평가에서 고정했다. '
        'Online도 동일한 archived gain·P·residual로 시작했다. 실패한 adaptation의 gain도 성공으로 숨기지 않고 그대로 진단했다.', '',
        '\n'.join(table), '',
        'Nominal K₀와 K_adapt는 sensor 동기화 경로에서 모두 9/9회 완료했다. 기존 nominal online 4/9회 실패도 GT에서는 0/9였다.', '',
        f'분리 시험 18회: `{timing_stats}`. '
        'Gyro 최신화는 pitch-rate뿐 아니라 encoder velocity의 body angular contribution도 바꾼다. '
        '따라서 pitch-rate 채널 하나만의 원인이라고 단정하지 않는다.',
        '- 기존 경로는 mj_step 이후 fresh joint qpos/qvel와 마지막 physics substep 이전의 IMU sensor cache를 혼합한다. '
        '복제 data의 gyro/quaternion을 최신화하면 이 시점 차이를 제거한다. '
        '이상은 정지 odometry의 1.7cm RMS만으로 발견하기 어렵고, transient feedback에서 중요했다.',
        '- 대표 K_adapt의 velocity gain 크기는 K₀보다 약 3.96배, pitch-rate gain은 약 2.46배이다. '
        '이 큰 gain이 cached gyro가 포함된 loop의 시간 오차에 더 민감했음을 동일 K의 교차실험이 뒷받침한다.', '',
        'GT를 RLS에도 사용한 cold-start adaptation 및 그 gain의 새 GT 평가:', '',
        '\n'.join(training_table), '',
        '## 실제 leg PD/contact plant 수치 선형화', '',
        '- 같은 360/12 leg PD, 같은 stand reference·motor limits·wheel contact·dt를 사용했다. '
        '수치 A/B를 controller에 적용하지 않았다. Nominal contact 조건에서만 계산했다.',
        f'- 실제 force balance 최적화의 최대 qacc 잔차는 {local["equilibrium"]["max_abs_qacc"]:.5f}. '
        '대부분 yaw와 leg 방향이며 **정확한 정적 평형은 확보하지 못했다**. 따라서 접지된 near-static operating point의 local 근사이다.',
        '- 전체 28차원 tangent state(qpos tangent 14 + qvel 14)의 20ms map F/G를 중앙 차분했다. '
        'Leg PD는 physics step마다 재계산하고 contact solver도 포함한다.',
        '- H는 실제 [axle p,v,pitch,pitch-rate]의 관측 Jacobian, E는 axle 중심 pitch pivot 및 rolling wheel rate를 포함하는 '
        '명시적인 4-state lift이다. A_local=HFE, B_local=HG. H E≈I를 검사했다.',
        '- H F−A_local H의 norm은 약 39로 0이 아니다. 숨은 leg/roll/yaw 상태가 있어 이 system은 4-state만으로 완전히 닫히지 않는다. '
        '따라서 이 투영을 유일하고 정확한 A_true라고 부르지 않는다.', '',
        '| state FD epsilon | A₀ 오차 norm | Ahat_final 오차 norm | B₀ 오차 norm | Bhat_final 오차 norm | 접촉 pair 변경 |',
        '|---:|---:|---:|---:|---:|---:|', *matrix_rows, '',
        '- 행렬 norm은 단위와 state scale에 의존한다. 현재 계수의 A 오차는 nominal보다 커졌고 B 오차는 줄었다. '
        '이는 네 residual 계수를 실제 A/B의 정확한 식별이라고 해석할 수 없다는 근거다.',
        '- 아주 작은 input 차분은 contact solver 오차에 민감했다. 독립 input 크기 0.001/0.01/0.05 Nm에서 B를 다시 계산했다. '
        'B_omega는 −0.04645/−0.04652/−0.04650으로 일치했다. 원본 sensitivity 결과를 함께 보존했다.',
        f'- 독립 50개 small-perturbation one-step validation component RMS [p m,v m/s,theta rad,omega rad/s]: '
        f'`{validation["heldout_component_rms"]}`. local 모델의 centered 응답은 검증됐지만 장기 안정성 보증은 아니다.',
        '- K 계산 시점의 Ahat와 마지막 RLS Ahat를 따로 기록했다. 후보가 거부되면 K는 이전 값이므로 둘을 섞으면 안 된다.',
        '- 4-state projection의 eigenvalue 판정은 epsilon에 따라 단위원 안팎을 오갔다. '
        '전체 28-state에는 neutral translation/yaw/wheel-angle modes가 있어 spectral radius≈1을 곧바로 실패로 판정할 수 없다. '
        '실제 nonlinear 동일 초기 조건 rollout을 gain 안정성 판단의 우선 근거로 사용했다.', '',
        '## 판단과 남은 한계', '',
        '1. 기존 nominal D-4 실패를 모델/gain 자체의 불안정성으로만 설명했던 판단은 수정해야 한다. '
        '같은 gain을 GT 또는 gyro 시점 정렬로 적용하면 실패가 사라졌다.',
        '2. Mass mismatch 일부는 GT에서도 실패한다. Sensor timing과 model-order/계수 식별 문제를 분리해서 다뤄야 한다.',
        '3. 현재 physical equilibrium의 pitch bias, yaw drift, 접촉·leg compliance는 그대로 유지했다. '
        '이번 진단에서 이를 수정하거나 Q/R를 다시 튜닝하지 않았다.',
        '4. 새 알고리즘 확장 전에 sensor/control/RLS transition의 시간 정렬을 검증하고, '
        '이 gain이 어떤 operating point·hidden state 조건에서 유효한지 다시 평가하는 것이 타당하다.', '',
        '초기 oracle에서 local object angular frame을 root frame으로 오해한 시험은 무효 표시 후 중단했다. '
        '`smoke` 및 `full`의 GT 결과는 분석에서 제외했고 corrected oracle만 사용했다. '
        '접촉 없는 초기 선형화도 제외했다. 이 보고서의 frame/velocity는 독립 유한차분 검사를 통과했다.', '',
        '## 실행 및 산출물', '',
        '```bash',
        '/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_lqr_diagnostic_state.py',
        '/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/debug_lqr_d4_diagnostics.py --output docs/exp/2026-10-14/new_diagnostics/paired_corrected',
        '/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/debug_lqr_sensor_timing.py --output docs/exp/2026-10-14/new_diagnostics/timing',
        '/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/debug_linearize_lqr_plant.py --output docs/exp/2026-10-14/new_diagnostics/linearization_gain_aligned',
        'MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_lqr_diagnostics.py --root docs/exp/2026-10-14/new_diagnostics',
        '```', '',
        '- `analysis/aggregates.csv/json`, `failures.csv/json`, `integrity.json`, 비교 PNG 2개.',
        '- `paired_corrected/`의 747개 NPZ와 실패 직전 CSV, actual initial state와 K/P 복원 기록.',
        '- `linearization_gain_aligned/`의 F/G/H/E, projected A/B, K 및 RLS 모델, equilibrium 잔차와 independent validation.',
        '- `test/test_lqr_diagnostic_state.py` 2개 PASS, `./scripts/agent-check.sh` PASS (Python syntax 330개, URDF XML 8개).',
        '- 브랜치: `agent/codex/dev_tita_gluon`. 기존 production/simulation 제어 코드는 변경하지 않았다.', '',
        'MuJoCo API 참고: [공식 functions 문서](https://mujoco.readthedocs.io/en/stable/APIreference/APIfunctions.html) '
        '(state copy, quaternion tangent integration/differencing, point Jacobian).']
    (REPO/'docs/exp/2026-10-14/lqr_diagnostics_summary.md').write_text('\n'.join(lines)+'\n')
    print('[VALIDATION_SIM] diagnostics report generated;',integrity)


if __name__=='__main__':
    main()
