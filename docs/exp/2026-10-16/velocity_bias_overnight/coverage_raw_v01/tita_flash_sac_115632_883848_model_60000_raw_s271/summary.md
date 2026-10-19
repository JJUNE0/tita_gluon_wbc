# tita_flash_sac_115632_883848_model_60000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_raw_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "5ef6fa3f00e36ec596faab257b839aab822ab1e04a3a2fd76ef8cf8597fc22dd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005795198468534878,
  "max_drift_m": 0.006175333537990141,
  "radial_IAE_m_s": 0.32622252241344785,
  "signed_longitudinal_delta_m": 0.005795138800143835,
  "tail_speed_mean_m_s": 5.321656095766911e-06,
  "tail_speed_rms_m_s": 0.002903388495863674,
  "tail_sensor_speed_mean_m_s": -3.85680216021911e-05,
  "tail_fk_speed_mean_m_s": -9.798239300183984e-06,
  "peak_tilt_rad": 0.06989710466915078,
  "peak_wheel_torque_nm": 0.8898304104804993,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.16199967376268362,
  "final_integral_m_s": 0.09883468629421355,
  "elapsed_wall_s": 4.357730559015181
}
```
