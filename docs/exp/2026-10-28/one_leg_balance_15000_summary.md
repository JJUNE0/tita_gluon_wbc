# One-leg balance and torque assessment

- Execution Domain: VALIDATION_SIM; repository checks: DESKTOP_DRY_RUN.
- Policy: `mj_lab/logs/flash_sac/tita_mjlab_151340_019495/model_15000`.
- Policy Checkpoint SHA256 (`actor.pt`): `27754ff6f8ede3c16d7cfb4eb75f1e9098d666b03fcf563e1ffcdd63e7c96ddc`.
- Branch: `agent/codex/tita-walk`.
- Evidence Status: PASS for probe execution and short standing-only survival; FAIL for demonstrated single-leg support in this checkpoint; SUSPICIOUS for a strict vertical-support-leg feasibility claim; NOT_TESTED for dynamic single-leg balance of the searched poses or hardware.

## Observed policy behavior

Frozen inference used the saved environment, noise, startup/reset randomization, 32 environments, seed 42, and 8 seconds per case. The standing-only ablation overrides only gait settling time to prevent activation. No learner updates or training configuration changes occurred. Terminal states were captured before the FlashSAC wrapper resets environments.

| Metric | Gait held off | Saved gait, enabled after 2 s |
| --- | ---: | ---: |
| First episodes surviving all 8 s | 32/32 | 0/32 |
| Mean completed episode duration | None completed; all censored at 8 s | 2.4748 s |
| Episodes ending with knee contact | 0 | 96 |
| Episodes ending with base contact | 0 | 0 |
| Double contact fraction, excluding terminal frames | 99.953% | 99.748% |
| Supported lifts above 1 cm, either foot | 0 | 0 |
| Valid samples within requested single-support phases | 0 | 0 |

The first scheduled swing starts around 2.5 s. This checkpoint falls after mode activation, before reaching valid scheduled swing samples. This supports investigating the gait-mode transition before attributing failure to the physical impossibility of supporting the robot on one leg. It does not isolate which observation, action, or learned response causes that transition failure. Gait activation also changes gait-conditioned wheel odometry masking.

The standing-only result demonstrates useful learned standing, but this 8 s probe does not include the configured interval pushes at 10–15 s. A 100,000-step policy and long-duration robustness were not evaluated.

## Actual actuator torque during rollouts

The torque probe samples joint-space `qfrc_actuator` after every 5 ms physics step, including terminal steps. Near saturation means absolute torque at least 98% of the configured limit. Limits are 60 Nm per leg joint and 12 Nm per wheel.

| Joint | Left peak during enabled gait | Right peak during enabled gait | Limit |
| --- | ---: | ---: | ---: |
| Leg 1 | 36.76 Nm | 36.13 Nm | 60 Nm |
| Leg 2 | 20.45 Nm | 24.22 Nm | 60 Nm |
| Knee | 50.33 Nm | 57.55 Nm | 60 Nm |
| Wheel | 8.70 Nm | 12.00 Nm | 12 Nm |

During enabled-gait steps, none of the six leg joints had a near-saturated sample. The right wheel had a near-limit fraction of approximately 0.023%. Knees do briefly reach 60 Nm during startup across the full rollout; this does not coincide with persistent saturation during the gait-enabled failure segment. Measured lack of saturation does not establish that a different recovery trajectory would require no extra torque.

The current knee-output randomization multiplies PD stiffness/damping through `randomize_motors`; it does not lower the 60 Nm hard torque cap. Thus lower gains can reduce control authority for a given target error without making the hard cap smaller.

## Nominal static support search

The CPU MuJoCo search uses the task's corrected inertias, spherical wheels of radius 0.0925 m, ground contact geometry, joint limits, and a 4–6 cm swing-clearance preference. It searches joint positions and body roll/pitch while placing the support wheel on the ground. Required joint torque is computed as `g(q) - J_contact(q)^T F_ground`, with vertical ground force equal to total weight. Whole-robot COM projection and free-base residuals are checked; an arbitrary torque-feasible pose with unbalanced external moments is not treated as equilibrium.

With soft support-axis preference, the initial torque-only search found near-equilibrium examples with a support-axis tilt around 29.7 degrees and peak leg torque 20.1 Nm. Those examples alone do not enforce the policy's available position-target range.

A second search also constrains nominal PD equilibrium targets to saved action ranges using `q_target = q + tau / Kp`. This includes the saved per-joint action scales and FlashSAC gains, and nominal motor stiffness.

| Metric, soft-axis search with PD constraints | Left support | Right support |
| --- | ---: | ---: |
| Support leg axis tilt from world vertical | 32.77 deg | 32.67 deg |
| Swing wheel ground clearance | 6.003 cm | 4.897 cm |
| COM projection error from contact | 0.0364 mm | 0.0345 mm |
| Minimum base/knee ground clearance | 8.68 cm | 8.42 cm |
| Maximum required leg torque | 23.90 Nm | 23.96 Nm |
| Maximum torque / nominal leg limit | 39.83% | 39.94% |
| Maximum PD target-bound numerical violation | 0.00000792 rad | 0.00000814 rad |

The maximum free-base moment residual norm is below 0.01 Nm for these soft-axis candidates. The left example requires approximately 19.97 / 12.28 / 23.90 Nm in its support leg. This gives evidence that nominal motor torque alone does not prohibit one-wheel support. The numerical target-bound violations are below 1e-5 rad, but several joint positions or position targets are close to their limits; recovery margin is not established.

Stronger vertical-axis preference still returns tilted support axes and approximately 1.3 cm COM error in the PD-constrained search. These compromise poses are not valid equilibria. Finite local multi-start optimization cannot prove that a nearly vertical support leg is impossible, and the approximately 33-degree soft-axis candidates are not proof of the operator's exact desired pose style.

These are approximate static model calculations, with nominal gains, no parameter randomization, and self-collision disabled as in the task. They are not demonstrations of dynamic stability, a 0.5 s supported lift under the learned controller, or real motor continuous torque capability. No candidate was installed as a training target or sent to the robot.

## Changes and verification

Only two diagnostic helpers were added for this assessment:

- `test/evaluate_one_leg_balance.py`: frozen standing/gait comparison, contact/clearance/support measures, and physics-substep torque recording.
- `test/check_one_leg_static_feasibility.py`: nominal static pose/torque search with optional saved-action/PD target constraints.

Training remains on the existing run. All 14 saved training-source hashes and the actor hash match the frozen checkpoint metadata; see `one_leg_balance_source_verification.json`. Full flat warmup rewards were not introduced.

Executed evidence:

- PASS: frozen behavior probe, `one_leg_balance_15000.{json,npz,log}`.
- PASS: physics-substep torque probe, `one_leg_balance_torque_15000.{json,npz,log}`; same survival and lift results as the original probe.
- PASS: nominal static searches, `one_leg_static_feasibility.{json,log}` and `one_leg_static_feasibility_pd.{json,log}`. The preliminary lower-bound-only lift search is retained as `one_leg_static_feasibility_unbounded.{json,log}`; its large-lift poses were not used for the small-lift assessment.
- Repository check result is recorded in `one_leg_balance_agent_check.log`.

Interpretation: standing has improved, while single-leg support is not yet demonstrated. The available evidence favors examining COM placement, posture preparation, and the learned gait transition over increasing motor torque limits. Current training and reward configuration are preserved.
