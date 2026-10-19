# tita_flash_sac_115632_883848_model_15000_seeded_v03_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_seeded_v03_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "guarded": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003",
  "onnx_sha256": "1fec00b7bc7eebbc5b6decf23ac6f29b8799c5cf64ff1dee51c1ba762cf013ed",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "b20e655d3ce3d0ab9ef33859f3f7c1d62baef55a10e995f3b6eed5ae8c707f2e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02984716764349607,
  "max_drift_m": 0.052198809673029305,
  "radial_IAE_m_s": 1.8601980683437958,
  "signed_longitudinal_delta_m": -0.029791178287461872,
  "tail_speed_mean_m_s": 2.405513517854223e-05,
  "tail_speed_rms_m_s": 2.6043160410216293e-05,
  "tail_sensor_speed_mean_m_s": 2.4289669606708732e-05,
  "tail_fk_speed_mean_m_s": 2.4889393679129347e-05,
  "peak_tilt_rad": 0.1234558158478829,
  "peak_wheel_torque_nm": 2.5056614875793457,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3667528586576414,
  "final_integral_m_s": -0.3667528586576414,
  "elapsed_wall_s": 5.117208612966351
}
```
