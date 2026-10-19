# High-Level Hybrid PPO Gate-0

## Evidence metadata

- Execution domains: `TRAINING_SIM`, `VALIDATION_SIM`
- Evidence status: `FAIL`
- Physical robot execution: `NOT_TESTED`
- Branch: `agent/codex/dev_tita_gluon`
- Frozen low-level checkpoint: `model_9000.pt`
- Frozen low-level SHA256:
  `9d8d1fad8f0e2c3e04eb9d937ca91706174ea8b97c21501eb6b2744defc8acde`
- Final high-level diagnostic checkpoint: `model_224.pt`
- Final high-level SHA256:
  `de8d7568d260102a5201f083aed35d7d8ddee8faec6c2f3b88e9b03a326734a3`
- Training seed: `20260813`
- Selection-layout seed: `20260830`
- Held-out seed: intentionally unused because no selection candidate passed
- W&B project: `tita-gluon-highlevel`
- Completed continuation run:
  <https://wandb.ai/bjy6614-postech/tita-gluon-highlevel/runs/6pfmow1r>

This is a position-only coordination Gate. GLUON orientation, self-collision,
and CBF filtering were disabled, matching the frozen deterministic baselines.
No collision-safety claim follows from this experiment.

## Implemented contract

The upper policy observes current/next target geometry, base and GLUON state,
executor state/progress, previous base command, and the four-option action mask.
It outputs two Gaussian commands and one categorical option:

```text
[vx, yaw_rate, HOLD/STOW/PREPARE_NEXT/EXECUTE_CURRENT]
```

The frozen TITA RMA Teacher remains the eight-action low-level controller. The
environment owns persistent graph/local-servo execution. A single arm-local
emergency is isolated rather than discarding every vector rollout; a true
low-level fall still ends the synchronized batch.

Two correctness issues were found and fixed before the reported run:

1. the task-completion reward was a persistent boolean and could pay `+20` on
   every waiting step; it is now a one-step event pulse and records the actual
   per-environment completion time;
2. raw forward route progress rewarded driving past a station; the dense term
   now rewards reduction in distance to the active station.

The upper control rate was changed from 50 Hz to 10 Hz (`decimation=5`) and PPO
`gamma` from `0.99` to `0.995`. At 50 Hz the original discount half-life was
about 1.38 seconds, shorter than a 2--4 second graph option and unsuitable for
the approximately 38 second task.

## Tests and smoke evidence

- `python -m py_compile`: `PASS`
- `/home/cocel/isaac/env_isaaclab/bin/python -m pytest -q
  test/test_sequential_inspection_go_no_go.py`: `PASS`, 13/13
- reward-pulse smoke: `PASS`, 3 PPO iterations, exit 0
- isolated-arm-failure smoke: `PASS`, 3 PPO iterations, exit 0
- 10 Hz/station-reward smoke: `PASS`, 3 PPO iterations, exit 0
- inherited inspection-curriculum Isaac smoke: `PASS`, one environment, 20
  physics steps, minimum soft-limit margin `0.316065 rad`, exit 0
- `./scripts/agent-check.sh`: `PASS`; 401 Python syntax checks, 13 URDF XML
  parses, diff integrity, and experiment-directory checks passed

The first plain `pytest` call used system Python and was `BLOCKED` because that
interpreter has no PyTorch. It was rerun with the project IsaacLab interpreter
and passed; it is not a code failure.

An attempted combined pytest invocation also included the standalone Isaac
smoke script. Its own `AppLauncher` argparse rejected pytest's arguments, so
that invocation was `BLOCKED`; running the smoke through its intended CLI
subsequently passed.

## Training behavior

The 10 Hz run was trained from random high-level weights to iteration 150, then
continued from saved optimizer/model states through iteration 224. The final
continuation completed normally and produced `model_224.pt`.

Stochastic rollout batches did learn partial task behavior:

- best observed stochastic success rate: `0.6094` (39/64);
- target-count mean at that batch: `2.9688 / 4`;
- concurrent-motion ratio: `0.7771`;
- emergency-hold rate: `0.1562`;
- mean logged cycle time: `65.0719 s`.

The later batches regressed. The final recorded batch before checkpoint 224 had
zero success, target-count mean `1.0312`, and emergency-hold rate `0.0469`.
There were no reported low-level failures in these batch summaries. This large
variance shows that stochastic sampling could trigger useful arm transitions,
but it did not yield a reliable deterministic policy.

## Deterministic selection evaluation

All candidates used the same eight selection layouts and greedy categorical /
mean Gaussian inference.

| checkpoint | success | mean targets | overlap | local abort | result |
|---|---:|---:|---:|---:|---|
| model 75 | 0/8 | 0.25 | 0.0034 | 0 | `FAIL` |
| model 100 | 0/8 | 0.00 | 0.0000 | 0 | `FAIL` |
| model 150 | 0/8 | 0.00 | 0.0000 | 0 | `FAIL` |
| model 224 | 0/8 | 1.00 | 0.0279 | 0 | `FAIL` |

No candidate advanced to the held-out seed because selection success was zero.
The tuned classical scheduler remains the valid comparator: 8/8 success and
37.830 seconds mean successful cycle time.

The final model diagnostic recorded 5,600 deterministic action decisions:

```text
HOLD=5591, STOW=0, PREPARE_NEXT=1, EXECUTE_CURRENT=8
mean abs raw continuous action=[0.1229, 0.1732]
```

Thus the continuous base head was not identically zero. The direct failure is
categorical option collapse: the policy executes target zero once, then almost
always selects `HOLD` instead of preparing subsequent targets.

## Gate decision and next bounded experiment

Gate 0 is `FAIL`. The current PPO policy neither matches task success nor beats
the classical scheduler. It must not be used as evidence that upper RL improves
coordination, and work on the CBF should not be justified by this policy yet.

The next experiment should change only the option-learning interface:

1. retain the same frozen low-level policy, task, graph profile, targets,
   continuous base head, and baseline metrics;
2. replace the single four-way categorical competition with a phase-conditioned
   binary `WAIT/TRIGGER` decision, with the executor mapping `TRIGGER` to the
   only semantically admissible transition (`PREPARE_NEXT` or
   `EXECUTE_CURRENT`);
3. log per-phase option probabilities and greedy decisions during training;
4. train from scratch and require deterministic selection success before any
   held-out evaluation;
5. if that also fails, add a scripted-scheduler behavior-cloning warm start as
   a separately labeled ablation rather than silently mixing it into the
   from-scratch result.

This preserves the paper's timing question while removing irrelevant
`STOW/PREPARE/EXECUTE` competition at states where only one progress transition
is meaningful.
