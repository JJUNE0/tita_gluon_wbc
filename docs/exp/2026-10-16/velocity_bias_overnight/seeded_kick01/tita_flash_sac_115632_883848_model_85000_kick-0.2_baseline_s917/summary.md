# tita_flash_sac_115632_883848_model_85000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
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
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "ac9f2dec546be415eb36fc255f21a26d0cfe087f05eac629e9d68f9983ef9a67",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.215765370648868,
  "max_drift_m": 7.215765370648868,
  "radial_IAE_m_s": 207.13520620817022,
  "signed_longitudinal_delta_m": 7.203835078689377,
  "tail_speed_mean_m_s": 0.12715090078168337,
  "tail_speed_rms_m_s": 0.1271527221865372,
  "tail_sensor_speed_mean_m_s": 0.12687601007982138,
  "tail_fk_speed_mean_m_s": 0.12687621476284602,
  "peak_tilt_rad": 0.06729897348253044,
  "peak_wheel_torque_nm": 2.0945005416870117,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.402302558999509
}
```
