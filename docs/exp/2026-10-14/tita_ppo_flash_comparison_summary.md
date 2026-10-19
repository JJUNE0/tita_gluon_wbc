# PPO / FlashSAC training and action-range comparison

Execution Domain: TRAINING_SIM for PPO training and FlashSAC suspension; VALIDATION_SIM for the common evaluation; DESKTOP_DRY_RUN for analysis and repository checks.

Evidence Status: PASS — requested PPO training and both matched native comparisons completed with finite metrics and unchanged pinned checkpoints. This is an execution/evidence status; it does not establish hardware readiness or guarantee convergence after changing SAC's range.

Policy Checkpoint SHA256, paused FlashSAC `model_70000/actor.pt`: `118f7c1a76cf5af2d968709073d03e6ce9867354ffafd1db3953d23547c4b962`.

Branch: `agent/codex/dev_tita_gluon`.

## Authorized scope and training budget

The user requested temporarily stopping the running FlashSAC and comparing it with roughly 2000 iterations of PPO. The user explicitly selected PPO 2000 iterations versus approximately 48000 FlashSAC vector steps. The prior constraint excluding velocity-estimator differences is retained: the comparison PPO is plain PPO with the same 33 actor inputs and 36 critic inputs as FlashSAC. It does not use the PPO velocity estimator or its auxiliary targets.

FlashSAC PID 3301796 was suspended with SIGSTOP after verifying its 70000-step checkpoint hash. The process and replay remain in memory; it has not been killed or restarted. Suspension evidence is `tita_flash_sac_ppo_comparison_pause.json`. SIGCONT can resume the same process.

PPO PID 3460441 is a fresh run using seed 42 and 4096 environments. Its environment is loaded from the verified FlashSAC checkpoint's `env.pkl`; reward terms, action scales, PD limits/delays, commands and physical randomization remain the saved configuration. PPO uses the existing plain `TitaFlatPPORunnerCfg` optimizer/network defaults, including 24 rollout steps per environment, five epochs, four minibatches, unbounded Gaussian raw actions and empirical observation normalization. FlashSAC remains its existing bounded actor and repeated-noise algorithm.

The comparison harness is `test/train_tita_ppo_comparison.py`. All new training logs, saved environment/agent configuration and checkpoints are in `docs/exp/2026-10-14/tita_ppo33_flash_comparison_151238/`. Launch metadata and console output are `tita_ppo33_flash_comparison_151238_launch.json` and `tita_ppo33_flash_comparison_151238_console.log`. Checkpoint manifests store completed iterations, vector steps, transitions and SHA256 hashes; PPO checkpoint filenames retain the runner's zero-based iteration index.

W&B run: https://wandb.ai/bjy6614-postech/tita_flat_flash_sac/runs/hzgdfyh2 . Metrics use `comparison/vector_step` as their axis. Both algorithms use project `tita_flat_flash_sac`; PPO checkpoint files stay local.

Collected budgets:

| PPO completed iterations | PPO vector steps | Existing FlashSAC checkpoint | Budget relation |
| --- | ---: | ---: | --- |
| 208 | 4992 | 5000 | SAC has 0.16% more transitions |
| 1875 | 45000 | 45000 | Exact equal collected transitions |
| 2000 | 48000 | 50000 | SAC has 4.17% more transitions |

After the user stated that the existing results were sufficient to establish the trend, the final evaluation was narrowed to the completed PPO 2000-iteration checkpoint, its two action-cap interventions and FlashSAC 50000 steps. The 1875-iteration checkpoint is retained, but no additional exact-budget evaluation or 70000-step evaluation was executed. FlashSAC has 4.17% more collected transitions in the final comparison. Learner sample reuse, network architecture, optimization objectives, initial episode-length randomization and action distributions differ between algorithms. A single training seed does not establish universal convergence speed.

## Common evaluation protocol

`test/eval_tita_ppo_flash_comparison.py` runs deterministic policies on the same saved environment, with 128 environments grouped equally by target x velocity 0, +0.4, +0.8 and -0.8 m/s. The native command ramp and zero yaw/lateral targets are retained. Reset seeds 42 and 43 are paired. The initial root/joint state, actor observations and actuator gains are checked for equality. Saved physical/startup/reset randomization remains; per-step observation corruption and random pushes are disabled identically.

Each trial includes only its first episode, up to 20 seconds. Physical terminal state is captured before automatic reset. Primary metrics are survival time capped at the shared horizon, fraction reaching the horizon without fall and the upright-weighted tracking integral divided by the full horizon, with zero contribution after failure. Conditional velocity/error averages over surviving time are secondary and subject to survival selection. Zero-command drift is recorded with episode survival so short failed episodes cannot be mistaken for successful standing.

Besides original PPO and saved FlashSAC actors, the evaluator tests the same PPO checkpoint with all raw actions capped at ±1 and with only wheel actions capped at ±1. These are inference interventions on a fixed actor. They can show sensitivity to the cap, but cannot establish how a PPO trained with that cap would perform or how expanding SAC's range would change convergence.

