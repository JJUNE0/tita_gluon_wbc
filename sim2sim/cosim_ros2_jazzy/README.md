# DDT TITA MuJoCo Sim-to-Sim (ROS 2 Jazzy)

Native ROS 2 Jazzy and MuJoCo environment for validating the deployment interface of an RL policy for the DDT TITA wheel-legged robot.

The goal is interface validation before any real-robot work:

- verify the 33-element observation and 10-step observation history;
- verify the eight-action joint mapping, default pose, scaling, and wheel signs;
- check zero-command stability and a small forward-velocity command;
- inspect MuJoCo state, policy outputs, and ROS 2 debug topics.

This package deliberately does **not** start, control, or modify real-robot hardware.

## Scope

The main entry point is `tita_mujoco_sim2sim.launch.py`. It loads a MuJoCo scene, runs the exported ONNX policy, and exposes a ROS 2 command/debug interface.

| Component | Purpose |
| --- | --- |
| `mujoco_policy_node.py` | MuJoCo loop, FSM, policy inference, ROS 2 I/O |
| `obs_builder.py` | 33-D proprioceptive observation and 10-step history |
| `action_adapter.py` | Eight policy actions to leg position / wheel velocity targets |
| `config/tita.yaml` | Model, policy, control, topic, and safety configuration |
| `launch/tita_mujoco_sim2sim.launch.py` | Sim-to-sim launch entry point |
| `scripts/` | Model inspection, conversion, trace, and physics comparison utilities |

The package also contains read-only relay and real-to-sim mirror utilities. They are intentionally outside the quick-start path below; they must never be used as a robot command path.

## Requirements

- Ubuntu 24.04
- ROS 2 Jazzy
- Python 3 virtual environment with `mujoco`, `onnxruntime`, `numpy`, and `PyYAML`
- `colcon` and ROS 2 Python dependencies declared in `package.xml`
- TITA MJCF scene and exported policy ONNX file

The default `config/tita.yaml` uses absolute paths expected in the full DDT_Lab checkout:

```text
../ddt_ros2_control/urdfs/tita_description/mujoco_corrected/scene.xml
../deploy/tita/policy.onnx
```

For a standalone clone, provide the equivalent files and update `model.scene_xml` and `policy.path` in a copied YAML configuration. Do not commit proprietary or large policy/model artifacts unless their distribution is explicitly permitted.

## First-time setup and build

This is an `ament_python` ROS 2 package, not a standalone Python-only application. `colcon build` installs its ROS 2 console entry points and launch/config/model resources, allowing `ros2 run` and `ros2 launch` to locate the package. Build once after cloning, then build again after changing Python, launch, configuration, or packaged model files.

### Full DDT_Lab workspace (recommended)

Clone this repository into the existing DDT_Lab workspace so the default scene and ONNX-policy paths are available:

```bash
cd /path/to/DDT_Lab
git clone git@github.com:JJUNE0/cosim_ros2_jazzy.git cosim_ros2_jazzy
```

Activate the Python environment, build the package, and source the generated ROS 2 environment:

```bash
cd /path/to/DDT_Lab
source ~/venvs/cosim_ros2_jazzy/bin/activate
source /opt/ros/jazzy/setup.bash

python3 -m pip install mujoco onnxruntime numpy PyYAML

colcon build --symlink-install \
  --paths cosim_ros2_jazzy \
  --packages-select cosim_ros2_jazzy

source install/setup.bash
```

For later terminals, source the same three environments before running ROS 2 commands:

```bash
cd /path/to/DDT_Lab
source ~/venvs/cosim_ros2_jazzy/bin/activate
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

### Standalone clone

You may clone the repository into any colcon workspace, but it does not include the TITA MJCF or policy ONNX file. Supply those assets yourself and change `model.scene_xml` and `policy.path` in a copied `config/tita.yaml` before launching.

## Quick start: MuJoCo sim-to-sim

Start the simulator with the passive viewer:

```bash
ros2 launch cosim_ros2_jazzy tita_mujoco_sim2sim.launch.py \
  viewer:=true tita_ns:=tita
```

For headless execution:

```bash
ros2 launch cosim_ros2_jazzy tita_mujoco_sim2sim.launch.py \
  viewer:=false tita_ns:=tita
