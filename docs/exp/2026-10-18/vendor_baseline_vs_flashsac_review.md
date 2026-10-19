# Company baseline recording and FlashSAC standing comparison

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domains: `ROBOT_READ_ONLY` (inspection/copy), `ROBOT_COMMAND_FREE_RUNTIME` (passive CAN + ROS subscriptions), `DESKTOP_DRY_RUN` (offline analysis).
- Evidence Status: capture/integrity/known protocol extraction `PASS`; quantitative controller-equivalence and physical cause `SUSPICIOUS`; matched-command A/B test `NOT_TESTED`.
- Company Policy Checkpoint SHA256: N/A; vendor MCU/control internals not exported, no FlashSAC process during capture.
- Comparison FlashSAC checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- Comparison ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`.
- Branch: `agent/codex/dev_tita_gluon`; no commit or deployment.
- Operator corrected the initial supported-standing answer: **ordinary floor standing, same support condition as the preceding RL run**. Existing `supported` filenames are preserved as raw provenance, not used as the load-condition label.
- Operator applied all motion commands manually using the existing company joystick, and confirmed folding the robot at the end. The agent transmitted no motion/motor/MCU commands.

## What was recorded and where

SBC originals:

```text
~/tita_ws/docs/exp/2026-10-18/vendor_supported_stand_capture/
  vendor_supported_stand_110850_177668585_*   # neutral/stand, 60.20 s CAN
~/tita_ws/docs/exp/2026-10-18/vendor_baseline_capture/
  vendor_commands_111015_362785206_*          # operator commands/fold, 94.35 s CAN
