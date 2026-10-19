# TITA FlashSAC / Fixed / Adaptive LQR — 6군 ablation 결과

Execution Domain: VALIDATION_SIM (검사: DESKTOP_DRY_RUN)

Evidence Status: SUSPICIOUS — 구현·재현 gate는 검증됐으며, 제어 성능은 아래의 실패율과 측정값으로 판단한다.

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Observed Metrics / Behavior / Log Summary:

첨부 설계의 A, B, C-3, C-4, D-3, D-4를 구현하고 nominal 및 독립 mismatch 평가를 실행했다. 정책 재학습, Q/R 온라인 학습, 하드웨어 실행은 포함하지 않는다. 각 trial의 PASS는 정의한 시뮬레이션 한계 안에서 시간을 완료했다는 뜻이며, 정지 성능 개선을 뜻하지 않는다.

Nominal에서 C-4의 최대 planar drift는 C-3 대비 -2.210 ± 0.044 m 변했다. D-3 frozen은 C-3 대비 -0.723 ± 0.418 m 변했다. D-4 frozen은 6/9회 실패했으므로 완료 trial의 작은 drift만으로 우위를 주장할 수 없다.

Nominal 최대 drift에서는 FlashSAC A가 0.497 m로 C-4의 0.605 m와 D-3의 2.092 m보다 작다. LQR은 pitch error를 줄였지만 이번 설정에서 FlashSAC보다 정지 위치 성능이 일관되게 좋아졌다는 근거는 없다. D-3의 일부 조건 개선과 D-4의 높은 실패율을 구분해야 한다.

| 조건 | C-3 → D-3 drift 차이 m / 추가 실패 | C-4 → D-4 drift 차이 m / 추가 실패 |
|---|---:|---:|
| nominal | -0.723 ± 0.418 / +0 | -0.271 ± 0.025 / +6 |
| mass_1.15 | -0.141 ± 0.009 / +4 | -0.031 ± 0.005 / +4 |
| mass_1.30 | -1.042 ± 0.003 / +5 | -0.254 ± 0.031 / +0 |
| gain_0.8 | -1.028 ± 0.039 / +0 | -0.370 ± 0.031 / +0 |
| gain_1.2 | -0.390 ± 0.445 / +0 | 0.000 ± 0.000 / +6 |
| lag_0.02 | 0.000 ± 0.000 / +3 | 0.000 ± 0.000 / +3 |
| lag_0.05 | 0.000 ± 0.000 / +3 | 0.000 ± 0.000 / +0 |
| friction_0.2 | -1.309 ± 0.545 / +0 | -0.289 ± 0.003 / +7 |
| friction_0.8 | -0.723 ± 0.418 / +0 | -0.246 ± 0.014 / +7 |

## 재현과 구현

