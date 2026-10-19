# Inspection-hub RMA Teacher restart with t-SNE disabled

- Execution Domain: `TRAINING_SIM`
- Evidence Status: `PASS` for 10,000-iteration training completion;
  `NOT_TESTED` for checkpoint play/evaluation
- Policy Checkpoint SHA256 (`model_9999.pt`):
  `737b82442649d90a612e819a94180bcd57e55393b66d87eb80041afc40e838e9`
- Physical robot commands: none
- Task ID:
  `Isaac-Velocity-Flat-Tita-Gluon-InspectionCurriculumArm-RMATeacher-v0-moo-ppo`

## Run contract

This is a clean 10,000-iteration restart with 4,096 environments. It does not
load the interrupted `model_4000.pt`, because that checkpoint does not contain
the discriminator, MOO normalization, domain curriculum, or environment
curriculum state required for a faithful training resume.

The ADD reward and domain curriculum both use `w_disc=0.5` and `w_fm=0.5`.
Teacher-latent t-SNE logging is disabled, and the plotting dependencies are
loaded lazily only when that optional diagnostic is explicitly enabled.

## Pre-launch evidence

- Python compilation: `PASS`
- Sequential inspection Go/No-Go tests: `PASS` (`10 passed`)
- Headless Isaac physics smoke: `PASS`
- `./scripts/agent-check.sh`: `PASS`

```text
TITA_GLUON_INSPECTION_CURRICULUM_SMOKE,domain=VALIDATION_SIM,status=PASS,
envs=2,physics_steps=120,hub_node_ids=(23,111,18,208),workspace_scale=1,
height_range=(0.25,0.45),resume=0,teacher_tsne=0,
minimum_soft_limit_margin_rad=0.294682,actions=8
```

## Training run

The verified run started at `2026-08-11 09:47:10 KST`:

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

- Process PID: `4064084`
- Local run directory:
  `lab/logs/co_rl/Tita_Gluon_InspectionCurriculumArm_RMATeacher-v0-mooppo/mooppo/2026-08-11_09-47-10_phase1-work-phase2-inspection-hubs`
- W&B run: `winter-lake-4` (`xltfluki`)
- W&B URL:
  `https://wandb.ai/bjy6614-postech/tita-gluon-moo-teacher/runs/xltfluki`
- Console log: `docs/exp/2026-08-11/inspection_curriculum_tsne_disabled_restart.log`

The saved YAML configuration was read back from the run directory and confirms:

```text
agent.add_cfg.w_disc=0.5
agent.add_cfg.w_fm=0.5
env.domain.w_gail=0.5
env.domain.w_fm=0.5
agent.resume=false
agent.enable_teacher_tsne=false
env.scene.num_envs=4096
agent.max_iterations=10000
```

The process completed iteration `9999/10000` and exited. The final checkpoint
was written at `2026-08-11 17:34:42 KST`; no Tcl/Tk cleanup, traceback, CUDA
out-of-memory, or NaN failure was found in the console log.

Final training metrics at iteration 9999:

```text
mean_reward=101.29
mean_episode_length=986.59
height_curriculum_scale=1.0000
gluon_workspace_scale=1.0000
termination_time_out=0.9427
termination_base_contact=0.0573
domain_level=0.5337
total_timesteps=983040000
total_training_time_s=27858.15
```

These are rollout statistics, not an independent policy evaluation. A
headless or GUI play run is still required before claiming final policy
quality.
