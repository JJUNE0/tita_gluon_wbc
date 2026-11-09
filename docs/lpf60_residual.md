# Shared-sensor LPF60 torque residual

Execution domains: TRAINING_SIM for training; VALIDATION_SIM for MuJoCo;
DESKTOP_DRY_RUN for bundle validation/build. Hardware operation is separate.

This publication contains the frozen Teacher80k and selected residual10k,
walk/inline, sit/stand/height-only and single-leg environments, production
sim2sim and Sim2Real sources. It excludes BFM, datasets and experiment histories.
Residual250Hz / Teacher50Hz / physics and PD500Hz. Residual-only LPF60Hz precedes
fresh PD sum, final motor effort clipping and the transport delay. The saved
shared-sensor contract,44x10 Actor input, torque bounds, pose ranges and action
scales remain unchanged. This specific10k checkpoint was selected from a50k run;
quality remains conditional on measured scenarios, not guaranteed by publication.

## Install

Use Python3.12 and the separate mjlab environment described in
[the mjlab README](../mj_lab/README.md). Initialize `third_party/mjlab` recursively.
MuJoCo playback needs ROS2 Jazzy sourced in the executing shell. No Isaac runtime
is needed for the published native mjlab Actor; point the legacy-named
`--isaac-python` export option at the mjlab interpreter as shown below.

## Train a fresh residual through10k

From the repository root, with the mjlab environment installed:

```bash
~/venvs/tita_mjlab/bin/python -m mj_lab.scripts.train_residual_torque \
  --teacher sim2sim/checkpoints/mjlab/task/base_velocity/height_roll_pitch/20261108/80000 \
  --reference-config mj_lab/config/residual_lpf60_10k.json \
  --output docs/exp/$(date +%F)/residual_lpf60_fresh10k \
  --steps 10000 --num-envs 4096 --batch-size 8096 \
  --buffer-size 1000000 --min-buffer 100000 --seed 42 \
  --actor-sensor-mode teacher_shared --residual-hz 250 --residual-lpf-hz 60 \
  --torque-max-lag 4 --pose-command-mode height_roll_pitch \
  --pose-roll-deg 30 --pose-pitch-deg 15 \
  --checkpoint-interval 2000 --video-interval 10000 --wandb-mode online
```

The output must be a new directory. This initializes residual networks,
optimizers, replay and normalizer fresh; Teacher is frozen. Reference JSON holds
actual saved learner settings, including the original learning-rate schedule.
Saved replay/optimizer state of the residual is not distributed: the registry
is a playback bundle, not a residual-training resume checkpoint. Training curves,
evaluation evidence and videos are logged online and retained under `docs/exp/`.
GPU nondeterminism and hardware differences can affect numerical reproducibility.

## Play the selected10k with the same Teacher

```bash
source /opt/ros/jazzy/setup.bash
~/venvs/tita_mjlab/bin/python sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.residual.torque.launch.py \
  --config sim2sim/config/lpf60_10k.json --lpf 60 \
  --isaac-python ~/venvs/tita_mjlab/bin/python
```

For a finite local check add `--headless --steps 1000`. For export only add
`--prepare-only`. The matching interpreter is automatically selected for the
torque runtime; override `--mujoco-python` if your environment lives elsewhere.
Interactive keys:1 prepares,0 enters RL after preparation; w/s and a/d command
motion/yaw, r stops; j/l roll, i/k pitch, u/o height, p nominal pose,2 reset.
Residual is gated off during nonzero velocity commands. Pose limits and ramps
come from the checkpoint. The default config also selects this published pair.

Teacher only uses `sim2sim.launch.py --ckpt
sim2sim/checkpoints/mjlab/task/base_velocity/height_roll_pitch/20261108/80000`
with the same explicit export interpreter. A causal ON/OFF benchmark should use
the torque runtime with residual disabled so physics/PD clocks remain matched.

## Sim2Real sources and artifacts

The matching pair is also available under `sim2real/checkpoints/`, referenced by
`sim2real/config/policies.json`. Duplicate binary contents share Git objects.
This keeps the existing standalone ROS workspace installation flow intact.

The required prebuilt amd64/arm64 TITA SDK libraries are included unchanged with
their Apache-2.0 license/notice. ONNX Runtime is fetched by CMake.

Build only (does not start a controller or access a robot):

```bash
source /opt/ros/jazzy/setup.bash
colcon --log-base docs/exp/$(date +%F)/sim2real_build_logs build \
  --base-paths sim2real/tita_ws/src \
  --build-base sim2real/tita_ws/build --install-base sim2real/tita_ws/install
```

The public launcher is `sim2real.residual.torque.launch.py`, with its default
`output_enabled=false`; bundle validation is performed before runtime startup.
See [the workspace documentation](../sim2real/tita_ws/README.md). Even with output
false, the launch runner is not a desktop validation tool: it may manage robot
services. This publication does not launch it, connect to hardware or deploy it.

## Included models

- Teacher SHA256: `5487e3584fddbdfc87b7485bb2ad4c7da8069a7679b1975789d64419e7482334`.
- Residual SHA256: `d6672529ee247a92b7043f50bb6deb501a65becbf760761a412b33d5701b6002`.
- Training run: [jv68rep7](https://forge.coreweave.com/wandb/bjy6614-postech/tita_sac_residual_amp/runs/jv68rep7).

Only this pair is checked in. Root ONNX exports and manifests are retained
byte-for-byte for hardware contract validation; their old absolute source paths
are provenance. Native sim2sim regenerates its separate local cache on relocation.
Model hashes are checked rather than silently changing observation/action order.
