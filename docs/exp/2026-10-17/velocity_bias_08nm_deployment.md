# Velocity bias: 1–3초 추정, 추가 토크 ±0.8 Nm 구현·실기 배포·빌드

Execution Domains: DESKTOP_DRY_RUN (구현·단위/재생 검사·x86 빌드), VALIDATION_SIM (MuJoCo 비교), ROBOT_READ_ONLY (기존 소스/실행 상태 확인), ROBOT_STATE_CHANGING (사용자가 명시적으로 요청한 소스 배포·백업·ARM 빌드), ROBOT_COMMAND_FREE_RUNTIME (ROS/CAN/SDK 없는 순수 수학 fixture 실행)

Evidence Status: **PASS** — 구현의 제한·상태 전이 검사, 로컬/ARM 빌드·설치 hash·수학 재생, 짧은 MuJoCo 자세/토크 회귀. 실제 보정 ON 실기의 drift·자세 안정성·motor Nm calibration은 **NOT_TESTED**. 전체 repository agent-check는 기존 공백 오류로 **FAIL**.

Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`

ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`

Config SHA256: `d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d`

Branch: `agent/codex/dev_tita_gluon`

사용자는 ‘초기 1초 제외, 1–3초 추정, 이후 완만한 적용, 추가 토크 휠당 ±0.8 Nm’ 방향에 동의하고 **sim2real 코드 수정 및 실기체 배포·빌드**를 명시적으로 요청했다. 이 요청을 배포·빌드 승인으로 사용했다. 실제 모터 실행은 수행하지 않았다. Git commit/push/PR 요청은 없어 수행하지 않았다.

## 구현된 동작

- `velocity_bias` 기본값은 false다. true일 때 기존 단일 제어 loop 안의 휠 목표속도 보정 경로를 사용한다. 정책·관측·raw previous action·다리 PD·500Hz 송신 경로는 유지한다.
- RL 진입 후 zero-command neutral hold에서 **0–1초는 추정 평균에서 제외**하고, **1–3초는 보정 0으로 유지하며 속도와 pitch를 시간 가중 평균**한다. 약 3초 이후 적용한다. Movement command로 hold를 이탈했다가 중립으로 돌아오면 이 과정을 다시 시작한다.
- 기존 `3*v` torque seed를 제거했다. 추정 평균은 속도 LPF 초기 상태에만 사용하며 적분/보정 초기값은 0이다. 이후 현재 속도에 대해 적분 gain 4, LPF tau 0.1초를 유지한다.
- **1초 smoothstep envelope ramp**, **휠당 최대 0.8 Nm/s의 correction slew**를 적용한다. 적분값을 제한된 실제 bias 출력에 맞춰 tracking하여 amplitude/rate limit 뒤에 숨은 적분이 쌓이지 않게 했다.
- 추가 계산 토크 제한은 **휠당 ±0.8 Nm**다. 실제 좌우 wheel Kd를 node에서 전달하고 `u_limit = 0.8*radius/max(Kd_L,Kd_R)`로 공통 bias 범위를 제한한다. 선택 checkpoint의 Kd=0.5, radius=0.0925에서 ±0.148 m/s, 휠 목표 offset ±1.6 rad/s다. 좌우 Kd가 달라도 어느 휠도 0.8 Nm를 넘지 않으며 final effort clipping도 추가 차이를 증가시키지 않는다. 최종 wheel torque 전체 제한은 기존 ±12 Nm다.
- Movement-command hold 이탈, RL 이탈, invalid timing은 보정을 즉시 0으로 만들고 추정을 reset한다. 기존 command hysteresis `[.02,.02,.03]` 진입 / `[.04,.04,.06]` 이탈을 유지한다.
- 추정·적용 중 절대 roll/pitch >0.3 rad 또는 추정속도 >1 m/s이면 correction을 차단한다. 적용 시점 이후 **1–3초 평균 pitch에서 5° 초과 편차**도 차단한다. Guard가 걸리면 같은 hold 동안 자동 재획득하지 않고, movement-command 이탈/재진입 또는 RL reset을 기다린다. 1초 ramp와 5°는 이번 구현의 실험용 설정이며 실기 최적값으로 검증된 수치가 아니다.
- 획득한 drift/pitch 기준 및 guard 전이를 node console에 기록한다. Runner summary와 launch 설명도 새 제한·추정 시간에 맞췄다. 기존 11개 bias diagnostic 및 TrainingSample schema는 유지했다.

