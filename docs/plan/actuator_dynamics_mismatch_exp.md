현재 Isaac Lab에서 PPO로 학습한 TITA 정책의 **zero-command stationary balance 실패 원인**을 분석하기 위한 simulation experiment를 구현해 주세요.

이번 작업의 목적은 residual policy를 학습하는 것이 아닙니다.
기존 PPO 정책을 완전히 고정한 상태에서, simulation actuator에 delay와 motor lag를 추가했을 때 제자리 정지 성능이 어떻게 변하는지 정량적으로 검증하는 것이 목적입니다.

# 1. 핵심 연구 가설

현재 PPO 정책은 이상적인 Isaac Lab actuator 환경에서는 속도 명령 추종과 외란 복원 성능이 좋습니다.

하지만 실제 로봇에서는 다음 actuation mismatch가 존재할 가능성이 있습니다.

1. Command transport delay
2. Motor response lag
3. Joint target tracking dynamics
4. Control-cycle jitter

이러한 mismatch 때문에 zero velocity command에서 stationary equilibrium을 유지하지 못하고 다음 현상이 발생한다는 가설을 검증합니다.

* pitch oscillation
* wheel의 앞뒤 왕복
* base position drift
* joint action chatter
* stationary limit cycle
* 최종 balance failure

# 2. 작업 원칙

다음 사항을 반드시 지켜 주세요.

* 기존 PPO checkpoint는 수정하거나 재학습하지 않습니다.
* PPO actor parameter는 완전히 freeze합니다.
* reward, observation, action scale을 임의로 변경하지 않습니다.
* 기존 환경의 기본 동작은 그대로 보존합니다.
* actuator delay와 lag가 모두 0일 때 기존 코드와 수치적으로 동일하게 동작해야 합니다.
* 아직 TD3, SAC, residual policy는 구현하지 않습니다.
* 우선 원인 분석과 실험 인프라만 구현합니다.
* action이 실제 actuator command에 전달되는 경로를 먼저 추적한 뒤, 올바른 위치에 actuation model을 삽입합니다.
* 정책 action이 joint position target, position residual, velocity target, torque 중 무엇인지 코드에서 확인하고 문서화합니다.

# 3. 먼저 수행할 코드 분석

현재 프로젝트에서 다음 흐름을 추적해 주세요.

```text
PPO actor output
→ action scale / offset
→ joint ordering or reindexing
→ desired joint command
→ PD controller or actuator model
→ torque
→ physics simulation
```

다음을 정확히 확인해 주세요.

* policy control frequency
* simulation physics frequency
* decimation
* policy action dimension
* action scale과 clip 범위
* action이 position target인지 torque인지
* PD stiffness와 damping
* actuator class와 actuator configuration
* joint별 torque/velocity limit
* previous action이 observation에 들어가는 timing
* action이 계산된 step과 physics에 적용되는 step의 관계

분석 결과를 별도의 Markdown 문서로 작성해 주세요.

# 4. 구현할 actuator mismatch model

actuation mismatch를 다음 세 요소로 분리해서 독립적으로 켜고 끌 수 있게 구현해 주세요.

## 4.1 Fixed action delay

정책이 출력한 action을 FIFO queue에 저장하고, 설정한 step만큼 이전 action을 actuator에 전달합니다.

[
a_t^{delay}=a_{t-d}^{policy}
]

설정 예시:

```yaml
actuation_delay:
  enabled: false
  steps: 0
```

초기화 직후 queue가 비어 있을 때는 다음 중 현재 환경에 가장 안전하고 일관적인 방식을 선택하고 문서화해 주세요.

* 최초 policy action으로 채우기
* zero action으로 채우기
* nominal/default joint target으로 채우기

## 4.2 First-order motor lag

delay가 적용된 command가 실제 actuator command로 즉시 바뀌지 않고, 1차 지연 시스템을 따라가도록 구현합니다.

[
a_t^{applied}
=============

a_{t-1}^{applied}
+
\alpha
\left(
a_t^{delay}-a_{t-1}^{applied}
\right)
]

[
\alpha=1-\exp\left(-\frac{\Delta t}{\tau}\right)
]

여기서:

* (\Delta t): policy action이 갱신되는 실제 시간 간격
* (\tau): motor time constant
* (\tau=0): lag 없음

설정 예시:

```yaml
motor_lag:
  enabled: false
  time_constant_sec: 0.0
```

가능하면 scalar time constant와 joint별 time constant를 모두 지원해 주세요.

```yaml
time_constant_sec: 0.03
```

또는:

```yaml
time_constant_per_joint_sec:
  - 0.03
  - 0.03
  - ...
```

