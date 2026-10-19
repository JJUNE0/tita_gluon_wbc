# tita_flash_sac_193248_068255_model_95000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "0f0275197a7023f41c60c2b0c7a7d6ddb4245a3716ec269693ed5da65da44e81",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 20.602550568095147,
  "max_drift_m": 20.602550568095147,
  "radial_IAE_m_s": 615.1116536353188,
  "signed_longitudinal_delta_m": -20.55045458655553,
  "tail_speed_mean_m_s": -0.3454802492420201,
  "tail_speed_rms_m_s": 0.3454802496032787,
  "tail_sensor_speed_mean_m_s": -0.3447544252429426,
  "tail_fk_speed_mean_m_s": -0.34475385639184203,
  "peak_tilt_rad": 0.06204698515073237,
  "peak_wheel_torque_nm": 0.5424095392227173,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.868661267042626
}
```
