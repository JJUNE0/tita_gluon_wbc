# Ctrl+C after FlashSAC: residual hip torque

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domains: `ROBOT_READ_ONLY` (process inspection, 4 s passive CAN receive), `DESKTOP_DRY_RUN` (offline decode, local fix/mock tests/build), `ROBOT_STATE_CHANGING` (separately approved file deployment/build only), `ROBOT_COMMAND_FREE_RUNTIME` (ARM mock helper tests without SDK/CAN).
- Evidence Status: post-stop pose/firmware torque and process evidence `PASS`; physical torque retention interpretation `SUSPICIOUS` (no calibrated force sensor); local and SBC fix tests/build `PASS`; fixed physical release `NOT_TESTED`.
- Policy checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`.
- Deployment config SHA256: `10d66ca07cc10e07d38e3a44e204768881fc2285aa5baa6fcefffc0792f1b1e7` (unchanged, RL leg 92/2.3).
- Branch: `agent/codex/dev_tita_gluon`; no commit/push.
- Operator observation: Ctrl+C completed, but motors still resist and hips curl inward.

## Immediate evidence

Read-only process inspection found no `tita_node`; company `tita-bringup.service` was inactive. The saved `processes_after_ctrl_c.txt` contains only this inspection shell and grep, not an active robot controller. No service was restarted and no motor command or torque-release command was sent by the agent.

A 3.996 s receive-only CAN snapshot contains 1,999 frames each for left motors, right motors and IMU (about 500 Hz). There are no 0x120..0x123 direct motor command frames or 0x12D channel commands in this post-exit window.

| Post-Ctrl+C | Left hip | Right hip |
|---|---:|---:|
| Native encoder angle | -0.8213 rad (~-47.1°) | +0.8272 rad (~+47.4°) |
| Firmware-reported torque mean | -33.51 Nm | +31.44 Nm |
| Firmware-reported torque range | -33.65 .. -33.38 Nm | +31.28 .. +31.60 Nm |
| Peak reported angular speed | 0 | 0 |

Knee reported torque also remained around -22.0 / -21.6 Nm. Firmware torque is telemetry, not independently calibrated joint force. Nevertheless, the fresh feedback and large curled hip angles agree with the operator's residual-force observation. There is no basis for calling this a zero-torque state merely because the process is gone.

Artifacts: [post-stop metrics](flashsac_shutdown_torque_review/post_stop_metrics.json), [raw CAN](flashsac_shutdown_torque_review/after_ctrl_c_can.log), [process snapshot](flashsac_shutdown_torque_review/processes_after_ctrl_c.txt).

## Code finding and interpretation

Before this patch:

1. Sit and supporting-estop are active pose/torque controllers. The final effective hip reference includes the original feedforward (-20/+20 Nm) and live position PD; resulting final commands can be nonzero.
2. Ctrl+C causes `rclcpp::ok()` to become false. The motor loop stops; the destructor only set `running_=false` and joined the thread.
3. Neither the normal loop exit nor destructor sent zero torque, a hardware disable command, or an MCU mode request.
4. The runner could then terminate/kill remaining launch/SDK processes. Process termination itself does not clear a command already retained downstream.

This is a **supporting-sit torque plus missing output finalization** problem. The slow-sit implementation should have been reviewed together with its process-exit behavior. Changing the descent time or setting sit gains lower would not establish a reliable output-release contract. A last active torque retained at the MCU/driver, after host-side position feedback stops, is consistent with the observed inward movement. The exact retention layer (MCU versus motor driver) is not isolated here, and the last SDK command was not captured in this post-stop snapshot.

The existing software `estop` intentionally remains latched with active support; it is not electrical torque disable. The added cleanup is for terminating the control loop/process, separate from a live four-second supporting sit.

## Local corrective patch

- New `control_loop_exit.hpp` wraps the sole existing writer loop. On orderly return or an exception escaping the loop, it attempts **ten all-joint zero-torque command batches**, separated by 2 ms (approximately 18 ms plus send/scheduling overhead).
- Zero batches execute after the final in-flight control write and before SDK destruction. A signal handler never writes CAN directly, and no second writer/node is added.
- The wrapper catches standard and non-standard loop exceptions, including shutdown-time ROS publication errors, so these cannot bypass cleanup by escaping the thread function.
- Output-disabled runs remain command-free. A prior CAN-error output latch is not retried. A failed/throwing zero send stops further retries and logs that motor torque release is unconfirmed.
- Success is logged as **transport accepted**, not motor ACK, calibrated zero torque or power isolation.
- The CAN-error message was corrected from “motor output OFF” to “command output OFF; motor torque release NOT confirmed”.
- Policy/gains/observation mapping, live sit trajectory and torque caps are unchanged.

Orderly zero cleanup removes position support; it does not perform a new sit trajectory after Ctrl+C. The operator should end RL with the existing return-to-sit flow and allow the pose transition to finish before process termination. Supporting/isolating the robot remains necessary when testing output release. Immediate zero torque while upright can remove leg support.

Limits: SIGKILL, a stuck SDK send, broken CAN, SBC power loss and firmware behavior can bypass/prevent this host cleanup. No functional MCU/motor watchdog is established by this patch. If a CAN failure already latched output off, this wrapper does not claim the motor was released. The physical stop contract must eventually include downstream watchdog/disable verification; graceful host cleanup alone cannot prove fail-safe behavior.

## Verification actually executed

- PASS DESKTOP_DRY_RUN: `test_control_loop_exit.cpp`, **9 scenarios**, mock sender only: orderly zero ordering/count; disabled gate; loop exception; non-standard exception; false/throwing send; prior fault latch; cleanup wait exception; single-writer join before SDK destruction.
- PASS DESKTOP_DRY_RUN: **full tita_controller node build**, ROS Jazzy/x86_64, isolated build/install under `test/sim2real/shutdown_work/`, ORT cache reused. One package completed in 28.6 s. Existing CMake CMP0135 developer warning only, no compile/link failure. No executable was run and no SDK object was constructed.
- PASS DESKTOP_DRY_RUN: post-stop packed motor feedback lengths/finite values and raw source SHA recorded.
- PASS ROBOT_STATE_CHANGING: after explicit operator approval, backed up old sources and installed controller, checked old source hashes, deployed scoped payload and rebuilt `tita_controller` on SBC ARM64/ROS Humble. Package build 41.7 s (colcon total 42.5 s).
- PASS ROBOT_COMMAND_FREE_RUNTIME: all 9 mock shutdown scenarios on ARM, installed binary patch string/hash and dependency linkage verified. Real controller executable was not run. Initial independent linkage check failed because the validation shell had not sourced ROS/overlay; sourcing both resolved the search paths. Both verification logs are retained.
- PASS ROBOT_READ_ONLY: installed policy/config hashes match the frozen 80000 policy and leg gains 92/2.3. No `tita_node` was running during verification. Company bringup service was already active at deployment preflight and remained active; no service or MCU mode changes were made.
- NOT_TESTED: actual zero-torque CAN output/feedback on physical hardware, motor ACK, watchdog or forced-kill/power-loss release.

Logs: [exit tests](flashsac_shutdown_torque_review/exit_tests.log), [desktop build](flashsac_shutdown_torque_review/desktop_build.log), [analysis](flashsac_shutdown_torque_review/post_stop_analysis.log).

## Scope and deployment status

Local changes: `tita_node.cpp`, new `include/tita_controller/control_loop_exit.hpp`, README. New analysis/test/deployment helper code is under `test/sim2real/`; before snapshots, CAN evidence, diffs and logs under docs/exp. No factory controller, network, gain/config/policy or state-machine trajectory changes.

The operator explicitly approved SBC update/rebuild. **The shutdown fix is now deployed and rebuilt in `/home/robot/tita_ws`.** The previous README, node source and installed controller are backed up under `docs/exp/2026-10-18/flashsac_shutdown_torque_fix/before_deployment.tar.gz` on SBC. Deployment did not execute a controller or release torque retained downstream. No shutdown/torque command was sent by the agent. Physical output release remains untested.

Deployment evidence: [SBC build](flashsac_shutdown_torque_review/remote_build.log), [ARM verification](flashsac_shutdown_torque_review/remote_verify.log), [initial unsourced verification](flashsac_shutdown_torque_review/remote_verify_unsourced.log), [post-build state and policy hashes](flashsac_shutdown_torque_review/remote_state_after.log), [executable SHA256](flashsac_shutdown_torque_review/executable_after.sha256), [backup SHA256](flashsac_shutdown_torque_review/backup.sha256).

Required `agent-check.sh`: `flashsac_shutdown_torque_review/agent_check_final.log`; pre-existing six trailing whitespace errors in `my_flat_env_cfg.py` cause overall FAIL and remain untouched. Python syntax 564 PASS and 8 URDF parses PASS. Final scoped source/diff review is recorded in `completion_integrity.json`.