- 브랜치: `agent/codex/dev_tita_gluon`. 기존 492개 status 항목 보존. 새 구현: `sim2sim/lqr/`.
- 새 파일: `__init__.py`, `runtime.py`, `model.py`, `estimator.py`, `controller.py`, `evaluate.py`, `report.py`, `config.json`.
- 검사/nominal 튜닝: `test/test_lqr_baseline_gate.py`, `test/test_lqr_adaptive.py`, `test/tune_lqr_nominal.py`, `test/check_lqr_ablation_results.py`.
- checkpoint는 `model_100000/actor.pt`이다. `network_state_dict`를 actor-only로 복원하며 critic/replay는 사용하지 않는다.
- 기존 export의 deterministic tanh mean 및 checkpoint piecewise action gain을 그대로 사용한다. Observation 33, action 8, policy history 없음, checkpoint joint order·scale·clip·last action 재사용.
- A는 기존 외부 position/velocity PD를 그대로 사용한다. B는 기존 FlashSAC wheel 채널과 adapter만 사용하며 leg는 공통 fixed PD로 교체한다.
- C/D는 unit gear 직접 torque motor에 양쪽 합 토크 u를 1/2씩 적용한다. 기존 wheel velocity reference에 torque를 더하지 않는다.
- Leg stand target은 checkpoint의 `[0.1,0.8,-1.5,0,0.1,0.8,-1.5,0]`. B/C/D는 Kp=360, Kd=12, leg torque ±60 Nm로 동일하다. A의 Kp=60/Kd=1.5는 보존했다.
- Nominal-only 후보 12개 × pitch 3개 × C-3/C-4 = 72회로 PD와 Q/R를 선택했다. 점수는 `100×실패 + 최대 planar drift + 10×pitch RMS`의 합이다. mismatch에서 재튜닝하지 않았다.
- 최초 airborne/약한 leg-PD 시험의 LQR 실패는 `fixed_gate`, `fixed_grounded_gate`에 보존했다. 최종 실험은 URDF wheel geometry로 접지 높이·roll을 계산해 모든 군을 동일하게 초기화한다. A parity gate는 초기화 변경 전 기존 launch 경로와 정확히 비교했다.
- 물리 dt=0.005 s, decimation=4, control dt=0.02 s. Wheel torque ±12 Nm, LQR 합 토크 ±24 Nm, slew 120 Nm/s. Fast control 50 Hz, RLS batch/gain candidate 5 Hz.
- 고정 Q4=[1.0, 2.0, 200.0, 5.0], Q3=Q4[1:], R=0.1. 각 mismatch에서 A0/B0/K0 고정.
- URDF 합성 물성: `{"m_b": 22.67215789, "m_w": 1.5094, "I_w": 0.006904999999999998, "I_b": 0.3766129060041546, "l": 0.2868176510473269, "r": 0.0925, "g": 9.81, "equilibrium_pitch": -0.044397555309199636, "equilibrium_roll": -0.06844295113911344, "com_base": [-0.0018990367553871667, 0.0014943543931277916, -0.005539976130390173], "axle_base": [-0.014628856270554186, 0.029181108442899173, -0.2908495068032185]}`.
- Nominal A/B는 URDF 질량·CoM·관성 및 parallel-axis 합성 + wheel motor 반작용 모델이다. MuJoCo mass matrix/linearization은 읽지 않았다. 3/4-state는 같은 exact ZOH 모델에서 position 상태만 제거한다.
- Encoder odometry는 IMU 회전, wheel 및 leg joint 회전을 FK 축에 투영한다. Controller/RLS API에는 root 위치·속도가 없다. World axle/CoM/heading velocity는 metric 계산에만 사용한다. MuJoCo의 unbounded encoder와 optional wrapped encoder 처리를 지원한다.
- 4개 이산 residual 계수만 추정한다. Trapezoidal 적분 보정은 연속 물성의 정확한 복원이 아니다. excitation/covariance/bounds, DARE/eigenvalue, gain 및 command 변화량, nominal/candidate transient 검사를 통과한 gain만 채택한다.

## 실제 실행된 검증

- 기존 launch: 지정 체크포인트 250 step, PASS (`baseline_launch.log`).
- 새 A vs 기존 ROS 노드: zero → 0.1 m/s → zero 300 step, PASS. observation/action/torque/qpos/qvel 최대 차이 모두 0.0 (`baseline_gate.json`).
- dynamics/RLS/controller/sensor 테스트 27개: PASS (`unit_tests_final_v2.log`). 자세/encoder 좌표계는 MuJoCo FK·angular velocity와 비교했다.
- 결과 integrity 검사: 810개 unique episode, 81개 paired 초기 조건, 실제 motor gain/lag response, torque limit/slew, nominal cold start 및 frozen gain/계수 유지 PASS (`full/integrity.json`). Motor 응답 최대 차이는 약 1.06e-6 Nm였다.
- `./scripts/agent-check.sh`: PASS. Python syntax 325개 및 URDF XML 8개, diff integrity 검사 완료. 기존 소스·설정 681개 hash 비교에서 변경 없음 (`source_integrity.json`).
- RLS shadow: 18회, 동일 probing 조건, 제어 gain은 K0 유지. One-step 혼합 RMS 감소율 평균 46.9%, 표준편차 2.7%. v와 omega의 단위가 다르므로 원본의 개별 출력 오차도 함께 확인한다.
- Full evaluation: 810회 = 9 조건 × 3 seeds × 3 pitch × 10 episodes. 각 episode 최대 12초. A/B/C-3/C-4 각 1회, D-3/D-4 각각 adaptation/frozen/online 3회.
- seed=42/43/44, pitch perturbation −0.035/0/+0.035 rad, seed별 초기 forward velocity ±0.02 m/s. 각 pair에 같은 seed·초기 상태·3초 시점 12 N/0.1 s 외란을 적용한다.
- Adaptation만 합 토크 0.5 Nm 범위의 0.7/1.3 Hz probing을 사용한다. Frozen 및 online 평가에는 probing이 없다. Frozen 평가는 새 시뮬레이션 상태에서 학습된 gain을 고정한다. Online 평가는 같은 학습 상태에서 RLS를 계속 실행한다.
- 실패 기준: pitch error 또는 roll >0.65 rad, base height <0.18 m, leg joint limit 0.01 rad 초과, nonfinite state. 실패 episode는 즉시 종료하며 완료 trial의 통계와 섞어 개선을 주장하지 않는다.

