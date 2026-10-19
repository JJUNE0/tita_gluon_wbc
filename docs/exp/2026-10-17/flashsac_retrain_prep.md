# FlashSAC 재학습 준비 — motor feedback·holdout·분리 수용시험 반영

Execution Domains: `DESKTOP_DRY_RUN` (기존 로그·코드·설정 분석), `TRAINING_SIM` (설정 dump·Isaac 마찰 단위 시험·새 task env 검사·8-step 학습 smoke; 실제 재학습 없음), `VALIDATION_SIM` (MuJoCo holdout 재생 6회, 수용시험 32회, 대안 grid 144회). 로봇 접근·배포 없음.

Evidence Status:
- **PASS**: 설정 일치 확인, 로컬 simulator 의미 확인, 새 task 이벤트 검사, 학습 smoke, holdout·수용시험 실행과 재현성.
- **FAIL**: 사전 고정한 holdout 일치 기준(모든 후보), A/B/C에서 현재 정책의 zero-command·후진 0.6 기준.
- **SUSPICIOUS**: 0.6 등가 계수의 물리적 원인.
- **NOT_TESTED**: 전체 재학습, 새 정책 성능, 실제 Nm 교정, 실기 재시험.

Policy: `tita_flash_sac_115632_883848/model_60000` (run `0r5o1bmm`). Checkpoint SHA256 `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`, ONNX SHA256 `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`, deploy config SHA256 `d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d`.

입력 원본 SHA256:
- 17:44:21 bag DB3 `0988f6b9dcc05cebdf7f85ce940be26cd4bf32c490e2e738a69e189f51db2118` (출처: [motor feedback 보고서](flashsac_60000_motor_feedback_report.md))
- `signals.npz` `306265894d6b945c9f696dd04303496259b7c86c55a0d3f0d45dba5a9c4af842`
- `metrics.json` `74bca80848f6aff5ec63f9c6ccdd3e9e47939fe248d4eede378b3d61d995bf00`
- fit에 쓴 14:11:13 `signals.npz` `2a21626ac6cb041f0a1ad335bea6b0a79c687b3948ba8a0d82d1ff37bea29efb`
- 학습 `env.yaml` `f1796a302b56e74be9ee292c1e35553b048b887bd7c29bb336e4b3099f6bd3a6`

Branch: `agent/codex/dev_tita_gluon`. Commit/push 없음.

## 결론

1. **설정:** 현재 task 설정은 학습 당시 `env.yaml`과 944개 항목에서 같다. 차이 4개는 env 생성 때 채워지는 값이다. 배포 config와 sim2sim export config의 관측·action·PD·clip 정의도 같다. 새 재학습 variant는 **DR event만** 바꾼다. 학습 smoke에서 생성된 `policy_interface.json`과 `action_mapping.json`이 원래 run과 바이트 단위로 같다.
2. **로컬 simulator 의미:** Kp/Kd를 같은 배율로 바꾸는 것은 clip 아래에서만 출력 토크 배율과 같다. Isaac joint `friction`은 docstring의 "단위 없음"과 달리, 이 설치본에서 **N m 단위 Coulomb 마찰**로 동작했다(무부하와 휠 무게 하중 모두). 학습 sim의 관절 armature는 0이고 MuJoCo는 0.01이다.
3. **Holdout:** 17:44:21 명령 시퀀스 재생에서 A/B/C 후보는 nominal보다 대부분의 지표가 훨씬 낫다. 그러나 **사전 기준을 모두 통과한 후보는 없다.** drift는 균형점 오프셋 쪽이, 무릎 자세·토크는 다리 등가 계수 쪽이 주로 설명한다. IMU 오프셋과 CoM은 여전히 구분되지 않는다.
4. **0.6의 의미:** 배율 1.0에 다리 마찰을 16 N m까지 넣어도 실기 자세가 재현되지 않는다. 0.6은 계속 **MuJoCo 등가 계수**로만 유지한다. firmware는 명령 ≈ 보고(≈1.0)를 보였지만 외부 Nm 교정이 없어 물리적 원인은 미식별이다.
5. **현재 정책 기준값:** nominal에서는 zero-command를 통과한다. A/B/C에서는 −0.19~−0.26 m/s 후진하고, **후진 0.6 m/s에서 세 조건 모두 자세 유지 실패**가 났다. nominal에서도 ±0.3 m/s 추종이 비대칭이다.

