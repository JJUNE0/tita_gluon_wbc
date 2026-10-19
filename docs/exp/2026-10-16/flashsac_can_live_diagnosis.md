# Direct SBC CAN diagnosis

- Date: 2026-10-16 (Asia/Seoul).
- Execution Domains: ROBOT_READ_ONLY, ROBOT_COMMAND_FREE_RUNTIME, ROBOT_STATE_CHANGING, DESKTOP_DRY_RUN.
- Evidence Status: FAIL at 500 Hz; PASS for bounded 10/100 Hz zero-torque transport; SUSPICIOUS shutdown behavior.
- Selected policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- Selected policy ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Branch: `agent/codex/dev_tita_gluon`.
- Authorization: operator requested direct execution and confirmed robot support,
  wheels isolated from unintended travel, and ability to cut power nearby.

## Finding

The ENOBUFS failure is reproducible using only the vendor SDK and zero torque,
without ROS, ONNX inference, joystick, transform_up or RL. At a requested 500 Hz,
the ninth SDK call failed after 0.0176184 seconds. The probe stopped immediately
without retrying. The qdisc drop counter increased from 7,806 to 7,807.

The observed transport supports the tested short 10/100 Hz runs but cannot
sustain the tested 500 Hz stream in its current configuration. This narrows the
failure to the SDK/CAN transmission path and its scheduling/load. It does not
identify a specific driver defect or prove that physical bus bandwidth alone
is the limiting factor. Rebooting did not remove the reproducer.

## Recorded measurements

| Requested SDK call rate | Duration | SDK calls | Captured transmitted frames | New qdisc drops | Result |
| --- | --- | --- | --- | --- | --- |
| 10 Hz | 1.00016 s | 10 | 40 | 0 | PASS |
| 100 Hz | 1.00019 s | 100 | 400 | 0 | PASS |
| 500 Hz | 0.0176184 s | 9 | 35 | 1 | FAIL, first-error abort |

Each SDK torque call creates four 48-byte CAN FD frames, IDs 0x120–0x123.
The 500 Hz configuration therefore requests 2,000 outgoing frames/s.
The 500 Hz failure affected ID 0x122; 35 of 36 attempted frames were observed.
Kernel acceptance/transmit capture does not establish motor-side execution.

Passive capture contained 14,254 received frames in approximately two seconds,
about 7,100 frames/s, before any probe torque sends. The dominant receive IDs
were 0x108, 0x109, 0x110–0x113 and 0x118, approximately 1,000 Hz each.
Telemetry load and competition with command transmission warrant investigation;
no firmware telemetry setting was modified.

Interface configuration was unchanged: `can0`, arbitration 1 Mbit/s, data
5 Mbit/s, FD enabled, qlen 10. Post-test CAN remained ERROR-ACTIVE with TX/RX
error counters zero and no bus-off/restart count increase. Device-level TX
drop statistics remained zero while qdisc drops increased: qdisc statistics
are needed to observe this failure. Initial drops predate this diagnosis.

## Method and changed files

Added only `test/sim2real/probe_can_zero_torque.cpp` and this report, plus evidence
logs. No existing production controller, launch, SDK library or CAN setting was
changed during this task. The earlier local send-failure guard remains undeployed.

The standalone probe validates fresh IMU/motor data and finite joint velocities
below 5 rad/s, sends exactly eight zero-torque values, stops at its first send
failure, bounds its requested duration to at most two seconds and rate to
1–500 Hz, and skips missed deadlines instead of catching up with bursts.
Every actual send run used one second as its upper limit. External timeout
also bounded each diagnostic process. No nonzero torque, pose target, gain,
residual, RLS, reference update or probing excitation was commanded.

The initial read-only SDK probe printed a completed PASS result with zero send
calls but hung in object destruction; external timeout had to SIGKILL it (137).
The final probe intentionally uses `_Exit` after flushing its result to bypass
that observed SDK destructor hang. This is confined to the test harness and
does not repair production shutdown behavior.

Installed workspace SDK SHA256:
`22460f0b59fd10265b100ab725828c34a62654f858468f1afaa28359c050ae7d`.
Stock `/opt/tita/ros2/tita_robot/lib/libtita_robot.so` SHA256:
`357834cff399b318b3842f10c5be0e292d2f6610f4f6d1221e6dd654328690bf`.
They differ in API symbols and size; no library substitution was attempted.

## Actual frozen-policy launcher, output disabled

Ran `ros2 launch tita_controller flashsac.launch.py output_enabled:=false` under
a five-second timeout. Existing bringup was already inactive; the precheck
would refuse this test if a controller/service were active. Startup printed
`motor output DISABLED; state: idle; policy 50.0 Hz` and recorded a rosbag.
This verifies loading and sensor/observation processing, not RL inference,
motor torque correctness or locomotion.

Shutdown reproduced a joystick SIGSEGV (-11) and a controller group that required
SIGTERM then SIGKILL. The owned runner nevertheless finalized its summary and
bag. Expected bounded-launch timeout exit was 124; runner recorded interrupt
exit 130. Runtime startup passes, graceful shutdown fails. SDK destructor hang
and joystick crash are distinct unresolved issues; the exact fault sites were
not traced in this task.

## Validation and final state

- PASS: desktop `g++ -std=c++17 -Wall -Wextra -fsyntax-only` on the probe.
- PASS: ARM64 probe compiled with the same SDK used by the SBC controller.
- PASS: final read-only probe exited normally; no command calls were made.
- PASS: bounded 10/100 Hz zero-torque trials; FAIL: bounded 500 Hz trial as above.
- FAIL: `./scripts/agent-check.sh`, solely pre-existing trailing whitespace in
  `my_flat_env_cfg.py` lines 431, 437, 443, 449, 455 and 461. Fast Python syntax
  and eight URDF parse checks pass. See `can_live_agent_check.log`.
- Final read-only inspection at 2026-10-16 21:17:54 KST: no matching motor,
  joystick or probe processes; bringup inactive; qdisc backlog zero. No further
  torque commands were sent after the zero500 probe.
- Tracked diff SHA256 is unchanged from task start:
  `40076fca037839dbd955f4644f404a0e3ea6c8b5e7a3fc86a79bb15150ddab47`.

## Evidence and next work

All raw evidence is retained in this date directory, on both desktop and SBC:
`can_live_passive_frames.log`, `can_live_zero{10,100,500}{,_frames,_before,_after}.log`,
`can_live_probe_*.log`, `can_live_initial_state.log`, `can_live_final_state.log`,
and `can_live_flashsac_false_outer.log`.
The no-output run is `flashsac_60000_211717_134788233_output_false*`, including
console, summary, recorder log, SQLite bag and finalized metadata.

The diagnostic supports investigating command rate, bus service time and
telemetry scheduling before another 500 Hz torque-enabled controller run.
100 Hz success is limited to zero torque for one second; it does not validate
100 Hz closed-loop control or justify changing the trained controller's timing.
Queue enlargement alone could increase command delay and was not attempted.
Torque sign, units, left/right mapping, transform_up and RL remain NOT_TESTED
by this diagnosis. No commit, push, service restart or policy deployment occurred.
