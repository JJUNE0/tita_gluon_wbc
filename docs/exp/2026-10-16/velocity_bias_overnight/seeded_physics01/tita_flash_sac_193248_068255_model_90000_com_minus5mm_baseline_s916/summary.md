# tita_flash_sac_193248_068255_model_90000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "08f0f8fb0cffaaa58ca08bb852b4d13d2fd0e2035179d358f48098cce80cb863",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.462486215158243,
  "max_drift_m": 10.462486215158243,
  "radial_IAE_m_s": 305.3033826235879,
  "signed_longitudinal_delta_m": 10.460084275053816,
  "tail_speed_mean_m_s": 0.1809390474402864,
  "tail_speed_rms_m_s": 0.18093952137266955,
  "tail_sensor_speed_mean_m_s": 0.18056074361175664,
  "tail_fk_speed_mean_m_s": 0.18054661439606215,
  "peak_tilt_rad": 0.10773209764925507,
  "peak_wheel_torque_nm": 1.836105227470398,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.571803889004514
}
```
