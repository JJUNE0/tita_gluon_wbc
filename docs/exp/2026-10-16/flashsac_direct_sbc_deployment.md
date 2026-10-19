# Approved Direct-startup SBC deployment

- Execution Domains: ROBOT_STATE_CHANGING (approved source installation/build only), ROBOT_COMMAND_FREE_RUNTIME (launch argument introspection), ROBOT_READ_ONLY (inspection/log retrieval), DESKTOP_DRY_RUN (repository checks).
- Evidence Status: PASS for SBC build, installed parity and static/runtime-link checks; NOT_TESTED for torque-enabled revised launcher, posture transitions and RL.
- Operator approval: explicitly approved SBC installation and rebuild, with no controller execution or additional torque tests.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Branch: `agent/codex/dev_tita_gluon`.

## Installed changes

Verified the four existing SBC source files against the archived known baseline,
and confirmed no active controller/probe and inactive vendor bringup. Verified
the approved archive SHA256
`5dd07adec3f0cfe920584359a56d127b7385051f34c75f5fbf9b86bd5a5acbab`
before extraction into `/home/robot/tita_ws`.

Deployed only:

- `run_flashsac.sh`: log-first Ready -> Direct requests for output true; false
  skips mode requests; failed requests prevent node startup. Also includes the
  previously tested repeated-Ctrl+C cleanup fix.
- `src/tita_controller/launch/flashsac.launch.py`: public entrypoint/help documenting
  the automatic Direct startup path through the logged runner.
- `src/tita_controller/src/tita_node.cpp`: prepared send-failure guard, latching
  further torque commands off on failed SDK send or exception.
- `README.md`: startup documentation.

Pre-change versions are backed up in
`docs/exp/2026-10-16/flashsac_direct_before_deployment.tar.gz` on SBC and desktop.
No unrelated workspace files, SDK libraries or policy artifacts were replaced.
The desktop modifications in this approval turn are this report and the status
cross-reference in `flashsac_direct_startup_fix.md`.

## Executed validation

- PASS: Humble ARM64 `colcon build --packages-select tita_controller` with
  `BUILD_TESTING=OFF` and `/usr/bin/python3`: one package finished in 26.8 s,
  command exit 0. See `flashsac_direct_sbc_build.log`.
- PASS: installed runner and public launch compare byte-for-byte with their
  sources. All four deployed source hashes match the reviewed desktop sources.
- PASS: `bash -n` on source/installed runners and Python compile on launch.
- PASS: `ros2 launch tita_controller flashsac.launch.py --show-args` only;
  confirms default output false and updated Direct-startup help without node execution.
- PASS: `ldd` has no missing dependency; built binary contains the send-failure
  latch diagnostic. Binary SHA256:
  `b8aa1e74eeeff2e34dc544edbce31180e7de75b1bda6ad02620e08600a122f11`.
- PASS: installed ONNX and config retain the pinned expected hashes.
- PASS: final process inspection lists no motor/joystick/probe executables;
  vendor bringup remains inactive. See `flashsac_direct_sbc_verify.log`.
- Previously executed desktop regression suite: 18 PASS, retained in
  `flashsac_direct_tests.log`; unchanged implementation was not retested needlessly.
- FAIL: mandatory `./scripts/agent-check.sh`, solely pre-existing whitespace in
  `my_flat_env_cfg.py` lines 431, 437, 443, 449, 455 and 461. Fast Python syntax
  and eight URDF parse checks pass. See `flashsac_direct_deployment_agent_check.log`.

## Scope and remaining limits

No controller, joystick reader, MCU initialization script, service restart or
torque command was executed during this deployment. The earlier observed MCU
mode was not deliberately changed. The updated controller has not been run
with torque output enabled; actual standing/RL stability remains NOT_TESTED.
Independent Direct-mode ACK is unavailable in this SDK. SDK destructor hangs
and joystick shutdown crashes remain unresolved; bounded group cleanup remains
available. No commit, push or additional package deployment occurred.
