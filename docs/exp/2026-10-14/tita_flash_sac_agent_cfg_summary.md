# TITA FlashSAC agent configuration

Execution Domains: TRAINING_SIM (configuration target), DESKTOP_DRY_RUN (executed checks).

Evidence Status: PASS for CPU configuration/integration and repository checks.
Native Isaac training: NOT_TESTED.

Policy Checkpoint SHA256 / ONNX Hash: N/A; no trained policy was produced.
Synthetic CPU test checkpoints were removed with their test fixtures.

Current branch: `agent/codex/dev_tita_gluon`.

## Changed files and resulting behavior

- Added `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/agents/flash_sac_cfg.py` with `TitaFlatFlashSACRunnerCfg` and `FlashSACAlgorithmCfg`. The runner owns rollout/replay/CLI defaults and estimator handling; `agent` owns model, optimizer schedule, reward normalization and SAC settings.
- Added `flash_sac_cfg_entry_point` to the existing My train/Play registrations in `robots/tita/__init__.py`, preserving their RSL-RL entry points and pre-existing modifications.
- Updated `scripts/flash_sac/runtime.py` and `train.py` to use the new defaults and task configuration rather than duplicated hard-coded learner values. A standard-library-only file loader supports CLI help and CPU tests before AppLauncher; native training resolves the task's registered configuration after startup. Explicit CLI arguments override runner defaults. `--no-compile` and `--no-amp` can disable flags enabled in the config.
- Updated `scripts/flash_sac/play.py` and the README for the same estimator observation policy.
- Added `test/test_flash_sac_config.py` and `test/fixtures/tita_flash_sac_before_cfg_extraction.json`; extended `test/test_flash_sac_entrypoints.py` to verify estimator target omission during train/resume/play.
- Added this report, test/check logs and the task-only source diff under `docs/exp/2026-10-14/`.

`use_velocity_estimator=False` is the current supported configuration. Before environment construction, FlashSAC sets `env_cfg.observations.estimator_target=None` on its run config. This avoids computing an unused PPO supervision group. Policy/critic observations and all existing learner default values remain the same. The shared `my_flat_env_cfg.py`, PPO config and vendor learner were not edited.

Setting `use_velocity_estimator=True` raises a descriptive error before environment mutation: a FlashSAC estimator network, replay targets, supervised loss and actor input connection are still unimplemented. The flag does not silently enable an ineffective estimator. Resume continues restoring the checkpoint's model/optimizer/schedule parameters.

## Observed metrics / behavior / log summary

DESKTOP_DRY_RUN / PASS — Executed:

```bash
PYTHONDONTWRITEBYTECODE=1 TORCHDYNAMO_DISABLE=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  -m unittest discover -s test -p 'test_flash_sac*.py' -v
```

Direct evidence: `Ran 24 tests in 1.660s`, `OK`, exit 0.
See [CPU test log](tita_flash_sac_agent_cfg_tests.log).
New tests verify all 38 previous learner fields and CLI defaults, edited config propagation, CLI priority, CPU AMP handling, compile/AMP disabling, target omission without changing shared PPO config, unsupported estimator rejection, and both native task registration declarations. Existing real CPU learner and mocked train/resume/play tests also pass.

DESKTOP_DRY_RUN / PASS — Executed the standalone config regression:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/cocel/isaac/env_isaaclab/bin/python \
  test/test_tita_my_flat_config_refactor.py
```

Direct evidence: 4 tests in 0.030 seconds, `OK`, exit 0. Both shared TRAIN/PLAY snapshots and term order remain unchanged. System-Python train/play `--help` commands also completed without simulator startup.

DESKTOP_DRY_RUN / PASS — Executed:

```bash
PYTHONPYCACHEPREFIX=/tmp/tita_flash_sac_cfg_agent_check_cache ./scripts/agent-check.sh
```

Direct evidence: 434 Python syntax checks passed, 0 failed; 13 URDF XML files OK; diff integrity, experiment directory checks and final result `PASS`, exit 0. See [agent-check log](tita_flash_sac_agent_cfg_agent_check.log).

[The task-only diff](tita_flash_sac_agent_cfg_task.diff) was inspected against source snapshots taken before this task. Of 61 existing regular files checked, exactly the six intended existing files changed; no unrelated modifications were detected. The temporary source/hash backup was kept under `test/` and removed before completion.

## Remaining limits

Native Isaac simulation and GPU training were not run for this configuration change. CPU integration uses mocked Isaac startup/environment dependencies. Velocity estimator learning remains unimplemented; its `True` setting is intentionally rejected. No commit, push or PR was created.
