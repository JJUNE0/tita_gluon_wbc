# tita_flash_sac_115632_883848_model_60000_baseline_entry

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: FAIL

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "FAIL",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_baseline_entry",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 0.0,
    "seed": 272,
    "estimator": "fk",
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "72d010b3d1fa79251553f54fdf3c0d7dde3b25d889f42f3a2ef092efbbc33587",
  "complete": false,
  "failure": [
    "base_height_limit",
    "leg_joint_limit"
  ],
  "duration_s": 0.0,
  "final_drift_m": 0.0,
  "max_drift_m": 0.0,
  "radial_IAE_m_s": 0.0,
  "signed_longitudinal_delta_m": 0.0,
  "tail_speed_mean_m_s": null,
  "tail_speed_rms_m_s": null,
  "tail_sensor_speed_mean_m_s": null,
  "tail_fk_speed_mean_m_s": null,
  "peak_tilt_rad": 0.11992663034275308,
  "peak_wheel_torque_nm": 0.0,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 0.12266731500858441
}
```
