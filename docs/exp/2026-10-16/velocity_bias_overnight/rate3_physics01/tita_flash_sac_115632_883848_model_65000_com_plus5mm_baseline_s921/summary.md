# tita_flash_sac_115632_883848_model_65000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "9414b5263419b86e5a154a9637b57bea4ff0a0eaffdefb6512a14ea8984b6e45",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.598132028695999,
  "max_drift_m": 3.598132028695999,
  "radial_IAE_m_s": 109.26556067722919,
  "signed_longitudinal_delta_m": 3.575638765300737,
  "tail_speed_mean_m_s": 0.05857066647496465,
  "tail_speed_rms_m_s": 0.05857140063151485,
  "tail_sensor_speed_mean_m_s": 0.058443659133046076,
  "tail_fk_speed_mean_m_s": 0.05844183736752894,
  "peak_tilt_rad": 0.06281980581138868,
  "peak_wheel_torque_nm": 0.2683103680610657,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.018176702957135
}
```
