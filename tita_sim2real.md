# TITA RL Closed-Loop Validation & Sim-to-Real — A to Z

> 검토 기준일: **2026-09-02 (Asia/Seoul)**
>
> 문서 작성 실행 도메인: `DESKTOP_DRY_RUN`
>
> 범위: **TITA 바퀴-다리 로봇만 포함**. GLUON 로봇팔, TITA+GLUON 결합 task, inspection/high-level WBC 실험은 제외한다.
>
> 본 감사 중 실물 연결·서비스 변경·모터 명령·정책 배포: **0회**
>
> 현재 종합 상태: `SUSPICIOUS` — 학습·ONNX·MuJoCo·단계식 실기 인프라는 존재하지만, 기본 Sim2Sim 설정이 현재 정책과 불일치하고 실기 Stage 3에서 약 6 Hz 진동 및 watchdog 진입이 남아 있다.

이 문서는 현재 working tree의 문서, Python/C++ 구현, YAML, ONNX 인터페이스와 해시, `/docs/exp/` 기록, 레거시 JSON/CSV를 서로 대조한 TITA 전용 기준서다. 단순 사용법이 아니라 다음 질문에 답하도록 구성했다.

- 어떤 task와 알고리즘으로 무엇을 학습하는가?
- 정책이 받는 33개 값과 내보내는 8개 값은 정확히 무엇인가?
- Isaac Lab, ONNX, MuJoCo, ROS 2, 실제 모터 사이에서 순서·단위·주기가 어떻게 이어지는가?
- 이 프로젝트에서는 왜 NP3O보다 estimator PPO가 더 적합했는가?
- 어떤 실험이 실제로 수행됐고, 무엇은 아직 주장할 수 없는가?
- 실물 연결부터 read-only, command-free, staged Sim2Real까지 어디서 멈춰야 하는가?
- 취업·면접에서 이 프로젝트를 과장 없이 어떻게 설명할 수 있는가?

---

## 1. 결론부터: 현재 무엇이 되고 무엇이 안 되는가

| 항목 | 현재 판정 | 직접 확인된 근거 |
|---|---|---|
| TITA `My-v0` estimator PPO 학습 경로 | `PASS` | Gym 등록이 `rsl_rl_cfg_entry_point=TitaFlatEstimatorPPORunnerCfg`를 가리키고 My41~45 학습 로그가 존재한다. |
| PPO ONNX 단일 입력 계약 | `PASS` | My43/My45 및 현재 `policy.onnx`를 직접 검사: `nn_input0 [1,33] -> nn_output [1,8]`. |
| NP3O exporter 이중 입력 계약 | `PASS` | NP3O exporter 구현은 현재 관측 `[1,33]` + history `[1,10,33]` -> action `[1,8]`을 명시한다. `policy_my7rsl.onnx`도 같은 shape의 legacy 호환 artifact지만 NP3O 산출물이라는 provenance는 확인되지 않았다. |
| DDT 계열 Isaac↔MuJoCo 수치 인터페이스 parity | `PASS` | 통제 입력에서 관측 차이 0, raw action 최대 차이 `2.98e-7`; action scale까지 맞춘 첫 tick도 수치 일치. |
| 기본 `sim2sim/cosim_ros2_jazzy/config/tita.yaml` launch 준비도 | `FAIL` | YAML은 history 10/이중 입력을 요구하지만 deploy 기본 `policy.onnx`는 단일 입력이다. strict runner가 `nn_input1` 누락으로 시작 단계에서 실패했다. |
| 명시적 My43/My45 Sim2Sim 설정 | `PASS` | 각각 history 0/단일 입력이며 실행·드리프트 기록이 있다. My43@2700의 5 s zero-command drift `0.022 m`가 비교군 중 최저다. |
| Read-only TITA 상태 획득 | `SUSPICIOUS` | IMU/joint는 약 441/443 Hz로 양호하지만 stereo 비동기·TF 오타, ultrasonic/Tower 비활성 문제가 남았다. |
| 실기 Stage 1/2 | `PASS` | historical real test에서 TransformUp+5 s settle, 1 s zero-command RL과 SAFE_HOLD까지 통과했다. |
| 실기 Stage 3/자유 주행 | `SUSPICIOUS` | 29.162 s 후 각속도 watchdog으로 SAFE_HOLD, 약 6 Hz pitch/L1/R1 진동 지속. |
| unrestricted Sim2Real 승인 | `BLOCKED` | certified E-stop, graceful Direct→MCU rollback, process/SBC/CAN loss 안전, 광범위 주행 안정성이 확인되지 않았다. |

핵심 운영 결론은 다음과 같다.

1. **현재 주력 DDT `My-v0`는 NP3O가 아니라 estimator PPO다.** `lab/README.md`, `docs/manual.md`, task 등록 파일의 “모든 TITA가 NP3O” 주석은 현재 코드와 다르다.
2. **현재 기본 launch를 그대로 실행하면 안 된다.** `config/tita.yaml`과 `policy.onnx`의 입력 수가 다르다. 검증에는 checkpoint별 YAML을 명시해야 한다.
3. **zero-command 기준 최선의 기록은 My43@2700**이다. My44는 학습 평균 reward가 가장 높았지만 실제 drift와 deceleration behavior는 퇴보했다. 즉 checkpoint 선택은 학습 reward만으로 하면 안 된다.
4. **PPO가 보편적으로 NP3O보다 우월하다고 증명된 것은 아니다.** 동일 환경·seed·step budget의 직접 A/B 기록이 없다. 다만 단일 입력 실기 runner, zero-cost NP3O, 풍부한 My 계열 검증을 고려하면 이 저장소에서는 PPO가 더 나은 **운용 선택**이었다.
5. **실기 정책 실행은 아직 연구 단계**다. Git 배포나 ONNX 복사는 실물 구동 승인이 아니며, 현재 증거는 unrestricted locomotion을 허용하지 않는다.

---

## 2. 증거를 읽는 규칙과 source-of-truth

### 2.1 증거 상태

- `PASS`: 해당 범위의 명령/검사가 직접 실행됐고 로그가 있다.
- `SUSPICIOUS`: 실행은 됐지만 품질·안전·동등성 또는 provenance가 불충분하다.
- `BLOCKED`: 필요한 근거나 안전 조건이 없어 다음 결론/단계로 갈 수 없다.
- `FAIL`: 명시된 계약 또는 test가 실제로 실패했다.
- `NOT_TESTED`: 계획·설정·코드는 있으나 해당 동작을 실행한 증거가 없다.

`PASS`는 항상 **행 단위 범위**로 해석해야 한다. 예를 들어 “ONNX shape `PASS`”는 보행 안정성 `PASS`가 아니고, “20 s no-crash `PASS`”는 정책 품질 `PASS`가 아니다.

### 2.2 신뢰 우선순위

충돌 시 다음 순서로 판단한다.

1. 현재 실행 코드와 task 등록
2. 현재 ONNX graph의 실제 input/output와 SHA256
3. checkpoint와 함께 저장된 `params/env.yaml`, `params/agent.yaml`
4. `/docs/exp/YYYY-MM-DD/*.md`의 실제 실행 로그
5. checkpoint별 Sim2Sim YAML provenance 주석
6. README, 오래된 매뉴얼, 소스 주석
7. `/docs/plan/`의 계획 문서

현재 working tree에는 사용자의 광범위한 기존 변경이 있고 이 문서는 특정 clean commit이 아니라 그 상태를 감사했다. 그러므로 재현 시에는 **코드 commit + env/agent YAML + checkpoint SHA256 + ONNX SHA256 + Sim2Sim YAML**을 한 묶음으로 고정해야 한다.

### 2.3 확인된 문서/코드 드리프트

| 충돌 | 실제 현재 상태 | 처리 원칙 |
|---|---|---|
| README가 `My-v0`를 NP3O 명령으로 안내 | Gym 등록은 estimator PPO | `lab/ddt_lab/scripts/rsl_rl/train.py` 사용 |
| README가 모든 TITA ONNX를 2-input이라 설명 | My26 이후 estimator PPO는 1-input | ONNX를 직접 검사 |
| `config/tita.yaml`은 2-input, 현재 `policy.onnx`는 1-input | startup `FAIL` | checkpoint 전용 YAML 명시 |
| `docs/manual.md`가 deploy script를 command-free처럼 표현 | script는 로컬 설정 수정, 원격 복사·빌드를 수행 | `ROBOT_STATE_CHANGING` 배포로 취급, 별도 승인 필요 |
| `docs/manual.md`의 `tita_stage1_controller play.launch.py` | 해당 launch가 현재 package에 없음 | 실제 SDK `direct_rl_mode.launch.py`, controller `stage1_hardware.launch.py`와 안전 문서를 기준으로 함 |
| SDK snapshot과 `tita_gluon_ws` controller | SDK는 2-input/history+handoff/blend, workspace는 1-input estimator/no-history의 더 단순한 FSM | 어느 tree를 빌드하는지 먼저 고정 |
| `torque_update_rate_hz: 250` | `isaac_reference_50hz` 코드 경로는 이 값을 쓰지 않으며 5 ms physics substep마다 torque를 재계산 | 실제 유효 주기는 physics 200 Hz, policy 50 Hz로 기록 |
| `MooStandDriveObservationBuilder`의 일부 오래된 순서 설명 | 실행 상수와 2026-08-20 audit는 interleaved Isaac order를 확인 | audit와 실행 상수 우선 |
| 소스가 `Experiments/RL_Experiments.md`, `Sim2Sim_Experiments.md`, `docs/plan_base_vel_estimator_ppo.md`를 참조 | 현재 저장소에 없음 | My2~40 전체 변화 복원은 `BLOCKED`; 남은 YAML 주석만 `SUSPICIOUS`로 인용 |
| 실기 Stage 결과가 `sdk/tita_low_level_sdk_ros2_humble/docs/TEST_STATUS.md`에만 있음 | 현재 규칙의 공식 위치는 root `docs/exp/YYYY-MM-DD/` | historical evidence로 인용하되 다음 실행부터 root `docs/exp/`에 hash/metadata와 함께 기록 |

---

## 3. 저장소 지도와 전체 폐루프

| 경로 | TITA에서의 역할 |
|---|---|
| `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/` | DDT NP3O/PPO 환경, reward, observation, event, task 등록 |
| `lab/ddt_lab/ddt_lab/algorithms/estimator/` | PPO에 3-D base velocity estimator를 결합한 actor/algorithm |
| `lab/ddt_lab/ddt_lab/algorithms/np3o/` | history encoder, Barlow Twins, cost critic를 가진 NP3O 포트 |
| `lab/ddt_lab/ddt_lab/tasks/moo_based/locomotion/velocity/tita_env/` | CO-RL MOO-PPO stand/drive 및 RMA teacher task/config |
| `lab/scripts/co_rl/` | CO-RL runner, MOO-PPO, discriminator, RMA teacher/student export |
| `sim2sim/cosim_ros2_jazzy/` | ROS 2 Jazzy + MuJoCo Sim2Sim, direct/relay/offline Real2Sim, ghost policy |
| `tita_gluon_ws/src/ddt_ros2_control/` | upstream 기반 HardwareBridge와 vendor/direct ROS 2 control 기반 |
| `tita_gluon_ws/src/tita_stage1_controller/` | 현재 단일 입력 estimator PPO용 fail-closed C++ controller |
| `sdk/tita_low_level_sdk_ros2_humble/` | pinned upstream과 단계식 Direct-mode reference snapshot/안전 문서 |
| `tita_gluon_ws/deploy/tita/` | ONNX, checkpoint별 평가 artifact, 레거시 Sim2Sim 결과 |
| `docs/exp/` | 규정상 공식 실험 기록 위치 |
| `test/` | test/debug/probe/log 전용 위치 |

전체 데이터 흐름은 다음과 같다.

```text
TRAINING_SIM
Isaac Lab state
  -> observation manager
  -> policy / critic / estimator
  -> 8-D action
  -> position/velocity action scaling
  -> delayed PD actuator
  -> PhysX
  -> checkpoint + params YAML

DESKTOP_DRY_RUN
checkpoint
  -> exporter adapter
  -> ONNX contract inspection + SHA256

VALIDATION_SIM
MuJoCo state
  -> matching observation builder
  -> ONNX Runtime
  -> matching action adapter
  -> PD/velocity torque + clamp
  -> corrected MJCF
  -> debug topics + quantitative probes

ROBOT_READ_ONLY
real joint/IMU/odom
  -> direct DDS OR TCP relay OR rosbag
  -> MuJoCo mirror / ghost policy
  -> no robot command publisher

ROBOT_COMMAND_FREE_RUNTIME
vendor idle + ownership/preflight/hash checks
  -> output remains disabled

ROBOT_STATE_CHANGING (별도 운영자 승인 필요)
vendor writer stop
  -> exact pinned Direct request
  -> one HardwareBridge + one controller
  -> measured-pose TransformUp
  -> 5 continuous stable seconds
  -> bounded RL
  -> SAFE_HOLD
  -> physically supported full power cycle
```

검증 사다리는 아래 순서를 건너뛰지 않는다.

```text
unit/static contract
-> Isaac playback
-> ONNX parity
-> deterministic MuJoCo
-> randomized/multi-seed MuJoCo
-> offline Real2Sim
-> live read-only Real2Sim
-> command-free on-robot preflight
-> Stage 1 posture only
-> Stage 2 bounded zero command
-> Stage 3 bounded low command
-> regression Sim2Sim
```

---

## 4. DDT TITA 환경: 학습 전에 반드시 알아야 할 계약

### 4.1 현재 Gym task와 알고리즘 연결

실제 등록 파일은 `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/__init__.py`다.

