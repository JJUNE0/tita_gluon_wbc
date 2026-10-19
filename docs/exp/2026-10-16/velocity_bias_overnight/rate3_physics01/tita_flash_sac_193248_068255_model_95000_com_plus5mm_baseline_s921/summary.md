# tita_flash_sac_193248_068255_model_95000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
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
  "final_drift_m": 0.8342738594530179,
  "max_drift_m": 0.8342738594530179,
  "radial_IAE_m_s": 28.171423378051312,
  "signed_longitudinal_delta_m": -0.8342460422816842,
  "tail_speed_mean_m_s": -0.011868327388405375,
  "tail_speed_rms_m_s": 0.011868806351706035,
  "tail_sensor_speed_mean_m_s": -0.011842371771226877,
  "tail_fk_speed_mean_m_s": -0.011842822109638579,
  "peak_tilt_rad": 0.06012964263814613,
  "peak_wheel_torque_nm": 0.26037314534187317,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.657063485996332
}
```
