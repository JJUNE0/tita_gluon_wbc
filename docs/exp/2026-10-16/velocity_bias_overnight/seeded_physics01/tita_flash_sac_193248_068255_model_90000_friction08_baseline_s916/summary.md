# tita_flash_sac_193248_068255_model_90000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
  "initial_physics_sha256": "7de6d925a7a398d8b8b6f5d71dfedbf2dcd9303f6660ddef5dd47159da3a767f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.027681607539822,
  "max_drift_m": 13.027681607539822,
  "radial_IAE_m_s": 382.56078336114655,
  "signed_longitudinal_delta_m": 13.027681235245984,
  "tail_speed_mean_m_s": 0.2234844234398998,
  "tail_speed_rms_m_s": 0.22348455233960746,
  "tail_sensor_speed_mean_m_s": 0.22300104239986596,
  "tail_fk_speed_mean_m_s": 0.22299867894534023,
  "peak_tilt_rad": 0.11197443235947935,
  "peak_wheel_torque_nm": 1.9543969631195068,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.53765542799374
}
```
