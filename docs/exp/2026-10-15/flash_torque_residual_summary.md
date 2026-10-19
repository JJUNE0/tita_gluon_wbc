# E 센서 시점 진단 및 F — FlashSAC Torque Residual

Execution Domain: VALIDATION_SIM (소스·무결성 검사: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: PASS — F-1 nominal drift 개선·구현 무결성. FAIL — E 안정화와 F-2 drift 개선. SUSPICIOUS — F-2의 국소 4-state 식별 모델.

Observed Metrics / Behavior / Log Summary:

**기존 FlashSAC wheel·leg 경로에 작은 위치·속도 토크를 더한 F-1은 9/9회 완료했고, α=1에서 최대 planar drift 평균을 0.497→0.328 m (34.0% 감소)로 줄였다.** F-2도 완료했지만 α=1 drift는 0.584 m로 악화됐다. E는 IMU 동기화와 Ground Truth에서도 모두 실패했다.

## E 센서 진단: 여기서 종료

| 군 | 상태 입력 | 완료/전체 | 종료 시각 범위 s |
|---|---|---:|---:|
| E-original | 기존 cache | 0/9 | 0.54–0.64 |
| E-sync | 현재 qpos/qvel 시점의 IMU | 0/9 | 0.52–0.62 |
| E-GT | MuJoCo 실제 axle/자세 상태 | 0/9 | 0.52–0.64 |

LQR 상태만 교체했다. 세 군 모두 actor는 기존 A의 sensor cache·33-value observation·전체 last_action을 유지한다. 동기화 IMU/GT는 mjData clone에 mj_forward를 수행해 얻었으며 원본 시뮬레이터를 refresh하지 않았다. E-original 9회는 기존 E archive와 state·physics substep motor torque·위치·leg error가 정확히 일치했다.

동일 초기 조건에서 IMU 시점 문제를 제거해도 E가 살아남지 못했다. 센서 시점 불일치만으로 E 실패를 설명할 수 없다. FlashSAC leg와 대체 LQR wheel의 협조/모델 조건 문제가 더 유력하지만 원인이 유일하게 확정된 것은 아니다. E는 재튜닝하지 않았다. 실패 전 drift/Pitch RMS를 12초 완료 군과 성능 비교하지 않는다.

## A drift 방향 및 F-1 경로

A의 초기 heading 기준 전후방 최대 이동 평균은 0.482 m, 좌우는 0.120 m이다. 초기 yaw=0이므로 world x/y가 이 초기 방향과 일치한다. 이는 매 순간 body heading 방향의 누적 이동과 다른 지표이며, 전후방 성분이 주원인이다.

F-1: Δτ = −2(p−p_hold)−0.5v. p_hold는 zero command episode 시작 시 encoder 경로 값 0을 고정한다. 위치는 encoder+동기화 IMU로 적분한 sagittal 경로이며 v는 같은 시점의 encoder/IMU 속도이다. GT position·velocity는 이 residual에 들어가지 않는다. Sagittal 경로 feedback은 world 2D 위치/yaw hold가 아니다.

합산 residual은 α×clip(Δτ, ±1 Nm)에 1초 smoothstep 활성화와 합 토크 slew 2 Nm/s를 적용한다. native wheel axis sign으로 바퀴당 절반씩 더하고 기존 Playback의 ±12 Nm/바퀴 saturation을 적용한다. α는 0, 0.1, 0.25, 0.5, 1로 낮게 시작했다. 실측 α=1 residual peak의 trial 평균은 0.658 Nm(total)이다.

기존 ActionAdapter는 원래 policy wheel velocity target/Kd=0.5 PD torque를 매 physics substep 만들고 기존 effort clipping을 적용한다. 이 출력에 residual을 더한 뒤 기존 final effort clipping을 거친다. Leg는 A의 Kp=60/Kd=1.5, action scale/clip/targets를 그대로 유지한다. 미리 clipping된 FlashSAC torque에 더한다는 기존 경로의 포화 순서를 기록했다. 이 nominal 실험에서 추가 포화는 발생하지 않았다.

전체 raw actor output 8개를 last_action으로 보존한다. residual Nm 값을 policy action 단위의 history에 넣지 않는다. 기존 wheel torque를 실제 적용하므로 E처럼 출력을 버리지는 않지만, residual은 학습 때 없는 외부 입력이고 이후 observation/actor action은 A와 달라질 수 있다. α=0은 state·위치·leg error·motor substeps뿐 아니라 별도 F-2 검사에서 actor observation/action까지 정확히 재현했다.

## Nominal 12초 비교

| 군 | 완료/전체 | 최대 planar drift m | 전후방 m | 좌우 m | Pitch error RMS rad | Wheel torque RMS Nm/바퀴 |
|---|---:|---:|---:|---:|---:|---:|
| A | 9/9 | 0.4968 ± 0.0185 | 0.4821 | 0.1198 | 0.0941 ± 0.0002 | 0.1683 ± 0.0125 |
| F-1_a0 | 9/9 | 0.4968 ± 0.0185 | 0.4821 | 0.1198 | 0.0941 ± 0.0002 | 0.1683 ± 0.0125 |
| F-1_a0.1 | 9/9 | 0.4770 ± 0.0171 | 0.4631 | 0.1143 | 0.0942 ± 0.0002 | 0.1493 ± 0.0136 |
| F-1_a0.25 | 9/9 | 0.4483 ± 0.0149 | 0.4356 | 0.1062 | 0.0943 ± 0.0001 | 0.1414 ± 0.0143 |
| F-1_a0.5 | 9/9 | 0.4040 ± 0.0116 | 0.3930 | 0.0935 | 0.0946 ± 0.0001 | 0.1366 ± 0.0148 |
| F-1_a1 | 9/9 | 0.3281 ± 0.0065 | 0.3202 | 0.0712 | 0.0950 ± 0.0001 | 0.1333 ± 0.0151 |
| F-2_a0 | 9/9 | 0.4968 ± 0.0185 | 0.4821 | 0.1198 | 0.0941 ± 0.0002 | 0.1683 ± 0.0125 |
| F-2_a0.25 | 9/9 | 0.5190 ± 0.0206 | 0.5035 | 0.1258 | 0.0940 ± 0.0002 | 0.1774 ± 0.0119 |
| F-2_a0.5 | 9/9 | 0.5412 ± 0.0228 | 0.5250 | 0.1317 | 0.0939 ± 0.0002 | 0.1710 ± 0.0117 |
| F-2_a1 | 9/9 | 0.5841 ± 0.0252 | 0.5665 | 0.1422 | 0.0938 ± 0.0002 | 0.1478 ± 0.0131 |

평균 ± sample 표준편차. Drift는 기존 A와 같은 cached axle world position 평가 정의를 유지하고, fresh GT axle 지표도 raw results에 별도 기록했다. Pitch error RMS는 기존 nominal equilibrium 기준의 cached sensor state로 모든 F군을 동일 평가했다. Fresh GT pitch error RMS도 metrics.csv에 있다. Wheel torque RMS는 초기의 미적용 zero row를 제외한 모든 실제 physics substep, 두 바퀴만 포함한다. Leg torque를 포함하지 않는다.

F-1 α=1은 각 초기 조건별 9/9쌍 모두 drift가 감소했다. 평균 Pitch RMS 변화는 +1.03%, wheel torque RMS 변화는 -20.76%다. 성공 판정은 9/9 완료, 모든 paired 최대 drift 감소, 각 trial pitch RMS ≤A의 110%, wheel torque RMS ≤A의 125%로 수치화했다. 이 여유 한도는 이번 분석의 운영 기준이며 원래 사용자 요청의 정량 사양은 아니다. F-1 모든 nonzero α는 이 기준을 만족하고 F-2 nonzero α는 drift 기준을 만족하지 못했다.

## F-2: FlashSAC 포함 폐루프 국소 식별

F-1 성공 확인 후 구현했다. C-4의 K/A/B는 사용하지 않았다. Frozen FlashSAC, 원래 observation/history, leg PD, wheel velocity PD와 contact를 모두 실제 실행한 상태에서 0.1/0.25/0.5 Nm(total amplitude) 다중 sine residual을 추가했다. 동일 seed/pitch의 A 궤적을 뺀 δx를 이용해 δx_next=A_closed δx+B_res Δτ를 offline least squares로 식별했다. 입력은 최종 command에서 원래 FlashSAC torque를 뺀 실제 추가 토크로 계산했다.

27 probing episodes 전부 12초 완료. Seed42/43의 18회(7,344 transitions)를 학습, seed44의 9회(3,672 transitions)를 held-out 검증에 사용했다. 2–10.5초 중 3초 외란 구간을 제외했다. 위치 translation에 policy/PD가 불변이므로 A의 첫 열 [1,0,0,0]을 강제했고, [δv,δpitch,δpitch_rate,Δτ] 4 regressors의 scaled rank=4, condition number는 29.05였다. 모든 값은 model.json/identification.npz에 있다.

LQR Q=diag(4,1,0.2,0.05), R=4로 고정했다. 새 K=[-0.999717, 0.156703, -4.047717, 0.029633], 식별 모델의 ρ(A_closed−B_res K)=0.999532. Pitch reference는 학습용 A의 4–12초 평균 pitch error 0.094531 rad를 고정했다. 제어에는 [p−p_hold,v,pitch_error−reference,pitch_rate]를 사용하고 F-1과 동일한 residual clamp/ramp/slew를 적용했다. α=0/0.25/0.5/1을 각각 9개 초기 조건에서 검증했다. Q/R·gain을 성능에 맞춰 추가 튜닝하지 않았다.

Held-out one-step RMS error [p,v,pitch,rate] = [2.4488474024851503e-05, 0.0018372689456618678, 6.919084624540494e-06, 0.0007396615506228455]. 해당 상태의 한 step 변화 RMS 대비 비율 = [0.1682, 0.5866, 0.0769, 0.4435]. 속도/각속도 변화 예측이 충분히 정밀하지 않다. 다리·roll·yaw·action history가 실제 데이터 수집에는 포함되지만 4-state 회귀의 상태에는 생략됐다. A는 정확한 정지 평형점이 아닌 움직이는 operating trajectory다. 따라서 모델의 eigenvalue만으로 실제 residual 제어 성능을 보장하지 않는다. 다중 step 검증은 f2_multistep_validation.json에 별도 기록했다.

F-2 α=1의 최대 drift 평균은 A 대비 17.6% 증가했다. **F-2는 넘어지지는 않았지만 위치 drift 개선 목표에는 FAIL이다.** 현재 증거는 F-1의 단순 residual이 더 유효함을 지지한다. F-2 악화를 단일 원인으로 확정하지 않으며, 식별 모델의 생략 상태·장기 예측 오차와 feedback 방향은 추적 대상이다.

## 검증·변경 범위·제한

- 본 평가: E 27 + A/F-1 54 + F-2 probing 27 + F-2 평가 36 = 144 episodes. 모든 군은 같은 nominal 9개 initial qpos/qvel, 12초 horizon, physics/control dt=0.005/0.02초와 기존 3초의 12 N/0.1초 외란을 사용했다. E는 외란 전에 종료했다.
- 무결성 PASS: 27개 기존 A/E substep archive 정확 재현, F-2 α=0 9개 actor observation/action 포함 정확 재현, initial/history/leg 오차 0.0, wheel 합산 최대 오차 4.75e-07 Nm(float32). RLS update/online adaptation 0.
- 단위 검사 2개: bound/ramp/slew·wheel-only addition과 α=0 full rollout archive 재현. 결과는 unit_tests_final.log에 기록한다.
- 초기 검사 로그 unit_tests.log/f1_smoke.log의 FAIL은 state가 달라서가 아니라 저장 배열 평균의 float32/64 반올림 차이 4.47e-08 Nm를 exact 비교한 문제다. 실제 substep 비교로 수정했다. 최종 E/F-1 데이터는 e_timing_final/f1_nominal만 채택한다. 초기 e_timing 및 중단된 smoke는 주 결과에 포함하지 않는다.
- 기존 소스/설정/보고서는 변경하지 않았다. 신규 test/eval_flash_torque_residual.py, test/eval_flash_closed_loop_residual.py, test/test_flash_torque_residual.py, test/analyze_flash_torque_residual.py와 본 날짜의 실험 증거를 추가했다. 각 실행 source hash 및 E/F-1 실행 당시 source snapshot도 보존했다.
- agent-check.sh PASS (Python syntax 337개, URDF XML 8개): agent_check.log. 최종 diff/기존 hash 보존 검사는 final_review.json/task.diff에 기록한다.
- 브랜치: agent/codex/dev_tita_gluon. Dynamics mismatch와 online adaptive residual은 NOT_TESTED; 이번 범위는 nominal 비교와 조건부 F-2이다. Hardware 실행·재학습 없음.
- Nominal 9개는 3 seed×3 pitch의 제한된 결정론적 초기 조건이다. F-1 개선을 다른 명령·지형·mismatch 또는 실물로 일반화하지 않는다. 남은 좌우/yaw drift와 path odometry 한계도 해결되지 않았다.

## 재현 및 산출물

```bash
MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_flash_torque_residual.py
MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_flash_torque_residual.py --stage e --output docs/exp/2026-10-15/new_residual/e_timing_final
MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_flash_torque_residual.py --stage f1 --output docs/exp/2026-10-15/new_residual/f1_nominal
```

F-2는 --baseline 인자로 위 F-1 결과 폴더를 지정할 수 있다. 이번 실행은 default인 flash_torque_residual/f1_nominal을 사용했다.

```bash
MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/eval_flash_closed_loop_residual.py --baseline docs/exp/2026-10-15/new_residual/f1_nominal --output docs/exp/2026-10-15/new_residual/f2_closed
MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/analyze_flash_torque_residual.py --root docs/exp/2026-10-15/new_residual --report docs/exp/2026-10-15/new_residual_summary.md
./scripts/agent-check.sh
```

산출물: [flash_torque_residual/comparison.png](flash_torque_residual/comparison.png), metrics.csv, aggregates.json, success_gates.json, integrity.json, f2_multistep_validation.json, 각 군 manifest/results.jsonl/NPZ, f2_closed/model.json 및 identification.npz.
