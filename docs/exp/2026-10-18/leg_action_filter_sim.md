# 다리 action 필터 sim 검증 — 현재 실기 셋(무릎만 92/2.3)

Execution Domain: `VALIDATION_SIM` (MuJoCo 500 Hz, native C++ state machine·observation·adapter bridge). 로봇 접근·배포·제품 코드 변경 없음.

| 항목 | 값 |
|---|---|
| Policy checkpoint SHA256 | `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c` (A80k) |
| ONNX SHA256 | `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9` |
| RL PD (hip/shoulder/knee) | 60/1.5 · 60/1.5 · 92/2.3, 휠 Kd 0.5 — 12:56 실기 config `a24c2137…`와 같다 |

**Evidence Status:**
- **PASS (sim)**: 다리 필터가 저주파 동작(정지·추종·회전·정지 재진입)을 해치지 않는다. 25 Hz proxy 교번은 제거한다.
- **NOT_TESTED**: 실기. 이 sim은 실기 25 Hz 진동 자체를 재현하지 못한다([pd92 분석](flashsac_80000_115354_pd92_review.md) 3절).

## 1. 설정

**필터 종류:** 50 Hz 정책 갱신마다 계산하고, 그 사이는 유지한다. 정책 관측의 `last_action`은 필터 전 원래 출력이다.

| 필터 | 정의 | 25 Hz 이득 | 비고 |
|---|---|---|---|
| `ma2_legs` | 다리 6개 action = (a[k] + a[k−1]) / 2 | 0 | DC 이득 1, 10 ms 지연 |
| `ma2_all` | 휠까지 같은 2-tap 평균 | 0 | |
| `ema0.5_legs` | 0.5·a[k] + 0.5·이전 출력 | 1/3 | |

RL 첫 tick의 필터 상태는 첫 action이다. 그래서 0에서 반걸음 튀는 일이 없다.

**물리 (다리 출력 계수 hip/shoulder/knee):**
- `1/1/0.65`: 의도한 운용점. 무릎 92 × 0.65 ≈ nominal 60이지만, 물리 무릎 토크 상한은 39 N m다.
- `1/1/0.55`, `1/1/0.78`: 무릎 계수 범위.
- `1/1/1`: 부족분이 없는 경우. 무릎이 1.53배 과보상된다.
- `0.65/0.65/0.65`: 다리 전체에 정적 계수를 적용한 경우.
- 마찰: 기본은 없음이다. 이전 grid의 fitted 마찰(다리 2, 휠 0.3 N m)은 의도한 운용점에서만 스트레스 조건으로 넣었다.
  - fitted 마찰은 nominal 물리(60/1.5, k = 1)에서도 정지 |v|를 0.02에서 0.1–0.34 m/s로 망가뜨린다.
  - 실기 A80k는 정지 drift가 −0.045 m/s로 잘 선다. 따라서 이 마찰값은 A80k에 맞지 않는 모델로 본다.
- 추가 토크 지연: 0 / 4 / 8 / 12 ms.

**시나리오:**
- stand 25 s.
- drive 60 s: 0 → +0.6 m/s → 0 → −0.6 → 0 → yaw +1.0 → 0 → yaw −1.0 → 0. native 0.5/s ramp를 쓴다.
- 진입 후 8 s는 sim의 일어서기 과도 구간이라 따로 기록했다.

**규모:** Part A 192 job, Part B 72 job. seed는 42다.

**출력:**
- [Part A 표](leg_action_filter_sim/part_a_tables.log), [Part B 표](leg_action_filter_sim/part_b_tables.log)
- `results.json`·`manifest.json`(각 폴더)
- [재현 확인](leg_action_filter_sim/regression_check.log): 최종 스크립트가 저장된 4개 job을 그대로 재현한다.

## 2. Part A — 저주파 안전성

의도한 운용점 `1/1/0.65`, 마찰 없음이다. 칸은 지연 0 / 4 / 8 / 12 ms 순이다.

