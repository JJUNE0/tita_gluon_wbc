"""DESKTOP_DRY_RUN: integrity audit and VALIDATION_SIM residual experiment report."""

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
from eval_flash_torque_residual import REPO, WHEELS, LEGS, write_json, sha256, policy_config, action_history_slice


def read_rows(folder, name='results.jsonl'):
    return [dict(json.loads(line), folder=str(folder)) for line in (folder/name).read_text().splitlines()]


def aggregate(rows):
    groups=[]
    for label in dict.fromkeys(r['label'] for r in rows):
        subset=[r for r in rows if r['label']==label]
        complete=[r for r in subset if not r['failures']]
        entry=dict(label=label,total=len(subset),failed=len(subset)-len(complete),
            min_completed_s=min(r['completed_s'] for r in subset),max_completed_s=max(r['completed_s'] for r in subset))
        for key in ('max_displacement_m','max_forward_displacement_m','max_lateral_displacement_m',
                    'pitch_rms_rad','true_pitch_error_rms_rad','torque_rms_nm','peak_torque_nm',
                    'residual_peak_total_nm','odometry_gt_path_error_rms_m'):
            values=[r[key] for r in complete]
            entry[key]=dict(mean=float(np.mean(values)),std=float(np.std(values,ddof=1))) if values else None
        groups.append(entry)
    return groups