## 4.3 Random delay 또는 jitter

고정 delay 실험이 완료된 후 사용할 수 있도록 옵션만 구현합니다.

```yaml
actuation_jitter:
  enabled: false
  min_delay_steps: 0
  max_delay_steps: 2
  resample_every_policy_step: true
```

초기 실험에서는 비활성화합니다.

# 5. 모델 삽입 위치

motor lag model은 가능한 한 다음 순서로 적용해 주세요.

```text
raw PPO action
→ 기존 action scale / offset / clip
→ fixed action delay
→ first-order motor lag
→ 기존 joint command 및 actuator controller
→ physics
```

단, 현재 action semantics와 actuator 구조를 분석한 결과 이 위치가 물리적으로 부적절하다면 더 적절한 위치를 선택하고 이유를 문서화해 주세요.

특히 다음을 구분해 주세요.

* policy target 자체의 delay/lag
* PD torque 출력의 delay/lag
* 실제 joint state response의 lag

이번 첫 실험에서는 **정책이 생성한 actuator command의 delay와 lag**를 모델링하는 것을 우선합니다.

# 6. 단위 테스트

전체 PPO 평가 전에 actuator model 자체를 검증하는 테스트를 추가해 주세요.

## Step-response test

한 개 또는 전체 관절에 다음 command를 입력합니다.

```text
0 → constant target
```

그리고 다음을 기록합니다.

* raw policy/command input
* delayed command
* lag-filtered applied command
* measured joint response

다음을 확인해야 합니다.

* delay만 켜면 설정한 step만큼 정확히 늦게 시작
* lag만 켜면 지수적으로 target에 접근
* delay와 lag를 함께 켜면 delay 이후 지수 응답
* delay=0, tau=0이면 입력과 applied command가 동일
* environment reset 시 queue와 lag state가 올바르게 초기화

간단한 자동화 테스트와 step-response plot을 생성해 주세요.

# 7. Frozen PPO stationary experiment

기존 PPO checkpoint를 고정하고 zero command에서 제자리 유지 성능을 평가합니다.

## Command

```text
vx = 0
vy = 0
yaw_rate = 0
```

## 초기 상태

최소한 다음 조건을 포함해 주세요.

1. nominal standing initial state
2. 작은 forward pitch perturbation
3. 작은 backward pitch perturbation
4. 작은 joint position perturbation
5. 가능하다면 작은 external push

perturbation 크기는 로봇을 즉시 넘어뜨리지 않는 안전한 범위로 설정합니다.

## Episode duration

기존 environment 설정을 우선 사용하되, stationary drift와 oscillation을 확인할 수 있도록 충분한 길이로 평가합니다.

예를 들어 20–30초 평가가 가능하도록 구성하되 기존 시스템의 control frequency와 episode 설정에 맞춰 결정해 주세요.

# 8. 실험 조건

최소한 다음 네 종류를 독립적으로 비교합니다.

## Condition A: Ideal actuator

```text
delay = 0
tau = 0
```

## Condition B: Delay only

```text
delay > 0
tau = 0
```

## Condition C: Lag only

```text
delay = 0
tau > 0
```

## Condition D: Delay + lag

```text
delay > 0
tau > 0
```

초기 parameter sweep은 실제 policy frequency에 맞춰 다음 수준을 포함하도록 구성해 주세요.

### Delay

```text
0, 1, 2, 3 policy steps
```

### Motor time constant

```text
0, 10 ms, 20 ms, 40 ms, 80 ms
```

단, control frequency를 확인한 뒤 의미 없는 조합은 조정해도 됩니다.

모든 실험 조건은 CLI 또는 config로 재현 가능해야 합니다.

예:

```bash
python evaluate_stationary.py \
  --checkpoint <checkpoint_path> \
  --delay-steps 2 \
  --motor-tau 0.04 \
  --num-episodes 20 \
  --seed 0
```

# 9. 평가 지표

각 episode에 대해 최소한 다음 값을 기록해 주세요.

## Stationary performance

* base x/y position drift
* planar displacement
* yaw drift
* base linear velocity RMS
* base angular velocity RMS
* wheel velocity RMS
* wheel position drift

## Balance performance

* roll RMS / maximum
* pitch RMS / maximum
* roll rate RMS
* pitch rate RMS
* base height mean / minimum
* termination 여부
* termination reason
* time to failure

## Actuator tracking

* raw policy action
* delayed action
* lag-filtered applied action
* measured joint position
* measured joint velocity
* desired–measured joint tracking error
* per-joint tracking-error RMS
* action–response cross-correlation 또는 estimated phase lag

## Action behavior

