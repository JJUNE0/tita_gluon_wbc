# tita_flash_sac_115632_883848_model_80000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
  "state_columns": [
    "base_x",
    "base_y",
    "base_z",
    "base_forward_speed",
    "roll",
    "pitch",
    "yaw",
    "raw_position",
    "raw_speed",
    "fk_position",
    "fk_speed"
  ],
  "initial_physics_sha256": "851e9a7583b6d335133037b904223c443f15e2e39c5dfffc05284cfa4de3a742",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.38534345811076,
  "max_drift_m": 10.38534345811076,
  "radial_IAE_m_s": 306.7089977171539,
  "signed_longitudinal_delta_m": 10.347910414038726,
  "tail_speed_mean_m_s": 0.17705424891277574,
  "tail_speed_rms_m_s": 0.1770546142378149,
  "tail_sensor_speed_mean_m_s": 0.17667203212856364,
  "tail_fk_speed_mean_m_s": 0.17667096389454973,
  "peak_tilt_rad": 0.08676879095471768,
  "peak_wheel_torque_nm": 0.4444679021835327,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 16.20021697698394
}
```
