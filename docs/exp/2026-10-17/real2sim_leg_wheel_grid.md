# Real-to-sim grid — 실기 zero-command drift를 재현하는 MuJoCo 물리 파라미터

Execution Domains: DESKTOP_DRY_RUN (기존 실기 bag NPZ에서 특징 추출), VALIDATION_SIM (MuJoCo rollout 1,380회). 로봇 접근·배포·학습 없음.

Evidence Status: **PASS** — 파이프라인, 결정론적 재실행 일치, 맞출 때 쓰지 않은 체크포인트·조이스틱 검증. **SUSPICIOUS** — 식별값의 물리적 해석(sim 등가 파라미터이며, 실기의 하드웨어 원인은 미확인). 하드웨어 측정·재학습 효과는 **NOT_TESTED**.

Policy Checkpoint / ONNX SHA256 (`tita_flash_sac_115632_883848`, run `0r5o1bmm`):
- model_60000 `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05` / `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a` (fit 대상)
- model_50000 `d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c` / `0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873` (검증)
- model_75000 `381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730` / `2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114` (검증)

Branch: `agent/codex/dev_tita_gluon`. Script SHA256 `0ff2b2c6ca7f28e4c12c3b05c250763f7ce47220fb66a70bb51ca410a8df7d37`.

> **정정 (2026-10-17, 이후 증거 반영):** [motor feedback 보고서](flashsac_60000_motor_feedback_report.md)에서 큰 부하의 hip·무릎 축은 firmware 보고 토크/명령 gain이 0.9989–0.9993이었다. 아래의 `leg_gain≈0.6`은 실기 자세·명령 토크·drift 특징을 맞추는 **MuJoCo 등가 계수**이며, 실제 모터 출력이 40% 부족하다는 측정값이 아니다. 반대로 firmware 값은 외부 Nm 교정이 아니므로 실제 gain이 1.0이라고 확정하지도 않는다. 아래 "해석" 절의 "다리 출력 부족" 표현과 [0.5, 1.05] 범위는 이 의미로만 읽는다. 강건성용 탐색 범위이며 실측 범위가 아니다. 후속 holdout·수용시험·재학습 설정은 [재학습 준비 보고서](flashsac_retrain_prep.md)에 있다. 본문 수치와 SHA256은 그대로 보존했다.

## 방법

- **입력:** 사용자 보고 실기 무게 25–26 kg는 URDF 25.69 kg과 같다. 그래서 질량 배율은 1.0으로 고정했다.
- **실기 목표:** 60k 자유 drift run의 RL+5–10초. 특징 9개는 무릎/허벅지 각도, hip 벌어짐, 무릎·hip·휠 명령 토크, 전후 속도, IMU pitch, RL+0.5초 무릎 각도다. 손실은 Σ((sim − 실기)/허용폭)². 허용폭은 스크립트의 `TOLERANCE`에 있다.
- **시뮬레이션:** 기존 sim2sim 경로를 그대로 쓴다(splay → transform_up → sit → RL 상태기계, 고정 ONNX, native PD/clip). 물리값은 첫 `mj_step` 전에 고정한다. `StaticEnv`에 추가한 축은 다음과 같다.
  - 다리 출력 토크 배율 (startup 포함 모든 단계)
  - 다리/휠 `dof_frictionloss`
  - base CoM x 이동
  - IMU 장착 pitch 오프셋: 정책 관측과 기록 쿼터니언 모두 오프셋된 센서 프레임을 사용
- **비교 기준:** 기록 토크는 실기 bag과 같은 배율 적용 전 명령 토크다. 처음 2초는 기존 grid 규칙대로 유한값·기울기·높이 guard만 적용한다(RL 진입 무릎 −2.708 rad이 관절 범위 −2.67 밖이므로).
- **검증:** 다리 배율 0.6이 정확히 적용됐다(applied/commanded 0.6000). 휠 경로는 기존과 동일하다. 휠 속도 proxy와 GT 속도의 상관은 모두 0.86 이상이다. 최종 스크립트 재실행 결과가 이전 결과와 특징값 최대 차이 0.0으로 같았다.

## 결과 1 — grid A (1,000 조합: 다리 배율 8 × 다리 마찰 5 × 휠 마찰 5 × IMU 5)

PASS 988 / FAIL 12 (모두 약한 다리 + 높은 마찰 조합의 base_height_limit). [log](real2sim_leg_wheel_grid/grid_a.log), [profile](real2sim_leg_wheel_grid/grid_a_profile.log).

