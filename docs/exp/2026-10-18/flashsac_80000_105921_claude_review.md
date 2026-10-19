# FlashSAC 80000 (A 80k) 실기 10:59 run — pitch 증가의 원인 검토

Execution Domain: `DESKTOP_DRY_RUN`. 이미 PC로 복사된 bag을 읽기만 했고, 기존 VALIDATION_SIM 기록과 비교했다. 로봇 접근·명령 없음.

Evidence Status:
- **PASS**: bag 무결성(quick_check)과 구간 집계.
- **SUSPICIOUS**: 원인 해석. sim 등가 모델에 근거한다.
- **NOT_TESTED**: 외부 속도·자세 GT, 손 접촉 여부.

- 정책: `tita_flash_sac_201940_278440/model_80000` (arm A, CoM-only DR). Checkpoint SHA256 `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`, ONNX SHA256 `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`.
- 배포: [slow_sit_80000_deployment.md](slow_sit_80000_deployment.md) (다른 에이전트 작업).
- Run: `flashsac_80000_105921_542288145_output_true` (velocity bias OFF, output true). Bag DB3 SHA256 `3cec1e2ae57132944fcb73fff6f9206fb92b51107559f8fd0a4bfbdc39f9b606`. 사본 위치는 `flashsac_80000_105921_pitch_review/`이며, 이 폴더는 다른 작업의 것이라 수정하지 않았다.
- Branch `agent/codex/dev_tita_gluon`. Commit/push 없음.

## 결론

1. **drift는 R0보다 줄었다.** 정지 유지 구간(중립 1 s 경과, RL+3 s 이후)의 FK 추정 속도는 −0.06 ~ −0.12 m/s다. R0 60k 실기는 −0.20 m/s였다.
2. **pitch는 약 8°로 R0(1.3–1.8°)보다 6–7° 더 앞으로 숙였다.** CoM만으로는 설명되지 않는다.
   - 다리 nominal인 CoM-only sim에서 A 80k의 pitch는 CoM 0에서 5.1°이고, CoM을 뒤로 옮길수록 줄어든다(−3.5 cm 1.1°, −5 cm −0.9°).
   - 다리 등가 계수 0.6·관절 마찰·CoM −2 cm인 **C 모델은 A 80k를 pitch 8.47°, 무릎 −2.25/−2.23 rad, 무릎 토크 28.3/25.6 N m로 예측했다.** 실기는 8.1–8.6°, −2.10/−2.02 rad, 30.5/24.1 N m다.
   - 같은 C 모델은 R0를 pitch 1.80°로 예측한다(실기 1.78°). C 모델은 R0의 14:11 run으로만 맞춘 것이다. 따라서 A 80k의 pitch 일치는 사후 fitting이 아닌 사전 예측이다.
3. **해석 (가설):** sim C에서 R0는 몸을 거의 수평으로 두는 대신 −0.19 m/s로 밀린다. 새 정책들(A 80k 8.5°, A 40k 7.0°, B 80k 7.0°)은 앞으로 숙여 무게중심을 바퀴 위로 보내는 방식으로 drift를 줄였다. 즉 pitch 증가는 균형점 차이를 보상한 결과다. 그 균형점 차이의 대부분은 CoM 단독이 아니라 웅크린 다리 자세(다리 등가 계수 쪽 요인)에서 온다. sim C에서 CoM −2 cm 단독의 2.7° 대비 약 +5.7°다. 몸을 수평으로 유지하면서 다리로 바퀴 위치를 옮기는 다른 평형이 가능한지는 확인하지 않았다.

## 실기 측정 (분석기: [test/sim2real/analyze_rl_segments_pitch.py](../../../test/sim2real/analyze_rl_segments_pitch.py))

상태 전이: idle → transform_up(6.4 s) → sit(12.4) → rl(15.8) → return_to_sit(56.9) → sit(60.9) → rl(62.0) → estop(92.8). training sample과 motor feedback은 각 5,144개이고, RL 구간은 2개다.

