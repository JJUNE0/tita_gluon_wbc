# FlashSAC B′ 재학습 (seed 42·7) — B 대비 변경과 실행 기록

Execution Domain: `TRAINING_SIM` (설정 diff, live env 검사, 8-step smoke, 전체 학습 2개 동시 실행 중). 로봇 접근·배포 없음.

Evidence Status:
- **PASS**: 설정 diff, env 검사, smoke, 학습 시작과 유한 update·W&B 연결.
- **NOT_TESTED**: 학습 완료, 정책 성능, 실기.
- 학습 중이라 Policy checkpoint SHA256은 아직 없다 (N/A).

기준: arm B `tita_flash_sac_201942_248862` ([sim2sim 보고서](flashsac_ab_sim2sim_report.md)). Branch `agent/codex/dev_tita_gluon`. Commit/push 없음.

## 목적

B는 다리가 약한 조건까지 포함해 실패 없이 drift를 거의 없앴다. 그러나 다리 출력이 nominal인 조건에서 7개 checkpoint 모두 2–3.6 Hz로 진동했고, CoM 0에서는 전진 drift가 있었다. B′는 B의 강건성을 유지하면서 이 두 문제를 겨냥한다.

## B 대비 변경 (설정 diff 2 leaf)

| 항목 | B | B′ `DDT-Velocity-Flat-Tita-My-Real2Sim-NomMix-v0` |
|---|---|---|
| 다리 Kp·Kd 공통 배율 | 모든 env에서 log-U[0.5, 1.05] | **50% env는 1.0 고정**, 나머지 50%는 log-U[0.5, 1.05]. 관절별 ±20% jitter는 양쪽 모두 유지 |
| base CoM x | U(−5.5, −1.5) cm | **U(−5.5, +0.5) cm** (URDF 값 0 포함) |

- **나머지:** B와 같다. base CoM y ±2 / z ±3 cm, 다른 body CoM 고정, 다리 마찰 U[0, 4] N m, 휠 마찰 U[0, 0.4] N m, 관측·action·PD·clip·보상·명령·FlashSAC 설정 모두 동일.
- **설정 diff 결과:** [B 대비](flashsac_bprime_training/config_diff_vs_B.log)는 `com_range.x`와 `nominal_probability: 0.5` 두 항목만 바뀌었다. 이번 수정 뒤에도 A·B task 설정은 이전 diff와 같았다(`recheck_*.log`).
- **코드:** `real2sim/events.py`에 `nominal_probability` 인자를 추가했다. 기본값 0은 기존과 같은 경로이고, 0일 때 추가 난수 호출도 없다. 공통 배율은 `asset.real2sim_leg_output_scale`에 기록한다. `real2sim/env_cfg.py`에 `MyTitaFlatReal2SimNominalMixEnvCfg`를 추가했다.
- **코드 SHA256:**
  - `env_cfg.py` `502ec0e65558dd98b14f5b4f0a6f93d7377e87f024b373f9918156c32ae5cd76`
  - `events.py` `6a2366404d0fc80a6e017127bfa89088725270a4b2a1465d81811669a99967cc`
  - `__init__.py` `bf9aa5fe27d3089bf448e3e7e6f450f671f7062bd43af2b89caf8e6859b0ca64`
  - 실행 중인 두 run이 이 파일을 불러왔으므로 학습 종료 전까지 수정하지 않는다.

## 실행 전 검사

- [actuator 검사](flashsac_bprime_training/event_check_actuator/event_check.json) (512 env) PASS:
  - 공통 배율 1.0 비율 48.8%, 범위 0.50–1.05
  - 다리 Kp 배율 0.41–1.24 (평균 0.86, B는 0.74)
  - 관절 간 log 상관 0.779
  - 마찰 범위, dynamic ≤ static, viscous 0 정상
