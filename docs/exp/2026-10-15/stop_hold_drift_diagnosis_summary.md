# 전후진·회전 후 정지 residual drift 진단

Execution Domain: VALIDATION_SIM (소스/무결성: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: FAIL — 현재 동기화 actor + F-1의 이동 후 정지 위치 유지. PASS — 진단 10회 완료·실제 drift 재현·토크/소스 무결성. 실기: NOT_TESTED.

Observed Metrics / Behavior / Log Summary:

**후진과 회전 후 정지하면 실제로 계속 움직이며 relative p도 증가하는 현상을 근사 조작 이력에서 재현했다. 단순 적분 오차로 설명되지 않는다.** 현재 GUI 정책/추정기/제어기/포화 제한은 변경하지 않았다.

## 실제 GUI 관찰 및 재현 범위

기존 live/run.log에는 초기 정지, vx=-0.1 (12–18.98 s), 정지, vx=+0.1 (32.02–39.70 s), 정지, vx=-0.1 (53.12–62.26 s), 마지막 이동 중 yaw=+0.15가 기록됐다. 62.26 s에 마지막 hold 진입, 약81 s부터 residual=-1 Nm에 포화됐다. 기록 당시 simulation201.98 s에도 command=[0,0,0], residual=-1 Nm였다. 기존 live telemetry에는 p/속도/GT가 없으므로 이 GUI의 정확한 drift 수치를 읽었다고 주장하지 않는다.

위 command 순서를 별도 headless에서 근사 재현했다. Hold 전환 시각은 event log를 사용하고 yaw 시작 시각은 1초 해상도 로그의 첫 관찰55.98 s를 사용했다. 따라서 exact GUI replay는 아니다. 동일 seed42/nominal 초기 조건, 동기화 actor, 기존 leg/wheel PD·전체 raw last_action, residual ±1 Nm 및2 Nm/s slew, 외부 push 없음. yaw가 없는 단일 전진/후진 비교8회×90 s와 근사 이력 hold/off2회×160 s를 실행했다.

## 마지막 정지 후: 근사 조작 이력

| 시간 구간 s | 군 | 실제 sagittal 속도 평균 m/s | 추정 속도 평균 m/s | residual 평균 Nm | 추정 relative p 구간 m | 실제 path 구간 m |
|---|---|---:|---:|---:|---:|---:|
| 70–90 | hold | 0.020106 | 0.020066 | -0.8290 | 0.193→0.593 | 0.193→0.594 |
| 100–120 | hold | 0.008426 | 0.008414 | -1.0000 | 0.707→0.875 | 0.708→0.876 |
| 140–160 | hold | 0.005327 | 0.005322 | -1.0000 | 1.001→1.108 | 1.003→1.109 |
| 140–160 | off | 0.012069 | 0.012050 | 0.0000 | 1.808→2.049 | 1.811→2.052 |

실제 path는 MuJoCo axle 변위를 heading에 투영한 누적 sagittal 경로이며 62.26 s를 원점으로 삼았다. World 2D 위치 오차와는 다르다. Hold의 마지막 구간 속도 추정 RMS 오차는4.41e-6 m/s이다. Residual은 drift를 줄이지만 제거하지 못했고, 20초 동안 약0.106 m 실제로 이동했다. 모든 실제 상태는 평가에만 사용하며 residual에는 encoder/IMU만 입력했다.

## 제어 해석

현재 제어는 sat(-2p-0.5v, ±1 Nm)와 ramp/slew다. p가 약+0.5 m이고 속도가 양수이면 이미 음의 residual 제한에 도달한다. 이후 p가 더 커져도 보정 크기가 증가하지 않는다. 이것은 포화 제한이 유지된 결과이며 위치값을 재설정하는 것으로 실제 움직임이 멈추지 않는다.

마지막140–160 s에서 FlashSAC wheel 경로의 signed 합 토크 평균은+0.99945 Nm, residual은-1 Nm, 실제 합은 약-0.00055 Nm였다. Actor/기존 velocity PD가 residual에 반응해 내는 토크와 상호작용하는 상태다. 평균 토크 상쇄만으로 정책이 의도적으로 residual을 거부한다고 해석하지 않으며, 역진자 균형에서 평균 순토크가 작을 수 있으므로 이 수치 단독으로 원인을 확정하지 않는다.

직선 방향 토크 검사에서 최종70–90 s 속도는 +1 Nm일 때 약+0.0123/+0.0125 m/s, -1 Nm일 때 약-0.0258/-0.0240 m/s였다(전진/후진 이력 순). 부호가 단순히 뒤집힌 additive 구현이라는 근거는 없다. 동일한 제한값에서도 상태 이력에 따라 응답이 달라진다. 토크 제한 증대, gain 재튜닝, integral, 정지 전환 제동 및 다른 residual 구조의 효과는 NOT_TESTED다.

IMU 동기화는 떨림을 줄였지만 FlashSAC 포함 폐루프 응답도 바꿨다. 기존 cached actor의 nominal zero-command F-1 성공을 동기화 actor의 이동/회전 후 정지 성능으로 일반화할 수 없다. 앞선32초 smoke PASS는 실패 없는 실행/합산 경로 검사이며 정지 위치 오차 수렴 보장이 아니었다. 이번 조건에서는 위치 유지 목표를 FAIL로 판정한다.

1D path residual은 yaw/좌우 위치를 제어하지 않는다. 관찰된 sagittal drift를 이 한계만으로 설명하지 않으며, yaw 입력의 인과 효과는 동일한 마지막 시각/이력에서 yaw만 제거한 쌍으로 아직 분리하지 않았다. 이번 결과는 한 seed의 제한된 진단이다.

## 변경과 검증

신규 test/debug_stop_hold_drift.py, 본 보고서와 stop_hold_drift_diagnosis/ 증거만 추가했다. 기존 viewer는 계속 실행하며 조작 상태를 건드리지 않았다. 10회 모두 넘어짐 없이 완료했지만 정지 성능 성공을 뜻하지 않는다. 잔차 제한/슬루 및 source hash 검사 PASS: integrity.json. 첫8회 당시 source는 full/source_snapshot.txt에 보존하고, 근사 이력 추가 후 source hash는 history/manifest.json에 기록했다.

agent-check.sh, 최종 diff 및 기존 변경 보존 결과는 agent_check.log, task.diff, final_review.json에 기록한다. 브랜치: agent/codex/dev_tita_gluon. Hardware 실행 없음.

[실제 경로·추정 위치·속도·토크 그래프](stop_hold_drift_diagnosis/history_stop_drift.png)

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/debug_stop_hold_drift.py --output docs/exp/2026-10-15/new_stop_drift/full
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/debug_stop_hold_drift.py --manual-history --output docs/exp/2026-10-15/new_stop_drift/history
```
