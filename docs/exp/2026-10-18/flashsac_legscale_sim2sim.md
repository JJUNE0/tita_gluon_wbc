# C1/C2 (다리 출력 스케일 학습) sim2sim 1차 평가 — checkpoint 40k–75k

Execution Domain: `VALIDATION_SIM` (평가 전용 export + 200 Hz sim2sim 수용시험). 로봇 접근·배포 없음.

**Evidence Status:**
- **PASS**: export 10개, 평가 480 rollout 실행. 모두 끝까지 돌았다.
- **NOT_TESTED**: 실기, 500 Hz native 경로, 무릎만 약한 물리, 25 Hz 진동(sim에서 재현 불가).

**학습 상태:** C1/C2는 15:27 systemd-oomd 종료로 77.7k/76.9k에서 멈췄다([학습 기록](flashsac_legscale_training.md) 중단 절). 평가 대상은 저장된 checkpoint 40k·50k·60k·70k·75k다.

## 1. 방법

- **export:** [`test/export_ab_checkpoints.py`](../../../test/export_ab_checkpoints.py)에 C1/C2를 추가했다(`2ed020a4…`).
  - `policy_interface.json`·`action_mapping.json`이 115632와 바이트 단위로 같고 ddt.json이 33/8을 보고한 것을 확인한 뒤에만 export했다.
  - parity 최대 오차는 ≤ 3.5e-6이다. `export.py` SHA256은 변하지 않았다([log](flashsac_legscale_sim2sim/export.log)).
- **배포 config:** 60/1.5다. C1/C2는 학습 쪽 보상이라 배포 쪽 보상은 넣지 않는다.
- **평가 스크립트:** [`test/evaluate_legscale_policies.py`](../../../test/evaluate_legscale_policies.py)(`7f2ffe7c…`). 프로토콜은 실행 전에 고정했다([evaluation_protocol.json](flashsac_legscale_sim2sim/evaluation_protocol.json)).
- **물리 세트 `cscale`:** acceptance suite(`10872182…`)에 추가했다.
  - nominal k = 1(회귀)
  - k 0.55 / 0.65 / 0.75: 다리 전체, startup 포함
  - k 0.65 + 마찰(다리 2, 휠 0.3 N m): 스트레스 조건, 선정에서 제외
- **시나리오·gate:** 기존 수용시험과 같다.
  - 시나리오: zero 30 s × 2 seed, 전후진 0.3/0.6, yaw ±0.5
  - gate: zero |v| ≤ 0.03, 변위 ≤ 0.75 m, pitch std ≤ 1°, startup pitch ≤ 10°, 추종 0.05/0.10, 정지 ≤ 0.05, yaw 0.05, 휠 clip ≤ 1%
- **선정:** nominal + k 0.55/0.65/0.75에서 통과한 gate 수(최대 112)로 정한다. 동점이면 k 불일치 조건의 평균 |zero v|가 작은 쪽, 그다음 늦은 step이다.
- **기준선:** R0(115632/60k), A80k(201940/80k, 60/1.5 기준). 200 Hz harness는 관절별 게인을 지원하지 않아 A80k의 무릎 92 배포는 재현하지 않았다.

**실행 이력:**
- 1차 시도는 worker 10개로 띄웠다가 15:27 oomd 종료로 중단됐다([log](flashsac_legscale_sim2sim/cscale_eval_oom_killed_attempt1.log)).
- 2차 시도는 작업 디렉터리를 `test/`로 잡아 상대 정책 경로 오류가 났다([log](flashsac_legscale_sim2sim/cscale_eval_attempt2_cwd_error.log)).
- 최종 실행은 별도 systemd user unit(`MemoryMax=16G`), worker 8개, repo root에서 했다([log](flashsac_legscale_sim2sim/cscale_eval.log)).

## 2. 결과

