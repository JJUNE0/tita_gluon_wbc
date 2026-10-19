# tita_flash_sac_115632_883848_model_60000_friction02_baseline_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction02_baseline_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "042d715eeb424d754f6b1f6385fcee516191294213e816fa94053ee7d66970c7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.9448521642594717,
  "max_drift_m": 0.9448521642594717,
  "radial_IAE_m_s": 29.589739562918034,
  "signed_longitudinal_delta_m": 0.7239329658357461,
  "tail_speed_mean_m_s": 0.017105682386262186,
  "tail_speed_rms_m_s": 0.017105682538932004,
  "tail_sensor_speed_mean_m_s": 0.017054447888869326,
  "tail_fk_speed_mean_m_s": 0.01708622135881054,
  "peak_tilt_rad": 0.06156953769017903,
  "peak_wheel_torque_nm": 0.09811236709356308,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.0224786450271495
}
```
