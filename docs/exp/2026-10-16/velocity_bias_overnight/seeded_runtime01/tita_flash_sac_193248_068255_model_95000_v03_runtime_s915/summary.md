# tita_flash_sac_193248_068255_model_95000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "final_drift_m": 0.013195197062082433,
  "max_drift_m": 0.08202198244364758,
  "radial_IAE_m_s": 1.0228391609866359,
  "signed_longitudinal_delta_m": 0.013190083567569897,
  "tail_speed_mean_m_s": 7.265947144733758e-06,
  "tail_speed_rms_m_s": 1.7534891629946747e-05,
  "tail_sensor_speed_mean_m_s": 7.502266776119033e-06,
  "tail_fk_speed_mean_m_s": 6.847577239285498e-06,
  "peak_tilt_rad": 0.08427200924026779,
  "peak_wheel_torque_nm": 0.5813603401184082,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23610512943833561,
  "final_integral_m_s": -0.23610512943833561,
  "elapsed_wall_s": 17.637653829995543
}
```
