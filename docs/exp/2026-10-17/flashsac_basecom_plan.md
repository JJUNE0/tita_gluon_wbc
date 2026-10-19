# FlashSAC CoM-only 재학습 실험 계획 — 이전 설정 대비 변경점

Execution Domains: `TRAINING_SIM` (설정 dump·live env 검사·8-step 학습 smoke, 멈춘 학습 프로세스 종료), `VALIDATION_SIM` (MuJoCo CoM sweep 12회, holdout 재생 5회, 수용시험 40회), `DESKTOP_DRY_RUN`. 로봇 접근·배포·전체 학습 없음.

Evidence Status:
- **PASS**: 설정 diff, env 검사, smoke, 인터페이스 동일성.
- **FAIL**: holdout 사전 기준(모든 CoM-only 후보), 현재 정책의 CoM −3.5/−5 cm zero-command 기준.
- **SUSPICIOUS**: CoM 단일 원인 가정. sim에서 drift 일부만 설명한다.
- **NOT_TESTED**: 전체 재학습, 새 정책 성능, 실기.

기준 정책: `tita_flash_sac_115632_883848/model_60000`. Checkpoint SHA256 `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`, ONNX SHA256 `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`. 학습 `env.yaml` SHA256 `f1796a302b56e74be9ee292c1e35553b048b887bd7c29bb336e4b3099f6bd3a6`.

Branch: `agent/codex/dev_tita_gluon`. Commit/push 없음.

## Operator 결정 (2026-10-17)

- IMU는 문제없는 것으로 본다. 무게중심(CoM)이 가장 큰 문제다.
- [재학습 준비](flashsac_retrain_prep.md)의 R1(다리 Kp·Kd 공통 배율, 관절 마찰)은 이번 실험에 넣지 않는다. 따라서 R1을 상속하는 R2(`...-Real2Sim-BaseCom-v0`)도 쓰지 않는다. 두 task의 코드는 남겨 두었고 사용하지 않는다.
- 10/14부터 떠 있던 학습 프로세스를 강제 종료한다.
  - 대상: PID 3301796, `tita_flash_sac_133201_468020`.
  - 상태: `T`(일시정지). GPU 4.8 GB 점유. 마지막 로그는 step 70000, `model_70000` 저장 메시지였는데 해당 run 폴더는 현재 없다.
  - 조치: SIGKILL. 하위 wandb-core와 wandb-xpu도 종료됐다. GPU 사용량은 898 MiB로 내려갔다.

## 이전 설정 대비 정확한 변경점

새 task `DDT-Velocity-Flat-Tita-My-BaseComShift-v0` (`MyTitaFlatBaseComShiftEnvCfg`)는 `MyTitaFlatEnvCfg`를 직접 상속한다. [설정 diff](flashsac_basecom_plan/config_diff/diff.log)에서 학습 당시 `env.yaml` 944개 항목 중 **바뀐 것은 `events.add_base_com` 4개뿐**이다. 나머지 4개 차이는 원래 task에서도 나오는 런타임 해석값이다(prim path 정규식, terrain `num_envs`/`env_spacing`).

| `events.add_base_com` | 이전 (115632) | 이번 |
|---|---|---|
| 적용 body | `.*` — base, 다리 6개, 휠 2개, 각각 독립 | `base_link`만 |
| x 오프셋 | U(−0.10, +0.10) m | **U(−0.055, −0.015) m** (중심 −3.5 cm) |
| y 오프셋 | U(−0.10, +0.10) m | U(−0.02, +0.02) m |
| z 오프셋 | U(−0.10, +0.10) m | U(−0.03, +0.03) m |
| 함수·mode | `randomize_rigid_body_com`, startup (env당 1회) | 동일 |

- **로봇 전체 CoM 기준 효과:**
  - 이전에는 전체 CoM x가 URDF 기준 0을 중심으로 표준편차 약 2.85 cm였다(body별 독립 ±10 cm에서 질량가중으로 계산).
  - 이번에는 base 11.36 kg / 전체 25.69 kg 비율로 전체 CoM x가 **−2.43 ~ −0.66 cm(중심 −1.55 cm, 표준편차 0.51 cm)** 이다.
  - 다리·휠 CoM은 더 이상 randomize하지 않는다. 이전에는 반경 9.25 cm 휠의 CoM도 ±10 cm까지 움직였다.
