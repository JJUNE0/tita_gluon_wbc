# D-4 실패·Ground-truth·학습 gain 진단

Execution Domain: VALIDATION_SIM (코드·로그 검사: DESKTOP_DRY_RUN)

Evidence Status: SUSPICIOUS — 진단 실행과 재현 gate는 PASS, 제어 성공/실패는 아래에 구분한다.

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

Observed Metrics / Behavior / Log Summary:

**Nominal의 D-4 실패는 학습된 gain 단독의 불안정성으로 설명되지 않았다.** 기존 sensor cache 경로는 학습 gain 고정 시 6/9회 실패했지만, 같은 gain과 같은 물리 초기 상태에서 GT 또는 동기화 센서를 사용하면 9/9회 완료했다. Gyro만 최신화한 9회도 모두 완료했다. 반면 일부 mass mismatch에서는 GT로도 실패가 남으므로 센서 시점 문제만으로 모든 조건을 설명할 수 없다.

## 공통 조건과 실행 근거

- 새 제어 알고리즘·PINN·RLS 구조·Q/R·leg PD·평형 pitch 기준을 추가하거나 변경하지 않았다. 기존 코드와 보고서를 보존했다.
- 신규 진단 코드는 모두 `test/`에 있다. 기존 Playback.step, actuator adapter, setup_scene, WheelLQR/RLS를 재사용했다.
- 9 dynamics 조건 × 3 seeds × 3 pitch = 81개 물리 초기 조건. 같은 archived K를 센서/GT에 교차 적용했다. Sensor/GT online 및 cold-start adaptation도 따로 실행했다. Nominal에 synchronized 센서 18회 추가: 총 747회.
- 기존 Fixed-4 및 D-4 adaptation/frozen/online 324회를 재현했다. 최종 시각·실패 여부·state·K·torque·residual이 일치한다. 최대 차이 0. 초기 qpos/qvel는 81개 pair에서 완전히 동일했다.
- Primary GT는 root quaternion/각속도 및 wheel axle world 위치·Jacobian 속도를 사용한다. 위치는 기존 estimator와 맞춰 midpoint heading 방향의 실제 axle 이동량을 누적한다. world x/y hold와는 다르며 yaw가 바뀌면 동일한 위치 목표로 해석할 수 없다.
- GT 읽기는 복제 mjData에서 mj_forward를 실행한다. 원본 dynamics 및 cached sensor timing을 바꾸지 않는다. Clone 비변경 검사와 pitch/axle 속도의 독립 유한차분 검사 2개 PASS (`oracle_tests.log`).
- GT는 이번 사용자 요청으로 허용된 진단용 입력이며 deployable controller/RLS에는 추가하지 않았다.
- 모든 평가 12초, dt=0.02 s, physics dt=0.005 s, 동일 torque/slew limit과 동일 disturbance. Adaptation만 기존 probing을 사용한다. 학습된 gain 비교는 probing 없이 새 episode에서 시작한다.

## 1. D-4 실패 원인

기존 경로의 79개 실패를 전부 재현하고 trigger를 분리했다: `{'pitch_error_limit': 79}`. Pitch error 한계가 직접 종료 사유였다. Roll/height/leg limit은 함께 기록했다.

대표 nominal seed42/pitch0 학습 gain: `[-2.615442415553816, -21.57940681835991, -37.74255970330144, -19.796536565920782]`. Gain 고정 실패 시각 1.90 s, cached pitch error 0.6519 rad, true pitch error 0.6609 rad, roll -0.0697 rad, base height 0.3229 m. Leg limit 최소 margin 0.6846 rad.
실패 직전 실제 wheel torque: `[10.317015647888184, 10.317015647888184]` Nm, episode peak 10.317 Nm, raw 합 torque clipping ratio 0.260, 실제 motor limit 도달 비율 0.000, slew 제한 적용 비율 0.938. Raw command clipping과 실제 motor saturation은 구분해야 한다. 종료 trigger는 pitch 한계였으며 slew/clipping의 기여를 배제하지 않는다.
- `analysis/failures.json`에 현재 K/직전 실제 적용 K, 실제 torque, saturation, pitch/roll, height, joint 값·limit margin·정확한 사유를 기록했다. 각 실패에는 마지막 0.3초 CSV가 있다.
- NPZ row t의 torque는 직전 [t−dt,t] 구간에 적용된 값이다. 대응하는 적용 gain은 이전 row의 K이다. Gain 변경과 torque/측정의 시간을 분리해서 해석해야 한다.

## 2–3. GT 상태 대조 및 K₀/K_adapt 재평가

아래는 실패 횟수/전체이다. K_adapt는 각 pair의 기존 센서 adaptation에서 얻은 **동일한 gain**이며 평가에서 고정했다. Online도 동일한 archived gain·P·residual로 시작했다. 실패한 adaptation의 gain도 성공으로 숨기지 않고 그대로 진단했다.

