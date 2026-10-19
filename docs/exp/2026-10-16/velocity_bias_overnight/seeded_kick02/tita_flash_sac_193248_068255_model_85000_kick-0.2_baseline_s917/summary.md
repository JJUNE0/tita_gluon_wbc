# tita_flash_sac_193248_068255_model_85000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "c5cce1b74de5607ac2dd5801f4eab1571c1a665c95e677eadf61ef868ae9fef9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.46325659217107,
  "max_drift_m": 6.46325659217107,
  "radial_IAE_m_s": 177.11592741588458,
  "signed_longitudinal_delta_m": 6.46042657267725,
  "tail_speed_mean_m_s": 0.11964909873773323,
  "tail_speed_rms_m_s": 0.11965076312484811,
  "tail_sensor_speed_mean_m_s": 0.11939051896515483,
  "tail_fk_speed_mean_m_s": 0.11938850809413325,
  "peak_tilt_rad": 0.06874786166064606,
  "peak_wheel_torque_nm": 1.6098670959472656,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.96990652801469
}
```
