# GLUON INNFOS Ethernet read-only probe

- Execution Domains: `ROBOT_READ_ONLY`, `ROBOT_STATE_CHANGING`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `SUSPICIOUS` (URDF axis 6 and the operator-observed physical
  configuration require reconciliation)
- Robot: GLUON 2L6-4L3
- SDK: INNFOS C++ SDK `3.2.0`

## Purpose

Verify the Ethernet/ECB/actuator discovery path and attempt to read raw sensor
feedback without enabling actuators, changing control modes, commanding motion
or torque, homing, clearing errors, or saving parameters.

## Network evidence

- Host interface: `enp3s0`
- Physical link: detected, `100 Mb/s`, full duplex
- Host IPv4: `192.168.1.100/24`
- NetworkManager profile: `gluon-readonly`, autoconnect disabled, never default
- ECB address returned by the SDK: `192.168.1.30`

Before the host IPv4 address was assigned, discovery returned `0x803` and zero
actuators. After assigning the dedicated address, discovery returned `0x0`.

## Observed behavior

- Six actuators were discovered with IDs `1` through `6`.
- All six reported online, disabled, mode `none`, and error code `0x0`.
- Synchronous position, velocity, current, voltage, motor-temperature, and
  inverter-temperature getters returned `0.0` for all actuators.
- Repeated explicit `requestCVPValue()` calls produced no current, velocity, or
  position callbacks for any actuator.
- Enabling host-side SDK auto-refresh polling at 100 ms during the process did
  not produce CVP callbacks.
- No actuator power-enable or robot command was issued during the read-only runs.

## Bounded ID 6 enable-for-read check

After explicit operator approval, actuator ID 6 alone was enabled without a
mode selection or position/current/velocity target. The arm was supported and
the operator remained ready at the emergency stop.

Observed asynchronous CVP feedback:

```text
current=-0.003132 A
velocity=0.712395 RPM
position=0.000427 turns
```

Observed synchronous feedback later in the same bounded run:

```text
position=0.000488 turns
velocity=5.227089 RPM
current=-0.003142 A
voltage=41.844727 V
motor_temperature=32.328125 degC
inverter_temperature=37.812500 degC
mode=current
error=0x0
```

The actuator returned `disable_after_read,id=6,success=1`. A separate subsequent
`ROBOT_READ_ONLY` run reported ID 6 as `enabled=0`, mode `none`, confirming the
disabled state. The nonzero velocity reading may represent a small physical
transient or estimator transient and must be treated as a safety-relevant
observation before enabling other joints.

## Minta Actuator Studio interference

An attempted ID 5 run initially failed before actuator enable because Minta
Actuator Studio (`AppRun`) owned the SDK UDP port `3030`. After Studio exited,
the port became available, but all six actuators were observed as `enabled=1`,
mode `current`. This state was attributed to the external Studio session rather
than the failed probe attempt.

`disableAllActuators()` returned `false`, while immediate per-actuator checks
reported IDs 1-6 as `enabled=0`. The per-actuator disabled state was used as the
safety result.

## IDs 1-5 sequential enable-for-read checks

Each remaining actuator was enabled alone, sampled, disabled, and confirmed as
`enabled=0` before advancing to the next ID. No control mode or target command
was sent.

| ID | Position (turns) | Velocity (RPM) | Current (A) | Voltage (V) | Motor temp (degC) | Inverter temp (degC) | Result |
|---:|---:|---:|---:|---:|---:|---:|:---|
| 1 | 8.854158 | 3.456116 | -0.029408 | 41.615234 | 31.074219 | 36.562500 | `PASS` |
| 2 | 0.720485 | 1.193047 | 0.023450 | 41.890625 | 29.894531 | 36.312500 | `PASS` |
| 3 | 12.965637 | 2.984047 | 0.028926 | 41.982422 | 32.699219 | 38.312500 | `PASS` |
| 4 | -1.008057 | -1.358986 | -0.003583 | 41.248047 | 33.281250 | 39.375000 | `PASS` |
| 5 | -0.048096 | 0.846863 | 0.007718 | 41.171875 | 32.003906 | 39.312500 | `PASS` |
| 6 | 0.000488 | 5.227089 | -0.003142 | 41.844727 | 32.328125 | 37.812500 | `PASS` |

All actuator errors were `0x0`. The velocity samples are short enable transients,
not steady-state motion measurements, and must not be used as calibration data.
A final command-free read reported IDs 1-6 as `enabled=0`, mode `none`.

## Simultaneous-enable manual sweep

- Execution Domain: `ROBOT_STATE_CHANGING`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `SUSPICIOUS`
- Raw data: `docs/exp/2026-08-04/gluon_joint_sweep.csv`
- Raw data SHA256: `73c7559a29767f33b532b4120d076e34a783807a6ba61ce58c20df5c56e34b36`

