# TITA+GLUON Teacher init-0.39 reference-parity training

- Execution Domain: `TRAINING_SIM`
- Evidence Status: `PASS` for command-contract validation and bounded smoke;
  `FAIL` for the 10,000-iteration run, which terminated at iteration 708;
  policy quality is `NOT_TESTED`
- Initial Checkpoint: `model_0.pt`
- Initial Checkpoint SHA256:
  `6b5a37653587025eccdcd6ceda851d43b284357b2e627bc52fb08344852e5a76`
- Environment YAML SHA256:
  `e38eb57a7d4d50b8e6b7f3e4df34160b94d89b89973f4dd073170795910d8ce2`
- Agent YAML SHA256:
  `16e06d06ac9851875e169a53c1184e9c53032cd7e013c58888b508257eafb652`
- Physical robot commands: none

## Objective

Train a new RMA Teacher for the combined TITA+GLUON articulation with a
deterministic reset-height contract and the saved arm-free reference run's
standing exposure and ADD mixture:

```text
0.0 <= t <= 5.0 s: velocity = 0, effective height = 0.39 m
5.0 <  t <  6.0 s: effective height blends from 0.39 m to sampled height
6.0 <= t:           existing sampled-height curriculum
```

Both actor command observation and height-aware reward terms consume the same
effective value returned by `CommandManager.get_command()`.

## Configuration

- Task:
  `Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-RMATeacher-TargetHeight-v0-moo-ppo`
- Environments: 4096
- Iterations: 10,000
- Seed: 42
- Algorithm: MOO-PPO RMA Teacher
- Device: `cuda:0`
- W&B project: `tita-gluon-moo-teacher`
- W&B run ID: `103r08gf`
- W&B run: <https://wandb.ai/bjy6614-postech/tita-gluon-moo-teacher/runs/103r08gf>
- Init phase: 5.0 s at 0.39 m
- Height transition: 1.0 s
- Explicit standing environments: 0.20
- ADD `w_disc / w_fm`: 0.5 / 0.5
- Height curriculum after init/transition: unchanged, initially 0.32--0.38 m
  and widened to 0.25--0.45 m
- GLUON curriculum: unchanged, fixed WORK first and expanded after rollout
  step 120,000

Run directory:

```text
/home/cocel/Desktop/Research/tita_gluon_wbc/lab/logs/co_rl/
Tita_Gluon_CurriculumArm_RMATeacher-v0-mooppo/mooppo/
2026-08-10_12-36-22_phase_init039_ramp1_refparity_v1
```

Console log:

```text
test/train_logs/tita_gluon_teacher_init039_ramp1_refparity_v1.log
```

Launch PID: `2181202`

Last saved checkpoint: `model_700.pt`

Last saved checkpoint SHA256:
`9fb414ddc2863072961d89c31c67ba56a9c37838e422261357e00911e3d94a3f`

## Validation evidence

### Command-contract test

`test/test_tita_gluon_init_height_command.py` instantiated the combined Isaac
environment and directly checked command, observation encoding, and reward
target at four timestamps:

| Time | Sampled height | Effective height | Velocity command |
|---:|---:|---:|---:|
| 0.0 s | 0.32 m | 0.39 m | zero |
| 5.0 s | 0.32 m | 0.39 m | zero |
| 5.5 s | 0.32 m | 0.355 m | sampled |
| 6.0 s | 0.32 m | 0.32 m | sampled |

Result: `PASS`.

### Bounded training smoke

A 4-environment, one-iteration TensorBoard smoke run completed with exit code
zero. It exercised environment construction, RMA Teacher initialization,
rollout collection, MOO reward update, and checkpoint/log shutdown.

Result: `PASS`.

### Long-run execution

The 4096-environment process completed 708 iterations and saved
`model_700.pt`. At iteration 708 the console still reported finite metrics:
mean reward 77.98, mean episode length 982.4, base-contact termination 0.0392,
and timeout 0.9608. It then terminated with Tk/Tkinter thread teardown errors,
including `RuntimeError: main thread is not in main loop` and
`Tcl_AsyncDelete: async handler deleted by wrong thread`.

Result: `FAIL` for the requested 10,000-iteration run. The failure occurred
after normal-looking training metrics and is currently attributed to a
visualization/Tk lifecycle path, not to CUDA OOM or a reported non-finite
policy value. That attribution remains `SUSPICIOUS` until reproduced.

## Observed early behavior and risks

- The randomly initialized policy had base-contact termination near 1.0 by
  iterations 5--6. This is early-training behavior, not evidence of failure or
  eventual recovery. Policy quality remains `NOT_TESTED` until later
  checkpoints are evaluated with the fixed zero-command stance protocol.
- W&B reported one out-of-order step-0 warning. Training continued and the run
  is syncing, but some step-0 metrics may be omitted from the online chart.
- The active user MuJoCo sim2sim process was left untouched. It consumes a
  small amount of the same GPU and may reduce training throughput.
- This run changes init height, standing exposure, and ADD mixture together.
  It is a reference-parity corrective run, not a single-variable causal
  ablation of the previously observed wide stance.
- No collision-safety guarantee or physical deployment is implied.
- `model_700.pt` is an incomplete checkpoint and has not replaced the existing
  `model_9000.pt` evaluation baseline.
