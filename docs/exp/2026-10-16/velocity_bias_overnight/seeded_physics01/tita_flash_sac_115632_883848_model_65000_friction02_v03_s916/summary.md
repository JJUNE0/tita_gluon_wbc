# tita_flash_sac_115632_883848_model_65000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
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
  "final_drift_m": 0.00699205888354663,
  "max_drift_m": 0.0074122417732257456,
  "radial_IAE_m_s": 0.28776545917561347,
  "signed_longitudinal_delta_m": -0.0006023992565629537,
  "tail_speed_mean_m_s": 4.815743869966374e-05,
  "tail_speed_rms_m_s": 4.815779386820573e-05,
  "tail_sensor_speed_mean_m_s": 2.7136270564627485e-05,
  "tail_fk_speed_mean_m_s": -3.605695342837432e-07,
  "peak_tilt_rad": 0.053095921203135665,
  "peak_wheel_torque_nm": 0.2215682566165924,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.026225445418376722,
  "final_integral_m_s": 0.026225445418376722,
  "elapsed_wall_s": 10.02799882099498
}
```
