# sim2real/tita_ws: minimal real-robot runtime with the sim2sim state machine

Execution Domain: DESKTOP_DRY_RUN (build, parity test, node start without CAN). No robot command was run.

Policy Checkpoint SHA256: `3fd6113b95be69e0956f1510d4002dd161bc7226e0f1d9ade205117fc3edaed6`
(`tita_flash_sac_172127_928297/model_100000`, used for the parity fixture and launch test).
ONNX SHA256: `e9c40d1af7e6a9e54f6336ef684927d3806f1a46ef02c34a91bd1ed732382039`

Evidence Status: PASS for build and C++/Python parity. Robot behavior: NOT_TESTED.

## Change

New `sim2real/tita_ws/src/tita_controller` (C++, one node, no ros2_control):
`state_machine.hpp` (port of sim2sim `state_machine.py`, with `damp` instead of `idle` as the
start state), `adapter.hpp` (port of `adapter.py`), `tita_node.cpp` (500 Hz loop on the
`tita_robot` CAN API, policy at the checkpoint rate, ELRS joystick switches for state requests),
`launch/tita.launch.py` (flattens the sim2sim `config.json` into node parameters).
Vendor `tita_robot`, `teleop_command`, `ros_utils` copied unchanged. `tita_gluon_ws` unchanged.

Removed relative to `tita_stage1_controller` + `hardware_bridge`: policy SHA checks, takeover token,
stage 1/2 split, 118 metadata command interfaces, CSV write log, settle/envelope/clipping gates,
ros2_control. Kept: leg_2 encoder wrap, torque mode (`set_target_joint_t`), data-staleness and
tilt -> damp, torque clipping, motor output off by default (`output_enabled`).

## Evidence

- `test/sim2real/test_sim2real_parity.py` (`sim2real_parity.log`): on 50 random states, C++ vs
  sim2sim Python observation max error 1.2e-7 (33 dims), RL torque 7.2e-6 Nm; state machine
  torque 1.2e-4 Nm over 6000 steps (Python uses float32 constants), 0 state mismatches, reached sit.
- `colcon build` (`sim2real_build.log`): 4 packages, exit 0, no warnings (system Python in PATH).
- Desktop launch, `output_enabled:=false` (`sim2real_desktop_launch.log`): policy and parameters
  load, read-only warning printed; no CAN device, so the loop stays in damp.
  Shutdown hangs: the vendor `tita_robot` destructor blocks when `can0` is absent
  (reproduced with a standalone program); launch escalates to SIGTERM.
- Not tested: real CAN/IMU data, joystick axis signs, loop timing on the robot, any motor output.
