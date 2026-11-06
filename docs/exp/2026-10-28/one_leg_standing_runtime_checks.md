# Walk state machine runtime checks

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256:
- `f56a3a7c4bf80569eefdc453fe41439dc8d4c6cec557a0dbdd535d640dcbec1b`; manual keys=True; PASS
- `f56a3a7c4bf80569eefdc453fe41439dc8d4c6cec557a0dbdd535d640dcbec1b`; manual keys=False; PASS

Observed Metrics / Behavior / Log Summary:

2 real ROS/MuJoCo/ONNX runs. Passive GUI creation only was suppressed for manual-key tests.
Checks cover startup state gating, no policy/gait during setup, sit-to-RL, saved wheel gate/zero-command gait, per-substep gate parity, idle/reentry and reset.
Full check results and observed poses: `docs/exp/2026-10-28/one_leg_standing_runtime_checks.json`. Finite physics and state transitions do not establish walking quality.
