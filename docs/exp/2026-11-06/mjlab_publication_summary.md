# Publish the mjlab pose, sit/stand and left/right support experiments

- Execution Domain: `DESKTOP_DRY_RUN`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A`; this publication changes source,
  documentation and validation evidence. No policy weights are published or changed.
- Evidence Status: `PASS` for the desktop checks listed below. GPU execution,
  new training, trained-policy quality and hardware behavior: `NOT_TESTED`.
- Preparation branch: `agent/codex/mjlab-pose-publication`.
- Original workspace branch: `agent/codex/tita-walk`.
- Base commit: `a96d234ff60f900adfd14251e9d2bb597c10ffc1`.
- W&B run URL: `N/A`; this is an explicitly local/offline publication check.
  No training or W&B upload was performed during this task. Historical run
  summaries retain their original results and checkpoint hashes.

## Authorized scope

The user requested mjlab and roll/pitch/height experiments, then explicitly
included sit/stand and left/right support. The user's later request to publish
directly to `main` overrides the repository's usual draft-PR publication path
for this task. Preparation and tests still run on an isolated agent branch;
the original workspace and its staged changes are preserved.

Included source and behavior:

- Path migration of the existing `lab/` tree to `isaac_lab/`, with the necessary
  active source/test references. The existing shared FlashSAC learner is reused.
- `mj_lab/` package, native robot/physics setup, flat/walk/inline environments,
  checkpoint interchange, training and deterministic playback.
- Roll/pitch/base-link-height commands, sit/stand, the standing-height variant,
  height-only training, fixed left/right references, left/right anchor variants,
  support-command and support-velocity environments.
- Shared W&B online defaults, the 10,000-vector-step video cadence, native
  checkpoint video support and warm-start/resume handling required by these tasks.
- Sim2Sim pose/support/gait observations, wheel control, saved command ranges,
  pose ramps, YAML caps/friction and support tilt handling. The runtime restores
  the contract saved with each checkpoint.
- Required corrected TITA MJCF assets, pose preview configuration, conventional
  experiment queue/evaluation tools, tests and selected historical summaries.
- Official mjlab v1.6.0 submodule at
  `0fb8a681136be94ffc636a3dd423cabb97d91f10`.

Excluded: `mj_lab/zeroshot_rl/`, BFM/FB experiments and dependencies, newly added
learned-residual experiments/runtime hooks, hardware-controller changes, model
checkpoints, datasets and local backup/debug snapshots. Residual controllers
already present in the base commit are retained; their test path migration is
not a new residual experiment.

The new package declaration omits the excluded zeroshot package. The copied
Sim2Sim code has its later learned-residual CLI, torque, payload and disturbance
hooks removed. This makes the selected publication independent of those files.

## Directly executed validation

| Check | Result | Evidence |
| --- | --- | --- |
| CPU mjlab environment/config/command and Sim2Sim suites | `PASS`: 98 passed, 41 skipped, 4 deselected, 53 subtests passed | `mjlab_publication_cpu_tests.log` |
| Shared FlashSAC config/entrypoint/W&B/video/warm-start and queue suites | `PASS`: 34 passed, 1 skipped, 2 subtests passed | `mjlab_publication_shared_tests.log` |
| Final Sim2Sim walk/hybrid/pose/state-machine/command-limit regression after removing residual hooks | `PASS`: 27 passed, 53 subtests passed | `mjlab_publication_sim2sim_final.log` |
| Native train and play CLI help | `PASS`: both exit 0 | `mjlab_publication_train_help.log`, `mjlab_publication_play_help.log` |
| Required `./scripts/agent-check.sh` | `PASS`: 647 Python files, 8 URDFs, diff integrity and experiment-directory checks | `mjlab_publication_agent_check.log` |
| Original workspace index audit | `PASS`: SHA256 unchanged from the pre-copy snapshot | Verification before publication |
| Scope audit | `PASS`: no excluded BFM/zeroshot/new learned-residual source, hardware changes, weights or checkpoint symlinks staged | Final diff and path inspection |

The primary suites used `/home/cocel/venvs/tita_mjlab/bin/python` with
`CUDA_VISIBLE_DEVICES=''`. Four inline cases requiring an unguarded GPU fixture
were explicitly deselected. GPU cases with existing guards were skipped.
The other skipped case is an existing guarded shared-suite check. Existing
GPU training was active, so this task did not allocate GPU simulation work.
Some playback contract tests used existing local checkpoints through an ignored,
unstaged fixture symlink; that symlink and the checkpoints are not published.
The pose playback suite skips cleanly when its local checkpoint is unavailable.

The first CPU run found one stale walk-test assumption: it expected the saved
sideways range even when the operator YAML cap was zero. The test now supplies
an explicit permissive cap while checking saved-range restoration. Dedicated
command-limit tests still check restrictive and zero caps. The initial result
is retained in `mjlab_publication_initial_cpu_tests.log`; the subsequent CPU and
final Sim2Sim suites passed. Historical summary whitespace was normalized in
the publication copy without changing its reported results.

## Remaining limits

These checks establish CPU command/reward/configuration and interface behavior,
not converged skill quality. GPU physics, fresh learning, export parity, viewer
interaction, online W&B uploads and physical robot operation were not rerun.
Checkpoints and large local evidence referenced by historical reports remain
in the original local experiment storage. A new checkout needs the submodule
and the documented mjlab environment before running native simulations.