| | 무릎 q | 허벅지 q | hip 벌어짐 | 무릎 τ | hip τ | 휠 τ | 속도 | pitch | 무릎 q @0.5s | loss |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 실기 60k | −2.153 | +1.113 | +0.122 | +29.3 | −34.5 | −0.301 | −0.203 | 1.78° | −2.165 | — |
| **최적** (배율 0.60, 다리 마찰 2, 휠 마찰 0.3, IMU +2°) | −2.185 | +1.113 | +0.119 | +31.3 | −34.6 | −0.296 | −0.241 | 1.90° | −2.132 | **1.3** |
| nominal sim | −1.845 | +0.860 | −0.011 | +17.2 | −6.2 | −0.001 | +0.015 | 3.96° | −1.676 | 122.9 |

파라미터별 profile loss (다른 축에 대해 최소):

- 다리 토크 배율: 0.5:26.8, **0.55:9.5, 0.6:1.3, 0.65:3.1**, 0.7:10.3, 0.8:42.0, 1.0:76.8 — **0.55~0.65로 좁게 확정된다**.
- 다리 마찰 [N m]: 0:9.5, 2:1.3, 4:1.9, 6:3.1, 8:5.2 — 2~6.
- 휠 마찰 [N m]: 0:5.4, 0.1:3.0, 0.2:1.6, 0.3:1.3, 0.4:2.0 — 0.1~0.4. 주로 휠 토크 특징이 결정한다.
- IMU 오프셋: −1:17.1, 0:15.2, 1:5.5, **2:1.3**, 3:6.7.

최적점에서 한 요인씩 nominal로 되돌린 결과 (속도 / pitch):

| 조건 | 속도 (m/s) | pitch |
|---|---:|---:|
| 최적 | −0.241 | 1.90° |
| 다리 배율 → 1.0 | −0.126 | 1.99° |
| IMU → 0 | −0.062 | 4.14° |
| 다리 배율 0.6만 | −0.239 | 5.00° |
| IMU +2°만 | −0.178 | 1.99° |
| nominal | +0.015 | 3.96° |

두 요인 모두 단독으로 후진 drift를 만든다. 실기 pitch까지 함께 맞추려면 두 요인이 모두 필요하다. 마찰 항은 토크와 hip 특징을 맞춘다.

## 결과 2 — grid B (360 조합): CoM과 IMU 오프셋은 구분 불가

[profile](real2sim_leg_wheel_grid/grid_b_profile.log). min loss:

| CoM x \ IMU | 0° | +1° | +2° |
|---|---:|---:|---:|
| −3 cm | 2.4 | 6.3 | 19.8 |
| −2 cm | **0.7** | 3.3 | 9.5 |
| −1 cm | 5.6 | **0.7** | 3.6 |
| 0 cm | 16.6 | 6.1 | **1.3** |
| +1 cm | 17.4 | 16.5 | 2.7 |

"CoM 1 cm 뒤"와 "IMU +1°"가 같은 효과를 내는 대각선 골짜기다. 이 데이터로는 둘을 구분할 수 없다. 다리 배율은 여기서도 0.6(0.55:5.3, 0.65:3.1, 0.7:32.6)으로 유지된다.

## 결과 3 — 맞출 때 쓰지 않은 데이터로 검증

[결과](real2sim_leg_wheel_grid/validation_results.json), [조이스틱 log](real2sim_leg_wheel_grid/joystick_validation.log). 후보는 모두 배율 0.6, 다리 마찰 2, 휠 마찰 0.3이다: A = IMU +2°, B = CoM −1 cm + IMU +1°, C = CoM −2 cm.

| 검증 | A | B | C | nominal |
|---|---:|---:|---:|---:|
| 50k 체크포인트, 실기 8–10초 (loss) | **2.3** | 3.6 | 5.1 | 158.0 |
| 75k 체크포인트, 실기 12.8–15.3초 (loss) | 19.5 | 28.2 | 11.2 | 164.3 |
| 조이스틱 +0.143 m/s 명령 → 속도 (실기 +0.009) | **+0.016** | +0.033 | +0.046 | +0.240 |
| seed 270/913 (60k, loss) | 1.2 / 1.2 | 0.7 / 0.6 | 0.9 / 0.9 | 123 |

- **50k:** 후보 A에서 무릎 −2.333 vs 실기 −2.339, 무릎 τ 33.0 vs 32.5, 휠 τ −0.33 vs −0.32, 속도 −0.33 vs −0.40.
- **75k:** 실기 비교 구간이 조이스틱 조작 직후이고 접촉 여부도 불확실해 약한 검증이다. 무릎·토크는 맞지만 hip 벌어짐과 pitch는 덜 맞는다.
- **조이스틱:** 식별 모델은 실기의 "+0.14 m/s 명령 시 drift 상쇄"를 재현한다. nominal sim은 같은 명령에 +0.24 m/s로 달린다. 움직이는 동안의 pitch(3.6° vs 2.2°)와 휠 토크는 부분적으로만 맞는다.

