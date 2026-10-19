# FlashSAC C1/C2 재학습 — 다리 토크 스케일 보정 (학습 쪽 보상)

Execution Domain: `TRAINING_SIM` (설정 diff, live env 검사, 8-step smoke, 전체 학습 2개 동시 실행 중). 로봇 접근·배포 없음.

Evidence Status:
- **PASS**: 설정·env·smoke 검사, 학습 시작(유한 update, W&B 연결).
- **NOT_TESTED**: 학습 완료, 정책 성능, 실기.
- 학습 중이라 Policy checkpoint SHA256은 아직 없다 (N/A).

기준 run: `tita_flash_sac_115632_883848` (`0r5o1bmm`, 학습 `env.yaml` SHA256 `f1796a30…`). Branch `agent/codex/dev_tita_gluon`. Commit 없음.

## 근거

- **다리 토크 스케일:** [회사 LQR 비교](vendor_lqr_vs_rl_claude_analysis.md)에서 같은 자세의 무릎 토크 비율(URDF 정적 / 명령·firmware)이 0.59–0.73(평균 약 0.655)이었다. 이전 동역학 grid의 0.60과 일치한다.
- **CoM:** URDF CoM은 실기와 1 cm 이내다.
- **보상 효과 확인:** [보상 검증](leg_torque_compensation_check.md)에서 k = 0.65만으로 실기 R0 drift를 재현했다(−0.197 vs −0.203 m/s). 정확히 보상하면 nominal 동작이 복원된다.
- **설계 원칙:** 고정 보상은 k 오차에 민감하므로, k 주변 분포로 학습해 정책이 실기 단위 그대로 동작하도록 한다.

## 두 arm (학습 당시 `env.yaml` 944 leaf 대비)

| 항목 | 이전 (115632) | C1 `DDT-Velocity-Flat-Tita-My-LegScale-v0` | C2 `DDT-Velocity-Flat-Tita-My-LegScale-Reward-v0` |
|---|---|---|---|
| 다리 Kp·Kd | 60/1.5, 각자 독립 ±20% | **공통 배율 log-U[0.55, 0.78] × 관절별 ±10%** | C1과 같음 |
| 휠 Kp·Kd | 독립 ±20% | 독립 ±20% (휠만) | 같음 |
| 다리 / 휠 Coulomb 마찰 | 0 / 0 | U[0, 2] / U[0, 0.4] N m | 같음 |
| CoM DR | 모든 body ±10 cm | **base만 ±1.5 cm** | 같음 |
| base 높이 목표 | 0.335 m | 0.335 m | **0.28 m** |
| `flat_orientation_l2` | −5 | −5 | **−15** |
| `joint_deviation_hip` | −1 | −1 | **−2.5** |
| zero-command 위치 drift sharpness | 8 | 8 | **20** |
| zero-command 정지 자세 (신규) | 없음 | 없음 | **−0.5 × Σ\|q − (hip 0, thigh 1.09, knee −2.16)\|** (\|cmd\| ≤ 0.05) |
| zero-command 선속도 L2 (신규) | 없음 | 없음 | **−4** (cmd = 0) |
| standing env 비율 | 0.1 | 0.1 | **0.2** |

- **설정 diff:** [C1](flashsac_legscale_training/config_diff_DDT-Velocity-Flat-Tita-My-LegScale-v0.log), [C2](flashsac_legscale_training/config_diff_DDT-Velocity-Flat-Tita-My-LegScale-Reward-v0.log). 표 외 항목 변경은 없다. action gain도 같다. 수정 후 A·B·B′ task 설정이 바뀌지 않은 것도 다시 확인했다.
- **목적:** C1은 물리 보정만의 효과를, C2는 회사 정지 동작 기반 보상의 추가 효과를 본다. 같은 seed(42)로 동시에 돌린다.

**Kp·Kd 범위와 배포 규칙 (사용자 질문 정리):**
- **적용 관절:** 다리 6관절(hip·허벅지·무릎) 모두에 같은 배율을 적용했다.
  - 무릎: 정적 비율로 직접 확인했다.
  - hip: 정적으로는 부정정이다. 다만 grid에서 다리 전체 0.6이 실기 hip 벌어짐·토크를 재현해 간접 근거가 있다.
  - 허벅지: 정지 토크가 약 1 N m라 식별되지 않았다. 같은 모터라는 가정이다.
  - 휠: 근거가 없어 제외했다.
- **배포 시 이중 보상 금지:** 학습 쪽 보상(C1/C2)은 sim 다리 Kp·Kd를 줄여 "실기에 60/1.5를 보냈을 때의 물리 토크"를 흉내 낸다. 그래서 C1/C2 정책은 **배포 config를 60/1.5 그대로** 써야 한다. 배포 쪽 ×1.53(92/2.3)은 nominal로 학습한 정책(R0 등)에만 쓴다. 둘을 같이 쓰면 실효 배율이 약 1.5배가 되어 과보상(sim k=0.75 → +0.17 m/s 전진 drift)과 같은 상황이 된다.

