# Sim-to-Sim Validation & Robot Assets (`sim2sim/`)

This directory contains MuJoCo-based physics validation environments, ROS 2 sim2sim integration nodes, and 3D URDF/Mesh assets for **TITA** and **GLUON**.

---

## 📁 Directory Structure

```text
sim2sim/
├── cosim/                 # MuJoCo ROS 2 Sim-to-Sim Validation Workspace
├── tita_gluon_urdf/       # Combined TITA + GLUON URDF & Mesh assets
├── gluon_urdf/            # Standalone GLUON arm URDF
└── gluon_2L6_4L3_urdf/    # GLUON 2L6_4L3 variant URDF
```

---

## ⚙️ Environment & Build Setup (`VALIDATION_SIM`)

### Prerequisites
- ROS 2 Jazzy or Humble
- MuJoCo (PyQt5 environment, e.g. `conda activate cosim`)
- PlotJuggler (Optional, for real-time plot analysis)

```bash
# Activate cosim Conda environment or ROS 2 environment
conda activate cosim
source /opt/ros/jazzy/setup.bash

# Build cosim ROS 2 packages
cd sim2sim/cosim
colcon build --symlink-install
source install/setup.bash
```

---

## 🚀 Usage Guide

### 1. ONNX Policy Inspection & Placement
Place your exported policy ONNX file into `tita_gluon_ws/deploy/tita/policy.onnx` or test directly:

```bash
# Verify ONNX tensor interface
python3 scripts/inspect_onnx.py ../../tita_gluon_ws/deploy/tita/policy.onnx
```
*Expected Interface*: `nn_input0 [1,33]`, `nn_input1 [1,10,33]`, `nn_output [1,8]`

---

### 2. Running MuJoCo Sim-to-Sim Simulator

#### Launch Simulator with MuJoCo Viewer
```bash
source install/setup.bash
ros2 launch cosim_ros2_jazzy tita_mujoco_sim2sim.launch.py viewer:=true tita_ns:=tita
```

#### Launch with PlotJuggler Visualization
```bash
ros2 launch cosim_ros2_jazzy tita_mujoco_sim2sim.launch.py \
  viewer:=true plot:=true tita_ns:=tita
```

#### Launch Headless (No GUI)
```bash
ros2 launch cosim_ros2_jazzy tita_mujoco_sim2sim.launch.py viewer:=false
```

---

### 3. FSM State Transition & Command Topics

#### FSM State Commands (`cmd_key`)
```bash
# Stand-up transition
ros2 topic pub --once /tita/command/manager/cmd_key std_msgs/msg/String "{data: transform_up}"

# Enable RL Balance Policy
ros2 topic pub --once /tita/command/manager/cmd_key std_msgs/msg/String "{data: balance}"

# Return to Idle
ros2 topic pub --once /tita/command/manager/cmd_key std_msgs/msg/String "{data: idle}"
```

#### Velocity Commands (`cmd_twist`)
```bash
# Zero-Command hold
ros2 topic pub -r 10 /tita/command/manager/cmd_twist geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

# Forward velocity (vx = 0.05 m/s)
ros2 topic pub -r 10 /tita/command/manager/cmd_twist geometry_msgs/msg/Twist \
  "{linear: {x: 0.05, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

---

### 4. Interactive Keyboard Teleoperation Node
```bash
source install/setup.bash
ros2 run cosim_ros2_jazzy keyboard_command_node
```
- **Key Bindings**:
  - `1`: `transform_up`
  - `0`: `balance` (RL Policy ON)
  - `6`: `idle`
  - `w` / `s`: Increase / Decrease forward velocity `vx`
  - `a` / `d`: Turn left / right `yaw_rate`
  - `r`: Reset velocity command
