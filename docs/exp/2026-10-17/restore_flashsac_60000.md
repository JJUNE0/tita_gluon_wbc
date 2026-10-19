# Restore FlashSAC model_60000 with motor feedback logging

- Execution domains: `DESKTOP_DRY_RUN`, `ROBOT_READ_ONLY`, `ROBOT_STATE_CHANGING` (requested policy replacement/build), `ROBOT_COMMAND_FREE_RUNTIME` (installed-message tests only).
- Evidence: policy deployment/build and scoped tests **PASS**; physical run **NOT_TESTED**; repository-wide agent-check **FAIL** due to pre-existing whitespace.
- Branch: `agent/codex/dev_tita_gluon`; no commit or publication.
- Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Config SHA256: `d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d`.

## Change

Restored the public FlashSAC launcher to the existing 60000 bundle. Updated its pinned checkpoint/ONNX/config hashes and the runner's bundle path, run identifier and recorded checkpoint hash together. The runner continues recording `/sim2real/motor_feedback`. Velocity bias remains disabled by default.

Changed files: `sim2real/tita_ws/src/tita_controller/launch/flashsac.launch.py`, `sim2real/tita_ws/run_flashsac.sh`, `sim2real/tita_ws/README.md`, `test/sim2real/test_flashsac_setup.py` (select active checkpoint), and `test/sim2real/deploy_restore_flashsac_60000.sh` (guarded backup/build/verification).

Inspected existing dirty state and task-only [before/after diff](restore_flashsac_60000/task_changes.patch). Deployment payload contains only launch, runner and README. The feedback-enabled node, message schemas, velocity-bias implementation and all three policy bundles were hash-verified unchanged. Installed node SHA256 remains `f086fa22038124386825752711c83fd20b1ef220cdbad7eaae002463d42b3c73`.

## Executed checks

- **PASS** desktop native PyTorch versus C++ ONNX: 256 samples, maximum action error `3.099e-06`; deterministic finite inference, state machine/gates/limits, selected bundle hashes and corruption rejection.
- **PASS** shell syntax: modified runner and deployment helper.
- **PASS** robot ARM64/Humble colcon build, installed launch validates the 60000 bundle, runner selects the same model and logging prefix.
- **PASS** robot command-free CDR/SQLite tests: 40 joined feedback/training pairs and 150 original TrainingSample frames (2 tests). No controller or SDK instantiated.
- **PASS** source/policy/installed-node preservation hashes and installed library dependency resolution.
- **FAIL** `./scripts/agent-check.sh`: existing trailing whitespace in `my_flat_env_cfg.py` at lines 431, 437, 443, 449, 455, 461. Python syntax 520/520 and URDF 8/8 **PASS**.
- **NOT_TESTED** physical behavior with restored checkpoint; no motor run in this task.

## Robot deployment

Target: `robot@192.168.0.28:/home/robot/tita_ws`. The previous source/install package was backed up before deployment to `docs/exp/2026-10-17/restore_flashsac_60000/before_deployment.tar.gz` on the robot. No active process was using the workspace controller package. The existing `/opt` bringup service was left running; no service stop/start, controller launch, MCU mode request or motor command was performed.

Logs, manifests and snapshots are under [restore_flashsac_60000/](restore_flashsac_60000/). The next operator-run public launch selects 60000 and automatically records motor feedback. Firmware-reported torque is not an independent physical torque calibration.
