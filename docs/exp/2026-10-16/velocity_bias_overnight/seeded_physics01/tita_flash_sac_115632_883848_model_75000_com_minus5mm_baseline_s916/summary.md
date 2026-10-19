# tita_flash_sac_115632_883848_model_75000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
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
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "e5e571a5d81e2c083830fddf7c7ded0af159bac463c743bb2157b1aad186c4e2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.7239513579716503,
  "max_drift_m": 1.7239513579716503,
  "radial_IAE_m_s": 53.514314812101354,
  "signed_longitudinal_delta_m": -1.722408352658564,
  "tail_speed_mean_m_s": -0.027462033962810575,
  "tail_speed_rms_m_s": 0.027463546185432185,
  "tail_sensor_speed_mean_m_s": -0.02740204120695271,
  "tail_fk_speed_mean_m_s": -0.02740025470005155,
  "peak_tilt_rad": 0.044068367962645905,
  "peak_wheel_torque_nm": 0.16093912720680237,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.126466471003368
}
```
