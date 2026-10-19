# TITA parent MDP with staged GLUON curriculum

- Date: 2026-08-09
- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS` for configuration, physics/action smokes, and one-iteration runner integration
- Long-horizon policy quality: `NOT_TESTED`
- Sim-to-real / physical robot: `NOT_TESTED`
- Current task ID: `Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-RMATeacher-TargetHeight-v0-moo-ppo`

## Provenance

The TITA parent configuration was aligned to the saved v4 RMA Teacher run:

```text
/home/cocel/Desktop/Research/isaaclab_add_reward_autotuning/logs/co_rl/
Tita_Flat_Stand_Drive-v3-mooppo/mooppo/2026-08-08_16-12-19
```

- Parent checkpoint `model_9999.pt` SHA256:
  `df81ed501e6b3ebecb67a5819a79be43cd17122ba78bd021db8c392fcb882891`
- Parent environment YAML SHA256:
  `6444b2224c36c7b3a330a1674fc6679e6575366218ae45c07017074175fdaca7`
- Parent agent YAML SHA256:
  `a24049e122c969b5f4764b6f0bb5591172f5ba1e320d883945efc12307fe3860`

The workspace does not duplicate that environment.  The combined config
inherits `TitaFlatEnvCfg_GTBaseVel_TargetHeight` and only appends GLUON asset,
action, observation, reset, and curriculum behavior.

## Parent MDP behavior

- 24 rollout steps per environment
- 10,000 iterations
- RMA Teacher, latent dimension 16, policy stack count 1
- eight TITA policy actions
- commanded base-height range starts at `(0.32, 0.38)` m
- base-height range linearly widens to `(0.25, 0.45)` m over rollout steps
  24,000 to 120,000 (iterations 1,000 to 5,000)
- height normalization is centered at 0.35 m with half-range 0.10 m

## GLUON extension

The GLUON action remains zero-dimensional from the policy's perspective, so
the lower-level policy output remains the original eight TITA actions.  The
action manager applies a separate implicit-PD joint target to GLUON.

The curriculum uses the previously validated WORK-to-waypoint joint-space
rays:

- rollout steps 0 to 120,000: GLUON fixed at WORK
- rollout steps 120,000 to 204,000: workspace scale linearly expands 0 to 1
- after rollout step 204,000: complete conditioned waypoint envelope

At intermediate scale `s`, an endpoint is
`q_work + s * (q_waypoint - q_work)`.  Each excursion returns through WORK;
there are no unvalidated direct waypoint-to-waypoint transitions.  This is a
conditioned joint-space curriculum that expands the end-effector envelope. It
is not uniform Cartesian sampling; an IK-backed sampler can later replace the
trajectory backend while preserving the scalar curriculum interface.

## Evidence

### Curriculum action/physics smoke

```text
command:
/home/cocel/isaac/env_isaaclab/bin/python \
  test/test_tita_gluon_curriculum_arm_smoke.py \
  --headless --num-envs 4 --fixed-steps 50 --moving-steps 320

result: PASS (exit code 0)
actions: 8
policy: RMATeacher
policy stacks: 1
configured maximum iterations: 10000
fixed-stage command span: 0 rad
midpoint workspace scale: 0.5
full workspace scale: 1.0
minimum expanded command span across environments: 0.200000048 rad
parent final height range: (0.25, 0.45) m
```

### Existing task regressions

```text
fixed-WORK smoke: PASS (exit code 0)
maximum arm hold error: 0.0113830306 rad

conditioned RandomArm smoke: PASS (exit code 0)
minimum completed segments per environment: 1
maximum command span: 0.349999994 rad
maximum measured span: 0.356991649 rad
maximum command velocity: 0.250819325 rad/s
maximum command acceleration: 0.313520432 rad/s^2
maximum tracking error: 0.167289615 rad
conditioned-path residual: 1.33280039e-07 rad
offline sigma_min: 0.0168257051
offline minimum joint margin: 36.9595059 deg
```

### Runner-integrated one-iteration smoke

```text
working directory: lab
command:
/home/cocel/isaac/env_isaaclab/bin/python scripts/co_rl/train.py \
  --task Isaac-Velocity-Flat-Tita-Gluon-CurriculumArm-RMATeacher-TargetHeight-v0-moo-ppo \
  --algo mooppo --num_envs 4 --max_iterations 1 --headless \
  --logger tensorboard --run_name agent_smoke_curriculum_rma_parent

result: PASS (exit code 0)
rollout timesteps: 96
throughput: 24 steps/s
collection time: 3.598 s
learning time: 0.257 s
iteration time: 3.85 s
Curriculum/widen_height_range: 0.0000
Curriculum/widen_gluon_workspace: 0.0000
actor input/output: 108 / 8
critic input: 117
privileged encoder input/latent: 25 / 16
```

Generated smoke artifacts:

- `model_0.pt` SHA256:
  `32351830b8c3f1447faa9cf0a850ece68ecfadbf1560cc0a1f1f36f075a146df`
- `params/agent.yaml` SHA256:
  `546ebbf5aba296d06e2303882fde8872898146dc74bf9fab494f1e66379c7713`
- `params/env.yaml` SHA256:
  `ed31a8febe67239a9730945a965991979ff1b7501f0ea1c1347a8cba715214fd`

## Known risks

- Policy quality at 4,096 environments and 10,000 iterations is not tested by
  the bounded smoke.
- The GLUON envelope is sampled along conditioned joint-space rays rather than
  uniformly in Cartesian end-effector space.
- The combined URDF still emits importer warnings for massless auxiliary
  links and unresolved visual references (`ch201`, cameras, `spad`, `spad1`).
- No physical robot command or deployment was performed.
