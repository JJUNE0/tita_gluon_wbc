# tita_flash_sac_115632_883848_model_15000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
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
  "initial_physics_sha256": "80c210c3cdf0187476f4a079d64fbe55a4038e6b7f956f4dde4fe411896f29e9",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 28.823671206963958,
  "max_drift_m": 28.823671206963958,
  "radial_IAE_m_s": 4757.968379278246,
  "signed_longitudinal_delta_m": -27.296857594213005,
  "tail_speed_mean_m_s": -0.08080477703878179,
  "tail_speed_rms_m_s": 0.08080533661389139,
  "tail_sensor_speed_mean_m_s": -0.0806187456937348,
  "tail_fk_speed_mean_m_s": -0.080662984731403,
  "peak_tilt_rad": 0.05864478820567731,
  "peak_wheel_torque_nm": 1.8887248039245605,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 59.533239643031266
}
```
