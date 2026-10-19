# tita_flash_sac_115632_883848_model_55000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "35d468ebec28a138bea16aa2dbeb43f98d63bddff3a8a4a03dd4e09557d9f687",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007344872776846884,
  "max_drift_m": 0.13499329108249586,
  "radial_IAE_m_s": 0.5887317388958653,
  "signed_longitudinal_delta_m": -0.007184866792367188,
  "tail_speed_mean_m_s": -4.140359769989121e-05,
  "tail_speed_rms_m_s": 4.1597481971871656e-05,
  "tail_sensor_speed_mean_m_s": -4.093127691131916e-05,
  "tail_fk_speed_mean_m_s": -3.7609329546460255e-05,
  "peak_tilt_rad": 0.11301520060922932,
  "peak_wheel_torque_nm": 2.26029109954834,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.24041019341124667,
  "final_integral_m_s": 0.24041019341124667,
  "elapsed_wall_s": 13.33753300504759
}
```