## Results and validation

### Early budget: PPO 208 iterations versus SAC 5000 steps

PASS: native evaluation exited 0 and completed four policies × two reset seeds, 256 first-episode trials per policy. All paired initial measurements were identical, actions and physical metrics were finite, and pinned checkpoint hashes remained unchanged. Raw evidence: `tita_ppo33_flash_early_151753.json` and eight trajectory NPZ files. Aggregated results and paired confidence intervals: `tita_ppo33_flash_early_analysis.json`. Console evidence: `tita_ppo33_flash_early_console.log`.

| Policy | Mean survival, capped at 20 s | 20 s without fall | Tracking integral / full horizon |
| --- | ---: | ---: | ---: |
| PPO, original actions | 19.7697 s | 98.83% | 0.9050 |
| PPO, wheel actions capped at ±1 | 3.1938 s | 11.33% | 0.0953 |
| PPO, all actions capped at ±1 | 2.1823 s | 5.86% | 0.0734 |
| FlashSAC 5000 steps | 2.0479 s | 5.86% | 0.0856 |

The original PPO actor's time-weighted wheel raw-action magnitude was 1.0531, and 53.61% of wheel component/tick samples during first-episode survival exceeded ±1. Wheel-only clipping preserves the original PPO leg outputs. Its survival loss versus the original PPO was -16.5759 s, with a 95% stratified physical-environment cluster bootstrap interval [-17.3729, -15.7263] s. Both reset seeds showed the same direction. These intervals describe this checkpoint and scene; they do not account for additional training seeds.

This early comparison supports the user's observation of much faster PPO learning even without a velocity estimator. It also shows a substantial fixed-policy sensitivity to the wheel command cap. It does not prove that a policy trained with bounded commands cannot learn or that enlarging SAC commands alone resolves convergence.

The early evaluator was updated afterward to retain extra per-joint action statistics for the final evaluations. The early raw files retain the original ten metric fields; the shared evaluation physics, policy loading, action-cap intervention and primary metric definitions are unchanged.

PASS: PPO completed all 2000 requested iterations (48000 vector steps, 196608000 transitions), with 2000 finite metric rows and final checkpoint `model_1999.pt`. SHA256: `4ce6a6471b70e2fec58cbf5d85f1403d94c172dec372625e3fdbae0cc51b3ca7`. Full completion metadata and hashes are in the training run's `run.json`.

### Final budget: PPO 2000 iterations versus SAC 50000 steps

PASS: native evaluation exited 0, completing four policies × two reset seeds, 256 first-episode trials per policy. Every paired initial measurement matched exactly, actions/physical measurements were finite and checkpoint hashes remained unchanged. Raw evidence: `tita_ppo33_flash_final_155117.json`, eight trajectory NPZ files and `tita_ppo33_flash_final_console.log`. Final statistics and paired intervals for both budgets are in `tita_ppo_flash_comparison_analysis.json`.

FlashSAC 50000-step actor SHA256: `c43844571362bf4c0e2a92d01bfcdddfe8730a3acfedd7809c91b329ce80fa23`.

| Policy | Mean survival, capped at 20 s | 20 s without fall | Tracking integral / full horizon |
| --- | ---: | ---: | ---: |
| PPO 2000 iterations, original actions | 19.9252 s | 99.61% | 0.9642 |
| PPO, wheel actions capped at ±1 | 1.2191 s | 1.95% | 0.0415 |
| PPO, all actions capped at ±1 | 0.9813 s | 0.78% | 0.0309 |
| FlashSAC 50000 steps | 5.7773 s | 24.22% | 0.1896 |

Paired mean survival differences versus original PPO: SAC -14.1479 s, 95% physical-environment cluster bootstrap interval [-15.0994, -13.1706] s; wheel-only cap -18.7061 s, interval [-19.0295, -18.3255] s. All-action cap -18.9439 s, interval [-19.1842, -18.6387] s. Each comparison had the same direction in both reset seeds.

The original PPO's time-weighted fraction of samples exceeding absolute raw action one was 50.52% / 49.01% for left/right wheels and 39.89% / 38.58% for left/right hip joints. These are component/tick samples over first-episode surviving time, unlike the historical CSV's environment-mean row fractions. Shoulder fractions were 0.43% / 0.24%; knee fractions were 5.38% / 3.11%. The wheel-only cap intervention alone strongly reduced survival; leg-only effects were not tested.

| Target vx | PPO mean survival | SAC mean survival | PPO / SAC tracking integral |
| --- | ---: | ---: | ---: |
| 0.0 m/s | 20.0000 s | 8.0216 s | 0.9837 / 0.3640 |
| +0.4 m/s | 20.0000 s | 6.8434 s | 0.9709 / 0.2332 |
| +0.8 m/s | 19.7006 s | 4.3691 s | 0.9534 / 0.0920 |
| -0.8 m/s | 20.0000 s | 3.8750 s | 0.9488 / 0.0693 |

