# PPO versus FlashSAC action mapping and actor update budget

Execution Domain: DESKTOP_DRY_RUN. Historical simulator evidence below is VALIDATION_SIM; no new simulator or hardware command was executed for this audit.

Evidence Status: PASS for source inspection, historical log/checkpoint association, checkpoint hashing, CSV statistics and update-budget arithmetic. SUSPICIOUS for a task-specific action-range bottleneck. NOT_TESTED for changes to training convergence after correcting that range or the noise setting.

Branch: `agent/codex/dev_tita_gluon`.

Policy Checkpoint SHA256, historical PPO `2026-07-28_17-29-09/model_2500.pt`: `7cd85f984a44ec9bab7cbf03566892505b307a3c9f9e24c65e82030a4298fdbe`.

Additional PPO checkpoints and all CSV/source hashes are recorded in `tita_flash_sac_ppo_action_mapping_analysis.json`. The referenced prior SAC noise probe used `model_30000/actor.pt`, SHA256 `bb22d26c8da4d48a399b7020008cf295268474dcda51c37e5faff7dbcc297ded`.

## Observed mismatch

The port retained native TITA action scales, then applied FlashSAC's normalized [-1, 1] action bound. Keeping the scales did not preserve PPO's available joint-command range: PPO's saved `clip_actions` is null and its Gaussian mean can exceed one.

The native action configuration processes leg targets as `q_default + 0.25 * raw_action` and wheel targets as `5 * raw_action`, with zero default wheel velocity. Thus the current bounded SAC can command at most ±0.25 rad leg deviations and ±5 rad/s wheel targets. The native processed-target clip of ±100 is a different stage and does not restore the lost range.

Historical My45c PPO evaluations provide direct evidence that the missing wheel range was used:

| PPO checkpoint iteration | Cruise mean measured base vx | Left wheel mean raw action | Right wheel mean raw action | Cruise rows with abs(left/right mean action) > 1 |
| --- | ---: | ---: | ---: | ---: |
| 1500 | 0.7455 m/s | 1.6645 | 1.7663 | 100% / 100% |
| 2500 | 0.8007 m/s | 1.7993 | 1.8693 | 100% / 100% |
| 2999 | 0.7362 m/s | 1.8199 | 1.9054 | 87% / 91% |

Each cruise contains 100 control ticks, or two simulated seconds. The generator records signed action means across eight environments at each tick. These fractions refer to time rows of environment-mean actions, not the fraction of individual environment actions. A mean above one nevertheless proves that actions outside the current SAC bound were applied in that tick. Signed and absolute means coincide for these cruise rows.

For checkpoint 2500, wheel target means were 8.9967 and 9.3464 rad/s. Those means cannot be produced by the current SAC adapter, which limits each wheel target to ±5 rad/s. This is a concrete difference in the command space, irrespective of how either policy estimates velocity.

Input CSVs: `test/eval_logs/eval_my45c_my43_weights_{1500,2500,2999}.csv`. Their corresponding native result logs identify the checkpoints. `test/eval_logs/_driver_45c.log` identifies the output CSVs, checkpoint paths, eight environments and successful process exits. The recorded driver uses the generator's default cruise command, 0.8 m/s; the CSV itself stores measured speed rather than a command column. Saved PPO `params/env.yaml` confirms wheel scale 5.0, and `params/agent.yaml` confirms no raw-action clipping. This is historical evidence, not a newly executed matched PPO/SAC rollout.

The URDF wheel collision radius is 0.0925 m. The SAC wheel target of 5 rad/s corresponds to a nominal no-slip pure-rolling target of 0.4625 m/s. This calculation is not a hard limit on actual base speed: leg motion, slip, external forces and wheel tracking error matter.

## Port audit and exploration evidence

Native action terms preserve joint order L1/L2/L3/L4-wheel/R1/R2/R3/R4-wheel. The adapter passes raw bounded actions to those terms, which apply scale and offset once. No joint-order or double-scaling defect was identified in this inspected path. The clamp in the training loop and adapter is idempotent; removing one of them would not expand a tanh actor's output range.