## Nominal 결과

| 조건 | 제어기 | 상태 | 완료/전체 | 실패율 | 최대 planar drift m | pitch error RMS rad | odometry error RMS m |
|---|---|---|---:|---:|---:|---:|---:|
| nominal | A | PASS | 9/9 | 0.0% | 0.497 ± 0.018 | 0.094 ± 0.000 | 0.004 ± 0.000 |
| nominal | B | PASS | 9/9 | 0.0% | 6.650 ± 0.021 | 0.041 ± 0.000 | 0.020 ± 0.001 |
| nominal | C-3 | PASS | 9/9 | 0.0% | 2.815 ± 0.046 | 0.019 ± 0.000 | 0.021 ± 0.000 |
| nominal | C-4 | PASS | 9/9 | 0.0% | 0.605 ± 0.002 | 0.024 ± 0.000 | 0.017 ± 0.000 |
| nominal | D-3 | PASS | 9/9 | 0.0% | 2.092 ± 0.392 | 0.021 ± 0.002 | 0.020 ± 0.001 |
| nominal | D-4 | FAIL | 3/9 | 66.7% | 0.335 ± 0.025 | 0.070 ± 0.004 | 0.017 ± 0.000 |

A의 최대 실제 drift: 0.497 ± 0.018 m. B의 최대 실제 drift: 6.650 ± 0.021 m. B는 FlashSAC가 학습하지 않은 leg controller 조합이므로 A/B 차이를 wheel actor 품질만으로 해석하지 않는다.

## Mismatch 결과