## 1. 학습 당시 metadata와 현재 설정

| 확인 항목 | 방법 | 결과 |
|---|---|---|
| 현재 task 설정 vs 학습 `env.yaml` | `train.py`와 같은 경로(`parse_env_cfg` → `seed` → `apply_env_cfg` → `dump_yaml`)로 dump 후 leaf 비교 | 944/944 동일. 차이 4개는 prim path 정규식과 terrain `num_envs`/`env_spacing`(런타임에 채움). [diff](flashsac_retrain_prep/config_diff/diff.log) |
| action gain | runner cfg vs checkpoint `action_mapping.json` | 동일 (2.8/2.0/2.8/6.0 ×2) |
| 배포 config vs sim2sim export | 30개 leaf 비교 | 관측 6항목(33차원)·scale·clip, action 8개(다리 위치 ×0.25, 휠 속도 ×20), Kp 60/Kd 1.5, 휠 Kd 0.5, 토크 한도 60/12, 기본 자세, decimation 4 @ 5 ms 모두 동일. 차이는 조이스틱 최대 명령(1.0 vs 0.2/0.3)과 경로뿐 |
| 학습 CLI | `docs/exp/2026-10-15/tita_flash_sac_115632_883848_args.json` | 4096 env, 100k vector step, seed 42, buffer 1M / min 100k, batch 2048, updates/step 2.0, n-step 3, save 5k |

`my_flat_env_cfg.py`는 학습 이후(10/16 11:39)에 수정됐지만 dump 기준으로 설정값은 바뀌지 않았다. 이 파일은 수정하지 않았다(기존 trailing whitespace 포함).

## 2. 구분 가능한 것과 아닌 것

| 요소 | 현재 근거 | 판정 |
|---|---|---|
| 다리 실효 출력 계수 (MuJoCo 등가) | 자세·명령 토크 특징으로 0.55–0.65. 50k 체크포인트와 17:44 holdout에서도 무릎 자세·토크를 재현 | **sim 등가 계수로는 식별됨.** 물리 원인은 미식별. 후보: Nm 교정 오차(명령과 firmware 추정이 Kt를 공유할 가능성), 링크 질량·관성·기하 오차, 하중 의존 마찰 |
| 배율 1.0 + 큰 다리 마찰 | 마찰 8/10/12/16 N m에서 최소 loss 76.8/75.2/74.8/76.7 (무릎 −1.79 vs 실기 −2.15, 토크 17 vs 29 N m). [log](real2sim_leg_wheel_grid/grid_c_gain1.log) | 이 모델 계열에서는 대안이 되지 않음 |
| 다리 Coulomb 마찰 | 2–6 N m에서 loss 비슷 | 약하게 식별. 배율과 일부 상쇄 |
| 휠 Coulomb 마찰 | 0.1–0.4 N m. 정상 휠 토크 특징이 결정하고, 17:44 중립 구간 firmware 휠 보고값도 −0.38/−0.43 N m | 약하게 식별. 휠 gain은 저토크라 결론 불가 |
| IMU pitch 오프셋 vs base CoM x | 1° ≈ 1 cm 대각선 골짜기. holdout에서 IMU형(A)은 segment 속도, CoM형(C)은 중립 drift가 더 잘 맞음 | **구분 불가.** 정적 수평 측정 등 별도 측정 필요 |
| 총질량 | 사용자 측정 25–26 kg ≈ URDF 25.69 kg | 총질량은 일치. 링크별 분포·관성은 미확인 |
| armature / 로터 관성 | Isaac 0, MuJoCo 0.01 kg m² (휠 실효 회전 관성 약 2.4배 차이) | 미식별. sim2sim 불일치로 기록 |
| actuator 지연 | 학습 DR 0–20 ms. real2sim grid에는 미포함 | 미식별 |

### 로컬 simulator 구현 확인 (Isaac Lab v2.3.0 / isaaclab 0.47.2 / Isaac Sim 5.1)