| Gym ID | 환경 | 현재 runner | 용도 |
|---|---|---|---|
| `DDT-Velocity-Flat-Tita-v0` | `TitaFlatEnvCfg` | NP3O | flat baseline |
| `DDT-Velocity-Flat-Tita-Play-v0` | play config | NP3O | baseline evaluation/export |
| `DDT-Velocity-Flat-Tita-My-v0` | `MyTitaFlatEnvCfg` | **RSL-RL estimator PPO** | 현재 Sim2Real-oriented 주력 |
| `DDT-Velocity-Flat-Tita-My-Play-v0` | play config | **RSL-RL estimator PPO** | 주력 evaluation/export |
| `DDT-Velocity-Flat-Tita-Jump-v0` | jump | NP3O | jump 연구 |
| `DDT-Velocity-Rough-Tita-v0` | rough | NP3O | rough terrain 연구 |

따라서 My task를 NP3O script로 실행하는 README 예시는 현재 `FAIL` 가능성이 있는 stale 안내다. runner entry key 자체가 다르므로 task와 script는 반드시 함께 맞춰야 한다.

### 4.2 시뮬레이션과 제어 주기

- Isaac physics timestep: `0.005 s` = **200 Hz**
- action decimation: `4`
- policy/action update: `0.020 s` = **50 Hz**
- episode: `20 s`
- MuJoCo My 계열: 동일하게 physics 200 Hz, policy 50 Hz, 한 action을 4 physics step 유지
- MuJoCo `rl_0`: action은 50 Hz에 계산하지만 PD/velocity torque는 매 5 ms substep의 최신 `q,dq`로 다시 계산
- 실제 C++ stack: controller/writer **500 Hz**, policy **50 Hz**

`sim2sim` YAML의 `timing.torque_update_rate_hz: 250`는 `isaac_reference_50hz` 코드 분기에서 사용되지 않는다. 실제 runtime을 설명할 때 250 Hz라고 말하면 안 된다.

### 4.3 TITA joint order는 두 가지다

```text
MuJoCo native / DDT action order:
[L1, L2, L3, L4, R1, R2, R3, R4]

Isaac observation joint order:
[L1, R1, L2, R2, L3, R3, L4, R4]

native -> observation reindex:
[0, 4, 1, 5, 2, 6, 3, 7]
```

중요한 비대칭은 의도적이다.

- observation의 joint position/velocity는 interleaved order다.
- DDT action head는 native left-chain-first order다.
- 따라서 observation에는 reindex가 필요하지만 DDT action output에는 reindex를 넣으면 안 된다.
- MOO-PPO는 이와 다른 action order를 사용하므로 별도 adapter가 필요하다.

### 4.4 DDT 33-D policy observation

정확한 벡터는 `rough_env_cfg.py::ObservationsCfg.PolicyCfg`, MuJoCo `obs_builder.py::ObservationBuilder`, C++ `rl_pipeline.cpp`에서 맞춰진다.

| Slice | 크기 | 값 | 순서/스케일 | 학습 noise |
|---|---:|---|---|---|
| `0:3` | 3 | body-frame base angular velocity | xyz × `0.25` | uniform `[-0.2, 0.2]` |
| `3:6` | 3 | projected gravity | xyz × `1.0` | uniform `[-0.05, 0.05]` |
| `6:9` | 3 | commanded velocity | `[vx, vy, wz] × [2, 2, 0.25]` | 없음 |
| `9:17` | 8 | joint position relative to default | interleaved; wheel position slots는 0으로 만든 뒤 default를 뺌 | uniform `[-0.01, 0.01]` |
| `17:25` | 8 | joint velocity | interleaved × `0.05` | uniform `[-1.5, 1.5]` |
| `25:33` | 8 | previous raw action | **DDT native action order** × `1.0` | 없음 |

수식으로는 다음과 같다.

```text
o_t = concat(
  0.25 * omega_body,
  R_body_world^T * [0,0,-1],
  [2*vx_cmd, 2*vy_cmd, 0.25*wz_cmd],
  reindex(q_without_wheel_position - q_default),
  0.05 * reindex(dq),
  a_(t-1)
)
```

주의할 점:

- actor는 true base linear velocity를 직접 받지 않는다.
- 학습 `My` actor에는 episode별 IMU/projected-gravity bias, gyro bias `±0.05`, encoder offset `±0.02 rad`가 추가된다. critic은 ground truth를 유지한다.
- MuJoCo의 standard builder는 이 33-D 계약을 재현하지만 학습 noise/bias sampling을 자동으로 복제하는 도구는 아니다.
- previous action은 직전 50 Hz policy output이고, history가 있는 구형/NP3O 정책은 초기 history 10칸을 현재 관측으로 채운다.

### 4.5 DDT 8-D action과 actuator 의미

```text
a_t order = [L1, L2, L3, L4, R1, R2, R3, R4]
```

| Joint | action 의미 | target | controller | limit |
|---|---|---|---|---|
| L1,L2,L3,R1,R2,R3 | default pose 주변 position residual | `q_des = q_default + 0.25*a` | `60*(q_des-q) - 1.5*dq` | effort `60 Nm`, velocity `30 rad/s` |
| L4,R4 wheels | velocity target | `dq_des = 5.0*a` | `0.5*(dq_des-dq)` | effort `12 Nm`, velocity `30 rad/s` |

기본 pose는 다음이다.

```text
[0.1, 0.8, -1.5, 0.0, 0.1, 0.8, -1.5, 0.0]
```

Isaac action config의 clip은 `[-100,100]`이어서 정상 action 범위에서는 사실상 unclipped다. 실제 보호는 actuator effort/velocity limit와 배포 stack의 target envelope/watchdog에서 온다.

### 4.6 물리 모델과 domain randomization

기본 TITA asset은 leg에 `DCMotorCfg`, wheel에 implicit actuator를 쓴다.

- leg: stiffness `60`, damping `1.5`, effort limit `60`, saturation effort `80`, velocity limit `30`
- wheel: stiffness `0`, damping `0.5`, effort limit `12`, velocity limit `30`
- 시작 base height: `0.4 m`

공통 randomization에는 다음이 포함된다.

- static/dynamic friction `0.2~1.6`, restitution `0~1`
- base mass additive `-0.5~+2.0 kg`
- inertia scale `0.9~1.1`
- base CoM xyz `±0.05 m`
- actuator Kp/Kd scale `0.8~1.2` log-uniform
- root pose/velocity 및 joint reset
- 주기적 push

`MyTitaFlatEnvCfg`는 leg/wheel을 `DelayedPDActuatorCfg(min_delay=0,max_delay=4)`로 교체해 episode별 `0~20 ms` delay를 학습한다. 단, 이 교체는 base `DCMotorCfg`의 **torque-speed saturation curve를 잃고 plain delayed PD가 된다.** effort/velocity 숫자는 유지되지만 motor physics가 완전히 동등한 것은 아니다. 이는 현재 Sim2Real gap의 중요한 미해결 항목이다.

### 4.7 command와 reward

현재 `My` command 설정:

- resampling `6~8 s`
- standing environment 비율 `10%`
- `vx in [-1,1] m/s`, `vy=0`, `wz in [-1.5,1.5] rad/s`
- non-stop command ramp `0.5 unit/s`

기본 reward 축은 선속도/회전속도 추종, z velocity, xy angular velocity, torque, joint acceleration, action rate, 좌우 mirror, undesired contact, flat orientation, base height다. 현재 My override의 핵심은 다음과 같다.

- linear velocity tracking `+2.0`
- yaw tracking `+1.0`
- xy angular velocity `-0.05`
- action rate `-0.01`
- hip deviation `-1.0`, shoulder deviation `-0.5`
- zero-command planar anchor reward `+1.0`, sharpness `8`, exact zero command에서만 활성
- zero-command wheel raw-action integral penalty `-0.05`, raw exponent `4`, accumulated error exponent `0.5`, exact zero command에서만 활성
- base external force/torque event는 현재 비활성

play config는 관측 corruption, push, mass/inertia/CoM/gain randomization, IMU/encoder bias를 끈다. 그러므로 play `PASS`는 randomized robustness `PASS`가 아니다.

---

## 5. 현재 주력: PPO + learned base-velocity estimator

### 5.1 네트워크 구조

구현은 다음 세 파일이 핵심이다.

- `algorithms/estimator/actor_critic_with_estimator.py`
- `algorithms/estimator/ppo_with_estimator.py`
- `robots/tita/agents/rsl_rl_ppo_cfg.py`

```text
raw proprio 33
  -> estimator normalizer
  -> estimator MLP [128, 64]
  -> estimated scaled base_lin_vel 3

concat(estimated velocity 3, raw proprio 33) = actor input 36
  -> actor normalizer
  -> actor MLP [512, 256, 128], ELU
  -> Gaussian action distribution
  -> action 8

critic observation
  -> true privileged state including base_lin_vel
  -> critic MLP [512, 256, 128]
  -> value
```

estimator target은 별도 observation group의 true body-frame base linear velocity × `2.0`이다. debug ONNX의 `est_vel`은 이 **scaled 값**이므로 m/s로 해석하려면 target scale을 되돌려야 한다.

중요한 구현 세부:

- estimator output은 actor 입력에 들어갈 때 `detach()`되지 않는다.
- 따라서 estimator는 supervised MSE뿐 아니라 actor PPO gradient도 받는다.
- `PPOWithEstimator.update()`는 RSL-RL `3.1.2` PPO update를 복사해 estimator loss를 삽입한 version-pinned 구현이다.
- RSL-RL upgrade 시 upstream PPO diff를 다시 검토하지 않으면 optimizer/loss 동작이 조용히 달라질 수 있다.
- `train.py`는 설치된 RSL-RL을 수정하지 않고 custom class를 runner namespace에 주입한다.
- actor, critic, estimator normalization이 모두 켜져 있다.

### 5.2 PPO 하이퍼파라미터

| 항목 | 값 |
|---|---:|
| rollout | `24 steps/env` |
| actor/critic hidden | `[512,256,128]`, ELU |
| estimator hidden/output | `[128,64] -> 3` |
| init noise std | `1.0` |
| clip parameter | `0.2` |
| value loss coefficient | `1.0` |
| estimator loss coefficient | `1.0` |
| entropy coefficient | `0.01` |
| epochs / minibatches | `5 / 4` |
| learning rate | `1e-3`, adaptive KL schedule |
| gamma / lambda | `0.99 / 0.95` |
| desired KL | `0.01` |
| max gradient norm | `1.0` |
| default max iterations | `2000` |
| checkpoint interval | `100` |
| seed | `42` |
| logger | W&B |

### 5.3 재현 가능한 학습

```bash
# Execution Domain: TRAINING_SIM
source /home/cocel/isaac/env_isaaclab/bin/activate
cd /home/cocel/Desktop/Research/tita_gluon_wbc/lab/ddt_lab
pip install -e .

python scripts/rsl_rl/train.py \
  --task DDT-Velocity-Flat-Tita-My-v0 \
  --num_envs 4096 \
  --seed 42 \
  --max_iterations 3000 \
  --headless
```

재개할 때는 run과 checkpoint를 명시한다.

```bash
# Execution Domain: TRAINING_SIM
python scripts/rsl_rl/train.py \
  --task DDT-Velocity-Flat-Tita-My-v0 \
  --num_envs 4096 \
  --seed 42 \
  --max_iterations 3000 \
  --resume \
  --load_run '<RUN_REGEX>' \
  --load_checkpoint 'model_<ITER>\.pt' \
  --headless
```

반드시 보존할 산출물:

- `logs/rsl_rl/tita_flat_rslrl_estimator/<run>/params/env.yaml`
- `params/agent.yaml`
- `model_<iter>.pt`와 SHA256
- W&B/TensorBoard scalar
- checkpoint sweep 결과
- export ONNX와 SHA256
- Isaac/MuJoCo 동일 protocol 결과

### 5.4 평가와 ONNX export

```bash
# Execution Domain: VALIDATION_SIM
python scripts/rsl_rl/eval_behavior.py \
  --task DDT-Velocity-Flat-Tita-My-Play-v0 \
  --checkpoint /absolute/path/to/model_<ITER>.pt \
  --num_envs 32 \
  --out /home/cocel/Desktop/Research/tita_gluon_wbc/test/eval_logs/<run>.csv \
  --headless

# Execution Domain: DESKTOP_DRY_RUN
python scripts/rsl_rl/play.py \
  --task DDT-Velocity-Flat-Tita-My-Play-v0 \
  --checkpoint /absolute/path/to/model_<ITER>.pt \
  --num_envs 1 \
  --export_policy \
  --headless
```

exporter는 policy class에 따라 adapter를 바꾼다.

- estimator PPO: estimator까지 graph에 bake한 `nn_input0 [1,33] -> nn_output [1,8]`
- 구형 history PPO: current + `[1,10,33]`; frame-major history를 학습 당시 term-major 330-D로 재조립
- no-history plain PPO: actor input 크기의 단일 입력
- diagnostic estimator export: action 외에 `est_vel [1,3]`를 두 번째 output으로 노출; deployment 기본 graph가 아니다.

export 후 파일명이나 README를 믿지 말고 graph와 hash를 검사한다.

```bash
# Execution Domain: DESKTOP_DRY_RUN
/home/cocel/venvs/cosim_ros2_jazzy/bin/python \
  sim2sim/cosim_ros2_jazzy/scripts/inspect_onnx.py /path/to/policy.onnx
sha256sum /path/to/policy.onnx
```

---

## 6. NP3O와 PPO: 무엇이 다르고 왜 이 프로젝트에서는 PPO가 더 나았나

### 6.1 NP3O 구현의 실제 구조

이 저장소의 NP3O는 단순 PPO가 아니다.

```text
current proprio 33 + history 10x33
  -> recent history window 5
  -> Barlow-Twins encoder/projector
  -> latent 16 + supervised velocity estimate 3
  -> concat(velocity 3, latent 16, current 33)
  -> actor

critic observation
  -> reward value head
  -> cost value head
  -> Lagrangian cost schedule
```

