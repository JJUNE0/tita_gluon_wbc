# C2_60k 실기 첫 run (legs 60/1.5) — 정지 명령에서 뒤로 −0.4 m/s

Execution Domain:
- `ROBOT_READ_ONLY`: 로그 복사. 이번 run과 그 ROS 로그만 복사했고 SHA256이 일치한다([copy_verification.log](flashsac_c2_60000_164307_review/copy_verification.log)).
- `DESKTOP_DRY_RUN`: 분석.
- 실기 주행(`ROBOT_STATE_CHANGING`)은 operator가 수행했다.

**대상 run:** `flashsac_c2_60000_164307_516750545_output_true` (2026-10-18 16:43). RL 34.6 s, 주행 비율 49%(전진 최대 1.0 m/s, yaw 0.56).

| 항목 | 값 |
|---|---|
| bundle | `flashsac_c2_60000` |
| Policy checkpoint SHA256 | `b4c8ae072787c3119864e75c2ebfbaf8284a02976dc68f1f282ad9480ae2e116` |
| ONNX SHA256 | `b12e40267bb3247762b0dd6283bd9f9cafffac52597ca74b387790bb4e925b7f` |
| config SHA256 | `9561fd1a…` |
| 설정 | 필터 none, velocity bias OFF |

**Evidence Status:**
- **FAIL (정지 성능):** zero-command drift가 −0.35 ~ −0.50 m/s다.
- **PASS:** 게인 fit 60.00/1.500, 휠 0.500으로 배포 config와 일치한다.

## 관측

- **정지 drift:** 명령을 0으로 되돌릴 때마다 약 1.5 s 안에 같은 상태로 들어간다. thigh 1.19–1.26 rad, pitch −3.8…−4.3°, FK 속도 −0.40…−0.50 m/s로 계속 후진한다.
  - 진입 후 10 s 이후 정지 구간 평균은 −0.352 m/s다(638 sample).
  - 휠 command 토크는 −0.4 N m 정도로 작다.
  - 진입 직후 3–4 s만 thigh 1.0–1.05, pitch +1.5°, v ≈ 0이었다.
- **thigh 자세는 정책이 고른 것이다.** thigh는 목표를 0.01 rad 이내로 따라간다(토크 −0.2/+0.7 N m). 따라서 관절이 못 따라간 결과가 아니다.
  - 무릎은 목표 −1.66/−1.69, 실제 −2.16이다. 0.48 rad 오차로 28–30 N m를 낸다. C2가 학습한 "약한 다리" 방식 그대로다.
- **sim과 비교:**

  | 항목 | sim k 0.55/0.65 | 실기 |
  |---|---|---|
  | thigh | 1.05–1.09 | 1.19–1.26 (+0.13–0.17 rad 더 굽힘) |
  | knee | −2.16 | −2.16 (같음) |
  | pitch | 1.2–1.6° | 약 −4° |
  | 정지 drift | ±0.005 m/s | −0.4 m/s |

  sim의 "무릎만 약함" 예측(+0.11)과도 방향이 반대다. 실기는 어느 sim 물리 조건에도 맞지 않는다.
- **진동:** A80k 무릎 92보다 훨씬 작다.

  | 항목 | C2 | A80k 무릎 92 |
  |---|---|---|
  | 무릎 action step RMS | 0.24 | 0.78 |
  | 무릎 토크 step | 3.6 N m | 18 N m |
  | hip 토크 step | 0.8–1.2 N m | 3–6 N m |
  | thigh 토크 부호 반전 | 3–12% | 99% |

  다만 action PSD 최고점은 여러 관절에서 아직 25 Hz다.
- **startup pitch peak:** 5.0°다.

## 해석과 한계

- C2_60k(60/1.5)는 실기에서 정지 drift 요구를 크게 벗어나므로 이 상태로는 쓸 수 없다.
- 25 Hz 진동은 A80k 무릎 92보다 크게 줄었다.
- 후진 원인은 미확정이다. 후보는 다음과 같다.
  1. 실기 thigh·pitch 평형이 sim 다리 계수 모델과 다르다. 예: shoulder·hip은 nominal이고 무릎만 약하다.
  2. A80k와 R0에서도 보인 실기 고유의 후진 편향(wheel/CoM 쪽)이 C2에서 크게 나타났다.
  3. C2 보상(정지 자세·속도 penalty)이 실기 관측 분포에서 다른 평형을 만들었다.
- 실기 run 1회 결과다. 원인 분리에는 sim 재현 시도가 필요하다. 예: thigh가 1.24에서 평형을 이루는 물리 조건 탐색.

## 파일

- **출력:** [`flashsac_c2_60000_164307_review/`](flashsac_c2_60000_164307_review/) — bag, console, summary, ROS 로그, `segments.*`, `pd_vibration.*`.
- **스크립트:** `analyze_rl_segments_pitch.py`, `analyze_pd_vibration.py`를 수정 없이 사용했다.
- **`./scripts/agent-check.sh`:** [log](flashsac_c2_60000_164307_review/agent_check.log).