Zero-command displacement after the full horizon was not negligible: among horizon survivors it averaged 0.4451 m for PPO (64/64 survivors) and 1.4913 m for SAC (24/64 survivors). These conditional survivor populations differ, so drift alone is not a paired whole-population score. Stable balance and high velocity-tracking reward do not establish tight position holding.

The tested PPO learned effective straight-line balance/tracking much earlier than the tested SAC, with no explicit velocity estimator in either actor. The cap interventions show that the trained PPO controller depends strongly on command authority outside the current SAC range. They do not establish that range is the only cause or prove that a bounded policy cannot learn a different strategy. Network/optimizer/reuse/noise differences remain; there was one training seed.

Learning curves and native comparison figures are `tita_ppo_flash_learning_curves.png` and `tita_ppo_flash_native_comparison.png`. Learning curves smooth logged metrics over approximately 1000 vector steps; reset/log collection windows differ. The native chart uses the shared first-episode metrics above.

FlashSAC stays suspended; PPO completed and closed its simulator after resuming from the early evaluation pause. PPO wall/loop time contains that pause, so this report does not claim a wall-time benchmark.

## Is the action bound required, and should it use the maximum limit?

There is no special SAC requirement that physical commands be numerically confined to ±1. The current FlashSAC implementation uses a squashed Gaussian in normalized action coordinates and computes its log probability with the tanh Jacobian correction (`vendor/flash_rl/agents/flashSAC/layer.py`, `NormalTanhPolicy`). A different policy distribution is possible, but removing tanh alone would leave the current density calculation and action transport inconsistent.

The normalized range can be mapped into a larger task-specific command range. [OpenAI's SAC implementation](https://raw.githubusercontent.com/openai/spinningup/master/spinup/algos/pytorch/sac/core.py) multiplies tanh output by the environment's action limit; its [SAC documentation](https://raw.githubusercontent.com/openai/spinningup/master/docs/algorithms/sac.rst) describes the squashed Gaussian and corresponding density calculation. The physical range is therefore a separate mapping choice.

For the current TITA native wheel scale, an adapter mapping `native_action = wheel_gain * u` followed by unchanged native processing gives `omega_target = 5 * wheel_gain * u`:

| Wheel gain | Normalized actor bound | Native wheel raw-action bound | Wheel target bound |
| --- | --- | --- | --- |
| 1, current | ±1 | ±1 | ±5 rad/s |
| 2, candidate | ±1 | ±2 | ±10 rad/s |
| 3, candidate | ±1 | ±3 | ±15 rad/s |
| 6, configured velocity maximum | ±1 | ±6 | ±30 rad/s |

A first candidate is wheel gain 3, covering the approximately 9 rad/s wheel commands observed in prior PPO cruise logs with additional command margin. This is an untested candidate, not a validated optimum. Gain 6 would increase physical exploration amplitude sixfold at the same normalized policy, including repeated-noise excursions. Wider action-space coverage is not equivalent to better exploration or convergence. Actual wheel speed can differ from a PD target.

Leg actions are position deviations, so their limits cannot be obtained from the 30 rad/s actuator velocity setting. They require joint-specific position bounds relative to the default pose. Effort limits (legs 60 Nm, wheels 12 Nm) are separate from either command range. A common gain equal to the wheel velocity limit would be inappropriate for the leg position channels.

A range experiment should use a fresh training run with explicit per-joint mapping, consistently saved/restored by training, play and checkpoint metadata. The learner/replay/critic should retain normalized coordinates while native observations and action penalties reflect the applied native actions. Existing replay generated with a different mapping should not be silently reused. Mapping and noise changes should be isolated to attribute their effects. No gain change, maximum-range experiment or production implementation change was executed in this task; convergence after widening the range remains NOT_TESTED.

PASS: CLI help and Python compilation were executed for the three new harnesses. The training harness initialized a real 4096-environment PPO run, verified 33 actor / 36 critic observations and eight actions, and completed 2000 iterations with finite losses and checkpoints. Both native comparisons exited successfully, for 16 total policy/seed cases and 2048 first-episode trials. Offline aggregation, cluster bootstrap and chart generation executed successfully. Repository-check and source-integrity evidence are recorded in `tita_ppo_flash_comparison_agent_check.log` and `tita_ppo_flash_comparison_source_check.log`.

Only `test/train_tita_ppo_comparison.py`, `test/eval_tita_ppo_flash_comparison.py`, `test/analyze_tita_ppo_flash_comparison.py` and evidence under `docs/exp/2026-10-14/` are added by this task. Production trainer/environment/agent configuration files are unchanged. No hardware action, commit, push or publication is part of this comparison.

PASS: source hashes confirm all 623 pre-existing inspected source/config files are unchanged; the only added sources are the three diagnostic harnesses named above. Final diffs were inspected. The repository check's executed test results are preserved in its log; no additional learner unit suite was run because the production learner was unchanged and the diagnostic paths were exercised natively.
