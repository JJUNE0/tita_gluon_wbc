# Fixed-checkpoint action noise and bound analysis

Execution Domain: VALIDATION_SIM; DESKTOP_DRY_RUN for offline statistics and repository checks.

Evidence Status: PASS — all 6 conditions × 2 reset seeds completed with finite native metrics and identical paired initial measurements. This status describes experiment execution, not policy quality or retraining convergence.

Policy Checkpoint SHA256 (`model_30000/actor.pt`): `bb22d26c8da4d48a399b7020008cf295268474dcda51c37e5faff7dbcc297ded` (verified before evaluation).

Branch: `agent/codex/dev_tita_gluon`.

## Scope and controlled protocol

The user requested analysis of exploration noise and the restricted action range, excluding velocity-estimator differences. The saved actor and its 33 policy inputs are fixed in every condition. Joint scales (legs 0.25 rad/action, wheels 5 rad/s/action), actuator effort/velocity limits, PD parameters and delays are unchanged. Every applied action remains within [-1, 1]. No expanded action range is applied.

Probe harness: `test/eval_flash_sac_noise_bounds.py`. Native console evidence: `tita_flash_sac_noise_bounds_console.log`. All evaluation artifacts are stored alongside this report under `docs/exp/2026-10-14/`.

96 environments: 32 each with body-frame velocity target 0, +0.6, -0.6 m/s, with zero lateral/yaw targets and the saved command ramp. Two reset seeds (42, 43). Every condition uses the same scene's startup physical randomization and matched seeded initial root/joint state, policy inputs, and actuator gains. The harness checks initial equality to 1e-5. Per-step sensor corruption and random pushes are disabled identically across conditions, while the saved persistent biases and reset/physical randomization remain. The comparison therefore isolates action effects under controlled observation/command conditions, rather than reproducing the complete stochastic training distribution.

The primary observation is each environment's first episode, up to 20 seconds. Terminated state is captured before native automatic reset; subsequent episodes do not enter the metrics. This avoids differences in subsequent resets influencing survival comparisons. The first-episode survival time is restricted/censored at the common 20-second horizon.

Conditions:

1. Deterministic `tanh(mu)`, original bounds.
2. Independent Gaussian action noise at each step, original bounds.
3. Current FlashSAC repeated-noise rule, original bounds.
4. Deterministic actions with leg components capped at ±0.75; wheels unchanged.
5. Deterministic actions with wheel components capped at ±0.75; legs unchanged.
6. Deterministic actions with all components capped at ±0.5.

Independent and repeated noise consume identical candidate Gaussian/CDF streams from a private generator. Only reuse of candidates changes. The repeated-noise duration uses the checkpoint's zeta exponent 2 and support 1–16, matching the current rollout mechanism.

Measurements include time to first termination, survival at 5/20 seconds, actual instantaneous velocity error and upright-weighted tracking reward, action-noise/action-change RMS, per-joint sigma and fraction near the original ±1 bound, cap-affected fractions, computed-versus-applied torque clipping, and local tanh gain. Per-env and stepwise measurements are retained for matched comparisons; the reset-batch W&B episodic metric is not used.

Raw results: `tita_flash_sac_noise_bounds_142122.json`, 12 compressed per-env trajectory histories, and `tita_flash_sac_noise_bounds_142122_policy_samples.npz`. Policy samples contain mu, sigma and tanh outputs before the diagnostic cap. Aggregated statistics and comparison confidence intervals: `tita_flash_sac_noise_bounds_analysis.json`. Figure: `tita_flash_sac_noise_bounds_results.png` (rendered and visually inspected).

## Native results

192 paired first-episode trials per condition (64 per command), for 1152 total trials. The measured initial root/joint state, policy inputs and PD gain differences were exactly zero across all paired conditions. The checkpoint hash remained unchanged at completion. Every action and diagnostic metric was finite, and every applied action stayed within [-1, 1].

| Condition | Mean first-episode survival, censored at 20 s | 20 s reached without fall |
| --- | ---: | ---: |
| Deterministic, original bounds | 4.9108 s | 20.83% |
| Independent noise, original bounds | 4.2677 s | 15.10% |
| Repeated noise, original bounds | 2.6530 s | 7.29% |
| Deterministic, leg cap ±0.75 | 4.0675 s | 16.67% |
| Deterministic, wheel cap ±0.75 | 3.0155 s | 11.98% |
| Deterministic, all cap ±0.5 | 0.6523 s | 0.00% |

The bound-contraction rows all use deterministic actions, so their comparisons against the deterministic baseline isolate the cap change. Survival-at-20 excludes trials that terminated at the exact final step; merely logging life_steps=1000 is insufficient.

Paired differences use 10000 cluster bootstrap resamples, grouping the same physical environment ID across both reset seeds and stratifying within the 3 command groups. This accounts for shared startup physics across reset seeds. Intervals describe these trials, not all trained policies or training seeds.

The repeat duration is shared across the environment batch in the original implementation. These intervals are conditional on the two fixed noise-duration streams; resampling environment IDs does not estimate uncertainty across additional globally shared duration streams. The consistent direction in both seeds is useful evidence, but more noise seeds/checkpoints are needed for broader claims.

