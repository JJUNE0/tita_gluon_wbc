# Approved SBC speed-limit deployment and build

- Execution Domains: ROBOT_STATE_CHANGING (approved file installation and build), ROBOT_COMMAND_FREE_RUNTIME (installed launch imports and argument inspection), ROBOT_READ_ONLY (hash/process/service checks), DESKTOP_DRY_RUN (repository checks).
- Evidence Status: PASS for SBC installation, build and installed parameter/hash validation; NOT_TESTED for motion with the new limits.
- Operator approval: explicitly requested immediate SBC deployment and build.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Config SHA256: `d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d`.
- Branch: `agent/codex/dev_tita_gluon`.
- Verification time: 2026-10-16 22:31:19 KST (SBC reports 13:31:19 UTC).

## Changes and deployment

Updated exactly two production files in `/home/robot/tita_ws`:

- `src/tita_controller/policies/flashsac_60000/config.json`: maximum forward/reverse command is now +/-1.0 m/s; maximum yaw command is +/-1.0 rad/s.
- `src/tita_controller/launch/flashsac.launch.py`: config hash updated to accept that configuration.

Both source files and their installed copies match the desktop files.
Launch SHA256: `4da431992f99db2a7fc7db0893e48c3a0a3684db3ef04bea3552ee4cfdd8390d`.
The previous command limits were 0.2 m/s and 0.3 rad/s. Existing 0.5 units/s
command ramp remains, requiring approximately 2 s from zero to full command.
Policy weights, actuator gains, torque limits and button transitions are unchanged.

Before replacement, the two original files were archived as
`flashsac_speed_limits_before_deployment.tar.gz` in the dated experiment
directory on both SBC and desktop. Archive SHA256:
`f7361235cc626249509e0472bdc21843bc3b052a8fabe81df78297fea1f445d7`.
Transfer hashes were checked before installation.

## Direct evidence

- PASS: ROS Humble ARM64 `colcon build --packages-select tita_controller --event-handlers console_direct+`, exit 0; one package completed in 1.87 s. C++ target was already current; updated config and launch were installed.
- PASS: installed public launch accepts checkpoint/ONNX/config hashes; generic launch forwards both 1.0 limits, 33 observations, eight actions and 50 Hz policy cadence.
- PASS: installed config and public launch match their SBC sources and desktop SHA256 values.
- PASS: `ros2 launch tita_controller flashsac.launch.py --show-args` lists arguments without starting the runner/controller.
- PASS: binary SHA256 remains `7bfb4e6a89e545f36438b08571fdf2f6b1bbf4db2e2d64b634ecccad407a5e66`; installed ONNX retains its pinned hash.
- PASS: final `/proc` inspection of executable arguments finds no motor controller or joystick executable; bringup remains inactive.

The initial broad `pgrep -af` in the verification command matched the
verification shell itself because its command text included a binary path.
That check exited 1; the log retains it. A corrected read-only inspection
compared each process's actual argv[0] and completed successfully, as shown
at the end of the verification log. No process was killed or started.

Logs: `flashsac_speed_limits_sbc_preflight.log`,
`flashsac_speed_limits_sbc_build.log`, `flashsac_speed_limits_sbc_verify.log`.
Required repository check: `flashsac_speed_limits_deployment_agent_check.log`.
The overall check remains blocked by existing trailing whitespace in
`my_flat_env_cfg.py`; Python syntax and URDF check results are in that log.
Tracked diff SHA256 remains
`40076fca037839dbd955f4644f404a0e3ea6c8b5e7a3fc86a79bb15150ddab47`.

## Limits

No physical controller execution, MCU mode request, service change or torque
test occurred. Existing backward drift and shutdown behavior remain unresolved.
The new limits are requested policy inputs, not verified chassis speeds.
The bundle manifest remains the original export/parity provenance record;
the new deployment config hash is recorded separately here and in launch.
No commit or push.
