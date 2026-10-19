# TITA+GLUON Collision-Free WBC Plan

## 1. Objective and evidence boundary

- Primary execution domains: `TRAINING_SIM`, `VALIDATION_SIM`
- Future execution domains: `DESKTOP_DRY_RUN`, `ROBOT_READ_ONLY`, staged
  `ROBOT_STATE_CHANGING` only after separate operator approval
- Current evidence status: `SUSPICIOUS`
- Physical deployment: `NOT_TESTED`

The objective is to build a modular collision-aware control stack for a GLUON
arm mounted on TITA while keeping the validated eight-action TITA locomotion
policy contract. The frozen low-level policy is task-agnostic but conditioned
on GLUON joint position and velocity. The upper planner commands TITA forward
velocity and yaw rate plus one persistent GLUON option. TITA height is fixed in
the first paper scope.

This plan deliberately does not enable PhysX articulation self-collision. A
large contact graph is too expensive and unstable for the intended batched RL
training. Collision safety instead comes from an explicit planning and command
filtering stack whose interventions can be measured and reproduced.

### 1.1 Locked first-paper scope and Go/No-Go question

The first paper is a four-pose sequential mobile visitation task motivated by
inspection. It does not include perception, contact, grasping, a height action,
or wheel-leg collision constraints in the claimed safety set.

```text
high-level action = [vx_cmd, yaw_rate_cmd, arm_option]
arm_option in {HOLD, STOW, PREPARE_NEXT, EXECUTE_CURRENT}
```

The policy option and executor state are separate. The executor owns:

```text
IDLE
GRAPH_EXECUTION
LOCAL_TARGET_SERVO
DWELL
EMERGENCY_HOLD
RECOVERY
```

Base commands may update at every high-level step. A new arm option is accepted
only when the executor is ready; graph edges and local-servo operations persist
until success, failure, timeout, or safety abort. Standard PPO remains usable
because this persistence and the categorical action mask are environment-side
contracts rather than a separate semi-MDP learning algorithm.

The immediate research gate is not the final CBF. It is:

> Can a high-level option policy reduce successful inspection cycle time on
> unseen layouts relative to a tuned classical concurrent scheduler while
> retaining the same final graph and safety layer?

Until that comparison passes in `VALIDATION_SIM`, the need for upper-level RL
is `NOT_TESTED`. The current desktop timing model is only a software-interface
sanity check.

## 2. Paper-derived design decisions

The local references are:

- `docs/paper/collison-free-mpc.pdf`
- `docs/paper/Humanoid Self-Collision Avoidanc using cb f.pdf`

The Collision-Free MPC paper represents the robot with a small set of
collision primitives and queries signed distances and closest-point Jacobians.
For collision pair `i`, it uses

```text
h_i(q) = d_i(q) - epsilon_i >= 0
```

as a relaxed barrier cost over an MPC horizon. This gives look-ahead behavior,
but the soft constraint is not a strict collision guarantee. Its benchmark
also shows that a simplified model with a fixed, directly queried pair list is
more optimizer-friendly than broad-phase nearest-body switching, whose gradient
direction can be discontinuous.

The CBF paper approximates humanoid geometry with spheres and capsules and
enforces selected signed-distance constraints in a whole-body QP. For a pair
`AB`,

```text
h_AB(q) = ||p_A - p_B|| - (rho_A + rho_B)
J_AB(q) = d h_AB / d q
```

and its acceleration-level exponential CBF is

```text
J_AB qdd + Jdot_AB qd
  + (alpha_1 + alpha_2) J_AB qd
  + alpha_1 alpha_2 h_AB >= 0.
```

That controller solves joint accelerations, torques, and contact forces with
full dynamics. The current TITA+GLUON environment does not expose that control
boundary: GLUON receives a position reference executed by implicit PD. The
acceleration-level humanoid QP therefore cannot be copied directly without
replacing the low-level control architecture.

The selected design is consequently layered:

1. Offline hpp-fcl path admission provides non-local path feasibility.
2. A small primitive-distance monitor covers the current full robot state.
3. A velocity-level CBF-QP filters GLUON IK or trajectory velocity before the
   existing position PD reference.
4. A relaxed barrier cost informs the future upper planner so it learns not to
   rely continuously on the reactive CBF shield.

## 3. Current baseline

The active combined task has these properties:

