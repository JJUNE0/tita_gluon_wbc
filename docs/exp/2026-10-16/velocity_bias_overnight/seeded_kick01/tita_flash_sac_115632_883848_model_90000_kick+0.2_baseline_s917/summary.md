# tita_flash_sac_115632_883848_model_90000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
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
  "initial_physics_sha256": "8c25e031663db8883caf93e3840c0e1bdc801720c3724af777003880f3547d59",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.858361704271842,
  "max_drift_m": 6.858361704271842,
  "radial_IAE_m_s": 208.58114250617837,
  "signed_longitudinal_delta_m": 6.857237669913105,
  "tail_speed_mean_m_s": 0.11337585797202558,
  "tail_speed_rms_m_s": 0.11337610877364557,
  "tail_sensor_speed_mean_m_s": 0.11313046865398722,
  "tail_fk_speed_mean_m_s": 0.11312871939911859,
  "peak_tilt_rad": 0.08531640802716955,
  "peak_wheel_torque_nm": 1.7408294677734375,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.779539770970587
}
```
