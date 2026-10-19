# tita_flash_sac_115632_883848_model_50000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "bc6b350abfa161dcf4bc5026f9ffff4954570ef32bd87984b232678b343b95ae",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.5151521384474634,
  "max_drift_m": 0.5151521384474634,
  "radial_IAE_m_s": 15.971712379480053,
  "signed_longitudinal_delta_m": -0.49882021825205586,
  "tail_speed_mean_m_s": -0.008185323478034807,
  "tail_speed_rms_m_s": 0.008185429827917054,
  "tail_sensor_speed_mean_m_s": -0.00816750777757687,
  "tail_fk_speed_mean_m_s": -0.008164885870555364,
  "peak_tilt_rad": 0.03541382277938254,
  "peak_wheel_torque_nm": 0.28118520975112915,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.598374000983313
}
```