- **PD 토크:** `DelayedPDActuator`는 목표값만 지연시킨 뒤 `IdealPDActuator.compute`에서 `τ = Kp(q*−q) + Kd(q̇*−q̇) + τ_ff`를 계산하고 effort limit으로 clip한다(`actuators/actuator_pd.py`).
  - 같은 배율 k를 Kp·Kd에 곱하면 `|τ| < limit`일 때만 출력 토크 ×k와 같다. 포화 시에는 Isaac이 `clip(k·τ)`, 실제 출력 손실은 `k·clip(τ)`라 다르다.
  - MuJoCo `IdentEnv`는 clip 뒤에 곱하므로 후자에 해당한다.
  - 17:44 run의 RL 다리 명령 최대는 약 42 N m(< 60)이라 정상 운용에서는 차이가 작다.
- **`randomize_actuator_gains`:** 기본 gain에서 출발해 Kp와 Kd를 **env·관절마다 독립으로** 샘플한다(`envs/mdp/events.py:527`). 현재 학습은 둘 다 log-uniform ×0.8–1.2다. 공통 배율을 표현하려면 별도 event가 필요하다.
- **Joint friction:**
  - `actuator_cfg.py` docstring은 static friction을 "unitless, `F_resist ≤ μ·F_spatial`"로 설명한다. Isaac Sim ≥5에서는 PhysX DOF friction 속성 [static, dynamic, viscous]로 기록된다(`articulation.py:827`).
  - [단위 시험](flashsac_retrain_prep/friction_semantics/friction_semantics.json): 학습 task의 TITA를 base 고정·중력 없음으로 놓고, 기본 자세 작성 후 0.1초 안정화했다. 휠에 0.5/1.5/3 N m, μ=0/1/2를 적용했다.
  - 결과: μ=1에서 0.5 N m는 정지, 1.5와 3 N m에서는 마찰 토크 1.000 N m. μ=2에서 0.5와 1.5 N m는 정지, 3 N m에서는 2.000 N m. 실효 휠 관성 0.00639 kg m².
  - [중력 시험](flashsac_retrain_prep/friction_semantics_gravity/friction_semantics.json)(휠 관절이 휠 무게 약 15 N 전달)에서도 1.000/2.000 N m로 같았다.
  - 따라서 이 설치본에서는 N m 단위 Coulomb 마찰로 다룬다. 로봇 전체 하중이 걸리는 무릎 조건은 미시험이다.
- **`randomize_joint_parameters`:** Isaac Sim ≥5에서 static·dynamic·viscous 마찰을 **같은 분포로** 함께 샘플한다(dynamic ≤ static으로 clamp). 휠에 쓰면 viscous 감쇠가 의도치 않게 커지므로 사용하지 않고 별도 event를 만들었다.
- **Armature:** 학습 USD의 관절 armature는 모두 0이다(`get_dof_armatures`). sim2sim MuJoCo 모델(`mujoco_corrected/scene.xml`)은 모든 관절에 0.01이다.

## 3. Holdout — 17:44:21 명령 시퀀스 재생

- **목적:** 14:11:13 자유 drift run으로 맞춘 후보를 이번 run 전체로 검증한다. 인접 frame을 무작위로 나누거나 재fitting하지 않았다.
- **재생 방식:** 실기 RL frame k의 명령을 sim policy tick k에 그대로 넣었다(재생 오차 2.96e−8).
- **사전 고정:** 지표와 기준은 실행 전에 [protocol](flashsac_retrain_prep/holdout_174421/holdout_protocol.json)으로 고정했다(SHA256 `eefa702dd43c0d598c469442b754ad8a61c54d8e4543c1b6d873f6b204fc8e18`).
- **비교 기준:** 실기 속도는 FK 추정(외부 GT 없음), sim 속도는 MuJoCo GT다. 토크는 양쪽 모두 명령 PD 토크다.
- **결과 파일:** [metrics](flashsac_retrain_prep/holdout_174421/holdout_metrics.json), [시계열](flashsac_retrain_prep/holdout_174421/holdout_timeseries.png).

