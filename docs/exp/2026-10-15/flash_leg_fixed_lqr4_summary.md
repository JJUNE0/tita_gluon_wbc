# E — FlashSAC Leg + Fixed 4-State LQR Wheel

Execution Domain: VALIDATION_SIM (파일·경로 검사: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: FAIL — E의 제어 성능. 구현·경로·baseline 재현 및 결과 무결성 검사는 PASS.

Observed Metrics / Behavior / Log Summary:

**기존 FlashSAC leg 경로를 보존하고 wheel 토크만 C-4로 교체한 E는 안정적인 zero-command 제어를 달성하지 못했다.** 전체 E 81회 중 81회 실패했다. Nominal E 종료 시각은 0.54–0.64초였다. 완료 전 drift가 작아 보이더라도 12초 완료한 A/C-4보다 좋은 결과로 해석하지 않는다.

## 적용 경로와 last_action

- 지정 model_100000 FlashSAC deterministic actor, 33-value observation, action scale/clip/joint order를 그대로 사용했다.
- Policy는 매 control step 전체 8개 action을 출력한다. 기존 ActionAdapter.compute를 매 physics step 실행한 후 **native wheel torque 2개만** C-4의 u/2로 덮어쓴다. Leg 6개는 A의 position reference·Kp=60/Kd=1.5·effort clipping 경로를 보존한다.
- 기존 wheel velocity target→Kd=0.5 PD 출력은 계산되지만 실제 적용하지 않는다. LQR torque 뒤에 wheel velocity PD를 다시 더하거나 torque를 velocity reference로 바꾸지 않는다.
- `last_action`에는 A와 동일하게 **직전 전체 raw actor output**을 넣는다. 미적용 wheel 출력도 포함하며 wheel 채널을 0으로 만들거나 torque 단위를 policy action에 넣지 않는다.
- 따라서 E의 last_action wheel 채널은 실제 실행된 wheel command와 다르다. 이는 정책의 내부 action history 의미는 보존하지만 실제 action/state 대응을 바꾸는 조합이다.
- Wheel 변화로 이후 joint velocity/gravity/actor output도 달라진다. “Leg 경로 보존”은 동일 observation/action에 대한 변환·PD가 같다는 뜻이며, E와 A rollout의 leg action 수치가 항상 같다는 뜻은 아니다.
- Audit: leg torque 차이 0.0, last_action observation 차이 0.0, wheel 교체 최대 오차 4.77e-07 Nm(float32 반올림). RLS transition/update 호출은 0.
- 별도 inference로 같은 observation에서 이전 wheel action history만 0으로 바꿔 leg 출력 변화를 측정했다. 이 counterfactual 출력은 실제 제어에 적용하지 않았다.
- Nominal에서 이 leg action 변화 RMS의 trial 평균은 0.2442(native policy action 단위)이다. 대표 trial RMS 0.2209, 최대 0.9906. 현재 leg action scale 0.25를 적용하면 대표 최대 target 변화는 약 0.2476 rad이다. 미적용 wheel history가 leg inference에 영향을 주는 것은 확인됐지만, 이것만이 실패 원인이라는 증거는 아니다.

## 동일 초기 조건의 A/C-4/E 비교

- 9 조건 × 3 seeds × 3 pitch × 3군 = 243회. Nominal + 기존 8 mismatch를 재사용했다.
- Seed=42/43/44, pitch perturbation −0.035/0/+0.035 rad, 같은 seed별 초기 velocity·접지 높이·roll·stand pose. A/C-4 162회는 기존 archive의 state·wheel torque·world axle position·leg error와 정확히 일치했다.
- Zero command, episode 최대 12초, control dt=0.02/physics dt=0.005 s, 3초의 12 N/0.1 s 외란 모두 동일하다. 3초 전에 실패한 E trial은 이 외란이 적용되기 전에 종료됐다.
- C-4와 E의 K₀, Q4=[1,2,200,5], R=0.1, sensor estimator·IMU cache timing·nominal equilibrium·24 Nm 합 토크·120 Nm/s slew를 유지했다.
- C-4의 fixed leg PD는 기존 360/12이고 E는 A의 FlashSAC leg PD 60/1.5이다. 이 차이는 요청한 ablation의 일부이며, E에서 다리를 고정하거나 gain을 재튜닝하지 않았다.

| 조건 | 군 | 완료/전체 | 실패율 | 최대 planar drift m | pitch error RMS rad |
|---|---|---:|---:|---:|---:|
| nominal | A | 9/9 | 0.0% | 0.497 ± 0.018 | 0.094 ± 0.000 |
| nominal | C-4 | 9/9 | 0.0% | 0.605 ± 0.002 | 0.024 ± 0.000 |
| nominal | E | 0/9 | 100.0% | N/A | N/A |
| mass_1.15 | A | 9/9 | 0.0% | 0.650 ± 0.013 | 0.104 ± 0.000 |
| mass_1.15 | C-4 | 9/9 | 0.0% | 0.092 ± 0.008 | 0.005 ± 0.001 |
| mass_1.15 | E | 0/9 | 100.0% | N/A | N/A |
| mass_1.30 | A | 9/9 | 0.0% | 0.239 ± 0.010 | 0.118 ± 0.000 |
| mass_1.30 | C-4 | 9/9 | 0.0% | 0.430 ± 0.002 | 0.017 ± 0.000 |
| mass_1.30 | E | 0/9 | 100.0% | N/A | N/A |
| gain_0.8 | A | 9/9 | 0.0% | 0.437 ± 0.018 | 0.095 ± 0.000 |
| gain_0.8 | C-4 | 9/9 | 0.0% | 0.601 ± 0.002 | 0.024 ± 0.000 |
| gain_0.8 | E | 0/9 | 100.0% | N/A | N/A |
| gain_1.2 | A | 9/9 | 0.0% | 0.535 ± 0.019 | 0.094 ± 0.000 |
| gain_1.2 | C-4 | 9/9 | 0.0% | 0.608 ± 0.002 | 0.024 ± 0.000 |
| gain_1.2 | E | 0/9 | 100.0% | N/A | N/A |
| lag_0.02 | A | 9/9 | 0.0% | 0.093 ± 0.030 | 0.099 ± 0.000 |
| lag_0.02 | C-4 | 9/9 | 0.0% | 0.605 ± 0.002 | 0.024 ± 0.000 |
| lag_0.02 | E | 0/9 | 100.0% | N/A | N/A |
| lag_0.05 | A | 9/9 | 0.0% | 0.787 ± 0.054 | 0.106 ± 0.001 |
| lag_0.05 | C-4 | 9/9 | 0.0% | 0.605 ± 0.002 | 0.025 ± 0.000 |
| lag_0.05 | E | 0/9 | 100.0% | N/A | N/A |
| friction_0.2 | A | 9/9 | 0.0% | 0.346 ± 0.013 | 0.092 ± 0.000 |
| friction_0.2 | C-4 | 9/9 | 0.0% | 0.644 ± 0.002 | 0.023 ± 0.000 |
| friction_0.2 | E | 0/9 | 100.0% | N/A | N/A |
| friction_0.8 | A | 9/9 | 0.0% | 0.484 ± 0.018 | 0.094 ± 0.000 |
| friction_0.8 | C-4 | 9/9 | 0.0% | 0.605 ± 0.002 | 0.024 ± 0.000 |
| friction_0.8 | E | 0/9 | 100.0% | N/A | N/A |

평균 ± sample 표준편차는 12초를 완료한 trial만 포함한다. E의 N/A는 미측정이 아니라 완료 trial이 없어서 동일 horizon 통계를 계산하지 않았다는 뜻이다. 종료 전 metric은 results.jsonl/metrics.csv에 별도 남겼다.

## 실패와 해석

정확한 실패 사유 분포: `{'pitch_error_limit': 71, 'joint_limit:joint_left_leg_3': 6, 'pitch_error_limit;joint_limit:joint_right_leg_3': 4}`. 대표 seed42/pitch0 E는 0.62초에 pitch error limit를 넘었다. Raw action/observation/history, discarded wheel PD torque, 실제 command/motor substeps, joint position/velocity/limit margin, K, CoM과 종료 snapshot은 각 NPZ에 있다.
- Nominal E의 body-frame CoM 변화 최대값 평균은 0.01124 m이다. 대표 E는 0.01216 m이며 기존 대표 C-4는 약 0.000365 m였다. E는 FlashSAC가 leg pose를 바꾸므로 고정 leg pose를 가정한 nominal WIP 모델의 조건이 유지되지 않는다.
- 기존 FlashSAC는 wheel velocity PD와 leg action을 함께 학습했다. Wheel을 별도 LQR로 바꾸면 wheel 응답·leg/wheel coordination·history/state 관계가 변한다. Leg 경로가 보존됐다는 사실만으로 혼합 loop의 안정성을 보장할 수 없다.
- 이 결과만으로 FlashSAC leg 자체나 Fixed LQR 자체가 나쁘다고 판단하지 않는다. E 조합은 실패했지만 같은 초기 조건의 A와 C-4는 완료했다.
- Ground-truth control, gyro 동기화, pitch 기준 수정, last_action 변경, gain tuning은 이번 E에서 수행하지 않았다: NOT_TESTED. 이 요인들의 기여를 분리한 실패 원인 확정은 아직 남아 있다.

## 검증·변경 범위·재현

- 기존 코드·설정·보고서는 변경하지 않았다. 신규 `test/eval_flash_leg_fixed_lqr4.py`, `test/test_flash_leg_fixed_lqr4.py`, `test/analyze_flash_leg_fixed_lqr4.py`와 이 실험 증거만 추가했다.
- Actor/observation/last_action 동등성과 wheel-only 교체 테스트 2개 PASS (`unit_tests.log`). 243개 episode의 gain 고정·history·leg torque·초기 상태 및 162개 archive 재현 audit PASS (`full/integrity.json`).
- `./scripts/agent-check.sh` PASS (Python syntax 333개, URDF XML 8개). 기존 파일 hash 보존 및 최종 diff 검사 기록도 실험 폴더에 있다.
- 브랜치: `agent/codex/dev_tita_gluon`. Hardware 실행·정책 재학습·online adaptation은 수행하지 않았다.

```bash
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_flash_leg_fixed_lqr4.py
MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_flash_leg_fixed_lqr4.py --output docs/exp/2026-10-15/new_e/full
MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_flash_leg_fixed_lqr4.py --results docs/exp/2026-10-15/new_e/full --report docs/exp/2026-10-15/new_e_summary.md
```

산출물: `full/results.jsonl`, `metrics.csv`, `aggregates.json`, `comparison.png` (nominal seed42, pitch perturbation −0.035 rad), 각 episode NPZ와 `integrity.json`.
