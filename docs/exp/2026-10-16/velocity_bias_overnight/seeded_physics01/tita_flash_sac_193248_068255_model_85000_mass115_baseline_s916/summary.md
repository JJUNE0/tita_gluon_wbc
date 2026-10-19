# tita_flash_sac_193248_068255_model_85000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "854245f67baf6092206d6438c4e48bb1cfe71b099fd1dae00fe3b78e3021d83f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.0229597939262245,
  "max_drift_m": 6.0229597939262245,
  "radial_IAE_m_s": 174.7759797106599,
  "signed_longitudinal_delta_m": -6.011203275473172,
  "tail_speed_mean_m_s": -0.10621195993533865,
  "tail_speed_rms_m_s": 0.10622487370947978,
  "tail_sensor_speed_mean_m_s": -0.1060513518562952,
  "tail_fk_speed_mean_m_s": -0.1060553283583963,
  "peak_tilt_rad": 0.07619314587472914,
  "peak_wheel_torque_nm": 0.9059112071990967,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.505421270034276
}
```
