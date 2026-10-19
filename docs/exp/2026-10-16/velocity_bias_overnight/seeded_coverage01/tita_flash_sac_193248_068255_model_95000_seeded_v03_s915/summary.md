# tita_flash_sac_193248_068255_model_95000_seeded_v03_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_seeded_v03_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "guarded": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "eb50aadec4da436f3f6475e30a88539d8e1205a1f473fa5a389974f3b48b867a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013195248824027757,
  "max_drift_m": 0.08202196203962735,
  "radial_IAE_m_s": 1.0228388970911737,
  "signed_longitudinal_delta_m": 0.013190135447783705,
  "tail_speed_mean_m_s": 7.268202119240578e-06,
  "tail_speed_rms_m_s": 1.7532353979234407e-05,
  "tail_sensor_speed_mean_m_s": 7.505948459583837e-06,
  "tail_fk_speed_mean_m_s": 6.849935141706757e-06,
  "peak_tilt_rad": 0.08427198070112962,
  "peak_wheel_torque_nm": 0.5813603401184082,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2361048987106528,
  "final_integral_m_s": -0.2361048987106528,
  "elapsed_wall_s": 4.617501789005473
}
```
