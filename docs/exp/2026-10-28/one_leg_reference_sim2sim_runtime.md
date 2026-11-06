# Walk state machine runtime checks

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256:
- `9e581ebc10b423575f35b9d71323bf76b77e35e0ceb051edd38ab59093ac6a59`; manual keys=True; PASS
- `9e581ebc10b423575f35b9d71323bf76b77e35e0ceb051edd38ab59093ac6a59`; manual keys=False; PASS

Observed Metrics / Behavior / Log Summary:

2 real ROS/MuJoCo/ONNX runs. Passive GUI creation only was suppressed for manual-key tests.
Checks cover startup state gating, no policy/gait during setup, sit-to-RL, saved wheel gate/zero-command gait, per-substep gate parity, idle/reentry and reset.
Full check results and observed poses: `docs/exp/2026-10-28/one_leg_reference_sim2sim_runtime.json`. Finite physics and state transitions do not establish walking quality.
