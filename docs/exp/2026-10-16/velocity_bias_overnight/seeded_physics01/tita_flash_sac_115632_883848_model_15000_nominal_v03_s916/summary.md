# tita_flash_sac_115632_883848_model_15000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "initial_physics_sha256": "194ceab6555a3204f7194bd5304c56ad93e7b49be7f7c0559e3131404d1f437d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.030311333690984255,
  "max_drift_m": 0.052409703600221035,
  "radial_IAE_m_s": 1.907112413624933,
  "signed_longitudinal_delta_m": -0.03025472092053864,
  "tail_speed_mean_m_s": 4.158113539546212e-05,
  "tail_speed_rms_m_s": 4.1590171582159396e-05,
  "tail_sensor_speed_mean_m_s": 4.1701447724682394e-05,
  "tail_fk_speed_mean_m_s": 4.2395975357852484e-05,
  "peak_tilt_rad": 0.12343977171873943,
  "peak_wheel_torque_nm": 2.5723841190338135,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.36848334055247417,
  "final_integral_m_s": -0.36848334055247417,
  "elapsed_wall_s": 9.480205178027973
}
```
