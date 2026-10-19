# tita_flash_sac_115632_883848_model_15000_b+0.10

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_b+0.10",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": 0.1
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
  "initial_physics_sha256": "cae9e9e146e56e646f979876a83a23d6b8d2c90d1b1302d1d4f9080b7977b2da",
  "complete": true,
  "failure": [],
  "duration_s": 40.0,
  "final_drift_m": 5.513268622036294,
  "max_drift_m": 5.513268622036294,
  "radial_IAE_m_s": 110.99140354858125,
  "signed_longitudinal_delta_m": -5.471372684678262,
  "tail_speed_mean_m_s": -0.1373774077841449,
  "tail_speed_rms_m_s": 0.13738027360998062,
  "tail_sensor_speed_mean_m_s": -0.1370895847997432,
  "tail_fk_speed_mean_m_s": -0.13705894804321833,
  "peak_tilt_rad": 0.03125032275910011,
  "peak_wheel_torque_nm": 0.11264824867248535,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 3.6520609419676475
}
```
