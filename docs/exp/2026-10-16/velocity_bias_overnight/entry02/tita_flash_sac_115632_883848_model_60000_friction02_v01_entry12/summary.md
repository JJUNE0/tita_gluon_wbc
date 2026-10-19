# tita_flash_sac_115632_883848_model_60000_friction02_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction02_v01_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "042d715eeb424d754f6b1f6385fcee516191294213e816fa94053ee7d66970c7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0026573976088628917,
  "max_drift_m": 0.007428889994225529,
  "radial_IAE_m_s": 0.20588987765354397,
  "signed_longitudinal_delta_m": 0.0025549534734743383,
  "tail_speed_mean_m_s": 6.742219082827093e-07,
  "tail_speed_rms_m_s": 6.762128701526458e-07,
  "tail_sensor_speed_mean_m_s": -3.4684056482776886e-05,
  "tail_fk_speed_mean_m_s": -6.139639632603485e-08,
  "peak_tilt_rad": 0.06149664847545666,
  "peak_wheel_torque_nm": 0.20464572310447693,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04234300704905114,
  "final_integral_m_s": 0.04234330655111556,
  "elapsed_wall_s": 5.085998049005866
}
```
