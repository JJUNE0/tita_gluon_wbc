# kv24 / residual 활성화 ramp1.5초 MuJoCo 수동 viewer

Execution Domain: VALIDATION_SIM (동등성/소스 검사: DESKTOP_DRY_RUN)

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`

ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: PASS — 요청 설정 실행 및32초 smoke. 장기 수동 정지 성능: NOT_TESTED.

Observed Metrics / Behavior / Log Summary:

요청한 kv=24, residual smoothstep activation ramp=1.5초로 새 test/play_flash_velocity_hold_kv24.py를 추가했다. kp=2, 합 residual±2 Nm(바퀴당 추가분 최대±1 Nm), 합 slew2 Nm/s, actor IMU 동기화, 기존 FlashSAC wheel/leg PD 및 전체 raw last_action은 유지했다. 실제 조작 경로는 기존 실험 viewer와 같고 ROS2/hardware 연결은 없다. 다른 sim2sim 패키지/launch/state machine은 변경하지 않았다.

32초 전진/정지/후진/정지 smoke는 실패 없이 완료했고 leg torque 변경 오차0 Nm, residual bound/slew 검사 PASS다. 1200개의 synthetic sensor step에서 기존 ablation의 TunedStopHold(kv24,ramp1.5)와 출력/진단 dict가 정확히 일치했다. Hold exit/re-entry, slew,2 Nm 포화/release를 포함했다: controller_equivalence.log.

기존 PID1240318의 kv0.5/ramp1초 residual viewer를 Q로 정상 종료하고 새 --viewer --manual 프로세스를 실행했다. 화면에 kv=24/ramp=1.5s/residual +/-2 Nm total을 표시한다. W/S 전후진±0.1(최대±0.2), A/D 회전±0.15(최대±0.3), SPACE 정지, R reset, P 데모, Q 종료. 키를 떼어도 명령은 유지된다. 초기 command는0이다. live/telemetry.json에 kv24/ramp1.5, p와 추정 v/평가용 GT v를 기록하며 GT는 residual에 입력하지 않는다.

새 viewer 시작과 smoke PASS는 완전 정지/원점 복귀 보장이 아니다. 이전 ablation에서 밀림 감소와 잔류 속도 증가의 tradeoff가 확인됐다.

신규 실행 파일·본 보고서·velocity_hold_kv24_live/ 증거 및 요청한 이전 viewer 종료 로그를 추가했다. 기존 소스 hash/변경 보존 및 final diff는 final_review.json/task.diff, agent-check.sh는 agent_check.log에 기록한다. 브랜치: agent/codex/dev_tita_gluon.

```bash
PYTHONDONTWRITEBYTECODE=1 MUJOCO_GL=glfw MPLCONFIGDIR=/tmp/lqr_mpl /home/cocel/venvs/cosim_ros2_jazzy/bin/python test/play_flash_velocity_hold_kv24.py --viewer --manual --output docs/exp/2026-10-15/velocity_hold_kv24_live/new_live
```
