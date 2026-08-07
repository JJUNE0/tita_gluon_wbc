# GLUON ID6 zero and software-limit update

- Execution Domain: `DESKTOP_DRY_RUN`, `VALIDATION_SIM`
- Date: 2026-08-04
- Policy Checkpoint SHA256 or ONNX Hash: N/A (robot model and controller-interface change)
- Evidence Status: `SUSPICIOUS`; both unsafe startup attempts were blocked and the startup-order fix builds, but its physical hold remains `NOT_TESTED`

## Requested contract

- Preserve the existing calibration of joints 1-5.
- Make actuator ID6 an active `axis_joint_6` revolute joint.
- Define the current physical ID6 pose as `q6=0`.
- Enforce a symmetric software range of `[-150, +150] deg`.
- Do not command or move the physical robot during this update.

## Assumptions and unresolved measurements

- Historical single-ID6 enable evidence measured position near zero
  (`0.000488 turns`), and the operator manually returned ID6 near turns zero.
- The first all-joint startup read ID6 at `-95.252563 turns`. A second startup,
  after temporarily using that value as an offset, read ID6 at `-2.537476
  turns`. The physical zero did not change by those amounts; both readings were
  captured after ID6 had been batch-enabled and left in default current mode.
- The old startup waited 300 ms after batch enable and then processed IDs 1-5
  before reading ID6. Since ID6 is unloaded, it could spin during that window.
  The changing readings therefore identify a startup-order defect rather than
  a stable encoder-zero offset.
- The ID6 36:1 reduction and `direction=+1` mapping are provisional because no
  ID6 direction or mechanical-stop sweep has been recorded.
- The `+/-150 deg` bounds are operator-selected software limits, not measured
  mechanical stops.
- A q6 zero target maps to `0 turns` and does not depend on the provisional
  direction sign. Signed
  nonzero ID6 commands require a direction check before being treated as
  calibrated.

## Validation evidence

- `generate_urdf.py`: `PASS`; both generated URDFs contain a revolute ID6 with
  limits `[-2.617993878, 2.617993878] rad`.
- `audit_inertials.py`: `PASS`; total mass remained `4.2676113806 kg` and all
  inertia triangle checks passed.
- CMake build of `gluon_innfos_multi_joint_pose`: `PASS` with the six-joint
  interface.
- Operator execution with the earlier `zero_turns=0` mapping: `FAIL` at the
  initial-state gate. The log reported ID6 `turns=-95.252563`, interpreted
  joint angle `-952.525635 deg`, and step `952.525635 deg`. The controller then
  disabled IDs 1-6 successfully; no motion waypoint was issued.
- Second operator execution with the temporary `zero_turns=-95.252563` mapping:
  `FAIL` at the initial-state gate. ID6 read `-2.537476 turns`, proving the
  earlier `-95.252563` value was not a reusable zero offset. IDs 1-6 were again
  disabled successfully and no motion waypoint was issued.
- Startup-order fix: ID6 is now enabled alone, required to be within 5 motor
  turns of zero, immediately given its measured position as a no-step target,
  and switched to Profile Position before IDs 1-5 are batch-enabled.
- Rebuilt six-joint controller and no-execute dry-run: `PASS`.
- `./scripts/agent-check.sh`: `PASS`; 281 Python syntax checks and 8 URDF XML
  parse checks passed.
- The operator supplied the gated hardware-run evidence above. The agent did
  not execute any hardware runtime or actuator command.
