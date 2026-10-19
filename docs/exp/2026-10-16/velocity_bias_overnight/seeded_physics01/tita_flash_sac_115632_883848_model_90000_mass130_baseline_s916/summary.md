# tita_flash_sac_115632_883848_model_90000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
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
  "initial_physics_sha256": "ab05416af08e01c365356eb03a9e56f35fada293118e65c01788c667ca86eba0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.860031948412653,
  "max_drift_m": 6.860031948412653,
  "radial_IAE_m_s": 205.7024572961368,
  "signed_longitudinal_delta_m": -6.857574618712925,
  "tail_speed_mean_m_s": -0.11439654844928693,
  "tail_speed_rms_m_s": 0.11439655027760018,
  "tail_sensor_speed_mean_m_s": -0.11415091929682186,
  "tail_fk_speed_mean_m_s": -0.11415077031925544,
  "peak_tilt_rad": 0.0761150841806224,
  "peak_wheel_torque_nm": 0.7649062871932983,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.288539454981219
}
```
