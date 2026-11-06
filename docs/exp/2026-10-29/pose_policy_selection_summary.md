# Frozen policy selection — stationary, velocity and pose

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `SUSPICIOUS` for overall capability; evaluation execution `PASS`.
- Selected checkpoint SHA256: `5cc4c3d1f7899230276a81aabaa9cd5b1e529572ad431d459c28d277f9fd6b8b`
- Selected ONNX SHA256: `1b21c8654ba249eaeba0ed3799c31e2c58674d33a558804d436c3dcc6110c92a`

## Finding

`tita_mjlab_114540_063797/model_20000` is the best tested nominal stationary/driving/stopping policy.
No tested checkpoint satisfies stationary, velocity, pose and complete crouch/rise requirements together.
The latest 100k checkpoint is not the best checkpoint. No training or deployment was started.

## Protocol

Screened all 20 latest checkpoints and all 20 original pose checkpoints at zero command for 20 s.
Then evaluated 24 checkpoints with the full supported command suite. Each independent case resets through the production IDLE/transform/RL state machine and warms up for 6 s.
Identical corrected flat MuJoCo model, sphere wheel contacts, friction 0.8 and 50 Hz control; each saved observation/action mapping, PD settings and command ramp is preserved. No residual controller, filter override, velocity bias or latch override was added.
Nominal pose: roll/pitch 0, height 0.335 m. Driving: vx +/-0.5 m/s, yaw +/-0.5 rad/s and combined vx/yaw 0.3. Stops last 12 s. Pose goals: heights 0.30/0.40, roll +/-10 deg, pitch +/-5 deg and a combined goal; full-crouch policies additionally test 0.25/0.50/0.10/0.07 m and two crouch/rise cycles.
Stationary/pose pass: last-3-s mean XY speed <0.01/0.02 m/s, |yaw rate| <0.05 rad/s, roll/pitch MAE <3 deg, height MAE <3 cm, no fall. Driving pass: vx/yaw MAE <0.10, lateral MAE <0.08, height MAE <5 cm, roll/pitch MAE <7 deg. Stopping additionally requires <=4 s to a continuous 0.5-s quiet interval. Rollback is checked separately: <10 cm. These are explicit screening thresholds, not hardware acceptance criteria.
A command outside a saved checkpoint range is unsupported, never silently clamped or counted as a pass. Original pose policies only support heights 0.27–0.42 m. Total pass counts across different command contracts are not directly comparable.

## Main candidates

Family mapping: `new` = `tita_mjlab_163655_667608`; `old_pose` = `tita_mjlab_202755_365015`; `old_stop` = `tita_mjlab_114540_063797`.

| Checkpoint family / step | Stationary | Velocity | Stop | Pose | Crouch/rise | Worst rollback |
|---|---:|---:|---:|---:|---:|---:|
| old_stop_20000 | 1/1 | 5/5 | 3/3 | 2/11 | 0/1 | 3.7 cm |
| old_pose_25000 | 1/1 | 5/5 | 2/3 | 5/7 | unsupported | 30.1 cm |
| old_pose_95000 | 1/1 | 5/5 | 2/3 | 5/7 | unsupported | 29.6 cm |
| new_100000 | 0/1 | 4/5 | 0/3 | 0/11 | 0/1 | 42.4 cm |

## Selected checkpoint measurements

| Command vx / yaw | Actual vx / yaw (last 3 s) |
|---|---|
| +0.50 / +0.00 | +0.483 / -0.056 |
| -0.50 / +0.00 | -0.453 / -0.006 |
| +0.00 / +0.50 | +0.034 / +0.479 |
| +0.00 / -0.50 | +0.017 / -0.548 |
| +0.30 / +0.30 | +0.322 / +0.250 |

Stop settle times (forward/backward/yaw): 2.78 s, 1.96 s, 0.18 s.

60-s nominal and post-drive holds all pass. Maximum XY offset after t=5 s:

- zero_nominal: 0.167 mm; final mean speed 0.000003 m/s; rollback 0.00 cm.
- forward_stop: 0.446 mm; final mean speed 0.000003 m/s; rollback 0.38 cm.
- backward_stop: 0.202 mm; final mean speed 0.000003 m/s; rollback 3.66 cm.

Extended velocity suite: 10/11 pass. +/-1.5 m/s straight and +/-1 rad/s yaw pass; +3 rad/s yaw fails height accuracy (actual height error 5.7 cm). Prefer |yaw| <=1 rad/s until stronger validation.

Pose limitations: selected 20k policy produces about 0.351 m for 0.30 m requested and 0.368 m for 0.40 m requested. Roll +10 deg has about 5 deg error. For 0.07 m requested, actual height remains about 0.286 m. It is unsuitable for accurate full pose control or full sitting.
Original pose 25k/95k track moderate roll/pitch better (5/7 pose cases pass), but still undershoot 0.40 m height and return about 30 cm after backward stopping. Original pose 95k also drifts 1.71 m during the 55-s settled interval after forward stopping.

## Randomized native cross-check

