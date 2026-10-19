# Vendor idle lockout: offline comparison with earlier healthy runs

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domain: `DESKTOP_DRY_RUN` only. No robot connection, ROS node, live subscription, service call or command was started in this analysis.
- Evidence Status: copied-file extraction/comparison PASS; root cause SUSPICIOUS / not established; corrected controller or hardware behavior NOT_TESTED.
- Vendor checkpoint SHA256: N/A (vendor controller internals unavailable).
- Comparison FlashSAC checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c` (no FlashSAC inference/control in this incident).
- Branch: `agent/codex/dev_tita_gluon`; no commit/push/deployment.

## Operator clarification and access boundary

The operator clarified that power remains on and the robot returns to **idle**, after which the joystick cannot re-enter normal operation. After a subsequent reboot the operator briefly reported normal operation, then reported the same idle symptom immediately after the agent's read-only inspection. That inspection showed vendor service MainPID325 active/running, no FlashSAC/rosbag/candump process, CAN bus-error counters0 and cumulative RX drops19883 at uptime45 s. There was no second recording session. The first capture's vendor MainPID was308 and remained running after that recorder was stopped.

All robot access was stopped after the repeated symptom report and remains stopped. This analysis uses only previously copied CAN/ROS data and saved service logs. The timing reported by the operator must be preserved; absence of explicit write commands does not establish that access had no indirect effect. No experiment isolated SSH/session-start effects, load, timing or other processes.

## Measured differences

The earlier healthy company-controller captures had verified joystick-controlled motion. Compare those against the39.14 s partial recording during the first reported problem:

| Signal | Healthy stand | Healthy commands | Idle problem |
|---|---:|---:|---:|
| Diagnostic messages | 60 | 95 | 39 |
| Joy diagnostic | OK60/60 | OK95/95 | **Timeout39/39** |
| BodyImu diagnostic | OK60/60 | OK95/95 | **Timeout39/39** |
| Robot diagnostic | OK60/60 | OK95/95 | **Timeout39/39** |
| ROS joystick messages | approximately198 Hz | approximately199 Hz | **198 Hz,7639 messages** |
| ROS IMU messages | approximately496 Hz | approximately497 Hz | **498 Hz,19200 messages** |
| ROS joint-state messages | approximately496 Hz | approximately497 Hz | **498 Hz,19200 messages** |
| Passive-command messages | 10491 | 15983 | **0** |
| Robot-velocity messages | 10491 | 15982 | **0** |
| Active-command messages | 10111 | 16126 | **6539** |

Thus diagnostic `Joy Timeout` does not mean that no joystick ROS messages exist. At least one joystick switch changes in the recording, but the vendor monitoring/forwarding path does not behave like the earlier healthy case. The passive command and velocity outputs disappear together. Service process liveness is insufficient to establish a functioning vendor control loop.

RightBattery Timeout occurs in **both healthy recordings and the problem recording**. Treating that indication alone as the cause would ignore the negative control. Camera/FaceTof/NeckTof mostly time out only in the problem trace; these broader indications are retained in JSON.

## Time and control-mode checks

In the problem recording, joystick/IMU/joint-state header stamps increase monotonically and are close to recorder receive time. Median receive-minus-header latency is approximately0.365/0.698/0.731 ms respectively; maxima10.42/11.32/11.28 ms. These messages are not simply still stamped1970 after synchronization. This does not prove that another vendor subscriber receives them or that its internal watchdog clock is correct. The boot logs' large automatic wall-time correction and transient timeout indications remain leads, not a demonstrated cause.

The CAN recording starts with locomotion status0 and stays there for all1958 status reports. It contains no0x170 RPC request, no0x120..0x123 SDK direct-motor command and no0x12D channel input. Public `robot_status_t::DIE=0` describes locomotion status; it is **not** the READY/AUTO/DIRECT control-mode enum. Neither the raw status0 nor the operator's word idle establishes an MCU Direct mode. No Direct command is observed during this interval, but there is no trace of the preceding healthy-to-idle transition.

## Interpretation and limits

The strongest current lead is **vendor inter-node reception/state monitoring/command forwarding**, including the path associated with passive_command and the hardware/controller-manager interface. Saved boot logs show passive_command waiting for a parameter service; it is absent from the saved ROS node list despite its OS process being present. This supports investigating initialization/communication/callback progress, but does not identify a particular deadlock or failed service as the cause.

An idle/fault guard followed by a recovery path that does not resume would fit the operator's experience. The available data does not show which guard fires, whether state is intentionally latched, or why monitoring reports simultaneous timeouts. An SSH-shell startup side effect, extra load or other command sources have not been ruled out. Do not present a service restart or forced MCU mode as a proven fix, and do not repeat accesses automatically to reproduce the failure.

The second reboot/inspection symptom has operator testimony and an inspection snapshot, but no copied live transition trace. Original-SBC versus PC hashes for the interrupted first capture remain unverified because access was halted. Local source hashes and SQLite integrity establish only the copied artifacts' local consistency.

## Files and actual validation

- New offline helper: `test/sim2real/audit_vendor_idle_offline.py`. Only SQLite deserialization and text CAN parsing; no socket, rclpy initialization or SDK construction.
- [Audit JSON](vendor_idle_offline_diagnosis/audit.json): source bag hashes, diagnostic counts, topic counts, sensor timing and CAN families.
- [Executed audit log](vendor_idle_offline_diagnosis/audit.log): PASS for all three SQLite checks, healthy/problemed diagnostic contrast, missing passive output and monotonic/fresh sensor headers.
- Source schema: `sim2real/tita_ws/src/tita_robot/include/tita_robot/canfd_api.hpp`, inspected without changes.
- Existing capture helper, controller/policy/config and previous evidence files are unchanged. Only this report, new offline helper and local evidence were added. Required agent-check result and final integrity record are in `vendor_idle_offline_diagnosis/`.
