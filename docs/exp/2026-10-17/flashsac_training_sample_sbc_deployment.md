# TrainingSample and velocity-bias SBC deployment

- Execution Domains: DESKTOP_DRY_RUN (review and local tests), ROBOT_STATE_CHANGING (operator-approved file replacement and build), ROBOT_COMMAND_FREE_RUNTIME (offline ARM calculations and serialization), ROBOT_READ_ONLY (installed artifacts and process checks).
- Evidence Status: PASS for source deployment, Humble/ARM64 build, generated message installation and offline data tests; NOT_TESTED for physical behavior and runtime publication frequency.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Config SHA256: `d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d`.
- Branch: `agent/codex/dev_tita_gluon`.
- SBC verification time: 2026-10-17 13:23 KST (04:23 UTC).
- Authorization: operator explicitly requested reviewing the additional training logger, updating the powered-on SBC and rebuilding. No controller or torque test was requested or executed.

## Reviewed and deployed changes

The existing velocity-bias implementation was already installed. All ten files
from that deployment matched the previous desktop manifest before replacement.
Seven current production/documentation files were copied into `/home/robot/tita_ws`:

- `src/tita_controller/msg/TrainingSample.msg` (new).
- `src/tita_controller/src/tita_node.cpp`.
- `src/tita_controller/include/tita_controller/adapter.hpp`.
- `src/tita_controller/CMakeLists.txt` and `package.xml`.
- Workspace `run_flashsac.sh` and `README.md`.

The message joins the controller snapshot, observation, raw ONNX action, wheel
velocity offsets, equivalent teacher action, computed torque, bias diagnostics,
state and validity/output/transport flags. Publication is scheduled at nominal
50 Hz and state transitions; invalid-sensor frames have an empty observation.
ROS time describes the controller read, and monotonic time plus sequence/tick
provide interval and gap analysis. The logged runner records
`/sim2real/training_sample` automatically.

The logging helper reproduces the adapter target calculation: scale/offset and
target clipping first, wheel offset in rad/s next, then inverse scale/offset.
Teacher fields retain policy order and ONNX export units. They describe targets
before PD/final effort clipping, not measured motor torque. Unrepresentable
post-clip targets are marked invalid; actor bounds require an additional offline
check. For physical training data select RL frames with `sensors_valid`,
`policy_valid`, `teacher_action_valid`, `output_enabled` and `torque_sent` true.
`torque_sent` indicates transport acceptance, not a motor acknowledgement.

The existing physical action computation is unchanged by these logging changes.
The velocity-bias header, geometry and launch files still match the previously
deployed versions: bias +/-2 m/s, no separate correction-torque cap, final wheel
effort clip +/-12 Nm, feature and output both OFF by default. Hardware response
sign and corrected closed-loop behavior remain unvalidated.

This deployment did not edit local production sources. It reviewed and copied
the operator's prepared changes. Two existing offline test sources were also
copied under SBC `test/sim2real/`; local additions are this report and evidence.
The [reviewed production diff](flashsac_training_sample_sbc_deploy/reviewed_production.diff)
contains all seven changes relative to the previous deployment.

## Direct verification evidence

- PASS, DESKTOP_DRY_RUN: 22 mocked runner tests, including automatic recording of the new topic. [Log](flashsac_training_sample_sbc_deploy/desktop_runner_tests.log).
- PASS, DESKTOP_DRY_RUN: two data tests, including 2,000 teacher/PD comparisons and 150 actual SQLite/CDR frames. [Log](flashsac_training_sample_sbc_deploy/desktop_data_tests_final.log).
- PASS, DESKTOP_DRY_RUN: `bash -n sim2real/tita_ws/run_flashsac.sh`.
- PASS, ROBOT_STATE_CHANGING: `source /opt/ros/humble/setup.bash; source install/setup.bash; colcon build --packages-select tita_controller --event-handlers console_direct+`. One package finished in 50.5 seconds, exit 0. [Build log](flashsac_training_sample_sbc_deploy/build.log).
- PASS, ROBOT_COMMAND_FREE_RUNTIME: strict ARM C++ compile and 2,000 teacher/PD comparisons, including joint order, negative/unequal scales, saturation and invalid inputs. The fixture imports neither ROS nor the robot SDK.
- PASS, ROBOT_COMMAND_FREE_RUNTIME: Humble's generated Python message and SQLite/CDR serialization round trip preserves 150 synthetic frames, integer times/sequence above 2^53, empty invalid frames and output-off flags. This is offline storage, not a running recorder/controller test.
- PASS, ROBOT_READ_ONLY: all eleven relevant source files match the desktop manifest; installed message, runner, launch, geometry and package metadata match sources. Frozen policy/config hashes match. Generated Python typesupport loads and `ldd` resolves the native message typesupport and all controller libraries.
- PASS, ROBOT_COMMAND_FREE_RUNTIME: `ros2 interface show tita_controller/msg/TrainingSample` and `ros2 launch tita_controller flashsac.launch.py --show-args`; these inspect installed metadata without running the launch actions.

ARM and installation evidence: [verify.log](flashsac_training_sample_sbc_deploy/verify.log),
[verification.json](flashsac_training_sample_sbc_deploy/verification.json),
[installed interface](flashsac_training_sample_sbc_deploy/installed_interface.txt).

Controller executable SHA256:
`033811f58fba4a229e0dc7ae7d024d05ad39430553794c491d031fde7c69f148`.

The first local data-test invocation incorrectly sourced a nonexistent
workspace-level setup file: the user's isolated desktop build was installed
directly with CMake. Sourcing its package-level `local_setup.bash` fixed the
test environment; no production code change was needed. Initial failure and
final passing logs are retained.

## Backup, runtime limits and completion

All six existing production targets were backed up before replacement; the new
message and two test files were absent. Archive members and their content hashes
were checked before extraction, and installed source hashes checked afterwards.

- Payload SHA256: `fa29f98b3c22ae6f5dcbd7d9cefa75855668619b2cc07f0f7b02d67f0a5dd088`.
- Backup SHA256: `ed613b4a00303cc211c352c31f6bf284ddd3bded49c6a21f3d6ca2f3a4814c63`.
- Backup, source manifests, build and verification logs are preserved on desktop and SBC under `docs/exp/2026-10-17/flashsac_training_sample_sbc_deploy/`.

No service start/stop, MCU initialization, CAN command, controller execution or
joystick reader was performed. There was no FlashSAC `tita_node` before/after;
the existing vendor bringup remained active. Actual 50 Hz publication, logging
load on the 500 Hz controller, bias behavior and motor acknowledgement remain
NOT_TESTED. Synthetic 20 ms timestamps establish serialization fidelity only.

The operator must source the new overlay in the terminal used for the next run:

```bash
cd ~/tita_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Subsequent public-launch runs keep their logs in SBC
`~/tita_ws/docs/exp/YYYY-MM-DD/`, with the new topic included automatically.

Repository completion check: [agent_check.log](flashsac_training_sample_sbc_deploy/agent_check.log).
Overall FAIL is the six existing trailing-whitespace errors in unrelated
`my_flat_env_cfg.py` at lines 431, 437, 443, 449, 455 and 461. Python syntax
checks (502 passed, zero failed), eight URDF parses and experiment-directory
checks PASS. These pre-existing changes were not modified.
Final scope/hash verification is stored in the artifact directory; no tracked
production change was made by this deployment task. No commit or publication.