주요 설정:

- history length `10`, Barlow window `5`
- encoder `[128,64]`, latent `[32,16]`, projector `64`
- PPO clip/entropy/gamma/lambda 등 core hyperparameter는 estimator PPO와 유사
- cost value loss와 constraint violation loss 계수 `0.1`
- export: `nn_input0 [1,33]`, `nn_input1 [1,10,33]` -> `nn_output [1,8]`

그러나 TITA baseline 환경에는 실제 cost manager가 선언되지 않았다. `IsaacLabNP3OWrapper`는 1-D all-zero cost placeholder를 만들고 스스로 다음처럼 기록한다.

```text
NP3O ≡ PPO + BarlowTwins
```

즉 cost critic과 Lagrangian 코드 경로는 계산되지만 현재 baseline에서 안전 constraint signal을 제공하지 않는다.

### 6.2 공정한 비교

| 비교 축 | estimator PPO | 현재 NP3O | 이 프로젝트 영향 |
|---|---|---|---|
| actor sensor input | current 33 | current 33 + history 10×33 | PPO runtime이 단순 |
| latent 목적 | true base velocity 3-D 직접 회귀 | velocity 3 + self-supervised latent 16 | PPO가 배포 결손 센서에 더 직접 대응 |
| constraint | 없음 | framework는 있으나 TITA cost가 0 | NP3O 안전 이점이 현재는 없음 |
| 학습 runner | official RSL-RL path + 작은 version-pinned extension | custom wrapper/storage/runner | PPO 유지보수 표면이 작음 |
| ONNX | single input | two inputs | 현재 `tita_gluon_ws` C++ runner는 PPO와 일치 |
| 실험 깊이 | My26~45, Isaac/MuJoCo, 일부 실기 | 동일 조건 직접 A/B 없음 | PPO 증거가 훨씬 풍부 |
| 실기 C++ 지원 | `[1,33]` + optional diagnostic output | history input 미지원 | NP3O를 바로 실기에 넣을 수 없음 |

### 6.3 “PPO가 더 좋았다”의 정확한 의미

**`PASS`로 말할 수 있는 것:** 이 저장소의 현재 Sim2Real 경로에서는 estimator PPO가 더 좋은 운용 선택이다.

이유는 다음과 같다.

1. `My-v0`의 실제 등록과 이후 실험 계보가 estimator PPO로 수렴했다.
2. 실물에서 직접 얻기 어려운 base linear velocity만 3-D auxiliary target으로 좁혀 학습한다.
3. ONNX가 단일 33-D 입력이라 observation history lifecycle과 두 번째 tensor wiring이 없다.
4. 현재 `tita_gluon_ws` C++ `OnnxPolicyRunner`가 바로 받는 계약이 `[1,33] -> [1,8]`이다.
5. NP3O의 cost가 all-zero라 constraint-aware 구조가 실질 안전 이득을 주지 않는다.
6. My43/My45에는 checkpoint sweep, Isaac behavior, corrected-MJCF MuJoCo drift가 모두 있다.
7. official RSL-RL runner를 최대한 보존해 custom algorithm stack보다 upgrade/debug surface가 작다.

**`BLOCKED`인 주장:** “PPO 알고리즘이 NP3O보다 학습 성능·표본 효율·강건성이 본질적으로 우월하다.”

그 주장을 하려면 다음 실험이 필요하다.

- 동일 env/reward/randomization/action/observation
- 동일 actor parameter budget과 observation information budget
- 동일 seed 최소 5개
- 동일 environment steps와 wall-clock/GPU budget
- 동일 checkpoint selection rule
- zero-command drift, command tracking, disturbance recovery, cost violation, Sim2Sim gap의 confidence interval
- NP3O에는 실제 물리적 cost term을 넣은 조건과 zero-cost ablation을 모두 포함
- 1-input/2-input runtime 차이를 알고리즘 성능과 분리

따라서 면접에서는 “PPO가 더 강한 알고리즘이었다”가 아니라 다음처럼 말하는 것이 정확하다.

> 이 프로젝트에서는 비용 신호가 비어 있는 NP3O의 복잡한 history/constraint 경로보다, 실제로 결손된 base velocity를 직접 추정하고 단일 33-D 입력으로 내보내는 estimator PPO가 배포 계약과 검증 증거 면에서 더 적합했습니다. 보편적 알고리즘 우월성은 동일 조건 A/B가 없어 주장하지 않습니다.

---

## 7. 별도 연구 계열: CO-RL MOO-PPO와 RMA

DDT estimator PPO와 CO-RL MOO-PPO는 이름만 다른 같은 정책이 아니다. observation, action order, scale, actuator gain, exporter, runner가 모두 다르다. YAML의 `policy.interface`에 따라 `MooStandDriveObservationBuilder`와 `MooStandDriveActionAdapter`를 선택하는 이유가 이것이다.

### 7.1 등록 task

현재 `lab/ddt_lab/ddt_lab/tasks/moo_based/locomotion/velocity/tita_env/__init__.py`에는 다음 TITA-only task가 있다.

| Gym ID | actor 정보 | 목적 |
|---|---|---|
| `Isaac-Velocity-Flat-Tita-v3-moo-ppo` | 기본 proprio | MOO stand/drive |
| `...-GTBaseVel-v3-moo-ppo` | true base velocity 추가 | oracle upper-bound |
| `...-GTBaseVel-TargetHeight-v3-moo-ppo` | true velocity + true height | target-height oracle |
| `...-Estimator-TargetHeight-v3-moo-ppo` | learned velocity estimator | deployable 방향 |
| `...-RMATeacher-TargetHeight-v3-moo-ppo` | privileged encoder latent | teacher 학습 |
| `...-Play-v3-moo-ppo` | play config | evaluation/export |

### 7.2 MOO observation 계약

기본 stack-policy 28-D는 joint position/velocity, body angular velocity, projected gravity, previous action으로 구성되고, non-stack command 4-D는 `[2*vx, vy, 0.25*wz, normalized_height]`다.

```text
plain, num_policy_stacks=0:
28 current stack + 4 command = 32

GT velocity+height teacher, num_policy_stacks=1:
(28 + base_lin_vel 3 + base_height 1) * (current+previous 2 frames)
+ command 4
= 68
```

2026-08-20 audit로 확인된 deployable 32-D current observation의 정확한 slice는 다음이다.

| Slice | 값 |
|---|---|
| `0:4` | hip/shoulder position `[L1,R1,L2,R2]` |
| `4:6` | leg position `[L3,R3]` |
| `6:10` | hip/shoulder velocity ×0.05 |
| `10:12` | leg velocity ×0.05 |
| `12:14` | wheel velocity ×0.05 |
| `14:17` | body angular velocity ×0.25 |
| `17:20` | projected gravity |
| `20:28` | previous raw action in MOO policy order |
| `28:32` | `[2*vx, vy, 0.25*wz, normalized_height]` |

height normalization은 observation에만 적용한다. command manager와 height reward는 meter 단위를 유지한다. checkpoint마다 curriculum range가 달라 center/half-range를 다시 구해야 한다. 잘못된 height default는 과거 MuJoCo에서 30 s에 4 m 이상 drift를 재현했으므로 단순 config 미관 문제가 아니다.

### 7.3 MOO action 계약

```text
MOO policy output order:
[L1, R1, L2, R2, L3, R3, L4, R4]

MuJoCo native로 변환할 index:
[0, 2, 4, 6, 1, 3, 5, 7]
```

- L1~L3/R1~R3: default offset 없는 **absolute position target**, scale `1.0`
- L4/R4: velocity target, scale `40.0`
- 대표 heightnorm v3 gain: leg `Kp=70,Kd=0.7`, wheel `Kd=0.55`
- 대표 torque limit: leg `55 Nm`, wheel `36 Nm`

DDT adapter의 `default + 0.25*a`, wheel `5*a`를 MOO 정책에 쓰거나 반대로 하면 interface shape는 맞아도 물리 의미가 완전히 깨진다.

### 7.4 MOO-PPO 학습 구조

- runner: `24 steps/env`, 기본 `1500 iterations`
- actor/critic: `[512,256,128]`, ELU
- PPO: clip `0.2`, entropy `0.01`, epochs `5`, minibatches `4`, lr `1e-3`, gamma/lambda `0.99/0.95`
- discriminator: `[256,256]`, lr `1e-4`, coefficient `0.5`, gradient penalty `0.1`
- MOO error vector: xy velocity, height, yaw, roll/pitch, hip/shoulder/leg deviation, action smoothness, torque rate, integrated xy/yaw pose, angular x/y와 vertical velocity
- CO-RL `StateHandler`는 `num_policy_stacks+1`개의 stack frame 뒤에 non-stack command를 붙인다.

`PASS`인 것은 runner/discriminator/environment 통합과 짧은 training signal이다. 전체 command distribution의 convergence나 Sim2Real ready는 아니다.

### 7.5 RMA teacher/student 계약

RMA는 actor와 environment latent encoder를 분리한다.

| 계열 | encoder input | actor input | 상태 |
|---|---|---|---|
| 2026-08-08 teacher | privileged 25 -> latent 16 | obs 68 + latent 16 = 84 -> 8 | fixed-MuJoCo teacher |
| 2026-08-09 student | history `50×36` -> latent 16 | obs 68 + latent 16 = 84 -> 8 | 최초 direct handoff에서 전복, `SUSPICIOUS` |
| 2026-08-19 deployable-v5 teacher | privileged 26 -> latent 16 | obs 32 + latent 16 = 48 -> 8 | actor에서 oracle 제거, handoff 문제 남음 |
| 2026-08-20 oracle-free stack0 | privileged 26 -> latent 16 | obs 32 + latent 16 = 48 -> 8 | viewer `PASS`, robustness `NOT_TESTED` |
| 2026-08-23 multihead student | history `50×32` -> packed 24 | packed actor input 92 -> 8 | runtime `PASS`, posture `SUSPICIOUS` |

25-D privileged vector:

```text
wheel contact 2
+ base mass*0.1 1
+ base CoM*10 3
+ Kp*0.01 8
+ Kd 8
+ body-frame base_lin_vel*[2,1,0.25] 3
= 25
```

deployable-v5의 26-D teacher privileged vector는 마지막에 base height 1을 추가한다. 이것은 teacher 학습용 oracle이고 실제 student runtime은 history adaptation으로 대체해야 한다.

현재 hardware C++ runner는 32/68/84/92-D MOO/RMA 계약이나 두 graph 실행을 지원하지 않는다. 따라서 이 계열의 MuJoCo 실행 `PASS`를 TITA 실기 배포 가능으로 해석하면 안 된다.

### 7.6 CO-RL 학습/export 예시

```bash
# Execution Domain: TRAINING_SIM
cd /home/cocel/Desktop/Research/tita_gluon_wbc
PYTHONPATH="$PWD/lab:$PWD/lab/ddt_lab" \
  /home/cocel/isaac/env_isaaclab/bin/python lab/scripts/co_rl/train.py \
  --task Isaac-Velocity-Flat-Tita-GTBaseVel-TargetHeight-v3-moo-ppo \
  --algo mooppo \
  --num_envs 4096 \
  --max_iterations 1500 \
  --headless
```

RMA checkpoint export에서는 **training run의 task ID와 `policy.class_name`을 먼저 확인**해야 한다. 잘못된 task ID는 다른 network class를 만들고 state dict shape mismatch를 낸다.

```bash
# Execution Domain: VALIDATION_SIM
PYTHONPATH="$PWD/lab:$PWD/lab/ddt_lab" \
  /home/cocel/isaac/env_isaaclab/bin/python lab/scripts/co_rl/play.py \
  --task Isaac-Velocity-Flat-Tita-RMATeacher-TargetHeight-v3-moo-ppo \
  --algo mooppo \
  --num_policy_stacks 1 \
  --checkpoint /absolute/path/to/model_9999.pt \
  --num_envs 1 \
  --headless
```

RMA teacher/student는 actor와 encoder를 각각 export하고 두 graph 모두 PyTorch↔ONNX parity와 SHA256을 기록해야 한다.

---

## 8. 정책 artifact registry와 호환성

### 8.1 직접 재검사한 대표 artifact

| 파일 | SHA256 | 실제 graph 계약 | 비고 |
|---|---|---|---|
| `tita_gluon_ws/deploy/tita/policy.onnx` | `025ad9b5a2022a9b2854623a3ff7149a73b3118585eb3744a1c5ab5e3e90090c` | `nn_input0 [1,33] -> nn_output [1,8]` | provenance 이름이 불명확; `sim2sim/cosim_ros2_jazzy/config/tita.yaml`과 불일치 |
| `policy_my7rsl.onnx` | `420e904a28ab66611d85bef9f34083a546ef70ab954d76fc8c2c87f41270c672` | `[1,33] + [1,10,33] -> [1,8]` | history PPO |
| `policy_my33_2999_estimator_diagnostic.onnx` | `339b120f8021d5bca196787d8952bf764c927ad77a3fa2796cbf49811b9c9132` | `[1,33] -> action [1,8] + estimator [1,3]` | 현재 workspace C++ YAML이 고정한 파일 |
| `policy_my43_2700.onnx` | `ecb0fd3ec56eb9aed5349250e9de11040156f59e3a98c54ae83dadde672a7705` | `[1,33] -> [1,8]` | DDT drift 최선 기록 |
| `policy_my45_2500.onnx` | `3be0b6b4e2dbeffc81f7b4f4a3ef82a0700b9124be2014aee0853e940520123f` | `[1,33] -> [1,8]` | integral wheel penalty |
| `policy_moo_stand_drive_20260807_4999_heightnorm_v3.onnx` | `6547d20a171334817ad3c26caa452c66dc50ff17fb2f36142d7d61004f9fb1c2` | `obs [1,68] -> actions [1,8]` | MOO oracle/stack, hardware 비호환 |

