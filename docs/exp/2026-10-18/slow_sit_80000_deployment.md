# Supporting sit + frozen FlashSAC 80000 SBC deployment

- Date: 2026-10-18 (Asia/Seoul)
- Execution Domains: `DESKTOP_DRY_RUN`, `VALIDATION_SIM`, `ROBOT_READ_ONLY`, `ROBOT_STATE_CHANGING` (deployment/build only)
- Evidence Status: local parity `PASS`; simulation acceptance `SUSPICIOUS` (see limits); SBC build/ARM verification `PASS`; physical motion `NOT_TESTED`.
- Branch: `agent/codex/dev_tita_gluon`; no commit/push.
- Selected checkpoint: `lab/ddt_lab/logs/flash_sac/tita_flash_sac_201940_278440/model_80000/actor.pt`
- Checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`
- ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`
- Deployment config SHA256: `2072d9a4f0fb271b1f585e5d3f0193904ecf1f0665864d77d6e3e295b7d41e6d`

## Behavior

실기 C++에 앞선 `flashsac_sit_validation.md`의 선택 후보를 이식했다. RL에서 왼쪽 버튼을 올리면 `return_to_sit`로 바뀌고 4초 동안 지지 PD를 유지하며 앉는다. 초기 유효 관절 목표는 직전 최종 토크(RL + 활성 bias 포함)와 관절 속도로 역산하여, 토크를 이어받으면서 피드백 게인이 처음부터 전부 작동하도록 한다. 목표는 smoothstep과 허벅지 0.3 rad 호를 거쳐 원래 sit PD/피드포워드와 같은 목표로 이동한다.

휠에는 IMU/encoder와 nominal FK로 계산한 CoM 기울기의 30/5/1 균형 보상이 들어간다. 무릎이 접히면 보상을 줄이고 최종 감쇠로 연결한다. ROS/CAN 송신자를 추가하지 않고 기존 500 Hz 최종 토크 경로와 다리 ±60 / 휠 ±12 Nm clipping을 그대로 쓴다. 기체에 MuJoCo를 설치하거나 모델 상태를 읽을 필요는 없다. FK 상수는 기존 corrected MuJoCo 모델에서 생성했고 1000개 임의 자세로 수치 일치를 검증했다.

오른쪽 재누름 또는 조종기 단절은 즉시 RL을 중단하고 `estop`을 고정한다. 정상 센서의 RL/sit/return에서는 같은 지지 앉기를 수행한다. 진행 중인 return에서 stop하면 경로와 시계를 재시작하지 않는다. 앉기가 끝나도 estop은 유지하고 RL 재진입을 막는다. 초기 idle/미완료 transform 상태의 stop, 센서·과도한 기울기·추론 오류는 기존 감쇠를 쓴다. estop 중에도 hard fault는 지지 앉기를 취소하지만 정지 latch는 유지한다. 감쇠 fault 이후 자동 지지/RL 복구는 없다.

`idle -> transform_up -> sit -> rl` 준비 과정, 조이스틱 edge/1초 hold 조건, 토크 부호와 native 좌우 순서는 유지했다. 새 정책도 33개 관측/8개 행동/50 Hz 형식이다. 출처 task는 `DDT-Velocity-Flat-Tita-My-BaseComShift-v0`이며 메타데이터 이름을 바꾸지 않았다. 원본 actor/export는 수정하지 않았다. 배포 복사본은 기존 조이스틱 범위인 전진 ±1 m/s, yaw ±1 rad/s를 유지하도록 export의 0.2/0.3 command cap만 명시적으로 덮어썼다. 별도의 manifest 필드로 원본 config hash와 override를 기록했다. 50000/60000/75000 번들은 보존한다.

`velocity_bias` 제어 법칙·한도는 이번 작업에서 변경하지 않았다. 기본값 false와 기존 활성화 옵션, training sample/motor feedback/rosbag 기록 경로를 유지한다. run ID는 `flashsac_80000_*`으로 바뀐다. 시뮬레이션은 모두 bias OFF이다.

## Validation evidence

Artifacts: [`slow_sit_80000_deploy/`](slow_sit_80000_deploy/).

| Domain / check | Result / evidence |
|---|---|
| DESKTOP_DRY_RUN / source actor vs ONNX | PASS, SHA identity + 256 samples max action error 4.411e-6 (`export_parity_final.log`) |
| DESKTOP_DRY_RUN / native PyTorch actor vs C++ ORT 1.19.2 | PASS, 256 observations, max error 3.457e-6; corrupt config/ONNX rejected (`setup.log`) |
| DESKTOP_DRY_RUN / sensor/adapter/state parity | PASS, obs error 1.20e-7, RL torque 7.17e-6, startup torque 1.17e-4, zero state mismatches/6000 (`parity.log`) |
| DESKTOP_DRY_RUN / pure FK and sit torque parity | PASS, 1000 random FK angles error 2.442e-15 rad, 5000 torque cases error 2.220e-12 Nm (`supporting_sit.log`) |
| DESKTOP_DRY_RUN / button/state/fault | PASS, 10 scenario groups including return interruption and hard fault during latched stop (`buttons.log`) |
| DESKTOP_DRY_RUN / portable x86 replay | PASS, 1000 fixtures max error 1.377e-14 (`replay.log`) |
| DESKTOP_DRY_RUN / runner/launch/recording mocks | PASS, 22 tests (`logging_tests_pass.log`); no real service/CAN commands |
| ROBOT_STATE_CHANGING / build | PASS, 1 package / 36.4 s (`remote_build.log`) |
| ROBOT_STATE_CHANGING / ARM replay / install validation | PASS, installed hashes/linkage + 10 button scenarios + 1000 ARM replay cases, max error 9.361e-13 (`remote_verify.log`) |
| Hardware motion / timing | NOT_TESTED; no robot controller was launched |