| 필터 | 정지 pitch·속도 (8 s 이후) | pitch std | startup pitch peak [°] | 주행 후 정지 \|v\| | vx 오차 (+0.6 / −0.6) | yaw 오차 (+1 / −1) | 넘어짐 |
|---|---|---|---|---|---|---|---|
| 없음 | 5.1°, −0.005 m/s | 0.01 / 0.01 / 0.01 / **0.58** (12 ms에서 3.5 Hz 흔들림) | 7.3 / 7.3 / 8.0 / 9.2 | 0.02 | +0.08 / 0.00 | −0.14 / +0.03 | 0 |
| **ma2_legs** | 5.1°, −0.005 | **0.01 (전부)** | 7.4 / 7.9 / 8.7 / 10.3 | 0.02 | +0.08 / 0.00 | −0.14 / +0.03 | 0 |
| ema0.5_legs | 5.1°, −0.004 | 0.01 (전부) | 7.8 / 8.5 / 9.4 / 10.9 | 0.02 | 같음 | 같음 | 0 |
| ma2_all | 5.1°, −0.005 | 0.59 (12 ms) | 8.6 / 9.3 / 10.8 / 12.6 | 0.02–0.03, 12 ms에서 휠 clip 3.6% | 같음 | 같음 | 0 |

**다른 물리 조건:**
- **무릎 k 0.55:**
  - 필터 없음: 지연 8–12 ms에서 2.7–3.1 Hz 흔들림이 생긴다(pitch std 2.5–2.9°).
  - `ma2_legs`·`ema0.5_legs`: 흔들림이 없다(0.01).
  - 주행 후 정지 0.12 m/s는 필터와 무관하다. 무릎이 약해서 생기는 drift다.
- **무릎 k 0.78, 다리 전체 0.65:** 모든 필터가 필터 없음과 같다. 정지는 0.06–0.07 m/s다.
- **무릎 k 1.0 (과보상):** 필터와 무관하게 +0.17–0.23 m/s 전진 drift가 생긴다.
- **fitted 마찰 (스트레스):** 모든 경우 정지 0.24 m/s다. 필터와 무관하다.

**넘어짐 집계 (각 48 job):** 없음 0, `ma2_legs` 0, `ema0.5_legs` 0, `ma2_all` 1(무릎 k 0.55 + 지연 12 ms 주행).

**Part A 결론:**
- `ma2_legs`는 정지 자세·속도·추종·회전을 바꾸지 않는다.
- 지연이 크거나 무릎이 약할 때 생기는 2.7–3.5 Hz 흔들림은 오히려 없앤다.
- 비용은 startup pitch peak +0.1…+1.1°다(지연이 클수록 크다).
- 휠까지 거는 `ma2_all`은 휠 clip이 늘고 넘어짐이 생겨 쓰지 않는다.

## 3. Part B — 25 Hz 대리 시험

**방법:**
- 물리는 `1/1/0.65`, 마찰 없음, stand 조건이다.
- 실기의 고주파 과반응을 `a + g(a − a_prev)`로 흉내 냈다. DC 이득은 1이고 25 Hz 이득은 1 + 2g다. 하드웨어 모델이 아니다.

**대표 결과:** 필터 없음 vs `ma2_legs`. knee step은 정책 갱신 순간의 무릎 토크 step이다.

| 게인 셋, g, 지연 | 필터 없음 | ma2_legs |
|---|---|---|
| 무릎만 92, g 1, 0 ms | 2.7 Hz 흔들림 (pitch std 2.7°) | 조용 (0.01°) |
| 무릎만 92, g 1.5, 0 ms | **25 Hz 교번** (lag-1 −0.85/−0.70, knee step 48 N m, pitch std 8.9°) | **25 Hz 성분 0** (lag-1 +0.79, knee step 1.2 N m), 2.7 Hz 1.6° |
| 무릎만 92, g 1.5, 4 ms | 넘어짐 (1.0 s) | 2.7 Hz 흔들림 4.2° |
| 무릎만 92, g 2 | 넘어짐 (0·4 ms) | 2.3 Hz 흔들림 7.4–7.6° |
| 92 전체, g 1, 0 ms | **25 Hz 교번** (lag-1 −0.88/−0.78, knee step 45 N m) | 조용 (0.12°) |
| 92 전체, g 1.5, 0 ms | 25 Hz 교번 (knee step 56 N m) | 2.7 Hz 흔들림 3.0° |
| 모든 셋, g 3 | 넘어짐 | 넘어짐 |

