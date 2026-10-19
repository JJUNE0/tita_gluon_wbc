# 다리 토크 스케일 보상 가능성 — sim 검증 (R0 model_60000)

Execution Domain: `VALIDATION_SIM` (MuJoCo 수용시험 48 rollout). 실기·배포 없음.

Evidence Status:
- **PASS**: 실행과 비교.
- **SUSPICIOUS**: 실기 전이. 다리 토크 스케일 k는 sim 등가·정적 추정값이다.
- **NOT_TESTED**: 실기 보상 시험.

Policy: R0 `tita_flash_sac_115632_883848/model_60000`. Checkpoint SHA256 `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`, ONNX SHA256 `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.

Branch `agent/codex/dev_tita_gluon`. Commit 없음.

## 배경

[회사 LQR 비교](vendor_lqr_vs_rl_claude_analysis.md)에서 같은 자세의 무릎 토크 비율(URDF 정적 / 명령·firmware)이 세 경우 모두 0.59–0.73(평균 약 0.655)으로 나왔다. 이전 동역학 grid 식별값 0.60과 일치한다. 그래서 실기 다리는 명령 단위 기준 k ≈ 0.65배의 토크를 내는 것으로 모델링했다. URDF CoM은 실기와 1 cm 이내로 일치한다.

**보상 방법:** RL PD 출력의 다리 토크에 c = 1/0.65 ≈ 1.54를 곱한다. 이는 다리 Kp·Kd를 60 → 92, 1.5 → 2.3으로 바꾼 것과 같다(clip 아래). startup 상태기계 PD는 실기에서 튜닝된 값이므로 그대로 두고, 휠도 그대로 둔다.

**sim 재현:** `startup_leg_gain = k`, RL `leg_gain = k·c`로 설정했다. 기존 수용시험 시나리오와 gate를 그대로 썼다([protocol](leg_torque_compensation_check/acceptance_R0_60000/acceptance_protocol.json) SHA256 `91ef55af…`).

## 결과 (seed 104; zero는 seed 270도 같은 경향)

| 조건 (실제 k, 보상 c) | 실효 다리 배율 | zero v̄ / 25 s 이동 | pitch | 전후진 ±0.3 | −0.6 | 정지 재진입 (+0.3 후) |
|---|---:|---|---:|---|---|---:|
| nominal | 1.00 | +0.015 / +0.38 m | 3.93° | +0.221 / −0.470 | −0.714 | +0.016 |
| **보상 없음, k=0.65** | 0.65 | **−0.197 / −4.93 m** | 4.15° | +0.145 / −0.531 | −0.768 | −0.182 |
| 보상, k=0.55 | 0.85 | −0.041 / −1.02 m | 2.05° | +0.206 / −0.461 | **실패 (base 높이)** | −0.046 |
| **보상, k=0.65** | 1.00 | **+0.018 / +0.44 m** | 3.75° | +0.234 / −0.462 | −0.710 | +0.018 |
| 보상, k=0.75 | 1.15 | **+0.172 / +4.30 m** | 4.64° | +0.336 / −0.334 | −0.593 | +0.172 |
| 보상, k=0.65 + 다리 마찰 2·휠 0.3 N m | 1.00 | +0.021 / +0.52 m | 3.77° (std 1.90°) | +0.276 / −0.498 | −0.767 | +0.036 |

- **다리 스케일 단독 재현:** 보상 없이 k=0.65만으로 실기 R0의 drift(−0.203 m/s)를 −0.197 m/s로 재현했다. CoM 이동·IMU 오프셋·마찰 없이다. 실기 R0 drift의 주원인을 다리 토크 스케일로 보는 근거다(pitch는 4.15° vs 실기 1.78°로 일치하지 않는다).
- **정확한 보상:** nominal 동작(drift, 추종, startup)이 그대로 복원된다.
- **k 오차 민감도:** k가 0.55면 실효 0.85가 되어 −0.04 m/s drift가 남고 −0.6 후진에서 주저앉는다. k가 0.75면 실효 1.15가 되어 +0.17 m/s 전진 drift가 생긴다. 보상 계수는 약 ±5–10% 정확도가 필요하다. 현재 추정 폭(0.59–0.73)으로는 고정 보상만으로 부족하다.
- **마찰 추가 시:** drift는 맞지만 느린 pitch 흔들림(std 1.9°)이 생긴다.

## 실기 적용 방법 (승인 전 제안)

- **배포 쪽 보상 (재학습 없음):** 새 bundle의 `config.json`에서 다리 `joint_kp`, `joint_kd`만 ×1.53(k = 0.655 기준)으로 바꾼다.
  - `tita_node.cpp`는 이 값을 `ActionAdapter`에 그대로 쓴다(54행).
  - 다른 곳의 `joint_kd` 사용은 velocity bias용 휠 Kd(3, 7번)뿐이라 다리 변경의 영향이 없다.
  - launch의 bundle hash 고정 때문에 배포 절차와 operator 승인이 필요하다.
  - 사전 예측(반증 가능): R0가 sim nominal처럼 무릎 약 −1.85 rad, pitch 약 3.8°, drift 약 0으로 서야 한다. 그렇지 않으면 "명령 단위 스케일" 해석이 약해진다.
- **학습 쪽 보상 (배포 변경 없음):** 다리 출력 스케일 DR을 식별값 중심(예: log-U[0.55, 0.78])으로 두고 학습한다. 정책이 실기 단위 그대로 동작하도록 배우고, k 불확실성에도 강건해진다.
- **혼합:** 배포 보상(×1.53)과 nominal 주변 ±15% 상관 배율 DR 학습을 함께 쓴다.

## 함께 기록: B′ 중단

사용자 요청으로 B′ 두 run을 중단했다. 회사 데이터가 B′의 전제(다리 1.0 비중 50%, CoM −2.5 cm 중심)와 어긋나서다. [B′ 기록](flashsac_bprime_training.md)에 반영했다.

## 변경·검사

- **test/ 변경:**
  - `real2sim_leg_wheel_grid.py`에 `startup_leg_gain` 키 추가(SHA256 `c3b828d1…`). 기존 키 동작은 그대로다.
  - `flashsac_acceptance_suite.py`에 `legcomp` 물리 세트 추가(`da1afdbe…`). 기존 abc·com 세트·시나리오·gate가 같은 것을 확인했다.
- **산출물:** [결과](leg_torque_compensation_check/acceptance_R0_60000/acceptance_metrics.json), [log](leg_torque_compensation_check/acceptance_R0_60000.log).
- **수정하지 않은 것:** 제어·학습·배포 코드.
- **`./scripts/agent-check.sh`:** [log](leg_torque_compensation_check/agent_check.log).