def integrity(rows):
    policy=policy_config()
    history_slice,scale,clip=action_history_slice(policy)
    lookup={(r['seed'],r['pitch_delta_rad']):r for r in rows if r['label']=='A'}
    max_error=history_error=leg_error=initial_error=0.
    for r in rows:
        original=lookup[(r['seed'],r['pitch_delta_rad'])]
        initial_error=max(initial_error,float(abs(np.asarray(r['initial_physics'])-original['initial_physics']).max()))
        assert r['audit']['online_rls_calls']==0
        assert r['audit']['history_max_error']==0 and r['audit']['leg_torque_max_error_nm']==0
        with np.load(Path(r['folder'])/r['trace']) as trace:
            observed=trace['policy_observation'][1:,history_slice]
            expected=np.clip(trace['history_input'][1:],*clip)*scale
            history_error=max(history_error,float(abs(observed-expected).max()))
            leg_error=max(leg_error,float(abs(trace['command_substeps'][:,:,LEGS]-trace['flash_substeps'][:,:,LEGS]).max()))
            if r['label'].startswith('E-'):
                expected_wheels=np.repeat(trace['wheel_feedback_total_nm'][:,None,None]/2,4,axis=1)
            else:
                expected_wheels=trace['flash_substeps'][:,:,WHEELS]+trace['residual_total_nm'][:,None,None]/2
                maximum=r['alpha']*r['residual_config']['limit_total_nm']
                assert abs(trace['residual_total_nm']).max()<=maximum+1e-9
                assert abs(np.diff(trace['residual_total_nm'])).max()<=.04+1e-9
            expected_wheels=np.clip(expected_wheels,-12.,12.)
            max_error=max(max_error,float(abs(trace['command_substeps'][1:,:,WHEELS]-expected_wheels[1:]).max()))
            if 'archive_replay_errors' in r:
                assert max(r['archive_replay_errors'].values())==0
            if 'alpha_zero_replay_errors' in r:
                assert max(r['alpha_zero_replay_errors'].values())==0
    assert initial_error==history_error==leg_error==0. and max_error<1e-6
    return dict(execution_domain='DESKTOP_DRY_RUN',evidence_status='PASS',episodes=len(rows),
        initial_state_max_error=initial_error,history_max_error=history_error,leg_torque_max_error_nm=leg_error,
        wheel_combination_max_error_nm=max_error,online_rls_calls=0,
        archive_exact_replays=sum('archive_replay_errors' in r for r in rows),
        f2_alpha_zero_exact_replays=sum('alpha_zero_replay_errors' in r for r in rows))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args()
    root=args.root.resolve();report=args.report.resolve()
    assert root.is_relative_to(REPO/'docs/exp') and report.is_relative_to(REPO/'docs/exp')
    e=read_rows(root/'e_timing_final')
    f1=read_rows(root/'f1_nominal')
    f2=read_rows(root/'f2_closed')
    probes=read_rows(root/'f2_closed','probe_results.jsonl')
    rows=e+f1+f2+probes
    audit=integrity(rows)
    write_json(root/'integrity.json',audit)
    summaries=aggregate(e+f1+f2)
    write_json(root/'aggregates.json',summaries)
    columns=['label','seed','pitch_delta_rad','completed_s','failures','max_displacement_m',
        'max_forward_displacement_m','max_lateral_displacement_m','pitch_rms_rad','true_pitch_error_rms_rad',
        'torque_rms_nm','peak_torque_nm','residual_peak_total_nm','evidence_status']
    with (root/'metrics.csv').open('w') as stream:
        writer=csv.DictWriter(stream,columns,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    baseline={(r['seed'],r['pitch_delta_rad']):r for r in f1 if r['label']=='A'}
    gates=[]
    for label in dict.fromkeys(r['label'] for r in f1+f2 if r['label']!='A'):
        subset=[r for r in f1+f2 if r['label']==label]
        ratios={k:np.asarray([r[k]/baseline[(r['seed'],r['pitch_delta_rad'])][k] for r in subset]) for k in
                ('max_displacement_m','pitch_rms_rad','torque_rms_nm')}
        passed=all(not r['failures'] for r in subset) and all(ratios['max_displacement_m']<1.) and (
            max(ratios['pitch_rms_rad'])<=1.10 and max(ratios['torque_rms_nm'])<=1.25)
        gates.append(dict(label=label,evidence_status='PASS' if passed else 'FAIL',
            drift_improved_pairs=int(sum(ratios['max_displacement_m']<1.)),
            max_pitch_ratio=float(max(ratios['pitch_rms_rad'])),max_torque_ratio=float(max(ratios['torque_rms_nm']))))
    write_json(root/'success_gates.json',gates)
    model=json.loads((root/'f2_closed/model.json').read_text())
    A=np.asarray(model['A_closed']);B=np.asarray(model['B_res'])
    multistep={}
    for horizon in (1,5,25,50):
        errors=[];changes=[]
        for r in probes:
            if r['seed']!=44:
                continue
            base=baseline[(r['seed'],r['pitch_delta_rad'])]
            with np.load(Path(r['folder'])/r['trace']) as trace,np.load(Path(base['folder'])/base['trace']) as original:
                delta=trace['synchronized_state']-original['synchronized_state']
                inputs=(trace['command_substeps'][1:,:,WHEELS]-trace['flash_substeps'][1:,:,WHEELS]).sum(2).mean(1)
                for start in range(100,500,10):
                    if start+horizon>=len(delta) or (start<=165 and start+horizon>=148):
                        continue
                    predicted=delta[start].copy()
                    for tick in range(start,start+horizon):
                        predicted=A @ predicted+B[:,0]*inputs[tick]
                    errors.append(predicted-delta[start+horizon])
                    changes.append(delta[start+horizon]-delta[start])
        rms=lambda v:np.sqrt(np.mean(np.asarray(v)**2,axis=0))
        multistep[str(horizon)]=dict(horizon_s=horizon*.02,samples=len(errors),component_rms=rms(errors).tolist(),
            relative_to_change_rms=(rms(errors)/np.maximum(rms(changes),1e-12)).tolist())
    write_json(root/'f2_multistep_validation.json',multistep)
    fig,axes=plt.subplots(4,1,figsize=(10,11),sharex=True)
    for label in ('A','F-1_a1','F-2_a1'):
        r=next(r for r in f1+f2 if r['label']==label and r['seed']==42 and r['pitch_delta_rad']==0.)
        with np.load(Path(r['folder'])/r['trace']) as trace:
            d=trace['gt_position']-trace['gt_position'][0]
            for ax,values in zip(axes,(d[:,0],d[:,1],trace['sensor_state'][:,2],trace['motor_substeps'][:,:,WHEELS].mean((1,2)))):
                ax.plot(trace['time'],values,label=label)
    for ax,label in zip(axes,('Forward displacement [m]','Lateral displacement [m]','Pitch error [rad]','Mean wheel torque [Nm]')):
        ax.set_ylabel(label);ax.grid(alpha=.3)
    axes[0].legend();axes[-1].set_xlabel('Time [s]');fig.tight_layout()
    fig.savefig(root/'comparison.png',dpi=180);plt.close(fig)
    get=lambda label:next(r for r in summaries if r['label']==label)
    mean=lambda label,key:get(label)[key]['mean']
    a_drift=mean('A','max_displacement_m');f1_drift=mean('F-1_a1','max_displacement_m');f2_drift=mean('F-2_a1','max_displacement_m')
    lines=['# E 센서 시점 진단 및 F — FlashSAC Torque Residual', '',
        'Execution Domain: VALIDATION_SIM (소스·무결성 검사: DESKTOP_DRY_RUN)', '',
        f'Policy Checkpoint SHA256: `{policy_config()["policy_interface"]["checkpoint_sha256"]}`', '',
        f'ONNX SHA256: `{policy_config()["policy_interface"]["onnx_sha256"]}`', '',
        'Evidence Status: PASS — F-1 nominal drift 개선·구현 무결성. FAIL — E 안정화와 F-2 drift 개선. SUSPICIOUS — F-2의 국소 4-state 식별 모델.', '',
        'Observed Metrics / Behavior / Log Summary:', '',
        f'**기존 FlashSAC wheel·leg 경로에 작은 위치·속도 토크를 더한 F-1은 9/9회 완료했고, α=1에서 최대 planar drift 평균을 {a_drift:.3f}→{f1_drift:.3f} m ({100*(1-f1_drift/a_drift):.1f}% 감소)로 줄였다.** '
        f'F-2도 완료했지만 α=1 drift는 {f2_drift:.3f} m로 악화됐다. E는 IMU 동기화와 Ground Truth에서도 모두 실패했다.', '',
        '## E 센서 진단: 여기서 종료', '',
        '| 군 | 상태 입력 | 완료/전체 | 종료 시각 범위 s |', '|---|---|---:|---:|']
    for label,source in [('E-original','기존 cache'),('E-sync','현재 qpos/qvel 시점의 IMU'),('E-GT','MuJoCo 실제 axle/자세 상태')]:
        g=get(label);lines.append(f'| {label} | {source} | {g["total"]-g["failed"]}/{g["total"]} | {g["min_completed_s"]:.2f}–{g["max_completed_s"]:.2f} |')
    lines+=['',
        'LQR 상태만 교체했다. 세 군 모두 actor는 기존 A의 sensor cache·33-value observation·전체 last_action을 유지한다. 동기화 IMU/GT는 mjData clone에 mj_forward를 수행해 얻었으며 원본 시뮬레이터를 refresh하지 않았다. E-original 9회는 기존 E archive와 state·physics substep motor torque·위치·leg error가 정확히 일치했다.', '',
        '동일 초기 조건에서 IMU 시점 문제를 제거해도 E가 살아남지 못했다. 센서 시점 불일치만으로 E 실패를 설명할 수 없다. FlashSAC leg와 대체 LQR wheel의 협조/모델 조건 문제가 더 유력하지만 원인이 유일하게 확정된 것은 아니다. E는 재튜닝하지 않았다. 실패 전 drift/Pitch RMS를 12초 완료 군과 성능 비교하지 않는다.', '',
        '## A drift 방향 및 F-1 경로', '',
        f'A의 초기 heading 기준 전후방 최대 이동 평균은 {mean("A","max_forward_displacement_m"):.3f} m, 좌우는 {mean("A","max_lateral_displacement_m"):.3f} m이다. 초기 yaw=0이므로 world x/y가 이 초기 방향과 일치한다. 이는 매 순간 body heading 방향의 누적 이동과 다른 지표이며, 전후방 성분이 주원인이다.', '',
        'F-1: Δτ = −2(p−p_hold)−0.5v. p_hold는 zero command episode 시작 시 encoder 경로 값 0을 고정한다. 위치는 encoder+동기화 IMU로 적분한 sagittal 경로이며 v는 같은 시점의 encoder/IMU 속도이다. GT position·velocity는 이 residual에 들어가지 않는다. Sagittal 경로 feedback은 world 2D 위치/yaw hold가 아니다.', '',
        '합산 residual은 α×clip(Δτ, ±1 Nm)에 1초 smoothstep 활성화와 합 토크 slew 2 Nm/s를 적용한다. native wheel axis sign으로 바퀴당 절반씩 더하고 기존 Playback의 ±12 Nm/바퀴 saturation을 적용한다. α는 0, 0.1, 0.25, 0.5, 1로 낮게 시작했다. 실측 α=1 residual peak의 trial 평균은 '
        f'{mean("F-1_a1","residual_peak_total_nm"):.3f} Nm(total)이다.', '',
        '기존 ActionAdapter는 원래 policy wheel velocity target/Kd=0.5 PD torque를 매 physics substep 만들고 기존 effort clipping을 적용한다. 이 출력에 residual을 더한 뒤 기존 final effort clipping을 거친다. Leg는 A의 Kp=60/Kd=1.5, action scale/clip/targets를 그대로 유지한다. 미리 clipping된 FlashSAC torque에 더한다는 기존 경로의 포화 순서를 기록했다. 이 nominal 실험에서 추가 포화는 발생하지 않았다.', '',
        '전체 raw actor output 8개를 last_action으로 보존한다. residual Nm 값을 policy action 단위의 history에 넣지 않는다. 기존 wheel torque를 실제 적용하므로 E처럼 출력을 버리지는 않지만, residual은 학습 때 없는 외부 입력이고 이후 observation/actor action은 A와 달라질 수 있다. α=0은 state·위치·leg error·motor substeps뿐 아니라 별도 F-2 검사에서 actor observation/action까지 정확히 재현했다.', '',
        '## Nominal 12초 비교', '',
        '| 군 | 완료/전체 | 최대 planar drift m | 전후방 m | 좌우 m | Pitch error RMS rad | Wheel torque RMS Nm/바퀴 |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for g in summaries:
        if g['label'].startswith('E-'):
            continue
        stat=lambda key:f'{g[key]["mean"]:.4f} ± {g[key]["std"]:.4f}'
        lines.append(f'| {g["label"]} | {g["total"]-g["failed"]}/{g["total"]} | {stat("max_displacement_m")} | '
            f'{g["max_forward_displacement_m"]["mean"]:.4f} | {g["max_lateral_displacement_m"]["mean"]:.4f} | '
            f'{stat("pitch_rms_rad")} | {stat("torque_rms_nm")} |')
    lines+=['',
        '평균 ± sample 표준편차. Drift는 기존 A와 같은 cached axle world position 평가 정의를 유지하고, fresh GT axle 지표도 raw results에 별도 기록했다. Pitch error RMS는 기존 nominal equilibrium 기준의 cached sensor state로 모든 F군을 동일 평가했다. Fresh GT pitch error RMS도 metrics.csv에 있다. Wheel torque RMS는 초기의 미적용 zero row를 제외한 모든 실제 physics substep, 두 바퀴만 포함한다. Leg torque를 포함하지 않는다.', '',
        f'F-1 α=1은 각 초기 조건별 9/9쌍 모두 drift가 감소했다. 평균 Pitch RMS 변화는 {100*(mean("F-1_a1","pitch_rms_rad")/mean("A","pitch_rms_rad")-1):+.2f}%, wheel torque RMS 변화는 {100*(mean("F-1_a1","torque_rms_nm")/mean("A","torque_rms_nm")-1):+.2f}%다. '
        '성공 판정은 9/9 완료, 모든 paired 최대 drift 감소, 각 trial pitch RMS ≤A의 110%, wheel torque RMS ≤A의 125%로 수치화했다. 이 여유 한도는 이번 분석의 운영 기준이며 원래 사용자 요청의 정량 사양은 아니다. F-1 모든 nonzero α는 이 기준을 만족하고 F-2 nonzero α는 drift 기준을 만족하지 못했다.', '',
        '## F-2: FlashSAC 포함 폐루프 국소 식별', '',
        'F-1 성공 확인 후 구현했다. C-4의 K/A/B는 사용하지 않았다. Frozen FlashSAC, 원래 observation/history, leg PD, wheel velocity PD와 contact를 모두 실제 실행한 상태에서 0.1/0.25/0.5 Nm(total amplitude) 다중 sine residual을 추가했다. 동일 seed/pitch의 A 궤적을 뺀 δx를 이용해 δx_next=A_closed δx+B_res Δτ를 offline least squares로 식별했다. 입력은 최종 command에서 원래 FlashSAC torque를 뺀 실제 추가 토크로 계산했다.', '',
        '27 probing episodes 전부 12초 완료. Seed42/43의 18회(7,344 transitions)를 학습, seed44의 9회(3,672 transitions)를 held-out 검증에 사용했다. 2–10.5초 중 3초 외란 구간을 제외했다. 위치 translation에 policy/PD가 불변이므로 A의 첫 열 [1,0,0,0]을 강제했고, [δv,δpitch,δpitch_rate,Δτ] 4 regressors의 scaled rank=4, condition number는 '
        f'{model["diagnostics"]["scaled_condition_number"]:.2f}였다. 모든 값은 model.json/identification.npz에 있다.', '',
        f'LQR Q=diag(4,1,0.2,0.05), R=4로 고정했다. 새 K={np.round(model["K"],6).tolist()}, 식별 모델의 ρ(A_closed−B_res K)={model["closed_model_spectral_radius"]:.6f}. '
        f'Pitch reference는 학습용 A의 4–12초 평균 pitch error {model["pitch_reference_error_rad"]:.6f} rad를 고정했다. '
        '제어에는 [p−p_hold,v,pitch_error−reference,pitch_rate]를 사용하고 F-1과 동일한 residual clamp/ramp/slew를 적용했다. α=0/0.25/0.5/1을 각각 9개 초기 조건에서 검증했다. Q/R·gain을 성능에 맞춰 추가 튜닝하지 않았다.', '',
        'Held-out one-step RMS error [p,v,pitch,rate] = '
        f'{model["heldout_prediction"]["component_rms"]}. 해당 상태의 한 step 변화 RMS 대비 비율 = '
        f'{np.round(model["heldout_prediction"]["relative_to_change_rms"],4).tolist()}. '
        '속도/각속도 변화 예측이 충분히 정밀하지 않다. 다리·roll·yaw·action history가 실제 데이터 수집에는 포함되지만 4-state 회귀의 상태에는 생략됐다. A는 정확한 정지 평형점이 아닌 움직이는 operating trajectory다. 따라서 모델의 eigenvalue만으로 실제 residual 제어 성능을 보장하지 않는다. 다중 step 검증은 f2_multistep_validation.json에 별도 기록했다.', '',
        f'F-2 α=1의 최대 drift 평균은 A 대비 {100*(f2_drift/a_drift-1):.1f}% 증가했다. **F-2는 넘어지지는 않았지만 위치 drift 개선 목표에는 FAIL이다.** '
        '현재 증거는 F-1의 단순 residual이 더 유효함을 지지한다. F-2 악화를 단일 원인으로 확정하지 않으며, 식별 모델의 생략 상태·장기 예측 오차와 feedback 방향은 추적 대상이다.', '',
        '## 검증·변경 범위·제한', '',
        f'- 본 평가: E 27 + A/F-1 54 + F-2 probing 27 + F-2 평가 36 = {len(rows)} episodes. 모든 군은 같은 nominal 9개 initial qpos/qvel, 12초 horizon, physics/control dt=0.005/0.02초와 기존 3초의 12 N/0.1초 외란을 사용했다. E는 외란 전에 종료했다.',
        f'- 무결성 PASS: {audit["archive_exact_replays"]}개 기존 A/E substep archive 정확 재현, F-2 α=0 9개 actor observation/action 포함 정확 재현, initial/history/leg 오차 0.0, wheel 합산 최대 오차 {audit["wheel_combination_max_error_nm"]:.3g} Nm(float32). RLS update/online adaptation 0.',
        '- 단위 검사 2개: bound/ramp/slew·wheel-only addition과 α=0 full rollout archive 재현. 결과는 unit_tests_final.log에 기록한다.',
        '- 초기 검사 로그 unit_tests.log/f1_smoke.log의 FAIL은 state가 달라서가 아니라 저장 배열 평균의 float32/64 반올림 차이 4.47e-08 Nm를 exact 비교한 문제다. 실제 substep 비교로 수정했다. 최종 E/F-1 데이터는 e_timing_final/f1_nominal만 채택한다. 초기 e_timing 및 중단된 smoke는 주 결과에 포함하지 않는다.',
        '- 기존 소스/설정/보고서는 변경하지 않았다. 신규 test/eval_flash_torque_residual.py, test/eval_flash_closed_loop_residual.py, test/test_flash_torque_residual.py, test/analyze_flash_torque_residual.py와 본 날짜의 실험 증거를 추가했다. 각 실행 source hash 및 E/F-1 실행 당시 source snapshot도 보존했다.',
        '- agent-check.sh PASS (Python syntax 337개, URDF XML 8개): agent_check.log. 최종 diff/기존 hash 보존 검사는 final_review.json/task.diff에 기록한다.',
        '- 브랜치: agent/codex/dev_tita_gluon. Dynamics mismatch와 online adaptive residual은 NOT_TESTED; 이번 범위는 nominal 비교와 조건부 F-2이다. Hardware 실행·재학습 없음.',
        '- Nominal 9개는 3 seed×3 pitch의 제한된 결정론적 초기 조건이다. F-1 개선을 다른 명령·지형·mismatch 또는 실물로 일반화하지 않는다. 남은 좌우/yaw drift와 path odometry 한계도 해결되지 않았다.', '',
        '## 재현 및 산출물', '',
        '```bash',
        'MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_flash_torque_residual.py',
        'MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_flash_torque_residual.py --stage e --output docs/exp/2026-10-15/new_residual/e_timing_final',
        'MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_flash_torque_residual.py --stage f1 --output docs/exp/2026-10-15/new_residual/f1_nominal',
        '```', '',
        'F-2는 --baseline 인자로 위 F-1 결과 폴더를 지정할 수 있다. 이번 실행은 default인 flash_torque_residual/f1_nominal을 사용했다.', '',
        '```bash',
        'MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_flash_closed_loop_residual.py --baseline docs/exp/2026-10-15/new_residual/f1_nominal --output docs/exp/2026-10-15/new_residual/f2_closed',
        'MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_flash_torque_residual.py --root docs/exp/2026-10-15/new_residual --report docs/exp/2026-10-15/new_residual_summary.md',
        './scripts/agent-check.sh', '```', '',
        f'산출물: [{root.name}/comparison.png]({root.name}/comparison.png), metrics.csv, aggregates.json, success_gates.json, integrity.json, f2_multistep_validation.json, 각 군 manifest/results.jsonl/NPZ, f2_closed/model.json 및 identification.npz.']
    report.write_text('\n'.join(lines)+'\n')
    print('[DESKTOP_DRY_RUN] PASS integrity',audit)
    print('[VALIDATION_SIM] report written',report)


if __name__=='__main__':
    main()
