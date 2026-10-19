# tita_flash_sac_115632_883848_model_50000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
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
  "checkpoint_sha256": "d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c",
  "onnx_sha256": "0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873",
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
  "initial_physics_sha256": "80771bea00818d7d118ff7ba828cec04f4db7b25fc5330c23a72e5fe9c54ae5d",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 2.9992976546507015,
  "max_drift_m": 2.9992976546507015,
  "radial_IAE_m_s": 427.5086648894585,
  "signed_longitudinal_delta_m": 2.213795425938296,
  "tail_speed_mean_m_s": 0.01311229778837414,
  "tail_speed_rms_m_s": 0.013112312872811302,
  "tail_sensor_speed_mean_m_s": 0.013091293336474123,
  "tail_fk_speed_mean_m_s": 0.013093205734544786,
  "peak_tilt_rad": 0.04186662055856871,
  "peak_wheel_torque_nm": 0.2994948923587799,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 49.65541527897585
}
```
