# tita_flash_sac_193248_068255_model_95000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "5ec74375d861563b6a882f426ef443c7058486b85355ccbf8b449ec5d5355a50",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.258266800287961,
  "max_drift_m": 7.258266800287961,
  "radial_IAE_m_s": 187.06386439955634,
  "signed_longitudinal_delta_m": -7.172854968021103,
  "tail_speed_mean_m_s": -0.15088474175927696,
  "tail_speed_rms_m_s": 0.15122742621473664,
  "tail_sensor_speed_mean_m_s": -0.15068679482794947,
  "tail_fk_speed_mean_m_s": -0.15070275851469403,
  "peak_tilt_rad": 0.07052339187331635,
  "peak_wheel_torque_nm": 1.4537074565887451,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.834524072008207
}
```
