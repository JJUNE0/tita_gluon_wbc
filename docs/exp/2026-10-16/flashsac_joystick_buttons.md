# FlashSAC lower-button control changes

- Execution Domain: DESKTOP_DRY_RUN.
- Evidence Status: PASS for local regression/parity/build and subsequently approved SBC deployment/build; NOT_TESTED for physical button mapping and robot motion.
- Policy checkpoint SHA256: `6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05`.
- ONNX SHA256: `f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a`.
- Branch: `agent/codex/dev_tita_gluon`.

## Final requested behavior

The operator corrected the right-button behavior during implementation: it
requires a continuous one-second press to start from idle; later a NEW press
stops immediately. Releasing the startup press does not stop. The left button
remains a latching selector: down enters RL only from sit; up during RL returns
directly to sit instead of idle. Software stop uses the original idle velocity
damping, as explicitly selected by the operator.

Both buttons must first be observed released. Already-held startup buttons
cannot start movement. Short right presses cancel; their time does not accumulate.
The startup hold is consumed and cannot also trigger stop. A later right press
has priority over a simultaneous left input. Stop is latched until process
restart and cannot be cleared by subsequent button or fault requests.
Invalid/stale joystick input after enabling also latches the damping stop.

RL return interpolates measured joint pose directly to the sit target for
2 seconds, followed by the original 0.2-second settle interval, without the
splay stage. A smoothstep blend also transitions from the previous computed
torque to the sit PD torque, preserving torque limits. Commands and previous
policy action are cleared outside RL. Pressing left too early does not queue
automatic RL: a fresh left down edge is required after sit completes.

## Changed files

- `sim2real/tita_ws/src/tita_controller/src/tita_node.cpp`: button decoding and
  monotonic hold timing integration, parameterized axis indices, stop logging,
  command clearing and measured-pose/previous-torque return entry.
- `sim2real/tita_ws/src/tita_controller/include/tita_controller/joystick_buttons.hpp`:
  pure button edge/hold/interlock logic.
- `sim2real/tita_ws/src/tita_controller/include/tita_controller/state_machine.hpp`:
  ReturnToSit and latched EStop states, smooth return and original stop damping.
- `sim2real/tita_ws/README.md`: revised operator procedure and test instructions.
- `test/sim2real/joystick_buttons_runtime.cpp`, `test_joystick_buttons.py`:
  standalone C++ behavior regression using the actual production headers.
- `test/sim2real/test_sim2real_parity.py`: keep its temporary fixtures/binary
  inside test/ as required by the repository instructions.

## Executed verification

- PASS: nine button/state scenario groups, compiled with C++17, Wall/Wextra,
  Werror and pedantic. Includes held-start interlock, exact one-second boundary,
  short-hold cancellation, consumed startup press, left selection and early-RL
  rejection, measured-pose/torque continuity, torque clipping, right-stop
  priority, link loss and irreversible damping stop from all phases.
  See `flashsac_joystick_buttons_tests.log`.
- PASS: desktop Jazzy colcon build of tita_controller, exit 0, one package,
  12.1 seconds. See `flashsac_buttons_desktop_build.log`.
- PASS: unchanged sim2sim observation/action/initial-transform parity: observation
  error 1.20e-7 across 50 samples, RL torque error 7.17e-6, state-machine torque
  error 1.17e-4, zero state mismatches across 6,000 steps.
  See `flashsac_buttons_parity.log`.
- Initial return test FAIL: endpoint roundoff left a tiny difference in held
  sit torque. The return now sets the exact sit target after interpolation;
  final scenario suite passes. Original failure retained in
  `flashsac_buttons_initial_failure.log`.
- Mandatory `./scripts/agent-check.sh`: FAIL from pre-existing trailing whitespace
  in `my_flat_env_cfg.py` lines 431, 437, 443, 449, 455 and 461. Fast Python syntax
  and eight URDF parse checks pass. See `flashsac_buttons_agent_check.log`.

## Limits and deployment status

Default node axis parameters are left=4 and right=6 based on the DDT two-position
channel convention, down=-1/up=+1. Physical lower-button mapping is NOT_TESTED;
confirm with output disabled before hardware deployment. These are startup
parameters, not runtime reconfiguration. Mid-position/non-finite/out-of-range
button data is invalid. Immediate stop means on receipt/processing of a fresh
right press, without a one-second delay; it is not an electrical emergency stop.
With invalid robot sensors the existing zero-command path still takes precedence
over computing damping from invalid velocity data.

Sit completion remains time based, and sit holds leg pose without RL balance
control. Smooth return and software stop require supported-robot verification;
the local tests do not establish balance or actuator performance. Earlier SDK
shutdown issues remain unresolved. Existing policy, adapter, 50 Hz inference,
500 Hz loop, Direct-startup sequence and logging are retained. No residual,
RLS, probing or adaptive gain/bias/reference updates were added.

No robot connection, deployment, controller execution or torque test occurred
during the initial local implementation task. The operator subsequently approved
SBC deployment/rebuild, which completed without controller execution; see
`flashsac_buttons_sbc_deployment.md`. No commit or push.