| 조건 | 제어기 | 상태 | 완료/전체 | 실패율 | 최대 planar drift m | pitch error RMS rad | odometry error RMS m |
|---|---|---|---:|---:|---:|---:|---:|
| mass_1.15 | A | PASS | 9/9 | 0.0% | 0.650 ± 0.013 | 0.104 ± 0.000 | 0.005 ± 0.000 |
| mass_1.15 | B | PASS | 9/9 | 0.0% | 6.828 ± 0.008 | 0.032 ± 0.000 | 0.023 ± 0.000 |
| mass_1.15 | C-3 | PASS | 9/9 | 0.0% | 0.601 ± 0.029 | 0.005 ± 0.001 | 0.018 ± 0.000 |
| mass_1.15 | C-4 | PASS | 9/9 | 0.0% | 0.092 ± 0.008 | 0.005 ± 0.001 | 0.017 ± 0.000 |
| mass_1.15 | D-3 | FAIL | 5/9 | 44.4% | 0.445 ± 0.026 | 0.005 ± 0.001 | 0.018 ± 0.000 |
| mass_1.15 | D-4 | FAIL | 5/9 | 44.4% | 0.064 ± 0.012 | 0.008 ± 0.000 | 0.017 ± 0.000 |
| mass_1.30 | A | PASS | 9/9 | 0.0% | 0.239 ± 0.010 | 0.118 ± 0.000 | 0.007 ± 0.000 |
| mass_1.30 | B | PASS | 9/9 | 0.0% | 6.877 ± 0.002 | 0.033 ± 0.000 | 0.023 ± 0.000 |
| mass_1.30 | C-3 | PASS | 9/9 | 0.0% | 2.892 ± 0.055 | 0.014 ± 0.000 | 0.009 ± 0.000 |
| mass_1.30 | C-4 | PASS | 9/9 | 0.0% | 0.430 ± 0.002 | 0.017 ± 0.000 | 0.011 ± 0.000 |
| mass_1.30 | D-3 | FAIL | 4/9 | 55.6% | 1.808 ± 0.042 | 0.015 ± 0.000 | 0.010 ± 0.000 |
| mass_1.30 | D-4 | PASS | 9/9 | 0.0% | 0.176 ± 0.030 | 0.059 ± 0.014 | 0.014 ± 0.001 |
| gain_0.8 | A | PASS | 9/9 | 0.0% | 0.437 ± 0.018 | 0.095 ± 0.000 | 0.004 ± 0.000 |
| gain_0.8 | B | PASS | 9/9 | 0.0% | 6.685 ± 0.021 | 0.041 ± 0.000 | 0.021 ± 0.001 |
| gain_0.8 | C-3 | PASS | 9/9 | 0.0% | 2.885 ± 0.046 | 0.020 ± 0.000 | 0.021 ± 0.000 |
| gain_0.8 | C-4 | PASS | 9/9 | 0.0% | 0.601 ± 0.002 | 0.024 ± 0.000 | 0.017 ± 0.000 |
| gain_0.8 | D-3 | PASS | 9/9 | 0.0% | 1.857 ± 0.076 | 0.023 ± 0.001 | 0.019 ± 0.000 |
| gain_0.8 | D-4 | PASS | 9/9 | 0.0% | 0.231 ± 0.032 | 0.039 ± 0.003 | 0.017 ± 0.000 |
| gain_1.2 | A | PASS | 9/9 | 0.0% | 0.535 ± 0.019 | 0.094 ± 0.000 | 0.004 ± 0.000 |
| gain_1.2 | B | PASS | 9/9 | 0.0% | 6.628 ± 0.024 | 0.041 ± 0.000 | 0.019 ± 0.001 |
| gain_1.2 | C-3 | PASS | 9/9 | 0.0% | 2.769 ± 0.046 | 0.019 ± 0.000 | 0.021 ± 0.000 |
| gain_1.2 | C-4 | PASS | 9/9 | 0.0% | 0.608 ± 0.002 | 0.024 ± 0.000 | 0.017 ± 0.000 |
| gain_1.2 | D-3 | PASS | 9/9 | 0.0% | 2.379 ± 0.411 | 0.020 ± 0.002 | 0.020 ± 0.001 |
| gain_1.2 | D-4 | FAIL | 3/9 | 66.7% | 0.607 ± 0.001 | 0.024 ± 0.000 | 0.017 ± 0.000 |
| lag_0.02 | A | PASS | 9/9 | 0.0% | 0.093 ± 0.030 | 0.099 ± 0.000 | 0.009 ± 0.000 |
| lag_0.02 | B | PASS | 9/9 | 0.0% | 5.410 ± 0.003 | 0.059 ± 0.000 | 0.031 ± 0.000 |
| lag_0.02 | C-3 | PASS | 9/9 | 0.0% | 2.813 ± 0.046 | 0.019 ± 0.000 | 0.021 ± 0.000 |
| lag_0.02 | C-4 | PASS | 9/9 | 0.0% | 0.605 ± 0.002 | 0.024 ± 0.000 | 0.017 ± 0.000 |
| lag_0.02 | D-3 | FAIL | 6/9 | 33.3% | 2.791 ± 0.036 | 0.019 ± 0.000 | 0.021 ± 0.000 |
| lag_0.02 | D-4 | FAIL | 6/9 | 33.3% | 0.604 ± 0.001 | 0.024 ± 0.000 | 0.017 ± 0.000 |
| lag_0.05 | A | PASS | 9/9 | 0.0% | 0.787 ± 0.054 | 0.106 ± 0.001 | 0.053 ± 0.004 |
| lag_0.05 | B | PASS | 9/9 | 0.0% | 4.773 ± 0.008 | 0.091 ± 0.001 | 0.044 ± 0.000 |
| lag_0.05 | C-3 | PASS | 9/9 | 0.0% | 2.814 ± 0.046 | 0.020 ± 0.000 | 0.021 ± 0.000 |
| lag_0.05 | C-4 | PASS | 9/9 | 0.0% | 0.605 ± 0.002 | 0.025 ± 0.000 | 0.017 ± 0.000 |
| lag_0.05 | D-3 | FAIL | 6/9 | 33.3% | 2.793 ± 0.036 | 0.020 ± 0.000 | 0.021 ± 0.000 |
| lag_0.05 | D-4 | PASS | 9/9 | 0.0% | 0.605 ± 0.002 | 0.025 ± 0.000 | 0.017 ± 0.000 |
| friction_0.2 | A | PASS | 9/9 | 0.0% | 0.346 ± 0.013 | 0.092 ± 0.000 | 0.004 ± 0.001 |
| friction_0.2 | B | PASS | 9/9 | 0.0% | 4.671 ± 0.030 | 0.040 ± 0.000 | 0.149 ± 0.013 |
| friction_0.2 | C-3 | PASS | 9/9 | 0.0% | 4.298 ± 0.069 | 0.019 ± 0.000 | 0.004 ± 0.001 |
| friction_0.2 | C-4 | PASS | 9/9 | 0.0% | 0.644 ± 0.002 | 0.023 ± 0.000 | 0.003 ± 0.002 |
| friction_0.2 | D-3 | PASS | 9/9 | 0.0% | 2.989 ± 0.492 | 0.021 ± 0.001 | 0.004 ± 0.002 |
| friction_0.2 | D-4 | FAIL | 2/9 | 77.8% | 0.353 ± 0.005 | 0.034 ± 0.002 | 0.004 ± 0.000 |
| friction_0.8 | A | PASS | 9/9 | 0.0% | 0.484 ± 0.018 | 0.094 ± 0.000 | 0.004 ± 0.000 |
| friction_0.8 | B | PASS | 9/9 | 0.0% | 6.545 ± 0.016 | 0.041 ± 0.000 | 0.020 ± 0.001 |
| friction_0.8 | C-3 | PASS | 9/9 | 0.0% | 2.815 ± 0.046 | 0.019 ± 0.000 | 0.021 ± 0.000 |
| friction_0.8 | C-4 | PASS | 9/9 | 0.0% | 0.605 ± 0.002 | 0.024 ± 0.000 | 0.017 ± 0.000 |
| friction_0.8 | D-3 | PASS | 9/9 | 0.0% | 2.092 ± 0.392 | 0.021 ± 0.002 | 0.020 ± 0.001 |
| friction_0.8 | D-4 | FAIL | 2/9 | 77.8% | 0.359 ± 0.010 | 0.072 ± 0.017 | 0.017 ± 0.000 |

