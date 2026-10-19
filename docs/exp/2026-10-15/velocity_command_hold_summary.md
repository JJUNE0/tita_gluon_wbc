# Velocity command + relative F-1 hold MuJoCo demo

Execution Domain: VALIDATION_SIM (코드·GUI 접근 검사: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: PASS — command/hold gate·토크 제한·32초 무전도 데모·GUI 실행. SUSPICIOUS — 실제 속도 추종 오차와 잔류 정지 drift.

Observed Metrics / Behavior / Log Summary:

동일 FlashSAC policy와 기존 wheel/leg PD를 유지하면서 이동 명령과 F-1 정지 hold를 연결했다. MuJoCo passive viewer를 로컬 :0 데스크톱에 실행했다. ROS2 노드/토픽/실제 로봇은 사용하지 않는다.

- 이동 명령: residual 목표를 0으로 두고 최대 2 Nm/s로 해제한 뒤 FlashSAC 제어만 적용한다. 이동 중 상대 위치 추정기는 적분하지 않는다.
- 정지 진입: encoder/동기화 IMU odometry를 한 번 reset하여 p_ref=0을 잡는다. 실제 속도가 남아 있어도 command가 정지이면 hold를 유지한다. 초기 정지부터 hold를 적용한다.
- Hold: −2p−0.5v, 합 토크 ±1 Nm, 1초 smoothstep ramp, 합 slew 2 Nm/s, 각 wheel에 축 부호를 적용해 절반씩 더한다. Leg torque와 full raw last_action은 원래 경로를 유지한다.
- Command hysteresis: enter |vx|/|vy|≤0.02 m/s, |yaw|≤0.03 rad/s; leave |vx|/|vy|≥0.04 m/s 또는 |yaw|≥0.06 rad/s. Cmd 0에서만 원점을 매 tick reset하는 방식이 아니다.
- Demo 32초 반복: 정지2초 → +0.2 m/s 전진5초 → 정지10초 → −0.2 m/s 후진5초 → 정지10초. 외부 push는 없다. 키를 누르면 자동 데모를 해제하고 직접 조작한다.

## 조작

W/S: vx를 ±0.1 m/s씩 변경(한도 ±0.2). A/D: yaw를 ±0.15 rad/s씩 변경(한도 ±0.3). Space: 정지. P: 자동 데모 전환. R: 시뮬레이션 초기화. Q/창 닫기: 종료. 키는 MuJoCo 창에 포커스를 두고 입력한다.

## 실행 결과 및 범위

Headless seed42, pitch perturbation0, 32초 완료: PASS, failures=[]. Hold 진입 3회(0/7/22초), 해제 2회(2/17초). 진입 시 p=0 확인. Leg torque 최대 경로 차이 0.0 Nm.

각 hold 구간의 진입 위치 대비 최대 planar 이동은 약 0.087/0.276/0.478 m다. 정지 명령 순간에 원점을 잡았으므로 감속 중 이동도 포함한다. 정지 후 drift 0이나 stopping distance 최적화를 달성했다고 해석하지 않는다.

전진 구간 3–7초의 평균 실제 sagittal axle velocity는 약 +0.430 m/s, 후진 18–22초는 약 −0.475 m/s였다(명령 ±0.2 m/s). 이동 중 residual은 해제됐으며 이 결과로 velocity tracking이 정확하다고 주장하지 않는다. 정책/기존 adapter를 재튜닝하지 않았다. Yaw 명령 gate는 단위 검사에서 검증했으나 yaw tracking의 정량 평가는 NOT_TESTED다.

Unit tests 2개 PASS: 정지 진입당 1회 reset·실제 이동에도 hold 유지, yaw 포함 hysteresis·포화·slew·이동 residual 해제. 기존 source/설정/보고서는 보존하고 신규 test/play_flash_velocity_hold.py, test/test_velocity_command_hold.py와 본 날짜 실험 증거만 추가했다.

초기 headless.log는 manifest 저장 함수 import 누락으로 simulation 전에 종료됐고 수정했다. 본 결과는 headless_checked만 사용한다.

GUI는 사용자 조작을 위해 계속 실행하며, 종료 시 live/trace.npz와 result.json을 기록한다. 실행 중 상태는 live/telemetry.json 및 run.log에 있다. 실행 시점 source/checkpoint hash는 manifest.json에 기록했다.

./scripts/agent-check.sh 및 최종 diff/기존 변경 보존 결과: agent_check.log, final_review.json, task.diff. 브랜치: agent/codex/dev_tita_gluon.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/test_velocity_command_hold.py
PYTHONDONTWRITEBYTECODE=1 MUJOCO_GL=glfw /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/play_flash_velocity_hold.py --viewer --output docs/exp/2026-10-15/new_velocity_hold/live
```
