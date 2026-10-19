# FlashSAC A80k, 무릎만 PD 92/2.3 실기 run 분석 — 25 Hz 진동 감소, 그러나 잔존

Execution Domain:
- `ROBOT_READ_ONLY`: 로그 복사. SHA256은 원격과 로컬이 일치한다([copy_verification.log](flashsac_80000_125618_knee92_review/copy_verification.log)).
- `DESKTOP_DRY_RUN`: bag 분석.
- 로봇 명령, 배포, 설정 변경은 하지 않았다.
- 실기 주행(`ROBOT_STATE_CHANGING`)은 operator가 수행했다. 배포는 Codex가 했다([flashsac_80000_knee_pd_92_23.md](flashsac_80000_knee_pd_92_23.md)).

**대상 run:** `flashsac_80000_125618_839843723_output_true` (2026-10-18 12:56:18–12:58:16 KST).
- 흐름: RL 38.7 s → return_to_sit → sit → estop.
- RL 중 주행 비율은 37%였다. 최대 명령은 전진 1.0 m/s, yaw 1.0 rad/s였다.
- velocity bias는 OFF였다.

**정책·설정:**

| 항목 | SHA256 / 값 |
|---|---|
| Policy checkpoint | `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c` |
| ONNX | `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9` |
| config | `a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719` |
| bag db3 | `ad0ae57d0129e10da59f57626503d976f7555babcdb9a94450b68a13b54236af` |

**Evidence Status:**
- **PASS**: logged command에서 게인을 fit했다. hip·shoulder는 60.00/1.500, knee는 92.00/2.300, 휠 Kd는 0.500이다. 배포 config와 일치한다.
- **PASS (관측)**: 25 Hz period-2 limit cycle이 RL 중 계속 남아 있다. 진폭은 92/92/92보다 작다.
- **NOT_TESTED**: action 필터, 재학습.

## 1. 비교 (정지 hold 구간, 같은 정책)

"92"는 92/2.3, "60"은 60/1.5이다. 관절 순서는 hip/shoulder/knee다.

| 항목 (L/R) | 60/60/60 (10:59) | 92/92/92 (11:53) | **60/60/92 (12:56)** |
|---|---|---|---|
| hold 길이 | 32.5 s | 35.8 s | 20.0 s |
| action step RMS hip | 0.008 / 0.005 | 0.49 / 0.47 | **0.38 / 0.19** |
| shoulder | 0.030 / 0.035 | 0.15 / 0.22 | 0.05 / 0.27 |
| knee | 0.016 / 0.011 | 0.82 / 1.03 | **0.78 / 0.79** |
| 정책 갱신 토크 step hip [N m] | 0.1 | 11.3 / 10.8 | **5.8 / 2.9** |
| shoulder | 0.4–0.5 | 3.5 / 5.0 | 0.8 / 4.1 |
| knee | 0.2 | 18.8 / 23.6 | **17.9 / 18.2** |
| Δa lag-1 hip·knee | −0.5…−0.8 (미세 noise) | −1.00 | **−1.00** |
| action PSD 최고점 | 저주파 | 25 Hz | **25 Hz (다리 전 관절)** |
| 25 Hz 속도 진폭 hip [rad/s] | ≈ 0 | 0.73 / 0.84 | 0.54 / 0.48 |
| shoulder | ≈ 0 | 0.27 / 0.29 | 0.18 / 0.23 |
| knee | ≈ 0 | 0.61 / 0.71 | 0.49 / 0.45 |
| shoulder 토크 부호 반전 (갱신 순간) | 0 / 11% | 67 / 98% | 0 / **99%** |
| gyro step RMS roll/pitch/yaw [rad/s] | 0.017 / 0.026 / 0.010 | 0.148 / 0.037 / 0.081 | 0.054 / 0.043 / 0.065 |
| 진동 시작 / 지속 | 없음 | 진입 2.4 s / RL의 100% | 진입 0.9 s / RL의 100% |

**자세·drift (held neutral):**

