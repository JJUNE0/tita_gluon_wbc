# tita_flash_sac_115632_883848_model_50000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
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
  "initial_physics_sha256": "f1deb2428568cc7c6d03beeb051d1f576c5638fd56482d9a18c9a0716128ed85",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.39880282887007557,
  "max_drift_m": 0.39880282887007557,
  "radial_IAE_m_s": 9.750391207352948,
  "signed_longitudinal_delta_m": 0.38021718469243143,
  "tail_speed_mean_m_s": 0.00932715729245936,
  "tail_speed_rms_m_s": 0.009327340584084675,
  "tail_sensor_speed_mean_m_s": 0.009307219404647616,
  "tail_fk_speed_mean_m_s": 0.009309456033200018,
  "peak_tilt_rad": 0.04186652999556806,
  "peak_wheel_torque_nm": 1.3749606609344482,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.565680306986906
}
```