수치는 완료 trial의 평균 ± sample 표준편차이다. 실패율의 분모는 전체 trial이다. `full/metrics.csv`, `full/results.jsonl`, `analysis/aggregates.json`에 분포·실패 사유·초기 상태·실제 적용된 물성이 있다. Mass/CoM은 base link 질량·관성 scale 1.15/1.30 및 CoM x +0.01/+0.02 m, motor gain 0.8/1.2, lag time constant 0.02/0.05 s, wheel/floor sliding friction 0.2/0.8을 각각 독립 적용했다. 마찰은 wheel과 floor 양쪽에 적용해 접촉 pair mixing에서 변경이 사라지지 않게 했다.

## 같은 초기 조건의 직접 비교

음수 차이는 후자의 값이 작다는 뜻이다. 양쪽 모두 완료한 pair만 수치 차이를 계산하며, 위 전체 실패율을 반드시 함께 본다. D는 gain 고정 평가이다. 실패한 adaptation에서 가져온 gain은 `adaptation_episode_status`로 별도 식별되며 적응 성공으로 간주하지 않는다.

| 조건 | 비교 (후자 − 전자) | 양쪽 완료 pair | 최대 drift 차이 m | pitch RMS 차이 rad |
|---|---|---:|---:|---:|
| nominal | A → B | 9 | 6.153 ± 0.039 | -0.053 ± 0.000 |
| nominal | B → C-3 | 9 | -3.834 ± 0.066 | -0.021 ± 0.000 |
| nominal | B → C-4 | 9 | -6.044 ± 0.022 | -0.017 ± 0.000 |
| nominal | C-3 → C-4 | 9 | -2.210 ± 0.044 | 0.004 ± 0.000 |
| nominal | C-3 → D-3 | 9 | -0.723 ± 0.418 | 0.002 ± 0.001 |
| nominal | C-4 → D-4 | 3 | -0.271 ± 0.025 | 0.046 ± 0.004 |
| nominal | D-3 → D-4 | 3 | -1.530 ± 0.016 | 0.048 ± 0.005 |
| mass_1.15 | A → B | 9 | 6.178 ± 0.021 | -0.072 ± 0.000 |
| mass_1.15 | B → C-3 | 9 | -6.227 ± 0.037 | -0.027 ± 0.001 |
| mass_1.15 | B → C-4 | 9 | -6.736 ± 0.015 | -0.026 ± 0.000 |
| mass_1.15 | C-3 → C-4 | 9 | -0.510 ± 0.023 | 0.001 ± 0.000 |
| mass_1.15 | C-3 → D-3 | 5 | -0.141 ± 0.009 | 0.000 ± 0.000 |
| mass_1.15 | C-4 → D-4 | 5 | -0.031 ± 0.005 | 0.002 ± 0.000 |
| mass_1.15 | D-3 → D-4 | 2 | -0.409 ± 0.003 | 0.003 ± 0.000 |
| mass_1.30 | A → B | 9 | 6.638 ± 0.008 | -0.085 ± 0.000 |
| mass_1.30 | B → C-3 | 9 | -3.985 ± 0.056 | -0.019 ± 0.000 |
| mass_1.30 | B → C-4 | 9 | -6.447 ± 0.003 | -0.016 ± 0.000 |
| mass_1.30 | C-3 → C-4 | 9 | -2.462 ± 0.053 | 0.003 ± 0.000 |
| mass_1.30 | C-3 → D-3 | 4 | -1.042 ± 0.003 | 0.001 ± 0.000 |
| mass_1.30 | C-4 → D-4 | 9 | -0.254 ± 0.031 | 0.042 ± 0.014 |
| mass_1.30 | D-3 → D-4 | 4 | -1.617 ± 0.048 | 0.031 ± 0.009 |
| gain_0.8 | A → B | 9 | 6.247 ± 0.039 | -0.053 ± 0.000 |
| gain_0.8 | B → C-3 | 9 | -3.799 ± 0.066 | -0.021 ± 0.000 |
| gain_0.8 | B → C-4 | 9 | -6.084 ± 0.023 | -0.017 ± 0.000 |
| gain_0.8 | C-3 → C-4 | 9 | -2.285 ± 0.044 | 0.004 ± 0.000 |
| gain_0.8 | C-3 → D-3 | 9 | -1.028 ± 0.039 | 0.003 ± 0.001 |
| gain_0.8 | C-4 → D-4 | 9 | -0.370 ± 0.031 | 0.015 ± 0.003 |
| gain_0.8 | D-3 → D-4 | 9 | -1.626 ± 0.063 | 0.016 ± 0.002 |
| gain_1.2 | A → B | 9 | 6.093 ± 0.043 | -0.053 ± 0.000 |
| gain_1.2 | B → C-3 | 9 | -3.859 ± 0.069 | -0.021 ± 0.000 |
| gain_1.2 | B → C-4 | 9 | -6.020 ± 0.025 | -0.017 ± 0.000 |
| gain_1.2 | C-3 → C-4 | 9 | -2.161 ± 0.044 | 0.005 ± 0.000 |
| gain_1.2 | C-3 → D-3 | 9 | -0.390 ± 0.445 | 0.001 ± 0.001 |
| gain_1.2 | C-4 → D-4 | 3 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| gain_1.2 | D-3 → D-4 | 3 | -2.121 ± 0.031 | 0.005 ± 0.000 |
| lag_0.02 | A → B | 9 | 5.317 ± 0.028 | -0.040 ± 0.000 |
| lag_0.02 | B → C-3 | 9 | -2.597 ± 0.044 | -0.040 ± 0.000 |
| lag_0.02 | B → C-4 | 9 | -4.805 ± 0.002 | -0.035 ± 0.000 |
| lag_0.02 | C-3 → C-4 | 9 | -2.208 ± 0.045 | 0.004 ± 0.000 |
| lag_0.02 | C-3 → D-3 | 6 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| lag_0.02 | C-4 → D-4 | 6 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| lag_0.02 | D-3 → D-4 | 6 | -2.187 ± 0.034 | 0.005 ± 0.000 |
| lag_0.05 | A → B | 9 | 3.986 ± 0.053 | -0.016 ± 0.001 |
| lag_0.05 | B → C-3 | 9 | -1.959 ± 0.041 | -0.071 ± 0.000 |
| lag_0.05 | B → C-4 | 9 | -4.168 ± 0.007 | -0.066 ± 0.001 |
| lag_0.05 | C-3 → C-4 | 9 | -2.209 ± 0.044 | 0.005 ± 0.000 |
| lag_0.05 | C-3 → D-3 | 6 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| lag_0.05 | C-4 → D-4 | 9 | 0.000 ± 0.000 | 0.000 ± 0.000 |
| lag_0.05 | D-3 → D-4 | 6 | -2.189 ± 0.035 | 0.005 ± 0.000 |
| friction_0.2 | A → B | 9 | 4.325 ± 0.029 | -0.053 ± 0.001 |
| friction_0.2 | B → C-3 | 9 | -0.372 ± 0.066 | -0.020 ± 0.000 |
| friction_0.2 | B → C-4 | 9 | -4.027 ± 0.031 | -0.016 ± 0.000 |
| friction_0.2 | C-3 → C-4 | 9 | -3.655 ± 0.071 | 0.004 ± 0.000 |
| friction_0.2 | C-3 → D-3 | 9 | -1.309 ± 0.545 | 0.002 ± 0.001 |
| friction_0.2 | C-4 → D-4 | 2 | -0.289 ± 0.003 | 0.010 ± 0.002 |
| friction_0.2 | D-3 → D-4 | 2 | -2.314 ± 0.112 | 0.012 ± 0.001 |
| friction_0.8 | A → B | 9 | 6.061 ± 0.035 | -0.054 ± 0.000 |
| friction_0.8 | B → C-3 | 9 | -3.730 ± 0.061 | -0.021 ± 0.000 |
| friction_0.8 | B → C-4 | 9 | -5.939 ± 0.018 | -0.017 ± 0.000 |
| friction_0.8 | C-3 → C-4 | 9 | -2.210 ± 0.044 | 0.004 ± 0.000 |
| friction_0.8 | C-3 → D-3 | 9 | -0.723 ± 0.418 | 0.002 ± 0.001 |
| friction_0.8 | C-4 → D-4 | 2 | -0.246 ± 0.014 | 0.048 ± 0.018 |
| friction_0.8 | D-3 → D-4 | 2 | -1.841 ± 0.409 | 0.050 ± 0.020 |

