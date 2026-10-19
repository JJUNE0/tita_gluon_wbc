# 2026-10-18 실기 run 종합 vs 학습 설정 — 다음 학습 결론

Execution Domain: `DESKTOP_DRY_RUN`. 이미 복사된 실기 로그와 기존 리뷰(Claude·Codex)를 다시 분석했다. 로봇 접근 없음.

**대상:** 오늘 실기 7개 run.
- A80k checkpoint `79f9175b…`(ONNX `26f0d86b…`) 6개
- C2_60k `b4c8ae07…`(ONNX `b12e4026…`) 1개

**Evidence Status:**
- **PASS**: 수치 집계. 각 run의 bag·SHA는 개별 리뷰에 있다.
- **SUSPICIOUS**: 원인 해석. 50 Hz 로그, FK 속도 추정(외부 위치 측정 없음), 운전 명령이 run마다 다르다.

## 1. 실기 run 요약 (정지 hold 구간)

| run | 정책·PD (hip·shoulder/knee) | 필터·bias | 정지 drift [m/s] | pitch [°] | 무릎 [rad] | 진동 | 출처 |
|---|---|---|---|---|---|---|---|
| 10:59 | A80k 60/60 | 없음 | −0.073 / −0.115 | 8.4 / 8.1 | −2.10, −2.02 | 조용 | [리뷰](flashsac_80000_105921_claude_review.md) |
| 11:53 | A80k 92/92 | 없음 | −0.049 | 4.8 | −1.76 | **25 Hz 강함**(knee step 19–24 N m) | [리뷰](flashsac_80000_115354_pd92_review.md) |
| 12:56 | A80k 60/92 | 없음 | −0.045 | 6.5 | −1.84 | 25 Hz 남음(knee step 18 N m) | [리뷰](flashsac_80000_125618_knee92_review.md) |
| 12:59 | A80k 60/92 | bias ON | −0.030 … −0.046 | 6.6–7.2 | — | — | [Codex](flashsac_knee92_bias_pair.md). bias −0.8 N m 상한 88% 포화, drift 유지 |
| 13:59 | A80k 60/92 | MA2 | −0.049 → +0.04 (구간별), 전체 +0.027±0.068 | 5.8 → 7.1 (std 0.34–0.63) | −1.81 | 25 Hz 소멸(hip 0.52→0.001 rad/s), **8–9 Hz 앞뒤 흔들림** | [Codex](leg_action_filter_real_review.md), 이 폴더 |
| 15:03 | A80k 60/92 | MA2 + notch 8.3 Hz | −0.018 ± 0.038 | 5.5 (std 0.29) | −1.82 | knee step 0.6 N m, **7–8 Hz 흔들림 남음** | [Codex](leg_notch_real_review.md), 이 폴더 |
| 16:43 | C2_60k 60/60 | 없음 | **−0.35 ~ −0.50** | **−3.9** | −2.16 (thigh 1.24) | knee step 3.6 N m | [리뷰](flashsac_c2_60000_164307_review.md) |

- **13:59 MA2 run:** return_to_sit 중 pitch 37°로 fall guard가 걸렸다. RL 중이 아니라 sit 전환 중이었다(Codex 리뷰).
- **운영자 체감:** 문제는 빠른 다리 떨림보다 몸통 앞뒤 흔들림이었다(Codex 리뷰).

## 2. 학습 가정 vs 실기 증거

A80k의 학습 task는 `…-BaseComShift-v0`다. 원래 My task에서 base CoM x만 U(−5.5, −1.5) cm로 바꿨다.

