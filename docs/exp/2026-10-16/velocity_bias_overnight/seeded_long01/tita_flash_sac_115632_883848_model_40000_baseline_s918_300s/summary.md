# tita_flash_sac_115632_883848_model_40000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
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
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "7aec6b1b690a57bd4b5bde62c7bf29b0a80c7dade549dd36853e4d25b9e5493f",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 34.87429543059638,
  "max_drift_m": 34.87429543059638,
  "radial_IAE_m_s": 5251.017659355356,
  "signed_longitudinal_delta_m": 34.71178394806964,
  "tail_speed_mean_m_s": 0.1156673322063367,
  "tail_speed_rms_m_s": 0.115667332242654,
  "tail_sensor_speed_mean_m_s": 0.11541729713442925,
  "tail_fk_speed_mean_m_s": 0.11541744763247061,
  "peak_tilt_rad": 0.11578615022425254,
  "peak_wheel_torque_nm": 0.31667107343673706,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 58.05037330696359
}
```
