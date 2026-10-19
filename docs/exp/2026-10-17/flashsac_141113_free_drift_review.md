# FlashSAC 14:11:13 순수 자유 drift baseline

Execution Domains: ROBOT_READ_ONLY (종료된 지정 로그 조회·복사·SHA256 확인), DESKTOP_DRY_RUN (로컬 atomic frame 분석·순수 수학 replay), VALIDATION_SIM (기존 nominal rollout 데이터 비교; 신규 시뮬레이션 없음)

Evidence Status: **PASS** — 로그 복사, bias OFF·zero command·프레임 및 수학 재구성 검사. **SUSPICIOUS** — nominal sim과 실기 추정속도의 방향·크기 차이. 실제 바닥 속도·이동거리 및 차이의 물리 원인은 **NOT_TESTED**.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Branch: `agent/codex/dev_tita_gluon`

사용자가 `flashsac_60000_141113_460666182_output_true`를 **순수 drift**로 지정했다. 이를 손 지지·의도적 이동 명령이 없는 실행이라는 operator annotation으로 기록한다. 손 지지 유무는 센서 로그만으로 독립 검증할 수 없다. 이전 13:56:54 혼합 실행과 합치지 않는다.

## 관측 결과

원격 summary에서 velocity bias=false, output=true를 확인했다. Atomic TrainingSample 3,407개 중 RL 560개, 첫 RL sample부터 마지막 RL sample까지 11.164초다. Console의 RL 진입→return_to_sit 간격은 약 11.174초다. RL 모든 프레임에서 command 세 축, wheel bias 두 축, bias diagnostics가 정확히 0이다. teacher_action=action_raw도 정확히 일치한다.

Bias OFF에서는 diagnostics의 속도값까지 초기화되므로 그 0을 정지 속도로 해석하지 않았다. 기록된 joint position/velocity, quaternion, gyro를 기존 `WheelVelocityBias` C++ 수학 구현에 입력하여 FK/IMU 속도만 수동 replay했다. 계산한 가상 보정은 원본 데이터나 로봇에 적용하지 않았다.

| RL 이후 구간 | 실기 FK/IMU 추정속도 평균 | 실기 wheel rolling proxy 평균 | 실기 피치 평균 ± 표준편차 | nominal sim FK 추정속도 평균 |
|---|---:|---:|---:|---:|
| 0.5–2초 | −0.2864 m/s | −0.2943 m/s | 1.588° ± 0.537° | +0.01870 m/s |
| 2–5초 | −0.2260 m/s | −0.2257 m/s | 1.762° ± 0.141° | +0.01521 m/s |
| 5–10초 | −0.2025 m/s | −0.2043 m/s | 1.782° ± 0.163° | +0.01512 m/s |

실기는 zero command 및 보정 OFF에서도 음의 추정속도가 수초간 지속된다. 즉 보정 시작 순간에만 속도가 일시적으로 크게 추정된 사례는 아니다. 사용자 관측인 후진 drift와 센서상 부호가 일치한다. 2초 이후에는 FK 추정과 단순 wheel proxy의 구간 평균도 가깝다. 다만 두 값 모두 같은 엔코더를 사용하므로 이 일치만으로 wheel slip이나 센서 frame/단위 오류를 배제할 수 없다.

실기 RL+2.004초 추정속도는 **−0.23855 m/s**, wheel proxy는 −0.22037 m/s, 피치는 1.680°다. 기존 nominal sim의 rollout+2.000초 FK 추정속도는 **+0.01516 m/s**, ground-truth forward speed는 +0.01517 m/s, 피치는 4.003°다. 이전의 실기 초기값 대 sim 장시간 정상상태 비교 대신 경과시간을 맞췄다. 단, 실기는 실제 transform_up→sit→RL 이후이며 sim의 초기 기립 상태·절차는 달라 완전히 같은 초기조건의 A/B 실험은 아니다.

비교 sim 원본은 `velocity_bias_grid_video/nominal/group_0.npz`, control dt=0.02초, 같은 checkpoint의 FlashSAC-only 기록이다. state 열은 `[base_x, base_y, base_z, forward_speed_GT, roll, pitch, yaw, fk_position, fk_speed]`다. 실제 지면 이동거리는 외부 GT가 없어 적분하여 측정값으로 제시하지 않았다. 마지막 약 1초에는 속도·자세가 변하므로 안정 구간의 대표 비교는 2–5초와 5–10초를 사용한다.

## 큰 보정토크와 연결되는 부분

기존 수학식을 이 baseline에 가상 replay하면 최초 eligible 시점은 RL+2.024초이고, 당시 추정속도는 −0.23078 m/s다. `3*v` seed와 첫 적분 갱신 후 적분값은 **−0.69569 m/s**다. 휠 Kd=0.5, 반경=0.0925m에서 이는 **휠당 −3.7605 Nm 상당**의 목표 offset이다.

이 값은 ramp 이전의 초기 적분값을 토크 단위로 환산한 것으로, 이 실행에서 실제 출력된 추가 토크가 아니다. 최초 eligible 프레임의 ramp 출력은 0이며 이후 ramp·slew를 따른다. 실제 기록된 보정은 실행 내내 0이다. 또한 shadow 계산은 보정이 적용되지 않은 원래 궤적을 계속 입력하므로 보정 ON의 이후 움직임을 예측하지 않는다.

