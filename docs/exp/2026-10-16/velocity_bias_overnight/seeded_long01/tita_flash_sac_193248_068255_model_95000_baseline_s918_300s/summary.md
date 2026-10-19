# tita_flash_sac_193248_068255_model_95000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
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
  "initial_physics_sha256": "6661f5839098126b9b6417b6e338eedc9f81d6081db34ffbe57205a83a133f18",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 13.712804294045677,
  "max_drift_m": 20.74165896601331,
  "radial_IAE_m_s": 3363.41826007932,
  "signed_longitudinal_delta_m": -12.20245023835271,
  "tail_speed_mean_m_s": -0.2858124173890294,
  "tail_speed_rms_m_s": 0.2858124173929856,
  "tail_sensor_speed_mean_m_s": -0.28541320011854704,
  "tail_fk_speed_mean_m_s": -0.2854685436612097,
  "peak_tilt_rad": 0.04488594214769237,
  "peak_wheel_torque_nm": 0.2235127091407776,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 18.901830621995032
}
```
