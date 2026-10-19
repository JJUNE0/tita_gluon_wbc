# FlashSAC tracking-reward variability diagnosis

Execution Domain: TRAINING_SIM (existing run history); DESKTOP_DRY_RUN (offline statistics and plotting).

Evidence Status: SUSPICIOUS — large tracking-return fluctuations and short logged episode durations; no causal action/noise experiment performed.

Policy Checkpoint SHA256 (reference `model_25000/actor.pt`): `83284802694a8ffd8ec054c77e3f0b241dff9d34525cd1e15c033a57921fd7ff` (verified against checkpoint metadata). The history spans changing policies through step 27400, not one fixed checkpoint.

Branch: `agent/codex/dev_tita_gluon`.

## Data and access

Run `8v7zlqel`, W&B project `bjy6614-postech/tita_flat_flash_sac`. Both the user-provided Forge URL and the canonical W&B URL were inaccessible to the browsing tool. The analysis uses the identical metric dictionaries written by `train.py` to local JSONL and passed to `wandb_run.log`.

Frozen history: `tita_flash_sac_reward_variability_history.jsonl`, 274 observations from vector step 100 through 27400. Statistics: `tita_flash_sac_reward_variability_analysis.json`. Figure: `tita_flash_sac_reward_variability.png`.

## Verified logging semantics

- The local `track_lin_vel_xy_exp` function returns `exp(-||v_command_xy - v_base_xy||^2 / 0.25)` multiplied by an upright factor `clamp(-projected_gravity_z, 0, 0.7) / 0.7`. It depends on orientation as well as velocity error.
- Isaac Lab's reward manager accumulates `term_value * weight * control_dt`; the tracking weight is 2 and control dt is 0.02 s. On reset, it averages these episode sums over the reset batch and divides by the fixed maximum episode length of 20 s, rather than each episode's actual duration.
- FlashSAC logs `info['log']` only at each 100th vector step, without accumulating intervening reset-batch records. If there was no reset at that step, Isaac's extras can retain the latest reset record. In the inspected late window every sampled step had termination(s), so the tracking record reflects a batch of roughly 17–47 ended episodes (17–45 terminal episodes plus up to 2 timeouts), not all 4096 environments.
- The PPO runner collects these extras during its 24-step rollout and averages them before logging. Its plotting population and smoothing therefore differ from this FlashSAC logger.
- `episode_length_mean` uses a separate rolling buffer of 100 completed episodes. It is not the same population as the individual reset-batch tracking return; dividing one by the other would not produce a valid duration-normalized tracking metric.
- The command's `error_vel_xy` metric also accumulates errors using a fixed 8 s denominator. Its strong positive correlation with tracking returns is not evidence of improving or worsening instantaneous tracking and is affected by episode duration.

For a fixed average raw tracking reward of 0.8 and upright factor 1, a 2 s episode logs approximately 0.16, while a 4 s episode logs approximately 0.32, despite identical average tracking quality. Reset-batch duration and command/state composition can produce large fluctuations without an equivalent change in whole-scene instantaneous performance.

## Observations, steps 20100–27400

| Metric | Mean | Population std | Range |
| --- | ---: | ---: | ---: |
| Episode tracking return / 20 s | 0.235909 | 0.079663 | 0.074387–0.457537 |
| Total current-step reward over all environments | 0.039989 | 0.000923 | 0.037920–0.042177 |
| Categorical critic loss | 2.671474 | 0.017603 | 2.638704–2.716611 |
| Logged rolling episode length, steps | 151.656892 | 27.313101 | 96.21–227.26 |
| Actor differential entropy | -3.837947 | 0.245273 | -4.509330–-3.363186 |
| Temperature alpha | 0.001556 | 0.000065 | 0.001403–0.001696 |

The logged mean episode duration averages approximately 3.03 s, versus a 20 s limit. Stable aggregate reward and loss do not establish good locomotion or stable individual tracking. Actor entropy is near its configured differential-entropy target of -3.82545; a negative differential entropy is valid.

All logged scalar values in the frozen history are finite (PASS). The episode-tracking metric has a 0.88965 correlation with rolling episode length over the entire history, and a 0.6023 level / 0.6370 first-difference correlation in the late window. These describe association, not causality, and the two metrics use different episode populations.

## Action-structure hypotheses

- `tanh` and observation-dependent standard deviations are standard SAC policy components, present in the [OpenAI Spinning Up SAC implementation](https://raw.githubusercontent.com/openai/spinningup/master/spinup/algos/pytorch/sac/core.py). Their presence alone does not identify a numerical instability.
- FlashSAC's noise-repeat mechanism is a plausible balance-performance factor. The current truncated zeta distribution has exponent 2, support 1–16, and theoretical mean 2.1338 steps (42.68 ms), with a maximum 320 ms. Actions are still recalculated at every step; only the exploration noise is reused. No independent/repeated-noise or deterministic matched rollout was executed, so causal status is NOT_TESTED.
- With unchanged native action scales, the FlashSAC bound limits leg position deviations to ±0.25 rad and wheel velocity deviations to ±5 rad/s; the current PPO wrapper has no ±1 raw-action clamp. This changes control authority and is a plausible balance limitation, but no action-saturation statistics are currently logged.
- The PPO actor has a supervised base-velocity estimator; the FlashSAC actor consumes 33-dimensional proprioception without it. This also changes the comparison.
- There are no logged per-action mu/std, saturation fraction, upright distribution or whole-scene instantaneous tracking-error samples. Existing aggregate metrics cannot isolate these hypotheses.

The next useful measurements are whole-scene instantaneous tracking reward and velocity error, duration-normalized per-episode tracking quality, reset counts and durations accumulated across each logging interval, and per-action exploration/saturation statistics. A matched fixed-command rollout of one checkpoint with deterministic, independent-noise, and repeated-noise actions would separate noise's immediate balance effect. Establishing a training-convergence cause would additionally require controlled training comparisons, with other settings held fixed.

## Scope and validation

Only diagnostic artifacts under `docs/exp/2026-10-14/` were added: this report, frozen history, analysis JSON, plot and agent-check log. Training source, hyperparameters, rewards and the running process were not modified. No new native rollout, new training run, or hardware action was performed. The plot was rendered and visually inspected; scalar finiteness and the reference checkpoint hash were checked directly. The final agent-check result is recorded in `tita_flash_sac_reward_variability_agent_check.log`.

Unresolved: causal attribution, instantaneous tracking quality, and deterministic locomotion performance. This diagnosis does not claim the current policy is stable or the requested training is complete.