별도 bias-ON 실행에서 처음 약 −4 Nm 상당으로 시작한 현상을, 이번 순수 baseline의 속도 입력으로도 재현한다. **기존 seed gain이 실기의 큰 음의 속도 추정에 곱해져 큰 초기 보정 목표를 만든다**는 수학적 경로는 확인했다. 왜 실기 baseline 속도가 nominal sim과 다른지는 아직 분리되지 않았다. 정책의 실제 동역학 gap, 센서/좌표계, 접촉·미끄럼 등의 원인을 이번 로그만으로 특정하지 않는다.

이번 baseline의 2–10초 평균 피치는 약 1.8°이고, 이전 bias-ON의 12–14° 평형 이동은 관측되지 않는다. 작은 주기 변동은 존재하며 ‘기존 정책에 진동이 전혀 없음’이라고 판정하지 않는다. 기존 bias-ON 결과는 [oscillation review](flashsac_bias_oscillation_review.md)를 참조한다. 서로 다른 실행이므로 자세 차이의 단독 인과 실험은 아니다.

다음 판단에는 동일한 bias OFF 자유 drift 구간의 고정 카메라·바닥 거리 측정을 대응시키는 것이 우선이다. 실제 이동속도도 약 −0.2 m/s인지 확인한 다음, seed 축소·초기 보정 제한과 pitch 변화 제한을 별도 검증하는 근거로 사용한다. 이번 작업에서 제어기 gain이나 실기 설정을 변경하지 않았다.

## 검증과 한계

- **PASS:** 원격/로컬 summary, console, bag-console, metadata.yaml, DB3 SHA256 **5개 일치**. [copy verification](flashsac_141113_free_drift_review/copy_verification.log).
- **PASS:** SQLite read-only quick_check=ok. Sequence 누락·역전 0개, monotonic time 역전 0개. RL snapshot 간격 최대 21.502ms, 30ms 초과 0개. 50Hz 기록이며 2ms 제어 deadline 검증은 아니다.
- **PASS:** RL의 sensors_valid/policy_valid/output_enabled/torque_sent/teacher_action_valid false 프레임 모두 0개. torque_sent는 transport 접수이며 모터 ACK나 실제 토크 측정이 아니다.
- **PASS:** 기준 정책·PD 토크 재구성 최대오차 `8.88e-16 Nm`; 독립 Python FK 계산과 C++ observer replay 최대차 `1.46e-8 m/s`; teacher/raw action 오차 0. strict warning 옵션으로 순수 C++ fixture 컴파일 후 실행했다.
- **PASS:** 분석 스크립트 실행 및 plot 육안 확인. 첫 실행은 결과 저장 시 상대경로 처리에서 실패했고 경로 resolve 수정 후 전체 재실행 및 assertions를 통과했다.
- **PASS:** `./scripts/agent-check.sh` 내 Python syntax **506/506**, URDF XML **8/8**.
- **FAIL:** 전체 `agent-check.sh`는 기존 `my_flat_env_cfg.py` 431/437/443/449/455/461행 trailing whitespace로 실패했다. 해당 파일은 수정하지 않았다. [전체 검사 로그](flashsac_141113_free_drift_review/agent_check.log).
- **NOT_TESTED:** 실제 바닥 속도·이동거리, measured motor torque, 하드웨어 보정 ON 효과. 로봇 제어·서비스 조작·배포·커밋·push 없음.

Console 종료에는 Ctrl-C/exit130과 SIGTERM/SIGKILL이 있다. Exit130 자체는 사용자 인터럽트와 일치하지만, 강제 종료까지 포함한 전체 shutdown을 정상 종료로 판정하지 않는다. 분석은 return_to_sit/damp 이후를 제외한 RL 구간만 사용했다. 외부 launch의 1970-01-01 경로와 별개로 구간 시간 계산에는 atomic monotonic_ns를 사용했다.

추가 파일은 이 보고서, [분석 스크립트](../../../../test/sim2real/analyze_free_drift_baseline.py), `flashsac_141113_free_drift_review/`의 복사 원본·hash·[metrics.json](flashsac_141113_free_drift_review/metrics.json)·signals.npz·[비교 그래프](flashsac_141113_free_drift_review/free_drift_comparison.png)·분석/검사 로그다. Task 시작/종료 git status 비교에 다른 파일 변경이 없었고 기존 dirty 파일은 유지했다. 추가 파일 diff를 별도 확인했다.

재현 명령 (DESKTOP_DRY_RUN):

```bash
source /opt/ros/jazzy/setup.bash
source test/sim2real/training_logging_work/install/share/tita_controller/local_setup.bash
MPLCONFIGDIR=/tmp/tita_free_drift_mpl /usr/bin/python3 test/sim2real/analyze_free_drift_baseline.py \
  docs/exp/2026-10-17/flashsac_141113_free_drift_review/flashsac_60000_141113_460666182_output_true_bag \
  --output docs/exp/2026-10-17/flashsac_141113_free_drift_review \
  --sim docs/exp/2026-10-17/velocity_bias_grid_video/nominal/group_0.npz
```