* policy action RMS
* applied action RMS
* action rate RMS
* action second-difference 또는 jerk proxy
* saturation ratio
* dominant oscillation frequency

가능하다면 pitch, wheel velocity 및 action signal에 대해 FFT 또는 PSD를 계산해 dominant oscillation frequency를 기록해 주세요.

# 10. 반복 실험

각 조건에서 여러 seed와 여러 initial perturbation으로 반복 평가해 주세요.

최소 권장:

```text
5 seeds × 4 initial-condition types
```

계산 비용이 크면 먼저 짧은 pilot 실험을 수행한 후 전체 sweep을 실행할 수 있게 구성합니다.

환경 개수가 많더라도 모든 environment의 metric을 무조건 평균내지 말고, episode별 결과와 aggregate 결과를 모두 저장해 주세요.

# 11. 결과 저장

다음 구조로 결과를 저장해 주세요.

```text
results/actuation_mismatch/
  experiment_config.yaml
  summary.csv
  episode_metrics.csv
  joint_metrics.csv
  trajectories/
  plots/
  report.md
```

`summary.csv`에는 condition별 mean, standard deviation, failure rate를 저장합니다.

# 12. 필수 그래프

최소한 다음 그래프를 생성해 주세요.

1. Delay/tau에 따른 pitch RMS heatmap
2. Delay/tau에 따른 base position drift heatmap
3. Delay/tau에 따른 failure rate heatmap
4. 대표 episode의 pitch time series
5. 대표 episode의 wheel velocity time series
6. raw action vs delayed action vs applied action
7. desired joint position vs measured joint position
8. delay/tau에 따른 joint tracking-error RMS
9. pitch와 wheel velocity의 PSD
10. stationary performance와 actuator mismatch 크기의 관계

그래프는 condition과 parameter가 명확히 구분되도록 작성해 주세요.

# 13. 성공 판정

다음 현상이 확인되면 1차 가설을 지지하는 것으로 판단합니다.

1. Ideal actuator에서는 PPO가 안정적으로 정지함
2. Delay 또는 lag가 커질수록 stationary drift나 oscillation이 증가함
3. 특정 delay/lag 영역에서 실물에서 관찰한 것과 유사한 limit cycle 또는 balance failure가 재현됨
4. moving command tracking보다 zero-command standing이 actuation mismatch에 더 민감함
5. action과 joint response 사이의 phase lag 증가가 balance 성능 저하와 상관관계를 가짐

반대로 다음 결과라면 motor lag 가설이 약하다고 판단해야 합니다.

* 상당한 delay/lag를 추가해도 standing 성능 변화가 거의 없음
* 실물과 전혀 다른 failure mode만 나타남
* actuator tracking error와 stationary failure 사이의 관계가 없음
* ideal simulation에서도 이미 정지하지 못함

결과를 가설에 맞추지 말고, 위 반증 결과도 그대로 보고해 주세요.

# 14. 선택적인 moving sanity check

주요 실험은 stationary zero-command입니다.

추가로 소수의 moving command에서 다음만 확인해 주세요.

```text
vx = low positive velocity
vx = low negative velocity
yaw_rate = low positive command
```

목적은 동일한 delay/lag가 moving tracking과 stationary regulation에 미치는 영향이 다른지 확인하는 것입니다.

새로운 locomotion benchmark를 만드는 작업으로 범위를 확대하지 마세요.

# 15. 최종 산출물

다음을 제출해 주세요.

1. 현재 action-to-actuator 경로 분석 문서
2. configurable delay/lag actuator model
3. unit test 및 step-response 검증
4. frozen PPO stationary evaluation script
5. reproducible experiment configs
6. CSV metric outputs
7. 자동 생성 그래프
8. 실험 결과를 요약한 `report.md`
9. 변경된 파일 목록과 각 파일의 역할
10. 실행 명령어
11. 기존 no-delay 동작이 유지된다는 regression test 결과

`report.md` 마지막에는 다음 질문에 명확하게 답해 주세요.

* Ideal simulation에서 정책은 실제로 안정적으로 정지하는가?
* Delay만으로 정지 실패가 재현되는가?
* Motor lag만으로 정지 실패가 재현되는가?
* Delay와 lag를 함께 넣을 때 failure가 더 잘 재현되는가?
* 어떤 parameter 영역이 실물 현상과 가장 유사한가?
* 현재 결과만으로 actuation mismatch가 주요 원인이라고 말할 수 있는가?
* 다음 단계로 residual policy 학습을 진행할 근거가 충분한가?

이번 작업에서는 residual policy를 구현하지 마세요.
우선 frozen PPO와 actuator mismatch만으로 원인 가설을 검증하는 데 집중해 주세요.
