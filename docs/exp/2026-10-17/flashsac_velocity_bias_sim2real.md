# FlashSAC optional velocity bias in the real-controller torque path

- Execution Domains: DESKTOP_DRY_RUN (implementation, x86 build, pure tests, passive bag replay and mocked launch), VALIDATION_SIM (passive comparison against the actual MuJoCo runtime).
- Evidence Status: PASS for implementation/build/parity/launch logging; NOT_TESTED for hardware feedback sign, corrected hardware trajectory and SBC execution.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Policy config SHA256: `d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d` (unchanged).
- Branch: `agent/codex/dev_tita_gluon`.

The operator requested a sim2real `velocity_bias:=true` argument corresponding
to sim2sim's `--velocity_bias`, and asked whether extra torque can be sent
over the existing CAN connection. It can: the controller modifies the final
wheel PD calculation inside the current motor loop, then sends the same
eight-element torque vector through the existing SDK method. It creates no
additional CAN sender, IDs, process or controller thread.

## Data flow and behavior

```text
flashsac.launch.py arguments
 -> logged run_flashsac.sh environment and summary
 -> tita.launch.py node parameters
 -> C++ IMU/encoder/relative-FK observer + velocity-bias integral (policy cadence)
 -> native wheel velocity target offsets
 -> existing PD and per-motor torque clip (500 Hz)
 -> existing output_enabled gate -> one set_target_joint_t() call per loop
```

The public launch accepts:

```bash
ros2 launch tita_controller flashsac.launch.py velocity_bias:=true
```

This retains default `output_enabled:=false`: it computes and records policy
and correction without torque transmission. Physical output additionally
requires `output_enabled:=true`. The public wrapper still performs the existing
service/recorder/MCU Direct startup flow when used on the robot; it was not
executed against hardware during this task.

`velocity_bias:=false` remains the default. Actor weights, observation/action
layout, raw action history, joystick/button sequence and motor torque limits
are unchanged. This mode runs an adaptive velocity offset with an integral;
it introduces no RLS, model identification, LQR gain/reference update or probing.

The observer uses IMU orientation/gyro, native eight-joint encoders and relative
wheel/base FK. It ports the sim2sim rolling-speed-minus-FK-offset-rate formula,
without using base position or translational velocity ground truth. Geometry
is extracted from the existing URDF into an installed JSON containing the
source URDF path/hash, joint origins, axes and wheel radius 0.0925 m.
Original URDF SHA256:
`0941b83136cd5c8c89bbb33165bff515a3a988d33319b67c8b06bfb9c71350ce`.

Holding enters below absolute command [0.02, 0.02, 0.03] and exits at
[0.04, 0.04, 0.06], matching sim2sim hysteresis. After two seconds of holding,
the law uses the same velocity seed gain 3, integral gain 4, LPF tau 0.1 s
and smooth 0.25 s ramp. Tilt above 0.3 rad or estimated speed above 1 m/s
inhibits adaptation. Movement clears the integral and slews correction to
zero; RL exit, policy/CAN faults and invalid timing clear the controller.
Actual steady-clock sample intervals are used; intervals above 60 ms reset
the bias. Inactive age/velocity telemetry is cleared, whereas Python's runtime
retains its last inactive sample; this does not change the law or torque.

## Hardware staging limits and torque meaning

The simulation's +/-2 m/s offset corresponds to approximately +/-10.81 N m
per wheel with Kd=0.5 and radius=0.0925 m. The new real-controller default
instead caps additional PD torque at **0.3 N m per wheel**, with equivalent
0.3 N m/s slew. This is a conservative initial software bound, not a verified
hardware tuning or a claim that it is sufficient to remove the observed drift.

```text
omega_target_i = omega_policy_i + native_sign_i * bias_m_s / wheel_radius
tau_i = clip(Kd_i * (omega_target_i - omega_measured_i), motor_effort_limit_i)
```

Offsets are added before final PD clipping, rather than adding to an already
clipped torque. Other six joints retain their baseline torque calculation.
For unequal wheel Kd, the common bias limit uses the larger Kd, bounding both
additional torques. Saturation can make the actual final difference smaller.

Arguments `velocity_bias_max_torque:=0.3` and
`velocity_bias_response_sign:=1.0` select the cap and low-frequency response
sign. The staged cap range is (0, 1] N m per wheel; sign is exactly +/-1.
The public launch rejects invalid values before constructing its runner.
`+1` is the MuJoCo closed-loop feedback sign, distinct from native motor
kinematic signs. Hardware feedback direction, sensor frame/timing, actuator
torque units and slip remain unvalidated; successful simulation and passive
replay do not establish stable hardware feedback.

