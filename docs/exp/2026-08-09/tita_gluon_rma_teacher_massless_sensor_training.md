# TITA+GLUON massless-sensor RMA Teacher training

- Execution Domain: `TRAINING_SIM`
- Evidence Status: `PASS` for launch and continued iteration; policy quality is `NOT_TESTED`
- Policy Checkpoint SHA256: `f4dc79f842438c366ed4d0be9915d6e465f078689794fa033da4c6558cc7a94c` (`model_0.pt`)
- Task: `Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-RMATeacher-TargetHeight-v0-moo-ppo`
- Run: `2026-08-09_17-15-39_massless_sensor_rma_teacher_v2`
- Process PID at launch verification: `420933`

## Configuration

- Environments: 4096
- Iterations: 10,000
- Rollout length: 24 steps per environment
- Seed: 42
- Device: `cuda:0`
- Algorithm: MOO-PPO with RMA Teacher
- Logger: TensorBoard
- Sensor/frame phantom mass: removed using `merge_fixed_joints=True`
- Runtime robot mass before training: `30.958568572998 kg`
- Policy input/output: 108 / 8
- Critic input: 117
- Privileged encoder input/latent: 25 / 16

Run directory:

```text
/home/cocel/Desktop/Research/tita_gluon_wbc/lab/logs/co_rl/
Tita_Gluon_CurriculumArm_RMATeacher-v0-mooppo/mooppo/
2026-08-09_17-15-39_massless_sensor_rma_teacher_v2
```

Launch command (working directory `lab/`):

```bash
/home/cocel/isaac/env_isaaclab/bin/python scripts/co_rl/train.py \
  --task Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-RMATeacher-TargetHeight-v0-moo-ppo \
  --algo mooppo \
  --num_envs 4096 \
  --max_iterations 10000 \
  --seed 42 \
  --headless \
  --logger tensorboard \
  --run_name massless_sensor_rma_teacher_v2
```

## Launch evidence

Iteration 0 completed without a runtime or CUDA error:

- Throughput: 25,584 steps/s
- Total timesteps: 98,304
- Iteration time: 3.84 s
- Mean reward: 65.29
- Mean episode length: 23.70
- Height curriculum: 0.0
- GLUON workspace curriculum: 0.0 (expected fixed-arm initial stage)

The process continued through at least iteration 6 during launch monitoring,
reaching 688,128 total timesteps at approximately 34,541 steps/s.  Early-policy
termination and reward values are initialization behavior and are not evidence
of converged policy quality.

## Logging defect encountered and corrected

The first 4096-environment launch (`17-14-17_massless_sensor_rma_teacher`)
failed at iteration 0 because the RMA t-SNE helper called `wandb.log()` while
the selected logger was TensorBoard.  The runner now performs t-SNE logging
only when the logger is W&B and an initialized W&B run exists.  A bounded
4-environment, one-iteration regression passed before the long run was
restarted.

## Artifact hashes

- `model_0.pt`: `f4dc79f842438c366ed4d0be9915d6e465f078689794fa033da4c6558cc7a94c`
- `params/agent.yaml`: `59fb0aa5ac41a22c34e685b7fa6160a894ba9c3cbb01183d5528b34b43b95af8`
- `params/env.yaml`: `15bb062e43a8a78a70313ffbe5ff98a870ffab0f454a340f7a7da51b97b7a4d9`

## Remaining risks

- Long-horizon convergence and final locomotion quality are not yet known.
- Isaac Sim 5.1 warns that importer-side merging of fixed bodies with inertia
  is deprecated; the current dynamics are correct, but the URDF should later
  pre-combine fixed mount/base inertia and represent sensor poses as frames.
- No physical robot command or deployment was performed.