| 조건 | K₀ 센서 | K₀ GT | K_adapt 센서 | K_adapt GT | online 센서 | online GT |
|---|---:|---:|---:|---:|---:|---:|
| nominal | 0/9 | 0/9 | 6/9 | 0/9 | 4/9 | 0/9 |
| mass_1.15 | 0/9 | 0/9 | 4/9 | 3/9 | 9/9 | 8/9 |
| mass_1.30 | 0/9 | 0/9 | 0/9 | 0/9 | 0/9 | 1/9 |
| gain_0.8 | 0/9 | 0/9 | 0/9 | 0/9 | 0/9 | 0/9 |
| gain_1.2 | 0/9 | 0/9 | 6/9 | 0/9 | 6/9 | 0/9 |
| lag_0.02 | 0/9 | 0/9 | 3/9 | 2/9 | 3/9 | 1/9 |
| lag_0.05 | 0/9 | 0/9 | 0/9 | 0/9 | 0/9 | 0/9 |
| friction_0.2 | 0/9 | 0/9 | 7/9 | 0/9 | 8/9 | 0/9 |
| friction_0.8 | 0/9 | 0/9 | 7/9 | 0/9 | 2/9 | 0/9 |

Nominal K₀와 K_adapt는 sensor 동기화 경로에서 모두 9/9회 완료했다. 기존 nominal online 4/9회 실패도 GT에서는 0/9였다.

분리 시험 18회: `{'learned_gyro_fresh': {'failed': 0, 'total': 9}, 'learned_quaternion_fresh': {'failed': 5, 'total': 9}}`. Gyro 최신화는 pitch-rate뿐 아니라 encoder velocity의 body angular contribution도 바꾼다. 따라서 pitch-rate 채널 하나만의 원인이라고 단정하지 않는다.
- 기존 경로는 mj_step 이후 fresh joint qpos/qvel와 마지막 physics substep 이전의 IMU sensor cache를 혼합한다. 복제 data의 gyro/quaternion을 최신화하면 이 시점 차이를 제거한다. 이상은 정지 odometry의 1.7cm RMS만으로 발견하기 어렵고, transient feedback에서 중요했다.
- 대표 K_adapt의 velocity gain 크기는 K₀보다 약 3.96배, pitch-rate gain은 약 2.46배이다. 이 큰 gain이 cached gyro가 포함된 loop의 시간 오차에 더 민감했음을 동일 K의 교차실험이 뒷받침한다.

GT를 RLS에도 사용한 cold-start adaptation 및 그 gain의 새 GT 평가:

| 조건 | GT adaptation 실패 | 그 gain의 새 GT 평가 실패 |
|---|---:|---:|
| nominal | 0/9 | 0/9 |
| mass_1.15 | 0/9 | 0/9 |
| mass_1.30 | 0/9 | 0/9 |
| gain_0.8 | 0/9 | 0/9 |
| gain_1.2 | 0/9 | 0/9 |
| lag_0.02 | 0/9 | 6/9 |
| lag_0.05 | 3/9 | 6/9 |
| friction_0.2 | 0/9 | 0/9 |
| friction_0.8 | 0/9 | 0/9 |

## 실제 leg PD/contact plant 수치 선형화

- 같은 360/12 leg PD, 같은 stand reference·motor limits·wheel contact·dt를 사용했다. 수치 A/B를 controller에 적용하지 않았다. Nominal contact 조건에서만 계산했다.
- 실제 force balance 최적화의 최대 qacc 잔차는 0.04727. 대부분 yaw와 leg 방향이며 **정확한 정적 평형은 확보하지 못했다**. 따라서 접지된 near-static operating point의 local 근사이다.
- 전체 28차원 tangent state(qpos tangent 14 + qvel 14)의 20ms map F/G를 중앙 차분했다. Leg PD는 physics step마다 재계산하고 contact solver도 포함한다.
- H는 실제 [axle p,v,pitch,pitch-rate]의 관측 Jacobian, E는 axle 중심 pitch pivot 및 rolling wheel rate를 포함하는 명시적인 4-state lift이다. A_local=HFE, B_local=HG. H E≈I를 검사했다.
- H F−A_local H의 norm은 약 39로 0이 아니다. 숨은 leg/roll/yaw 상태가 있어 이 system은 4-state만으로 완전히 닫히지 않는다. 따라서 이 투영을 유일하고 정확한 A_true라고 부르지 않는다.

