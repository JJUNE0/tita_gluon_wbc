# Walk state machine runtime checks

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256:
- `856a9da1352da53cb3f97ae5268017ddfad6662a47570e4d971b9b84251331d9`; manual keys=True; PASS
- `856a9da1352da53cb3f97ae5268017ddfad6662a47570e4d971b9b84251331d9`; manual keys=False; PASS

Observed Metrics / Behavior / Log Summary:

2 real ROS/MuJoCo/ONNX runs. Passive GUI creation only was suppressed for manual-key tests.
Checks cover startup state gating, no policy/gait during setup, sit-to-RL, saved wheel gate/zero-command gait, per-substep gate parity, idle/reentry and reset.
Full check results and observed poses: `docs/exp/2026-10-28/support_velocity_sim2sim_probe.json`. Finite physics and state transitions do not establish walking quality.
