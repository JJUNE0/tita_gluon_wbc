# Real-controller velocity bias aligned with sim2sim limits

- Execution Domains: DESKTOP_DRY_RUN (source changes, x86 build, pure math, mocked launch, passive recorded-bag replay), VALIDATION_SIM (passive comparison with actual MuJoCo runtime).
- Evidence Status: PASS for build, implementation parity, logging and computed output bounds; NOT_TESTED for hardware feedback or SBC execution.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Policy config SHA256: `d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d` (unchanged).
- Branch: `agent/codex/dev_tita_gluon`.

The operator clarified that the real controller should use sim2sim's
**velocity bias +/-2 m/s**, with no separate correction-torque cap. This
supersedes the initial 0.3 N m staging cap in
`flashsac_velocity_bias_sim2real.md`. No +/-2 N m configuration was applied.

## Current behavior

| Setting | Current real controller | sim2sim default |
| --- | --- | --- |
| Velocity-bias limit | +/-2 m/s | +/-2 m/s |
| Velocity-bias slew | 3 m/s² | 3 m/s² |
| Neutral acquisition | 2 s | 2 s |
| Integral / seed gains | 4 / 3 | 4 / 3 |
| LPF time constant | 0.1 s | 0.1 s |
| Smooth ramp | 0.25 s | 0.25 s |
| Separate correction-torque cap | None | None |
| Final wheel torque limits, selected policy | +/-12 N m | +/-12 N m |

The optional mode still defaults OFF. When enabled, the observer and law run
at policy cadence and add native wheel velocity target offsets before the
existing PD and motor effort clip. The same 500 Hz eight-joint torque vector
is sent through the original CAN API if output is enabled. Other six joint
torques, raw policy actions/history, command limits, joystick/state handling,
checkpoint and policy configuration are unchanged.

With this policy's Kd=0.5 and radius=0.0925 m, a 2 m/s offset corresponds
to 10.81081 N m additional PD torque per wheel before final clipping. This
is an available bound, not a constant torque. Final policy-plus-bias torque
remains clipped at each motor's configured limit. The velocity limit and
torque limit have different units and are not interchangeable.

Removed the obsolete `velocity_bias_max_torque` launch/node setting and
`TITA_VELOCITY_BIAS_MAX_TORQUE` forwarding. The public/generic launch and
runner explicitly reject stale cap settings before controller startup, so
an old command cannot silently discard its expected cap. Runtime summaries
and startup messages now state +/-2 m/s and 3 m/s², rather than the old Nm
cap/slew. The response-sign argument remains, with the MuJoCo sign +1 as default.

```bash
ros2 launch tita_controller flashsac.launch.py velocity_bias:=true
```

The default output flag is still false. This command shape computes/logs the
selected mode; real torque output additionally requires output_enabled=true.
It was not executed against hardware in this task, and the modified files
were not deployed to SBC.

## Executed validation

Artifacts: `docs/exp/2026-10-17/flashsac_velocity_bias_sim_limits/`.

- PASS: ROS Jazzy x86 colcon build of tita_controller, 13.8 s. Installed launch,
  geometry, policy/config and runner files match sources; `--show-args` lists
  the bias switch/sign and no correction-torque-cap argument.
- PASS: four C++ port tests, including 4,000 original Python PI comparisons
  over both signs, acquisition/reentry, movement/tilt/speed/timing inhibition,
  RL reset, unchanged leg torques and exact OFF-mode baseline calculations.
- PASS: 5,501 real-bag samples replayed against Python's actual default bias
  law. Observer max difference 5.74e-8 m/s. Bias reaches -2 and +2 m/s;
  additional computed torque peak 10.81081081081081 N m; final wheel torque
  peak 12 N m. Tests explicitly check corrections can exceed the former 0.3
  and proposed 2 N m caps, while final motor torque stays bounded.
- PASS: 500 actual MuJoCo runtime samples compared with C++. The Python
  WheelVelocityBias is used without any cap or slew overrides. Holding and
  eligibility agree exactly; velocity max difference 1.21e-6 m/s; bias max
  difference 9.08e-7 m/s; wheel target-offset max difference 9.83e-6 rad/s.
- PASS: 22 logging/launch tests, including the real launch framework with
  mocked service/CAN/controller processes, bias selection propagation,
  removed-cap rejection, invalid-sign rejection, output-disabled behavior,
  MCU initialization order and interrupt cleanup.
- PASS: shell syntax check and installed/source hash comparisons.
- Required repository `./scripts/agent-check.sh`: full output retained in
  `agent_check.log`; existing unrelated whitespace failures are not repaired.

The MuJoCo comparison and bag replay are passive calculations along an
unchanged baseline trajectory. They do not establish corrected closed-loop
motion, a stable hardware feedback sign, or sim-to-real drift improvement.
The sensor/observer implementation still uses relative URDF FK, actual sample
intervals and timing resets; it does not use simulation ground-truth base
velocity. Previously documented inactive telemetry clearing remains.

## Changed files and completion scope

- Runtime: `include/tita_controller/velocity_bias.hpp`, `src/tita_node.cpp`,
  both launch files, and workspace `run_flashsac.sh`.
- Documentation: workspace README and this follow-up experiment entry.
- Verification: `test/sim2real/velocity_bias_runtime.cpp`,
  `test_velocity_bias_port.py`, `compare_velocity_bias_sim_runtime.py`,
  `test_flashsac_logging.py`.

Before snapshots, final task diff and scope/hash records are stored alongside
the logs. Earlier 0.3 N m test artifacts remain intact; current tests write to
the new artifact directory. No sim2sim source, policy weights, geometry or
SDK was changed. No SSH, robot power-on, controller execution, deployment,
commit or push occurred. Hardware feedback direction, real-time performance,
slip/torque calibration and corrected robot behavior remain NOT_TESTED.
