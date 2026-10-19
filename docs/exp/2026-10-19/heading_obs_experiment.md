# heading 실험 (actor + critic heading 관측) — MA2 run 학습 중, MA2 없는 run 예약

- Execution Domain: TRAINING_SIM
- Policy Checkpoint SHA256: N/A (학습 예약 단계)
- Evidence Status:
  - 환경 검사: MA2 run PASS (12/12, `heading_obs_task_check.json`). 추가 항목 포함 재검사도 PASS(`<task>_check.json`). MA2 없는 run도 PASS
  - 학습 결과: NOT_TESTED
  - MA2 run은 10:26 시작, wandb `imjyqmur`
- 배경:
  - `heading_drift_experiment.md`의 critic-only run(unit `heading-ma2-fast-s42`)은 학습 시작 전에 취소했다(사용자 결정, 2026-10-19 09:55).
  - heading 소스 선택의 근거는 `heading_source_review.md`다.

## 구성

| 항목 | 값 |
|---|---|
| 태스크 | `DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-HeadingObs-v0` (`MyTitaFlatPosKneeMA2SphereFastHeadingObsEnvCfg`) |
| 베이스 | ③ 구 휠, MA2, ±1.5 m/s / ±3 rad/s, ramp 없음 |
| 보상 | `zero_command_heading_drift` (critic-only 버전과 같음: 1.0 s warmup 후 world yaw 기준, exp(−5·\|Δψ\|), weight 1.0) |
| actor 관측 (35번째) | `heading_error` = `GyroHeadingError`. 0 밴드(0.02/0.02/0.03)에서 1.0 s 유지 후 (yaw rate + bias)·dt를 적분한다. 명령이 들어오거나 reset되면 0이다. 출력 clip ±0.5 rad, 내부 적분은 유지한다. scale 2, noise ±0.003 rad, 에피소드별 bias 잔차 U(±0.0014 rad/s = ±0.08 °/s) |
| critic 관측 | 부모의 critic(+ `heading_drift_error`)에 `heading_error`를 bias·noise 없이 추가 (37 → 39) |
| 실기 계산 계획 | RL 진입 전 정지(idle/sit) 구간의 gyro z 중앙값을 바이어스로 저장하고, 위와 같은 규칙으로 (gyro z − 바이어스)를 적분한다. IMU 쿼터니언은 쓰지 않는다 |
| 학습 | FlashSAC, seed 42, 100k step, 4096 env |
| 실행 | `test/launch_heading_experiment.sh`. unit `heading-obs-ma2-fast-s42`가 `sphere-chain`(⑤ 학습) 종료를 기다린 뒤 시작한다. 로그는 `heading_obs_experiment/heading-obs-ma2-fast-s42_console.log`다 |

## 환경 검사 (`test/check_heading_obs_task.py`, CPU 8 env, yaw rate 소스 고정)

모두 PASS:
- 정책 bias가 ±0.0014 안이고, critic bias는 0
- warmup 중 0
- warmup 후 (0.1 + bias)·dt·10 적분이 정확
- 출력 clip 0.5, 내부 적분 유지
- 명령 입력 시 0
- reset 시 0
- 정책 관측 35개, 마지막이 heading_error
- critic = 부모 + heading_error
- heading drift 보상 존재
- scale·noise 설정
- 30 step 유한

## 소스 해시 (예약 시점)

| 파일 | SHA256 |
|---|---|
| real2sim `env_cfg.py` | `d2703d7b232a7b02476f0061789a12b82b74e60c169dd5bfeb398c0afd0b8a97` |
| real2sim `observations.py` | `5d93cc8d1ebdf689cfa31659b2cbc99ede0ac1f9f4375decbc4586335b841cb6` |
| real2sim `rewards.py` | `aaf947df53887d86af7537d78498c46f5a2406f52796c8ec4c0978ae74975114` |
| real2sim `__init__.py` | `65cb8cba7b4b526744c158cd03c354e20049d156e58f1c86183423cb27bb6ae7` |

## 배포 전 남은 일

- export, sim2sim `ObservationBuilder`, `tita_node`에 `heading_error`를 추가하고 parity를 확인한다.
- 실기 gyro 바이어스 추정 구간을 정한다.
- sim2sim 스크린은 sim2sim adapter가 이 관측을 지원해야 돌릴 수 있다.


## 추가: MA2 없는 heading run (예약, 2026-10-19 11:04)

