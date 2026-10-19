# tita_flash_sac_115632_883848_model_90000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
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
  "initial_physics_sha256": "52ed719826815c3906b2fd95a44df11b9b48d555ed06bf7d7d9df6838eecb989",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 33.69750276921067,
  "max_drift_m": 33.69750276921067,
  "radial_IAE_m_s": 5068.8793292134405,
  "signed_longitudinal_delta_m": 32.407474687635805,
  "tail_speed_mean_m_s": 0.1152315877407955,
  "tail_speed_rms_m_s": 0.11523158774576804,
  "tail_sensor_speed_mean_m_s": 0.11498232961339303,
  "tail_fk_speed_mean_m_s": 0.11498024732397923,
  "peak_tilt_rad": 0.07073675653800304,
  "peak_wheel_torque_nm": 0.19447743892669678,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 54.16409619001206
}
```
