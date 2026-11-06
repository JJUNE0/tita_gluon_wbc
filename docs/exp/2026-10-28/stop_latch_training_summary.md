# Velocity-qualified stop latch and moving position anchor

Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN.

Evidence Status: PASS for contract/logic tests, export, native learning, runtime
regressions and starting retraining. SUSPICIOUS for unchanged-policy stress
diagnostics: changing observations alone caused continued drift and a push
instability. Retrained stopping/push performance and 100k completion are NOT_TESTED.

Policy Checkpoint SHA256 (fresh 60-step validation):
`d13828eefe0b92440551642ff0c1cf464aadf38c2b4f322186672599daaa87fa`

ONNX SHA256: `5df21c76dae2d4012524890640064f5ec8239f97e74ec73adf9f0b05590956e0`.

Warm-start checkpoint SHA256: `6051d031f8df0c0d0f267613c9e3493f0c555d1d63ad6947690ca52a3016afaa`.

Fixed-policy diagnostic checkpoint SHA256: `6d0a0604907cf9c48ec6588847f5aae3ea73e450d058cc52bb695e087873408d`.

Branch: `agent/codex/tita-walk`. No commit, push, PR, robot command or deployment.

## Resulting behavior

New mjlab walk configs require emitted command within the existing zero band,
planar body speed below 0.1 m/s, absolute body yaw rate below 0.15 rad/s and gait
disabled before holding wheel-odometry position. While coasting or moving too
quickly after a shove, the reference follows current odometry and the clean
position-error observation is zero. The first settled sample establishes the
new reference; the final deceleration/walking interval is excluded. Exceeding
velocity thresholds again releases the reference, matching the proposed dynamic
latch condition; there is no added dwell time or hysteresis.

The native accumulated error is bounded to +/-0.3 m before it is stored. This
is equivalent to moving the implicit odometry reference to remain within
0.3 m of current odometry, rather than clipping only the policy output while
an unbounded error remains hidden. Sim2sim explicitly clamps its reference
within `[s - clip_m, s + clip_m]`. This is the moving-anchor option; no leak
coefficient was introduced.

The existing position-drift reward previously anchored on command zero alone.
It now uses the same velocity/gait eligibility for new configs, follows the
actual pose while unlatched, and bounds the XY reference displacement norm to
0.3 m. Its reward weight and exponential kernel are unchanged. Heading-error
observations and heading-drift reward retain their previous semantics.

Actor/critic dimensions remain 40/44. Current simulator truth supplies body
velocity to the latch, via native root-link velocity and the main sim2sim
ObsState. This velocity is not added as another policy observation. A future
robot implementation would need an equivalent velocity estimate; hardware
runtime code was not changed.

The saved wheel observation explicitly carries `velocity_thresholds` and
`moving_anchor`; invalid settings or missing/non-finite body velocity are
rejected. New flags default to disabled/None in old configs. Existing saved
walk policies, flat configs and Isaac training configs retain their prior
behavior. A running old policy is not silently switched to the new latch.

## Executed checks and observed metrics

- PASS: native CUDA suite, 23 passed / 8 task-specific skips;
  `stop_latch_native_checks.log`. Native/adapter agreement includes coasting
  at zero command, lateral/yaw eligibility, first settled sample, drift after
  settling, fast-push release/reacquisition, bounded integral, return from
  the cap (0.30 -> 0.28 m), matching position reward and partial-reset isolation.
  Existing gait, wheel gate, dimensions and timing checks also pass.
- PASS: hybrid adapter suite, 3 tests, including missing/invalid measured
  velocity and metadata rejection; `stop_latch_hybrid_checks.log`.
- PASS: legacy walk adapter suite, 8 passed / 1 Torch-only skip;
  `stop_latch_legacy_adapter_checks.log`.
- PASS: native old 45k checkpoint playback, 10 steps;
  `stop_latch_legacy_native.log`.
- PASS: fresh native smoke, 60 vector steps / 55 finite learner updates,
  `mj_lab/logs/flash_sac/tita_mjlab_103029_016421/model_60`;
  `stop_latch_smoke_training.log`.
- PASS: weights-only warm-start smoke from old model_50000 into the new
  environment, 60 steps / 55 finite updates;
  `mj_lab/logs/flash_sac/tita_mjlab_103154_482969/model_60`, actor SHA256
  `8b176a834f3ed5400df68c7afbc194f537b90756cbc794425ad2806c567968e2`;
  `stop_latch_warm_start_smoke.log`.
- PASS: ONNX parity, 256 samples, maximum absolute error
  `5.7220458984375e-06`; actual launcher, 300 finite headless steps at
  `[0.3, 0, 0]`; `stop_latch_export_runtime.log`.
