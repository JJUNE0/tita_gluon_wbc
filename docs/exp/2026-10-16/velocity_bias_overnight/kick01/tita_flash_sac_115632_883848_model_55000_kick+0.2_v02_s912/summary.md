# tita_flash_sac_115632_883848_model_55000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "56bc084e0dfbcba80b51a4b8434e405f6ab5c280d2672d7c96a893ad0735c0b9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.023579011598753277,
  "max_drift_m": 0.12385451232250679,
  "radial_IAE_m_s": 1.5385822645318439,
  "signed_longitudinal_delta_m": 0.02357530024759347,
  "tail_speed_mean_m_s": -1.8978179369655248e-05,
  "tail_speed_rms_m_s": 1.9020279837791415e-05,
  "tail_sensor_speed_mean_m_s": -1.8767451989585877e-05,
  "tail_fk_speed_mean_m_s": -1.5449521381761113e-05,
  "peak_tilt_rad": 0.11292881689464207,
  "peak_wheel_torque_nm": 2.327134370803833,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.24346903535315503,
  "final_integral_m_s": 0.24349959889316122,
  "elapsed_wall_s": 17.796590248995926
}
```
