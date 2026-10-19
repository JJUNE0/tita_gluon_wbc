# tita_flash_sac_193248_068255_model_95000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
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
  "initial_physics_sha256": "9bad2fd21e173e5fa762c31013a3ba0187843391a383957e787ef9bba8406ac9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.085506421002323,
  "max_drift_m": 9.085506421002323,
  "radial_IAE_m_s": 265.70319941789506,
  "signed_longitudinal_delta_m": -8.850989682297268,
  "tail_speed_mean_m_s": -0.17472664641705718,
  "tail_speed_rms_m_s": 0.17566415957949041,
  "tail_sensor_speed_mean_m_s": -0.17450327512295843,
  "tail_fk_speed_mean_m_s": -0.17452389470891344,
  "peak_tilt_rad": 0.044885943580426524,
  "peak_wheel_torque_nm": 1.5756149291992188,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.940579005982727
}
```