- TITA policy action dimension: 8
- GLUON policy action dimension: 0
- GLUON command: separate implicit-PD position target
- PhysX self-collision: disabled
- current locomotion-training trajectory set: 12 dense-checked
  `WORK <-> conditioned waypoint` rays
- current inspection graph: 256 dense-checked `WORK <-> hub` rays, from which
  four ordered task hubs are selected
- q6 in the large reachability artifact: fixed at zero
- current offline collision backend: Pinocchio 2.7.0 + hpp-fcl 2.4.4
- current large-map collision pair count: 51
- current inspection WORK-ray gate: 10 mm clearance, 10 degree joint margin,
  translational `sigma_min >= 0.015`, and at most 2 degree joint sampling

The existing large reachability artifact contains collision-free poses, not a
proof that arbitrary pairs of poses are connected by collision-free paths.
The only admitted online transitions are therefore stored graph edges.

The existing combined collision model is provisional because TITA collision
geometry is simplified or absent on some bodies, the mount jig has not been
measured, and no gripper/tool geometry or TCP offset is included.

## 4. Target runtime architecture

```text
upper task planner (hybrid PPO)
  |  TITA: vx, yaw_rate
  |  GLUON: HOLD / STOW / PREPARE_NEXT / EXECUTE_CURRENT
  v
option mask + persistent executor FSM
  v
offline mesh-validated base-relative graph -> selected hub
  v
online world-target transform + differential IK local servo
  v
tracking-error-aware discrete CBF-QP -> qd_safe
  v
qd_safe -> integrated q_ref
  v
existing GLUON joint-position PD
  v
actual q, qd, distance, intervention feedback
```

The TITA locomotion action stays at eight dimensions. The frozen policy receives
`vx`, zero lateral velocity, yaw rate, fixed height, measured `q_arm`, and
measured `qd_arm`. The high-level three-column action is consumed by a wrapper
above it and never silently appended to the low-level action vector.

Graph transition mode uses a fixed base-relative joint trajectory. Local target
servo mode does not regenerate a complete IK path each control step. It updates
the world target in the moving base frame and computes a differential command:

```text
T_B_target[k] = inverse(T_W_B[k]) * T_W_target
qd_nom[k] = pinv_damped(J_position+facing(q[k])) * K * e_EE[k]
```

This prevents IK branch switching and repeated hpp-fcl planning chatter while
the base moves. The graph transition and local servo are both filtered before
integration into the position reference.

The inspection task constrains Cartesian position and the link6 inspection
axis, not roll about that axis. The angular Jacobian is projected into the
target-axis tangent plane; inserting a zero roll command into a full 6D
Jacobian would incorrectly constrain roll and can force a non-local IK branch.

## 5. Offline collision-free graph

### 5.1 Node admission

Each candidate node shall record:

- GLUON joint vector
- link6/TCP Cartesian pose in TITA base coordinates
- joint-limit margin
- translational Jacobian minimum singular value
- minimum signed distance over the selected combined-model pairs
- q6/tool/orientation contract
- combined and standalone URDF hashes

Initial graph generation remains conservative:

- joint-limit margin: at least 10 degrees
- `sigma_min`: at least 0.015
- collision clearance: 10 mm in the current graph artifact
- path sample joint spacing: no more than 2 degrees
- minimum path samples: 33
- TITA poses: nominal stand plus reset-envelope representatives

These values are admission parameters, not hardware safety guarantees.

### 5.2 Edge admission

Every graph edge must be checked along the full interpolated joint path. An
occupied Cartesian voxel alone must never be interpreted as an edge. The first
expanded implementation may remain a WORK-centered hub:

```text
WORK -> target -> WORK -> next target
```

This is slower than arbitrary target-to-target routing but preserves a simple
reviewable path contract. A later graph may add local target-to-target edges
only after each added edge passes the same dense gates.

### 5.3 Current builder status

`test/build_tita_gluon_cartesian_hub_graph.py` produced the current 256-target
artifact against the current URDF hashes. The four task nodes are 23, 111, 18,
and 208 in `LEFT_HIGH -> RIGHT_LOW -> LEFT_LOW -> RIGHT_HIGH` order. The graph
remains `SUSPICIOUS`, not certified: the 10 mm inflation, provisional mount and
collision meshes, three sampled TITA postures, and absence of a tool model are
explicit limitations.

