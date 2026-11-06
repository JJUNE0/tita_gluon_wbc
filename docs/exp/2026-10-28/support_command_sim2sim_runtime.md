# Walk state machine runtime checks

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256:
- `6fc80e153d04a048021d2b3a2cc4c0c18b96b7e1ef8233d191f6ca59f677f630`; manual keys=True; PASS
- `6fc80e153d04a048021d2b3a2cc4c0c18b96b7e1ef8233d191f6ca59f677f630`; manual keys=False; PASS

Observed Metrics / Behavior / Log Summary:

2 real ROS/MuJoCo/ONNX runs. Passive GUI creation only was suppressed for manual-key tests.
Checks cover startup state gating, no policy/gait during setup, sit-to-RL, saved wheel gate/zero-command gait, per-substep gate parity, idle/reentry and reset.
Full check results and observed poses: `docs/exp/2026-10-28/support_command_sim2sim_runtime.json`. Finite physics and state transitions do not establish walking quality.
