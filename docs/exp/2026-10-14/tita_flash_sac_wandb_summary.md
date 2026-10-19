# TITA FlashSAC W&B logging

Execution Domains: TRAINING_SIM (runtime target), DESKTOP_DRY_RUN (executed checks).

Evidence Status: PASS for CPU integration and repository checks.
Native Isaac simulation and live W&B upload: NOT_TESTED.

Policy Checkpoint SHA256 / ONNX Hash: N/A; no trained TITA policy was produced.
Synthetic CPU test checkpoints were created under test/ and removed.

Current branch: `agent/codex/dev_tita_gluon`.

## Changed files and resulting behavior

- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/agents/flash_sac_cfg.py`: added default project `tita_flat_flash_sac`, optional entity/display name, mode and run ID. Default logger remains `tensorboard`.
- `lab/ddt_lab/scripts/flash_sac/train.py`: added `--logger wandb` plus `--wandb_project`, `--wandb_entity`, `--run_name`, `--wandb_mode` and `--wandb_run_id`. Imports W&B only when selected, before Torch/Isaac imports. Logs resolved agent config, reward weights, dimensions, scalar training/environment metrics and final status/checkpoint metadata. Charts use vector `step` as a custom axis. Explicit run ID requests SDK resume with `allow`; default is a new run. W&B local files and run metadata stay in `docs/exp/YYYY-MM-DD/`. Checkpoint weights are not automatically uploaded.
- The training logger now retains the latest value for each learner metric across critic-only updates. Previously, with two updates per vector step, the final critic-only dictionary discarded the actor loss before logging. This changes metric reporting, not learner updates or rollout behavior.
- Runtime resources use an ExitStack so SDK finish/reporting failures still close the environment and simulator.
- `lab/ddt_lab/scripts/flash_sac/README.md`: documented W&B commands, defaults, optional dependency, local/offline logging and online run continuation. SDK run resume is ignored in offline mode.
- `test/test_flash_sac_config.py`: preserved comparison of all original CLI defaults while permitting the new W&B options; all original learner defaults are still compared.
- Added `test/test_flash_sac_wandb.py` with a fake SDK/Isaac and real CPU FlashSAC. No credentials, network traffic or actual W&B backend process are used.
- Added this report, test/check logs and the task-only diff under `docs/exp/2026-10-14/`.

## Observed metrics / behavior / log summary

DESKTOP_DRY_RUN / PASS — Executed:

```bash
PYTHONDONTWRITEBYTECODE=1 TORCHDYNAMO_DISABLE=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  -m unittest discover -s test -p 'test_flash_sac*.py' -v
```

Direct final evidence: `Ran 31 tests in 2.957s`, `OK`, exit 0.
See [CPU test log](tita_flash_sac_wandb_tests.log).
Seven new checks cover W&B config/CLI priority, SDK import ordering, actual CPU train-loop metric/config forwarding, actor loss retention with two updates, local run-ID recording, existing online run-ID/checkpoint continuation, failed-run status/cleanup, SDK finish-failure cleanup, optional-dependency absence for console, and a clear missing-SDK error before simulator startup. Existing learner, replay, checkpoint and config regressions also pass.

The main W&B fixture ran 4 vector steps with 4 environments and 6 real learner updates. Every post-warmup log contained actor and critic loss. The fake SDK received scalar environment metrics and both selected reward weights. Its final summary contained PASS and a 64-character actor checkpoint hash, and finish was called with exit code 0. Injected logging errors called finish with exit code 1 and closed both simulator and environment. All fixture files were removed.

DESKTOP_DRY_RUN / PASS — System-Python `train.py --help` completed with the new W&B options and no simulator startup.

DESKTOP_DRY_RUN / PASS — Executed:

```bash
PYTHONPYCACHEPREFIX=/tmp/tita_flash_sac_wandb_agent_check_cache ./scripts/agent-check.sh
```

Direct evidence: 435 Python syntax checks passed, 0 failed; 13 URDF XML files OK; diff integrity, experiment directory checks and final result PASS, exit 0. See [agent-check log](tita_flash_sac_wandb_agent_check.log).

[The task-only diff](tita_flash_sac_wandb_task.diff) was inspected against snapshots taken before editing. Of 60 existing regular files checked, exactly the four intended files changed; no unrelated changes were detected. The temporary baseline backup was stored under test/ and removed before completion. Environment/reward configs, vendor learner and other existing changes were preserved.

## Usage and remaining limits

From `lab/ddt_lab/`, run:

```bash
python scripts/flash_sac/train.py \
  --task DDT-Velocity-Flat-Tita-My-v0 \
  --num_envs 4096 --steps 100000 --device cuda:0 --headless \
  --logger wandb --wandb_project tita_flat_flash_sac
```

Authenticate with `wandb login` in the same environment if needed. Missing SDK installation is reported only when W&B logging is selected. `--wandb_mode offline` records locally; when mode is unspecified, the SDK honors `WANDB_MODE`.

Live account authentication, upload and native GPU/Isaac execution were not performed. Tests verify the installed SDK call contract with a fake W&B module; they do not prove backend connectivity. No commit, push or PR was created.
