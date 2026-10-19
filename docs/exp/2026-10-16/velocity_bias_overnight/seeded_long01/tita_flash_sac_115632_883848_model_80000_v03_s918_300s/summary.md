# tita_flash_sac_115632_883848_model_80000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
  "initial_physics_sha256": "5b3521df98c267163433f775bdb0aeb015b60616146b9ea8d6520ac042e379c9",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.15202062563424654,
  "max_drift_m": 0.1524103025084373,
  "radial_IAE_m_s": 42.26429465709087,
  "signed_longitudinal_delta_m": 0.15132365928700373,
  "tail_speed_mean_m_s": 6.049011887040867e-06,
  "tail_speed_rms_m_s": 6.072346327398967e-06,
  "tail_sensor_speed_mean_m_s": 5.186224895658458e-06,
  "tail_fk_speed_mean_m_s": 1.0022668492043938e-06,
  "peak_tilt_rad": 0.08429118503087207,
  "peak_wheel_torque_nm": 0.7028185725212097,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.9159215887300693,
  "final_integral_m_s": 0.9159215887300693,
  "elapsed_wall_s": 60.70252215198707
}
```
