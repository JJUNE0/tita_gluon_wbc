# TITA + GLUON Whole-Body Control (WBC) Repository

This repository integrates Reinforcement Learning (RL), Sim-to-Sim validation, Hardware Low-Level SDKs, and ROS 2 Deployment for the **TITA wheel-legged robot** combined with the **INNFOS GLUON robotic arm**.

---

## 📁 Repository Structure

```text
tita_gluon_wbc/
├── lab/             # RL Training & Task Environments (Isaac Lab)
├── sdk/             # Hardware Low-Level SDKs & Driver Interfaces
├── sim2sim/         # MuJoCo Validation Simulator & Robot URDF/Mesh Assets
└── tita_gluon_ws/   # ROS 2 Hardware Deployment Workspace & Controllers
```

---

## 🛠 Directory Overview

### 1. `lab/` (RL Training & Environments)
- **`ddt_lab/`**: Isaac Lab based reinforcement learning training environments and task definitions for TITA and GLUON.

### 2. `sdk/` (Low-Level Hardware SDKs)
- **`tita_low_level_sdk/` & `tita_low_level_sdk_ros2_humble/`**: TITA lower-body wheel-legged motor control & CAN socket communication SDK.
- **`TITA-SDK-ROS2/`**: TITA official ROS 2 SDK wrapper.
- **`innfos-cpp-sdk/` & `innfos-gluon-controller/`**: INNFOS GLUON upper-body robotic arm C++ SDK & motor controller driver.

### 3. `sim2sim/` (Sim-to-Sim Validation & Assets)
- **`cosim/`**: MuJoCo physics-based sim-to-sim validation environment.
- **`tita_gluon_urdf/`**: Combined URDF, Mesh, and USD assets for TITA + GLUON.
- **`gluon_urdf/` & `gluon_2L6_4L3_urdf/`**: Standalone GLUON arm URDF files.

### 4. `tita_gluon_ws/` (ROS 2 Real Robot Deployment)
- **`src/`**: ROS 2 packages including `ddt_ros2_control` and `tita_stage1_controller` for Whole-Body Control (WBC).
- **`deploy/`**: Real robot deployment scripts (`deploy_tita_policy.bash`), environment setup, and policy runner.
- **`crsf-app/`**: Remote controller (RC / Joystick) reader interface application.

---

## 🚀 Quick Start & Build Guide

### ROS 2 Workspace Build (`tita_gluon_ws`)
```bash
cd tita_gluon_ws
colcon build --symlink-install
source install/setup.bash
```

### RL Environment Setup (`lab`)
```bash
# Activate Isaac Lab virtual environment
source ~/isaac/env_isaaclab/bin/activate

# Register new ddt_lab package location
cd lab/ddt_lab
pip install -e .
```