### 5.4 Hub-local target regions

Each graph hub `v_j` owns an offline-tested local target region `R_j`. A first
implementation may use a small axis-aligned region, but the stored bounds must
come from IK, joint-limit, singularity, and mesh-collision sampling rather than
from visual tuning alone.

`EXECUTE_CURRENT` is enabled only when the current world target, expressed in
the current TITA base frame, is inside the selected hub region. If a moving base
causes the target to leave that region during local servo or dwell, the arm
holds, the base performs a controlled stop, and the option aborts. A STOW
recovery starts only after a graph path from the measured state has been
validated.

## 6. Primitive collision model

Use a deliberately small set of spheres, capsules, and boxes rather than every
URDF mesh. Start pair selection from the observed reachability rejection
histogram:

- GLUON link5 against TITA base
- GLUON link3 against TITA base
- GLUON link2 against GLUON link5
- GLUON link4 against TITA base
- distal links against the mount jig and other non-adjacent arm links

The exact pair list and primitive fits must be versioned data, not hard-coded
implicitly across several controllers. Each primitive record needs body name,
local endpoints or center, radius/half extents, and a source-geometry hash.

The first runtime target is approximately 10 to 15 high-risk pairs. A fixed
pair list is preferred over broad-phase nearest-body switching so the distance
gradient remains continuous across ordinary motion.

## 7. Tracking-error-aware discrete CBF filter

Given nominal joint velocity `qd_nom` from IK or a graph trajectory, solve a
sampled command filter whose pairwise constraints have the conceptual form

```text
dt * J_i(q[k]) * qd[k] + gamma * h_i(q[k]) >= rho_i
```

with

```text
rho_i = rho_tracking_i + rho_delay_i + rho_geometry_i + rho_discretization_i.
```

The QP objective remains a weighted least-squares projection of `qd_nom`, with
joint-limit constraints and explicitly logged slack if relaxation is enabled.

and joint-limit constraints

```text
 qd_j + alpha_q (q_j - q_lower_j) >= 0
-qd_j + alpha_q (q_upper_j - q_j) >= 0.
```

The safe velocity is integrated to the existing position reference:

```text
q_ref[k+1] = q_ref[k] + qd_safe * dt.
```

The constraint state must use measured simulation/robot joint positions rather
than only the commanded path. Strict CBF invariance cannot be claimed through
a position-PD plant without a bounded tracking-error and delay model. Until
those bounds are measured, collision margin must include conservative tracking
and latency inflation.

Required filter outputs are:

- minimum signed distance and responsible pair
- nominal and filtered joint velocity
- CBF intervention norm
- slack and infeasibility status
- command hold/reject/fallback reason

On invalid distance/Jacobian, infeasible QP, stale state, or non-finite output,
the immediate response is arm HOLD plus controlled base stop, not passage of
the unfiltered command and not an unverified STOW motion.

The margin is described as data-calibrated when derived from percentiles. A
conditional safety statement is permitted only when execution error remains
inside a calibrated bound that is checked on held-out data. The terms
"formally certified graph", "guaranteed collision-free execution", and
"robust safety guarantee" are out of scope without stronger evidence.

## 8. Batched RL integration

CPU Pinocchio/hpp-fcl and a general-purpose QP per environment per physics step
will not scale to 4096 environments. Training should use:

- offline graph nodes and edges for hard target/path admission
- batched PyTorch forward kinematics for the small primitive set
- batched analytic capsule/sphere distances and gradients on the GPU
- CBF filtering at the GLUON command update rate rather than every internal
  PhysX substep when validated safe
- hpp-fcl only for offline builds and smaller validation batches

Log at least:

- minimum distance p01/p50/p99 and violations per pair
- CBF intervention rate and magnitude
- target rejection/resampling rate
- GLUON tracking error and torque
- TITA contact, tilt, velocity, yaw, and height errors
- wheel horizontal separation during zero-velocity commands
- completion and timeout rates

The future upper planner receives a penalty for targets that cause repeated CBF
intervention. This gives MPC-like anticipation while retaining the CBF as the
last local command shield.

## 9. Go/No-Go task and experiment split

The fixed target order is `LEFT_HIGH -> RIGHT_LOW -> LEFT_LOW -> RIGHT_HIGH`.
Episode resets add small longitudinal, lateral, and height offsets while
preserving order. Target poses are oracle metadata. Success requires position
and facing tolerances to remain satisfied for at least 0.3 seconds.

