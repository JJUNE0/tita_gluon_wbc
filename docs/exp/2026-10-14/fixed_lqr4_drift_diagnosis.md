# Fixed 4-State LQR drift 진단

Execution Domain: DESKTOP_DRY_RUN (기존 VALIDATION_SIM 로그 분석)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

Evidence Status: SUSPICIOUS — 일정한 위치 bias의 수치적 원인은 확인했다. 평형점 수정 또는 Q/R 변경 후의 새 rollout은 NOT_TESTED이다.

Observed Metrics / Behavior / Log Summary:

기존 full ablation의 nominal C-4 9개 trial에서 마지막 2초를 분석했다.
대표 trial은 seed 42, 초기 pitch disturbance 0이다. 코드·설정·기존 보고서는 변경하지 않았다.

## 위치 피드백과 pitch 피드백의 상쇄

대표 trial의 마지막 2초 평균은 다음과 같다.

| 값 | 관측치 |
|---|---:|
| Encoder 상대 위치 | −0.64675 m |
| Encoder 전진 속도 | −0.00037 m/s |
| 기준 대비 pitch 오차 | +0.02302 rad (약 +1.32°) |
| 실제 body pitch | −0.02138 rad (약 −1.23°) |
| 양쪽 합 wheel torque | 약 +0.00065 Nm |
| Torque saturation ratio | 0 |
| Odometry position error RMS | 0.0170 m |

고정 gain은 `K=[−1.9990, −5.4564, −56.3368, −8.0559]`이다.
`u=−Kx`에서 위치 항은 −1.29286 Nm, pitch 항은 +1.29671 Nm이다.
속도와 pitch-rate 항까지 더하면 거의 0이다.
즉 위치가 0으로 복귀하는 대신, 일정한 pitch 기준 오차를 상쇄하는 위치에 머물고 있다.

속도·pitch rate가 작고 평균 torque가 거의 0인 조건에서
`e_p ≈ −(K_theta/K_p) × theta_bias`이며,
이를 계산하면 −0.64867 m이다. 실제 encoder 위치 −0.64675 m와 가깝다.
9개 trial에서도 동일한 상쇄와 약 0.023 rad pitch bias가 관측됐다.

## 평형 기준이 바뀐 이유

현재 nominal model은 **목표 stand joint pose**로 CoM과 wheel axle을 합성해
평형 body pitch를 −0.04440 rad (약 −2.54°)로 고정한다.
하지만 finite-gain leg PD가 중력 하에서 목표 각도를 정확히 유지하지는 않는다.
대표 trial의 좌우 leg-3 오차는 약 −0.04376/−0.04018 rad이다.

로그의 평균 leg 오차를 목표 자세에 더한 뒤, 기존 URDF 질량·CoM·FK로
평형점을 다시 계산하면 −0.02154 rad (약 −1.23°)가 나온다.
이는 측정 body pitch −0.02138 rad와 가깝다.
Nominal 대비 평형 변화 +0.02286 rad가 controller에 남은 pitch 오차 +0.02302 rad를 설명한다.
실제 CoM을 로그에서 가져와 재구성한 wheel axle과 비교하면,
관측 자세에서 CoM의 수평 offset은 약 0.046 mm로 이미 axle 위에 가깝다.
이 재구성은 진단용이며 controller에 MuJoCo ground truth를 입력하지 않았다.

따라서 주된 문제는 **목표 leg pose에서 계산한 평형점과 하중을 받은 실제 leg pose의 평형점이 다른 것**이다.
Torque saturation이나 0.6 m 수준의 encoder 오차가 주원인이라는 근거는 없다.

## Q/R 튜닝의 역할과 한계

기존 nominal tuning에서 Kp=360, Kd=12, R=0.1을 유지하고
position cost만 바꾼 C-4의 최대 planar drift 평균은 다음과 같다.

| Q_position | 최대 planar drift 평균 |
|---:|---:|
| 0.01 | 2.152 m |
| 0.1 | 1.389 m |
| 1.0 | 0.604 m |

따라서 position cost를 키우는 것은 실제로 bias를 줄였다.
하지만 pitch 기준 오차가 계속 남으면 유한한 위치 gain에서 일정한 위치 오프셋을 허용하게 된다.
Q_position을 더 키웠을 때의 안정성·torque·slew 응답은 아직 검증하지 않았다.

권장 순서는 다음과 같다.

1. URDF 기반 하중·leg PD 정적 평형을 확인하고, 실제 stationary pose와 일치하는 pitch 기준을 설정한다.
   목표 pose를 유지하는 gravity compensation도 대안이지만 새 검증이 필요하다.
2. Wheel 차동 torque/yaw 안정화를 별도 검증한다.
3. 평형 bias를 정리한 후 공통 nominal 조건에서 Q_position 및 R을 재튜닝한다.
4. 남는 상수 외란의 정상상태 오차가 있으면 위치 적분/LQI를 별도 ablation으로 검토한다.
   추가 상태·anti-windup·torque 제한을 검증해야 하며, 기존 C-4와 같은 제어기로 보고하지 않는다.

## Yaw와 world position hold의 한계

대표 trial은 12초 동안 yaw가 약 2.555 rad (146.4°) 변했다.
현재 odometry의 위치는 **그때그때의 heading을 따른 signed 전진 이동량의 누적**이다.
Yaw가 크게 바뀌면 이 값이 0이 되는 것만으로 world x/y의 시작 위치 복귀를 보장하지 않는다.
따라서 평형점과 Q/R를 수정하더라도 실제 위치 hold 평가에는 yaw와 좌우 비대칭 원인도 다뤄야 한다.

상세 계산은 `fixed_lqr4_drift_diagnosis.json`에 기록했다.
이번에는 기존 로그와 URDF 재구성만 분석했고, 제어기 변경 또는 추가 simulation rollout은 수행하지 않았다.
