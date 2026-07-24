# TITA + GLUON WBC 전체 워크플로 매뉴얼 (Closed-Loop Validation Manual)

이 매뉴얼은 **TITA 바퀴-다리 로봇**과 **INNFOS GLUON 로봇팔**의 강화학습(RL), 시뮬레이션 검증(Sim2Sim), 실시간 센서 미러링(Real2Sim), 그리고 온봇 실체 배포(Sim2Real / Direct Mode)를 실행하기 위한 전체 통합 가이드입니다.

---

## 📂 이관된 리포지토리 모듈 매핑

| 이관 폴더 (`tita_gluon_wbc/`) | 주요 구성 요소 | 워크플로 단계 |
| :--- | :--- | :--- |
| **`lab/`** | `ddt_lab` (Isaac Lab RL) | **1단계 (IsaacSim 학습)** & **2단계 (ONNX 내보내기)** |
| **`sim2sim/`** | `cosim`, `tita_gluon_urdf` | **3단계 (MuJoCo Sim2Sim)** & **4단계 (Read-Only Real2Sim)** |
| **`sdk/`** | `TITA-SDK-ROS2`, `innfos-cpp-sdk`, `tita_low_level_sdk` | **5단계 (하드웨어 인터페이스 & SDK)** |
| **`tita_gluon_ws/`** | `src/` (`ddt_ros2_control`), `deploy/` | **5단계 (온봇 정책 배포)** & **6단계 (Sim2Real Direct 실행)** |

---

## ⚠️ 안전 가이드라인 (AGENTS.md 규칙 준수)

> **[IMPORTANT]**
> - **Domain Naming**: 명령 실행 시 Execution Domain(`TRAINING_SIM`, `VALIDATION_SIM`, `DESKTOP_DRY_RUN`, `ROBOT_READ_ONLY`, `ROBOT_COMMAND_FREE_RUNTIME`, `ROBOT_STATE_CHANGING`)을 반드시 명시하십시오.
> - **Command-Free First**: 실기 테스트 5~6단계는 반드시 command-free dry-run (`fsm_mode=idle`, output disabled)으로 시작해야 합니다.
> - **Single Writer Invariant**: 모터 하드웨어 작성자(Hardware Writer)는 동시 단 1개 프로세스만 소유해야 합니다.

---

## 1. RL 학습 (`TRAINING_SIM`)

Isaac Lab 가상환경을 활성화하고 `ddt_lab` 패키지를 등록한 후 TITA + GLUON 정책을 학습합니다.

```bash
# 1. Isaac Lab 가상환경 활성화
source ~/isaac/env_isaaclab/bin/activate

# 2. ddt_lab 패키지 설치/등록
cd lab/ddt_lab
pip install -e .

# 3. RL 학습 실행 (NP3O 알고리즘)
python scripts/np3o/train.py \
  --task=DDT-Velocity-Flat-Tita-My-v0 \
  --num_envs 4096 \
  --headless
```


- **체크포인트 위치**: `lab/ddt_lab/logs/np3o/tita_flat/<run_id>/model_<iter>.pt`
- **관측/행동 설계**: Actuator delay + IMU/encoder bias 반영 모듈 적용.

---

## 2. Play & ONNX 내보내기 (`TRAINING_SIM` -> `DESKTOP_DRY_RUN`)

학습된 PyTorch 체크포인트를 ONNX 모델로 내보냅니다.

```bash
cd lab/ddt_lab

python scripts/np3o/play.py \
  --task=DDT-Velocity-Flat-Tita-My-Play-v0 \
  --checkpoint /path/to/model_3000.pt \
  --export_policy \
  --headless
```

- **산출물**: `<checkpoint_dir>/exported/policy.onnx`
- **인터페이스 검증**: `nn_input0 [1,33]`, `nn_input1 [1,10,33]`, `nn_output [1,8]`

---

## 3. MuJoCo Sim-to-Sim 검증 (`VALIDATION_SIM`)

ONNX 정책을 MuJoCo 독립 물리 시뮬레이터에서 검증합니다.

### 3.1 빌드 및 환경 설정
```bash
cd sim2sim/cosim
conda activate cosim
source /opt/ros/jazzy/setup.bash

colcon build --symlink-install
source install/setup.bash
```

### 3.2 ONNX 정책 파일 배치 및 검사
```bash
# ONNX 정책을 배포 디렉토리로 복사
cp /path/to/policy.onnx tita_gluon_ws/deploy/tita/policy.onnx

# ONNX 텐서 입력/출력 셰이프 검사
python3 sim2sim/cosim/scripts/inspect_onnx.py tita_gluon_ws/deploy/tita/policy.onnx
```

### 3.3 시뮬레이터 실행 및 명령 전달
```bash
# 시뮬레이터 및 PlotJuggler 실행
ros2 launch cosim_ros2_jazzy tita_mujoco_sim2sim.launch.py viewer:=true plot:=true tita_ns:=tita

# FSM 상태 전환: Stand-up -> RL Balance
ros2 topic pub --once /tita/command/manager/cmd_key std_msgs/msg/String "{data: transform_up}"
ros2 topic pub --once /tita/command/manager/cmd_key std_msgs/msg/String "{data: balance}"

# 전진 속도 명령 (vx = 0.05 m/s)
ros2 topic pub -r 10 /tita/command/manager/cmd_twist geometry_msgs/msg/Twist \
  "{linear: {x: 0.05, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

---

## 4. Read-Only Real-to-Sim 미러링 (`ROBOT_READ_ONLY`)

실제 로봇 센서 데이터만 수신하여 시뮬레이터에 미러링합니다. (하드웨어 제어 명령 수신 금지)

```bash
cd sim2sim/cosim
source install/setup.bash

# TCP Relay 수신기 및 MuJoCo 미러 실행
ros2 launch cosim_ros2_jazzy tita_mujoco_relay_real2sim.launch.py \
  server_host:=192.168.0.28 port:=50051 \
  real_tita_ns:=tita4252763 relay_ns:=tita_relay \
  viewer:=true mirror_base_orientation:=true
```

---

## 5. 정책 배포 (`DESKTOP_DRY_RUN` -> `ROBOT_COMMAND_FREE_RUNTIME`)

ONNX 모델을 온봇 SBC로 동기화하고 사전 사전 점검(Preflight)을 수행합니다.

```bash
cd tita_gluon_ws

# 정책 배포 및 preflight 검사 스크립트 실행
./deploy/deploy_tita_policy.bash ./deploy/tita/policy.onnx
```

- **기대 출력**: `POLICY DEPLOYMENT PASS`, `COMMAND OUTPUT: DISABLED`

---

## 6. Staged Sim-to-Real 실체 제어 (`ROBOT_STATE_CHANGING`)

> 🚨 **operator_arm 호출 전 물리적 안전 및 긴급 차단기 준비 필수**

```bash
cd tita_gluon_ws
source install/setup.bash

# 1. Unarmed Play Launch 실행 (Command Output Disabled)
ros2 launch tita_stage1_controller play.launch.py

# 2. Operator Arm (운용자 승인 서비스 호출)
ros2 service call /tita_lowlevel/runtime/operator_arm std_srvs/srv/SetBool "{data: true}"

# 3. 비상정지 / SAFE_HOLD 전환
ros2 service call /tita_stage1_controller/request_safe_hold std_srvs/srv/Trigger "{}"
```
