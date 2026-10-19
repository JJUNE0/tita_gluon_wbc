# TITA FlashSAC GPU training launch

Execution Domain: TRAINING_SIM (native Isaac Lab rollout); DESKTOP_DRY_RUN (regression tests).

Evidence Status: PASS — native GPU startup, finite learner updates, and online W&B logging verified. The requested full training remains in progress.

Policy Checkpoint SHA256: N/A (no checkpoint produced at launch).

Branch: `agent/codex/dev_tita_gluon`.

## Requested execution

Task `DDT-Velocity-Flat-Tita-My-v0`, 4096 environments, 100000 vector steps, seed 42, `cuda:0`, headless, W&B project `tita_flat_flash_sac`.

Interpreter: `/home/cocel/isaac/env_isaaclab/bin/python`. The sandbox cannot see CUDA devices; the approved host execution can access the RTX 3090 (24576 MiB).

Current launch: PID 3301796, run name `tita_flash_sac_4096_20261014_133201`. Detached process, console log `tita_flash_sac_4096_20261014_133201_console.log`; exact command and launch metadata in `tita_flash_sac_4096_20261014_133201_launch.json`.

W&B run: [8v7zlqel](https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/8v7zlqel). Online authentication loaded the existing credentials without prompting. Native run prefix: `tita_flash_sac_133201_468020`; progress is recorded in `tita_flash_sac_133201_468020_metrics.jsonl` and SDK metadata in `tita_flash_sac_133201_468020_wandb.json`.

Observed progress: vector step 900, 1748 learner updates. At step 500: 2048000 transitions, about 51308 transitions/s, reward mean 0.00027126, actor loss 0.24356, critic loss 2.22880, temperature 0.00933913; all finite. The host process was running and occupied 4824 MiB of GPU memory. These are startup/training metrics, not locomotion-quality evidence.

Checkpoint output: `lab/ddt_lab/logs/flash_sac/tita_flash_sac_133201_468020/`, every 5000 steps and at normal exit. No checkpoint exists at the verified startup step, so its SHA256 remains N/A.

## Compatibility fixes required by native execution

- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py`: set the legacy `sim.disable_contact_processing = True` attribute after construction, matching the original rough config. Isaac Lab 2.3 rejects it as a constructor keyword and automatically configures contact processing for sensors. All resolved training/play settings and manager term order remain equal to the pre-refactor fixture.
- `lab/ddt_lab/scripts/flash_sac/runtime.py`: bind the process-local `scripts` namespace to this repository's `lab/scripts`. A separately installed Wolf regular package named `scripts` otherwise shadows local CoRL config imports during task registration. Both train and play use this helper.
- `test/test_tita_my_flat_config_refactor.py`: regression against the installed Isaac Lab `SimulationCfg` constructor without launching native simulator modules.
- `test/test_flash_sac_config.py`: reproduce a foreign regular `scripts` package and verify local CoRL namespace resolution.

Initial launches stopped before training: `132850` rejected the simulation constructor keyword; `133022` imported the foreign Wolf wrapper and could not resolve `CoRlHybridPpoActorCriticCfg`. Their automatic run summaries and console logs retain the original errors. Neither produced a checkpoint.

## Validation evidence

- PASS: 5 config regression tests, including installed constructor compatibility and complete train/play fixture equality. Log: `tita_flash_sac_training_config_regression.log`.
- PASS: 32 FlashSAC tests, including import collision regression, actual CPU learner updates, checkpoint restore, timeout handling, and W&B lifecycle with a fake SDK. Log: `tita_flash_sac_training_cpu_tests.log`.
- PASS: `./scripts/agent-check.sh`: 435 Python syntax checks, 13 URDF parses, diff integrity and experiment directory checks. Log: `tita_flash_sac_training_agent_check.log`.
- PASS: reviewed the current-task source diff in `tita_flash_sac_training_source.diff`; the 505-file source baseline confirms only the two intended runtime/config files changed. The two test files listed above received the corresponding regression additions. Pre-existing unrelated edits were retained.

No commit, push, or publication was performed. Native GPU execution was explicitly requested; the long-running training process remains detached and active after startup verification.

Startup evidence is separate from completion of the requested 100000 steps or locomotion quality validation. Native training uses the existing 33-dimensional policy and 36-dimensional critic; the PPO velocity estimator is disabled by the FlashSAC runner config.