| 항목 | 값 |
|---|---|
| 태스크 | `DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObs-v0` (`MyTitaFlatPosKneeSphereHeadingObsEnvCfg`) |
| 베이스 | ② 구 휠, MA2 없음, **기본 명령 ±1.0 m/s / ±1.5 rad/s, ramp 0.5** |
| heading 항 | MA2 run(`...Fast-HeadingObs-v0`)의 설정 객체를 그대로 사용: 보상, critic `heading_drift_error`, actor·critic `heading_error`. 검사에서 cfg 사전이 같음을 확인 |
| 명령을 빠르게 하지 않은 이유 | MA2 없음 + 빠른 명령(④)은 sim 25 Hz 대리 지표에서 g ≤ 1.5 교번 또는 넘어짐이 나왔다 |
| 실행 | `test/launch_heading_experiment.sh noma2`. unit `heading-obs-noma2-s42`가 `heading-obs-ma2-fast-s42` 종료를 기다린 뒤 시작한다 |

비교 축:

| 비교 | 보는 것 |
|---|---|
| MA2 run 대 MA2 없는 run | MA2 + 빠른 명령 대 MA2 없음 + 기본 명령 (두 요인이 함께 다름) |
| MA2 없는 run 대 ② | heading 보상·관측 효과 |
| MA2 run 대 ③ | heading 보상·관측 효과 |

예약 시점 해시: real2sim `env_cfg.py` `19c4f746813a35389189fd86b8ffaff7b90fe65340331fda3ec1fc3aea9c7bd1`, `__init__.py` `0b50a49d84d017c34a433ee7982e4b66042d97e55b9e9dcf0514e60d33656422`. 실행 중인 MA2 run은 이전 해시(`d2703d7b…`, `65cb8cba…`) 시점에 import됐다. 이번 변경은 새 클래스 추가뿐이다.

## sim2sim 검증: MA2 heading run (`tita_flash_sac_102630_755853`, 2026-10-19 12:45)

- Execution Domain: VALIDATION_SIM (MuJoCo, production sim2sim adapter, `test/screen_sphere_wheel_runs.py`)
- Evidence Status: PASS (정지 heading 유지) / **FAIL (정지 직후 회전)**. 실기 NOT_TESTED. 배포 비권장
- Policy Checkpoint SHA256: `sphere_wheel_screen/policies.json`의 `exp6_heading_ma2_fast` 6개 (ONNX parity ≤ 3.7e-6)

### sim2sim 지원 추가

- `checkpoint.py`: `GyroHeadingError` → kind `heading_error` (clip_rad, zero_thresholds, warmup_s; 학습용 bias_range는 제외)
- `adapter.py` `ObservationBuilder.heading_error`: 학습과 같은 규칙. `gyro_bias` 속성은 실기 보정값 자리다
- `lab/ddt_lab/scripts/flash_sac/export.py`: 35-관측 actor export 허용
- 단위 테스트 `test/test_sim2sim_heading_error.py` PASS: warmup 0, 적분, clip과 내부값 유지, 명령 시 0, bias 차감, reset

### 결과

| 지표 (plant A = 구 휠 + 무릎 L0.60/R0.75) | ⑥ 50k–100k | ③ 70k (heading 항 없음) | 기준 75k |
|---|---|---|---|
| 정지 8–32 s yaw rate | **−0.00 °/s (6개 모두, plant B도 같음)** | −0.57 | +0.21 |
| 정지 1–8 s 회전 | −1.4 ~ −2.8° | −4.9° | — |
| 주행 후 정지 \|yaw\| 평균 | 0.32–1.18 °/s | 0.76 | 0.39 |
| 25 Hz 대리 g = 1.5 | 교번 없음 | 없음 | 없음 |
| 빠른 명령 추종 vx / wz 최대 오차 | 0.11–0.52 / 0.06–0.41 | 0.29 / 0.08 | — |

무릎 조건별 진단(`heading_obs_experiment/sim2sim_diag/`, 90k·60k·③ 70k × A / 좌우 반전 / 0.68 대칭 / nominal / 원통):

| | 정지 8–32 s yaw rate (5개 조건) | 각 정지의 처음 1 s 회전 | RL 시작 첫 1 s |
|---|---|---|---|
| ⑥ 90k | 모두 −0.00 °/s | 구 휠 −7 ~ −16°, 원통 −4 ~ −7° | −11 ~ −14° |
| ⑥ 60k | 모두 −0.00 ~ −0.01 °/s | 구 휠 −14 ~ −18°, 원통 −5 ~ −11° | −13 ~ −15° |
| ③ 70k | −0.05 ~ −2.24 °/s | −0.1 ~ −4.7° | −2.6 ~ +0.4° |

