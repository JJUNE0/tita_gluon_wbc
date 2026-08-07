# GLUON HOME/WORK IK stabilization

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `SUSPICIOUS`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (analytic position-only DLS; no learned policy)
- Robot hardware commands: none

## Motivation

The previous GUI test started Cartesian IK at q=0. Runtime logs showed that this
pose was nearly fully extended (`sigma_min` approximately `2.5e-5`). A held key
could also place the Cartesian target 25--35 mm ahead of the slew-limited arm.
The combination produced large joint motion, repeated command slew saturation,
and poor operator feel even though the earlier static headless checks passed.

## Change

- `H`: enter joint-space HOME at `[0, 0, 0, 0, 0, 0] rad`.
- `Z`: enter joint-space WORK at `[0, 0.8, 1.6, 0.8, 0, 0] rad`, wait for a
  2 deg joint-error gate and 25 stable control ticks, then enable Cartesian IK.
- Run Cartesian DLS only in WORK; use the WORK posture as the nullspace nominal.
- Restrict WORK workspace to x `[0.43, 0.49]`, y `[-0.01, 0.05]`,
  z `[-0.17, -0.10]` m in `base_link`.
- Limit the local Cartesian servo target to 10 mm ahead of the current EE.
- Keep all six joint commands below 20 deg/s and keep q6 at zero.

## Observed metrics and log summary

WORK pose runtime conditioning:

- EE position: `[0.462038, 0.021868, -0.135892] m` in `base_link`
- Jacobian singular values: `[0.428363, 0.118734, 0.020601]`
- runtime soft-limit violations: 0
- result: `GLUON_WORK_POSE_CONDITIONING: PASS`

Headless HOME-to-WORK hold:

- final position error: `2.596 mm`
- joint-limit violations: 0
- velocity-limit violations: 0
- maximum q6 deviation: `0.000693 deg`
- result: `GLUON_KEYBOARD_IK: PASS`

Six independent 10 mm Cartesian targets from WORK:

| Direction | Final error (mm) | Joint/velocity violations | Result |
|---|---:|---:|---|
| +X | 2.456 | 0 / 0 | `PASS` |
| -X | 2.733 | 0 / 0 | `PASS` |
| +Y | 2.357 | 0 / 0 | `PASS` |
| -Y | 2.844 | 0 / 0 | `PASS` |
| +Z | 2.929 | 0 / 0 | `PASS` |
| -Z | 1.833 | 0 / 0 | `PASS` |

Across these runs, maximum command slew was `0.349069 rad/s` (20 deg/s),
maximum measured velocity ratio was `0.2263`, and maximum q6 deviation was
`0.001232 deg`.

## Evidence assessment

Automated numerical and runtime evidence is `PASS`. The experiment remains
overall `SUSPICIOUS` until the operator repeats the GUI key test and confirms
that H/Z transitions and W/S/A/D/Q/E motion are visually smooth. The earlier
GUI behavior is therefore not treated as accepted merely because the headless
regression passes.

## Workspace frame and reach-envelope follow-up

Operator feedback reported that Y motion felt correct while X/Z motion did
not. Inspection showed that the command remains correctly expressed in the
CAD `base_link`, but the articulation root is mounted at -90 deg about world Y.
The viewport mapping is therefore:

- `base +X = world +Z`
- `base +Y = world +Y`
- `base +Z = world -X`

This explains why Y alone matched the visual world-axis intuition. It does not
by itself indicate a bad joint1 axis. The joint1 local Z axis, after its URDF
origin rotation, is base +X; the Isaac root mounting rotation maps it to world
+Z as expected on the physical robot.

A deterministic URDF FK analysis sampled 500,000 joint configurations inside
the declared joint limits:

- shoulder center in `base_link`: `[0.1205, -0.0000179, 0] m`
- approximate maximum link6 radius from shoulder: `0.475541 m`
- sampled XYZ bounds in `base_link`: X `[-0.14934, 0.57840]`,
  Y `[-0.47415, 0.47345]`, Z `[-0.47400, 0.47378] m`
