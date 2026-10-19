# tita_flash_sac_115632_883848_model_60000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "6eb69d875de8667dc3d86dec5f30e59f8860cc8bd9c4e7217141b346d14cfdc6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.051216589505071596,
  "max_drift_m": 0.05273739051776558,
  "radial_IAE_m_s": 2.202008956938647,
  "signed_longitudinal_delta_m": -0.051206825862619786,
  "tail_speed_mean_m_s": -0.00010486848547218459,
  "tail_speed_rms_m_s": 0.0002959250763389867,
  "tail_sensor_speed_mean_m_s": -0.00010483666462400608,
  "tail_fk_speed_mean_m_s": -0.00010263696906464518,
  "peak_tilt_rad": 0.06682015761560978,
  "peak_wheel_torque_nm": 0.14255166053771973,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.43032096105162
}
```
