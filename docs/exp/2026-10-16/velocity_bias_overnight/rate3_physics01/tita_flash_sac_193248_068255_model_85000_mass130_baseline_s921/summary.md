# tita_flash_sac_193248_068255_model_85000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "a8c25717ef3266bd233535218686aa1a2b6be2b5366fea0c8a71b23efbb8d345",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.848461124907232,
  "max_drift_m": 12.848461124907232,
  "radial_IAE_m_s": 380.85139300814296,
  "signed_longitudinal_delta_m": -12.848029355754518,
  "tail_speed_mean_m_s": -0.21821726377464024,
  "tail_speed_rms_m_s": 0.21822201289164833,
  "tail_sensor_speed_mean_m_s": -0.21782567538886907,
  "tail_fk_speed_mean_m_s": -0.21782733723187092,
  "peak_tilt_rad": 0.08714358324730731,
  "peak_wheel_torque_nm": 1.2667932510375977,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.842802794009913
}
```