A separate original-mjlab 32-environment, 8-s screen preserves saved reset/physics DR and fixes zero velocity/nominal pose. Selected 20k mean final-3-s speed is 0.073 m/s, vs 0.058 m/s for original pose 25k. The existing loose upright screen (speed <0.1 m/s, height >0.25 m, tilt <30 deg) gives 25/32 and 32/32. Neither passes the stricter mean-speed <0.01 m/s, height error <3 cm, tilt <7 deg snapshot in any environment.
This short native screen does not log episode-reset history and ends before scheduled pushes; it is not a robustness/survival acceptance test. Good deterministic sim2sim holding does not establish reliable randomized training or hardware performance.

## Replay

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt mj_lab/logs/flash_sac/tita_mjlab_114540_063797/model_20000 \
  --pose 0 0 0.335
```

## Artifacts

- [Command comparison](pose_policy_selection/command_comparison.png)
- [60-second holds](pose_policy_selection/long_hold_comparison.png)
- [Continuous sim2sim video](pose_policy_selection/selected_policy.mp4)
- [Aggregate metrics and all checkpoint hashes](pose_policy_selection/selection_summary.json)
- Per-case traces and execution/export logs: `pose_policy_selection/`.

## Changes and validation

Only evaluation/report tooling and experiment evidence were changed; production training, policies and sim2sim control code were not edited.
Added `test/evaluate_pose_policy_commands.py`, `test/render_selected_pose_policy.py`, `test/report_pose_policy_selection.py`. Updated `test/diagnose_settled_stop_drift.py` and `test/sweep_sit_stand_checkpoints.py` to accept older saved latch/curriculum configurations without changing their defaults.
Executed: 40 zero-command checkpoint screens; 24 full command suites; 9 long-hold trials across 3 checkpoints; 11 extended velocity cases; two 32-environment native screens; a continuous 39-s production-loop video (975 frames, no fall). These completed with finite outputs (`PASS` execution); capability failures are retained as `SUSPICIOUS` and shown above.
`python3 -m py_compile` for all five evaluation/report files: `PASS`. `./scripts/agent-check.sh`: `PASS` (direct log: [policy_selection_agent_check.log](policy_selection_agent_check.log)).
Incremental diffs of both pre-existing helpers were inspected. The hash audit found no changed production source; two concurrently modified FB test files were observed and preserved. See [change audit](policy_selection_change_audit.json) and `policy_selection_diff_*.txt`.
Branch: `agent/codex/tita-walk`. No commits, publication or hardware commands.

## All full-suite checkpoints

| Label | Stand | Velocity | Stop | Pose | Rollback |
|---|---:|---:|---:|---:|---:|
| new_10000 | 0/1 | 2/5 | 0/3 | 1/9 | 1.0 cm |
| new_100000 | 0/1 | 4/5 | 0/3 | 0/11 | 42.4 cm |
| new_15000 | 0/1 | 3/5 | 2/3 | 0/9 | 2.1 cm |
| new_20000 | 0/1 | 5/5 | 0/3 | 0/11 | 14.0 cm |
| new_5000 | 0/1 | 0/5 | 0/3 | 0/9 | 26.3 cm |
| old_pose_100000 | 0/1 | 5/5 | 1/3 | 1/7 | 38.5 cm |
| old_pose_15000 | 0/1 | 3/5 | 2/3 | 1/7 | 31.7 cm |
| old_pose_20000 | 1/1 | 5/5 | 2/3 | 2/7 | 39.2 cm |
| old_pose_25000 | 1/1 | 5/5 | 2/3 | 5/7 | 30.1 cm |
| old_pose_30000 | 0/1 | 5/5 | 1/3 | 1/7 | 40.6 cm |
| old_pose_40000 | 1/1 | 1/5 | 1/3 | 5/7 | 34.5 cm |
| old_pose_45000 | 0/1 | 5/5 | 3/3 | 1/7 | 19.3 cm |
| old_pose_50000 | 0/1 | 3/5 | 1/3 | 0/7 | 27.6 cm |
| old_pose_55000 | 0/1 | 3/5 | 0/3 | 2/7 | 34.0 cm |
| old_pose_60000 | 1/1 | 5/5 | 3/3 | 3/7 | 15.7 cm |
| old_pose_65000 | 0/1 | 4/5 | 2/3 | 0/7 | 23.2 cm |
| old_pose_70000 | 1/1 | 5/5 | 3/3 | 3/7 | 31.4 cm |
| old_pose_75000 | 0/1 | 5/5 | 1/3 | 0/7 | 29.1 cm |
| old_pose_80000 | 0/1 | 5/5 | 2/3 | 0/7 | 32.5 cm |
| old_pose_85000 | 1/1 | 4/5 | 2/3 | 3/7 | 26.6 cm |
| old_pose_90000 | 0/1 | 5/5 | 2/3 | 4/7 | 31.3 cm |
| old_pose_95000 | 1/1 | 5/5 | 2/3 | 5/7 | 29.6 cm |
| old_stop_20000 | 1/1 | 5/5 | 3/3 | 2/11 | 3.7 cm |
| old_stop_70000 | 0/1 | 1/5 | 0/3 | 1/11 | 18.4 cm |
