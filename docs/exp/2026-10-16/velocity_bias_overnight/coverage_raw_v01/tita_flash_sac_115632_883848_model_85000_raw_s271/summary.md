# tita_flash_sac_115632_883848_model_85000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
  },
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "83be9d61635e01648456f1806990434e3c5e6850f7c6b7cb8a3afc587378487e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05728614881778704,
  "max_drift_m": 0.06796133121111249,
  "radial_IAE_m_s": 3.432826555993044,
  "signed_longitudinal_delta_m": 0.057279536421534036,
  "tail_speed_mean_m_s": 4.465009403943134e-06,
  "tail_speed_rms_m_s": 4.59549517037783e-06,
  "tail_sensor_speed_mean_m_s": 4.51636059455344e-06,
  "tail_fk_speed_mean_m_s": 4.861417170236363e-06,
  "peak_tilt_rad": 0.0672611346768146,
  "peak_wheel_torque_nm": 0.53460294008255,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.583296356311457,
  "final_integral_m_s": 0.5832837920684457,
  "elapsed_wall_s": 4.281837162969168
}
```
