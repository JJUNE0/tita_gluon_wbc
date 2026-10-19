# tita_flash_sac_115632_883848_model_65000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "c288cfa94fac43aa806d4ddf35da612a7f7c18224cc799a4cb032ae4db54e2f5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.5530436026817642,
  "max_drift_m": 3.5530436026817642,
  "radial_IAE_m_s": 107.64756809549903,
  "signed_longitudinal_delta_m": 3.5356288089665027,
  "tail_speed_mean_m_s": 0.05815891717127495,
  "tail_speed_rms_m_s": 0.05815940169689769,
  "tail_sensor_speed_mean_m_s": 0.05803280330530515,
  "tail_fk_speed_mean_m_s": 0.05803079690359324,
  "peak_tilt_rad": 0.06262865050113109,
  "peak_wheel_torque_nm": 0.2683592438697815,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.086711087962613
}
```