- q=0 FK contract error: `5.90e-7 m`
- result: `GLUON_WORKSPACE_ANALYSIS: PASS`

The approximate outer radius remains analysis-only after operator review; its
cyan sphere overlay was removed from the GUI. After further operator feedback,
the W1 cuboid surface was also removed. The GUI retains only eight magenta
corner points and the thin yellow trajectory boundary described below.
Headless creation of these markers and the HOME-to-WORK controller regression returned
`GLUON_KEYBOARD_IK: PASS` with `2.596 mm` final error and zero joint/velocity
limit violations.

## W1 active command workspace

The original W0 (`0.06 x 0.06 x 0.07 m`) was a deliberately small initial
validation gate rather than the robot's full workspace. A W1 candidate was
selected using 500,000 soft-limit URDF FK samples and the q1--q5 linear
Jacobian, filtering samples below `sigma_min=0.01`.

Two larger candidates were rejected because one or more Isaac runtime corner
tests exceeded the 5 mm error criterion. The accepted W1 in `base_link` is:

- X `[0.36, 0.48] m`
- Y `[-0.08, 0.09] m`
- Z `[-0.20, -0.11] m`
- size `0.12 x 0.17 x 0.09 m`
- volume ratio relative to W0: approximately `7.29`

The conditioned 5 x 5 x 5 sample-grid check had maximum nearest-sample
distance `7.57 mm`, 95th percentile `4.74 mm`, and median `2.65 mm`. All eight
W1 corners were then commanded independently from WORK in Isaac Sim:

| X | Y | Z | Final error (mm) | Result |
|---:|---:|---:|---:|---|
| 0.36 | -0.08 | -0.20 | 3.168 | `PASS` |
| 0.36 | -0.08 | -0.11 | 4.359 | `PASS` |
| 0.36 | 0.09 | -0.20 | 3.323 | `PASS` |
| 0.36 | 0.09 | -0.11 | 3.316 | `PASS` |
| 0.48 | -0.08 | -0.20 | 4.691 | `PASS` |
| 0.48 | -0.08 | -0.11 | 3.108 | `PASS` |
| 0.48 | 0.09 | -0.20 | 4.949 | `PASS` |
| 0.48 | 0.09 | -0.11 | 1.723 | `PASS` |

Every run had zero joint-position and velocity-limit violations, command slew
at or below 20 deg/s, and maximum q6 deviation below `0.0012 deg`. Because the
worst corner passes the 5 mm threshold by only `0.051 mm`, W1 boundary behavior
remains `SUSPICIOUS` pending interactive operator evaluation and should not be
treated as a collision-free hardware workspace.

## W1 corner-loop trajectory

The W1 cuboid opacity was first reduced from `0.12` to `0.025`, then the cuboid
was removed entirely after operator review. The final GUI keeps only eight
magenta corner markers and a thin yellow closed path. The path is the following
Hamiltonian cycle, where each bit selects the lower or upper X/Y/Z bound:

```text
000 -> 001 -> 101 -> 111 -> 011 -> 010 -> 110 -> 100 -> 000
```

`P` starts one traversal (and cancels an active traversal). From HOME it first
enters WORK, then advances the Cartesian planner. Planner lead is
gated at `8 mm`; the existing local DLS target remains limited to `10 mm` ahead
of the measured EE. A corner is accepted after measured error remains at or
below `5 mm` for five control ticks.

The first candidate traversed the same loop in the opposite direction. It
stalled on its final `001 -> 000` edge with `7.33 mm` error and is recorded as
`FAIL`; reducing the waypoint distance alone did not resolve the local IK path.
Reversing the traversal order produced the following direct headless runtime
evidence:

- command: `run_gluon_keyboard_ik.py --headless --device cpu --max-steps 22000 --run-corner-trajectory --trajectory-speed-m-s 0.03 --trajectory-corner-tolerance-m 0.005 --final-error-limit-m 0.005`
- completed: one closed loop, 9/9 waypoints (8 unique corners plus return)
- physics/control steps: `9465 / 2367`
- maximum accepted corner error: `4.750 mm`
- final Cartesian error: `3.269 mm`
- joint-position / velocity-limit violations: `0 / 0`
- maximum measured velocity ratio: `0.1981`
- maximum command slew: `0.349069 rad/s` (`20 deg/s`)
- maximum q6 deviation: `0.000988 deg`
- result: `GLUON_KEYBOARD_IK: PASS`

