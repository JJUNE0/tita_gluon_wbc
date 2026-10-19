# tita_flash_sac_115632_883848_model_50000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "3676b3c97680ba2f32b6ed44a0391aaaccf1f7a2bed78f2d4a916323720117fa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.6825492687582454,
  "max_drift_m": 0.6825492687582454,
  "radial_IAE_m_s": 24.49645919411426,
  "signed_longitudinal_delta_m": 0.6717730137426555,
  "tail_speed_mean_m_s": 0.009334211367559877,
  "tail_speed_rms_m_s": 0.009334364654254081,
  "tail_sensor_speed_mean_m_s": 0.00931427983550747,
  "tail_fk_speed_mean_m_s": 0.009316500839794555,
  "peak_tilt_rad": 0.08120015151125104,
  "peak_wheel_torque_nm": 1.5010478496551514,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.630904001998715
}
```
