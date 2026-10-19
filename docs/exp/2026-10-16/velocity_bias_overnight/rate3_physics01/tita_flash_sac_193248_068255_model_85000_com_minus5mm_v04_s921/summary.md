# tita_flash_sac_193248_068255_model_85000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "06e1d08fbcbe20a122b403a688f7da77f9f04ff9be36227107978c07d62b20ad",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004742420918671278,
  "max_drift_m": 0.01869386471983281,
  "radial_IAE_m_s": 0.18931930277198905,
  "signed_longitudinal_delta_m": 0.0047398902258972185,
  "tail_speed_mean_m_s": 0.00012669376797622289,
  "tail_speed_rms_m_s": 0.0001269995163403818,
  "tail_sensor_speed_mean_m_s": 0.00012652691029855064,
  "tail_fk_speed_mean_m_s": 0.0001262923860788017,
  "peak_tilt_rad": 0.053697646461358106,
  "peak_wheel_torque_nm": 0.38997408747673035,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.09142605742954796,
  "final_integral_m_s": 0.09142605742954796,
  "elapsed_wall_s": 9.742227550013922
}
```
