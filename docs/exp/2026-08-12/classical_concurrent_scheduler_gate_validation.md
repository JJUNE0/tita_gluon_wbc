# Classical concurrent scheduler Gate validation

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS` for the position-only timing baseline
- Policy checkpoint: `model_9000.pt`
- Policy checkpoint SHA256: `9d8d1fad8f0e2c3e04eb9d937ca91706174ea8b97c21501eb6b2744defc8acde`
- Safety configuration: self-collision disabled, CBF disabled

## Selection protocol

A bounded `DESKTOP_DRY_RUN` screened 21 combinations from:

- arm start distance: 0.5, 0.8, 1.1, 1.4, 1.7 m;
- base speed scale during arm execution: 0.0, 0.2, 0.4, 0.6.

Each candidate ran 64 deterministic timing episodes. The selected candidate
was then checked in Isaac physics on a four-environment selection seed and an
eight-environment held-out seed. This is a two-stage coarse search rather than
an exhaustive Isaac grid.

The first Isaac attempt exposed a baseline implementation defect: a constant
signed command during local servo crossed the target and repeatedly toggled
between local servo and dwell. Three of four environments eventually exited
their local region. The final scheduler uses the same bounded proportional
route controller as ordinary travel, scaled during graph/local execution, so
the base command converges continuously to zero at the station.

## Frozen classical scheduler

- Arm transition start distance: 1.4 m
- Base-command speed scale during arm execution: 0.6
- Maximum base command: 0.5 m/s
- Graph profile: 60 deg/s and 180 deg/s^2
- Local controller: position-only differential IK
- Target frame: gravity-aligned world route

## Evidence

### Selection seed

- Seed: 20260820
- Environments: 4
- Success: 4/4
- Mean successful cycle time: 37.790 s
- Concurrent-motion ratio: 0.879
- Falls / base contacts / timeouts: 0 / 0 / 0
- Local-region exits / option rejections: 0 / 0
- Result: `scheduler_train_grid_proportional_d1p4_s0p6_4env.json`

### Held-out seed

- Seed: 20260821
- Environments: 8
- Success: 8/8
- Mean successful cycle time: 37.830 s
- Cycle-time range: 36.960--38.260 s
- Concurrent-motion ratio: 0.885
- Falls / base contacts / timeouts: 0 / 0 / 0
- Local-region exits / option rejections: 0 / 0
- Maximum tilt norm by environment: 0.208--0.252
- Maximum absolute base-height deviation by environment: 0.042--0.046 m
- Result: `scheduler_heldout_d1p4_s0p6_8env_seed20260821.json`

Against the held-out stop-and-go mean of 50.765 s, the frozen scheduler reduces
cycle time by 25.48% while retaining 100% task success in this small sample.

## Interpretation and limits

The deterministic concurrent timing baseline is now usable for the
position-only Gate-0 comparison. It is intentionally strong enough that a
future high-level policy must beat a 37.83 s held-out cycle time, not merely the
50.77 s stop-and-go baseline.

This result is not collision-safety evidence. Self-collision, detailed-mesh
distance monitoring, orientation tracking, and CBF filtering remain disabled.
The 60 deg/s arm profile also exceeds the 20 deg/s arm-motion distribution used
for low-level training. These limitations must remain identical when comparing
the high-level policy against this baseline.
