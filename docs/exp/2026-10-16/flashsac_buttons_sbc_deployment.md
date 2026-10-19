# Approved SBC button-code deployment and rebuild

- Execution Domains: ROBOT_STATE_CHANGING (approved source installation/build only), ROBOT_COMMAND_FREE_RUNTIME (pure C++ regression and launch argument inspection), ROBOT_READ_ONLY (checks/log retrieval), DESKTOP_DRY_RUN (repository checks).
- Evidence Status: PASS for deployment, ARM64 build and nine pure button/state scenarios; NOT_TESTED for actual button mapping and robot motion.
- Operator approval: explicitly approved reflecting the new button code on SBC and rebuilding, with no controller run or torque test.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Branch: `agent/codex/dev_tita_gluon`.

## Deployment

Verified baseline source hashes and absence of active controller/joystick/probe
processes; bringup was already inactive. Checked the reviewed archive SHA256:
`65b6d7779f99680c8f2ee061e76b3deffe53a958300fffdfc821b5d2e977b1bd`.
The three existing target files were backed up before replacing them; the new
button header was confirmed absent before installation.

Updated only these production files under `/home/robot/tita_ws`:

- `src/tita_controller/src/tita_node.cpp`.
- `src/tita_controller/include/tita_controller/state_machine.hpp`.
- `src/tita_controller/include/tita_controller/joystick_buttons.hpp` (new).
- `README.md`.

Right hold >=1 s prepares the robot from idle, then a new right press latches
the original velocity-damping stop without waiting one second. Releasing the
startup hold is harmless. Left down selects RL only from sit; left up in RL
blends directly back to sit over 2 s plus 0.2 s settle. Both buttons must first
be seen released. Details are in `flashsac_joystick_buttons.md`.

Also copied the pure C++ regression source into `test/sim2real/` and compiled
its binary there for ARM64 verification. It imports no ROS/CAN/robot SDK and
does not execute physical torque commands. Deployment-time desktop changes are
this report and the status cross-reference in the implementation report.

## Direct validation evidence

- PASS: Humble ARM64 colcon build of `tita_controller`, exit 0, one package,
  28.7 seconds. See `flashsac_buttons_sbc_build.log`.
- PASS: ARM64 pure C++ regression, nine scenario groups, compiled with
  `-Wall -Wextra -Werror -pedantic`; see `flashsac_buttons_sbc_unit_tests.log`.
- PASS: all four deployed source files match desktop SHA256 values, and
  installed policy/config retain pinned hashes.
- PASS: built binary includes right-hold, sit-return, latched-stop and CAN
  send-failure diagnostic strings; runtime linkage has no missing library.
  Binary SHA256: `7bfb4e6a89e545f36438b08571fdf2f6b1bbf4db2e2d64b634ecccad407a5e66`.
- PASS: `ros2 launch tita_controller flashsac.launch.py --show-args` only;
  the controller was not executed. Existing installed runner still matches
  its source, retaining Direct initialization and experiment logging.
- PASS: final inspection lists no motor/joystick/probe executables; service
  remains inactive. See `flashsac_buttons_sbc_verify.log` (22:15:20 KST).
- FAIL: required repository `./scripts/agent-check.sh`, due solely to existing
  whitespace in `my_flat_env_cfg.py` lines 431, 437, 443, 449, 455 and 461.
  Fast Python syntax and eight URDF parse checks pass; see
  `flashsac_buttons_deployment_agent_check.log`.

Pre-change backup: `flashsac_buttons_before_deployment.tar.gz` in the dated
experiment directory on SBC and desktop. Build, regression and verification
logs are saved on both machines. Unrelated tracked work remains unchanged;
tracked diff SHA256 remains
`40076fca037839dbd955f4644f404a0e3ea6c8b5e7a3fc86a79bb15150ddab47`.

## Remaining limits

No controller, joystick reader, MCU mode sequence, robot-motion test, service
change or torque output was run during this deployment. Actual mapping of
lower buttons to default axes left=4/right=6 still needs output-disabled
verification. Sit is a pose hold, not policy balance; transition/stop behavior
on the supported robot remains NOT_TESTED. Stop requires process restart to
clear and uses velocity damping, not electrical power isolation. Existing SDK
shutdown issues are unchanged. No commit or push.
