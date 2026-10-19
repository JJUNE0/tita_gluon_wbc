# tita_flash_sac_115632_883848_model_15000_nominal_fk

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_nominal_fk",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "04f5051eb8c1358de8af79edba19981b106a50c09ed3818724903d8ad4e0e126",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.035060159438585314,
  "max_drift_m": 0.05529167158343269,
  "radial_IAE_m_s": 2.1310056603958927,
  "signed_longitudinal_delta_m": -0.03500759843883738,
  "tail_speed_mean_m_s": 9.447104370372897e-06,
  "tail_speed_rms_m_s": 1.0298973728446295e-05,
  "tail_sensor_speed_mean_m_s": 9.706840840063924e-06,
  "tail_fk_speed_mean_m_s": 1.0315831135258663e-05,
  "peak_tilt_rad": 0.13720104370366415,
  "peak_wheel_torque_nm": 0.9593527317047119,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.36678868041492,
  "final_integral_m_s": -0.3668038806341245,
  "elapsed_wall_s": 15.735854406957515
}
```
