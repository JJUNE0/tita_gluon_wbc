# Walk state machine runtime checks

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256:
- `ca003031014536df172a93e161bcb9a795afdf1cc2da29c3cd30a5d5ddc02ad2`; manual keys=True; PASS
- `ca003031014536df172a93e161bcb9a795afdf1cc2da29c3cd30a5d5ddc02ad2`; manual keys=False; PASS
- `0868450122ce8a8e41ae04e42c0b1ff2d0567ffcad3f9c27e35315aef4f18913`; manual keys=True; PASS
- `0868450122ce8a8e41ae04e42c0b1ff2d0567ffcad3f9c27e35315aef4f18913`; manual keys=False; PASS
- `3ec4745778cd8cbcdc4338915ca86ae1f6bc7067f3f583918b42a9c7f9c86aa1`; manual keys=True; PASS
- `3ec4745778cd8cbcdc4338915ca86ae1f6bc7067f3f583918b42a9c7f9c86aa1`; manual keys=False; PASS
- `f71449f130dd4f37b0281324b1e112d2a62bf8a988a91ae8e6b45fe97d244d3b`; manual keys=True; PASS
- `f71449f130dd4f37b0281324b1e112d2a62bf8a988a91ae8e6b45fe97d244d3b`; manual keys=False; PASS

Observed Metrics / Behavior / Log Summary:

8 real ROS/MuJoCo/ONNX runs. Passive GUI creation only was suppressed for manual-key tests.
Checks cover startup state gating, no policy/gait during setup, sit-to-RL, saved wheel gate/zero-command gait, per-substep gate parity, idle/reentry and reset.
Full check results and observed poses: `docs/exp/2026-10-28/hybrid_sim2sim_runtime.json`. Finite physics and state transitions do not establish walking quality.
