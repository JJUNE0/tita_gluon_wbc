# Vendor LQR additional capture session

- Date/time: 2026-10-18 17:12 KST (Asia/Seoul).
- Execution Domains: `ROBOT_READ_ONLY` (attempted SSH, PC address/route/neighbour inspection), `DESKTOP_DRY_RUN` (review existing capture/analysis tools and shell syntax).
- Evidence Status: SUSPICIOUS (resumed capture interrupted after operator reported unresponsive joystick); partial CAN/ROS reception and SQLite checks PASS; cause and useful LQR excitation NOT_TESTED. Existing recorder shell syntax PASS.
- Policy checkpoint SHA256: N/A (vendor controller; no exported vendor policy).
- Comparison FlashSAC checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- Branch: `agent/codex/dev_tita_gluon`; no commit/push/deployment.

The operator reports that the robot is powered on in its original vendor mode and requests help collecting additional LQR data. Current physical standing/folded condition has been requested and is pending. No motion commands were issued and no recorder was started during these unsuccessful connection attempts.

## Prior evidence and intended capture

The existing [vendor reproduction review](vendor_lqr_reproduction.md) reports adequate ROS joint/IMU/effort sampling but insufficient independent excitation to distinguish wheel feedback coefficients. Additional data should distinguish quiet standing, operator-commanded motion/recovery and any operator-applied disturbances; do not pool these labels or infer unobserved target torque/gains.

Reuse `test/sim2real/capture_vendor_baseline.sh` once connected: initial60 s neutral standing, then a separately annotated capture for recovery/command data. It subscribes to existing ROS topics and uses receive-only `candump -L can0`, verifies vendor service active and refuses an active FlashSAC `tita_node`. It issues no SDK, CAN transmit, MCU-mode or service-state commands. Standing/contact conditions and manual disturbance timing must be recorded as operator annotations, not assumed from the previous session.

Recorder SHA256: `8b83dc2597f6b651324038e47319b19c9f49ef421eaff9d6ca6c188a8f9b9665`. `bash -n` PASS. Recorder source is unchanged. Existing destination is `~/tita_ws/docs/exp/2026-10-18/vendor_baseline_capture/`, with unique phase/time filenames, CAN raw log, rosbag, console, ROS inventory, vendor service snapshots and summary. New completed captures will be copied and SHA256 verified on the PC before offline analysis.

## Connection findings

- Existing SSH endpoint: `robot@192.168.0.28`.
- Master-socket attempt timed out; a fresh direct SSH attempt then returned `No route to host`.
- PC Wi-Fi has192.168.0.215/24; the route to192.168.0.28 uses `wlo1` with that source address.
- Neighbour entry for192.168.0.28 is `FAILED`. This is evidence of present local reachability failure, not a diagnosed robot/software fault or proof of a particular power state.
- Asked operator whether PC/robot share a network and whether robot IP changed. No network settings were modified.

## Resumed capture and operator-reported joystick problem

The operator subsequently said ready/start. SSH connected; vendor service was active/running with MainPID308, no `tita_node` or pre-existing recorder was present, and97 GB was free. The first inspection briefly saw1970 on the freshly booted SBC; a second inspection confirmed automatic NTP synchronization to2026-10-18 **before** the recorder was started. No clock settings were changed by the agent.

The unmodified receive-only harness started `vendor_stand_171439_905205199` at17:14:39 KST. After its CAPTURE_READY output, the agent told the operator that recording was active. The operator then reported the joystick did not work and suspected Direct mode. The agent terminated only the verified owned capture parent PID2823 with SIGTERM; its trap stopped candump and rosbag and finalized storage. Capture exit143 at17:15:24 KST was intentional. No further captures were started.

After termination, no recorder/candump or FlashSAC `tita_node` process remained, and vendor service still had MainPID308, active/running. The operator reported the joystick still did not respond after the recorder was stopped, then chose to power-cycle. No vendor service, MCU-mode, motor-command or network-setting changes were issued. No automatic restart or capture after power-cycle is authorized by this record; first confirm vendor joystick operation with the operator.

### Partial evidence

- CAN duration39.1438 s,279336 frames; SQLite quick_check `ok`.
- ROS messages include19200 IMU,19200 joint states,7639 joystick,6539 active-command and2300 odometry messages. No recorded passive-command messages. Joystick axes[4] changed from-1 to+1, so at least some remote switch data reached ROS; this does not establish all control inputs were functioning.
- No0x170 RPC request, no0x120..0x123 SDK direct-motor command and no0x12D channel-input frames appear in the partial CAN recording. This supports that no Direct request was transmitted during the recorded interval; it cannot rule out an MCU mode set before capture.
- Firmware locomotion status key0x1001 stayed0 (robot_status_t::DIE); this is a locomotion-status enum, **not** the MCU READY/AUTO/DIRECT enum. Do not interpret it as a decoded Direct-mode acknowledgement.
- Boot/service logs include passive_command waiting for a parameter service and a transient RobotTimeout/RobotOK around automatic time synchronization before capture. These are possible leads, not an established cause. The service process remained running.
- Post-stop CAN interface: ERROR-ACTIVE with bus-error counters0, cumulative RX dropped21910. Load average8.68/3.74/1.40. No pre-capture load/drop baseline was taken, so do not attribute these counters or joystick failure to the recorder without additional evidence.

The raw harness summary carries the **previous session's hard-coded floor-standing annotation**. Actual posture/contact in this session was not confirmed; status0 and the operator's joystick report mean this must not be treated as a successful standing LQR baseline. Preserve raw summary provenance and use this correction in analysis.

Partial raw files are copied under `vendor_lqr_capture_session/vendor_stand_171439_905205199*`. Source-to-PC SHA256 verification is pending because the operator opted to power-cycle; no further hardware reads were started after that instruction. Existing captures and all controller sources remain unchanged. New files are partial evidence and read-only diagnostic logs; no production/test code was changed. Required agent-check is recorded in this evidence directory.
