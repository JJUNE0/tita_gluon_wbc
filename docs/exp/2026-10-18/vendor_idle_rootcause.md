# Vendor idle investigation: boot wall-clock jump and broken control-loop deadline

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domains: `ROBOT_READ_ONLY` (approved inspection, no recorder/controller execution or state changes), `DESKTOP_DRY_RUN` (static binary/source analysis and virtual-time reproduction).
- Evidence Status: installed timing defect, boot clock-step chronology and virtual mechanism PASS; attribution of the complete idle/joystick fault SUSPICIOUS pending recovery verification. Vendor restart/fix and physical effect NOT_TESTED.
- Vendor policy checkpoint SHA256: N/A (factory controller).
- Comparison FlashSAC checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`; FlashSAC was not running.
- Branch: `agent/codex/dev_tita_gluon`; no commit/push/deployment.

## Main finding

The installed factory ros2_control loop starts with a1970 wall-clock reference and later receives a very large forward clock change during automatic NTP synchronization. Its deadline remains based on the old reference and is advanced by only2 ms per cycle. Once wall time is in2026, sleeping on this old deadline cannot throttle the loop normally. The installed update thread is continuously runnable and accounts for approximately98.8% of one CPU core, matching this failure mechanism.

This is a concrete timing defect exposed by the observed startup sequence, and the strongest current explanation for loss of normal vendor control. It is **not yet a complete experimentally confirmed explanation of every vendor Timeout or the idle guard**, because this authorized turn excludes service restart or motor-affecting commands. Do not describe this as a verified repair until synchronization-before-start recovery is tested.

## Actual boot sequence

Boot ID: `d48f3539-8b67-4200-958e-1e953e649cf4`; factory bringup MainPID325. The journal exposes monotonic and realtime timestamps independently:

| Boot monotonic time | Realtime/ROS time | Event |
|---|---|---|
| 6.597500 s | 2026 timestamp | timesyncd logs restoration from saved time |
| 10.929288 s | epoch28.795730 s (1970) | hardware bridge reports MCU mode |
| 10.970556 s | epoch28.836998 s (1970) | controller manager starts500 Hz loop; ROS log time28.835394336 s |
| 12.797926 s | epoch30.664367 s (1970) | passive_command waits for parameter service |
| 17.002239 s | epoch1792311463.593205 s (2026-10-18 17:17:43 KST) | initial NTP synchronization |
| 17.034551 s | epoch1792311463.625518 s | vendor RobotTimeout event |
| about45 s uptime | 17:18:11 KST | agent's earlier post-reboot read-only inspection |

The change to2026 precedes that earlier SSH inspection by approximately28 s. The user-reported timing of idle relative to access remains an observation, but it is not evidence that SSH sent a Direct command. The chronology identifies an independently occurring clock event before the inspection. The earlier saved-time restoration followed by1970 at control startup suggests another clock change or initialization detail; who causes the earlier reset is **not established**. The later NTP forward step itself is directly observed.

Full evidence: [time correlation](vendor_idle_rootcause/time_correlation.log), [clock/version/binary symbols](vendor_idle_rootcause/clock_and_binary.log), [runtime threads](vendor_idle_rootcause/vendor_runtime.log), [current synchronization/thread CPU](vendor_idle_rootcause/clock_setters.log).

## Installed algorithm and binary agreement

- Package: `ros-humble-controller-manager`, version `2.43.1-1jammy.20241029.131514`; package.xml2.43.1.
- Installed executable SHA256: `9af17139e8f33a8e2af4daaf19b74ee846a655265358aa0d550a9bd0027de87a`.
- Official [2.43.1 source](https://raw.githubusercontent.com/ros-controls/ros2_control/2.43.1/controller_manager/src/ros2_control_node.cpp) was fetched successfully on the PC; SHA256 `c8920e2f98738e0664de97fc9160f17b7b36d9e30ca1cef66ae71caaf839968f`. The browser cache initially failed for the tag URL; direct HTTP retrieval succeeded. Local copy: `test/sim2real/vendor_idle_work/ros2_control_node_2.43.1.cpp` (upstream Apache2.0 header preserved).
- This version initializes an absolute system-clock deadline from the controller clock, increments by the fixed period, and sleeps to that deadline. There is no forward-step rebase in this loop. The newer [upstream clock documentation](https://github.com/ros-controls/ros2_control/blob/master/controller_manager/doc/clocks.rst) describes steady-clock trigger timing, but that is not the installed Humble behavior.
- Static ARM disassembly confirms the installed executable uses the same structure. At0x37b4, x20 receives initial controller nanoseconds; x28 holds the fixed period. At0x38dc the loop obtains system-clock time;0x38e4 skips the sleep path if the deadline is already behind.0x393c advances x20 only by x28, then branches back to the loop. No process was paused/attached to read this; objdump operated on the executable file.
- [Full disassembly](vendor_idle_rootcause/ros2_control_disassembly.txt), [time-call summary](vendor_idle_rootcause/binary_time_calls.log). Copied ARM binary was **never executed** on the desktop.

The CPU observation supports this mechanism, but static analysis does not expose the live deadline register. We did not use ptrace, gdb, perf or service restart to force proof on a robot.

## Other hypotheses examined

- The robot's `.bashrc` returns immediately for noninteractive shells; its interactive tail only sources ROS Humble. `.profile` has standard bash/PATH setup. No `.bash_profile`, user SSH rc or system SSH rc was found in the inspected paths. No active SSH ForceCommand or PAM exec/script entry was found. **No Direct auto-execution was found in these inspected login paths.** This is not an exhaustive audit of every authentication hook.
- Bringup remains active/running MainPID325. No FlashSAC `tita_node`, rosbag or candump was running during inspection.
- All six checked vendor processes inherit ROS domain42 and ROS_LOCALHOST_ONLY0, with factory `/opt/tita/ros2` libraries. No inherited workspace overlay or per-process domain mismatch was found.
- Domain42 graph inspection sees passive_command parameter services but not controller_manager services; domain0 is empty. Short discovery can miss nodes, so this is supporting context rather than a definitive deadlock detector.
- Factory hardware bridge logs MCU mode at boot. The private library is **not** the modified development hardware_bridge source in this repository; local source must not be presented as the installed implementation.
- Factory SDK library imports steady_clock and no obvious clock-setting symbol; checked binaries do not expose a settimeofday/clock_settime import. This does not explain the earlier1970 reset and does not prove absence of indirect clock setters elsewhere.

Earlier offline healthy/fault comparison is preserved in [vendor_idle_offline_diagnosis.md](vendor_idle_offline_diagnosis.md): healthy diagnostics Joy/BodyImu/Robot allOK, fault allTimeout39/39; joystick198 Hz and IMU/joints approximately498 Hz still reach recorder; passive command and robot velocity outputs are absent. Those findings fit a vendor path failure, not simply a missing radio link, but do not prove this deadline defect alone causes all missing subscriptions/outputs.

## Desktop reproduction

New `test/sim2real/test_vendor_clock_jump.py` uses virtual integer timestamps only. No system clock, ROS clock, robot process or output was modified.

- PASS: ordinary start gives positive wait on10000/10000 synthetic cycles.
- PASS: observed-scale forward step gives zero positive waits on100000 cycles and leaves the deadline more than1.7e9 s behind.
- PASS: initializing the same scheduler after synchronization restores positive wait on10000/10000 cycles.
- PASS: pinned upstream source contains the matched system-clock/deadline constructs.

[Executed4-test log](vendor_idle_rootcause/clock_model_tests.log), [virtual timing results](vendor_idle_rootcause/clock_model.json). This test demonstrates scheduling arithmetic and supports the recovery proposal; it does not simulate vendor dynamics or certify a safe robot restart.

## Concrete recovery check and permanent prevention

Currently NTP=yes and NTPSynchronized=yes; the old control-loop thread has not recovered by itself. The smallest discriminating next test is **one vendor service restart after synchronized time is established**, followed by read-only checks for normal controller CPU, restored passive/velocity outputs and valid vendor diagnostics, and the operator's joystick confirmation. Do not force MCU Direct/AUTO manually for this test.

The concrete proposed command is `sudo systemctl restart tita-bringup.service`. It has **not been issued**. Restarting this service can change motor/control state and lies outside the operator's inspection-only approval, so it requires separate operator authorization under AGENTS.md section3. Prepare the robot for the vendor startup behavior before executing it.

If that test restores normal operation, permanent prevention should start factory control only after a valid, synchronized, stable wall clock is available. A bounded pre-start clock guard is preferable to a fixed arbitrary sleep; `After=time-sync.target` alone should not be treated as proof that synchronization actually completed. The [official time-wait-sync documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd-time-wait-sync.service.html) describes the separate synchronization wait and the `/run/systemd/timesync/synchronized` marker. Neither a boot-order override nor an upstream controller replacement was installed during this turn. Additional in-run clock jumps would require a separate timing-robust controller fix.

## Scope and checks

Added only the desktop regression test, pinned upstream source, this report and inspection/analysis evidence under `vendor_idle_rootcause/`. No existing controller, config, service, SDK, capture helper or policy source was changed. No recording, motor/MCU command, process attach, service restart or clock adjustment was performed. Required [agent-check](vendor_idle_rootcause/agent_check.log) is overall FAIL from the same six pre-existing `my_flat_env_cfg.py` whitespace errors; Python syntax612 PASS, URDF8 PASS. The four virtual-time tests PASS. Final scope/source checks are recorded in this evidence directory. Physical recovery remains NOT_TESTED until separately authorized.
