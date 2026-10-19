# TITA + GLUON Whole-Body Control

Isaac Lab 학습 → MuJoCo sim2sim 검증 → ROS 2 실기 실행.

| 경로 | 용도 |
|---|---|
| `lab/ddt_lab` | Isaac Lab 학습 환경과 FlashSAC |
| `sim2sim` | MuJoCo 검증 및 로봇 모델 |
| `sim2real/tita_ws` | TITA 실기 controller |
| `sdk` | 하드웨어 SDK |

## 1. 환경 구축 (`DESKTOP_DRY_RUN`)

저장소 루트에서 시작한다. 새 터미널에서는 `TITA_REPO`를 다시 설정한다.

```bash
export TITA_REPO="$PWD"
source ~/isaac/env_isaaclab/bin/activate
cd "$TITA_REPO/lab/ddt_lab"
pip install -e .
cd "$TITA_REPO"
```

[Isaac Lab 설치 안내](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/isaaclab_pip_installation.html). 현재 기준: Isaac Sim 5.1 / Python 3.11.

MuJoCo 환경은 처음 한 번 생성한다 (Ubuntu 24.04 / ROS Jazzy, 시스템 Python 3.12).

```bash
source /opt/ros/jazzy/setup.bash
/usr/bin/python3 -m venv --system-site-packages ~/venvs/cosim_ros2_jazzy
~/venvs/cosim_ros2_jazzy/bin/python -m pip install mujoco==3.10.0 onnxruntime==1.27.0 numpy PyYAML
```

## 2. 학습 (`TRAINING_SIM`)

기준: [flat_env_cfg.py](lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/flat_env_cfg.py), FlashSAC, 관측 35개 / action 8개.

```bash
cd "$TITA_REPO"
source ~/isaac/env_isaaclab/bin/activate
python lab/ddt_lab/scripts/flash_sac/train.py \
  --task DDT-Velocity-Flat-Tita-v0 \
  --num_envs 1024 --steps 100000 --device cuda:0 --headless
```

Checkpoint: `lab/ddt_lab/logs/flash_sac/tita_flash_sac_<run>/model_<step>/`.
추가 옵션: [FlashSAC README](lab/ddt_lab/scripts/flash_sac/README.md).

## 3. sim2sim 검증 (`VALIDATION_SIM`)

`<run>`과 checkpoint 번호를 실제 학습 결과로 바꾼다. 최초 실행 시 ONNX export와 parity 검증을 자동 수행한다.

```bash
cd "$TITA_REPO"
export TITA_CKPT="$TITA_REPO/lab/ddt_lab/logs/flash_sac/tita_flash_sac_<run>/model_65000"

# Headless 검증
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt "$TITA_CKPT" --headless --steps 1000

# Viewer (터미널에서 실행)
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py --ckpt "$TITA_CKPT"
```

키: `1` 기립 → `0` RL, `w/s` 전후, `a/d` 회전, `r` 정지, `6` idle, `Ctrl+C` 종료.
Export: `$TITA_CKPT/sim2sim/actor/`. 상세: [sim2sim README](sim2sim/README.md).

## 4. sim2real 실행 (`ROBOT_STATE_CHANGING`)

먼저 **데스크톱에서** sim2sim 검증을 마친 export를 TITA로 복사한다. `<TITA_IP>`를 로봇 주소로 바꾼다.

```bash
# 데스크톱 → TITA: 정책 파일 전송
export TITA_ROBOT="robot@<TITA_IP>"
ssh "$TITA_ROBOT" 'mkdir -p ~/tita_ws/policies/flat_candidate'
scp "$TITA_CKPT/sim2sim/actor/"{policy.onnx,config.json,manifest.json} \
  "$TITA_ROBOT:~/tita_ws/policies/flat_candidate/"
```

이후 **로봇의 `~/tita_ws`**에서 현재 controller 소스를 빌드한다.

```bash
cd ~/tita_ws
source /opt/ros/humble/setup.bash
exp_dir="$PWD/docs/exp/$(TZ=Asia/Seoul date +%F)"
mkdir -p "$exp_dir"
colcon --log-base "$exp_dir/colcon" build --packages-up-to tita_controller \
  --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3 && \
  source install/setup.bash
```

**방금 복사한 정책**은 `policy_dir`로 지정한다.

```bash
# 로봇에서 실행: 복사한 정책, 모터 출력 OFF
ros2 launch tita_controller tita.launch.py \
  policy_dir:="$HOME/tita_ws/policies/flat_candidate" output_enabled:=false
```

이후 구동 준비가 완료되면, 'output_enabled:=true' 로 다시 실행한다.

```bash
# 로봇에서 실행: 복사한 정책, 모터 출력 OFF
ros2 launch tita_controller tita.launch.py \
  policy_dir:="$HOME/tita_ws/policies/flat_candidate" output_enabled:=true
```


기존 정책 실행 명령어

```bash
# 모터 출력 ON
ros2 launch tita_controller flashsac.launch.py \
  policy:=flashsac_headw0_65000 output_enabled:=true
```

배포·조작 방법: [실기 README](sim2real/tita_ws/README.md).
학습·검증·실기 로그: 각 workspace의 `docs/exp/YYYY-MM-DD/`.