## 식별과 online 평가

| 조건 | 제어기 | adaptation 실패 | gain 채택 평균 | frozen 실패 | online 실패 |
|---|---|---:|---:|---:|---:|
| nominal | D-3 | 0/9 | 36.6 | 0/9 | 4/9 |
| nominal | D-4 | 0/9 | 45.3 | 6/9 | 4/9 |
| mass_1.15 | D-3 | 4/9 | 32.3 | 4/9 | 4/9 |
| mass_1.15 | D-4 | 4/9 | 23.4 | 4/9 | 9/9 |
| mass_1.30 | D-3 | 5/9 | 11.7 | 5/9 | 5/9 |
| mass_1.30 | D-4 | 0/9 | 37.1 | 0/9 | 0/9 |
| gain_0.8 | D-3 | 0/9 | 50.6 | 0/9 | 5/9 |
| gain_0.8 | D-4 | 0/9 | 52.0 | 0/9 | 0/9 |
| gain_1.2 | D-3 | 0/9 | 17.8 | 0/9 | 3/9 |
| gain_1.2 | D-4 | 2/9 | 25.4 | 6/9 | 6/9 |
| lag_0.02 | D-3 | 0/9 | 18.7 | 3/9 | 3/9 |
| lag_0.02 | D-4 | 3/9 | 1.0 | 3/9 | 3/9 |
| lag_0.05 | D-3 | 3/9 | 2.2 | 3/9 | 3/9 |
| lag_0.05 | D-4 | 0/9 | 0.0 | 0/9 | 0/9 |
| friction_0.2 | D-3 | 0/9 | 36.2 | 0/9 | 2/9 |
| friction_0.2 | D-4 | 5/9 | 44.2 | 7/9 | 8/9 |
| friction_0.8 | D-3 | 0/9 | 36.6 | 0/9 | 4/9 |
| friction_0.8 | D-4 | 0/9 | 45.3 | 7/9 | 2/9 |

