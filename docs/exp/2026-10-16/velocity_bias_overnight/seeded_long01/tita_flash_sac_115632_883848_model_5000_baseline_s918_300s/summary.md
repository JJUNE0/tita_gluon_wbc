# tita_flash_sac_115632_883848_model_5000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
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
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "65218c0f51ba1e8e455ead804618fb3569f6936691847505c6cd07e05f04b918",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 36.05368899452505,
  "max_drift_m": 36.05368899452505,
  "radial_IAE_m_s": 6470.293162530568,
  "signed_longitudinal_delta_m": -5.007361578023276,
  "tail_speed_mean_m_s": -0.16874805673492868,
  "tail_speed_rms_m_s": 0.16997365847471754,
  "tail_sensor_speed_mean_m_s": -0.16793117812399747,
  "tail_fk_speed_mean_m_s": -0.1678954534930272,
  "peak_tilt_rad": 0.07376482571343979,
  "peak_wheel_torque_nm": 3.895056962966919,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 46.05725520598935
}
```
