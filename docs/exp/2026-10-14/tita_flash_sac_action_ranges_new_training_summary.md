# FlashSAC training with PPO-selected action ranges

Execution Domain: TRAINING_SIM; integration playback: VALIDATION_SIM; regression checks: DESKTOP_DRY_RUN.

Evidence Status: PASS for launch, finite initial updates and integration checks; SUSPICIOUS for the ongoing full training because completion and policy quality are not yet established.

Policy Checkpoint SHA256 (new full run): N/A at startup; first checkpoint is scheduled for vector step 5000. This is a fresh learner, not a resumed old policy.

Policy Checkpoint SHA256 (native integration actor.pt, model_8): `e7cc9a4347dda13c7836b8b5e38cd2bf1262082214dec4c2008f36eca1b7a4df`.

Selection-source PPO SHA256: `4ce6a6471b70e2fec58cbf5d85f1403d94c172dec372625e3fdbae0cc51b3ca7`.

Branch: `agent/codex/dev_tita_gluon`. No commit or publication was requested.

## Running experiment

- PID: `3749238`; confirmed running after W&B initialization and initial updates.
- W&B: [5v50prs6](https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/5v50prs6).
- Run name: `tita_flash_sac_action_ranges_20261014_172127`.
- Task: `DDT-Velocity-Flat-Tita-My-v0`; 4096 environments, 100000 vector steps, CUDA device 0, seed 42.
- Checkpoint directory: `lab/ddt_lab/logs/flash_sac/tita_flash_sac_172127_928297/`.
- Metrics: `docs/exp/2026-10-14/tita_flash_sac_172127_928297_metrics.jsonl`.
- Console: `docs/exp/2026-10-14/tita_flash_sac_action_ranges_20261014_172127_console.log`.
- Launch manifest: `tita_flash_sac_action_ranges_20261014_172127_launch.json`.
- Resolved mapping: `tita_flash_sac_172127_928297_action_mapping.json` and the run directory's `action_mapping.json`.

The observed startup snapshot reached vector step 400, 1638400 transitions, and 748 learner updates. All recorded scalar metrics were finite. Actor loss 0.52712, critic loss 2.10815, temperature 0.009546, mean step reward −0.08197. Mean completed episode length was 10.81 control steps in this early snapshot: finite optimization does not establish useful locomotion. These are startup measurements, not convergence results.

Resolved `agent.json` was compared against the original FlashSAC run: **no learner setting differences**. Thus noise reuse (up to 16 steps), temperature, network architecture, update cadence and replay settings are retained; only the physical mapping of normalized actions changes. The original baseline PID `3301796` remains SIGSTOP-paused with its in-memory simulator/replay retained.

Command, from `lab/ddt_lab`:

```bash
/home/cocel/isaac/env_isaaclab/bin/python -u scripts/flash_sac/train.py \
  --task DDT-Velocity-Flat-Tita-My-v0 \
  --num_envs 4096 --steps 100000 --seed 42 --device cuda:0 --headless \
  --logger wandb --wandb_project tita_flat_flash_sac \
  --run_name tita_flash_sac_action_ranges_20261014_172127
```

## Resulting behavior and changed files

The runner config holds native-order negative gains `(3.2,2,2.8,6)` and positive gains `(2.4,2,2.8,6)` on each side. The adapter applies these about zero, preserving the neutral pose. Existing native leg/wheel scales turn them into hip offsets −0.8/+0.6 rad, shoulder ±0.5 rad, knee ±0.7 rad, and wheel targets ±30 rad/s. All selected leg targets are inside measured soft joint position limits.

Actor/replay/critic action inputs remain normalized in `[-1,1]`; only simulator actions are mapped. Last-action observations and native action-dependent rewards consequently use native action units. The configuration and checkpoint metadata keep this distinction explicit.

| Changed source file | Purpose |
|---|---|
| `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/agents/flash_sac_cfg.py` | Selected gains and validation |
| `lab/ddt_lab/scripts/flash_sac/env_adapter.py` | Sign-dependent native action mapping; normalized input tensor retained |
| `lab/ddt_lab/scripts/flash_sac/runtime.py` | Mapping version, metadata validation and legacy unit-gain restoration |
| `lab/ddt_lab/scripts/flash_sac/train.py` | Fresh config gains; saved gains on resume; run/W&B mapping metadata |
| `lab/ddt_lab/scripts/flash_sac/play.py` | Restore checkpoint action mapping |
| `lab/ddt_lab/scripts/flash_sac/README.md` | Action ranges and checkpoint semantics |
| `test/test_flash_sac_action_ranges.py` | New mapping, normalized replay and legacy play/resume regression coverage |
| `test/test_flash_sac_entrypoints.py` | Existing playback expectation now checks mapped native actions |
| `test/probe_tita_ppo_action_ranges.py` | Native signed distributions and paired candidate-cap rollouts |
| `test/analyze_tita_ppo_action_ranges.py` | Quantiles, phase statistics, paired bootstrap and distribution plots |

Detailed selection evidence: [PPO range-selection report](tita_ppo_action_range_selection_summary.md).

## Executed checks

- `python -m unittest discover -s test -p 'test_flash_sac*.py' -v`: **38 tests PASS**, log `tita_flash_sac_action_ranges_tests.log`. Includes actual CPU learner transitions with normalized replay, selected native gains, malformed mapping rejection, and old-checkpoint unit-gain play/resume.
- Native Isaac train, 4 environments / 8 steps / buffer 128 / warmup 8 / batch 8: **PASS**, 10 finite learner updates, checkpoint `tita_flash_sac_171843_365528/model_8`; log `tita_flash_sac_action_ranges_native_train.log`.
- Native Isaac play of that checkpoint, 4 environments / 8 steps: **PASS**, finite reward; log `tita_flash_sac_action_ranges_native_play.log`.
- `./scripts/agent-check.sh`: **PASS**, 442 Python syntax checks and 13 URDF XML checks; whitespace and experiment-directory checks also passed. Log `tita_flash_sac_action_ranges_agent_check.log`.
- Final task-relative diff inspected. Source-hash comparison against the 626-file pre-task baseline found only the listed six existing Python files changed and three new Python scripts; README changes were separately reviewed. No source files were removed or unrelated source edits made.

Larger gains enlarge physical exploration under unchanged normalized noise. Selected PPO caps retained 98.80% first-episode survival but still caused 5 falls out of 416 paired trials. The new FlashSAC run must establish its own convergence. Wheel target bounds do not enforce measured wheel velocity bounds under the existing DelayedPD/PhysX configuration. FlashSAC deployment/export and hardware validation were outside this task.
