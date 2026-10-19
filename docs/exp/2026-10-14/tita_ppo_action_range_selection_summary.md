# PPO action distributions and FlashSAC range selection

Execution Domain: VALIDATION_SIM (native rollouts), DESKTOP_DRY_RUN (analysis and regression tests), TRAINING_SIM (new range mapping).

Policy Checkpoint SHA256 (PPO model_1999.pt): `4ce6a6471b70e2fec58cbf5d85f1403d94c172dec372625e3fdbae0cc51b3ca7`

Evidence Status: PASS for distribution collection, candidate rollouts and CPU mapping tests. New FlashSAC convergence: NOT_TESTED at selection time.

Branch: `agent/codex/dev_tita_gluon`.

The user requested coefficients based on the converged PPO action distribution, including leg position targets, and then authorized starting FlashSAC with those coefficients. The PPO checkpoint is the plain 33-observation actor trained for 2000 iterations; it has no velocity estimator. Its environment configuration matches the original FlashSAC comparison.

## Observed distributions

`test/probe_tita_ppo_action_ranges.py` evaluated 13 profiles: stand, forward/backward 0.4, 0.8 and 1.0 m/s, yaw ±1.5 rad/s, forward/backward combined turns, walk-stop and turn-stop. Commands use the native 0.5-unit/s ramp. Each profile has 16 environments, 20-second first episodes, and seeds 42/43/44: 624 trials and 624000 observations per joint. All baseline trials survived 20 seconds. Native startup/reset randomization, actuator delays and reset IMU/encoder biases remain; policy observation corruption and random pushes are disabled consistently for evaluation. Terminal physical state is captured before automatic resets.

Absolute deterministic PPO mean-action percentiles, in native raw-action units:

| Joint | Left p99.5 | Right p99.5 | Left p99.9 | Right p99.9 |
|---|---:|---:|---:|---:|
| Hip | 2.941 | 2.772 | 3.601 | 3.325 |
| Shoulder | 0.955 | 0.753 | 1.602 | 1.393 |
| Knee | 1.788 | 1.505 | 2.361 | 1.896 |
| Wheel | 5.550 | 4.802 | 10.456 | 6.259 |

Rare startup/recovery commands have large tails. Absolute maxima alone would demand excessive position targets. Signed hip tails also differ by side, so the selected common left/right hip range is asymmetric about the default pose. Analysis separates startup, tracking and stopping phases; it records both counterfactual Gaussian samples on baseline states and actually executed Gaussian PPO rollouts. These are different distributions.

Plots: [signed distributions](tita_ppo_signed_action_distribution.png), [absolute action tails](tita_ppo_action_tail_distribution.png).

## Paired candidate rollouts

Seeds 42/43, 208 environments per condition, seven conditions, 2912 first-episode trials. Matched initial physical/observation states and a separate Gaussian RNG preserve comparisons. Survival is over the full 20-second horizon. Tracking below uses the full horizon, assigning zero after termination; it avoids selecting only surviving steps.

| Condition | Mean survival, s | 20-second survival | XY tracking | Yaw tracking |
|---|---:|---:|---:|---:|
| Original deterministic PPO | 20.000 | 100.00% | 0.96460 | 0.97526 |
| Original Gaussian PPO | 20.000 | 100.00% | 0.95744 | 0.95180 |
| Selected legs, wheels ±15 rad/s | 13.458 | 62.02% | 0.63987 | 0.65497 |
| Selected legs, wheels ±20 rad/s | 18.148 | 89.42% | 0.87217 | 0.88517 |
| **Selected legs, wheels ±30 rad/s** | **19.771** | **98.80%** | **0.95438** | **0.96561** |
| Symmetric hip ±0.6-rad offset, wheels ±30 | 19.761 | 98.56% | 0.95369 | 0.96476 |
| Hip targets ±0.75 rad, wheels ±30 | 19.723 | 98.56% | 0.95238 | 0.96329 |

