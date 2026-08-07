# GLUON INNFOS read-only probe

Standalone C++ discovery and sensor probe for the INNFOS GLUON arm. ROS 2 is
intentionally not involved at this stage.

Measured motor-to-URDF offsets, directions, and staged joint limits are stored
in `config/gluon_calibration.yaml`. Entries marked `pending` or a top-level
`partial_measurement_only` status must not be used for state-changing control.
The hardware HOMING convention places active joints 1-5 at their negative URDF
mechanical-limit references. This is an encoder-reference pose, not an RL reset
or commanded startup pose.

Execution domain: `ROBOT_READ_ONLY`

By default, the executable calls Ethernet discovery and read APIs only. It
temporarily enables host-side SDK feedback polling during the process, then
turns that polling off. The default path does **not** call actuator power
enable/disable, mode changes, position/current/velocity commands, homing, error
clearing, actuator parameter setters, or parameter saving.

An explicitly gated selected-actuator enable path exists only for the case where
the SDK will not return feedback from disabled actuators. It requires both
one or more repeated `--enable-for-read ID` arguments and
`--confirm-enable-may-move`, refuses an actuator that was already enabled,
never selects a mode or target, and performs best-effort disable of every
selected actuator on every normal or exception exit.

An explicitly gated calibration logger can enable all discovered actuators at
once without selecting a mode or sending a target. It refuses to start unless
every actuator is initially disabled, records raw CVP feedback to CSV at about
20 Hz, and disables all actuators on normal completion, Ctrl-C, or exception.

## Build

Build outside the source tree:

```bash
cmake -S tita_gluon_ws/src/gluon -B /tmp/gluon_innfos_readonly_build
cmake --build /tmp/gluon_innfos_readonly_build --parallel
```

The CMake target links the repository copy of:

```text
sdk/innfos-cpp-sdk/sdk/lib/linux_x86_64/libActuatorController.so
```

## Run

The bundled SDK broadcasts to `192.168.1.255`. For the direct cable used in the
2026-08-04 read-only check, NetworkManager was configured with a dedicated host
address and no default route:

```bash
nmcli connection add type ethernet ifname enp3s0 con-name gluon-readonly \
  connection.autoconnect no ipv4.method manual \
  ipv4.addresses 192.168.1.100/24 ipv4.never-default yes ipv6.method disabled
nmcli connection up gluon-readonly
```

Run the `connection add` command only if that profile does not already exist.
The observed ECB address was `192.168.1.30`.

Start with a bounded one-sample probe:

```bash
timeout 30s /tmp/gluon_innfos_readonly_build/gluon_innfos_readonly_probe
```

Collect five samples at 200 ms intervals:

```bash
timeout 30s /tmp/gluon_innfos_readonly_build/gluon_innfos_readonly_probe \
  --samples 5 --period-ms 200
```

Read an actuator's firmware loop gains, output limits, position limits, and
profile-position settings without enabling it:

```bash
/tmp/gluon_innfos_readonly_build/gluon_innfos_readonly_probe \
  --read-controller-config 1
```

Some firmware parameters refresh only while the actuator is enabled. With the
arm supported and the operator ready at the emergency stop, the explicitly
acknowledged variant enables only the requested actuator, reads configuration,
and immediately disables it without selecting a mode or target:

```bash
/tmp/gluon_innfos_readonly_build/gluon_innfos_readonly_probe \
  --read-controller-config 1 --confirm-enable-may-move
```

When the arm is supported, the workspace is clear, the emergency stop is ready,
and the operator explicitly authorizes a state-changing check, enable one or
more selected actuators for the bounded read:

```bash
timeout -k 5s 20s /tmp/gluon_innfos_readonly_build/gluon_innfos_readonly_probe \
  --samples 1 --enable-for-read 6 --confirm-enable-may-move
```

For example, a synchronized manual-feedback capture for IDs 2-4 repeats the
selection option:

```bash
/tmp/gluon_innfos_readonly_build/gluon_innfos_readonly_probe \
  --samples 900 --period-ms 200 \
  --enable-for-read 2 --enable-for-read 3 --enable-for-read 4 \
  --confirm-enable-may-move
```

The process prints `disable_after_read,...,success=1` when the requested disable
is acknowledged. If it does not, use the physical emergency stop.

If an external application leaves actuators enabled, support the entire arm and
use the explicitly acknowledged disable-only path:

