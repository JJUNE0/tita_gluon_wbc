# tita_flash_sac_115632_883848_model_75000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
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
  "initial_physics_sha256": "4a68ebadd660cceba434c95fe2ec96e2d15510d6e30defea553c96829bfd5925",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.7236780217143133,
  "max_drift_m": 1.7236780217143133,
  "radial_IAE_m_s": 49.450764469319836,
  "signed_longitudinal_delta_m": 1.723658625679739,
  "tail_speed_mean_m_s": 0.030457004530198905,
  "tail_speed_rms_m_s": 0.030458843924898622,
  "tail_sensor_speed_mean_m_s": 0.030391152434379128,
  "tail_fk_speed_mean_m_s": 0.03039075132678557,
  "peak_tilt_rad": 0.05746113980448175,
  "peak_wheel_torque_nm": 0.15948261320590973,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.938717911951244
}
```
