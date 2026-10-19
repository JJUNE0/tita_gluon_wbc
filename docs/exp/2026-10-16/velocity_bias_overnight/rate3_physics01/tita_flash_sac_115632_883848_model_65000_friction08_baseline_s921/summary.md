# tita_flash_sac_115632_883848_model_65000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "0846c3e63fa0f48d282439e06597cea1fcc0f94522db844d45f0b570f7320ddf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.0304499783086465,
  "max_drift_m": 2.0304499783086465,
  "radial_IAE_m_s": 61.77074104008087,
  "signed_longitudinal_delta_m": 2.0105970875563286,
  "tail_speed_mean_m_s": 0.03274171390342649,
  "tail_speed_rms_m_s": 0.03274378301724701,
  "tail_sensor_speed_mean_m_s": 0.032670902743973135,
  "tail_fk_speed_mean_m_s": 0.032669821583688446,
  "peak_tilt_rad": 0.05966256302624373,
  "peak_wheel_torque_nm": 0.2286326140165329,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.302681903995108
}
```
