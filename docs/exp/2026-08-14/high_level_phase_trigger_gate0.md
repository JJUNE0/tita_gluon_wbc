# High-Level Phase-Conditioned Trigger Gate-0

## Evidence metadata

- Execution domains: `DESKTOP_DRY_RUN`, `TRAINING_SIM`, `VALIDATION_SIM`
- Overall evidence status: `SUSPICIOUS`
- Deterministic validation status: `BLOCKED` (shared GPU resource contention)
- Physical robot execution: `NOT_TESTED`
- Branch: `agent/codex/dev_tita_gluon`
- Training seed: `20260813`
- Intended selection seed: `20260831`
- Frozen low-level checkpoint: `model_9000.pt`
- Frozen low-level SHA256:
  `9d8d1fad8f0e2c3e04eb9d937ca91706174ea8b97c21501eb6b2744defc8acde`
- W&B run:
  <https://wandb.ai/bjy6614-postech/tita-gluon-highlevel/runs/29q0ajiy>

This is still a position-only coordination Gate. Self-collision and CBF were
disabled, so this experiment provides no collision-safety evidence.

## Interface change

The four-way policy option was replaced with a binary categorical head:

```text
[vx, yaw_rate, WAIT/TRIGGER]
```

The executor retains its four-way FSM. `TRIGGER` resolves to the only valid
progress transition in the current phase: `PREPARE_NEXT` or
`EXECUTE_CURRENT`. The observation tail is now:

```text
[WAIT valid, TRIGGER valid, PREPARE phase, EXECUTE phase]
```

Invalid external trigger requests degrade to HOLD and are reported as rejected.
STOW remains a recovery primitive and is not policy-visible in this Gate.
Training logs include phase-specific trigger probability, sampled-trigger ratio,
greedy-trigger ratio, and sample count.

## Test evidence

- System-Python pytest: `BLOCKED`; that interpreter has no PyTorch.
- IsaacLab-Python unit tests: `PASS`, 14/14.
- Python syntax compilation of changed runtime/training/evaluator files: `PASS`.
- Four-environment Isaac training smoke: `PASS`, two PPO iterations,
  `model_0.pt` and `model_1.pt` saved.
- Smoke TensorBoard tags for all eight phase diagnostics: `PASS`.

## Training evidence

The from-scratch run used 64 environments, 10 Hz high-level control, 64 rollout
steps per environment, and W&B logging. It reached completed iteration 109.
The run was stopped at the already-saved `model_100.pt` boundary when an
unrelated process saturated the shared GPU; no other process was modified.

Saved checkpoints:

| checkpoint | SHA256 |
|---|---|
| model 25 | `ed3a3d80890c5c551c7f2486aea829f8ddc836848b66c66248f69bd3b86242ce` |
| model 50 | `18f240f8fa18709f9271ef64b787fb7875423a1ecd0802fa76cbacbac19cb731` |
| model 75 | `ea203c4f1116f70e9f048b508108a6934ce2ddbd91a67f7e941da95b1ce8a2c1` |
| model 100 | `92175c9f53f7cb77228011cf1c748b9668437cb7592f4670bec728591c8c4320` |

Observed stochastic episode batches were variable:

- peak success: 42.19% at iteration 54;
- peak mean target count: 2.6406/4 at iteration 54;
- latest batch at iteration 108: success 23.44%, mean targets 1.6562/4,
  local abort 76.56%, concurrent ratio 59.32%;
- no low-level fall was reported in the inspected episode summaries.

The binary head removed the irrelevant four-way competition, but did not by
itself eliminate credit-assignment instability. EXECUTE generally learned
faster than PREPARE. Importantly, iteration-100 on-policy diagnostics showed:

```text
PREPARE: P(TRIGGER)=0.6209, greedy trigger ratio=0.6667
EXECUTE: P(TRIGGER)=0.6661, greedy trigger ratio=0.7692
```

Therefore model 100 is a plausible deterministic candidate and must not be
declared failed from stochastic batch summaries alone.

## Validation attempt and decision

A four-environment, one-batch, 70-second deterministic evaluation of model 25
was started on selection seed 20260831. An unrelated forecasting process was
already saturating the GPU. The evaluator remained healthy but did not finish
after more than 22 minutes wall time, so only the evaluator was interrupted.
No result JSON was produced and no pass/fail claim is made from that attempt.

Gate-0 remains `SUSPICIOUS`, with deterministic selection `BLOCKED`. When the
GPU is free, evaluate model 100 first on the fixed selection seed. Only a
selection pass may advance to held-out layouts. If model 100 fails, screen
models 25/50/75, then consider behavior-cloning warm start as an explicitly
labeled ablation. Do not start CBF work on the strength of this run yet.
