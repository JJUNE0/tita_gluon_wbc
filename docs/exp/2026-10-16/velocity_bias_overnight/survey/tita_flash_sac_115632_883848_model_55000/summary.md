# tita_flash_sac_115632_883848_model_55000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "6fd8b3c8fe0c8e1b25a8438c6fbc679007a24db85ff7c61acd7d74cbd95fe224",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.746733922098625,
  "max_drift_m": 6.746733922098625,
  "radial_IAE_m_s": 201.84907474218286,
  "signed_longitudinal_delta_m": 6.706822076113495,
  "tail_speed_mean_m_s": 0.11299235036599928,
  "tail_speed_rms_m_s": 0.11299236615173083,
  "tail_sensor_speed_mean_m_s": 0.11274846054639187,
  "tail_fk_speed_mean_m_s": 0.11274995137151038,
  "peak_tilt_rad": 0.09079383102431149,
  "peak_wheel_torque_nm": 0.3085598349571228,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.507830088958144
}
```