### 8.2 runner 호환성

| Runtime | 지원 계약 | 호환 정책 | 비호환 정책 |
|---|---|---|---|
| MuJoCo `PolicyRunner` | config로 1-input 또는 2-input strict validation | DDT estimator PPO, 구형 history PPO/NP3O | config shape가 다른 모든 artifact |
| MuJoCo RMA runner | actor+teacher/student encoder 두 graph | 해당 checkpoint별 MOO RMA | 단일 DDT runner로 실행 불가 |
| `tita_gluon_ws` 현재 C++ | `[1,33] -> [1,8]`, optional `[1,3]` diagnostic | My26 이후 estimator PPO | NP3O/history, MOO/RMA |
| SDK snapshot C++ | `[1,33] + [1,10,33] -> [1,8]` | historical `d53a5b0b69e5382dc5f40909ecaa7481221397aa3b3400c922b13a33576273e6` policy | 현재 single-input `policy.onnx`, My43/My45 |

정책 파일을 `policy.onnx`로 덮어쓰는 것만으로 배포 계약이 바뀌지 않는다. runner, YAML, fixture, hash gate와 test를 한 번에 갱신해야 한다.

---

## 9. MuJoCo Sim2Sim: 올바른 실행과 검증

### 9.1 build

실제 colcon workspace root는 `sim2sim/`이고 package는 `cosim_ros2_jazzy`다.

```bash
# Execution Domain: VALIDATION_SIM
source /home/cocel/venvs/cosim_ros2_jazzy/bin/activate
source /opt/ros/jazzy/setup.bash
cd /home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim

colcon build --symlink-install \
  --paths cosim_ros2_jazzy \
  --packages-select cosim_ros2_jazzy
source install/setup.bash
```

새 YAML/launch/resource를 추가하면 rebuild가 필요하다. symlink된 기존 Python만 바꾼 경우에는 즉시 반영될 수 있지만, 최종 검증에서는 build를 생략하지 않는 편이 추적성이 높다.

### 9.2 config 선택

현재 기본 `tita.yaml`을 쓰지 않는다. 명시적으로 artifact와 맞는 config를 선택한다.

- DDT zero-drift 기준점: `tita_my43_2700.yaml`
- DDT integral-penalty 비교: `tita_my45_2500.yaml`
- MOO/RMA: checkpoint 이름과 완전히 일치하는 전용 YAML

```bash
# Execution Domain: DESKTOP_DRY_RUN
cd /home/cocel/Desktop/Research/tita_gluon_wbc
/home/cocel/venvs/cosim_ros2_jazzy/bin/python \
  sim2sim/cosim_ros2_jazzy/scripts/inspect_onnx.py \
  tita_gluon_ws/deploy/tita/policy_my43_2700.onnx
sha256sum tita_gluon_ws/deploy/tita/policy_my43_2700.onnx
```

### 9.3 headless gate를 먼저 통과

```bash
# Execution Domain: VALIDATION_SIM
cd /home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim
source /home/cocel/venvs/cosim_ros2_jazzy/bin/activate
source /opt/ros/jazzy/setup.bash
source install/setup.bash

CFG="$PWD/cosim_ros2_jazzy/config/tita_my43_2700.yaml"
timeout 20s ros2 launch cosim_ros2_jazzy tita_mujoco_sim2sim.launch.py \
  config:="$CFG" viewer:=false keyboard:=false joystick:=false
```

확인할 startup evidence:

- corrected MJCF path
- 예상 policy path와 SHA256
- 실제 interface summary
- policy 50 Hz, effective policy dt 20 ms
- ONNX missing input/output, non-finite state, traceback 없음
- timeout 전까지 process가 자발적으로 crash하지 않음

20 s 생존만으로 behavior를 `PASS`로 두지 않는다.

### 9.4 viewer와 FSM

```bash
# Execution Domain: VALIDATION_SIM
ros2 launch cosim_ros2_jazzy tita_mujoco_sim2sim.launch.py \
  config:="$CFG" viewer:=true keyboard:=true joystick:=false
```

시뮬레이터에서만 다음 순서로 확인한다.

```text
idle
-> reference_transform_up
-> reference_stand_hold / handoff bridge complete
-> rl_0 (alias: balance)
-> zero command
-> 작은 vx
-> 작은 wz
-> idle
```

```bash
# Execution Domain: VALIDATION_SIM
ros2 topic pub --once /tita/command/manager/cmd_key \
  std_msgs/msg/String "{data: transform_up}"
ros2 topic pub --once /tita/command/manager/cmd_key \
  std_msgs/msg/String "{data: balance}"
ros2 topic pub -r 10 /tita/command/manager/cmd_twist \
  geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

My43 YAML의 command clamp는 training보다 좁은 `|vx|<=0.2`, `vy=0`, `|wz|<=0.3`이다. simulator에서 큰 명령이 들어가도 그대로 policy에 전달되지 않는다.

### 9.5 반드시 보는 debug/metric

주요 topic:

```text
/cosim_ros2_jazzy/debug/state
/cosim_ros2_jazzy/debug/obs
/cosim_ros2_jazzy/debug/obs_history
/cosim_ros2_jazzy/debug/action_raw
/cosim_ros2_jazzy/debug/action_scaled
/cosim_ros2_jazzy/debug/joint_target
/cosim_ros2_jazzy/debug/torque_cmd
/cosim_ros2_jazzy/debug/torque_clip_by_joint
/cosim_ros2_jazzy/debug/base_rpy
/cosim_ros2_jazzy/debug/base_ang_vel
/cosim_ros2_jazzy/debug/projected_gravity
```

평가 protocol은 최소 다음을 포함한다.

1. 3~5 s settle 후 zero-command 10/30/60 s
2. planar endpoint drift와 path length를 함께 측정
3. roll/pitch RMS와 peak, angular velocity RMS/peak
4. base height mean/minimum
5. left/right wheel velocity, wheel angle drift, raw wheel action
6. action rate/second difference, target tracking error, torque RMS/clipping ratio
7. 작은 전진/후진/yaw step과 stop transient
8. seed, 초기 pitch, mass/friction, delay sweep
9. termination reason/time-to-failure
10. pitch-wheel-action PSD로 limit-cycle 주파수 비교

### 9.6 `reference_transform_up`의 구조적 문제

MOO/RMA config 계열의 `reference_transform_up`/`reference_stand_hold`는 open-loop high-gain reference PD hold이고 active wheel balance가 없다. YAML의 `use_imu_wheel_balance`는 해당 state에서 읽히지 않는 dead key다. pose와 timer를 여러 번 바꿔도 tilt가 사라지지 않은 이유다.

현재 ad-hoc stand pose:

```text
[-0.05, 0.9, -2.6, 0.0, 0.05, 0.9, -2.6, 0.0]
```

이 pose에서 RMA policy entry joint error `1.207 rad`가 반복 관측됐다. 해결책은 timer 재조정이 아니라 다음 중 하나다.

- transition state 자체에 pitch feedback 기반 wheel balance를 넣고 검증
- checkpoint reset distribution과 CoM에 맞는 실제 안정 stand pose를 데이터로 도출
- policy가 학습한 handoff distribution에 transition을 포함해 재학습

현재는 어느 것도 production-ready로 완료되지 않았다: `BLOCKED`.

---

## 10. 실제 TITA 연결과 Read-Only Real2Sim

### 10.1 확인된 로봇 환경

2026-07-29 read-only 기록에서 확인된 값:

- historical SSH: `robot@192.168.0.28`
- hostname/user: `tita` / `robot`
- Ubuntu 22.04, `aarch64`, ROS 2 Humble
- robot setup: `/opt/tita/ros2/setup.bash`
- `ROS_DOMAIN_ID=42`
- namespace: `/tita4252763`

IP는 네트워크/session 의존 값이다. relay launch default `192.168.42.1`과 기록된 `192.168.0.28`도 다르다. 먼저 현재 route와 SSH를 확인하고 모든 launch에 `server_host`를 명시한다.

### 10.2 첫 연결: publish/service 없이 확인

```bash
# Execution Domain: ROBOT_READ_ONLY
ip route
ssh -o BatchMode=yes -o ConnectTimeout=5 robot@<CURRENT_ROBOT_IP> \
  'hostname; whoami; uname -m'
```

로봇에서 graph를 볼 때 비대화형 SSH는 환경이 비어 있을 수 있다.

```bash
# Execution Domain: ROBOT_READ_ONLY
source /opt/tita/ros2/setup.bash
export ROS_DOMAIN_ID=42
ros2 node list --no-daemon --spin-time 10
ros2 topic list -t --no-daemon --spin-time 10
ros2 topic info -v /tita4252763/joint_states
ros2 topic info -v /tita4252763/imu_sensor_broadcaster/imu
ros2 topic info -v /tita4252763/chassis/odometry
```

이 단계에서는 command topic publish, service/action call, daemon restart, vendor process 변경을 하지 않는다.

### 10.3 경로 A: direct DDS

desktop과 robot이 같은 DDS domain에서 discovery되고 message type이 호환되면 relay는 필수가 아니다. Humble↔Jazzy라는 이유만으로 TCP relay가 반드시 필요하다는 증거는 없다.

```bash
# Execution Domain: ROBOT_READ_ONLY
source /opt/ros/jazzy/setup.bash
source /home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim/install/setup.bash
export ROS_DOMAIN_ID=42
ros2 topic list --no-daemon --spin-time 10 | rg '^/tita4252763/'
```

discovery가 확인됐을 때만 mirror를 실행한다.

```bash
# Execution Domain: ROBOT_READ_ONLY
CFG=/home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim/cosim_ros2_jazzy/config/tita_my43_2700.yaml
ros2 launch cosim_ros2_jazzy tita_mujoco_real2sim.launch.py \
  config:="$CFG" \
  real_tita_ns:=tita4252763 \
  use_state_relay:=false \
  viewer:=true \
  mirror_base_orientation:=true \
  mirror_base_position:=false
```

이 node는 real `q,dq,IMU,odom`을 MuJoCo state로 mirror할 뿐 real command publisher를 만들지 않는다. odometry z까지 그대로 mirror하는 것은 frame/height 정의가 검증되기 전에는 끈다.

### 10.4 경로 B: TCP state relay

DDS discovery가 불안정할 때 robot sender는 subscribe-only state를 JSON line protocol로 내보낸다.

기본 sender:

- bind `0.0.0.0:50051`, `50 Hz`
- joint states, IMU, odometry
- motor status와 FSM 포함 시도
- observed command는 기본 `include_command=false`
- raw joy는 axis/sign/scale를 명시적으로 확인하지 않으면 거부

로봇에 package가 실제 설치돼 있고 prefix가 확인된 경우에만 sender를 실행한다.

```bash
# Execution Domain: ROBOT_READ_ONLY
source /opt/tita/ros2/setup.bash
export ROS_DOMAIN_ID=42
ros2 pkg prefix cosim_ros2_jazzy
ros2 launch cosim_ros2_jazzy tita_state_relay_sender.launch.py \
  tita_ns:=tita4252763 \
  bind_host:=0.0.0.0 \
  port:=50051 \
  include_command:=false
```

desktop:

```bash
# Execution Domain: ROBOT_READ_ONLY
source /home/cocel/venvs/cosim_ros2_jazzy/bin/activate
source /opt/ros/jazzy/setup.bash
source /home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim/install/setup.bash

CFG=/home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim/cosim_ros2_jazzy/config/tita_my43_2700.yaml
ros2 launch cosim_ros2_jazzy tita_mujoco_relay_real2sim.launch.py \
  config:="$CFG" \
  server_host:=<CURRENT_ROBOT_IP> \
  port:=50051 \
  real_tita_ns:=tita4252763 \
  relay_ns:=tita_relay \
  viewer:=true \
  mirror_base_position:=false
```

receiver는 finite JSON/schema/1 MiB size를 검사하고 다음 local diagnostics를 낸다.

- packet rate
- network latency
- estimated drop
- reconnect count
- connection status

이 TCP protocol에는 인증과 암호화가 없다. trusted isolated LAN, 방화벽 제한 또는 운영자가 검토한 SSH tunnel이 필요하다. 공용망에 `0.0.0.0:50051`을 노출하면 안 된다.

### 10.5 경로 C: offline rosbag

가장 재현 가능하고 위험이 낮은 경로다. recorder는 joint/IMU/odom만 선택하고 command topic은 제외한다.

```bash
# Execution Domain: ROBOT_READ_ONLY
python3 -m cosim_ros2_jazzy.tita_readonly_bag_record \
  --namespace tita4252763 \
  --output-dir /home/robot/bags/tita_readonly \
  --label tita_state \
  --duration 30
```

복사한 bag을 desktop에서 재생한다.

```bash
# Execution Domain: DESKTOP_DRY_RUN
CFG=/home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim/cosim_ros2_jazzy/config/tita_my43_2700.yaml
ros2 launch cosim_ros2_jazzy tita_mujoco_offline_real2sim.launch.py \
  config:="$CFG" \
  bag_path:=/absolute/path/to/bag \
  viewer:=true \
  loop:=false
