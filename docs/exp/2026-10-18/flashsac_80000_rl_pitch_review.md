# FlashSAC 80000: RL standing pitch review

- Date: 2026-10-18 (Asia/Seoul)
- Execution Domains: `ROBOT_READ_ONLY` (log copy, no controller), `DESKTOP_DRY_RUN` (recording/FK/controller-math analysis).
- Evidence Status: recorded measurements and torque reconstruction `PASS`; physical root cause `SUSPICIOUS`; new hardware experiment or corrective controller `NOT_TESTED`.
- Checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`.
- Run: `flashsac_80000_105921_542288145_output_true`.
- Operator clarification: the unwanted pitch is while **standing in RL**, rather than sitting.
- Branch: `agent/codex/dev_tita_gluon`; no commit, deployment or physical execution in this review.

## Main finding

RL 피치는 줄일 여지가 있다. 앉기 제어의 파라미터를 바꾸는 문제와는 구분해야 한다. 이번 실행은 `velocity_bias=false`이고, 지지 앉기 제어는 RL 동안 토크를 만들지 않는다. RL에서는 frozen policy + 기존 PD만 작동한다.

두 RL 구간 모두 중립 명령에서 약 +8.5°가 반복됐다. 진입 후 2초 이상, 명령 abs <= `[.02,.02,.03]`, pitch 각속도 abs < 0.1 rad/s인 구간을 따로 보면 아래와 같다. 이 조건은 손 접촉이나 실제 이동이 없었다는 증거는 아니다.

| Condition | Samples | IMU pitch mean | Std | Nominal FK CoM lean mean |
|---|---:|---:|---:|---:|
| Actual RL episode 1, quiet neutral | 1318 | +8.405° | 0.788° | +0.456° |
| Actual RL episode 2, quiet neutral | 591 | +8.366° | 0.828° | +0.643° |
| Same ONNX nominal MuJoCo continued RL, last 3 s | — | +5.058° | 0.002° | not evaluated here |

따라서 기울기는 새 정책의 nominal 시뮬에서도 이미 존재하고, 이번 실기는 거기에 약 3.3°가 더해졌다. nominal 시뮬은 실제 robot inertia/friction/CoM/센서 오프셋을 식별해 맞춘 모델이 아니다. 이 차이를 한 가지 모델 파라미터의 잘못으로 단정하지 않는다.

실기 관절의 추종 오차도 크다.

| Quiet neutral | Policy knee reference L/R | Measured knee L/R | Difference magnitude |
|---|---|---|---|
| RL 1 | -1.595 / -1.624 rad | -2.098 / -2.018 rad | 28.9° / 22.6° |
| RL 2 | -1.622 / -1.642 rad | -2.103 / -2.062 rad | 27.6° / 24.1° |

비교 nominal 시뮬의 평균 측정 무릎은 -1.762 / -1.775 rad였다. 실기에서는 더 접힌 다리 자세를 유지하고 있으며, commanded knee torque 평균은 약 +24~30 Nm이다. 이 수치는 계산된 관절 토크이며 calibrated physical torque가 아니다. 목표/관절/토크 재구성으로 자료의 해석은 검증했지만, 실물 부하·마찰·모터 토크 변환·encoder 영점 중 무엇이 오차를 지배하는지는 아직 식별하지 않았다.

같은 실기 관절 자세에서 몸통 피치만 0°라고 가정해 nominal FK를 계산하면 CoM lean은 평균 약 -7.95° / -7.72°가 된다. 실제 측정 피치에서는 그 값이 0° 근처다. **현재 다리 자세와 모델 기준으로는 몸통을 기울여 균형을 잡는 상태라는 해석과 일치**한다. 실제 CoM을 직접 측정한 결과는 아니며, 몸통을 수평으로만 강제했을 때의 폐루프 성능을 증명하는 것도 아니다.

## What to adjust

1. 먼저 실기 다리의 관절 목표/측정/토크 오차를 nominal 및 mismatch sim과 맞춰 본다. 특히 무릎이 목표보다 0.4~0.5 rad 접혀 있는 이유를 확인하고, encoder 영점·구동기/부하 모델·중력 보상과 PD를 검증한다.
2. 이후 몸통 pitch와 CoM 균형이 함께 맞는 다리 기준 자세 또는 정책 학습/보상을 검증한다. 고정된 다리 자세에서 휠 토크만 추가하여 몸통 수평을 강제하면 속도/위치 균형과 충돌할 수 있다.
3. IMU floor-relative attitude를 별도로 교정하지 않았으므로 +8.4° 전부가 실제 바닥 기준 기울기라고 단정하지 않는다. 다만 idle 약 -0.5°, 준비 sit 약 +2.6°, RL 약 +8.4°로 변하는 기록이 있어 단순한 동일 상수 오프셋만으로 설명되지는 않는다.

새 checkpoint의 저장된 training env는 `flat_orientation_l2` weight -5를 포함하며, `base_link` CoM startup randomization은 x [-0.055,-0.015] m, y [-0.02,+0.02] m, z [-0.03,+0.03] m다. 모델/학습 조건 차이를 검토할 단서이며, 해당 randomization이 실제 피치를 유발했다는 증거는 아니다. 현재 열린 다른 training config 대신 이 checkpoint의 saved `env.yaml`을 조사했다.

## Supporting-sit observations (separate from operator's concern)

일반 return과 estop 모두 토크가 이식한 4초 제어 법칙과 최대 약 3e-12 Nm 오차로 일치했다. 일반 return은 4초 후 sit 상태, estop은 앉기 이후에도 latch 유지였다. 약 2.36 / 2.42초에 pitch -13.11° / -13.53°까지 갔다가 최종 약 +3°로 복귀했다. 해당 순간 휠 balance multiplier는 약 4%였고, 무릎 기반 fade와 pitch 변화가 겹친다. 이는 별도 개선 대상으로 남는다. 실제 contact/하강 속도/정지 거리는 이번 센서만으로 측정하지 않았다.

종료 시 `teleop_command_node` exit -7(SIGBUS) 및 controller group SIGTERM/SIGKILL이 기록됐다. RL pitch와는 발생 시점이 다르며, 종료 경로 문제는 별도 미해결 사항이다. 이번 작업에서 실행기를 수정하거나 재실행하지 않았다.

## Evidence, reproducibility and scope

[전체 시계열](flashsac_80000_105921_pitch_review/pitch_overview.png), [앉기 상세](flashsac_80000_105921_pitch_review/sit_pitch_detail.png), [분석 JSON](flashsac_80000_105921_pitch_review/analysis.json), [분석 로그](flashsac_80000_105921_pitch_review/analysis_final.log).

기체 원본 bag/metadata/console/summary를 `flashsac_80000_105921_pitch_review/`에 복사했다. SQLite quick_check와 분석 전후 SHA 동일성, finite 센서/토크, sequence 연속성을 검증했다. 5144 samples, invalid sensor 0, torque transport failure 0, bias 0. 샘플 주기는 중앙값 약 20 ms, p99 약 20.414 ms, 최대 약 20.563 ms. transport success는 motor ACK/실제 토크 계측과 구분한다.

```bash
# DESKTOP_DRY_RUN, no ROS node or robot SDK instance
source /opt/ros/jazzy/setup.bash
source test/sim2real/training_logging_work/install/share/tita_controller/local_setup.bash
MPLCONFIGDIR=/tmp/tita_pitch_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python \
  test/sim2real/analyze_supporting_sit_pitch.py \
  docs/exp/2026-10-18/flashsac_80000_105921_pitch_review
```

Changed source: only new `test/sim2real/analyze_supporting_sit_pitch.py`. Added experiment records/plots/raw log copies under docs/exp. No production, policy, launch or SBC files changed. `agent-check.sh` result is recorded in `flashsac_80000_105921_pitch_review/agent_check.log`; existing `my_flat_env_cfg.py` six whitespace issues remain untouched.
