# tita_flash_sac_115632_883848_model_60000_nominal_baseline_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_nominal_baseline_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
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
  "initial_physics_sha256": "da0801102229951c083c96c8583f9099f7e3487cc41411cf1232290252a896fd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.9209299507793638,
  "max_drift_m": 0.9209299507793638,
  "radial_IAE_m_s": 27.38567790939404,
  "signed_longitudinal_delta_m": 0.920176750453567,
  "tail_speed_mean_m_s": 0.015726436874853297,
  "tail_speed_rms_m_s": 0.015728616594161193,
  "tail_sensor_speed_mean_m_s": 0.015692409318549195,
  "tail_fk_speed_mean_m_s": 0.015693801926282416,
  "peak_tilt_rad": 0.06981454330281389,
  "peak_wheel_torque_nm": 0.1521259844303131,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.242221715976484
}
```
