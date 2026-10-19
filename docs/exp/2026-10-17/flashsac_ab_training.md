# FlashSAC A/B 동시 재학습 — CoM-only (A) vs CoM + 다리 계수·마찰 (B)

Execution Domain: `TRAINING_SIM` (설정 diff·live env 검사·8-step smoke·전체 학습 2개 동시 실행 중). 로봇 접근·export·배포 없음.

Evidence Status:
- **PASS**: 두 arm의 설정 diff, env 검사, smoke, 학습 시작과 유한 update·W&B 연결.
- **NOT_TESTED**: 학습 완료, 정책 성능, 실기.
- 학습 중이라 Policy checkpoint SHA256은 아직 없다 (N/A).

기준 run: `tita_flash_sac_115632_883848` (`0r5o1bmm`). model_60000 checkpoint SHA256 `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`. 학습 `env.yaml` SHA256 `f1796a302b56e74be9ee292c1e35553b048b887bd7c29bb336e4b3099f6bd3a6`.

Branch: `agent/codex/dev_tita_gluon` (HEAD `17a6cfe`, 작업 트리에 미커밋 변경 다수). Commit/push 없음.

## 결정과 배경

- 사용자가 A와 B를 동시에 실행하도록 요청했다(2026-10-17).
- 전제는 [CoM-only 계획](flashsac_basecom_plan.md)의 operator 판단(IMU 정상, CoM이 주원인)이다.
- B는 [real2sim grid](real2sim_leg_wheel_grid.md)와 [17:44 holdout](flashsac_retrain_prep.md)에서 실기를 가장 잘 재현한 조합(CoM + 다리 등가 계수·마찰)에 맞춘 arm이다.
- 다리 계수는 실제 모터 출력 부족을 측정한 값이 아니며([motor feedback](flashsac_60000_motor_feedback_report.md)), 범위는 강건성 탐색 범위다.

## 두 arm의 설정 (학습 당시 `env.yaml` 944 leaf 대비)

| 항목 | 이전 (115632) | A `DDT-Velocity-Flat-Tita-My-BaseComShift-v0` | B `DDT-Velocity-Flat-Tita-My-Real2Sim-BaseComShift-v0` |
|---|---|---|---|
| CoM randomization 대상 | 모든 body, 각 ±10 cm | base_link만 | base_link만 |
| base CoM x / y / z | ±10 / ±10 / ±10 cm | −5.5~−1.5 / ±2 / ±3 cm | −5.5~−1.5 / ±2 / ±3 cm |
| Kp/Kd 독립 ±20% (log-uniform) | 모든 관절 | 모든 관절 (동일) | 휠만 |
| 다리 Kp·Kd 공통 배율 | 없음 | 없음 | log-U[0.5, 1.05] × 관절별 ±20% jitter |
| 다리 관절 Coulomb 마찰 | 0 | 0 | U[0, 4] N m (dynamic = static × U[0.8, 1.0]) |
| 휠 관절 Coulomb 마찰 | 0 | 0 | U[0, 0.4] N m (동일 방식) |

- **설정 diff:** [A](flashsac_ab_training/config_diff_DDT-Velocity-Flat-Tita-My-BaseComShift-v0/diff.log)는 CoM 4개 leaf만 바뀌었다. 리팩터 뒤에도 이전에 검증한 diff와 같다. [B](flashsac_ab_training/config_diff_DDT-Velocity-Flat-Tita-My-Real2Sim-BaseComShift-v0/diff.log)는 CoM 4개, 휠 전용 gain 1개, event 3개(각 17 leaf)가 추가됐다.
- **공통 유지:** 관측 33·action 8·gain·PD·clip, 나머지 DR, 보상, 명령 분포, 종료 조건, FlashSAC 설정. 마찰 단위는 이 설치본에서 N m Coulomb으로 확인했다([단위 시험](flashsac_retrain_prep/friction_semantics/friction_semantics.json)).
- **코드 SHA256:**
  - `real2sim/env_cfg.py` `a52f390473f02d41e6e0bdcc66717c1d0e58e7a69fa75c6b05099abe88fc9e83`
  - `real2sim/__init__.py` `9ae7d26baceb3d5f41f54c79f30cbd7d3573d5410e01a205273d167d571da263`
  - `real2sim/events.py` `1041a01c88f698fc173140a0de6d9752d74c84a28cb24ad4f446e8105cdc5256`
  - 실행 중인 두 프로세스가 시작 시 이 파일들을 불러왔으므로, 학습 종료 전까지 수정하지 않는다.

## 실행 전 검사

| 검사 | A | B |
|---|---|---|
| live env (CoM) | PASS: base x −5.50~−1.50 cm (평균 −3.48), 다른 body 차이 0 ([json](flashsac_basecom_plan/event_check/event_check.json)) | PASS: x −5.48~−1.50 cm (평균 −3.56), 다른 body 차이 0 ([json](flashsac_ab_training/armB_check_basecom_shift_task/event_check.json)) |
| live env (gain·마찰) | 해당 없음 | PASS: 다리 Kp 배율 0.414–1.253, 관절 간 log 상관 0.779, 다리 마찰 0–4, 휠 0–0.4 N m, dynamic ≤ static, viscous 0 ([json](flashsac_ab_training/armB_check_real2sim_task_events/event_check.json)) |
| 8-step smoke | PASS (`tita_flash_sac_185135_714007`) | PASS (`tita_flash_sac_201902_461399`, [log](flashsac_ab_training/armB_train_smoke.log)) |
| `policy_interface.json`, `action_mapping.json` | 115632와 바이트 동일 | 115632와 바이트 동일 |

