# Command-selected left, right and double support

Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN.

Evidence Status: PASS for the new command/reward path, native physics, finite learner updates, video, ONNX parity and actual sim2sim mode changes. One additional legacy export test is FAIL because its historical checkpoint fixture is absent; learned three-mode balance remains NOT_TESTED.

Policy Checkpoint SHA256: first full-run checkpoint pending at startup verification. Separate 40-step pipeline probe: `6fc80e153d04a048021d2b3a2cc4c0c18b96b7e1ef8233d191f6ca59f677f630`.

ONNX Hash, pipeline probe: `eebe2449d8b0c82017f0e5603e79135afbadfe0da6e20a72d4d5229fde65c00d`.

Branch: `agent/codex/tita-walk`.

## Behavior

New task `support_command` extends the working reference-balance settings:

| Command ID | Requested ground support | Requested lift |
| --- | --- | --- |
| 0 | Left wheel | Right wheel |
| 1 | Right wheel | Left wheel |
| 2 | Both wheels | Neither |

The velocity command stays zero on vx, vy and yaw. There is no gait command, phase clock or forced alternating sequence. At reset each environment samples uniformly among the three goals. A goal is held for a random 3–5 seconds, then either other goal is selected with equal probability, without resetting physics. Left-to-right changes can therefore occur directly; there is no mandatory intermediate mode 2.

The policy and critic both receive a three-element one-hot support command. Their dimensions are now **38/42**, with eight actions, compared with 35/39 in the fixed-side task. A new experiment is initialized from scratch; no old weights or learner state are reused.

Existing reward weights remain alive +2, contact/clearance +2, pose hint +0.5, support-leg tilt -1, stationary -0.5, action-rate -0.005, joint acceleration -2.5e-7, and termination -10. All are timestep-scaled at 0.02 s. Both wheel policy actions, PD, torque limits, nominal/zero-velocity reset, base/knee termination, and all existing domain randomization remain enabled.

The existing manager key `single_support` now evaluates the **commanded support target**. For IDs 0/1 it applies the previous partial-clearance and contact-mismatch formula to the selected side. The target remains 4 cm with saturated credit, not a hard maximum height. The pose hint and hip-to-wheel vertical preference are mirrored by support side, with the same magnitude ranges and weights as before. For ID 2 the raw contact score is +1 with both contacts, 0 with one contact, -1 with neither. Single-leg pose-hint and tilt rewards are zero in ID 2; no extra body-upright reward was introduced.

Per-mode `command_time_s` and `success_time_s` metrics distinguish time spent requesting each mode from time actually achieving it. Single support requires selected-wheel contact, no opposite contact, at least 1 cm opposite-wheel clearance, and no failure termination. Both support requires both contacts and no failure. `mode_match_fraction` and total commanded single-support success seconds are also logged. These are cumulative measures, not longest uninterrupted hold duration.

Older fixed-left checkpoints remain compatible: side parameters added to their reward kernels default to left and preserve their previous values. Shared flat/walk/inline and old alternating configurations were not changed.

## Playback and video

Native player and sim2sim accept `--support-mode 0`, `1`, or `2`. Sim2sim defaults to mode 2 from the saved contract and keeps the existing standing-entry reset. Keyboard startup remains `1`, wait for sit, then `0`; keys **7/8/9** select support goals **0/1/2**, without a reset. Existing simulated `cmd_key` messages `support_left`, `support_right`, and `support_both` perform the same selection. Velocity inputs remain separate and zero-range for this task.

Native single-environment previews show **2 -> 0 -> 2 -> 1**, 2.5 seconds each, with the active support label drawn on top of the existing vx/vy overlay. This is a demonstration command sequence, not the training sampler. Explicit `--support-mode` pins one goal. The ten-second probe video was encoded and all 500 frames decoded; it contains 125 mode-0, 125 mode-1 and 250 mode-2 frames.

Testing exposed that mjlab `get_observations()` returns a cached per-tick value after an external goal change. The native player now explicitly refreshes observations on such changes, so the next action sees the requested goal. The standard training loop already refreshes observations after command-manager updates. Initial failure evidence is retained in `support_command_tests_initial_failure.log`.

The shared FlashSAC exporter also needed 38 added to its supported input-dimension list; actor construction, weights, action scaling and learning algorithm were unchanged. The initial expected rejection is retained in `support_command_sim2sim_prepare_initial_failure.log`.

## Experiment transition and active run