| 항목 | 60/60/60 | 92/92/92 | **60/60/92** |
|---|---|---|---|
| pitch | 8.4° | 4.81° | **6.51 ± 0.51°** |
| FK 속도 [m/s] | −0.073 | −0.049 | **−0.045 ± 0.036** |
| 무릎 [rad] | −2.10 / −2.02 | −1.76 / −1.75 | −1.84 / −1.81 |
| hip [rad] | 약 ±0.08–0.10 | 0.06 / −0.05 | 0.10–0.11 / −0.09…−0.10 |

startup pitch peak는 8.8°였다. 휠은 startup에서 12 N m clip이 있었다.

## 2. 해석

- **진동이 줄어든 원인:** hip·shoulder 게인이 60으로 돌아가 hip 토크 step이 절반 이하가 됐다. 몸통 roll 진동(gyro)도 63% 줄었다. 사용자가 느낀 "훨씬 완화"와 맞다.
- **그러나 limit cycle은 남아 있다.**
  - 다리 전 관절이 RL 시간 내내 25 Hz로 교번한다(lag-1 −1.00).
  - 무릎 토크 step은 18 N m로 92/92/92 때와 거의 같다.
  - 오른쪽 shoulder는 갱신의 99%에서 토크 부호가 바뀐다. 소리의 유력 원인으로 본 조건이 그대로다.
  - 이번 run은 진입 0.9 s부터 시작했다.
- **자세 효과는 sim 예측보다 작다.** sim은 무릎만 올려도 pitch 4.7–5.1°라고 예측했지만 실기는 6.5°였다. hip이 더 벌어졌다(0.10 vs 0.06). 진동이 평균 자세에 영향을 줬을 가능성이 있다. drift는 92/92/92와 비슷하다.
- **결론:** 무릎 게인 ×1.53만으로도 25 Hz 루프 이득이 1을 넘는다. 게인 보상과 25 Hz 진동은 분리되지 않는다. 25 Hz 대책(다리 action 필터 등)이 따로 필요하다.

## 3. 학습 쪽 함의 (사용자 질문: 지금 학습 중인 C1/C2도 지금 셋으로?)

- **"지금 셋에 맞춘 학습"의 의미:** 배포 무릎 92/2.3은 실기 무릎을 sim nominal(60/1.5)처럼 만드는 배포 쪽 보상이다. 이에 맞는 학습은 sim 액추에이터를 nominal(기존 ±20% DR)로 두는 것이다. sim에 92/2.3을 넣으면 sim 무릎이 실기보다 약 1.5배 단단해져 다시 어긋난다.
- **C1/C2(sim 다리 6개 0.55–0.78, 배포 60/1.5)는 반대 방식이다.**
  - 지금 셋과 함께 쓰면 무릎이 이중 보상된다.
  - C1/C2는 hip도 약하게 학습한다. 그런데 hip 게인은 sim에서 자세에 영향이 없었고, 실기에서는 25 Hz 진동의 큰 몫이었다.
- **필터 없이 재학습하면 진동이 다시 나올 가능성이 높다.** 지금 셋에 맞춘 nominal 재학습만으로는 무릎 25 Hz 교번이 A80k처럼 남을 것으로 본다. 25 Hz 대책을 같이 넣어야 의미가 있다.

## 4. 파일

- **출력:** [`flashsac_80000_125618_knee92_review/`](flashsac_80000_125618_knee92_review/)
  - 복사한 bag, console, summary
  - `segments.json`·`signals.npz`·`segments.log`
  - `pd_vibration.json`·`pd_vibration_series.npz`·`pd_vibration.log`
- **스크립트:** 기존 [`analyze_rl_segments_pitch.py`](../../../test/sim2real/analyze_rl_segments_pitch.py)와 [`analyze_pd_vibration.py`](../../../test/sim2real/analyze_pd_vibration.py)(`77589ff2…`)를 수정 없이 사용했다.
- **interface:** 현재 local `flashsac_80000/config.json`(`a24c2137…`)이다. action 항은 이전과 같다.
- **`./scripts/agent-check.sh`:** [log](flashsac_80000_125618_knee92_review/agent_check.log).