| 구간 | 길이 / 이동 비율 | 정지 유지 FK 속도 | pitch | 무릎 q L/R | 허벅지 q L/R | 무릎 토크 명령 = 보고 | startup (0–3 s) pitch peak / 휠 토크 peak 명령·보고 |
|---|---|---:|---:|---|---|---|---|
| RL 1 | 41.1 s / 27% | −0.073 ± 0.053 m/s (창별 −0.063, −0.056, −0.093) | 8.40 ± 0.79° | −2.10 / −2.02 | 0.88 / 0.92 | 30.5 / 24.1 N m | 14.0° / 12.0 · 12.18 N m |
| RL 2 | 30.8 s / 52% | −0.115 ± 0.036 m/s | 8.13 ± 0.71° | −2.09 / −2.03 | 0.90 / 0.94 | 29.3 / 25.1 N m | 13.2° / 12.0 · **14.24 N m** |

- firmware 보고 무릎 토크는 명령과 같다(이전 run과 동일). 외부 Nm 교정은 아니다.
- startup 휠 토크의 firmware 보고 peak(14.24 N m)가 software clip(12 N m)을 넘었다. 60k run에서 −12.95 N m가 관찰된 것과 같은 현상이며, 원인(캐시 지연·과도·단위)은 미식별이다.
- 손 접촉 여부는 기록에 없다. 정지 유지 구간을 자유 drift로 단정하지 않는다.

## sim 대비 (zero-command, 5–30 s; [log](flashsac_80000_105921_claude_review/sim_vs_real_stance.log))

| 정책 / 물리 | 속도 | pitch | 무릎 L/R | 무릎 토크 L/R |
|---|---:|---:|---|---|
| A 80k / nominal | −0.007 | 5.07° | −1.76 / −1.78 | 16.7 / 16.7 |
| A 80k / CoM −3.5 cm | −0.066 | 1.05° | −1.72 / −1.75 | 15.4 / 15.4 |
| A 80k / CoM −5 cm | −0.068 | −0.93° | −1.68 / −1.72 | 14.6 / 14.7 |
| **A 80k / C** | −0.015 | **8.47°** | **−2.25 / −2.23** | **28.3 / 25.6** |
| **실기 A 80k** | −0.06 ~ −0.12 | **8.1–8.6°** | −2.10 / −2.02 | 30.5 / 24.1 |
| R0 / C | −0.187 | 1.80° | −2.13 / −2.19 | 28.6 / 31.3 |
| 실기 R0 (14:11) | −0.203 | 1.78° | −2.15 / −2.15 | 30.2 / 27.9 |
| B 80k / C | +0.007 | 7.00° | −1.89 / −1.90 | 28.1 / 28.2 |
| A 40k / C | +0.005 | 7.04° | −2.06 / −2.04 | 29.7 / 27.8 |

- **C가 맞는 것:** pitch와 무릎 토크, 그리고 R0·A 80k 두 정책의 pitch 차이를 모두 맞춘다.
- **drift:** 실기 A 80k(−0.06 ~ −0.12)는 C(−0.015, 0.1 Hz대 느린 출렁임)와 CoM −3.5 cm(−0.066) 사이다. C의 동역학 재현이 제한적이라는 이전 한계와 맞는다.

## 다음 단계 제안

- **수평 유지 평형의 가능성:** sim C에서 몸을 수평에 가깝게 유지하면서 drift도 없는 정책이 가능한지 확인한다. 예를 들어 `flat_orientation_l2` 강화나 무릎·허벅지 자세 목표로 다리를 써서 바퀴를 CoM 아래로 보내는 방식이다. 단, 이런 제약이 drift를 되살릴 수 있으므로 같은 C·CoM 조건에서 drift와 pitch를 함께 본다.
- **B′ 평가:** B′(학습 중)는 C 조건 pitch를 R0·A 80k와 같은 표에 넣어 비교한다.
- **startup:** startup pitch peak 13–14°와 휠 토크 보고 peak > 12 N m는 별도로 추적한다.

## 변경·검사

- **신규:** `test/sim2real/analyze_rl_segments_pitch.py` (SHA256 `d82c5efd…`). RL 구간 여러 개를 허용하고, bag은 read-only로 연다.
- **산출물:** `flashsac_80000_105921_claude_review/` (`segments.json`, `signals.npz`, sim 비교 log)와 이 보고서.
- **수정하지 않은 것:** 제어 코드·배포 bundle·다른 에이전트 폴더.
- **`./scripts/agent-check.sh`:** [log](flashsac_80000_105921_claude_review/agent_check.log).