The source Wolf velocity adapter also uses [-1, 1] and native scale/offset processing. It does not implicitly provide a larger TITA wheel range. The source adapter is `/home/cocel/Desktop/Research/wolf-quadruped/rl/wolf-stair-rl/scripts/flash_rl/velocity_env_adapter.py`; the general adapter defaults to `scaled_joint_offset_v1` and separately offers a legacy joint-limit mapping. Copying the default mapping into a task tuned with unbounded PPO therefore requires task-specific range calibration.

The previous fixed-SAC-checkpoint native probe already separated independent and repeated action noise without changing estimator inputs or actor weights. Mean first-episode survival capped at 20 seconds was 4.2677 s with independent noise versus 2.6530 s with repeated noise. Both reset seeds had the same direction. That supports a noise-repetition concern for this checkpoint; it does not prove a retraining convergence effect. Full protocol, uncertainty and measurements are in `tita_flash_sac_noise_bounds_summary.md`.

## Optimization-budget confound

The actual SAC run arguments are 4096 environments, batch size 2048 and two critic updates per vector step. The agent updates its actor every second critic update. After replay warmup:

| Quantity per newly collected transition | Current FlashSAC | Current PPO |
| --- | ---: | ---: |
| Direct actor-loss sample uses | `2 / 2 * 2048 / 4096 = 0.5` | `5 epochs = 5` |

PPO collects 24 steps per environment and uses five epochs with four minibatches. The direct actor-loss sample budget per newly collected transition is therefore ten times larger than SAC's current budget. This is a sample-use count, not ten times more useful learning, ten times more compute, or a predicted convergence-time ratio. Replay distributions and objectives differ.

The original Wolf defaults use 1024 environments with the same batch/update settings, yielding two actor-loss sample uses per collected transition. Increasing to 4096 without increasing the learner budget reduced this ratio fourfold. SAC forwards current and next observations together for normalization, but its direct actor objective uses only the current half; the count above concerns that objective.

Consequently, equal environment transitions do not make the current PPO/SAC convergence comparison equal in actor optimization budget. The action mapping and this budget must be considered separately. Velocity-estimator differences were excluded from this diagnosis as requested.

## Corrective direction and remaining uncertainty

A controlled correction should keep SAC's normalized action `u = tanh(mu + sigma * epsilon)` and explicitly map each joint's normalized output into its intended native command range. Wheel and leg mappings should be calibrated separately against the command task and actual PPO-used commands. The actor, replay and critic should share the normalized action coordinates; the environment adapter should apply the configured mapping once. Native last-action observations and action penalties should reflect the action that was actually applied. Training, play, checkpoint metadata and resume must agree on the mapping.

Changing only the actor to output unbounded actions or removing a clamp does not implement this consistent mapping. A larger command mapping also increases physical exploration amplitude, so noise amplitude needs checking together with the range. The repeated-noise setting can be isolated with a fresh run using `actor_noise_zeta_max=1`; resume currently restores checkpoint hyperparameters, so editing the default alone does not change a resumed actor's repetition setting.

No expanded range, gain change, learner-budget change or fresh training ablation was executed. The evidence supports a range mismatch and a repeated-noise robustness problem, but does not establish either as the sole reason for slower convergence. Improved convergence after a correction remains NOT_TESTED.

## Changed files and validation

This task adds this report, `tita_flash_sac_ppo_action_mapping_analysis.json`, and the audit's repository-check/source-integrity logs under `docs/exp/2026-10-14/`. It makes no production behavior change.

Executed offline checks validate all three historical CSVs, their 100 cruise rows, finite action values, checkpoint references in native logs, checkpoint SHA256 hashes and current SAC argument values. These checks returned PASS. Repository validation is recorded in `tita_flash_sac_ppo_action_mapping_agent_check.log`; source integrity is recorded in `tita_flash_sac_ppo_action_mapping_source_check.log`. Existing simulator evidence was read, not rerun. No additional learner unit tests were required for these documentation/statistics-only additions.
