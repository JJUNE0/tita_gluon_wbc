# TITA inline driving/stepping environment and fresh training

Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN.

Evidence Status: PASS for configuration/native learning/export/runtime/video
checks and starting fresh full training. Full 100k completion and learned
single-support/propulsion quality are NOT_TESTED.

Policy Checkpoint SHA256 (fresh 60-step smoke):
`dd87ed7dd304028825b45e191277903d29fe7e3267854ed0bbb6e1b2a045263f`.

ONNX SHA256:
`23a69ec8faab04d7002cff36b3bb671ff1ba6d35970f3cf306b9f1007fc8f993`.

Full-run checkpoint SHA256: N/A until the first scheduled save at 5,000 steps.
Branch: `agent/codex/tita-walk`. No commit, push, PR or robot operation.

## Final requested behavior

The user's corrected timing takes precedence: the full left/right cycle is
**2 seconds (0.5 Hz)**; feet are offset by **1 second**. Each foot has a
**0.4-second swing**, below the requested 0.5-second limit. Stance fraction is
80%, so each foot has 1.6 seconds stance per full cycle. With half-cycle offsets,
total double support is 1.2 seconds per cycle, and each single-support interval
is 0.4 seconds. Leading side is randomized between the two initial half phases.

`mj_lab/robots/tita/inline_env_cfg.py` derives from flat, reusing the existing
walk gait/reward utilities. New default task is `inline`; legacy `flat` and
`walk` remain selectable for saved experiments. Old configs are not overwritten.

| Condition | Gait | Wheel policy |
|---|---|---|
| Forward/back straight command | On after gait's 1 s startup settle | On |
| Zero command | Off | On |
| Pure yaw command | Off | On |
| Combined translation/yaw | Off | On |

The gate requires emitted abs(vx) > 0.02 m/s, abs(vy) <= 0.02 m/s and yaw == 0.
vy is fixed zero by flat's command ranges. The command cohort is fixed by
ordered environment IDs: 512 of 1,024 sample vx only, with vy/yaw zero and no
standing override. The other 512 retain flat's mixed vx/yaw sampling and its
10% standing-command sampling. Therefore 50% is the **straight-only cohort**,
not a promise that exactly 50% of policy ticks have active gait (settling and
small vx can disable it).

Flat's ranges are retained: vx +/-1.5 m/s, vy 0, yaw +/-3 rad/s. Wheel actions
retain scale 20 during gait. Gains, delays, wheel contacts, terrain, physical
randomization, reset distributions and the baseline reward weights come from
flat. This includes the mass/inertia/CoM/push/bias settings, rather than walk's
reduced-randomization bootstrap. Actor/critic sizes remain 40/44.

## Reward and hold details

Gait-only contact schedule reward is 2, clearance reward is 1 with 4 cm target,
and a small stance-push reward is 0.5. The push term removes the base's rigid
translation and angular contribution from wheel-centre velocity, rotates the
relative velocity into the body frame, and rewards a stance leg moving opposite
commanded vx. Reverse commands reverse the desired leg motion.

The push speed target is min(abs(vx), stride * frequency / stance_fraction).
With a 6 cm stroke, 0.5 Hz and 80% stance this caps at **0.0375 m/s**. Wheels
can still supply most translation; the gait shapes a gentle leg push and lift.
A reward target is not a guarantee of a learned 6 cm stroke.

Flat's symmetric-joint penalty is masked only while gait is enabled, and
hip/shoulder deviation become -0.1 during gait. Their flat values apply outside
gait. Other flat rewards retain their weights/parameters. Base and knee contact
terminate, with -10 termination reward. The settled velocity-qualified position
latch and moving anchor from the prior task are retained.

Saved playback metadata now carries `straight_only` and explicit
`wheel_enable: always` on the two plain wheel velocity actions. Sim2sim restores
this directly, keeping legacy zero-wheel and gait-disabled-wheel policies
unchanged. Its viewer wheel-policy indicator reports the always-enabled mode.

## Fresh training

The user corrected the previous warm-start choice. That run was stopped with
SIGINT at step 14,734 / 29,269 updates, with its last saved
checkpoint `mj_lab/logs/flash_sac/tita_mjlab_103305_882054/model_10000` preserved, SHA256
`d03664a733dcce3af23454e9a235dbd1d394d39d561d9ed2de6c9662a9426f24`. Its automatic FAIL/KeyboardInterrupt result records
the requested interruption, not a newly observed numerical failure.

New run: `tita_mjlab_105509_377182`; PID 1108441; tmux
`mjlab_inline_fresh_20261028_105506`.

- **From scratch**: fresh actor, critic, optimizer, observation/reward
  normalization and replay. `resume=None`, `warm_start=None`; no prior
  checkpoint is read. The seed is 42; matching initial seeds do not constitute
  checkpoint continuation. Fresh initialization should be the default for
  future experiments unless the user explicitly asks to resume/warm-start.
- FlashSAC, 1,024 environments, CUDA 0; target 100,000 new vector steps;
  two learner updates per step. Initial verified snapshot: 800
  steps / 1402 finite updates.
