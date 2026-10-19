# FlashSAC model_50000 교체·실기 배포·빌드

Execution Domains: DESKTOP_DRY_RUN (bundle·launch·adapter·native inference 검증), ROBOT_READ_ONLY (원격 상태·기존 hash 확인), ROBOT_STATE_CHANGING (명시적으로 요청된 정책 파일 배포·백업·빌드), ROBOT_COMMAND_FREE_RUNTIME (ROS node·SDK·CAN 없는 ARM ONNX 추론).

Evidence Status: PASS — 정책·설정 hash, x86/ARM 추론, adapter/state machine 비교, ARM colcon 빌드 및 설치 검증. 실제 model_50000의 실기 drift·기립·명령 추종 성능은 NOT_TESTED. Repository agent-check 전체는 기존 공백 오류로 FAIL.

Policy Checkpoint SHA256: `d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c`

ONNX SHA256: `0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873`

Config SHA256: `08bf0628ddcfc1bbd964573b56cc64f7b9889476f247098ba5e53b324ed7b6e8`

Branch: `agent/codex/dev_tita_gluon`

## 변경과 승인 범위

사용자가 같은 run의 model_50000 정책 교체·실기체 배포·빌드를 명시적으로 요청했다. 대상 actor는 `lab/ddt_lab/logs/flash_sac/tita_flash_sac_115632_883848/model_50000`이다. [직전 후보 평가](flashsac_hardware_candidates.md)의 hash 검증된 ONNX를 사용했다. 첫 SSH는 sandbox 네트워크 제한으로 실패했고, 승인된 배포 범위의 SSH/SCP를 도구 권한 확장으로 실행했다. 추가 사용자 확인은 요구하지 않았다.

- 신규 `sim2real/tita_ws/src/tita_controller/policies/flashsac_50000/{policy.onnx,config.json}`. ONNX는 기존 export와 byte-identical하다. 설정의 command 최대값은 기존 실기 1.0 m/s·1.0 rad/s를 유지하고, 사용되지 않는 PC 전용 policy path를 `policy.onnx`로 정리했다. observation/action·PD·effort·주기는 기존 bundle과 동일하다.
- `sim2real/tita_ws/src/tita_controller/launch/flashsac.launch.py`: 50000 bundle과 checkpoint/ONNX/config 고정 hash로 교체.
- `sim2real/tita_ws/run_flashsac.sh`: 설치 bundle 경로, summary checkpoint hash, run ID를 `flashsac_50000_...`으로 일치시켰다.
- `sim2real/tita_ws/README.md`: 현재 정책·검증 경로·기존 60000 보관과 복구 조건을 갱신.
- `test/sim2real/test_flashsac_setup.py`: 선택 정책과 native reference를 50000으로 변경. 신규 `test/sim2real/deploy_flashsac_50000.sh` 및 `test/sim2real/flashsac_50000_work/`의 입력·기준 결과·수정 전 test snapshot을 사용했다.

기존 60000 bundle은 유지했다. controller C++와 velocity-bias law는 수정하지 않았다. bias는 기본 false이고 output도 기본 false다. 모터 실행·service start/stop·MCU/CAN 명령은 이번 작업에서 수행하지 않았다.

## 실제 실행한 검증

1. **PASS:** ROS Jazzy 환경의 `test_flashsac_setup.py --torch-python .../online_rl/bin/python`. Native FlashSAC PyTorch와 x86 C++ ONNX의 256개 observation 최대 action 오차 **2.623e−6**. config/ONNX 손상 거부, 33obs/8actions/50Hz, deterministic inference 및 순수 C++ 상태 전이 검사 포함. [로그](flashsac_50000_deployment/native_parity.log).
2. **PASS:** `test_sim2real_parity.py .../flashsac_50000`. 50개 입력의 observation 최대 오차 **1.20e−7**, torque **7.17e−6 Nm**, 6,000 step 상태 torque **1.17e−4 Nm**, 상태 불일치 **0/6000**. [로그](flashsac_50000_deployment/adapter_parity.log).
3. **PASS:** runner·배포 helper의 `bash -n`. 수정 전후 local task diff를 확인했다. bundle 생성 시 기존 robot·observation·action 설정 일치를 assert했다.
4. **PASS:** 원격 `robot@192.168.0.28:/home/robot/tita_ws`의 기존 source·설치 hash 확인 후, whitelist 9-member payload를 적용했다. 배포 전/검증 후 controller·joystick 미실행, `tita-bringup.service` inactive. source 및 installed file 일치, 고정 bundle hash, launch import와 generic parameter 변환, 동적 library missing 없음 확인. 실제 node는 생성하지 않았다.
5. **PASS:** ARM ROS Humble `colcon build --packages-select tita_controller --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3`. **1 package, 1.15초**. C++ 소스가 바뀌지 않은 증분 빌드/설치다. [로그](flashsac_50000_deployment/robot_deploy_build.log).
6. **PASS:** 설치된 새 ONNX를 ARM C++에서 순수 추론하고 별도의 native PyTorch 기준 256입력과 비교. 최대 action 오차 **2.906e−6**, finite/deterministic 및 순수 상태 검사 통과. [원격 검증 로그](flashsac_50000_deployment/robot_verify.log), [결과 JSON](flashsac_50000_deployment/arm_parity.json).
7. **PASS:** `./scripts/agent-check.sh`의 Python 구문 **513/513**, URDF **8/8**. **FAIL:** 전체는 기존 `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py` 431/437/443/449/455/461행 trailing whitespace 때문이다. 해당 파일은 수정하지 않았다. [로그](flashsac_50000_deployment/agent_check.log).

## 설치와 백업

설치 node SHA256은 이전과 같은 `fd3f0285acfe42a60bb998e9d3824f4ff669bb326e934c9527e9893f9f26be95`다. 새 runner는 `efecc46632524e6926d2f7ea14d9c31dd09d60ca293b090639a8e67344d0d861`. [설치 hash](flashsac_50000_deployment/installed.sha256).

이전 source launch·runner·README, 60000 bundle, install/tita_controller 전체를 원격에 백업했다:

`/home/robot/tita_ws/docs/exp/2026-10-17/flashsac_50000_deployment/before_deployment.tar.gz`

Backup SHA256: `c556b4fc9b27290ebe9ad944405b048602f1c8020a6b6e63439b6884e60c7db0`. [백업 hash](flashsac_50000_deployment/backup.sha256). 복구 시에는 컨트롤러가 정지한 상태에서 기존 launch와 runner, 설치 파일을 함께 복구해야 정책 경로·hash·로그 ID가 일치한다. 이번 작업은 복구를 실행하지 않았다.

아래는 **사용자 실행용** 새 정책 단독 실험 명령이다. 이번 작업에서 실행하지 않았다.

```bash
# ROBOT_STATE_CHANGING: operator only
cd ~/tita_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch tita_controller flashsac.launch.py output_enabled:=true velocity_bias:=false
```

변경 범위는 위 파일과 실험 artifact뿐이다. 시작/종료 status, 수정 전 snapshot 대비 task diff, 신규 파일 내용을 검토했다. 기존 사용자 변경의 revert·stage 및 commit/push는 하지 않았다. 실기 성능은 이후 operator 실행 로그로 별도 평가해야 한다.
