# tita_flash_sac_193248_068255_model_95000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "d75dee25ee7f6ed348bf419046907d26ccdda1e736ecb5b554bf6801213f98df",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.885367245581753,
  "max_drift_m": 8.885367245581753,
  "radial_IAE_m_s": 262.1048906890115,
  "signed_longitudinal_delta_m": -8.691092325595369,
  "tail_speed_mean_m_s": -0.16732356266376433,
  "tail_speed_rms_m_s": 0.1680837434741975,
  "tail_sensor_speed_mean_m_s": -0.16710979097156226,
  "tail_fk_speed_mean_m_s": -0.16712888865628325,
  "peak_tilt_rad": 0.044872324240152084,
  "peak_wheel_torque_nm": 1.5768808126449585,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.613869388995226
}
```
