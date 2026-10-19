# Motor torque feedback logging

- Execution domains: `DESKTOP_DRY_RUN`, `ROBOT_READ_ONLY`, `ROBOT_STATE_CHANGING` (explicitly approved software deployment/build), `ROBOT_COMMAND_FREE_RUNTIME` (serialization only).
- Evidence: deployment/build and message tests **PASS**; actual new controller feedback acquisition **NOT_TESTED**; repository-wide agent-check **FAIL** from pre-existing whitespace.
- Branch: `agent/codex/dev_tita_gluon`; no commit or publication.
- Active checkpoint: FlashSAC model_75000, SHA256 `381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730`.
- ONNX SHA256: `2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114`.

## What changed

The controller now reads the SDK `get_joint_t()` cache at the existing policy/log cadence (nominal 50 Hz, plus state transitions). It publishes eight native-order firmware-reported torques, validity and read-completion time on `/sim2real/motor_feedback`. The same valid torque values populate `JointState.effort`. Invalid feedback contains NaN and leaves effort empty; diagnostic validity does not modify control behavior.

Each feedback message shares the existing TrainingSample header, sequence ID, control tick and monotonic sample time. TrainingSample itself remains byte-for-byte unchanged. Position, velocity, IMU, commands, actions and current computed torque remain in TrainingSample. The new topic is explicitly included in the runner's rosbag list.

Feedback is read before the current inference and transmission. The message additionally includes the preceding 500 Hz computed torque, its SDK transport-result flag and transport-return timestamp. These do not establish motor acknowledgement, CAN reception time, or a synchronized q/dq/torque acquisition frame. The two topics can be delivered independently; join IDs and check gaps before comparison. A same-row ratio during fast changes is not an actuator gain estimate. Use valid, transmitted, nearly steady command windows and inspect delay.

This collects firmware-reported torque, potentially inferred from current. It cannot independently validate torque constants, gear ratios or physical output calibration. The real-to-sim equivalent gain of 0.6 remains an identification result, not an established physical 40% torque deficit.

## Changed files

- `sim2real/tita_ws/src/tita_controller/src/tita_node.cpp`: cache read and diagnostic publication; preceding command metadata.
- `sim2real/tita_ws/src/tita_controller/msg/MotorFeedback.msg`: separate diagnostic schema.
- `sim2real/tita_ws/src/tita_controller/CMakeLists.txt`: register new message.
- `sim2real/tita_ws/run_flashsac.sh`: record topic and describe it in run summaries.
- `sim2real/tita_ws/README.md`: units, timing, joining and interpretation.
- `test/sim2real/test_training_logging.py`: actual SQLite/CDR round-trip and join coverage.
- `test/sim2real/deploy_motor_feedback_logging.sh`: guarded backup, deployment, ARM build and command-free verification.

Existing dirty files were inspected before editing. Task-only before snapshots and [diff](motor_feedback_logging/task_changes.patch) preserve the changes against this task's starting state. Payload contains only the five production/documentation files above. Launch defaults, 50000/60000/75000 policy bundles, velocity-bias implementation and TrainingSample schema were verified unchanged using SHA256 manifests before and after deployment.

## Executed validation

| Check | Evidence | Result |
| --- | --- | --- |
| Desktop generated CDR/SQLite tests | 40 joined pairs, preceding/current flags, NaN invalid reads; 150 original frames with large integer IDs/timestamps; 2,000 teacher/PD cases | PASS, 3 tests |
| Existing real 75000 bag | Unchanged schema SHA256; 2,725 messages decoded including 1,004 RL frames; increasing sequence IDs | PASS |
| Desktop C++ build | Node translation unit compiled; final link unresolved SDK symbols including existing CAN/read/send APIs and get_joint_t; desktop SDK link unavailable | FAIL at link; no desktop full-build PASS claimed |
| Robot ARM64/Humble colcon | tita_controller finished in 41.3 s, total 41.9 s; installed binary dependencies resolved | PASS |
| Installed ARM CDR/SQLite | Two serialization tests, 40 feedback pairs and 150 TrainingSample frames; no node or SDK instantiated | PASS |
| Shell syntax | Runner and deployment helper, `bash -n` | PASS |
| `./scripts/agent-check.sh` | Python syntax 520/520 and URDF 8/8 PASS; existing trailing whitespace in my_flat_env_cfg.py at 431/437/443/449/455/461 | FAIL overall |
| Physical acquisition / controller timing | No controller launched or motor test performed in this task | NOT_TESTED |

## Deployment and next experiment

Target: `robot@192.168.0.28:/home/robot/tita_ws`. Source and installed controller package were backed up before replacement to `docs/exp/2026-10-17/motor_feedback_logging/before_deployment.tar.gz` (12 MB, SHA256 `c2457a335ad135b38d23c75108516aa55a506ece80eaf571b72663a12bac37ae`).

Installed node SHA256: `f086fa22038124386825752711c83fd20b1ef220cdbad7eaae002463d42b3c73`.
Installed runner SHA256: `5fe3d388254feb7639f122592a31be36d35c419016b23a85ad314324fd628a69`.

The workspace controller package was unused throughout deployment. The default `/opt` bringup service remained active with its original controller PID 970 and joystick PID 1000. No service was stopped or started; no controller node, SDK instance, CAN socket, MCU command or motor command was run by this task. Installed SDK library SHA256 remained `22460f0b59fd10265b100ab725828c34a62654f858468f1afaa28359c050ae7d`.

On the operator's next regular FlashSAC run, the runner will record the new topic automatically. Begin diagnosis with velocity bias disabled, mark hand-contact intervals, and compare leg command versus firmware-reported torque after the initial RL transient. Actual feedback availability, missing IDs, SDK cache age/latency and added logging cost must be checked from that run before interpreting ratios. Current checkpoint stays 75000; this task did not choose or change the experiment policy.

Evidence logs and manifests: [artifact directory](motor_feedback_logging/), including desktop_tests.log, legacy_bag_compatibility.log, desktop_build.log, build.log, remote_verify_session.log, remote_after.log, agent_check.log, preserved.sha256 and installed.sha256.