- **방향 유지 (성공)**: heading 관측을 받은 정책은 warmup 뒤 정지 heading을 모든 무릎 조건에서 유지한다(−0.00 °/s). 비대칭 방향에 따라 ±2 °/s까지 돌던 ③과 대조된다. 가설("actor가 heading 오차를 보면 비대칭과 무관하게 잡는다")을 sim이 지지한다.
- **정지 직후 회전 (실패)**:
  - 모든 정지(yaw 명령 뒤뿐 아니라 전후진 명령 뒤에도)와 RL 시작에서, warmup 1 s 동안 같은 방향(시계)으로 7–18° 돈 뒤 멈춘다.
  - 무릎 조건과 무관하다(좌우 반전에서도 같은 부호). 따라서 plant 탓이 아니라 정책 고유의 습관이다.
  - 보상 기준과 관측이 모두 warmup 뒤에 시작하므로, warmup 1 s가 heading 벌점이 없는 구간이 됐다.
  - 원통 휠에서는 비틀림 저항 때문에 작아질 뿐 남는다.
  - warmup 뒤 남은 오차(−1.3 ~ −2.8°)는 0으로 되돌리지 않는다.
- 결론: ⑥ 체크포인트는 실기 배포를 권하지 않는다. 매 정지마다 약 10° 회전하기 때문이다.

### 다음 학습 수정 제안

- warmup을 0으로 둔다. 0 밴드 진입 순간을 보상 기준과 관측의 기준으로 같이 쓴다. 회전 명령 해제 후 감속 중 회전도 오차에 포함된다.
- 또는 warmup 구간에 yaw-rate 페널티를 넣는다.
- 지금 학습 중인 MA2 없는 run(`heading-obs-noma2-s42`)도 같은 1 s warmup 설계라서 같은 습관이 생길 가능성이 크다.

### 정지 직후 회전의 모양과 해석 (`heading_obs_experiment/stop_flick.png`)

⑥ 90k, plant A, 명령이 정확히 0이 된 순간을 0 s로 맞춤:

| 정지 종류 | 0–1 s 회전 | 0–1 s yaw 각속도 | 1–3 s 회전 | ③ 70k 0–1 s 회전 |
|---|---:|---|---:|---:|
| 전진 0.6 m/s 정지 후 | −9.6° | 0.1 s 안에 −11 °/s, 1 s 동안 약 −9 °/s 유지 | −1.3° | −0.6° |
| 회전 +1.0 rad/s 정지 후 | −7.4° | −6 ~ −8 °/s 유지 | −0.8° | −0.9° |

- 명령이 0이 되는 순간 시계 방향(위에서 볼 때 오른쪽, yaw 음수) 회전이 거의 일정한 속도로 시작된다. warmup이 끝나 heading 관측이 켜지는 1.0 s에 0.2–0.3 s 만에 멈춘다. 타이머 모양이다.
- 해석: 정책이 heading 관측을 자기 내부의 일정한 시계 방향 바이어스를 상쇄하는 피드백으로 쓴다.
  - 관측이 0으로 고정된 warmup 동안에는 상쇄가 없어 바이어스만큼(약 −9 °/s) 돈다.
  - 관측이 켜지면 오차가 약 −1.3 ~ −2.8°까지 쌓인 지점에서 균형이 맞아 멈춘다.
  - 그 잔여 오차를 0으로 되돌리지 않는 것도 같은 이유다. 바이어스를 상쇄하려면 0이 아닌 오차가 필요하다(바이어스가 있는 비례 제어와 같은 모양).
  - 무릎 조건(좌우 반전 포함)과 무관하게 부호가 같다는 점도 정책 고유 바이어스라는 해석과 맞는다.
- 실기 의미: 조이스틱을 놓을 때마다(또는 RL 진입 직후) 약 1 s 동안 오른쪽으로 8–17° 돈 뒤 멈춘다.
- warmup 0의 기대 효과: 관측이 정지 순간부터 켜져 바이어스가 바로 상쇄된다. 남는 회전은 균형 오차(약 2°) 수준으로 줄 것으로 본다. 정지 직후 오차도 보상에 포함되므로 바이어스 자체를 없앨 동기도 커진다(가설, 미검증).

## MA2 없는 run 중지 → warmup 0 재학습 (2026-10-19 12:55)

