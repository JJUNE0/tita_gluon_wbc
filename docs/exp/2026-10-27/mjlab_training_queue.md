# mjlab flat/walk 100k queue and Isaac comparison

Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN

Evidence Status: PASS for queue installation and validation. The two full
training runs and their final comparisons are NOT_TESTED while waiting.

Policy Checkpoint SHA256 (current Isaac walk model_45000, observed while scheduling):
`2be00e8aa13519d820d1efa2243fc065a4b87b338236962e74ee753d205744bf`

Policy Checkpoint SHA256 (Isaac flat model_100000 reference):
`83b266e64ffce1d32cd6c7530a673e3d44a9e0705fa0ede72e4bb4c324200b68`

New mjlab checkpoint hashes: pending; the queue records the final actual hashes
and result files after each training process exits.

Branch: `agent/codex/tita-walk`. No commit, push, PR or hardware commands.

## Installed queue

Detached tmux session: `mjlab_flat_walk_20261027_224638`.

1. Wait for the existing Isaac PID 418996, run
   `tita_flash_sac_214239_278101`, to exit, including video and W&B cleanup.
2. Verify its actual `model_100000/actor.pt` hash and checkpoint step.
3. Train mjlab `flat` with the existing FlashSAC for 100,000 vector steps.
4. Train mjlab `walk` independently for 100,000 vector steps.
5. Generate separate flat/walk Isaac-vs-mjlab learning-curve PNGs and a raw CSV,
   write a summary with checkpoint/metric-file hashes, and upload the two graphs
   and final-window table to a separate W&B comparison run.

Both mjlab runs start from scratch: 1,024 environments, seed 42, CUDA 0,
1,000,000-transition replay, warmup 100,000 transitions, batch 2,048,
2 learner updates per vector step, n-step 3. Checkpoints every 5,000 steps;
online W&B project `tita_flat_flash_sac`; 500-frame CMD/ACT vx/vy videos every
10,000 steps. No resume or warm-start checkpoint is used.

The dependency is identified by PID, Linux start ticks and boot ID, so a reused
PID does not cause the queue to wait for an unrelated process. A file lock
prevents concurrent copies of the queue runner. The preceding process is never
signalled. A missing/corrupt 100k dependency checkpoint stops the queue instead
of calling an interrupted Isaac run complete. An individual mjlab failure is
recorded; the other independent job is still attempted. A failed/incomplete run
does not receive a successful full-comparison report.

The detached queue survives closing the terminal; it is not a reboot-persistent
system service. Runtime status and errors are written to the state JSON.

Local queue records:

- Manifest: `mjlab_flat_walk_20261027_224638_manifest.json`
- Live state: `mjlab_flat_walk_20261027_224638_state.json`
- Queue console: `mjlab_flat_walk_20261027_224638_queue.log`
- Launch confirmation: `mjlab_training_queue_launch.json`

Training console logs go into `docs/exp/<actual-start-date>/`; native training
also records metrics and W&B/video evidence there. The queue's fixed state file
points to each finished run's actual result, metrics and checkpoint directory.
Final figures/CSV/report go into `docs/exp/<actual-comparison-date>/`, with prefix
`mjlab_flat_walk_20261027_224638`. The state JSON records the comparison result
path and its W&B URL when available.

## Comparison references and metrics

- Flat: Isaac `tita_flash_sac_173757_852342/model_100000`, the completed selected
  `DDT-Velocity-Flat-Tita-v0` baseline. Confirmed 35 actor observations, hip
  default 0, wheel scale 20, vx ±1.5, vy 0, yaw ±3, and 100k logged steps.
- Walk: the current Isaac axes-weight run
  `tita_flash_sac_214239_278101/model_100000` after it completes.

Each task gets a six-panel PNG: episode return, episode length, logged linear
tracking error, logged yaw tracking error, mean step reward and training
throughput. Faint raw curves and a trailing-20-log-sample average share the
original vector-step axis. The CSV preserves original unsmoothed samples.

Added mjlab velocity-command metrics using the same scaling as Isaac's command
diagnostics. `compute(dt=0)` during partial resets does not accumulate extra
error. This addition only logs diagnostics; action, observation and reward
calculations are unchanged. Logged command errors are not labelled as raw RMS
tracking errors. Different contact physics/randomization and a single seed mean
these figures are learning-run comparisons, not proof that one engine is better.
Throughput also includes the machine's other load.

## Files changed for this scheduling request

- `scripts/queue_mjlab_flash_sac.py`: durable local process queue and state log.
- `test/analyze_mjlab_isaac_training.py`: paired learning curves, CSV, hashes,
  summary and W&B figure upload.
- `test/test_mjlab_training_queue.py`: real subprocess wait/order/integrity tests
  and real plotting/CSV tests using temporary fixtures exclusively under `test/`.
- `mj_lab/robots/tita/mdp.py`: velocity diagnostic accumulators only.
- `test/test_mjlab_tita.py`: diagnostic scaling/reset-isolation regression.
- This report and queue manifest/state/launch records.

Pre-existing migration, training and unrelated workspace edits were preserved.

## Executed checks

Observed Metrics / Behavior / Log Summary:

- PASS: `python -m pytest -q test/test_mjlab_training_queue.py test/test_mjlab_tita.py`:
  21 passed, 3 inapplicable cases skipped. `mjlab_queue_checks.log`.
- PASS: real subprocess predecessor wait, flat-before-walk ordering and final
  comparison invocation; no training starts while the predecessor is alive.
- PASS: checkpoint hash/step rejection, two PNGs and raw CSV creation,
  incomplete-run and non-monotonic-metric rejection.
- PASS: native GPU velocity diagnostics match Isaac's scaling and do not
  double-count reset-only reads.
- PASS: `./scripts/agent-check.sh`; `mjlab_queue_agent_check.log`.
- PASS: live tmux session and `waiting_for_isaac` heartbeat confirmed, both
  mjlab jobs pending, queued source hashes matching current files.
- NOT_TESTED: completion of the two queued 100k runs and actual final graph
  upload; their future result records will provide direct evidence.