| 후보 | segment 속도 MAE | RMSE 속도 / yaw / pitch / 무릎 q / 무릎 τ | 중립(7.71–9.25 s) 속도 sim/실기 | 무릎 q | 무릎 τ | pitch | 사전 기준 |
|---|---:|---|---:|---:|---:|---:|---|
| nominal | 0.202 | 0.220 / 0.059 / 2.58 / 0.312 / 10.9 | +0.043 / −0.207 | −1.848 / −2.116 | 17.2 / 27.4 | 4.19 / 1.33 | 불통과 |
| A IMU +2° | **0.057** | 0.133 / 0.091 / 1.57 / 0.048 / 2.75 | −0.346 / −0.207 | −2.162 | 31.6 | 0.69 | 불통과 (중립 속도, 무릎 τ) |
| B CoM −1 cm + IMU +1° | 0.062 | 0.139 / 0.085 / 1.55 / **0.045** / 2.46 | −0.299 / −0.207 | −2.157 | 31.1 | 0.85 | 불통과 (중립 속도) |
| C CoM −2 cm | 0.084 | 0.157 / 0.071 / 1.68 / 0.048 / **2.38** | **−0.258** / −0.207 | −2.156 | 30.6 | 1.12 | 불통과 (segment MAE 0.084 > 0.08) |
| D IMU +2°만 (다리 nominal) | 0.058 | **0.098** / 0.058 / 1.77 / 0.353 / 11.2 | −0.146 / −0.207 | −1.805 | 16.9 | 2.47 | 불통과 |
| E 다리 계수·마찰만 | 0.115 | 0.179 / 0.063 / 2.57 / 0.093 / 3.49 | +0.001 / −0.207 | −2.206 | 30.4 | 4.84 | 불통과 |

모든 행에서 마찰 조건은 다리 2 N m, 휠 0.3 N m이고, A/B/C/E의 다리 계수는 0.6이다.

- **결과 요약:** A/B/C는 nominal 대비 segment 속도 오차를 58–72%, 무릎 q RMSE를 85% 줄였다.
- **남은 오차:** 중립 후진을 0.05–0.14 m/s 과대 예측한다. 무릎 토크는 약 3–4 N m 높다. yaw RMSE는 A/B가 nominal보다 약간 나쁘다.
- **분해:** D는 속도만, E는 자세만 맞춘다. 두 메커니즘이 모두 필요하다는 grid 결론과 같다.
- **Startup (0–1 s) 휠 명령 토크 peak:** 실기 10.84 N m(계산값; firmware 보고 peak −12.95 N m는 [보고서](flashsac_60000_motor_feedback_report.md) 참조), A/B/C 12.0 N m(clip), nominal 7.47 N m. Startup은 정지 평가와 분리해서 다룬다.

## 4. 재학습 설계

원칙:

- **인터페이스 보존:** 관측 33(항목·순서·scale·noise), action 8(scale·offset·piecewise gain), PD, clip, decimation, 기본 자세, startup 상태기계를 바꾸지 않는다.
- **조이스틱 로그로 BC하지 않는다.** 예를 들어 +0.18 m/s 명령에서 속도가 0이던 frame을 command=0으로 재라벨링하지 않는다. 관측에 원래 command와 previous action이 들어 있어서 인과가 깨지기 때문이다. 실기 로그는 real-to-sim fitting과 holdout 검증에만 쓴다.
- **zero-command 안정성과 command 추종을 같은 학습에서 함께 다룬다.** 명령 분포(x U[−1,1], yaw U[−1.5,1.5], standing 10%, ramp 0.5, 초기 2초 zero)와 보상은 R1/R2에서 바꾸지 않는다. 개선 효과를 DR 변경에만 귀속시키기 위해서다.

