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
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 0.5,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 5.0
    }
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
  "initial_physics_sha256": "8a46eb8da72f4d8dcedc72e2f3114c61fb96b8817010954a82b7f026409f30c9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01236342512816776,
  "max_drift_m": 0.03296945408054609,
  "radial_IAE_m_s": 0.7819934519027802,
  "signed_longitudinal_delta_m": 0.00994786031129058,
  "tail_speed_mean_m_s": 0.0006013399263055755,
  "tail_speed_rms_m_s": 0.02822812100744091,
  "tail_sensor_speed_mean_m_s": 0.0017170510973600497,
  "tail_fk_speed_mean_m_s": 0.00011494502493203498,
  "peak_tilt_rad": 0.18051348998854277,
  "peak_wheel_torque_nm": 6.778616905212402,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2921881670629305,
  "final_integral_m_s": -0.2921881670629305,
  "elapsed_wall_s": 5.433449658041354
}
```
