# tita_flash_sac_115632_883848_model_50000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "b6fbd8cecc69a2caab562197a099693af7f0bca4e2c4ee0a8dbf96e99c763b1e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.12244439931705683,
  "max_drift_m": 0.32809118596867026,
  "radial_IAE_m_s": 13.732044969928964,
  "signed_longitudinal_delta_m": -0.03182836905154893,
  "tail_speed_mean_m_s": 0.010179167392517565,
  "tail_speed_rms_m_s": 0.01019199338458744,
  "tail_sensor_speed_mean_m_s": 0.010293688991471593,
  "tail_fk_speed_mean_m_s": 0.01019482151868341,
  "peak_tilt_rad": 0.04025049997167707,
  "peak_wheel_torque_nm": 0.14173057675361633,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.577707896998618
}
```