```

PC copies and analysis: [vendor_supported_stand_review/](vendor_supported_stand_review/).

Each trial includes raw `*_can.log`, SQLite rosbag + metadata, bag/runner console, ROS topic/node lists, service snapshot and summary. `operator_annotation.json` records the corrected condition. CAN frames: 440,366 stand + 690,516 commands. The command capture was planned for 120 s and finalized early at the operator's “enough” message by terminating only the owned recorder parent; exit 143 is intentional and bags finalized normally.

Recorder subscriptions include joint states, IMU, joystick, passive/active locomotion commands, odometry, robot velocity, status and rosout where published. All bus traffic is preserved independently through receive-only `candump -L can0`. No robot SDK instance was created, no service/controller was stopped or activated, and CAN configuration was unchanged. Vendor service remained `active/running`, MainPID **350** before and after.

Initial discovery temporarily showed only a few topics. After sourcing the vendor overlay and allowing discovery, the existing IMU/joy/odom topics were found and recorded; no broadcaster was activated by the agent.

## Measured difference from RL

| Condition | IMU pitch |
|---|---:|
| Company stand, near-zero forward/yaw | mean **+1.426°**, std **0.310°** |
| Previous FlashSAC RL 1, quiet neutral | mean **+8.405°**, std **0.788°** |
| Previous FlashSAC RL 2, quiet neutral | mean **+8.366°**, std **0.828°** |

The preceding RL selection excludes its first 2 s and requires near-zero command and abs pitch gyro < 0.1 rad/s. The vendor selection requires firmware STAND mode and near-zero channel command. These are retrospective windows with different histories, not identical-command randomized trials. Both use normalized IMU quaternions; no independent floor-level calibration was performed.

The company controller achieves a flatter body on the same reported floor-standing condition. This is evidence that the RL lean is not simply an unavoidable property of the hardware. Whole leg posture and controller references differ:

| Measured joint angle | Company stand L / R | RL quiet 1 L / R |
|---|---|---|
| Thigh | **1.104 / 1.082 rad** | **0.885 / 0.930 rad** |
| Knee | **-2.178 / -2.135 rad** | **-2.098 / -2.018 rad** |
| Hip | **0.0008 / -0.0002 rad** | **0.0840 / -0.0907 rad** |

The company knees are more folded while its body is flatter. Thus the preceding knee-tracking observation cannot by itself explain the RL pitch; thigh/hip/height/whole-body balance references must also be considered. RL reference-to-measurement error remains a recorded fact, but company internal joint references/gains are unavailable. Do not treat company encoder positions or firmware-reported torque as known policy target actions.

## Operator-command segment

CAN channel input reached forward **[-1.5,+1.5]**, yaw **[-3,+3]**. The current RL joystick caps are +/-1 m/s and +/-1 rad/s. The factory values are observed channel ranges, not a newly established full factory speed specification. Its LocomotionCmd interface uses body pose and chassis twist; internal speed shaping is not recovered here. Unequal input scales preclude attributing movement magnitude solely to the policy/controller.

In firmware STAND mode, pitch p01/p99 was approximately **-0.824° / +3.608°**. There was also a short **-20.693°** pitch excursion around **8.165 s** of this command recording; the maximum was +4.124°. This was before the final fold and is retained rather than removed as a transition. The company controller did not maintain perfectly flat posture through every input.

Yaw input versus IMU gyro_z has descriptive best cross-correlation about 0.983 with a 0.04 s lag. Forward input versus mean wheel-speed proxy has descriptive best correlation about 0.808 at 0.82 s lag. Search range was 0..1 s on a 100 Hz retrospective interpolation over the operator input window. These values are not measured controller communication delays or proof of ground-truth velocity tracking. Wheel rotation does not establish base displacement/slip, and aggressive reversals/turns are mixed in this trial.

Firmware mode transitions: STAND(3) until approximately 78.02 s, TRANSFORM_DOWN(4), then status 0 at approximately 82.42 s. The operator confirmed folding at the end, so this sequence is intentional. Raw data for folding is retained separately from STAND selection.

## Control-path evidence and limits

Both captures contain the public `api_channel_input_t` family **0x12D**, with forward/yaw/body-pose fields, and no SDK direct-motor frames **0x120..0x123**. Public SDK comments describe default AUTO_LOCOMOTION as MCU control and channel input as its upper-level command path. In contrast, FlashSAC on the SBC builds observations, runs the frozen actor, calculates PD torque and calls `set_target_joint_t` in MCU Direct mode. This explains why the same robot can behave differently under the two controllers.

The company captures also contain nonzero **0x110..0x113** families. Their precise field semantics are not established by the available public headers. They were preserved but not silently decoded as 0x120-style torque commands. Internal factory targets, gains, torque limits and algorithms cannot be claimed from this capture alone. Firmware torque feedback is not calibrated physical torque.

Relevant schema: `sim2real/tita_ws/src/tita_robot/include/tita_robot/canfd_api.hpp` (0x108/109 motor feedback, 0x118 IMU, 0x12D channel input, 0x103 firmware mode); `tita_robot.hpp` AUTO_LOCOMOTION comments; SDK `LocomotionCmd.msg`. The active factory joystick YAML is preserved as `vendor_tita_joy.yaml`.

## Validation and unresolved items

- PASS: all **23 copied raw files** match SBC SHA256 (`remote_inventory.json`, `comparison_audit.log`). Original files were not edited during analysis.
- PASS: SQLite quick_check; known packed payload lengths, finite fields and bounded quaternion norms. Raw command-trial quaternion norm was 0.98889..0.99840; normalization matches the FlashSAC node's procedure and validity envelope.
- PASS: static ROS-vs-CAN joint mapping, 29,549 samples, position-error p99 about 0.000575 rad.
- SUSPICIOUS: dynamic receive-time alignment, leg p99 about 0.00288 rad, wheel p99 about 0.0583 rad, max periodic error about 0.387 rad. Wheel wrap is handled, but ROS/controller-read time and CAN receive time are not identical acquisition times; this is not an actuator-tracking error measurement.
- Initial command analysis was attempted before its copy finished and then hit a too-strict raw quaternion norm check. Both failed logs are retained; final analysis uses verified complete copies and explicit normalization. No threshold was changed on the robot.
- NOT_TESTED: identical-command/height A/B, external velocity/contact/CoM measurement, decoding factory hidden control targets, and any corrected RL controller.

[Stand graph](vendor_supported_stand_review/stand_overview.png), [command graph](vendor_supported_stand_review/commands_overview.png), [comparison metrics](vendor_supported_stand_review/comparison_summary.json).

Changed code: only new receive-only harness `test/sim2real/capture_vendor_baseline.sh`, offline `analyze_vendor_baseline.py` and `summarize_vendor_comparison.py`; added docs/exp raw evidence/report. Production/controller/policy/training sources unchanged. Shell syntax, actual captures, offline extraction/mapping and copied-file hashes were verified. Required `agent-check.sh` result is in `vendor_supported_stand_review/agent_check.log`; prior six `my_flat_env_cfg.py` whitespace errors are preserved.
