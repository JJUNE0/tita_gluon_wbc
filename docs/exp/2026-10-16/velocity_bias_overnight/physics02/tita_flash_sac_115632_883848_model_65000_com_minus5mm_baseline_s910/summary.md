# tita_flash_sac_115632_883848_model_65000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "ac5a7a7ba4ba02dab5c81e786ed334a70e7f97254aac23a9d2d26d114ed06eb8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.5703024816791433,
  "max_drift_m": 0.5703024816791433,
  "radial_IAE_m_s": 17.96037198121017,
  "signed_longitudinal_delta_m": 0.5688246436482475,
  "tail_speed_mean_m_s": 0.008385875646628418,
  "tail_speed_rms_m_s": 0.008392804979429342,
  "tail_sensor_speed_mean_m_s": 0.00836776438582991,
  "tail_fk_speed_mean_m_s": 0.008367008076152274,
  "peak_tilt_rad": 0.055781937160144235,
  "peak_wheel_torque_nm": 0.24583232402801514,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.79127172299195
}
```