초기 보조 검증 실패 로그도 보존했다. `load_policy`의 task guard가 현재 training default에 의존하여, 참조 검증을 저장한 아키텍처와 실제 task metadata로 구성했다. batch=1 ONNX는 입력별 추론으로 수정했다. 기존 runner 테스트의 ±2 m/s / 3 m/s² / cap 거절 문구 기대값은 현재 구현된 ±0.8 Nm / slew 0.8 Nm/s에 맞췄다. 이 수정으로 production bias law를 바꾸지 않았다.

## New-policy simulation findings and limits

Plant: MuJoCo 3.10.0, flat floor, native C++ controller math; policy Python ORT 1.27.0. Runtime C++ ORT tested separately at 1.19.2. Plant/IMU/encoder only feed the controller. No physics oracle, RLS, adaptation or learning.

| New-policy scenario | Max downward speed | Peak floor normal | Peak tilt | Result |
|---|---:|---:|---:|---|
| Neutral seed 42, production return/stop | 0.1112 m/s | 497.4 N | 10.01 deg | acceptance PASS |
| Neutral seed 270, production return/stop | 0.1109 m/s | 512.7 N | 10.01 deg | contact force criterion FAIL |
| Neutral seed 913, production return/stop | 0.1113 m/s | 503.3 N | 10.03 deg | acceptance PASS |
| Forward command +0.25 m/s, seed 42 | 0.1046 m/s | 432.6 N | 7.68 deg | travel criterion FAIL: 0.639 m |

각 항목의 return/stop은 물리 궤적이 같고 latch/final state가 다르다. 중립 6개 rollout 중 acceptance 4 PASS / 2 FAIL이며, 이동 2개는 travel FAIL이다. rollout 실행 자체는 모두 PASS, fault 없음. 2mg(약 504 N), 이동 0.5 m 등은 앞선 실험과 같은 사전 실험 기준이며 기체 제조사 사양이 아니다. forward 테스트는 최종 수평 속도 약 1.63e-5 m/s로 멈췄지만 이동 거리가 기준을 넘었다. 즉 이 동작은 토크를 즉시 끊는 방식이나 즉시 정지거리를 보장하는 방식이 아니다.

앞선 model_60000에서는 nominal acceptance 18/18 PASS였지만 mismatch C의 접촉력은 FAIL이었다. 새 정책으로 바꾸었으므로 그 성공률을 그대로 적용하지 않는다. model_80000의 mismatch, reverse/yaw/max-command, 외란, 실제 지지 조건 및 bias ON 조합은 NOT_TESTED이다. 실제 앉기 속도/충격/이동거리가 시뮬과 같다고 주장하지 않는다.

## Deployment and operator command

Operator explicitly requested SBC update after powering on the robot. Read-only preflight confirmed SSH access and no `tita_node` process. Only selected files are transferred; existing source SHA checks must match before extraction. Backup includes the old source and installed controller package. No service stop/start, MCU command, CAN command or physical controller execution is part of deployment/build verification. ARM verification executables link only pure math and do not instantiate the robot SDK.

SBC backup/build/verification: `~/tita_ws/docs/exp/2026-10-18/slow_sit_80000_deploy/`.

```bash
# ROBOT_STATE_CHANGING — operator execution, not executed by the agent
cd ~/tita_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch tita_controller flashsac.launch.py output_enabled:=true
# velocity_bias:=true remains available; its combination with this stop is NOT_TESTED.
```

All experiment console/ROS/bag logs remain under `~/tita_ws/docs/exp/YYYY-MM-DD/` with Korea date. A right-button software stop stays latched until restart.

## Scope / required checks

Production changes: `state_machine.hpp`, new `supporting_sit.hpp` / `sit_geometry.hpp`, node sensor/stop handoff, pinned public launch and runner, new `policies/flashsac_80000/{policy.onnx,config.json,manifest.json}`, README. Tests: FK export/parity/replay/deploy scripts, native simulation bridge/harness, button scenarios, policy/setup/logging checks. No SDK, robot networking configuration, training config, residual or online learning changes.

`agent-check.sh` predeployment: FAIL solely from six pre-existing trailing whitespace lines in `my_flat_env_cfg.py` (431/437/443/449/455/461). Python syntax 541 PASS / 0 FAIL and URDF 8 PASS. These unrelated changes are preserved. Final check: `agent_check_final.log`. Scoped source hash audit: `scope_audit.json`; the five requested existing workspace files changed and other pre-existing workspace sources were preserved. The new files are the two sit headers and three policy bundle files. Final installed executable identity and backup hash are in `installed.sha256` / `backup.sha256`.
