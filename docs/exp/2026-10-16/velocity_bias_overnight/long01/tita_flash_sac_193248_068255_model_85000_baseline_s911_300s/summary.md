# tita_flash_sac_193248_068255_model_85000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "4e2983442be50ecb825ea34a4dd41cddcd1f9cbee977c07e8641265efd1e7c4c",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 35.80159250282631,
  "max_drift_m": 35.80159250282631,
  "radial_IAE_m_s": 5355.901275789829,
  "signed_longitudinal_delta_m": 34.056242196096235,
  "tail_speed_mean_m_s": 0.12384417712851134,
  "tail_speed_rms_m_s": 0.12384417714196828,
  "tail_sensor_speed_mean_m_s": 0.12357619748571934,
  "tail_fk_speed_mean_m_s": 0.12357426411385238,
  "peak_tilt_rad": 0.0697244148092322,
  "peak_wheel_torque_nm": 0.5138702988624573,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 61.14503222098574
}
```
