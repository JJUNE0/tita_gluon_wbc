# Timestamped FlashSAC training frames

- Execution Domain: DESKTOP_DRY_RUN
- Evidence Status: PASS (desktop build, synthetic SQLite round trip and mocked runner); hardware NOT_TESTED
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`
- Branch: `agent/codex/dev_tita_gluon`
- Observed metrics: final C++/interface build succeeds; 22 runner tests pass; 2 data tests pass, covering 2,000 target/PD comparisons and 150 serialized SQLite frames.

## Change

Added `/sim2real/training_sample` (`tita_controller/msg/TrainingSample`) to the
controller and automatic rosbag topic list. A single message carries observation,
raw ONNX action, wheel target offsets, equivalent teacher action, command,
joint/IMU snapshot, computed torque, bias diagnostics, state and validity/output
flags. This removes receipt-time joins between those fields for new training
frames. Legacy debug topics remain available.

At nominal policy cadence (20 ms / 50 Hz), and on state transitions, each frame has:

- `header.stamp`: ROS time just after sensor read, shared with legacy JointState/IMU.
- `sequence_id`: exact uint64 frame counter, zero-based and reset on node restart.
- `control_tick`: motor-loop index, normally advancing by 10 between policy frames.
- `monotonic_ns`: steady-clock timestamp for interval/gap analysis independently of ROS clock jumps.

Invalid-sensor frames are also published at that cadence, with an empty
observation and validity flags. The existing inference and physical action path
retain their prior scheduling/targets; logging adds work to that loop, whose
hardware timing impact is NOT_TESTED. Stamps describe controller snapshots, not
original CAN acquisition times. Sequence gaps reveal missing published training
frames; a stalled control loop also requires monotonic-time analysis.

The frame's `teacher_action` inverts the existing action adapter after adding
wheel bias:

```text
physical_target = clip(action_raw * scale + offset, target_low, target_high)
physical_target[wheel] += wheel_velocity_bias[side]  # rad/s
teacher_action = (physical_target - offset) / scale
```

Action fields are in policy order. `teacher_action` is in gain-scaled ONNX output
units, so normalized actor training must divide by the checkpoint's export gains.
It is recorded without silently clipping it to actor bounds. `teacher_action_valid`
checks successful current-frame inference and adapter invertibility/target
representability; actor bounds still need an offline check. Targets outside the
adapter's range due to post-clip bias are logged and marked invalid.

For physical teacher data, start with RL frames where `sensors_valid`,
`policy_valid`, `teacher_action_valid`, `output_enabled`, and `torque_sent` are true,
then filter command, bias eligibility, saturation and observed behavior as needed.
`torque_sent` is transport acceptance, not motor acknowledgement or measured
torque. Output-off and transmission-fault frames can now be identified in the
same message. Observation history still contains raw previous actor action;
student training/execution must account for this convention.

## Files

- `sim2real/tita_ws/src/tita_controller/msg/TrainingSample.msg`: typed atomic record.
- `sim2real/tita_ws/src/tita_controller/src/tita_node.cpp`: timestamp, sequence, packet publication and flags.
- `sim2real/tita_ws/src/tita_controller/include/tita_controller/adapter.hpp`: logging-only target inversion helper; physical PD method unchanged.
- `sim2real/tita_ws/src/tita_controller/CMakeLists.txt`, `package.xml`: generated interface/typesupport dependencies.
- `sim2real/tita_ws/run_flashsac.sh`: record topic and name it in run summaries.
- `sim2real/tita_ws/README.md`: units, filtering and build guidance.
- `test/sim2real/test_flashsac_logging.py`: assert new topic is passed to recorder.
- `test/sim2real/training_action_runtime.cpp`, `test_training_logging.py`: target inversion and real SQLite/CDR round trip.

## Executed validation

- **PASS:** Isolated desktop CMake build/install of generated C/C++/Python interfaces and full `tita_node`; existing cached ONNX Runtime and desktop dependency overlay used. [Final build log](training_logging_build_final.log).
- **PASS:** `source /opt/ros/jazzy/setup.bash; python3 test/sim2real/test_flashsac_logging.py`, 22 tests / 21.544 s. Only mock service, recorder, CAN command and controller processes are invoked. [Runner tests](training_logging_runner_tests.log).
- **PASS:** With the newly built message overlay, `python3 test/sim2real/test_training_logging.py`, 2 tests / 3.469 s. 2,000 C++ comparisons exercise shuffled action order, negative/unequal scales, offsets, effort clipping, post-target-clip bias, invalid inputs and unchanged raw actions. Actual SQLite/CDR storage preserves 150 complete frames, integer sequence/time values above 2^53, empty invalid frames and output-off flags. These timestamps were synthesized at 20 ms intervals; this is not a measured 50 Hz hardware timing test. [Data tests](training_logging_data_tests.log).
- **PASS:** `bash -n sim2real/tita_ws/run_flashsac.sh`.
- Repository completion check: [agent-check log](training_logging_agent_check.log).

An initial build exposed an unqualified generated-message namespace; this was
corrected to `tita_controller::msg`. The first data-test attempt exposed Jazzy's
required rosbag TopicMetadata ID argument; the test now supports that constructor
and the older Humble signature. Initial failure logs were retained alongside final
passing logs. Humble/ARM builds and physical timing are NOT_TESTED.

No controller binary was executed, no CAN socket was opened by the tests, and no
hardware deployment was performed. The desktop's existing workspace installation
was not updated: the new build was isolated under `test/sim2real/`. Before robot
collection, rebuild `tita_controller` on the SBC and source its overlay so both
the executable and recorder have the new message type. The runner's data location
continues to be `sim2real/tita_ws/docs/exp/YYYY-MM-DD/` on the machine running it.
