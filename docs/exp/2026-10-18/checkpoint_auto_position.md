# Checkpoint-driven position observation and MA2 loading

Execution Domain: DESKTOP_DRY_RUN / VALIDATION_SIM

Evidence Status: SUSPICIOUS overall because required repository agent-check fails on pre-existing whitespace; focused export, adapter, runtime, desktop C++ build and task diff checks: PASS. Hardware: NOT_TESTED.

Policy Checkpoint SHA256 (PosKneeMA2 model_75000 actor.pt): `9c22f34e0e3b9d7840f29250c214452bb84cadde6037d277d90df55221e84150`

ONNX SHA256: `128734f230868b947c9eac59ef647b8394043c6603781a335fd4e3b4700a2001`

Branch: `agent/codex/dev_tita_gluon`

## Behavior and changed files

- `lab/ddt_lab/scripts/flash_sac/export.py`: initialize 33/34-input FlashSAC actors from metadata; validate the resolved TITA layout in the shared exporter.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/checkpoint.py`: resolve WheelPositionError parameters and MA2JointPositionAction from saved env.yaml; reject unknown types, invalid position parameters and partial leg MA2 layouts; derive the saved filter mode.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/adapter.py`: stateful encoder/IMU position error with wheel unwrap, reference latch and reset.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/sim2sim_node.py`, `cli.py` and `launch/sim2sim.launch.py`: default filter auto-selection and RL reference lifecycle; record the resolved mode.
- `sim2real/tita_ws/src/tita_controller/include/tita_controller/adapter.hpp`, `src/tita_node.cpp`, `launch/tita.launch.py`: matching C++ calculation, exported parameter transport and reset on transition/fault. Generic robot launch restores the saved filter automatically.
- `sim2sim/README.md`, `sim2real/tita_ws/README.md`: usage and deployment boundary.
- New tests: `test/test_checkpoint_auto_position.py`, `test/check_training_position_reference.py`, `test/check_checkpoint_auto_runtime.py`, `test/sim2real/checkpoint_position_parity.cpp`.
- Existing parity fixture updated for new position parameters/string metadata: `test/sim2real/parity.cpp`, `test/sim2real/test_sim2real_parity.py`.

The observation is `5 * clip(radius * mean(q_wheel + pitch + q_thigh + q_knee) - reference, +/-clip_m)` with scale read from the checkpoint (5 for this run). Inside inclusive command thresholds the reference is fixed; outside it follows the distance and outputs zero. Inference omits training noise and radius randomization. Wheel angles unwrap with atan2(sin(delta), cos(delta)). The first action after reset passes through; only the six legs are averaged, wheels and raw last_action remain untouched. Nominal PD is read from training config, including knees 92/2.3.

## Executed validation and direct log evidence

- PASS `export34.log`: real PosKneeMA2 model_75000, 34 -> 8 ONNX; 256 inputs; max absolute output error 3.4571e-6.
- PASS `export33.log`: isolated copy of A80k under test/, 33 -> 8; 256 inputs; max error 2.9802e-6. Original A80k checkpoint/export untouched.
- PASS `position_parity_final.log`: four focused tests; unknown/invalid metadata rejection, actual saved 33/34/PPO interfaces, formula/sign/pitch/threshold/clip/wrap/reset, generic launch auto and explicit overrides with Node mocked. 1000 sequence samples per actor: Python/C++ max observation error 1.1921e-7; combined observation/action/PD error 1.11e-5 (34) / 7.15e-6 (33).
- PASS `training_reference_final.log`: actual training WheelPositionError code on CPU with Isaac types stubbed; 3000 samples including wheel wraps, threshold boundaries, move/stop and resets; max scaled error 5.8293e-5, about 11.7 micrometres before scale, from Torch absolute-angle float32 rounding at hundreds of radians.
- PASS `sim34.log`: public checkpoint-only launcher, auto=ma2_legs, 1000 finite MuJoCo control steps; final base position approximately [0.0827, 0.0393, 0.3522] m. Execution check, not a locomotion-quality evaluation.
- PASS `runtime34.log`, `runtime33.log`: actual ROS/MuJoCo node, 1100 audited steps per policy, 990 RL inferences per run; raw history and applied filter checked every inference/substep; exit/reentry relatches position and reset clears history/filter.
- PASS `cpp_build_final.log`: complete desktop tita_node compile/link with generated messages; executable not run. Build artifacts live only in test/sim2real/checkpoint_auto_work/.
- PASS `filter_regression.log`: four existing MA2/notch/filter tests, including Python/C++ mapping, reset and teacher/PD checks.
- PASS `export_regression.log`: two existing signed-gain/compiled-prefix/legacy exporter tests.
- PASS `full_adapter_parity34.log`, `full_adapter_parity33.log`: existing full adapter/state-machine parity helper with both actual exported interfaces.
- PASS `legacy_adapter_compatible_fixture.log`: 11 unchanged legacy adapter tests using the archived PPO33 configuration with the expected wheel scale 5; actual FlashSAC A80k has separate export/runtime/parity coverage above.

Earlier attempts are retained: `legacy_adapter.log` fails because its hardcoded model_15000 fixture no longer exists; substituting A80k in `legacy_adapter_active_fixture.log` passes 10/11, with the remaining wheel-target assertion expecting scale 5 rather than A80k's saved 20. These are fixture mismatches, not edits to trained scales. An initial C++ fixture stream used scientific notation for integer fields (fixed in test); an initial launch mock attempted ROS logs outside writable roots (rerun with ROS_LOG_DIR here); initial CMake linkage lacked the installed tita_robot prefix (fixed build invocation); initial training comparison tolerance underestimated float32 precision after many rotations (analytic small-angle checks retain tight tolerance). No production workaround was added for these test setup issues.

## Usage and remaining limits

```bash
# VALIDATION_SIM: normal playback, 34 observations and MA2 automatically selected.
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt lab/ddt_lab/logs/flash_sac/tita_flash_sac_180212_290240/model_75000
# Export only: append --prepare-only.
```

Keep run env.yaml, agent.json and policy_interface.json with the model/ddt.json; weights alone fail clearly. Exported folder: `lab/ddt_lab/logs/flash_sac/tita_flash_sac_180212_290240/model_75000/sim2sim/actor`. Robot generic launch consumes its policy.onnx/config.json; raw Torch checkpoint interpretation happens on the desktop. New algorithm types still require implementation. Wheel travel must be below pi radians between observations (at 50 Hz, below about 157 rad/s); encoder discontinuities/missed observations outside that assumption remain a hardware validation risk. Finite playback is not a gait-quality claim. No robot connection, deployment, physical command, service stop, commit or publication was performed. Frozen robot bundles and pins were not changed.

## Change integrity

Pre-existing workspace changes were recorded in `checkpoint_auto_position/status_before.txt` and source snapshots in `checkpoint_auto_position/before/`. Final scoped diff and tracked-file integrity check are recorded alongside this report. Required `./scripts/agent-check.sh` executed: FAIL solely from six pre-existing trailing-whitespace lines in `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py` (431, 437, 443, 449, 455, 461). The task-start SHA256 and completion SHA256 for that file match. It was not edited. Fast checks PASS: 635 Python files compiled, zero syntax errors; 8 URDF files parsed. Experiment directory checks PASS. Task-scoped `git diff --no-index --check` PASS for all 13 edited existing files and four new test files, including previously untracked source paths. `completion_integrity.json` confirms no unrelated tracked-file changes; `task.diff` was reviewed against the task-start snapshots. No commit, push or PR.
