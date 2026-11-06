# Inline gait penalty relaxation — fresh FlashSAC run

Execution Domain: TRAINING_SIM / DESKTOP_DRY_RUN

Evidence Status: PASS for scoped tests, source/configuration checks and a fresh running learner. Full 100000-step completion and learned foot lift are NOT_TESTED for this new run.

Policy Checkpoint SHA256: N/A — first new checkpoint is scheduled at step 5000.

Reference Policy Checkpoint SHA256: `53f54576ddfc1cce3bcf040dcf7cffee74592873bfb4a513e11aa1f2dab83dbe` (previous run, model_100000).

Branch: `agent/codex/tita-walk`.

## Behavior

Only when the existing straight-command gait flag is enabled, reduce the effective penalties as agreed. Standing, pure turning and mixed-command cases with gait disabled retain the flat penalties. The old combined roll/pitch term is split into two axis terms; their sum outside gait is numerically equal to the old combined penalty.

| Penalty | Gait enabled, previous | Gait enabled, new | Gait disabled |
| --- | ---: | ---: | ---: |
| Roll angular velocity squared | -0.05 | -0.01 | -0.05 |
| Pitch angular velocity squared | -0.05 | -0.03 | -0.05 |
| Flat orientation | -5.0 | -1.0 | -5.0 |
| Hip deviation | -0.1 | -0.02 | -1.0 |
| Shoulder deviation | -0.1 | -0.02 | -0.5 |
| Joint mirror (unchanged) | 0 | 0 | -1.0 |

The manager weights remain the gait-disabled weights; the existing per-environment scaling applies the effective gait-enabled coefficients. The scaling callable keeps its original name for saved environment pickles and now forwards an optional angular axis.

The 2 s gait cycle, 1 s left/right offset, 0.4 s swing per foot, 4 cm clearance target, active wheel policy, 50% straight-command cohort, command ranges, physics, randomization, observation/action layout and FlashSAC settings remain unchanged. Saved native configuration comparison confirms that only the six expected reward entries differ, after accounting for mjlab's initialization of terrain num_envs/env_spacing. Evidence: `inline_relaxed_penalties_config_verification.json`.

Deferred idea, NOT IMPLEMENTED: keep the stance foot closer to the robot center of mass and send the swing foot farther from the body, inspired by inline skating. Revisit placement and its direction in a later experiment.

## Training

The previous contact-corrected experiment completed normally at 100000 vector steps and 199802 finite updates while this change was prepared. Its final checkpoint was saved before reward source edits; original source hashes were verified at that boundary. Its final result is `tita_mjlab_114239_024280_result.json`; checkpoint `mj_lab/logs/flash_sac/tita_mjlab_114239_024280/model_100000`. No stop signal was needed.

New run: `tita_mjlab_133533_474303`.

W&B: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/u0depuk3

Checkpoint directory: `mj_lab/logs/flash_sac/tita_mjlab_133533_474303`.

PID: `1245338`; tmux: `mjlab_inline_relaxed_20261028_133530`.

Initialization: **from scratch**. Saved args verify `resume=null`, `warm_start=null`, `wandb_run_id=null`; the trainer constructs a fresh actor, critic, optimizer, normalizers and replay buffer. Step numbering started at zero. No previous policy is loaded.

Budget: 100000 vector steps, 1024 environments, seed 42, CUDA 0, two updates per step. Online W&B logging; checkpoints every 5000 vector steps; videos every 10000 vector steps, 500 frames each, with the existing command/actual velocity overlays.

Observed metrics / behavior / log summary at verification: step **1300**, **2402** finite updates, mean instantaneous reward `-0.110061`. The active source hashes still match launch provenance. Early learning metrics establish startup only; they do not establish physical stepping.

Launch provenance: `inline_relaxed_penalties_training_launch.json`.

Console: `inline_relaxed_penalties_training_console.log`.

Metrics: `docs/exp/2026-10-28/tita_mjlab_133533_474303_metrics.jsonl`.

## Changed files and validation

- `mj_lab/robots/tita/inline_env_cfg.py`: gait-only effective coefficients and separate roll/pitch costs.
- `mj_lab/robots/tita/mdp.py`: forward the axis through the existing gait-based penalty scaler, retaining its saved callable name.
- `test/test_mjlab_inline.py`: update inheritance expectations and verify actual weighted penalties on a mixed gait-on/off batch, including equality to flat angular costs outside gait.
- Experiment provenance, logs, diff and this report under `docs/exp/2026-10-28/`.

PASS: `/home/cocel/venvs/tita_mjlab/bin/python -m pytest test/test_mjlab_inline.py test/test_mjlab_tita.py -q`: **30 passed, 8 conditional skips**, 2 existing mass-randomization warnings; `inline_relaxed_penalties_tests.log`. Coverage includes native CUDA physics, command gating, wheel actions, timing, contacts, termination and the changed reward arithmetic.

PASS: `./scripts/agent-check.sh`: exit 0, **716 Python syntax checks**, **8 URDF XML parses**, diff integrity and experiment-directory checks; `inline_relaxed_penalties_agent_check.log`.

PASS: incremental diff inspected in `inline_relaxed_penalties_changes.diff`. Pre-existing edits were preserved. Hash checks confirm flat/walk configs, robot settings, train/play and checkpoint code unchanged; `inline_relaxed_penalties_preserved_hashes.json`. No unrelated source files changed, and no commit or publication was performed.

Unresolved limits: physical gait quality, zero-command drift and full-budget learning outcomes remain NOT_TESTED for the fresh policy. No hardware run or sim2sim evaluation of the new policy was performed.
