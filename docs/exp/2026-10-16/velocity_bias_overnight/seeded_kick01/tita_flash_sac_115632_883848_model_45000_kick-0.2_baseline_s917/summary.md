# tita_flash_sac_115632_883848_model_45000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "6ff96664336f59668c00b70abad85e3fbb9dd5e7f4e96d753c8af88984596612",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.385156704100815,
  "max_drift_m": 2.385156704100815,
  "radial_IAE_m_s": 67.96839034123992,
  "signed_longitudinal_delta_m": 2.313224205774123,
  "tail_speed_mean_m_s": 0.04234231198041589,
  "tail_speed_rms_m_s": 0.0429489846797977,
  "tail_sensor_speed_mean_m_s": 0.04106912601820241,
  "tail_fk_speed_mean_m_s": 0.042244894128358766,
  "peak_tilt_rad": 0.05225784126584343,
  "peak_wheel_torque_nm": 2.7509965896606445,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.28285381902242
}
```
