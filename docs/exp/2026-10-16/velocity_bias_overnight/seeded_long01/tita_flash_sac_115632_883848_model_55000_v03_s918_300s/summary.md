# tita_flash_sac_115632_883848_model_55000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "ea08b03a912c26111a1e46d653f939a69fe8a85c8579c26164e798cb260dfba4",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.016943221783354882,
  "max_drift_m": 0.0457121130549272,
  "radial_IAE_m_s": 3.7127978335553653,
  "signed_longitudinal_delta_m": -0.016407956430936992,
  "tail_speed_mean_m_s": -1.1175697138049168e-05,
  "tail_speed_rms_m_s": 1.1201504766448647e-05,
  "tail_sensor_speed_mean_m_s": -1.146485636102633e-05,
  "tail_fk_speed_mean_m_s": -8.95755472571858e-06,
  "peak_tilt_rad": 0.08949493767047323,
  "peak_wheel_torque_nm": 0.9421302080154419,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.20875425057894595,
  "final_integral_m_s": 0.20875425057894595,
  "elapsed_wall_s": 44.56405123701552
}
```
