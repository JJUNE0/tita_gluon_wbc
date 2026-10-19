# tita_flash_sac_115632_883848_model_15000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "2e8966a51e48d17508693dec4fb93308303992fe7384acb8c8c2166c81cee1bb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.869733537069284,
  "max_drift_m": 7.869733537069284,
  "radial_IAE_m_s": 234.7194710414264,
  "signed_longitudinal_delta_m": -7.860748402877125,
  "tail_speed_mean_m_s": -0.1320467751179129,
  "tail_speed_rms_m_s": 0.13206619211488582,
  "tail_sensor_speed_mean_m_s": -0.13174126348698448,
  "tail_fk_speed_mean_m_s": -0.13179601076938977,
  "peak_tilt_rad": 0.05882262469220656,
  "peak_wheel_torque_nm": 2.0246665477752686,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.210397136979736
}
```
