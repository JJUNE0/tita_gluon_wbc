# tita_flash_sac_193248_068255_model_90000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
  "initial_physics_sha256": "8e44895214e437d8ae00e1dbe370cfb100623cb5db5ec0c4e1a8fc17d33f2eec",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 15.933481074924288,
  "max_drift_m": 15.933481074924288,
  "radial_IAE_m_s": 469.7223647520849,
  "signed_longitudinal_delta_m": 15.909824259831488,
  "tail_speed_mean_m_s": 0.2721057704793432,
  "tail_speed_rms_m_s": 0.2721058032786984,
  "tail_sensor_speed_mean_m_s": 0.2715170061697358,
  "tail_fk_speed_mean_m_s": 0.2715148670976652,
  "peak_tilt_rad": 0.11795031609155804,
  "peak_wheel_torque_nm": 1.9105417728424072,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.0610268979799
}
```