Base travel time between targets and graph transition time must both remain in
the approximate 2--4 second range; otherwise timing is trivial or infeasible.
Current and next target geometry, current option, executor state, option
progress, arm state, and action mask are policy observations. During `DWELL`,
the base may move at a limited rate while the local servo maintains the world
inspection pose, but `PREPARE_NEXT` is masked.

Task-level coordination compares three planners under the same final graph and
tracking-error-aware CBF:

1. stop-and-go;
2. a concurrent scheduler grid-searched over start distance and base speed
   scale during arm motion;
3. high-level RL.

Controller-level safety replays identical initial states and nominal graph/local
commands through graph-only, nominal discrete CBF, and error-aware discrete CBF
layers. This avoids swapping filters under a policy trained for a different
intervention distribution. An end-to-end filter swap is supplementary only.

Primary metrics are task success, successful-episode cycle time, detailed-mesh
collision/minimum distance, fall rate, and base-arm concurrent-motion ratio.

## 9.1 Later workspace and safety curriculum

The recommended single training pipeline is:

1. TITA stabilization with GLUON at WORK.
2. Expand graph target radius/complexity while every motion returns through
   admitted edges.
3. Add the online primitive monitor and record distances without modifying
   commands.
4. Enable the CBF filter and an intervention penalty.
5. Expand Cartesian target sampling and orientation/q6 only after rebuilding
   the graph with the gripper/tool model.

`model_9000.pt` remains useful only as a historical narrow-workspace baseline.
It is not a collision-safe checkpoint for the expanded workspace and is not
used to initialize the new inspection curriculum.

The first mobile Gate-0 diagnostic showed that the selected wide inspection
hubs are outside the arm-motion support used to train `model_9000.pt`. The
fixed-root graph/local executor passes, but the frozen locomotion policy changes
body attitude after a wide hub transition, moving the world-fixed target about
0.27 m in the base frame and triggering the local-region abort. Scheduler/RL
timing comparisons are therefore invalid until a low-level policy is trained
on the inspection-hub distribution and revalidated. To avoid mixing the old
checkpoint's narrow-arm behavior into this prerequisite, the dedicated task
starts an RMA Teacher from random network initialization:

1. rollout steps 0--120,000: GLUON remains fixed at WORK while the inherited
   TITA height curriculum widens from `(0.32, 0.38)` to `(0.25, 0.45)`;
2. rollout steps 120,000--216,000: GLUON motion widens linearly from WORK to
   the four selected inspection hubs;
3. rollout steps 216,000--240,000: train at the complete four-hub envelope.

At 24 rollout steps per iteration this is one 10,000-iteration run. No resume
flag or source checkpoint is used. The resulting checkpoint must pass the
wide-hub mobile prerequisite before any high-level scheduler/RL comparison.

### 9.1 2026-08-11 automatic Gate audit

The dedicated random-initialization run completed, but its four-target mobile
prerequisite did not pass. On the exact inspection play task, both the new
`model_9000.pt` and `model_9999.pt` had zero base contacts in a 128-environment
full-hub evaluation. The new `model_9000.pt` is the provisional freeze candidate
because its tilt-norm p99 (`0.142`) and height RMSE (`0.009 m`) were lower than
the corresponding `model_9999.pt` values (`0.262` and `0.018 m`). This is the
checkpoint in run `2026-08-11_09-47-10_phase1-work-phase2-inspection-hubs`, not
the historical narrow-workspace `model_9000.pt` discussed above.

The corrected stop-and-go evaluator still failed before completing the ordered
targets. The audit found three coupled issues:

1. the original evaluator tilted the longitudinal route with the settled base
   quaternion; route translation is now gravity-aligned while hub poses retain
   the settled full base attitude;
2. a zero orientation gain still retained angular Jacobian constraints; the
   explicit position-only mode now solves a translational 3D DLS problem;
3. after those corrections, base-relative target drift can still invalidate a
   hub region, and an intentionally wide diagnostic region merely moves the
   failure to the target-1 graph transition.

Therefore Gate 0 remains `FAIL`. Initial WORK-pose/center-of-mass tuning is
deferred, but scheduler tuning and high-level PPO are blocked until the
stop-and-go executor completes the task across seeds without an unvalidated
region expansion. The full evidence is in
`docs/exp/2026-08-11/sequential_inspection_automatic_gate_audit.md`.

