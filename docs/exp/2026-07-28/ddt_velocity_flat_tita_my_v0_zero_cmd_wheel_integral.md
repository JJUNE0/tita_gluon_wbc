# DDT-Velocity-Flat-Tita-My-v0 — `zero_command_wheel_action` → integral penalty (My45)

## Change

`zero_command_wheel_action_penalty` (per-step `|wheel_action|**4` quartic, `mdp/rewards.py`)
replaced with `ZeroCommandWheelActionIntegralPenalty` (`ManagerTermBase`):

- Accumulates the same per-step quartic term over time, like the I term of a
  PID controller, for as long as the velocity command stays in the zero-band.
- Integral resets to 0 on episode reset **and** as soon as the command leaves
  the zero-band (same convention as `ZeroCommandPositionDrift`'s anchor) —
  each zero-command hold starts its own fresh integration window.
- Returned reward is `integral_error ** integral_exponent` with
  `integral_exponent=0.5` (sqrt) — a concave kernel that penalizes a small
  nonzero integral disproportionately more than a large one (opposite shape
  of the `exponent=4` on the raw per-step term), to drive the accumulated
  error toward exactly 0 rather than tolerate a small persistent bias.

Params in `my_flat_env_cfg.py`: `exponent=4.0`, `integral_exponent=0.5`,
`command_threshold=0.0`, weight `-0.1` (unchanged from My44).

## Training

- **Execution domain**: `TRAINING_SIM`
- **Task**: `DDT-Velocity-Flat-Tita-My-v0` (rsl_rl track, `ActorCriticWithEstimator`)
- **Command**: `scripts/rsl_rl/train.py --task DDT-Velocity-Flat-Tita-My-v0 --max_iterations 3000 --headless`
- **Run dir**: `lab/ddt_lab/logs/rsl_rl/tita_flat_rslrl_estimator/2026-07-28_11-44-51`
- **Log**: `test/train_logs/train_my_zero_cmd_wheel_integral_20260728_114444.log`
- Completed cleanly: `Learning iteration 2999/3000`, checkpoint saved, process exited normally.
- Final-iteration episode stats: `time_out` 0.9963, `base_contact` 0.0037 (stable), `Episode_Reward/zero_command_wheel_action` -0.2138, `Episode_Reward/zero_command_position_drift` 0.1553.
- **Evidence status**: PASS

## Validation — Isaac-native zero-command drift probe (`eval_behavior.py`)

- **Execution domain**: `VALIDATION_SIM`
- **Command**: `scripts/rsl_rl/eval_behavior.py --task=DDT-Velocity-Flat-Tita-My-Play-v0 --checkpoint <model_N.pt> --num_envs 8 --out test/eval_logs/eval_my_zc_wheel_integral_<N>.csv --headless`
- Ran across 5 saved checkpoints, `zero_hold` phase (3s), 8-env average:

| ckpt | drift_x (3s) | mean\|wheel_action\| | max\|wheel_action\| | tilt_end | decel ang_vel_end |
|---|---|---|---|---|---|
| 1500 | +0.0005 | 0.1146 | 0.4153 | 0.132 | 0.212 |
| 2000 | -0.0087 | 0.0860 | 0.3072 | 0.121 | 0.149 |
| **2500** | **-0.0088** | **0.0446** | **0.191** | 0.138 | 0.172 |
| 2900 | -0.0134 | 0.1060 | 0.6261 | 0.165 | 0.139 |
| 2999 (final) | +0.0337 | 0.0865 | 0.4156 | 0.168 | 0.246 |

- Checkpoint 2500 is best on both drift magnitude and `mean|wheel_action|`
  (the metric this reward directly targets) — the final checkpoint (2999) is
  not the best, consistent with prior rounds (My43/My44) where the
  highest-iteration or highest-`Train/mean_reward` checkpoint was not the
  best on zero-command behavior.
- Vs. My44@2500 (quartic-only, same weight): Isaac drift **+0.153 m/3s → -0.0088 m/3s**.
- **Evidence status**: PASS

## Validation — MuJoCo sim-to-sim drift probe

- **Execution domain**: `VALIDATION_SIM`
- **Policy checkpoint**: `model_2500.pt`, SHA256 `a078b2e1835566c1d6333c447a8fee3d1318c57cdae61ba82d26e2770283b163`
- **Exported ONNX**: `tita_gluon_ws/deploy/tita/policy_my45_2500.onnx`, SHA256 `3be0b6b4e2dbeffc81f7b4f4a3ef82a0700b9124be2014aee0853e940520123f`
- **Cosim config**: `sim2sim/cosim_ros2_jazzy/config/tita_my45_2500.yaml`
- **Command**: `python3 cosim_ros2_jazzy/scripts/probe_zero_command_drift_mujoco.py --config cosim_ros2_jazzy/config/tita_my45_2500.yaml --settle_s 1.0 --hold_s 5.0` (env: `~/venvs/cosim_ros2_jazzy` + ROS 2 Jazzy + `sim2sim/install/setup.bash`)
- **Log**: `test/eval_logs/mujoco_drift_my45_2500.log`

Result (5.0s zero-command hold):

- Planar `|xy|` drift = **0.0634 m** (mean vx-equiv 0.0127 m/s)
- Base height: start 0.3875 → min 0.3825 → final 0.3825 m (~5mm dip, stable)
- `joint_left_leg_4` (wheel) delta -4.50 rad vs `joint_right_leg_4` delta -1.16 rad over the hold — asymmetric residual wheel spin, likely the direct cause of the lateral/forward drift direction.

Comparison across all rounds (5.0s MuJoCo hold, same probe/params):

| checkpoint | drift (5.0s) |
|---|---|
| My41@5800 | 0.445 m |
| My42@1800 | 0.349 m |
| My43@2700 | **0.022 m** (best overall) |
| My44@2500 (quartic-only) | 0.181 m |
| **My45@2500 (integral)** | **0.0634 m** |

My45 recovers most of the My44 regression (~2.9x better than My44) and beats
My41/My42, but does not reach My43@2700's 0.022 m. The integral reward change
is a clear net improvement over the quartic-only My44 baseline it directly
replaces, but has not yet matched the best checkpoint found so far (My43).

- **Evidence status**: PASS

## Files changed

- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/mdp/rewards.py` — `ZeroCommandWheelActionIntegralPenalty` class
- `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py` — reward term registration
- `sim2sim/cosim_ros2_jazzy/config/tita_my45_2500.yaml` — new cosim config
- `tita_gluon_ws/deploy/tita/policy_my45_2500.onnx` — exported policy

## Unresolved risks / next steps

- Not root-caused why My43@2700 still outperforms My45@2500 on MuJoCo drift — integral reward helps but is not sufficient on its own; the asymmetric left/right wheel-4 spin suggests a policy-level imbalance not directly penalized by this term (it sums both wheels together).
- Only Isaac-side checkpoint selection (2500) was validated in MuJoCo; other checkpoints (2000, 2900) were not cross-checked in MuJoCo and might rank differently there.
- No sim-to-real (`ROBOT_READ_ONLY`/staged sim-to-real) validation performed — deployment requires separate operator approval per `AGENTS.md` §3.
