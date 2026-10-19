# tita_flash_sac_115632_883848_model_50000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "5c4ecfc1249621928036ec0b121117c2c28462f355424b0863b99146e1e7e7c8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.5167366664769276,
  "max_drift_m": 0.5167366664769276,
  "radial_IAE_m_s": 14.782748713457627,
  "signed_longitudinal_delta_m": 0.4352274486278862,
  "tail_speed_mean_m_s": 0.00938879500446722,
  "tail_speed_rms_m_s": 0.009388926522021427,
  "tail_sensor_speed_mean_m_s": 0.009370722741999344,
  "tail_fk_speed_mean_m_s": 0.00937276354620748,
  "peak_tilt_rad": 0.04159593924450733,
  "peak_wheel_torque_nm": 0.29918789863586426,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.3337269120384
}
```
