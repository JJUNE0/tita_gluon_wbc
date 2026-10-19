# 동기화 IMU 수동 조작 MuJoCo 재실행

Execution Domain: VALIDATION_SIM (소스 검사: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: PASS — 32초 headless smoke 완료, 동기화 actor 및 기존 stop-hold 경로 실행. 수동 조작 장기 성능: NOT_TESTED.

Observed Metrics / Behavior / Log Summary:

신규 `test/play_flash_velocity_hold_sync.py`로 actor quaternion/gyro를 현재 joint qpos/qvel 시점의 clone mj_forward 센서와 맞췄다. 기존 실행 파일/정책/PD/last_action 및 StopHold 제어식은 보존했다. Command ramp는 추가하지 않았다. 명령 ±0.2 m/s에 실제 속도 약 ±0.5 m/s인 추종 문제는 해결 범위 밖이다. Root 위치/속도는 residual에 사용하지 않으며 기존 33-value actor observation도 선속도를 포함하지 않는다.

32초 seed42 smoke: 실패 없음, hold 진입 3회/해제 2회, leg torque 변경 오차 0 Nm, residual ±1 Nm 및 slew 2 Nm/s 검증 PASS. raw 결과는 velocity_command_hold_sync/smoke/result.json, trace.npz, smoke.log. 기존 reset 직후의 residual 재시작은 새로운 검증 segment로 처리해 reset 경계에서만 slew 연속성 검사를 제외한다.

요청한 기존 TITA viewer를 Q로 종료하고 새 viewer를 --manual로 시작했다. 초기 command=0. W/S vx ±0.1 (범위 ±0.2), A/D yaw ±0.15 (범위 ±0.3), SPACE 정지, P 자동 데모, R 초기화, Q 종료. 키를 떼어도 명령은 유지된다. 새 창에는 SYNC IMU가 표시된다. ROS2 연결과 hardware 실행은 없다. live/telemetry.json 및 run.log로 GUI 실행을 기록한다.

기존 파일 hash/변경 상태 보존 검사와 이번 변경 diff는 velocity_command_hold_sync/final_review.json 및 task.diff, agent-check 결과는 agent_check.log에 기록한다. 신규 실행 파일/본 보고서/실험 증거만 추가했다.

브랜치: agent/codex/dev_tita_gluon.

```bash
PYTHONDONTWRITEBYTECODE=1 MUJOCO_GL=glfw MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/play_flash_velocity_hold_sync.py --viewer --manual --output docs/exp/2026-10-15/velocity_command_hold_sync/new_live
```