```

### 10.6 ghost policy

ghost는 real sensor snapshot/observed command를 local MuJoCo policy에 넣어 “실제 상태에서 정책이 무엇을 냈을지” 계산한다. real command publisher가 없고 local debug topic만 낸다.

사용 전 조건:

- relay에 command를 포함하려면 `processed_twist`를 subscribe-only로 명시
- real FSM allowed mode와 sensor/command freshness 확인
- policy/config interface/hash 일치
- ghost rollout은 짧은 horizon마다 real snapshot으로 reset

`sim2sim/cosim_ros2_jazzy/test/test_real_policy_ghost.py`는 sender/ghost/launch에 real command publisher token이 없는지 정적 검사한다. 그래도 launch 전 `ros2 node info`로 publisher endpoint를 재감사한다.

### 10.7 2026-07-29 센서 준비도

| 센서 | 관측 | 판정 |
|---|---|---|
| joint state | 8축 finite, 약 `443.35 Hz` | `PASS` |
| body IMU | quaternion/gyro/accel finite, 약 `440.73 Hz` | `PASS` |
| chassis odom | 약 `53.46 Hz` | `PASS`, covariance 0 주의 |
| face/neck SPAD | 약 `14.15/13.87 Hz`, finite points | `PASS` |
| stereo raw | 좌/우 약 `17.0/14.1 Hz`, median skew `51.04 ms` | `FAIL` for synchronization |
| right camera TF | image `right_camera`, TF `right_camara` | `FAIL` |
| ultrasonic | publisher 없음 | `FAIL`/driver inactive |
| Tower cloud/odom | endpoint 흔적, 실제 메시지 없음 | `SUSPICIOUS`/unknown |

locomotion proprio pipeline에는 joint/IMU가 핵심이지만, 이 결과만으로 low-level command path freshness, latency distribution, calibration, safety를 `PASS`로 볼 수 없다.

---

## 11. Staged Sim2Real와 fail-closed hardware stack

### 11.1 가장 중요한 invariant

```text
vendor motor writer XOR direct motor writer
```

이 stack은 vendor balance에 RL node를 하나 더 붙이는 구조가 아니다. takeover 전에는 vendor가 유일한 writer이고, takeover 후에는 Direct-mode HardwareBridge + controller_manager + Stage1Controller만 writer여야 한다. 둘이 동시에 존재하면 즉시 `BLOCKED`다.

### 11.2 pinned reference와 한계

- upstream `DDTRobot/ddt_ros2_control`: `e7b32d9746df900680641ff2845ffb0b5ffe99ed`
- official `start.bash` SHA256: `0a2bca4a146f9127ad558b50ca745826cc93ee920f3bb9538521555ea94f97b3`
- ONNX Runtime reference: `1.19.2`
- raw CAN Direct sequence를 다른 script/code/runbook에 복제하는 것은 금지
- SAFE_HOLD는 emergency stop이 아님
- crash, SBC loss, CAN loss, ROS shutdown은 certified E-stop이 아님
- graceful in-session Direct→MCU rollback은 확인되지 않음
- 확인된 복구는 물리 지지 후 full TITA power OFF/ON, vendor MCU idle 재확인

### 11.3 기본 launch는 inert해야 한다

```text
execute_vendor_stop = false
execute_start_bash = false
enable_hardware_output = false
operator_arm = false
auto_enter_rl = false
respawn = false
```

launch argument를 permissive하게 주는 것과 operator arm은 별도 gate다. 이전 session의 승인은 새 full-power session에 재사용할 수 없다.

### 11.4 승인 전 command-free preflight

SDK reference tree를 정확히 bootstrap/build한 뒤, vendor service가 active이고 MCU exact idle인 상태에서만 수행한다.

```bash
# Execution Domain: ROBOT_COMMAND_FREE_RUNTIME
cd /path/to/tita_low_level_sdk_ros2_humble
source /opt/ros/humble/setup.bash
source direct_ws/install/setup.bash
source lowlevel_ws/install/setup.bash
./scripts/command_free_preflight.bash
```

필수 결과:

```text
ready: true
blockers: []
command_output: DISABLED
```

이 결과도 takeover 승인이 아니다.

### 11.5 실제 상태 전환의 운영 gate

다음은 설명용 sequence이며, 실행에는 해당 power session의 별도 운영자 승인·물리 지지·승인된 power cut 준비가 필요하다.

```text
1. TITA full power ON
2. vendor stack이 exact FSM idle을 만들었는지 확인
3. 8 motors Online, policy/config/controller/logger hash 확인
4. command-free preflight PASS
5. 운영자가 해당 session takeover를 명시 승인
6. tita-bringup.service만 중지
7. vendor process/controller/CAN writer가 모두 사라졌음을 증명
8. pinned official start.bash를 정확히 1회 실행
9. one HardwareBridge + one controller_manager + one Stage1Controller
10. measured initial pose -> TransformUp
11. 5초 연속 standing settle
12. bounded zero-command RL
13. bounded low command
14. watchdog/operator request -> SAFE_HOLD
15. 물리 지지 -> full power cycle -> vendor MCU idle 재확인
```

`pkill`, `killall`, 자동 vendor restart, 자동 power cycle은 이 절차에 포함되지 않는다.

### 11.6 현재 두 controller tree의 차이

이 차이를 해결하지 않고 실기에 들어가면 안 된다.

| 항목 | SDK reference snapshot | `tita_gluon_ws` 현재 workspace |
|---|---|---|
| policy | historical `d53a5b0b69e5382dc5f40909ecaa7481221397aa3b3400c922b13a33576273e6` | My33 diagnostic `339b120f8021d5bca196787d8952bf764c927ad77a3fa2796cbf49811b9c9132` |
| ONNX | 2-input, history 10 | 1-input, optional estimator output |
| FSM | handoff/prepare/blend 포함 | settle 후 바로 `RL_RUNNING` |
| real 기록 | Stage 1/2 `PASS`, Stage 3 `SUSPICIOUS` | 현재 exact config의 별도 real validation 기록을 찾지 못함 |
| angular watchdog | Stage 3 기록 `2.5 rad/s` | current YAML `1.5 rad/s` |
| command gain | Stage 3 기록 `0.3` | current YAML `0.75` |
| RL duration | historical bounded 1 s/Stage3 session | current YAML `0.0` = automatic timeout 없음 |
| repeated clipping | historical `5`, diagnostic allowance | current `0`, clipped diagnostic false |

현재 workspace 값은 더 보수적인 부분도 있지만(`1.5 rad/s`, clipping 0), gain `0.75`와 무제한 duration은 historical Stage 3보다 범위가 넓다. 이 정확한 조합의 실기 증거가 없으므로 `NOT_TESTED`; 과거 Stage 3 `PASS`를 이 config로 이식하면 안 된다.

### 11.7 현재 workspace C++ FSM과 watchdog

실제 `tita_gluon_ws` enum:

```text
WAIT_FOR_HARDWARE
-> MEASURE_INITIAL_POSE
-> TRANSFORM_UP
-> STANDING_SETTLE
-> RL_RUNNING
-> SAFE_HOLD / FAULT
```

핵심 gate:

- hardware state가 finite/fresh하고 `0.10 s` 연속 안정
- stand error `<=0.15 rad`
- wheel speed `<=0.3 rad/s`
- roll/pitch `<=0.35 rad`
- acceleration norm `5~15 m/s^2`
- dropped logger records 없음
- 5 s 연속 standing settle
- joystick freshness/zero gate가 설정대로 만족
- observation/inference/target finite
- inference deadline `<=10 ms`
- operational joint envelope와 target delta/slew
- control period `<=10 ms`
- unexpected clipping 제한
- write failure 3회 미만
- fall tilt `0.65 rad` 미만

SAFE_HOLD는 새 policy output을 거부하고 wheel velocity를 0으로 ramp하며 stand pose를 hold한다. writer/logger는 유지되고 power cycle required가 표시된다. initial pose capture 전 hard fault는 `FAULT`, capture 후 critical fault는 `SAFE_HOLD`로 간다.

### 11.8 deploy script의 실제 의미

`tita_gluon_ws/deploy/deploy_tita_policy.bash`는 단순 validator가 아니다.

- ONNX가 single `[1,33] -> [1,8]`인지 검사
- zero-input inference finite 검사
- SHA256 계산
- vendor service active/direct process 없음 확인
- remote policy backup
- local controller config/preflight/test fixture의 hash 갱신
- policy/controller/SDK source를 robot으로 rsync
- remote move/build/test/preflight 수행
- 최종 output은 disabled로 유지

그러나 local 파일과 원격 SBC를 모두 변경하므로 실행 도메인은 `ROBOT_STATE_CHANGING`이다. 명시적 배포 승인 없이 실행하면 안 되며, 실행해도 모터 takeover 승인이 생기지 않는다.

### 11.9 실기 Stage 결과

| Stage | 결과 | 해석 |
|---|---|---|
| Stage 1 | `PASS` | vendor takeover, pinned Direct request, one writer, measured TransformUp, 5 s settle, SAFE_HOLD, full-power recovery |
| Stage 2 | `PASS` | native mapping, bounded blend, 1 s zero-command RL, write failure 없음, timed SAFE_HOLD, logger flush |
| Stage 3 | `SUSPICIOUS` | gain 0.3, 29.162 s; combined `vx=-0.3,wz=-0.3`에서 angular velocity `>2.5 rad/s`, SAFE_HOLD; 14,582 writer records 성공, 약 6 Hz 진동 지속 |

Stage 3에서 writer API가 모두 성공했다는 사실은 control stability가 좋았다는 뜻이 아니다. 오히려 transport failure가 아니라 policy/plant closed-loop limit cycle 가능성을 좁혀 준 증거다.

### 11.10 다음 실기 전 go/no-go

다음이 모두 충족되기 전에는 `BLOCKED`다.

- 사용할 controller tree 하나를 정하고 SDK/workspace drift 제거
- 사용할 checkpoint와 ONNX hash를 한 개로 고정
- 해당 graph contract에 맞춘 C++ unit/integration test
- 같은 policy/config로 corrected MuJoCo zero/step/delay/lag sweep
- 6 Hz mode를 simulation 또는 hardware log에서 재현하고 root cause 분리
- current gain/timeout/watchdog 조합의 승인된 bounded protocol
- physical support와 approved power cut 준비
- fresh-session ownership/preflight evidence
- 실험 로그를 `docs/exp/YYYY-MM-DD/`에 기록할 계획

---

## 12. 실험 전체 연대기와 증거 판정

이 절의 `PASS`는 각 행에 적힌 범위만 뜻한다. 예를 들어 한 iteration smoke test의 `PASS`는 학습 파이프라인이 실행됐다는 뜻이지, 보행 정책이 수렴했다는 뜻이 아니다. 반대로 reward가 높아도 zero-command drift나 실기 안정성이 나쁘면 정책 품질은 별도로 판정한다.

### 12.1 문서화된 실험 목록

| 날짜 | 실험 문서 | 실행 도메인 | 핵심 판정 |
|---|---|---|---|
| 2026-07-24 | `docs/exp/2026-07-24/moo_rsl_rl_port_summary.md` | `TRAINING_SIM` | 구 RSL-RL 이식 smoke test `PASS`; reference parity는 이후 재검토 필요 |
| 2026-07-24 | `docs/exp/2026-07-24/ddt_velocity_flat_tita_my_v0_training.md` | `TRAINING_SIM`, `VALIDATION_SIM` | My41~44 비교 `PASS`; reward와 정지 안정성이 불일치 |
| 2026-07-25 | `docs/exp/2026-07-25/moo_reference_parity_4096x100.md` | `TRAINING_SIM` | 9,830,400 step 실행 `PASS`; 수렴 품질은 `SUSPICIOUS` |
| 2026-07-25 | `docs/exp/2026-07-25/moo_reward_terms_configuration.md` | `TRAINING_SIM` | reward vector 연결 및 1-iteration smoke `PASS` |
| 2026-07-28 | `docs/exp/2026-07-28/fold_reset_event_validation.md` | `VALIDATION_SIM` | reset distribution `PASS`; discriminator 부재로 다음 step `BLOCKED` |
| 2026-07-28 | `docs/exp/2026-07-28/ddt_velocity_flat_tita_my_v0_zero_cmd_wheel_integral.md` | `TRAINING_SIM`, `VALIDATION_SIM` | My45 학습/Isaac/MuJoCo 비교 `PASS`; 좌우 비대칭 `SUSPICIOUS` |
| 2026-07-29 | `docs/exp/2026-07-29/tita_static_elevation_capture.md` | `ROBOT_READ_ONLY` | 대용량 정적 rosbag capture `PASS`; stereo/일부 센서 `SUSPICIOUS` |
| 2026-08-07 | `docs/exp/2026-08-07/co_rl_moo_port_reset.md` | `DESKTOP_DRY_RUN` | parity 불확실 구 port 제거/초기화 기록 `PASS` |
| 2026-08-07 | `docs/exp/2026-08-07/co_rl_tita_source_import_smoke.md` | `TRAINING_SIM` | source import, rollout, 1 iteration `PASS`; 정책 품질 `NOT_TESTED` |
| 2026-08-09 | `docs/exp/2026-08-09/rma_student_20260809_999_sim2sim.md` | `VALIDATION_SIM` | interface/runtime `PASS`; 15.86 s 전에 rollover되어 품질 `FAIL` |
| 2026-08-19 | `docs/exp/2026-08-19/rma_teacher_student_zero_command_drift.md` | `VALIDATION_SIM` | 동일 actor 비교 `PASS`; 단일 deterministic rollout이라 일반화 `SUSPICIOUS` |
| 2026-08-20 | `docs/exp/2026-08-20/rma_teacher_deployable_obs_v5_model9999_sim2sim.md` | `VALIDATION_SIM` | PT/ONNX parity 및 10 s rollout `PASS`; handoff 오차 `SUSPICIOUS` |
| 2026-08-20 | `docs/exp/2026-08-20/rma_teacher_oracle_free_model9999_observation_order_audit.md` | `DESKTOP_DRY_RUN` | observation/action order audit `PASS` |
| 2026-08-20 | `docs/exp/2026-08-20/rma_teacher_oracle_free_stack0_corrected_model9999_sim2sim.md` | `VALIDATION_SIM` | oracle-free graph/viewer 연결 `PASS`; robustness `NOT_TESTED` |
| 2026-08-23 | `docs/exp/2026-08-23/rma_student_multihead_808_model1500_mujoco_viewer.md` | `VALIDATION_SIM` | multi-head runtime `PASS`; low base/handoff 상태 `SUSPICIOUS` |
| Stage 1~3 | `sdk/tita_low_level_sdk_ros2_humble/docs/TEST_STATUS.md` | `ROBOT_STATE_CHANGING` | Stage 1/2 `PASS`, Stage 3 진동/SAFE_HOLD `SUSPICIOUS`; root `docs/exp/` 밖의 historical record |

`docs/exp/` 밖의 2026-07-08~09 JSON/CSV/NPZ는 현재 로깅 규칙을 만족하지 않는다. 아래에서는 값 자체는 참고하되 provenance가 약한 legacy evidence로 분리한다. Gluon-only 또는 TITA-Gluon 결합 실험은 이 문서의 범위에서 제외했다.

### 12.2 estimator-PPO 계열: My16~My45

#### 초기 관찰 설계 변화

| Run | 핵심 변화 | 관찰된 의미 | 판정 |
|---|---|---|---|
| My16 | 36-D에 true base linear velocity 포함 | oracle upper-bound 역할, 실기 배포 불가 | `PASS` as oracle, deployability `FAIL` |
| My18 | wheel 기반 naive velocity estimate | 외부 estimator 없이 속도 힌트 도입 | 정량 원본 부족으로 `SUSPICIOUS` |
| My23 | ground-truth 비교 구성 | estimator 효과 비교 기준 | 정량 원본 부족으로 `SUSPICIOUS` |
| My26 | estimator를 33-D single-input policy에 내장 | current deployment contract의 출발점 | graph contract `PASS` |
| My27 | `ZeroCommandPositionDrift` 추가 | model 2500 부근 약 `0.012~0.013 m/10 s`, My26 약 `0.130 m/10 s`; 학습 중 비단조 | 기록 범위 `PASS` |
| My28 | command 범위 `vx ±1.5`, `wz ±2.5` | 최종 약 `0.105 m/10 s`, `1.4 m/s` 주행 안정 기록 | `SUSPICIOUS`: artifact provenance 제한 |
| My31 | tracking weight `2/2` | checkpoint별 약 `0.01~0.09 m/10 s`로 선택 민감 | `SUSPICIOUS` |
| My34~40 | 여러 reward/config 반복 | YAML 주석이 일부 stale/copy 상태 | 정확한 delta 복원 `BLOCKED` |

My27의 중요한 교훈은 “마지막 checkpoint가 항상 최선”이 아니라는 것이다. 동일 run 안에서도 zero-command drift가 비단조였기 때문에 checkpoint selection metric을 training reward 하나로 두면 안 된다.

#### My41~45 정량 비교

| Run | 선택 checkpoint / reward | Isaac zero-command | corrected MuJoCo | 해석 |
|---|---|---|---|---|
| My41 | iter 5800 / `49.16` | 3 s drift `0.160 m`, max tilt `0.093 rad`, final angular speed `0.162 rad/s` | 5 s drift `0.445 m`; height `0.375→0.309→0.366 m` | sim2sim gap 큼 |
| My42 | iter 1800 / `49.94` | drift `0.185 m`, tilt `0.062 rad`, angular `0.121 rad/s` | drift `0.349 m`, height dip 약 `0.014 m` | My41보다 MuJoCo 개선, Isaac drift는 악화 |
| My43 | iter 2700 / `50.18` | drift `0.044 m`, tilt `0.069 rad`, angular `0.255 rad/s` | drift `0.022 m/5 s` | 이 비교군의 MuJoCo 최선 |
| My44 | iter 2500 / `53.58` | drift `0.153 m`, final angular `0.233 rad/s` | drift `0.181 m/5 s` | reward 최고지만 정지 성능은 My43보다 나쁨 |
| My45 | iter 2500 / train 3000 | drift `-0.0088 m/3 s`, mean wheel action `0.0446` | drift `0.0634 m/5 s`, height dip `0.005 m`; left wheel delta `-4.50`, right `-1.16 rad` | 정지 성능 양호, 좌우 비대칭 조사 필요 |

My43은 raw wheel action의 quartic penalty와 exact-zero 항을 사용했고, My45는 wheel command의 시간 적분을 quartic으로 벌점화했다. My45b에서 external force를 다시 켜자 MuJoCo drift가 YAML 기록상 `0.2372 m/5 s`로 악화됐다. 현재 hybrid인 My45c는 중앙 실험 로그가 완결되지 않아 `SUSPICIOUS`다.

checkpoint/hash 기록:

| Run | checkpoint SHA256 | ONNX SHA256 |
|---|---|---|
| My41 | `84561096eb9c1619964b4b2710819bbb70c7ecbbb5cb891c9961fed6d5ed1dfc` | `13ab688dbadec802c0874227dd222a4ee2f48889297b147d2b656aa344ff358b` |
| My42 | `30b0c28a0d8af084f5455527fc5fb990ff9737e3408962b362dc90cc1e8721ba` | `41d4d5e8f3f7a934675dc3287aff74c027168d9670d8c813e2c798441ab0876c` |
| My43 | `3766e05c683d6f2565bbeb2c21f500f872b243ffe39fb48b40fd3ae7ff608ef8` | `ecb0fd3ec56eb9aed5349250e9de11040156f59e3a98c54ae83dadde672a7705` |
| My44 | `eda9cb740012ad433373038b7ad6fb3438b2669de0f7e047d2666826504f043d` | `794050ca80524802189138e0e73fd028e119a3d2a8c4329cad6610494a5bb5e3` |
| My45 | `a078b2e1835566c1d6333c447a8fee3d1318c57cdae61ba82d26e2770283b163` | `3be0b6b4e2dbeffc81f7b4f4a3ef82a0700b9124be2014aee0853e940520123f` |

### 12.3 MOO / CO-RL 실험

초기 RSL-RL port는 import/unit/headless one-step/one-iteration 등 14개 검사를 통과했다. 그러나 reference implementation parity를 확신할 수 없어 이후 제거하고 source-faithful CO-RL port를 다시 시작했다. 따라서 과거 smoke `PASS`는 유지하되 최종 알고리즘 정합성 증거로 사용하지 않는다.

4096 environments × 100 iterations reference run:

- checkpoint SHA256 `2380078591cfa4e4ab04d15179f1b7fa1aa22a90680b9097e2fc4f9fd566f1af`
- episode length `10.10 → 148.03`
- mean reward `21.25`
- return `20.1482`, discounted return `0.6656`, MOO objective `0.1448`
- 9,830,400 environment steps, 약 4분 1초
- base contact가 흔하고 curve만으로 수렴을 입증하지 못함

이는 대규모 training loop 통합 증거로는 `PASS`, locomotion quality로는 `SUSPICIOUS`다. 16-env reward 구성 smoke는 384 steps를 실행해 각 reward term 연결을 확인했다. fold reset은 joint reset range `0~0.85`, position noise `±0.03`, velocity `±0.1`을 확인했으나 discriminator 부재로 reset 다음 step 검증이 `BLOCKED`됐다.

source-faithful CO-RL smoke에서는 1 env × 4 steps가 finite였고 observation group은 stack `32`, non-stack command `4`, privileged `2/3/20`이었다. 1 iteration은 24 steps를 끝내고 checkpoint SHA256 `e520da824f699f29f7be67465a09a8e56c994561b1a7d7ae0c8937e5347901e5`, value loss `0.0452`, surrogate `-0.1039`, discriminator loss `15777.84`를 기록했다. 실행 경로는 `PASS`; 높은 discriminator loss와 극소 budget 때문에 학습 성능은 `NOT_TESTED`다.

### 12.4 RMA teacher/student 실험

| 날짜/run | 관찰 | 판정 |
|---|---|---|
| 08-09 student 999 | interface와 runtime 정상, 15.86 s 이전 rollover | integration `PASS`, policy `FAIL` |
| 08-19 teacher 9999 | 15 s drift `0.12739 m`, yaw `0.8868 rad`, tilt `1.858°` | 단일 rollout `SUSPICIOUS` |
| 08-19 student 999 | 동일 actor, latent만 다름; drift `0.01875 m`, yaw `-0.0307 rad`, tilt `3.563°` | drift 85.3% 감소/6.79× 개선, 일반화 `SUSPICIOUS` |
| 08-20 deployable v5 | PT/ONNX max error `<1e-6`; 10 s drift `0.03617 m`, yaw `1.42°`, tilt `1.95°`, no fall | parity `PASS`, behavior `SUSPICIOUS` |
| 08-20 oracle-free stack0 | graph/viewer 실행, handoff 완료 | integration `PASS`, robustness `NOT_TESTED` |
| 08-23 multi-head 808/1500 | history `50×32→24`, actor `92→8`, runtime finite | runtime `PASS`; base z `0.203 m`/handoff `SUSPICIOUS` |

08-19 비교는 actor weight를 동일하게 두고 teacher privileged latent와 student inferred latent만 바꿔 latent 경로 효과를 격리했다는 점이 좋다. 다만 한 seed, 한 zero-command rollout이므로 “student가 teacher보다 일반적으로 우수하다”는 결론은 내릴 수 없다.

artifact identity:

| Run | checkpoint SHA256 | actor SHA256 | encoder SHA256 |
|---|---|---|---|
| 08-09 / 08-19 student 999 | `e37f6c1936d699627afb109ef141138958a3f0890028c1c8e1c107056b4a8b10` | `caa4645a6b3ff5e608b5705c520f5947eb954b4d8ec38acdc51cec50350e1f27` | `490c21e247bdf15858873211b5d8d833918cda4fb819cb9fb9fcf6a49976718d` |
| 08-19 teacher 9999 | `df81ed501e6b3ebecb67a5819a79be43cd17122ba78bd021db8c392fcb882891` | `caa4645a6b3ff5e608b5705c520f5947eb954b4d8ec38acdc51cec50350e1f27` | `ed88c5995a7648767621a9cc16001053a696156272eeead07cc2831f833b8352` |
| 08-20 deployable v5 | `020ae1d400ea14c85ecf33210ee76ec2d44ffc03cd0132de0b4cd719cc3dc1b6` | `4913cd9612aeafcc8f51cfe31dc45014ab9725ef29d5c343cb5fbbe23cbf984e` | `6de7a0daae71fdf57177a4f4d29f53b8c91a367b01aeaa5d81c16ad0a15b4a83` |
| 08-20 oracle-free stack0 | `efff7f99f3eb1a99f6bd06c37fae7b6b46c26ae7b75f3bdf41492304c6f46eea` | `d1f97d24f2adbccff4b9ec6f9bec9c0df51bf8aa68ea97bf0fcc2e41a8041686` | `f5626236dc23bd76ff9c4c4900d7658a350870a518dcbe738026c0f2c967aec2` |
| 08-23 multi-head | `7196c14cd3db12a38c311f371b9024f5e0e31c00ae17db237767d3631eded782` | runtime export; 원 문서에 SHA256 없음 | runtime export; 원 문서에 SHA256 없음 |

08-19 teacher/student actor가 byte-identical하다는 것은 표의 동일 actor hash로도 확인된다. observation-order audit는 비대칭 초기 posture가 adapter reorder 오류가 아니라 policy output에서 나온다는 것을 확인했다. 이는 sim2sim 문제를 만났을 때 tensor contract와 policy behavior를 분리한 좋은 진단 사례다.

### 12.5 read-only 센서 캡처

정적 elevation bag:

- duration `12.94 s`, size `916.6 MiB`, 총 `13,452` messages
- joint state `5,482`, IMU `5,481`, odometry `650`
- image streams `347/205` 등
- 관찰 rate: joint 약 `443.35 Hz`, IMU `440.73 Hz`, odometry `53.46 Hz`, ToF 약 `14 Hz`

데이터 획득 자체는 `ROBOT_READ_ONLY / PASS`다. stereo frame imbalance, right TF typo, 일부 비활성 센서 때문에 sensor readiness 전체는 `SUSPICIOUS`다. policy 최소 입력에는 joint/IMU/command가 핵심이지만, odometry는 read-only estimator 검증과 gap 진단의 ground truth로 중요하다.

### 12.6 legacy 2026-07-08~09 sim2sim artifacts

`tita_gluon_ws/deploy/tita/` 아래에는 policy trace, physics dump/comparison, handoff, actuator response, RL0 FSM, joint tracking, zero/drive JSON·CSV·NPZ가 남아 있다. 당시 대표 policy SHA256은 현재 policy가 아닌 `d53a5b0b69e5382dc5f40909ecaa7481221397aa3b3400c922b13a33576273e6`이다.

검증 흐름에서 확인된 주요 값:

- 서로 다른 initial observation에서는 action max difference `3.5747`
- 동일 observation을 강제하면 Isaac/Python runner parity max difference `2.98e-7`
- corrected model handoff 동일 observation A/B는 정확히 일치
- observation을 주입하면 obs difference `0.01446`, action difference `0.0720`
- legacy 10 s: max pitch `0.073 rad`, max wheel speed `6.82 rad/s`
- legacy 30 s: max pitch `0.0175 rad`, max wheel speed `0.281 rad/s`
- final 60 s: effective dt `0.020004 s`, max pitch `0.0853 rad`, roll `0.0350 rad`, max raw action `2.59`, scaled target `12.52`, torque `25.50`, action clipping 없음, max wheel speed `9.46 rad/s`

이 묶음은 원인 분리 과정의 유용한 증거지만 현행 `docs/exp/YYYY-MM-DD/` 밖에 있고 필수 metadata/hash가 일관되지 않아 전체 판정은 `SUSPICIOUS`다. 지금 policy의 회귀 기준으로 직접 재사용하지 말고 동일 실험을 현재 hash로 다시 생성해야 한다.

### 12.7 실기 Stage 1~3에서 얻은 것

Stage 1은 writer ownership, pinned request, measured transform-up, 5 s settle, SAFE_HOLD, full-power recovery를 검증했다. Stage 2는 1초 zero-command RL과 bounded blend, native mapping, timed SAFE_HOLD, log flush를 검증했다. 이 두 결과는 해당 SDK snapshot과 당시 config에 한해 `PASS`다.

Stage 3은 gain `0.3`, 총 `29.162 s` 실행 중 combined `vx=-0.3`, `wz=-0.3`에서 angular velocity가 `2.5 rad/s`를 넘어 SAFE_HOLD에 진입했다. writer 14,582회는 모두 성공했고 약 6 Hz oscillation이 지속됐다. 따라서 통신 failure보다 policy-plant closed-loop mode, actuator dynamics, delay, gain 또는 state-estimation mismatch를 우선 의심한다. Stage 3는 watchdog이 작동했다는 점은 `PASS`, 정책 안정성은 `SUSPICIOUS`다.

---

## 13. Sim-to-real gap: 증거 기반 원인 트리

### 13.1 모델/관절 동역학 gap

원본 MuJoCo MJCF의 base mass는 `13.2 kg`, URDF 기준은 `11.3623 kg`로 약 `16.17%` 차이였고 base inertia 성분은 최대 약 `85.7%`까지 달랐다. 또 원본 joint는 damping `0.1`, frictionloss `0.2`를 넣었지만 Isaac 쪽은 external PD를 기준으로 한다. corrected MJCF는 URDF inertial을 복사하고 joint passive damping/friction을 0으로 맞췄다.

이 수정으로 “policy 차이”처럼 보이던 결과 중 일부가 plant 차이였음을 분리했다. 그러나 실기의 motor current loop, reduction/compliance, backlash, static friction, battery voltage, thermal derating은 여전히 모델링돼 있지 않다.

### 13.2 actuator와 timing gap

현재 My training env는 `0~4` physics-step, 즉 `0~20 ms` delayed PD를 randomize한다. 반면 이 actuator를 구성하는 과정에서 기존 `DCMotor`의 torque-speed saturation 표현을 잃는다. MuJoCo reference mode는 policy 50 Hz/action hold 4회이지만 torque는 200 Hz마다 다시 계산한다. YAML의 `torque_update_rate_hz: 250`는 이 경로에서 사용되지 않는다.

실기 writer가 500 Hz라고 해서 policy와 actuator가 500 Hz로 새 결정을 내리는 것은 아니다. 실제 chain은 대략 다음과 같다.

```text
50 Hz policy target
  -> target interpolation / writer loop
  -> vendor SDK + motor controller
  -> unmeasured latency, bandwidth, saturation, compliance
  -> joint/IMU feedback
