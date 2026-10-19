# tita_flash_sac_115632_883848_model_40000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
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
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "baa210e664677078ddef8a5c884f2aac138a6d83f9628912c74385fe24461b89",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.090300576791374,
  "max_drift_m": 6.090300576791374,
  "radial_IAE_m_s": 191.74921081059034,
  "signed_longitudinal_delta_m": 4.414170178054312,
  "tail_speed_mean_m_s": 0.11206434773797483,
  "tail_speed_rms_m_s": 0.11206434776088499,
  "tail_sensor_speed_mean_m_s": 0.11199234541473313,
  "tail_fk_speed_mean_m_s": 0.11200934945456663,
  "peak_tilt_rad": 0.10854517159727983,
  "peak_wheel_torque_nm": 0.21975082159042358,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.192946030001622
}
```
