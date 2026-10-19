# tita_flash_sac_193248_068255_model_95000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "7ecc93e40b3201e947dc524cba63f688374feab51ae26a31d81f629ef8547bf0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.032997204969799125,
  "max_drift_m": 0.06045392535214757,
  "radial_IAE_m_s": 1.9500728922731838,
  "signed_longitudinal_delta_m": 0.03299629261790966,
  "tail_speed_mean_m_s": 2.2779330641841943e-05,
  "tail_speed_rms_m_s": 2.278418228587523e-05,
  "tail_sensor_speed_mean_m_s": 2.293649093380617e-05,
  "tail_fk_speed_mean_m_s": 2.241908498839761e-05,
  "peak_tilt_rad": 0.07234595014093204,
  "peak_wheel_torque_nm": 0.3753349184989929,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.0413111418944604,
  "final_integral_m_s": -0.0413111418944604,
  "elapsed_wall_s": 6.610256196989212
}
```
