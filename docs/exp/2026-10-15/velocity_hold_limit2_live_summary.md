# 합 residual ±2 Nm MuJoCo 수동 viewer

Execution Domain: VALIDATION_SIM (소스/제어 동등성: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: PASS — 32초 smoke 완료 및 viewer 시작. 위치 복귀·수동 조작 장기 성능: NOT_TESTED.

Observed Metrics / Behavior / Log Summary:

요청에 따라 동기화 actor + 기존 FlashSAC leg/wheel + F-1 stop hold의 합 residual 한도를 ±2 Nm(바퀴당 최대±1 Nm 추가)로 올린 새 실행 파일 test/play_flash_velocity_hold_limit2.py를 추가했다. 기존 kp=2, kv=0.5, 1초 ramp, 2 Nm/s slew, zero-command gate, raw last_action, native axis sign, 최종 wheel effort clipping을 유지했다. 이전 실행 파일은 변경하지 않았다.

별도 32초 전진/정지/후진/정지 smoke: 실패 없음, hold3회 진입/2회 해제, leg torque 변경 오차0 Nm, residual bound/slew 검사 PASS. 이전 sweep의 BoundedStopHold(limit2)와1200개 synthetic sensor step의 출력/진단 dict가 정확히 같았으며2 Nm 포화, hold exit/re-entry 및 release를 포함했다: controller_equivalence.log.

기존 PID1219119의 ±1 Nm viewer에 Q를 보내 종료한 후 새로운 --viewer --manual 프로세스를 실행했다. 화면에 SYNC IMU 및 residual +/-2 Nm total을 표시한다. 초기 command=0. W/S 전후진 명령±0.1(최대±0.2), A/D 회전±0.15(최대±0.3), SPACE 정지, R reset, P 데모, Q 종료. 키를 떼어도 명령은 유지된다. live/telemetry.json에 relative p, 추정 v, 평가용 GT v와2 Nm 한도를 기록해 실제 움직임과 추정값을 비교할 수 있다. GT는 기존처럼 평가용이며 residual에는 사용하지 않는다.

이전 sweep에서±2 Nm는 포화를 해소했지만 정지점 복귀를 달성하지 못했다. 이번 viewer 시작 PASS는 위치 유지 성능 보장이 아니다. Hardware/ROS2 연결 없음.

신규 실행 파일·본 보고서·velocity_hold_limit2_live/ 증거 및 요청에 따라 종료한 이전 viewer의 최종 로그만 추가했다. agent-check.sh 결과는 agent_check.log, 기존 변경 보존과 최종 diff는 final_review.json/task.diff에 기록한다. 브랜치: agent/codex/dev_tita_gluon.

```bash
PYTHONDONTWRITEBYTECODE=1 MUJOCO_GL=glfw MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/play_flash_velocity_hold_limit2.py --viewer --manual --output docs/exp/2026-10-15/velocity_hold_limit2_live/new_live
```