```

The command sequence below is the recommended low-risk validation path. Start in `transform_up`, enable `balance` (mapped to `rl_0`), confirm zero-command behavior, then test a small `0.05 m/s` forward command.

```bash
ros2 topic pub --once /tita/command/manager/cmd_key \
  std_msgs/msg/String "{data: transform_up}"

ros2 topic pub --once /tita/command/manager/cmd_key \
  std_msgs/msg/String "{data: balance}"

ros2 topic pub -r 10 /tita/command/manager/cmd_twist \
  geometry_msgs/msg/Twist \
  "{linear: {x: 0.00, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

ros2 topic pub -r 10 /tita/command/manager/cmd_twist \
  geometry_msgs/msg/Twist \
  "{linear: {x: 0.05, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

Stop the repeating `cmd_twist` publisher with `Ctrl-C`. Return to idle with:

```bash
ros2 topic pub --once /tita/command/manager/cmd_key \
  std_msgs/msg/String "{data: idle}"
```

### Optional keyboard and PlotJuggler

In a second terminal, after sourcing the workspace:

```bash
ros2 run cosim_ros2_jazzy keyboard_command_node
```

Keyboard mapping: `1` = `reference_transform_up`, `0` = `rl_0`, `6` = `idle`, `w`/`s` = forward velocity, `a`/`d` = yaw, `r` = reset velocity.

To publish scalar plot topics and open PlotJuggler (when installed):

```bash
sudo apt install ros-jazzy-plotjuggler-ros
ros2 launch cosim_ros2_jazzy tita_mujoco_sim2sim.launch.py \
  viewer:=true plot:=true tita_ns:=tita
```

## ROS 2 interface

Primary command topics:

```text
/tita/command/manager/cmd_key      std_msgs/msg/String
/tita/command/manager/cmd_twist    geometry_msgs/msg/Twist
/tita/command/manager/cmd_pose     geometry_msgs/msg/PoseStamped
```

Legacy aliases `/command/cmd_key` and `/command/cmd_twist` remain available for compatibility, but new tools should use the namespaced topics above.

Useful outputs:

```text
/joint_states
/imu
/cosim_ros2_jazzy/debug/obs
/cosim_ros2_jazzy/debug/action_raw
/cosim_ros2_jazzy/debug/action_scaled
/cosim_ros2_jazzy/debug/projected_gravity
/cosim_ros2_jazzy/debug/base_ang_vel
/cosim_ros2_jazzy/plot/*
```

Example checks:

```bash
ros2 topic echo /cosim_ros2_jazzy/debug/action_raw
ros2 topic echo /cosim_ros2_jazzy/debug/projected_gravity
ros2 topic list | rg '^/cosim_ros2_jazzy/(debug|plot)'
```

## Configuration and safety

`config/tita.yaml` is the source of truth for the ONNX interface, joint order, action scale, default pose, limits, and control timing. The active policy interface is:

```text
current observation: [1, 33]
history:             [1, 10, 33]
action:              [1, 8]
```

Do not raise action scale, torque limits, velocity limits, command range, or control frequency without an explicit, documented validation plan. This package is not considered validated until observation/action conventions, zero-command stability, and low-speed forward motion have been checked against Isaac Lab.

## Model and policy inspection

Run these from the package directory after activating the Python environment:

```bash
python3 scripts/inspect_onnx.py /path/to/policy.onnx
python3 scripts/inspect_mujoco_model.py /path/to/scene.xml
```

To generate an MJCF copy from a URDF, write the result under `models/generated/`; do not edit the source URDF in place:

```bash
python3 scripts/convert_urdf_to_mjcf.py \
  --urdf /path/to/robot.urdf \
  --out models/generated/tita_converted.xml
```

## GitHub upload (this package only)

This package is maintained as its own Git repository. Run the following from this directory to stage only package files:

```bash
cd /path/to/cosim_ros2_jazzy
git status --short
git add .
git status --short
git diff --cached --stat
git commit -m "Add ROS 2 Jazzy MuJoCo sim-to-sim package"
git push -u origin main
```

Review `git status --short` and `git diff --cached` before committing. The included `.gitignore` excludes local build products, Python caches, rosbag recordings, and generated MJCF output.

To use SSH rather than HTTPS authentication, configure the remote once:

```bash
git remote set-url origin git@github.com:JJUNE0/cosim_ros2_jazzy.git
ssh -T git@github.com
git push -u origin main
```

## License

This package declares the Apache-2.0 license in `package.xml`. Add a repository-level `LICENSE` file before public distribution if one is not already present.
