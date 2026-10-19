# tita_flash_sac_115632_883848_model_80000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "ff0ea9eb54537af6d3301b705c78d05253b17588ebdf67aa9d564c099f6087a3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.859238806583203,
  "max_drift_m": 11.859238806583203,
  "radial_IAE_m_s": 354.7764737434243,
  "signed_longitudinal_delta_m": 11.817805773519355,
  "tail_speed_mean_m_s": 0.19957017840594507,
  "tail_speed_rms_m_s": 0.19957044630320292,
  "tail_sensor_speed_mean_m_s": 0.19913908398955713,
  "tail_fk_speed_mean_m_s": 0.19913811912721802,
  "peak_tilt_rad": 0.1032545871407986,
  "peak_wheel_torque_nm": 1.9158804416656494,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.477268857997842
}
```
