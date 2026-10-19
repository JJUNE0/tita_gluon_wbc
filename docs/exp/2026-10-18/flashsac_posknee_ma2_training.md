# A80k 후속 학습 1개 — URDF CoM + 위치 오차 관측 + 다리 MA2 + 무릎 92/2.3

Execution Domain: `TRAINING_SIM` (설정 diff, live env 검사, smoke, 전체 학습 1개 실행 중). 로봇 접근·배포 없음.

**Evidence Status:**
- **PASS**: 설정 diff, live env 검사, smoke(유한 update), 학습 시작(W&B 연결, step 1500까지 유한).
- **NOT_TESTED**: 학습 완료, 정책 성능, sim2sim, 실기.
- 학습 중이라 Policy checkpoint SHA256은 아직 없다(N/A).

**기준:** A80k(`tita_flash_sac_201940_278440`, task `…-BaseComShift-v0`). 근거는 [실기 종합](real_runs_vs_training.md) 3절이다.

## A 대비 변경 (config diff 기준)

| # | 항목 | A | 이번 학습 `DDT-Velocity-Flat-Tita-My-PosKneeMA2-v0` |
|---|---|---|---|
| 1 | base CoM DR | x −5.5…−1.5, y ±2, z ±3 cm | **x, y, z 모두 ±1.5 cm (URDF 중심)**. 다른 body CoM은 고정(A와 같음) |
| 2 | actor 관측 | 33 | **34**: 마지막에 `wheel_position_error`를 추가했다. critic은 36에서 37로 늘었다(노이즈 없음) |
| 3 | 다리 action | 그대로 적용 | **다리 6개 MA2** (현재 + 직전 원래 action 평균). reset 후 첫 step은 원래 값을 쓴다. 휠은 그대로이고 `last_action` 관측과 action_rate 보상은 원래 출력 기준이다 |
| 4 | 무릎 PD | 60/1.5, Kp·Kd 각각 독립 ±20% | **92/2.3 × 공통 배율 log-U[0.55, 1.0] × 관절별 jitter 0.8–1.2** |
| — | hip·shoulder·휠 | 각각 독립 ±20% | 같다(이벤트 대상을 `.*_leg_[124]`로 한정) |

보상, 명령, push, IMU bias, joint offset, 지연 0–20 ms, FlashSAC 설정, seed 42는 A와 같다.

**설정 diff:** [config_diff_vs_A.log](flashsac_posknee_ma2_training/config_diff_vs_A.log).
- 위 항목 외에 차이로 나오는 것은 `prim_path`(`{ENV_REGEX_NS}`), `terrain.num_envs`·`env_spacing`이다. 이전 diff와 같은 표기 차이로, 해석 전 설정과 저장된 설정을 비교해서 생긴다.

**위치 오차 관측 정의:** [`real2sim/observations.py`](../../../lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/real2sim/observations.py).
- `s = R·mean(q_wheel + body_pitch + q_thigh + q_knee)`. 엔코더와 자세만 쓰고 GT 위치는 쓰지 않는다.
- 명령이 zero band(|vx|, |vy| ≤ 0.02, |yaw| ≤ 0.03)를 벗어나면 기준이 s를 따라가고 관측은 0이다.
- band 안에서는 기준을 고정하고 `clip(s − ref, ±0.3 m)`를 낸다. 관측 scale은 5, 노이즈는 ±5 mm, 반지름은 episode마다 ×U(0.97, 1.03)이다.
- 다리·자세 보정 부호는 MuJoCo에서 확인했다([`check_wheel_odometry_sign.py`](../../../test/sim2real/check_wheel_odometry_sign.py)): A80k 주행 중 바퀴 중심 이동 대비 20 ms당 오차가 c = +1이면 0.08–0.12 mm, 보정 없으면 0.56–0.63 mm다.

## 실행 전 검사

**live env** ([check.json](flashsac_posknee_ma2_training/env_check/check.json), 128 env, CPU): PASS.
- 관측: policy 34, critic 37, priv 18, action 8. policy_interface에 `wheel_position_error`가 기록된다.
- 무릎 Kp 배율 0.46–1.15(평균 0.75), Kd 0.46–1.15. hip·shoulder·휠은 0.80–1.20이다.
- base CoM 분산 ±1.5 cm, 다른 body 0이다.
- MA2: 다리 6개 처리값이 기본값 + scale × 평균(0.4, −0.2) = 0.1과 일치한다. 휠은 원래 값이고, manager action(=`last_action`)도 원래 값이다.
- 위치 오차 로직(상태를 직접 써넣는 방식):
  - 고정 직후 0이다.
  - 휠 +0.1 rad → R·0.1(오차 ≤ 2e-6), 허벅지 +0.05 rad → R·0.05다.
  - 반지름 배율 0.970–1.030이다.
  - 명령 중 0, 재고정 0, clip 0.30이다.
  - 1차 시도(물리 스텝 방식)는 command zero 창과 env 리셋 때문에 판정이 불가능했다([log](flashsac_posknee_ma2_training/env_check_attempt1_stepping.log)).

**smoke:** `tita_flash_sac_180142_514585`, 4 env, 8 step, min_buffer 16 / buffer 64 / batch 16. 이전 smoke와 같은 설정이다. PASS(update 6회, 유한)였다([log](flashsac_posknee_ma2_training/train_smoke.log)).
- 앞선 두 번(256·4096 env, 기본 replay)은 warmup 전에 끝나 update가 0이었다. 로그는 남겨 두었다.

## 실행 (2026-10-18 18:02 KST 시작)

| 항목 | 값 |
|---|---|
| run_name | `posknee_ma2_s42` |
| native run | `tita_flash_sac_180212_290240` |
| W&B | [xooow0ny](https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/xooow0ny) |

- **명령:** 4096 env, 100k step, seed 42.
- **실행 방식:** systemd user unit `posknee-ma2-s42.service`(MemoryMax 32G, VS Code와 다른 cgroup)로 띄웠다([launch](posknee_ma2_s42_launch.json), [console](posknee_ma2_s42_console.log)).
- **시작 확인:** step 1500까지 유한했다. update 2948, 메모리 4.2 GB, GPU 65% / 5.8 GB였다.
- **예상 종료:** 단독 실행이라 약 600 step/min이므로 21:00 KST 전후다.

## 코드 (학습 중 수정 금지)

**신규:**
- `real2sim/actions.py` (`f57b125f…`)
- `real2sim/observations.py` (`4bb4bdc2…`)

**추가:**
- `real2sim/env_cfg.py`에 `MyTitaFlatPosKneeMA2EnvCfg` (`4c00a64a…`)
- `real2sim/__init__.py`에 task 등록 (`c2b37b08…`)
- 기존 task와 `my_flat_env_cfg.py`는 변경 없음

**test:**
- `test/check_posknee_ma2_task.py`
- `test/sim2real/check_wheel_odometry_sign.py`

## 남은 일 (이 정책을 sim2sim·실기에서 돌리기 전)

이 정책은 **관측이 34개**라 지금 배포 경로(33개)에서 그대로 돌릴 수 없다. 다음이 필요하다.
1. `wheel_position_error`를 sim2sim adapter와 `tita_node` `ObservationBuilder`(상태 보존, 휠 각도 unwrap)에 같은 정의로 추가한다. export 인터페이스도 함께 바꾼다.
2. Python–C++ parity를 검증한다.
3. 배포는 무릎 92/2.3 + `leg_action_filter:=ma2_legs`로 한다.
4. 실기는 별도 승인 후에만 진행한다.
