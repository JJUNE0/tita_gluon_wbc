# Walk state machine runtime checks

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256:
- `436ff2b3c2752a67e618c53a7c83c9b8e2415aee3437ea5ccb525999c674daf7`; manual keys=True; PASS
- `436ff2b3c2752a67e618c53a7c83c9b8e2415aee3437ea5ccb525999c674daf7`; manual keys=False; PASS

Observed Metrics / Behavior / Log Summary:

2 real ROS/MuJoCo/ONNX runs. Passive GUI creation only was suppressed for manual-key tests.
Checks cover startup state gating, no policy/gait during setup, sit-to-RL, saved wheel gate/zero-command gait, per-substep gate parity, idle/reentry and reset.
Full check results and observed poses: `docs/exp/2026-10-28/support_command_sim2sim_25000_runtime.json`. Finite physics and state transitions do not establish walking quality.
