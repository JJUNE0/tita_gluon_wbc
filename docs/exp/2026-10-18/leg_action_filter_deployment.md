# Optional leg-only MA2: implementation and approved SBC deployment

- Date: 2026-10-18 (Asia/Seoul).
- Execution Domains: `DESKTOP_DRY_RUN` (build/math/logging tests), `VALIDATION_SIM` (production Python node integration), `ROBOT_READ_ONLY` (preflight), `ROBOT_STATE_CHANGING` (explicitly requested source deployment/build), `ROBOT_COMMAND_FREE_RUNTIME` (ARM mock/message/launch validation only).
- Checkpoint SHA256: `79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c`.
- ONNX SHA256: `26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9`.
- Config SHA256: `a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719` (mixed leg PD unchanged).
- Evidence Status: local tests/build, finite simulation integration and SBC installation/ARM verification PASS; physical vibration suppression NOT_TESTED.
- Branch: `agent/codex/dev_tita_gluon`; no commit/push.

## Behavior

`leg_action_filter` accepts `none` (default) or `ma2_legs`. At every 50 Hz inference, six leg outputs become half current raw plus half previous raw. Wheels pass through, selected using action-to-native-joint mapping rather than policy index assumptions. The first action after RL entry passes through; RL exit, inference failure or CAN failure clears history. A non-20 ms policy is rejected when filtering is selected.

The 500 Hz loop uses this held applied target and current position/velocity in the existing ActionAdapter. It does not repeatedly average per motor tick. Observation `last_action` remains raw. Baseline torque and wheel-bias torque both use the same applied leg action, so their difference remains a wheel-only correction. Supporting sit, estop, faults and orderly shutdown zero commands keep their existing control paths. First-action initialization does not smooth away the initial RL target jump.

The public FlashSAC launch passes the option to the logged runner and generic launch; root runner delegation preserves it. Invalid modes are rejected before runner construction. Python sim2sim exposes the same option through ROS launch and `--leg_action_filter ma2_legs`, with identical filter reset/update math in `adapter.py`.

## Logging and learning samples

The existing `TrainingSample` wire fields are unchanged. Its comment and teacher calculation now explicitly describe **applied** targets (filtered legs plus wheel bias). Raw policy output remains `action_raw` and `/sim2real/debug/action`.

New `/sim2real/action_filter_sample` (`ActionFilterSample`) records header, sequence ID, control tick, monotonic time, mode and policy-order `action_applied`. Join to TrainingSample by sequence ID AND monotonic time within one recording; this also distinguishes unfiltered and filtered runs. It is emitted for the same sampling events, including invalid/output-disabled frames, and is always included in the runner's recorder topic list. Use training validity flags before learning from a joined sample. No actor training/export bounds are assumed by teacher inversion.

Both messages are separate DDS publications: the IDs make pairing explicit but do not guarantee delivery. A consumer must reject unmatched pairs, not assume equal topic counts. This design keeps old bags readable. An actual pre-filter bag was decoded with the rebuilt message package to verify compatibility.

## Executed checks

- PASS DESKTOP_DRY_RUN: C++ filter/adapter self-checks and 3 Python tests. 500 random inputs across four mode/mapping combinations match C++ exactly; reset/reentry, wheel pass-through, first/DC/period-2 response, disabled identity, raw preservation, invalid inputs and teacher/bias torque reconstruction checked.
- PASS DESKTOP_DRY_RUN: 23 mock runner/launch lifecycle tests. The actual public ROS launch with mocked service/CAN/controller commands forwards MA2 and bias together, preserves output-disabled behavior and records the new topic. That forwarding test was rerun after its assertions were expanded.
- PASS DESKTOP_DRY_RUN: desktop C++ node plus all generated messages compile/link; package 41.0 s, colcon total 41.1 s. Existing CMake CMP0135 warning only. The real robot node executable was not run.
- PASS DESKTOP_DRY_RUN: 4 message/teacher logging tests, including actual SQLite round trip, >2^53 integer join precision and new ActionFilterSample CDR round trip. An old real TrainingSample bag still decodes.
- PASS DESKTOP_DRY_RUN: existing adapter/state parity: observation max error 1.20e-7, torque 1.10e-5 Nm, startup state torque 1.17e-4 Nm, zero mismatches over 6000 steps.
- PASS VALIDATION_SIM: actual Sim2SimNode/ONNX/MuJoCo at 500 Hz physics / 50 Hz inference, 1000 steps each in OFF/MA2, 890 RL steps each. Raw observation history, applied sequence and reset assertions pass; state remains finite. Maximum absolute pitch 6.498 deg in each run. This is a finite integration smoke, not a locomotion-quality or vibration-margin experiment. Debug publications were captured in local test sinks to inspect exact values. Initial sandbox DDS restrictions were logged; the run was repeated successfully with localhost-only DDS on domain 87.
- NOT_TESTED: real motor/controller execution, physical 25 Hz attenuation, new stability margin or disturbances. The earlier 264-job proxy study was reviewed previously, not repeated here.

Detailed logs, before snapshots, source diffs, payload and integrity manifests are under [leg_action_filter_deployment/](leg_action_filter_deployment/). Test fixtures and deployment helper are under `test/sim2real/`.

## Deployment

The user explicitly requested implementation and deployment. SBC read-only preflight confirmed no running `tita_node` and matching prior sources. The deployment helper checks before hashes, backs up the old controller sources, runner, README and installed controller, uploads only the scoped sim2real changes and the pure C++ test, then rebuilds `tita_controller`. Python sim2sim changes remain on the PC. No controller launch, torque command, MCU mode request or company-service mutation is included.

SBC package build PASS: 42.7 s (colcon total 43.2 s). Source payload hashes, installed launch/runner byte comparisons, ARM pure filter/adapter/teacher checks, both modes through installed launch functions with node/runner construction mocked, new message CDR/uint64 and library linkage PASS. Installed policy pins and mixed gains match the prior deployment. Both the new filter log string and preceding shutdown-zero string are present in the installed executable. No physical controller was executed; preflight and verification both found no `tita_node`.

Logs: [SBC build](leg_action_filter_deployment/remote_build.log), [ARM verification](leg_action_filter_deployment/remote_verify.log), [executable SHA](leg_action_filter_deployment/executable_after.sha256), [backup SHA](leg_action_filter_deployment/backup.sha256). Backup path is `~/tita_ws/docs/exp/2026-10-18/leg_action_filter_deployment/before_deployment.tar.gz`. No rollback was applied.

## Operator selection after deployment

```bash
cd ~/tita_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch tita_controller flashsac.launch.py output_enabled:=true leg_action_filter:=ma2_legs
```

Velocity bias remains OFF in this command. Omitting the filter argument keeps filtering OFF. Joystick idle → transform_up → sit → RL and return/stop operations are unchanged. Host transport success does not prove motor acknowledgement or electrical isolation. Actual filter effects still need a supervised operator trial.

## Completion scope

Changed production areas: C++ filter/node, launch/runner, one added ROS message and CMake entry, TrainingSample comment, Python adapter/node/CLI/launch and README. No checkpoint, ONNX, gain config, state-machine trajectory or shutdown helper changes. Existing source edits were snapshotted and preserved. Final scoped diffs match the reviewed saved diffs and other scanned existing sources remain unchanged; see `completion_integrity.json`.

Required [agent-check](leg_action_filter_deployment/agent_check_final.log): overall FAIL only from the six pre-existing trailing-whitespace errors in `my_flat_env_cfg.py` (431,437,443,449,455,461). Python syntax 585 PASS and URDF parsing 8 PASS. These unrelated errors were preserved.