This remains a local W1 validation. Since joint1 rotates about base +X (world
+Z), sweeping the local cross-section through the approximately `+-148 deg`
q1 range should yield a substantially larger annular/cylindrical-sector W2.
W2 is not yet approved: it still requires manipulability, joint-limit, runtime
IK, and collision filtering rather than a geometric sweep alone.

The automated corner-loop evidence is `PASS`; the overall experiment status
remains `SUSPICIOUS` until the operator confirms the corner/path markers and
interactive `P` behavior in the GUI.

## Faster W1 trajectory follow-up

After the initial interactive run was judged too slow, the simulation defaults
were increased together rather than changing only the Cartesian planner:

- keyboard Cartesian speed: `0.05 -> 0.10 m/s`
- corner trajectory speed: `0.03 -> 0.06 m/s`
- HOME/WORK/IK joint command slew: `20 -> 40 deg/s`
- W1 cuboid: removed; only magenta corners and yellow path remain

Direct headless runtime evidence using the new defaults:

- command: `run_gluon_keyboard_ik.py --headless --device cpu --max-steps 15000 --run-corner-trajectory --final-error-limit-m 0.005`
- completed: one closed loop, 9/9 waypoints
- physics/control steps: `4873 / 1219` (previous baseline: `9465 / 2367`)
- maximum accepted corner error: `4.928 mm`
- final Cartesian error: `3.271 mm`
- joint-position / velocity-limit violations: `0 / 0`
- maximum measured velocity ratio: `0.3562`
- maximum command slew: `0.698134 rad/s` (configured `40 deg/s`)
- maximum q6 deviation: `0.001663 deg`
- result: `GLUON_KEYBOARD_IK: PASS`

The loop completed in approximately half as many simulation steps with no
runtime limit violations. Evidence for this faster `VALIDATION_SIM` profile is
`PASS`; visual operator acceptance remains `SUSPICIOUS`, and these values are
not automatically approved for hardware execution.

## Headless segment dynamics diagnosis

Operator observation reported severe vibration on a specific part of the fast
loop. The same run was repeated headlessly with:

```text
--log-segment-dynamics --status-log-every-controls 0
```

The diagnostics aggregate 200 Hz joint position error, velocity,
acceleration, and implicit-PD estimated torque, plus 50 Hz IK singular value,
command slew, and planner lead limiting. For an IsaacLab implicit actuator,
`computed_torque` and `applied_torque` are estimates reconstructed from the PD
law because PhysX does not expose the exact solver torque.

The strongest oscillation evidence occurred on segment 3:

```text
start [0.48, -0.08, -0.11] -> target [0.48, 0.09, -0.11] m
```

- control/physics samples: `202 / 808`
- minimum `sigma_min`: `0.0014145`
- maximum goal/servo error: `16.886 / 10.283 mm`
- slew-limited controls: `195 / 202`
- target-lead-limited controls: `29 / 202`
- actual joint-velocity sign flips J1--J6: `[12, 4, 0, 7, 1, 0]`
- command-direction sign flips J1--J6: `[23, 24, 18, 13, 1, 0]`
- largest sampled acceleration: J5 `61.637 rad/s^2`
- torque clipping: zero on every joint and every segment

Segment 1 reached a still smaller `sigma_min=0.0002696`, but had zero actual
velocity sign flips and only one command-direction flip. Singularity proximity
alone therefore does not fully explain the visible vibration. Segment 3 is the
combination of low manipulability, almost continuous 40 deg/s command slew
saturation, discontinuous planner lead gating, and repeated DLS command
direction changes.

