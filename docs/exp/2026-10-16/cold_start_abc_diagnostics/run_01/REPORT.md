# model_60000 — Cold-start 위치·입력 정보량·Target Offline 식별 A/B/C

작성일: 2026-10-16 (Asia/Seoul)

Execution Domain: **VALIDATION_SIM** (분석: **DESKTOP_DRY_RUN**)

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

Evidence Status: 단계별 PASS/FAIL/NOT_TESTED를 아래에 구분한다. 새 제어기·gain·GT 피드백·Phase D/E/F는 **NOT_TESTED**.

Observed Metrics / Behavior / Log Summary:

기존 run_05 전체 증거와 source를 보호했다. A는 원래 입력의 exact replay이고 센서 FK 보정은 오프라인 진단값이다. C의 Target은 첫 physics 이전에 설정하고 종료까지 고정했다. Offline 모델은 진단용으로만 저장했으며 제어에는 사용하지 않았다.

## Phase A — 기준점 이동과 센서만의 보정

`p_base_diagnostic = p_encoder − sum[delta(R_IMU*d_FK(q)) dot f_mid]`. 관절각과 IMU만 사용하는 함수이며 GT는 결과 검증에만 사용한다. leg·roll/pitch·yaw 항의 합은 대칭 곱 분해로 각20ms 구간에서 정확히 닫힌다. 속도는 gyro×offset 및 leg FK Jacobian 항을 원래 rolling 속도에서 뺀다.

| Target | 군 | 시각 s | 기존 sensor−base mm | 보정 후 mm | leg mm | roll/pitch mm | yaw mm |
|---|---|---:|---:|---:|---:|---:|---:|
| gain0.8 | Fixed | 1 | -23.858 | 4.4078 | -22.199 | -6.0609 | 0.0027632 |
| gain0.8 | Fixed | 5 | -25.918 | 4.4358 | -24.939 | -5.4254 | -0.0088637 |
| gain0.8 | Fixed | 10 | -25.9 | 4.4521 | -24.995 | -5.369 | -0.022321 |
| friction0.8 | Fixed | 1 | -24.418 | 4.2794 | -23.766 | -4.9533 | 0.0084241 |
| friction0.8 | Fixed | 5 | -26.023 | 4.3204 | -26.116 | -4.2243 | -0.0082039 |
| friction0.8 | Fixed | 10 | -26.002 | 4.3599 | -26.198 | -4.1401 | -0.027495 |
| friction0.2 | Fixed | 1 | -30.693 | -2.4705 | -23.643 | -4.5722 | -0.0068998 |
| friction0.2 | Fixed | 5 | -32.813 | -2.3033 | -27.268 | -3.1092 | -0.13258 |
| friction0.2 | Fixed | 10 | -32.884 | -2.2089 | -27.322 | -3.0552 | -0.29812 |
| gain1.2 | Fixed | 1 | -24.413 | 4.1351 | -24.572 | -3.9486 | 0.0037701 |
| gain1.2 | Fixed | 5 | -26.204 | 4.1342 | -27.45 | -2.8802 | -0.0076483 |
| gain1.2 | Fixed | 10 | -26.226 | 4.1275 | -27.488 | -2.8144 | -0.02072 |
| lag0.02 | Fixed | 1 | -26.029 | 4.5903 | -26.21 | -4.4121 | 0.0034782 |
| lag0.02 | Fixed | 5 | -25.726 | 4.6081 | -26.343 | -3.9817 | -0.0089504 |
| lag0.02 | Fixed | 10 | -25.728 | 4.6162 | -26.417 | -3.9039 | -0.023205 |
| nominal | Fixed | 1 | -24.343 | 4.2531 | -23.919 | -4.7159 | 0.0029581 |
| nominal | Fixed | 5 | -26.086 | 4.2581 | -26.538 | -3.8028 | -0.007716 |
| nominal | Fixed | 10 | -26.104 | 4.254 | -26.569 | -3.7705 | -0.020013 |

