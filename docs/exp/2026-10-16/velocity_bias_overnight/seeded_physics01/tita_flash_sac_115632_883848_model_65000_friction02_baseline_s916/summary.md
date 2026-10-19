# tita_flash_sac_115632_883848_model_65000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "3bb83dc79c6b38fcd96c6e250463198d11a6ab2c23be3a707606f70e8085409f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.157516459655664,
  "max_drift_m": 1.157516459655664,
  "radial_IAE_m_s": 37.29162792801188,
  "signed_longitudinal_delta_m": 0.7831508130587845,
  "tail_speed_mean_m_s": 0.02101510951956545,
  "tail_speed_rms_m_s": 0.02102098103470736,
  "tail_sensor_speed_mean_m_s": 0.020650661072812108,
  "tail_fk_speed_mean_m_s": 0.020625825233500823,
  "peak_tilt_rad": 0.05475042341077341,
  "peak_wheel_torque_nm": 0.17191177606582642,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.902297177992295
}
```
