# Stop-hold residual torque 제한 비교

Execution Domain: VALIDATION_SIM (소스/동등성 검사: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: PASS — 제한값 비교4회 완료 및 ±2 Nm 후보의 잔류 속도 개선. FAIL — 정지 위치 복귀 목표. SUSPICIOUS — 단일 seed/근사 조작 이력의 일반화. Hardware: NOT_TESTED.

Observed Metrics / Behavior / Log Summary:

**다음 MuJoCo 시험의 residual 제한 후보는 합 토크 ±2 Nm, 바퀴당 추가분 ±1 Nm를 권장한다.** ±1.5 Nm에서도 개선됐으나 후반 포화가 남았고, ±2 Nm에서는 포화가 없어졌다. ±3 Nm는 이 조건에서 ±2 Nm와 전체 trace가 정확히 같아 추가 이득이 없었다. 현재 수동 조작 viewer의 제한은 변경하지 않았다.

## 비교 조건

Nominal seed42, 동기화 IMU actor, 동일 초기 상태/근사 수동 조작 이력: 초기정지 → 후진(-0.1) → 정지 → 전진(+0.1) → 정지 → 후진(-0.1)+회전(+0.15) → 62.26초부터 최종정지. 총160초. 이전 stop_hold_drift_diagnosis의 이력과 같으며 yaw 시작 시각은1초 해상도 로그에 근거한 근사다.

Residual 합 토크 제한만 ±1/1.5/2/3 Nm로 변경했다. kp=2, kv=0.5, stop command hysteresis, 1초 smoothstep ramp, 합 slew2 Nm/s, 전체 raw last_action, FlashSAC leg/wheel PD와 최종±12 Nm/바퀴 effort clipping은 동일하다. 센서 추정 p/v만 residual에 사용하고 GT는 평가용이다. 바퀴당 보정은 native sign을 적용한 합 residual의 절반이다.

## 결과: 각 제한당1회, 4/4회160초 완료

| 합 residual 제한 ±Nm | 바퀴당 추가분 한도 ±Nm | 마지막20초 실제 속도 평균 mm/s | 최종정지 이후 최대 planar 이동 m | 전체 pitch error RMS rad | 전체 wheel torque RMS Nm/바퀴 | 후반 residual 포화 비율 |
|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | 0.50 | 5.327 | 1.1081 | 0.090383 | 0.344903 | 100% |
| 1.5 | 0.75 | 1.603 | 0.7954 | 0.090351 | 0.344498 | 100% |
| 2.0 | 1.00 | 0.822 | 0.7774 | 0.090343 | 0.344483 | 0% |
| 3.0 | 1.50 | 0.822 | 0.7774 | 0.090343 | 0.344483 | 0% |

최종정지는62.26초이며 최대 planar 이동은 해당 시점 axle world position으로부터160초까지의2D 변위 크기다. 마지막20초 속도는140≤t<160의 GT sagittal 평균이다. 전 구간 RMS는0≤t≤160이며 wheel torque는 두 바퀴의 모든 physics substep이다(초기의 미적용 zero row 포함, 군 간 정의 동일). 전 구간 peak wheel torque는 모든 군5.14203 Nm/바퀴로 같았다.

±2 Nm의 drift 개선은 ±1 Nm 대비 약29.8%, 마지막 구간 잔류 속도 감소는84.6%다. Pitch RMS와 실제 wheel RMS가 악화되지 않았다. 하지만62.26초 정지점에서 약0.78 m 벗어난 위치가 남아 있으므로 정지 위치 유지 성공으로 판정하지 않는다. 0.822 mm/s 역시 정확한0은 아니다.

±2/3 Nm의 실제 residual peak는 합 토크1.55433 Nm였다(summary.json). 두 군은 raw PD 요구량이 ±2 Nm에 도달하지 않아 제한을 더 늘려도 입력이 같았다. 따라서 이 조건에서 ±3 Nm를 선택할 근거는 없다. Gain은 고정이므로 제한을 늘려도 포화 전의 초기 정지 응답/제동 강도가 직접 커지지는 않는다. 잔류 drift와 위치 복귀를 개선하려면 제한 증대의 효과와 kp/kv·정지 전환 제동을 구분해 후속 검증해야 한다. 이번에는 후속 구조나 gain을 추가하지 않았다.

## 검증 및 변경 범위

신규 test/eval_stop_residual_limits.py와 이 보고서·residual_limit_sweep/ 증거만 추가했다. BoundedStopHold는 기존 gate/estimator/activation을 사용하고 제한만 교체한다. 600개의 synthetic sensor step에서 limit1은 기존 StopHold의 출력과 진단 dict를 정확히 재현했다: unit_check.log. Limit1의160초 trace는 이전 진단의 time/GT/position/rpy/command/residual/relative_p와 정확히 일치했다: baseline_reproduction.json. Limit2/3 전체 NPZ 필드도 정확히 일치했다. 잔차 제한·slew·leg torque 무변경·전체 raw last_action 보존을 매 실행 확인했다. 근거: screen/results.jsonl, summary.json, 각 NPZ와screen.log.

agent-check.sh 결과는 agent_check.log, 최종 diff/기존 파일 보존은 final_review.json 및 task.diff에 기록한다. 브랜치: agent/codex/dev_tita_gluon.

이 추천은 단일 nominal seed/한 조작 이력에서의 다음 시뮬레이션 시험값이다. 다른 yaw/속도/초기 자세/마찰·질량·motor mismatch와 hardware에서의 허용 범위는 NOT_TESTED다. 모터 effort limit12 Nm와 residual 추가 제한은 다른 값이며,12 Nm 사양만으로 residual 증대의 안정성을 보장하지 않는다.

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_stop_residual_limits.py --output docs/exp/2026-10-15/new_residual_limits/screen
```