All six actuators were initially verified disabled, enabled together without a
mode selection or target command, and sampled at approximately 20 Hz. The
operator manually swept the arm for 111.782 seconds. The CSV contains 2,207
samples per actuator (13,242 data rows). Ctrl-C followed the operator's
completion signal; the cleanup path disabled all actuators and individually
verified IDs 1-6 as `enabled=0`.

The first received raw position was retained as the provisional visual-zero.
The extrema below are recomputed from the saved CSV, not inferred from the
URDF. Joint degrees use the provisional 36:1 conversion and do not yet include
joint direction signs.

| ID | Provisional zero (turns) | Min (turns) | Max (turns) | Span (turns) | Span at joint (deg) | Status |
|---:|---:|---:|---:|---:|---:|:---|
| 1 | 8.854813 | -6.676645 | 24.388829 | 31.065474 | 310.655 | `PASS` |
| 2 | 0.772385 | -10.001526 | 10.068814 | 20.070340 | 200.703 | `PASS` |
| 3 | 12.631287 | -2.692383 | 26.504089 | 29.196472 | 291.965 | `PASS` |
| 4 | -1.007996 | -14.908936 | 14.206421 | 29.115357 | 291.154 | `PASS` |
| 5 | -0.047729 | -14.468445 | 14.803894 | 29.272339 | 292.723 | `PASS` |
| 6 | 0.000244 | -0.002502 | 0.002319 | 0.004821 | 0.048 | `NOT_TESTED` |

ID 6 did not undergo a meaningful sweep. The operator reported that the current
physical configuration has no corresponding axis available to rotate, so ID 6
was explicitly excluded from this calibration. Its observed span is consistent
with stationary feedback noise and no ID 6 joint limit can be inferred. At
capture time, the referenced URDF still modeled `axis_joint_6` as revolute; the
model reconciliation below subsequently fixed it at q6=0 and removed it from
the active interface. IDs 1-5 are useful provisional raw bounds, but are not
yet deployable limits:
direction-to-URDF mapping, a safety margin, and collision-aware limit selection
remain unresolved.

## Result

```text
Ethernet physical link: PASS
ECB discovery: PASS
Six-actuator CAN discovery: PASS
Read-only CVP sensor feedback while actuators are disabled: SUSPICIOUS
ID 6 gated enable and CVP feedback: PASS
ID 6 disable and read-only state confirmation: PASS
IDs 1-5 sequential enabled-feedback validation: PASS
Simultaneous enable, 20 Hz CSV capture, and final disable: PASS
Manual sweep bounds for IDs 1-5: PASS (provisional)
Manual sweep bound for ID 6: NOT_TESTED (excluded by operator; no turnable physical axis)
Final IDs 1-6 disabled state: PASS
Minta Actuator Studio coexistence: BLOCKED (UDP port 3030 conflict)
Position/current/velocity target commands: none
```

The official SDK behavior observed here requires an actuator to be enabled
before CVP feedback is returned. Minta Actuator Studio and this probe cannot own
UDP port `3030` simultaneously. All future runs must close Studio first and
verify the initial enable state before any probe-managed enable.

## Five-DOF model reconciliation

- Execution Domain: `VALIDATION_SIM`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `PASS` for structural conversion; `NOT_TESTED` in Isaac Lab runtime

Following the operator's confirmation that the connected physical configuration
has no sixth rotary axis available, `axis_joint_6` was changed from `revolute`
to `fixed` at its q6=0 transform. The generator applies the change to both the
canonical and simulation URDFs. The active Isaac Lab joint list and bootstrap
contract now contain axes 1-5, with action dimension 5 and provisional
observation dimension 22. Fixed-joint merging is disabled for this asset so
`link6` remains available as the named end-effector body. This is incompatible
with policies exported against the earlier six-action interface.

```text
canonical URDF SHA256: 8c3c51af866782962d4335afbd48c5e1597c3b18a07827fe7655998ea4ac08f1
simulation URDF SHA256: 7ec33c22a73aaa68d7bd26e874be9207afe4bec95de9be04be49d694674f79b7
inertial audit: PASS
```

## Candidate all-limit reference pose

- Execution Domains: `ROBOT_STATE_CHANGING`, followed by `ROBOT_READ_ONLY`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `SUSPICIOUS` as an operational start pose; `PASS` as a
  provisional repeatable limit-reference capture
- Raw data: `docs/exp/2026-08-04/gluon_limit_start_pose.csv`
- Raw data SHA256: `f2b922453fc7598ed632c4552d2128a5eefd745d97dda7df0e8af34d67fda9a5`

The operator manually placed active joints 1-5 at one physical-limit side and
requested that pose as a possible start pose. All actuators were initially
disabled. They were enabled together for three seconds of feedback capture,
without a target or mode command, and were then disabled and individually
verified as `enabled=0`.