| policy | gate (/112) | 스트레스 gate | 평균 \|zero v\| (k 불일치) | k 0.65 정지 자세 hip / thigh / knee, pitch | rollout 실패 |
|---|---|---|---|---|---|
| R0_60k | 56 | 10 | 0.190 | 0.01 / 1.03–1.07 / −2.21…−2.23, 4.1° | k0.55 후진 2 |
| A_80k (60/1.5) | 69 | 18 | 0.038 | 0 / 0.85–0.88 / −2.02, 9.5° | k0.55 후진 2·yaw 1 |
| C1_40k | 57 | 15 | 0.067 | 0 / 0.93 / −2.05, 5.9° | 0 |
| C1_50k | 70 | 19 | 0.046 | 0 / 0.97–0.98 / −2.03, 2.8° | 0 |
| **C1_60k** | **83** | 24 | 0.024 | 0 / 0.97–0.98 / −2.03, 3.0° | 0 |
| C1_70k | 77 | 21 | 0.023 | 0 / 0.95–0.96 / −2.04, 4.3° | 0 |
| C1_75k | 63 | 22 | 0.061 | 0 / 0.98–1.0 / −2.03, 2.0° | 0 |
| C2_40k | 78 | 13 | 0.027 | 0 / 1.07–1.10 / −2.17, 1.0° | 0 |
| C2_50k | 63 | 20 | 0.067 | 0 / 1.04–1.08 / −2.16, 2.1° | 0 |
| **C2_60k** | **81** | 12 | **0.011** | 0 / 1.05–1.09 / −2.16, 1.6° | 0 |
| C2_70k | 69 | 18 | 0.046 | 0 / 1.05–1.08 / −2.16, 2.0° | 0 |
| C2_75k | 59 | 12 | 0.077 | 0 / 1.10–1.11 / −2.16, −0.2° | 0 |

회사 stand는 hip 0, thigh 1.09, knee −2.16, pitch 1.4°다.

**선정 checkpoint별 물리 조건 분해:** [전체 분해](flashsac_legscale_sim2sim/cscale_breakdown.log).

| | nominal (k = 1) | k 0.55 | k 0.65 | k 0.75 | k 0.65 + 마찰 |
|---|---|---|---|---|---|
| **C1_60k** gate | 13/28 | 19/28 | 24/28 | 27/28 | 24/28 |
| zero v / pitch std | **+0.202** / 0.10 | +0.033 / 2.09 | −0.021 / **1.51** | −0.018 / 0.82 | +0.008 / 2.48 |
| 0.6 추종 오차 (전진 / 후진) | +0.15 / +0.07 | +0.02 / +0.04 | −0.07 / −0.01 | −0.07 / +0.01 | −0.08 / +0.04 |
| **C2_60k** gate | 12/28 | 25/28 | 22/28 | 22/28 | 12/28 |
| zero v / pitch std | **+0.251** / 0.12 | −0.003 / 0.99 | −0.005 / 0.78 | +0.023 / 0.53 | −0.036 / 2.28 |
| 0.6 추종 오차 (전진 / 후진) | +0.19 / +0.24 | 0.00 / **−0.21** | +0.05 / **−0.23** | +0.03 / −0.13 | +0.01 / −0.27 |
| yaw +0.5 오차 | −0.10 | −0.03 | −0.14 | −0.13 | −0.08 |

## 3. 해석

- **C1/C2 모두 k 0.55–0.75에서 R0·A80k보다 낫다.**
  - gate는 81–83/112로, R0 56, A80k 69보다 많다.
  - rollout 실패가 0이다. R0·A80k는 k 0.55 후진에서 넘어졌다.
  - 학습 쪽 보상은 sim에서 의도대로 작동한다.
- **C2_60k는 정지 성능이 가장 좋다.**
  - k 0.55/0.65에서 |zero v| ≤ 0.005 m/s, pitch 1.2–1.6°다.
  - 정지 자세가 회사 stand와 거의 같다(thigh 1.05–1.09, knee −2.16, hip 0).
  - 대신 **후진 추종이 약하다**(−0.6 명령에 −0.37–0.47 m/s). yaw 추종도 약하다(+0.5 명령에 +0.36–0.37).
