# TITA sim2sim cleanup and checkpoint adapter

Execution Domain: DESKTOP_DRY_RUN. Native playback checks: VALIDATION_SIM.
Resolved-interface capture check: TRAINING_SIM. Real2sim tests used synthetic
messages on localhost domain 87; no physical robot was connected or commanded.

Evidence Status: PASS for the functional checks listed below. GUI playback was
operator-stopped and is recorded as SUSPICIOUS; startup, keyboard dispatch and
clean viewer shutdown were observed. Locomotion quality was not evaluated here.

Branch: `agent/codex/dev_tita_gluon`. No commit, push, PR or deployment.

Policy Checkpoint SHA256:

| Policy | SHA256 |
| --- | --- |
| FlashSAC expanded-range model_15000/actor.pt | f330e86adeb4b5be2ed276fae01063df63e15bc625d8ad0125746263c42e73a2 |
| PPO comparison model_1999.pt | 4ce6a6471b70e2fec58cbf5d85f1403d94c172dec372625e3fdbae0cc51b3ca7 |
| Estimator PPO 2026-07-24_19-16-43/model_1800.pt | 30b0c28a0d8af084f5455527fc5fb990ff9737e3408962b362dc90cc1e8721ba |
| Four-environment capture smoke model_8/actor.pt | 983a7e993b5d47068ea9581e71b80c5c39a89d738d5f78a5a8b3f7db479748de |

## Changed files and behavior

- Added `sim2sim/sim2sim_ros2_jazzy/`: `launch/{sim2sim,real2sim}.launch.py`,
  `config/tita.yaml`, package/setup/resource files and Python modules
  `checkpoint.py`, `adapter.py`, `mujoco_env.py`, `sim2sim_node.py`,
  `keyboard.py`, `real2sim_node.py`, `cli.py`, `__init__.py`.
- Removed backed-up `sim2sim/cosim/`, `sim2sim/cosim_ros2_jazzy/`, old
  `build/install/log`, `play_flash_sac.py`, `tita_gluon_mujoco_sim2sim.py`.
  Active replay supports current TITA PPO/FlashSAC only; GLUON/MOO,
  relay/ghost launches, old diagnostics and per-checkpoint YAMLs were removed.
- Updated `lab/ddt_lab/scripts/flash_sac/{train.py,export.py,README.md}`,
  `lab/ddt_lab/scripts/rsl_rl/train.py` and `sim2sim/README.md`.
  Added `lab/ddt_lab/ddt_lab/policy_interface.py` to save resolved manager
  joint order and observation scales. The PPO hook is limited to My flat TITA.
- Updated `test/test_flash_sac_{export,entrypoints}.py`; added
  `test/test_sim2sim_{checkpoint_adapter,ppo_parity,real2sim_readonly}.py`.
  Removed backed-up obsolete legacy launcher/RMA viewer and test helpers.
- Added this report, backup manifests, task-relative diff and verification logs.

The common loader finds saved `env.yaml`, `agent.json`/`agent.yaml`, optional
resolved `policy_interface.json`, and FlashSAC `ddt.json`. It parses Isaac YAML
tags as data without constructing Python objects. Observation term order,
clip-before-scale, joint selection, action term order, scale, default offset,
processed target clipping, PD gains and torque limits come from saved config.
PPO empirical normalization and the learned velocity estimator are preserved.
FlashSAC signed gains are embedded once in deterministic ONNX output.
Last-action observations retain native policy action order.

The direct launch accepts `--ckpt`; ROS launch uses `ckpt:=`.
No manual export or checkpoint-specific YAML selection is needed.
Verified exports cache beneath each checkpoint and are invalidated by source,
checkpoint/config, generated config and ONNX hashes. Simulation uses localhost
ROS domain 87 and in-process keyboard callbacks. Real2sim has only state
subscriptions and diagnostic publishers, updates MuJoCo via `mj_forward`,
and never publishes robot controls or advances policy physics.

## Observed metrics / behavior / log summary

