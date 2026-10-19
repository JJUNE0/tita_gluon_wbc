# heading drift 보상 실험 — 예약

- Execution Domain: TRAINING_SIM
- Policy Checkpoint SHA256: N/A (학습 예약 단계)
- Evidence Status: 환경 검사 PASS (13/13, `heading_drift_experiment/heading_task_check.json`). 학습 NOT_TESTED
- 근거와 베이스 선택: `sphere_hardware_yaw_review.md`

## 구성

| 항목 | 값 |
|---|---|
| 태스크 | `DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-Heading-v0` (`MyTitaFlatPosKneeMA2SphereFastHeadingEnvCfg`) |
| 베이스 | ③ `MyTitaFlatPosKneeMA2SphereFastEnvCfg`: 구 휠, MA2, ±1.5 m/s / ±3 rad/s, ramp 없음 |
| 추가 보상 | `zero_command_heading_drift` (`real2sim/rewards.py: ZeroCommandHeadingDrift`), weight 1.0. 정지 1.0 s 후 world yaw를 기준으로 exp(−5·\|Δψ\|)를 주고, upright로 감쇠한다. 명령이 들어오거나 reset되면 기준을 해제한다 |
| critic 관측 | `heading_drift_error` (`real2sim/observations.py`): 보상 항의 `heading_error`를 그대로 읽는다(scale 2, clip ±3.2). critic 37 → 38 |
| 정책 관측 | 34개 그대로 (배포 인터페이스 변경 없음) |
| 학습 | FlashSAC, seed 42, 100k step, 4096 env |
| 실행 | `test/launch_heading_experiment.sh`. unit `heading-ma2-fast-s42`가 `sphere-chain`(⑤ 학습) 종료를 기다린 뒤 시작한다. 로그는 `heading_drift_experiment/heading-ma2-fast-s42_console.log`다 |

## 환경 검사 (`test/check_heading_drift_task.py`, CPU 8 env, 상태 직접 쓰기)

모두 PASS:
- warmup 전 보상 0
- warmup 시점 기준 설정
- root yaw +0.2 rad → 오차 0.2, 보상 exp(−1)
- critic 관측 = 보상 오차
- 명령 입력 시 기준 해제
- ±π wrap
- reset 시 해제
- 정책 관측 34
- critic 항 = 베이스 + `heading_drift_error`
- 명령 범위·ramp·구 휠·MA2가 ③과 같음
- 30 step 유한

첫 실행의 FAIL 2건은 검사 코드 실수였다(wrap 기대 부호, critic 항 비교에 그룹 설정 키 포함). 수정 후 재검사했다. 첫 실행 로그는 `*_attempt1_testbugs.*`에 있다.

## 소스 해시 (예약 시점)

| 파일 | SHA256 |
|---|---|
| real2sim `env_cfg.py` | `a23a6725f0f752d98443717f961ea5a889d7139dac5f407ea726c591e8e29bd0` |
| real2sim `rewards.py` | `aaf947df53887d86af7537d78498c46f5a2406f52796c8ec4c0978ae74975114` |
| real2sim `observations.py` | `2cbfcc3023dc26316a5dd8e9a3c5327ad55a9c2234704c1b1371591863b11afb` |
| real2sim `__init__.py` | `f326de4f37ca0ebcc1d70643d6b9720c530ec214b76ab4455c59d23dc4d10135` |

⑤(`cyl-noma2-s42`)는 수정 전에 이미 import된 상태로 학습 중이다. 이번 수정의 영향을 받지 않는다.
