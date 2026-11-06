# mjlab hybrid walk checkpoint support in sim2sim

Execution Domains: VALIDATION_SIM, DESKTOP_DRY_RUN; TRAINING_SIM preservation check.

Evidence Status: PASS for hybrid export, command/gait/action parity, finite
playback and state-machine regression. Extended walking quality and the actual
GUI window are NOT_TESTED. Broad optional test discovery has the fixture and
environment failures documented below.

Policy Checkpoint SHA256:
`ca003031014536df172a93e161bcb9a795afdf1cc2da29c3cd30a5d5ddc02ad2`

ONNX SHA256:
`dbbfac689a585bc6feb6b4e0da7d0282df49a292272836ad697c1982d343a06f`

Checkpoint: `mj_lab/logs/flash_sac/tita_mjlab_085110_097268/model_25000`.
Branch: `agent/codex/tita-walk`. No commit, publication or robot operations.

## Behavior and changed files

The launcher previously rejected the saved custom wheel action class. It now
restores `GaitGatedWheelVelocityAction` with its explicit saved metadata on
both wheel joints. Disabled gait permits the scaled/clipped wheel policy
targets; enabled gait sets the processed wheel velocity targets to zero.
The current actor observation's mode remains fixed across all four physics
substeps. Raw action history and nominal saved wheel PD remain intact.

The saved command deadband, settling time, ramp and gait parameters determine
switching. mjlab uses integer episode steps for its clock, including the first
command ramp sample at the settling boundary. Isaac's existing accumulated
clock and legacy fixed-wheel walk behavior are preserved. Unknown metadata,
partial gates, gated leg joints and gates without gait observations fail
explicitly. Viewer text includes the wheel-policy ON/OFF state.

Production and documentation files:

- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/checkpoint.py`:
  recognize/validate saved hybrid actions and export their gate/clock metadata.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/adapter.py`:
  native-order target gate after affine scaling/clipping; episode-step clock.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/sim2sim_node.py`:
  pass the actor's mode to physics, restore mjlab command timing, viewer status.
- `sim2sim/README.md` and `mj_lab/README.md`: hybrid playback behavior.

Validation files:

- `test/test_sim2sim_hybrid.py`: explicit metadata and reordered target/PD tests.
- `test/test_mjlab_tita.py`: accept the real hybrid playback contract and compare
  the actual sim2sim post-physics update against native mjlab managers.
- `test/check_sim2sim_walk_state_machine.py`: hybrid mode transitions and
  verification that each physics substep uses the actor's observed gate.

Pre-existing dirty edits and staged renames were preserved. Incremental source
diffs were reviewed against `hybrid_sim2sim_before_*.txt`; the starting status is
`hybrid_sim2sim_preexisting_status.txt`. Generated exports for the target and
three legacy policies were refreshed; original actor weights were not changed.

## Observed Metrics / Behavior / Log Summary

- PASS: model_25000 ONNX export parity, 256 samples, maximum absolute error
  `4.231929779052734e-06`; `hybrid_sim2sim_25000_zero.log`.
- PASS: actual launcher, zero command 300 steps and forward command
  `[0.3, 0, 0]` 500 steps; finite physics and clean shutdown.
  Forward final base position `[2.20276, -0.08952, 0.43146]` m.
  Logs: `hybrid_sim2sim_25000_zero.log`, `hybrid_sim2sim_25000_moving.log`.
- PASS: native mjlab suite, 21 passed / 6 task-specific skips. This includes
  400 ticks of stop/start/stop/lateral/stop comparison of native command, full
  five-value gait and all eight processed targets with the production adapter
  and actual sim2sim update block. `hybrid_sim2sim_native_checks.log`.
- PASS: focused hybrid adapter tests, 2 passed;
  `hybrid_sim2sim_focused_unit_checks.log`.
- PASS: legacy walk suite under MuJoCo Python, 8 passed / 1 Torch-only skip;
  under Isaac Python, 8 passed / 1 MuJoCo-only skip, including actual Isaac
  training-clock parity. `hybrid_sim2sim_legacy_walk_checks.log`,
  `hybrid_sim2sim_isaac_parity.log`.
- PASS: 8 actual ROS/MuJoCo/ONNX runs, 159 recorded checks, hybrid walk plus
  mjlab fixed-wheel walk, Isaac walk and mjlab flat, each with manual key
  callbacks and headless startup. Only passive GUI creation was suppressed in
  manual-key cases. Stop/start gates, per-substep flags, fresh RL entry, idle
  and reset passed. `hybrid_sim2sim_runtime.json`, `.log`, `.md`.
- PASS: `./scripts/agent-check.sh`: syntax 710 passed / 0 failed, 8 URDF parses,
  diff integrity and experiment directory checks;
  `hybrid_sim2sim_agent_check.log`.
- PASS: active training PID 994292 remained alive; SHA256 checks confirm native
  `mj_lab/robots/tita/mdp.py`, `walk_env_cfg.py` and `mj_lab/checkpoint.py` were
  unchanged. `hybrid_sim2sim_training_preserved.json`.
- FAIL / environment and fixture limitations: an initial broad
  `test_sim2sim_*.py` discovery ran 37 tests with 14 errors / 1 skip. Twelve
  errors use pre-existing checkpoint fixtures pointing at removed `lab/`
  paths; one requires Torch absent from the MuJoCo interpreter and one imported
  ROS before sourcing its setup. See `hybrid_sim2sim_unit_checks.log`. These
  unrelated fixtures were preserved; relevant suites were subsequently run in
  their proper interpreters, and the real ROS runtime checks source Jazzy.

Short finite playback and mode agreement establish execution correctness;
they do not establish robust gait quality, tracking over long episodes or
equivalence of randomized training physics and nominal sim2sim physics.

## Run

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt mj_lab/logs/flash_sac/tita_mjlab_085110_097268/model_25000
```

In the terminal, press `1`, wait for sit, then `0` for policy control.
Hold `w/s` for forward/back, `q/e` for lateral movement; `r` requests stop.
The hybrid checkpoint stops gait within its command deadband and restores
wheel policy control. `6` returns to idle; `2` resets the pose and policy state.
