# tita_flash_sac_115632_883848_model_65000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "d0871b60b28af3961074838e8830503f125937fa14b1a62fc152064a3315da1a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05863484083026452,
  "max_drift_m": 0.09959621213150319,
  "radial_IAE_m_s": 3.5485558399473764,
  "signed_longitudinal_delta_m": 0.05861489056000636,
  "tail_speed_mean_m_s": 7.252069248977307e-07,
  "tail_speed_rms_m_s": 1.0145644886926084e-06,
  "tail_sensor_speed_mean_m_s": 5.441308690604559e-07,
  "tail_fk_speed_mean_m_s": -8.027448395063851e-07,
  "peak_tilt_rad": 0.18153604971476578,
  "peak_wheel_torque_nm": 1.3937971591949463,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.39429403211652847,
  "final_integral_m_s": -0.39429403211652847,
  "elapsed_wall_s": 10.099132934003137
}
```