| Arm | 내용 | 상태 |
|---|---|---|
| R0 | 기존 `tita_flash_sac_115632_883848` (50k/60k/75k) | 기준값. 60k 수용시험 완료 |
| R1 `DDT-Velocity-Flat-Tita-My-Real2Sim-v0` | 다리 Kp·Kd 공통 배율 log-U[0.5, 1.05] × 관절별 ±20% jitter / 다리 Coulomb 마찰 U[0, 4] N m / 휠 마찰 U[0, 0.4] N m (dynamic = static × U[0.8, 1.0], viscous 0) / 휠 gain은 기존 ±20% | **구현·env 검사·smoke PASS**. 전체 학습 미실행 |
| R2 `...-Real2Sim-BaseCom-v0` | R1 + CoM randomization을 base만 x ±3 / y ±2 / z ±3 cm로 제한 (기존: 휠 포함 모든 body ±10 cm) | 구현·설정 diff 확인. 전체 학습 미실행 |
| R1b (제안) | reset 일부(예: 20%)를 sit 자세에서 시작: leg_2 0.9, leg_3 −2.6, hip ∓0.05, 정지, base z는 접지에 맞춰 약 0.18 m. 현재 학습 reset은 기본 자세 ×[0.5, 1.0](무릎 −1.5~−0.75 rad)이라, 실기·sim2sim RL 진입 자세(무릎 ≈ −2.65 rad, base z ≈ 0.18 m)를 학습 중에 본 적이 없다. startup 과도(A/B/C 휠 토크 clip, pitch 9°) 대응용 | 미구현 (접지 높이를 맞춘 reset event 필요) |
| R3 (조건부) | R1/R2가 A/B/C zero-command 기준에 실패할 때만 진행: standing 25–30%, zero-command 시 GT 선속도 L2 패널티, 근영역 추종 kernel | 미구현 (새 보상 코드 필요) |
| R4 (승인 필요) | zero-command 휠 odometry 등 적분 정보 관측 추가 | 인터페이스 변경이라 tita_node와 ONNX 변경, 별도 승인 필요 |

- **DR 범위의 성격:** R1/R2의 범위는 nominal 1.0과 MuJoCo 등가 후보(0.6, 2 N m, 0.3 N m)를 포함하도록 고른 **강건성 탐색 범위**다. 실측 범위가 아니다. 균형점 오프셋(IMU ±2.9°, CoM)은 이미 학습 DR 안에 있는데도 메모리 없는 정책이 상쇄하지 못하므로, R1/R2만으로 해결된다고 가정하지 않는다.
- **학습 설정:** 115632와 같다(4096 env, 100k step, seed 42, 같은 FlashSAC agent cfg). 여력이 있으면 seed 2개.
- **checkpoint 선택:** 40k–100k(10k 간격)를 아래 수용시험(nominal + A/B/C)으로 먼저 고른다. holdout 재생과 14:11 재생은 선택된 checkpoint의 최종 확인과 R0 비교에만 쓴다. 선택이 holdout에 과적합되는 것을 막기 위해서다.
- **추가 out-of-fit 점검:** D, E, 다리 계수 0.8, 마찰 극단 조건.
- **Export 차단 요인:** `lab/ddt_lab/scripts/flash_sac/export.py:36`이 `task == DDT-Velocity-Flat-Tita-My-v0`만 허용한다. R1/R2 정책을 export하려면 같은 33/8 인터페이스의 variant를 허용하는 변경이 필요하다. 배포 경로라 승인 후 진행한다. Export 후에는 기존 Torch↔ONNX·adapter parity 시험과 배포 config 인터페이스 비교를 반복한다.
- **실기:** 별도 operator 승인 후 단계적으로만 진행한다. A/B/C에서 후진 0.6 실패가 있었으므로 초기 후진 명령 상한을 낮게(예: 0.3 m/s) 두는 것을 권한다.

학습 실행 명령 (`TRAINING_SIM`, 실행하지 않음):

```bash
cd lab/ddt_lab
/home/cocel/isaac/env_isaaclab/bin/python -u scripts/flash_sac/train.py \
  --task DDT-Velocity-Flat-Tita-My-Real2Sim-v0 --num_envs 4096 --steps 100000 --seed 42 \
  --device cuda:0 --headless --logger wandb --wandb_project tita_flat_flash_sac --run_name real2sim_R1_s42
```

참고로 2026-10-14 13:32에 시작된 학습 프로세스(PID 3301796, `tita_flash_sac_4096_20261014_133201`)가 3일 넘게 떠 있다. GPU 5.8 GB, 사용률 약 3%다. 사용자 프로세스라 건드리지 않았다.

