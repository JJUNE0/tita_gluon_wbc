# Sequential Inspection Automatic Gate Audit

## Metadata

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `FAIL`
- Hardware interaction: none
- Seed: `20260811`
- Candidate checkpoint `model_9000.pt` SHA256:
  `9d8d1fad8f0e2c3e04eb9d937ca91706174ea8b97c21501eb6b2744defc8acde`
- Candidate checkpoint `model_9999.pt` SHA256:
  `737b82442649d90a612e819a94180bcd57e55393b66d87eb80041afc40e838e9`

The objective was to choose a frozen low-level checkpoint and determine
whether the four-target stop-and-go prerequisite was ready for scheduler and
high-level PPO evaluation. It was not.

## Checkpoint comparison

Both checkpoints were evaluated on the exact inspection curriculum play task
with 128 environments and 1,000 policy steps per checkpoint.

| Metric | model 9000 | model 9999 |
|---|---:|---:|
| base contacts | 0 | 0 |
| planar velocity RMSE | 0.04583 m/s | 0.04569 m/s |
| yaw-rate RMSE | 0.04596 rad/s | 0.05140 rad/s |
| height RMSE | 0.00904 m | 0.01768 m |
| arm tracking p99 | 0.05005 rad | 0.04988 rad |
| tilt-norm p99 | 0.14248 | 0.26169 |

Both isolated low-level evaluations are `PASS`, but `model_9000.pt` is the
provisional freeze candidate because its height and attitude errors are
materially lower. This does not make it a passing sequential-task checkpoint.
The initial asymmetric arm posture/center-of-mass appearance remains a tuning
backlog item and was deliberately not changed in this audit.

Evidence:

- `inspection_checkpoint_9000_9999_full_hub_eval.json`
- `inspection_checkpoint_9000_9999_full_hub_eval.log`

## Route-frame correction

The first baseline implementation rotated the entire longitudinal route offset
by the settled base quaternion. A nonzero base pitch therefore changed target
height by approximately `route_s * sin(pitch)`. The evaluator now uses:

- the settled full base pose for each hub pose;
- the settled yaw only for horizontal route translation.

Runs produced before this correction are diagnostic only and are not Gate
evidence.

## Four-target stop-and-go result

With the corrected route frame and the normal position-plus-facing local
servo, `model_9999.pt` completed target 0 but all four environments failed at
target 1:

- success rate: `0/4`;
- fall rate and base contacts: `0`;
- final position error: `0.458--0.503 m`;
- final facing error: `0.806--1.164 rad`;
- minimum joint-limit margin: `-0.0436-- -0.0455 rad`;
- final tilt norm: `0.365--0.382`.

Evidence:

- `model9999_stop_and_go_decoupled_route_validation.json`
- `model9999_stop_and_go_decoupled_route_validation.log`

## Position-only diagnosis

The executor previously retained angular Jacobian rows when
`local_orientation_gain=0`. A zero angular twist still constrained orientation
and could drive the differential IK solution onto a distant branch. The
position-only contract was corrected to solve a 3D translational DLS problem
when orientation gain is zero.

The corrected fixed-root executor smoke passed in two environments. The mobile
diagnosis did not:

1. With a provisional `(0.35, 0.20, 0.35) m` hub AABB, the target moved to
   `y=-0.253 m` in the base frame and triggered a local-region exit at target 0.
   All arm joint margins were positive; the final tilt norm was `0.320`.
2. With an intentionally non-admissible `(0.60, 0.60, 0.60) m` diagnostic
   AABB, the region abort disappeared, but the run still ended during the
   target-1 graph transition at `1.83 m` route progress. This wide gate is not
   safety evidence.
3. Before the position-only contract correction, the apparent limiting joint
   was `gluon_2L6_4L3_axis_joint_3` at `2.442 rad`, beyond its runtime soft
   upper limit of approximately `2.400 rad`. That result explains the old
   behavior but is not a valid position-only result.

Evidence:

- `position_only_executor_contract_smoke.log`
- `model9000_position_only_contract_fix_validation.json`
- `model9000_position_only_contract_fix_validation.log`
- `model9000_position_only_unbounded_gate_diagnostic.json`
- `model9000_position_only_unbounded_gate_diagnostic.log`
- `model9000_target1_joint_limit_diagnostic.json`

## Go/No-Go decision

`FAIL`: do not run the concurrent-scheduler grid, high-level PPO, CBF
ablation, or Sim2Real stage yet. The upper policy would otherwise be trained
against executor failures rather than a valid coordination problem.

The next validation sequence is:

1. log relative base yaw as well as tilt while stop-and-go holds each route
   station;
2. make target admission and route tracking consistent under the measured
   base attitude, without treating an unvalidated larger AABB as safe;
3. reselect or locally validate hub-to-target regions with positive per-joint
   margin, especially for target 1;
4. bound graph-transition completion time and diagnose why the target-1
   transition did not finish in the 50 s run;
5. require a multi-seed, multi-environment stop-and-go pass before scheduler
   tuning or high-level PPO.

## Tests

- `PASS`: IsaacLab Python `py_compile` for the modified evaluator and action
  implementation.
- `PASS`: `10 passed` in `test/test_sequential_inspection_go_no_go.py`.
- `PASS`: fixed-root position-only executor smoke, 2 environments, 835 physics
  steps, maximum joint tracking error `0.04097 rad`.
- `FAIL`: four-target mobile stop-and-go prerequisite, as detailed above.
