# sim2sim --residual_wheel_pd 연결

Execution Domain: VALIDATION_SIM (소스·수치 검사: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c`

ONNX SHA256: `0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873`

Evidence Status: PASS — 옵션 전달·기존 경로 재현·토크 합산/제한·정지 진입 초기화. 정지 성능 및 실기 적용: NOT_TESTED. 저장소 전체 agent-check 결과는 아래 검증 로그에 기록한다.

Observed Metrics / Behavior / Log Summary:

다음 명령에서 기존 FlashSAC 토크에 정지 유지 residual을 추가한다. 기본값은 비활성이다.

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_50000 \
  --residual_wheel_pd
```

- RL 상태의 정지 명령에만 `u = smoothstep(t/1.5) * clip(-2*p - 24*v, -2, 2)`를 계산한다. 합 토크 slew는 2 Nm/s이다.
- 정지 진입: abs([vx,vy,yaw]) ≤ [0.02,0.02,0.03]. 해제: 어느 성분이든 ≥ [0.04,0.04,0.06]. 이동 시에는 기존 residual을 slew로 0까지 내린다.
- 정지 진입 시 encoder 상대 위치를 한 번 0으로 초기화한다. 실제 속도가 남아 있어도 HOLD를 매번 재설정하지 않는다. RL 이탈/reset 시 residual 상태를 초기화한다.
- 위치/속도는 wheel radius와 joint chain의 운동학, encoder와 IMU로 구한다. 기존 WheelOdometry와 수치 비교했다. Root translation을 크게 바꿔도 추정 결과는 동일하며 root linear velocity를 feedback에 쓰지 않는다.
- 옵션을 켜면 mjData clone에 mj_forward를 수행해 **actor와 residual 모두 현재 joint state 시점의 IMU**를 사용한다. 원본 physics sensor cache는 수정하지 않는다. 옵션을 끄면 원래 actor 센서 경로를 유지한다.
- ActionAdapter가 physics substep마다 만든 기존 토크에 바퀴당 signed u/2를 더하고 기존 actuator effort limit로 다시 clip한다. Leg 6개와 raw actor output 기반 last_action은 원래 경로를 유지한다.
- ROS launch에도 `residual_wheel_pd:=true`를 전달할 수 있다. 실물 제어 경로는 변경하지 않았다.

변경 파일: `residual_wheel_pd.py`에 제어 로직 1개 class, `sim2sim_node.py`에 RL callback 연결, `cli.py`와 `sim2sim.launch.py`에 opt-in 인자 전달. 기존 `mujoco_env.py`, `adapter.py`, `state_machine.py`는 보존했다. 검증 스크립트는 `test/test_residual_wheel_pd.py`에 있다.

## 검증

- 단위/통합 검사 **4개 PASS**: 기존 odometry와의 수치 동등성·physics cache 보존, ramp/limit/slew/재진입/reset, CLI runtime 인자 전달, 실제 ROS node의 opt-out 재현과 opt-in RL callback.
- 수정 전 node/옵션 OFF/옵션 ON을 각각 600 step 실행했다. 수정 전과 OFF는 모든 qpos/qvel·ctrl·raw action 배열이 정확히 일치했다. ON은 RL 490 step, residual 최대 2 Nm, step당 변화 최대 0.040000000000000036 Nm, leg 토크 오차 0이었다.
- 사용자가 지정한 실제 CLI 경로에서도 `--residual_wheel_pd --headless --steps 600` 실행 PASS. 마지막 base 위치는 [0.5908383, −0.0420460, 0.3182060] m이다. 이는 유한 실행/연결 검증이며 drift 개선이나 완전 정지의 증거가 아니다.
- 샌드박스 ROS에서 `getifaddrs: Operation not permitted` 메시지가 있었지만 node 생성·MuJoCo 실행·종료 및 모든 검사는 완료됐다. 외부 ROS 통신은 검증하지 않았다.
- `./scripts/agent-check.sh`: **전체 FAIL**. Python syntax 363개와 URDF 8개는 PASS지만, 기존 수정 파일 `my_flat_env_cfg.py`의 trailing whitespace 때문에 저장소 diff 검사가 실패했다. 해당 파일은 수정하지 않았다. 이번 변경의 diff 검사는 PASS다. 로그: `residual_wheel_pd_integration/agent_check.log`. 최종 task diff와 보존 확인: `task.diff`, `final_review.json`.
- 브랜치: `agent/codex/dev_tita_gluon`. Hardware 실행·재학습·배포 없음. 이전 실험의 model_100000 성능을 이번 model_50000에 일반화하지 않는다.

재현:

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=87 ROS_LOCALHOST_ONLY=1
export ROS_LOG_DIR="$PWD/docs/exp/2026-10-15/residual_wheel_pd_integration/ros_logs"
/home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_residual_wheel_pd.py
```

증거: [runtime_audit.json](residual_wheel_pd_integration/runtime_audit.json), [runtime_tests.log](residual_wheel_pd_integration/runtime_tests.log), [cli_headless.log](residual_wheel_pd_integration/cli_headless.log), 수정 전 파일 snapshot과 before.json.
