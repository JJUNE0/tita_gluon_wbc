# Velocity bias 기본 대기 2초 적용

Execution Domain: VALIDATION_SIM

Evidence Status: PASS — 2초 기본값 적용, nominal 300초 궤적 완전 일치, 관련 검사 18개 통과.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Branch: `agent/codex/dev_tita_gluon`

사용자가 현재 주 체크포인트 `tita_flash_sac_115632_883848/model_60000`에 대해 2초 대기를 선택했다. `WheelVelocityBias._target()`의 활성 문턱을 1.2초에서 2초로 변경했다. 기존 `--velocity_bias` 명령으로 적용되며 새 인자는 없다. 이득/한도/observer/정책/launch/action 경로는 그대로다.

타이머는 기존과 같이 **RL 상태의 zero-command hold 진입부터** 잰다. RL을 zero command로 시작하는 이번 실험에서는 RL 전이 후 2초다. 이동 명령 후 다시 정지 명령으로 들어오면 2초 대기를 다시 적용한다. 단순 RL 경과 시간만을 저장하는 전역 타이머로 바꾼 것은 아니다. 큰 기울기/추정 속도의 기존 억제 조건도 유지한다.

선택 근거는 [활성 시간 비교](velocity_bias_activation_timing.md)의 명목 환경·seed913·300초 결과다. 동일 체크포인트라도 질량/CoM/마찰 변화에서 항상 최적인 시간은 아니다. 비교한 0/0.5/1/1.2/2/3초 중 **명목 환경 위치 IAE는 2초가 최저**였다.

| 지표, RL 진입 위치 기준 | 기존 1.2초 | 선택 2초 |
|---|---:|---:|
| 300초 위치 IAE | 2,817.19 mm·s | **465.96 mm·s** |
| 최대 XY 이탈 | 31.02 mm | 31.02 mm |

IAE는 약 **83.46% 감소**했으며 최대 이탈은 동일했다. heading hold나 실기 성공을 검증한 결과는 아니다. 2초 대기 및 ±2 m/s 한도를 실기에 배포하지 않았다. Hardware evidence: NOT_TESTED.

변경 파일은 runtime `velocity_bias.py`, 현재 기본값을 검증하는 `test/test_velocity_bias_activation.py`, 사용 중인 문서 `velocity_bias_overnight_summary.md`와 과거 비교 보고서의 후속 변경 안내, 이 기록이다. 원래 1.2초 조건의 실험 표/원시 데이터는 수정하지 않았다. 변경 전 내용과 최종 task diff를 `velocity_bias_default_2s/`에 보관한다.

기존 velocity-bias math/센서/ROS/CLI/lifecycle, M4 결합 경로, 현재 2초 타이머 검사 및 **production 기본값으로 300초 폐루프를 재실행하여 이전 선택 결과의 전체 state trace와 비교**하는 회귀를 실행했다. 검사 **18/18 PASS**이며 300초 15,001개 상태의 최대 차이는 **0**이었다. 첫 2초의 모터 토크도 baseline과 완전히 일치했다. 현재 production과 연구용 2초 observer/control 출력도 정확히 일치했다.

초기 검사 시 ROS 환경 미로딩 및 기본 ROS 로그 디렉터리의 읽기 전용 권한 때문에 통합 검사 2개가 실행되지 못했다. 두 실행 로그를 각각 `tests_without_ros_env.log`, `tests_ros_log_readonly.log`로 보관했다. ROS Jazzy 환경 및 task 내부 로그 디렉터리로 재실행한 최종 `tests.log`에서 18/18 PASS를 확인했다. 코드 변경으로 환경 오류를 우회하지 않았다.

최종 검사 명령(저장소 루트):

```bash
source /opt/ros/jazzy/setup.bash
ROS_DOMAIN_ID=87 ROS_LOCALHOST_ONLY=1 \
ROS_LOG_DIR="$PWD/docs/exp/2026-10-17/velocity_bias_default_2s/ros_logs" \
  /home/cocel/venvs/cosim_ros2_jazzy/bin/python -m unittest discover \
  -s test -p 'test_velocity_bias*.py'
```

전체 `./scripts/agent-check.sh`는 **FAIL**이다. Python 구문 **483/483 PASS**, URDF **8/8 PASS**이며, 원인은 기존 사용자 변경 `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py` 431/437/443/449/455/461행 trailing whitespace다. 관련 없는 파일은 수정하지 않았다. 직접 출력을 `agent_check.log`에 기록했다.

최종 diff 확인에서 runtime 변경은 활성 문턱 한 줄뿐이며 다른 runtime 파일의 hash는 유지됐다. 기존 status 항목 삭제나 task artifact 디렉터리 밖의 신규 상태 항목은 없었다. 변경 전 파일과 task diff, hash·범위 확인 결과는 `before.json`, `task_files.diff`, `completion_integrity.json`에 기록한다.

커밋/push/실기 실행/배포는 수행하지 않았다.
