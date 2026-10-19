# tita_flash_sac_193248_068255_model_85000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "b81b816cbbd4124b4d8d2b8789532d6d9e3bb713093fa49ae73cdfea1a7bc41e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.848492100544949,
  "max_drift_m": 12.848492100544949,
  "radial_IAE_m_s": 380.8519323523475,
  "signed_longitudinal_delta_m": -12.848061186555892,
  "tail_speed_mean_m_s": -0.2182183316676913,
  "tail_speed_rms_m_s": 0.2182230822854579,
  "tail_sensor_speed_mean_m_s": -0.21782675253993453,
  "tail_fk_speed_mean_m_s": -0.21782841623886823,
  "peak_tilt_rad": 0.08714353511239104,
  "peak_wheel_torque_nm": 1.2667845487594604,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.435161168978084
}
```
