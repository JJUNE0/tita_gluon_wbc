# tita_flash_sac_115632_883848_model_15000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003",
  "onnx_sha256": "1fec00b7bc7eebbc5b6decf23ac6f29b8799c5cf64ff1dee51c1ba762cf013ed",
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
  "initial_physics_sha256": "72cbdc7a36154af8436b579301523f9e2b1a970fbc7e23de8d8cad772aa46a24",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.965962134497382,
  "max_drift_m": 3.965962134497382,
  "radial_IAE_m_s": 119.57618548766513,
  "signed_longitudinal_delta_m": -3.941257816276127,
  "tail_speed_mean_m_s": -0.06596914678764071,
  "tail_speed_rms_m_s": 0.0743758790371118,
  "tail_sensor_speed_mean_m_s": -0.06963270391251594,
  "tail_fk_speed_mean_m_s": -0.06656681419060007,
  "peak_tilt_rad": 0.15112066439128324,
  "peak_wheel_torque_nm": 6.8517680168151855,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.479906446009409
}
```
