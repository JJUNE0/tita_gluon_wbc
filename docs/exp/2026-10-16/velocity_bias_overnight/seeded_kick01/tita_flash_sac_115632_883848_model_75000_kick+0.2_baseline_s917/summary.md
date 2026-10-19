# tita_flash_sac_115632_883848_model_75000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "72dd3b16ae1ec0e18dab2ec793c22110949f90b73330649a96c7d09c59cf1cc8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.1759107005379872,
  "max_drift_m": 0.1759107005379872,
  "radial_IAE_m_s": 8.866031266890815,
  "signed_longitudinal_delta_m": 0.1759016574600207,
  "tail_speed_mean_m_s": 0.0011908499219186342,
  "tail_speed_rms_m_s": 0.0012082127675962324,
  "tail_sensor_speed_mean_m_s": 0.001188378414534104,
  "tail_fk_speed_mean_m_s": 0.00118887477732668,
  "peak_tilt_rad": 0.06829326341097364,
  "peak_wheel_torque_nm": 1.7288684844970703,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.771073678974062
}
```
