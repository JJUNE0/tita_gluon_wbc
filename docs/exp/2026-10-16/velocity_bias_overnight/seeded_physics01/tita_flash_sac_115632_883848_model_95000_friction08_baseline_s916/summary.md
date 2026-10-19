# tita_flash_sac_115632_883848_model_95000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
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
  "initial_physics_sha256": "d7a51163fbd74bc316c8eb32abfb3200a80bc2936cea8ba8c1f73191508a81de",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.8140532090183071,
  "max_drift_m": 0.8140532090183071,
  "radial_IAE_m_s": 18.533099741538642,
  "signed_longitudinal_delta_m": 0.8132735223504153,
  "tail_speed_mean_m_s": 0.01985433547830803,
  "tail_speed_rms_m_s": 0.019920792950000033,
  "tail_sensor_speed_mean_m_s": 0.019811707687686694,
  "tail_fk_speed_mean_m_s": 0.019811749972466493,
  "peak_tilt_rad": 0.06367801355769354,
  "peak_wheel_torque_nm": 0.17591172456741333,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.802389948978089
}
```