The chosen case (`asym_soft_w6`) keeps leg targets inside measured soft position limits. Expanding hips toward the hard limit gave no observed benefit. Differences among wheel-30 variants are small and do not establish a uniquely optimal range. The selected cap still causes 5 falls out of 416 trials. Paired, profile-stratified bootstrap (10000 resamples) estimates mean survival change −0.229 s, 95% CI [−0.415, −0.046], and XY tracking change −0.0102, CI [−0.0199, −0.0019], relative to uncapped PPO. It is a practical bounded approximation, not identical PPO behavior.

## Applied FlashSAC mapping

The actor, critic action input and replay retain normalized `u ∈ [-1,1]`. Only the adapter converts to native actions:

`a_native = u * (positive_gain if u >= 0 else negative_gain)`.

Native order: left hip, shoulder, knee, wheel; right hip, shoulder, knee, wheel.

Negative gains: `(3.2, 2.0, 2.8, 6.0, 3.2, 2.0, 2.8, 6.0)`.

Positive gains: `(2.4, 2.0, 2.8, 6.0, 2.4, 2.0, 2.8, 6.0)`.

| Joint | Existing native scale | Offset/velocity range | Absolute target range |
|---|---:|---:|---:|
| Hip | 0.25 rad | −0.8 / +0.6 rad | −0.7 to +0.7 rad |
| Shoulder | 0.25 rad | ±0.5 rad | +0.3 to +1.3 rad |
| Knee | 0.25 rad | ±0.7 rad | −2.2 to −0.8 rad |
| Wheel | 5 rad/s | ±30 rad/s | ±30 rad/s |

Zero continues to request the default pose. Native action order/scales, reward definitions, command ranges and actuator settings are retained. Last-action observations and action rewards see mapped native actions, which is consistent with the native PPO environment. The asymmetric sign mapping is deterministic environment dynamics; SAC density/entropy remain in normalized coordinates.

The measured soft hip bounds are ±0.706858 rad; knee upper bound is −0.796743 rad. Targets fit these bounds, but actual physical trajectories may overshoot targets. Also, `DelayedPDActuatorCfg.velocity_limit=30` does not impose a 30-rad/s hard PhysX ceiling: the measured articulation velocity limits are approximately 15 rad/s for legs and 50 rad/s for wheels. Uncapped PPO wheel speeds reached 45.824/39.127 rad/s. The selected wheel **target** bound is 30; it is not a guarantee that measured wheel velocity stays below 30.

Checkpoint metadata, run parameters and W&B record the resolved mapping. Playback/resume restore saved gains; legacy FlashSAC checkpoints restore their original unit gains. A fresh learner is required for the changed mapping because the old replay/critic learned different physical consequences for the same normalized actions. Noise cadence (1–16 steps), temperature, architecture and other learner hyperparameters stay at the original defaults for this experiment. Larger gains also increase physical exploration at the same normalized noise.

## Evidence and implementation

- Distribution: `tita_ppo_action_distribution_164207.json`, three NPZ files.
- Candidates and native results: `tita_ppo_action_range_candidates.json`, `tita_ppo_action_caps_165307.json`, fourteen NPZ files.
- Analysis: `tita_ppo_action_range_selection_analysis.json`, produced by `test/analyze_tita_ppo_action_ranges.py`.
- Production changes: `agents/flash_sac_cfg.py`, FlashSAC `env_adapter.py`, `runtime.py`, `train.py`, `play.py` and `README.md`.
- Tests: `test/test_flash_sac_action_ranges.py`; existing entrypoint test expectation updated to compare mapped native actions.
- Executed CPU regression suite: `python -m unittest discover -s test -p 'test_flash_sac*.py' -v`, **38 tests PASS**; log `tita_flash_sac_action_ranges_tests.log`.
- Native integration and required repository checks are recorded in the accompanying new-training launch report.

These measurements select a usable action range. They do not establish that a newly trained FlashSAC policy will converge faster; the new run is the required follow-up evidence.
