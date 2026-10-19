# Inspection-hub RMA Teacher from-scratch contract

- Execution Domain: `TRAINING_SIM` (interrupted run) and `VALIDATION_SIM` (smoke)
- Evidence Status: `FAIL` for 10,000-iteration completion due to a headless
  Tkinter cleanup crash; `SUSPICIOUS` for incomplete policy quality
- Policy Checkpoint SHA256 (`model_4000.pt`):
  `c8498627a74d20f1bccf3e432ede27717d6b6e893091409c7ce509cf8a97a278`
- Physical robot commands: none
- Task ID:
  `Isaac-Velocity-Flat-Tita-Gluon-InspectionCurriculumArm-RMATeacher-v0-moo-ppo`

## Training contract

The clean run does not load `model_9000.pt` or any other checkpoint. With 24
rollout steps per policy iteration, its 10,000 iterations are divided into:

| Rollout steps | Iterations | GLUON workspace | TITA height curriculum |
|---:|---:|---|---|
| 0--120,000 | 0--5,000 | fixed at WORK | inherited widening completes |
| 120,000--216,000 | 5,000--9,000 | linearly widens to four hubs | full range |
| 216,000--240,000 | 9,000--10,000 | complete four-hub envelope | full range |

Runner checks confirm `resume=False`, a separate experiment namespace, the
RMA Teacher policy contract, the existing eight-dimensional TITA action, and
`w_disc=w_fm=0.5` in both the ADD reward and domain-curriculum score.

## Evidence

Pure Python Go/No-Go contract:

```text
10 passed in 0.93s
```

Headless Isaac physics smoke:

```text
TITA_GLUON_INSPECTION_CURRICULUM_SMOKE,domain=VALIDATION_SIM,status=PASS,
envs=2,physics_steps=120,hub_node_ids=(23,111,18,208),workspace_scale=1,
height_range=(0.25,0.45),resume=0,
minimum_soft_limit_margin_rad=0.294682,actions=8
```

This smoke validates registration, curriculum boundaries, full-hub command
execution, finite joint state, and soft-limit margin. It does not establish
locomotion learning quality, collision safety, or superiority over the tuned
scheduler.

## Discarded misconfigured run

The first launch at `2026-08-10 18:45:13 KST` inherited
`w_disc/w_fm=0.2/0.8`. It was stopped at iteration 97 and must not be resumed
or used for evaluation. Its W&B run was `faithful-shape-2` (`ho47idxt`).

## Interrupted corrected training run

The corrected from-scratch run started at `2026-08-10 18:51:28 KST` with PID
`2740233` and is no longer running:

```text
/home/cocel/isaac/env_isaaclab/bin/python -u scripts/co_rl/train.py \
  --task Isaac-Velocity-Flat-Tita-Gluon-InspectionCurriculumArm-RMATeacher-v0-moo-ppo \
  --algo mooppo \
  --num_envs 4096 \
  --max_iterations 10000 \
  --w_disc 0.5 \
  --w_fm 0.5 \
  --logger wandb \
  --headless
```

Local run directory:
`lab/logs/co_rl/Tita_Gluon_InspectionCurriculumArm_RMATeacher-v0-mooppo/mooppo/2026-08-10_18-51-28_phase1-work-phase2-inspection-hubs`

W&B run: `revived-monkey-3`, id `fluxzxx6`,
`https://wandb.ai/bjy6614-postech/tita-gluon-moo-teacher/runs/fluxzxx6`.

The saved configuration was read back from disk and contains:

```text
agent.add_cfg.w_disc=0.5
agent.add_cfg.w_fm=0.5
env.domain.w_gail=0.5
env.domain.w_fm=0.5
resume=false
```

The run completed iteration 4034 but crashed before the next periodic save;
the latest recoverable checkpoint is `model_4000.pt`. The terminal error was
`Tcl_AsyncDelete: async handler deleted by the wrong thread`, preceded by
Tkinter object cleanup errors. There was no CUDA OOM or NaN evidence. The
runner imports Matplotlib and generates a W&B t-SNE figure every 100
iterations, which is the likely headless Tkinter source.

At checkpoint iteration 4000:

```text
mean_reward=106.84
mean_episode_length=942.26
termination_time_out=0.8737
termination_base_contact=0.1265
height_curriculum_scale=0.7501
gluon_workspace_scale=0.0
domain_level=0.5124
```

The checkpoint represents 40% of the requested run. It is still in the fixed
WORK-arm phase: the GLUON workspace curriculum starts at iteration 5000, so no
moving-arm training evidence exists yet. Do not treat `model_4000.pt` as the
final low-level policy. The original command intentionally contained no resume
or checkpoint arguments.