transform_up 중에는 원래 runtime odometry가 아직 초기화되지 않았다. 저장된 startup qpos/qvel로 복원한 센서 odometry는 **별도 오프라인 stream**이며 기존 RL 목표에 이어 붙이지 않았다. 첫 기록은 startup 첫20ms 후이며 그 이전 이동을 측정했다고 주장하지 않는다. 보정 후 남은 오차는 기존 encoder와 wheel midpoint의 차이 및 FK/이산화 오차다. 이를 전부 slip이라고 부르거나 base GT 유지 해결로 일반화하지 않는다.

## Phase B — 포화 제외와 정보량

raw feedback, probe, bias를 합친 pre_global_clip → absolute band/ramp/slew 후 requested → native wheel clipping 후 actual_u를 구분했다. `actual_u`는 알려진 software 추가 명령이다. gain/lag 이후의 physical_motor는 FlashSAC를 포함한 전체 토크이며 분리된 실제 residual로 취급하지 않는다.

| Stage / Target / 군 | 필터 | transition 중앙값 | rank | condition | innovation % | B 오차 %, 검증 가능한 경우 |
|---|---|---:|---:|---:|---:|---:|
| shadow/friction0.8/KOnly | all_after1s | 2950 | 25 | 5.1851e+05 | 0.15718 | N/A |
| shadow/friction0.8/KOnly | unsaturated_after1s | 485 | 25 | 3.379e+06 | 1.4663 | N/A |
| shadow/friction0.8/KOnly | deployed_eligibility | 485 | 25 | 3.379e+06 | 1.4663 | N/A |
| shadow/gain1.2/KOnly | all_after1s | 2950 | 25 | 5.932e+05 | 0.05865 | N/A |
| shadow/gain1.2/KOnly | unsaturated_after1s | 121 | 25 | 3.871e+06 | 1.7883 | N/A |
| shadow/gain1.2/KOnly | deployed_eligibility | 122 | 25 | 3.5885e+06 | 1.7883 | N/A |
| shadow/nominal/KOnly | all_after1s | 2950 | 25 | 4.0073e+05 | 0.2615 | N/A |
| shadow/nominal/KOnly | unsaturated_after1s | 636 | 25 | 6.3318e+05 | 1.6855 | N/A |
| shadow/nominal/KOnly | deployed_eligibility | 636 | 25 | 6.3318e+05 | 1.6855 | N/A |
| shadow/gain0.8/KOnly | all_after1s | 2950 | 25 | 3.2642e+05 | 0.16844 | N/A |
| shadow/gain0.8/KOnly | unsaturated_after1s | 230 | 25 | 9.1063e+05 | 3.8291 | N/A |
| shadow/gain0.8/KOnly | deployed_eligibility | 230 | 25 | 9.1063e+05 | 3.8291 | N/A |
| shadow/lag0.02/KOnly | all_after1s | 2950 | 25 | 3.6549e+05 | 0.11887 | N/A |
| shadow/lag0.02/KOnly | unsaturated_after1s | 251 | 25 | 2.5396e+06 | 1.5607 | N/A |
| shadow/lag0.02/KOnly | deployed_eligibility | 251 | 25 | 2.5396e+06 | 1.5607 | N/A |
| shadow/friction0.2/KOnly | all_after1s | 2950 | 25 | 2.2377e+05 | 0.39062 | 1.4695 |
| shadow/friction0.2/KOnly | unsaturated_after1s | 654 | 25 | 1.0255e+06 | 3.9129 | 2.5831 |
| shadow/friction0.2/KOnly | deployed_eligibility | 655 | 25 | 9.8689e+05 | 3.9172 | 1.904 |
| primary/nominal/E6 | all_after1s | 8950 | 25 | 4.5779e+05 | 0.11922 | N/A |
| primary/nominal/E6 | unsaturated_after1s | 3724 | 25 | 7.7068e+05 | 0.40376 | N/A |
| primary/nominal/E6 | deployed_eligibility | 3724 | 25 | 7.7068e+05 | 0.40376 | N/A |
| primary/nominal/KOnly | all_after1s | 8950 | 25 | 4.5708e+05 | 0.11936 | N/A |
| primary/nominal/KOnly | unsaturated_after1s | 3749 | 25 | 8.0928e+05 | 0.41066 | N/A |
| primary/nominal/KOnly | deployed_eligibility | 3749 | 25 | 8.0928e+05 | 0.41066 | N/A |
| primary/friction0.8/E6 | all_after1s | 8950 | 25 | 5.693e+05 | 0.059562 | N/A |
| primary/friction0.8/E6 | unsaturated_after1s | 3908 | 25 | 1.2799e+06 | 0.16406 | N/A |
| primary/friction0.8/E6 | deployed_eligibility | 3908 | 25 | 1.2799e+06 | 0.16406 | N/A |
| primary/friction0.8/KOnly | all_after1s | 8950 | 25 | 5.693e+05 | 0.059562 | N/A |
| primary/friction0.8/KOnly | unsaturated_after1s | 3908 | 25 | 1.2799e+06 | 0.16406 | N/A |
| primary/friction0.8/KOnly | deployed_eligibility | 3908 | 25 | 1.2799e+06 | 0.16406 | N/A |
| primary/gain1.2/E6 | all_after1s | 8950 | 25 | 6.7147e+05 | 0.022822 | N/A |
| primary/gain1.2/E6 | unsaturated_after1s | 116 | 25 | 3.7247e+06 | 2.203 | N/A |
| primary/gain1.2/E6 | deployed_eligibility | 117 | 25 | 3.5499e+06 | 2.251 | N/A |
| primary/gain1.2/KOnly | all_after1s | 8950 | 25 | 6.7147e+05 | 0.022822 | N/A |
| primary/gain1.2/KOnly | unsaturated_after1s | 116 | 25 | 3.7247e+06 | 2.203 | N/A |
| primary/gain1.2/KOnly | deployed_eligibility | 117 | 25 | 3.5499e+06 | 2.251 | N/A |
| primary/gain0.8/E6 | all_after1s | 8950 | 25 | 3.303e+05 | 0.15119 | N/A |
| primary/gain0.8/E6 | unsaturated_after1s | 4385.5 | 25 | 7.6005e+05 | 0.20229 | N/A |
| primary/gain0.8/E6 | deployed_eligibility | 4385.5 | 25 | 7.6005e+05 | 0.20229 | N/A |
| primary/gain0.8/KOnly | all_after1s | 8950 | 25 | 3.303e+05 | 0.15119 | N/A |
| primary/gain0.8/KOnly | unsaturated_after1s | 4385.5 | 25 | 7.6005e+05 | 0.20229 | N/A |
| primary/gain0.8/KOnly | deployed_eligibility | 4385.5 | 25 | 7.6005e+05 | 0.20229 | N/A |
| primary/lag0.02/E6 | all_after1s | 8950 | 25 | 3.4091e+05 | 0.065587 | N/A |
| primary/lag0.02/E6 | unsaturated_after1s | 3749 | 25 | 1.7006e+06 | 0.10307 | N/A |
| primary/lag0.02/E6 | deployed_eligibility | 3749 | 25 | 1.7006e+06 | 0.10307 | N/A |
| primary/lag0.02/KOnly | all_after1s | 8950 | 25 | 3.4091e+05 | 0.065587 | N/A |
| primary/lag0.02/KOnly | unsaturated_after1s | 3749 | 25 | 1.7006e+06 | 0.10307 | N/A |
| primary/lag0.02/KOnly | deployed_eligibility | 3749 | 25 | 1.7006e+06 | 0.10307 | N/A |
| primary/friction0.2/E6 | all_after1s | 8950 | 25 | 3.4296e+05 | 0.25179 | 2.6853 |
| primary/friction0.2/E6 | unsaturated_after1s | 6654 | 25 | 1.158e+06 | 0.54118 | 5.3553 |
| primary/friction0.2/E6 | deployed_eligibility | 6655 | 25 | 1.1354e+06 | 0.54181 | 4.9745 |
| primary/friction0.2/KOnly | all_after1s | 8950 | 25 | 3.5388e+05 | 0.24695 | 1.0707 |
| primary/friction0.2/KOnly | unsaturated_after1s | 6654 | 25 | 1.3503e+06 | 0.51972 | 2.8501 |
| primary/friction0.2/KOnly | deployed_eligibility | 6655 | 25 | 1.3067e+06 | 0.52073 | 2.7117 |
| composite_shadow/combo_gain_low_friction/KOnly | all_after1s | 2950 | 25 | 3.8466e+05 | 0.93457 | N/A |
| composite_shadow/combo_gain_low_friction/KOnly | unsaturated_after1s | 1248 | 25 | 4.0455e+05 | 4.5912 | N/A |
| composite_shadow/combo_gain_low_friction/KOnly | deployed_eligibility | 1248 | 25 | 4.0455e+05 | 4.5912 | N/A |
| composite_shadow/combo_gain_high_friction/KOnly | all_after1s | 2950 | 25 | 4.0842e+05 | 0.19637 | N/A |
| composite_shadow/combo_gain_high_friction/KOnly | unsaturated_after1s | 506 | 25 | 3.1522e+06 | 1.679 | N/A |
| composite_shadow/combo_gain_high_friction/KOnly | deployed_eligibility | 506 | 25 | 3.1522e+06 | 1.679 | N/A |
| composite_primary/combo_gain_low_friction/E6 | all_after1s | 8950 | 25 | 3.7225e+05 | 0.30468 | N/A |
| composite_primary/combo_gain_low_friction/E6 | unsaturated_after1s | 4000.5 | 25 | 5.3281e+05 | 1.0327 | N/A |
| composite_primary/combo_gain_low_friction/E6 | deployed_eligibility | 4000.5 | 25 | 5.3281e+05 | 1.0327 | N/A |
| composite_primary/combo_gain_low_friction/KOnly | all_after1s | 8950 | 25 | 3.9652e+05 | 0.31253 | N/A |
| composite_primary/combo_gain_low_friction/KOnly | unsaturated_after1s | 4141 | 25 | 5.8063e+05 | 1.1451 | N/A |
| composite_primary/combo_gain_low_friction/KOnly | deployed_eligibility | 4141 | 25 | 5.8063e+05 | 1.1451 | N/A |
| composite_primary/combo_gain_high_friction/E6 | all_after1s | 8950 | 25 | 4.244e+05 | 0.064733 | N/A |
| composite_primary/combo_gain_high_friction/E6 | unsaturated_after1s | 2551 | 25 | 8.3284e+05 | 0.2728 | N/A |
| composite_primary/combo_gain_high_friction/E6 | deployed_eligibility | 2551 | 25 | 8.3284e+05 | 0.2728 | N/A |
| composite_primary/combo_gain_high_friction/KOnly | all_after1s | 8950 | 25 | 4.2585e+05 | 0.064641 | N/A |
| composite_primary/combo_gain_high_friction/KOnly | unsaturated_after1s | 2555.5 | 25 | 8.5618e+05 | 0.27184 | N/A |
| composite_primary/combo_gain_high_friction/KOnly | deployed_eligibility | 2555.5 | 25 | 8.5618e+05 | 0.27184 | N/A |