- **C1_60k는 추종이 낫다.** 그러나 k 0.65에서 pitch std 1.51°로 정지 중 흔들림 gate를 실패했다.
- **둘 다 nominal(k = 1)에서 +0.20–0.25 m/s 전진 drift가 생긴다.**
  - 실기 다리가 약하지 않거나, 오늘 데이터처럼 무릎만 약하고 hip·shoulder가 정상이면 과보상 drift가 날 수 있다.
  - 실기 후보로 보기 전에 500 Hz native harness에서 무릎만 약한 물리(1/1/0.65)로 확인이 필요하다.
- **checkpoint별 차이:**
  - 75k가 60–70k보다 나쁘다(C1 63, C2 59). 학습 곡선이 단조롭지 않다.
  - 학습 중단으로 75k 이후는 없다.
- **이 평가로 판단할 수 없는 것:** 실기 25 Hz 진동 위험. C1/C2는 hip도 약하게 학습했다. 별도 실기 감시가 필요하다.

## 3a. 500 Hz native 후보 비교와 25 Hz 여유 (추가, 학습은 operator 결정으로 정지 유지)

**조건:** `VALIDATION_SIM`, [`sim_leg_action_filter.py`](../../../test/sim2real/sim_leg_action_filter.py) part c/d(`e3350bb8…`).
- 기존 part a/b 결과를 그대로 재현한다([regression](leg_action_filter_sim/regression_check.log)).
- 결과: [part c](leg_action_filter_sim/part_c.log), [part d](leg_action_filter_sim/part_d.log).
- 필터 없음, 마찰 없음(part d는 다리 마찰 2 N m 조건 포함), seed 42다.
- 물리는 무릎만 약함 `1/1/0.65`, 전체 약함 `0.65`, 약함 없음 `1/1/1` 세 가지다.

**실기가 어느 물리에 가까운가:**
- 실기 A80k 무릎 92는 pitch 6.5°, drift −0.045였다.
- sim에서 `1/1/0.65`는 5.1°, −0.005이고 `0.65`는 4.6°, −0.079다. 실기는 이 둘 사이다.
- `1/1/1`이면 +0.17 m/s 전진 drift가 나와야 하는데, 실기에서는 나오지 않았다. 따라서 실기는 nominal이 아니다.

**두 그럴듯한 물리에서의 정지·추종 (지연 0/4 ms):**

| 배포 조합 | pitch | 정지 drift | pitch std | 주행 후 정지 | vx 오차 +0.6 / −0.6 |
|---|---|---|---|---|---|
| A80k + 무릎 92 | 4.6–5.1° | −0.079 … −0.005 | 0.01 | 0.02–0.07 | +0.03…+0.08 / 0…−0.04 |
| C1_60k + 60/1.5 | 3.0–3.8° | −0.019 … +0.024 | 1.26–1.55 | 0.02 | −0.07…−0.05 / −0.01…+0.03 |
| C2_60k + 60/1.5 | 1.7–3.1° | −0.004 … **+0.112** | 0.70–0.89 | 0.04–0.06 | +0.04…+0.11 / **−0.17…−0.23** |
| C + 무릎 92 | — | +0.16…+0.25 | — | 0.13–0.23 | 이중 보상이라 쓰지 않는다 |
| C + hip·shoulder 39 | — | 물리에 따라 −0.16…+0.05 | — | — | 민감해서 쓰지 않는다 |

**25 Hz 대리 문턱 g (part d):** 25 Hz 교번이 처음 생기는 g다. 클수록 여유가 크다.

