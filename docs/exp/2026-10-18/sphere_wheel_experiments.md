# 휠 점 접촉 / MA2 / 명령 범위 학습 실험 5개

- Execution Domain: TRAINING_SIM
- Policy Checkpoint SHA256: N/A (학습 시작 단계)
- Evidence Status: 환경 검사 PASS (5개 태스크). 학습 시작 확인은 아래 "시작 확인" 참고. 결과는 NOT_TESTED
- 근거: `flashsac_posma2_50000_202450_review.md` 7절. 원통 휠의 정지 yaw 저항이 정책의 휠 차동을 가렸다. `flashsac_posma2_75000_210936_review.md`(75k 실기)

## 실험 구성

모든 실험의 기반은 `MyTitaFlatPosKneeMA2EnvCfg`(posma2 run `tita_flash_sac_180212_290240`)이고, 표에 적은 것만 바꿨다. 공통 설정은 FlashSAC, seed 42, 100k step, 4096 env다.

| 실험 | 태스크 | 휠 충돌 | 다리 MA2 | 명령 lin_vel_x / ang_vel_z | systemd unit | 시작 |
|---|---|---|:---:|---|---|---|
| ① | `DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-v0` | 구 | O | ±1.0 / ±1.5 | `sphere-ma2-s42` | 즉시 |
| ② | `DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-v0` | 구 | X | ±1.0 / ±1.5 | `sphere-noma2-s42` | 즉시 |
| ③ | `DDT-Velocity-Flat-Tita-My-PosKneeMA2-Sphere-Fast-v0` | 구 | O | ±1.5 / ±3.0, **ramp 없음** | `sphere-ma2-fast-s42` | ①② 종료 후, 혼자 |
| ④ | `DDT-Velocity-Flat-Tita-My-PosKnee-Sphere-Fast-v0` | 구 | X | ±1.5 / ±3.0, **ramp 없음** | `sphere-noma2-fast-s42` | ③ 종료 후, 혼자 |
| ⑤ | `DDT-Velocity-Flat-Tita-My-PosKnee-v0` | 원통(기존) | X | ±1.0 / ±1.5 | `cyl-noma2-s42` | ④ 종료 후, 혼자 |

①②⑤의 명령 ramp는 기본값 0.5 units/s다. ③④는 `ramp_rate` 1000 units/s라서 방출 명령이 매 step 목표값과 같다. reset settle 구간과 standing env 샘플링은 그대로다.

비교 축:

| 비교 | 보는 효과 |
|---|---|
| ① vs posma2 | 휠 접촉 |
| ② vs ① | MA2 (구 휠) |
| ⑤ vs posma2 | MA2 (원통 휠) |
| ② vs ⑤ | 휠 접촉 (MA2 없음) |
| ③ vs ① | 명령 범위 + ramp 제거 (두 요인이 함께 바뀜) |
| ④ vs ③ | MA2 (빠른 명령, ramp 없음) |

### 휠 점 접촉 구현

- `sphere_wheel_urdf()`(real2sim `env_cfg.py`)가 원본 URDF를 읽는다. `left_leg_4`, `right_leg_4`의 collision cylinder(반경 0.0925 m, 길이 0.034 m)를 같은 반경의 sphere로 바꾼 복사본을 `/tmp/ddt_lab_real2sim/tita_sphere_wheels_<sha12>.urdf`에 쓴다.
- 메시 경로 `package://tita_description/`는 절대경로로 바꾼다. 시각 메시, 질량·관성, 관절, 다른 collision은 그대로다. 원본 `robot.urdf`는 수정하지 않는다.
- 효과:
  - 원통은 폭 방향 선 접촉이라 제자리 회전에 비틀림 마찰이 걸린다.
  - 구는 한 점 접촉이라 비틀림 마찰이 없다.
  - 구르는 반경, 전후·옆 마찰, 마찰 DR(0.2–1.6)은 같다.
- 한계:
  - 비틀림 저항 0은 실기보다 낮은 극단이다.
  - 몸이 옆으로 기울 때 접촉점 이동이 원통과 다르다(원통은 가장자리 ±1.7 cm).
  - Isaac에서 원통의 정지 yaw 저항은 직접 측정하지 않았다(MuJoCo에서만 확인).

### 주의

- ③④: ramp가 없어서 명령이 계단처럼 바뀐다. ramp는 원래 조이스틱 증분에 맞추고 명령 시작 시 어깨 떨림을 줄이려고 넣었다(`RampedVelocityCommand` docstring). 그 떨림이 다시 나올 수 있다. 실기 조이스틱 명령 형태도 배포 전에 확인해야 한다.
- ②④⑤: MA2가 없으므로 export에서 `leg_action_filter: none`이 기록된다. 원래 MA2로 억제했던 실기 25 Hz 교번이 다시 나올 수 있다.
- ③④: 실기 배포 시 조이스틱 명령 스케일도 바꿔야 한다.
- 배포는 별도 승인 사항이다.

## 환경 검사 (TRAINING_SIM, `test/check_sphere_wheel_tasks.py`, CPU, 16 env)

| 태스크 | 휠 collision (USD) | 다리 action | 명령 범위 | obs / action | 30 step 유한 | 결과 |
|---|---|---|---|---|:---:|:---:|
| PosKneeMA2 (기준) | Cylinder ×2, r 0.0925 | MA2 | ±1.0 / ±1.5 | 34 / 8 | O | PASS |
| ① | Sphere ×2, r 0.0925 | MA2 | ±1.0 / ±1.5 | 34 / 8 | O | PASS |
| ② | Sphere ×2 | JointPosition | ±1.0 / ±1.5 | 34 / 8 | O | PASS |
| ③ | Sphere ×2 | MA2 | ±1.5 / ±3.0 | 34 / 8 | O | PASS |
| ④ | Sphere ×2 | JointPosition | ±1.5 / ±3.0 | 34 / 8 | O | PASS |
| ⑤ | Cylinder ×2 | JointPosition | ±1.0 / ±1.5 | 34 / 8 | O | PASS |