`all_after1s`와`unsaturated_after1s`는 같은 시간 기준이다. deployed_eligibility는 실제 과거 learner의 필터와 일치함을 A/B/c로 재검사했다. 포화 제거는 표본과 excitation도 제거할 수 있어 condition이 반드시 좋아지는 것은 아니다. Direct B가 없는 환경의 B 정확도는NOT_TESTED다.

## Phase C — 같은 데이터의 Offline LS와 RLS

학습 seed720/721/722, 검증 seed730/731×3pitch는 분리했다. 모든 모델은 test 수집 전에 동결했다. 제어는 원래 FlashSAC+0.4828Nm bias와 안전한0.01Nm 입력만 사용한다. LQR/Reference/Bias 갱신은 없다. 같은 train stream의1–60초와10–60초를 사전 구분했고 p 목표나 회귀 중심을 재설정하지 않았다. 주 판정은10–60초 학습, 독립60초 snapshot6개의 결과다.10초 snapshot은 과도 영역 진단이다.

| Target | 모델 | 60초 예측 PASS/6 | 정보 gate | paired2초 p/v NRMSE % | absolute 첫2초 p/v NRMSE % | Direct B 오차 % |
|---|---|---:|---|---:|---:|---:|
| friction0.2 | transient_LS | 6/6 | PASS | 0.21334 / 1.6475 | 2.2958 / 1.3192 | 0.027604 |
| friction0.2 | transient_RLS | 0/6 | PASS | 1.4222e+55 / 3.667e+57 | 1.5188e+54 / 3.1091e+55 | 0.62777 |
| friction0.2 | post_LS | 6/6 | PASS | 0.23707 / 1.618 | 2.3303 / 1.3164 | 0.0031528 |
| friction0.2 | post_RLS | 0/6 | PASS | 1.9259e+07 / 1.1497e+09 | 9.8729e+06 / 4.1942e+07 | 0.22449 |
| friction0.2 | post_LS_Bc | 0/6 | PASS | 135.81 / 351.12 | 366.54 / 190.52 | 7.297 |
| friction0.2 | post_RLS_Bc | 0/6 | PASS | 150.98 / 518.03 | 256.51 / 122.94 | 2.3586 |
| friction0.8 | transient_LS | 0/6 | PASS | 12.401 / 65.616 | 19.323 / 14.908 | 0.11726 |
| friction0.8 | transient_RLS | 0/6 | PASS | 2.5695e+21 / 2.6291e+23 | 2.3555e+21 / 2.4255e+22 | 0.1873 |
| friction0.8 | post_LS | 0/6 | PASS | 17.309 / 53.917 | 31.455 / 25.715 | 0.01853 |
| friction0.8 | post_RLS | 0/6 | PASS | 2.2357e+16 / 1.6168e+18 | 2.4038e+16 / 1.9361e+17 | 0.011212 |
| friction0.8 | post_LS_Bc | 0/6 | PASS | 1266.1 / 5517.6 | 2333.2 / 1863.3 | 158.86 |
| friction0.8 | post_RLS_Bc | 0/6 | PASS | 1200.6 / 5194.4 | 2369.5 / 1761.8 | 163.79 |
| gain0.8 | transient_LS | 0/6 | PASS | 32.66 / 219.4 | 35.38 / 21.143 | 0.11124 |
| gain0.8 | transient_RLS | 0/6 | PASS | 3.5026e+40 / 6.9585e+42 | 3.796e+39 / 6.801e+40 | 0.3058 |
| gain0.8 | post_LS | 0/6 | PASS | 16.218 / 96.585 | 17.063 / 10.841 | 0.030982 |
| gain0.8 | post_RLS | 0/6 | PASS | 1.3474e+14 / 1.1297e+16 | 7.2659e+13 / 5.1229e+14 | 0.1622 |
| gain0.8 | post_LS_Bc | 0/6 | PASS | 873.68 / 3904.6 | 2274.4 / 1566.9 | 208.19 |
| gain0.8 | post_RLS_Bc | 0/6 | PASS | 764.15 / 3345.8 | 1856.4 / 1288.8 | 214.83 |
| gain1.2 | transient_LS | 0/6 | PASS | 26.194 / 165.81 | 19.122 / 15.095 | 0.044286 |
| gain1.2 | transient_RLS | 0/6 | PASS | 165.1 / 1501 | 49.019 / 35.019 | 0.10376 |
| gain1.2 | post_LS | 0/6 | PASS | 14.517 / 89.946 | 4.2417 / 4.8847 | 0.074553 |
| gain1.2 | post_RLS | 0/6 | PASS | 1.9072e+26 / 2.4833e+28 | 5.2288e+24 / 6.4188e+25 | 0.20145 |
| gain1.2 | post_LS_Bc | 0/6 | PASS | 1038.8 / 4466 | 1442.7 / 1552.8 | 115.64 |
| gain1.2 | post_RLS_Bc | 0/6 | PASS | 961.38 / 4099.8 | 1334.5 / 1371 | 120.05 |
| lag0.02 | transient_LS | 0/6 | PASS | 19.797 / 122.85 | 28.77 / 17.377 | 4.4313 |
| lag0.02 | transient_RLS | 0/6 | PASS | 1.6334e+05 / 1.2115e+07 | 19928 / 1.937e+05 | 5.8411 |
| lag0.02 | post_LS | 0/6 | PASS | 15.428 / 95.371 | 12.475 / 10.537 | 1.7156 |
| lag0.02 | post_RLS | 0/6 | PASS | 1.4539e+10 / 5.3039e+11 | 9.9445e+09 / 3.1021e+10 | 6.6239 |
| lag0.02 | post_LS_Bc | 0/6 | PASS | 1056.5 / 4461.7 | 2074.5 / 1124.1 | 373.94 |
| lag0.02 | post_RLS_Bc | 0/6 | PASS | 991.24 / 4160.2 | 2028.1 / 1071.9 | 380.91 |
| nominal | transient_LS | 0/6 | PASS | 20.586 / 132.18 | 37.269 / 26.08 | 0.025152 |
| nominal | transient_RLS | 0/6 | PASS | 2543.8 / 64007 | 630.41 / 1315.5 | 0.02114 |
| nominal | post_LS | 0/6 | PASS | 15.964 / 130.59 | 30.494 / 20.25 | 0.064091 |
| nominal | post_RLS | 0/6 | PASS | 8.1221e+32 / 1.3771e+35 | 4.8022e+31 / 7.436e+32 | 0.013158 |
| nominal | post_LS_Bc | 0/6 | PASS | 958.18 / 4294.8 | 1384.8 / 1398 | 147.98 |
| nominal | post_RLS_Bc | 0/6 | PASS | 871.15 / 3863.1 | 1215.5 / 1158.6 | 153.52 |

