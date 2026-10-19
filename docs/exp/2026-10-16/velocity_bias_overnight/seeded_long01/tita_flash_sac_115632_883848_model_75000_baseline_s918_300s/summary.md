# tita_flash_sac_115632_883848_model_75000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
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
  "initial_physics_sha256": "6366aad38c3f71b70b0d14f6ff0d7398d51fb21b6fb83762cb9999959ce9bb17",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 1.9726141992552937,
  "max_drift_m": 1.9726141992552937,
  "radial_IAE_m_s": 171.35854390261005,
  "signed_longitudinal_delta_m": 1.963453735061141,
  "tail_speed_mean_m_s": 0.01430568251925775,
  "tail_speed_rms_m_s": 0.014307795975727506,
  "tail_sensor_speed_mean_m_s": 0.014274887642869877,
  "tail_fk_speed_mean_m_s": 0.014274895478694455,
  "peak_tilt_rad": 0.053446876826112044,
  "peak_wheel_torque_nm": 0.15775179862976074,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 59.833725164004136
}
```