### 9.2 2026-08-12 position-only prerequisite resolution

The position-only stop-and-go prerequisite now passes. The remaining failure
was not caused only by workspace drift: the graph executor advanced phase 1
and phase 2 from a live, mutated phase tensor in one control update, so a hub
trajectory could be skipped after STOW. Graph completion now uses a snapshot
of the completed phase. The stop-and-go controller also now commands exactly
zero base velocity during graph execution, local servo, and dwell, and admits
local execution only after measured base speed and yaw rate satisfy the stop
gate.

With gravity-aligned target positions, translational-only differential IK, the
normal local regions, and a validation graph profile of 60 deg/s and
180 deg/s^2, the frozen 2026-08-11 `model_9000.pt` completed all four ordered
targets in 9/9 environments over two seeds. The held-out eight-environment run
had a 50.765 s mean successful cycle time, zero falls, zero base contacts, zero
timeouts, and zero local-region exits. This is a `PASS` only for the
position-only deterministic execution prerequisite. Self-collision and CBF
remain disabled, orientation is not yet validated, and the 60 deg/s profile is
outside the 20 deg/s arm-motion distribution used in low-level training.

The detailed evidence is in
`docs/exp/2026-08-12/position_only_stop_and_go_gate_validation.md`. Gate 0 now
advances to the concurrent-scheduler grid search; high-level PPO remains
blocked until that deterministic baseline is tuned and frozen.

### 9.3 2026-08-12 classical concurrent baseline freeze

The position-only classical scheduler is now frozen at a 1.4 m arm-transition
start distance and a 0.6 base-command speed scale during arm execution. A
21-candidate bounded dry-run provided the coarse selection, followed by Isaac
validation on a four-environment selection seed and an eight-environment
held-out seed. Both Isaac batches completed every target in every environment.
The held-out mean cycle time was 37.830 s with a 0.885 concurrent-motion ratio,
zero falls, zero base contacts, zero timeouts, and zero local-region exits.

This is 25.48% faster than the 50.765 s held-out stop-and-go mean. The initial
constant-speed scheduler was rejected after producing local servo/dwell
chatter and local-region exits; the frozen scheduler uses proportional braking
to make its station command converge continuously to zero. The detailed
evidence is in
`docs/exp/2026-08-12/classical_concurrent_scheduler_gate_validation.md`.

The scheduler freeze unblocks position-only high-level policy development, but
does not pass the collision-safety or full inspection-pose Gates. Any RL
comparison must retain the same disabled self-collision/CBF configuration and
60 deg/s graph profile until those later components are validated separately.

### 9.4 2026-08-13 high-level PPO Gate-0 result

The first from-scratch high-level hybrid PPO experiment is complete and Gate 0
is `FAIL`. Before training, the wrapper was corrected so task completion pays a
one-step bonus rather than a persistent per-step bonus, arm-local failures do
not discard unrelated vector rollouts, and dense route reward measures progress
toward the active station rather than unbounded forward travel. The upper loop
runs at 10 Hz over the frozen 50 Hz locomotion controller with `gamma=0.995`.

Stochastic training rollouts reached a maximum observed 39/64 task success, but
none of model 75, 100, 150, or 224 completed a deterministic selection layout.
The final model completed target zero and then selected `HOLD` 5,591 times out
of 5,600 decisions; it selected `PREPARE_NEXT` once. This is categorical option
collapse, not a low-level fall or deterministic collision abort. The detailed
evidence is in `docs/exp/2026-08-13/high_level_hybrid_ppo_gate0.md`.

The next Gate-0 attempt is intentionally bounded. Keep the task, frozen
low-level checkpoint, continuous base head, graph/local executor, and scheduler
baseline unchanged. Replace the four-way arm choice with a phase-conditioned
binary `WAIT/TRIGGER` head; the executor maps `TRIGGER` to the sole meaningful
progress transition for the current phase. Log phase-conditioned option
probabilities and require deterministic selection success before using the
held-out seed. A scheduler behavior-cloning initialization is a later explicit
ablation only if the second from-scratch attempt also fails.

## 10. Zero-command stance diagnosis

### 10.1 Saved training-contract differences

