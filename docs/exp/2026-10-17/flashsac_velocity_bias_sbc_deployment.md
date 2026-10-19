# Approved velocity-bias SBC deployment and build

- Execution Domains: ROBOT_STATE_CHANGING (approved source replacement and build), ROBOT_COMMAND_FREE_RUNTIME (pure calculation replay and launch metadata inspection), ROBOT_READ_ONLY (process/hash/linkage checks), DESKTOP_DRY_RUN (artifact preparation and repository checks).
- Evidence Status: PASS for deployment, ARM64 build, installed hashes and passive replay; NOT_TESTED for corrected physical motion and hardware feedback sign.
- Operator approval: robot powered on by the operator; explicitly requested uploading velocity-bias code and building, without starting the controller or a torque test.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Config SHA256: `d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d`.
- Branch: `agent/codex/dev_tita_gluon`.
- Final SBC verification time: 2026-10-17 12:56:39 KST (03:56:39 UTC in SBC output).

## Deployed behavior

The selected implementation is the operator-approved sim2sim configuration:
velocity bias +/-2 m/s, slew 3 m/s², two-second neutral hold, seed/integral
gains 3/4, LPF tau 0.1 s and 0.25 s ramp. There is no separate correction-torque
cap. The final selected-policy wheel torque is still clipped at +/-12 N m.
The mode defaults OFF; output_enabled also defaults false.

Bias changes the two wheel velocity targets before existing PD/effort clipping
inside the current controller. The same eight-joint torque vector is sent
through the existing CAN method. No additional CAN transmitter or controller
thread was introduced. Original action history, other six joint torque paths,
joystick/state behavior, policy weights and command limits are retained.

Updated these ten production/documentation targets under `/home/robot/tita_ws`:

- `src/tita_controller/src/tita_node.cpp`.
- `src/tita_controller/include/tita_controller/adapter.hpp`.
- `src/tita_controller/include/tita_controller/velocity_bias.hpp` (new).
- `src/tita_controller/config/velocity_bias_geometry.json` (new).
- `src/tita_controller/launch/flashsac.launch.py` and `launch/tita.launch.py`.
- `src/tita_controller/CMakeLists.txt` and `package.xml` (Eigen dependency/config install).
- Workspace `run_flashsac.sh` and `README.md` (argument forwarding, logs and documentation).

Four additional test payload files provide the pure C++ fixture, standard-library
comparison script, input samples and independent Python-reference outputs.
All are under `test/sim2real/`, separate from the production executable.
The desktop's ARM comparison script is the only new local code in this
deployment task; the production implementation was already prepared and tested.

## Backup, integrity and build

Preflight found the vendor bringup active and no FlashSAC tita_node process.
The current policy/ONNX hashes matched the prepared bundle. Eigen headers and
CMake discovery were available on SBC; no dependency installation was needed.

All eight existing production targets were backed up before replacement;
the new header/geometry and test files were absent. Backup and existence/hash
records are preserved on both machines in
`docs/exp/2026-10-17/flashsac_velocity_bias_sbc_deploy/`.

- Backup `before_deployment.tar.gz` SHA256:
  `6a6fed751cdcfeb4567caf2cf29fc7ea665c7056c739e3c1b1d18d025c6ba8ac`.
- Reviewed deployment payload SHA256:
  `543dd9be997eb80302b7d22c05236747012d156c754d927fcd39b9b7396f50ad`.
- PASS: every archive member and all 14 deployed file hashes verified against
  the desktop manifest before/after installation.
- PASS: ROS Humble ARM64 `colcon build --packages-select tita_controller
  --event-handlers console_direct+`, exit 0; one package finished in 38.5 s.
- Built SBC executable SHA256:
  `c82c5c36ba44e36c89671d8aa53c1368296000537898d6de5b5af421f6e0160a`.
- PASS: installed launch, geometry, policy/config and runner match sources;
  installed bundle passes pinned hash validation; runtime linkage has no
  missing shared libraries.

## Validation without robot commands

The pure C++ test executable imports neither ROS nor the robot SDK. It was
compiled and run on ARM with 5,501 recorded sensor/action samples and compared
with the independent Python reference prepared on the desktop. This is a
passive replay along a baseline recording, not a corrected robot trajectory.

- PASS: all 5,501 samples within parity tolerances.
- Maximum velocity estimate error: 5.74e-8 m/s.
- Maximum bias error: 5.95e-8 m/s.
- Maximum wheel target-offset error: 9.51e-7 rad/s.
- Maximum corrected-torque error: 7.16e-6 N m.
- Bias remains within +/-2 m/s, final wheel torque within +/-12 N m, and
  other six joint computed torques equal their baseline values exactly.

The first additional fixture compilation used `-I/usr/include/eigen3` with
`-Werror`; Ubuntu's older ARM Eigen NEON header triggered class-memaccess
warnings treated as errors. The production controller build had already
succeeded. Recompiling the fixture with Eigen as a system include
(`-isystem /usr/include/eigen3`), matching production's dependency treatment,
passed with strict warnings for project code. No production source or Eigen
header was changed to bypass the diagnostic. Initial `verify.log` and passing
`verify_final.log` are both retained.

PASS: installed launch modules imported for parameter/hash checks only;
33 observations, eight actions and 50 Hz policy cadence validate. `ros2 launch
tita_controller flashsac.launch.py --show-args` lists velocity_bias and
velocity_bias_response_sign, with no obsolete torque-cap argument. It does
not execute the logged runner or create the robot controller.

## Runtime state and limits

No service start/stop, MCU Ready/Direct request, motor-node execution, joystick
reader startup or physical torque test was performed by this task. Final
inspection finds no tita_node process; the pre-existing vendor bringup remains
active. Running the public launch later retains its documented automatic
bringup-stop/recording/Direct-init behavior; merely uploading/building did not
trigger those actions.

Hardware feedback direction, sensor frame/timing, slip, actual torque units,
500 Hz real-time performance and corrected physical balance remain NOT_TESTED.
The available +/-2 m/s correction can correspond to about 10.81 N m extra PD
torque per wheel before the final clip; successful passive replay does not
establish stable closed-loop hardware response.

## Logs and completion

The artifact directory on desktop and SBC retains payload/manifest, backup,
before-state hashes, build output, initial/final verification, and ARM replay
output. Local `preflight.log` and `backup.log` are also mirrored to SBC.

Required repository `./scripts/agent-check.sh`: see
`flashsac_velocity_bias_sbc_deploy/agent_check.log`. Existing unrelated
trailing-whitespace failures are not modified. Final task scope/hash records
are saved as `completion_integrity.json`. No commit or push.
