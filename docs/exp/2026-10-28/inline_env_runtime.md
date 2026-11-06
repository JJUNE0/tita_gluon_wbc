# Walk state machine runtime checks

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256:
- `dd87ed7dd304028825b45e191277903d29fe7e3267854ed0bbb6e1b2a045263f`; manual keys=True; PASS
- `dd87ed7dd304028825b45e191277903d29fe7e3267854ed0bbb6e1b2a045263f`; manual keys=False; PASS
- `d13828eefe0b92440551642ff0c1cf464aadf38c2b4f322186672599daaa87fa`; manual keys=True; PASS
- `d13828eefe0b92440551642ff0c1cf464aadf38c2b4f322186672599daaa87fa`; manual keys=False; PASS

Observed Metrics / Behavior / Log Summary:

4 real ROS/MuJoCo/ONNX runs. Passive GUI creation only was suppressed for manual-key tests.
Checks cover startup state gating, no policy/gait during setup, sit-to-RL, saved wheel gate/zero-command gait, per-substep gate parity, idle/reentry and reset.
Full check results and observed poses: `docs/exp/2026-10-28/inline_env_runtime.json`. Finite physics and state transitions do not establish walking quality.