```

6 Hz oscillation을 설명하려면 단순 fixed delay뿐 아니라 first-order actuator lag, jitter, torque-speed saturation, target slew와 SDK 내부 interpolation을 sweep해야 한다.

### 13.3 observation/estimator gap

actor는 true linear velocity를 직접 보지 않고 learned estimator에 의존한다. simulation의 IMU/gravity/joint noise와 실기의 bias, vibration, filtering, timestamp skew가 다르면 estimator latent가 systematic하게 어긋날 수 있다. My env가 per-episode gyro/gravity/encoder bias를 넣는 것은 좋은 방향이지만:

- camera/odometry는 policy input이 아니어서 estimator correction에 직접 쓰이지 않음
- inter-sensor timestamp/transport delay가 training에 명시적으로 들어가지 않음
- history length가 0인 current estimator-PPO는 temporal filtering 능력이 제한됨
- real log에서 estimator output과 odometry truth의 정량 비교가 아직 없음

따라서 실기 다음 단계 전에 motor command를 쓰지 않는 `ROBOT_READ_ONLY` shadow inference로 estimator error, action spectrum, watchdog margin을 먼저 측정해야 한다.

### 13.4 initial-state/handoff gap

MuJoCo reset posture는 실제 RL entry에서 얻은 `[-0.024, 0.891, -2.634, 0, 0.028, 0.894, -2.648, 0]`인데 policy default offset은 `[0.1, 0.8, -1.5, 0]` 양측이다. `reference_transform_up`은 open-loop high-gain trajectory이고 wheel balance option은 config에만 있고 실제로 쓰이지 않는다. 반복 handoff error가 약 `1.207 rad`였던 이유를 정책 불량 하나로 돌릴 수 없다.

학습 reset distribution, transform-up final pose, policy default pose, 첫 action target을 같은 좌표계와 단위로 비교해야 한다. entry state가 학습 support 밖이면 좋은 steady-state policy도 첫 수 프레임에서 큰 corrective action을 낼 수 있다.

### 13.5 reward/selection gap

My44는 mean reward가 가장 높았지만 corrected MuJoCo drift는 My43보다 컸다. 이는 weighted training objective가 실제 deployment KPI와 같지 않음을 직접 보여 준다. selection은 최소한 다음 vector로 해야 한다.

```text
[zero drift, yaw drift, max tilt, wheel speed/action,
 action spectrum, torque/saturation, height dip,
 estimator error, perturbation recovery, handoff transient]
