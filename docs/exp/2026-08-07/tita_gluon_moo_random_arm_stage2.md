# TITA+GLUON CO-RL/MOO conditioned moving-arm stage 2

- Execution Domain: `TRAINING_SIM` (task configuration), `VALIDATION_SIM` (tests)
- Evidence Status: `PASS` for environment, dynamics, fixed-stage regression, and one-iteration runner integration; `SUSPICIOUS` for geometric coverage and existing importer warnings; policy quality `NOT_TESTED`
- Branch: `agent/codex/dev_tita_gluon`
- Robot hardware commands: none
- Combined URDF: `sim2sim/tita_gluon_urdf/urdf/tita_gluon_2L6_4L3.urdf`
- Combined URDF SHA256: `2db28c8a6a685c0a8238628ab697904193759549079782fbfeea8f7e015fded7`
- Smoke checkpoint: `lab/logs/co_rl/Tita_Gluon_RandomArm_Flat_Stand_Drive-v0-mooppo/mooppo/2026-08-07_18-00-14_agent_smoke_random_arm_stage2/model_0.pt`
- Policy checkpoint SHA256: `0064524476ab6ba270f10b51fac54a25e4eef0d51d1bf725849ad86f95f1fd70`
- ONNX hash: `N/A` (policy export was outside this stage-2 integration task)

## Implemented contract

- The validated low-level TITA policy remains eight-dimensional. The GLUON
  trajectory action term consumes zero policy actions, so the policy does not
  learn or directly command the arm in this stage.
- `gluon_joint_pos` and `gluon_joint_vel` remain the last two terms of the
  inherited CO-RL `stack_policy`; its dimension remains 44.
- Each simulated environment independently samples one of 12 conditioned
  GLUON joint-space waypoints. Motion always follows
  `WORK -> waypoint -> WORK`; unvalidated direct waypoint-to-waypoint edges are
  not used.
- Each segment uses a quintic smoothstep with zero velocity and acceleration at
  its endpoints. Nominal duration is sampled from 2.5--4.0 s and extended when
  needed to keep commanded speed at or below 20 deg/s and acceleration at or
  below 40 deg/s^2. Endpoint dwell is sampled from 0.25--0.75 s.
- Episode reset returns the arm command and physical reset state to WORK
  `[0.0, 0.8, 1.6, 0.8, 0.0, 0.0] rad`.
- The original fixed-WORK Gym environments and runner namespace remain
  registered. Moving-arm training uses its own environment IDs and experiment
  directory.

## Waypoint conditioning evidence

Every dense WORK-to-waypoint edge was rechecked at 33 samples with TITA at the
recorded stand posture `[0.0, 0.8, -1.5, 0.0, 0.0, 0.8, -1.5, 0.0] rad`.

```text
waypoints: 12
minimum translational Jacobian sigma_min: 0.0168257051
required sigma_min: 0.015
minimum standalone-URDF joint-limit margin: 36.9595059 deg
required joint-limit margin: 10 deg
Pinocchio/hpp-fcl clearance gate: 0.015 m
path model collision result: none
```

This is a `VALIDATION_SIM` conditioning gate, not a physical safety
certificate. The checker uses the available combined URDF geometry, one TITA
pose, and no future gripper/tool geometry.

## Validation evidence

### Batched integrated dynamics smoke

```text
command:
/home/cocel/isaac/env_isaaclab/bin/python \
  test/test_tita_gluon_random_arm_smoke.py \
  --headless --steps 320 --num-envs 4
result: PASS (exit code 0)
environments: 4
joints: 14
policy actions: 8
waypoints selected across final per-environment state: 4
minimum completed segments per environment: 1
maximum commanded joint span: 0.349999994 rad
maximum measured joint span: 0.356991649 rad
maximum command velocity: 0.250819325 rad/s
maximum command acceleration: 0.313520432 rad/s^2
maximum instantaneous tracking error: 0.167289615 rad
maximum conditioned-line residual: 1.33280039e-07 rad
observation dimensions: stack_policy=44, none_stack_policy=4,
  priv_extrio=2, priv_prio=3, priv_physical=20
```

The smoke executes the actual action-manager, articulation PD, physics, and
scene-update boundary. It verifies finite state, independent batched sampling,
movement in every environment, at least one completed segment, trajectory
limits, hub-path membership, action dimension, and exact observation order.

### Fixed-WORK regression

```text
command:
/home/cocel/isaac/env_isaaclab/bin/python \
  test/test_tita_gluon_moo_smoke.py --headless --steps 25
result: PASS (exit code 0)
joints: 14
policy actions: 8
observation dimensions: stack_policy=44, none_stack_policy=4,
  priv_extrio=2, priv_prio=3, priv_physical=20
```

The existing fixed-arm environment still constructs and holds WORK after the
new stage-2 environment was registered.

### Runner-integrated bounded training smoke

```text
command (working directory: lab):
/home/cocel/isaac/env_isaaclab/bin/python scripts/co_rl/train.py \
  --task Isaac-Velocity-Flat-Tita-Gluon-RandomArm-GTBaseVel-TargetHeight-v0-moo-ppo \
  --algo mooppo --num_envs 4 --max_iterations 1 --headless \
  --logger tensorboard --run_name agent_smoke_random_arm_stage2 \
  --experiment_description \
  'VALIDATION_SIM stage-2 moving-arm one-iteration smoke'
result: PASS (exit code 0)
learning iterations: 1
rollout timesteps: 96
throughput: 26 steps/s
collection time: 3.347 s
learning time: 0.245 s
iteration time: 3.59 s
actor input/output: 48 / 8
critic input: 73
checkpoint: model_0.pt (5,397,729 bytes)
```

The runner built actor, critic, and discriminator components, injected the MOO
dependencies, completed rollout and optimization, and wrote a checkpoint.
One random-policy iteration is integration evidence only. Its discriminator
loss and normalized delta are not evidence of training convergence.

## Diagnosed validation issue

The first moving-arm launch failed because the new action configuration was
not exported from the task `mdp` package. The export was added, after which the
batched dynamics and runner-integrated tests completed. Importing this IsaacLab
task with plain Python and no `SimulationApp` also fails on `pxr`; all recorded
runtime tests therefore use `AppLauncher`, as required by Isaac Sim.

## Remaining risks

- The 0.1673 rad maximum instantaneous simulated tracking error is below the
  current 0.20 rad smoke threshold but is large enough to monitor during longer
  locomotion runs. GLUON PD gains and trajectory rates remain provisional.
- Waypoint conditioning does not yet cover arbitrary TITA poses, terrain,
  external obstacles, attached gripper/tool geometry, cable routing, or real
  actuator limits. It must not be treated as real-robot collision avoidance.
- Isaac's importer still reports existing unresolved visual/mass warnings for
  TITA sensor links (`ch201`, cameras, `spad`, `spad1`). Execution completed,
  but this remains `SUSPICIOUS`.
- Long-horizon locomotion stability, reward convergence, learned behavior,
  policy export, sim-to-sim, and sim-to-real are `NOT_TESTED` in this stage.
