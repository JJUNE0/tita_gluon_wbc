# tita_flash_sac_115632_883848_model_80000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "8d160aa7395d03deeec143ce54d389a51b57d38fc4d3e68ab5b14fe3d9ea5c81",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 59.72202740387189,
  "max_drift_m": 59.72202740387189,
  "radial_IAE_m_s": 8919.165904877866,
  "signed_longitudinal_delta_m": 59.72181935651033,
  "tail_speed_mean_m_s": 0.20064195423945974,
  "tail_speed_rms_m_s": 0.20064195426163253,
  "tail_sensor_speed_mean_m_s": 0.20020840930516487,
  "tail_fk_speed_mean_m_s": 0.20020766430375214,
  "peak_tilt_rad": 0.08728460672411154,
  "peak_wheel_torque_nm": 0.4761526584625244,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 49.808401714020874
}
```