```

단일 scalar가 필요하면 먼저 hard safety constraint를 통과시킨 뒤 Pareto/frontier 또는 normalized score를 사용한다. unsafe rollout이 높은 reward로 선택되는 구조는 피한다.

### 13.6 계획돼 있지만 아직 실행되지 않은 actuator mismatch 실험

`docs/plan/actuator_dynamics_mismatch_exp.md`는 frozen PPO를 대상으로 delay `0~3` policy steps, actuator time constant `0/10/20/40/80 ms`, 여러 seed와 perturbation을 sweep하고 zero-command metrics 및 PSD를 비교하는 계획이다. 이것은 실행 로그가 아니므로 현재 상태는 `NOT_TESTED`다.

권장 보강:

- Stage 3 로그의 약 6 Hz peak와 simulation PSD peak를 같은 estimator로 계산
- fixed delay와 random jitter를 분리
- torque-speed envelope, target slew, first-order lag를 각각 단독/조합 sweep
- left/right parameter asymmetry 포함
- policy hash, MJCF hash, config hash, seed를 각 row에 기록
- baseline My43/My45와 current candidate를 동일 matrix로 비교

---

## 14. 코드에서 확인되는 핵심 기술

### 14.1 manager-based RL 구성

Isaac Lab의 scene, observations, actions, commands, rewards, termination, events, curriculum을 config class로 분리했다. 이 구조는 실험 delta를 작게 만들고 같은 task에서 train/play 변형을 상속으로 관리한다. 다만 상속과 YAML 주석이 많아 effective config dump를 아티팩트로 남겨야 재현성이 생긴다.

### 14.2 asymmetric actor-critic와 privileged learning

actor에는 배포 가능한 proprioception만 주고 critic에는 true base velocity/privileged dynamics를 줄 수 있다. 학습 중 critic은 더 정확한 state로 variance를 줄이고, 배포 actor는 oracle sensor를 요구하지 않는다. RMA teacher/student도 같은 철학을 latent adaptation으로 확장한다.

### 14.3 auxiliary estimator의 end-to-end 학습

PPOWithEstimator는 33-D observation에서 3-D base linear velocity를 추정하고 이를 actor input에 붙인다. estimator output을 detach하지 않으므로 estimator는 supervised MSE뿐 아니라 PPO actor gradient도 받는다. 이 설계는 task-useful representation을 학습할 수 있지만 loss scale에 따라 velocity accuracy와 control utility가 충돌할 수 있어 둘을 별도 metric으로 봐야 한다.

### 14.4 ONNX contract와 runtime adapter

single-input estimator PPO, two-input history NP3O, multi-head RMA는 graph contract가 다르다. runtime은 이름, rank, shape, dtype, output 개수를 strict하게 검증해야 한다. 실제 `sim2sim/cosim_ros2_jazzy/config/tita.yaml`의 history `10`과 deploy 기본 single-input ONNX 조합이 fail-fast한 것은 silent corruption보다 안전한 동작이다.

### 14.5 좌표계와 joint order adapter

native actuator order와 observation interleaved order가 다르므로 reindex를 한 곳에서 명시하고, round-trip unit test를 둬야 한다. command frame, quaternion convention, projected gravity, joint offset/scale까지 계약으로 취급한다. 동일 observation parity test가 runner 문제와 physics 문제를 분리하는 가장 빠른 방법이었다.

### 14.6 deterministic sim2sim과 단계적 진단

좋은 진단 순서는 다음과 같다.

1. 같은 tensor를 두 runner에 넣어 action parity 확인
2. 같은 state에서 observation parity 확인
3. policy를 고정하고 plant만 A/B
4. corrected inertial/passive joint parameter 적용
5. reset/handoff를 고정
6. delay/lag/noise/randomization을 한 축씩 추가
7. 최종 closed-loop statistics 비교

이 순서는 “MuJoCo에서 넘어진다”는 큰 현상을 tensor, adapter, initial state, actuator, rigid-body model로 나눠 추적 가능하게 만든다.

### 14.7 실기 안전 구조

실기 경로는 one-writer invariant, ownership preflight, measured initial pose, bounded blend, watchdog, SAFE_HOLD, append-only log를 조합한다. 중요한 점은 `SetJointCommand` 호출 성공이 stability evidence가 아니라는 것이다. state freshness, action/target/torque envelope, loop deadline, fall/velocity threshold가 모두 독립적으로 감시돼야 한다.

---

## 15. 재현 가능한 closed-loop 검증 절차

### 15.1 아티팩트 freeze

실험 전에 다음을 한 manifest에 고정한다.

- git commit/dirty status
- task ID와 effective environment config
- checkpoint SHA256, exported ONNX SHA256
- ONNX input/output names, shapes, dtype
- robot URDF/MJCF SHA256
- runtime YAML SHA256
- seed, env count, iteration, simulation dt/decimation
- hardware SDK commit/request ABI와 controller binary hash

현재 deploy 기본 `tita_gluon_ws/deploy/tita/policy.onnx`의 확인된 contract는 `[1,33] -> [1,8]`, SHA256 `025ad9b5a2022a9b2854623a3ff7149a73b3118585eb3744a1c5ab5e3e90090c`다. `policy_my7rsl.onnx`는 33-D + `10×33` two-input이며 SHA256 `420e904a28ab66611d85bef9f34083a546ef70ab954d76fc8c2c87f41270c672`다. 서로 교환 가능한 파일이 아니다.

### 15.2 최소 회귀 matrix

| Gate | 입력 | 필수 출력 | 실패 시 |
|---|---|---|---|
| static contract | ONNX + YAML | exact names/shapes/history/action semantics | export/runtime 수정, rollout 금지 |
| tensor parity | saved observation | PyTorch/ONNX/C++ action diff tolerance | adapter/export 원인 분리 |
| reset parity | same q/dq/base/command | observation slice별 diff | 좌표계/default pose 수정 |
| 5 s zero command | seeds × model variants | drift/yaw/tilt/wheel/action/torque | selection 탈락 또는 gap 분석 |
| command steps | ±vx, ±wz, combined | tracking/overshoot/settling/PSD | gain/reward/dynamics 재검토 |
| perturbation | push/mass/friction/delay/lag | recovery/fall/saturation rate | randomization/support 확대 |
| handoff | measured entry distribution | first-action/target delta/tilt transient | reset/transform/blend 정렬 |
| shadow inference | live read-only state | freshness, estimator error, action/watchdog margins | motor command 금지 |
| bounded robot | 승인된 짧은 zero command | all gates + SAFE_HOLD recovery | 다음 Stage 금지 |

### 15.3 experiment log template

모든 새 결과는 `docs/exp/YYYY-MM-DD/<task_or_run>.md`에 아래를 기록한다.

```markdown
# <run name>

- Execution Domain: VALIDATION_SIM
- Evidence Status: PASS | SUSPICIOUS | BLOCKED | FAIL | NOT_TESTED
- Git commit / dirty state:
- Checkpoint SHA256:
- ONNX SHA256 and graph contract:
- URDF/MJCF/config hashes:
- Exact command, seed, duration:
- Safety controls:

## Metrics
...

## Observed behavior and log summary
...

