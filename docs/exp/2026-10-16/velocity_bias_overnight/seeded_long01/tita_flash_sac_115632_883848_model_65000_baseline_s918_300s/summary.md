# tita_flash_sac_115632_883848_model_65000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
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
  "initial_physics_sha256": "18c6fb9b6527aa982fc729c148e114aae7972c43c9af71170b696d589e3fbf78",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 8.507228423661584,
  "max_drift_m": 8.507228423661584,
  "radial_IAE_m_s": 1348.799621261864,
  "signed_longitudinal_delta_m": 7.822165337403942,
  "tail_speed_mean_m_s": 0.02708938518823783,
  "tail_speed_rms_m_s": 0.027089442473067757,
  "tail_sensor_speed_mean_m_s": 0.027030516438434148,
  "tail_fk_speed_mean_m_s": 0.027028448510796117,
  "peak_tilt_rad": 0.05962681225858191,
  "peak_wheel_torque_nm": 0.2507609724998474,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 53.408497694996186
}
```
