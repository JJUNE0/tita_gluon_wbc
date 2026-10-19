# TITA sim2sim

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256: 9c22f34e0e3b9d7840f29250c214452bb84cadde6037d277d90df55221e84150

ONNX SHA256: 128734f230868b947c9eac59ef647b8394043c6603781a335fd4e3b4700a2001

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "checkpoint": "/home/cocel/Desktop/Research/tita_gluon_wbc/lab/ddt_lab/logs/flash_sac/tita_flash_sac_180212_290240/model_75000/actor.pt",
  "checkpoint_sha256": "9c22f34e0e3b9d7840f29250c214452bb84cadde6037d277d90df55221e84150",
  "onnx_sha256": "128734f230868b947c9eac59ef647b8394043c6603781a335fd4e3b4700a2001",
  "policy_steps": 1000,
  "headless": true,
  "residual_wheel_pd": false,
  "fixed_residual_lqr": false,
  "velocity_bias": false,
  "leg_action_filter": "ma2_legs",
  "leg_notch_hz": 8.3,
  "leg_notch_q": 3.0,
  "detail": "Finite MuJoCo playback completed; this is not a locomotion quality evaluation.",
  "final_base_position_m": [
    0.08269047737121582,
    0.03934532031416893,
    0.35220861434936523
  ],
  "viewer_threads_stopped": true
}
```