## Logs

The existing torque topic contains the final eight-joint computed command.
New `/sim2real/debug/velocity_bias` has 11 fields:

```text
holding, eligible, hold_age_s, v_hat_m_s, filtered_v_m_s, integral_m_s,
bias_m_s, wheel_offset_L_rad_s, wheel_offset_R_rad_s,
actual_added_computed_torque_L_Nm, actual_added_computed_torque_R_Nm
```

The runner records this topic and logs enabled/cap/sign/acquisition/slew,
policy/config hashes, geometry hash, and installed binary/runner hashes when
present. The final two diagnostic values are the difference between corrected
and uncorrected computed torque after clipping, not measured applied torque.

## Validation actually executed

Artifacts are in `docs/exp/2026-10-17/flashsac_velocity_bias/`.

- PASS: x86 ROS Jazzy colcon build, 15.3 s; final installation refresh 0.40 s.
  Installed launch/config/geometry/policy/runner copies match source. Installed
  `--show-args` lists the three new arguments without starting controller nodes.
- PASS: four C++ port tests, compiled with strict warnings, including 4,000 PI
  updates across both signs, acquisition/movement/reentry, tilt/speed/timing
  inhibition, RL reset, zero OFF-mode difference and torque/leg invariants.
- PASS: 5,501 timestamp-aligned samples from the finalized real bag
  `flashsac_60000_223217_076704901_output_true` replayed passively. Maximum
  FK velocity difference from the Python URDF observer is 5.74e-8 m/s;
  additional computed torque peak is 0.3000000000000007 N m (floating error).
  Bias range is +/-0.0555 m/s; 1,142 samples satisfy eligibility. No corrected
  robot trajectory or closed-loop improvement is inferred.
- PASS: actual MuJoCo `WheelVelocityBias` versus C++ on 500 sensor samples,
  using the same reduced cap/slew and a baseline-only simulated plant.
  Maximum velocity difference 1.21e-6 m/s; bias difference 1.78e-8 m/s;
  holding and eligibility match exactly. Inactive telemetry is normalized as
  described above. This is implementation parity, not a new closed-loop trial.
- PASS: 21 mocked logging/launch tests, including real ROS launch orchestration
  of mock processes, argument propagation, invalid-cap rejection before runner
  construction, output-disabled/no-CAN mode, Direct startup order, recorder
  failure and interrupt cleanup. No physical CAN API is exercised.
- PASS: existing baseline observation/torque/state parity: 50 observation
  samples, max error 1.20e-7; RL torque 7.17e-6 N m; state torque 1.17e-4 N m;
  0/6,000 state mismatches. Nine existing pure button/state scenarios pass.
- Required repository `./scripts/agent-check.sh`: output in `agent_check.log`.
  Existing unrelated trailing-whitespace failures are retained rather than fixed.

Initial nonfinal validation logs are preserved: a targeted invocation replaced
ROS PYTHONPATH, another lacked writable ROS_LOG_DIR, and unittest discovery
was incorrectly used for a script-style button check (the script's nine cases
ran, but discovery returned no unittest cases). Final invocations preserve ROS
paths/use a task-local ROS log directory and execute the button script directly.
The first actual-MuJoCo comparison also exposed inactive age/velocity telemetry
differences; the final comparison normalizes those inactive fields and still
checks all holding/eligible/control values. See final logs for successful results.

## Changed files and scope

- `sim2real/tita_ws/src/tita_controller/src/tita_node.cpp`: optional controller,
  state/fault gating, final torque integration and diagnostics. Removed one
  pre-existing duplicate `joy_mutex_` declaration to make this file compile;
  the before snapshot preserves that duplication.
- `include/tita_controller/adapter.hpp`: optional native wheel target offsets.
- New `include/tita_controller/velocity_bias.hpp`: observer and bias law.
- New `config/velocity_bias_geometry.json`: extracted URDF geometry/provenance.
- `launch/flashsac.launch.py`, `launch/tita.launch.py`, workspace
  `run_flashsac.sh`: optional arguments, forwarding, validation and logs.
- `CMakeLists.txt`, `package.xml`: Eigen build dependency and geometry install.
- Workspace README and four files in `test/sim2real/` document/verify the feature.

`before.json` preserves current-task starting versions; `task_changes.diff`
and `completion_integrity.json` record the final change scope and hashes.
No sim2sim production code, checkpoint/config, unrelated tracked changes,
robot services or SBC files were modified. No commit, push, deployment or
physical command was performed. SBC build, real-time timing and hardware
closed-loop behavior are NOT_TESTED.
