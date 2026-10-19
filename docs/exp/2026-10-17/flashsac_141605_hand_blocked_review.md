# FlashSAC 14:16:05 손 지지 실행 — 초기 5초 제외 비교

Execution Domains: ROBOT_READ_ONLY (종료 로그 조회·복사·hash 확인), DESKTOP_DRY_RUN (로컬 atomic sample 분석·순수 수학 replay)

Evidence Status: **PASS** — 복사 무결성·bias OFF·zero command·토크 재구성. **SUSPICIOUS** — 손 지지 조건의 동역학 해석에는 접촉력과 실제 몸체 이동량이 없어 한계가 있다. 실제 지면 이동속도·자율 정지 성능은 **NOT_TESTED**.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Branch: `agent/codex/dev_tita_gluon`

대상 실행: `flashsac_60000_141605_080644640_output_true`. 사용자는 **초기 몇 초를 제외하고 손으로 막았다**고 설명했다. 정확한 접촉 시작 시각·접촉력은 측정되지 않았다. 요청대로 대표 분석에서 **첫 5초를 제외**하고 RL+5–20초를 사용한다. 5초는 분석상 제외 기준이며 실제 손 접촉 시작 시각으로 추정한 값이 아니다. 3초·7초 제외의 민감도도 함께 기록했다. 초기 신호를 손 지지 정지의 근거로 사용하지 않는다.

## 관측 결과

동일 checkpoint·ONNX·config 및 controller binary hash의 앞선 [14:11:13 자유 drift](flashsac_141113_free_drift_review.md)와 비교했다. 새 실행 summary는 bias=false, output=true다. Atomic sample 3,666개 중 RL 1,209개, 마지막 RL sample은 첫 sample 이후 24.150초다. RL 모든 프레임에서 command 세 축, wheel bias 두 축, bias diagnostics가 0이고 teacher_action=action_raw다.

| 같은 RL 경과 구간: 5–10초 | 자유 drift | 손 지지 실행 |
|---|---:|---:|
| FK/IMU 속도 추정 평균 | −0.20251 m/s | −0.00431 m/s |
| FK/IMU 속도 추정 표준편차 | 0.02145 m/s | 0.03148 m/s |
| Wheel rolling proxy 평균 | −0.20429 m/s | −0.00479 m/s |
| 피치 평균 | 1.782° | 3.850° |
| 피치 표준편차 | 0.163° | 0.282° |
| 휠 평균 계산 토크 (좌우 평균) | −0.301 Nm | −0.522 Nm |
| 위 휠 토크의 시간 표준편차 | 0.569 Nm | 1.467 Nm |

새 실행의 **5–20초**에서는 FK/IMU 추정속도 평균 **−0.00312 m/s**, 표준편차 0.03051 m/s, 피치 **3.810° ± 0.238°**다. 추정속도 순간값 범위는 −0.0850~+0.0718 m/s로 움직임·진동이 존재한다. 평균이 0에 가깝다는 사실을 매 순간 완전 정지와 혼동하지 않는다. 휠 계산 토크는 평균 −0.467 Nm, 시간 표준편차 1.435 Nm다. 외부 지지가 있어 자율 제어 성능 개선율을 계산하지 않는다.

Bias OFF일 때 기록된 속도 diagnostics도 0으로 초기화된다. 위 속도는 원시 joint/IMU를 기존 C++ observer 수학 fixture에 입력하여 재계산했다. 별도 ROS node·CAN sender는 생성하지 않았으며, shadow 보정은 실제 plant나 기록된 데이터에 적용하지 않았다. Raw action에서 환산한 휠 목표속도 proxy도 JSON에 기록했다. 이는 실제 몸체 목표속도가 아니라 native wheel target의 반경 환산값이다.

## 초기 제외 시간 민감도

종료 시각을 RL+20초로 고정했다.

| 제외한 초기 시간 | 사용 구간 | FK/IMU 추정속도 평균 | 피치 평균 |
|---|---|---:|---:|
| 3초 | 3–20초 | −0.00584 m/s | 3.769° |
| **5초 (대표값)** | **5–20초** | **−0.00312 m/s** | **3.810°** |
| 7초 | 7–20초 | −0.00319 m/s | 3.799° |

