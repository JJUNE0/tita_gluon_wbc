# Stop residual kv / activation ramp ablation

Execution Domain: VALIDATION_SIM (무결성/분석: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: PASS — 53개 조합 탐색·추가 조건 검증 및 종합 위치 오차 개선. FAIL — 보편적인 zero-velocity 정지/원점 복귀. SUSPICIOUS — 목적함수·평가 horizon에 따른 최적값 의존성. 실기: NOT_TESTED.

Observed Metrics / Behavior / Log Summary:

**시험한 범위의 추천 절충안은 kp=2, kv=24, residual 활성화 ramp=1.5 s, 합 residual ±2 Nm, 합 slew 2 Nm/s다.** 고정된 종합점수 기준으로 53개 탐색 조합 중 최저이며, 새로운 초기 조건의20개 paired 검증에서도 평균 점수가 가장 낮았다. 다만 kv를 키우면 미세 진동과 일부 구간의 잔류 속도가 증가한다. 위치 밀림을 줄이는 후보이지 완전 정지를 해결한 계수는 아니다. 현재 수동 viewer의 기존0.5/1초 설정과 소스는 변경하지 않았다.

## 제어와 탐색 범위

FlashSAC wheel/leg 및 전체 raw last_action, 동기화 actor IMU, 기존 wheel velocity PD/leg PD를 유지했다. StopHold의 command gate와 stop 진입 시 encoder/IMU odometry를1회0으로 재설정하는 경로도 동일하다. GT 상태는 평가에만 사용했다.

정지 시 raw residual은 -2p-kv*v, smoothstep 활성화 후 ±2 Nm 제한과2 Nm/s slew를 유지한다. 정확한 순서는 `target = smoothstep(min(hold_age/ramp_s,1)) * clip(-2p-kv*v, -2, 2)`이며 target을 slew한다. ramp=0이면 즉시 활성화하되 slew는 유지한다. 바퀴당 native sign을 적용해 절반씩 합산한 뒤 기존±12 Nm/바퀴 clipping을 적용한다. 여기서 ramp는 **residual 활성화 ramp**이며 속도 명령 ramp가 아니다. 속도 명령은 기존 step 방식이다.

1. Screen: kv=[0,0.5,2,4,8,16,32], ramp=[0,0.25,1,2]의28조합×3 command=84회.
2. Refine: kv=[24,48,64,128], ramp=[1,1.5,2,3]의16조합×3=48회.
3. Zoom: kv=[20,28,32], ramp=[1.25,1.5,1.75]의9조합×3=27회.
4. 새 초기 조건 검증: baseline0.5/1초, 후보24/1.5초, 대안28/1.75초 각각 seed43/44×pitch[-0.035,0,+0.035]×3 command=54회.
5. 긴 조작 이력 검증: 위3설정×(seed43,pitch+0.035)/(seed44,pitch-0.035)=6회×160초.
6. 소스/경로 검증용 baseline40초 smoke1회. **총220회**, 성능 비교219회. 모두 낙상/실패 guard 없이 요청 horizon을 완료했다. 이는 정지 성능 성공 판정과 다르다.

짧은 시험은 초기2초 정지, 2–7초 drive, 7–40초 정지다. Drive는 전진+0.2, 후진-0.2, 후진-0.1+yaw+0.15의3종이다. Screen/Refine/Zoom은 seed42/pitch0이다. 긴 시험은 이전 사용자 조작 로그의 근사 이력(12–18.98초 후진,32.02–39.70초 전진,53.12–62.26초 후진,55.98–62.26초 yaw+0.15, 이후 정지)이며 exact live replay가 아니다. 모든 군 동일 physics/control dt=0.005/0.02초, nominal 접촉/모터 조건, 외란 없음. Episode 초기 qpos/qvel은 같은 seed/pitch 쌍에서 hash가 일치했다. 앞선 HOLD의 영향으로 정지 직전 상태는 설정마다 달라질 수 있다.

## 평가 기준

결과를 보기 전에 manifest에 기록한 각 trial의 종합점수는 다음과 같다. 작을수록 좋다.

`score = mean(planar error) + 0.5*max(planar error) + 0.5*reverse excursion + 5*tail velocity RMS`

Planar error는 마지막 정지 명령 시점의 axle world xy로부터의 변위 크기다. Reverse excursion은 정지 당시 heading에 투영한 이동 중, 직전 drive 방향의 반대쪽으로 넘어간 최대 거리다. 긴 시험의 마지막 drive는 후진으로 분류한다. 이는 현재 heading에 따른 encoder 누적 path와 다른 지표다. Tail velocity RMS는 마지막10초 GT sagittal 속도다. Mean score는 각 episode에 동일 가중치를 준다. 점수와 가중치는 이번 운영상의 선택이며 사용자 지정 사양이나 보편적인 물리 최적성 기준이 아니다.

후보 조건은 전 episode 완료, paired baseline 대비 정지 구간 pitch error RMS≤110%, pitch rate RMS≤125%, 전체 wheel torque RMS≤125%다. 이 허용폭은 시험 전에 정한 운영 기준이다. 탐색53조합 중34조합이 이 기준을 충족했다. 큰 kv/짧은 ramp는 drift 점수가 좋아도 후진 시 wheel torque 또는 pitch rate 기준을 초과하는 경우가 있었다.

## 한 요인 비교와 추천값

| kv | ramp s | 탐색 평균 score | 제약 충족 |
|---:|---:|---:|---|
| 0.5 | 1.0 | 0.608744 | PASS |
| 24 | 1.0 | 0.494668 | FAIL — 후진 wheel RMS 기준 초과 |
| **24** | **1.5** | **0.499954** | **PASS** |
| 24 | 2.0 | 0.506681 | PASS |
| 24 | 3.0 | 0.515593 | PASS |
| 28 | 1.75 | 0.507472 | PASS |

kv24만 적용하고1초 ramp를 유지하는 것과24/1.5초는 구분해야 한다. 더 긴1.5초 activation이 torque 과도를 줄여 허용 기준을 만족했다. Gate를 무시하면 더 낮은 점수가 있는 조합도 있으므로 무제약 최저와 다르다. 연속적인 전체 계수 공간의 전역 최적값을 구한 것은 아니다.

## 새 초기 조건: 각 설정18회 평균

| 설정 kv/ramp s | score | 최대 planar 이동 m | 반대 방향 최대 이동 m | 마지막10초 속도 RMS mm/s | Pitch RMS rad | Wheel RMS Nm/바퀴 |
|---|---:|---:|---:|---:|---:|---:|
| 0.5 / 1 | 0.609084 | 0.391169 | 0.197230 | 3.324 | 0.094106 | 0.335870 |
| **24 / 1.5** | **0.499778** | **0.337726** | **0.128122** | **5.405** | **0.094036** | **0.356135** |
| 28 / 1.75 | 0.507445 | 0.329148 | 0.115576 | 9.898 | 0.094075 | 0.354098 |

24/1.5초는 baseline 대비 score17.95%, 최대 planar 이동13.66%, 반대 방향 최대 이동35.04% 감소했다. Pitch error RMS 변화-0.07%, pitch rate RMS+6.88%, wheel RMS+6.03%다. **잔류 속도 RMS는62.62% 증가했다.** 위치 오차가 작다는 사실과 더 빨리 완전히 멈춘다는 주장을 혼동하지 않는다. 일부 미세 주기 응답과 늦은 수렴이 남는다.

방향별 탐색 대표값(seed42): 전진 후 반대 방향 최대 이동0.436→0.285 m, 후진 후 최대 planar 이동0.500→0.481 m. 회전 후 최대 planar 이동은0.191→0.194 m로 소폭 악화됐으나 반대 방향 이동은0.154→0.100 m로 줄었다. 모든 drift 지표가 일괄 개선된 것은 아니다.

## 긴160초 조작 이력: 각 설정2회 평균

| 설정 kv/ramp s | score | 최종정지 이후 최대 planar 이동 m | 마지막10초 속도 RMS mm/s |
|---|---:|---:|---:|
| 0.5 / 1 | 1.399769 | 0.777389 | 0.791 |
| 24 / 1.5 | 1.318574 | 0.755506 | 1.085 |
| 28 / 1.75 | 1.295393 | 0.745570 | 1.186 |

긴 이력에서는28/1.75초가 위치 오차/점수에 더 유리하다. 24/1.5초의 최대 이동 감소는2.82%에 그치고 잔류 속도는37.13% 증가했다. **Gain/ramp 조정만으로 원점 복귀와 완전 정지를 해결하지 못했다.** 포화 비율은 세 설정 모두0이다. 따라서 이번 후보의 남은 오차를 torque 한도 부족만으로 설명할 수 없다.

18개 짧은 조건과2개 긴 조건을 동일하게 가중한20개 검증의 평균 score는 baseline0.688152,24/1.5초0.581657,28/1.75초0.586240이다.24/1.5초가15.48% 개선되고20/20 paired score가 감소했다. 최대 planar 이동은14/20, 반대 방향 이동은14/20에서 감소했고, tail 속도 RMS는6/20에서만 감소했다. 전체20개 평균 최대 이동은11.70%, 반대 방향 이동은25.24% 감소했지만 tail 속도 RMS는61.96% 증가했다.

가중치 민감도도 남겼다. 짧은/긴 horizon을 각각 baseline으로 정규화해50:50으로 합치면28/1.75초가 약간 더 좋다. 이 대안 가중 규칙은 long 결과3개가 이미 파일에 생긴 뒤 기록한 **사후 민감도 분석**이며 사전 등록 기준이라고 주장하지 않는다(final_selection_plan.json). 추천24/1.5초는 원래 episode별 score 평균 및28보다 작은 잔류 속도/낮은 gain을 고려한 절충안이다. 보편적으로 유일한 최적값은 아니다. 잔류 속도를 악화시키지 않는 것이 필수라면 이 후보는 그 요구를 충족하지 못한다. Screen의0.5/ramp0~0.25초는 잔류 속도를 유지하면서 점수가 약0.2% 좋아지는 정도였으며 추가 초기 조건에서는 검증하지 않았다.

## 구현·검증·산출물

- 신규 test/eval_stop_kv_ramp.py: TunedStopHold와 병렬 headless evaluator. 기존 StopHold의 gate/encoder estimator를 그대로 사용하고 kv/ramp만 교체한다. 기존 소스/설정/GUI는 유지했다.
- 신규 test/analyze_stop_kv_ramp.py: paired 초기 상태/운영 기준 검사와 순위 계산.
- 1500 sensor step에서0.5/1초가 기존±2 Nm StopHold의 출력/진단 dict와 정확히 일치했다. Saturation/release/hold re-entry 포함: controller_test.log.
- Smoke40초는 기존 residual_limit_sweep limit2_s42의 time/GT/rpy/position/command/residual/relative_p 및 모든 physics substep motor torque와 정확히 일치했다: baseline_reproduction.json.
- 모든220회 source hash·입력 snapshot 일치, residual≤2 Nm, slew≤2 Nm/s, wheel≤12 Nm, leg torque 변경0, wheel 합산 오차<1e-6 Nm, 전체 raw last_action 보존 확인: integrity.json. 모든 paired 초기 hash는 분석기에서 검사했다.
- 각 stage inputs.json/manifest.json/results.jsonl/NPZ, metrics.csv, search/validation/long/combined_validation_ranking.json, summary.json 및 best_settings.json에 수치와 추천값을 기록했다.
- 최종 agent-check 결과는 agent_check.log, task diff/기존 변경 보존은 final_review.json/task.diff에 기록한다. 브랜치 agent/codex/dev_tita_gluon. 커밋/배포/실기 실행/정책 재학습/online adaptation 없음.

[계수 탐색 heatmap](stop_kv_ramp_ablation/search_heatmap.png), [정지 후 위치·실제 속도 비교](stop_kv_ramp_ablation/search_response.png).

## 재현

아래STAGE를 smoke/screen/refine/zoom/validation/long으로 바꾸면 저장된 동일 design을 실행할 수 있다. 새로운 output 경로가 필요하다.

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_stop_kv_ramp.py --design docs/exp/2026-10-15/stop_kv_ramp_ablation/STAGE_design.json --output docs/exp/2026-10-15/new_stop_kv_ramp/STAGE --workers 3
PYTHONDONTWRITEBYTECODE=1 /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_stop_kv_ramp.py --results docs/exp/2026-10-15/stop_kv_ramp_ablation/validation docs/exp/2026-10-15/stop_kv_ramp_ablation/long --output docs/exp/2026-10-15/new_combined_ranking.json
./scripts/agent-check.sh
```

검증 범위는 nominal 평지·제한된3 command 및 근사 수동 이력이다. Dynamics mismatch, 추정기 bias/slip 다양성, 더 긴 episode, 실제 로봇 및 다른 정책의 최적 계수는 NOT_TESTED다.
