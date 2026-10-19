# tita_flash_sac_115632_883848_model_15000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
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
  "initial_physics_sha256": "7a5112a26c976ba7896195ac5c36c977a0ee0588199db23aa46fe33a8c870fe2",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.02719892906124007,
  "max_drift_m": 0.05240966646395749,
  "radial_IAE_m_s": 8.764341886340365,
  "signed_longitudinal_delta_m": -0.027094731528956213,
  "tail_speed_mean_m_s": 8.327658502924986e-06,
  "tail_speed_rms_m_s": 8.337403082090687e-06,
  "tail_sensor_speed_mean_m_s": 8.48245232611283e-06,
  "tail_fk_speed_mean_m_s": 8.722704916206323e-06,
  "peak_tilt_rad": 0.12343982579471602,
  "peak_wheel_torque_nm": 2.572371482849121,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.35509978414958293,
  "final_integral_m_s": -0.35509978414958293,
  "elapsed_wall_s": 52.59389541699784
}
```
