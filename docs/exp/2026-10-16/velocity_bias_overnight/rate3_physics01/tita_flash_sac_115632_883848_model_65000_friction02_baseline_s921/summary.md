# tita_flash_sac_115632_883848_model_65000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "5620ca94a97c3a5646b49533b5f187b647d181bb08bd25443bb5a3b254c65c59",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.1575149675401815,
  "max_drift_m": 1.1575149675401815,
  "radial_IAE_m_s": 37.29160119876249,
  "signed_longitudinal_delta_m": 0.7831499861969042,
  "tail_speed_mean_m_s": 0.021015049561821732,
  "tail_speed_rms_m_s": 0.021020921469598036,
  "tail_sensor_speed_mean_m_s": 0.02065060529237561,
  "tail_fk_speed_mean_m_s": 0.020625770285100306,
  "peak_tilt_rad": 0.054750393366225225,
  "peak_wheel_torque_nm": 0.17191684246063232,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.243952053016983
}
```
