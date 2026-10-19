# tita_flash_sac_193248_068255_model_85000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b",
  "onnx_sha256": "5d2438e3be90051d15448f31e014bdcdd44f963c2caabea6f5c8a62f0c9e2e0e",
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
  "initial_physics_sha256": "47d3e52c02d92d9c1985ef07f6f76df2a0267187234d6de78c827c79b82f15cd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09643565606895017,
  "max_drift_m": 0.12322519496988395,
  "radial_IAE_m_s": 6.316795483386075,
  "signed_longitudinal_delta_m": 0.09131130540960099,
  "tail_speed_mean_m_s": -0.000579579720416919,
  "tail_speed_rms_m_s": 0.009097835105047324,
  "tail_sensor_speed_mean_m_s": 7.456298426145676,
  "tail_fk_speed_mean_m_s": 7.456297727490935,
  "peak_tilt_rad": 0.6255485169009374,
  "peak_wheel_torque_nm": 9.219682693481445,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.2174461610266
}
```