The largest estimated torque ratio over the entire trajectory was only
`0.1981` (J3 on segment 2); segment 3 also had zero torque clipping. The direct
evidence therefore rejects actuator torque saturation as the primary cause and
identifies the Cartesian IK/planner command layer as the primary diagnosis.
The trajectory still completed 9/9 waypoints with zero position/velocity-limit
violations, so runtime completion remains `PASS`, while smooth-motion
acceptance is `FAIL` for segment 3 until the command oscillation is corrected.

## W2 cylindrical-workspace implementation

- Execution Domain: `VALIDATION_SIM`
- Policy checkpoint / ONNX hash: `N/A` (deterministic position-only DLS; no learned policy)
- URDF SHA256: `b9b25074b7a417a9e499f14fee852699ac6f8a00ab4b137f90ec843eccc8ede4`
- USD SHA256: `a5b9514205ae7b3de4321ab308fc6e8aa4f3b17533c172fe53f7269a5b49a42d`
- Functional evidence: `PASS`
- Smooth-motion evidence: `SUSPICIOUS`

The active Cartesian W1 AABB was replaced by a cylindrical sector around the
joint1 `base_link +X` axis:

- X `[0.36, 0.48] m`
- radius `[0.13, 0.21] m`
- absolute theta `[-175, +35] deg`
- coordinate representation: theta offset `[-105, +105] deg` about `-70 deg`
- geometric volume `0.00598159 m^3`, `3.25795x` W1

Keyboard increments are now interpreted as `[dX, dR, r*dtheta]`: W/S changes
X, A/D changes radius, and Q/E moves tangentially about the joint1 axis. W2
clamping and the P-key planner use the same cylindrical coordinates. The
yellow path is sampled densely in cylindrical space, so theta edges are actual
arcs rather than Cartesian chords; only yellow samples and eight magenta
vertices are rendered.

The deterministic 250,000-sample URDF FK/Jacobian analysis reported:

- samples above `sigma_min=0.01`: `99.3116%`
- W2 5x5x5 conditioned nearest-sample distance: maximum `8.781 mm`, p95
  `6.584 mm`, median `3.830 mm`
- `GLUON_WORKSPACE_ANALYSIS: PASS`

The first `+-120 deg` W2 candidate was rejected. It reached 5/9 waypoints but
stopped on the outer-radius theta arc with q1 at its `-2.455 rad` soft limit.
This demonstrated that random FK point support does not guarantee a continuous
IK branch. The accepted `-175..+35 deg` sector preserves approximately five
degrees of q1 margin on the observed branch.

Final runtime command:

```bash
/home/cocel/isaac/env_isaaclab/bin/python \
  lab/ddt_lab/scripts/gluon/run_gluon_keyboard_ik.py \
  --headless --device cpu --max-steps 18000 \
  --run-corner-trajectory --final-error-limit-m 0.005 \
  --log-segment-dynamics --status-log-every-controls 0
```

Final observed metrics:

- completed `9/9` waypoints, one closed loop
- physics/control steps: `8469 / 2118`
- maximum accepted vertex error and final error: `4.738 mm`
- joint-position / velocity-limit violations: `0 / 0`
- maximum velocity-limit ratio: `0.3371`
- torque clipping: zero on all joints and segments
- maximum estimated torque ratio: `0.1769`
- maximum q6 deviation: `0.001374 deg`
- `GLUON_KEYBOARD_IK: PASS`

The formerly severe W1 segment had 24 total actual velocity sign flips. W2
removed that segment and most W2 segments had zero flips. W2 segment 7
(`X=0.48 m`, theta `-175 deg`, radius `0.21 -> 0.13 m`) remains the limiting
case: `sigma_min=0.000333`, nine actual velocity sign flips, maximum goal error
`15.785 mm`, and maximum sampled acceleration `49.496 rad/s^2`. A radial-only
planner speed scale of `0.5` reduced this from 11 flips and `28.158 mm` goal
error without changing the 0.06 m/s axial/theta speed. Increasing radial DLS
damping to 0.03 reduced error but increased flips to 13, so it was rejected.

Thus W2 functional tracking is `PASS`, but visual smoothness remains
`SUSPICIOUS` pending GUI/operator confirmation. This simulation result is not
a collision-free workspace claim and does not authorize hardware deployment.
