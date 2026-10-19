# tita_flash_sac_115632_883848_model_85000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
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
  "initial_physics_sha256": "eeddfc20067f7e4f8ca529af4aa2f4a0264314a63179fea2a630447bec489f4b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.518286748626196,
  "max_drift_m": 7.518286748626196,
  "radial_IAE_m_s": 222.88138708236488,
  "signed_longitudinal_delta_m": 7.513796317370471,
  "tail_speed_mean_m_s": 0.1281037369825546,
  "tail_speed_rms_m_s": 0.12810505253932158,
  "tail_sensor_speed_mean_m_s": 0.12782668417378254,
  "tail_fk_speed_mean_m_s": 0.12782676222271422,
  "peak_tilt_rad": 0.06730979277556504,
  "peak_wheel_torque_nm": 0.07609474658966064,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.332548202946782
}
```