```bash
timeout -k 5s 20s /tmp/gluon_innfos_readonly_build/gluon_innfos_readonly_probe \
  --disable-all --confirm-disable-may-drop
```

The tool checks every discovered actuator after the command. The bundled SDK
may return `false` from the aggregate disable call even when every individual
actuator reports `enabled=0`; individual post-disable states are authoritative
for this diagnostic.

## Bounded position step

`gluon_innfos_safe_position_step` is a deliberately narrow bring-up utility,
not a general robot controller. Without both execution acknowledgements it
only prints the plan. Its hard-coded argument gates allow at most 10 RPM,
10 RPM/s profile acceleration, 10 A current limit, and a 120-second timeout.
It refuses to run if any actuator is initially enabled, enables only the
selected actuator, aborts on a drive error/current threshold/overshoot/timeout,
and verifies disable after a successful move. It never saves parameters or
invokes firmware homing.

The executable limits are input ceilings, not recommended defaults. A current
limit above the initially validated 0.5 A requires an explicit operator decision
for the connected mechanism. Setting `--current-abort-a 0` disables only the
additional software two-sample current watchdog; the drive current limit,
drive-error, position-overshoot, timeout, and disable guards remain active.

Dry-run the first ID1 inward step from `HOMING_A`:

```bash
/tmp/gluon_innfos_readonly_build/gluon_innfos_safe_position_step \
  --id 1 --expected-start-turns 24.388589 --target-turns 23.688589 \
  --max-start-error-turns 0.25 --max-step-turns 0.75 \
  --profile-max-rpm 5 --profile-acceleration 10 \
  --current-limit-a 0.5 --current-abort-a 0.4 --timeout-s 20
```

Physical execution additionally requires both `--execute` and
`--confirm-robot-may-move`. Before using them, support the arm, clear its sweep
volume, keep the emergency stop ready, close Minta Actuator Studio, and obtain
explicit operator approval for that exact move. A failed run must be followed
by an independent disabled-state check; do not retry an actuator communication
error automatically.

To isolate Profile Position activation without requesting displacement, set
the expected and target turns to the same current value and add a bounded hold
duration. The utility uses the freshly measured start as the actual hold target,
checks for errors after the safety-parameter writes and pre-mode target write,
then monitors position, current, and drive errors throughout the hold:

```bash
/tmp/gluon_innfos_readonly_build/gluon_innfos_safe_position_step \
  --id 1 --expected-start-turns 24.3562 --target-turns 24.3562 \
  --max-start-error-turns 0.25 --max-step-turns 0.05 \
  --profile-max-rpm 5 --profile-acceleration 10 \
  --current-limit-a 0.5 --current-abort-a 0.4 --timeout-s 20 \
  --diagnostic-hold-s 5
```

`--diagnostic-hold-s` is capped at 20 seconds and is rejected unless the
planned step is zero. The physical acknowledgements remain mandatory for
execution.

## Multi-joint calibrated pose controller

`gluon_innfos_multi_joint_pose` commands active joints 1-6 together and keeps
all six in Profile Position hold after they reach the target. It reads
`config/gluon_calibration.yaml` at runtime, converts six URDF joint targets in
degrees to motor turns, and rejects targets outside the configured URDF soft
limits. ID 6 uses the provisional `turns=0 -> q6=0`, `direction=+1`, 36:1
mapping and an operator-selected `+/-150 deg` software range. Its direction and
mechanical range have not been measured.

Because ID6 is unloaded, it can spin if left in the drive's default current
mode after enable. The controller therefore requires ID6 to start within 5
motor turns (50 output degrees at 36:1) of zero, enables it alone first, immediately preloads its measured
position as a no-step target, and enters Profile Position before batch-enabling
IDs 1-5. `id6_bootstrap_start` and `id6_bootstrap_hold` must both report a
near-zero, stable position before normal multi-joint startup continues.

Build and dry-run the calibrated all-zero pose from the repository root:

```bash
cmake -S tita_gluon_ws/src/gluon -B /tmp/gluon_innfos_readonly_build
cmake --build /tmp/gluon_innfos_readonly_build --parallel

/tmp/gluon_innfos_readonly_build/gluon_innfos_multi_joint_pose \
  --joint-deg 0 0 0 0 0 0 \
  --max-joint-step-deg 170 \
  --waypoint-step-deg 5 \
  --profile-max-rpm 10 --profile-acceleration 10 \
  --current-limit-a 10 --current-abort-a 2 \
  --timeout-s 120 --hold-until-signal
```