## 5. 분리 수용시험 — 현재 model_60000 기준값

[protocol](flashsac_retrain_prep/acceptance_model_60000/acceptance_protocol.json)(SHA256 `7454e5d8406e6b6151acfdb8da073f1ae18d0f5fa21c3d94b8fea15cb2da1c83`)은 rollout 전에 고정했다. 기준값은 재학습 정책에 적용할 **제안 gate**다.

- **startup (0–3 s):** 실패 없음, pitch peak ≤ 10°
- **zero-command (5–30 s):** nominal과 A/B/C 모두 |v̄| ≤ 0.03 m/s, |이동| ≤ 0.75 m, pitch std ≤ 1°
- **전후진 (6–13 s 유지):** 추종 오차 ≤ 0.05 m/s(±0.3) / ≤ 0.10 m/s(±0.6). 정지 재진입(18–23 s) |v̄| ≤ 0.05 m/s
- **yaw:** 오차 ≤ 0.05 rad/s, 회전 중 병진 ≤ 0.05 m/s
- **회귀 방지:** 토크 RMS·pitch std는 R0의 1.2배 이하, 휠 clip 비율 ≤ 1%

sim 통과는 실기 성공 근거가 아니다. [metrics](flashsac_retrain_prep/acceptance_model_60000/acceptance_metrics.json)

| 지표 | nominal | A | B | C |
|---|---:|---:|---:|---:|
| zero: v̄ / 이동 / pitch std | **+0.015** / +0.38 m / 0.02° | −0.259 / −6.47 m / 1.06° | −0.215 / −5.36 m / 1.23° | −0.187 / −4.67 m / 1.31° |
| zero: 휠 τ RMS·peak / 다리 τ RMS·peak | 0.12·0.12 / 10.6·17.3 | 0.36·0.73 / 25.9·36.2 | 0.38·0.71 / 27.0·38.0 | 0.40·0.71 / 27.2·38.4 |
| +0.3 / −0.3 m/s → v̄ | +0.221 / −0.470 | +0.136 / −0.535 | +0.126 / −0.491 | +0.181 / −0.462 |
| +0.6 / −0.6 m/s → v̄ | +0.481 / −0.714 | +0.398 / **실패** | +0.408 / **실패** | +0.410 / **실패** |
| 정지 재진입 (+0.3 후 / −0.3 후) | +0.016 / +0.016 | −0.247 / −0.208 | −0.231 / −0.166 | −0.223 / −0.140 |
| yaw ±0.5 → ωz / 회전 중 v̄ | +0.514, −0.462 / +0.013, −0.125 | +0.525, −0.654 / −0.147, −0.223 | +0.522, −0.661 / −0.134, −0.233 | +0.535, −0.669 / −0.120, −0.238 |
| startup 휠·다리 τ peak / pitch peak | 7.47·44.1 / 6.9° | 11.98·58.7 / 9.2° | 12.00·57.2 / 7.8° | 12.00·55.0 / 6.1° |

- **후진 −0.6 실패:** A/B/C에서 base 높이가 약 5초에 걸쳐 0.25 → 0.18 m로 낮아지고 pitch가 +9–10°까지 커지다가 harness 기준(0.18 m)에 걸렸다. 실제 전복까지 갔는지는 단정하지 않는다. 같은 명령에서 nominal은 0.344 m를 유지했다.
- **seed:** seed 104/270의 zero 결과 차이는 0.001 m/s 이하다.
- **nominal의 추종 비대칭(+0.3 → +0.22, −0.3 → −0.47)** 도 재학습 비교 대상이다.

## 한계

- fit은 자유 drift run 하나, holdout은 조이스틱 run 하나다. 두 run 모두 외부 속도 GT가 없다.
- holdout 기준은 손으로 정한 값이다. 기준 불통과는 "이 모델 계열이 이 run을 정해진 정밀도로 재현하지 못함"을 뜻한다. 실기 원인을 반증한 것이 아니다.
- 마찰 단위 시험은 휠 관절, 0.1초, 휠 무게까지의 하중이다. 로봇 전체 하중이 걸리는 무릎, 긴 시간의 stick-slip은 미시험이다.
- 새 task의 효과(정지·추종 개선)는 전체 학습 전이라 **NOT_TESTED**다. smoke는 학습 루프가 도는지만 확인한다.
- 수용시험 gate는 sim 기준이다. 실기 판정은 별도 승인된 재시험에서만 가능하다.

