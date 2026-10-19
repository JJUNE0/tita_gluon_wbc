# tita_flash_sac_115632_883848_model_55000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "56bc084e0dfbcba80b51a4b8434e405f6ab5c280d2672d7c96a893ad0735c0b9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.847866547091271,
  "max_drift_m": 6.847866547091271,
  "radial_IAE_m_s": 208.18959943529873,
  "signed_longitudinal_delta_m": 6.774939925738443,
  "tail_speed_mean_m_s": 0.1130500304254009,
  "tail_speed_rms_m_s": 0.11305004719032964,
  "tail_sensor_speed_mean_m_s": 0.11280606653097285,
  "tail_fk_speed_mean_m_s": 0.11280755211729677,
  "peak_tilt_rad": 0.11500490107582073,
  "peak_wheel_torque_nm": 1.8283113241195679,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.024868797976524
}
```
