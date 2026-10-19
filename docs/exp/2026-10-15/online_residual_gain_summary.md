# G — Online Adaptive Residual Feedback Control

Execution Domain: VALIDATION_SIM (소스·경로·무결성 검사: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: FAIL — 현재 G의 고정 F-1 대비 실용적인 강건성 회복 목표. PASS — 전 실험 완료·구현 무결성. SUSPICIOUS — 일부 조건의 소폭 개선과 gain 효과 해석.

Observed Metrics / Behavior / Log Summary:

**현재 G는 고정 F-1보다 mismatch에 더 강건하다는 근거를 확보하지 못했다.** 고정 F-1의 baseline을 먼저 측정하고 제한된 단일 α를 온라인 조정했으나, 주요 악화 조건의 drift를 회복하지 못했다. 이 알고리즘은 gain 최적화이며 Online Dynamics Identification 또는 Adaptive LQR이 아니다. k_p/k_v 두 계수 학습이나 RLS/LQR 모델 갱신은 수행하지 않았다.

## Phase 2 — 12초 Dynamics Mismatch Baseline

기존 9조건 × 9초기조건 × A/F-1 = 162 episodes. 전 조건에서 두 군 모두 9/9 완료했다. 기존 A 81회와 nominal F-1 9회는 archive의 physics substep 토크 및 상태를 정확히 재현했다.

| 조건 | A 최대 drift 평균 m | F-1 최대 drift 평균 m | F-1 nominal 대비 |
|---|---:|---:|---:|
| nominal | 0.4968 | 0.3281 | +0.0% |
| mass_1.15 | 0.6499 | 0.4509 | +37.4% |
| mass_1.30 | 0.2393 | 0.2140 | -34.8% |
| gain_0.8 | 0.4374 | 0.2989 | -8.9% |
| gain_1.2 | 0.5350 | 0.3481 | +6.1% |
| lag_0.02 | 0.0928 | 0.0923 | -71.9% |
| lag_0.05 | 0.7872 | 1.0968 | +234.3% |
| friction_0.2 | 0.3459 | 0.2059 | -37.2% |
| friction_0.8 | 0.4836 | 0.3160 | -3.7% |

Nominal 대비 20% 이상 drift가 악화된 조건은 mass_1.15, lag_0.05였다. 이 20%는 추가 분석 기준이며 사용자 요구 사양이 아니다. Motor gain 0.8은 12초에서 nominal보다 drift가 작았다. 따라서 motor gain 감소가 반드시 이 horizon의 성능을 저하시킨다고 가정할 수 없다. Lag 50 ms에서는 F-1이 A보다 drift가 컸다.

## Phase 3 — G의 학습 규칙과 제한

- Base residual은 기존 F-1의 −2e_p−0.5v이다. p_hold=episode 시작 encoder 경로 0을 고정하고 encoder+현재 시점의 IMU로 p/v를 계산한다. Actor는 기존 A의 cache·33-value observation·전체 raw 8-action history를 유지한다.
- α 중심값은 1에서 시작하며 [0.5,2]에 제한한다. ±0.1 탐색을 ABBA 다음 BAAB 순서로 적용한다. 각 block은 3초이며 앞 1초는 평가에서 제외하고 나머지 2초의 센서 cost를 평가한다. 시작은 4초 이후다. 초기 3초의 외란 구간을 피해 학습한다.
- 8 blocks(24초) 후에만 중심값을 최대 0.1 갱신한다. 실제 α dose와 비용의 관계를 회귀하면서 constant/linear/quadratic 시간 추세를 nuisance 항으로 제거한다. |gradient|>2×회귀 표준오차이고 예상 탐색 효과가 평균 cost의 0.5%보다 클 때만 갱신한다. 불확실하면 유지한다. 이 표준오차는 직렬 상관이 있는 폐루프 데이터의 휴리스틱이며 통계적 인과 보증은 아니다.
- α 변화율도 0.25/s로 제한한다. α가 1을 넘어도 적용 residual 합 토크는 반드시 ±1 Nm(바퀴당 ±0.5 Nm)로 제한하고, 기존 1초 smoothstep ramp·합 토크 slew 2 Nm/s·기존 최종 actuator saturation을 유지한다. Alpha를 키워도 토크 한도를 늘리지 않는다.
- |pitch error|>0.25 rad, |pitch rate|>1 rad/s 또는 |encoder forward velocity|>0.5 m/s이면 탐색/평가를 중단하고 중심값을 1로 복귀시키며 4초 cooldown 후 다시 시작한다. 복귀 α와 torque도 slew를 거친다. 이는 학습 guard이고 로봇 하드웨어 안전 제어기의 구현이 아니다.
- Cost는 mean[(p/0.5)²]+mean[(v/0.05)²]+0.25×var(pitch)/0.02²+0.05×mean[(pitch_rate/0.2)²]+0.02×mean[(command_wheel_RMS/0.5)²]이다. 위치·속도·자세 센서 및 기존 제어 명령만 사용한다. 실제 motor gain/lag, true root position/velocity, GT drift, mismatch 이름은 optimizer에 전달하지 않는다. 토크 사용량 항은 gain/lag를 적용하기 전 명령 토크이며 실측 motor torque라고 부르지 않는다.
- FlashSAC wheel PD 토크는 매 physics step 그대로 계산하고 residual만 더한다. Leg torque와 last_action 의미를 바꾸지 않는다. Learned α는 torque 생성에만 쓰고 observation history에 넣지 않는다.

## 동일 60초 A/F-1/G 비교

기존 12초와 60초 drift를 직접 성능 비교하지 않는다. 60초는 이 보수적인 업데이트 규칙의 두 평가 주기(기본 28/52초)를 확보하기 위해 사용했다. 9 static conditions × 9초기조건 × 3군 = 243회, 20초에 motor gain을 1.0→0.8로 바꾸는 추가 조건 27회다. 변화 시각·gain은 motor 모델에만 적용하고 optimizer에는 알려주지 않았다.

| 조건 | 완료 A/F-1/G | A drift m | F-1 drift m | G drift m | G−F-1 paired 변화 | 개선 쌍 | G accepted/guard |
|---|---:|---:|---:|---:|---:|---:|---:|
| nominal | 9/9/9 (각 9) | 2.2723 | 0.4793 | 0.4736 | -1.19% | 9/9 | 18/0 |
| mass_1.15 | 9/9/9 (각 9) | 2.8916 | 1.1304 | 1.2125 | +7.26% | 0/9 | 0/0 |
| mass_1.30 | 9/9/9 (각 9) | 1.1433 | 0.6785 | 0.6882 | +1.42% | 0/9 | 0/0 |
| gain_0.8 | 9/9/9 (각 9) | 2.2513 | 0.5529 | 0.5499 | -0.54% | 9/9 | 9/0 |
| gain_1.2 | 9/9/9 (각 9) | 2.2658 | 0.4504 | 0.4584 | +1.78% | 0/9 | 0/0 |
| lag_0.02 | 9/9/9 (각 9) | 0.7390 | 0.3252 | 0.3374 | +3.75% | 3/9 | 9/4 |
| lag_0.05 | 9/9/9 (각 9) | 3.5493 | 5.7050 | 5.7050 | +0.00% | 0/9 | 0/2873 |
| friction_0.2 | 9/9/9 (각 9) | 0.4723 | 0.3060 | 0.3220 | +5.20% | 0/9 | 9/0 |
| friction_0.8 | 9/9/9 (각 9) | 2.1516 | 0.4453 | 0.4393 | -1.36% | 8/9 | 8/0 |
| step_gain_0.8 | 9/9/9 (각 9) | 2.3414 | 0.5490 | 0.5455 | -0.63% | 9/9 | 9/0 |

Drift는 기존 평가와 같은 cached world axle의 최대 planar displacement이며, sensor input은 synchronized state다. 표의 drift 평균은 완료 trial만 포함하고 paired 변화는 두 군 모두 완료한 동일 seed/pitch끼리 계산한다. 완료 수가 9보다 적으면 survivor 평균만으로 개선이라고 판단하지 않는다. 평균±sample SD, final drift, tail 12초 속도/encoder path drift, odometry error는 paired_comparisons.json/metrics.csv에 있다.

| 조건 | G/F-1 Pitch RMS 비 | G/F-1 실제 wheel torque RMS 비 | G α 중심값 범위 |
|---|---:|---:|---:|
| nominal | 1.0000 | 1.0024 | 1.00–1.00 |
| mass_1.15 | 0.9991 | 1.0680 | 1.00–1.00 |
| mass_1.30 | 1.0001 | 0.9999 | 1.00–1.00 |
| gain_0.8 | 1.0001 | 1.2380 | 1.10–1.10 |
| gain_1.2 | 0.9999 | 1.0018 | 1.00–1.00 |
| lag_0.02 | 0.9998 | 0.9993 | 0.80–1.00 |
| lag_0.05 | 1.0000 | 1.0000 | 1.00–1.00 |
| friction_0.2 | 1.0002 | 0.9999 | 0.90–0.90 |
| friction_0.8 | 1.0003 | 1.0029 | 1.00–1.10 |
| step_gain_0.8 | 1.0001 | 1.2455 | 1.10–1.10 |

## 탐색만 유지한 대조 진단

주 비교군 A/F-1/G와 별도로 nominal, mass_1.15, gain_0.8, step_gain_0.8의 각 9초기조건에서 G-probe를 실행했다(36회). G와 같은 탐색·guard·cost 계산을 유지하되 centre_step=0으로 α 중심값을 1에 고정했다. G 대 F-1 차이에 gain 학습과 탐색 효과가 섞이는 것을 확인하는 진단이다.

| 조건 | F-1 drift m | G-probe drift m | G drift m | G−G-probe 평균 drift m |
|---|---:|---:|---:|---:|
| nominal | 0.4793 | 0.4929 | 0.4736 | -0.01931 |
| mass_1.15 | 1.1304 | 1.2125 | 1.2125 | +0.00000 |
| gain_0.8 | 0.5529 | 0.5839 | 0.5499 | -0.03395 |
| step_gain_0.8 | 0.5490 | 0.5792 | 0.5455 | -0.03369 |

## 해석 및 다음 단계 판단

이번 분석에서 실용적인 추가 개선 기준(9/9 완료, paired 평균 drift ≥5% 감소, ≥7/9쌍 개선, 평균 pitch RMS ≤110%, wheel RMS ≤125%)을 충족한 조건: 없음. 5%/7쌍 및 허용 비율은 결과를 과장하지 않기 위한 보고 기준이며 사용자 지정 기준이 아니다. 작은 음의 paired 차이는 raw metric 개선으로 남기되 강건성 회복 성공과 동일하게 취급하지 않는다.

특히 50 ms lag에서 G의 accepted updates 합계는 0, guard activation events 합계는 2873였다. 반복되는 센서 guard가 평가 창과 cooldown을 재설정해 탐색/학습이 진행되지 않았다. 실제 α와 residual 및 물리 궤적도 F-1과 같았다. 안정적으로 넘어지지 않는 것과 drift 복구는 서로 다른 결과다.

Residual hard cap 때문에 α 증가가 사용할 수 있는 최대 보정 토크를 늘리지는 않는다. 포화 비율은 residual_limit_fractions.json에 기록했다. 탐색 구간의 비용 gradient와 전체 episode의 최대 GT planar drift는 서로 다른 목표이며 gain 변화가 센서 cost를 줄여도 GT 2D 위치 유지가 보장되지는 않는다. Encoder 경로에는 yaw/slip 및 추정 오차가 남는다.

ABBA/BAAB와 quadratic time trend를 사용해 단순한 시간 감소를 학습 효과로 해석하는 오류를 줄였지만, 상태 carry-over, 동역학 변화 중의 비선형 추세, 비용 window의 직렬 상관은 완전히 분리하지 못한다. G-probe 대조도 탐색 순서 하나의 국소 진단이다. Gain 학습이 유익하다는 주장은 G/F-1만 아니라 G/G-probe와 함께 판단해야 한다.

단일 α 검증에서 고정 F-1보다 분명한 강건성 회복 근거가 확보되지 않으면 k_p/k_v 두 계수로 확대하거나 Online Dynamics Identification/LQR로 돌아가지 않는다. 이번 실험은 두 계수 적응을 구현하지 않았다: NOT_TESTED.

## Phase 4 — Sim2Real 준비 상태

현재 결과만으로 실제 TITA 온라인 적응 실행의 근거가 충분하다고 판단하지 않는다. Hardware 명령·배포는 수행하지 않았다. 실기 준비에서 필요한 항목은 encoder/IMU timestamp 정렬, wheel torque/current 단위와 축 부호, 기존 velocity PD에 residual을 더할 수 있는 인터페이스, command saturation/rate limit 확인이다. 이 항목의 실기 검증은 NOT_TESTED이며 본 결과는 시뮬레이터 검증에 한정한다.

## 실행·무결성·변경 범위

- 본 결과: 12초 baseline 162 + 60초 A/F-1/G 270 + G-probe 36 = 468 episodes. Smoke와 단위 검사 rollouts는 주 결과에서 제외한다. 같은 3 seeds×3 pitch, grounded pose/initial velocity, physics/control dt=0.005/0.02초, 기존 3초의 12 N/0.1초 외란을 유지했다.
- Integrity PASS: archive 90회 정확 재현; 60초 A/F-1의 12초 baseline prefix 및 G의 탐색 전 4초 prefix 정확 일치. Initial state·leg torque·history·gradient 오차 0. wheel 합산 최대 오차 4.77e-07 Nm(float32), 센서 window cost 재구성 최대 오차 0. GT 배열은 평가에만 사용했다.
- Unit tests PASS (5개): 시간 추세와 실제 probe gradient 분리, 무효과 비용의 갱신 거부/guard, 적응 비활성 G와 F-1의 실제 mismatch rollout 정확 동등성. 추가 hard-bound 검사는 unit_tests_final.log를 참조한다.
- 초기 guard 카운터가 시작 전/cooldown 중의 활성화를 누락하는 로깅 문제를 발견해 latch만 수정했다. 제어 계산은 변경하지 않았다. 모든 G/G-probe 126회 저장 센서·명령을 새 코드로 재입력하여 적용 α·중심값·accepted/rejected가 전체 tick에서 정확히 동일함을 확인했다(guard_sensor_replay.json). 원본 simulation results/NPZ/source snapshot은 보존하고 표의 guard 횟수만 sensor replay로 보정했다. 본 수정 후 468회 전체를 물리 재실행한 것으로 주장하지 않는다.
- 초기 report_generation*.log의 분석 실패는 NumPy window indexing 및 float32 토크 RMS의 batched reduction 반올림 차이였다. 명령 RMS를 제어기와 같은 per-tick 순서로 재구성해 수정했고, 최종 window cost 재구성 오차는 0이다. 실험 데이터는 변경하지 않았다.
- ./scripts/agent-check.sh PASS: agent_check.log. 최종 diff 및 기존 hash/Git 상태 보존 기록: final_review.json/task.diff.
- 기존 소스/설정/보고서는 수정하지 않았다. 신규 test/eval_online_residual_gain.py, test/eval_online_residual_probe_control.py, test/test_online_residual_gain.py, test/analyze_online_residual_gain.py, test/audit_online_residual_sensor_replay.py와 본 날짜의 결과만 추가했다.
- 브랜치: agent/codex/dev_tita_gluon. Actor checkpoint는 동일한 model_100000이며 재학습·RLS·LQR gain 갱신 없음.
- 초기 조건은 9개 결정론적 조합이며 세 seeds 아래 pitch 3개가 묶여 있다. 9개 독립 무작위 표본으로 해석하지 않는다. Longer horizon·다른 지형/명령·센서 잡음·실제 하드웨어 강건성은 NOT_TESTED.

## 재현

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_online_residual_gain.py
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase baseline --conditions nominal mass_1.15 mass_1.30 --output docs/exp/2026-10-15/new_gain/baseline_mass
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase baseline --conditions gain_0.8 gain_1.2 lag_0.02 --output docs/exp/2026-10-15/new_gain/baseline_motor
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase baseline --conditions lag_0.05 friction_0.2 friction_0.8 --output docs/exp/2026-10-15/new_gain/baseline_contact
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase online --conditions nominal mass_1.15 mass_1.30 --output docs/exp/2026-10-15/new_gain/online_mass
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase online --conditions gain_0.8 gain_1.2 lag_0.02 --output docs/exp/2026-10-15/new_gain/online_motor
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase online --conditions lag_0.05 friction_0.2 friction_0.8 --output docs/exp/2026-10-15/new_gain/online_contact
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_gain.py --phase online --conditions step_gain_0.8 --output docs/exp/2026-10-15/new_gain/online_step
```

이번 실행은 baseline을 baseline_mass/baseline_motor/baseline_contact 3묶음, online을 online_mass/online_motor/online_contact/online_step로 나누어 독립 프로세스로 실행했다. 모든 실제 argv 대응 conditions/duration/source hash는 각 manifest.json, 실행 당시 source는 runner_source.txt에 있다. 분석기는 동일한 폴더 이름을 요구한다.

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_online_residual_probe_control.py --output docs/exp/2026-10-15/new_gain/probe_control
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/audit_online_residual_sensor_replay.py --root docs/exp/2026-10-15/new_gain
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_online_residual_gain.py --root docs/exp/2026-10-15/new_gain --report docs/exp/2026-10-15/new_gain_summary.md
./scripts/agent-check.sh
```

산출물: [online_residual_gain/comparison.png](online_residual_gain/comparison.png), metrics.csv, paired_comparisons.json, probe_control_comparison.json, practical_success.json, adaptation_events.json, integrity.json, 각 episode NPZ 및 manifest/results.jsonl.
