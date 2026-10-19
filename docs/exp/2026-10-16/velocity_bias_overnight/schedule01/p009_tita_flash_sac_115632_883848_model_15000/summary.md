# p009_tita_flash_sac_115632_883848_model_15000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p009_tita_flash_sac_115632_883848_model_15000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "gain_velocity": 0.2,
      "gain_floor": 0.05
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
  "initial_physics_sha256": "8a46eb8da72f4d8dcedc72e2f3114c61fb96b8817010954a82b7f026409f30c9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.12765847960471188,
  "max_drift_m": 0.1663717064064271,
  "radial_IAE_m_s": 8.655752670356007,
  "signed_longitudinal_delta_m": -0.1275062006188398,
  "tail_speed_mean_m_s": 0.0009406439517757074,
  "tail_speed_rms_m_s": 0.02839377059056433,
  "tail_sensor_speed_mean_m_s": -0.00020174069255097924,
  "tail_fk_speed_mean_m_s": 0.00034776846445979276,
  "peak_tilt_rad": 0.17942837197035244,
  "peak_wheel_torque_nm": 7.0541863441467285,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.29169805442329777,
  "final_integral_m_s": -0.29139189377934427,
  "elapsed_wall_s": 13.375333215983119
}
```