- **x 중심값 근거:** 다리 nominal로 한 CoM sweep에서 실기 pitch 1.78°가 −3.5 ~ −4 cm 부근에서 맞았다. 범위 하한 쪽은 다리 계수 후보 C의 −2 cm도 포함한다. 탐색 범위이며 실측 CoM이 아니다.

**그대로인 것:**
- 관측 33(항목·순서·scale·noise), critic 36
- action 8(scale·offset·piecewise gain 2.8/2.0/2.8/6.0)
- actuator: Kp 60 / Kd 1.5, 휠 Kd 0.5, effort 60/12, 지연 0–4 step
- 나머지 DR 전부: 바닥 마찰 0.2–1.6, base 질량 −0.5~+2 kg, 관성 ×0.85–1.15, Kp/Kd 독립 ±20%(모든 관절), IMU bias ±0.05, 관절 offset ±0.02, push, reset 분포
- 보상 가중치 전부, 명령 분포(x ±1, yaw ±1.5, standing 10%, ramp 0.5, 초기 2초 zero), 종료 조건, 에피소드 20초, dt 5 ms × decimation 4
- FlashSAC agent cfg와 학습 CLI(4096 env, 100k step, seed 42, buffer 1M/100k, batch 2048, updates/step 2.0, n-step 3, save 5k)

학습 smoke(`tita_flash_sac_185135_714007`)의 `policy_interface.json`·`action_mapping.json`은 115632와 바이트 단위로 같다.

**이번에 넣지 않은 것:** 다리 actuator 배율·관절 마찰(R1), IMU 오프셋 변경, 보상 변경, sit 자세 reset(R1b), 관측 변경.

## 근거 — CoM-only sim 결과

[sweep](flashsac_basecom_plan/com_only_gain1_results.json): 다리 배율 1.0, 마찰 0, IMU 0, 현재 model_60000. 14:11 자유 drift의 RL+5–10 s 구간과 비교했다.

| base CoM x | 0 | −2 cm | −3.5 cm | −4 cm | −5 cm | 실기 |
|---|---:|---:|---:|---:|---:|---:|
| 속도 (m/s) | +0.015 | −0.055 | −0.124 | −0.143 | −0.180 | −0.203 |
| pitch (°) | 3.96 | 3.23 | 1.96 | 1.37 | 0.32 | 1.78 |
| 무릎 q (rad) | −1.845 | −1.793 | −1.736 | −1.719 | −1.678 | −2.153 |

- pitch가 맞는 지점(−3.5 ~ −4 cm)에서 후진은 실기의 약 60–70%다. 무릎 자세·토크·휠 토크는 재현되지 않는다.
- [17:44 holdout](flashsac_retrain_prep/holdout_174421_com_only/holdout_metrics.json) (protocol SHA256 `5f07598d…`, 기준은 이전과 동일): segment 속도 MAE는 nominal 0.202 → CoM −3.5 cm 0.121, −4 cm 0.109. 중립 구간 속도는 −0.074 / −0.097 m/s(실기 −0.207)로, 이 구간 drift의 약 1/3–1/2이다. 사전 기준은 모두 불통과다. 참고로 C(CoM −2 cm + 다리 계수·마찰)는 0.084로 가장 낫다.

## 학습 후 평가 계획과 현재 정책 기준값

[CoM 계열 수용시험 protocol](flashsac_basecom_plan/acceptance_model_60000_com/acceptance_protocol.json) (SHA256 `d9e251ec…`)은 시나리오·gate가 기존 protocol과 같고 물리 세트만 바뀌었다: nominal, CoM −2/−3.5/−5 cm, C(스트레스). 현재 60k 기준값([metrics](flashsac_basecom_plan/acceptance_model_60000_com/acceptance_metrics.json)):