Physical execution requires adding both acknowledgement flags:

```text
--execute --confirm-robot-may-move
```

If a manually reached mechanical stop lies outside a drive's stored position
range, Profile Position may report `ERR_STEP_OVER` even while holding the
measured current position. The explicit
`--allow-temporary-position-range-expansion` option expands only the affected
unsaved minimum/maximum values enough to contain the measured start-to-target
path plus 0.5 motor turns. It verifies readback, does not enable the position
limit, and does not save parameters to flash. Power cycling restores the last
saved values.

The executable refuses to start if any discovered actuator is already enabled.
It batch-enables IDs 1-6, reads their current positions, installs those values
as pre-mode hold targets, applies temporary unsaved profile/current limits,
individually activates and verifies Profile Position using the SDK example
sequence, verifies all six hold states, and then sends
the six calibrated targets through synchronized intermediate waypoints. The
default waypoint size is five output-joint degrees and may be reduced with
`--waypoint-step-deg`. A waypoint above ten degrees, profile velocity above 10
motor RPM, or acceleration above 10 RPM/s requires the additional
`--confirm-high-speed-profile` acknowledgement. The bounded high-speed ceilings
are 180 output-joint degrees per waypoint, 120 motor RPM, and 300 RPM/s. This
allows the drive's Profile Position planner to execute a direct target without
changing or clearing its protection.
`--max-joint-step-deg` remains the independent limit on total displacement from
the measured starting pose. During motion and hold the controller monitors each
actuator's position, current, and drive error. Ctrl-C causes all six actuators
to be disabled and verified individually.

This utility checks calibrated joint limits but does not perform geometric
self-collision or environment-collision checking. The arm must be supported
before starting and before Ctrl-C because disabling all six joints can allow
gravity-driven motion. A fault on any one active joint aborts the whole pose and
disables all six. Use `--hold-seconds N` instead of `--hold-until-signal` only
when automatic disable after the requested hold duration is intended.

At the 36:1 reduction, 10 motor RPM is approximately 1.67 output-joint degrees
per second. A 153-degree full-range return therefore needs at least about 92
seconds. A direct 120 motor RPM profile with 300 RPM/s acceleration has an
idealized approximately eight-second travel time for that displacement, before
communication and settling overhead. This is a materially higher-energy motion
and must be validated progressively with a clear workspace and emergency stop.

To capture a provisional visual-zero and manual joint sweep for all six axes,
close Minta Actuator Studio, support the arm, clear the workspace, and keep the
physical emergency stop ready. The acknowledgement flag is mandatory:

```bash
/tmp/gluon_innfos_readonly_build/gluon_innfos_readonly_probe \
  --record-all-seconds 180 \
  --output docs/exp/2026-08-04/gluon_joint_sweep.csv \
  --confirm-all-enable-may-move
```

Do not move the robot until the program prints `SWEEP_READY`. Although all six
actuators are enabled together for feedback, manually sweep one joint at a time
and stop before collision, cable strain, or a hard mechanical stop. Ctrl-C
causes the normal cleanup path to disable all six and print each verified
`post_disable_state`.

The default expected actuator count is six. Use `--expected-actuators 0` only
when intentionally diagnosing a partial bus.

Output includes actuator ID and ECB IP together because actuator IDs are only
required to be unique behind the same ECB. Position is reported in the raw SDK
unit (`turns`) and velocity in raw SDK `RPM`; no joint-angle conversion or joint
name mapping is assumed yet. The probe issues explicit asynchronous CVP read
requests and reports whether current, velocity, and position callbacks were
received for every actuator; this distinguishes actual feedback from a
zero-initialized SDK cache.

## Result labels

- `SENSOR_READ_PASS`: six actuators were discovered and every actuator expected
  to provide feedback returned complete asynchronous current/velocity/position
  values. In gated enable mode, only the selected actuator is expected to return
  CVP feedback.
- `SENSOR_READ_SUSPICIOUS`: some actuators were found, but the count or values
  need review.
- `SENSOR_READ_BLOCKED`: no actuator was discovered, commonly due to power,
  cabling, ECB, or host IPv4 configuration.
- `SENSOR_READ_FAIL`: local initialization or argument failure.
