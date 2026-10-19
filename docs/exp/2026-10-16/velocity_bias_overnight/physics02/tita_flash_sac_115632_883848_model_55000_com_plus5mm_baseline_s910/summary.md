# tita_flash_sac_115632_883848_model_55000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "00e82e9ffeb146ceec9c3be4e4f50b7e4f30979acb1f03da40f0f36f42531e74",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.778067770945605,
  "max_drift_m": 7.778067770945605,
  "radial_IAE_m_s": 231.50728491740915,
  "signed_longitudinal_delta_m": 7.659555893997602,
  "tail_speed_mean_m_s": 0.13142194099561658,
  "tail_speed_rms_m_s": 0.13142198023070592,
  "tail_sensor_speed_mean_m_s": 0.13113826809962278,
  "tail_fk_speed_mean_m_s": 0.1311393276648375,
  "peak_tilt_rad": 0.0926051545379718,
  "peak_wheel_torque_nm": 0.3233928084373474,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.025476971000899
}
```