| 학습 가정 (A) | 실기 증거 | 판정 |
|---|---|---|
| 다리 출력 계수 1.0 (Kp 60/1.5 ±20%) | 같은 자세의 무릎 토크 비율(URDF/실기)이 0.64–0.73이다(회사 LQR, R0, A80k). 무릎은 60에서 −2.10(sim nominal −1.85), 92에서 −1.82다 | **무릎은 실기가 약 0.65배 약하다.** 무릎 92(×1.53) 배포로 자세가 nominal 쪽으로 돌아왔다 |
| hip·shoulder 출력 계수 1.0 | C2(다리 6개 모두 0.55–0.78로 학습)가 실기에서 thigh 1.24, pitch −4°, −0.4 m/s로 후진했다. hip 게인 상승(92)은 25 Hz를 키웠다 | 다리 전체 약화 학습은 틀렸다. **hip·shoulder는 nominal 유지**가 맞다(간접 근거) |
| base CoM 뒤 3.5 cm | 회사 정지 자세에서 URDF CoM이 바퀴 접점과 1 cm 이내다 | **틀린 가정.** URDF 중심으로 되돌린다 |
| 강체 관절, 목표 지연 0–20 ms, 필터 없음 | 게인을 올리면 25 Hz period-2가 생긴다. MA2(+10 ms)는 25 Hz를 없앴지만 8–9 Hz를 만들었다. notch를 더해도 7–8 Hz가 남았다. 어느 것도 MuJoCo에서 재현되지 않았다 | 실기 고주파 루프 여유가 sim보다 작다. **배포에만 넣은 필터는 진동 주파수를 옮길 뿐이다.** 정책이 필터 지연을 모른 채 돌기 때문이다 |
| 위치 관측 없음(GT drift 보상만) | 모든 A80k 변형(게인·필터·bias)에서 정지 drift가 −0.07…+0.04 m/s로 남았다. bias −0.8 N m는 포화돼도 제거하지 못했다 | 배포 쪽 보정은 한계다. **정책이 위치를 보고 적분 동작을 해야 한다**(회사 LQR은 위치 되먹임으로 60 s에 −1.9 cm) |
| 관절 마찰 0 | grid fitted 휠 마찰 0.3 N m를 넣으면 nominal 정책도 sim에서 정지를 못 한다. 실기 A80k는 선다 | 큰 휠 마찰 DR은 근거 없음. 마찰 DR은 작게 둔다 |
| C2 정지 자세 보상(회사 stand) | sim에서는 회사 stand와 같았지만 실기에서는 정반대 평형이었다 | 자세 보상만으로는 해결되지 않는다. 주 arm에서는 제외한다 |

## 3. 결론 — A 대비 다음 학습 변경 (우선순위)

1. **CoM DR → URDF 중심 base ±1.5 cm.** 확신 높음.
2. **무릎만 보상.** 학습 무릎 명령 92/2.3 + 무릎 출력 계수 DR log-U[0.55, 1.0]으로 하고, 배포도 92/2.3으로 둔다.
   - hip·shoulder는 60/1.5 nominal ±20%로 유지하고, 다리 전체 약화 DR은 쓰지 않는다.
   - 확신: 무릎은 높음, hip·shoulder는 중간.
3. **다리 MA2 필터를 학습 루프에 포함한다.** 배포도 `leg_action_filter:=ma2_legs`로 같게 한다.
   - 실기 고주파 여유를 고려해 목표 지연 DR을 0–20 ms에서 0–30 ms로 넓히는 것도 함께 검토한다.
   - 확신 중간: 7–9 Hz 모드의 원인이 분리되지 않았다.
4. **위치 오차 관측(엔코더·IMU 기반, 명령 0일 때 latch, clip)을 actor에 추가한다.** 관측이 33에서 34로 늘어 C++·export·sim2sim을 함께 바꿔야 한다. 확신 중간–높음: drift에 대한 구조적 대책이다.
5. 보상, 명령, push, FlashSAC 설정은 A와 같다.

**arm 구성:**
- P1 = 1 + 2 + 3: 인터페이스 변화가 없어 바로 학습할 수 있다.
- P2 = P1 + 4: 구현과 parity 검증 뒤에 학습한다.
- P1은 배포 경로가 이미 있어(무릎 92 config, MA2 옵션) 빠르게 실기 비교가 가능하다.

**당분간 실기 운용:** A80k 60/92 + MA2 + notch가 drift −0.018, pitch 5.5°로 수치상 가장 낫다. 다만 7–8 Hz 몸통 흔들림이 남고, 운전 명령이 run마다 달라 비교가 확정적이지 않다.

## 파일

- **필터 run 공통 지표:** [`real_runs_vs_training/`](real_runs_vs_training/). `analyze_rl_segments_pitch.py`를 수정 없이 썼다.
- **`./scripts/agent-check.sh`:** [log](real_runs_vs_training/agent_check.log).
