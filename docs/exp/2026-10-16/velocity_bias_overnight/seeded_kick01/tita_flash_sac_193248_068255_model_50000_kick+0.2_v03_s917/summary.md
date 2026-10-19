# tita_flash_sac_193248_068255_model_50000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "e70b49ab72c81db34a2b45bcf93d2f8926342786f192607d4cf70c06a11be147",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09453697388045072,
  "max_drift_m": 0.1134710542649875,
  "radial_IAE_m_s": 5.5903897862339464,
  "signed_longitudinal_delta_m": 0.09453595359487861,
  "tail_speed_mean_m_s": 5.50299798716526e-05,
  "tail_speed_rms_m_s": 5.537022731274811e-05,
  "tail_sensor_speed_mean_m_s": 5.483809144468779e-05,
  "tail_fk_speed_mean_m_s": 5.5904004050829935e-05,
  "peak_tilt_rad": 0.07726021263133576,
  "peak_wheel_torque_nm": 2.060487747192383,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6973043587652816,
  "final_integral_m_s": 0.6973043587652816,
  "elapsed_wall_s": 8.967332486994565
}
```
