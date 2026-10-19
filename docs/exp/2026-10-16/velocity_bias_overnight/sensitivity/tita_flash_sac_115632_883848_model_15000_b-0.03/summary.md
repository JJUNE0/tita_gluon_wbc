# tita_flash_sac_115632_883848_model_15000_b-0.03

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_b-0.03",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": -0.03
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
  "final_drift_m": 4.866714932439543,
  "max_drift_m": 4.866714932439543,
  "radial_IAE_m_s": 98.0769378158262,
  "signed_longitudinal_delta_m": -4.855003888608545,
  "tail_speed_mean_m_s": -0.12058880720590656,
  "tail_speed_rms_m_s": 0.12059086539107342,
  "tail_sensor_speed_mean_m_s": -0.12037693857308307,
  "tail_fk_speed_mean_m_s": -0.1203627353347811,
  "peak_tilt_rad": 0.03777288981908433,
  "peak_wheel_torque_nm": 0.11665982007980347,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.03,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 3.731472876970656
}
```
