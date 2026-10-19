# tita_flash_sac_193248_068255_model_85000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
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
  "checkpoint_sha256": "520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b",
  "onnx_sha256": "5d2438e3be90051d15448f31e014bdcdd44f963c2caabea6f5c8a62f0c9e2e0e",
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
  "initial_physics_sha256": "cbd5286036469307dc8a34b48bf8217f8f809607ca629fe085e47fed2ec29884",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.803100458648201,
  "max_drift_m": 6.803100458648201,
  "radial_IAE_m_s": 197.45735853779487,
  "signed_longitudinal_delta_m": 6.8024890263793285,
  "tail_speed_mean_m_s": 0.11925017966919114,
  "tail_speed_rms_m_s": 0.11925214737232911,
  "tail_sensor_speed_mean_m_s": 0.11899243023197559,
  "tail_fk_speed_mean_m_s": 0.11899046243810282,
  "peak_tilt_rad": 0.06865888099997064,
  "peak_wheel_torque_nm": 0.5032657384872437,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.155265274981502
}
```