| ID | Mean position (turns) | Observed span over 2.958 s (turns) | Distance from prior matching sweep extreme (joint deg, 36:1) |
|---:|---:|---:|---:|
| 1 | 24.385013 | 0.000487 | 0.038 |
| 2 | -9.951151 | 0.000424 | 0.504 |
| 3 | -2.645052 | 0.000367 | 0.473 |
| 4 | -14.783711 | 0.000428 | 1.252 |
| 5 | 14.654906 | 0.000427 | 1.490 |
| 6 | 0.000261 | 0.000427 | N/A (fixed/excluded) |

ID 1 reported error `0x80` during the final synchronous sample, which the SDK
defines as an actuator CAN communication error. A subsequent disabled,
command-free read reported IDs 1-6 online with error `0x0`; therefore this is
treated as a transient requiring recurrence monitoring, not as a physical-limit
indicator.

This pose is suitable as a provisional homing/reference anchor because it lies
close to the previously observed extrema. It is not accepted as an operational
control or RL reset pose: joints at hard stops have effectively no safety
margin in one direction. A separate inward-offset start pose must be measured
and validated before state-changing control.

## HOMING_A repeatability sweep

- Execution Domains: `ROBOT_STATE_CHANGING`, followed by `ROBOT_READ_ONLY`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `PASS` for full-range capture; `SUSPICIOUS` for homing
  repeatability
- Raw data: `docs/exp/2026-08-04/gluon_homing_repeatability_sweep.csv`
- Raw data SHA256: `758e022ac776dfdf4d4b2fbe580cfaafd6400ef71f1a16a61d8bcc4edfa6bf5e`

Starting at the candidate all-limit `HOMING_A` pose, the operator manually
moved active joints between HOMING_A and their opposite limits. The run lasted
177.532 seconds and contains 3,505 samples per actuator (21,030 data rows).

| ID | Minimum (turns) | Maximum (turns) | Full span (turns) | Joint span at 36:1 (deg) |
|---:|---:|---:|---:|---:|
| 1 | -6.653128 | 24.436944 | 31.090072 | 310.901 |
| 2 | -10.055854 | 10.161151 | 20.217005 | 202.170 |
| 3 | -2.718872 | 26.534729 | 29.253601 | 292.536 |
| 4 | -14.996887 | 14.307129 | 29.304016 | 293.040 |
| 5 | -14.360779 | 14.710266 | 29.071045 | 290.710 |
| 6 | -0.003723 | 0.002197 | 0.005920 | 0.059 (fixed/excluded) |

Heuristic endpoint-visit analysis found that the HOMING_A-side returns for IDs
1, 3, and 4 generally clustered within approximately 0.2-0.5 joint degrees
after incomplete approaches were excluded. ID 2 showed approximately 1.4
degrees of spread, while ID 5 did not contain enough clearly completed HOMING_A
returns to validate repeatability. Because the continuous log has no explicit
operator event markers, incomplete approaches cannot be separated from true
hard-stop contacts without heuristic filtering. The HOMING_A offsets therefore
remain provisional. A subsequent per-joint run must record an explicit button
or Enter event at every lightly contacted stop.

The recording cleanup individually verified IDs 1-6 as `enabled=0`. A
subsequent command-free read reported all six online, mode `none`, and error
`0x0`.

## ID1 marked five-cycle homing run

- Execution Domain: `ROBOT_STATE_CHANGING`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `PASS` for provisional motor-encoder hard-stop repeatability
- Raw data: `docs/exp/2026-08-04/gluon_id1_homing_cycles.csv`
- Raw data SHA256: `d4b4482e0f1248c29975a765453616cdb71cb2b6ab38680f8b332e8d2771eea7`

Only physical joint 1 was moved while all actuator feedback was recorded. The
79.127-second log contains 1,563 samples per actuator. Six visits to each side
were detected: the initial endpoint acquisition plus five complete A-B cycles.

| Endpoint | Role | Median (turns) | Visit peak-to-peak (turns) | Joint equivalent at 36:1 (deg) |
|:---|:---|---:|---:|---:|
| Upper | `HOMING_A` | 24.388589 | 0.034411 | 0.344 |
| Lower | Opposite B | -6.627420 | 0.031613 | 0.316 |

The median-to-median range is 31.016009 motor turns, or 310.160 joint degrees
under the provisional 36:1 ratio. The result supports adopting 24.388589 turns
as the provisional ID1 HOMING_A motor-encoder anchor. It does not measure
gearbox/output-link backlash or establish the URDF direction sign. No target,
mode, homing-save, or parameter-save command was issued. Cleanup verified IDs
1-6 as `enabled=0`.

The operator subsequently confirmed that physical A-to-B motion is
counterclockwise when viewed from above. Because raw turns decrease from A to B
while URDF positive joint-1 rotation is counterclockwise, the calibrated ID1
direction is `-1`. The midpoint zero is 8.8805845 turns, only 0.258 joint
degrees from the earlier visual-zero estimate. The generated URDF now uses
`[-2.584484342, 2.584484342] rad`, seven degrees inside the measured mechanical
stops at approximately `+/-2.706657389 rad`. The staged mapping is recorded in
`tita_gluon_ws/src/gluon/config/gluon_calibration.yaml` and remains marked
partial until IDs 2-5 are completed.

