# High-Level BC/PPO Gate-0

## Evidence metadata

- Execution domains: `DESKTOP_DRY_RUN`, `TRAINING_SIM`, `VALIDATION_SIM`
- Overall evidence status: `FAIL`
- Physical robot execution: `NOT_TESTED`
- Branch: `agent/codex/dev_tita_gluon`
- Training seed: `20260813`
- Deterministic selection seed: `20260831`
- Frozen low-level checkpoint SHA256:
  `9d8d1fad8f0e2c3e04eb9d937ca91706174ea8b97c21501eb6b2744defc8acde`
- Selected high-level checkpoint SHA256:
  `3d13ec69f9832b49850e36133bfa7415eca377d699bc5c7685b9fc92df563767`
- W&B run:
  <https://wandb.ai/bjy6614-postech/tita-gluon-highlevel/runs/ckft33nw>

This remains a position-only coordination Gate. Self-collision and CBF were
disabled, so none of the results provide collision-safety evidence.

## From-scratch deterministic selection

The phase-conditioned binary `WAIT/TRIGGER` checkpoints 25, 50, 75, and 100
were evaluated deterministically with eight environments. All four failed:
success rates were 0%, with mean completed-target counts of 0.0, 0.5, 1.0,
and 0.5 respectively. This closes the previously blocked selection audit.

## Scheduler behavior-cloning result

The full 64-environment scheduler dataset contained 24,768 samples: 24,320
`WAIT` and 448 `TRIGGER`. After 20 BC epochs, teacher success was 64/64,
trigger recall was 1.0, classification accuracy was 0.99015, and continuous
action MSE was 0.002991.

Deterministic `model_bc.pt` evaluation achieved 8/8 success, 38.625 s mean
cycle time, 0.9071 concurrent-motion ratio, and zero local abort, emergency
hold, or low-level failure. It was stable but 0.795 s slower than the frozen
37.830 s classical scheduler.

## PPO stability probes

BC followed by ordinary PPO with exploration standard deviation 0.5 destroyed
the policy. Reducing it to 0.1 did not fix the update instability: `model_0`
completed 0/8 and timed out after two targets, while `model_25` produced 8/8
local aborts.

An optional BC-state policy anchor was added to PPO. It distills the frozen BC
actor's continuous mean and categorical distribution. The hybrid actor also
uses 0.1 times the critic learning rate (`3e-5` versus `3e-4`). Both features
default to disabled for other PPO users.

The one-update probe with anchor coefficient 10 achieved 8/8 success, 37.850 s
mean cycle time, 0.90555 overlap, 4.0 completed targets, and zero local abort,
emergency hold, or low-level failure. It is 0.020 s slower than the scheduler,
so it is stable but does not pass the strict timing Gate.

## Bounded 25-iteration selection

| checkpoint | SHA256 | success | successful cycle time | overlap |
|---|---|---:|---:|---:|
| model 0 | `3d13ec69...563767` | 8/8 | 37.850 s | 0.90555 |
| model 5 | `32d66a19...d15035` | 6/8 | 39.350 s | 0.80213 |
| model 24 | `cef52e98...51dda0` | 7/8 | 38.714 s | 0.81288 |

Later PPO updates did not improve the policy. Gate-0 remains `FAIL`; held-out
evaluation and CBF implementation remain blocked. Model 0 is retained only as
the selected diagnostic checkpoint.

## Test evidence

- IsaacLab-Python syntax compilation: `PASS`.
- IsaacLab-Python unit tests: `PASS`, 15/15.
- Four-environment BC/anchor training smoke: `PASS`.
- Deterministic selection JSON files: recorded in this directory.
- `./scripts/agent-check.sh`: `PASS` (401 Python syntax checks, 13 URDF XML
  parses, diff integrity, and experiment-log checks).

## Next decision

Do not extend this run blindly. The 20 ms gap is below the practical resolution
of one eight-layout batch. Repeat model 0 and the classical scheduler over
multiple fixed seeds with confidence intervals. Only then decide whether to
try slower anchor decay or critic warm-up. CBF work remains out of scope until
the coordination Gate is explicitly accepted.
