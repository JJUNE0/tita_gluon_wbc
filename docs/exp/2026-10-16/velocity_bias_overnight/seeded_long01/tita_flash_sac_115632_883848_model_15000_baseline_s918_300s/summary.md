# tita_flash_sac_115632_883848_model_15000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "7a5112a26c976ba7896195ac5c36c977a0ee0588199db23aa46fe33a8c870fe2",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 29.546336325675995,
  "max_drift_m": 29.546336325675995,
  "radial_IAE_m_s": 4869.670476985197,
  "signed_longitudinal_delta_m": -27.58698642814438,
  "tail_speed_mean_m_s": -0.08153826988836946,
  "tail_speed_rms_m_s": 0.08153884316915681,
  "tail_sensor_speed_mean_m_s": -0.08135435408878917,
  "tail_fk_speed_mean_m_s": -0.08139646936416954,
  "peak_tilt_rad": 0.05868303611742398,
  "peak_wheel_torque_nm": 1.9245799779891968,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 54.52316256001359
}
```
