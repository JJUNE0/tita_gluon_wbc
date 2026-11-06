# Walk state machine runtime checks

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256:
- `b8f14f1c3bfa7832e2161535f52be595e803d567ae7faac39917de79a990fae7`; manual keys=True; PASS
- `b8f14f1c3bfa7832e2161535f52be595e803d567ae7faac39917de79a990fae7`; manual keys=False; PASS

Observed Metrics / Behavior / Log Summary:

2 real ROS/MuJoCo/ONNX runs. Passive GUI creation only was suppressed for manual-key tests.
Checks cover startup state gating, no policy/gait during setup, sit-to-RL, saved wheel gate/zero-command gait, per-substep gate parity, idle/reentry and reset.
Full check results and observed poses: `docs/exp/2026-10-28/support_episode_sim2sim_runtime.json`. Finite physics and state transitions do not establish walking quality.
