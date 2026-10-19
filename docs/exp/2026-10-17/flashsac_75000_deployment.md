# FlashSAC model_75000 교체·배포·빌드

Execution Domains: DESKTOP_DRY_RUN (bundle와 순수 수학·추론 검사), ROBOT_READ_ONLY (기존 파일 hash·실행 상태 확인), ROBOT_STATE_CHANGING (명시적으로 요청한 정책 교체와 ARM 빌드), ROBOT_COMMAND_FREE_RUNTIME (ROS node·CAN·SDK 없는 ARM ONNX 추론).

Evidence Status: PASS — 로컬/ARM 추론·설치 hash·ARM colcon 빌드. 실기 model_75000의 기립·drift·명령 응답은 NOT_TESTED. 전체 agent-check는 기존 공백 오류로 FAIL.

Policy Checkpoint SHA256: `381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730`

ONNX SHA256: `2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114`

Config SHA256: `34817048ee7b40836d84de632dff4abfe5b0feb50f3a5f861e951f332450cfae`

Branch: `agent/codex/dev_tita_gluon`

사용자가 50000 실험 후 같은 run의 75000으로 먼저 교체하고 50000 분석을 이어가도록 명시적으로 요청했다. actor는 `lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_75000`이며 기존 검증된 export ONNX를 byte-identical하게 새 bundle로 보관했다. [앞선 후보 비교](flashsac_hardware_candidates.md)에서 75000의 명령 과응답을 확인했으므로 이번 파일·추론 검증 PASS를 실기 우월성의 증거로 해석하지 않는다.

## 변경

- 신규 `sim2real/tita_ws/src/tita_controller/policies/flashsac_75000/{policy.onnx,config.json}`. robot PD·limits·observation/action 설정은 기존 50000과 같음을 assert했고, command 최대 1.0m/s·1.0rad/s를 유지했다. config의 policy path는 portable `policy.onnx`다.
- `sim2real/tita_ws/src/tita_controller/launch/flashsac.launch.py`: bundle와 고정 hash를 75000으로 선택.
- `sim2real/tita_ws/run_flashsac.sh`: bundle·checkpoint hash·`flashsac_75000_...` 로그 ID를 일치시킴.
- `sim2real/tita_ws/README.md`, `test/sim2real/test_flashsac_setup.py`: 현재 선택 정책과 검증 경로를 갱신.
- 신규 배포 helper `test/sim2real/deploy_flashsac_75000.sh`, fixture 입력·PyTorch 기준과 수정 전 test snapshot은 `test/sim2real/flashsac_75000_work/`에 보관.

기존 50000/60000 bundle은 보존했다. C++ controller·velocity-bias law는 수정하지 않았다. bias 기본 false, motor output 기본 false다. 로봇 노드·서비스 start/stop·MCU·CAN·모터 명령은 수행하지 않았다.

## 검증

- **PASS:** native PyTorch ↔ x86 C++ ONNX, 256개 관측 최대 action 오차 **2.384e−6**. 손상된 config/ONNX 거부, 33obs/8actions/50Hz, finite/deterministic 및 순수 C++ 상태 검사. [로그](flashsac_75000_deployment/native_parity.log).
- **PASS:** Python/C++ adapter 50개 입력: 관측 최대오차 **1.20e−7**, torque **7.17e−6 Nm**. 6,000 step state-machine torque 오차 **1.17e−4 Nm**, 상태 불일치 **0/6000**. [로그](flashsac_75000_deployment/adapter_parity.log).
- **PASS:** runner 및 새 배포 helper의 Bash syntax. 변경 전 local snapshot과 최종 task diff를 확인했다.
- **PASS:** 원격 `robot@192.168.0.28:/home/robot/tita_ws`는 배포 전 controller/joystick 미실행, bringup inactive였다. 기존 50000 설치 hash를 확인하고 whitelist 9-member payload 적용 전 source/install을 백업했다. source/install bundle·launch·runner 일치, 이전 50000/60000 hash 보존, library missing 없음, launch import와 33obs/8actions/50Hz parameter 변환을 확인했다.
- **PASS:** ROS Humble ARM `colcon build --packages-select tita_controller --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3`: **1 package, 1.16초**. C++가 동일한 증분 빌드·설치다. [빌드 로그](flashsac_75000_deployment/robot_deploy_build.log).
- **PASS:** 설치된 ONNX로 ARM C++ 순수 추론 256개를 PyTorch와 비교, 최대 action 오차 **2.563e−6**. 검증 종료 시에도 controller/joystick 미실행·bringup inactive. [검증 로그](flashsac_75000_deployment/robot_verify.log), [결과](flashsac_75000_deployment/arm_parity.json).
- 필수 `./scripts/agent-check.sh`는 [로그](flashsac_75000_deployment/agent_check.log)에 보관한다. Python syntax와 URDF는 PASS, 전체는 기존 `my_flat_env_cfg.py` 431/437/443/449/455/461행 공백 오류로 FAIL이다. 해당 파일은 수정하지 않았다.

## 백업·설치

이전 source launch·runner·README, 50000/60000 bundle, install/tita_controller 전체:

`/home/robot/tita_ws/docs/exp/2026-10-17/flashsac_75000_deployment/before_deployment.tar.gz`

Backup SHA256: `780819892e2b875698cdf7273a8181ba87a02b3a036d1fb89c3200c61487bc5a`.

설치 node SHA256: `fd3f0285acfe42a60bb998e9d3824f4ff669bb326e934c9527e9893f9f26be95` (이전과 동일). Runner SHA256: `f348d1ac4641c26b3bdd8b19f17d906d24a12568c6112b459980c58f3d0ab044`. [설치 hash](flashsac_75000_deployment/installed.sha256).

아래는 operator 실행용이며 이번 작업에서는 실행하지 않았다.

```bash
# ROBOT_STATE_CHANGING: operator only
cd ~/tita_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch tita_controller flashsac.launch.py output_enabled:=true velocity_bias:=false
```

이후 [50000 결과 분석](flashsac_50000_real_review.md)을 수행했다. 코드·보고서·실험 artifact 외의 사용자 변경은 수정하지 않았고 commit/push 없음. 실기 성능 판정은 이후 operator 실행 기록이 필요하다.
