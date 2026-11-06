# Walk state machine runtime checks

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256:
- `cb631c7e55b25113f99560dbc35067630afef68a1e2235827d95bfc98ca6af21`; manual keys=True; PASS
- `cb631c7e55b25113f99560dbc35067630afef68a1e2235827d95bfc98ca6af21`; manual keys=False; PASS

Observed Metrics / Behavior / Log Summary:

2 real ROS/MuJoCo/ONNX runs. Passive GUI creation only was suppressed for manual-key tests.
Checks cover startup state gating, no policy/gait during setup, sit-to-RL, saved wheel gate/zero-command gait, per-substep gate parity, idle/reentry and reset.
Full check results and observed poses: `docs/exp/2026-10-28/support_velocity_sim2sim_runtime.json`. Finite physics and state transitions do not establish walking quality.
