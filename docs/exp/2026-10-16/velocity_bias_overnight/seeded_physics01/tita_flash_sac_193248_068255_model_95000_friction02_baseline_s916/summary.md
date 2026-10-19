# tita_flash_sac_193248_068255_model_95000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "ee968977b801042dc85a11db22db6abcbccb30936e5b773ff5f9d6bb23405bd8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.531151780417474,
  "max_drift_m": 4.531151780417474,
  "radial_IAE_m_s": 135.4692993579547,
  "signed_longitudinal_delta_m": -4.523581411284825,
  "tail_speed_mean_m_s": -0.07609009148268214,
  "tail_speed_rms_m_s": 0.07609018109220189,
  "tail_sensor_speed_mean_m_s": -0.07596416085383104,
  "tail_fk_speed_mean_m_s": -0.07596626684111976,
  "peak_tilt_rad": 0.04871573401098295,
  "peak_wheel_torque_nm": 0.2504569888114929,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.094352792017162
}
```