첫 3/5/7초를 제외해도 평균 속도가 0 부근이라는 관측은 유지된다. 따라서 후반의 추정속도는 자유 drift처럼 지속적인 −0.2 m/s 평균으로 남지 않는다. 이는 정지 지지 조건에서도 항상 고정된 −0.2 m/s 오프셋이 기록된다는 가설을 약하게 만든다. 다만 실제 몸체 속도 GT, wheel slip 및 센서 frame 보정의 정확성을 증명하지는 않는다. 손 지지로 자세·접촉·휠 운동이 함께 달라지기 때문이다.

손 지지 구간은 자유 drift보다 피치와 휠 계산 토크의 주기 변동이 크다. 이를 bias 제어기 성능이나 단독 원인으로 해석하지 않는다. 별도 bias-ON 실행의 12–14° 피치 변화와도 구분한다. **초기 2초 값에서 계산한 seed를 ‘손으로 정지시켰는데도 큰 보정이 발생한다’는 근거로 사용하지 않는다.** 초기 구간은 이번 대표 분석에서 제외했고 실제 보정 ON 실험도 아니다.

## 검증 및 실행 범위

- **PASS:** 원격/로컬 summary, console, bag-console, metadata.yaml, DB3 SHA256 **5개 일치**. [copy_verification.log](flashsac_141605_hand_blocked_review/copy_verification.log).
- **PASS:** SQLite read-only quick_check=ok, 원본 DB hash 분석 전후 일치. Atomic sequence 누락·역전 0개, monotonic time 역전 0개.
- **PASS:** RL snapshot 간격 최대 20.956ms, 30ms 초과 0개. 이는 약 50Hz snapshot 검사이며 2ms 제어 deadline 검증이 아니다.
- **PASS:** RL에서 sensors_valid, policy_valid, output_enabled, torque_sent, teacher_action_valid의 false 프레임 모두 0개. Transport 접수는 모터 ACK가 아니다.
- **PASS:** 기존 fixture를 `g++ -std=c++17 -O2 -Wall -Wextra -Werror -pedantic`로 컴파일·실행. Raw action/PD의 기준 토크와 기록된 실제 계산 명령 차이는 최대 **8.88e−16 Nm**. 실제 measured motor torque는 없다.
- 분석 스크립트와 보고서·비교 plot·복사/검증 기록만 추가했다. 제어 코드·설정·정책은 변경하지 않았고 하드웨어 실행·서비스 조작·배포·commit/push는 수행하지 않았다. 기존 dirty/untracked 파일은 유지했다.
- **PASS:** `./scripts/agent-check.sh`의 Python syntax **507/507**, URDF XML **8/8**. **FAIL:** 전체 검사는 기존 `my_flat_env_cfg.py` 431/437/443/449/455/461행 trailing whitespace로 실패했다. 해당 파일은 수정하지 않았다. [agent_check.log](flashsac_141605_hand_blocked_review/agent_check.log).

Console의 return_to_sit은 RL+24.160초, damp는 +25.034초, estop은 **+46.644초**로 대표 비교 구간 이후다. Software stop 로그는 `new right press or joystick invalid/stale`의 복합 사유 문구이며 이 로그만으로 어느 조건인지 단정하지 않는다. 종료의 Ctrl-C/exit130과 뒤이은 SIGTERM/SIGKILL은 별도 종료 현상으로 기록하며 전체 shutdown 정상 판정은 하지 않는다. 이들을 RL+5–20초의 drift 원인으로 연결하지 않았다.

추가 파일: [분석 스크립트](../../../../test/sim2real/analyze_hand_blocked_drift.py), 이 보고서와 `flashsac_141605_hand_blocked_review/`의 원본 복사본·[metrics.json](flashsac_141605_hand_blocked_review/metrics.json)·signals.npz·[비교 그래프](flashsac_141605_hand_blocked_review/hand_vs_free.png)·검증 로그. 그래프에는 제외한 첫 5초를 회색으로 표시했으며 원본 시계열은 보존했다. 두 실행은 각 RL 진입 시점으로 정렬했다.

재현 명령 (DESKTOP_DRY_RUN):

```bash
source /opt/ros/jazzy/setup.bash
source test/sim2real/training_logging_work/install/share/tita_controller/local_setup.bash
MPLCONFIGDIR=/tmp/tita_hand_drift_mpl /usr/bin/python3 test/sim2real/analyze_hand_blocked_drift.py \
  docs/exp/2026-10-17/flashsac_141605_hand_blocked_review/flashsac_60000_141605_080644640_output_true_bag \
  --free-signals docs/exp/2026-10-17/flashsac_141113_free_drift_review/signals.npz \
  --output docs/exp/2026-10-17/flashsac_141605_hand_blocked_review
```
