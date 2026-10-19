# Selected TITA flat configuration promotion

- Execution Domain: `TRAINING_SIM` (configuration and 10-step smoke check), `DESKTOP_DRY_RUN` (regression checks).
- Policy Checkpoint SHA256: `ff083cbfc8a8571009a27454e75dc88463e9ebc796fa79e8782ccb4a5bea239d` (reference headw0 65k only; no policy loaded for these checks).
- Evidence Status: `PASS` for configuration equivalence and smoke checks. New policy training, policy sim2sim evaluation and hardware validation: `NOT_TESTED`.
- Branch: `agent/codex/promote-tita-flat-cfg`. No commit, push, deployment or hardware commands.

## Selection and resulting behavior

Promoted `MyTitaFlatPosKneeSphereHeadingObsW0EnvCfg`, used by headw0 50k and 65k, into standalone `TitaFlatEnvCfg` in `flat_env_cfg.py`. Selection follows `flashsac_headw0_50000_142158_review.md` (65k recommended after the turn screen) and `flashsac_headw0_65000_153755_review.md` (operator reports better turning). This is the selected configuration, not a claim that all real-run metrics pass: the 65k report still marks position hold `FAIL` and turning `SUSPICIOUS`.

Final declarations include sphere wheel collisions, unfiltered leg position actions, knee PD 92/2.3 and knee-only output scale 0.55–1.0 with jitter 0.8–1.2, base-only CoM variation ±1.5 cm, wheel-position and gyro-heading observations, and zero heading warmup. Velocity commands retain ±1.0 m/s, ±1.5 rad/s and ramp 0.5. Policy/critic/action dimensions are 35/39/8.

`DDT-Velocity-Flat-Tita-v0` and its Play counterpart now register FlashSAC and estimator PPO instead of NP3O. FlashSAC's default task is the canonical flat ID. The old NP3O flat interface is therefore no longer provided under that canonical ID. The Play config additionally disables knee output randomization alongside other gain/bias overrides.

Deleted `my_flat_env_cfg.py`. Its exact task-start contents are archived in `real2sim/base_env_cfg.py` to preserve historical experimental settings and My task IDs. Source/archive SHA256: `144ebf809c1211a8ac3632b5e5575548dfc95b5dbf83320309b66c045b497cd9`. The package aliases the old module path to the archive so saved config pickle imports resolve. Only the baseline import line was changed in the already-modified `real2sim/env_cfg.py`; its pre-existing experiment additions were retained.

Jump now derives directly from the rough baseline and declares its original flat-terrain overrides, preserving its NP3O observation history and command interface independently of the promoted flat task.

## Changed files for this task

Paths below are relative to `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/` unless otherwise specified:

- `flat_env_cfg.py`: final selected settings and Play config.
- `my_flat_env_cfg.py`: deleted; contents preserved in new `real2sim/base_env_cfg.py`.
- `real2sim/env_cfg.py`: baseline import only.
- `__init__.py`: canonical task routing, historical My routing and pickle module alias.
- `jump_env_cfg.py`: preserve previous rough-derived jump behavior.
- `agents/flash_sac_cfg.py`: canonical flat default task.
- `lab/ddt_lab/scripts/flash_sac/README.md`: task, dimensions and compatibility notes.
- `test/test_tita_my_flat_config_refactor.py`, `test/test_flash_sac_config.py`: moved baseline and new task routing.
- `test/test_tita_flat_promotion.py`: complete resolved-value/manager-order comparison, source identity, Play isolation and jump checks.
- `test/check_tita_flat_promotion_runtime.py`: real Isaac config/import/dimension/10-step check.
- `test/fixtures/tita_real2sim_base_before_flat_promotion.json`: snapshot captured before source migration. The earlier historical fixture is unchanged.
- This report and local `flat_cfg_promotion_*` evidence files in `docs/exp/2026-10-19/` (logs/JSON follow existing Git ignore rules).

## Executed checks and direct evidence

Interpreter: `/home/cocel/isaac/env_isaaclab/bin/python`.

| Check | Result | Observed evidence |
|---|---|---|
| Task-start `test_tita_my_flat_config_refactor.py` | `FAIL` (pre-existing) | 3 failed comparisons: historical fixture predates current hip offsets, wheel scales, reward and DR settings. |
| Updated archived-baseline regression | `PASS` | `python -m unittest discover -s test -p 'test_tita*config_refactor.py'`: 5 tests, OK. Uses the new task-start snapshot; the original fixture remains unchanged. |
| Selected-flat promotion regression | `PASS` | `python -m unittest discover -s test -p test_tita_flat_promotion.py`: 5 tests, OK. All resolved values and manager term order equal the original HeadingObsW0 chain. |
| FlashSAC defaults/config/registry regression | `PASS` | `python -m unittest discover -s test -p test_flash_sac_config.py`: 7 tests, OK. |
| Initial sandbox Isaac launch | `BLOCKED` | `flat_cfg_promotion_runtime.log`: GPU/NVML initialization unavailable inside the sandbox; stopped the stalled launch. |
| Local Isaac smoke check | `PASS` | `flat_cfg_promotion_runtime_host.log`, `flat_cfg_promotion_runtime.json`; process exit 0, all 6 checks true. |

Runtime command:

```bash
/home/cocel/isaac/env_isaaclab/bin/python test/check_tita_flat_promotion_runtime.py \
  --headless --device cpu \
  --output docs/exp/2026-10-19/flat_cfg_promotion_runtime.json
```

Observed: real `to_dict()` configurations identical; old module pickle globals resolve; historical My task still uses archived class; policy 35, critic 39, privileged 18, actions 8; plain `JointPositionAction`; both environments produce finite observations/rewards over 10 zero-action steps. This verifies configuration composition and initialization, not trained-policy balance or real-world performance.

Final repository check: `./scripts/agent-check.sh`, with direct output recorded in `flat_cfg_promotion_agent_check.log`. Final diff review checks task changes separately from the pre-existing dirty worktree; unrelated files were not edited by this task.

Remaining limitations: no new training, exported-policy sim2sim regression or hardware validation. The source configuration's documented real-run backward turn arcs and position-hold oscillation remain unresolved.