## Current turns snapshot after ID1 calibration

- Execution Domain: `ROBOT_STATE_CHANGING`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `PASS` for position capture and cleanup; `SUSPICIOUS` for
  recurring ID1 error `0x80`
- Raw data: `docs/exp/2026-08-04/gluon_current_turns_snapshot.csv`
- Raw data SHA256: `5d623e57922787de296a98f84bf2f7ad7a8fca66961ce8694ad3f6b4945c624e`

The stationary two-second snapshot reported ID1-6 positions of 24.387054,
-9.989212, -2.645142, -14.783630, -14.168030, and 0.000122 motor turns,
respectively. ID1 again reported the SDK actuator CAN communication error
`0x80` during the final synchronous sample. Feedback remained available and
cleanup individually verified IDs 1-6 as `enabled=0`.

## ID1 firmware controller configuration

- Execution Domains: `ROBOT_READ_ONLY`, then `ROBOT_STATE_CHANGING` for an
  explicitly acknowledged single-actuator parameter refresh
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `PASS` for enabled parameter refresh and cleanup;
  `SUSPICIOUS` for the disabled-cache result

Reading ID1 while disabled returned zeros for nearly all parameters except the
6000 RPM velocity range, indicating an unrefreshed SDK cache rather than zero
controller gains. ID1 was then enabled without a mode or target command, the
configuration was refreshed, and ID1 was immediately disabled and verified as
`enabled=0`.

```text
position loop: Kp=0.349999964, Ki=0, Kd=0
position output: Umax=0.998999953, Umin=-0.998999953
velocity loop: Kp=5.0, Ki=0.009999931
velocity output: Umax=0.665999949, Umin=-0.665999949
current loop: Kp=0.309999943, Ki=0.080999970
profile position: acceleration=1200, deceleration=-1200, max_velocity=3000
velocity range/limit: 6000 / 4199.999928 RPM
current range/limit: 33 / 16.5 A
drive position limit enabled: false
stored drive position limits: [-14, 14] motor turns
filters enabled: false
reported cutoff values: 0.00390625
```

The SDK exposes a cascaded position PID, velocity PI, and current PI structure.
The header does not document gain normalization or loop sample periods, so the
gain values are firmware settings rather than directly portable SI gains. The
saved 3000 RPM profile velocity and 16.5 A current limit are not accepted for a
first physical move. No control gain, limit, mode, target, homing, or saved
parameter was modified during this inspection.

The operator confirmed that the current physical poses for joints 2-5 match
negative URDF joint values. Because their current raw turns are below the
recorded visual-zero turns, IDs 2-5 use `direction=+1`; together with ID1 this
gives `[-1, +1, +1, +1, +1]`. The measured hard-stop ranges were converted
through the 36:1 ratio and the generated URDF limits were placed seven degrees
inside each hard stop. IDs 2-5 remain `provisional_from_sweep` because their
zero references are visual rather than externally metrologized.

The operator selected the all-negative-limit configuration as the hardware
HOMING convention to preserve a convenient future gripper configuration. The
encoder references are ID1 raw maximum and IDs 2-5 raw minima: 24.388589,
-10.055854, -2.718872, -14.996887, and -14.360779 turns. This HOMING pose is
defined only for encoder referencing and must not be used directly as an RL
reset or commanded startup pose because it lies at the mechanical stops.

## First bounded ID1 commanded step

- Execution Domains: `DESKTOP_DRY_RUN`, `ROBOT_STATE_CHANGING`, followed by
  `ROBOT_READ_ONLY`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `FAIL` for reaching the target; `PASS` for watchdog abort
  and final disabled-state verification

The bounded-step utility was built successfully. Its dry run passed, a 6 RPM
request was rejected by the 5 RPM hard gate, and an execution request missing
the second acknowledgement was rejected before SDK initialization.

With explicit operator approval, ID1 alone was commanded from the measured
24.356570-turn start toward 23.688589 turns. Temporary unsaved settings read
back as 5 RPM profile maximum velocity, +/-10 profile acceleration/deceleration,
and a 0.5 A current limit. The intended step was -0.7 motor turns, equivalent
to approximately +7 degrees at the output joint under the calibrated ID1 sign.

The position reached 24.347478 turns, only about 0.0091 motor turns from the
measured start, before the drive reported `0x80`. The SDK defines this as
`ERR_CAN_COMMUNICATION`. Peak observed current magnitude before the abort was
0.220604 A, below both the 0.4 A watchdog threshold and 0.5 A temporary limit.
The utility immediately stopped and reported `scope_disable,success=1`; it did
not retry or continue toward URDF zero.

