# tita_flash_sac_193248_068255_model_85000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
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
  "initial_physics_sha256": "c9262a3b00666f797b9fdf98f6b4145a82ae0a78141d1195f6b7bc81e47ea758",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 35.78964929321891,
  "max_drift_m": 35.78964929321891,
  "radial_IAE_m_s": 5352.422099037265,
  "signed_longitudinal_delta_m": 34.08332728105979,
  "tail_speed_mean_m_s": 0.12384402553413679,
  "tail_speed_rms_m_s": 0.1238440255480243,
  "tail_sensor_speed_mean_m_s": 0.12357604641571852,
  "tail_fk_speed_mean_m_s": 0.12357411323493518,
  "peak_tilt_rad": 0.06972436776333879,
  "peak_wheel_torque_nm": 0.5130490064620972,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 18.917321752000134
}
```