## 실행 상태 (2026-10-17 20:19 KST 시작)

| arm | run_name | native run | PID | W&B |
|---|---|---|---|---|
| A | `basecom_shift_A_s42` | `tita_flash_sac_201940_278440` | 3092837 | [7gy479xy](https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/7gy479xy) |
| B | `real2sim_basecom_shift_B_s42` | `tita_flash_sac_201942_248862` | 3092935 | [rgva5dwa](https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/rgva5dwa) |

- **공통 CLI:** `scripts/flash_sac/train.py --num_envs 4096 --steps 100000 --seed 42 --device cuda:0 --headless --logger wandb --wandb_project tita_flat_flash_sac` (cwd `lab/ddt_lab`).
- **실행 방식:** `setsid nohup`으로 실행해 각자 독립 세션이다.
- **기록 파일:** console log는 `<run_name>_console.log`, 실행 기록은 [A launch](basecom_shift_A_s42_launch.json) / [B launch](real2sim_basecom_shift_B_s42_launch.json).
- **시작 직후 확인:** 두 run 모두 step 300/update 548까지 유한 보상이었다. GPU 사용률 98%, 메모리 10.7 GB / 24 GB (각 4.8 GB). 처리량은 run당 약 23.4k transitions/s(단독 실행 약 49k)다.
- **예상 소요:** 100k step 기준 약 4.9시간, 10/18 01:15 KST 전후 종료 예상. checkpoint는 5k step마다 `lab/ddt_lab/logs/flash_sac/<native run>/model_<step>`에 저장된다.
- **이전 프로세스:** 10/14부터 일시정지돼 있던 학습(PID 3301796)은 사용자 요청으로 사전에 종료했다([CoM-only 계획](flashsac_basecom_plan.md)).

진행 확인 (`DESKTOP_DRY_RUN`):

```bash
tail -n 2 docs/exp/2026-10-17/basecom_shift_A_s42_console.log docs/exp/2026-10-17/real2sim_basecom_shift_B_s42_console.log
ps -o pid,etime,stat -p 3092837,3092935; nvidia-smi --query-compute-apps=pid,used_memory --format=csv
```

## 학습 후 평가 계획 (사전 고정 protocol 사용)

1. **Export:** `lab/ddt_lab/scripts/flash_sac/export.py:36`의 task 고정 검사를 같은 33/8 인터페이스 variant까지 허용하도록 바꿔야 한다. 배포 경로라 승인이 필요하다. 이후 Torch↔ONNX·adapter parity와 배포 config 인터페이스 비교를 반복한다.
2. **Checkpoint 선택:** 40k–100k(10k 간격)를 sim 수용시험으로 선택한다.
   - 물리 세트: [CoM 계열](flashsac_basecom_plan/acceptance_model_60000_com/acceptance_protocol.json) (nominal, CoM −2/−3.5/−5 cm, C)과 [A/B/C 계열](flashsac_retrain_prep/acceptance_model_60000/acceptance_protocol.json).
   - 기준값은 현재 model_60000 결과다.
3. **최종 확인:** 선택된 checkpoint만 holdout 재생(17:44 `abc`·`com_only` protocol)과 14:11 재생으로 확인한다. holdout은 선택에 쓰지 않는다.
4. **판정 축:**
   - 주 판정: A와 B 각각의 CoM 조건 zero-command(|v̄| ≤ 0.03 m/s)와 정지 재진입.
   - 보조 판정: C(스트레스)와 후진 0.6 m/s.
   - 회귀 확인: nominal 추종·토크·pitch.
   - 해석: A만 통과하면 CoM 단일 요인으로 충분하다는 근거가 된다. B만 통과하면 다리 쪽 요인이 필요하다는 근거가 된다.
5. **실기:** 별도 operator 승인 후에만 진행한다. 초기 후진 명령 상한은 낮게 둔다.

## 한계

- seed 1개(42)씩이다. arm 차이가 작으면 seed 분산과 구분하지 못한다.
- 두 run이 GPU를 공유해 처리량이 단독 실행의 절반이다. 학습 결과(정책)에는 영향이 없다고 보지만, wall-clock 비교는 의미가 없다.
- A·B의 CoM 범위는 sim 등가 추정에 기반한 탐색 범위다. 실측 CoM이 아니다.

## 변경·검사

- **수정:** `real2sim/env_cfg.py`에서 CoM 범위를 `BASE_COM_SHIFT_RANGE`와 `_shift_base_com()`으로 묶고 B 클래스(`MyTitaFlatReal2SimBaseComShiftEnvCfg`)를 추가했다. `real2sim/__init__.py`에 B task를 등록했다.
- **기존 파일:** 기존 task registry, `my_flat_env_cfg.py`, 학습 스크립트는 수정하지 않았다.
- **산출물:** `flashsac_ab_training/`(diff·env 검사·smoke log), 두 run의 console log와 launch.json, `train.py`가 만든 `tita_flash_sac_2019*_*` evidence.
- **`./scripts/agent-check.sh`:** [log](flashsac_ab_training/agent_check.log).
