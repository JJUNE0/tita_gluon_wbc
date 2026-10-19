# tita_flash_sac_115632_883848_model_15000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "76b09a94e2e7f4c756c4fa9f802108b5b9dae82f48975ecd8f804f88a12676e6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.554883587378399,
  "max_drift_m": 7.554883587378399,
  "radial_IAE_m_s": 231.05858338667232,
  "signed_longitudinal_delta_m": -7.489844374358305,
  "tail_speed_mean_m_s": -0.12252039373498817,
  "tail_speed_rms_m_s": 0.12252987793026149,
  "tail_sensor_speed_mean_m_s": -0.12226750281917416,
  "tail_fk_speed_mean_m_s": -0.1222437908653664,
  "peak_tilt_rad": 0.054664319724954336,
  "peak_wheel_torque_nm": 3.7951819896698,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.205106833949685
}
```