**순서 재현:** 92 전체가 무릎만 92보다 낮은 g에서 먼저 교번한다. 실기 순서와 같다.

**필터 효과:**
- 필터가 없을 때 25 Hz 교번이 생긴 **모든 경우에서 `ma2_legs`가 25 Hz 성분을 0으로 만들었다**(적용 action의 25 Hz 진폭 ≤ 0.002).
- 과반응을 더 키우면 불안정이 2–3 Hz 흔들림으로 옮겨간다. 필터가 없으면 같은 조건에서 넘어지거나 강하게 교번한다.

**Proxy 한계:**
- g는 2.7 Hz에서도 이득을 약 +20% 올리고 위상을 앞당긴다.
- 무릎 k 0.65 물리의 60/60/60은 g = 0에서도 2.7 Hz로 흔들린다(실기 60/1.5는 조용했다).
- 그래서 이 proxy의 저주파 결과는 비관적이라고 본다.

**해석:** 실기 무릎만 92는 "중간 정도" 교번(knee step 18 N m)이다. 문턱 근처로 본다. proxy 기준으로는 `ma2_legs`가 25 Hz 교번을 없애고, 남더라도 작은 2–3 Hz 흔들림 정도일 것으로 예상한다.

## 4. 권고

1. **후보:** `ma2_legs`.
   - 다리 6개 action만 2-tap 평균하고 휠은 그대로 둔다.
   - RL 첫 tick은 첫 action으로 초기화한다.
   - `last_action` 관측은 원래 출력을 쓴다.
2. **구현 (다음 단계):**
   - `tita_node` ActionAdapter 입력에 필터를 넣고 config 옵션으로 둔다(기본 OFF).
   - sim2sim adapter에도 같은 옵션을 넣고 C++–Python parity를 검사한다.
   - 실기 배포는 operator 승인 사항이다. 배포 경로는 Codex가 관리하므로 조율이 필요하다.
3. **실기 시험 감시 항목 (승인 후):**
   - 25 Hz 지표: 정지 중 다리 |Δa| RMS, lag-1, 무릎 토크 step. 0에 가까워야 한다.
   - 2–3 Hz pitch 흔들림: pitch std > 약 1°이거나 앞뒤 흔들림이 보이면 즉시 return_to_sit.
   - startup pitch peak: 지금 8.8°, sim 기준 +1° 안팎 증가가 예상된다.

## 5. 한계

- 이 sim은 실기 25 Hz 진동을 재현하지 못한다. Part B는 대리 시험일 뿐이다.
- 하드웨어 지연·compliance·backlash는 측정되지 않았다.
- seed 1개, 평지만 다뤘다.
- 진입 직후 sim의 일어서기 과도(물리에 따라 0.2–0.4 m/s로 굴러감)는 실기와 다를 수 있다.

## 6. 파일

- **신규 test 스크립트:** [`test/sim2real/sim_leg_action_filter.py`](../../../test/sim2real/sim_leg_action_filter.py) (`44b64193…`).
  - 결과는 `75a11b90…`로 만들었다. 그 뒤 표 출력과 `--tables-only`만 추가했고, 재현 확인을 마쳤다.
  - `validate_sit_transitions.py`(`f843256c…`)·`sim_pd_gain_latency_chatter.py`(`bb74c017…`)는 import만 했다.
- **출력:** [`leg_action_filter_sim/`](leg_action_filter_sim/)
- **수정하지 않은 것:** 제품 코드, 배포 파일, 학습 task(C1/C2 학습 중)는 수정하지 않았다.
- **`./scripts/agent-check.sh`:** [log](leg_action_filter_sim/agent_check.log).