## Interpretation
사실 / 추론 / 아직 검증하지 않은 항목을 분리한다.
```

### 15.4 단계별 운용 체크리스트

`TRAINING_SIM`

- task registration과 effective config 확인
- observation/action slice unit test
- seed와 checkpoint cadence 기록
- training reward 외 deployment KPI 평가
- 선택 checkpoint를 hash로 고정하고 export parity 실행

`VALIDATION_SIM`

- corrected model 사용 여부 기록
- viewer 전에 headless deterministic test
- same-observation action parity
- zero/step/perturbation/handoff matrix
- PSD, clipping, torque-speed envelope와 saturation 기록
- 모든 결과를 `docs/exp/`에 저장

`ROBOT_READ_ONLY`

- vendor controller만 writer인지 확인
- state/topic freshness/rate/frame audit
- policy shadow inference만 수행, output API 호출 금지
- estimator와 odometry 비교, predicted action envelope 기록

`ROBOT_COMMAND_FREE_RUNTIME`

- direct binary를 띄우더라도 motor output disabled 보장
- exact SDK ABI, ownership, logger, watchdog self-test
- stale/non-finite/deadline fault injection으로 SAFE_HOLD 경로 확인

`ROBOT_STATE_CHANGING`

- 별도 operator 승인, physical support, approved power cut
- 한 writer만 존재, fresh-session preflight
- zero command와 짧은 duration부터 시작
- exit code가 아니라 telemetry/watchdog/behavior로 판정
- Stage 후 로그 flush, power cycle/recovery, 새 실험 문서 작성

---

## 16. 취업·면접용 프로젝트 설명

### 16.1 30초 요약

> TITA wheeled-legged robot의 locomotion 정책을 Isaac Lab에서 학습하고 ONNX로 export한 뒤, MuJoCo와 실제 로봇까지 같은 observation/action contract로 연결했습니다. 단순히 “시뮬레이터에서 돈다”가 아니라 inertial·PD·관절 순서·history contract를 검증하고, one-writer와 SAFE_HOLD를 둔 단계적 sim-to-real 절차를 만들었습니다. PPO estimator 정책은 현재 single-input C++ 배포 경로와 가장 잘 맞았고, zero-command drift를 기준으로 reward/checkpoint를 반복 개선했습니다. 실기에서는 6 Hz 진동과 watchdog 진입을 확인해 actuator delay·lag·estimator mismatch를 다음 회귀 실험으로 구조화했습니다.

### 16.2 STAR 답변 예시

**상황:** Isaac에서는 서 있던 정책이 MuJoCo 또는 실기에서 drift/oscillation을 보였고, 정책·adapter·물리 모델 중 원인을 구분하기 어려웠다.

**과제:** 학습에서 실기까지 tensor와 timing 계약을 추적하고, 위험한 실기 시행착오를 줄이는 재현 가능한 검증 경로를 만드는 것이었다.

**행동:** 33-D observation과 8-D action을 slice 단위로 명세하고 joint reindex를 고정했다. PyTorch/ONNX/runtime에 동일 tensor를 넣어 action parity를 확인한 뒤 URDF/MJCF inertial과 passive joint dynamics를 교정했다. zero-command drift, tilt, wheel action, torque, PSD로 checkpoint를 비교하고, 실기는 read-only → command-free → bounded command와 one-writer/SAFE_HOLD gate로 나눴다.

**결과:** runner parity를 `2.98e-7` 수준으로 확인했고, corrected MuJoCo에서 My43 drift를 `0.022 m/5 s`까지 낮췄다. 실기 Stage 1/2를 통과했고 Stage 3의 약 6 Hz mode에서 watchdog이 안전하게 개입했다. 이 결과를 actuator lag/delay sweep과 shadow estimator 검증이라는 다음 작업으로 연결했다.

### 16.3 “왜 PPO가 NP3O보다 좋았나?”에 대한 정확한 답

면접에서 가장 안전하고 기술적으로 정확한 답은 다음과 같다.

> 모든 조건에서 PPO의 보행 성능이 NP3O보다 우월하다고 증명한 것은 아닙니다. 이 repository에는 동일 task·seed·budget의 직접 비교가 없습니다. 다만 estimator-PPO는 현재 33-D single-input ONNX/C++ runtime과 일치하고, My41~45의 Isaac/MuJoCo/실기 증거가 가장 많이 축적되어 운영상 더 좋은 선택이었습니다. 반면 NP3O는 10-frame history와 두 입력을 요구하고, TITA cost config가 없어 당시 실행에서는 사실상 PPO+Barlow-Twins 형태였습니다. 안전 비용 제약이라는 NP3O의 장점을 검증하지 못한 채 배포 복잡도만 늘어났기 때문에 현 단계에서는 PPO를 baseline으로 선택했습니다.

좋지 않은 답은 “NP3O보다 PPO reward가 높았다”이다. 그런 controlled result는 없다.

### 16.4 예상 기술 질문과 답변 포인트

**Q. actor에 base linear velocity가 없는데 어떻게 제어합니까?**

33-D proprioception으로 3-D velocity를 추정하는 auxiliary estimator를 actor 앞에 두고, critic은 학습 때 true velocity를 볼 수 있다. estimator는 MSE와 PPO gradient를 함께 받으며 export 시 single graph로 bake된다.

**Q. 왜 sim2sim을 합니까?**

같은 policy를 다른 physics/runtime에서 돌리면 policy 자체, tensor adapter, initial state, rigid-body/actuator model을 분리할 수 있다. 실제 장비에서 찾기 전에 싸고 반복 가능한 regression gate가 된다.

**Q. reward가 높으면 좋은 정책 아닌가요?**

My44가 반례다. mean reward `53.58`로 비교군 최고였지만 MuJoCo zero drift `0.181 m/5 s`로 My43의 `0.022 m/5 s`보다 나빴다. reward와 deployment KPI를 분리해 선택해야 한다.

**Q. 실기 안전은 어떻게 보장했습니까?**

보장을 주장하지 않고 risk를 줄였다. one-writer ownership, measured initial pose, bounded blend, state freshness, finite/range/deadline/watchdog, SAFE_HOLD, physical support와 별도 operator 승인을 결합했다. Stage 3는 불안정성을 발견했고 watchdog이 개입한 `SUSPICIOUS` 결과다.

**Q. 6 Hz 진동 원인은 무엇입니까?**

아직 확정하지 않았다. writer failure는 없어 transport보다는 closed-loop mode 가능성이 크다. actuator lag/delay와 torque-speed envelope, target interpolation, estimator bias/timestamp, handoff state, gain을 각각 sweep하고 실기 PSD와 비교해야 한다.

**Q. 왜 history가 있는 NP3O/RMA가 항상 더 낫지 않습니까?**

history는 partially observable dynamics를 추정하는 데 유리하지만 graph/runtime/state-buffer contract가 복잡해지고 train-deploy history initialization mismatch가 생긴다. 성능 이득은 controlled benchmark로 입증해야 하며, 현재 single-input deployment evidence는 estimator-PPO가 더 성숙하다.

**Q. 가장 어려웠던 버그는 무엇입니까?**

서로 다른 initial observation 때문에 생긴 action 차이를 runner 오류로 오해할 수 있었던 점이다. 동일 tensor를 강제했을 때 차이가 `2.98e-7`로 줄어 adapter/export가 아니라 state/physics 경로 문제임을 확인했다.

### 16.5 이력서 bullet 예시

- Built an end-to-end RL locomotion validation pipeline for an 8-DoF wheeled-legged robot across Isaac Lab, ONNX, MuJoCo, and a guarded C++ hardware runtime.
- Defined and verified a deployable 33-D proprioceptive observation and 8-D hybrid position/velocity action contract, including cross-runtime joint-order adapters and sub-micro numerical parity checks.
- Reduced corrected-MuJoCo zero-command drift to `0.022 m/5 s` in the best documented PPO run and showed why training reward alone was an unreliable deployment selector.
- Designed staged robot bring-up with one-writer ownership, bounded handoff, watchdogs, append-only telemetry, and SAFE_HOLD; isolated a real ~6 Hz closed-loop instability for actuator/estimator gap analysis.

수치는 해당 artifact/hash와 조건을 함께 설명할 수 있을 때만 사용한다. “production-safe”, “sim-to-real solved”, “PPO universally beats NP3O” 같은 표현은 현재 증거로 뒷받침되지 않는다.

---

## 17. 현재 미해결 리스크와 우선순위

| 우선순위 | 항목 | 상태 | 완료 조건 |
|---|---|---|---|
| P0 | SDK snapshot과 current `tita_gluon_ws` controller drift | `BLOCKED` | 단일 canonical tree/ABI/config 선정, hash 고정, tests 재실행 |
| P0 | `sim2sim/cosim_ros2_jazzy/config/tita.yaml` history 10 + deploy 기본 single-input policy 불일치 | `FAIL` | 올바른 pair로 수정하고 strict runner smoke `PASS` |
| P0 | Stage 3 약 6 Hz oscillation | `SUSPICIOUS` | log PSD 재현, delay/lag/gain/estimator A/B로 원인 범위 축소 |
| P0 | current gain `0.75`, duration `0`의 실기 승인/증거 부재 | `NOT_TESTED` | bounded config와 별도 operator 승인; current 조합 자동 실행 금지 |
| P1 | actuator torque-speed/lag model 부재 | `NOT_TESTED` | planned matrix 실행 및 real response identification |
| P1 | transform-up/handoff 약 `1.207 rad` error | `SUSPICIOUS` | training reset/entry/default pose 정렬과 first-action transient gate |
| P1 | estimator real error 미측정 | `NOT_TESTED` | read-only odometry/IMU synchronized comparison |
| P1 | My45 좌우 wheel delta 비대칭 | `SUSPICIOUS` | symmetry audit, multiple seeds/model A/B |
| P1 | NP3O vs PPO controlled comparison 부재 | `BLOCKED` | 동일 task/seed/steps/eval matrix, cost config 포함 |
| P2 | legacy artifacts가 `docs/exp/` 밖에 있음 | `SUSPICIOUS` | current hashes로 재실행하고 표준 log로 이관 |
| P2 | My34~40와 My45c provenance 불완전 | `BLOCKED` | original config/checkpoint/log 복구 또는 결과 주장 폐기 |
| P2 | stereo/TF 및 비활성 센서 | `SUSPICIOUS` | frame/rate audit와 재캡처 |

권장 작업 순서는 P0 contract drift 수정 → current hash로 deterministic sim2sim 회귀 → actuator/PSD sweep → read-only shadow estimator → handoff 정렬 → 별도 승인된 bounded robot Stage다. 앞 gate가 실패하면 뒤 단계로 진행하지 않는다.

---

## 18. 소스 탐색 인덱스

### 학습/task

- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/__init__.py`: Gym task 등록
- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/locomotion_env_cfg.py`: 공통 observation/action/reward/event 기반
- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/rough_env_cfg.py`: TITA의 33-D observation, 8-D action, reward/event 기준
- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py`: estimator-PPO용 delay/bias/command/reward override와 play 설정
- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/agents/rsl_rl_ppo_cfg.py`: estimator-PPO runner config
- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/agents/np3o_cfg.py`: NP3O runner config
- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/mdp/`: observations, rewards, costs, events와 command 구현
- `lab/ddt_lab/ddt_lab/assets/ddt_robot.py`: `DDT_TITA_CFG` articulation, actuator, joint limits/default pose
- `lab/ddt_lab/ddt_lab/algorithms/estimator/`와 `lab/ddt_lab/ddt_lab/algorithms/np3o/`: PPOWithEstimator와 NP3O 구현
- `lab/ddt_lab/scripts/rsl_rl/`와 `lab/ddt_lab/scripts/np3o/`: 학습, 평가, export, 진단 entry point

### MOO/RMA

- `lab/ddt_lab/ddt_lab/tasks/moo_based/locomotion/velocity/tita_env/`: MOO/CO-RL task, observation/reward/action 및 RMA-teacher config
- `lab/scripts/co_rl/core/modules/teacher_student.py`: RMA teacher/student actor와 adaptation module
- `lab/scripts/co_rl/core/algorithms/moo_ppo.py`: MOO-PPO 및 teacher/student update
- `lab/scripts/co_rl/core/runners/moo_on_policy_runner.py`: teacher/student 생성, checkpoint와 runner 계약
- `docs/exp/2026-07-24/`~`docs/exp/2026-08-23/`: source-port, teacher/student, sim2sim 기록

### export/sim2sim

- `sim2sim/cosim_ros2_jazzy/cosim_ros2_jazzy/`: ONNX runner, observation/history/action adapter, MuJoCo loop, Real2Sim와 ghost node
- `sim2sim/cosim_ros2_jazzy/config/`: checkpoint별 policy/model/timing/gain/watchdog 설정
- `tita_gluon_ws/src/ddt_ros2_control/urdfs/tita_description/mujoco/`와 `mujoco_corrected/`: 비교한 원본/corrected MJCF
- `sim2sim/cosim_ros2_jazzy/scripts/`: inspection, parity, physics-gap, drift와 handoff probe
- `sim2sim/cosim_ros2_jazzy/launch/`: Sim2Sim, direct/relay/offline Real2Sim, ghost launch entry point
- `tita_gluon_ws/deploy/tita/`의 policy artifacts: 실제 사용 전 hash/graph contract 재확인 필수

### 실기/안전

- `sdk/tita_low_level_sdk_ros2_humble/`: pinned upstream, direct-control reference snapshot, 안전/Stage 문서와 tests
- `tita_gluon_ws/src/`: current C++ controller/runtime
- `tita_gluon_ws/src/tita_stage1_controller/config/`: current policy/control/watchdog 설정
- `tita_gluon_ws/deploy/tita/`: deploy script와 legacy diagnostic artifacts
- `docs/plan/actuator_dynamics_mismatch_exp.md`: 아직 실행되지 않은 gap 실험 계획

### 문서 해석 원칙

1. executable code와 실제 artifact shape/hash를 최우선으로 본다.
2. 같은 이름이라도 SDK snapshot, workspace current controller, legacy artifact를 합치지 않는다.
3. config comment는 effective runtime 값과 충돌하면 근거로 사용하지 않는다.
4. `PASS`의 범위를 항상 적고 smoke/integration/behavior/safety를 분리한다.
5. 실기 결과는 해당 commit, policy, gain, duration, watchdog에만 적용한다.

---

## 19. 결론

이 repository에서 가장 성숙한 TITA 경로는 **33-D proprioception + embedded velocity estimator PPO → single-input ONNX → corrected MuJoCo → staged C++ runtime**이다. 강점은 observation/action 계약을 코드 수준에서 추적하고, reward가 아닌 deployment metric으로 checkpoint를 비교하며, 실기를 ownership와 watchdog gate로 나눈 점이다.

동시에 아직 “sim-to-real 완료” 상태는 아니다. default policy/history mismatch가 있고, SDK snapshot과 current controller가 갈라져 있으며, Stage 3에서 약 6 Hz closed-loop instability가 관측됐다. 따라서 다음 성공 기준은 더 오래 로봇을 움직이는 것이 아니라, **한 canonical artifact/config를 고정하고 현재 hash로 sim2sim 회귀와 actuator/estimator gap 실험을 통과한 뒤 read-only shadow evidence를 확보하는 것**이다.

PPO 선택은 NP3O에 대한 보편적 우월성 주장이 아니라, 현재 배포 계약과 축적된 실험 증거에 기반한 engineering decision이다. 이 구분을 지키는 것이 이 프로젝트의 기술적 신뢰성과 면접에서의 설득력을 동시에 높인다.
