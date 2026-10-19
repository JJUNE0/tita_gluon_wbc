# FlashSAC zero-command wheel drift — 재학습용 reward/DR 개선안

Execution Domain: DESKTOP_DRY_RUN (기존 실기 bag NPZ·MuJoCo rollout NPZ·학습 env.yaml 오프라인 재집계). 새 시뮬레이션·로봇 실행·학습 없음.

Evidence Status: **PASS** — 기존 기록에서 자세·PD 토크·drift 재집계. **SUSPICIOUS** — 아래 원인 해석(다리 구동 모델 gap → 평형 자세 이동 → wheel drift). 제안의 효과는 **NOT_TESTED**.

Policy Checkpoint SHA256 (run `0r5o1bmm` = `tita_flash_sac_115632_883848`):
- A/60000 `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`
- A/50000 `d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c`
- A/75000 `381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730`

Branch: `agent/codex/dev_tita_gluon`

> **후속 정정:** 아래의 "실기 관절이 명령 토크보다 정적으로 약하다"는 가설은 이후 [firmware 보고 토크](flashsac_60000_motor_feedback_report.md)(hip·무릎 reported/command ≈ 0.999)로 지지되지 않았다. 다만 외부 Nm 교정은 아직 없다. 현재 해석과 재학습 설정은 [real2sim grid](real2sim_leg_wheel_grid.md)와 [재학습 준비](flashsac_retrain_prep.md)를 따른다.

## 관측 요약

[analysis.log](flashsac_wheel_drift_retrain_recommendations/analysis.log) (RL+5초 이후, 정확히 zero command; sim은 5–10초). 토크는 계산된 PD 명령이며 실측 모터 토크가 아니다.

| 기록 | drift (m/s) | 무릎 leg_3 (rad) | 무릎 PD 토크 (N m) | hip leg_1 (rad) | hip PD 토크 (N m) |
|---|---:|---:|---:|---:|---:|
| sim 60k nominal | +0.015 | −1.85 | +17 | ≈0 | ±6 |
| sim 60k CoM 뒤 + 질량 15% | −0.101 | −1.96 | +20 | ≈0 | ±5 |
| 실기 60k 자유 drift | −0.190 | −2.15 | +28~30 | ±0.12 | ±35 |
| 실기 50k OFF | −0.127 | −2.29 | +29~30 | ±0.08 | ±28 |
| 실기 75k OFF | −0.242 | −2.07 | +26~29 | ±0.12 | ±34 |

- 세 체크포인트 모두 실기에서 후진 drift가 있다. 체크포인트 선택이 아니라 정책 계열 공통의 sim2real gap이다.
- sim2sim과 실기는 같은 웅크린 자세(무릎 ≈ −2.7 rad)에서 RL에 진입한다. sim은 0.5초 안에 무릎을 −1.85까지 펴고 높이 0.337 m를 유지한다. 실기는 −2.1~−2.3에서 멈춘다. 초기조건이 아니라 구동/부하 모델 차이를 가리킨다.
- URDF 질량(25.69 kg)으로 계산한 무릎 정적 부하 상한은 휠당 축하중 111 N × shank 0.2 m ≈ 22 N m다. 실기 계산 토크 25–30 N m는 이를 넘는다. 따라서 실기 관절이 명령 토크보다 정적으로 약하거나(토크 상수·전류 제한·마찰), 실기가 URDF보다 무겁다(≥ 약 34 kg). 어느 쪽인지는 이 자료로 구분할 수 없다.
- hip은 PD 목표(L −0.46 / R +0.45 rad)의 반대쪽으로 서서히 벌어진다(±0.03 → ±0.12 rad). 토크 변화와 관절 가속도 변화의 상관은 네 run 모두 양수(+0.1~+0.8)라 단순 토크 부호 반전은 지지되지 않는다.
- sim에서 질량 증가 조건은 실기와 같은 방향의 추세를 보인다: 무릎이 더 굽고, 무릎 토크가 커지고, drift가 후진 쪽이다. 실기는 그 연장선에 있다. 이것은 추세의 일치이지 인과의 증명이 아니다.

## 학습 설정에서 확인한 gap (env.yaml)