A separate command-free discovery afterward found all six actuators online,
`enabled=0`, mode `none`, and error `0x0`. Disabled actuators still did not
return fresh CVP callbacks, so the post-check's sensor-feedback result remains
`SUSPICIOUS`, while the final disabled state is `PASS`. Because ID1 `0x80` also
appeared in earlier stationary captures, no further commanded motion should be
attempted until the ID1-to-ECB CAN communication path is diagnosed.

## ID1 communication-layer isolation test

- Execution Domains: `ROBOT_READ_ONLY`, `ROBOT_STATE_CHANGING`, followed by
  `ROBOT_READ_ONLY`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `PASS` for Ethernet, discovery, active ID1 feedback, and
  final disable; `SUSPICIOUS` for the unreproduced intermittent `0x80`

The host-to-ECB Ethernet path returned 50 of 50 ICMP replies with 0% loss and
0.123 ms average round-trip time. The link negotiated at 100 Mb/s full duplex.
Five independent SDK discovery processes each returned `discovery_error=0x0`
and exactly IDs 1-6. NIC RX/TX error and drop counters did not increase during
the repeated discovery test. Minta Actuator Studio was not running and UDP port
3030 was unoccupied.

With explicit operator approval, ID1 alone was enabled for feedback without a
mode selection or position, velocity, or current target. Asynchronous CVP was
complete and six synchronous samples all reported online, enabled, current
mode, and `error=0x0`. Position remained between 24.356085 and 24.356327 turns;
observed current remained between -0.020409 and 0.041428 A. The apparent
instantaneous velocity estimator ranged from -5.244255 to 5.481720 RPM despite
the negligible position span and is not interpreted as physical sustained
motion. Cleanup returned `disable_after_read,success=1` and verified ID1
`enabled=0`.

A final independent command-free check found IDs 1-6 online, disabled, mode
`none`, and error `0x0`; NIC drop counters again remained unchanged. The test
therefore does not support a persistent Ethernet failure or a persistent ID1
CAN disconnection. Because `0x80` appeared during the earlier profile-position
command and in some earlier stationary captures, it remains an intermittent or
transaction-dependent fault. The next diagnostic should isolate profile-mode
activation from target transmission instead of repeating the full move.

## ID1 zero-displacement Profile Position hold

- Execution Domains: `DESKTOP_DRY_RUN`, `ROBOT_STATE_CHANGING`, followed by
  `ROBOT_READ_ONLY`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `PASS` for safety writes, pre-mode target, Profile Position
  activation, five-second hold, and final disable; `SUSPICIOUS` for velocity
  feedback and the still-unisolated nonzero-target transaction

The bounded-step tool gained a `--diagnostic-hold-s` path that requires a zero
planned step, uses the freshly measured position as its hold target, and checks
errors after each setup phase. Build, zero-step dry run, nonzero-step rejection,
and the original move dry-run regression all passed.

With explicit operator approval, ID1 started at 24.356206 turns. Temporary,
unsaved safety parameters read back as a 0.5 A current limit, +/-10 profile
acceleration/deceleration, and 5 RPM maximum profile velocity. Error status was
`0x0` after the safety writes, after writing the current position before the
mode switch, and after activating Profile Position and rewriting the same hold
target.

During the five-second hold, position stayed between 24.355782 and 24.356631
turns, a 0.000849-turn span or approximately 0.0085 output-joint degrees at
36:1. Peak current magnitude was 0.362618 A, below the 0.4 A abort threshold.
Every sampled error code was `0x0`. The velocity getter nevertheless ranged
from -12.908936 to +8.148193 RPM despite negligible encoder displacement, so
instantaneous SDK velocity must not yet be used as a reliable safety or RL
observation without filtering and timestamp validation.

The utility verified ID1 `enabled=0` after the hold. A subsequent independent
command-free check found IDs 1-6 online, disabled, mode `none`, and error `0x0`.
This result excludes the safety-parameter writes, current-position target
write, and Profile Position activation/hold as deterministic causes of `0x80`.
The remaining controlled test is a very small nonzero target step; the earlier
full -0.7-turn request must not be repeated until that smaller transaction is
validated.

## ID1 inward soft-limit move retry after cable-slack adjustment

- Execution Domains: `DESKTOP_DRY_RUN`, `ROBOT_STATE_CHANGING`, followed by
  `ROBOT_READ_ONLY`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `PASS` for target tolerance, error monitoring, and final
  disable; `SUSPICIOUS` for the single-run cable-tension hypothesis

The operator observed that the actuator CAN cable may have been pulled during
the failed attempt, adjusted the cable slack, and explicitly requested another
bounded move to the same seven-degree-inside soft-limit target. Because the
first attempt had already moved slightly inward, the measured start was
24.356085 turns and the fixed target remained 23.688589 turns, an intended
remaining move of approximately 6.68 output-joint degrees. The dry run passed.