각 snapshot은 paired 응답·c를 포함한 absolute 예측·baseline·Direct B를 모두 통과해야 예측PASS다. 정보량은 별도 gate이며 예측이 좋아도 정보 gate 미달이면 온라인 K로 넘어갈 근거로 사용하지 않는다. 정보량이 부족한데 Offline/RLS 모두FAIL이라고 해서 상태 표현이 원인이라고 확정하지 않는다.

| Target | post Offline LS | post RLS | 해석 |
|---|---|---|---|
| nominal | FAIL/NOT_TESTED | FAIL/NOT_TESTED | 둘 다FAIL/미실험: 정보·영역·모델 가정을 분리해 재검토 |
| gain0.8 | FAIL/NOT_TESTED | FAIL/NOT_TESTED | 둘 다FAIL/미실험: 정보·영역·모델 가정을 분리해 재검토 |
| gain1.2 | FAIL/NOT_TESTED | FAIL/NOT_TESTED | 둘 다FAIL/미실험: 정보·영역·모델 가정을 분리해 재검토 |
| friction0.2 | PASS | FAIL/NOT_TESTED | Offline PASS/RLS FAIL: 온라인 방법·유효 표본 우선 |
| friction0.8 | FAIL/NOT_TESTED | FAIL/NOT_TESTED | 둘 다FAIL/미실험: 정보·영역·모델 가정을 분리해 재검토 |
| lag0.02 | FAIL/NOT_TESTED | FAIL/NOT_TESTED | 둘 다FAIL/미실험: 정보·영역·모델 가정을 분리해 재검토 |

