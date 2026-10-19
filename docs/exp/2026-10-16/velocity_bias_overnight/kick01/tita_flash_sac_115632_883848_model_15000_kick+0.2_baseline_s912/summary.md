# tita_flash_sac_115632_883848_model_15000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "bbcd2cb56e8eba353e5f15cfa2b12619cfcc765a96eddfe2f486275c80131e99",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.374723404954399,
  "max_drift_m": 7.374723404954399,
  "radial_IAE_m_s": 220.85859427542,
  "signed_longitudinal_delta_m": -7.310257088518993,
  "tail_speed_mean_m_s": -0.12217946462580745,
  "tail_speed_rms_m_s": 0.12218987309057416,
  "tail_sensor_speed_mean_m_s": -0.12192489117257878,
  "tail_fk_speed_mean_m_s": -0.12190073558575167,
  "peak_tilt_rad": 0.08881015248372726,
  "peak_wheel_torque_nm": 3.084069013595581,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.278504964022432
}
```
