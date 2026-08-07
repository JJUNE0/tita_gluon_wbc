# GLUON P2-P3 keyboard marker and position-only DLS IK

- Date: 2026-08-05
- Execution Domain: `VALIDATION_SIM`
- Branch: `dev_gluon`
- Policy Checkpoint SHA256 or ONNX Hash: N/A (model-based IK)
- IsaacLab revision: `549768529e3859845794a05b8fd3dfd00edadc9e`
- Canonical URDF SHA256: `eb6bbc1f2305fac3da832a911f00efbc82b5c7af57d905b3008bc5531707089e`
- Sim URDF SHA256: `b9b25074b7a417a9e499f14fee852699ac6f8a00ab4b137f90ec843eccc8ede4`
- USD bundle SHA256: `ac95b231160d0a2b6f08bbd59af3c23e391bb6c8d1a094dc044709e0570577b4`
- Automated Evidence Status: `PASS`
- Operator keyboard acceptance: `NOT_TESTED`
- Overall Evidence Status: `SUSPICIOUS`

## Objective

Run the six-axis USD in Isaac Sim at 200 Hz, update a `base_link` XYZ target
at 50 Hz, and control `link6` with bounded position-only DLS on q1--q5 while
holding q6 at zero. Display the target sphere, current EE frame, and live
state/metrics in the GUI.

## Implementation contract

- W/S: base +X/-X
- A/D: base +Y/-Y
- Q/E: base +Z/-Z
- R: reset target to current EE
- H: restore the startup q=0 Cartesian target
- SPACE: pause/resume target updates while physics and hold continue
- ESC: clean exit
- physics/control: 200/50 Hz
- Cartesian speed: 0.05 m/s (`Se3Keyboard` delta 0.001 m per control tick)
- workspace W0: x `[0.52, 0.58]`, y `[-0.04, 0.04]`, z `[-0.18, -0.10]` m
- DLS damping/gain: `0.01` / `2.0`
- q1--q5 nullspace target: q=0, gain `0.1`
- q6 target: 0 rad
- command slew: 20 deg/s
- runtime `soft_joint_pos_limits` and actuator velocity watchdogs

PhysX returns the fixed-base `link6` Jacobian at body index minus one. Its
linear rows are at the rigid-body COM in world coordinates. The implementation
shifts the Jacobian to the `link6` frame origin with the angular rows and then
rotates it into `base_link`.

## Commands

Pure math and Jacobian frame validation:

```bash
/home/cocel/isaac/env_isaaclab/bin/python -m pytest -q \
  test/test_gluon_ik_math.py

timeout 300s env PYTHONUNBUFFERED=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  test/test_gluon_jacobian_runtime.py --headless
```

Hold and scripted Cartesian closed loop:

```bash
timeout 300s env PYTHONUNBUFFERED=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  lab/ddt_lab/scripts/gluon/run_gluon_keyboard_ik.py \
  --headless --max-steps 200 --final-error-limit-m 0.005

timeout 300s env PYTHONUNBUFFERED=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  lab/ddt_lab/scripts/gluon/run_gluon_keyboard_ik.py \
  --headless --max-steps 1200 \
  --scripted-target-offset-m -0.01 0.01 -0.01 \
  --final-error-limit-m 0.005
```

GUI smoke and operator command:

```bash
# finite GUI smoke used during implementation
/home/cocel/isaac/env_isaaclab/bin/python \
  lab/ddt_lab/scripts/gluon/run_gluon_keyboard_ik.py \
  --max-steps 200 --final-error-limit-m 0.005

# operator session
/home/cocel/isaac/env_isaaclab/bin/python \
  lab/ddt_lab/scripts/gluon/run_gluon_keyboard_ik.py
```

## Direct evidence

Pure math:

```text
10 passed
```

Jacobian finite-difference comparison at
`[5,-5,5,-5,5,0] deg`:

```text
raw_max_abs=1.09069936e-01
rotated_max_abs=3.61472368e-03
shifted_max_abs=6.06514513e-05
GLUON_JACOBIAN_RUNTIME: PASS,frame=base_link
```

q=0 hold:

```text
final_error_m=8.8695208e-07
joint_limit_violations=0
velocity_limit_violations=0
max_abs_q6_deg=0.000692607508
startup_command_delta_rad=0
GLUON_KEYBOARD_IK: PASS
```

Combined `[-10,+10,-10] mm` base-frame offset:

```text
final_error_m=0.0030695037
joint_limit_violations=0
velocity_limit_violations=0
max_command_slew_rad_s=0.349066406
max_abs_q6_deg=0.00121504653
GLUON_KEYBOARD_IK: PASS
```

Independent W0 direction cases after 1,000 physics steps:

| Case | Offset m | Final error mm | Result |
|---|---:|---:|---|
| +X | `[+0.003,0,0]` | 2.928 | `PASS` |
| -X | `[-0.010,0,0]` | 0.508 | `PASS` |
| +Y | `[0,+0.010,0]` | 0.531 | `PASS` |
| -Y | `[0,-0.010,0]` | 0.531 | `PASS` |
| +Z | `[0,0,+0.010]` | 0.609 | `PASS` |
| -Z | `[0,0,-0.010]` | 3.977 | `PASS` |

All six cases reported zero joint-limit and runtime velocity-limit violations,
command slew at or below 20 deg/s, and q6 below 0.002 deg.

The non-headless path created the real Isaac Sim keyboard device and status
window without API errors. A captured desktop frame was inspected directly:
the complete robot, dark ground plane, green target sphere, current EE frame,
and live status panel were visible. This proves rendering and UI creation, but
does not prove that an operator pressed each key.

An intentional impossible threshold (`--final-error-limit-m 1e-12`) printed
`FAIL` and returned shell status 1, proving that CI can observe a failed run.

## Debugging record

- System Python lacked PyTorch; tests were rerun in the explicit IsaacLab env.
- The first velocity watchdog read saw zero limits before the first actuator
  write. Initial position hold is now written before watchdog sampling.
- Root rotation alone did not make the COM Jacobian match the `link6` frame;
  the rigid-body point shift reduced error from `3.6e-3` to `6.1e-5`.
- Position-only q1--q5 leaves a two-dimensional nullspace. A q=0 posture term
  stopped gravity-driven redundancy drift without changing actuator gains.
- Cartesian gain 2.0 reduced the inner-PD gravity steady error below 5 mm while
  the 20 deg/s command slew remained active.

## Remaining operator acceptance

The following remains `NOT_TESTED` until the user runs the indefinite GUI
command and physically presses the keys:

- W/S, A/D, Q/E visually agree with base-frame marker directions
- R and H reset behavior
- SPACE target-update pause/resume
- ESC clean termination
- no objectionable visual oscillation during interactive use

No physical robot, ROS hardware bridge, SDK, actuator enable, or real command
was used.

## Repository completion check

Execution Domain: `DESKTOP_DRY_RUN`

After the completion-audit corrections, the repository gate reported:

```text
PASS: No whitespace or conflict-marker errors.
[TEST-FAST] Syntax Check Results: 288 passed, 0 failed.
[TEST-FAST] XML Parse Check: 8 URDF files OK.
PASS: docs/exp/ directory naming convention OK.
PASS: Code changes accompanied by experiment log entry in docs/exp/.
Final result: PASS
```

This gate does not replace the outstanding operator keyboard acceptance; the
overall P2-P3 evidence therefore remains `SUSPICIOUS` until the listed GUI keys
are manually exercised.