- 중지: `heading-obs-noma2-s42` (1 s warmup, run `tita_flash_sac_124141_691725`, wandb `eavi51sk`)를 step 8300에서 멈췄다(사용자 결정). 로그는 `heading-obs-noma2-s42_console_stopped_8300_warmup1s.log`다.
- 재학습 태스크: `DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObsW0-v0` (`MyTitaFlatPosKneeSphereHeadingObsW0EnvCfg`)
  - MA2 없는 heading run과 같고, heading 보상과 actor·critic `heading_error`의 `warmup_s`만 0.0이다.
  - 보상은 첫 정지 step에서 기준을 잡고, 관측은 그다음 step부터 적분한다(warmup_steps = 1).
- 환경 검사 PASS (`DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-HeadingObsW0-v0_check.json`):
  - 세 항의 warmup이 0이다.
  - 보상 기준이 첫 호출에서 잡힌다.
  - 관측은 첫 호출 0, 이후 적분한다.
  - 나머지 heading 설정은 기준과 같다.
  - 관측 35개, MA2 없음, 기본 명령, 구 휠이다.
- 실행: `test/launch_heading_experiment.sh noma2w0`. unit `heading-obs-noma2-w0-s42`, 12:55:47 시작, wandb `gpiijbvm`. step 300까지 유한하다.
- 시작 시점 해시:
  - `env_cfg.py` `5eb19aa54da5442a37a254adb75b477cabbca2f6ffcc71684c37e41bae772fb3`
  - `__init__.py` `497cd7ab4c310eeabb9db4f54a75041751db8804355a5c66c0019df57579af4c`
  - `observations.py` `5d93cc8d…`
  - `rewards.py` `aaf947df…`
- 배포 시 sim2sim·C++의 heading warmup도 config의 `warmup_s`(0)를 따른다. sim2sim `ObservationBuilder`는 이미 config 값을 읽는다.

## warmup 0 run 중간 확인 (model_45000, 학습 중) 및 sim2sim 명령 설정

- Execution Domain: VALIDATION_SIM (`heading_obs_experiment/w0_45k_slip/`)
- Policy Checkpoint SHA256: `f1afd22c40dcba6060a5ff13cac519e94811f295a6f7a199d91c5b319f0094ff` (ONNX `8f81d4ae…`, parity 3.5e-6)
- Evidence Status: PASS (sim), 실기 NOT_TESTED

### 정지 직후 회전 (warmup 1 s 대 0)

| | 정지마다 처음 1 s 회전 | 1 s 이후 | 정지 8–32 s yaw rate |
|---|---|---|---|
| ⑥ MA2 heading (warmup 1 s) 90k, plant A | −7 ~ −14° | −0.8 ~ −1.3° | −0.00 °/s |
| warmup 0 45k, plant A (구 휠, 왼쪽 약함) | −1.7 ~ +0.9° | −1.8 ~ +0.4° | −0.00 °/s |
| warmup 0 45k, A_nom (구 휠, nominal) | −0.3 ~ +0.6° | 0 ~ +0.7° | −0.00 °/s |
| warmup 0 45k, B_nom (원통, nominal = 뷰어) | −0.2 ~ +0.6° | 0 ~ +0.6° | +0.01 °/s |

warmup을 없애자 정지 직후 회전이 사라졌다. 정지 heading 유지는 그대로다. RL 시작 첫 1 s 회전도 ±1.2° 이내다.

### 미끄러짐 (106 s 주행 일정, 8 s 이후)

| plant | 바퀴 굴림 대비 몸통 이동 | 옆미끄럼 누적 / 평균 \|v_y\| | 엔코더 대비 실제 회전 |
|---|---|---|---|
| B_nom (뷰어와 같은 원통 휠) | 0.975 | 0.21 m / 2.0 mm/s | 0.942 |
| A (구 휠) | 0.972 | 0.27 m / 2.5 mm/s | 0.985 |
| A_nom | 0.977 | 0.26 m / 2.7 mm/s | 0.975 |
| 참고: 실기 yaw 명령 구간 (`heading_source_review.md`) | — | — | 0.89–0.93 |

정지 중 미끄러짐은 없다(이동 0, 회전 ≤ 0.3°). 회전 중 원통 휠은 약 6% 헛돈다. 실기(7–11%)보다 작다.

### sim2sim 키보드 명령 = 학습 명령