| state FD epsilon | A₀ 오차 norm | Ahat_final 오차 norm | B₀ 오차 norm | Bhat_final 오차 norm | 접촉 pair 변경 |
|---:|---:|---:|---:|---:|---:|
| 1e-05 | 0.8305 | 1.0260 | 0.0458 | 0.0253 | 0 |
| 5e-05 | 0.8745 | 0.9810 | 0.0552 | 0.0166 | 0 |
| 0.0001 | 0.8779 | 0.9759 | 0.0589 | 0.0136 | 0 |

- 행렬 norm은 단위와 state scale에 의존한다. 현재 계수의 A 오차는 nominal보다 커졌고 B 오차는 줄었다. 이는 네 residual 계수를 실제 A/B의 정확한 식별이라고 해석할 수 없다는 근거다.
- 아주 작은 input 차분은 contact solver 오차에 민감했다. 독립 input 크기 0.001/0.01/0.05 Nm에서 B를 다시 계산했다. B_omega는 −0.04645/−0.04652/−0.04650으로 일치했다. 원본 sensitivity 결과를 함께 보존했다.
- 독립 50개 small-perturbation one-step validation component RMS [p m,v m/s,theta rad,omega rad/s]: `{'local': [2.4284924213800944e-09, 1.147912927037464e-07, 1.4465263357745295e-08, 5.679736222337618e-07], 'nominal': [5.267019785669253e-08, 4.2790351476824244e-05, 3.016747997038404e-06, 0.0002959873884516398], 'adapted': [8.205877476862418e-07, 4.5080177306509795e-05, 7.487521763989964e-07, 8.006774343372019e-05]}`. local 모델의 centered 응답은 검증됐지만 장기 안정성 보증은 아니다.
- K 계산 시점의 Ahat와 마지막 RLS Ahat를 따로 기록했다. 후보가 거부되면 K는 이전 값이므로 둘을 섞으면 안 된다.
- 4-state projection의 eigenvalue 판정은 epsilon에 따라 단위원 안팎을 오갔다. 전체 28-state에는 neutral translation/yaw/wheel-angle modes가 있어 spectral radius≈1을 곧바로 실패로 판정할 수 없다. 실제 nonlinear 동일 초기 조건 rollout을 gain 안정성 판단의 우선 근거로 사용했다.

## 판단과 남은 한계

1. 기존 nominal D-4 실패를 모델/gain 자체의 불안정성으로만 설명했던 판단은 수정해야 한다. 같은 gain을 GT 또는 gyro 시점 정렬로 적용하면 실패가 사라졌다.
2. Mass mismatch 일부는 GT에서도 실패한다. Sensor timing과 model-order/계수 식별 문제를 분리해서 다뤄야 한다.
3. 현재 physical equilibrium의 pitch bias, yaw drift, 접촉·leg compliance는 그대로 유지했다. 이번 진단에서 이를 수정하거나 Q/R를 다시 튜닝하지 않았다.
4. 새 알고리즘 확장 전에 sensor/control/RLS transition의 시간 정렬을 검증하고, 이 gain이 어떤 operating point·hidden state 조건에서 유효한지 다시 평가하는 것이 타당하다.

초기 oracle에서 local object angular frame을 root frame으로 오해한 시험은 무효 표시 후 중단했다. `smoke` 및 `full`의 GT 결과는 분석에서 제외했고 corrected oracle만 사용했다. 접촉 없는 초기 선형화도 제외했다. 이 보고서의 frame/velocity는 독립 유한차분 검사를 통과했다.

## 실행 및 산출물

```bash
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_lqr_diagnostic_state.py
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/debug_lqr_d4_diagnostics.py --output docs/exp/2026-10-14/new_diagnostics/paired_corrected
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/debug_lqr_sensor_timing.py --output docs/exp/2026-10-14/new_diagnostics/timing
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/debug_linearize_lqr_plant.py --output docs/exp/2026-10-14/new_diagnostics/linearization_gain_aligned
MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_lqr_diagnostics.py --root docs/exp/2026-10-14/new_diagnostics
```

- `analysis/aggregates.csv/json`, `failures.csv/json`, `integrity.json`, 비교 PNG 2개.
- `paired_corrected/`의 747개 NPZ와 실패 직전 CSV, actual initial state와 K/P 복원 기록.
- `linearization_gain_aligned/`의 F/G/H/E, projected A/B, K 및 RLS 모델, equilibrium 잔차와 independent validation.
- `test/test_lqr_diagnostic_state.py` 2개 PASS, `./scripts/agent-check.sh` PASS (Python syntax 330개, URDF XML 8개).
- 브랜치: `agent/codex/dev_tita_gluon`. 기존 production/simulation 제어 코드는 변경하지 않았다.

MuJoCo API 참고: [공식 functions 문서](https://mujoco.readthedocs.io/en/stable/APIreference/APIfunctions.html) (state copy, quaternion tangent integration/differencing, point Jacobian).
