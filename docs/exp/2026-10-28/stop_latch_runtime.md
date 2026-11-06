# Walk state machine runtime checks

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256:
- `d13828eefe0b92440551642ff0c1cf464aadf38c2b4f322186672599daaa87fa`; manual keys=True; PASS
- `d13828eefe0b92440551642ff0c1cf464aadf38c2b4f322186672599daaa87fa`; manual keys=False; PASS
- `6d0a0604907cf9c48ec6588847f5aae3ea73e450d058cc52bb695e087873408d`; manual keys=True; PASS
- `6d0a0604907cf9c48ec6588847f5aae3ea73e450d058cc52bb695e087873408d`; manual keys=False; PASS

Observed Metrics / Behavior / Log Summary:

4 real ROS/MuJoCo/ONNX runs. Passive GUI creation only was suppressed for manual-key tests.
Checks cover startup state gating, no policy/gait during setup, sit-to-RL, saved wheel gate/zero-command gait, per-substep gate parity, idle/reentry and reset.
Full check results and observed poses: `docs/exp/2026-10-28/stop_latch_runtime.json`. Finite physics and state transitions do not establish walking quality.