ID1 alone was enabled with the same temporary unsaved 0.5 A current limit,
5 RPM profile maximum velocity, and +/-10 acceleration/deceleration. Safety
parameter writes, the pre-mode current-position target, and Profile Position
activation all reported `error=0x0`. Motion proceeded without any `0x80` and
stopped at 23.700236 turns after satisfying the three-sample +/-0.02-turn target
tolerance. This is 0.011647 motor turns, or approximately 0.116 output-joint
degrees, above the requested target. The measured displacement from the fresh
start was -0.655849 motor turns, or approximately 6.558 output-joint degrees.

Peak observed current magnitude was approximately 0.452 A, below the 0.5 A
temporary limit. Samples above the 0.4 A watchdog threshold were not
consecutive, so the two-hit abort rule did not trigger. The SDK velocity getter
again produced magnitudes well above the configured 5 RPM profile limit and is
not accepted as reliable instantaneous velocity evidence.

The utility verified ID1 `enabled=0` after reaching tolerance. A separate
command-free check found IDs 1-6 online, disabled, mode `none`, and error `0x0`.
The successful run is consistent with the operator's cable-tension hypothesis,
but one failure followed by one success does not establish causality. Cable
strain relief and repeated low-risk motion cycles are required before relying
on the connection for full-range homing or closed-loop RL operation.

## ID1 direct move to calibrated URDF zero

- Execution Domains: `DESKTOP_DRY_RUN`, `ROBOT_STATE_CHANGING`, followed by
  `ROBOT_READ_ONLY`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `PASS` for existing-gain position tracking and final disable;
  `SUSPICIOUS` for unvalidated velocity feedback and the mechanism-wide safety
  of the operator-selected 10 A ceiling

The operator clarified that the objective was to test whether the actuator's
existing firmware position-controller gains track a reference and to place ID1
at calibrated URDF zero. No position, velocity, or current-loop gain was changed
or saved during this sequence.

An initial ten-degree staged move with a 0.5 A drive limit was aborted by the
additional 0.4 A two-consecutive-sample watchdog after approximately 1.18
degrees. Repeating with 2 RPM and lower acceleration also hit that software
threshold. Both runs reported `error=0x0`, executed their scope disable, and
were followed by disabled-state verification. The operator correctly identified
the 0.4 A software threshold as overly conservative relative to the drive
limit. Disabling only that extra watchdog allowed a full ten-degree move to
complete under the 0.5 A drive limit.

At the operator's explicit request, the temporary unsaved drive current limit
was then set to 10 A and read back as 10 A. A separate 2 A two-sample software
watchdog remained active. The saved firmware limit observed before this test was
16.5 A and the SDK-reported current range was 33 A; these electrical values do
not by themselves establish a mechanically safe continuous current. Four
approximately 10.48-degree stages completed with `error=0x0`; observed peak
current in their complete logs remained below approximately 0.61 A.

From a fresh measured start of 18.322324 turns, ID1 received the calibrated
zero reference 8.8805845 turns as one direct Profile Position target. Temporary
settings read back as 10 A current limit, 10 RPM maximum profile velocity, and
+/-10 acceleration/deceleration. The move traversed approximately 94.4 output-
joint degrees and completed with every sampled drive error equal to `0x0`. The
full-rate internal 2 A current watchdog did not trigger. Console motion rows
were thinned for operator readability, so their displayed subset must not be
used to claim an exact peak current for this direct move.

A separate enable-for-read verification measured ID1 at 8.893297 turns. This is
0.012713 motor turns, or approximately 0.127 output-joint degrees, from the
calibrated zero. That verification disabled ID1 successfully. A final independent
command-free check found IDs 1-6 online, disabled, mode `none`, and error `0x0`.
The result supports using the existing firmware gains with position references
for ID1 bring-up; it does not yet validate the noisy instantaneous velocity
feedback, the other joints, continuous 10 A operation, or RL deployment.

## ID2 local tracking diagnostic

- Execution Domains: `ROBOT_STATE_CHANGING`, followed by `ROBOT_READ_ONLY`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `PASS` for -5 and 0 degree tracking and cleanup;
  `SUSPICIOUS` for the interrupted +5 degree stage

With IDs 1-5 initially near model zero, the calibrated multi-joint controller
held IDs 1, 3, 4, and 5 at zero while commanding ID2 through -5, 0, and +5
degrees. The -5-degree stage reached 0.271533 turns against a 0.272385-turn
target, and the zero-degree stage reached 0.771293 turns against a
0.772385-turn target. Sampled peak ID2 currents were 0.404231 A and 0.423882 A,
respectively. Both stages completed their two-second holds and verified IDs
1-5 disabled.

Before the +5-degree command was sent, the operator manually moved ID2. The
next enable therefore measured 10.409949 turns and the initial-state gate
rejected the resulting 91.376-degree planned step. No +5-degree target was
sent. Cleanup output and a separate command-free probe confirmed IDs 1-5
disabled and all six drives online with error `0x0`.

## ID2-ID4 marked five-cycle homing run

- Execution Domain: `ROBOT_STATE_CHANGING`, followed by `ROBOT_READ_ONLY`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `PASS` for ID3 and selected-axis cleanup; `SUSPICIOUS` for
  ID2 and ID4 endpoint repeatability
