# tita_flash_sac_193248_068255_model_85000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "d42c1ad588d7b8fc1fe563821ac00a47c713af437d39b025b05c51550bb29f2b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.709301594859236,
  "max_drift_m": 8.709301594859236,
  "radial_IAE_m_s": 256.32185039493237,
  "signed_longitudinal_delta_m": 8.70719868638153,
  "tail_speed_mean_m_s": 0.14953472554534497,
  "tail_speed_rms_m_s": 0.14953774197751335,
  "tail_sensor_speed_mean_m_s": 0.1491242210538469,
  "tail_fk_speed_mean_m_s": 0.14922516112535894,
  "peak_tilt_rad": 0.07313290494961411,
  "peak_wheel_torque_nm": 0.6244699954986572,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.385260456008837
}
```