## 실행 전 검사

- **actuator (512 env, 각각 PASS):**
  - 다리 Kp 배율: C1 0.498–0.852 (평균 0.658), C2 0.497–0.845 (평균 0.655)
  - 공통 배율 0.55–0.78, nominal(1.0) 비율 0, 관절 간 log 상관 0.75
  - 다리 마찰 ≤ 2, 휠 ≤ 0.4 N m, 관측 33, action 8
  - 보상 항 전부 유한하다. C2의 새 항은 20 step 누적 env 평균 정지 자세 −0.256, 정지 선속도 −0.236으로 정상 계산된다.
- **CoM (각각 PASS):** base x 오프셋 C1 ±1.50 cm(평균 +0.02), C2 ±1.48 cm. 다른 body는 고정이다.
- **8-step smoke:** C1 `tita_flash_sac_114427_281767`, C2 `tita_flash_sac_114438_812692` 모두 PASS(exit 0, update 6회). 두 run 모두 `policy_interface.json`·`action_mapping.json`이 115632와 바이트 단위로 같다.

## 실행 상태 (2026-10-18 11:45 KST 시작)

| arm | run_name | native run | PID | W&B |
|---|---|---|---|---|
| C1 | `legscale_C1_s42` | `tita_flash_sac_114458_484840` | 492648 | [a4y2fxqy](https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/a4y2fxqy) |
| C2 | `legscale_reward_C2_s42` | `tita_flash_sac_114500_483968` | 492819 | [rbgftx30](https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/rbgftx30) |

- **공통 설정:** 4096 env, 100k step, seed 42, `setsid nohup`으로 분리 실행.
- **시작 직후 확인:** step 300까지 유한하고, run당 약 24k transitions/s다. GPU 97% / 10.8 GB.
- **예상 종료:** 16:30 KST 전후.
- **기록 파일:** [C1 launch](legscale_C1_s42_launch.json), [C2 launch](legscale_reward_C2_s42_launch.json).

## 학습 후 평가 계획

1. **평가 전용 export:** 인터페이스 동일성 확인 후 수행한다(`test/export_ab_checkpoints.py` 방식). `export.py`는 수정하지 않는다.
2. **수용시험 물리 세트:** 다리 배율 k ∈ {0.55, 0.65, 0.75}와 nominal(k = 1, 회귀 확인), 마찰 유무를 둔다.
   - 주 판정: k = 0.65에서 zero-command drift ≤ 0.03 m/s, pitch, 진동, 후진 0.6 실패 없음.
   - R0·A 80k와 같은 표로 비교한다.
3. **C2 추가 확인:** 정지 자세가 회사 stand(pitch 1.4°, 허벅지 1.09, 무릎 −2.16, hip 0)에 얼마나 가까운지 본다.
4. **실기:** 별도 승인 후에만 진행한다. 배포 config는 60/1.5 그대로다.

## 변경·검사

- **신규:** `real2sim/rewards.py` (`375239f1…`), C1/C2 config 클래스(`env_cfg.py` `e9702ec4…`), task 등록(`__init__.py` `fe1d4fb8…`).
- **test/:** `check_real2sim_task_events.py`에 `--kp-range`와 보상 항 합계 검사 추가(`86f4ae20…`). `check_basecom_shift_task.py`에 `--y-range`, `--z-range` 추가(`69992e6b…`). 둘 다 기본값은 기존과 같다.
- **학습 중 수정 금지:** 실행 중인 run이 위 파일을 불러왔으므로 종료 전까지 수정하지 않는다.
- **`./scripts/agent-check.sh`:** [log](flashsac_legscale_training/agent_check.log).

## 중단 (2026-10-18 15:27 KST, 비의도적 — systemd-oomd)

- **원인:** 15:26–15:27에 systemd-oomd가 메모리 압박으로 `app-org.chromium.Chromium-723408.scope`(VS Code와 그 하위 프로세스, 28.2 GB)를 종료했다.
  - 이 cgroup에 C1/C2 학습 두 개, VS Code, Claude가 15:26에 띄운 sim2sim 평가 worker 10개가 함께 있었다.
  - 평가 worker 추가가 압박의 직접 계기였다. 근거는 journalctl의 `systemd-oomd killed some process(es) in this unit`, `Failed with result 'oom-kill'`이다.
- **진행 정도:**
  - 마지막 log는 C1 step 77700, C2 step 76900이다(15:27).
  - 저장된 checkpoint는 각 `model_5000`–`model_75000`이다. `model_75000`의 actor SHA256은 ddt.json과 일치한다: C1 `a4bf5bfa…`, C2 `663f7a89…`.
  - 학습 미완료다(목표 100k). W&B run은 중단 상태로 남는다.
- **재발 방지:** 이후 평가는 별도 systemd user unit(`MemoryMax=16G`)과 worker 8개로 실행한다.
- **재개 여부:** operator 결정 사항이다. checkpoint에 agent/critic/temperature 상태는 있지만 replay buffer는 없다.