| Check actually executed | Evidence |
| --- | --- |
| FlashSAC CPU regression suite | PASS, 41 tests; `sim2sim_cleanup_flash_tests.log` |
| Metadata/adapter/cache and native PPO parity | PASS, 13 tests; `sim2sim_cleanup_policy_tests.log` |
| Synthetic real2sim ROS/MuJoCo state mapping | PASS, 2 tests; `sim2sim_cleanup_readonly_tests.log` |
| Native PPO vs portable PPO on 512 observations, both plain/estimator | PASS, maximum difference 0.0 |
| PyTorch vs ONNX Runtime on 256 observations for Flash/PPO/estimator | PASS, max absolute differences 5.0962e-6 / 3.8147e-6 / 7.6294e-6 |
| All three policies in new MuJoCo/ROS runtime | PASS, 100 control steps each, finite state/actions, exit 0; `sim2sim_cleanup_*_runtime.log` |
| New ROS package colcon build | PASS, one package; `sim2sim_cleanup_build.log` |
| Both installed launch descriptions, --show-args | PASS, only sim2sim and real2sim launch files |
| Installed ROS sim2sim launch, explicit actor.pt | PASS, 10 steps and child exit 0; `sim2sim_cleanup_roslaunch.log` |
| Installed real2sim launch, synthetic namespace, no viewer | PASS for startup and clean operator stop, child exit 0; `sim2sim_cleanup_real2sim_launch.log` |
| GUI/terminal run, 0/w keys and Ctrl-C | SUSPICIOUS operator stop; 1497 policy steps, process exit 0, viewer threads stopped; `sim2sim_cleanup_gui.log` |
| Actual Isaac environment interface capture | PASS, 4 environments / 8 training steps; `sim2sim_cleanup_training_capture.log` |
| New captured-interface checkpoint export | PASS, 256 samples, max error 5.2452e-6; `sim2sim_cleanup_resolved_prepare.log` |
| Pre-task source integrity comparison | PASS, no unexpected source modifications; preserved unrelated lab, hardware, URDF and LQR sources |

Isaac capture confirms articulation order L1,R1,L2,R2,L3,R3,L4,R4 and action
term order L1,L2,L3,L4,R1,R2,R3,R4. Its observation output matches the legacy
TITA convention exactly in float32. The 0.05 velocity scale is serialized as
0.05000000074505806 after manager tensor conversion; this changes no output.
The temporary eight-step run was moved under `sim2sim_cleanup_capture_run/`
so it cannot displace the full training run in newest-checkpoint selection.

Required completion gate: `./scripts/agent-check.sh`, with results recorded in
`sim2sim_cleanup_agent_check.log`. The final task-relative diff was inspected
against backup contents, rather than treating unrelated dirty HEAD changes as
part of this task: `sim2sim_cleanup_task_relative.diff`.

## Backup and remaining limits

Before removing legacy code, exact contents including local edits were saved
to `sim2sim_cleanup_before.tar.gz`: 1153 members, 107800835 bytes,
SHA256 `e91d95632c90ddd9cc3e7094fc8155351ea335a71737136764d448b5cbea5c61`.
Training hook and fake-test fixture originals are in two additional archives.
No unrelated source changes were reverted or staged.

Weights alone cannot describe observation/action semantics: keep the run's
saved sidecars. Existing current-TITA checkpoints use the articulation
convention verified by the native capture; new training saves resolved names.
Unsupported observation functions, history/modifiers and non-TITA joints fail
with a clear adapter error. The retained MuJoCo PD/model does not reproduce
training actuator latency or persistent sensor/encoder bias randomization.
These finite checks validate execution and mapping, not long-horizon quality
or sim-to-real readiness. Actual robot state mirroring remains NOT_TESTED.

The existing `~/venvs/cosim_ros2_jazzy` virtual environment name is retained;
the source package has been renamed. Historical experiment documents retain
old paths as historical evidence; removed source is recoverable from backup.

## Current command

From repository root (`VALIDATION_SIM`):

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt lab/ddt_lab/logs/flash_sac/tita_flash_sac_172127_928297/model_15000/actor.pt
```

Replace `--ckpt` with a PPO `model_N.pt` or another FlashSAC `actor.pt`.