The arm-free reference run and the TITA+GLUON run did not differ only by the
arm:

| Item | Arm-free RMA Teacher | TITA+GLUON model 9000 |
|---|---:|---:|
| runtime mass | 25.690956 kg | 30.958569 kg |
| explicit standing-env ratio | 0.20 | 0.05 |
| ADD `w_disc / w_fm` | 0.5 / 0.5 | 0.2 / 0.8 |
| startup all-body inertia/COM randomization | enabled | disabled |
| PhysX position/velocity iterations | 4 / 0 | 8 / 1 |

The mounted GLUON plus jig adds about 5.268 kg, roughly 20.5% of the original
TITA mass, at an elevated/offset location. At the same time, explicit standing
exposure was reduced by 4x and the ADD reward mixture changed. The previous
claim that the reference MDP was inherited unchanged is therefore too strong.

### 10.2 Fixed zero-command validation

The diagnostic used 32 environments, 400 policy steps, a 150-step settling
window, seed 20260810, no observation noise/domain randomization/pushes, and
forced zero planar/yaw velocity. Heights 0.35 and 0.39 m were split evenly.

| Case | Wheel horizontal separation | Hip absolute sum | Height abs. error | XY speed |
|---|---:|---:|---:|---:|
| arm-free `model_9999` | 0.5645 m | 0.0442 rad | 0.0102 m | 0.0201 m/s |
| GLUON `model_9000`, arm fixed | 0.6814 m | 0.0458 rad | 0.0107 m | 0.0206 m/s |
| GLUON `model_9000`, arm moving | 0.6726 m | 0.0432 rad | 0.0087 m | 0.0269 m/s |

The visual splay is not primarily a hip-yaw deviation. The GLUON policy uses a
more extended shoulder/leg geometry and increases wheel separation by about
19--21%. This is a plausible robust support strategy for the heavier elevated
payload, made inexpensive by the weak Huber-style posture terms and the
reduced standing exposure.

### 10.3 Height 0.39 interpretation

For the existing `model_9000`, changing only the command height is not a fix:

| GLUON condition | Height | Wheel separation | XY speed |
|---|---:|---:|---:|
| fixed arm | 0.35 m | 0.6819 m | 0.0029 m/s |
| fixed arm | 0.39 m | 0.6810 m | 0.0384 m/s |
| moving arm | 0.35 m | 0.6743 m | 0.0217 m/s |
| moving arm | 0.39 m | 0.6709 m | 0.0321 m/s |

The user-reported arm-free sim2sim behavior at 0.39 m remains valuable
deployment evidence, but it must not be transferred to `model_9000` by config
alone. In the current Isaac validation, 0.39 m barely changes stance width and
increases drift.

For the next training run, 0.39 m should instead be an explicit learned
init-phase contract:

- velocity command is zero during init phase
- height command is exactly 0.39 m, visible consistently to observation and
  reward
- transition from 0.39 m to the sampled episode height is ramped rather than
  stepped
- explicit standing-env ratio is restored to 0.20
- ADD weights are restored to the saved reference value 0.5/0.5 unless an
  ablation proves otherwise
- add a zero-command wheel-separation or foot-under-hip geometry objective
- retain the existing height-aware shoulder/leg terms, but prevent large
  deviations from becoming too cheap outside the Huber quadratic region

Do not change the deployment default height for `model_9000` until this new
training/ablation passes both Isaac validation and the exact known-good
sim2sim protocol.

## 11. Validation gates

### Gate 0: upper-RL necessity

- prerequisite: the frozen low-level checkpoint passes wide-hub attitude,
  fall, command-tracking, and world-target local-region validation
- four ordered target poses execute with the persistent option FSM
- stop-and-go and tuned scheduler use the same graph/local executor
- scheduler parameters are selected on training layouts and frozen for unseen
  layouts
- high-level RL improves successful cycle time or the safety/time Pareto front
  on unseen layouts; otherwise simplify the method or drop the upper RL claim

### Gate A: reference parity

- saved environment values explicitly match the arm-free reference where not
  intentionally overridden
- standing ratio is 0.20
- ADD weights are 0.5/0.5
- TITA action order and scaling are unchanged
- every intentional mismatch is listed in the experiment record

### Gate B: zero-command stance

- zero base contacts across the fixed protocol
- wheel separation is no more than the reference mean plus a provisional
  30 mm, pending a measured hardware stance target
