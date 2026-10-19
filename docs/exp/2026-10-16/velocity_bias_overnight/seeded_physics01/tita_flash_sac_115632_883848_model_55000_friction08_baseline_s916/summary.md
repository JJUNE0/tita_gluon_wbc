# tita_flash_sac_115632_883848_model_55000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "f4b3925d312ba444dda28b40c9dcda93770cba4188af2e2eecb3a3b8707c6130",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.640207413678104,
  "max_drift_m": 6.640207413678104,
  "radial_IAE_m_s": 196.82823342571038,
  "signed_longitudinal_delta_m": 6.178110609997437,
  "tail_speed_mean_m_s": 0.11301862309284041,
  "tail_speed_rms_m_s": 0.11301863363267796,
  "tail_sensor_speed_mean_m_s": 0.11277664860985541,
  "tail_fk_speed_mean_m_s": 0.11277806786357572,
  "peak_tilt_rad": 0.09068523876407641,
  "peak_wheel_torque_nm": 0.306962251663208,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.925062960013747
}
```