- 다리·휠 actuator: `DelayedPDActuator`, friction 0, armature 없음. DR은 Kp/Kd를 각각 독립적으로 ×0.8–1.2만 변경한다.
- 질량: base_link에 −0.5~+2 kg만 더한다(전체 −2~+8%). MuJoCo 질량 +15/+30% 시험은 학습 분포 밖이다.
- CoM: 모든 body(휠 포함)에 x/y/z ±0.1 m. 휠 반경은 0.0925 m라 휠 CoM이 바퀴 밖까지 이동한다.
- 관측: actor 33차원 중 병진 속도 정보는 휠 각속도뿐이다. 그런데 joint_vel 노이즈 U(±1.5) rad/s(±0.139 m/s 상당)가 휠에도 들어간다. 실기 자유 drift 5–10초 구간의 휠 속도 전체 표준편차(실제 움직임 포함)는 0.37–0.42 rad/s다.
- Zero command 노출: `rel_standing_envs=0.1`과 reset 후 2초뿐이다. `ZeroCommandPositionDrift`는 exp(−8·d) 형태라 0.5 m 이상 이탈하면 거의 0이 되어 gradient가 사라진다.
- sim에서도 저속 추종 오차가 크다: +0.1 m/s 명령에 약 +0.27 m/s ([hardware candidates](flashsac_hardware_candidates.md)).

## 개선안 (우선순위 순, 모두 actor 입출력 33/8 유지)

1. **다리 구동 강도·마찰 DR**: Kp와 Kd를 같은 factor로 묶어 토크 스케일 0.6–1.1로 randomize한다. 다리 관절 정적 마찰도 추가한다. 범위는 먼저 실기 정지 자세를 재현하는 sim 파라미터를 찾아 그 주변으로 잡는다.
2. **질량·CoM 범위 재설계**: base 질량을 −1~+5 kg로 넓힌다. CoM은 base만 x ±3 cm, z ±3 cm, y ±2 cm로 하고, 다리는 ±1 cm, 휠은 0으로 한다. 실기 무게를 측정하고 URDF에 없는 탑재물이 있는지 확인한다.
3. **휠 구동 모델 DR**: 휠 Coulomb/viscous 마찰과 armature를 추가하고, 토크 스케일 0.7–1.1을 좌우 독립으로 둔다. 실기 drift 중 −0.3~−0.6 N m의 정상 토크가 필요한 것은 구동계 저항이 있다는 뜻이다.
4. **휠 속도 관측 노이즈 분리**: joint_vel 항은 하나로 유지하고 관절별 노이즈 벡터를 쓴다. 다리 ±1.5, 휠 ±0.3~0.5 rad/s. 관측 순서가 같으므로 배포 인터페이스는 바뀌지 않는다.
5. **Zero-command reward 보강**: `rel_standing_envs`를 0.25–0.3으로 올리고, 0.2 m/s 이하 저속 명령 샘플을 늘린다. Zero command일 때 GT 선속도 L2 패널티(−w·‖v_xy‖²)를 추가해 위치 exp 항의 포화를 보완한다. 근영역 추종 kernel(std ≈ 0.1)도 추가한다.

reward만으로는 메모리 없는 정책의 정상상태 오차를 없앨 수 없다. 학습 분포 밖의 실기 mismatch에는 DR이 우선이다. 그래도 drift가 남으면 zero-command 구간의 휠 odometry 변위를 관측에 추가해 적분 정보를 주는 방안을 검토한다. 이 방안은 tita_node와 ONNX 인터페이스 변경이 필요하고 별도 배포 승인이 필요하다.

## 검증 제안

- Real-to-sim: 토크 스케일 {1.0, 0.8, 0.65}, 질량 {1.0, 1.15, 1.3}, 휠 마찰 {0, 0.2} grid에서 실기 정지 자세(무릎 −2.1~−2.3, 무릎 토크 25–30 N m)를 재현하는 조합을 찾는다.
- 재학습 정책의 합격 기준: 같은 grid 전체에서 zero-command |v| ≤ 0.03 m/s. 기존 hardware candidates의 명령 추종 screen도 함께 통과해야 한다.

## 변경·검사

- 신규 [분석 스크립트](../../../test/sim2real/summarize_real_vs_sim_stance.py)와 이 보고서, 분석 로그. 제어 코드·학습 설정·정책·배포는 변경하지 않았다.
- `./scripts/agent-check.sh` 결과는 [agent_check.log](flashsac_wheel_drift_retrain_recommendations/agent_check.log)에 있다.
