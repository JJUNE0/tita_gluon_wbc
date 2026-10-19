# TITA+GLUON RMA Teacher 10,000-Iteration Checkpoint Selection

- Training Execution Domain: `TRAINING_SIM`
- Evaluation Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS`
- Selected checkpoint: `model_9000.pt`
- Selected checkpoint SHA256: `6b540459bd8ad833e2822d1a3bcad8bdc87f556877a37fc066f39dfd463dfc3b`
- Training run: `2026-08-09_17-15-39_massless_sensor_rma_teacher_v2`
- Evaluation artifact: `tita_gluon_teacher_checkpoint_eval.json`

## Outcome

`model_9000.pt` is the best Teacher among the four evaluated checkpoints. It
completed the full evaluation without a base-contact termination, had the lowest
aggregate planar-velocity and yaw-rate RMSE, the lowest GLUON joint-tracking p99
error, the lowest tilt p99, and the lowest GLUON torque p99. `model_8500.pt` also
had no contact termination, but was worse than `model_9000.pt` on all of those
tracking and stability metrics.

`model_9500.pt` and `model_9999.pt` improved base-height RMSE but each incurred one
base-contact termination in `yaw_left_low`. Their tilt p99 values were also 90%
and 125% higher than `model_9000.pt`, respectively. Safety/survival was prioritized
before height-only accuracy, so neither later checkpoint was selected.

## Training Completion Evidence

The 4,096-environment RMA Teacher process exited normally after iteration 9,999,
which is the final iteration produced by a 10,000-iteration zero-based training
loop. The process PID was absent after exit and TensorBoard contained scalar step
9,999. The final checkpoint was therefore evaluated as the requested 10,000-step
candidate.

Final training scalar snapshot:

- GLUON workspace curriculum: `1.0`
- Mean reward: `61.1280`
- Mean episode length: `957.08 / 1000`
- Timeout termination fraction: `0.934336`
- Base-contact termination fraction: `0.065664`
- Base-height feature error: `0.123920`
- Yaw-rate feature error: `0.133323`

Checkpoint integrity:

| Requested iteration | File | SHA256 | Size (bytes) |
|---:|---|---|---:|
| 8,500 | `model_8500.pt` | `749967099e5f7fd82fb9458ca3945a56c8aeceb73ef9c07fba97238fb683ad50` | 6,549,509 |
| 9,000 | `model_9000.pt` | `6b540459bd8ad833e2822d1a3bcad8bdc87f556877a37fc066f39dfd463dfc3b` | 6,549,509 |
| 9,500 | `model_9500.pt` | `e2404448d4e4bc3bfb86f6e0f95afe066164eabecf412163b93016fb16e4449d` | 6,549,509 |
| 10,000 (final) | `model_9999.pt` | `269859355aaa8af672ff07abab30e598e4a57b527f5c73de5e2f72d55a567f54` | 6,549,509 |

## Fixed Evaluation Protocol

- Task: `Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-Play-v0-moo-ppo`
- Seed: `20260809`
- Environments: `256`
- Horizon: `1,000` policy steps, `20 s` per environment
- Exposure: `5,120 simulated environment-seconds` per checkpoint
- GLUON workspace scale: `1.0`
- GLUON completed trajectory segments: `1,259` for every checkpoint
- Height curriculum: disabled; fixed command heights `0.25`, `0.35`, `0.45 m`
- Motion commands: stand, `+0.75 m/s`, `-0.5 m/s`, `+1.5 rad/s`, `-1.5 rad/s`
- Scenario count: 15 motion/height combinations, assigned across every checkpoint

All checkpoints were loaded into the same environment configuration and evaluated
with the RMA Teacher privileged observation path. No physical robot command or
deployment was performed.

## Evaluation Results

Lower is better for every error, torque, tilt, and action-delta column.

| Checkpoint | Timeout fraction | Base contacts | XY RMSE (m/s) | Yaw RMSE (rad/s) | Height RMSE (m) | Arm p99 (rad) | TITA torque p99 (Nm) | Arm torque p99 (Nm) | Tilt p99 | Action delta p99 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `model_8500.pt` | 1.000000 | 0 | 0.044970 | 0.080602 | 0.011032 | 0.032891 | **33.9382** | 1.37010 | 0.076768 | 0.154291 |
| **`model_9000.pt`** | **1.000000** | **0** | **0.043028** | **0.074174** | 0.009401 | **0.032658** | 40.2514 | **1.27147** | **0.072520** | 0.146337 |
| `model_9500.pt` | 0.996094 | 1 | 0.049088 | 0.074460 | 0.007843 | 0.033721 | 37.9512 | 1.28829 | 0.138013 | **0.146336** |
| `model_9999.pt` | 0.996094 | 1 | 0.053556 | 0.080648 | **0.006797** | 0.033553 | 34.8232 | 1.34359 | 0.163497 | 0.147499 |

Relative to `model_8500.pt`, the selected `model_9000.pt` reduced XY RMSE by
4.32%, yaw RMSE by 7.98%, height RMSE by 14.78%, arm p99 error by 0.71%, tilt p99
by 5.53%, and action-delta p99 by 5.16%, while preserving zero contact failures.

Relative to the final checkpoint, `model_9000.pt` reduced XY RMSE by 19.66%, yaw
RMSE by 8.03%, arm p99 error by 2.67%, and tilt p99 by 55.65%. The tradeoff is a
38.33% larger height RMSE and a higher TITA torque p99 (`40.25 Nm` versus
`34.82 Nm`). The contact-free result and substantially better stability/tracking
were judged more important than the final checkpoint's `2.60 mm` height-RMSE
advantage.

## Harness Regression and Rerun

The first four-checkpoint run evaluated `model_8500.pt` but failed while resetting
for `model_9000.pt`. The evaluator had wrapped `env.step()` in
`torch.inference_mode()`, causing a lazily allocated MOO episode-statistics buffer
to become an inference tensor that could not be updated on the next reset.

The evaluator now uses `torch.no_grad()`: policy autograd remains disabled, while
simulator-owned tensors retain normal update semantics. Python compilation passed,
and the complete rerun crossed all three checkpoint-reset boundaries, evaluated
all four candidates, wrote the JSON artifact, and exited with code zero.

## Evidence Interpretation

- Training completion: `PASS`
- Four-checkpoint fixed-protocol evaluator execution: `PASS`
- `model_8500.pt`: `PASS`
- `model_9000.pt`: `PASS`, selected best Teacher
- `model_9500.pt`: `SUSPICIOUS` because of one `yaw_left_low` base contact
- `model_9999.pt`: `SUSPICIOUS` because of one `yaw_left_low` base contact and the
  highest tilt p99

The JSON top-level `PASS` denotes successful execution of the evaluation protocol;
it does not erase the candidate-quality warnings above.

## Unresolved Risks

- This is one deterministic seed on flat simulation. It is sufficient for a
  controlled checkpoint comparison, not a statistical robustness claim.
- Each checkpoint was tested for 20 seconds per environment. Longer evaluation,
  multiple seeds, terrain variation, pushes, and explicit dynamics sweeps remain
  necessary before policy export or staged Sim2Real.
- `model_9000.pt` has the highest TITA applied-torque p99 of the four candidates.
  Joint-specific torque limits and hardware-equivalent actuator saturation must be
  audited before deployment.
- The validation used the Teacher privileged observation path. It does not prove
  RMA Student performance or hardware observability.
- No real robot was enabled, commanded, or moved during this work.
