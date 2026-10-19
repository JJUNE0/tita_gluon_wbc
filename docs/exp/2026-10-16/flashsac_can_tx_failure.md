# FlashSAC idle CAN transmission failure

- Execution Domain: ROBOT_READ_ONLY (diagnosis and log retrieval), DESKTOP_DRY_RUN (changes and checks).
- Evidence Status: FAIL (operator's hardware run); PASS (desktop build and mock shutdown tests); SUSPICIOUS (transport cause unresolved).
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`
- Policy ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`
- Branch: `agent/codex/dev_tita_gluon`

## Observations

Operator enabled output using `ros2 launch tita_controller flashsac.launch.py output_enabled:=true`.
The first errors follow `motor output ENABLED; state: idle; policy 50.0 Hz`.
There is no transition to RL in the saved console. Idle retains the original
velocity damping torque and sends commands at the 500 Hz motor loop rate;
policy inference only runs in RL.

The copied console contains 6,400 `No buffer space available` messages over a
run whose startup-to-SIGINT timestamps span approximately four seconds.
Linux CAN documents `ENOBUFS` as a full driver queue:
https://github.com/torvalds/linux/blob/master/net/can/af_can.c
This identifies the failed layer, but does not establish why the queue filled.

Post-run read-only snapshot: `can0` UP, CAN FD, arbitration 1 Mbit/s, data
5 Mbit/s, TX queue length 10, ERROR-ACTIVE, TX/RX error counters zero,
bus-off/restart counters zero. RX drops are cumulative 18,450.
This snapshot does not prove the physical bus was healthy during the failure.
No matching controller/joystick/launch processes were found at that inspection;
`tita-bringup.service` was inactive. No service or CAN configuration was changed.

The existing controller discarded `set_target_joint_t`'s boolean result.
SDK header inspection and desktop library disassembly show a boolean send status
propagates to this call. The loop therefore continued attempting sends after errors.
The short TX queue and loop catch-up after scheduling overruns are possible
contributors, not proven causes. Bitrate, wiring, driver and runtime load need
further evidence before a transport fix is selected.

The pasted outer-launch log also shows a second Ctrl+C aborting the runner
with exit -2 during cleanup. The saved summary has no Finished marker.
The joystick exited -7 (SIGBUS) during shutdown; that cause remains unresolved.

## Local changes

- `sim2real/tita_ws/src/tita_controller/src/tita_node.cpp`: check send status and
  exceptions. On failure latch output off, request Damp, clear previous action,
  and log the failure. Later ticks send no further torque commands in this process.
  This cannot undo any frames already sent or guarantee a hardware stop.
- `sim2real/tita_ws/run_flashsac.sh`: ignore additional INT/TERM while the bounded
  owned-process cleanup and recorder finalization run.
- `test/sim2real/test_flashsac_logging.py`: reproduce repeated Ctrl+C during a
  delayed shutdown using actual desktop ROS launch and mock controller/recorder;
  verify descendants exit, summary finishes and bag metadata is written.

Changes are local only. No updated code was copied to the SBC, and no physical
runtime was launched. CAN send-failure handling on real hardware is NOT_TESTED.
No automatic service restart, CAN reset, queue resizing or torque test occurred.

## Validation

- PASS: `bash -n sim2real/tita_ws/run_flashsac.sh`.
- PASS: 14 desktop tests, including repeated Ctrl+C and recorder finalization;
  see `flashsac_can_fault_tests.log`.
- PASS: desktop Jazzy `colcon build --packages-select tita_controller`, one package;
  see `flashsac_can_desktop_build.log` and `flashsac_can_desktop_colcon/`.
- FAIL: `./scripts/agent-check.sh`, solely pre-existing trailing whitespace in
  `my_flat_env_cfg.py` lines 431, 437, 443, 449, 455 and 461. Fast Python syntax
  and eight URDF parse checks pass. See `flashsac_can_agent_check.log`.
- PASS: reviewed task diff in `flashsac_can_changes.patch`; tracked-worktree diff
  hash remains `40076fca037839dbd955f4644f404a0e3ea6c8b5e7a3fc86a79bb15150ddab47`.
  Task code is in already-untracked files; unrelated tracked edits remain unchanged.

## Retained evidence

- `flashsac_can_operator_terminal.log`: original pasted terminal attachment.
- `flashsac_can_post_run_state.log`: read-only CAN/service/process inspection output.
- `flashsac_60000_205958_457641980_output_true_console.log` and `_summary.md`:
  unmodified copies of the failed hardware run, retaining its original NOT_TESTED
  status. This report records the subsequent FAIL assessment.
- Matching `_bag/` and `_bag_console.log`: copied recorder data. Read-only SQLite
  inspection found 197 joint/observation/state/torque messages, 198 IMU/action
  messages, 780 joy messages and 14 rosout messages. This verifies recorded rows,
  not successful delivery of torque frames.

Do not treat this local guard as a repair of the CAN transport. Establish the
transport cause before the next operator-controlled torque-enabled run.
