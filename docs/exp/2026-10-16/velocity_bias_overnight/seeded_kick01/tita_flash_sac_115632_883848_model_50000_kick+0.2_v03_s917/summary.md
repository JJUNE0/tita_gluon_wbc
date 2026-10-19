# tita_flash_sac_115632_883848_model_50000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "3676b3c97680ba2f32b6ed44a0391aaaccf1f7a2bed78f2d4a916323720117fa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003561243639587704,
  "max_drift_m": 0.09314452181419396,
  "radial_IAE_m_s": 0.3712334345731319,
  "signed_longitudinal_delta_m": -0.0034790173334454636,
  "tail_speed_mean_m_s": 3.4338442286547632e-06,
  "tail_speed_rms_m_s": 6.158069396403573e-06,
  "tail_sensor_speed_mean_m_s": 3.6006505228297496e-06,
  "tail_fk_speed_mean_m_s": 6.025045575002525e-06,
  "peak_tilt_rad": 0.08026468681266441,
  "peak_wheel_torque_nm": 1.5304142236709595,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.02137319157807245,
  "final_integral_m_s": 0.02137319157807245,
  "elapsed_wall_s": 10.868477264011744
}
```
