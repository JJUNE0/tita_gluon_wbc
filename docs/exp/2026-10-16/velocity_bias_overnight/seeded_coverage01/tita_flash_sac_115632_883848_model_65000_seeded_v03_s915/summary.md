# tita_flash_sac_115632_883848_model_65000_seeded_v03_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_seeded_v03_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
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
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "b19288e5b981f0b8980c50777f2d0684536a784c722da92afec2ae97fa5bc8a7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0011580548379429567,
  "max_drift_m": 0.010977614009271197,
  "radial_IAE_m_s": 0.050822729901456594,
  "signed_longitudinal_delta_m": -0.001134869486688198,
  "tail_speed_mean_m_s": -2.1723580353408958e-05,
  "tail_speed_rms_m_s": 2.1888968187950213e-05,
  "tail_sensor_speed_mean_m_s": -2.1538981916660922e-05,
  "tail_fk_speed_mean_m_s": -2.2730545857145706e-05,
  "peak_tilt_rad": 0.05666680076887087,
  "peak_wheel_torque_nm": 0.34579235315322876,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.048698589370362484,
  "final_integral_m_s": 0.048698589370362484,
  "elapsed_wall_s": 4.690449686022475
}
```