Adaptation의 decimated guard 상태 빈도: `{'cold_start': 162, 'insufficient_excitation_or_bounds': 842, 'accepted': 4648, 'command_step_limit': 1562, 'gain_step_limit': 2062, 'validation_transient': 138, 'Unstable candidate gain': 1}`. 추정 모델의 eigenvalue 안정성은 MuJoCo의 안정성을 보장하지 않으며, 거부 시 마지막 검증 gain을 유지한다.

## 연구 질문에 대한 판정

1. FlashSAC-only drift: 위 nominal A 표와 seed별 trace에 실측값을 기록했다.
2. Leg PD 효과: A/B pair 표로 확인한다. Wheel 정책을 고정해도 stand leg PD·학습 분포 변경에 따른 영향이 남는다.
3. Fixed 3-State 균형: C-3의 전체 조건 완료율과 pitch RMS로 판단한다. 위치 비용이 없어 자세 안정화와 위치 복귀가 같은 목표가 아니다.
4. Relative position 효과: C-3/C-4 pair 표로 확인한다. 위치는 encoder 기반이고 actual axle drift와 odometry error를 별도 보고한다.
5. Excitation: shadow에서 regressor rank 2 및 confidence를 확인했다. 지속 정지에서의 식별성이나 모든 mismatch의 식별 성공을 보장하지 않는다.
6. Prediction error: shadow에서 감소했다. Adaptation trace에 v/omega one-step nominal/adaptive 오차, 계수·covariance·SVD를 저장했다.
7. 제어 성능으로의 연결: 예측 오차 감소만으로 성공 판정을 내리지 않는다. Frozen/online 실패율과 paired drift/pitch가 근거다.
8–9. D-3 vs C-3 / D-4 vs C-4: 위 pair·전체 실패율 표에 직접 비교했다. 실패 trial을 제외한 좋은 평균만으로 Adaptive LQR 우위를 주장하지 않는다.
10. Mismatch별 효과/실패: 전체 표와 학습 실패율을 사용한다. Gain을 채택하지 않은 trial은 nominal fallback 효과이며 적응의 효과로 분류하지 않는다.
11. Motor lag는 상태에 없는 motor internal state를 만들며, slip은 no-slip 모델과 encoder odometry를 동시에 훼손한다. 잔차 4개만으로 정확히 모델링할 수 없고 yaw/roll·leg compliance도 식별 계수에 섞일 수 있다.
12. 실제 배포 전에는 encoder unwrap/axis sign·IMU frame/지연·joint chain·torque unit 및 실제 clipping·motor lag·watchdog·operator stop을 별도로 검증해야 한다. 이번 코드는 hardware에 배포하거나 physical command를 실행하지 않았다.