User-authorized SIGINT stopped fixed-left run `tita_mjlab_155513_268911` at **40,166 steps / 80,132 updates**. Its last logged mean episode length was 19.5714 s. A logged completed episode at step 40100 had 19.60 s selected single support and a timeout; this is a sampled episode, not a full frozen-policy success-rate evaluation. That episode's peak swing clearance was approximately 0.53 m, so the existing saturated 4 cm reward did not impose a maximum lift height. No new height-limit penalty was added in this task.

Preserved checkpoint: `mj_lab/logs/flash_sac/tita_mjlab_155513_268911/model_40000`.

Preserved actor SHA256: `fe8ca785da4353b79ef0b5af37ca073495b2156fa72395d939c3171bef8d27dd`.

The generic trainer records FAIL/KeyboardInterrupt for the deliberate stop; its cause, checkpoint hash and verified process exit are recorded in `support_command_previous_stop.json`.

New run: **`tita_mjlab_163835_917365`**.

W&B: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/630hkkcw

PID `1403441`; tmux `mjlab_support_command_20261028_163832`.

Initialization is **FROM_SCRATCH** with `resume=null`, `warm_start=null`, and a new W&B run. Budget: 100,000 vector steps, 1024 environments, seed 42, CUDA 0, two updates per step after replay warmup. Checkpoints every 5,000 steps; W&B online and 500-frame videos every 10,000 steps.

Startup verification: **500 steps, 802 finite learner updates**, source hashes match launch provenance. This establishes startup only; learned right-side support and command transitions are unverified.

Provenance: `support_command_training_launch.json`; console: `support_command_training_console.log`; metrics: `tita_mjlab_163835_917365_metrics.jsonl`.

## Changed files

- Added `mj_lab/robots/tita/support_command_env_cfg.py`: command sampler, conditional rewards and per-mode metrics.
- `mj_lab/robots/tita/stand_one_leg_reference_env_cfg.py`: optional side selection, with old left defaults preserved.
- `mj_lab/scripts/train.py`, `mj_lab/checkpoint.py`, `mj_lab/scripts/play.py`: task registration, saved one-hot interface, fixed support selection and labeled video preview.
- `isaac_lab/ddt_lab/scripts/flash_sac/export.py`: accept the verified 38-input actor layout.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/{adapter,checkpoint,cli,sim2sim_node}.py`: saved-layout support command, validation, CLI forwarding and existing-key-channel switching.
- `mj_lab/README.md`, `sim2sim/README.md`: command semantics and playback instructions.
- Added `test/test_mjlab_support_command.py`; extended `test/check_sim2sim_walk_state_machine.py` with actual support-goal transition checks.
- Evidence and this report under `docs/exp/2026-10-28/`.

## Executed validation and limits

- PASS: scoped native/support/old-reference/alternating/inline/flat-walk/sim2sim regression suite: **64 passed, 8 conditional skips, 39 subtests passed**; `support_command_tests.log`.
- PASS: separate fresh 16-environment, 40-step FlashSAC probe, **74 finite updates** and checkpoint save; `support_command_learner_probe.log`.
- PASS: complete 500-frame native preview encode/decode with all three goals; `support_command_video_probe.json`, `support_command_video_decode.json`, `.mp4`.
- PASS: actual ONNX export with 38 inputs / 8 outputs and 256-sample maximum absolute parity error **5.72e-6**; `support_command_sim2sim_prepare.log`.
- PASS: actual ROS/MuJoCo/ONNX manual-callback and headless startup tests, all three one-hot goals, monotonic simulation time during switches, no resets; `support_command_sim2sim_runtime.json`. Tests use local ROS domain 90; passive GUI creation alone is suppressed in the manual case.
- PASS: full launcher with `--headless --steps 140 --support-mode 1`; `support_command_sim2sim_cli.log` confirms mode 1 reaches runtime. This checks CLI forwarding and finite physics, not balance quality.
- PASS: source provenance and preservation checks, `support_command_source_verification.json`.
- FAIL, pre-existing missing fixture: additional `test/test_flash_sac_export.py` run had **2 passed, 1 failed** because `isaac_lab/ddt_lab/logs/flash_sac/tita_flash_sac_172127_928297/model_15000/actor.pt` is absent. It fails at file validation before export. This unrelated test was not rewritten or hidden; see `support_command_export_tests.log` and `support_command_legacy_fixture_check.json`. The new checkpoint's actual export and runtime checks passed independently.
- Required repository check and final incremental diff are recorded in `support_command_agent_check.log` and `support_command_changes.diff`.

Unresolved risks: success on the trained fixed-left task does not establish symmetry, landing, stable command transfer or all-mode robustness in the new policy. The pose preference remains loose, and large lifts remain possible. Timeout and actual mode-match/support times must be interpreted separately. No physical robot control, deployment, commit, push or publication was performed.
