# TITA+GLUON CO-RL/MOO fixed-WORK baseline

- Execution Domain: `TRAINING_SIM` (task configuration), `VALIDATION_SIM` (tests)
- Evidence Status: `PASS` for task/runner integration; `SUSPICIOUS` for the existing TITA sensor-link USD warnings
- Branch: `agent/codex/dev_tita_gluon`
- Robot hardware commands: none
- Combined URDF: `sim2sim/tita_gluon_urdf/urdf/tita_gluon_2L6_4L3.urdf`
- Combined URDF SHA256: `2db28c8a6a685c0a8238628ab697904193759549079782fbfeea8f7e015fded7`
- Smoke checkpoint: `lab/logs/co_rl/Tita_Gluon_Flat_Stand_Drive-v0-mooppo/mooppo/2026-08-07_15-07-42_agent_smoke_subset_reset/model_0.pt`
- Policy checkpoint SHA256: `383361fbd0e314c558f0a57f9599e38dbe10d54b69757765604c899355339ac5`
- ONNX hash: `N/A` (export was outside this environment-integration smoke)

## Implemented contract

- One floating-base articulation contains eight TITA joints and six mounted
  GLUON joints.
- The low-level policy action remains the validated eight-dimensional TITA
  action. A zero-dimensional action-manager term applies the GLUON WORK target
  `[0.0, 0.8, 1.6, 0.8, 0.0, 0.0] rad` every physics step.
- The combined asset uses the existing TITA delayed-PD actuator settings and
  the standalone GLUON `SIM_NOMINAL` implicit-PD settings.
- CO-RL observation groups remain `stack_policy`, `none_stack_policy`, and the
  sorted `priv_*` groups. The inherited TITA `stack_policy` order is unchanged;
  `gluon_joint_pos` and `gluon_joint_vel` are appended at its tail.
- Catch-all actuator gain/friction domain randomization was narrowed to the
  eight TITA joints. The two custom all-body startup inertia/COM terms are
  disabled because their current subset implementation returns a full-body
  tensor and shape-mismatches on the combined articulation. Base mass/COM and
  TITA actuator domain randomization remain active.

Exact `stack_policy` term order:

```text
hip_shoulder_joint_pos
leg_joint_pos
hip_shoulder_joint_vel
joint_vel
wheel_joint_vel
base_ang_vel
base_projected_gravity
actions
base_lin_vel_x
base_lin_vel_y
base_lin_vel_z
base_height
gluon_joint_pos
gluon_joint_vel
```

## Validation evidence

### Combined articulation/action smoke

```text
command: /home/cocel/isaac/env_isaaclab/bin/python \
  test/test_tita_gluon_moo_smoke.py --headless --steps 25
result: PASS (exit code 0)
joints: 14
policy actions: 8
group dimensions: stack_policy=44, none_stack_policy=4,
  priv_extrio=2, priv_prio=3, priv_physical=20
maximum GLUON WORK hold error after 100 physics steps: 0.0142874122 rad
stack_policy order: exact match with the contract above
```

This smoke drives the action-manager/physics/scene-update boundary directly.
It intentionally does not call the raw MOO reward path, because the CO-RL
runner owns discriminator and normalizer injection.

### Runner-integrated bounded training smoke

```text
command (working directory: lab):
/home/cocel/isaac/env_isaaclab/bin/python scripts/co_rl/train.py \
  --task Isaac-Velocity-Flat-Tita-Gluon-GTBaseVel-TargetHeight-v0-moo-ppo \
  --algo mooppo --num_envs 4 --max_iterations 1 --headless \
  --logger tensorboard --run_name agent_smoke_subset_reset \
  --experiment_description 'VALIDATION_SIM final one-iteration smoke'
result: PASS (exit code 0)
learning iterations: 1
rollout timesteps: 96
throughput: 33 steps/s
collection time: 2.670 s
learning time: 0.222 s
checkpoint: model_0.pt (5,397,729 bytes)
```

The runner constructed actor/critic/discriminator components, injected the MOO
learning components, completed rollout and optimization, and wrote the smoke
checkpoint.

## Diagnosed failures during validation

1. Running from repository root initially failed to resolve `scripts.co_rl`;
   the test now adds the repository `lab/` directory explicitly.
2. Restricting the existing custom startup inertia randomizer to TITA bodies
   failed with a `[23] -> [9]` assignment mismatch. The combined baseline now
   disables only the two incompatible all-body startup terms.
3. Calling `ManagerBasedMOORLEnv.step()` without a CO-RL runner failed with
   `MOORewardManager: Discriminator not set`, which is the expected imported
   runtime contract. The direct dynamics smoke stays below the reward boundary,
   while the bounded training smoke validates the full runner boundary.

## Remaining risks and next phase

- Isaac's URDF importer reports unresolved visual references and missing mass
  for the existing TITA sensor-only links (`ch201`, cameras, `spad`, `spad1`).
  Dynamics and training completed, but the importer noise remains
  `SUSPICIOUS` and should be removed in a later description cleanup.
- GLUON is fixed at one WORK target in this milestone. Collision-aware random
  arm trajectories, arm target observations, self/environment collision
  termination, and curriculum scheduling are not implemented yet.
- The GLUON gains are simulation baselines, not identified real-drive gains.
- This run proves integration and finite execution, not locomotion convergence
  or policy quality with the arm payload.