| 지표 | nominal | CoM −2 cm | CoM −3.5 cm | CoM −5 cm | C |
|---|---:|---:|---:|---:|---:|
| zero: v̄ (m/s) / 25 s 이동 | +0.015 / +0.38 m | −0.054 / −1.35 m | −0.123 / −3.07 m | −0.177 / −4.42 m | −0.187 / −4.67 m |
| +0.3 / −0.3 m/s → v̄ | +0.221 / −0.470 | +0.179 / −0.551 | +0.157 / −0.606 | +0.133 / −0.673 | +0.181 / −0.462 |
| −0.6 m/s → v̄ | −0.714 | −0.798 | −0.880 | −0.962 | 실패 (base 높이) |
| 정지 재진입 (+0.3 후) | +0.016 | −0.050 | −0.118 | −0.176 | −0.223 |
| yaw +0.5 / −0.5 → ωz | +0.514 / −0.462 | +0.509 / −0.476 | +0.513 / −0.480 | +0.516 / −0.469 | +0.535 / −0.669 |

Gate(사전 고정, sim 기준):
- zero-command: |v̄| ≤ 0.03 m/s, 이동 ≤ 0.75 m, pitch std ≤ 1°
- 전후진 추종: 오차 ≤ 0.05 m/s(±0.3) / ≤ 0.10 m/s(±0.6)
- 정지 재진입: ≤ 0.05 m/s
- yaw: 오차 ≤ 0.05 rad/s, 회전 중 병진 ≤ 0.05 m/s
- 회귀 방지: 토크 RMS·pitch std는 기준 정책의 1.2배 이하, 휠 clip 비율 ≤ 1%

이번 실험의 주 판정은 CoM −2/−3.5/−5 cm에서의 zero-command와 정지 재진입이다. nominal은 회귀 확인용이다. C는 이번 실험이 다루지 않는 요인이 섞인 스트레스 참고용이다. 실기 판정은 별도 승인된 재시험에서만 가능하다.

## 실행 전 남은 일

- 학습 실행 명령 (`TRAINING_SIM`, 승인 후):

```bash
cd lab/ddt_lab
/home/cocel/isaac/env_isaaclab/bin/python -u scripts/flash_sac/train.py \
  --task DDT-Velocity-Flat-Tita-My-BaseComShift-v0 --num_envs 4096 --steps 100000 --seed 42 \
  --device cuda:0 --headless --logger wandb --wandb_project tita_flat_flash_sac --run_name basecom_shift_s42
```

- 학습 후 export 전에 `lab/ddt_lab/scripts/flash_sac/export.py:36`의 task 고정 검사를 같은 33/8 인터페이스 variant까지 허용하도록 바꿔야 한다. 배포 경로라 승인이 필요하다.
- 기대치: sim 근거로는 CoM만으로 실기 drift의 일부만 설명된다. 재학습 정책이 실기에서 여전히 후진하거나 무릎이 낮게 서면, 다음 후보는 이번에 제외한 다리 등가 계수·마찰 요인이다.

## 변경·검사

- **수정:** `real2sim/env_cfg.py`에 `MyTitaFlatBaseComShiftEnvCfg` 추가(SHA256 `ccd8e57d…`). `real2sim/__init__.py`에 `DDT-Velocity-Flat-Tita-My-BaseComShift-v0` 등록(`7b388dbb…`).
- **test/ 변경:** 신규 `check_basecom_shift_task.py`(`203e81a6…`). `real2sim_holdout_replay.py`에 `--set com_only` 추가(`342dcd43…`, 기존 abc protocol 동일성 확인). `flashsac_acceptance_suite.py`에 `--physics-set com` 추가(`9872c73e…`, 기존 abc protocol 동일성 확인).
- **산출물:** `flashsac_basecom_plan/`(9.3 MB), `flashsac_retrain_prep/holdout_174421_com_only/`, smoke evidence `tita_flash_sac_185135_714007_*`.
- **PASS 항목:**
  - 설정 diff (4항목만 변경)
  - [env 검사](flashsac_basecom_plan/event_check/event_check.json): base CoM 오프셋 x −0.0550~−0.0150 m(평균 −0.0348), y ±0.0199, z ±0.0300, 다른 body CoM의 env 간 차이 0, 관측 33/36, action 8, 20 step 유한
  - [학습 smoke](flashsac_basecom_plan/train_smoke.log): 8 step, update 6회, exit 0
  - CoM sweep 12/12, holdout 5/5 실행, 수용시험 40회 실행
- **기존 파일:** 기존 task registry와 `my_flat_env_cfg.py`는 수정하지 않았다.
- **`./scripts/agent-check.sh`:** [log](flashsac_basecom_plan/agent_check.log).