- PASS: 4 real ROS/MuJoCo/ONNX state-machine runs / 92 checks using new and
  legacy contracts, manual key callbacks and headless startup. Only passive
  GUI creation is suppressed; `stop_latch_runtime.json`, `.log`, `.md`.
- PASS: `./scripts/agent-check.sh`; syntax/XML parsing, diff integrity and
  experiment naming; `stop_latch_agent_check.log`.

## Fixed-policy stress diagnostics

`test/compare_stop_latch_sim2sim.py` uses the same frozen 45k actor in both
cases, with an explicitly recorded observation-parameter override for the
candidate. This tests how the existing policy reacts; it is not a comparison
of two trained policies. Nominal physics and finite states were used in four
650-step runs. Diagnostics do not terminate an episode after a fall.

The abrupt-stop test drives at the saved walk range's maximum 0.5 m/s, then
intentionally bypasses its saved deceleration ramp to emit an abrupt zero.
The push test applies 40 N forward force for 0.3 seconds while commanded zero.
Post-event measurements:

| Scenario | Legacy | New observation on unchanged policy |
|---|---:|---:|
| Stop: maximum backward motion from running peak | 0.170 m | 0.000 m |
| Stop: forward excursion | 0.090 m | 2.072 m |
| Push: maximum backward motion from running peak | 0.327 m | 0.000 m |
| Push: forward excursion | 0.197 m | 23.121 m |

The candidate kept moving above the latch speed threshold, so its position
error stayed zero. In the push case it became unstable (maximum roll/pitch
measure approximately 179.6 degrees); the long displacement includes continued
simulation after instability. Removing the reverse motion alone is not a
successful stop. The position-hold policy needs retraining with the revised
observation and reward, then the same stress tests must be repeated. No
improved control-performance claim is made from these results.

Evidence: `stop_latch_fixed_policy_diagnostics.json`, `.log`, `.png`.

![Fixed-policy stop and push diagnostics](stop_latch_fixed_policy_diagnostics.png)

## Restarted experiment

The user selected restart after validation. Previous run
`tita_mjlab_093903_465777` was stopped with SIGINT after checks. Its automatic
result records FAIL/KeyboardInterrupt at step 51,053 / 101,907 updates for this
requested stop. The last saved model_50000 is preserved and used for warm start.

New run: `tita_mjlab_103305_882054`; PID 1089143; tmux
`mjlab_stop_latch_20261028_103302`.

- 1,024 environments, seed 42, CUDA 0, FlashSAC; 100,000 requested new vector
  steps, two learner updates per step.
- Weights/observation normalization from old model_50000; fresh optimizer,
  reward normalizer and replay; new environment and latch settings.
- Verified initial progress: 1,500 steps /
  2,802 finite updates. This is an inspection snapshot.
- Checkpoint every 5,000 steps. W&B video every 10,000, 500 frames, existing
  commanded/actual vx/vy overlay. First scheduled new video is pending.
- W&B: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/9fj8e1w6
- Checkpoints: `mj_lab/logs/flash_sac/tita_mjlab_103305_882054/model_<step>`.
- Console: `stop_latch_training_console.log`; metrics:
  `tita_mjlab_103305_882054_metrics.jsonl`; provenance: `stop_latch_training_launch.json`.

The old trainer retained its already-imported behavior while files were edited;
old sidecars retain the old settings. For source provenance, the original
startup hashes and `stop_latch_before_*` snapshots describe that old runtime.
Checkpoint disk-source hashes taken during these edits can reflect changed
files rather than already-imported code. New training started only after the
native source edits and its recorded launch hashes match those sources.

## Changed files and review

- `mj_lab/robots/tita/mdp.py`: velocity-qualified wheel latch, stored integral
  bound, reset state and matching world-position reward anchor.
- `mj_lab/robots/tita/walk_env_cfg.py`: opt new walk configs into the settings.
- `mj_lab/checkpoint.py`: save those observation settings.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/checkpoint.py`: validate/restore
  optional latch metadata.
- `sim2sim/sim2sim_ros2_jazzy/sim2sim_ros2_jazzy/adapter.py`: measured-speed latch
  and moving reference; explicit rejection if required velocity is unavailable.
- `test/test_mjlab_tita.py`, `test/test_sim2sim_hybrid.py`: new logic, reward,
  adapter and malformed-input checks.
- `test/compare_stop_latch_sim2sim.py`: saved-policy stop/push diagnostics.
- `mj_lab/README.md`, `sim2sim/README.md`: behavior and compatibility.

Starting status: `stop_latch_preexisting_status.txt`; incremental diff:
`stop_latch_incremental.diff`. Task diffs were reviewed against snapshots.
Pre-existing dirty files and staged renames were preserved; no unrelated
source files were changed. Remaining risks are retraining performance,
threshold sensitivity and slip/velocity-estimation error.