## 해석과 DR 범위 제안

1. **다리 출력 부족 (sim 등가 배율 ≈ 0.6, 범위 0.55~0.65)**
   - 학습 DR(Kp/Kd 독립 ×0.8–1.2) 밖이고, 단독으로 −0.24 m/s drift를 만든다.
   - 40% 부족은 크다. 재학습 전에 다리 모터의 토크 상수, 기어비, 전류 제한, SDK 토크 단위 변환을 먼저 점검할 가치가 있다. 설정 오류라면 하드웨어 수정이 가장 직접적인 해결이다.
   - DR로 다룬다면 Kp·Kd를 같은 factor로 묶어 [0.5, 1.05]를 권한다. 관측에 직전 목표(last action)와 관절각이 모두 있으므로 정책이 PD 추종 오차로 다리 강도를 추론할 수 있다.
2. **다리 관절 Coulomb 마찰 ≈ 2 N m (2~6):** DR [0, 6] N m.
3. **휠 Coulomb 마찰 ≈ 0.3 N m (0.1~0.4):** DR [0, 0.4] N m, 좌우 독립.
   - Isaac Lab actuator `friction`/`dynamic_friction` 단위는 버전마다 달라 확인이 필요하다. 짧은 breakaway 시험으로 N m 단위인지 먼저 확인할 것.
4. **균형점 오프셋 (IMU +2° ≈ CoM −2 cm):**
   - 학습에는 이미 IMU 중력 bias ±0.05(±2.9°)와 CoM ±10 cm가 있다. 그런데도 메모리 없는 정책은 이를 상쇄하지 못한다(IMU +2°만으로 −0.18 m/s).
   - 그래서 DR을 넓혀서는 해결되지 않는다. 대신 다음을 검토한다.
     - 실기 IMU 장착 오프셋을 정적 수평 측정으로 확인한다(이 데이터로는 CoM과 구분 불가).
     - 정책 관측에 적분 정보를 넣는다.

## 다음 단계로 쓸 수 있는 산출물

후보 A/B/C 설정은 "실기 실패를 재현하는 sim2sim 수용 시험"으로 바로 쓸 수 있다. 재학습한 정책을 이 세 설정에서 zero-command로 돌린다. |v| ≤ 0.03 m/s 같은 기준을 실기 투입 전에 확인하면 된다.

## 한계

- fit은 자유 drift run 한 개(5초 구간)에 기반한다. seed 변화는 결과를 거의 바꾸지 않으므로 불확실성의 주원인은 실기 run 간 차이와 모델 구조다.
- 식별값은 MuJoCo 등가 파라미터다. 실제 원인(토크 상수, 전류 제한, 열 derate, 기어 마찰)을 구분하지 않는다.
- 허용폭은 손으로 정한 값이다.

## 재현 (VALIDATION_SIM)

```bash
PY=/home/cocel/venvs/cosim_ros2_jazzy/bin/python
$PY test/real2sim_leg_wheel_grid.py --stage grid --name grid_a \
  --leg-gain 1.0 0.9 0.8 0.7 0.65 0.6 0.55 0.5 --leg-friction 0 2 4 6 8 \
  --wheel-friction 0 0.1 0.2 0.3 0.4 --imu-pitch -1 0 1 2 3 --workers 12
$PY test/real2sim_leg_wheel_grid.py --stage grid --name grid_b \
  --leg-gain 0.55 0.6 0.65 0.7 --leg-friction 2 4 6 --wheel-friction 0.2 0.3 \
  --com -0.03 -0.02 -0.01 0 0.01 --imu-pitch 0 1 2 --workers 12
$PY test/real2sim_leg_wheel_grid.py --stage jobs --name validation \
  --jobs-file docs/exp/2026-10-17/real2sim_leg_wheel_grid/validation_jobs.json --workers 12
```

grid A 약 2분, grid B 약 45초, 검증 약 5초(12 workers).

## 변경·검사

- 신규 파일: [test/real2sim_leg_wheel_grid.py](../../../test/real2sim_leg_wheel_grid.py), 이 보고서, `real2sim_leg_wheel_grid/` 산출물(5.8 MB).
- 기존 하네스(`static_target_domain.py` 등)·제어 코드·학습 설정·정책은 수정하지 않았다.
- `./scripts/agent-check.sh` 결과는 [agent_check.log](real2sim_leg_wheel_grid/agent_check.log)에 있다.
