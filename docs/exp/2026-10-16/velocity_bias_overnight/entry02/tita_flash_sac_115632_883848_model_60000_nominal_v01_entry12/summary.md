# tita_flash_sac_115632_883848_model_60000_nominal_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_nominal_v01_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "final_drift_m": 0.004454916033307205,
  "max_drift_m": 0.006702839673371237,
  "radial_IAE_m_s": 0.27602104002144323,
  "signed_longitudinal_delta_m": 0.0044396209415750515,
  "tail_speed_mean_m_s": -1.1213890154580215e-05,
  "tail_speed_rms_m_s": 1.1459591629945201e-05,
  "tail_sensor_speed_mean_m_s": -1.1259676735876449e-05,
  "tail_fk_speed_mean_m_s": -9.15580966922008e-06,
  "peak_tilt_rad": 0.0692900479944012,
  "peak_wheel_torque_nm": 0.21433603763580322,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04742847274564161,
  "final_integral_m_s": 0.047440734243073816,
  "elapsed_wall_s": 4.164124543953221
}
```
