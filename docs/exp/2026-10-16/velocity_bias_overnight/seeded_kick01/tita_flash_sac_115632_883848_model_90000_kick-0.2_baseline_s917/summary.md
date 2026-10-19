# tita_flash_sac_115632_883848_model_90000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
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
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "b3d19690c04c1145a9684e694dd52127f3767a688284a72de9e0f1886fd01282",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.5011117573184105,
  "max_drift_m": 6.5011117573184105,
  "radial_IAE_m_s": 187.73659762667393,
  "signed_longitudinal_delta_m": 6.499573625303144,
  "tail_speed_mean_m_s": 0.11326862357862987,
  "tail_speed_rms_m_s": 0.11326891943234643,
  "tail_sensor_speed_mean_m_s": 0.11302340973318752,
  "tail_fk_speed_mean_m_s": 0.11302171938120201,
  "peak_tilt_rad": 0.07060415023120559,
  "peak_wheel_torque_nm": 1.8677119016647339,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.058490145020187
}
```