- Checkpoint every 5,000 steps; W&B video every 10,000, 500 frames with the
  existing commanded/actual vx/vy overlay.
- W&B: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/ynykppyu
- Checkpoints: `mj_lab/logs/flash_sac/tita_mjlab_105509_377182/model_<step>`.
- Console: `inline_env_training_console.log`; metrics:
  `tita_mjlab_105509_377182_metrics.jsonl`; source/launch provenance:
  `inline_env_training_launch.json`.

Single-environment inline previews cannot represent a 50/50 cohort. Their
10-second default schedule is stop 1 s, forward 4 s, backward 3 s, turn 1 s,
stop 1 s. Preview speeds are +/-0.5 m/s and yaw 0.5 rad/s within saved ranges.
Explicit --command bypasses both that schedule and the training cohort sampler.
Video JSON records yaw command and gait state/phase in addition to vx/vy.

## Executed checks and observed metrics

- PASS: new native CUDA suite, **5 tests**: exact inheritance of flat actions,
  physical/event config and unaffected rewards; 50% cohort under resampling
  and partial resampling; stop/forward/reverse/turn/mixed gating; retained wheel
  drive; 0.4 s swings, 1 s offset and no simultaneous flight; stance-push
  direction and invariance to body rigid motion. `inline_env_native_checks.log`.
- PASS: existing flat/walk native suite, **23 passed / 8 task-specific skips**;
  `inline_env_legacy_native_checks.log`.
- PASS: hybrid adapter tests, **3 passed**; `inline_env_hybrid_checks.log`.
- PASS: legacy walk adapter, **8 passed / 1 Torch-only skip**;
  `inline_env_legacy_adapter_checks.log`.
- PASS: fresh native inline smoke, 60 steps / 55 finite updates, saved
  `mj_lab/logs/flash_sac/tita_mjlab_105042_191683/model_60`;
  `inline_env_smoke_training.log`. Saved args show resume/warm_start null.
- PASS: ONNX parity on 256 samples, max absolute error
  `5.0067901611328125e-06`; real headless launcher, 300 steps at `[0.3,0,0]`;
  `inline_env_export_runtime.log`.
- PASS: **4 real ROS/MuJoCo/ONNX runs / 94 checks**, new inline and legacy
  gated-wheel walk, manual key callbacks and headless startup. Checks include
  wheel drive during gait and inline gait disabled during turns, plus reset,
  startup and all-substep mode agreement. Passive GUI creation alone is
  suppressed. `inline_env_runtime.json`, `.log`, `.md`.
- PASS: explicit-command native video, 80 frames;
  `inline_env_native_video.log`, `inline_env_smoke_preview.mp4`.
- PASS: default scheduled native video, **500 frames**, all four command tuples
  observed: zero, +/-0.5 vx, yaw 0.5. `inline_env_command_schedule.log`,
  `inline_env_command_schedule.mp4`, `tita_mjlab_play_105449_426436.json`.
  These use an untrained smoke policy and do not establish gait quality.
- PASS: `./scripts/agent-check.sh`, syntax/XML, diff integrity and experiment
  path checks; `inline_env_agent_check.log`.

Initial test-harness failures were corrected: comparing fresh config with
manager-mutated terrain config, using a nonexistent processed-action property,
and an outdated expected error string after stricter metadata validation.
Initial evidence is preserved as `inline_env_native_initial_checks.log` and
`inline_env_hybrid_initial_checks.log`. Production changes were not relaxed to
make these tests pass.

## Changed files and review

- New `mj_lab/robots/tita/inline_env_cfg.py`: unified flat-based environment.
- `mj_lab/robots/tita/mdp.py`: optional straight-only command cohort and gait,
  stance-push reward. Legacy defaults preserve previous behavior.
- `mj_lab/scripts/train.py`: inline task/default; existing FlashSAC maintained.
- `mj_lab/scripts/play.py`: mixed-mode preview and explicit-command handling.
- `mj_lab/checkpoint.py`: straight gait and wheel-drive playback metadata.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/checkpoint.py`, `adapter.py`,
  `sim2sim_node.py`: restore metadata and update viewer wheel mode.
- New `test/test_mjlab_inline.py`; updated
  `test/check_sim2sim_walk_state_machine.py`, `test/test_sim2sim_hybrid.py`.
- `mj_lab/README.md`, `sim2sim/README.md`: configuration and usage.

Pre-existing dirty edits/staged renames were preserved. Starting status:
`inline_env_preexisting_status.txt`; source backups: `inline_env_before_*`;
incremental final diff: `inline_env_incremental.diff`. Task diffs were inspected;
no unrelated source files were changed. Flat/walk config source files and
Isaac training settings are untouched.

Remaining risks: actual learned lift/contact duration and backward stance
motion, robustness at the retained +/-1.5 m/s command range and full flat
randomization, and stop/turn transitions need evaluation after training.
Reward references and timing tests do not prove the physical policy follows
them. Full-run 10k video uploads are pending at this inspection.