- 나머지 collision(Cube)은 기준과 같다. 결과는 `sphere_wheel_experiments/env_check/*.json`, `*.log`에 있다.
- 첫 검사에서는 instance proxy 탐색 누락으로 collision prim을 찾지 못했다. 탐색을 고쳐 재검사했다.
- 기준과 ①은 실험 4·5 클래스를 추가하기 전 파일로 검사했다. 해당 클래스 코드는 같다. ②–⑤는 최종 파일로 검사했다.

## 소스 해시 (학습 시작 시점)

| 파일 | SHA256 |
|---|---|
| real2sim `env_cfg.py` (①② 시작 시점) | `37be97c31e6f230f6f8db7399bbaeda80816f10713d7bcc91ce9b25ac00b1f77` |
| real2sim `env_cfg.py` (③④⑤, ramp 제거 후) | `ee62644f1b28609cf5815a88d0f1b92bfbc7b904bb8a7a69b0a557f1364e66cb` |
| real2sim `__init__.py` | `e48b7b38b4887125a2396927bb5f063dd6bbfcb86fdd6967f1cfd38a9ccd55b9` |
| 원본 `tita_description/urdf/robot.urdf` | `0941b83136cd5c8c89bbb33165bff515a3a988d33319b67c8b06bfb9c71350ce` |
| 생성 `tita_sphere_wheels_8e5fd1031897.urdf` | `8e5fd1031897d06ff1461bef929d4bef01729db0737b98b4a6f5602032816bfc` |

## 실행

- ①②: `test/launch_sphere_wheel_experiments.sh`로 시작했다.
- ③→④→⑤: `sphere-chain` unit(`test/run_sphere_wheel_chain.sh`)이 담당한다. ①②가 active가 아닐 때까지 60 s마다 확인한다. 그다음 학습을 하나씩 별도 unit으로 `systemd-run --wait` 실행한다. 한 run이 실패해도 다음 run은 진행된다.
- 순차로 바꾼 이유: GPU가 99%로 포화돼 동시 실행의 총 처리량이 단독과 같다. 3개 동시 약 236×3 step/min, 이전 단독 약 730 step/min(posknee 79.2k / 108 min)이다. 순차면 결과가 하나씩 더 빨리 나온다.
- 메모리 상한: unit당 MemoryMax 16G, MemoryHigh 14G. 이전 단일 run 실측은 RAM 4.2 GB, GPU 5.8 GB였다.
- 콘솔 로그: `sphere_wheel_experiments/<unit>_console.log`

## 시작 확인

| 실험 | unit | W&B run | 시작 | 확인 |
|---|---|---|---|---|
| ① | `sphere-ma2-s42` | [`jb40q3rp`](https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/jb40q3rp) | 22:04:37 | 22:28 step 7100, updates 14148, 유한 |
| ② | `sphere-noma2-s42` | [`3lbfdj7n`](https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/3lbfdj7n) | 22:04:37 | 22:28 step 7200, updates 14348, 유한 |
| ③ | `sphere-ma2-fast-s42` | — | ①② 종료 후 (ramp 없음 버전) | `sphere-chain` 대기(bash/sleep만 실행) |
| ④ | `sphere-noma2-fast-s42` | — | ③ 종료 후 | 대기 |
| ⑤ | `cyl-noma2-s42` | — | ④ 종료 후 | 대기 |

- 자원: 22:28 기준 3개 동시 실행에 GPU 15.2 GB / 99%, unit당 RAM 4.2 GB.
- **③ 첫 시도 실패 (FAIL, 수정됨):**
  - 세 unit이 같은 초에 시작했다. URDF→USD 변환이 같은 임시 디렉터리 `/tmp/IsaacLab/usd_20261018_220450_1824`를 썼다.
  - ③은 `left_leg_1.tmp.usd`를 열지 못해 `[Fatal] attempted member lookup on NULL TfRefPtr<UsdStage>`로 12 s 만에 종료됐다. 로그는 `sphere-ma2-fast-s42_console_attempt1_usd_race.log`다.
  - 수정:
    - ③을 혼자 재시작했다.
    - 실행 스크립트에 시작 간격(전체 실행 90 s, ⑤는 ④보다 180 s 뒤)을 넣었다.
    - ④⑤ 대기 unit을 다시 만들었다. 이전 대기 unit은 bash/sleep만 실행 중일 때 멈췄고, 그 로그는 `*_console_queue1_replaced.log`다.
- **③ 두 번째 시도 중지 (23:49, 사용자 결정):**
  - ramp 0.5 버전 `im4knfd6`(run dir `lab/ddt_lab/logs/flash_sac/tita_flash_sac_222613_442713`)를 step 17400에서 멈췄다. 로그는 `sphere-ma2-fast-s42_console_attempt2_stopped_17400.log`다.
  - 사유: 3개 동시라 너무 느렸고, ③④는 ramp를 없애기로 했다.
  - ④⑤의 이전 대기 unit도 멈췄다. 로그는 `*_console_queue2_replaced.log`다.
- 23:51: ① step 25300, ② step 25600. ③④ 재검사 PASS(ramp 1000), ⑤ 재검사 PASS(ramp 0.5).
- 예상: ①②는 ③이 빠진 뒤 각각 빨라져 약 3–3.5 시간 뒤 종료된다. 그 뒤 ③④⑤가 각각 약 2.3 시간씩 걸린다(단독 속도 기준 추정).