| Paired comparison | Mean survival change | 95% bootstrap interval |
| --- | ---: | ---: |
| Repeated minus independent noise | -1.6147 s | [-2.3269, -0.9678] s |
| Repeated minus deterministic | -2.2578 s | [-3.2010, -1.3717] s |
| Independent minus deterministic | -0.6431 s | [-1.4809, +0.1532] s |
| Leg cap 0.75 minus original cap | -0.8433 s | [-1.7613, +0.0455] s |
| Wheel cap 0.75 minus original cap | -1.8953 s | [-2.7051, -1.1557] s |
| All cap 0.5 minus original cap | -4.2585 s | [-5.3527, -3.2228] s |

Noise repetition shortened mean survival by about 37.8% versus independent noise and worsened results in both reset seeds. The independent-noise-versus-deterministic interval includes zero; these trials do not establish a reliable disadvantage from Gaussian exploration alone. Inference action-change RMS was actually smaller for repeated noise (0.4597) than independent noise (0.6039), although mean survival was worse. Thus smaller consecutive action changes did not imply better balance. Measured action-noise RMS was 0.3672 and 0.3542, respectively.

The fixed-horizon upright-weighted tracking integral (raw tracking accumulated until first failure, divided by 20 s, with zero after failure) was 0.1471 deterministic, 0.1335 independent noise and 0.0863 repeated noise. Conditional tracking/error averages over surviving time alone are subject to survival selection and should not be treated as direct task-score comparisons. The retained histories also support paired common-prefix comparisons of up to 2 seconds.

## Original-bound utilization

In deterministic original-bound rollouts, time-weighted fractions with absolute action ≥0.95 were 1.11% for leg components and 6.35% for wheel components. By command and reset seed, wheel fractions ranged approximately 3.49–9.38%. Per-trial-equal-weighted fractions are higher because short failed episodes often contain extreme actions; they describe a different population. Stable, longer trajectories did not continuously sit at the bound.

Time-weighted computed-versus-applied torque clipping was about 0.012% for legs and 0% for wheels in the deterministic baseline. This identifies policy target-range utilization separately from actuator torque clipping. It does not imply that every physical limitation has been ruled out.

The wheel-cap contraction consistently worsened survival. That establishes sensitivity to reducing the currently available wheel command range for this policy. Original-bound utilization and the pure-rolling calculation below support investigating high-command feasibility, but do not prove that expanding the current bound would improve this checkpoint.

## Interpretation limits

The native URDF (`tita_gluon_ws/src/ddt_ros2_control/urdfs/tita_description/urdf/robot.urdf`) specifies wheel collision-cylinder radius 0.0925 m. With wheel target `omega_target = 5 * action`, the original bound gives a maximum commanded wheel speed of 5 rad/s, or nominal rolling speed 0.4625 m/s. Under a fixed-leg, no-slip pure-rolling model, 0.6 m/s requires `action = 0.6 / (5 * 0.0925) = 1.2973`, and 1.0 m/s requires action 2.1622. Both exceed the saved SAC actor's bound. The underlying 30 rad/s actuator velocity limit does not expand this policy target range.

This is a kinematic target-range mismatch, not a proven hard limit on measured base speed: wheel tracking error, slip, external forces and leg/body motion can make actual speeds differ. It is direct evidence that the same `scale=5` with bounded SAC actions covers a different nominal wheel-command range from the currently unbounded PPO actor.

| Applied cap | Leg position deviation bound | Wheel target speed bound | Nominal wheel rolling target |
| --- | ---: | ---: | ---: |
| 1.0 | ±0.25 rad | ±5 rad/s | ±0.4625 m/s |
| 0.75 | ±0.1875 rad | ±3.75 rad/s | ±0.346875 m/s |
| 0.5 | ±0.125 rad | ±2.5 rad/s | ±0.23125 m/s |

Noise comparisons test this fixed policy's inference-time balance and tracking, not a noise setting's effect on learning convergence. Bound contraction can demonstrate sensitivity to available action range, and saturation data can identify candidate bottlenecks. They cannot establish that expanding the bound or changing joint scales would improve a policy trained with the original bound. No retraining, expanded-range experiment, hardware action, or live training configuration change is part of this task.

## Validation and changes

Added only `test/eval_flash_sac_noise_bounds.py` and the native/offline evidence under `docs/exp/2026-10-14/`. CLI help and Python compilation completed successfully before the native run. The native command exited 0 with PASS, all 12 conditions completed, and initial equality/action bounds/finite measurements/checkpoint hash were checked by the harness. No velocity-estimator difference was part of the comparisons.

Final source integrity and `./scripts/agent-check.sh` evidence are recorded in `tita_flash_sac_noise_bounds_source_check.log` and `tita_flash_sac_noise_bounds_agent_check.log`. The production-source baseline verifies unrelated code was retained. The new harness diff is preserved in `tita_flash_sac_noise_bounds_harness.diff`. No commit, push or publication was performed.

PASS: 505 existing source files unchanged; CLI help, harness compilation and the native comparison exited successfully. PASS: repository agent-check, including 436 Python syntax checks, 13 URDF parses, diff integrity and experiment-directory naming. No additional learner unit tests were needed because production learner/runtime/config source was unchanged.

The strongest next training comparison is a fresh run with `actor_noise_zeta_max=1`, preserving state-dependent sigma, tanh and the current action scaling. Current `train.py --resume` restores the saved agent hyperparameters, including the repetition setting, so editing runner defaults alone would not override it on resume. This recommendation follows fixed-policy inference evidence; improved training convergence is NOT_TESTED. Expanded wheel targets/scales are also NOT_TESTED. No running training settings were changed.
