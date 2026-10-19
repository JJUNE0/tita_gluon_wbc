# tita_flash_sac_193248_068255_model_50000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "604f73a9b7af4ba012f944ce38a832332ded44f60bc228893c63e2be75800597",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.97176335791108,
  "max_drift_m": 6.97176335791108,
  "radial_IAE_m_s": 196.95837779640897,
  "signed_longitudinal_delta_m": 6.971250428837533,
  "tail_speed_mean_m_s": 0.12611118528566218,
  "tail_speed_rms_m_s": 0.12611597421161982,
  "tail_sensor_speed_mean_m_s": 0.12583865829683552,
  "tail_fk_speed_mean_m_s": 0.12583697819501385,
  "peak_tilt_rad": 0.05841818775050167,
  "peak_wheel_torque_nm": 2.370551824569702,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.930786921002436
}
```