## 남은 한계

- RLS는 closed-loop predictive residual을 식별하며 실제 A/B 물성의 유일한 식별을 증명하지 않는다. Q/R nominal 튜닝과 같은 seed 42가 평가에도 있어 독립 held-out 최적 성능 주장에는 부족하다.
- Roll/yaw 안정화는 이 WIP LQR에 없다. Heading 변화가 크면 전진 odometry의 적분은 world x 위치 hold와 다르다. Odometry error는 evaluation-only forward path 적분과 비교하고 planar displacement/yaw 변화도 기록한다.
- Nominal pitch inertia는 body sagittal y 축 합성이고 작은 roll·wheel-axis tilt·leg compliance를 단순화했다. 고정 PD가 완전한 leg lock은 아니므로 leg error/velocity/CoM 변화가 원본에 있다.
- 기존 MuJoCo pipeline의 sensor 읽기와 fresh qpos/qvel 시점에는 physics step 수준의 차이가 있을 수 있다. Training config의 randomized actuator delay 0–4 physics steps는 기존 Sim2Sim 실행기가 구현하지 않으며 A/B에서도 추가하지 않았다. 이번 motor-lag mismatch는 그 차이를 진단하는 별도 조건이다.
- Pitch 추정은 IMU frame quaternion을 사용한다. 별도 raw root quaternion을 trace에 저장하지 않아 pitch sensor와 ground-truth의 독립 오차 RMS는 NOT_TESTED이다. 위치·속도 추정 오차는 실측했다.
- Locomotion↔stationary switching은 첨부 Phase 7이며 이번 6군 zero-command ablation 범위 밖이다: NOT_TESTED. Nonzero command를 stationary LQR로 보내는 hardware용 mode manager는 제공하지 않는다.

## 산출물과 실행 명령

- PNG: `full/analysis/nominal_trajectories.png`, `ablation_comparison.png`, `D-3_identification.png`, `D-4_identification.png`.
- CSV/JSON: `full/metrics.csv`, `full/results.jsonl`, `full/analysis/aggregates.csv`, `paired_comparisons.json`.
- 각 episode NPZ: 시각, 센서 기반 state, evaluation truth, wheel torque, leg 움직임, CoM, 계수, covariance, singular values, gain, prediction error, gain 거부 사유. 초기 중단된 trace도 보존한다.

저장소 루트에서 다음을 실행한다. Output은 비어 있는 새 경로여야 한다.

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py --ckpt lab/ddt_lab/logs/flash_sac/tita_flash_sac_172127_928297/model_100000 --headless --steps 250
source /opt/ros/jazzy/setup.bash
ROS_DOMAIN_ID=87 ROS_LOCALHOST_ONLY=1 ROS_LOG_DIR=/tmp/lqr_ros_logs /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_lqr_baseline_gate.py
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_lqr_adaptive.py
/home/cocel/venvs/cosim_ros2_jazzy/bin/python -m sim2sim.lqr.evaluate --stage shadow --nominal-only --output docs/exp/2026-10-14/lqr_rerun/shadow
/home/cocel/venvs/cosim_ros2_jazzy/bin/python -m sim2sim.lqr.evaluate --stage full --shadow-evidence docs/exp/2026-10-14/lqr_rerun/shadow/results.jsonl --output docs/exp/2026-10-14/lqr_rerun/full
MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python -m sim2sim.lqr.report --results docs/exp/2026-10-14/lqr_rerun/full --shadow-evidence docs/exp/2026-10-14/lqr_rerun/shadow/results.jsonl --report docs/exp/2026-10-14/lqr_rerun_summary.md
./scripts/agent-check.sh
```

모델링 참고: [Cui et al., Modeling and Control of a Wheeled Biped Robot, Micromachines 2022](https://www.mdpi.com/2072-666x/13/5/747). 이번 구현의 구체적 운동방정식과 residual correction은 사용자 첨부 설계를 따른다.
