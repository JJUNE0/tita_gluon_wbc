# FlashSAC real-data logging audit

- Execution Domain: DESKTOP_DRY_RUN
- Evidence Status: SUSPICIOUS (mock lifecycle PASS; training alignment limitations)
- Hardware cadence / losses / bias feedback validation: NOT_TESTED
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`
- Config SHA256: `d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d`
- Branch: `agent/codex/dev_tita_gluon`
- Scope: inspect current source and local installation; run mocked lifecycle tests. No hardware access, deployment, controller execution, or production code edits.

## Storage and lifecycle

`flashsac.launch.py` validates the installed frozen policy, then invokes the installed `run_flashsac.sh`, which starts SQLite rosbag recording before the inner `tita.launch.py` controller launch. It records joint state, IMU, joystick, obs, action, computed torque, state, velocity bias diagnostics, and rosout. Console, recorder console, ROS logs, run summary, and policy/config/binary hashes are retained.

Files go to **`sim2real/tita_ws/docs/exp/YYYY-MM-DD/` on the machine running the launch**, with the Korea date; this is distinct from repository-root `docs/exp/`. No collection duration limit is configured. The recorder captures received messages without a separate sampling timer or compression/splitting configuration.

Recorder startup failure prevents controller startup. Readiness checks that a `.db3` exists, not that every topic subscription is matched. Recorder process exit is checked every 0.2 s and triggers owned-controller cleanup; this is not a disk-space/message-drop watchdog. Ctrl+C stops the controller before finalizing the recorder, using bounded SIGINT/TERM/KILL cleanup. Wait for the runner's saved/exit message. Bringup service shutdown occurs even with motor output disabled; the actual runner was not run on the robot during this audit.

Local installed launch files, runner and policy bundle match the inspected source files byte for byte. This does not verify the installation on a different robot/SBC.

## Intended cadence and fields

| Item | Intended cadence | Meaning |
|---|---|---|
| Motor loop / CAN torque command | 2 ms, 500 Hz | Not recorded on every motor tick |
| Policy inference in RL | 20 ms, 50 Hz; also valid state changes | Config is 0.005 s times decimation 4; C++ divides by its 0.002 s motor period |
| JointState / IMU | 20 ms, 50 Hz; also valid state changes | Snapshot used by controller; not original CAN acquisition timestamps |
| obs / action / torque / state / velocity_bias | Same publish cycle | Suppressed when sensor validity check fails |
| Joy | CRSF receive callback | `update_rate=10` does not set Joy rate in `joy_only` mode; actual receive rate must be measured |
| rosout / console | Event driven | No fixed sampling rate |

The 33-element obs is built before inference and contains the previous **raw** actor action. The 8-element action is the ONNX output, including export-time actor gains, before adapter scale/offset/clip and before wheel velocity bias. Torque is the final computed PD command after bias and torque clipping, not measured motor torque and not proof of successful transmission. JointState.effort and IMU.linear_acceleration are not populated from measured sensors.

## Training-data limitations

1. **Common sample ID/timestamp absent:** JointState and IMU share a ROS publication stamp. Float32MultiArray obs/action/torque/bias and String state have no header or sequence ID. Bag receipt timestamps allow approximate alignment, but ordering/counts alone do not prove correct pairing if drops occur. Sensor sample acquisition age and loop jitter/overruns are not recorded.
2. **Teacher action must be reconstructed:** `/sim2real/debug/action` is raw actor output even when `velocity_bias:=true`. Bias diagnostics contain wheel target velocity offsets (indices 7/8, rad/s), allowing reconstruction with saved action scale/offset/clip and export gains. A wheel target is `clip(raw_action * scale + offset, low, high) + dq_bias`; recorded final torque additionally reflects PD and effort saturation. Do not train on raw action alone as the corrected teacher target.
3. **Action history convention matters:** Current real controller leaves raw actor action in the next observation. The simulation fine-tuning collector uses corrected action history. A dataset builder/student rollout must explicitly handle this difference; the bags are not a direct drop-in replacement for simulation replay.
4. **Runtime output status absent from each sample:** Startup output selection is in the summary; transmission errors are in console/rosout. There is no per-frame output-enabled, transmit-success, sensor-valid or fault flag. Invalid-sensor ticks publish nothing, including state. Filter RL intervals and exclude faults/output-off periods using the available logs; diagnostics alone cannot establish actuation.
5. **Default collection is not corrected-teacher collection:** Both `velocity_bias` and motor output default to false. Plain launch records output-disabled computations with no correction. Hardware feedback sign/quality remain NOT_TESTED.

For this 50 Hz actor-distillation task, retaining every policy tick is the relevant target; 500 Hz torque logs would serve separate motor/latency analysis. At nominal cadence, 3 min corresponds to 9,000 policy samples and 5 min to 15,000, before startup, gating, invalid data and fault filtering. These are arithmetic counts, not verified sufficient data quantities.

After a physical collection, inspect the finalized bag for RL duration, per-topic counts, inter-message interval median/p99/max, gaps, alignment, bias eligible fraction, torque saturation and output faults. There were no local hardware bags in `sim2real/tita_ws/docs/exp/` to measure actual cadence during this audit.

## Executed checks

- `bash -n sim2real/tita_ws/run_flashsac.sh`: PASS.
- After sourcing `/opt/ros/jazzy/setup.bash`, `python3 test/sim2real/test_flashsac_logging.py`: **PASS, 22 tests, 21.143 s**. ROS launch orchestration exercised with mocked service/CAN/controller/recorder, including startup failures, recorder death, bias forwarding, Ctrl+C/descendant cleanup and finalization. This does not test real SQLite throughput or robot control timing. See [test log](flashsac_logging_audit_tests.log).
- Repository completion check output: [agent-check log](flashsac_logging_audit_agent_check.log).

Observed behavior: existing automatic recording is suitable for initial diagnostics and retains the ingredients for reconstructed teacher targets, subject to receipt-time pairing. Strict synchronized training records and actual hardware cadence/loss evidence are still missing. Production behavior was not changed.
