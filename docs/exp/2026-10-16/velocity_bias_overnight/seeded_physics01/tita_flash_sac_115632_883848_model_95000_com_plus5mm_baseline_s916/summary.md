# tita_flash_sac_115632_883848_model_95000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "9d7baecd0b3531249823e35e05b097619acd499dc8c759011f0d5e09b1de01e8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.1563931758054298,
  "max_drift_m": 3.1563931758054298,
  "radial_IAE_m_s": 89.44321402236808,
  "signed_longitudinal_delta_m": 3.1550989343788025,
  "tail_speed_mean_m_s": 0.05796441146355869,
  "tail_speed_rms_m_s": 0.05797590585838202,
  "tail_sensor_speed_mean_m_s": 0.05783933192624672,
  "tail_fk_speed_mean_m_s": 0.05783926047790377,
  "peak_tilt_rad": 0.06955956642724748,
  "peak_wheel_torque_nm": 0.20697452127933502,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.14164000301389
}
```