- 범위는 이미 export 때 학습 env의 `lin_vel_x`, `ang_vel_z`를 쓰고 있었다(warmup 0 run: ±1.0 m/s, ±1.5 rad/s).
- ramp는 0.5/s로 하드코딩돼 있었다. ramp 없음(1000/s)으로 학습한 ③④⑥과는 달랐다.
- 수정:
  - `checkpoint.py`가 학습 `ramp_rate`를 `sim_command_ramp`로 export한다(없으면 None = 계단).
  - `sim2sim_node.py` 키보드가 그 값을 쓰고, 시작 시 범위와 ramp를 출력한다.
  - 이 키가 없는 이전 config는 0.5/s를 유지한다.
- config 지문이 바뀌므로 다음 실행 때 CLI가 자동으로 다시 export한다.
- 확인: warmup 0 45k 재export(ramp 0.5, 관측 35, 필터 none), headless 300 step PASS. ⑥ 90k는 ramp 1000, ② 60k는 0.5로 읽힌다.

## warmup 0 run 학습 완료 (100k, 2026-10-19 15:30 확인) 및 후반 체크포인트 스크린

- Execution Domain: TRAINING_SIM (학습 완료 확인), VALIDATION_SIM (MuJoCo 스크린). 로봇 명령 없음
- Evidence Status:
  - 학습: PASS (100k 정상 종료, 넘어짐 종료 0.02%)
  - 스크린: PASS (기본 36/36, 회전 18/18, 강건성 55/60)
  - 강건성 FAIL 5건은 모두 25 Hz probe g = 3에서 넘어진 것
- 체크포인트 actor SHA256:

| step | actor SHA256 |
|---|---|
| 75k | `8e57560840cc2bcbab9b58459e9d016a0650380e1005bdf73e3cf0549927b4f2` |
| 80k | `42f3a7a1ba96786173864093e7960673172fe67441aa4b0e10da968110632e01` |
| 85k | `3d5a11b48b82f75ab2253fc30e451a90fe18f4a984842103ad669c8f8d54bd7b` |
| 90k | `87dd73ca1933bf43c50b36fed7fbad7e2a1e8238af0458904f43075400b407e1` |
| 95k | `925e932814f43b02dcf661ced77f73940444eadb7d94df2155f17d3c2fe0fce3` |
| 100k | `3cd73e64d014031dacaa183c477fab3264ca29de68abcde4322c2b684db32e4a` |

- export parity: 3.0–4.3e-6 (`sphere_wheel_screen/prepare_exp7_tail.log`)
- 학습 보상: 스텝 보상 평균 50k 0.0594 → 80k 0.0607 → 90k–100k 0.0607–0.0608. 대략 80k 이후 평평하다.
- 마지막 에피소드 보상: heading 0.315, 위치 0.117, 회전 추종 0.771

### 제자리 회전 (`--turn`)

정지 → +1 rad/s 5 s → 정지 → −1 rad/s 5 s → 정지. 각 칸은 \|vx\| (m/s) / 이동 (m) / 허벅지 변화 (°) / pitch 변화 (°) / 회전 추종 비율이다.

| step | A (구 휠, 무릎 L0.60/R0.75) | A_nom (구 휠, 공칭 무릎) | B_nom (원통 휠, 공칭) |
|---|---|---|---|
| 50k (실기) | 0.086 / 0.14 / 2.0 / 1.7 / 1.03 | 0.080 / 0.15 / 3.2 / 2.5 / 1.01 | 0.085 / 0.28 / 3.3 / 2.6 / 0.89 |
| 60k | 0.057 / 0.06 / 1.5 / 0.9 / 1.04 | 0.043 / 0.09 / 0.8 / 3.1 / 1.04 | 0.047 / 0.11 / 0.6 / 3.2 / 0.90 |
| **65k** | **0.007 / 0.08 / 1.2 / 1.1 / 1.06** | 0.046 / 0.10 / 0.9 / 0.9 / 1.05 | 0.043 / 0.10 / 0.7 / 0.9 / 0.99 |
| 75k | 0.084 / 0.18 / 2.2 / 3.9 / 0.98 | 0.069 / 0.14 / 2.1 / 2.3 / 0.98 | 0.092 / 0.32 / 2.9 / 2.7 / 0.79 |
| 80k | 0.029 / 0.16 / 2.6 / 3.1 / 1.01 | 0.034 / 0.12 / 1.1 / 2.7 / 1.02 | 0.037 / 0.14 / 0.8 / 2.6 / 0.98 |
| 85k | 0.041 / 0.06 / 3.0 / 4.0 / 1.01 | 0.112 / 0.16 / 0.6 / 2.4 / 1.00 | 0.108 / 0.31 / 0.9 / 2.9 / 0.76 |
| 90k | 0.058 / 0.16 / 2.7 / 3.6 / 1.00 | 0.031 / 0.06 / 0.5 / 2.7 / 1.01 | 0.037 / 0.12 / 0.2 / 1.9 / 0.76 |
| 95k | 0.075 / 0.12 / 2.2 / 2.7 / 1.02 | 0.103 / 0.23 / 1.8 / 4.2 / 1.03 | 0.098 / 0.28 / 1.8 / 3.9 / 0.84 |
| 100k | 0.063 / 0.15 / 1.7 / 2.5 / 1.01 | 0.026 / 0.09 / 1.0 / 1.0 / 1.01 | 0.025 / 0.08 / 0.7 / 1.1 / 0.83 |

