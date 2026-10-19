# tita_flash_sac_115632_883848_model_90000_com_plus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_com_plus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "edababaeea9c0e1a21741bca3825c9b1df89316b2a98d943e242da5ceef04170",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04088419643177103,
  "max_drift_m": 0.06523324324439544,
  "radial_IAE_m_s": 2.3434209670483,
  "signed_longitudinal_delta_m": 0.04088412574919039,
  "tail_speed_mean_m_s": 0.00011034145489279218,
  "tail_speed_rms_m_s": 0.00011494136521418934,
  "tail_sensor_speed_mean_m_s": 0.00010980506584762428,
  "tail_fk_speed_mean_m_s": 0.00011091693586092878,
  "peak_tilt_rad": 0.06934915373597783,
  "peak_wheel_torque_nm": 0.5741122364997864,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4355618081089759,
  "final_integral_m_s": 0.4355618081089759,
  "elapsed_wall_s": 12.37095893197693
}
```
