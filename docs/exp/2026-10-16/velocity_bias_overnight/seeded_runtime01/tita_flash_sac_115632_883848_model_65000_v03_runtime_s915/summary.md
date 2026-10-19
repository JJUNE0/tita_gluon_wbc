# tita_flash_sac_115632_883848_model_65000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "final_drift_m": 0.0011580395574663264,
  "max_drift_m": 0.010977584498011804,
  "radial_IAE_m_s": 0.05082243397213598,
  "signed_longitudinal_delta_m": -0.0011348535370655785,
  "tail_speed_mean_m_s": -2.1723747098617134e-05,
  "tail_speed_rms_m_s": 2.188987046585105e-05,
  "tail_sensor_speed_mean_m_s": -2.153926398707163e-05,
  "tail_fk_speed_mean_m_s": -2.2730656616263038e-05,
  "peak_tilt_rad": 0.05666680296898985,
  "peak_wheel_torque_nm": 0.3457942605018616,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0486986606050241,
  "final_integral_m_s": 0.0486986606050241,
  "elapsed_wall_s": 14.471229345013853
}
```
