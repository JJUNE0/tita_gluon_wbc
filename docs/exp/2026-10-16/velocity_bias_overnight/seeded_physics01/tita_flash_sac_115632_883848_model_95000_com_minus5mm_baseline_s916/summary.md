# tita_flash_sac_115632_883848_model_95000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "1efa0be7650fb491e06b6fc65ed8a72ede3c3ffa5ab1b641bfc96bb99d4f9fd6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.9479508126623224,
  "max_drift_m": 0.9479508126623224,
  "radial_IAE_m_s": 32.24755347205689,
  "signed_longitudinal_delta_m": -0.9474147225236467,
  "tail_speed_mean_m_s": -0.011767829273764381,
  "tail_speed_rms_m_s": 0.011828967173516187,
  "tail_sensor_speed_mean_m_s": -0.01174215324886392,
  "tail_fk_speed_mean_m_s": -0.011742004859898151,
  "peak_tilt_rad": 0.05671592563466521,
  "peak_wheel_torque_nm": 0.15089163184165955,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 16.097658112004865
}
```