- Raw data: `docs/exp/2026-08-04/gluon_id234_homing_cycles_raw.log`
- Raw data SHA256: `025faa70f06bc6cf8cd1607822f1c17b1675ade6e8477d61b6c2bdfdefc32fbd`

The selected-feedback logger enabled only IDs 2, 3, and 4. IDs 1, 5, and 6
remained disabled. The operator manually traversed all three selected joints
between their lightly contacted physical stops five times. The log contains
120 synchronized samples per selected actuator over approximately 104 seconds,
with no nonzero drive error rows. Peak sampled absolute currents were 0.130690
A, 0.096938 A, and 0.110969 A for IDs 2, 3, and 4, respectively.

| ID | Endpoint | Visits | Median (turns) | Visit peak-to-peak (joint deg) |
|---:|:---|---:|---:|---:|
| 2 | Negative/HOMING_A | 5 | -9.801316 | 3.1084 |
| 2 | Positive/B | 5 | 10.361084 | 1.9865 |
| 3 | Negative/HOMING_A | 5 | -2.632019 | 0.3733 |
| 3 | Positive/B | 5 | 26.492536 | 0.3121 |
| 4 | Negative/HOMING_A | 5 | -14.784180 | 1.4244 |
| 4 | Positive/B | 5 | 14.207440 | 0.0110 |

The updated zero candidates apply the mean shift of the two endpoint medians
relative to the earlier sweep, preserving the prior physical-stop asymmetry:
ID2 0.9996205 turns, ID3 12.6536170 turns, and ID4 -0.9514870 turns. Mechanical
limits and seven-degree-inset URDF soft limits were regenerated from these
anchors. ID3 is marked `provisional_pass`. ID2 remains provisional because its
five-cycle spread is approximately 2-3 degrees, and ID4 remains provisional
because one negative-side visit appears incompletely seated. These encoder
measurements do not measure output-link backlash.

Normal Ctrl-C cleanup reported `post_disable_state=0` for IDs 2-4 and
`SENSOR_READ_PASS`. A subsequent command-free probe independently reported all
six actuators online, disabled, mode `none`, and error `0x0`; disabled-state CVP
values remain unavailable through this SDK and are therefore reported as
`SUSPICIOUS`, not as calibration samples.

Two subsequent all-zero multi-joint attempts stopped immediately after their
first printed motion sample with the generic `actuator error during multi-joint
motion` watchdog result. All printed per-axis samples had error `0x0` and less
than 0.05 A current, and cleanup verified IDs 1-5 disabled. A command-free
follow-up found all six drives online, disabled, and reporting error `0x0`.
Because the motion logger printed only every fifth cycle, the responsible ID
and transient code were not preserved. The failure path was therefore amended
to print the exact ID, position, target, current, and nonzero error code before
throwing; no watchdog threshold or state-changing behavior was relaxed.

A repeat run identified `ID4 error=0x200`, which the bundled SDK defines as
`ERR_STEP_OVER`. ID4 was asked to move from 0.351562 to -0.951487 motor turns in
one target update. A later attempt with an eight-degree host-side total-step
gate correctly stopped before mode activation because manually positioned ID2
was at -109.329798 joint degrees while the requested zero was more than eight
degrees away. Cleanup again verified IDs 1-5 disabled.

The multi-joint controller now divides an accepted total move into synchronized
five-degree waypoints by default, waits for every joint to settle at each
waypoint, and retains the existing error, current, overshoot, timeout, and final
disable checks. The drive's step-over protection is not cleared or modified.
The total displacement gate remains controlled separately by
`--max-joint-step-deg`, and the waypoint size may be reduced but not increased
above ten degrees with `--waypoint-step-deg`. Build and all-zero desktop dry-run
evidence are `PASS`; segmented execution on hardware is `NOT_TESTED`.

The first one-degree segmented hardware attempt still produced
`ID3 error=0x200` for a 0.100232-turn first target increment. This contradicts
the bundled SDK's Profile Position examples, which issue targets separated by
10-30 turns, so target magnitude alone does not explain the fault. Those SDK
examples exclusively call the single-actuator `activateActuatorMode()` API;
none demonstrates the batch mode-activation overload used by the initial
multi-joint controller. The controller was aligned with the demonstrated SDK
sequence: each active actuator is now switched to Profile Position separately,
immediately assigned its measured current-position target, and checked for
mode, error, and position consistency before any trajectory waypoint is sent.
Batch enable and fail-safe multi-axis disable behavior are unchanged. This
change is `PASS` for build and desktop dry-run and `NOT_TESTED` on hardware.