### 정지·강건성

| step | A 정지 yaw | A 주행 후 정지 \|yaw\| 평균 / 최대 (°/s) | A 정지 pitch | 무릎 4종 정지 yaw | 무릎 4종 주행 후 정지 | 25 Hz g = 2 | 25 Hz g = 3 |
|---|---|---|---|---|---|---|---|
| 50k (실기) | 0.000 | 0.063 / 0.157 | 4.1° | 0.000 | 0.035–0.054 | 넘어짐 | 넘어짐 |
| 60k | 0.000 | 0.042 / 0.174 | 3.9° | 0.000 | 0.017–0.037 | 버팀 (교번 0.046) | 넘어짐 |
| **65k** | 0.000 | 0.040 / 0.094 | **2.9°** | 0.000 | 0.022–0.043 | 넘어짐 | 넘어짐 |
| 75k | 0.000 | 0.042 / 0.135 | 2.6° | 0.000 | 0.020–0.043 | 버팀 (0.115) | 넘어짐 |
| 80k | 0.000 | 0.039 / 0.075 | 5.2° | 0.000 | 0.029–0.038 | 버팀 (0.11) | 넘어짐 |
| 85k | 0.000 | 0.023 / 0.053 | 5.7° | 0.000 | 0.026–0.054 | 버팀 (0.087) | 넘어짐 |
| 90k | 0.000 | **0.014 / 0.026** | 4.3° | 0.000 | 0.012–0.061 | 버팀 (0.31) | 버팀 (0.098) |
| 95k | 0.000 | 0.018 / 0.047 | 4.6° | 0.000 | 0.020–0.034 | 버팀 (0.23) | 넘어짐 |
| 100k | 0.000 | 0.034 / 0.136 | 3.8° | 0.000 | 0.032–0.058 | 버팀 (0.105) | 넘어짐 |

"무릎 4종"은 A_mirror, A_sym068, A_sym055, A_nom이다.

### 해석

- 정지 heading은 모든 체크포인트, 모든 조건에서 0.00 °/s다.
- **실기와 가장 비슷한 plant A에서 제자리 회전은 65k가 여전히 가장 좋다.**
  - 75k–100k의 허벅지 변화는 1.7–3.0°, pitch 변화는 2.5–4.0°로 65k(1.2°/1.1°)보다 크다.
  - 원통 휠에서는 85k–100k의 회전 추종이 0.76–0.84로 떨어진다(65k 0.99).
- 학습을 더 하면 25 Hz 교란에 대한 생존 여유는 커진다. 75k–100k는 g = 2에서 버티고, 90k는 g = 3도 버틴다. 하지만 버티는 동안의 교번 진폭은 0.09–0.31이다.
- 증거의 한계:
  - plant마다 결정적 rollout 1회다.
  - 1–3° 차이는 실기에서 본 허벅지 +13–18°에 비해 작다.
  - 그래서 체크포인트 순위는 약한 증거다.
  - 50k < 60k 순서는 운영자의 sim2sim 뷰어 관찰과 일치한다.
- 실기 후보 순위:
  1. **65k**: 회전 자세, 정지 pitch
  2. 60k: 회전, 25 Hz 여유
  3. 100k: 공칭 무릎에서 회전 양호, g = 2 생존. 다만 plant A에서 허벅지 1.7°, pitch 2.5°
- `test/screen_sphere_wheel_runs.py` 변경: `ROBUST`에 exp7 75k–100k 추가. 로그는 `sphere_wheel_screen/{prepare,evaluate}_exp7_tail*.log`