| 배포 조합 | 무릎만 약함 | 전체 0.65 |
|---|---|---|
| A80k + 60/1.5 (실기 조용) | 1.5 | > 1.5 |
| A80k + 무릎 92 (실기 교번) | 1.5 | 1.0 |
| C2_60k + 60/1.5 | 1.0 | 1.0 |
| C1_60k + 60/1.5 | **0.5** | 1.0 |

- 실기 순서(60/1.5 조용, 무릎 92 교번)는 전체 0.65 물리에서 재현된다. 실기 과반응은 g ≈ 1–1.5 사이로 본다.
- 그렇다면 C1·C2(60/1.5)도 실기에서 25 Hz 교번이 생길 가능성이 높다. C1이 가장 취약하다.
- 다리 마찰을 넣어도 C1/C2의 느린 pitch 흔들림(1.4–2.1°)은 줄지 않았다. A80k 60/1.5의 sim 흔들림은 마찰로 사라졌다.

**sim2real 다음 시험 권고:**

| 순서 | checkpoint | 배포 PD (hip·shoulder / knee / 휠 Kd) | 이유와 위험 |
|---|---|---|---|
| 1 | **C2_60k** (`b4c8ae07…`, ONNX `b12e4026…`) | **60/1.5 / 60/1.5 / 0.5** (설계값, 무릎 보상 없음) | 정지 자세가 회사 stand와 같고(pitch 1.7–3.1°), 약한 다리 물리에서 drift가 가장 작다. 위험은 세 가지다: 25 Hz 교번이 지금 셋과 비슷하게 생길 수 있다, 무릎만 약하면 +0.11 m/s 전진 drift가 날 수 있다, 후진·yaw 추종이 약하다(−0.6 명령에 약 −0.4). |
| 기준 | A80k | 60/1.5 / 92/2.3 / 0.5 (지금 셋) | 실기에서 확인된 기준선이다: pitch 6.5°, drift −0.045, 25 Hz 교번이 남아 있다. |
| 비권고 | C1_60k | 60/1.5 | 25 Hz 여유가 가장 작다(g 0.5). 느린 pitch 흔들림도 있다. |
| 비권고 | C + 무릎 92, 92 전체 | | 이중 보상 drift가 생기거나 25 Hz 교번이 심해진다. |

**C2_60k를 실기에 올리려면 두 가지가 필요하다.**
- 배포 bundle을 만들려면 `export.py`의 task guard를 바꾸거나 평가 export를 bundle로 옮겨야 한다. 둘 다 operator 승인 사항이고, Codex 배포 절차를 따른다.
- 25 Hz 교번이 나오면 즉시 return_to_sit한다. 이후 다리 action 필터 구현(기본 OFF)을 진행한다.

## 4. 다음 단계 (제안)

1. **500 Hz native harness 확인:** C1_60k·C2_60k (+C1_70k, C2_40k)를 물리 1/1/0.65(무릎만 약함), 0.65 전체, 1/1/1에서 돌린다. 지연 0/4 ms, stand·drive 조건이다.
2. **학습 재개 여부:** operator 결정 사항이다. replay buffer 없이 75k에서 이어가거나, 오늘 결과(무릎만 보상, action 필터)를 반영해 새로 설계한다.

## 5. 파일

- **출력:** [`flashsac_legscale_sim2sim/`](flashsac_legscale_sim2sim/)
  - `exports/`(ONNX·config·parity)
  - `cscale_metrics.json`·`cscale_summary.json`·`cscale_rollouts_results.json`
  - `cscale_breakdown.log`
  - rollout 신호는 scratch에 두었다(대용량).
- **test 변경:**
  - `export_ab_checkpoints.py`: C1/C2 RUNS 추가
  - `flashsac_acceptance_suite.py`: `cscale` 세트 추가. 기존 세트는 그대로다.
  - `evaluate_legscale_policies.py`: 신규
- **`./scripts/agent-check.sh`:** [log](flashsac_legscale_sim2sim/agent_check.log).
