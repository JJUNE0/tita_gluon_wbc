# Single-command FlashSAC launch with automatic bringup stop

- Date: 2026-10-16 (Asia/Seoul)
- Execution Domain: DESKTOP_DRY_RUN (implementation/mock validation), ROBOT_READ_ONLY (permission query), ROBOT_STATE_CHANGING (SBC code update/build only).
- Evidence Status: PASS for local/SBC builds, 11 mock/integration tests and static installation checks; physical runtime NOT_TESTED.
- Branch: agent/codex/dev_tita_gluon
- Policy Checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`
- ONNX Hash: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`
- Delivery archive SHA256: `d1323b080944ca8da196e160330eac11c3279038ce04ff6bd36d3c35a094587e`

## Operator command and behavior

```bash
cd ~/tita_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch tita_controller flashsac.launch.py
```

The public launch validates the pinned policy bundle before constructing an
installed logged-runner process. The runner creates console/summary logs, checks
the installed workspace prefix, records the existing service state, and stops
`tita-bringup.service` using exactly
`sudo -n /usr/bin/systemctl stop tita-bringup.service` when necessary. A read-only
`sudo -n -l` check confirmed the existing operator permission; sudoers/polkit was
not modified. No sudo command to stop a service was executed during development.

The runner confirms bringup is no longer active and waits up to five seconds
for any old controller/joystick process to disappear. Failure at either step
prevents the new controller from starting. Recording starts next; only after
the SQLite database is created does the runner invoke generic `tita.launch.py`
with the installed pinned policy. This avoids public-launch recursion.

Default controller torque output remains false. Because service stopping changes
runtime state, the public launch is classified ROBOT_STATE_CHANGING even with
output disabled. The robot must be supported before the operator launches it.
`output_enabled:=true` remains the explicit actuator-output selection.
Idle retains original velocity damping and transform-up/ready/RL order is unchanged.

Ctrl+C ends the inner launch and finalizes rosbag; the old service is never
automatically restarted. Public launch shutdown allows 20 seconds before SIGTERM
and another 10 seconds before SIGKILL. Recorder failure also ends the inner launch.
`./run_flashsac.sh false|true` remains an alias for the public launch.

All controller/session/rosbag logs are under workspace `docs/exp/YYYY-MM-DD/`.
A sourced ament environment hook also sets the outer ROS launch log path there.

## Changed files

- `sim2real/tita_ws/src/tita_controller/launch/flashsac.launch.py`: public launch invokes installed runner, retains hash checks and default output gate.
- `sim2real/tita_ws/run_flashsac.sh`: public alias/internal runner, automatic service stop, stop-state/process checks, generic internal launch.
- `sim2real/tita_ws/src/tita_controller/CMakeLists.txt`: install runner and register log environment hook.
- `sim2real/tita_ws/src/tita_controller/env/flashsac_logs.sh.in`: initialize ROS_LOG_DIR during workspace setup.
- `sim2real/tita_ws/README.md`: one-command operator instructions.
- `test/sim2real/test_flashsac_logging.py`: mock service/sudo scenarios and real ROS launch engine with mocked children.
- This report, task diff, delivery archive and logs.

The controller C++ code, frozen actor and gains are unchanged. Old archive
`/home/robot/flashsac_60000_source_6e3ed6d41e91.tar.gz` remains available on SBC.

## Executed checks

- Local `colcon build --packages-select tita_controller`: PASS.
- `test/sim2real/test_flashsac_logging.py`: PASS, 11 tests. Covers automatic stop,
  already inactive service, permission denial, unsuccessful stop, lingering old
  processes, no launch without storage, recorder exit, logging/finalization,
  explicit output selection, policy validation ordering and public-to-internal
  launch without recursion. The real ROS launch engine test uses fake systemctl,
  sudo, rosbag and controller commands, not hardware or real service operations.
  [Log](flashsac_auto_stop_tests.log).
- Bash syntax and Python compile checks: PASS.
- Environment hook and installed launch `--show-args`: PASS. Initial hook used
  AMENT_CURRENT_PREFIX, which retained the ROS underlay prefix during optimized
  colcon setup; the hook was corrected to the configured installation prefix.
  Rebuild and a resolved-path assertion confirmed logs stay inside the workspace.
  [Log](flashsac_auto_stop_hook_check.log).
- SBC Humble build: PASS, `tita_controller` finished in 1.12 s, colcon exit 0.
  [Log](flashsac_auto_stop_sbc_build.log). Previous 39 deployment file hashes
  were checked before extraction to avoid overwriting pre-existing user edits.
- SBC installed runner/source comparison, Bash/Python syntax, policy hash,
  environment hook, launch arguments and logged-runner action construction: PASS.
  No constructed action was executed. Existing bringup remains active with
  controller PID 941 and joystick PID 1075. [Log](flashsac_auto_stop_sbc_check.log).
- Final SBC/PC source, policy, README and runner comparison: PASS, 40/40 file
  SHA256 values match. Final task diff inspected:
  [flashsac_auto_stop_changes.patch](flashsac_auto_stop_changes.patch).
- Required `./scripts/agent-check.sh`: FAIL from the existing trailing whitespace
  in `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py`
  at lines 431, 437, 443, 449, 455 and 461. Python syntax: PASS, 462 files;
  URDF XML: PASS, 8 files. [Log](flashsac_auto_stop_agent_check.log).
- Final changed script/launch/hook diff integrity: PASS. Tracked working-tree
  diff SHA256 is unchanged at
  `40076fca037839dbd955f4644f404a0e3ea6c8b5e7a3fc86a79bb15150ddab47`;
  the index remains empty. Logs are retained on both SBC and PC.

Permission evidence: [flashsac_auto_stop_permission_check.log](flashsac_auto_stop_permission_check.log).
No controller launch, CAN/UART access, service stop/restart or physical actuation
was performed on SBC. Actual stop-and-run behavior, actuator signs/units and
real rosbag collection remain NOT_TESTED. Existing unrelated changes are preserved;
nothing was staged, committed or pushed.
