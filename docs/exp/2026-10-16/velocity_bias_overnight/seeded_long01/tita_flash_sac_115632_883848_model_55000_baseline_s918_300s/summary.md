# tita_flash_sac_115632_883848_model_55000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
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
  "initial_physics_sha256": "ea08b03a912c26111a1e46d653f939a69fe8a85c8579c26164e798cb260dfba4",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 33.41220320376267,
  "max_drift_m": 33.41220320376267,
  "radial_IAE_m_s": 5029.81858625104,
  "signed_longitudinal_delta_m": 31.195967373794222,
  "tail_speed_mean_m_s": 0.11255723015678111,
  "tail_speed_rms_m_s": 0.11255723016102363,
  "tail_sensor_speed_mean_m_s": 0.11231432297961808,
  "tail_fk_speed_mean_m_s": 0.11231569858074919,
  "peak_tilt_rad": 0.09092399458439027,
  "peak_wheel_torque_nm": 0.34922999143600464,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 44.973644723009784
}
```