- height and XY drift do not regress materially from the arm-free reference
- evaluate init-phase 0.35 and 0.39 ablations rather than assuming either one

### Gate C: collision graph

- current URDF hashes match the artifact
- every stored edge passes dense joint limit, singularity, and hpp-fcl gates
- rejection statistics and known geometry omissions are recorded

### Gate D: runtime primitive monitor

- batched primitive distances agree with hpp-fcl on a held-out joint set
- false-safe results are zero in the held-out set
- gradient finite differences pass away from closest-feature switches

### Gate E: CBF filter

- no admitted collision-margin violation in bounded simulation tests
- intervention, slack, and infeasibility metrics are finite and logged
- unsafe/stale input causes hold or controlled fallback
- tracking-error robustness margin is measured before hardware use

### Gate F: staged Sim2Real

- tool/gripper/mount geometry and inertia are measured
- q/qd, latency, and tracking-error envelopes are validated read-only first
- operator separately authorizes each state-changing stage

## 12. Immediate implementation order

1. Keep the 2026-08-11 `model_9000.pt` as the provisional low-level candidate;
   do not export or deploy it yet.
2. Preserve the passing position-only stop-and-go execution contract and its
   measured stop gate as the deterministic reference.
3. Revalidate orientation/facing and each hub-local region with per-joint
   margins before claiming the full inspection-pose task.
4. Keep the 9/9 two-seed stop-and-go result as the position-only prerequisite;
   do not reinterpret it as collision-safety evidence.
5. Preserve the frozen classical scheduler parameters (1.4 m, 0.6 scale) and
   its 37.830 s held-out baseline for the position-only Gate-0 comparison.
6. Keep the phase-conditioned binary `WAIT/TRIGGER` interface, but treat the
   2026-08-19 BC/PPO result as `FAIL`: the stable model-0 policy achieved 8/8
   selection success at 37.850 s, 0.020 s slower than the 37.830 s scheduler.
   Repeat both methods over multiple fixed seeds before funding more PPO work.
7. If Gate 0 passes, finish the hub-local region validator and add nominal
   discrete CBF while logging one-step execution error.
8. Calibrate pairwise margins, add the tracking-error-aware filter, and run
   identical-trajectory safety replay before any staged Sim2Real work.
9. Tune the asymmetric init/WORK arm posture separately after the execution
   contract is stable; do not silently mix that change into Gate-0 evidence.

### 2026-08-14 Gate-0 trigger-head checkpoint

The binary interface and phase diagnostics are implemented and passed unit and
Isaac smoke tests. A from-scratch run reached iteration 109 and saved
`model_100.pt`. Stochastic rollout behavior improved over the four-way head
(peak batch success 42.19%), but remained highly variable and suffered frequent
local-region aborts. At iteration 100, both PREPARE and EXECUTE phases had a
greedy-trigger majority in the on-policy batch, so `model_100.pt` remains a
candidate rather than a declared failure.

Deterministic full-horizon selection is `BLOCKED` until the shared GPU is free:
an unrelated training process saturated the device, making a single 70-second
episode exceed 22 minutes wall time. Do not start held-out evaluation or CBF
work yet. The immediate next action is deterministic selection of model 100 on
the fixed selection seed, followed by models 25/50/75 only if model 100 fails.

### 2026-08-19 Gate-0 BC/PPO audit

The blocked deterministic audit is complete. From-scratch trigger checkpoints
25/50/75/100 all achieved 0/8 success. Scheduler behavior cloning produced a
stable 8/8 policy but was 0.795 s slower than the classical scheduler. Ordinary
PPO destroyed that initialization on its first update even after reducing the
continuous exploration standard deviation from 0.5 to 0.1.

A BC-state distillation anchor and a 0.1 actor/critic learning-rate ratio made
the first PPO update stable. The selected model 0 achieved 8/8 success in
37.850 s with no local abort, emergency hold, or low-level failure. Models 5
and 24 regressed to 6/8 and 7/8. Because the frozen scheduler remains faster at
37.830 s, Gate-0 is still `FAIL`; held-out evaluation and CBF work remain
blocked. The next bounded action is a multi-seed paired comparison of model 0
and the scheduler, not longer training. Detailed evidence is in
`docs/exp/2026-08-19/high_level_bc_ppo_gate0.md`.