## 변경 파일

실기 production 파일 6개:

1. `sim2real/tita_ws/src/tita_controller/include/tita_controller/velocity_bias.hpp`
2. `sim2real/tita_ws/src/tita_controller/src/tita_node.cpp`
3. `sim2real/tita_ws/src/tita_controller/launch/flashsac.launch.py`
4. `sim2real/tita_ws/src/tita_controller/launch/tita.launch.py`
5. `sim2real/tita_ws/run_flashsac.sh`
6. `sim2real/tita_ws/README.md`

검증/배포 파일: 기존 `test/sim2real/velocity_bias_runtime.cpp` 갱신, 신규 `test/sim2real/test_velocity_bias_08nm.py`, `run_bounded_bias_mujoco.py`, `deploy_velocity_bias_08nm.sh`. 실제 변경 전 파일은 artifact `before/`에 보관했다. 이 보고서와 `velocity_bias_08nm_deployment/`에 모든 결과를 기록했다. 기존 unrelated dirty/untracked 파일을 수정·stage·revert하지 않았으며 시작/종료 git status 및 task diff를 확인했다.

## 실행한 검증

**PASS: 7개 단위/재생 테스트.** 초기 1초 제외·3초 전 무출력·zero seed·양방향 응답·ramp/slew·긴 포화 후 반전·좌우 비대칭 Kd·최종 effort clipping·pitch guard latch·command/RL exit·재획득·bias OFF의 정확한 기준 토크 일치를 검사했다. 네 기록의 총 **14,934 frame**을 수정된 수학 controller에 수동 입력하여 추가 토크 bound를 확인했다. 이는 기록된 상태를 사용한 shadow 계산이며 수정된 controller가 실제로 만들 미래 궤적은 아니다. [unit_tests.log](velocity_bias_08nm_deployment/unit_tests.log), [passive_replay.json](velocity_bias_08nm_deployment/passive_replay.json).

**PASS: x86 ROS Jazzy 전체 tita_controller C++ 빌드.** 기존 test 경로의 CMake build tree를 사용해 `tita_node`까지 compile/link했다. 실제 node 실행은 하지 않았다. [desktop_build.log](velocity_bias_08nm_deployment/desktop_build.log).

**PASS: MuJoCo의 실제 새 C++ controller로 4환경 × baseline/보정 20초 = 8회 비교.** 같은 seed 913, checkpoint와 초기조건을 각 pair에 사용했다. 모든 실행에서 roll/pitch 최대 <0.3 rad, 추가 wheel torque ≤0.8 Nm (Python float32 PD 비교 허용오차 1e−6 Nm), 다리 토크는 기준과 동일했다. 이 PASS는 짧은 회귀의 자세/토크 기준이며 절대 정지 성공 판정이 아니다.

| 환경 | 20초 최종 이동량 baseline → 보정 | 마지막 5초 평균 GT 전진속도 baseline → 보정 | 보정 최대 / wheel |
|---|---:|---:|---:|
| Nominal | 0.2736 → 0.0257 m | +0.01536 → +0.000033 m/s | 0.3294 Nm |
| 마찰 μ=0.2 | 0.3152 → 0.0371 m | +0.01711 → −0.000004 m/s | 0.3318 Nm |
| CoM 앞 5mm, mass ×1.15 | 1.4394 → 0.4580 m | −0.07485 → −0.01225 m/s | 약 0.8 Nm |
| CoM 뒤 5mm, mass ×1.15 | 1.9838 → 1.1865 m | −0.10083 → −0.05018 m/s | 약 0.8 Nm |

마지막 두 환경은 상한에 걸려 drift가 남는다. 요청한 0.8 Nm 상한을 임의로 높이지 않았다. 초기 실패 로그도 보존했다: 첫 harness 실행은 관측 key 이름을 수정한 뒤 재실행했고, strict 1e−8 Nm 비교는 float32 diagnostic/PD rounding 때문에 실패해 known double bias bound 복원 및 1e−6 Nm 수치 허용오차로 교정했다. 실제 C++ 토크 경로는 단위/ARM 검사에서 0.8 Nm 이하를 직접 확인했다. [mujoco.log](velocity_bias_08nm_deployment/mujoco.log), [mujoco_results.json](velocity_bias_08nm_deployment/mujoco_results.json).

