# tita_flash_sac_193248_068255_model_85000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "0e411dd38f76df0acff629b71e96036eb5f456d42be2edf63a551b887bcfdd05",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.658178201096932,
  "max_drift_m": 8.658178201096932,
  "radial_IAE_m_s": 254.18956413744834,
  "signed_longitudinal_delta_m": 8.6580487104604,
  "tail_speed_mean_m_s": 0.14922785553304924,
  "tail_speed_rms_m_s": 0.14923115074858362,
  "tail_sensor_speed_mean_m_s": 0.14883084969206048,
  "tail_fk_speed_mean_m_s": 0.14892077493589292,
  "peak_tilt_rad": 0.07307623993084822,
  "peak_wheel_torque_nm": 0.6187353730201721,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.935904296988156
}
```
