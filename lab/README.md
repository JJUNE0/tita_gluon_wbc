# Reinforcement Learning & Training Environments (`lab/`)

This directory contains Isaac Lab based Reinforcement Learning (RL) training environments, tasks, and policy export tools for the **TITA wheel-legged robot** and **INNFOS GLUON arm**.

---

## 📁 Directory Structure

```text
lab/
└── ddt_lab/
    ├── ddt_lab/
    │   ├── tasks/          # Task definitions (locomotion & manipulation)
    │   ├── managers/       # Custom observation/action/reward managers
    │   ├── algorithms/     # Training algorithms (NP3O, PPO)
    │   └── assets/         # Robot configs and asset loaders
    ├── pyproject.toml
    └── setup.py
```

---

## ⚙️ Environment Setup & Package Registration

For complete Isaac Lab environment setup, please refer to the official [Isaac Lab Pip Installation Guide](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/isaaclab_pip_installation.html).

Activate the Isaac Lab Python virtual environment and register the `ddt_lab` package in editable mode (`pip install -e .`):

```bash
# 1. Activate Isaac Lab virtual environment (e.g. env_isaaclab)
source ~/isaac/env_isaaclab/bin/activate

# 2. Register new ddt_lab package location
cd lab/ddt_lab
pip install -e .

# 3. Verify editable location points to tita_gluon_wbc
pip show ddt_lab
```



---

## 🚀 Usage Guide

### 1. Policy Training (`TRAINING_SIM`)

To train a policy with Isaac Lab (e.g. NP3O algorithm):

```bash
cd lab/ddt_lab

python scripts/np3o/train.py \
  --task=DDT-Velocity-Flat-Tita-My-v0 \
  --num_envs 4096 \
  --headless
```

- **Tasks**:
  - `DDT-Velocity-Flat-Tita-v0` (Baseline locomotion)
  - `DDT-Velocity-Flat-Tita-My-v0` (Includes actuator delay + IMU/encoder bias for Sim2Real)
- **Checkpoints**: Saved to `logs/np3o/tita_flat/<run_date_time>/model_<iter>.pt`

---

## 📦 2. Policy Evaluation & ONNX Export

### Play Policy with Isaac Sim Viewer
```bash
python scripts/np3o/play.py \
  --task=DDT-Velocity-Flat-Tita-My-Play-v0 \
  --checkpoint /path/to/logs/np3o/tita_flat/<run_id>/model_3000.pt \
  --num_envs 50
```

### Export ONNX Policy without GUI
```bash
python scripts/np3o/play.py \
  --task=DDT-Velocity-Flat-Tita-My-Play-v0 \
  --checkpoint /path/to/model_3000.pt \
  --export_policy \
  --headless
```

- **Exported Output**: `<checkpoint_dir>/exported/policy.onnx` and `policy.pt`
- **ONNX Input/Output Specifications**:
  - `nn_input0`: Current Observation `[1, 33]`
  - `nn_input1`: Observation History `[1, 10, 33]`
  - `nn_output`: Action Targets `[1, 8]`