이 실기 제한 law는 의도적으로 기존 sim2sim의 `3*v` seed/2초 acquisition과 달라졌다. 과거 sim2sim 동등성 실험을 현재 controller와 동일 알고리즘이라고 재사용하지 않는다. 이번 검증은 위 신규 bounded-law tests와 실제 C++/MuJoCo 비교를 대상으로 수행했다. 기존 sim2sim 소스는 변경하지 않았다.

## 실기 배포·빌드 증거

대상은 `robot@192.168.0.28:/home/robot/tita_ws`, ROS Humble ARM64다. 배포 전 로컬/원격 대상 6개 source hash가 일치했고 실행 중 `tita_node`가 없었다. Bringup service는 inactive였고, 이번 작업에서 service start/stop·MCU Ready/Direct·CAN 송신·joystick reader·controller 실행은 하지 않았다.

원격 **기존 소스 6개와 install/tita_controller 전체를 백업**한 뒤 검토한 8-member payload만 반영했다. 추가 두 member는 `test/velocity_bias_08nm/`의 pure-math fixture와 입력 데이터다. 배포 manifest의 모든 hash를 적용 전/후 확인했다.

- Backup: `/home/robot/tita_ws/docs/exp/2026-10-17/velocity_bias_08nm_deployment/before_deployment.tar.gz`
- Backup SHA256: `9b017e0c0f4441a158fb3f50fb550c73f806dbb2f48d97b72704acc0239df4b3`
- **PASS: `colcon build --packages-select tita_controller --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3`**, 1 package, 36.4초. [robot_deploy_build.log](velocity_bias_08nm_deployment/robot_deploy_build.log).
- Installed ARM node SHA256: `fd3f0285acfe42a60bb998e9d3824f4ff669bb326e934c9527e9893f9f26be95`
- Installed runner SHA256: `929cae68d5c065dc33e895c67dcc7164116f3ba4d057fc3add8e6a132eadc2d4`
- **PASS:** 설치된 launch/runner와 source 일치, ONNX/config pinned hash 유지, source된 ROS 환경의 ldd에서 missing library 없음. 설치 launch module을 import하여 정책 hash·33개 관측·8개 action을 검증했다. Node는 생성하지 않았다.
- **PASS:** ARM에서 SDK/ROS 없는 수학 fixture를 strict warning으로 compile/run, **3,407 frame × 29열**을 x86과 비교했다. 보정/주요 diagnostics 동일, 전체 최대 수치 차이 **3.55e−15**, 추가 토크 최대 **0.7999999999999999 Nm/wheel**. [robot_verify.log](velocity_bias_08nm_deployment/robot_verify.log), [arm_comparison.json](velocity_bias_08nm_deployment/arm_comparison.json).
- 최초 ldd 검증은 helper에서 ROS environment source보다 먼저 검사하여 실패했다. 순서를 고쳐 전체 verify를 재실행해 통과했다. 이 수정은 검증 helper에만 해당하며 production binary는 추가 변경하지 않았다.
- 최종 read-only 확인에서도 service inactive, tita_node 미실행이다. 실제 보정 ON 기체 성능·물리 Nm 단위·feedback polarity는 NOT_TESTED다.

## 실행 방법과 완료 검사

아래는 **operator가 실기 실험을 시작할 때 사용할 명령**이며 이번 작업에서는 실행하지 않았다. `velocity_bias`는 명시적으로 true를 줘야 켜진다.

```bash
# ROBOT_STATE_CHANGING: operator execution only
cd ~/tita_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch tita_controller flashsac.launch.py output_enabled:=true velocity_bias:=true
```

추정 완료 시 `velocity bias acquired: drift=..., pitch_reference=...`가 출력된다. Guard 차단 시 `velocity bias inhibited... correction OFF...`가 출력된다. 실제 추가 토크는 기존 bias diagnostic의 마지막 두 값으로 확인한다. 이는 계산된 command 차이이며 measured torque는 아니다.

필수 `./scripts/agent-check.sh`는 실행했다. Fast Python syntax **510/510**, URDF **8/8 PASS**이며 전체 결과는 기존 `my_flat_env_cfg.py` 431/437/443/449/455/461행 trailing whitespace 때문에 **FAIL**이다. 해당 파일은 수정하지 않았다. [agent_check.log](velocity_bias_08nm_deployment/agent_check.log). Bash syntax와 변경 launch Python syntax도 별도 확인했다. Production task diff, payload member list, hash manifest와 관련 없는 파일 변경이 없음을 검토했다. Git commit/push/PR 없음.