- [CoM 검사](flashsac_bprime_training/event_check_com/event_check.json) PASS: base x 오프셋 −5.50 ~ +0.49 cm (평균 −2.44), 다른 body 고정, 관측 33/36, action 8.
- [8-step smoke](flashsac_bprime_training/train_smoke.log) PASS (`tita_flash_sac_095126_661575`). `policy_interface.json`·`action_mapping.json`이 115632와 바이트 단위로 같다.

## 실행 상태 (2026-10-18 09:51 KST 시작)

| seed | run_name | native run | PID | W&B |
|---|---|---|---|---|
| 42 | `bprime_nommix_s42` | `tita_flash_sac_095147_230888` | 270533 | [xiryuxc3](https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/xiryuxc3) |
| 7 | `bprime_nommix_s7` | `tita_flash_sac_095149_279860` | 270682 | [g13hpgpl](https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/g13hpgpl) |

- **공통 CLI:** `--num_envs 4096 --steps 100000 --device cuda:0 --headless --logger wandb --wandb_project tita_flat_flash_sac`. `setsid nohup`으로 분리 실행했다.
- **기록 파일:** [s42 launch](bprime_nommix_s42_launch.json), [s7 launch](bprime_nommix_s7_launch.json), console log `<run_name>_console.log`.
- **시작 직후 확인:** step 1000까지 유한 보상이었다. GPU 98% / 10.4 GB, run당 약 24k transitions/s. 14:35 KST 전후 종료 예상이다.

## 학습 후 평가 (A/B와 같은 절차)

1. [`test/export_ab_checkpoints.py`](../../../test/export_ab_checkpoints.py)와 같은 방식으로 평가 전용 export를 한다. 인터페이스 동일성 확인 후에만 수행하며, `export.py`는 수정하지 않는다.
2. [`test/evaluate_ab_policies.py`](../../../test/evaluate_ab_policies.py)와 같은 protocol(CoM 세트 1단계 → A/B/C 세트·17:44 재생 2단계)으로 평가한다. R0, A 40k, B 80k와 비교한다.
3. 실기 후보는 [사후 안전 선별](flashsac_ab_sim2sim_report.md#7-실기-후보-사후-안전-선별) 기준(실패 0, 정지 진동 없음, startup pitch ≤ 10°, R0보다 작은 drift)을 hard filter로 적용한다. 두 seed 모두에서 같은 성질이 나오는지도 본다.
4. 실기는 별도 operator 승인 후에만 진행한다.

## 변경·검사

- **수정:** `real2sim/events.py`, `real2sim/env_cfg.py`, `real2sim/__init__.py`.
- **test/:** `check_real2sim_task_events.py`에 `--expect-nominal-fraction` 추가, `check_basecom_shift_task.py`에 `--x-range` 추가. 둘 다 기본값은 기존과 같다.
- **`./scripts/agent-check.sh`:** [log](flashsac_bprime_training/agent_check.log).

## 중단 (2026-10-18 약 11:36 KST, 사용자 요청)

- **이유:** [회사 LQR 비교](vendor_lqr_vs_rl_claude_analysis.md)의 근거와 B′의 전제가 어긋났다.
  - 실기 다리 토크 스케일은 약 0.65로, nominal 1.0과 다르다.
  - URDF CoM은 실기와 1 cm 이내로 일치한다.
- **종료 방식:** 두 run(PID 270533, 270682)은 SIGTERM에 20 s 동안 응답하지 않아 SIGKILL로 종료했다. wandb 보조 프로세스도 스스로 종료돼 남은 학습 프로세스는 없다. GPU 사용량은 1.1 GB로 내려갔다.
- **진행 정도:** 마지막 log는 s42 step 35800, s7 step 36100이다. 저장된 checkpoint는 각 `model_5000`–`model_35000`이다. 평가하지 않았고 최종 summary도 없다(W&B run은 중단 상태로 남는다).
- **결과 판정:** 학습 미완료라 Policy checkpoint 성능은 **NOT_TESTED**다.
