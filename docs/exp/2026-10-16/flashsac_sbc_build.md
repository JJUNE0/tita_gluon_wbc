# Frozen FlashSAC SBC workspace replacement and build

- Date: 2026-10-16 (Asia/Seoul)
- Execution Domain: ROBOT_STATE_CHANGING (authorized source replacement/build); ROBOT_READ_ONLY (inspection); DESKTOP_DRY_RUN (local packaging/checks).
- Evidence Status: PASS (SBC Humble ARM build and static installation checks); robot runtime NOT_TESTED.
- Branch: agent/codex/dev_tita_gluon
- Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`
- ONNX Hash: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`
- Source archive SHA256: `6e3ed6d41e910f8289a4347e881b66d049511821286a27c6ac4b85c074ee27ce`

## Authorized scope and observed deployment

The user explicitly requested replacing the existing failed `~/tita_ws` and
performing the build only. No controller startup or service changes were requested.
Before replacement, the old workspace occupied 4.9 GB. No AGENTS.md was found
inside its non-build/install source tree. System service definitions were read:
both bringup/perception use `/opt/ros/humble` and `/opt/tita/ros2`, not `~/tita_ws`.
The running motor/joystick processes also use those `/opt` paths.

The source archive was copied to
`/home/robot/flashsac_60000_source_6e3ed6d41e91.tar.gz` and its full SHA256 verified
on the SBC before any workspace changes. The old directory was moved intact to
`/home/robot/tita_backups/tita_ws_before_flashsac_2026-10-16_112137`.
The requested `/home/robot/tita_ws` path was recreated cleanly with the new
source, selected policy, README and logged runner. Old code is outside the active
workspace; backups/logs were preserved.

The build shell clears old ROS overlay paths and sources only `/opt/ros/humble`
before building. The saved manifest continues to describe the original export;
this operation neither retrains nor re-exports the actor.

## Build command and logs

Working directory: `/home/robot/tita_ws`.

```bash
source /opt/ros/humble/setup.bash
colcon --log-base /home/robot/tita_ws/docs/exp/2026-10-16/colcon_build \
  build --packages-up-to tita_controller --executor sequential \
  --event-handlers console_direct+ \
  --cmake-args -DBUILD_TESTING=OFF -DPython3_EXECUTABLE=/usr/bin/python3
```

SBC logs are saved under `/home/robot/tita_ws/docs/exp/2026-10-16/`:
`flashsac_sbc_deploy.log`, `flashsac_sbc_build.log`, `colcon_build/`, and
`flashsac_sbc_install_check.log` (created after a successful build).
They were also collected into this PC repository date directory.
Build: [flashsac_sbc_build.log](flashsac_sbc_build.log).
Deployment: [flashsac_sbc_deploy.log](flashsac_sbc_deploy.log).
Installation: [flashsac_sbc_install_check.log](flashsac_sbc_install_check.log).

Preflight evidence: [flashsac_sbc_build_preflight.log](flashsac_sbc_build_preflight.log).

## Checks and limits

- Source archive transfer and remote SHA256 verification: PASS.
- Workspace replacement and backup path: PASS, directly observed in SSH output.
- SBC Humble ARM build: PASS, exit 0, four packages finished in 1 minute 5 seconds:
  `ros_utils`, `tita_robot`, `teleop_command`, `tita_controller`. The only stderr
  package entry was `tita_robot`'s architecture diagnostic; no compiler errors.
- Executable architecture: PASS, ARM aarch64 ELF.
- Installed package prefix: PASS, `/home/robot/tita_ws/install/tita_controller`.
- Dynamic linkage: PASS, no `not found` entries; ARM ONNX Runtime 1.19.2,
  `libtita_robot.so` and ROS Humble libraries resolved.
- Installed ONNX/config hashes: PASS, match the selected export.
- `ros2 launch tita_controller flashsac.launch.py --show-args`: PASS,
  default `output_enabled=false`; this introspection did not execute child nodes.
- Existing bringup state: PASS for preservation, still active with original motor
  PID 941 / joystick PID 1075 and unchanged `/opt` execution paths.
- Local required `./scripts/agent-check.sh`: FAIL, exit 1, from pre-existing
  whitespace in `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py`
  at lines 431, 437, 443, 449, 455 and 461. Python syntax: PASS, 462 files;
  URDF parsing: PASS, 8 files. [Log](flashsac_sbc_build_agent_check.log).
- Physical torque sign/unit, left/right mapping, CAN/UART initialization, idle /
  transform-up / RL behavior and control timing: NOT_TESTED.
- Services were not stopped/restarted and the controller was not launched.

Local changes for this operation: workspace README paths, refreshed delivery
archive, setup/runbook report references, and this report/logs. No compiler
compatibility changes were needed; runtime controller code was unchanged. Existing unrelated local changes
are preserved; nothing was staged, committed or pushed.