## 별도 probing/토크 예산 계획

이번 예산은 기존0.4328–0.5328Nm·2Nm/s·wheel±12Nm 그대로다. 늘리지 않았다. 다음 연구는 안전한 target에서 bounded 입력의 진폭/지속시간을 따로 등록하고, 원래 예산 대조군을 남겨 정보 rank/condition/innovation와 물리 drift를 함께 평가해야 한다. 상태 guard/clip 발생 시 excitation 중단, 더 큰 예산은 개발 seed의 별도 pilot·operator 검토 후 독립 manifest로만 수행한다. 이번 데이터에서 실패한 모델의 Q/R·상태·threshold를 바꾸지 않았다.

## 검증·보존·범위

Phase A의 센서 FK 보정은 진단 배열일 뿐 기존 estimator/controller/runtime에 연결하지 않았다. Offline Target 모델은 online controller에 전달하지 않았다. M4와 actor·native PD·raw history·기존모델/보고서를 보존했다. 질량/CoM/50ms lag의 C 수집은 기존 안전성 prerequisite 실패로NOT_TESTED다. Phase D/E/F·실기·commit/push 없음.

브랜치: `agent/codex/dev_tita_gluon`. 신규 코드5개는 plan의source hash와 snapshot을 참조한다. 실제 단위 검사·agent-check·완료 감사는각 로그와 completion_audit.json에 기록한다.

증거: [동결 계획](plan.json), [A exact replay/수치](A_results.json), [B 정보량/모델](B_results.json), [C 동결 모델](C_models_frozen.json), [C 독립 비교](C_comparison.json), [최종 감사](completion_audit.json).
