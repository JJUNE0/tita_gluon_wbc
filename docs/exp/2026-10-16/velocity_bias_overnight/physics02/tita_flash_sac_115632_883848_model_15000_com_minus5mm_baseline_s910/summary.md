# tita_flash_sac_115632_883848_model_15000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
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
  "checkpoint_sha256": "966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003",
  "onnx_sha256": "1fec00b7bc7eebbc5b6decf23ac6f29b8799c5cf64ff1dee51c1ba762cf013ed",
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
  "initial_physics_sha256": "16866ed5ba61977377968b6f192d069d4c4b5c05fb212a88d39648f716b5b725",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.265415825182776,
  "max_drift_m": 8.265415825182776,
  "radial_IAE_m_s": 250.99207187864545,
  "signed_longitudinal_delta_m": -8.169118151986556,
  "tail_speed_mean_m_s": -0.1355527984236804,
  "tail_speed_rms_m_s": 0.13556623846337226,
  "tail_sensor_speed_mean_m_s": -0.13526644098064308,
  "tail_fk_speed_mean_m_s": -0.135234856797982,
  "peak_tilt_rad": 0.051817684693436616,
  "peak_wheel_torque_nm": 1.8065592050552368,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.293141402013134
}
```