Individual mode activation moved the failure earlier into the hold gate and
identified ID2 reporting `0x200` while its measured position changed by only
0.000061 turns. Enabled configuration reads then exposed a position-range
mismatch: ID1 was at 24.15 turns with a stored maximum of 14, ID2 was at -9.98
turns with a stored minimum of -9, and ID4 was at -14.78 turns with a stored
minimum of -14. The controller now offers an explicit unsaved temporary-range
expansion for this case. It expands only enough to contain each measured
start-to-target path plus 0.5 turns, verifies the result without enabling the
position-limit flag, and never calls a save API. Hardware validation of this
recovery path remains `NOT_TESTED`.

After the operator visually approved the resulting link-2 model-zero pose, a
selected ID2 feedback capture measured 0.199681, 0.199494, 0.199618, 0.199618,
and 0.199681 turns. The median 0.199618 turns is adopted as the new ID2 zero;
the five-sample peak-to-peak is 0.000187 turns, or approximately 0.0019 output-
joint degrees. The previously measured stop medians then map to mechanical
limits of -100.009340 and +101.614660 degrees. Applying the existing seven-
degree inset gives updated URDF soft limits of -93.009340 and +94.614660
degrees. ID2 was individually disabled and verified after capture. This is a
visual-zero calibration and remains `SUSPICIOUS` with respect to external
metrology and output-link backlash.

The operator then approved the simultaneous model-zero pose of links 3-5. Five
selected-feedback samples gave median zero anchors of 12.354797 turns for ID3,
-0.220703 turns for ID4, and 0.214417 turns for ID5. Their sample peak-to-peak
spreads were 0.000244, 0.000244, and 0.000306 turns, respectively (at most
approximately 0.0031 output-joint degrees). IDs 3-5 were individually disabled
and verified after capture.

Using the existing stop medians, these visual zeros produce mechanical ranges
of [-149.868160, +141.377390] degrees for ID3, [-145.634770, +144.281430]
degrees for ID4, and [-145.751960, +144.958490] degrees for ID5. The regenerated
seven-degree-inset URDF limits are [-142.868160, +134.377390], [-138.634770,
+137.281430], and [-138.751960, +137.958490] degrees, respectively. These remain
visual-zero calibrations without external metrology or output-link backlash
measurement.

To support a separately acknowledged fast-return experiment, the multi-joint
argument gates now permit at most 120 motor RPM, 300 RPM/s acceleration, and a
180-degree direct waypoint only when `--confirm-high-speed-profile` is present.
The original 10 RPM, 10 RPM/s, and ten-degree-or-smaller envelope remains valid
without that acknowledgement. At 36:1, 120 motor RPM corresponds to 20 output-
joint degrees per second. The idealized full 153-degree motion time is about
eight seconds at 300 RPM/s acceleration, excluding settling and communication
overhead. Build and desktop argument-gate tests are `PASS`; high-speed hardware
execution is `NOT_TESTED` and remains a staged operator experiment.

The operator subsequently refined only link 3's visual-zero pose. Five ID3-only
feedback samples measured 12.069763, 12.069946, 12.069824, 12.069824, and
12.070190 turns. Their median, 12.069824 turns, replaces the previous ID3 zero;
the 0.000427-turn spread is approximately 0.0043 output-joint degrees. The
existing stop medians now map to mechanical limits of -147.018430 and
+144.227120 degrees, with seven-degree-inset URDF limits of -140.018430 and
+137.227120 degrees. ID3 was disabled and verified after capture. This remains
a visual calibration without external metrology.

## Multi-joint calibrated pose controller dry run

- Execution Domain: `DESKTOP_DRY_RUN`
- Policy Checkpoint SHA256 / ONNX Hash: `N/A` (no policy was loaded)
- Evidence Status: `PASS` for build and argument/configuration gates;
  `NOT_TESTED` on robot hardware

A standalone C++ controller was added at
`tita_gluon_ws/src/gluon/src/innfos_multi_joint_pose.cpp`. It loads active-joint
calibration from `tita_gluon_ws/src/gluon/config/gluon_calibration.yaml`, accepts
five URDF joint targets in degrees, converts them to raw motor turns, and keeps
IDs 1-5 enabled in Profile Position hold until a duration expires or the
operator presses Ctrl-C. ID 6 is not enabled or commanded.

The all-zero dry run produced the calibrated targets 8.8805845, 0.772385,
12.631287, -1.007996, and -0.047729 motor turns for IDs 1-5. A joint-1 target of
149 degrees was rejected because it exceeds the calibrated +148.080045-degree
soft limit. An execution request missing the second physical-motion
acknowledgement was rejected before SDK initialization. The executable built
with `-Wall -Wextra -Wpedantic` and the repository SDK 3.2.0.

The implemented state-changing path requires exactly six discovered and
initially disabled actuators, batch-enables only IDs 1-5, captures and commands
the measured current pose before batch Profile Position activation, checks the
configured per-run maximum joint displacement, monitors per-axis current,
position overshoot, drive errors and timeout, and individually verifies all
five disabled states on exit. No controller gain, homing, or saved parameter is
changed. Hardware execution remains `NOT_TESTED`; the program provides only
joint-limit checking and has no geometric collision checker.