## 변경·검사

신규 파일 (기존 파일 수정 없음, 아래 정정 메모 제외):

- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/real2sim/{__init__.py, env_cfg.py, events.py}` — 새 task 2개 등록. 기존 TITA registry(`robots/tita/__init__.py`)와 `my_flat_env_cfg.py`는 건드리지 않았다.
- `test/diff_flash_env_cfg_vs_checkpoint.py`, `test/isaac_joint_friction_semantics_check.py`, `test/check_real2sim_task_events.py`, `test/real2sim_holdout_replay.py`, `test/flashsac_acceptance_suite.py`.
- `test/real2sim_leg_wheel_grid.py` 확장: 명령 시퀀스 재생, gyro 기록, 3축 명령 ramp up/down. grid 당시 SHA256 `0ff2b2c6…`, 현재 `cb203d46…`.
- 이 보고서와 `flashsac_retrain_prep/` 산출물(11 MB), `real2sim_leg_wheel_grid/grid_c_gain1*`.
- 학습 smoke run `lab/ddt_lab/logs/flash_sac/tita_flash_sac_182811_356859`와 그 evidence(`tita_flash_sac_182811_356859_*`).
- [real2sim grid](real2sim_leg_wheel_grid.md)와 [이전 추천](flashsac_wheel_drift_retrain_recommendations.md) 보고서 상단에 정정 메모를 추가했다(본문·수치·SHA256 보존).

실행한 검사:

- **설정:** dump/diff 3회 PASS (원 task 944/944; R1·R2는 의도한 event 항목만 변경, action gain 동일).
- **마찰 단위 시험:** 2회 PASS.
- **새 task env 검사:** PASS. [event_check](flashsac_retrain_prep/event_check_Real2Sim/event_check.json): 다리 Kp 배율 0.402–1.241, 관절 간 log 상관 0.770(이론 약 0.77), 휠 Kd 0.80–1.20, 마찰 범위, dynamic ≤ static, viscous 0, 관측 33/critic 36/action 8, 20 step 유한.
- **학습 smoke:** PASS (4 env, 8 step, update 6회, exit 0; [log](flashsac_retrain_prep/real2sim_train_smoke.log)). `policy_interface.json`·`action_mapping.json`이 115632와 바이트 단위로 동일.
- **VALIDATION_SIM:** holdout 6/6 실행(사전 기준 0/6 통과), 수용시험 32회 실행(후진 0.6 A/B/C 3회 harness 실패), 배율 1.0 대안 grid 144/144 PASS.
- **재현성:** 확장된 grid 스크립트로 grid A 1000회를 재실행했다. 이전 결과와 특징값 최대 차이 0.0, 상태 변화 0건이다. [log](flashsac_retrain_prep/grid_a_recheck_extended_script.log)
- **`./scripts/agent-check.sh`:** [log](flashsac_retrain_prep/agent_check.log).

하지 않은 것: 전체 재학습, export.py 변경, 정책 export·배포, 실기 실행, 모터·제어 gain 변경, commit/push.

## 재현

```bash
# TRAINING_SIM (설정/시뮬레이터 확인)
P=/home/cocel/isaac/env_isaaclab/bin/python
$P test/diff_flash_env_cfg_vs_checkpoint.py --run lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848 \
  --task DDT-Velocity-Flat-Tita-My-Real2Sim-v0 --output <dir>
$P test/isaac_joint_friction_semantics_check.py [--gravity] --output <dir>
$P test/check_real2sim_task_events.py --output <dir>
# VALIDATION_SIM (MuJoCo)
M=/home/cocel/venvs/cosim_ros2_jazzy/bin/python
cd test && $M real2sim_holdout_replay.py && $M flashsac_acceptance_suite.py
```
