# tita_flash_sac_115632_883848_model_85000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_s271",
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
    "estimator": "fk"
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
  "final_drift_m": 0.05677985020008843,
  "max_drift_m": 0.06998323552944648,
  "radial_IAE_m_s": 3.4060909110585857,
  "signed_longitudinal_delta_m": 0.056773130518575535,
  "tail_speed_mean_m_s": 4.12684515861817e-06,
  "tail_speed_rms_m_s": 4.267368494535237e-06,
  "tail_sensor_speed_mean_m_s": 4.1796365853010014e-06,
  "tail_fk_speed_mean_m_s": 4.524302110159086e-06,
  "peak_tilt_rad": 0.0672611346768146,
  "peak_wheel_torque_nm": 0.5334663987159729,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5833001442943866,
  "final_integral_m_s": 0.5832873895404677,
  "elapsed_wall_s": 4.342567527026404
}
```
