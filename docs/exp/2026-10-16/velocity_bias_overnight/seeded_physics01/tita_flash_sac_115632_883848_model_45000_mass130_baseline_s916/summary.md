# tita_flash_sac_115632_883848_model_45000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
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
  "initial_physics_sha256": "faa3eff743868275db059e4ae532b312ac8d884881a7f77f66b391b3f9549b8e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.087288602548172,
  "max_drift_m": 12.087288602548172,
  "radial_IAE_m_s": 361.1382063574822,
  "signed_longitudinal_delta_m": -11.948024743712836,
  "tail_speed_mean_m_s": -0.2048916394233128,
  "tail_speed_rms_m_s": 0.2048937443173852,
  "tail_sensor_speed_mean_m_s": -0.20450174716217526,
  "tail_fk_speed_mean_m_s": -0.2044973332914104,
  "peak_tilt_rad": 0.02953504988672781,
  "peak_wheel_torque_nm": 0.6482030153274536,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.830265026015695
}
```
