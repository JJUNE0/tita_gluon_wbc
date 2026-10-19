# p007_tita_flash_sac_115632_883848_model_15000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p007_tita_flash_sac_115632_883848_model_15000",
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
      "gain_velocity": 0.1,
      "gain_floor": 0.1
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
  "final_drift_m": 0.02805317979409274,
  "max_drift_m": 0.07987691097522671,
  "radial_IAE_m_s": 3.356045152691396,
  "signed_longitudinal_delta_m": -0.026922523726966924,
  "tail_speed_mean_m_s": 0.0009164996653244089,
  "tail_speed_rms_m_s": 0.028653014203281296,
  "tail_sensor_speed_mean_m_s": -2.8149499863176503e-05,
  "tail_fk_speed_mean_m_s": 0.000395902348449462,
  "peak_tilt_rad": 0.1794977487164784,
  "peak_wheel_torque_nm": 7.397223949432373,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.29059470994386905,
  "final_integral_m_s": -0.2886242089437456,
  "elapsed_wall_s": 12.14643960999092
}
```
